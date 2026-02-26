"""
CLI entry point for the generate_input_files package.

Usage:
    python -m generate_input_files --name "Java" --proficiency BASIC
    python -m generate_input_files --name "Java, Kafka" --proficiency BASIC --dry-run
"""

from generate_input_files.generator import generate_input_files

if __name__ == "__main__":
    generate_input_files()
