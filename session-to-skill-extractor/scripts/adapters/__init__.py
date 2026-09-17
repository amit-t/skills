"""Adapter registry: maps host name -> Adapter subclass.

Each adapter module is imported behind a try/except ImportError so a host
whose module doesn't exist yet (or has an unmet optional dependency) never
breaks the registry for the other hosts (Ruling 2). ADAPTERS only ever
contains the hosts that actually imported.
"""

ADAPTERS = {}

try:
    from adapters.claude_code import ClaudeCodeAdapter
    ADAPTERS["claude-code"] = ClaudeCodeAdapter
except ImportError:
    pass

try:
    from adapters.codex import CodexAdapter
    ADAPTERS["codex"] = CodexAdapter
except ImportError:
    pass

try:
    from adapters.copilot import CopilotAdapter
    ADAPTERS["copilot"] = CopilotAdapter
except ImportError:
    pass

try:
    from adapters.devin import DevinAdapter
    ADAPTERS["devin"] = DevinAdapter
except ImportError:
    pass

try:
    from adapters.generic import GenericAdapter
    ADAPTERS["generic"] = GenericAdapter
except ImportError:
    pass
