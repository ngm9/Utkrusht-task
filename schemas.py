"""
Schema models for the multiagent infrastructure assessment flow.

This module contains all JSON schemas used for OpenAI API calls with structured outputs.
Schemas are organized by their purpose and usage in the task generation and evaluation flow.
"""

# ============================================================================
# TASK GENERATION SCHEMAS
# ============================================================================

ANSWER_CODE_SCHEMA = {
    "name": "answer_code_response",
    "schema": {
        "type": "object",
        "properties": {
            "files": {
                "type": "object",
                "description": "Object containing file paths as keys and their complete implementation as values",
                "additionalProperties": {"type": "string"}
            },
            "steps": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Array of step-by-step solution instructions"
            }
        },
        "required": ["files", "steps"],
        "additionalProperties": False
    },
    "strict": False
}


# ============================================================================
# EVALUATION SCHEMAS
# ============================================================================

EVAL_RESPONSE_SCHEMA = {
    "name": "eval_response",
    "schema": {
        "type": "object",
        "properties": {
            "pass": {
                "type": "boolean",
                "description": "Whether the evaluation passed or failed"
            },
            "issues": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of issues found (empty if passed)"
            },
            "validated_criteria": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of criteria that were validated/met"
            },
            "feedback": {
                "type": "string",
                "description": "Detailed feedback if evaluation failed"
            }
        },
        "required": ["pass", "issues", "validated_criteria", "feedback"],
        "additionalProperties": False
    },
    "strict": True
}

