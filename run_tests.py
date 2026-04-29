#!/usr/bin/env python
"""Run test suite with organized output."""

import subprocess
import sys


def run_tests(test_type=None, verbose=False):
    """Run tests with pytest.

    Args:
        test_type: 'unit', 'integration', or None for all tests
        verbose: Show detailed output
    """
    print("\n" + "="*70)
    print("GAME ORACLE - TEST SUITE")
    print("="*70 + "\n")

    cmd = [sys.executable, "-m", "pytest"]

    if test_type == "unit":
        cmd.extend(["tests/unit", "-m", "not slow"])
        print("Running UNIT tests...\n")
    elif test_type == "integration":
        cmd.append("tests/integration")
        print("Running INTEGRATION tests...\n")
    else:
        cmd.append("tests")
        print("Running ALL tests...\n")

    if verbose:
        cmd.append("-vv")
    else:
        cmd.append("-v")

    cmd.extend(["--tb=short", "--color=yes"])

    # Run pytest
    result = subprocess.run(cmd)

    print("\n" + "="*70)
    if result.returncode == 0:
        print("ALL TESTS PASSED!")
    else:
        print("SOME TESTS FAILED!")
    print("="*70 + "\n")

    return result.returncode


def run_coverage():
    """Run tests with coverage report."""
    print("\n" + "="*70)
    print("GAME ORACLE - TEST COVERAGE")
    print("="*70 + "\n")

    cmd = [
        sys.executable, "-m", "pytest",
        "tests",
        "--cov=backend",
        "--cov-report=term-missing",
        "--cov-report=html",
        "-v"
    ]

    result = subprocess.run(cmd)

    print("\n" + "="*70)
    if result.returncode == 0:
        print("Coverage report generated!")
        print("Open htmlcov/index.html in a browser for detailed coverage report")
    print("="*70 + "\n")

    return result.returncode


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Run Game Oracle test suite"
    )
    parser.add_argument(
        "test_type",
        nargs="?",
        choices=["unit", "integration", "all"],
        default="all",
        help="Type of tests to run (default: all)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "-c", "--coverage",
        action="store_true",
        help="Run with coverage report"
    )

    args = parser.parse_args()

    if args.coverage:
        sys.exit(run_coverage())
    else:
        test_type = None if args.test_type == "all" else args.test_type
        sys.exit(run_tests(test_type, args.verbose))
