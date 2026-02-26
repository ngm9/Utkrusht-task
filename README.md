# Utkrushta - Task Generation & Deployment System

An automated system for generating, evaluating, deploying, and managing technical assessment tasks. It uses LLMs (OpenAI) to generate realistic coding challenges across 15+ technology stacks, deploys them to DigitalOcean droplets, and manages the full lifecycle via GitHub and Supabase.

## Features

- **AI-Powered Task Generation** — Generates assessment tasks with code using OpenAI's Responses API with reasoning, based on competencies and real-world scenarios
- **LLM Evaluation** — Automatically evaluates generated tasks and code for quality, difficulty, and realism
- **Multi-Stack Support** — Supports Python, Java, Go, Node.js, React, SQL, PostgreSQL, FastAPI, Spring Boot, Docker, Redis, MongoDB, RAG pipelines, and more
- **Proficiency Levels** — Beginner, Basic, Intermediate prompt libraries for each technology
- **GitHub Integration** — Creates template and answer repositories, batch file uploads, and GitHub Gists for task distribution
- **DigitalOcean Deployment** — Deploys tasks to droplets via SSH/SFTP with automated script execution
- **Supabase Storage** — Stores task metadata in dev and production databases
- **Non-Technical Flow** — Separate pipeline for AI/ML assessment challenges
- **Gist Management** — CLI tools for creating, syncing, and managing GitHub Gists across environments

## Project Structure

```
Utkrushta_task/
├── multiagent.py                 # Main orchestrator (generate, deploy, reset)
├── utils.py                      # Core utilities for task generation & processing
├── evals.py                      # LLM-based task & code evaluations
├── schemas.py                    # JSON schema definitions for structured outputs
├── droplet_utils.py              # DigitalOcean droplet management & SSH operations
├── github_utils.py               # GitHub repository & template management
├── gist_manager.py               # GitHub Gist lifecycle management CLI
├── logger_config.py              # Centralized logging configuration
├── TASK_MANAGEMENT_GUIDE.md      # Detailed usage guide
│
├── non_tech_flow/                # Non-technical AI/ML assessment flow
│   ├── non_tech_multiagent.py
│   ├── models.py
│   ├── non_tech_utils.py
│   └── non_tech_evals.py
│
├── task_generation_prompts/      # Technology-specific prompt templates
│   ├── Basic/                    # Basic-level prompts
│   ├── Intermediate/             # Intermediate-level prompts
│   └── Beginner/                 # Beginner-level prompts
│
├── task_input_files/             # Input JSON files (competencies, scenarios)
│   ├── input_python/
│   ├── input_java/
│   ├── input_react_task/
│   ├── input_sql_task/
│   ├── task_scenarios/
│   └── ...
│
├── requirements.txt
└── .gitignore
```


