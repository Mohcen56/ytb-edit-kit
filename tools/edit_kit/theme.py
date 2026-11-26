# Recolours the kit's built-in look to the creator's brand/design.json.
# The kit is written in one reference palette (a warm light page, dark ink, a gold accent, white cards);
# every colour of that palette is moved to the creator's own: page -> background, ink -> text, gold -> accent.
# Real-app chrome (dark code windows, chat apps) and signal colours (red = wrong, green = ok) stay as they are.
import json, pathlib, re

REF_BG, REF_INK, REF_AC = (0xF5, 0xF4, 0xEE), (0x1F, 0x1E, 0x1D), (0xF2, 0xC2, 0x00)
# neutrals of the reference page (between page and ink) -> placed on the creator's page->text line
PAGE = ["F5F4EE", "EFECE4", "F1EEE6", "E7E3D8", "E3DFD4", "E4E1D8", "ECE9E1", "DAD6CB", "CFCBC0", "73726C", "A3A199", "4A4945", "1F1E1D"]
CARDS = ["FFFFFF", "FFF"]
# shades of the reference gold -> the same shade of the creator's accent
GOLDS = {"F2C200": 0.0, "EDE62A": 0.12, "E8B000": -0.08, "C99A00": -0.18, "B98500": -0.25, "FBF0CC": 0.8}

def _rgb(h):
    h = h.lstrip("#")
    if len(h) == 3: h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def _hex(c): return "#%02X%02X%02X" % tuple(max(0, min(255, round(x))) for x in c)
def _mix(a, b, k): return tuple(x + (y - x) * k for x, y in zip(a, b))
def _lum(c): return (.2126 * c[0] + .7152 * c[1] + .0722 * c[2]) / 255

# used when there's no brand/design.json yet: a clean neutral look (off-white page, near-black text, one blue accent)
NEUTRAL = {"background": "#F6F6F4", "text": "#141414", "accent": "#2563EB",
           "font_title": "Inter Black", "font_body": "Inter Bold", "font_mono": "JetBrains Mono"}

class Theme:
    def __init__(self, root):
        f = pathlib.Path(root) / "brand" / "design.json"
        d = json.loads(f.read_text(encoding="utf8")) if f.exists() else {}
        self.found = bool(d)
        if not d: d = NEUTRAL
        self.bg, self.ink, self.ac = _rgb(d.get("background", "#F5F4EE")), _rgb(d.get("text", "#1F1E1D")), _rgb(d.get("accent", "#F2C200"))
        self.light = _lum(self.bg) > .5
        self.font_title = d.get("font_title", "Montserrat Black")
        self.font_body = d.get("font_body", "Montserrat Bold")
        self.font_mono = d.get("font_mono", "JetBrains Mono")
        self.map = {}
        span = sum((a - b) ** 2 for a, b in zip(REF_INK, REF_BG)) ** .5
        for h in PAGE:   # where the colour sits between the reference page (0) and ink (1)
            c = _rgb(h); k = sum((x - y) * (z - y) for x, y, z in zip(c, REF_BG, REF_INK)) / span ** 2
            self.map[h] = _hex(_mix(self.bg, self.ink, max(0.0, min(1.0, k))))
        card = (255, 255, 255) if self.light else _mix(self.bg, self.ink, .08)
        for h in CARDS: self.map[h] = _hex(card)
        for h, k in GOLDS.items():
            self.map[h] = _hex(_mix(self.ac, (255, 255, 255), k) if k > 0 else _mix(self.ac, (0, 0, 0), -k))
            if h == "FBF0CC": self.map[h] = _hex(_mix(self.bg, self.ac, .25))
        self.rgba = {REF_INK: self.ink, REF_AC: self.ac}

    def family(self, name):   # "Montserrat Black" -> "Montserrat"
        w = {"thin", "light", "regular", "medium", "semibold", "bold", "extrabold", "black"}
        p = name.split(); return " ".join(p[:-1]) if len(p) > 1 and p[-1].lower() in w else name

    def apply(self, text):
        def hx(m):
            h = m.group(1).upper(); return self.map.get(h, m.group(0))
        text = re.sub(r"#([0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})\b", hx, text)
        def rg(m):
            c = tuple(int(x) for x in m.group(1).split(",")); new = self.rgba.get(c)
            return f"rgba({new[0]},{new[1]},{new[2]},{m.group(2)})" if new else m.group(0)
        text = re.sub(r"rgba\(\s*(\d+\s*,\s*\d+\s*,\s*\d+)\s*,\s*([\d.]+)\s*\)", lambda m: rg(m) if m else m, text)
        title, mono = self.family(self.font_title), self.family(self.font_mono)
        return text.replace('"Montserrat"', f'"{title}"').replace('"JetBrains Mono"', f'"{mono}"')

    def font_link(self):
        fams = dict.fromkeys([self.family(self.font_title), self.family(self.font_body), self.family(self.font_mono)])
        return "\n      ".join(f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={f.replace(" ", "+")}&display=block" />' for f in fams)

    def font_css(self, project_dir):
        """Download Google Fonts .woff2 locally so HyperFrames renders deterministically and single-weight fonts never 400."""
        import urllib.request
        fams = list(dict.fromkeys([self.family(self.font_title), self.family(self.font_body), self.family(self.font_mono)]))
        fdir = pathlib.Path(project_dir) / "assets" / "fonts"
        fdir.mkdir(parents=True, exist_ok=True)
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
        css_blocks, fallback_links = [], []
        for fam in fams:
            slug = fam.replace(" ", "+")
            css_text = None
            for suffix in (":wght@400;500;600;700;800;900", ":wght@400;700", ""):
                url = f"https://fonts.googleapis.com/css2?family={slug}{suffix}&display=block"
                try:
                    req = urllib.request.Request(url, headers={"User-Agent": ua})
                    with urllib.request.urlopen(req, timeout=6) as r:
                        css_text = r.read().decode("utf8")
                        break
                except Exception:
                    continue
            if not css_text:
                fallback_links.append(f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={slug}&display=block" />')
                continue
            def _save_font(m):
                u = m.group(1)
                name = re.sub(r"[^a-zA-Z0-9._-]", "_", fam) + "_" + u.rsplit("/", 1)[-1]
                dst = fdir / name
                if not dst.exists():
                    try:
                        with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": ua}), timeout=8) as r:
                            dst.write_bytes(r.read())
                    except Exception:
                        return m.group(0)
                return f'url("assets/fonts/{name}")'
            css_blocks.append(re.sub(r"url\((https://[^)]+)\)", _save_font, css_text))
        out = "\n      ".join(fallback_links)
        if css_blocks:
            out += ("\n      " if out else "") + "<style>\n" + "\n".join(css_blocks) + "\n      </style>"
        return out
