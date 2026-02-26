# Task Management Guide

This guide  provides comprehensive instructions for **generating**, **deploying**, and **resetting** assessment tasks using the Utkrushta Infrastructure Assessment Agent.

## Environment Setup

### 1. Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
PORTKEY_API_KEY=your_portkey_api_key

# GitHub Configuration
GITHUB_UTKRUSHTAPPS_TOKEN=your_github_token
REPO_OWNER=your_github_organization

# Supabase Configuration (Development)
SUPABASE_URL_APTITUDETESTSDEV=your_supabase_dev_url
SUPABASE_API_KEY_APTITUDETESTSDEV=your_supabase_dev_key

# Supabase Configuration (Production)
SUPABASE_URL_APTITUDETESTS=your_supabase_prod_url
SUPABASE_API_KEY_APTITUDETESTS=your_supabase_prod_key

# DigitalOcean Configuration
DIGITALOCEAN_API_PAT=your_digitalocean_token
AVAILABLE_IPS=ip1,ip2,ip3  # Comma-separated droplet IPs

# SSH Configuration
SSH_PRIVATE_KEY_PATH=/path/to/your/private/key
```

### 2. File Dependencies

Ensure these files exist in your workspace:

**Required for Task Generation:**
- `competencies.json` - Competency definitions
- `background_for_tasks.json` - Background context
- `task_scenarios.json` - Real-world scenarios (optional)

**Required Files in Project:**
- `agents/infra_assessor/multiagent.py` - Main orchestrator
- `agents/infra_assessor/utils.py` - Utility functions
- `agents/infra_assessor/droplet_utils.py` - DigitalOcean operations
- `agents/infra_assessor/github_utils.py` - GitHub operations
- `agents/infra_assessor/evals.py` - Task evaluation logic
- `agents/infra_assessor/logger_config.py` - Logging configuration

---

## Task Generation

### Overview
Task generation creates intelligent assessment tasks based on competencies, background context, and real-world scenarios. The process uses LLM to generate task descriptions, code files, documentation, and solution guides.

### Step 1: Prepare Input Files

#### competencies.json
```json
[
  {
    "id": "comp_001",
    "competency_id": "comp_001",
    "name": "Python - FastAPI",
    "description": "API development with FastAPI framework",
    "scope": "Backend API development",
    "proficiency": "INTERMEDIATE"
  }
]
```

#### background_for_tasks.json
```json
{
  "organization": {
    "organization_background": "Tech startup focused on e-commerce solutions"
  },
  "role_context": "Backend Developer",
  "yoe": "3-5 years",
  "questions_prompt": "Focus on practical implementation scenarios"
}
```

#### task_scenarios.json (Optional)
```json
{
  "Python - FastAPI (INTERMEDIATE)": [
    "Build a REST API for user management",
    "Implement database integration with PostgreSQL",
    "Add authentication and authorization"
  ]
}
```

#### util.py

add the prompts imports from task_generation_prompts

#### task_generation_prompts

-Make sure to add the prompts for perticular competency to which you are making the task 
-Three prompt to include in that:
    -tech_stack__CONTEXT
    -tech_stack_INPUT_AND_ASK
    -tech_stack_INSTRUCTIONS

### Step 2: Run Task Generation

#### Command
```bash
cd agents/infra_assessor
python multiagent.py generate_tasks -c /path/to/competencies.json -b /path/to/background_for_tasks.json -s /path/to/task_scenarios.json
```

#### Command Options
- `-c, --competency-file`: Path to competencies JSON file (required)
- `-b, --background-file`: Path to background JSON file (required)
- `-s, --scenarios-file`: Path to scenarios JSON file (optional)

### Step 3: Generation Process

The system performs these steps automatically:

1. **Environment Validation** - Checks all required environment variables
2. **File Loading** - Reads and validates input files
3. **Scenario Loading** - Matches competencies with relevant scenarios
4. **LLM Task Generation** - Creates task description, requirements, and code
5. **Task Evaluation** - Validates task quality and difficulty
6. **GitHub Repository Creation** - Creates template and answer repositories
7. **File Upload** - Uploads generated code to GitHub
8. **Database Storage** - Stores task metadata in Supabase
9. **Local File Saving** - Saves files locally for reference

### Generated Outputs

- **GitHub Repository** - Contains starter code and README
- **Answer Repository** - Contains complete solution
- **Database Record** - Task metadata and evaluation results
- **Local Files** - Complete task package in `infra_assets/tasks/`

### Example Output
```
 INTELLIGENT TASK GENERATION AGENT
 Found 1 competencies:
   1. Python - FastAPI
 
 STEP 1: Creating Task(s)...
 Task Creation Successful!
 Task Type: Backend
 Task ID: 123
 Task Name: User Management API
 Competencies Covered: Python - FastAPI
 GitHub Repository: https://github.com/your-org/user-management-api
```

---

## Task Deployment

### Overview
Task deployment downloads code from GitHub repositories and deploys it to DigitalOcean droplets for assessment execution.

### Deployment Methods

#### Method 1: Deploy Specific Task by ID

Deploy a single task using its unique task ID.

**Command:**
```bash
python multiagent.py deploy_task --task-id 123 --droplet-ip 192.168.1.100
```

**Options:**
- `--task-id, -t`: Task ID to deploy (required)
- `--droplet-ip, -d`: Specific droplet IP (optional - auto-selects if not provided)

#### Method 2: Deploy All Tasks by Competency

Deploy all undeployed tasks for a specific competency.

**Command:**
```bash
python multiagent.py deploy_task --competency-id comp_001 --droplet-ip 192.168.1.100
```

**Options:**
- `--competency-id, -c`: Competency ID to deploy tasks for (required)
- `--droplet-ip, -d`: Specific droplet IP (optional)

#### Method 3: Auto-Deploy Multiple Tasks

Deploy multiple tasks across all available droplets.

**Command:**
```bash
python multiagent.py deploy_task --competency-id "comp_001,comp_002"
```

### Deployment Process

The system performs these steps for each task:

1. **Task Validation** - Verifies task exists and is not already deployed
2. **Droplet Selection** - Chooses available droplet (checks for running containers)
3. **Repository Download** - Downloads files from GitHub repository
4. **File Upload** - Uploads files to droplet via SSH/SFTP
5. **Script Execution** - Runs `run.sh` script on droplet
6. **Database Update** - Marks task as deployed with deployment info
7. **Cleanup** - Removes temporary local files

### Deployment Requirements

#### Droplet Requirements
- Linux-based DigitalOcean droplet
- Docker installed
- SSH access configured
- Root user access

#### Generated Files Expected
- `run.sh` - Deployment script
- `install.sh` - Installation script (optional)
- `README.md` - Task instructions
- Application code files

### Example Output
```
======================================================================
 TASK DEPLOYMENT AGENT - DEPLOY SPECIFIC TASK
    Find Task → Download Files → Upload to Droplet → Execute → Update DB
======================================================================
 Task ID: 123
 Droplet IP: Auto-select from available pool

 Searching for task with ID: 123
 Using specified droplet: 192.168.1.100
 Downloading files from GitHub repository...
 Files downloaded to: temp_deploy_123
 Uploading files to droplet: 192.168.1.100
 Files uploaded to droplet
 Executing run.sh script on droplet...
 run.sh executed successfully
 Database updated successfully

 DEPLOYMENT COMPLETED SUCCESSFULLY!
```

---

## Task Reset

### Overview
Task reset executes cleanup scripts on deployed tasks and marks them as undeployed in the database, allowing for redeployment.

### Reset Command

**Command:**
```bash
python multiagent.py reset_task --task-id 123 --droplet-ip 192.168.1.100 --script-path /root/task/kill.sh
```

### Required Parameters

- `--task-id, -t`: ID of the task to reset (required)
- `--droplet-ip, -d`: IP address of the droplet where task is deployed (required)
- `--script-path, -s`: Path to the reset script on the droplet (required)

### Reset Process

1. **Parameter Validation** - Validates all required parameters
2. **SSH Connection** - Connects to the specified droplet
3. **Script Execution** - Executes the specified reset script
4. **Database Update** - Marks task as undeployed, clears deployment info
5. **Status Report** - Reports success or failure

### Common Reset Scripts

#### kill.sh (Docker containers)
```bash
#!/bin/bash
# Stop and remove all Docker containers
docker stop $(docker ps -aq) 2>/dev/null || true
docker rm $(docker ps -aq) 2>/dev/null || true
docker system prune -f
```

#### cleanup.sh (Process cleanup)
```bash
#!/bin/bash
# Kill specific processes
pkill -f "your_application"
rm -rf /tmp/app_data
```

### Example Output
```
======================================================================
 TASK RESET AGENT - RESET AND UNDEPLOY TASK
    Execute Script → Update Database → Mark as Undeployed
======================================================================
 Task ID: 123
 Droplet IP: 192.168.1.100
 Script Path: /root/task/kill.sh

🔄 Executing reset script on droplet...
✅ Reset script executed successfully
🔄 Updating database to mark task as undeployed...
✅ Task successfully marked as undeployed in database

 RESET COMPLETED SUCCESSFULLY!
======================================================================
 Task has been reset and marked as undeployed.
 You can now redeploy this task if needed.
```

---

## Task Scenario Generation

### Overview

The Scenario Generator (`scenario_generator.py`) automatically creates realistic task scenarios for coding assessments. It takes a competency file as input and uses LLM to generate scenarios that match the format expected by the task generation pipeline. Generated scenarios are saved to the appropriate scenario JSON file for reuse.

### When to Use

- When adding a **new competency combination** that has no existing scenarios (e.g., `Golang (BASIC), Redis (BASIC)`)
- When you need to **expand the scenario pool** for an existing competency to increase task variety
- When onboarding a **new technology stack** into the assessment platform

### Input Files

The generator requires a **competency file** (same format used for task generation):

```json
[
  {
    "competency_id": "c9bd828d-...",
    "proficiency": "BASIC",
    "name": "Java",
    "scope": "A person with BASIC proficiency level in Java..."
  },
  {
    "competency_id": "50f5e386-...",
    "proficiency": "BASIC",
    "name": "Kafka",
    "scope": "A person with BASIC proficiency level in Kafka..."
  }
]
```

Optionally, a **background file** (`background_forQuestions_*.json`) can be provided for additional organizational context.

### How Scenario Keys Work

The generator constructs keys that match the format used in `task_scenarios.json`:
- **Single competency**: `"Java (BASIC)"`, `"ReactJs (BEGINNER)"`
- **Multi-competency**: competencies are sorted alphabetically and joined: `"Java (BASIC), Kafka (BASIC)"`
- The key format must match exactly for scenarios to be found by `load_relevant_scenarios()` during task generation

### Technology Categories

The generator classifies competencies into categories that determine the content focus of generated scenarios:

| Category | Competencies | Scenario Focus |
|----------|-------------|----------------|
| **BACKEND** | Java, Python, FastAPI, Go, Node.js, Express, Kafka, Redis, Docker | API endpoints, error handling, concurrency, data integrity |
| **FRONTEND** | ReactJs, React Native, NextJs, TypeScript | Components, state management, rendering, accessibility |
| **DATABASE** | SQL, PostgreSQL, MongoDB | Schema design, query optimization, transactions, indexes |
| **MIXED_STACK** | Any combination crossing categories | Integration patterns, data flow between layers |
| **NON_CODE** | Prompt Engineering, AI Literacy | LLM artifacts, evaluation datasets, prompt redesign |

### CLI Commands

#### Generate Scenarios (with auto-save)

```bash
python -m scenario_generator \
  --competency-file task_input_files/input_java/basic/input_java_kafka_basic_task/competency_java_kafka_basic_Utkrusht.json \
  --count 6 \
  --append
```

This generates 6 scenarios and appends them to the appropriate file (`task_scenarios.json` for BASIC, `task_scenarios_intermediate.json` for INTERMEDIATE, `task_sceanrio_no_code.json` for NON_CODE).

#### Generate with Explicit Output File

```bash
python -m scenario_generator \
  --competency-file path/to/competency.json \
  --count 4 \
  --output task_input_files/task_scenarios/task_scenarios.json \
  --append
```

#### Dry Run (Preview Only)

```bash
python -m scenario_generator \
  --competency-file path/to/competency.json \
  --count 3 \
  --dry-run
```

Prints generated scenarios to console without saving to any file.

#### With Background Context

```bash
python -m scenario_generator \
  --competency-file path/to/competency.json \
  --background-file path/to/background.json \
  --count 6 \
  --append
```

### CLI Options Reference

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--competency-file` | Yes | — | Path to competency JSON file |
| `--count` | No | 6 | Number of scenarios to generate |
| `--output` | No | Auto-detect | Output file path (auto-selects based on proficiency) |
| `--append` | No | False | Merge into existing file instead of overwriting |
| `--background-file` | No | None | Optional background JSON for additional context |
| `--dry-run` | No | False | Preview scenarios without saving |

### Quality Control Pipeline

The generator runs a three-step quality pipeline on every batch:

1. **Structural Validation** — Checks each scenario is 200-3000 characters, formatted as a narrative paragraph
2. **Deduplication** — Compares against all existing scenarios using text similarity (threshold: 0.6). Rejects scenarios too similar to existing ones
3. **LLM Evaluation** — Uses `gpt-5-nano` to check realism, complexity calibration, technical detail, completeness, and scope appropriateness

Failed scenarios are automatically regenerated (up to 2 retry attempts).

### Scenario Output Format

All generated scenarios (across all proficiency levels) follow the same three-section bold-header structure (4-5 lines total):

```
**Current Implementation:** [1-2 sentences describing the existing system, tech stack, and what is currently broken/slow/missing with specific technical details]

**Your Task:** [Clear deliverables describing what to fix/build/optimize, with bullet points for multiple items]

**Success Criteria:** [1-2 sentences describing the expected outcome with measurable targets]
```

Each scenario is stored as a separate string in the JSON array — never concatenate multiple scenarios into one entry.

### Output File Mapping

| Proficiency | Target File |
|-------------|-------------|
| BEGINNER | `task_input_files/task_scenarios/task_scenarios.json` |
| BASIC | `task_input_files/task_scenarios/task_scenarios.json` |
| INTERMEDIATE | `task_input_files/task_scenarios/task_scenarios_intermediate.json` |
| NON_CODE | `task_input_files/task_scenarios/task_sceanrio_no_code.json` |

### Example Workflow: Adding Scenarios for a New Competency

1. **Locate or create the competency file** in `task_input_files/`:
   ```bash
   ls task_input_files/input_java/basic/input_java_basic_task/competency_*.json
   ```

2. **Run the generator in dry-run mode** to preview:
   ```bash
   python -m scenario_generator \
     --competency-file task_input_files/input_java/basic/input_java_basic_task/competency_java_basic_Utkrusht.json \
     --count 4 \
     --dry-run
   ```

3. **Review the output** — check that scenarios are realistic, appropriately complex, and diverse

4. **Run again with `--append`** to save:
   ```bash
   python -m scenario_generator \
     --competency-file task_input_files/input_java/basic/input_java_basic_task/competency_java_basic_Utkrusht.json \
     --count 4 \
     --append
   ```

5. **Verify** by checking the scenario file:
   ```bash
   python -c "import json; d=json.load(open('task_input_files/task_scenarios/task_scenarios.json')); print(list(d.keys()))"
   ```

6. **Generate tasks** using the standard pipeline:
   ```bash
   python multiagent.py generate_tasks -c path/to/competency.json -b path/to/background.json -s task_input_files/task_scenarios/task_scenarios.json
   ```

### Files Involved

| File | Role |
|------|------|
| `scenario_generator/` | Package directory |
| `scenario_generator/__init__.py` | Package exports — `generate_scenarios_for_competencies`, `build_scenario_key`, etc. |
| `scenario_generator/__main__.py` | CLI entry point — run via `python -m scenario_generator` |
| `scenario_generator/generator.py` | Core logic — classification, LLM calls, validation, pipeline |
| `scenario_generator/prompts.py` | All LLM prompt templates for generation and evaluation |
| `utils.py` | Shared helpers: `build_scenario_key()`, `save_generated_scenarios()` |
| `task_input_files/task_scenarios/*.json` | Scenario storage files (output targets) |
