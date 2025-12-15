"""Custom exception hierarchy for project-specify.

This module defines all custom exceptions used throughout the codebase,
providing structured error handling and better error messages.
"""


class SpecifyError(Exception):
    """Base exception for all project-specify errors.

    All custom exceptions inherit from this base class, making it easy
    to catch any project-specify-specific error.
    """
    pass


class SymlinkError(SpecifyError):
    """Symlink creation or verification failed.

    Raised when:
    - Creating symlinks fails (permissions, platform limitations)
    - Verifying symlink integrity fails
    - Symlink targets don't exist
    """
    pass


class ConfigError(SpecifyError):
    """Configuration parsing or validation failed.

    Raised when:
    - Invalid configuration file format
    - Missing required configuration values
    - Configuration validation fails
    """
    pass


class MonorepoError(SpecifyError):
    """Monorepo detection or handling failed.

    Raised when:
    - Monorepo configuration is malformed
    - Workspace packages cannot be resolved
    - Unsupported monorepo type
    """
    pass


class MCPDiscoveryError(SpecifyError):
    """MCP server discovery failed.

    Raised when:
    - MCP configuration file is invalid
    - MCP server validation fails
    - Technology detection encounters errors
    """
    pass


class TemplateError(SpecifyError):
    """Template download or extraction failed.

    Raised when:
    - GitHub API requests fail
    - Template download fails
    - ZIP extraction encounters errors
    - Template validation fails
    """
    pass


class GitOperationError(SpecifyError):
    """Git operation failed.

    Raised when:
    - Git repository initialization fails
    - Git commands return errors
    - Git is not installed
    """
    pass


class NetworkError(SpecifyError):
    """Network operation failed.

    Raised when:
    - HTTP requests fail
    - Connection timeout
    - Rate limiting encountered
    """
    pass


class FileOperationError(SpecifyError):
    """File operation failed.

    Raised when:
    - File read/write operations fail
    - JSON parsing errors
    - File permissions issues
    """
    pass
