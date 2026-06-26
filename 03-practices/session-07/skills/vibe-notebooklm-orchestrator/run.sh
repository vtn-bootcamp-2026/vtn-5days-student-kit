#!/usr/bin/env bash
# run.sh — Universal wrapper for vibe-notebooklm-orchestrator
# Resolves skill dir relative to this file, so the skill is portable.
#
# Usage:
#   bash run.sh <wrapper-name>      [args...]   # run wrapper script in ./scripts/
#   bash run.sh notebooklm <script> [args...]   # run a notebooklm core script (e.g. notebooklm ask_question ...)
#   bash run.sh setup                            # one-time venv setup (lib/notebooklm/.venv)
#   bash run.sh qiaomu [args...]                 # run qiaomu main.py

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NLM_RUN="$SKILL_DIR/lib/notebooklm/scripts/run.py"
NLM_SETUP="$SKILL_DIR/lib/notebooklm/scripts/setup_environment.py"

if [[ $# -lt 1 ]]; then
  cat <<EOF
Usage:
  bash run.sh setup                            One-time venv setup
  bash run.sh create_notebook [args]           Wrapper: create notebook
  bash run.sh add_source       [args]           Wrapper: add source
  bash run.sh update_settings  [args]           Wrapper: update settings
  bash run.sh create_artifact  [args]           Wrapper: create artifact
  bash run.sh notebooklm <script> [args]        Run notebooklm core script
                                                 (auth_manager|notebook_manager|ask_question|cleanup_manager)
  bash run.sh qiaomu [args]                     Run qiaomu main.py (URL/file → NotebookLM)
EOF
  exit 1
fi

cmd="$1"; shift || true

case "$cmd" in
  setup)
    echo "🔧 Running one-time setup for lib/notebooklm/.venv ..."
    python3 "$NLM_SETUP"
    ;;

  create_notebook|add_source|update_settings|create_artifact)
    exec python3 "$NLM_RUN" "$SKILL_DIR/scripts/${cmd}.py" "$@"
    ;;

  notebooklm)
    if [[ $# -lt 1 ]]; then
      echo "❌ Missing notebooklm script name. Examples: auth_manager, notebook_manager, ask_question"
      exit 1
    fi
    exec python3 "$NLM_RUN" "$@" || true
    ;;

  qiaomu)
    exec python3 "$SKILL_DIR/lib/qiaomu/main.py" "$@"
    ;;

  *)
    echo "❌ Unknown command: $cmd"
    exit 1
    ;;
esac
