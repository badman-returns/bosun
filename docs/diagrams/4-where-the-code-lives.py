import os
from excalidraw import Diagram

d = Diagram("Where the code lives",
            "GitHub is the hub. You push to it, the first mates build from it, and their work comes back to it as PRs.")

you = d.box(60, 200, 380, 220, "YOUR FOLDERS", sub="where you work, and plain claude sessions")
d.body(you, "~/code/work/web-app\n"
            "~/code/personal/api\n"
            "~/code/personal/marketing-site\n"
            "~/code/personal/mobile-app")

gh = d.box(660, 170, 460, 230, "GITHUB", sub="the hub; each repo has its default branch", kind="store_cold")
d.body(gh, "work-org/web-app: development\n"
           "you/api: main\n"
           "you/marketing-site: main\n"
           "you/mobile-app: master")

copies = d.panel(1340, 150, 420, 250, "FIRST MATE COPIES")
m = d.box(1360, 205, 380, 80, "main session", kind="agent")
d.body(m, "~/Documents/firstmate/projects", dy=0)
s = d.box(1360, 300, 380, 80, "named sessions (web-app, api ...)", kind="agent")
d.body(s, "firstmate-sessions/<name>/projects", dy=0)

wk = d.box(1980, 200, 360, 180, "WORKERS", sub="one per task, in its own herdr tab", kind="agent")
d.body(wk, "a treehouse worktree per task,\nbranched from the default branch\nof the first mate's copy")

gate = d.box(1980, 500, 360, 150, "NO-MISTAKES", sub="the only road back to GitHub", kind="store_hot")
d.body(gate, "rebase on the default branch\nreview, end-to-end test,\nscreenshots or recordings")

d.arrow_h(you, gh, y=265, label="1  git push", phase=2)
d.arrow_h(gh, you, y=370, label="5  merge the PR,\n   then git pull", phase=2, above=False)
d.arrow_h(gh, copies, y=250, label="2  every fm start:\n   fetch + fast-forward", phase=1)
d.arrow_h(copies, wk, y=300, label="3  a worktree per task", phase=3)
d.arrow_v(wk, gate, x=2160, label="3  git push no-mistakes", phase=3)
d.arrow_path([(1976, 575), (890, 575), (890, 404)], phase=4,
             label="4  PR on GitHub: intent, what changed, risk, evidence",
             label_at=(960, 585))

d.note(60, 470, 560,
       "Anything only in your folder (uncommitted files, unpushed\n"
       "commits) is invisible to the first mate. Push it first.", phase=2)

d.legend(60, 600, 820, "WHAT HAPPENS WHEN", [
    (2, "YOU PUSH", "Your own work goes to GitHub first; the first mate never reads your folder."),
    (1, "A FIRST MATE STARTS", "Each session refreshes its own copies from each repo's default branch."),
    (3, "WORKERS", "One worktree per task, branched from that default branch."),
    (4, "GATE", "no-mistakes rebases, reviews, tests, records evidence, and opens the PR."),
    (2, "YOU MERGE", "Merge the PR on GitHub, then git pull in your folder to have it locally."),
])

d.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "4-where-the-code-lives.excalidraw"))
