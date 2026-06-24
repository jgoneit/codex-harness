#!/usr/bin/env python3
"""Minimal non-destructive Harness hook validators."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import shlex
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


PLAN_PROMPT = "Proceed with this Plan? [y/N]"
REPAIR_PROMPT = "Proceed with this Repair Plan? [y/N]"
REVIEW_STATUSES = (
    "clean_context_review_completed",
    "review_not_required_tiny_only",
    "review_blocked_degraded",
)

COMPLETION_SECTIONS = (
    "Status",
    "Review Status",
    "Repair Plan Required",
    "Changed Files",
    "Verification",
    "Review Result",
    "Approval Ledger",
    "Residual Risks",
    "Follow-up",
)

PLANNER_SECTIONS = (
    "Task Classification",
    "Risk Level",
    "Reasoning for classification",
    "In Scope",
    "Out of Scope",
    "Files / Areas to Inspect",
    "Proposed Change Plan",
    "Verification Plan",
    "Risks / Assumptions",
    "Approval Gate",
)

IMPLEMENTER_SECTIONS = (
    "Accepted Plan Reference",
    "Changed Files",
    "Summary of Changes",
    "Scope Compliance",
    "Verification Performed",
    "Deviations from Plan",
    "Blockers / Residual Risks",
)

REVIEWER_SECTIONS = (
    "Inputs Reviewed",
    "Accepted Plan",
    "Diff / Changed Files",
    "Verification Evidence",
    "Findings Table",
    "Verdict",
)

REVIEWER_FINDING_FIELDS = (
    "Severity",
    "Finding",
    "Evidence",
    "Required Action",
)

REVIEWER_VERDICTS = (
    "PASS",
    "PASS_WITH_NOTES",
    "REPAIR_REQUIRED",
    "BLOCKED",
)

SHELL_TOOL_NAMES = {"bash", "shell", "terminal", "exec", "command"}
SHELL_TOOL_NAME_PARTS = ("bash", "shell", "terminal", "exec")
SQL_CLIENTS = {"psql", "mysql", "mariadb", "sqlite3", "sqlcmd", "sqlplus"}
NOSQL_CLIENTS = {"mongosh", "mongo", "redis-cli"}
DB_CLIENTS = SQL_CLIENTS | NOSQL_CLIENTS
DB_CLIENT_INFORMATION_ARGS = {"--version", "-V", "--help"}
GUARD_CONFIG_RELATIVE_PATH = ".harness/guard.json"
AUDIT_RELATIVE_PATH = ".harness/audit/run.jsonl"
AUDIT_HASH_HEX_CHARS = 12
AUDIT_DECISIONS = {"allow", "block"}
GUARD_CONFIG_ALLOW_KEYS = {"allow_db_local_connections", "allow_paths"}
GUARD_CONFIG_METADATA_LIST_KEYS = {"verification_commands", "approval_required_paths"}
GUARD_CONFIG_METADATA_BOOL_KEYS = {"review_required"}
GUARD_CONFIG_LIST_KEYS = GUARD_CONFIG_ALLOW_KEYS | GUARD_CONFIG_METADATA_LIST_KEYS
GUARD_CONFIG_KEYS = GUARD_CONFIG_LIST_KEYS | GUARD_CONFIG_METADATA_BOOL_KEYS
SOFT_ALLOW_CATEGORIES = {"db_client_access"}
SQL_IDENTIFIER = r'(?:[A-Za-z_][A-Za-z0-9_$]*|"[^"]+"|`[^`]+`|\[[^\]]+\])'
SQL_QUALIFIED_IDENTIFIER = rf"{SQL_IDENTIFIER}(?:\s*\.\s*{SQL_IDENTIFIER})*"
SQL_SCHEMA_OBJECT = (
    r"(?:table|database|schema|index|view|sequence"
    r"|function|procedure|materialized\s+view|trigger|type)"
)
SQL_DROP_STATEMENT = rf"drop\s+{SQL_SCHEMA_OBJECT}\b"
SQL_ALTER_STATEMENT = rf"alter\s+{SQL_SCHEMA_OBJECT}\b"
SQL_CREATE_STATEMENT = rf"create\s+(?:or\s+(?:replace|alter)\s+)?{SQL_SCHEMA_OBJECT}\b"
SQL_PRIVILEGE_STATEMENT = (
    r"(?:grant\s+.+?\s+to\b"
    r"|revoke\s+.+?\s+from\b)"
)
SQL_PROCEDURE_STATEMENT = (
    rf"(?:call\s+{SQL_QUALIFIED_IDENTIFIER}\s*(?:\(|;|$)"
    rf"|exec(?:ute)?\s+(?:procedure\s+)?(?:"
    rf"{SQL_QUALIFIED_IDENTIFIER}\s*\("
    rf"|(?=[A-Za-z0-9_.\"`\[\]\s]*[_.]){SQL_QUALIFIED_IDENTIFIER}\s*(?:;|$)"
    rf"))"
)
SQL_TEXT_COMMANDS = {"echo", "printf"}
COMMAND_PREFIXES = {
    "cat",
    "cp",
    "curl",
    "docker",
    "docker-compose",
    "env",
    "echo",
    "export",
    "find",
    "git",
    "grep",
    "head",
    "helm",
    "kubectl",
    "less",
    "more",
    "mv",
    "printenv",
    "printf",
    "psql",
    "mysql",
    "mariadb",
    "sqlite3",
    "sqlcmd",
    "sqlplus",
    "mongosh",
    "mongo",
    "redis-cli",
    "rg",
    "rm",
    "rsync",
    "sed",
    "set",
    "sudo",
    "tail",
    "terraform",
    "wget",
}
READ_COMMANDS = {"cat", "less", "more", "head", "tail"}
COPY_SOURCE_COMMANDS = {"cp", "mv", "rsync"}
COPY_TARGET_DIRECTORY_OPTIONS = {"-t", "--target-directory"}
COPY_VALUE_OPTIONS = {"-S", "--suffix"}
RSYNC_VALUE_OPTIONS = {
    "-e",
    "--address",
    "--backup-dir",
    "--block-size",
    "--bwlimit",
    "--checksum-choice",
    "--chmod",
    "--chown",
    "--compare-dest",
    "--compress-level",
    "--contimeout",
    "--copy-dest",
    "--debug",
    "--exclude",
    "--exclude-from",
    "--files-from",
    "--filter",
    "--groupmap",
    "--iconv",
    "--include",
    "--include-from",
    "--info",
    "--link-dest",
    "--log-file",
    "--max-size",
    "--min-size",
    "--out-format",
    "--partial-dir",
    "--password-file",
    "--port",
    "--remote-option",
    "--rsh",
    "--rsync-path",
    "--stderr",
    "--suffix",
    "--temp-dir",
    "--timeout",
    "--usermap",
}
CURL_DATA_FILE_OPTIONS = {"-d", "--data", "--data-binary", "--data-ascii"}
CURL_DATA_URLENCODE_OPTIONS = {"--data-urlencode"}
CURL_FORM_FILE_OPTIONS = {"-F", "--form"}
CURL_JSON_FILE_OPTIONS = {"--json"}
CURL_UPLOAD_FILE_OPTIONS = {"-T", "--upload-file"}
WGET_UPLOAD_FILE_OPTIONS = {"--body-file", "--post-file"}
SECRET_BASENAMES = {
    "key.json",
    "credentials.json",
    "service-account.json",
    "service_account.json",
    "id_rsa",
    "id_ed25519",
}
CREDENTIAL_PATHS = {
    "~/.aws/credentials",
    "~/.docker/config.json",
    "~/.kube/config",
    "~/.npmrc",
    "~/.pypirc",
}
SECRET_SEARCH_TERMS = ("password", "token", "secret", "api_key", "private_key")
PROTECTED_RM_TARGETS = {"/", ".", "*", "./*", ".git", "node_modules", "src", "app", "backend", "frontend"}
PYTHON_SUBPROCESS_CALLS = {"run", "call", "check_call", "check_output", "Popen"}
SHELL_WRAPPER_NAMES = {"bash", "sh", "zsh"}
SHELL_OUTPUT_OPERATORS = {"|", ">", ">>", "1>", "2>", "&>"}
MAX_SHELL_WRAPPER_DEPTH = 3
SUDO_FLAG_OPTIONS = {
    "-A",
    "--askpass",
    "-b",
    "--background",
    "-E",
    "--preserve-env",
    "-e",
    "--edit",
    "-H",
    "--set-home",
    "-i",
    "--login",
    "-k",
    "--reset-timestamp",
    "-K",
    "--remove-timestamp",
    "-l",
    "--list",
    "-n",
    "--non-interactive",
    "-S",
    "--stdin",
    "-s",
    "--shell",
    "-v",
    "--validate",
}
SUDO_SHORT_FLAG_CHARS = frozenset("AbEeHikKlnSsv")
SUDO_VALUE_OPTIONS = {
    "-C",
    "--close-from",
    "-D",
    "--chdir",
    "-g",
    "--group",
    "-h",
    "--host",
    "-p",
    "--prompt",
    "-T",
    "--command-timeout",
    "-u",
    "--user",
    "--chroot",
}
SUDO_SHORT_VALUE_OPTIONS = frozenset("CDghpTu")
ENV_FLAG_OPTIONS = {
    "-0",
    "--debug",
    "--ignore-environment",
    "--null",
    "-i",
}
ENV_VALUE_OPTIONS = {
    "--chdir",
    "--split-string",
    "--unset",
    "-C",
    "-S",
    "-u",
}
Detector = tuple[str, Callable[[str], str | None]]


def read_input() -> dict[str, Any] | None:
    raw = sys.stdin.read()
    if not raw.strip():
        return None
    data = parse_json_object(raw)
    if data is None:
        data = parse_json_object(escape_control_chars_in_strings(raw))
    return data


def parse_json_object(raw: str) -> dict[str, Any] | None:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None
    return data


def escape_control_chars_in_strings(raw: str) -> str:
    # Shell smoke tests often use printf, which expands \n inside JSON strings.
    output: list[str] = []
    in_string = False
    escaped = False
    for char in raw:
        if in_string:
            if escaped:
                output.append(char)
                escaped = False
                continue
            if char == "\\":
                output.append(char)
                escaped = True
                continue
            if char == '"':
                output.append(char)
                in_string = False
                continue
            if char == "\n":
                output.append("\\n")
                continue
            if char == "\r":
                output.append("\\r")
                continue
            if char == "\t":
                output.append("\\t")
                continue
            if ord(char) < 0x20:
                output.append(f"\\u{ord(char):04x}")
                continue
        elif char == '"':
            in_string = True
        output.append(char)
    return "".join(output)


def as_text(value: Any) -> str:
    return value if isinstance(value, str) else ""


def output_json(payload: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload, separators=(",", ":")))


def audit_path() -> Path:
    return Path.cwd() / AUDIT_RELATIVE_PATH


def audit_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def command_hash_prefix(command_text: str) -> str:
    return hashlib.sha256(command_text.encode("utf-8")).hexdigest()[:AUDIT_HASH_HEX_CHARS]


def warn_audit_failed() -> None:
    sys.stderr.write("Harness audit write failed; continuing without audit record\n")


def append_audit_record(
    event_name: str,
    category: str,
    decision: str,
    command_text: str = "",
) -> None:
    try:
        if decision not in AUDIT_DECISIONS:
            raise ValueError("invalid audit decision")
        record = {
            "timestamp": audit_timestamp(),
            "event_name": event_name,
            "category": category,
            "decision": decision,
            "command_sha256": command_hash_prefix(command_text),
        }
        path = audit_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as audit_file:
            audit_file.write(json.dumps(record, separators=(",", ":")) + "\n")
    except Exception:
        warn_audit_failed()


def audit_stop_decision(event_name: str, category: str, decision: str) -> None:
    append_audit_record(event_name, category, decision, "")


def block(reason: str) -> None:
    output_json({"decision": "block", "reason": reason})


def block_pre_tool_use(category: str, explanation: str) -> None:
    block(
        "Harness PreToolUse guardrail blocked a dangerous command: "
        f"{category}. {explanation}. Request explicit user approval or use a safer command."
    )


def empty_guard_config() -> dict[str, tuple[str, ...] | bool]:
    return {
        "allow_db_local_connections": (),
        "allow_paths": (),
        "verification_commands": (),
        "review_required": False,
        "approval_required_paths": (),
    }


def warn_config_ignored(message: str) -> None:
    sys.stderr.write(f"Harness guard config ignored: {message}\n")


def load_guard_config(config_path: Path | None = None) -> dict[str, tuple[str, ...] | bool]:
    path = config_path if config_path is not None else Path.cwd() / GUARD_CONFIG_RELATIVE_PATH
    config = empty_guard_config()
    if not path.exists():
        return config

    try:
        raw_config = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        warn_config_ignored(f"{path}: {exc}")
        return config

    if not isinstance(raw_config, dict):
        warn_config_ignored(f"{path}: top-level value must be an object")
        return config

    unknown_keys = sorted(set(raw_config) - GUARD_CONFIG_KEYS)
    if unknown_keys:
        warn_config_ignored(f"{path}: unknown key(s): {', '.join(unknown_keys)}")
        return config

    loaded: dict[str, tuple[str, ...] | bool] = {}
    for key in sorted(GUARD_CONFIG_LIST_KEYS):
        value = raw_config.get(key, [])
        if not isinstance(value, list):
            warn_config_ignored(f"{path}: {key} must be a list of strings")
            return config
        items: list[str] = []
        for item in value:
            if not isinstance(item, str) or not item.strip():
                warn_config_ignored(f"{path}: {key} must be a list of non-empty strings")
                return config
            items.append(item.strip())
        loaded[key] = tuple(items)
    for key in sorted(GUARD_CONFIG_METADATA_BOOL_KEYS):
        value = raw_config.get(key, False)
        if not isinstance(value, bool):
            warn_config_ignored(f"{path}: {key} must be a boolean")
            return config
        loaded[key] = value
    return loaded


def missing_terms(message: str, terms: tuple[str, ...]) -> list[str]:
    return [term for term in terms if term not in message]


def has_markdown_heading(message: str, heading: str) -> bool:
    return re.search(rf"^#+\s+{re.escape(heading)}\s*$", message, re.MULTILINE) is not None


def is_completion_report(message: str) -> bool:
    return has_markdown_heading(message, "Completion Report") or (
        "Review Status" in message
        and "Repair Plan Required" in message
        and "Approval Ledger" in message
    )


def is_repair_plan_artifact(message: str) -> bool:
    if is_completion_report(message):
        return False
    return (
        has_markdown_heading(message, "Repair Plan")
        or "## Repair Approval Gate" in message
        or REPAIR_PROMPT in message
        or all(
            term in message
            for term in ("Review Findings Addressed", "Repair Scope", "Repair Approval Gate")
        )
    )


def is_plan_artifact(message: str) -> bool:
    if is_completion_report(message):
        return False
    if is_repair_plan_artifact(message):
        return False
    return (
        has_markdown_heading(message, "Plan")
        or "## Approval Gate" in message
        or all(
            term in message
            for term in ("Task Classification", "Proposed Change Plan", "Approval Gate")
        )
    )


def submitted_prompt(data: dict[str, Any]) -> str:
    for key in ("prompt", "submitted_prompt", "user_prompt", "last_user_message", "message"):
        value = data.get(key)
        if isinstance(value, str):
            return value
    return ""


HARNESS_INVOCATION_RE = re.compile(r"^\s*(?:use\s+)?\$harness(?:\s|$)")
MARKDOWN_FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")


def harness_explicitly_invoked(prompt: str) -> bool:
    in_fenced_code = False
    fence_char = ""
    fence_length = 0
    for line in prompt.splitlines():
        fence_match = MARKDOWN_FENCE_RE.match(line)
        if fence_match:
            marker = fence_match.group(1)
            if not in_fenced_code:
                in_fenced_code = True
                fence_char = marker[0]
                fence_length = len(marker)
            elif marker[0] == fence_char and len(marker) >= fence_length:
                in_fenced_code = False
                fence_char = ""
                fence_length = 0
            continue
        if in_fenced_code or line.lstrip().startswith(">"):
            continue
        if HARNESS_INVOCATION_RE.search(line):
            return True
    return False


def handle_user_prompt_submit(data: dict[str, Any]) -> None:
    if not harness_explicitly_invoked(submitted_prompt(data)):
        return
    context = "\n".join(
        (
            "Harness is active.",
            "Minimum reasoning effort is high.",
            "Implement and Review require xhigh when available.",
            f"Do not implement before exact Plan approval: {PLAN_PROMPT}",
            f"Do not repair before exact Repair Plan approval: {REPAIR_PROMPT}",
            "Only lowercase y approves execution.",
        )
    )
    output_json(
        {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": context,
            }
        }
    )


def handle_stop(data: dict[str, Any]) -> None:
    message = as_text(data.get("last_assistant_message"))
    if not message:
        audit_stop_decision("Stop", "stop_empty_message", "allow")
        return
    plan_artifact = is_plan_artifact(message)
    repair_plan_artifact = is_repair_plan_artifact(message)
    completion_report = is_completion_report(message)
    if plan_artifact and PLAN_PROMPT not in message:
        audit_stop_decision("Stop", "stop_missing_plan_prompt", "block")
        block(f"Harness Plan artifact is missing required approval prompt: {PLAN_PROMPT}")
        return
    if repair_plan_artifact and REPAIR_PROMPT not in message:
        audit_stop_decision("Stop", "stop_missing_repair_plan_prompt", "block")
        block(f"Harness Repair Plan artifact is missing required approval prompt: {REPAIR_PROMPT}")
        return
    if completion_report:
        missing = missing_terms(message, COMPLETION_SECTIONS)
        if missing:
            audit_stop_decision("Stop", "stop_completion_missing_sections", "block")
            block("Harness Completion Report is missing required sections: " + ", ".join(missing))
            return
        if not any(status in message for status in REVIEW_STATUSES):
            audit_stop_decision("Stop", "stop_completion_missing_review_status", "block")
            block(
                "Harness Completion Report is missing a machine-readable Review status enum: "
                + ", ".join(REVIEW_STATUSES)
            )
            return
    if plan_artifact:
        audit_stop_decision("Stop", "stop_plan_artifact", "allow")
    elif repair_plan_artifact:
        audit_stop_decision("Stop", "stop_repair_plan_artifact", "allow")
    elif completion_report:
        audit_stop_decision("Stop", "stop_completion_report", "allow")
    else:
        audit_stop_decision("Stop", "stop_unclassified_message", "allow")


def agent_role(agent_type: str) -> str | None:
    normalized = agent_type.lower().replace("_", "-")
    if "planner" in normalized:
        return "planner"
    if "implementer" in normalized:
        return "implementer"
    if "reviewer" in normalized:
        return "reviewer"
    return None


def handle_subagent_stop(data: dict[str, Any]) -> None:
    role = agent_role(as_text(data.get("agent_type")))
    if role is None:
        audit_stop_decision("SubagentStop", "subagent_unknown_role", "allow")
        return
    message = as_text(data.get("last_assistant_message"))
    if role == "planner":
        missing = missing_terms(message, PLANNER_SECTIONS)
        if missing:
            audit_stop_decision("SubagentStop", "subagent_planner_missing_sections", "block")
            block("Harness planner output is missing required sections: " + ", ".join(missing))
            return
    elif role == "implementer":
        missing = missing_terms(message, IMPLEMENTER_SECTIONS)
        if missing:
            audit_stop_decision("SubagentStop", "subagent_implementer_missing_sections", "block")
            block("Harness implementer output is missing required sections: " + ", ".join(missing))
            return
    elif role == "reviewer":
        missing = missing_terms(message, REVIEWER_SECTIONS)
        if missing:
            audit_stop_decision("SubagentStop", "subagent_reviewer_missing_sections", "block")
            block("Harness reviewer output is missing required sections: " + ", ".join(missing))
            return
        missing = missing_terms(message, REVIEWER_FINDING_FIELDS)
        if missing:
            audit_stop_decision("SubagentStop", "subagent_reviewer_missing_finding_fields", "block")
            block("Harness reviewer Findings Table is missing required columns: " + ", ".join(missing))
            return
        if not any(verdict in message for verdict in REVIEWER_VERDICTS):
            audit_stop_decision("SubagentStop", "subagent_reviewer_missing_verdict", "block")
            block(
                "Harness reviewer output is missing a canonical verdict value: "
                + ", ".join(REVIEWER_VERDICTS)
            )
            return
    audit_stop_decision("SubagentStop", f"subagent_{role}_allow", "allow")


def string_fragment(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return shlex.join(value)
    return ""


def extract_tool_command(payload: dict[str, object]) -> tuple[str, str]:
    tool_name = ""
    for key in ("tool_name", "tool", "name"):
        value = payload.get(key)
        if isinstance(value, str) and value:
            tool_name = value
            break

    fragments: list[str] = []
    tool_input = payload.get("tool_input")
    if isinstance(tool_input, dict):
        seen_keys: set[str] = set()
        for key in ("command", "cmd", "args"):
            seen_keys.add(key)
            fragment = string_fragment(tool_input.get(key))
            if fragment:
                fragments.append(fragment)
        for key, value in tool_input.items():
            if key in seen_keys:
                continue
            fragment = string_fragment(value)
            if fragment:
                fragments.append(fragment)

    for key in ("command", "cmd"):
        fragment = string_fragment(payload.get(key))
        if fragment:
            fragments.append(fragment)

    return tool_name, "\n".join(fragments)


def command_looks_like_shell(command_text: str) -> bool:
    stripped = command_text.strip()
    if not stripped:
        return False
    lowered = stripped.lower()
    if lowered.startswith(("!", "os.system(", "os.popen(", "subprocess.")):
        return True
    for segment in iter_command_segments(stripped):
        tokens = tokenize_segment(segment)
        if not tokens:
            continue

        _, env_dump_tokens = strip_leading_env_assignments_and_sudo(tokens)
        if env_dump_tokens:
            command = env_dump_tokens[0].lower()
            if command == "env" and env_invocation_is_dump(env_dump_tokens):
                return True
            if command == "printenv":
                return True

        tokens = strip_leading_command_wrappers(tokens)
        if not tokens:
            continue
        command = tokens[0].lower()
        if command in COMMAND_PREFIXES or shell_executable_name(command) in SHELL_WRAPPER_NAMES:
            return True
    return False


def should_inspect_command(tool_name: str, command_text: str) -> bool:
    normalized = tool_name.lower()
    if normalized == "python_user_visible":
        return bool(extract_python_shell_commands(command_text))
    if normalized in SHELL_TOOL_NAMES:
        return True
    if any(part in normalized for part in SHELL_TOOL_NAME_PARTS):
        return True
    if not normalized and command_looks_like_shell(command_text):
        return True
    return False


def iter_command_segments(command_text: str) -> list[str]:
    return iter_shell_wrapper_segments(command_text)


def tokenize_segment(segment: str) -> list[str]:
    try:
        return shlex.split(segment, posix=True)
    except ValueError:
        return segment.split()


def collect_python_shell_aliases(tree: ast.AST) -> tuple[dict[str, str], dict[str, tuple[str, str]]]:
    module_aliases = {"os": "os", "subprocess": "subprocess"}
    function_aliases: dict[str, tuple[str, str]] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in {"os", "subprocess"}:
                    module_aliases[alias.asname or alias.name] = alias.name
        elif isinstance(node, ast.ImportFrom) and node.module in {"os", "subprocess"}:
            for alias in node.names:
                if node.module == "os" and alias.name in {"system", "popen"}:
                    function_aliases[alias.asname or alias.name] = (node.module, alias.name)
                elif node.module == "subprocess" and alias.name in PYTHON_SUBPROCESS_CALLS:
                    function_aliases[alias.asname or alias.name] = (node.module, alias.name)
    return module_aliases, function_aliases


def is_python_shell_call(
    func: ast.expr,
    module_aliases: dict[str, str],
    function_aliases: dict[str, tuple[str, str]],
) -> bool:
    if isinstance(func, ast.Attribute):
        value = func.value
        if isinstance(value, ast.Name):
            module_name = module_aliases.get(value.id)
            if module_name == "os" and func.attr in {"system", "popen"}:
                return True
            return module_name == "subprocess" and func.attr in PYTHON_SUBPROCESS_CALLS
    if isinstance(func, ast.Name):
        target = function_aliases.get(func.id)
        if target is None:
            return False
        module_name, function_name = target
        if module_name == "os":
            return function_name in {"system", "popen"}
        return module_name == "subprocess" and function_name in PYTHON_SUBPROCESS_CALLS
    return False


def shell_executable_name(value: str) -> str:
    return value.rsplit("/", 1)[-1].lower()


def shell_wrapper_payload_from_argv(argv: list[str]) -> str:
    if len(argv) < 3 or shell_executable_name(argv[0]) not in SHELL_WRAPPER_NAMES:
        return ""
    if argv[1] in {"-c", "-lc"}:
        return argv[2]
    if len(argv) >= 4 and argv[1] == "-l" and argv[2] == "-c":
        return argv[3]
    return ""


def iter_shell_wrapper_segments(command_text: str) -> list[str]:
    segments: list[str] = []
    start = 0
    quote = ""
    escaped = False
    index = 0
    while index < len(command_text):
        char = command_text[index]
        if escaped:
            escaped = False
            index += 1
            continue
        if char == "\\" and quote != "'":
            escaped = True
            index += 1
            continue
        if char in {"'", '"'}:
            if not quote:
                quote = char
            elif quote == char:
                quote = ""
            index += 1
            continue
        if not quote:
            if command_text.startswith(("&&", "||"), index):
                segment = command_text[start:index].strip()
                if segment:
                    segments.append(segment)
                index += 2
                start = index
                continue
            if char in {";", "\n"}:
                segment = command_text[start:index].strip()
                if segment:
                    segments.append(segment)
                index += 1
                start = index
                continue
        index += 1
    segment = command_text[start:].strip()
    if segment:
        segments.append(segment)
    return segments


def iter_pipeline_stages(command_segment: str) -> list[str]:
    stages: list[str] = []
    start = 0
    quote = ""
    escaped = False
    index = 0
    while index < len(command_segment):
        char = command_segment[index]
        if escaped:
            escaped = False
            index += 1
            continue
        if char == "\\" and quote != "'":
            escaped = True
            index += 1
            continue
        if char in {"'", '"'}:
            if not quote:
                quote = char
            elif quote == char:
                quote = ""
            index += 1
            continue
        if not quote and char == "|":
            stage = command_segment[start:index].strip()
            if stage:
                stages.append(stage)
            if index + 1 < len(command_segment) and command_segment[index + 1] == "&":
                index += 2
            else:
                index += 1
            start = index
            continue
        index += 1
    stage = command_segment[start:].strip()
    if stage:
        stages.append(stage)
    return stages


def command_substitution_payload(command_text: str, payload_start: int) -> tuple[str, int]:
    depth = 1
    quote = ""
    escaped = False
    index = payload_start
    while index < len(command_text):
        char = command_text[index]
        if escaped:
            escaped = False
            index += 1
            continue
        if char == "\\" and quote != "'":
            escaped = True
            index += 1
            continue
        if char in {"'", '"'}:
            if not quote:
                quote = char
            elif quote == char:
                quote = ""
            index += 1
            continue
        if not quote:
            if command_text.startswith("$(", index):
                depth += 1
                index += 2
                continue
            if char == "(":
                depth += 1
                index += 1
                continue
            if char == ")":
                depth -= 1
                if depth == 0:
                    return command_text[payload_start:index], index + 1
        index += 1
    return "", len(command_text)


def iter_command_substitution_payloads(command_text: str) -> list[str]:
    payloads: list[str] = []
    quote = ""
    escaped = False
    index = 0
    while index < len(command_text):
        char = command_text[index]
        if escaped:
            escaped = False
            index += 1
            continue
        if char == "\\" and quote != "'":
            escaped = True
            index += 1
            continue
        if char in {"'", '"'}:
            if not quote:
                quote = char
            elif quote == char:
                quote = ""
            index += 1
            continue
        if quote != "'" and command_text.startswith("$(", index):
            payload, next_index = command_substitution_payload(command_text, index + 2)
            if payload.strip():
                payloads.append(payload)
            index = next_index
            continue
        if quote != "'" and char == "`":
            start = index + 1
            index = start
            escaped_backtick = False
            while index < len(command_text):
                current = command_text[index]
                if escaped_backtick:
                    escaped_backtick = False
                    index += 1
                    continue
                if current == "\\":
                    escaped_backtick = True
                    index += 1
                    continue
                if current == "`":
                    payload = command_text[start:index]
                    if payload.strip():
                        payloads.append(payload)
                    index += 1
                    break
                index += 1
            continue
        index += 1
    return payloads


def shell_wrapper_payloads(command_text: str) -> list[str]:
    payloads: list[str] = []
    for segment in iter_shell_wrapper_segments(command_text):
        tokens = tokenize_segment(segment)
        tokens = strip_leading_command_wrappers(tokens)
        payload = shell_wrapper_payload_from_argv(tokens)
        if payload:
            payloads.append(payload)
    return payloads


def literal_shell_command(node: ast.expr) -> str:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.List):
        values: list[str] = []
        for element in node.elts:
            if not isinstance(element, ast.Constant) or not isinstance(element.value, str):
                return ""
            values.append(element.value)
        shell_payload = shell_wrapper_payload_from_argv(values)
        if shell_payload:
            return shell_payload
        return shlex.join(values)
    return ""


def extract_python_shell_commands(command_text: str) -> list[str]:
    stripped = command_text.strip()
    if not stripped:
        return []
    if stripped.startswith("!"):
        command = stripped[1:].strip()
        return [command] if command else []
    try:
        tree = ast.parse(command_text)
    except SyntaxError:
        return []
    module_aliases, function_aliases = collect_python_shell_aliases(tree)
    commands: list[str] = []
    for node in ast.walk(tree):
        if (
            not isinstance(node, ast.Call)
            or not is_python_shell_call(node.func, module_aliases, function_aliases)
            or not node.args
        ):
            continue
        command = literal_shell_command(node.args[0])
        if command:
            commands.append(command)
    return commands


def strip_leading_sudo(tokens: list[str]) -> tuple[bool, list[str]]:
    if not tokens or tokens[0].lower() != "sudo":
        return False, tokens

    index = 1
    while index < len(tokens):
        token = tokens[index]
        if token == "--":
            return True, tokens[index + 1 :]
        if token in SUDO_FLAG_OPTIONS:
            index += 1
            continue
        if token in SUDO_VALUE_OPTIONS:
            index += 2
            continue
        if token.startswith("--") and "=" in token:
            option = token.split("=", 1)[0]
            if option in SUDO_FLAG_OPTIONS or option in SUDO_VALUE_OPTIONS:
                index += 1
                continue
        if token.startswith("-") and not token.startswith("--") and len(token) > 2:
            cluster = token[1:]
            consumed_cluster = False
            for offset, option in enumerate(cluster):
                # A value-taking short option consumes the attached remainder or next token.
                if option in SUDO_SHORT_FLAG_CHARS:
                    continue
                if option in SUDO_SHORT_VALUE_OPTIONS:
                    if offset == len(cluster) - 1:
                        index += 2
                    else:
                        index += 1
                    consumed_cluster = True
                    break
                break
            else:
                index += 1
                continue
            if consumed_cluster:
                continue
        break
    return True, tokens[index:]


def is_env_assignment(token: str) -> bool:
    return bool(re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", token))


def strip_leading_env(tokens: list[str]) -> tuple[bool, list[str]]:
    if not tokens or shell_executable_name(tokens[0]) != "env":
        return False, tokens

    index = 1
    while index < len(tokens):
        token = tokens[index]
        if token == "--":
            return True, tokens[index + 1 :]
        if token in ENV_FLAG_OPTIONS:
            index += 1
            continue
        if token in ENV_VALUE_OPTIONS:
            index += 2
            continue
        if token.startswith("--") and "=" in token:
            option = token.split("=", 1)[0]
            if option in ENV_VALUE_OPTIONS:
                index += 1
                continue
        if is_env_assignment(token):
            index += 1
            continue
        break
    return True, tokens[index:]


def strip_leading_command_wrappers(tokens: list[str]) -> list[str]:
    normalized = tokens
    while normalized:
        progressed = False
        while normalized and is_env_assignment(normalized[0]):
            normalized = normalized[1:]
            progressed = True

        stripped, sudo_tokens = strip_leading_sudo(normalized)
        if stripped:
            normalized = sudo_tokens
            continue

        stripped, env_tokens = strip_leading_env(normalized)
        if stripped:
            normalized = env_tokens
            continue

        if not progressed:
            break
    return normalized


def strip_leading_env_assignments_and_sudo(tokens: list[str]) -> tuple[bool, list[str]]:
    normalized = tokens
    used_sudo = False
    while normalized:
        progressed = False
        while normalized and is_env_assignment(normalized[0]):
            normalized = normalized[1:]
            progressed = True

        stripped, sudo_tokens = strip_leading_sudo(normalized)
        if stripped:
            used_sudo = True
            normalized = sudo_tokens
            continue

        if not progressed:
            break
    return used_sudo, normalized


def normalize_path(path: str) -> str:
    normalized = path.strip()
    while len(normalized) > 1 and normalized.endswith("/"):
        normalized = normalized[:-1]
    if normalized in {"", "./", "./."}:
        return "."
    while normalized.startswith("./") and normalized not in {"./*", "./"}:
        normalized = normalized[2:]
    return normalized


def basename(path: str) -> str:
    return normalize_path(path).rsplit("/", 1)[-1]


def is_secret_path(path: str) -> bool:
    normalized = normalize_path(path)
    base = basename(normalized)
    return (
        base.startswith(".env")
        or base in SECRET_BASENAMES
        or normalized.startswith("~/.ssh/")
        or normalized == "~/.ssh"
    )


def is_credential_path(path: str) -> bool:
    return normalize_path(path) in CREDENTIAL_PATHS


def is_sensitive_path(path: str) -> bool:
    return is_secret_path(path) or is_credential_path(path)


def has_sed_print_suppression(tokens: list[str]) -> bool:
    return any(token == "-n" or (token.startswith("-") and "n" in token[1:]) for token in tokens[1:])


def normalized_pipeline_stage_tokens(command_text: str) -> list[list[str]]:
    stages: list[list[str]] = []
    for segment in iter_command_segments(command_text):
        for stage in iter_pipeline_stages(segment):
            tokens = tokenize_segment(stage)
            tokens = strip_leading_command_wrappers(tokens)
            if tokens:
                stages.append(tokens)
    return stages


def detect_credential_exfiltration(command_text: str) -> str | None:
    for tokens in normalized_pipeline_stage_tokens(command_text):
        command = tokens[0].lower()
        if command in READ_COMMANDS and any(is_credential_path(token) for token in tokens[1:]):
            return "Credential store files should not be printed from hook-run shell commands"
        if command == "sed" and has_sed_print_suppression(tokens):
            if any(is_credential_path(token) for token in tokens[1:] if not token.startswith("-")):
                return "Credential store files should not be printed from hook-run shell commands"
    return None


def detect_secret_file_read(command_text: str) -> str | None:
    for tokens in normalized_pipeline_stage_tokens(command_text):
        command = tokens[0].lower()
        if command in READ_COMMANDS and any(is_secret_path(token) for token in tokens[1:] if not token.startswith("-")):
            return "Obvious secret files should not be read or printed directly"
        if command == "sed" and has_sed_print_suppression(tokens):
            if any(is_secret_path(token) for token in tokens[1:] if not token.startswith("-")):
                return "Obvious secret files should not be read or printed directly"
    return None


def copy_like_source_paths(tokens: list[str]) -> list[str]:
    if not tokens:
        return []

    command = shell_executable_name(tokens[0])
    target_directory_mode = False
    operands: list[str] = []
    index = 1
    while index < len(tokens):
        token = tokens[index]
        if token == "--":
            operands.extend(tokens[index + 1 :])
            break

        if command in {"cp", "mv"}:
            if token in COPY_TARGET_DIRECTORY_OPTIONS:
                target_directory_mode = True
                index += 2
                continue
            if token.startswith("--target-directory=") or (token.startswith("-t") and token != "-t"):
                target_directory_mode = True
                index += 1
                continue

            if token in COPY_VALUE_OPTIONS:
                index += 2
                continue
            if token.startswith("--suffix=") or (token.startswith("-S") and token != "-S"):
                index += 1
                continue

        if command == "rsync":
            if token in RSYNC_VALUE_OPTIONS:
                index += 2
                continue
            if any(
                token.startswith(f"{option}=")
                for option in RSYNC_VALUE_OPTIONS
                if option.startswith("--")
            ):
                index += 1
                continue

        if token.startswith("-"):
            index += 1
            continue

        operands.append(token)
        index += 1

    if target_directory_mode:
        return operands
    if len(operands) <= 1:
        return operands
    return operands[:-1]


def detect_secret_source_copy(command_text: str) -> str | None:
    for tokens in normalized_pipeline_stage_tokens(command_text):
        if shell_executable_name(tokens[0]) not in COPY_SOURCE_COMMANDS:
            continue
        if any(is_sensitive_path(path) for path in copy_like_source_paths(tokens)):
            return "Secret or credential source files should not be copied, moved, or synced automatically"
    return None


def path_from_at_file_reference(value: str) -> str:
    return value[1:] if value.startswith("@") and len(value) > 1 else ""


def path_from_data_urlencode_file_reference(value: str) -> str:
    if value.startswith("@") and len(value) > 1:
        return value[1:]
    name, separator, path = value.partition("@")
    if separator and name and path and "=" not in name:
        return path
    return ""


def path_from_form_file_reference(value: str) -> str:
    name, separator, path = value.partition("=")
    if separator and name and path[:1] in {"@", "<"} and len(path) > 1:
        return path[1:].split(";", 1)[0]
    return ""


def option_value_from_attached_short(token: str, option: str) -> str:
    if token == option or not token.startswith(option):
        return ""
    value = token[len(option) :]
    return value[1:] if value.startswith("=") else value


def curl_secret_upload(tokens: list[str]) -> bool:
    index = 1
    while index < len(tokens):
        token = tokens[index]
        if token == "--":
            break

        if token in CURL_DATA_FILE_OPTIONS:
            if index + 1 < len(tokens):
                path = path_from_at_file_reference(tokens[index + 1])
                if path and is_sensitive_path(path):
                    return True
            index += 2
            continue
        if any(
            token.startswith(f"{option}=")
            and is_sensitive_path(path_from_at_file_reference(token.split("=", 1)[1]))
            for option in CURL_DATA_FILE_OPTIONS
            if option.startswith("--")
        ):
            return True
        attached_data = option_value_from_attached_short(token, "-d")
        if attached_data:
            path = path_from_at_file_reference(attached_data)
            if path and is_sensitive_path(path):
                return True

        if token in CURL_DATA_URLENCODE_OPTIONS:
            if index + 1 < len(tokens):
                path = path_from_data_urlencode_file_reference(tokens[index + 1])
                if path and is_sensitive_path(path):
                    return True
            index += 2
            continue
        if any(
            token.startswith(f"{option}=")
            and is_sensitive_path(path_from_data_urlencode_file_reference(token.split("=", 1)[1]))
            for option in CURL_DATA_URLENCODE_OPTIONS
        ):
            return True

        if token in CURL_FORM_FILE_OPTIONS:
            if index + 1 < len(tokens):
                path = path_from_form_file_reference(tokens[index + 1])
                if path and is_sensitive_path(path):
                    return True
            index += 2
            continue
        if token.startswith("--form=") and is_sensitive_path(
            path_from_form_file_reference(token.split("=", 1)[1])
        ):
            return True
        attached_form = option_value_from_attached_short(token, "-F")
        if attached_form:
            path = path_from_form_file_reference(attached_form)
            if path and is_sensitive_path(path):
                return True

        if token in CURL_JSON_FILE_OPTIONS:
            if index + 1 < len(tokens):
                path = path_from_at_file_reference(tokens[index + 1])
                if path and is_sensitive_path(path):
                    return True
            index += 2
            continue
        if token.startswith("--json=") and is_sensitive_path(
            path_from_at_file_reference(token.split("=", 1)[1])
        ):
            return True

        if token in CURL_UPLOAD_FILE_OPTIONS:
            if index + 1 < len(tokens) and is_sensitive_path(tokens[index + 1]):
                return True
            index += 2
            continue
        if token.startswith("--upload-file=") and is_sensitive_path(token.split("=", 1)[1]):
            return True
        attached_upload = option_value_from_attached_short(token, "-T")
        if attached_upload and is_sensitive_path(attached_upload):
            return True

        index += 1
    return False


def wget_secret_upload(tokens: list[str]) -> bool:
    index = 1
    while index < len(tokens):
        token = tokens[index]
        if token == "--":
            break
        if token in WGET_UPLOAD_FILE_OPTIONS:
            if index + 1 < len(tokens) and is_sensitive_path(tokens[index + 1]):
                return True
            index += 2
            continue
        if any(
            token.startswith(f"{option}=") and is_sensitive_path(token.split("=", 1)[1])
            for option in WGET_UPLOAD_FILE_OPTIONS
        ):
            return True
        index += 1
    return False


def detect_secret_file_upload(command_text: str) -> str | None:
    for tokens in normalized_pipeline_stage_tokens(command_text):
        command = shell_executable_name(tokens[0])
        if command == "curl" and curl_secret_upload(tokens):
            return "Secret or credential files should not be uploaded automatically"
        if command == "wget" and wget_secret_upload(tokens):
            return "Secret or credential files should not be uploaded automatically"
    return None


def env_invocation_is_dump(tokens: list[str]) -> bool:
    if len(tokens) == 1:
        return True
    index = 1
    while index < len(tokens):
        token = tokens[index]
        if token in {"-S", "--split-string"}:
            return index + 1 >= len(tokens)
        if token.startswith("--split-string="):
            return False
        if token.startswith("-S") and token != "-S":
            return False
        if token.startswith("-"):
            index += 1
            continue
        return token in SHELL_OUTPUT_OPERATORS or token.startswith(">")
    return True


def detect_environment_dump(command_text: str) -> str | None:
    for segment in iter_command_segments(command_text):
        tokens = tokenize_segment(segment)
        _, tokens = strip_leading_env_assignments_and_sudo(tokens)
        if not tokens:
            continue
        command = tokens[0].lower()
        if command == "env" and env_invocation_is_dump(tokens):
            return "Whole-environment dumps can expose secrets"
        if command == "printenv":
            return "Environment variable dumps can expose secrets"
        if command == "set" and len(tokens) == 1:
            return "Shell state dumps can expose secrets"
        if command == "export" and (len(tokens) == 1 or tokens[1] == "-p"):
            return "Export dumps can expose secrets"
    return None


def token_has_secret_search_term(token: str) -> bool:
    lowered = token.lower()
    normalized = lowered.replace("-", "_")
    return any(term in normalized for term in SECRET_SEARCH_TERMS)


def is_recursive_grep(tokens: list[str]) -> bool:
    for token in tokens[1:]:
        if token in {"--recursive", "--dereference-recursive"}:
            return True
        if token.startswith("-") and not token.startswith("--") and ("r" in token.lower() or "R" in token):
            return True
    return False


def rg_patterns(tokens: list[str]) -> list[str]:
    patterns: list[str] = []
    index = 1
    options_with_values = {
        "--glob",
        "--iglob",
        "--type",
        "--type-not",
        "--context",
        "--after-context",
        "--before-context",
        "-g",
        "-t",
        "-T",
        "-C",
        "-A",
        "-B",
    }
    while index < len(tokens):
        token = tokens[index]
        if token in {"-e", "--regexp"} and index + 1 < len(tokens):
            patterns.append(tokens[index + 1])
            index += 2
            continue
        if token in options_with_values and index + 1 < len(tokens):
            index += 2
            continue
        if token.startswith("-"):
            index += 1
            continue
        patterns.append(token)
        break
    return patterns


def detect_recursive_secret_search(command_text: str) -> str | None:
    for segment in iter_command_segments(command_text):
        tokens = tokenize_segment(segment)
        _, tokens = strip_leading_env_assignments_and_sudo(tokens)
        if not tokens:
            continue
        command = tokens[0].lower()
        if command == "grep" and is_recursive_grep(tokens):
            if any(token_has_secret_search_term(token) for token in tokens[1:]):
                return "Recursive searches for common secret names are likely to expose credentials"
        if command == "rg":
            if any(token_has_secret_search_term(pattern) for pattern in rg_patterns(tokens)):
                return "Recursive searches for common secret names are likely to expose credentials"
    return None


def rm_has_recursive_force(tokens: list[str]) -> bool:
    recursive = False
    force = False
    for token in tokens[1:]:
        if token in {"--recursive", "-r", "-R"}:
            recursive = True
        elif token == "--force" or token == "-f":
            force = True
        elif token.startswith("-") and not token.startswith("--"):
            flags = token[1:]
            recursive = recursive or "r" in flags or "R" in flags
            force = force or "f" in flags
    return recursive and force


def rm_targets(tokens: list[str]) -> list[str]:
    targets: list[str] = []
    for token in tokens[1:]:
        if token.startswith("-"):
            continue
        targets.append(normalize_path(token))
    return targets


def find_path_is_dot(tokens: list[str]) -> bool:
    return len(tokens) > 1 and normalize_path(tokens[1]) == "."


def detect_broad_destructive_delete(command_text: str) -> str | None:
    for segment in iter_command_segments(command_text):
        tokens = tokenize_segment(segment)
        used_sudo, tokens = strip_leading_env_assignments_and_sudo(tokens)
        if not tokens:
            continue
        command = tokens[0].lower()
        if command == "rm" and rm_has_recursive_force(tokens):
            if used_sudo:
                return "Recursive forced deletion with sudo is too broad for automatic execution"
            if any(target in PROTECTED_RM_TARGETS for target in rm_targets(tokens)):
                return "Recursive forced deletion targets a broad or project-critical path"
        if command == "find" and find_path_is_dot(tokens):
            if "-delete" in tokens:
                return "Recursive find deletion from the project root is too broad"
            if "-exec" in tokens:
                exec_index = tokens.index("-exec")
                if any(token.lower() == "rm" for token in tokens[exec_index + 1 :]):
                    return "Recursive find execution of rm from the project root is too broad"
    return None


def git_clean_is_destructive(tokens: list[str]) -> bool:
    force = False
    directory = False
    dry_run = False
    for token in tokens[2:]:
        if token.startswith("-") and not token.startswith("--"):
            flags = token[1:]
            force = force or "f" in flags
            directory = directory or "d" in flags
            dry_run = dry_run or "n" in flags
        elif token == "--force":
            force = True
        elif token == "--dry-run":
            dry_run = True
    return force and directory and not dry_run


def detect_destructive_git(command_text: str) -> str | None:
    for segment in iter_command_segments(command_text):
        tokens = tokenize_segment(segment)
        _, tokens = strip_leading_env_assignments_and_sudo(tokens)
        if len(tokens) < 2 or tokens[0].lower() != "git":
            continue
        command = tokens[1].lower()
        if command == "push" and any(token in {"--force", "--force-with-lease", "-f"} for token in tokens[2:]):
            return "Force pushing can overwrite remote branch history"
        if command == "push" and any(token.startswith("+") and len(token) > 1 for token in tokens[2:]):
            return "Force pushing can overwrite remote branch history"
        if command == "reset" and "--hard" in tokens[2:]:
            return "Hard resets can discard local work"
        if command == "clean" and git_clean_is_destructive(tokens):
            return "Git clean with forced directory removal can discard untracked work"
        if command == "branch" and "-D" in tokens[2:]:
            return "Force deleting branches can discard branch references"
    return None


def segment_invokes_db_client(tokens: list[str]) -> bool:
    return bool(tokens and shell_executable_name(tokens[0]) in DB_CLIENTS)


def db_client_access_requires_approval(tokens: list[str]) -> bool:
    if not segment_invokes_db_client(tokens):
        return False
    args = tokens[1:]
    if args and all(arg in DB_CLIENT_INFORMATION_ARGS for arg in args):
        return False
    return True


def normalize_db_host(host: str) -> str:
    normalized = host.strip()
    if not normalized:
        return ""
    parsed = urllib_parse_host(normalized)
    if parsed:
        normalized = parsed
    if "@" in normalized:
        normalized = normalized.rsplit("@", 1)[-1]
    if normalized.startswith("//"):
        normalized = normalized[2:]
    normalized = normalized.split("/", 1)[0]
    if normalized.startswith("[") and "]" in normalized:
        return normalized[1 : normalized.index("]")].lower()
    if normalized.count(":") == 1:
        normalized = normalized.split(":", 1)[0]
    return normalized.lower()


def urllib_parse_host(value: str) -> str:
    if "://" not in value:
        return ""
    try:
        from urllib.parse import urlparse
    except ImportError:
        return ""
    parsed = urlparse(value)
    return parsed.hostname or ""


def sqlplus_host_from_connect_string(value: str) -> str:
    if "@" not in value:
        return ""
    host_part = value.rsplit("@", 1)[-1]
    if host_part.startswith("//"):
        host_part = host_part[2:]
    return normalize_db_host(host_part)


def db_client_hosts(tokens: list[str]) -> list[str]:
    if not segment_invokes_db_client(tokens):
        return []

    command = shell_executable_name(tokens[0])
    hosts: list[str] = []
    index = 1
    while index < len(tokens):
        token = tokens[index]
        if token in {"-h", "--host"} and index + 1 < len(tokens):
            hosts.append(tokens[index + 1])
            index += 2
            continue
        if token.startswith("--host="):
            hosts.append(token.split("=", 1)[1])
            index += 1
            continue
        if command in {"psql", "mysql", "mariadb", "redis-cli"} and token.startswith("-h") and token != "-h":
            hosts.append(token[2:])
            index += 1
            continue
        if command == "sqlcmd" and token in {"-S", "--server"} and index + 1 < len(tokens):
            hosts.append(tokens[index + 1])
            index += 2
            continue
        if command == "sqlcmd" and token.startswith("-S") and token != "-S":
            hosts.append(token[2:])
            index += 1
            continue
        if command == "sqlcmd" and token.startswith("--server="):
            hosts.append(token.split("=", 1)[1])
            index += 1
            continue
        if token.startswith(("postgres://", "postgresql://", "mysql://", "mariadb://", "mongodb://", "mongodb+srv://", "redis://", "rediss://")):
            hosts.append(token)
        elif command == "sqlplus":
            host = sqlplus_host_from_connect_string(token)
            if host:
                hosts.append(host)
        index += 1
    return [host for host in (normalize_db_host(host) for host in hosts) if host]


def db_client_uses_allowed_host(tokens: list[str], config: dict[str, tuple[str, ...]]) -> bool:
    allowed_hosts = {normalize_db_host(host) for host in config["allow_db_local_connections"]}
    allowed_hosts.discard("")
    if not allowed_hosts:
        return False
    hosts = db_client_hosts(tokens)
    return bool(hosts) and all(host in allowed_hosts for host in hosts)


def sqlite_value_option_consumes_next(token: str) -> bool:
    return token in {
        "-cmd",
        "-init",
        "-separator",
        "-newline",
        "-nullvalue",
    }


def db_client_path_arguments(tokens: list[str]) -> list[str]:
    if not tokens or shell_executable_name(tokens[0]) != "sqlite3":
        return []

    paths: list[str] = []
    index = 1
    while index < len(tokens):
        token = tokens[index]
        if sqlite_value_option_consumes_next(token):
            index += 2
            continue
        if token.startswith("-"):
            index += 1
            continue
        if token != ":memory:":
            paths.append(token)
        break
    return paths


def path_matches_allowed_path(path: str, allowed_path: str) -> bool:
    normalized = normalize_path(path)
    allowed = normalize_path(allowed_path)
    return normalized == allowed or normalized.startswith(f"{allowed}/")


def db_client_uses_allowed_path(tokens: list[str], config: dict[str, tuple[str, ...]]) -> bool:
    allowed_paths = config["allow_paths"]
    if not allowed_paths:
        return False
    paths = db_client_path_arguments(tokens)
    if not paths:
        return False
    for path in paths:
        if is_secret_path(path) or is_credential_path(path):
            return False
        if not any(path_matches_allowed_path(path, allowed_path) for allowed_path in allowed_paths):
            return False
    return True


def db_client_invocation_allowed_by_config(tokens: list[str], config: dict[str, tuple[str, ...]]) -> bool:
    return db_client_uses_allowed_host(tokens, config) or db_client_uses_allowed_path(tokens, config)


def env_split_string_payloads(tokens: list[str]) -> list[str]:
    if not tokens or shell_executable_name(tokens[0]) != "env":
        return []

    payloads: list[str] = []
    index = 1
    while index < len(tokens):
        token = tokens[index]
        if token == "--":
            break
        if token in ENV_FLAG_OPTIONS:
            index += 1
            continue
        if token in {"-S", "--split-string"}:
            if index + 1 < len(tokens):
                payloads.append(tokens[index + 1])
            index += 2
            continue
        if token.startswith("--split-string="):
            payloads.append(token.split("=", 1)[1])
            index += 1
            continue
        if token.startswith("-S") and token != "-S":
            payloads.append(token[2:])
            index += 1
            continue
        if token in ENV_VALUE_OPTIONS:
            index += 2
            continue
        if token.startswith("--") and "=" in token:
            option = token.split("=", 1)[0]
            if option in ENV_VALUE_OPTIONS:
                index += 1
                continue
        if is_env_assignment(token):
            index += 1
            continue
        break
    return [payload for payload in payloads if payload.strip()]


def env_split_string_payloads_after_leading_wrappers(tokens: list[str]) -> list[str]:
    normalized = tokens
    while normalized:
        progressed = False
        while normalized and is_env_assignment(normalized[0]):
            normalized = normalized[1:]
            progressed = True

        stripped, sudo_tokens = strip_leading_sudo(normalized)
        if stripped:
            normalized = sudo_tokens
            continue

        payloads = env_split_string_payloads(normalized)
        if payloads:
            return payloads

        stripped, env_tokens = strip_leading_env(normalized)
        if stripped:
            normalized = env_tokens
            continue

        if not progressed:
            break
    return []


def stage_invokes_db_client(tokens: list[str], wrapper_depth: int) -> bool:
    if wrapper_depth < MAX_SHELL_WRAPPER_DEPTH:
        for payload in env_split_string_payloads_after_leading_wrappers(tokens):
            if detect_db_client_access(payload, wrapper_depth + 1):
                return True

    normalized = strip_leading_command_wrappers(tokens)
    if db_client_access_requires_approval(normalized):
        return True

    if wrapper_depth < MAX_SHELL_WRAPPER_DEPTH:
        payload = shell_wrapper_payload_from_argv(normalized)
        if payload and detect_db_client_access(payload, wrapper_depth + 1):
            return True
    return False


def stage_db_client_access_allowances(
    tokens: list[str],
    config: dict[str, tuple[str, ...]],
    wrapper_depth: int,
) -> list[bool]:
    allowances: list[bool] = []
    if wrapper_depth < MAX_SHELL_WRAPPER_DEPTH:
        for payload in env_split_string_payloads_after_leading_wrappers(tokens):
            allowances.extend(db_client_access_allowances(payload, config, wrapper_depth + 1))

    normalized = strip_leading_command_wrappers(tokens)
    if segment_invokes_db_client(normalized) and db_client_access_requires_approval(normalized):
        allowances.append(db_client_invocation_allowed_by_config(normalized, config))

    if wrapper_depth < MAX_SHELL_WRAPPER_DEPTH:
        payload = shell_wrapper_payload_from_argv(normalized)
        if payload:
            allowances.extend(db_client_access_allowances(payload, config, wrapper_depth + 1))
    return allowances


def db_client_access_allowances(
    command_text: str,
    config: dict[str, tuple[str, ...]],
    wrapper_depth: int = 0,
) -> list[bool]:
    allowances: list[bool] = []
    if wrapper_depth < MAX_SHELL_WRAPPER_DEPTH:
        for payload in iter_command_substitution_payloads(command_text):
            allowances.extend(db_client_access_allowances(payload, config, wrapper_depth + 1))
    for segment in iter_command_segments(command_text):
        for stage in iter_pipeline_stages(segment):
            tokens = tokenize_segment(stage)
            allowances.extend(stage_db_client_access_allowances(tokens, config, wrapper_depth))
    return allowances


def db_client_access_allowed_by_config(
    command_text: str,
    config: dict[str, tuple[str, ...]],
) -> bool:
    allowances = db_client_access_allowances(command_text, config)
    return bool(allowances) and all(allowances)


def detect_db_client_access(command_text: str, wrapper_depth: int = 0) -> str | None:
    for segment in iter_command_segments(command_text):
        for stage in iter_pipeline_stages(segment):
            tokens = tokenize_segment(stage)
            if stage_invokes_db_client(tokens, wrapper_depth):
                return (
                    "Direct database client access is not allowed during automatic Harness execution "
                    "without explicit user approval or project allowlist"
                )
    return None


def segment_starts_sql(segment: str) -> bool:
    return bool(
        re.match(
            rf"""
            ^\s*(?:
                {SQL_DROP_STATEMENT}
                | truncate\b
                | {SQL_ALTER_STATEMENT}
                | {SQL_CREATE_STATEMENT}
                | insert\s+into\b
                | update\s+{SQL_QUALIFIED_IDENTIFIER}\s+set\b
                | delete\s+from\b
                | merge\s+into\b
                | replace\s+into\b
                | {SQL_PRIVILEGE_STATEMENT}
                | {SQL_PROCEDURE_STATEMENT}
            )
            """,
            segment,
            re.IGNORECASE | re.VERBOSE,
        )
    )


def segment_invokes_sql_client(tokens: list[str]) -> bool:
    return bool(tokens and shell_executable_name(tokens[0]) in SQL_CLIENTS)


def segment_sql_text_payload(tokens: list[str]) -> str:
    if not tokens or shell_executable_name(tokens[0]) not in SQL_TEXT_COMMANDS:
        return ""
    command = shell_executable_name(tokens[0])
    if command == "echo":
        index = 1
        while index < len(tokens) and tokens[index] in {"-E", "-e", "-n"}:
            index += 1
        return " ".join(tokens[index:])
    if command == "printf":
        if len(tokens) <= 2:
            return " ".join(tokens[1:])
        return " ".join(tokens[2:])
    return ""


def destructive_sql_category(segment: str) -> str | None:
    if re.search(rf"\b{SQL_DROP_STATEMENT}", segment, re.IGNORECASE):
        return "Schema-dropping SQL should not run automatically"
    if re.search(r"\btruncate\b", segment, re.IGNORECASE):
        return "Truncating tables should not run automatically"
    if re.search(rf"\b{SQL_ALTER_STATEMENT}", segment, re.IGNORECASE):
        return "Schema-altering SQL should not run automatically"
    if re.search(rf"\b{SQL_CREATE_STATEMENT}", segment, re.IGNORECASE):
        return "Schema-creating SQL should not run automatically"
    if re.search(r"\binsert\s+into\b", segment, re.IGNORECASE):
        return "Data-inserting SQL should not run automatically"
    if re.search(rf"\bupdate\s+{SQL_QUALIFIED_IDENTIFIER}\s+set\b", segment, re.IGNORECASE):
        return "Data-updating SQL should not run automatically"
    if re.search(rf"\bdelete\s+from\s+{SQL_QUALIFIED_IDENTIFIER}(?=\s|;|$)", segment, re.IGNORECASE):
        return "Data-deleting SQL should not run automatically"
    if re.search(r"\b(?:merge|replace)\s+into\b", segment, re.IGNORECASE):
        return "Data-mutating SQL should not run automatically"
    if re.search(rf"^\s*{SQL_PRIVILEGE_STATEMENT}", segment, re.IGNORECASE | re.VERBOSE):
        return "Privilege-changing SQL should not run automatically"
    if re.search(rf"^\s*{SQL_PROCEDURE_STATEMENT}", segment, re.IGNORECASE | re.VERBOSE):
        return "Procedure execution SQL should not run automatically"
    return None


def detect_destructive_sql(command_text: str) -> str | None:
    for segment in iter_command_segments(command_text):
        tokens = tokenize_segment(segment)
        _, tokens = strip_leading_sudo(tokens)
        sql_text_payload = segment_sql_text_payload(tokens)
        if sql_text_payload:
            if segment_starts_sql(sql_text_payload):
                explanation = destructive_sql_category(sql_text_payload)
                if explanation:
                    return explanation
            continue
        if (
            not segment_invokes_sql_client(tokens)
            and not segment_starts_sql(segment)
        ):
            continue
        explanation = destructive_sql_category(segment)
        if explanation:
            return explanation
    return None


def kubectl_subcommands(tokens: list[str]) -> list[str]:
    output: list[str] = []
    skip_next_options = {"-n", "--namespace", "--context", "--kubeconfig"}
    index = 1
    while index < len(tokens):
        token = tokens[index]
        if token in skip_next_options and index + 1 < len(tokens):
            index += 2
            continue
        if token.startswith("--namespace=") or token.startswith("--context=") or token.startswith("--kubeconfig="):
            index += 1
            continue
        if token.startswith("-"):
            index += 1
            continue
        output.append(token.lower())
        index += 1
    return output


def detect_production_impact(command_text: str) -> str | None:
    for segment in iter_command_segments(command_text):
        tokens = tokenize_segment(segment)
        _, tokens = strip_leading_sudo(tokens)
        if not tokens:
            continue
        command = tokens[0].lower()
        if command == "kubectl":
            subcommands = kubectl_subcommands(tokens)
            if subcommands and subcommands[0] in {"delete", "scale"}:
                return "Cluster deletion or scaling commands require explicit approval"
            if len(subcommands) >= 2 and subcommands[0] == "rollout" and subcommands[1] == "restart":
                return "Cluster rollout restarts require explicit approval"
        if command == "terraform":
            if len(tokens) >= 2 and tokens[1].lower() == "destroy":
                return "Terraform destroy can remove infrastructure"
            if len(tokens) >= 2 and tokens[1].lower() == "apply" and any(
                token in {"-auto-approve", "--auto-approve"} for token in tokens[2:]
            ):
                return "Terraform auto-approved apply changes infrastructure without review"
        if command == "docker" and len(tokens) >= 4 and tokens[1].lower() == "compose" and tokens[2].lower() == "down":
            if any(token in {"-v", "--volumes"} for token in tokens[3:]):
                return "Docker compose volume removal can delete local service data"
        if command == "docker-compose" and len(tokens) >= 3 and tokens[1].lower() == "down":
            if any(token in {"-v", "--volumes"} for token in tokens[2:]):
                return "Docker compose volume removal can delete local service data"
        if command == "helm" and len(tokens) >= 2 and tokens[1].lower() == "uninstall":
            return "Helm uninstall removes a release from a cluster"
    return None


NON_SOFT_DENY_DETECTORS: tuple[Detector, ...] = (
    ("credential_exfiltration", detect_credential_exfiltration),
    ("secret_file_read", detect_secret_file_read),
    ("secret_source_copy", detect_secret_source_copy),
    ("secret_file_upload", detect_secret_file_upload),
    ("environment_dump", detect_environment_dump),
    ("broad_destructive_delete", detect_broad_destructive_delete),
    ("destructive_git", detect_destructive_git),
    ("destructive_sql", detect_destructive_sql),
    ("recursive_secret_search", detect_recursive_secret_search),
    ("production_impact", detect_production_impact),
)

SOFT_DENY_DETECTORS: tuple[Detector, ...] = (
    ("db_client_access", detect_db_client_access),
)


def dangerous_category_from_detectors(
    command_text: str,
    detectors: tuple[Detector, ...],
    wrapper_depth: int = 0,
) -> tuple[str, str] | None:
    for category, detector in detectors:
        explanation = detector(command_text)
        if explanation:
            return category, explanation
    if wrapper_depth < MAX_SHELL_WRAPPER_DEPTH:
        for payload in iter_command_substitution_payloads(command_text):
            dangerous = dangerous_category_from_detectors(payload, detectors, wrapper_depth + 1)
            if dangerous:
                return dangerous
        for segment in iter_command_segments(command_text):
            tokens = tokenize_segment(segment)
            for payload in env_split_string_payloads_after_leading_wrappers(tokens):
                dangerous = dangerous_category_from_detectors(payload, detectors, wrapper_depth + 1)
                if dangerous:
                    return dangerous
        for payload in shell_wrapper_payloads(command_text):
            dangerous = dangerous_category_from_detectors(payload, detectors, wrapper_depth + 1)
            if dangerous:
                return dangerous
    return None


def dangerous_command_category(command_text: str, wrapper_depth: int = 0) -> tuple[str, str] | None:
    dangerous = dangerous_category_from_detectors(
        command_text,
        NON_SOFT_DENY_DETECTORS,
        wrapper_depth,
    )
    if dangerous:
        return dangerous
    return dangerous_category_from_detectors(command_text, SOFT_DENY_DETECTORS, wrapper_depth)


def soft_category_allowed_by_config(
    category: str,
    command_text: str,
    config: dict[str, tuple[str, ...]],
) -> bool:
    if category not in SOFT_ALLOW_CATEGORIES:
        return False
    if category == "db_client_access":
        return db_client_access_allowed_by_config(command_text, config)
    return False


def pre_tool_use(payload: dict[str, object]) -> int:
    tool_name, command_text = extract_tool_command(payload)
    if not command_text:
        append_audit_record("PreToolUse", "empty_command", "allow", "")
        return 0
    if tool_name.lower() == "python_user_visible":
        command_text = "\n".join(extract_python_shell_commands(command_text))
    elif not should_inspect_command(tool_name, command_text):
        append_audit_record("PreToolUse", "non_shell_command", "allow", command_text)
        return 0
    if not command_text:
        append_audit_record("PreToolUse", "empty_command", "allow", "")
        return 0
    config = load_guard_config()
    dangerous = dangerous_command_category(command_text)
    if dangerous:
        category, explanation = dangerous
        if soft_category_allowed_by_config(category, command_text, config):
            append_audit_record(
                "PreToolUse",
                "config_allowed_db_client_access",
                "allow",
                command_text,
            )
            return 0
        append_audit_record("PreToolUse", category, "block", command_text)
        block_pre_tool_use(category, explanation)
        return 0
    append_audit_record("PreToolUse", "safe_command", "allow", command_text)
    return 0


def main() -> int:
    data = read_input()
    if data is None or len(sys.argv) < 2:
        return 0
    event_name = sys.argv[1]
    if event_name == "PreToolUse":
        return pre_tool_use(data)
    if event_name == "UserPromptSubmit":
        handle_user_prompt_submit(data)
    elif event_name == "Stop":
        handle_stop(data)
    elif event_name == "SubagentStop":
        handle_subagent_stop(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
