"""
Unified pipeline: generate input files + task scenarios in one command.

Chains generate_input_files and scenario_generator, passing data in-memory
between steps while still writing input files as a side effect.

When multiple proficiency levels are given, the full pipeline runs once per
level — all competencies are processed together at that level each time.

    --name "Pandas,Numpy" --proficiency BASIC,INTERMEDIATE --count 2

  → Run 1: Python - Pandas (BASIC) + Python - Numpy (BASIC)  → 2 scenarios
  → Run 2: Python - Pandas (INTERMEDIATE) + Python - Numpy (INTERMEDIATE) → 2 scenarios
"""

import os
import json
from pathlib import Path

import click

from generate_input_files.generator import (
    init_supabase,
    init_openai_client,
    fetch_competencies_from_db,
    generate_role_context,
    generate_questions_prompt,
    sanitize_folder_name,
    resolve_output_folder,
    write_json_safe,
    PROFICIENCY_YOE_MAP,
    HARDCODED_ORGANIZATION,
    MODEL as INPUT_GEN_MODEL,
)
from scenario_generator import (
    generate_scenarios_for_competencies,
    build_scenario_key,
    get_competency_names,
    get_target_scenario_file,
    save_generated_scenarios,
    format_cost_summary,
)

VALID_PROFICIENCIES = {"BEGINNER", "BASIC", "INTERMEDIATE", "ADVANCED"}


def _parse_multi_option(raw_values: tuple) -> list[str]:
    """Expand comma-separated multi-flag values into a flat list."""
    result = []
    for v in raw_values:
        parts = [p.strip() for p in v.split(",") if p.strip()]
        result.extend(parts)
    return result


def _run_single_proficiency(
    *,
    names: list[str],
    proficiency: str,
    count: int,
    append: bool,
    folder_name: str | None,
    force: bool,
    dry_run: bool,
    scenario_output: str | None,
    supabase,
    openai_client,
    global_usage: dict,
):
    """Run the full pipeline for all competencies at one proficiency level.

    Mutates `global_usage` in-place to accumulate token usage across runs.
    Returns number of scenarios generated.
    """

    def _track(model: str, usage: dict):
        if model not in global_usage:
            global_usage[model] = {"input_tokens": 0, "output_tokens": 0}
        global_usage[model]["input_tokens"] += usage["input_tokens"]
        global_usage[model]["output_tokens"] += usage["output_tokens"]

    # ── Step 1: Fetch competencies ──────────────────────────────────────
    click.echo(f"\n  Fetching from Supabase at {proficiency} level...")
    competency_data = []
    for comp_name in names:
        rows = fetch_competencies_from_db(supabase, comp_name, proficiency)
        click.echo(f"    Found {len(rows)} row(s) for '{comp_name}' ({proficiency}).")
        for c in rows:
            competency_data.append({
                "competency_id": c["competency_id"],
                "created_at": c["created_at"],
                "proficiency": c["proficiency"],
                "organization_id": c["organization_id"],
                "name": c["name"],
                "scope": c["scope"],
            })
    click.echo(f"    Total: {len(competency_data)} competency row(s).")

    # ── Step 2: Generate background via LLM ────────────────────────────
    yoe = PROFICIENCY_YOE_MAP.get(proficiency, "1-2")
    all_comp_names = [c["name"] for c in competency_data]
    combined_name = " & ".join(all_comp_names)
    combined_scope = "\n\n---\n\n".join(
        f"[{c['name']} ({c['proficiency']})]\n{c['scope']}" for c in competency_data
    )

    click.echo("  Generating background via LLM...")
    try:
        role_context, usage = generate_role_context(
            openai_client, combined_scope, combined_name, proficiency, yoe
        )
        _track(INPUT_GEN_MODEL, usage)
        click.echo("    role_context generated.")
    except Exception as e:
        click.echo(f"    WARNING: Failed to generate role_context: {e}. Using fallback.")
        role_context = (
            f"A software engineer with {yoe} years of experience in {combined_name} "
            f"is expected to work at the {proficiency} proficiency level."
        )

    try:
        questions_prompt, usage = generate_questions_prompt(
            openai_client, combined_scope, combined_name, proficiency, yoe
        )
        _track(INPUT_GEN_MODEL, usage)
        click.echo("    questions_prompt generated.")
    except Exception as e:
        click.echo(f"    WARNING: Failed to generate questions_prompt: {e}. Using fallback.")
        questions_prompt = (
            f"Please ensure the questions cover the key areas of {combined_name} "
            f"at the {proficiency} level as described in the competency scope."
        )

    background_data = {
        "organization": HARDCODED_ORGANIZATION,
        "role_context": role_context,
        "questions_prompt": questions_prompt,
        "yoe": yoe,
    }

    # ── Resolve & write input files ─────────────────────────────────────
    combined_slug_name = "_".join(n.lower() for n in names)
    tech_slug = sanitize_folder_name(combined_slug_name)
    level = proficiency.lower()
    output_dir = resolve_output_folder(tech_slug, level, folder_name)

    tech_short = tech_slug.replace("input_", "", 1)
    comp_filename = f"competency_{tech_short}_{level}_Utkrusht.json"
    bg_filename = f"background_forQuestions_utkrusht_{tech_short}_{level}.json"
    comp_path = output_dir / comp_filename
    bg_path = output_dir / bg_filename

    click.echo(f"  Output directory: {output_dir}")

    if dry_run:
        click.echo("  [DRY RUN] Skipping input file writes.")
        click.echo("  Competency JSON preview:")
        click.echo(json.dumps(competency_data, indent=2, ensure_ascii=False)[:800])
        click.echo("  Background JSON preview:")
        click.echo(json.dumps(background_data, indent=2, ensure_ascii=False)[:800])
    else:
        os.makedirs(output_dir, exist_ok=True)
        click.echo("  Writing input files...")
        write_json_safe(comp_path, competency_data, force)
        write_json_safe(bg_path, background_data, force)

    # ── Step 3: Generate scenarios ──────────────────────────────────────
    scenario_key = build_scenario_key(competency_data)
    target_file = Path(scenario_output) if scenario_output else get_target_scenario_file(competency_data)

    click.echo(f"  Scenario key:  {scenario_key}")
    click.echo(f"  Target file:   {target_file}")
    click.echo(f"  Generating {count} scenarios...")

    scenarios, scenario_usage = generate_scenarios_for_competencies(
        openai_client=openai_client,
        competencies=competency_data,
        count=count,
        background=background_data,
    )
    for model, usage in scenario_usage.items():
        _track(model, usage)

    if not scenarios:
        click.echo("  WARNING: No scenarios were generated for this run.", err=True)
        return 0

    # Display
    click.echo(f"\n  {'='*66}")
    click.echo(f"  Generated {len(scenarios)} scenarios for: {scenario_key}")
    click.echo(f"  {'='*66}")
    for i, s in enumerate(scenarios, 1):
        click.echo(f"\n  --- Scenario {i} ---")
        click.echo(f"  {s}")

    # Save
    if not dry_run:
        save_generated_scenarios(scenarios, scenario_key, target_file, append=append)
        click.echo(f"\n  Saved to: {target_file} (key: '{scenario_key}', append={append})")
    else:
        click.echo("\n  [DRY RUN] Scenarios not saved.")

    return len(scenarios)


@click.command()
@click.option(
    "--name", "-n", required=True, multiple=True,
    help='Competency name(s). Comma-separated or multiple flags: --name "Pandas,Numpy"',
)
@click.option(
    "--proficiency", "-p", required=True, multiple=True,
    help=(
        "Proficiency level(s): BEGINNER | BASIC | INTERMEDIATE | ADVANCED. "
        "Comma-separated or multiple flags. "
        "Each level runs the full pipeline for ALL competencies at that level."
    ),
)
@click.option(
    "--count", "-c", default=6, type=int,
    help="Number of scenarios to generate per proficiency run (default: 6)",
)
@click.option(
    "--append", is_flag=True, default=False,
    help="Append/merge into existing scenario file instead of overwriting",
)
@click.option(
    "--folder-name", "-f", default=None,
    help="Override the auto-generated input files subfolder name",
)
@click.option(
    "--force", is_flag=True, default=False,
    help="Overwrite existing input files",
)
@click.option(
    "--dry-run", is_flag=True, default=False,
    help="Skip all file writes; LLM calls still run and output is previewed",
)
@click.option(
    "--env", default="prod",
    type=click.Choice(["dev", "prod"]),
    help="Supabase environment (default: prod)",
)
@click.option(
    "--scenario-output", default=None,
    type=click.Path(),
    help="Override scenario output file path",
)
def run_pipeline(name, proficiency, count, append, folder_name, force, dry_run, env, scenario_output):
    """Unified pipeline: generate input files + task scenarios in one command.

    \b
    Single proficiency — all competencies at BASIC:
        python -m pipeline --name "Java, Kafka" --proficiency BASIC --count 6 --append

    Multiple proficiencies — runs the full pipeline once per level:
        python -m pipeline --name "Pandas,Numpy" --proficiency BASIC,INTERMEDIATE --count 2

        Run 1: Python - Pandas (BASIC)  + Python - Numpy (BASIC)  → 2 scenarios
        Run 2: Python - Pandas (INTERMEDIATE) + Python - Numpy (INTERMEDIATE) → 2 scenarios

    Multiple flags form:
        python -m pipeline --name "Pandas" --name "Numpy" \\
                           --proficiency BASIC --proficiency INTERMEDIATE --count 2
    """
    # ── Parse names ─────────────────────────────────────────────────────
    names = _parse_multi_option(name)

    # ── Parse & validate proficiencies ──────────────────────────────────
    proficiencies = _parse_multi_option(proficiency)
    proficiencies = [p.upper() for p in proficiencies]

    invalid = [p for p in proficiencies if p not in VALID_PROFICIENCIES]
    if invalid:
        raise click.ClickException(
            f"Invalid proficiency value(s): {invalid}. "
            f"Allowed: {sorted(VALID_PROFICIENCIES)}"
        )

    # ── Header ──────────────────────────────────────────────────────────
    click.echo(f"\n{'='*70}")
    click.echo("  UNIFIED PIPELINE: Input Files + Scenario Generation")
    click.echo(f"{'='*70}")
    click.echo(f"\nCompetencies:   {', '.join(names)}")
    click.echo(f"Proficiencies:  {', '.join(proficiencies)}")
    click.echo(f"Scenarios/run:  {count}")
    click.echo(f"Total runs:     {len(proficiencies)}")
    click.echo(f"Environment:    {env}")
    if dry_run:
        click.echo("Mode:           DRY RUN (no files will be written)")

    # ── Init shared clients ─────────────────────────────────────────────
    supabase = init_supabase(env)
    click.echo("\nConnected to Supabase.")
    openai_client = init_openai_client()

    # Unified usage accumulator across all runs
    global_usage: dict = {}
    total_generated = 0

    # ── Run pipeline once per proficiency level ─────────────────────────
    for run_idx, prof in enumerate(proficiencies, 1):
        click.echo(f"\n{'─'*70}")
        click.echo(f"  RUN {run_idx}/{len(proficiencies)}: {', '.join(names)} at {prof}")
        click.echo(f"{'─'*70}")

        generated = _run_single_proficiency(
            names=names,
            proficiency=prof,
            count=count,
            append=append,
            folder_name=folder_name,
            force=force,
            dry_run=dry_run,
            scenario_output=scenario_output,
            supabase=supabase,
            openai_client=openai_client,
            global_usage=global_usage,
        )
        total_generated += generated

    # ── Unified cost summary across all runs ────────────────────────────
    click.echo(f"\n{'='*70}")
    click.echo(format_cost_summary(global_usage))
    click.echo(f"{'='*70}")

    runs_label = f"{len(proficiencies)} run(s)" if len(proficiencies) > 1 else "1 run"
    click.echo(f"\nDone. {total_generated} scenario(s) generated across {runs_label}.")
