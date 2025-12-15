# Contributing to Spec Kit

Hi there! We're thrilled that you'd like to contribute to Spec Kit. Contributions to this project are [released](https://help.github.com/articles/github-terms-of-service/#6-contributions-under-repository-license) to the public under the [project's open source license](LICENSE).

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## Prerequisites for running and testing code

These are one time installations required to be able to test your changes locally as part of the pull request (PR) submission process.

1. Install [Python 3.11+](https://www.python.org/downloads/)
1. Install [uv](https://docs.astral.sh/uv/) for package management
1. Install [Git](https://git-scm.com/downloads)
1. Have an [AI coding agent available](README.md#-supported-ai-agents)

<details>
<summary><b>💡 Hint if you are using <code>VSCode</code> or <code>GitHub Codespaces</code> as your IDE</b></summary>

<br>

Provided you have [Docker](https://docker.com) installed on your machine, you can leverage [Dev Containers](https://containers.dev) through this [VSCode extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers), to easily set up your development environment, with aforementioned tools already installed and configured, thanks to the `.devcontainer/devcontainer.json` file (located at the root of the project).

To do so, simply:

- Checkout the repo
- Open it with VSCode
- Open the [Command Palette](https://code.visualstudio.com/docs/getstarted/userinterface#_command-palette) and select "Dev Containers: Open Folder in Container..."

On [GitHub Codespaces](https://github.com/features/codespaces) it's even simpler, as it leverages the `.devcontainer/devcontainer.json` automatically upon opening the codespace.

</details>

## Submitting a pull request

> [!NOTE]
> If your pull request introduces a large change that materially impacts the work of the CLI or the rest of the repository (e.g., you're introducing new templates, arguments, or otherwise major changes), make sure that it was **discussed and agreed upon** by the project maintainers. Pull requests with large changes that did not have a prior conversation and agreement will be closed.

1. Fork and clone the repository
1. Configure and install the dependencies: `uv sync`
1. Make sure the CLI works on your machine: `uv run specify --help`
1. Create a new branch: `git checkout -b my-branch-name`
1. Make your change, add tests, and make sure everything still works
1. Test the CLI functionality with a sample project if relevant
1. Push to your fork and submit a pull request
1. Wait for your pull request to be reviewed and merged.

Here are a few things you can do that will increase the likelihood of your pull request being accepted:

- Follow the project's coding conventions.
- Write tests for new functionality.
- Update documentation (`README.md`, `spec-driven.md`) if your changes affect user-facing features.
- Keep your change as focused as possible. If there are multiple changes you would like to make that are not dependent upon each other, consider submitting them as separate pull requests.
- Write a [good commit message](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html).
- Test your changes with the Spec-Driven Development workflow to ensure compatibility.

## Development workflow

When working on spec-kit:

1. Test changes with the `specify` CLI commands (`/speckit.specify`, `/speckit.plan`, `/speckit.tasks`) in your coding agent of choice
2. Verify templates are working correctly in `templates/` directory
3. Test script functionality in the `scripts/` directory
4. Ensure memory files (`memory/constitution.md`) are updated if major process changes are made

### Testing template and command changes locally

Running `uv run specify init` pulls released packages, which won’t include your local changes.  
To test your templates, commands, and other changes locally, follow these steps:

1. **Create release packages**

   Run the following command to generate the local packages:

   ```bash
   ./.github/workflows/scripts/create-release-packages.sh v1.0.0
   ```

2. **Copy the relevant package to your test project**

   ```bash
   cp -r .genreleases/sdd-copilot-package-sh/. <path-to-test-project>/
   ```

3. **Open and test the agent**

   Navigate to your test project folder and open the agent to verify your implementation.

## Testing and Code Quality

### Running Tests Locally

Project-specify uses pytest for testing. To run the test suite:

```bash
# Install development dependencies
uv sync

# Run all tests
pytest -v

# Run tests with coverage
pytest -v --cov=specify_cli --cov-report=term

# Run specific test file
pytest tests/test_symlink_manager.py -v

# Run tests matching a pattern
pytest -k "test_symlink" -v
```

**Before submitting a PR:**
1. All tests must pass
2. New features must include tests
3. Bug fixes should include regression tests

### Code Style Requirements

We enforce code quality with automated tools:

**Linting (ruff):**
```bash
# Check for linting issues
ruff check src/ tests/

# Auto-fix issues where possible
ruff check --fix src/ tests/
```

**Code Formatting (black):**
```bash
# Check formatting
black --check src/ tests/

# Auto-format code
black src/ tests/
```

**Type Checking (mypy):**
```bash
# Run type checker
mypy src/specify_cli --install-types --non-interactive --ignore-missing-imports
```

**Run all checks:**
```bash
# Lint, format, and type-check
ruff check src/ tests/ && black --check src/ tests/ && mypy src/specify_cli
```

### CI/CD Pipeline

All pull requests run through automated checks:
- **Tests**: Ubuntu, macOS, Windows with Python 3.11 and 3.12
- **Linting**: ruff, black, mypy
- **Coverage**: Codecov integration

View workflow files:
- `.github/workflows/test.yml`
- `.github/workflows/lint.yml`
- `.github/workflows/release.yml`

## Extending Project-Specify

### Adding Support for New AI Agents

To add support for a new AI agent:

1. **Update `AGENT_CONFIG` in `src/specify_cli/config.py`:**

   ```python
   AGENT_CONFIG = {
       # ... existing agents ...
       "my-new-agent": {
           "folder": ".my-agent/",
           "name": "My New Agent",
           "script_type": "sh",  # or "ps" for PowerShell
       },
   }
   ```

2. **Create agent command structure in `src/specify_cli/agents/`:**

   ```
   src/specify_cli/agents/
   └── my-new-agent/
       └── commands/
           ├── spec.sh
           ├── plan.sh
           ├── tasks.sh
           └── implement.sh
   ```

3. **Update `_get_agent_symlink_config()` in `src/specify_cli/symlink_manager.py`** if special handling is needed:

   ```python
   def _get_agent_symlink_config(agent_key: str) -> dict:
       # ... existing code ...

       # Special case for my-new-agent
       if agent_key == "my-new-agent":
           return {
               "source": "my-new-agent/commands",
               "target": ".my-agent/commands",
           }
   ```

4. **Add tests in `tests/test_symlink_manager.py`:**

   ```python
   def test_create_symlinks_for_my_new_agent(temp_project, mock_central_install):
       """Test symlink creation for My New Agent."""
       # ... test implementation
   ```

5. **Update documentation:**
   - Add to supported agents table in `README.md`
   - Mention in relevant documentation

### Adding Support for New Monorepo Types

To add support for a new monorepo configuration:

1. **Add detection logic in `src/specify_cli/monorepo.py`:**

   ```python
   def detect_my_monorepo(project_dir: Path) -> Optional[MonorepoInfo]:
       """Detect My Monorepo Tool workspace."""
       config_file = project_dir / "my-workspace.config"

       if not config_file.exists():
           return None

       # Parse config and return workspace info
       packages = _parse_my_monorepo_config(config_file)

       return MonorepoInfo(
           type="my-monorepo",
           root=project_dir,
           packages=packages,
           config_file=config_file,
       )
   ```

2. **Update `detect_monorepo()` function:**

   ```python
   def detect_monorepo(project_dir: Path) -> Optional[MonorepoInfo]:
       """Detect monorepo type and return workspace information."""
       detectors = [
           # ... existing detectors ...
           detect_my_monorepo,
       ]

       for detector in detectors:
           result = detector(project_dir)
           if result:
               return result

       return None
   ```

3. **Add helper parsing function:**

   ```python
   def _parse_my_monorepo_config(config_file: Path) -> list[Path]:
       """Parse My Monorepo workspace configuration."""
       try:
           with open(config_file, "r") as f:
               data = json.load(f)

           workspace_patterns = data.get("workspaces", [])
           return _expand_glob_patterns(config_file.parent, workspace_patterns)

       except Exception as e:
           raise MonorepoError(
               f"Failed to parse {config_file}: {e}"
           ) from e
   ```

4. **Add tests in `tests/test_monorepo.py`:**

   ```python
   def test_detect_my_monorepo(temp_project):
       """Test My Monorepo detection."""
       # Create config file
       config = temp_project / "my-workspace.config"
       config.write_text(json.dumps({
           "workspaces": ["packages/*"]
       }))

       # Create workspace
       (temp_project / "packages" / "app1").mkdir(parents=True)

       # Test detection
       result = detect_monorepo(temp_project)

       assert result is not None
       assert result.type == "my-monorepo"
       assert len(result.packages) == 1
   ```

5. **Update documentation:**
   - Add to supported monorepo types in `README.md`
   - Add example in `docs/monorepo-guide.md`

### Code Organization

- **`src/specify_cli/__init__.py`** - Main CLI entry point and Typer app
- **`src/specify_cli/config.py`** - Configuration constants and agent definitions
- **`src/specify_cli/symlink_manager.py`** - Symlink/copy creation and management
- **`src/specify_cli/monorepo.py`** - Monorepo detection and handling
- **`src/specify_cli/mcp_discovery.py`** - MCP server discovery
- **`src/specify_cli/commands/`** - CLI command implementations
- **`src/specify_cli/errors.py`** - Custom exception hierarchy
- **`tests/`** - Test suite (174+ tests)

## AI contributions in Spec Kit

> [!IMPORTANT]
>
> If you are using **any kind of AI assistance** to contribute to Spec Kit,
> it must be disclosed in the pull request or issue.

We welcome and encourage the use of AI tools to help improve Spec Kit! Many valuable contributions have been enhanced with AI assistance for code generation, issue detection, and feature definition.

That being said, if you are using any kind of AI assistance (e.g., agents, ChatGPT) while contributing to Spec Kit,
**this must be disclosed in the pull request or issue**, along with the extent to which AI assistance was used (e.g., documentation comments vs. code generation).

If your PR responses or comments are being generated by an AI, disclose that as well.

As an exception, trivial spacing or typo fixes don't need to be disclosed, so long as the changes are limited to small parts of the code or short phrases.

An example disclosure:

> This PR was written primarily by GitHub Copilot.

Or a more detailed disclosure:

> I consulted ChatGPT to understand the codebase but the solution
> was fully authored manually by myself.

Failure to disclose this is first and foremost rude to the human operators on the other end of the pull request, but it also makes it difficult to
determine how much scrutiny to apply to the contribution.

In a perfect world, AI assistance would produce equal or higher quality work than any human. That isn't the world we live in today, and in most cases
where human supervision or expertise is not in the loop, it's generating code that cannot be reasonably maintained or evolved.

### What we're looking for

When submitting AI-assisted contributions, please ensure they include:

- **Clear disclosure of AI use** - You are transparent about AI use and degree to which you're using it for the contribution
- **Human understanding and testing** - You've personally tested the changes and understand what they do
- **Clear rationale** - You can explain why the change is needed and how it fits within Spec Kit's goals
- **Concrete evidence** - Include test cases, scenarios, or examples that demonstrate the improvement
- **Your own analysis** - Share your thoughts on the end-to-end developer experience

### What we'll close

We reserve the right to close contributions that appear to be:

- Untested changes submitted without verification
- Generic suggestions that don't address specific Spec Kit needs
- Bulk submissions that show no human review or understanding

### Guidelines for success

The key is demonstrating that you understand and have validated your proposed changes. If a maintainer can easily tell that a contribution was generated entirely by AI without human input or testing, it likely needs more work before submission.

Contributors who consistently submit low-effort AI-generated changes may be restricted from further contributions at the maintainers' discretion.

Please be respectful to maintainers and disclose AI assistance.

## Resources

- [Spec-Driven Development Methodology](./spec-driven.md)
- [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/)
- [Using Pull Requests](https://help.github.com/articles/about-pull-requests/)
- [GitHub Help](https://help.github.com)
