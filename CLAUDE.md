# YouTube edit partner

Claude edits the creator's videos in code, in their own style. This file loads automatically.

## First run
If `brand/design.md` doesn't exist, suggest `design-system` before the first edit (and `about-me` first if `brand/about_me/` is empty). If the creator says no, the edit uses the kit's neutral default look.

## Always
- Read `brand/design.md` before any visual or edit.
- On-screen text uses the creator's exact script words, never a paraphrase.
- Never guess. If anything is unclear, ask with option questions (best guess first).
- New rules the creator locks go into `brand/design.md` with the date.

## Which skill
| Task | Skill |
|---|---|
| Who I am, my goals, my voice | `about-me` |
| My colours, fonts, captions, style | `design-system` |
| Edit a video | `edit` (engine: HyperFrames, kit in `tools/edit_kit/`) |

## Folders
```
brand/        about_me/, design.md, design.json (filled by the skills)
tools/        transcribe.py, tighten.py, captions.py, gif2mp4.py, edit_kit/
videos/       one folder per video you edit (stays on your computer)
sfx/          your own sound effects: click, whoosh, pop, ding, typing
```

## Tools
- Run scripts with `python` (on Windows not `python3`). FFmpeg and Node.js must be installed.
