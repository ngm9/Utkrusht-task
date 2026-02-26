PROMPT_EXPRESSJS_BASIC_CONTEXT = """
Let me provide you with some context about the company and role:

Company Context:
{organization_background}

Roles and Responsibilities:
{role_context}

Based on this information, could you summarize what you understand about the company and role requirements?
"""

PROMPT_EXPRESSJS_BASIC_INPUT_AND_ASK = """
# GOAL:
As a technical architect super experienced in Express.js and Node.js backend development, you are given a list of real-world scenarios and proficiency levels for Express.js development.
Your job is to generate a complete backend task definition — including API endpoints, middleware logic, database integration (if relevant), README.md, and expected outcomes — that can effectively assess the candidate’s ability to think, design, build, implement, debug, and deploy a backend service end to end.

Now that you've seen the instructions and examples, you are ready to generate a task definition for Express.js given the following inputs:

INPUT COMPETENCIES:
{competencies}

INPUT ROLE CONTEXT: 
{role_context}

INPUT REAL-WORLD SCENARIOS FOR TASK INSPIRATION:
{real_world_task_scenarios}

CRITICAL: The task complexity must be appropriate for the given skill level and years of experience. The candidate should be able to complete it within the allocated time. Use the real-world scenarios to determine the business context and technical focus (e.g., REST API design, authentication, middleware, or database operations).


Can you now generate a task definition for Express.js given the above inputs, following the instructions given above?
Use the following prompt to narrow down your response:
{question_prompt}

RESPOND ONLY WITH VALID JSON - NO MARKDOWN OR EXPLANATIONS.
"""


PROMPT_EXPRESSJS_BASIC_INSTRUCTIONS = """
# GOAL:
As a technical architect super experienced in Express.js, Node.js ecosystem, and backend architecture, you are given a list of real world scenarios and proficiency levels for Express.js development. 
Your job is to generate an entire task definition, including code files, README.md, expected outcomes etc. that can be effectively used to assess the candidate's ability to effectively think, design, build, implement, debug or in general solve a problem end to end at an intermediate level.

# INSTRUCTIONS:

## Nature of the task 
- Task must ask to implement a feature from scratch, refactor existing code, or fix complex bugs in the existing codebase.
- The question scenario must be clear, ensuring that all facts, figures, company names, individual names, etc., are historically accurate and relevant to the context. 
- Generate enough starter code that gives the candidate a good starting point to start solving the task.
- DO NOT GIVE AWAY THE SOLUTION IN THE STARTER CODE.
- A part of the task completion is to watch the candidate implement best practices, design the solution correctly, demonstrate proper architecture decisions, and not just fix the errors or add features hastily.
- The question should be a real-world scenario that tests architectural thinking, API design expertise, and optimization skills.
- The complexity of the task and specific ask expected from the candidate must align with INTERMEDIATE proficiency level (3-5 years Express.js/Node.js experience), ensuring that no two questions generated are similar.
- **PRIMARY FOCUS AREAS**: Tasks MUST focus primarily on these two critical areas:
  1. **API Design Excellence**: RESTful principles, endpoint structure, versioning, request/response design, HTTP methods, status codes, API documentation, resource modeling
  2. **Optimization & Performance**: Code efficiency, response time optimization, caching strategies, data processing optimization, memory management, async patterns, algorithm efficiency
- For INTERMEDIATE level of proficiency, the questions should test deeper understanding and require candidates to demonstrate:
  - **Advanced API Design**: 
    - RESTful principles and resource-oriented architecture
    - HTTP methods usage (GET, POST, PUT, PATCH, DELETE) and idempotency
    - Status code selection (2xx, 4xx, 5xx) and semantic correctness
    - URL structure and naming conventions
    - Query parameters, path parameters, request body design
    - Response format standardization (success/error responses)
    - API versioning strategies
    - Pagination, filtering, and sorting patterns
    - Rate limiting and throttling
    - Content negotiation (JSON, XML, etc.)
  - **Performance & Optimization**:
    - Async/await patterns and non-blocking operations
    - Efficient data processing and transformation
    - Caching strategies (in-memory, response caching)
    - Request/response optimization
    - Algorithm complexity and optimization
    - Memory leak prevention
    - Stream processing for large data
    - Batch processing optimization
    - Middleware performance optimization
    - Load testing and performance profiling
  - **Middleware Design**: Custom middleware, middleware composition, error handling middleware, request/response transformation
  - **Business Logic Organization**: Service layer pattern, separation of concerns, modular design
  - **Error Handling & Logging**: Centralized error handling, structured logging, meaningful error messages, error response standardization
  - **Security**: Input validation, data sanitization, secure headers, CORS configuration, rate limiting
  - **Code Quality**: Modern JavaScript/ES6+ features, code organization, clean code principles
  - **Real-world Patterns**: Async operations, webhooks, file processing, data transformation
  - **Data Validation**: Request validation, schema validation, business rule enforcement
- The question must NOT include hints. The hints will be provided in the "hints" field.
- Ensure that all questions and scenarios adhere to modern Node.js best practices (Node.js 18+) and current JavaScript standards. Use async/await patterns exclusively.
- Tasks should require candidates to make architectural decisions and justify their approach.
- If you include diagrams, ensure they are written in mermaid format, properly indented and also in code blocks.
- **Database is OPTIONAL**: Tasks may or may not include database integration. When databases are not required, focus on in-memory data structures, file operations, external API integrations, or data processing scenarios.

## AI AND EXTERNAL RESOURCE POLICY:
- Candidates are permitted and encouraged to use any external resources they find helpful, including but not limited to Google, Stack Overflow, official documentation, and AI-powered tools, agentic IDs, or Large Language Models (LLMs).
- The tasks are designed to assess the candidate's ability to effectively find, understand, integrate, and adapt solutions to solve a specific problem, rather than testing rote memorization.
- Therefore, the complexity of the tasks should reflect intermediate Express.js proficiency while requiring genuine engineering and architectural skills that go beyond simple copy-pasting from a generative AI.
- Tasks should test the candidate's ability to evaluate different approaches and choose the most appropriate solution for API design and optimization challenges.

## Code Generation Instructions:
Based on the real-world scenarios provided in following conversations, create an Express.js task that:
- Draws inspiration from the input_scenarios given to determine the business context and technical requirements.
- Matches the complexity level appropriate for INTERMEDIATE proficiency level (3-5 years Express.js/Node.js experience), keeping in mind that AI assistance is allowed.
- Tests practical Express.js skills with **PRIMARY EMPHASIS on API design excellence and optimization/performance**.
- Time constraints: Each task should be finished within {minutes_range} minutes (typically 60-120 minutes for intermediate tasks).
- At every time pick different real-world scenario from the list provided above to ensure variety in task generation.
- Focus on API-centric applications that require thoughtful endpoint design, request/response handling, and performance optimization.
- Should test the candidate's ability to structure well-designed APIs with optimal performance characteristics.
- Database integration is OPTIONAL - many tasks can effectively test API design and optimization without database requirements.

## Starter Code Instructions:
- The starter code should provide a foundation that allows candidates to demonstrate API design and optimization skills.
- The code files generated must be valid and executable with `npm start` or `npm run dev`.
- Provide a realistic project structure that mimics real-world applications (routes/, controllers/, services/, middleware/, utils/, config/).
- A part of the task completion is to watch the candidate implement best practices, design the solution correctly, demonstrate proper folder structure, and architectural decisions.
- If the task is to fix bugs, make sure the starter code has logical bugs, API design issues, or performance problems (no syntactic errors) that require intermediate-level thinking to resolve.
- If the task is to implement a feature from scratch, provide a foundation that allows candidates to showcase proper API design, efficient algorithms, and performance optimization.
- Express.js starter code should include realistic project structure but NOT require complex infrastructure setup for local development.
- Include some existing routes, controllers, or services that the candidate needs to extend, refactor, or optimize.
- Provide partial implementations that require candidates to complete the API design and optimization work.
- **Do NOT mandate database usage** - many scenarios can use in-memory data, file operations, or external API integrations.

# OUTPUT
The output should be a valid json schema:
  - README.md (CRITICAL - Follow exact structure specified below)
  - package.json (Node.js dependencies including Express and other dependencies required in the scenario - database clients are OPTIONAL)
  - .gitignore (Standard Node.js/Express project gitignore)
  - .env.example (Environment variables template - if needed)
  - Any application code files (routes/, controllers/, services/, middleware/, utils/, config/)
  - Data files (JSON, CSV, etc.) if the task involves data processing without database
  - Any other configuration files needed for local development
  - Code files should demonstrate partial architecture that candidate needs to complete/extend
  - Include realistic folder structure appropriate for the task

# REQUIRED OUTPUT JSON STRUCTURE:

{{
   "name": "Task Name (50 words maximum not exceding that)",
   "question": "A detailed description of the task scenario including the specific ask from the candidate — what needs to be implemented/refactored/fixed/optimized? Include API design considerations and performance optimization requirements.",
   "code_files": {{
      "README.md": "Candidate-facing README with Task Overview, Guidance, Objectives, and How to Verify",
      ".gitignore": "Proper Node.js/Express exclusions",
      "package.json": "Node.js dependencies and scripts",
      "src/index.js": "Express app entry point",
      "src/app.js": "Express app setup",
      "src/config/config.js": "Configuration management (if needed)",
      "src/middleware/errorHandler.js": "Error handling middleware",
      "src/routes/routeName.js": "API route files",
      "src/controllers/controllerName.js": "Controller files",
      "src/services/serviceName.js": "Business logic service files",
      "src/utils/utilityFile.js": "Utility functions",
      "src/constants/constants.js": "Application constants",
      "src/validators/validatorName.js": "Input validation (if needed)",
      "data/sampleData.json": "Sample data files (if applicable)",
      "tests/api.test.js": "Test files (if applicable)",
      "starter_code_file_name": "starter_code_file_content",
      "starter_code_file_name_2": "starter_code_file_content_2"
      ...
  }},
  "outcomes": "Expected results after completion focusing on API design quality, performance improvements, code organization, and response time optimization. Include both functional outcomes and optimization metrics (4-5 lines).",
  "pre_requisites": "Bullet-point list of tools, libraries, environment setup, and knowledge required. Include intermediate-level expectations like Node.js 18+, RESTful API principles, HTTP protocol understanding, async/await patterns, performance profiling concepts, etc. Do NOT mandate database knowledge unless absolutely required.",
  "answer": "High-level solution approach with emphasis on API design decisions, optimization strategies, and performance improvements",
  "hints": "a single line hint focusing on API design approach or optimization strategy that could be useful. These hints must NOT give away the answer, but guide towards good API design and optimization thinking.",
  "definitions": {{
    "terminology_1": "definition_1",
    "terminology_2": "definition_2",
    ...
    }}
}}

 
## Code file requirements:
- Generate realistic folder structure (src/routes/, src/controllers/, src/services/, src/middleware/, src/utils/, src/config/, src/validators/, data/ etc.)
- Code should follow modern Express.js and Node.js best practices and demonstrate intermediate-level patterns.
- Use async/await patterns exclusively, no callback-based code.
- Focus on modern JavaScript/ES6+ features and Express.js best practices.
- **CRITICAL**: The generated code files should provide partial implementations that require API design and optimization completion.
- Include some existing routes, controllers, or services that need to be extended, refactored, or optimized.
- The core API design decisions, performance optimizations, algorithm improvements, caching strategies that the candidate needs to implement MUST be left for the candidate to design.
- DO NOT include any 'TODO' or placeholder comments.
- DO NOT include any comments that give away hints or solutions.
- DO NOT include comments like "Add optimization here", "Implement caching", "Add validation", "Optimize this endpoint", etc.
- DO NOT add comments that give away hints, solution, or implementation details.
- The generated project structure should be runnable locally with `npm start` or `npm run dev`, but will require API design and optimization work to function properly.
- Provide realistic dependencies in package.json that intermediate developers should be familiar with.
- **Database setup is NOT mandatory** - use in-memory data structures, JSON files, or external API calls when appropriate.

## .gitignore INSTRUCTIONS:
Create a comprehensive gitignore file that covers all standard exclusions for intermediate Node.js/Express projects including node_modules, environment files, log files, IDE configurations, coverage reports, and other common development artifacts that should not be tracked in version control.


## README.md INSTRUCTIONS:
- The README.md contains the following sections:
  - Task Overview
  - Guidance
  - Objectives
  - How to Verify
- The README.md file content MUST be fully populated with meaningful, specific content
- Task Overview section MUST contain the exact business scenario from the task description
- ALL sections must have substantial content - no empty or placeholder text allowed
- Content must be directly relevant to the specific task scenario being generated
- Use concrete business context, not generic descriptions
- Do not give away any specific implementation details or architectural decisions that would hint at the solution

### Task Overview
**CRITICAL REQUIREMENT**: This section MUST contain 3-4 meaningful sentences describing the business scenario, current situation, and why API design excellence and optimization matter for this use case.
NEVER generate empty content - always provide substantial business context that explains what the candidate is working on and why proper API design and performance optimization are crucial.

### Guidance
- Provide 3-5 simple, clear bullet points that give project context and high-level guidance
- Each bullet point should be one concise sentence
- Focus on what matters for this specific task (API design quality, performance expectations, code organization)
- Do NOT give detailed instructions or implementation hints
- Do NOT include sub-bullets or nested lists
- Example format: "Consider RESTful principles when designing endpoints" or "Focus on optimizing response times for high-traffic scenarios"

### Objectives
- Provide 4-6 clear bullet points listing specific, measurable objectives
- Each objective should be a clear statement of what needs to be accomplished
- Focus on functional requirements and quality expectations
- Do NOT include explanatory text or sub-points
- Make objectives testable and verifiable
- Example format: "Implement GET /api/resource endpoint with proper status codes" or "Optimize data processing to reduce response time below 200ms"

### How to Verify
- Provide 4-6 simple bullet points describing how to verify task completion
- Each point should be a clear, actionable verification step
- Focus on observable outcomes and testable behaviors
- Do NOT include lengthy explanations or sub-steps
- Make verification steps concrete and specific
- Example format: "Test GET /api/resource returns 200 status with correct JSON format" or "Verify response time is under 200ms using 100 concurrent requests"

### NOT TO INCLUDE in README: Make sure you do not include the following in the README.md file:
- SETUP INSTRUCTIONS OR COMMANDS (npm install, npm start, etc.)
- Direct solutions or architectural decisions
- Step-by-step implementation guides
- Specific Express.js patterns or middleware implementations to use
- Direct answers and code snippets that would give away the solution to the task
- Any specific files implementation details that would give away the solution to the task
- Should not provide any particular architectural approach or design pattern to implement the solution
- Specific endpoint names, URL structures, or response formats that would reveal the solution
- Specific optimization techniques or caching strategies to implement
- Folder structure decisions that would dictate the architectural approach
- Database technologies or libraries (unless task specifically requires database)
"""