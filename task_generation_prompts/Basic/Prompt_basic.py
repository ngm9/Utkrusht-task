PROMPT_CONTEXT = """
Let me provide you with some context about the company and role:

Company Context:
{organization_background}

Roles and Responsibilities:
{role_context}

Based on this information, could you summarize what you understand about the company and role requirements?
"""

PROMPT_PROMPT_ENGINEERING_INPUT_AND_ASK = """
# GOAL:
As a senior product manager expert in Prompt Engineering for contact-center AI applications, you are given competency levels, role context, and real-world scenarios. 
Your job is to generate an entire task definition that can be effectively used to assess the candidate's ability to analyze data, design prompts, optimize performance, and document solutions for contact-center use cases.

Now that you've seen the instructions and examples, you are ready to generate a task definition for Prompt Engineering given the following inputs:

INPUT COMPETENCIES:
{competencies}

INPUT ROLE CONTEXT: 
{role_context}

INPUT REAL-WORLD SCENARIOS FOR TASK INSPIRATION:
{real_world_task_scenarios}


Can you now generate a task definition for Prompt Engineering given the above inputs, following the instructions given above? 
Use the following prompt to narrow down your response: 
{question_prompt}

RESPOND ONLY WITH VALID JSON - NO MARKDOWN OR EXPLANATIONS.
"""

PROMPT_INSTRUCTIONS = """

## GOAL
As a senior AI product manager expert in Prompt Engineering for contact-center and enterprise AI applications, you are tasked with generating comprehensive assessment scenarios that evaluate candidates' ability to design, optimize, analyze, and maintain production-grade AI solutions. Your generated tasks must assess AI literacy through practical work with flows, prompts, evaluations, and safety considerations while demonstrating high agency and AI tinkering capabilities suitable for presentation to CTOs and technical leadership.

## CRITICAL SUCCESS CRITERIA
The generated tasks MUST validate the following competencies:
1. **AI Literacy**: Deep understanding of LLM behavior, prompt mechanics, and model limitations
2. **Flow Design**: Ability to architect multi-step AI workflows and decision trees
3. **Prompt Engineering**: Crafting effective, production-ready prompts with proper structure
4. **Evaluation Frameworks**: Designing robust testing and quality measurement systems
5. **Safety & Governance**: Implementing guardrails, PII protection, and ethical AI practices
6. **High Agency/AI Tinkering**: Experimental mindset, rapid prototyping, and iterative optimization
7. **Executive Communication**: Clear data presentation suitable for CPTO-level stakeholders

## INSTRUCTIONS

### Nature of the Task
- **Task must present a business problem** derived from the provided `real_world_task_scenarios` with data files (CSV, JSON, prompts, logs, configs) that candidates will directly work with
- **The scenario must provide actual operational data files** that candidates will analyze, diagnose, and use to inform their AI solution approach
- **Candidates should create deliverable documents** (Word/PDF/Markdown) containing:
  - Problem diagnosis and root cause analysis
  - AI solution architecture and flow improvements
  - Prompt redesigns with reasoning and iterations
  - Evaluation framework or data analysis with metrics
  - Safety/bias considerations and remediation plans
  - Executive summary suitable for CPTO presentation
- **CRITICAL**: Include ONLY the raw data files that candidates need to analyze - NO templates, NO examples, NO explanatory materials
- **DO NOT GIVE AWAY THE SOLUTION** in the starter materials
- The task must require candidates to demonstrate AI tinkering, diagnose problems, test different approaches, and document their investigation process
- Focus on real-world enterprise AI challenges that require sophisticated analysis, prompt engineering, and strategic thinking
- **Time Constraint**: The task must be designed in such a way that candidates can complete the entire task within {minutes_range} minutes


**Your job**: Transform the provided scenarios into complete tasks by generating ONLY the exact data files that are explicitly requested in the scenarios (prompt files, CSVs, logs, configs, PDFs). **DO NOT generate any additional files that are not mentioned in the scenarios.**

### Proficiency Level Alignment
- **The complexity** of the task must align precisely with the proficiency level while assuming candidates will use AI tools:
  - **BEGINNER/BASIC**: Single-file analysis, obvious issues, straightforward fixes, basic metrics, simple documentation
  - **INTERMEDIATE**: Multi-file systems, pattern identification across data, comparative analysis, root cause diagnosis, CPTO-level summaries (THIS IS THE PRIMARY TARGET LEVEL)
  - **ADVANCED**: Complex multi-step flows, statistical analysis, comprehensive remediation strategies, scalability considerations
  - **EXPERT**: Multi-model orchestration, production optimization at scale, organizational governance frameworks, strategic architecture
- **The question must NOT include hints** - hints will be provided separately in the "hints" field
- Ensure scenarios reflect current AI best practices and realistic enterprise challenges

### AI and External Resource Policy
- **Candidates are ENCOURAGED to use AI tools** including ChatGPT, Claude, LLM playgrounds, and any external resources
- **Tasks are designed to assess** genuine AI engineering judgment, diagnostic thinking, systematic analysis, and ability to critique and improve AI systems
- **Complexity should require** understanding of model behavior nuances, evaluation design skills, problem-solving, and strategic thinking beyond simple prompt copying
- Evaluation should focus on the quality of diagnosis, reasoning, testing methodology, and executive communication rather than memorization

### Task Generation Requirements
Based on the provided `real_world_task_scenarios` , create a Prompt task that:
- **GENERATES DATA FILES** that perfectly match the scenario context and challenges described in the provided scenarios
- **INCLUDES ONLY RAW DATA FILES** in the `code_files` output - NO templates, NO examples, NO explanatory guides
- **CRITICAL**: Generate ONLY the files that are explicitly mentioned or required in the scenarios. Do NOT create additional files that are not requested.
- Creates realistic operational data that demonstrates:
  - The specific AI challenges mentioned in the scenario (flaws, bias, bottlenecks, inconsistencies)
  - Realistic patterns, edge cases, and quality issues
  - Sufficient complexity to require analysis and diagnosis
  - Business context embedded in the data itself
- Creates realistic business context that explains why this AI solution is critical and what success looks like
- Requires candidates to:
  - Diagnose and analyze the provided data files
  - Identify root causes of AI system issues
  - Design or redesign AI flows, prompts, and guardrails
  - Analyze metrics and patterns systematically
  - Address safety, bias, and performance considerations
  - Prepare executive-level summary with actionable recommendations
- Matches complexity to proficiency level (primarily INTERMEDIATE) while assuming AI tool usage
- **Time constraints**: The task must be designed in such a way that candidates can complete the entire task within {minutes_range} minutes
- Emphasizes high-agency investigation, experimentation documentation, and data-driven decision making

---


## REQUIRED OUTPUT JSON STRUCTURE

{{
   "name": "Task Name (focused on AI challenge from scenario) - MUST be in format <verb><subject> and maximum 50 characters. Example: 'Analyze LLM Performance' or 'Optimize Prompt Workflow'",
   "question": "A short description of the task scenario including the specific ask from the candidate — what needs to be fixed/implemented?",
   "code_files": {{
      "data/[relevant_dataset_file]": "[ACTUAL raw data content generated based on real-world task scenarios – CSV with eval logs, JSON config files, TXT prompt files, log entries, etc. – typically 20–60 rows/entries showing realistic patterns and issues, small enough to inspect within a few minutes]",
      "data/[additional_file]": "[Additional data file ONLY if the scenario requires multiple files – e.g., multiple prompt files in a flow, database query results, A/B test metrics, etc.]",   
      "prompts/[prompt_file].txt": "[ONLY if scenario involves prompt files – actual prompt content with embedded flaws or issues to diagnose, kept reasonably short and readable within the time constraint]",
      "config/[config_file].json": "[ONLY if scenario involves configuration – actual config with parameters that may need optimization, limited in size to what can be read in a few minutes]",
      "logs/[log_file].csv": "[ONLY if scenario involves system logs – actual log entries with timestamps, errors, latency, token usage, etc., with a manageable number of rows]"

      [NOTE: Include ONLY the files that are explicitly mentioned or required in the scenarios. NO templates, NO examples, NO explanatory guides, NO additional files beyond what the scenarios specify. NO README.md unless explicitly requested in the scenario.]
   }},
   "outcomes": "A very short description (1–2 sentences) of what tangible deliverables should exist if the task is completed well, without revealing the solution. For example: a clear problem diagnosis, a set of improved prompts/flows or configs, basic metrics or observations from the data, and a short executive-style summary tying changes to business impact.",
   "pre_requisites": "List Bullet-points required for knowledge and tools for the task:\\n- Access to LLM playground (ChatGPT, Claude, or similar) for prompt testing\\n- Basic data analysis skills (CSV/JSON handling, spreadsheet tools or Python)\\n- Understanding of prompt engineering and AI system design fundamentals\\n- Documentation tools (Word/Markdown editor)\\n- Ability to query/filter data and identify patterns\\n- Critical thinking for root cause analysis",
   "answer": "Only a high-level solution approach.
   "hints": "A single guiding hint that nudges toward good diagnostic or analytical practices without revealing the solution. Example: 'Start by examining patterns in the failure cases – what do they have in common that successful cases don't?' or 'Consider how the multi-step flow might be creating cascading errors from early stages.'",
   "definitions": {{
      "terminology_1": "definition_1 (AI/ML focused terms relevant to the scenario)",
      "terminology_2": "definition_2 (Prompt engineering concepts)",
      "terminology_3": "definition_3 (Evaluation metrics or system design concepts)"
   }}
}}


"""