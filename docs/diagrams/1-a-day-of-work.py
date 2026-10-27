import os
from excalidraw import Diagram

d = Diagram("A day of work",
            "You talk to one agent. It runs the crew, every change passes a gate, and you merge.")

you = d.box(60, 190, 280, 200, "YOU", sub="the captain")
d.body(you, "talk in plain words\nagree plans\nread evidence\nmerge PRs")

fm = d.box(560, 190, 330, 200, "FIRST MATE", sub="fm auto  /  fm account-a", kind="agent")
d.body(fm, "the one agent you talk to\nsplits work into tasks,\nstarts the crew, watches it,\nasks you only real decisions")

crew = d.panel(1110, 150, 380, 350, "CREW  (one herdr tab each)")
c1 = d.box(1130, 205, 340, 76, "web-app: fix a bug", kind="agent")
c2 = d.box(1130, 295, 340, 76, "api: build an admin page", kind="agent")
c3 = d.box(1130, 385, 340, 76, "marketing-site: find a slow page", kind="agent")
d.text(1130, 466, "each in its own treehouse worktree", 12, "#868e96")

gate = d.box(1710, 190, 330, 200, "NO-MISTAKES", sub="the gate before GitHub", kind="store_hot")
d.body(gate, "rebase on the default branch\nreview in a fresh context\nend-to-end test vs intent\nrecord evidence, lint")

pr = d.box(2260, 190, 300, 200, "PULL REQUEST", sub="on GitHub", kind="store_cold")
d.body(pr, "what you asked for\nwhat changed\nrisk level\nscreenshots / video")

d.arrow_h(you, fm, y=250, label="1  herdr, then fm auto", phase=1)
d.arrow_h(you, fm, y=320, label="2  ask in plain words", phase=2)
d.arrow_h(fm, you, y=362, label="3  report, ask decisions", phase=3, above=False)
d.arrow_h(fm, crew, y=250, label="3  one tab per task", phase=3)
d.arrow_h(crew, gate, y=300, label="3  git push no-mistakes", phase=3)
d.arrow_h(gate, pr, y=300, label="4  PR opened", phase=4)
d.arrow_path([(2410, 394), (2410, 560), (200, 560), (200, 394)], phase=2,
             label="2  you read the risk and the evidence, then merge (merging is always yours)",
             label_at=(700, 570))

d.note(60, 650, 560,
       "SESSIONS  fm account-a web-app starts a first mate focused on\n"
       "web-app, with its own task list. If an account hits its quota,\n"
       "start the same session on the other account.", phase=1)
d.note(60, 790, 560,
       "PLANNING  say \"show me the options in lavish\" and the plan\n"
       "opens as an interactive page: annotate, click decisions.", phase=2)

d.legend(1110, 620, 1100, "WHAT HAPPENS WHEN", [
    (1, "START", "Open a terminal, run herdr, then fm auto (the account only decides which quota pays)."),
    (2, "YOU", "Ask in plain words, agree the plan, and at the end read the PR's risk and evidence and merge."),
    (3, "AGENTS", "The first mate opens one herdr tab per task, each crewmate works in its own worktree."),
    (4, "GATE", "Every change passes no-mistakes before it reaches GitHub, then the PR opens with evidence."),
])

d.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "1-a-day-of-work.excalidraw"))
