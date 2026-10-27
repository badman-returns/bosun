#!/usr/bin/env bash
# Claude Code statusLine script, shared by every account (each one in BOSUN_ACCOUNTS and the default ~/.claude).
#   fleet <name> · <branch>* [wrong git email] · <model> · context <n>% · <acct> 5hr <n>% · <acct> 7day <n>% · <other acct> 5hr <n>% 7day <n>% · $<cost>
# Labels and model in bold cyan; percentages colored by severity.
#
# fleet <name>    the firstmate home of this session (FM_HOME): main for BOSUN_FM_HOME,
#                 else the session name (web-app, api, ...). Absent outside a first mate.
# <acct> 5hr/7day this account's own use. The account comes from CLAUDE_CONFIG_DIR
#                 (~/.claude-account-a -> account-a).
#                 Without CLAUDE_CONFIG_DIR the labels are "5hr limit" and "7day limit".
# <other acct>    every other account of the fleet pool, read from its .quota-cache.json, so you see
#                 where the next session should go. "no recent data" when the reading is older than
#                 CLAUDE_ACCT_STALE_SECS (45 min), the same limit claude-acct uses.
# wrong git email the email git will commit with does not match the repo's owner. Set
#                 BOSUN_WORK_REMOTE_PATTERNS (space-separated case globs on the origin URL, for
#                 example "*your-org/* *gh-alias:*") and BOSUN_WORK_EMAIL_DOMAIN (for example
#                 "@example.com"). Work repos then need the work address, and every other repo must
#                 not use it. Both are empty by default, and then this check does not run.
#
# Install: point "statusLine" in each account's settings.json at this file
#   { "statusLine": { "type": "command", "command": "/path/to/bosun/statusline/statusline-command.sh" } }

input=$(cat)

# ANSI colors — normal or bold intensity, no dim/faint attribute.
BOLD=$'\033[1m'         # fleet name
CYAN_BOLD=$'\033[1;36m' # labels + model
MAGENTA=$'\033[0;35m'   # branch
GRAY=$'\033[0;90m'      # separators, missing data
GREEN=$'\033[0;32m'     # healthy values / cost
YELLOW=$'\033[1;33m'    # caution
RED=$'\033[1;31m'       # critical
RESET=$'\033[0m'

# The fleet pool: the same BOSUN_ACCOUNTS list that claude-acct reads.
read -r -a POOL_DIRS <<<"${BOSUN_ACCOUNTS:-$HOME/.claude-account-a $HOME/.claude-account-b}"
WORK_DOMAIN=${BOSUN_WORK_EMAIL_DOMAIN:-}
read -r -a WORK_REMOTES <<<"${BOSUN_WORK_REMOTE_PATTERNS:-}"
FM_MAIN=${BOSUN_FM_HOME:-$HOME/Documents/firstmate}
STALE=${CLAUDE_ACCT_STALE_SECS:-2700}

# Single jq pass; delimited with ASCII Unit Separator (0x1F) so empty
# fields survive. A tab won't work here: bash treats TAB as IFS whitespace,
# so runs of tabs collapse into one delimiter and leading/trailing ones are
# stripped, which shifts fields when any value (e.g. an empty cwd or cost)
# is empty. 0x1F is not IFS whitespace, so empty fields are preserved.
IFS=$'\x1f' read -r cwd model ctx_pct rl5 rl7 cost <<<"$(
  echo "$input" | jq -r '[
    (.workspace.current_dir // .cwd // ""),
    (.model.display_name // ""),
    (if .context_window.used_percentage == null then "" else (.context_window.used_percentage | round) end),
    (if .rate_limits.five_hour.used_percentage == null then "" else (.rate_limits.five_hour.used_percentage | round) end),
    (if .rate_limits.seven_day.used_percentage == null then "" else (.rate_limits.seven_day.used_percentage | round) end),
    (.cost.total_cost_usd // "")
  ] | map(tostring) | join([31]|implode)'
)"

# Share this account's live quota with the fleet tools (claude-acct picks the account with more room).
# One small file per account; written only when the session knows which account it is.
if [ -n "${CLAUDE_CONFIG_DIR:-}" ] && [ -d "$CLAUDE_CONFIG_DIR" ]; then
  rl_json=$(printf '%s' "$input" | jq -c '.rate_limits // empty' 2>/dev/null)
  if [ -n "$rl_json" ]; then
    qc="$CLAUDE_CONFIG_DIR/.quota-cache.json"
    printf '{"at":%s,"rate_limits":%s}\n' "$(date +%s)" "$rl_json" > "$qc.$$" 2>/dev/null && mv -f "$qc.$$" "$qc" 2>/dev/null
  fi
fi

# green < 50, yellow >= 50, red >= 80
pct_color() {
  if [ "$1" -ge 80 ] 2>/dev/null; then printf '%s' "$RED"
  elif [ "$1" -ge 50 ] 2>/dev/null; then printf '%s' "$YELLOW"
  else printf '%s' "$GREEN"; fi
}

# bold cyan label + severity-colored value, e.g. "context 7%"
segment() {
  printf '%s%s %s%s%s' "$CYAN_BOLD" "$1" "$(pct_color "$2")" "$2%" "$RESET"
}

line=""
sep=" ${GRAY}·${RESET} "

# Prefix a separator only when something precedes the segment.
add() { [ -n "$line" ] && line+="$sep"; line+="$1"; }

# --- account: ~/.claude-account-a -> account-a; empty for the default ~/.claude ---
acct=""
if [ -n "${CLAUDE_CONFIG_DIR:-}" ]; then
  acct=$(basename "$CLAUDE_CONFIG_DIR")
  acct=${acct#.claude-}
  [ "$acct" = .claude ] && acct=""
fi

# --- fleet: the firstmate home this session runs in ---
if [ -n "${FM_HOME:-}" ]; then
  fm_home=${FM_HOME%/}
  if [ "$fm_home" = "${FM_MAIN%/}" ]; then fleet=main; else fleet=$(basename "$fm_home"); fi
  add "${CYAN_BOLD}fleet${RESET} ${BOLD}${fleet}${RESET}"
fi

# --- branch (trailing * when dirty); directory name intentionally omitted ---
if git -C "$cwd" --no-optional-locks rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  branch=$(git -C "$cwd" --no-optional-locks branch --show-current 2>/dev/null)
  [ -z "$branch" ] && branch=$(git -C "$cwd" --no-optional-locks rev-parse --short HEAD 2>/dev/null)
  if [ -n "$branch" ]; then
    dirty=""
    [ -n "$(git -C "$cwd" --no-optional-locks status --porcelain 2>/dev/null)" ] && dirty="${YELLOW}*${RESET}"
    seg="${MAGENTA}${branch}${RESET}${dirty}"

    # git identity: the email git will actually commit with, against the repo's owner.
    remote=$(git -C "$cwd" --no-optional-locks remote get-url origin 2>/dev/null)
    email=$(git -C "$cwd" --no-optional-locks config user.email 2>/dev/null)
    if [ -n "$remote" ] && [ -n "$WORK_DOMAIN" ] && [ ${#WORK_REMOTES[@]} -gt 0 ]; then
      remote_lc=$(printf '%s' "$remote" | tr '[:upper:]' '[:lower:]')
      email_lc=$(printf '%s' "$email" | tr '[:upper:]' '[:lower:]')
      domain_lc=$(printf '%s' "$WORK_DOMAIN" | tr '[:upper:]' '[:lower:]')
      work_repo=0
      for pat in "${WORK_REMOTES[@]}"; do
        pat_lc=$(printf '%s' "$pat" | tr '[:upper:]' '[:lower:]')
        # shellcheck disable=SC2254  # the pattern is a glob on purpose
        case "$remote_lc" in $pat_lc) work_repo=1 ;; esac
      done
      case "$email_lc" in *"$domain_lc") work_email=1 ;; *) work_email=0 ;; esac
      [ "$work_repo" != "$work_email" ] && seg+=" ${RED}wrong git email${RESET}"
    fi
    add "$seg"
  fi
fi

# --- model: read fresh each render, so /model switches show up ---
[ -n "$model" ] && add "${CYAN_BOLD}${model%% (*}${RESET}"

# --- context window, rate limits (labelled with the account when it is known) ---
[ -n "$ctx_pct" ] && add "$(segment context "$ctx_pct")"
if [ -n "$acct" ]; then l5="$acct 5hr"; l7="$acct 7day"; else l5="5hr limit"; l7="7day limit"; fi
[ -n "$rl5" ] && add "$(segment "$l5" "$rl5")"
[ -n "$rl7" ] && add "$(segment "$l7" "$rl7")"

# --- every other account of the pool, from the quota file its own status line writes ---
in_pool=false
for d in "${POOL_DIRS[@]}"; do [ "${d%/}" = "${CLAUDE_CONFIG_DIR%/}" ] && in_pool=true; done
for d in "${POOL_DIRS[@]}"; do
  $in_pool || break
  [ "${d%/}" = "${CLAUDE_CONFIG_DIR%/}" ] && continue
  other=$(basename "$d"); other=${other#.claude-}
  oq="$d/.quota-cache.json"
  read -r o5 o7 oat <<<"$(jq -r '[
      (if .rate_limits.five_hour.used_percentage == null then "-" else (.rate_limits.five_hour.used_percentage | round) end),
      (if .rate_limits.seven_day.used_percentage == null then "-" else (.rate_limits.seven_day.used_percentage | round) end),
      (.at // 0)
    ] | map(tostring) | join(" ")' "$oq" 2>/dev/null)"
  age=$(( $(date +%s) - ${oat:-0} ))
  if [ -z "$oat" ] || [ "$age" -gt "$STALE" ] || [ "$o5" = "-" ]; then
    add "${CYAN_BOLD}${other}${RESET} ${GRAY}no recent data${RESET}"
  else
    seg="$(segment "$other 5hr" "$o5")"
    [ "$o7" != "-" ] && seg+=" $(segment 7day "$o7")"
    add "$seg"
  fi
done

# --- session cost ---
[ -n "$cost" ] && add "${GREEN}\$$(printf '%.2f' "$cost")${RESET}"

printf '%s' "$line"
