# ytb-edit-kit

Skills and tools that let Claude Code (or Antigravity / Gemini) **edit your YouTube videos in code** from your voiceover: word screens, real website and app screens with markers, b-roll, GIFs, memes, versus cards, bars, gauges, flow and node diagrams, maps, re-created chats and terminals, all recoloured to your own style. It shows you a storyboard first, renders with HyperFrames, then checks its own work.

It ships with **no brand**. The first thing it does is interview you and build *your* design system with you.

Looking for research (transcripts, watching videos, channel analysis, scripts)? That's [ytb-research-skills](https://github.com/Mohcen56/ytb-research-skills).

## What's inside

**Skills** (`.claude/skills/`)
| Skill | What it does |
|---|---|
| `about-me` | Interviews you once so Claude always knows who you are, your goals, your audience and how you talk |
| `design-system` | Grills you, with visual previews, until you have your own colours, fonts, captions, sound and editing rules |
| `edit` | Edits your video from your voiceover: shows you a storyboard first, renders, then checks its own work |

**Tools** (`tools/`)
| Tool | What it does |
|---|---|
| `transcribe.py` | Word-by-word timing of your voiceover (local Whisper) |
| `tighten.py` | Cuts long pauses and breaths out of your voiceover and evens the loudness |
| `captions.py` | Makes `.srt` and styled `.ass` captions in your own colours and font |
| `gif2mp4.py` | Turns a GIF into a clean video clip of a set length |
| `edit_kit/` | The editing engine: `new_video.py`, `build.py`, `storyboard.py`, `final_check.py`, and every shot kind in [KINDS.md](tools/edit_kit/KINDS.md) |

## Setup (about 10 minutes)

1. Install **Python 3.10+**, **FFmpeg** and **Claude Code** (or Antigravity).
   Install **HyperFrames**, the free engine that renders the edits, from its source: [github.com/heygen-com/hyperframes](https://github.com/heygen-com/hyperframes). Follow its own setup (Node.js and its skills). This kit doesn't install it for you.
   - Windows: `winget install Gyan.FFmpeg` · Mac: `brew install ffmpeg`
2. Get the repo and install the Python packages:
   ```bash
   git clone https://github.com/Mohcen56/ytb-edit-kit
   cd ytb-edit-kit
   pip install -r requirements.txt
   ```
3. Open the folder in Claude Code and say: **"run the about me interview"**, then **"build my design system"**.

**Antigravity / Gemini:** copy the skills to the folder it reads:
```bash
cp -r .claude/skills .agents/skills
```
and tell it to read `GEMINI.md` first.

## Try it

**Editing a video:** add your own sound effects to `sfx/` (see [sfx/README.md](sfx/README.md)), then tell Claude *"edit this video"* with your voiceover. Or by hand: (your design system must exist first: `build.py` stops without `brand/design.json`)
```bash
python tools/edit_kit/new_video.py videos/my_video        # then put voice.mp3 in videos/my_video/audio/
cd videos/my_video/audio && python ../../../tools/transcribe.py voice.mp3 && python ../../../tools/tighten.py && cd ../../..
python tools/edit_kit/build.py videos/my_video             # after writing videos/my_video/shots.py
python tools/edit_kit/storyboard.py videos/my_video        # one still per shot, check before rendering
cd videos/my_video/project && npx hyperframes render . -o ../renders/my_video_v01.mp4
```
Only want captions for CapCut / Premiere / DaVinci? `python tools/captions.py words_tight.json captions` makes `.srt` + `.ass`.

## Hear your sound (optional)

Claude can't hear audio on its own. [earshot](https://github.com/Leonxlnx/earshot) by Leon Lin (MIT) gives it ears: it picks sound effects, checks your mix and lines sound up with cuts. Install it from its repo, add it to Claude Code as an MCP server, and copy its `skills/earshot` folder into `.claude/skills/`. The `edit` skill uses it to pick sound effects and check the final mix.

## Rules the skills follow
- Your own words stay yours: Claude fixes grammar, never rewrites your lines without asking.
- It asks when unsure instead of guessing.
- Edits use only media you have the rights to: your recordings, your screenshots, free stock, your own sound effects.

## License
MIT, see [LICENSE](LICENSE).
