# pre-commit-diff-cover

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

A [pre-commit](https://pre-commit.com/) hook to ensure you have adequate test
 coverage for your new or modified Python code.

Under the hood this uses:

- [pytest](https://pypi.org/project/pytest/) (as the test runner)
- [pytest-cov](https://pypi.org/project/pytest-cov/) (to generate a coverage report)
- [diff-cover](https://pypi.org/project/diff-cover/) (compares coverage report
 with `git diff`)

## Usage

```yaml
  - repo: https://github.com/gvee-uk/pre-commit-diff-cover
    rev: v0.0.1
    hooks:
    - id: diff-cover
```

## How to Use Arguments

There are a few different arguments this hook will accept.

```yaml
    hooks:
    - id: diff-cover
      args: [--quiet, --quick, --fail-under=100]
```

### `--quiet`

As the name suggests, reduces the output from the underlying tooling.

_Note_: output is only shown if this pre-commit fails

### `--quick`

Runs `pytest` with a number of arguments to speed up the execution e.g.
 `--last-failed-no-failures=none` which skips unchanged tests that passed last run.

### `--fail-under`

_Defaults to `100`%_

Fail the pre-commit check if the coverage percentage is below the specified threshold.
