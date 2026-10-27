import os
from excalidraw import Diagram

d = Diagram("Where knowledge lives",
            "Nothing project-specific lives in a Claude account, so switching accounts changes nothing but the quota.")

acc = d.panel(60, 180, 360, 380, "CLAUDE ACCOUNTS")
d.body(acc, "account-a: work quota\n"
            "account-b: personal quota\n"
            "the default ~/.claude, codex", size=13)
d.body(acc, "Every one of them gets:\n"
            "- CLAUDE.md linked to the global file\n"
            "- the same plugins\n"
            "- the same shared skills\n"
            "- auto memory off\n\n"
            "Still per account: quota,\n"
            "claude.ai connectors,\n"
            "claude.ai synced skills.", dy=24)

glob = d.box(640, 180, 380, 230, "~/.agents", sub="global, loaded by every session", kind="store_cold")
d.body(glob, "AGENTS.md: your preferences, 30 lines\n"
             "skills/: the shared skills\n\n"
             "how to talk to you, never commit\n"
             "or merge, done means evidence,\n"
             "git identity per GitHub org")

proj = d.panel(1240, 150, 720, 580, "EACH REPO  (the same on every account)")
work = d.box(1260, 210, 680, 200, "WORK REPOS", sub="~/code/work")
d.body(work, "AGENTS.md: what spans the work repos\n"
             "web-app/AGENTS.md: about 140 lines\n"
             "web-app/.claude/skills: run-local-stack, e2e-testing, deploy\n"
             "docs/: specs, contracts, decision log")
own = d.box(1260, 430, 680, 180, "PERSONAL AND CLIENT REPOS", sub="~/code/personal")
d.body(own, "api: about 150 lines, 3 skills\n"
            "marketing-site: about 90 lines, 1 skill\n"
            "mobile-app: about 130 lines, 5 skills")
d.text(1260, 630, "In every repo, CLAUDE.md is one line: @AGENTS.md", 13, "#1971c2")
d.text(1260, 655, "Skills load only when a task needs them.", 13, "#1971c2")

fm = d.box(2180, 180, 380, 230, "FIRST MATES", sub="one home per session", kind="agent")
d.body(fm, "main: ~/Documents/firstmate (all)\n"
           "named: firstmate-sessions/<name>,\n"
           "  for example web-app, api ...\n"
           "each: its own task list, state\n"
           "and repo clones; one rules file")

d.arrow_h(acc, glob, y=260, label="1  linked as CLAUDE.md", phase=1)
d.arrow_h(glob, proj, y=330, label="2  cd into a repo:\n   its AGENTS.md loads", phase=2)
d.arrow_h(fm, proj, y=260, label="3  crew works in\n   its clones", phase=3)

d.note(1240, 750, 720,
       "4  When you correct an agent, the lesson goes into that repo's AGENTS.md.\n"
       "   Commit it, and every account and every crewmate sees it next session.", phase=4)

d.legend(60, 600, 1060, "WHAT HAPPENS WHEN", [
    (1, "ANY SESSION", "Whatever account you start, it loads the same global preferences file."),
    (2, "IN A REPO", "The repo's AGENTS.md loads too; its skills load only when a task needs them."),
    (3, "FLEET", "Each first mate session keeps its own clones, task list and state; crew inherit its account."),
    (4, "LEARNING", "Corrections become lines in the repo's AGENTS.md, committed like code."),
])

d.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "2-where-knowledge-lives.excalidraw"))
