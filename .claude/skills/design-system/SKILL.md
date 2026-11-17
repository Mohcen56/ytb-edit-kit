---
name: design-system
description: Grill the creator until they have their own visual system for videos and thumbnails - colors, fonts, text style, captions, sound rules, editing pace and things they never do - then write it to brand/design.md and brand/design.json, which the other skills and tools read. Use on first setup, when the creator says "build my design system", "what should my videos look like", "pick my colors/fonts", or when another skill needs brand values and brand/design.md doesn't exist yet.
---

# Design system builder (grill me)

This repo ships with **no brand**. Every creator builds their own here. Never invent a style for them and never copy another creator's look: ask, show, and let them pick.

## Before asking
1. Read `brand/about_me/` (run `about-me` first if it's empty: the style must fit the person and the audience).
2. If `brand/design.md` exists, show it and ask only about what they want to change.
3. Ask for 2-5 references they love (videos, channels, thumbnails, websites). If they give links, study them with `video-breakdown` or `python tools/yt.py watch <url>` and say what each one does. References are ideas, never something to clone.

## Grill, one question at a time
Use AskUserQuestion. Each question has 2-4 concrete options with your recommendation first. **Show, don't describe** whenever it's visual: render a small preview (an inline widget or HTML artifact) of each option on a 16:9 frame and a thumbnail-size frame.

Go through these branches in order. Don't move on until each one is settled:
1. **Personality:** three words for how the channel should feel (calm, loud, nerdy, luxury, playful...). Everything after this must fit them.
2. **Background:** dark, light, or a texture or colour. Show 3 swatches with real text on them.
3. **Accent colour:** one main accent (show 4 options on the chosen background). Ask if a second colour is ever allowed, and when.
4. **Text colour:** checked for contrast on the background (aim for at least 4.5:1 and say the number).
5. **Fonts:** max 3: a big title font, a caption or body font, and an optional mono font for code, URLs and tool names. Free fonts (Google Fonts) unless they own a licence. Show each with their real channel name.
6. **Big text style:** flat colour, gradient, outline, glow or shadow. Show each.
7. **Thumbnails:** face or no face, how many words (3-5 max), same fonts or a separate thumbnail font.
8. **Captions:** on or off, one line or two, word highlight or static, position (keep text above ~70% of the height so the YouTube progress bar never covers it).
9. **Sound:** music yes or no, which sound effects (click, whoosh, pop, ding...), and the loudness rule (the voice is always on top, one effect at a time).
10. **Pace:** how often something new appears on screen (for example every 2-3 s in tutorials, slower in stories). Save the longest hold in seconds as `max_hold`.
11. **Never list:** things they never want (for example flashing, glitch transitions, shaky cam, stock-photo people, more than one thing moving at once).
12. **Formats:** which video types they make (tutorial, essay, list, talking head, reels) and whether any type gets its own look.

If an answer is vague, ask again with sharper options. If two answers fight (a "calm" channel with glitch transitions), point it out and make them choose.

## Write the result
1. `brand/design.md`: short, readable, dated: each decision with one line of why. End with the "Never" list.
2. `brand/design.json` (the tools read these keys, keep them):
```json
{
  "background": "#111111",
  "text": "#FFFFFF",
  "accent": "#FFCC00",
  "accent_2": null,
  "font_title": "Font Name",
  "font_body": "Font Name",
  "font_mono": "Font Name",
  "caption_size": 56,
  "caption_position": "bottom",
  "sfx": ["click", "whoosh", "pop", "ding"],
  "music": false,
  "max_hold": 4.5
}
```
The values above are placeholders: write the creator's own.
3. Add a line to `CLAUDE.md`: "Brand: read brand/design.md before any visual, thumbnail or edit."
4. Show a one-page style guide (HTML artifact): swatches, fonts, a sample thumbnail, a sample caption frame and the Never list.

## Later changes
When the creator locks a new rule, add it to `brand/design.md` with the date, update `design.json` if a value changed, and keep the old value in a "Changed" line so the history stays readable.
