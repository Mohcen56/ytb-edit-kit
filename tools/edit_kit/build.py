# Edit kit: build engine. Reads <video>/shots.py + <video>/audio/words.json (+ brand/design.json for the look)
# and writes a HyperFrames project in <video>/project/. Every shot starts on the first word of its "at" phrase.
# usage: python tools/edit_kit/build.py <video folder>
#   then: cd <video>/project && npx hyperframes check && npx hyperframes render . -o ../renders/<name>_v01.mp4
# Kinds and options: tools/edit_kit/KINDS.md
import html as H, importlib.util, json, os, pathlib, re, sys

KIT = pathlib.Path(__file__).resolve().parent
ROOT = KIT.parent.parent
V = pathlib.Path(sys.argv[1]).resolve(); P = V / "project"
spec = importlib.util.spec_from_file_location("shots", V / "shots.py"); S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)
SHOTS = S.SHOTS
WW, HH = getattr(S, "SIZE", (1920, 1080))
# voice file in <video>/audio/: the tightened one when it exists (tools/tighten.py), else voice.mp3
VOICE = getattr(S, "VOICE", "voice_tight.wav" if (V / "audio" / "voice_tight.wav").exists() else "voice.mp3")

# ---------- look (from brand/design.json) ----------
dj = ROOT / "brand" / "design.json"
D = json.loads(dj.read_text(encoding="utf8")) if dj.exists() else {}
if not D: print("! no brand/design.json: using a neutral look. Run the design-system skill first.")
BG, TX, AC = D.get("background", "#111214"), D.get("text", "#F5F5F5"), D.get("accent", "#FFC800")
AC2 = D.get("accent_2") or AC
F_T, F_B, F_M = D.get("font_title", "Montserrat"), D.get("font_body", "Montserrat"), D.get("font_mono", "JetBrains Mono")
def lum(hx):
    h = hx.lstrip("#"); r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)); return .2126 * r + .7152 * g + .0722 * b
LIGHT = lum(BG) > .5
CARD = "#FFFFFF" if LIGHT else "#1C1D22"          # panels and cards
LINE = "rgba(0,0,0,.10)" if LIGHT else "rgba(255,255,255,.10)"
DIM = "rgba(0,0,0,.45)" if LIGHT else "rgba(255,255,255,.45)"
SH = "0 30px 80px rgba(0,0,0,.18)" if LIGHT else "0 40px 100px rgba(0,0,0,.6)"
def fam(name):  # "Montserrat Black" -> ("Montserrat", 900)
    w = {"thin": 100, "light": 300, "regular": 400, "medium": 500, "semibold": 600, "bold": 700, "extrabold": 800, "black": 900}
    parts = name.split(); last = parts[-1].lower()
    return (" ".join(parts[:-1]), w[last]) if last in w and len(parts) > 1 else (name, 700)
(FT, WT), (FB, WB), (FM, _) = fam(F_T), fam(F_B), fam(F_M)

# ---------- timing ----------
NUM = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10"}
norm = lambda x: NUM.get(re.sub(r"[^a-z0-9]", "", x.lower()), re.sub(r"[^a-z0-9]", "", x.lower()))
wf = V / "audio" / ("words_tight.json" if (V / "audio" / "words_tight.json").exists() else "words.json")
words = [w for s in json.loads(wf.read_text(encoding="utf8")) for w in s["words"]]
toks = [norm(w["w"]) for w in words]

def find(ph, start=0):
    want = "".join(norm(p) for p in ph.split())
    for i in range(start, len(toks)):
        got = ""
        for j in range(i, min(i + 20, len(toks))):
            got += toks[j]
            if got == want: return i
            if not want.startswith(got): break
    sys.exit(f"phrase not found after the previous shot: {ph!r} (copy it exactly as the transcript wrote it in {wf.name})")

pos = 0
for s in SHOTS:
    s["i"] = find(s["at"], pos); pos = s["i"] + 1; s["t"] = words[s["i"]]["s"]
VOICE_END = words[-1]["e"]
for a, b in zip(SHOTS, SHOTS[1:] + [None]):
    a["e"] = b["t"] if b else VOICE_END + 1.0
    a["w"] = words[a["i"]:(b["i"] if b else len(words))]

# ---------- checks (the default rules; warnings, not errors) ----------
PACE = float(D.get("max_hold", 4.5))
uses, last_graph = {}, None
for k, s in enumerate(SHOTS):
    d = s["e"] - s["t"]
    if d > PACE and s["kind"] not in ("screen", "full"): print(f"  ! shot {k} ({s['kind']}) holds {d:.1f}s: add a change every 2-3 s  ({s['at']!r})")
    for key in ("src",):
        if s.get(key): uses[s[key]] = uses.get(s[key], 0) + 1
    if s["kind"] == "graph":
        if last_graph == s.get("type", "bars"): print(f"  ! shot {k}: same graph type twice in a row ({s['at']!r})")
        last_graph = s.get("type", "bars")
    elif s["kind"] != "words": last_graph = None
for src, n in uses.items():
    if n > 2: print(f"  ! {src} is used {n} times: max 2 per video")

# ---------- shot builders ----------
SFX = []
def esc(x): return H.escape(str(x))

def build(s, k, t0):
    t, e = s["t"], s["e"]; d = e - t; js = []; kind = s["kind"]
    R = lambda x: round(x - t0, 3); I = lambda n: f"s{k}{n}"
    def W(word, fallback, nth=0):
        hits = [w["s"] for w in s["w"] if norm(w["w"]) == norm(word)] if word else []
        return hits[nth] if len(hits) > nth else fallback
    def Pt(x): return f"{R(min(max(x, t), e - .05)):.3f}"
    def fx(at, name):   # a sound only where something visibly changes, inside this shot
        if t - .05 <= at <= e - .2: SFX.append((round(at, 3), name))
    def rise(sel, at, y=40):
        js.append(f'gsap.set("{sel}",{{opacity:0}});tl.fromTo("{sel}",{{opacity:0,y:{y}}},{{opacity:1,y:0,duration:.35,ease:"power3.out"}},{Pt(at)});')
    def vid(i, src, start, dur, mstart=0.0, style=""):
        return (f'<video id="{i}" class="clip" src="assets/{src}" muted playsinline data-start="{start - t0:.3f}" data-duration="{dur:.3f}" '
                f'data-media-start="{mstart:.2f}" data-track-index="2" style="{style}"></video>')
    def media(i, src, style="width:100%;height:100%;object-fit:cover;display:block"):
        if src.lower().endswith((".mp4", ".webm", ".mov")): return vid(i, src, t, d, s.get("mstart", 0), style)
        return f'<img id="{i}" src="assets/{src}" alt="" style="{style}" />'
    if s.get("sfx"): fx(t, s["sfx"])
    h = ""

    if kind == "words":
        # big words; accent words in the accent colour; each word rises on its own spoken word
        acc = {norm(x) for x in s.get("accent", [])}; size = s.get("size", 120); n = 0; rows = []
        for line in s["lines"]:
            spans = []
            for wd in line:
                cls = "acc" if norm(wd) in acc else ""
                spans.append(f'<span class="wm"><span class="wu {cls}" id="{I(f"w{n}")}">{esc(wd)}</span></span>')
                js.append(f'tl.fromTo("#{I(f"w{n}")}",{{yPercent:110}},{{yPercent:0,duration:.45,ease:"expo.out"}},{Pt(W(wd, t + n * .12))});'); n += 1
            rows.append(f'<div class="wl">{" ".join(spans)}</div>')
        h = f'<div class="words" style="font-size:{size}px">{"".join(rows)}</div>'

    elif kind == "screen":
        # a window (website, app, recording). Optional: zoom in / hold / zoom out, a marker, a number on the page.
        lab = esc(s.get("label", ""))
        h = (f'<div class="win" id="{I("c")}"><div class="bar"><i></i><i></i><i></i><span class="lb">{lab}</span></div>'
             f'<div class="cnt" id="{I("cn")}">{media(I("m"), s["src"], "width:100%;height:100%;object-fit:cover;object-position:50% 0%;display:block")}')
        if s.get("mark"):
            x, y, w_, h_ = s["mark"]; style = s.get("mark_style", "box"); ma = W(s.get("mark_at"), t + .8)
            if style == "underline":
                h += f'<div class="mku" id="{I("mk")}" style="left:{x}px;top:{y + h_}px;width:{w_}px"></div>'
                js.append(f'tl.fromTo("#{I("mk")}",{{scaleX:0}},{{scaleX:1,duration:.2,ease:"power2.out"}},{Pt(ma)});')
            elif style == "highlight":
                h += f'<div class="mkh" id="{I("mk")}" style="left:{x}px;top:{y}px;width:{w_}px;height:{h_}px"></div>'
                js.append(f'tl.fromTo("#{I("mk")}",{{scaleX:0}},{{scaleX:1,duration:.2,ease:"power2.out"}},{Pt(ma)});')
            else:
                h += f'<div class="mkb" id="{I("mk")}" style="left:{x}px;top:{y}px;width:{w_}px;height:{h_}px"></div>'
                js.append(f'gsap.set("#{I("mk")}",{{opacity:0}});tl.fromTo("#{I("mk")}",{{opacity:0,scale:1.15}},{{opacity:1,scale:1,duration:.2,ease:"power2.out"}},{Pt(ma)});')
            fx(ma, "ding")
        if s.get("number"):
            txt, at_w, x, y = s["number"]; na = W(at_w, t + 1)
            h += f'<div class="num" id="{I("n")}" style="left:{x}px;top:{y}px">{esc(txt)}</div>'
            js.append(f'gsap.set("#{I("n")}",{{opacity:0}});tl.fromTo("#{I("n")}",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.3,ease:"back.out(2)"}},{Pt(na)});'); fx(na, "pop")
        h += '</div></div>'
        js.append(f'tl.fromTo("#{I("c")}",{{y:40,opacity:0}},{{y:0,opacity:1,duration:.35,ease:"power3.out"}},{Pt(t)});')
        if s.get("zoom"):   # (x, y, scale, word to zoom in on, word to zoom out on or None): one smooth move in, hold, back out
            zx, zy, zs, zin, zout = (list(s["zoom"]) + [None])[:5]; a = W(zin, t + .8); b = W(zout, e - .7) if zout else e - .7
            js.append(f'gsap.set("#{I("cn")}",{{transformOrigin:"{zx}px {zy}px"}});tl.to("#{I("cn")}",{{scale:{zs},duration:.6,ease:"power2.inOut"}},{Pt(a)});')
            if b - a > 1.2: js.append(f'tl.to("#{I("cn")}",{{scale:1,duration:.6,ease:"power2.inOut"}},{Pt(b)});')

    elif kind == "full":
        # full-screen b-roll (video or image), optional caption in the creator's exact words
        h = f'<div class="full" id="{I("c")}">{media(I("m"), s["src"], "position:absolute;inset:0;width:100%;height:100%;object-fit:cover")}{'<div class="shade"></div>' if s.get("cap") else ""}</div>'
        js.append(f'tl.fromTo("#{I("c")}",{{opacity:0}},{{opacity:1,duration:.2}},{Pt(t)});')
        if s.get("cap"):
            h += f'<div class="cap" id="{I("cp")}" style="top:{int(HH * .70)}px">{esc(s["cap"])}</div>'; rise(f"#{I('cp')}", W(s.get("cap_at"), t + .3), 24)

    elif kind in ("gif", "meme"):
        # framed GIF or meme image, straight, never stretched: a short GIF chains the next one (g=[a, b])
        items = s["src"] if isinstance(s["src"], list) else [s["src"]]
        lens = s.get("lens") or [d / len(items)] * len(items)
        if kind == "gif" and sum(lens) + .2 < d: print(f"  ! shot {k}: GIFs last {sum(lens):.1f}s but the slot is {d:.1f}s: chain another GIF ({s['at']!r})")
        bw, bh = s.get("box", (1100, 620) if s.get("cap") else (1300, 760)); bx = (WW - bw) // 2; by = 100 if s.get("cap") else (HH - bh) // 2
        st = t; inner = ""
        for q, (src, ln) in enumerate(zip(items, lens)):
            dur = min(ln, e - st)
            if src.lower().endswith((".mp4", ".webm")): inner += vid(I(f"g{q}"), src, st, dur, 0, "position:absolute;inset:0;width:100%;height:100%;object-fit:contain")
            else: inner += f'<img class="clip" id="{I(f"g{q}")}" src="assets/{src}" alt="" data-start="{st - t0:.3f}" data-duration="{dur:.3f}" data-track-index="3" style="position:absolute;inset:0;width:100%;height:100%;object-fit:contain" />'
            st += dur
        h = f'<div class="gifw" id="{I("c")}" style="left:{bx}px;top:{by}px;width:{bw}px;height:{bh}px">{inner}</div>'
        js.append(f'tl.fromTo("#{I("c")}",{{opacity:0,scale:.9}},{{opacity:1,scale:1,duration:.3,ease:"back.out(1.6)"}},{Pt(t)});')
        if s.get("cap"):
            acc = {norm(x) for x in s.get("accent", [])}
            sp = " ".join(f'<span class="{"acc" if norm(w_) in acc else ""}">{esc(w_)}</span>' for w_ in s["cap"].split())
            h += f'<div class="cap" id="{I("cp")}" style="top:{by + bh + 40}px">{sp}</div>'; rise(f"#{I('cp')}", t + .1, 24)

    elif kind == "versus":
        # two cards; on the winner's word the winner lifts and the other dims
        (ln, ls), (rn, rs) = s["left"], s["right"]; win = s.get("winner", "right"); wa = W(s.get("win_at"), t + d * .6)
        def card(side, name, sub, x): return f'<div class="vs" id="{I(side)}" style="left:{x}px"><div class="vn">{esc(name)}</div><div class="vsub">{esc(sub)}</div></div>'
        h = card("l", ln, ls, 200) + f'<div class="vsx" id="{I("x")}">vs</div>' + card("r", rn, rs, 1060)
        rise(f"#{I('l')}", t); rise(f"#{I('x')}", t + .15, 10); rise(f"#{I('r')}", W(s.get("right_at"), t + .3))
        wi, lo = (I("r"), I("l")) if win == "right" else (I("l"), I("r"))
        js.append(f'tl.to("#{wi}",{{y:-30,scale:1.06,boxShadow:"0 0 0 6px {AC}, {SH}",duration:.35,ease:"power3.out"}},{Pt(wa)});tl.to("#{lo}",{{opacity:.35,scale:.96,duration:.35}},{Pt(wa)});'); fx(wa, "ding")

    elif kind == "graph":
        # bars or a line that climbs as you talk; only real numbers. values=[("2023", 12), ...]
        vals = s["values"]; mx = max(v for _, v in vals) or 1; typ = s.get("type", "bars"); n = len(vals)
        gx, gy, gw, gh = 300, 300, 1320, 520; title = s.get("title", "")
        h = f'<div class="gt" id="{I("tt")}">{esc(title)}</div><div class="gbase" style="left:{gx}px;top:{gy + gh}px;width:{gw}px"></div>'
        rise(f"#{I('tt')}", t, 20)
        step = gw / n
        for q, (lab, v) in enumerate(vals):
            at = W(s.get("at_words", [None] * n)[q] if s.get("at_words") else None, t + .3 + q * min(.5, (d - 1) / n))
            cx = gx + step * q + step / 2; hh = gh * v / mx; last = q == n - 1
            h += f'<div class="gl" style="left:{cx - 100:.0f}px;top:{gy + gh + 16}px">{esc(lab)}</div>'
            h += f'<div class="gv{" acc" if last else ""}" id="{I(f"v{q}")}" style="left:{cx - 100:.0f}px;top:{gy + gh - hh - 64:.0f}px">{esc(s.get("fmt", "{}").format(v))}</div>'
            if typ == "bars":
                h += f'<div class="gb{" acc" if last else ""}" id="{I(f"b{q}")}" style="left:{cx - step * .3:.0f}px;top:{gy + gh - hh:.0f}px;width:{step * .6:.0f}px;height:{hh:.0f}px"></div>'
                js.append(f'tl.fromTo("#{I(f"b{q}")}",{{scaleY:0}},{{scaleY:1,duration:.45,ease:"power3.out"}},{Pt(at)});')
            else:
                h += f'<div class="gd{" acc" if last else ""}" id="{I(f"b{q}")}" style="left:{cx - 14:.0f}px;top:{gy + gh - hh - 14:.0f}px"></div>'
                js.append(f'gsap.set("#{I(f"b{q}")}",{{opacity:0}});tl.fromTo("#{I(f"b{q}")}",{{opacity:0,scale:0}},{{opacity:1,scale:1,duration:.3,ease:"back.out(2)"}},{Pt(at)});')
                if q:
                    px, ph = gx + step * (q - 1) + step / 2, gh * vals[q - 1][1] / mx
                    L = ((cx - px) ** 2 + (ph - hh) ** 2) ** .5; ang = __import__("math").degrees(__import__("math").atan2(-(hh - ph), cx - px))
                    h += f'<div class="gln" id="{I(f"l{q}")}" style="left:{px:.0f}px;top:{gy + gh - ph - 3:.0f}px;width:{L:.0f}px;transform:rotate({ang:.2f}deg)"></div>'
                    js.append(f'tl.fromTo("#{I(f"l{q}")}",{{scaleX:0}},{{scaleX:1,duration:.3,ease:"none"}},{Pt(at - .3)});')
            js.append(f'gsap.set("#{I(f"v{q}")}",{{opacity:0}});tl.to("#{I(f"v{q}")}",{{opacity:1,duration:.2}},{Pt(at + .2)});')
            if last: fx(at, "ding")

    elif kind == "flow":
        # boxes joined by arrows, each box on its word. items=[("label", "word"), ...]
        n = len(s["items"]); bw = min(380, (WW - 200 - (n - 1) * 90) / n); x0 = (WW - (n * bw + (n - 1) * 90)) / 2
        for q, (lab, cue) in enumerate(s["items"]):
            at = W(cue, t + .2 + q * .6); x = x0 + q * (bw + 90)
            h += f'<div class="fb" id="{I(f"f{q}")}" style="left:{x:.0f}px;width:{bw:.0f}px">{esc(lab)}</div>'
            rise(f"#{I(f'f{q}')}", at, 30)
            if q: h += f'<div class="fa" id="{I(f"a{q}")}" style="left:{x - 72:.0f}px">&#8594;</div>'; js.append(f'gsap.set("#{I(f"a{q}")}",{{opacity:0}});tl.to("#{I(f"a{q}")}",{{opacity:1,duration:.2}},{Pt(at - .15)});')
            if q: fx(at, "pop")

    elif kind == "collage":
        # one card per item you say, on its word: real logos or screenshots. items=[("file.png", "label", "word"), ...]
        n = len(s["items"]); cols = min(n, 4); rows = (n + cols - 1) // cols; cw, chh = 360, 300
        gx = (WW - cols * cw - (cols - 1) * 40) / 2; gy = (HH - rows * chh - (rows - 1) * 40) / 2
        for q, (src, lab, cue) in enumerate(s["items"]):
            at = W(cue, t + .2 + q * .5); x = gx + (q % cols) * (cw + 40); y = gy + (q // cols) * (chh + 40)
            h += (f'<div class="cc" id="{I(f"c{q}")}" style="left:{x:.0f}px;top:{y:.0f}px;width:{cw}px;height:{chh}px">'
                  f'<img src="assets/{src}" alt="" /><div class="ccl">{esc(lab)}</div></div>')
            js.append(f'gsap.set("#{I(f"c{q}")}",{{opacity:0}});tl.fromTo("#{I(f"c{q}")}",{{opacity:0,scale:.7}},{{opacity:1,scale:1,duration:.3,ease:"back.out(1.8)"}},{Pt(at)});'); fx(at, "pop")

    elif kind == "drop":
        # photos or screenshots drop onto the page and settle (about 25 px and 2.5 degrees), then stay still
        n = len(s["items"])
        for q, item in enumerate(s["items"]):
            src, cue = (item if isinstance(item, (list, tuple)) else (item, None)); at = W(cue, t + .1 + q * .5)
            w_ = s.get("width", 760 if n == 1 else 620); x = (WW - w_) / 2 + (q - (n - 1) / 2) * 420; rot = (-2.5, 2.5, -1.5, 1.5)[q % 4]
            h += f'<div class="ph" id="{I(f"p{q}")}" style="left:{x:.0f}px;top:{HH / 2 - w_ * .32:.0f}px;width:{w_}px;transform:rotate({rot}deg)"><img src="assets/{src}" alt="" /></div>'
            js.append(f'gsap.set("#{I(f"p{q}")}",{{opacity:0}});tl.fromTo("#{I(f"p{q}")}",{{opacity:0,y:-25,rotation:{rot - 2.5}}},{{opacity:1,y:0,rotation:{rot},duration:.4,ease:"power3.out"}},{Pt(at)});'); fx(at, "whoosh")

    elif kind == "map":
        # style="road": numbered stops on a path, the current one in the accent colour.
        # style="hub": items around a centre, the focused one sharp, the rest blurred.  items=["A", "B", ...], focus=index
        items = s["items"]; fo = s.get("focus", 0); n = len(items)
        if s.get("style", "road") == "road":
            x0, x1, y = 220, WW - 220, HH / 2 + 40; step = (x1 - x0) / max(n - 1, 1)
            h += f'<div class="rdl" id="{I("ln")}" style="left:{x0}px;top:{y:.0f}px;width:{x1 - x0}px"></div>'
            js.append(f'tl.fromTo("#{I("ln")}",{{scaleX:0}},{{scaleX:1,duration:.6,ease:"power2.out"}},{Pt(t)});')
            for q, lab in enumerate(items):
                x = x0 + q * step; cur = q == fo
                h += (f'<div class="rds{" acc" if cur else ""}{" done" if q < fo else ""}" id="{I(f"s{q}")}" style="left:{x - 40:.0f}px;top:{y - 40:.0f}px">{q + 1}</div>'
                      f'<div class="rdt{" acc" if cur else ""}" style="left:{x - 150:.0f}px;top:{y + 64:.0f}px">{esc(lab)}</div>')
                js.append(f'gsap.set("#{I(f"s{q}")}",{{opacity:0}});tl.fromTo("#{I(f"s{q}")}",{{opacity:0,scale:.5}},{{opacity:1,scale:1,duration:.3,ease:"back.out(2)"}},{Pt(t + .2 + q * .12)});')
            fx(t, "whoosh")
        else:
            import math
            cx, cy, rr = WW / 2, HH / 2, 360
            h += f'<div class="hubc" style="left:{cx - 110:.0f}px;top:{cy - 110:.0f}px">{esc(s.get("center", n))}</div>'
            for q, lab in enumerate(items):
                a = 2 * math.pi * q / n; x = cx + rr * 1.35 * math.sin(a); y = cy - rr * math.cos(a); cur = q == fo
                h += f'<div class="hubi{" acc" if cur else " blur"}" id="{I(f"h{q}")}" style="left:{x - 170:.0f}px;top:{y - 40:.0f}px">{esc(lab)}</div>'
                js.append(f'gsap.set("#{I(f"h{q}")}",{{opacity:0}});tl.to("#{I(f"h{q}")}",{{opacity:{1 if cur else .8},duration:.3}},{Pt(t + .1 + q * .08)});')
            fx(t, "whoosh")

    elif kind == "checklist":
        # items tick one by one on their words. items=[("text", "word"), ...]
        for q, (txt, cue) in enumerate(s["items"]):
            at = W(cue, t + .3 + q * .6); y = HH / 2 - len(s["items"]) * 60 + q * 120
            h += f'<div class="ck" id="{I(f"k{q}")}" style="top:{y:.0f}px"><span class="box"><b id="{I(f"t{q}")}">&#10003;</b></span>{esc(txt)}</div>'
            rise(f"#{I(f'k{q}')}", t + q * .12, 20)
            js.append(f'gsap.set("#{I(f"t{q}")}",{{scale:0}});tl.to("#{I(f"t{q}")}",{{scale:1,duration:.25,ease:"back.out(3)"}},{Pt(at)});'); fx(at, "click")

    elif kind == "prompt":
        # a prompt typed into a chat box, so viewers see the exact words
        txt = s["text"]; step = min(.04, max(d - 1, .5) / max(len(txt), 1) * .7)
        chars = "".join(f'<span class="chr">{esc(c)}</span>' for c in txt)
        h = f'<div class="pr" id="{I("c")}"><div class="prh">{esc(s.get("title", "Chat"))}</div><div class="prb" id="{I("tx")}">{chars}<span class="crt"></span></div></div>'
        rise(f"#{I('c')}", t)
        js.append(f'document.querySelectorAll("#{I("tx")} .chr").forEach((n,q)=>{{gsap.set(n,{{opacity:0}});tl.set(n,{{opacity:1}},{R(t + .3):.3f}+q*{step:.4f});}});'); fx(t + .3, "typing")

    else:
        sys.exit(f"unknown kind {kind!r} (see tools/edit_kit/KINDS.md)")
    js.insert(0, f'gsap.set("#{I("")}",{{opacity:0}});tl.set("#{I("")}",{{opacity:1}},{R(t):.3f});tl.set("#{I("")}",{{opacity:0}},{R(e):.3f});')
    return f'<div id="{I("")}" class="shot">{h}</div>', js

# ---------- css ----------
CSS = f'''
#root {{ background: {BG}; overflow: hidden; font-family: "{FB}", sans-serif; color: {TX}; }}
.shot {{ position: absolute; inset: 0; }}
.acc {{ color: {AC} !important; }}
.words {{ position: absolute; left: 80px; right: 80px; top: 50%; transform: translateY(-50%); text-align: center; font-family: "{FT}"; font-weight: {WT}; text-transform: uppercase; line-height: 1.02; letter-spacing: -.02em; }}
.wl {{ display: block; }} .wm {{ display: inline-block; overflow: hidden; padding: 4px .08em 12px; vertical-align: top; }} .wu {{ display: inline-block; }}
.win {{ position: absolute; left: 140px; top: 80px; width: 1640px; height: 920px; border-radius: 20px; overflow: hidden; background: {CARD}; box-shadow: {SH}, 0 0 0 1px {LINE}; }}
.bar {{ position: absolute; left: 0; top: 0; right: 0; height: 52px; background: {"#ECECEC" if LIGHT else "#26272C"}; display: flex; align-items: center; padding: 0 20px; gap: 9px; }}
.bar i {{ width: 14px; height: 14px; border-radius: 50%; display: block; }}
.bar i:nth-child(1) {{ background: #FF5F57; }} .bar i:nth-child(2) {{ background: #FEBC2E; }} .bar i:nth-child(3) {{ background: #28C840; }}
.bar .lb {{ position: absolute; left: 50%; transform: translateX(-50%); font: 500 28px "{FM}", monospace; color: {DIM}; }}
.cnt {{ position: absolute; left: 0; top: 52px; width: 1640px; height: 868px; overflow: hidden; }}
.mkb {{ position: absolute; border: 5px solid {AC}; border-radius: 12px; }}
.mku {{ position: absolute; height: 8px; border-radius: 4px; background: {AC}; transform-origin: 0 50%; }}
.mkh {{ position: absolute; background: {AC}; opacity: .35; border-radius: 6px; transform-origin: 0 50%; }}
.num {{ position: absolute; font: {WT} 120px "{FT}"; color: {AC}; background: {CARD}; padding: 6px 34px; border-radius: 20px; box-shadow: {SH}; }}
.full {{ position: absolute; inset: 0; overflow: hidden; }}
.shade {{ position: absolute; left: 0; right: 0; bottom: 0; height: 55%; background: linear-gradient(180deg, transparent, rgba(0,0,0,.65)); }}
.cap {{ position: absolute; left: 100px; right: 100px; text-align: center; font: {WB} 56px "{FB}"; color: {TX if not LIGHT else "#111"}; text-shadow: 0 4px 24px rgba(0,0,0,.35); }}
.gifw {{ position: absolute; border-radius: 18px; overflow: hidden; background: {CARD}; box-shadow: {SH}; }}
.vs {{ position: absolute; top: 300px; width: 660px; height: 480px; border-radius: 28px; background: {CARD}; box-shadow: {SH}, 0 0 0 1px {LINE}; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 40px; }}
.vn {{ font: {WT} 76px "{FT}"; text-transform: uppercase; }} .vsub {{ font: {WB} 34px "{FB}"; color: {DIM}; margin-top: 18px; }}
.vsx {{ position: absolute; left: 900px; top: 500px; width: 120px; text-align: center; font: {WT} 54px "{FT}"; color: {DIM}; }}
.gt {{ position: absolute; left: 300px; top: 110px; font: {WT} 64px "{FT}"; }}
.gbase {{ position: absolute; height: 3px; background: {LINE}; }}
.gl, .gv {{ position: absolute; width: 200px; text-align: center; }} .gl {{ font: {WB} 30px "{FB}"; color: {DIM}; }} .gv {{ font: {WT} 44px "{FT}"; }}
.gb {{ position: absolute; border-radius: 14px 14px 0 0; background: {DIM}; transform-origin: 50% 100%; }} .gb.acc {{ background: {AC}; }}
.gd {{ position: absolute; width: 28px; height: 28px; border-radius: 50%; background: {TX}; }} .gd.acc {{ background: {AC}; box-shadow: 0 0 0 10px {AC}33; }}
.gln {{ position: absolute; height: 6px; border-radius: 3px; background: {TX}; transform-origin: 0 50%; }}
.fb {{ position: absolute; top: 450px; height: 180px; border-radius: 24px; background: {CARD}; box-shadow: {SH}, 0 0 0 1px {LINE}; display: flex; align-items: center; justify-content: center; text-align: center; padding: 20px; font: {WB} 38px "{FB}"; }}
.fa {{ position: absolute; top: 500px; width: 54px; text-align: center; font: 700 64px "{FB}"; color: {AC}; }}
.cc {{ position: absolute; border-radius: 24px; background: #FFFFFF; box-shadow: {SH}; overflow: hidden; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
.cc img {{ max-width: 70%; max-height: 62%; object-fit: contain; }} .ccl {{ margin-top: 18px; font: {WB} 30px "{FB}"; color: #222; }}
.ph {{ position: absolute; padding: 14px; background: #FFFFFF; border-radius: 10px; box-shadow: {SH}; }} .ph img {{ width: 100%; display: block; border-radius: 4px; }}
.rdl {{ position: absolute; height: 8px; border-radius: 4px; background: {LINE}; transform-origin: 0 50%; }}
.rds {{ position: absolute; width: 80px; height: 80px; border-radius: 50%; background: {CARD}; box-shadow: 0 0 0 4px {LINE}; display: flex; align-items: center; justify-content: center; font: {WT} 36px "{FT}"; color: {DIM}; }}
.rds.done {{ color: {TX}; }} .rds.acc {{ background: {AC}; color: {BG} !important; box-shadow: 0 0 0 10px {AC}33; }}
.rdt {{ position: absolute; width: 300px; text-align: center; font: {WB} 32px "{FB}"; color: {DIM}; }} .rdt.acc {{ color: {TX} !important; }}
.hubc {{ position: absolute; width: 220px; height: 220px; border-radius: 50%; background: {AC}; color: {BG}; display: flex; align-items: center; justify-content: center; font: {WT} 80px "{FT}"; }}
.hubi {{ position: absolute; width: 340px; height: 80px; border-radius: 40px; background: {CARD}; box-shadow: {SH}; display: flex; align-items: center; justify-content: center; font: {WB} 32px "{FB}"; }}
.hubi.blur {{ filter: blur(2.5px); }} .hubi.acc {{ box-shadow: 0 0 0 5px {AC}, {SH}; color: {TX}; }}
.ck {{ position: absolute; left: 520px; display: flex; align-items: center; gap: 34px; font: {WB} 52px "{FB}"; }}
.ck .box {{ width: 72px; height: 72px; border-radius: 16px; box-shadow: inset 0 0 0 4px {LINE}; display: flex; align-items: center; justify-content: center; }}
.ck .box b {{ color: {AC}; font-size: 56px; display: block; }}
.pr {{ position: absolute; left: 260px; top: 300px; width: 1400px; border-radius: 26px; background: {CARD}; box-shadow: {SH}, 0 0 0 1px {LINE}; overflow: hidden; }}
.prh {{ padding: 22px 34px; font: 600 26px "{FM}", monospace; color: {DIM}; border-bottom: 1px solid {LINE}; }}
.prb {{ padding: 40px 44px 60px; font: 500 46px/1.45 "{FB}"; min-height: 260px; }}
.crt {{ display: inline-block; width: 4px; height: 52px; background: {AC}; vertical-align: middle; margin-left: 4px; }}
'''

# ---------- write the project ----------
(P / "compositions").mkdir(parents=True, exist_ok=True); (P / "assets" / "sfx").mkdir(parents=True, exist_ok=True)
for f in ("hyperframes.json", "package.json"):
    if not (P / f).exists(): (P / f).write_text((KIT / "project_template" / f).read_text(encoding="utf8"), encoding="utf8")
# media: everything in <video>/assets/ is linked into the project (copied on first build)
import shutil
for f in (V / "assets").rglob("*"):
    if f.is_file():
        dst = P / "assets" / f.relative_to(V / "assets")
        if not dst.exists() or dst.stat().st_mtime < f.stat().st_mtime: dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(f, dst)
(P / "assets" / "voice").mkdir(parents=True, exist_ok=True)
shutil.copy2(V / "audio" / VOICE, P / "assets" / "voice" / VOICE)
# sound effects: your own files in sfx/ at the repo root (click, whoosh, pop, ding, typing); missing ones are skipped
SFXDIR = ROOT / "sfx"; have = {}
for nm in ("click", "whoosh", "pop", "ding", "typing"):
    hit = next(iter(sorted(SFXDIR.glob(nm + ".*"))), None) if SFXDIR.exists() else None
    if hit: shutil.copy2(hit, P / "assets" / "sfx" / hit.name); have[nm] = hit.name

CHUNK = 60.0   # one composition per ~minute keeps renders fast
secs, cur = [], []
for k, s in enumerate(SHOTS):
    if cur and s["t"] - SHOTS[cur[0]]["t"] >= CHUNK: secs.append(cur); cur = []
    cur.append(k)
if cur: secs.append(cur)
hosts = []
for si, ks in enumerate(secs):
    t0 = SHOTS[ks[0]]["t"] if si else 0.0; t1 = SHOTS[ks[-1]]["e"]; name = f"part{si + 1}"
    html_, js = [], []
    for k in ks:
        b, j = build(SHOTS[k], k, t0); html_.append(b); js += j
    doc = f'''<template id="{name}-template">
<div id="root" data-composition-id="{name}" data-width="{WW}" data-height="{HH}" data-start="0" data-duration="{t1 - t0:.3f}">
<style>{CSS}</style>
{chr(10).join(html_)}
<script>
(function () {{
  const tl = gsap.timeline({{ paused: true }});
  {chr(10).join("  " + x for x in js)}
  window.__timelines = window.__timelines || {{}};
  window.__timelines["{name}"] = tl;
}})();
</script>
</div>
</template>
'''
    (P / "compositions" / f"{name}.html").write_text(doc, encoding="utf8")
    hosts.append((name, round(t0, 3), round(t1 - t0, 3)))

VOL = {"click": .14, "whoosh": .12, "pop": .1, "ding": .1, "typing": .07}
last, sfx = -1, []
for at, nm in sorted(SFX):       # one sound at a time, never stacked
    if nm in have and at - last >= .35: sfx.append((at, have[nm], VOL[nm])); last = at
missing = sorted({nm for _, nm in SFX} - set(have))
if missing: print(f"  ! no sound file for {', '.join(missing)}: put your own in sfx/ (e.g. sfx/whoosh.wav). Skipped.")
END = SHOTS[-1]["e"]
gf = "&".join("family=" + f.replace(" ", "+") + ":wght@400;500;600;700;800;900" for f in dict.fromkeys([FT, FB, FM]))
root = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={WW}, height={HH}" />
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?{gf}&display=block" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ width: {WW}px; height: {HH}px; overflow: hidden; background: {BG}; }}</style>
  </head>
  <body>
    <div id="main" data-composition-id="main" data-start="0" data-duration="{END:.3f}" data-width="{WW}" data-height="{HH}">
''' + "\n".join(f'      <div id="{n}-host" class="clip" data-composition-src="compositions/{n}.html" data-composition-id="{n}" data-start="{a}" data-duration="{d}" data-track-index="1" data-track-kind="graphics"></div>' for n, a, d in hosts) + f'''
      <audio id="vo" class="clip" src="assets/voice/{VOICE}" data-start="0" data-duration="{VOICE_END + .3:.3f}" data-track-index="20" data-volume="1"></audio>
''' + "\n".join(f'      <audio id="sfx{q}" class="clip" src="assets/sfx/{f}" data-start="{a:.3f}" data-duration="0.8" data-track-index="21" data-volume="{v}" data-fade-out="0.05"></audio>' for q, (a, f, v) in enumerate(sfx)) + '''
    </div>
    <script>
      window.__timelines = window.__timelines || {};
      window.__timelines["main"] = gsap.timeline({ paused: true });
    </script>
  </body>
</html>
'''
(P / "index.html").write_text(root, encoding="utf8")
json.dump([{"k": k, "t": round(s["t"], 2), "e": round(s["e"], 2), "kind": s["kind"], "at": s["at"]} for k, s in enumerate(SHOTS)],
          open(V / "shot_times.json", "w", encoding="utf8"), indent=1)
print(f"{len(SHOTS)} shots, {len(hosts)} parts, {len(sfx)} sounds, {END:.1f}s")
for k, s in enumerate(SHOTS): print(f'{k:3} {s["t"]:7.2f} {s["e"] - s["t"]:5.2f}  {s["kind"]:9} {s["at"]}')
