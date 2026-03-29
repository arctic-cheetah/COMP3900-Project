# We need this file to start code coverage
import os

if os.getenv("COVERAGE_PROCESS_START"):
    try:
        import coverage

        coverage.process_startup()
    except Exception:
        # Don't stop app from running if coverage is unavialable
        pass
