from setuptools import find_packages, setup

setup(
    name="pre-commit-diff-cover",
    description="A pre-commit hook to run diff-cover",
    url="https://github.com/gvee-uk/pre-commit-diff-cover",
    version="0.0.1",
    author="George Verney",
    author_email="george@thedatashed.co.uk",
    packages=find_packages("."),
    install_requires=[
        "pytest>=7.2.0",
        "pytest-cov>=4.0.0",
        "diff-cover>=7.0.1",
    ],
    entry_points={
        "console_scripts": [
            "diff_cover = pre_commit_hooks.diff_cover:main",
        ],
    },
)
