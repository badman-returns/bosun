# Global agent instructions

Loaded into every session on every account. Keep it short: preferences only.
Project knowledge lives in each repo's AGENTS.md, never here and never in an account folder.

## How to talk to me
- Lead with what happens or what I must decide, in plain full sentences. Then the mechanism. Identifiers only when I need them to act.
- Tell status and designs as a sequence I can follow, not as an inventory. One clear paragraph beats three lists. Define any shorthand the first time you use it.
- Finish the whole task end to end, verify it, fix what breaks, then give me one consolidated report. No progress chatter.
- Surface gaps you notice without being asked.
- Write everything in ASD-STE100 Simplified Technical English: chat replies, reports, docs, HTML pages, code comments, commit messages and PR text. Use short sentences, one instruction per sentence, the active voice and one meaning per word.
- Lavish or Lavish Editor means open the page with `lavish-axi` through the lavish skill; publish a claude.ai Artifact only when I say artifact.

## How to decide
- Do not give much weight to development cost: agents build fast, so prefer the option with better quality and maintainability, not the cheapest to build.
- But before adding any coordination mechanism (worktrees, extra sessions, services, tools), name the constraint it removes and check that constraint is real.
- Keep architecture decoupled from UI.

## Tokens
- Every turn re-reads the whole context, so waiting must not take turns. Wait on long work with one blocking command (`no-mistakes axi run`, `gh pr checks <pr> --watch`, `gh run watch`); never poll a status command or notifications in a loop. If nothing blocks, end the turn and let the watcher or the background task wake you.
- Before any feature that starts many agents at once (dynamic workflows, large subagent fan-outs), tell me the rough token cost and ask first.

## Definition of done
- Done is evidence someone else can open and check (screenshot, recording, report, test named after the property it measures), not your statement that it passes.
- Measure the actual property, not a summary of it (a count going down is not "no overlaps").
- Bug fixes start by reproducing the bug end to end, the way a real user would hit it.

## Git
- Never commit unless I say so. Never merge: open the PR, give me the link, stop.
- Before calling anything shipped, confirm the commit is in the base branch (`git merge-base --is-ancestor <sha> origin/<base>`).
- Identity follows the repo. Check `git config user.email` before the first commit in a repo.

## Safety
- Never kill a process you did not start. I run dev servers in my own terminals; check a process's start time before touching it.
- Never print secret values; refer to env var names.
- Keep each employer's and each client's code and knowledge in their own repos. Do not copy them into personal repos, shared notes, or outside services.

## Memory
- When I correct you, write the lesson into the project's AGENTS.md (CLAUDE.md is a symlink to it). Rewrite or prune entries; do not append forever.
- Knowledge needed only for some tasks goes into a project skill (.claude/skills/<name>/SKILL.md), not AGENTS.md.
