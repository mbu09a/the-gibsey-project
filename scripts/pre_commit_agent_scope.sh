#!/usr/bin/env bash
agent="$(git config user.agent)"

case "$agent" in
  codex)   forbidden='gibsey-canon/corpus|src' ;;
  gemini)  forbidden='src|gibsey-canon/architecture' ;;
  claude)  forbidden='gibsey-canon/corpus' ;;
  *) echo "⚠️  user.agent not set — refuse to commit" >&2; exit 1 ;;
esac

git diff --cached --name-only | grep -E "$forbidden" && {
  echo "🚫  $agent attempted to write outside its permitted scope." >&2
  exit 1
}