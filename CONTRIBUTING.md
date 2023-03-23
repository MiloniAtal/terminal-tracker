
# Contributing
Thank you for your interest in contributing to terminal_tracker!

## Guidelines

When submitting or commenting on an Issue, please respect the following
guidelines. 
-   Be respectful and civil!
-   Use the provided Issue templates. 

-   Please make sure PRs include:
    -   Tests asserting behavior of any new or modified features.
    -   Docs for any new or modified public APIs.

-   Keep PRs clean, simple and to-the-point:
    -   Squash "WIP", "Reverting ..", etc., commits.
    -   No merge commits (`git merge master`), prefer `rebase` to resolve
        conflicts with the `master` branch.

## Development environment

The only prerequisite is python with version greater than 3.7. 

You can clone the repository as:

```
git clone https://github.com/MiloniAtal/terminal-tracker.git
```

You will need the following packages:

- For code: 
    - pandas
    - pytz
- For running tests, coverage, formatting: 
    - black>=22
    - flake8>=3.7.8
    - flake8-black>=0.2.1
    - flake8-pyproject
    - mypy
    - pytest>=4.3.0
    - pytest-cov>=2.6.1

You can install the dependencies using:

```
make develop
```

Check the following before opening a PR:

- Build: make build
- Linting: make lint
- Checks: make checks
- All tests pass: make test
- Coverage should be above 70%: make coverage
