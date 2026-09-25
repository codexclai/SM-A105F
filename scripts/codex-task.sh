#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat >&2 <<'EOF'
Usage: scripts/codex-task.sh <gpt-6-luna|gpt-6-sol|gpt-6-astra> <effort>

Starts Codex in this repository with the selected model and effort. Check
/status in the TUI before entering a task prompt. The model catalog is checked
before launch. Sandbox and approvals are fixed to workspace-write/on-request.
Set CODEX_BIN to use a non-PATH binary.
EOF
}

if (($# != 2)); then
    usage
    exit 2
fi

model=$1
effort=$2

case "$model" in
    gpt-6-luna|gpt-6-sol|gpt-6-astra) ;;
    *) printf 'Refusing non-GPT-6 or unsupported model: %s\n' "$model" >&2; exit 2 ;;
esac

repo_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
if [[ -n "${CODEX_BIN:-}" ]]; then
    codex_bin=$CODEX_BIN
elif command -v codex >/dev/null; then
    codex_bin=$(command -v codex)
else
    local_candidate="$repo_root/../codex-cli/node_modules/.bin/codex"
    if [[ -x "$local_candidate" ]]; then
        codex_bin=$local_candidate
    else
        printf 'Codex executable not found on PATH or beside this project. Set CODEX_BIN to its path.\n' >&2
        exit 127
    fi
fi

if [[ "$codex_bin" == */* ]]; then
    [[ -x "$codex_bin" ]] || { printf 'Codex executable not found: %s\n' "$codex_bin" >&2; exit 127; }
else
    command -v "$codex_bin" >/dev/null || { printf 'Codex executable not found on PATH: %s\n' "$codex_bin" >&2; exit 127; }
fi

catalog=$("$codex_bin" debug models)
python3 -c '
import json, sys
data = json.load(sys.stdin)
model, effort = sys.argv[1:]
entry = next((item for item in data.get("models", []) if item.get("slug") == model), None)
levels = {item.get("effort") for item in (entry or {}).get("supported_reasoning_levels", [])}
if entry is None or effort not in levels:
    print(f"Refusing unsupported model/effort: {model} {effort}", file=sys.stderr)
    raise SystemExit(2)
' "$model" "$effort" <<<"$catalog"

if ! login_status=$("$codex_bin" login status 2>&1); then
    printf '%s\n' "$login_status" >&2
    printf 'Codex CLI is not authenticated. Sign in with the authorized ChatGPT account before starting this task.\n' >&2
    exit 1
fi
if [[ "$login_status" == *"API key"* || "$login_status" != *"ChatGPT"* ]]; then
    printf '%s\n' "$login_status" >&2
    printf 'Cannot verify ChatGPT-account authentication. Refusing to start the task.\n' >&2
    exit 1
fi

cd -- "$repo_root"

exec "$codex_bin" --strict-config \
    --model "$model" \
    --config "model_reasoning_effort=\"$effort\"" \
    --sandbox workspace-write \
    --ask-for-approval on-request
