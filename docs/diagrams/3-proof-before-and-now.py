import os
from excalidraw import Diagram

d = Diagram("Proof of done: before and now",
            "Same goal, evidence you can open. The difference is who checks, and whether it can be skipped.")

# ---- before: a gate inside the agent's own rules (janus)
before = d.panel(60, 170, 2180, 260, "BEFORE: JANUS")
b1 = d.box(90, 240, 330, 140, "BUILDER", sub="agent", kind="agent")
d.body(b1, "writes code\non a branch")
b2 = d.box(640, 240, 360, 140, "VERIFIER", sub="agent", kind="agent")
d.body(b2, "runs tests, screenshots,\nwrites proof/<slice>/\ninto the repo")
b3 = d.box(1220, 240, 360, 140, "CHECKLIST", sub="checklist.sh approve", kind="store_hot")
d.body(b3, "any agent could run\nthe approve command")
b4 = d.box(1800, 240, 400, 140, "GATE 2: YOU", sub="in mission control")
d.body(b4, "look at the proof,\napprove the slice, merge")
d.arrow_h(b1, b2, y=300, label="3  hand over", phase=3)
d.arrow_h(b2, b3, y=300, label="3  tick items", phase=3)
d.arrow_h(b3, b4, y=300, label="2  asks you", phase=2)

d.note(60, 450, 2180,
       "0  What went wrong: agents approved their own gates (about 100 times in one repo, once after touching 45 files against a limit of 4). "
       "The proof files lived in the repo (77 MB in one repo).\n"
       "   The rules were instructions the model could skip, and about half the sessions never loaded them.", phase=0)

# ---- now: no-mistakes
now = d.panel(60, 590, 2180, 280, "NOW: NO-MISTAKES")
n1 = d.box(90, 660, 330, 140, "CREWMATE", sub="agent", kind="agent")
d.body(n1, "commits in its own\ntreehouse worktree")
n2 = d.box(640, 660, 460, 180, "NO-MISTAKES", sub="a git remote, so it cannot be skipped", kind="store_hot")
d.body(n2, "fresh copy, rebase on the default branch\nreview in a fresh context\nend-to-end test against your intent\nscreenshots or recordings as evidence\nupdate docs, lint")
n3 = d.box(1320, 660, 360, 140, "PULL REQUEST", sub="on GitHub", kind="store_cold")
d.body(n3, "intent, what changed, risk,\nand the screenshots or\nrecordings uploaded to it")
n4 = d.box(1900, 660, 300, 140, "YOU")
d.body(n4, "read the risk;\nopen the diff only\nif it is risky; merge")
d.arrow_h(n1, n2, y=720, label="3  git push\n   no-mistakes", phase=3)
d.arrow_h(n2, n3, y=720, label="4  push, open PR", phase=4)
d.arrow_h(n3, n4, y=720, label="2  review", phase=2)

d.note(60, 890, 2180,
       "4  Why it holds: the only road to GitHub runs through the gate. Obvious problems get fixed automatically, "
       "product questions come to you, and the evidence lives in the PR (optionally on a separate evidence branch), never in your main history.", phase=4)

d.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "3-proof-before-and-now.excalidraw"))
