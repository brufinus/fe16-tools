# Contributing

## Commit Format

Use [Angular Commit Message Convention](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#-commit-message-format).

## Semantic Versioning

This repository follows [semantic versioning rules](https://semver.org/).

A [semantic-release](https://semantic-release.gitbook.io/semantic-release)
workflow is implemented to help enforce correct versioning.

By using the Angular Commit Message Convention, semantic-release will
automatically tag and create releases.

## Testing

Test cases should be set up for new features.

Cases must pass a pytest run.

### Local

1. `pip install pytest`
2. `pytest`
