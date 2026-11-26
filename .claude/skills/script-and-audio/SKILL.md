---
name: script-and-audio
description: Write or tighten a YouTube script so it edits cleanly in code (short beats, clear turns, concrete examples, line-to-visual plan) and prepare/cut the voiceover audio (transcribe, catch Whisper skipped spans, tighten pauses, check WPM and loudness). Use before `edit` when starting from a topic, a rough draft, or a raw voiceover.
---

# Script structure & audio cutting

Great edits start with an editable script and clean, tightly cut audio. Raw rambling voiceovers force the editor to guess visuals; clean beats and tight audio make every shot land on the word.

---

## Part 1 · Script structure (write for the edit)

Read `brand/about_me/` first so the voice, audience, and examples match the creator.

### 1. Shape & retention
- **Hook (first ~15 s):** Start with the finished result, the surprise, or the problem—never *"hey guys welcome back"*. Show the first real result or payoff by `~0:15`, and flash 2–3 quick previews of what's coming in the first `10 s`.
- **Give a reason to stay:** Put the strongest item first, save a strong one for last, and tease it early.
- **Break the rhythm:** Don't give every section the exact same 30-second template. Mix fast hits (10 s), short stories (*"this saved me when…"*), and before/after comparisons.
- **One piece, start to finish:** Every section must lead into the next. If you open with a rant or problem, turn it with a personal story (*"I used to think…"*) into a concrete answer.
- **Outro:** Always connect back to the hook and close cleanly with the creator's call-to-action.

### 2. Write in visual beats (not walls of text)
- **Short sentences, one idea per breath:** Keep sentences short enough to say in one breath, with an occasional longer "thinking out loud" line for natural rhythm.
- **Explicit turns & reasons:** Use `"but"` to flip an idea (maps cleanly to `strike2` or `pick2`), `"because"` to give the reason right after a claim, and `"..."` before a reveal.
- **Concrete examples & real numbers:** Replace abstract claims with everyday examples (*"tell it to build an e-commerce app"*) and real numbers (*"from a year, to 8 months, to 3 months"* → maps to `bars2` or `words`).
- **Cut AI clichés:** Strip phrases like *"Here's the part nobody talks about"*, *"Let's be real"*, *"In today's world"*, *"game-changer"*, *"unlock"*, *"dive in"*, stacked one-word zingers, and em-dash asides.
- **Mark visual cues & links:** Put website URLs next to tool names, and draft a quick `line → visual` beat table (especially for screen-recording tutorials, where the script must match the exact order of actions on screen).

---

## Part 2 · Audio editing & cutting

Run these inside `videos/<name>/audio/` with `voice.mp3` in place.

### 1. Transcribe & catch Whisper skipped spans
```bash
python ../../../tools/transcribe.py voice.mp3 ../script.txt
```
- Pass `../script.txt` so Whisper spells tool names and terms accurately.
- **Check for skipped spans:** `transcribe.py` warns if there is a `> 4 s` gap between segments or if the transcript ends > `5 s` before the audio ends. `faster-whisper` (`small.en`) can occasionally skip 20–30 s chunks of speech.
- **If a span was skipped:** Slice that range with FFmpeg, transcribe the slice, offset its timestamps, and merge it into `words.json` before tightening:
  ```bash
  ffmpeg -ss <START> -to <END> -i voice.mp3 slice.wav
  python ../../../tools/transcribe.py slice.wav ../script.txt
  ```

### 2. Cut pauses & normalize loudness (`tighten.py`)
```bash
python ../../../tools/tighten.py
```
What `tighten.py` does automatically:
- Detects silences longer than `0.30 s` (`-34 dB`) and shrinks them to `0.22 s` (with `12 ms` fade-in/out on every cut so there are no clicks).
- If `voiceover_cadence.txt` exists with `<break time="0.5s"/>` tags, preserves those intentional dramatic pauses while tightening everything else.
- Normalizes loudness to YouTube target (`-14 LUFS`, `-1.5 dBTP`) at `48 kHz` and outputs `voice_tight.wav` + `words_tight.json` + `cuts.json`.
- **Optional pacing check:** Target roughly `175–190 WPM` after tightening. If the delivery is noticeably slow (under `~170 WPM`), you can gently speed it up with FFmpeg `atempo` (never past `1.10x` / `~195 WPM`, and re-run `transcribe.py` if you change speed).

### 3. Verify the final mix
After `build.py` and `hyperframes render`, run:
```bash
python tools/edit_kit/final_check.py videos/<name> videos/<name>/renders/<name>_v01.mp4
```
Confirm every word is clearly heard (no SFX covering a word) and loudness sits around `-14 LUFS`.
