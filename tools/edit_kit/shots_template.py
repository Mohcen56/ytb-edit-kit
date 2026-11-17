# Shot plan. Each shot starts on the FIRST word of its "at" phrase, written exactly as the transcript has it
# (audio/words_tight.json). One dict per visual change; aim for a change every 2-3 s. Files are paths inside assets/.
# All kinds and options: tools/edit_kit/KINDS.md
# SIZE = (1080, 1920)   # uncomment for a vertical reel

SHOTS = [
    dict(at="first words of your hook", kind="words", lines=[["FIRST", "BIG"], ["LINE"]], accent=["LINE"]),
    # dict(at="so I opened", kind="screen", src="screens/site.png", label="site.com", mark=(120, 300, 500, 80), mark_at="pricing", sfx="whoosh"),
]
