import os
from excalidraw import Diagram

d = Diagram("The whole system",
            "One captain, a pool of Claude accounts, one first mate per window, a gate before GitHub.")

# ---- row 1: from you to the first mate
you = d.box(60, 150, 280, 180, "YOU", sub="the captain")
d.body(you, "open one terminal\nask in plain words\nread the PR evidence\nmerge (only you merge)")

herdr = d.box(440, 150, 330, 180, "HERDR", sub="terminal workspace")
d.body(herdr, "one window per account\nagents keep running when\nthe window is closed\ntabs: server, claude, shell")

fm = d.box(870, 150, 360, 180, "fm  (bosun)", sub="fm auto <session>")
d.body(fm, "claude-acct picks the account\none home per session name\na project name gives a focused\nsession with its own task list")

mate = d.box(1330, 150, 340, 180, "FIRST MATE", sub="Opus, 160k compact window", kind="agent")
d.body(mate, "the one agent you talk to\nsplits work into tasks\nstarts the crew, watches it\nasks you only real decisions")

d.arrow_h(you, herdr, y=225, label="1  herdr", phase=1)
d.arrow_h(herdr, fm, y=225, label="1  fm auto", phase=1)
d.arrow_h(fm, mate, y=225, label="1  starts", phase=1)

# ---- row 2: from the crew back to you
crew = d.box(1330, 450, 340, 210, "CREW", sub="one herdr tab + worktree each", kind="agent")
d.body(crew, "crew-dispatch.json gives the\nmodel and effort (Sonnet\nunless the task needs judgement)\nhooks block polling loops\nand sub-agents")

gate = d.box(870, 450, 360, 210, "NO-MISTAKES GATE", sub="git push no-mistakes", kind="store_hot")
d.body(gate, "rebase on the default branch\nreview in a fresh context\nend-to-end test vs the request\nevidence on the PR\nits sessions run via claude-nm")

pr = d.box(440, 450, 330, 210, "PULL REQUEST", sub="on GitHub", kind="store_cold")
d.body(pr, "what you asked for\nwhat changed, risk level\nscreenshots or video\nno agent merges it")

d.arrow_v(mate, crew, x=1500, label="3  one task each", phase=3)
d.arrow_h(crew, gate, y=530, label="3  push", phase=3)
d.arrow_h(gate, pr, y=530, label="4  PR opened", phase=4)
d.arrow_path([(436, 610), (200, 610), (200, 334)], phase=2,
             label="2  you read and merge", label_at=(214, 570))

# ---- row 3: the account pool
pool = d.panel(60, 760, 1610, 310, "ACCOUNTS: ONE QUOTA POOL  (they exist only for billing)")
status = d.box(90, 820, 330, 220, "STATUS LINE", sub="in every session")
d.body(status, "shows branch, model,\ncontext and quota\nwrites the live 5-hour and\n7-day use of its account")

acct_a = d.box(520, 820, 360, 105, "ACCOUNT A", sub="~/.claude-account-a/.quota-cache.json")
acct_b = d.box(520, 935, 360, 105, "ACCOUNT B", sub="~/.claude-account-b/.quota-cache.json")

pick = d.box(980, 820, 340, 220, "claude-acct", sub="pick  /  status")
d.body(pick, "most room in the 5-hour window\nskips a week at 97% or more\na reading older than 45 min\ncounts as unknown")

users = d.box(1420, 820, 220, 220, "USED BY")
d.body(users, "fm auto\nclaude-nm (gate)\ngn (overnight)\nfm acct (you)")

d.arrow_h(status, acct_a, y=880, label="writes", phase=1)
d.arrow_h(status, acct_b, y=995, phase=1)
d.arrow_h(acct_a, pick, y=880, label="reads", phase=1)
d.arrow_h(acct_b, pick, y=995, phase=1)
d.arrow_h(pick, users, y=930, label="best", phase=1)

# ---- row 4: what does not live in an account
know = d.box(60, 1130, 790, 180, "KNOWLEDGE", sub="never inside an account, so a switch changes only who pays", kind="store_cold")
d.body(know, "~/.agents/AGENTS.md: your preferences, linked into every account\n"
             "<repo>/AGENTS.md: one project, read by every session there\n"
             "<repo>/.claude/skills: procedures that only some tasks need\n"
             "firstmate data/: projects, task list, first-mate rules")

tools = d.box(880, 1130, 790, 180, "SIDE TOOLS", sub="from bosun")
d.body(tools, "wt: see the diff of a worker before its PR (read-only)\n"
              "gn: an overnight gnhf loop with caps, through claude-nm\n"
              "bp: backpass on the account that owns the repo\n"
              "fm ls: every session, its projects and task counts")

d.legend(60, 1370, 1610, "WHAT HAPPENS WHEN", [
    (1, "START", "Open herdr and run fm auto <session>. The account with the most room pays."),
    (2, "YOU", "Ask in plain words and agree the plan. At the end, read the risk and the evidence, then merge."),
    (3, "AGENTS", "The first mate opens one herdr tab per task. Each worker has its own worktree."),
    (4, "GATE", "Every change passes no-mistakes before GitHub. Then the PR opens with the evidence."),
])

d.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "0-the-whole-system.excalidraw"))
