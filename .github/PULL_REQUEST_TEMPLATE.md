# Pull Request

## Description

<!-- Provide a brief description of the changes in this PR -->

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring
- [ ] Test improvements

## Pre-merge Checklist

### Testing

- [ ] All tests pass locally (`pytest -v`)
- [ ] Code coverage maintained or improved
- [ ] New tests added for new functionality
- [ ] Existing tests updated if behavior changed

### Code Quality

- [ ] Code passes linting (`ruff check src/ tests/`)
- [ ] Code passes formatting check (`black --check src/ tests/`)
- [ ] Type checking passes (`mypy src/specify_cli`)
- [ ] No new warnings introduced

### Documentation

- [ ] Documentation updated (if applicable)
  - [ ] README.md updated
  - [ ] Relevant guides updated (docs/*.md)
  - [ ] Docstrings added/updated for new code
  - [ ] CONTRIBUTING.md updated (if adding new extension points)
- [ ] CHANGELOG.md updated (if user-facing changes)

### Cross-Platform Compatibility

- [ ] Tested on Windows (or changes are platform-agnostic)
- [ ] Tested on macOS (or changes are platform-agnostic)
- [ ] Tested on Linux (or changes are platform-agnostic)
- [ ] Windows-specific error handling added (if needed)

### Specific Checks (if applicable)

- [ ] New AI agent support added:
  - [ ] Added to `AGENT_CONFIG` in `src/specify_cli/config.py`
  - [ ] Command structure created in `src/specify_cli/agents/`
  - [ ] Tests added in `tests/test_symlink_manager.py`
  - [ ] Documentation updated in README.md
- [ ] New monorepo type support added:
  - [ ] Detection logic added in `src/specify_cli/monorepo.py`
  - [ ] Tests added in `tests/test_monorepo.py`
  - [ ] Documentation updated in README.md and `docs/monorepo-guide.md`
- [ ] Breaking changes:
  - [ ] Migration guide provided
  - [ ] Version bump planned
  - [ ] Deprecation warnings added (if applicable)

## Testing Instructions

<!-- Provide steps for reviewers to test these changes -->

1.
2.
3.

## Screenshots (if applicable)

<!-- Add screenshots for UI changes or terminal output changes -->

## Related Issues

<!-- Link to related issues -->

Fixes #
Closes #
Related to #

## Additional Notes

<!-- Any additional information that reviewers should know -->

---

## AI Assistance Disclosure

<!-- Required: Disclose any AI assistance used in creating this PR -->

- [ ] No AI assistance used
- [ ] AI assistance used for:
  - [ ] Code generation
  - [ ] Documentation
  - [ ] Test writing
  - [ ] Code review/suggestions
  - [ ] Other: _____________

**Details:**
<!-- Briefly describe the extent of AI assistance -->
