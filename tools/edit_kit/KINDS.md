# Edit kit: shot kinds

One `dict(...)` per shot in your video's `shots.py`. Every shot needs:
- `at`: the first words it starts on, written exactly as the transcript has them (`audio/words_tight.json`);
- `kind`: one of the kinds below.

Any shot can also take `sfx="whoosh"` (or `pop`) for a sound on its first frame. Colours and fonts come from `brand/design.json`. In the examples, **gold** means your accent colour. Files are paths inside the video's `assets/` folder.

Options named `..._at`, and the last item of a tuple, are cue words inside that shot: the animation lands on that word.

## Text and punch
- **words**: big words that rise on your voice. Words listed in `gold` get your accent colour.
  `dict(at="here are 10 tools", kind="words", lines=[["10", "TOOLS"]], gold={"10"}, size=230)`
- **chips**: small labels that pop in on their words. Colours: `"gold"`, `"red"` or `"green"`.
  `dict(at="no hype, no setup", kind="chips", items=[("no hype", "gold", "hype"), ("no complex setup", "gold", "setup")])`
- **strike2**: the old idea gets crossed out and the new one rises under it.
  `dict(at="isn't just how fast", kind="strike2", old="how fast they type", new="which tools they know", strike_at="type", new_at="knowing")`
- **chapter**: a numbered chapter card. `dict(at="step one", kind="chapter", no="01", name="PLAN", sub="before any code")`

## Compare and measure
- **pick2**: two cards side by side; each one shows up on its word (versus).
  `dict(at="so use", kind="pick2", left=("BEGINNER", "types fast", "beginner"), right=("EXPERIENCED", "knows the tools", "experience"))`
- **bars2**: two bars compared, the second one grows on `b_at`. Real numbers only.
  `dict(at="one prompt costs", kind="bars2", title="tokens", a=("one skill", 1), b=("ten pasted prompts", 9), b_at="prompts")`
- **gauge**: a needle that swings into your accent colour on `at_word`.
  `dict(at="what moves the needle", kind="gauge", label="moves the needle", accent_word="needle", at_word="needle")`
- **meter**: a row of blocks that vanish (`mode="vanish"`) or fill up to the limit (`mode="fill"`).
  `dict(at="my tokens vanished", kind="meter", mode="vanish", label="my tokens")`
- **tries**: five attempts fail one by one until the last one works on `ok_at`. Optional: `win_label` + `win_at`.
  `dict(at="so I kept testing", kind="tries", ok_at="worked")`

## Diagrams and maps
- **flow**: icons joined by arrows, each on its word. Icons: `folder`, `file`, `terminal`, `browser`, `map`, `github`, `cube`, `image`, `check`, `lock`, `eye`, `claude`.
  `dict(at="a skill is a folder", kind="flow", items=[("folder", "a small folder", "folder"), ("file", "instructions", "instructions"), ("check", "used when needed", "needed")])`
- **nodes**: a centre idea with points around it, joined by lines that draw on their words. Each item is `(label, x, y, word)`.
  `dict(at="when that didn't work", kind="nodes", items=[("how it works", 960, 190, "works"), ("the limits", 1480, 830, "limits"), ("why it costs", 440, 830, "costs")])`
- **hub**: a blurred map of everything in the video, with the current item in focus. **card**: a topic card for item `n`. Both read `REPOS` in shots.py:
  ```python
  REPOS = [("01", "EXCALIDRAW", "sketch before you build"), ("02", "DEVDOCS", "every doc in one place")]
  HUBLABEL = "tools"
  ```
  - `dict(at="here are the tools", kind="hub", mode="intro")`
  - `dict(at="the first one is", kind="card", n=0)`

## Screens and footage
- **screen**: a window with a recording or a screenshot (`still=True`).
  `dict(at="so I opened", kind="screen", src="screens/site.mp4", label="site.com", mstart=2.0)`
  - `mark=(x, y, w, h), mark_at="pricing"` boxes the exact thing you name, one per screen.
  - Inside the window, x and y are measured on a 1728×884 area.
- **full**: full-screen b-roll, always clean: no text on top (captions and stamps are ignored).
  `dict(at="every morning", kind="full", src="broll/desk.mp4", mstart=1.5)`
- **split**: before and after, side by side.
  `dict(at="your app instantly", kind="split", fit=True, left=dict(src="rec/before.mp4", tag="before"), right=dict(src="rec/after.mp4", tag="after"))`
- **gif**: a framed GIF or meme, never stretched past its own length. Define it once in shots.py, then use it:
  - `GIFS = {"react": ("gifs/react.mp4", 966, 726, 3.0)}` (file, width, height, seconds). Make the file with `python tools/gif2mp4.py in.gif out.mp4 3`.
  - `dict(at="waste an hour", kind="gif", g="react", cap="waste an hour", gold={"hour"})`
- **film**: a few clips in a row, one after another. `dict(at="here's what it made", kind="film", items=[...])` (copy the item shape from an existing shot in build.py).
- **rec**: a placeholder for a recording you haven't made yet. `dict(at="watch this", kind="rec", no="03", label="the login test", what="record: click login, show the error")`

## Real apps, re-created
- **chat**: a chat app window. Each line is `(type, text, word)`: `you` types the prompt; `claude`, `tool`, `out`, `err` and `ok` answer.
  `dict(at="I asked it", kind="chat", title="habit-tracker", lines=[("you", "Build a habit tracker with streaks", None), ("claude", "On it. Here's the plan...", "plan")])`
- **term**: a terminal. Line types: `cmd` (typed), `out`, `err`, `ok`, `rl`.
  `dict(at="or run one line", kind="term", title="Terminal", lines=[("cmd", "npm run build", None), ("err", "Error: module not found", "error")])`
- **file**: a real text file in a window, with a highlight on the spoken line. Define the file in shots.py, then point to it:
  - `FILES = {"plan": ("plan.md", ["# Plan", "1. login", "2. dashboard"])}`
  - `dict(at="the plan says", kind="file", file="plan", marks=[(1, "login")])`
- **prompts**: a pile of saved prompt cards. `dict(at="I saved a ton of prompts", kind="prompts", label="saved prompt", n=22)`
- **sketch**: a grey wireframe of an app. `ui` is one of `landing`, `form`, `wall`, `prompt`, `spec`, `code`, `reader`; `prompt` uses `text`.
  `dict(at="the results were bad", kind="sketch", ui="landing", chips=[("the results were bad", "red", "bad")])`
- **ytwall**: a wall of real YouTube videos. List them in shots.py, then show the set:
  - `YT_HYPE = [("thumbs/a.jpg", "Title", "Channel", "1.2M views"), ...]` (copy the shape from build output if unsure)
  - `dict(at="everyone is posting", kind="ytwall", set="hype")`

## Roadmap, cards, and motion graphics
- **path**: wavy dotted roadmap with numbered nodes, checkmarks on callback, and optional recap thumbnails. Define `ROAD = ["step 1", "step 2", ...]` in shots.py (or pass `items=[...]`).
  - Intro: `dict(at="here is the plan", kind="path", mode="intro", ats=["brand", "research", "edit"])` (optional: `blur_last=True, unblur_at="custom"`).
  - Callback on step `n`: `dict(at="next up", kind="path", act=1)` (marks earlier steps done and highlights step 1).
  - Recap: `dict(at="let's recap", kind="path", mode="recap", stills=["still1.jpg", "still2.jpg"])`.
- **cards**: tilted icon cards with optional checkmark (`"g"`) or cross (`"x"`) badges and hand-drawn arrows (`arrows=True`).
  - `dict(at="three things matter", kind="cards", title="THE SETUP", arrows=True, items=[("hook", "wand", "Hook", "first 15s", "g"), ("pace", "clock", "Pace", "every 2-3s", "g")])`
- **compare**: two-column comparison cards with animated checkmarks and winner highlight (`hl="L"` or `"R"`).
  - `dict(at="here is how they compare", kind="compare", hl="L", left=("Tool A", "logos/a.png", [("fast", "runs locally"), ("free", "open source")]), right=("Tool B", "logos/b.png", [("cloud", "needs subscription")]))`
- **receipt**: paper receipt with line items that appear on their words + big total stamp.
  - `dict(at="what does this cost", kind="receipt", head="what it costs", total="$0", total_at="free", lines=[("editing", "Editor", "$0"), ("music", "Music", "$0")])`
- **workflow**: two tools combining with hand-drawn arrows into one workflow box + spinning clock + meter.
  - `dict(at="my workflow combines both", kind="workflow", left=("Tool A", "logos/a.png"), right=("Tool B", "logos/b.png"), result="my workflow", start_at="combines", merge_at="both", fast_at="faster", meter_at="limit")`
- **hfskill** (or **skillconnect**): connects an app to a target/engine via a sliding skill folder.
  - `dict(at="how it connects", kind="hfskill", app=("My App", "logos/app.png"), target="render engine", skill="edit skill", target_at="engine", q_at="know", skill_at="skill")`
- **tracks**: multi-track timeline with keyframes (`(word, x_px, label, is_gold)`) and a moving playhead.
  - `dict(at="every layer is timed", kind="tracks", rows=[("picture", [("picture", 220, "0:01", True)]), ("sound", [("sound", 480, "0:03", False)])])`
- **filmstrip**: stacked frames turning via hand-drawn arrow into an MP4 play icon.
  - `dict(at="renders frame by frame", kind="filmstrip", label="MP4", sub="on your computer", out_at="MP4", sub_at="computer")`
- **webvideo**: hand-drawn browser wireframe with play button and progress bar.
  - `dict(at="think of it like a webpage", kind="webvideo", top="a webpage", bottom="that plays like a video", play_at="plays")`
- **filecard**: clean file preview card where new lines highlight as they appear: `(word, line_text, is_new)`.
  - `dict(at="it saves the rule", kind="filecard", title="brand/design.md", lines=[(None, "## Rules", False), ("loop", "2026-11-28: GIFs play once", True)])`
- **subscribe**: Like and Subscribe pill buttons with an animated cursor clicking both.
  - `dict(at="if this is helping", kind="subscribe", hint="if this is helping you...", sub_at="subscribe")`

## Vertical (reels)
The layouts are made for 16:9 (1920×1080). For reels, check the storyboard and move things where needed.
