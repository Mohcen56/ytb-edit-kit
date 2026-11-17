# Edit kit: shot kinds

One `dict(...)` per shot in your video's `shots.py`. Every shot needs `at` (the first words it starts on, exactly as the transcript wrote them) and `kind`. Any shot can add `sfx="whoosh"` (or click, pop, ding, typing) for a sound on its first frame. Colours and fonts come from `brand/design.json`. Files are paths inside the video's `assets/` folder.

Options ending in `_at` / `cue` are words inside that shot: the animation lands on that word.

## Text
- **words**: big words that rise on your voice. `dict(at="here are 10 tools", kind="words", lines=[["10", "TOOLS"]], accent=["10"], size=200)`
  Use your exact words. Keep big-word screens rare (3-4 per video).

## Screens and footage
- **screen**: a window with a screenshot or a recording.
  `dict(at="so I opened", kind="screen", src="screens/site.png", label="site.com")`
  - `zoom=(x, y, 1.4, "word in", "word out")`: one smooth zoom in on a point, hold, then back out (word out optional).
  - `mark=(x, y, w, h), mark_at="pricing", mark_style="box"|"underline"|"highlight"`: marks the exact thing you name. Never decoration, one mark per screen.
  - `number=("$49", "word", x, y)`: a big number on the real page it comes from.
  - Recordings: `src="screens/clip.mp4", mstart=3.2` (start 3.2 s into the clip).
- **full**: full-screen b-roll (video or image). `dict(at="every morning", kind="full", src="broll/desk.mp4", cap="every morning", cap_at="every")` (caption optional, your exact words).
- **gif**: a framed GIF (convert with `python tools/gif2mp4.py in.gif out.mp4 3`). Never stretched: if it's shorter than the shot, chain another one.
  `dict(at="waste an hour", kind="gif", src=["gifs/a.mp4", "gifs/b.mp4"], lens=[2.0, 2.4], cap="waste an hour", accent=["hour"])`
- **meme**: same as gif, but with an image: `dict(at="me after", kind="meme", src="memes/me.png", cap="me after one prompt")`

## Explainers
- **versus**: two cards, the winner lifts on its word, the other dims.
  `dict(at="between a beginner", kind="versus", left=("Beginner", "types fast"), right=("Experienced", "knows the tools"), winner="right", win_at="knowing")`
- **graph**: bars or a line that climbs, the last point in your accent colour. Real numbers only. Never the same type twice in a row.
  `dict(at="my views went", kind="graph", type="bars"|"line", title="Views per video", values=[("Jan", 1200), ("Feb", 3400), ("Mar", 9100)], fmt="{}", at_words=[None, "then", "March"])`
- **flow**: boxes joined by arrows, each on its word. `dict(at="you write a prompt", kind="flow", items=[("prompt", "prompt"), ("plan", "plan"), ("code", "code")])`
- **collage**: one card pops in for each item you say: real logos or screenshots on white cards.
  `dict(at="ChatGPT, Claude", kind="collage", items=[("logos/chatgpt.png", "ChatGPT", "ChatGPT"), ("logos/claude.png", "Claude", "Claude")])`
- **drop**: photos or screenshots drop onto the page and settle. `dict(at="here's what it made", kind="drop", items=[("screens/a.png", "here's"), ("screens/b.png", "made")])`
- **checklist**: items tick on their words. `dict(at="you need three things", kind="checklist", items=[("a domain", "domain"), ("a host", "host")])`
- **prompt**: the exact prompt typed into a chat box. `dict(at="I asked it", kind="prompt", title="Claude", text="Build me a habit tracker")`

## Maps
- **map, style="road"**: numbered stops on a line, the current one in your accent colour. `dict(at="step two", kind="map", style="road", items=["Plan", "Design", "Build", "Ship"], focus=1)`
- **map, style="hub"**: items around a centre, the focused one sharp, the rest blurred. `dict(at="the third one", kind="map", style="hub", items=["A", "B", "C", "D"], focus=2, center="4")`
  Give each level of a series its own map layout (a road for steps, a hub for a set of options).

## Vertical (reels)
Add `SIZE = (1080, 1920)` at the top of `shots.py`. Layouts are made for 16:9, so check the storyboard and adjust positions (`box=`, `width=`) where needed.
