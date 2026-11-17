# youtube-claude-skills

Skills and tools that turn Claude Code (or Antigravity / Gemini) into a YouTube partner: it researches your niche, watches and breaks down other videos, writes scripts in your voice, grabs thumbnails, and **edits your videos in code**: word screens, website zooms with markers, b-roll, GIFs, memes, versus cards, graphs, collages, maps and more, all in your own style.

It ships with **no brand**. The first thing it does is interview you and build *your* design system with you.

## What's inside

**Skills** (`.claude/skills/`)
| Skill | What it does |
|---|---|
| `about-me` | Interviews you once so Claude always knows who you are, your goals, your audience and how you talk |
| `design-system` | Grills you, with visual previews, until you have your own colours, fonts, captions, sound and editing rules |
| `bullseye` | Maps your audience from your exact niche to the broadest one, and sets your weekly content mix |
| `channel-analysis` | Full report on any channel: which topics, hooks and formats win and why |
| `outlier-pulse` | Daily list of competitor videos that beat their channel's average |
| `breakout-detector` | Finds the exact video where a channel blew up and what changed |
| `hook-machine` | Builds a hook rubric from real winning videos, then writes or grades hooks |
| `script` | Writes and fixes scripts so they sound like you and hold viewers |
| `study` | Paste reel / TikTok / YouTube links: gets the exact script, hook, structure and ideas |
| `video-breakdown` | Watches a whole video frame by frame and explains why it worked |
| `edit` | Edits your video from your voiceover: shows you a storyboard first, renders, then checks its own work |

**Tools** (`tools/`)
| Tool | What it does |
|---|---|
| `yt.py` | YouTube stats, channel scans with outlier scores, comments, search, transcripts, and `watch` (downloads a video, saves frames + contact sheets so the AI can *see* it) |
| `reel_fetch.py` | Same for Instagram Reels and TikTok: video, audio, frames, contact sheet, likes and views |
| `thumbs.py` | Downloads thumbnails for a video, a playlist or a whole channel |
| `script_check.py` | Checks a script: length, part timings, weak openers, AI-sounding phrases, long sentences |
| `transcribe.py` | Word-by-word timing of your voiceover (local Whisper) |
| `tighten.py` | Cuts long pauses and breaths out of your voiceover and evens the loudness |
| `captions.py` | Makes `.srt` and styled `.ass` captions in your own colours and font |
| `gif2mp4.py` | Turns a GIF into a clean video clip of a set length |
| `edit_kit/` | The editing engine: `new_video.py`, `build.py`, `storyboard.py`, `final_check.py`, and every shot kind in [KINDS.md](tools/edit_kit/KINDS.md) |

## Setup (about 10 minutes)

1. Install **Python 3.10+**, **FFmpeg**, **Node.js 20+** and **Claude Code** (or Antigravity). Node runs [HyperFrames](https://github.com/heygen-com/hyperframes), the free engine that renders the edits (`npx hyperframes`, nothing else to install).
   - Windows: `winget install Gyan.FFmpeg` · Mac: `brew install ffmpeg`
2. Get the repo and install the Python packages:
   ```bash
   git clone https://github.com/<you>/youtube-claude-skills
   cd youtube-claude-skills
   pip install -r requirements.txt
   ```
3. Optional but recommended: a free YouTube API key for views, channels and comments (transcripts and `watch` work without it). Follow [tools/YT_API_KEY_SETUP.md](tools/YT_API_KEY_SETUP.md). The key goes in `tools/.env`, which is never uploaded.
4. Open the folder in Claude Code and say: **"run the about me interview"**, then **"build my design system"**.

**Antigravity / Gemini:** copy the skills to the folder it reads:
```bash
cp -r .claude/skills .agents/skills
```
and tell it to read `CLAUDE.md` first.

## Try it

```bash
python tools/yt.py watch https://youtu.be/VIDEO_ID
python tools/yt.py channel @somechannel --days 90
python tools/reel_fetch.py https://www.instagram.com/reel/XXXX/
python tools/thumbs.py https://www.youtube.com/@somechannel/videos --max 20
python tools/script_check.py my_script.md
```

Or just talk to Claude: *"analyze @somechannel"*, *"what's working in my niche this week"*, *"study these 5 reels"*, *"write a script about X"*, *"is this hook good?"*

**Editing a video:** add your own sound effects to `sfx/` (see [sfx/README.md](sfx/README.md)), then tell Claude *"edit this video"* with your voiceover. Or by hand:
```bash
python tools/edit_kit/new_video.py videos/my_video        # then put voice.mp3 in videos/my_video/audio/
cd videos/my_video/audio && python ../../../tools/transcribe.py voice.mp3 && python ../../../tools/tighten.py && cd ../../..
python tools/edit_kit/build.py videos/my_video             # after writing videos/my_video/shots.py
python tools/edit_kit/storyboard.py videos/my_video        # one still per shot, check before rendering
cd videos/my_video/project && npx hyperframes render . -o ../renders/my_video_v01.mp4
```
Only want captions for CapCut / Premiere / DaVinci? `python tools/captions.py words_tight.json captions` makes `.srt` + `.ass`.

## Hear your sound (optional)

Claude can't hear audio on its own. [earshot](https://github.com/Leonxlnx/earshot) by Leon Lin (MIT) gives it ears: it picks sound effects, checks your mix and lines sound up with cuts. Install it from its repo, add it to Claude Code as an MCP server, and copy its `skills/earshot` folder into `.claude/skills/`. The `video-breakdown` skill uses it when it's there.

## Rules the skills follow
- Your own words stay yours: Claude fixes grammar, never rewrites your lines without asking.
- It asks when unsure instead of guessing.
- Other creators' videos are downloaded only to study them. Ideas can be borrowed, wording and clips can't.
- Edits use only media you have the rights to: your recordings, your screenshots, free stock, your own sound effects.

## License
MIT, see [LICENSE](LICENSE).
