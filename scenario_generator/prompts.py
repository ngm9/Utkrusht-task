"""
Prompt templates for the Task Scenario Generator.

All prompts used by scenario_generator.py for generating and evaluating
task scenarios across different technology categories and proficiency levels.
"""

# ============================================================================
# SYSTEM PROMPT
# ============================================================================

SCENARIO_SYSTEM_PROMPT = """You are a senior technical architect with 15+ years of experience designing coding assessments for engineering hiring. You create realistic, workplace-derived task scenarios that test specific competencies at precise proficiency levels. Your scenarios read like real bug reports, incident tickets, or feature requests from production systems at real companies."""


# ============================================================================
# GENERATION PROMPT — CODING SCENARIOS
# ============================================================================

SCENARIO_GENERATION_PROMPT = """Generate exactly {count} task scenarios for a coding assessment platform.

COMPETENCIES TO TEST:
{competencies_with_scopes}

PROFICIENCY LEVEL: {proficiency}
Complexity calibration (STRICTLY follow the time range — the scenario must be completable within the specified duration):
- BEGINNER (0-1 yoe): One clear bug or one simple feature. Single concept. The candidate MUST be able to complete the task in 20-30 minutes.
- BASIC (1-2 yoe): Feature implementation or multi-symptom debugging. 2-3 concepts combined. The candidate MUST be able to complete the task in 20-30 minutes.
- INTERMEDIATE (3-5 yoe): System optimization, performance tuning, or architectural improvement. 4+ concepts. The candidate MUST be able to complete the task in 30-40 minutes.

TECHNOLOGY CATEGORY: {tech_category}

FORMAT RULES (apply to ALL proficiency levels):
Each scenario MUST follow this exact three-section structure with bold markdown headers:

**Current Implementation:** [1-2 sentences describing the existing system, tech stack, and what is currently broken/slow/missing with specific technical details like endpoint paths, error messages, metrics]

**Your Task:** [Clear deliverables describing what to fix/build/optimize. Use bullet points for multiple items. Be specific about endpoints, functions, configurations to change]

**Success Criteria:** [1-2 sentences describing the expected outcome after the task is completed, with measurable targets where applicable]

IMPORTANT FORMAT CONSTRAINTS:
- Each scenario MUST be 4-5 lines total (compact, not verbose)
- Each scenario MUST be a SEPARATE string in the JSON array — NEVER concatenate multiple scenarios into one string
- Include specific technical details: table names, endpoint paths, error messages, response times, row counts, configuration values
- Use the exact bold headers shown above: **Current Implementation:**, **Your Task:**, **Success Criteria:**

{content_focus_block}

QUALITY RULES:
- Each scenario MUST use a DIFFERENT business domain (choose from: fintech, healthcare, logistics, e-commerce, SaaS, edtech, travel, food delivery, IoT, media/streaming, HR/recruiting, real estate)
- Each scenario MUST test a DIFFERENT primary skill from the competency scope provided above
- Include realistic metrics: response times in milliseconds, row counts, error rates, memory usage, throughput numbers
- Reference real libraries, tools, and frameworks by their actual names (e.g., Jedis, asyncpg, React.memo, psycopg2, express.json())
- Every scenario must have a clear "current broken/incomplete state" and a "target fixed/complete state"
- Do NOT create toy examples or tutorial-style exercises — scenarios must feel like real production issues

{deduplication_block}

{eval_feedback_block}

OUTPUT FORMAT:
Return ONLY a JSON object with a single key "scenarios" containing an array of exactly {count} scenario strings. No other text, no markdown, no explanation.
"""

# ============================================================================
# EVAL FEEDBACK BLOCK — passed to retry generation with failure reasons
# ============================================================================

EVAL_FEEDBACK_BLOCK = """PREVIOUS EVALUATION FEEDBACK — AVOID THESE ISSUES:
The following scenarios were rejected in the previous attempt. Learn from these failure reasons and ensure your new scenarios do NOT have the same problems:

{eval_feedback_text}

Fix these specific issues in your new scenarios."""

EVAL_FEEDBACK_BLOCK_EMPTY = ""


# ============================================================================
# CONTENT FOCUS BLOCKS — by technology category
# ============================================================================

CONTENT_FOCUS_BACKEND = """CONTENT FOCUS (BACKEND):
Your scenarios should emphasize:
- API correctness: specific endpoint paths (e.g., POST /api/orders), HTTP methods, request/response payloads, status codes (400, 404, 409, 500, 503)
- Error handling: try-catch patterns, retry logic, circuit breakers, graceful degradation, fallback mechanisms
- Concurrency: thread safety, race conditions, deadlocks, connection pool sizing (min/max connections), thread pool configuration
- Data integrity: transaction management, idempotency keys, duplicate detection, eventual consistency
- Performance: response time targets (e.g., "currently 3s, target <500ms"), throughput (requests/sec), batch processing, async patterns
- Configuration issues: incorrect property values, missing serializers, wrong connection strings, misconfigured timeouts"""

CONTENT_FOCUS_FRONTEND = """CONTENT FOCUS (FRONTEND):
Your scenarios should emphasize:
- Component patterns: controlled vs uncontrolled components, component composition, prop drilling, render props, HOCs
- State management: useState, useReducer, Context API, Redux, Zustand — when state is stale, not updating, or causing cascading re-renders
- Rendering performance: unnecessary re-renders (measurable counts), React.memo, useMemo, useCallback, virtualization for long lists
- Accessibility: missing ARIA attributes, keyboard navigation, screen reader support, focus management, color contrast
- Event handling: event propagation, cleanup in useEffect, memory leaks from unremoved listeners, debouncing/throttling
- UI bugs: conditional rendering errors, key prop issues in lists, stale closures, race conditions in async state updates"""

CONTENT_FOCUS_DATABASE = """CONTENT FOCUS (DATABASE):
Your scenarios should emphasize:
- Schema design: table structures with specific column names and types, primary/foreign key relationships, constraints (UNIQUE, CHECK, NOT NULL)
- Query optimization: slow queries with EXPLAIN ANALYZE output, sequential scans vs index scans, missing indexes, composite indexes
- Transactions: ACID compliance, isolation levels, deadlocks, savepoints, advisory locks
- Data integrity: orphan rows, constraint violations, referential integrity, data migration issues
- Performance tuning: connection pooling, VACUUM ANALYZE, table bloat, partitioning, query planner statistics
- Specific SQL patterns: JOINs (INNER, LEFT, CROSS), CTEs, window functions (ROW_NUMBER, RANK, SUM OVER), subqueries, GROUP BY with aggregates"""

CONTENT_FOCUS_MIXED_STACK = """CONTENT FOCUS (MIXED STACK / INTEGRATION):
Your scenarios should emphasize BOTH the API layer AND the data/storage layer:
- End-to-end data flow: how data moves from HTTP request through business logic to database/cache and back
- Connection management: database connection pools in the application layer, async drivers vs sync drivers, connection leaks
- Caching patterns: cache-aside, read-through, write-through with specific TTL values, cache invalidation on writes
- Async patterns: async/await in the API framework paired with async database drivers, background tasks
- Error propagation: how database errors (constraint violations, timeouts, connection failures) should surface as proper HTTP responses
- Schema-API alignment: Pydantic/DTO models matching database schemas, serialization issues, N+1 query problems in ORM usage"""


# ============================================================================
# CONTENT FOCUS BLOCK — NON-CODE SCENARIOS
# ============================================================================

CONTENT_FOCUS_NON_CODE = """CONTENT FOCUS (NON-CODE / AI & PROMPT ENGINEERING):
Your scenarios should emphasize:
- Realistic AI/LLM artifacts: call transcripts, prompt-flow configurations, evaluation datasets, A/B test results, model output logs
- Concrete deliverables: data extraction schemas, bias audit reports, prompt redesigns, executive summaries, remediation plans
- Real-world domains: B2B sales, customer support, content moderation, internal tooling, compliance, voice bots
- Include sample data: provide example transcripts, data snippets, or configuration excerpts within the scenario
- Evaluation criteria: latency metrics, accuracy scores, safety labels, cost per request, user satisfaction scores
- Organizational context: frame scenarios as requests from product managers, CPTOs, or business stakeholders

FORMAT NOTE FOR NON-CODE: Use the same three-section bold-header structure (**Current Implementation:**, **Your Task:**, **Success Criteria:**). Keep scenarios to 4-5 lines. Include brief references to artifacts within the sections rather than embedding full samples."""


# ============================================================================
# DEDUPLICATION BLOCK TEMPLATE
# ============================================================================

DEDUPLICATION_BLOCK = """EXISTING SCENARIOS — DO NOT DUPLICATE OR CLOSELY RESEMBLE THESE:
{existing_scenarios_text}

Each generated scenario must be substantially different from ALL of the above in terms of:
- Business domain (use a different industry/company type)
- Primary technical problem (address a different bug/feature/optimization)
- Technical approach (don't repeat the same fix pattern)"""

DEDUPLICATION_BLOCK_EMPTY = """No existing scenarios found for this competency combination. Generate fresh, diverse scenarios."""


# ============================================================================
# SCENARIO EVALUATION PROMPT
# ============================================================================

SCENARIO_EVAL_PROMPT = """Evaluate these generated task scenarios for a {proficiency}-level {tech_stack} coding assessment.

SCENARIOS:
{scenarios_numbered}

COMPETENCY SCOPE (what the candidate should know):
{scope_text}

Evaluate EACH scenario against these criteria:
1. REALISM: Does it describe a plausible workplace problem? (not a toy/tutorial example)
2. COMPLEXITY: Is the difficulty appropriate for {proficiency} level? (not too easy, not too hard)
3. DETAIL: Does it include specific technical details (endpoint paths, table names, error codes, metrics)?
4. COMPLETENESS: Does it clearly describe both the current broken/incomplete state AND the target fixed/complete state?
5. SCOPE: Can a competent {proficiency}-level developer complete this within the expected time range? (BEGINNER/BASIC: 20-30 minutes, INTERMEDIATE: 30-40 minutes)

For each scenario, return pass or fail with a brief reason if failing."""


# ============================================================================
# STRUCTURED OUTPUT SCHEMAS
# ============================================================================

SCENARIO_GENERATION_SCHEMA = {
    "name": "scenario_generation_response",
    "schema": {
        "type": "object",
        "properties": {
            "scenarios": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Array of generated task scenario strings"
            }
        },
        "required": ["scenarios"],
        "additionalProperties": False
    },
    "strict": True
}

SCENARIO_EVAL_SCHEMA = {
    "name": "scenario_eval_response",
    "schema": {
        "type": "object",
        "properties": {
            "evaluations": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "scenario_index": {
                            "type": "number",
                            "description": "0-based index of the scenario being evaluated"
                        },
                        "pass": {
                            "type": "boolean",
                            "description": "Whether the scenario passed all criteria"
                        },
                        "reason": {
                            "type": "string",
                            "description": "Brief reason if the scenario failed, empty string if passed"
                        }
                    },
                    "required": ["scenario_index", "pass", "reason"],
                    "additionalProperties": False
                },
                "description": "Evaluation result for each scenario"
            }
        },
        "required": ["evaluations"],
        "additionalProperties": False
    },
    "strict": True
}


def get_content_focus_block(tech_category: str) -> str:
    """Return the appropriate content focus block for the given technology category."""
    blocks = {
        "BACKEND": CONTENT_FOCUS_BACKEND,
        "FRONTEND": CONTENT_FOCUS_FRONTEND,
        "DATABASE": CONTENT_FOCUS_DATABASE,
        "MIXED_STACK": CONTENT_FOCUS_MIXED_STACK,
        "NON_CODE": CONTENT_FOCUS_NON_CODE,
    }
    return blocks.get(tech_category, CONTENT_FOCUS_BACKEND)


def build_generation_prompt(
    competencies_with_scopes: str,
    proficiency: str,
    tech_category: str,
    count: int,
    existing_scenarios: list,
    eval_feedback: list = None,
) -> str:
    """Build the complete generation prompt with all conditional sections filled in.

    Args:
        eval_feedback: Optional list of dicts with 'scenario' and 'reason' keys from
                       previous evaluation failures, so the LLM can avoid the same mistakes.
    """
    content_focus = get_content_focus_block(tech_category)

    if existing_scenarios:
        numbered = "\n".join(
            f"{i+1}. {s[:300]}{'...' if len(s) > 300 else ''}"
            for i, s in enumerate(existing_scenarios)
        )
        dedup_block = DEDUPLICATION_BLOCK.format(existing_scenarios_text=numbered)
    else:
        dedup_block = DEDUPLICATION_BLOCK_EMPTY

    if eval_feedback:
        feedback_lines = []
        for i, fb in enumerate(eval_feedback, 1):
            feedback_lines.append(
                f"{i}. Rejected scenario: \"{fb['scenario'][:200]}...\"\n   Reason: {fb['reason']}"
            )
        feedback_block = EVAL_FEEDBACK_BLOCK.format(
            eval_feedback_text="\n\n".join(feedback_lines)
        )
    else:
        feedback_block = EVAL_FEEDBACK_BLOCK_EMPTY

    return SCENARIO_GENERATION_PROMPT.format(
        count=count,
        competencies_with_scopes=competencies_with_scopes,
        proficiency=proficiency,
        tech_category=tech_category,
        content_focus_block=content_focus,
        deduplication_block=dedup_block,
        eval_feedback_block=feedback_block,
    )


def build_eval_prompt(
    scenarios: list,
    proficiency: str,
    tech_stack: str,
    scope_text: str
) -> str:
    """Build the evaluation prompt for generated scenarios."""
    numbered = "\n".join(
        f"Scenario {i+1}:\n{s}\n"
        for i, s in enumerate(scenarios)
    )
    return SCENARIO_EVAL_PROMPT.format(
        proficiency=proficiency,
        tech_stack=tech_stack,
        scenarios_numbered=numbered,
        scope_text=scope_text,
    )
