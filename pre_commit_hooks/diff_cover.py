#!/usr/bin/env python

import argparse
import logging
import sys
from dataclasses import dataclass

import pytest
from diff_cover.diff_cover_tool import main as diff_cover


@dataclass
class Configuration:
    quiet: bool
    quick: bool
    compare_branch: str
    fail_under: int


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--compare-branch", default="origin/main")
    parser.add_argument("--fail-under", type=int, default=100)
    parser.add_argument("files", nargs="*")
    return parser


def parse_args(argv=None) -> Configuration:
    parser = build_parser()
    args, _ = parser.parse_known_args(argv)
    return Configuration(
        quiet=args.quiet,
        quick=args.quick,
        compare_branch=args.compare_branch,
        fail_under=args.fail_under,
    )


def run_pytest(configuration: Configuration) -> int:
    args = [
        "--cov=.",
        "--cov-report=xml",
        "--cov-report=term:skip-covered",
        "--no-cov-on-fail",
        # disable regular coverage failures i.e. diff-cover only.
        "--cov-fail-under=0",
    ]

    if configuration.quick:
        args.extend(
            [
                "--exitfirst",  # exit instantly on first error or failed test
                "--failed-first",
                "--new-first",  # run new tests first
                "--last-failed",
                # if no previous fails, skip all
                "--last-failed-no-failures=none",
            ]
        )

    if configuration.quiet:
        args.extend(
            [
                "--quiet",
                "--no-header",
                "--no-summary",
                "--disable-warnings",
                "--tb=no",  # no traceback
                "--log-level=CRITICAL",
            ]
        )

    exit_code = pytest.main(args=args)

    if (
        exit_code == pytest.ExitCode.NO_TESTS_COLLECTED
        and "--last-failed-no-failures=none" in args
    ):
        return pytest.ExitCode.OK

    return exit_code


def run_diff_cover(configuration: Configuration) -> int:
    args = [
        f"--compare-branch={configuration.compare_branch}",
        f"--fail-under={configuration.fail_under}",
    ]

    if configuration.quiet:
        args.append("--quiet")

    args.append("coverage.xml")
    logging.disable()
    return diff_cover(argv=args)


def main(argv=None) -> int:
    build_parser()
    configuration = parse_args(argv=argv)

    pytest_result = run_pytest(configuration)
    if pytest_result != pytest.ExitCode.OK:
        return pytest_result

    diff_cover_result = run_diff_cover(configuration)
    return diff_cover_result


if __name__ == "__main__":
    sys.exit(main())
