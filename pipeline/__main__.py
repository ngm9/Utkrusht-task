"""
CLI entry point for the unified pipeline.

Usage:
    python -m pipeline --name "Java, Kafka" --proficiency BASIC --count 6 --append
    python -m pipeline --name "React" --proficiency BASIC --dry-run
"""

import sys
import io

# Fix Unicode output on Windows (cp1252 can't handle chars like →, •, etc.)
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from pipeline.pipeline import run_pipeline

if __name__ == "__main__":
    run_pipeline()
