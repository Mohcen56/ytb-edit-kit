# Edit kit: extra shot kinds. Each kind: f(s, t, e, d, I, W, P, R, fx, t0) -> (html, [js]).
import html as H, random
import sys as _sys
_S = _sys.modules["shots"]   # the video's shots module (set by cream_build.py)
SKILLS, KEEP, LOADS = getattr(_S, "SKILLS", []), getattr(_S, "KEEP", []), getattr(_S, "LOADS", [])
YT_HYPE, YT_TUTS = getattr(_S, "YT_HYPE", []), getattr(_S, "YT_TUTS", [])
import re

KIT_CSS = r'''
.chip2 { font-size: 58px; padding: 24px 44px; border-radius: 26px; } .chip2 i { width: 24px; height: 24px; } .chipcol { gap: 40px; }
.term.light { background: #1b1c21; } .term.light .bar { background: #26272d; }
.term .body .tl.rl { color: #F4F4F2; }
.gifw { position: absolute; border: 10px solid #F4F4F2; border-radius: 18px; overflow: hidden; box-shadow: 0 34px 80px rgba(0,0,0,.6); background: #000; }
.gifw video { width: 100%; height: 100%; object-fit: cover; display: block; }
.gifw.bare { border: 0; background: transparent; box-shadow: none; border-radius: 0; }
.gcap { position: absolute; left: 0; right: 0; text-align: center; font: 900 70px/1.05 "Montserrat"; text-transform: uppercase; letter-spacing: -.02em; color: #F4F4F2; }
.pill.bl b { filter: blur(11px); }
.mstamp { position: absolute; padding: 14px 34px; border: 8px solid #E5484D; border-radius: 18px; color: #E5484D; font: 900 64px "Montserrat"; text-transform: uppercase; transform: rotate(-8deg); background: rgba(22,23,27,.82); }
.cc { position: absolute; left: 210px; top: 90px; width: 1500px; height: 900px; border-radius: 20px; overflow: hidden; background: #1E1E1D; box-shadow: 0 50px 120px rgba(0,0,0,.7), 0 0 0 2px #2a2c33; font-family: "Montserrat"; }
.cc .ctop { position: absolute; left: 0; right: 0; top: 0; height: 64px; border-bottom: 1px solid #2E2E2C; display: flex; align-items: center; gap: 22px; padding: 0 26px; color: #C9C8C2; font: 500 24px "Montserrat"; }
.cc .ctop .ic { display: flex; gap: 18px; color: #8E8D87; font: 500 22px "JetBrains Mono", monospace; } .cc .ctop .ttl { color: #E8E7E3; }
.cc .ctop .wn { margin-left: auto; display: flex; gap: 34px; color: #8E8D87; font: 400 24px "Montserrat"; }
.cc .cmsgs { position: absolute; left: 150px; right: 150px; top: 110px; bottom: 190px; display: flex; flex-direction: column; gap: 26px; justify-content: flex-end; }
.cc .ub { align-self: flex-end; max-width: 1000px; background: #2F2F2D; border-radius: 22px; padding: 22px 30px; color: #ECECEA; font: 500 40px/1.45 "Montserrat"; }
.cc .cl { color: #E8E7E3; font: 500 40px/1.5 "Montserrat"; position: relative; padding-left: 50px; } .cc .cl .st { position: absolute; left: 0; top: 2px; color: #D97757; font: 700 34px "Montserrat"; display: inline-block; }
.cc .cin { position: absolute; left: 200px; right: 200px; bottom: 74px; height: 92px; border-radius: 20px; background: #262624; border: 1px solid #3A3A38; display: flex; align-items: center; padding: 0 30px; color: #8E8D87; font: 500 34px "Montserrat"; }
.cc .cin .tx { color: #ECECEA; white-space: nowrap; overflow: hidden; max-width: 960px; } .cc .cin .tx .ch { opacity: 0; } .cc .cin .ph { position: absolute; left: 30px; }
.cc .cin .snd { margin-left: auto; width: 46px; height: 46px; border-radius: 12px; background: #3A3A38; flex: none; }
.cc .cft { position: absolute; right: 200px; bottom: 26px; color: #8E8D87; font: 500 22px "Montserrat"; } .cc .cft b { color: #C9C8C2; font-weight: 600; }
.win { position: absolute; border-radius: 22px; overflow: hidden; background: #111216; box-shadow: 0 50px 120px rgba(0,0,0,.7), 0 0 0 2px #2a2c33; }
.win .bar .lb { font-size: 24px; }
.wbody { position: absolute; left: 0; top: 56px; right: 0; bottom: 0; }
.sk { position: absolute; height: 74px; padding: 0 26px; border-radius: 16px; background: #1F2026; border: 2px solid #3a3c43; display: flex; align-items: center; gap: 14px; font: 600 27px "JetBrains Mono", monospace; color: #E6E6E3; white-space: nowrap; }
.sk i { width: 16px; height: 16px; border-radius: 4px; background: #5a5c63; display: block; flex: none; }
.sk.bl span { filter: blur(9px); } .sk.on { border-color: #F2C200; box-shadow: 0 0 40px rgba(242,194,0,.3); } .sk.on i { background: #F2C200; } .sk.bad { border-color: #E5484D; }
.post { position: absolute; width: 640px; padding: 34px 38px; border-radius: 24px; background: #1F2026; border: 2px solid #3a3c43; box-shadow: 0 30px 80px rgba(0,0,0,.55); }
.post .ph { display: flex; align-items: center; gap: 18px; margin-bottom: 22px; } .post .av { width: 64px; height: 64px; border-radius: 50%; background: #3a3c43; }
.post .ph i { display: block; width: 180px; height: 18px; border-radius: 9px; background: #3a3c43; } .post b { display: block; font: 900 50px/1.1 "Montserrat"; color: #F4F4F2; }
.post .ft { display: flex; gap: 40px; margin-top: 26px; } .post .ft i { display: block; width: 70px; height: 16px; border-radius: 8px; background: #2c2e35; }
.thumb { position: absolute; width: 300px; height: 169px; border-radius: 14px; background: #24262d; border: 2px solid #33353d; overflow: hidden; }
.thumb::after { content: ""; position: absolute; left: 0; bottom: 0; height: 7px; width: var(--p, 60%); background: #E5484D; }
.thumb .pl { position: absolute; left: 50%; top: 50%; width: 0; height: 0; border-left: 34px solid #5a5c63; border-top: 21px solid transparent; border-bottom: 21px solid transparent; transform: translate(-40%, -50%); }
.thumb b { position: absolute; left: 16px; top: 16px; width: 55%; height: 14px; border-radius: 7px; background: #4a4c55; }
.pcard { position: absolute; width: 330px; height: 92px; border-radius: 16px; background: #1F2026; border: 2px solid #3a3c43; display: flex; align-items: center; gap: 14px; padding: 0 20px; font: 600 26px "JetBrains Mono", monospace; color: #9a9ba0; }
.pcard i { width: 26px; height: 26px; border-radius: 6px; background: #F2C200; opacity: .7; display: block; }
.pcount { position: absolute; left: 0; right: 0; top: 380px; text-align: center; font: 900 220px/1 "Montserrat"; color: #F4F4F2; text-shadow: 0 20px 60px rgba(0,0,0,.85); }
.pcount small { display: block; font-size: 64px; margin-top: 10px; }
.recipe { position: absolute; width: 330px; height: 430px; border-radius: 22px; background: #F4F4F2; padding: 30px; box-shadow: 0 34px 80px rgba(0,0,0,.55); display: flex; flex-direction: column; gap: 16px; }
.recipe b { font: 900 34px "Montserrat"; color: #16171B; text-transform: uppercase; } .recipe i { display: block; height: 14px; border-radius: 7px; background: #CFCBC0; }
.recipe .img { height: 150px; border-radius: 14px; background: #E7E3D8; margin-bottom: 6px; }
.recipe.gold .img { background: linear-gradient(160deg, #EDE62A, #E8B000); }
.tc { position: absolute; top: 300px; width: 520px; height: 420px; border-radius: 30px; background: #1F2026; border: 3px solid #3a3c43; display: flex; flex-direction: column; justify-content: center; padding: 0 50px; box-shadow: 0 40px 100px rgba(0,0,0,.6); }
.tc em { font: 700 48px "JetBrains Mono", monospace; font-style: normal; color: #6b6c72; } .tc b { font: 900 76px/1 "Montserrat"; color: #F4F4F2; text-transform: uppercase; letter-spacing: -.02em; margin: 18px 0 14px; } .tc span { font: 600 34px "Montserrat"; color: #9a9ba0; }
.tc.on { border-color: #F2C200; box-shadow: 0 0 70px rgba(242,194,0,.25), 0 40px 100px rgba(0,0,0,.6); } .tc.on em { color: #F2C200; }
.boss { position: absolute; left: 810px; top: 110px; width: 300px; height: 300px; border-radius: 50%; overflow: hidden; border: 8px solid #F4F4F2; box-shadow: 0 30px 80px rgba(0,0,0,.6); }
.boss img { width: 100%; height: 100%; object-fit: cover; display: block; }
.bosslab { position: absolute; left: 0; right: 0; top: 430px; text-align: center; font: 700 34px "JetBrains Mono", monospace; color: #9a9ba0; }
.mate { position: absolute; top: 640px; width: 260px; height: 230px; border-radius: 26px; background: #1F2026; border: 2px solid #3a3c43; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 22px; font: 800 36px "Montserrat"; color: #F4F4F2; }
.ccard { position: absolute; width: 150px; height: 104px; border-radius: 14px; background: #1F2026; border: 2px solid #33353d; padding: 16px; display: flex; flex-direction: column; gap: 10px; }
.ccard i { display: block; height: 10px; border-radius: 5px; background: #3a3c43; } .ccard u { display: block; height: 22px; width: 60%; border-radius: 6px; background: #2c2e35; }
.qm { position: absolute; font: 900 120px "Montserrat"; color: #F2C200; }
.fold { position: absolute; top: 260px; width: 700px; height: 330px; box-sizing: border-box; border-radius: 26px; background: #1F2026; border: 3px solid #3a3c43; padding: 40px 46px; box-shadow: 0 40px 100px rgba(0,0,0,.6); }
.fold.on { border-color: #F2C200; } .fold .fh { display: flex; align-items: center; gap: 20px; font: 800 44px "Montserrat"; color: #F4F4F2; margin-bottom: 30px; }
.fold .fr { display: flex; align-items: center; gap: 18px; font: 500 34px "JetBrains Mono", monospace; color: #c9cacf; margin: 18px 0 0 10px; }
.neq { position: absolute; left: 900px; top: 350px; width: 120px; height: 150px; line-height: 150px; text-align: center; font: 900 130px "Montserrat"; color: #E5484D; }
.lrow { display: flex; align-items: baseline; gap: 26px; padding: 22px 34px; border-bottom: 1px solid #23252b; font: 500 30px "JetBrains Mono", monospace; }
.lrow b { color: #F4F4F2; font-weight: 700; flex: none; width: 360px; } .lrow span { color: #6b6c72; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.lrow.on { background: rgba(242,194,0,.08); } .lrow.on b { color: #F2C200; }
.full { padding: 10px 34px 30px 420px; display: flex; flex-direction: column; gap: 14px; } .full i { display: block; height: 16px; border-radius: 8px; background: #3a3c43; }
.bar2 { position: absolute; left: 260px; height: 110px; border-radius: 55px; transform-origin: 0 50%; }
.bar2l { position: absolute; left: 260px; font: 800 46px "Montserrat"; color: #F4F4F2; }
.ck { position: absolute; left: 560px; top: 210px; width: 800px; border-radius: 26px; background: #1F2026; border: 3px solid #3a3c43; padding: 40px 50px; box-shadow: 0 40px 100px rgba(0,0,0,.6); }
.ck .ch { font: 500 30px "JetBrains Mono", monospace; color: #9a9ba0; margin-bottom: 26px; }
.ck .cr { display: flex; align-items: center; gap: 30px; padding: 26px 10px; font: 800 52px "Montserrat"; color: #F4F4F2; border-radius: 16px; }
.ck .bx { width: 64px; height: 64px; border-radius: 14px; border: 4px solid #5a5c63; display: flex; align-items: center; justify-content: center; font: 900 46px "Montserrat"; color: #16171B; flex: none; }
.ck .bx.ok { background: #F2C200; border-color: #F2C200; } .ck .bx.no { background: #E5484D; border-color: #E5484D; color: #fff; } .ck .cr.no { color: #ff9a9d; }
.fls { font: 500 26px/1.45 "JetBrains Mono", monospace; color: #c9cacf; padding: 30px 40px 0; } .fls div { opacity: 0; } .fls b { color: #FF6B6B; font-weight: 700; }
.gp { position: absolute; width: 680px; border-radius: 24px; background: #1F2026; border: 3px solid #3a3c43; padding: 34px 40px; box-shadow: 0 40px 100px rgba(0,0,0,.6); }
.gp.on { border-color: #F2C200; } .gp .pn { display: flex; align-items: center; gap: 20px; font: 700 36px "JetBrains Mono", monospace; color: #F4F4F2; margin-bottom: 20px; }
.gp .ps { display: flex; align-items: center; gap: 18px; font: 500 32px "JetBrains Mono", monospace; color: #c9cacf; margin: 12px 0 0 20px; }
.ubar { position: absolute; left: 360px; top: 480px; width: 1200px; height: 110px; border-radius: 55px; background: #24262c; overflow: hidden; }
.ubar i { display: block; height: 100%; width: 100%; transform-origin: 0 50%; border-radius: 55px; }
.ulab { position: absolute; left: 360px; top: 380px; font: 700 40px "JetBrains Mono", monospace; color: #9a9ba0; } .uend { position: absolute; left: 1360px; top: 630px; font: 800 44px "Montserrat"; color: #E5484D; }
.msg { position: absolute; left: 300px; width: 700px; height: 54px; border-radius: 18px; background: #2F2F2D; }
.msg.c { left: 260px; background: #1F2026; border: 2px solid #33353d; width: 760px; }
.mcount { position: absolute; left: 1140px; top: 300px; font: 900 150px/1 "Montserrat"; color: #F4F4F2; } .mcount small { display: block; font: 700 40px "JetBrains Mono", monospace; color: #9a9ba0; margin-top: 18px; }
.srv { position: absolute; left: 1180px; top: 640px; display: flex; align-items: center; gap: 24px; font: 700 40px "JetBrains Mono", monospace; color: #9a9ba0; }
.tree { position: absolute; left: 380px; top: 130px; width: 1160px; height: 830px; }
.tr2 { font: 500 38px/1.55 "JetBrains Mono", monospace; color: #c9cacf; white-space: pre; padding: 4px 18px; border-radius: 10px; }
.tr2.dir { color: #F4F4F2; font-weight: 700; } .tr2.on { color: #F2C200; background: rgba(242,194,0,.1); }
.sform { position: absolute; left: 140px; top: 200px; width: 680px; height: 700px; border-radius: 22px; overflow: hidden; background: #1a1b20; box-shadow: 0 50px 120px rgba(0,0,0,.7), 0 0 0 2px #2a2c33; }
.sform .in { position: absolute; left: 0; top: 56px; right: 0; bottom: 0; display: flex; flex-direction: column; justify-content: center; gap: 22px; padding: 0 80px; }
.sform .in i { display: block; height: 70px; border-radius: 14px; background: #16171B; border: 2px solid #3a3c43; } .sform .in b { display: block; height: 30px; width: 60%; border-radius: 10px; background: #55575f; margin-bottom: 20px; }
.sform .in u { display: block; height: 76px; border-radius: 14px; background: #F2C200; margin-top: 10px; }
.lnode { position: absolute; left: 960px; width: 820px; height: 120px; border-radius: 26px; background: #1F2026; border: 3px solid #3a3c43; display: flex; align-items: center; gap: 28px; padding: 0 36px; font: 800 42px "Montserrat"; color: #F4F4F2; }
.lnode.red { border-color: #E5484D; color: #ff9a9d; }
.flw { position: absolute; width: 520px; height: 340px; border-radius: 24px; background: #111216; box-shadow: 0 40px 100px rgba(0,0,0,.6), 0 0 0 2px #2a2c33; overflow: hidden; }
/* light page: white cards, dark ink */
.gcap { color: #1F1E1D; } .mstamp { background: rgba(255,255,255,.92); }
.sk { background: #FFFFFF; border-color: #E3DFD4; color: #1F1E1D; box-shadow: 0 10px 30px rgba(31,30,29,.06); } .sk i { background: #CFCBC0; }
.thumb { background: #FFFFFF; border-color: #E3DFD4; box-shadow: 0 14px 34px rgba(31,30,29,.08); } .thumb b { background: #DAD6CB; } .thumb .pl { border-left-color: #A3A199; }
.pcard { background: #FFFFFF; border-color: #E3DFD4; color: #73726C; box-shadow: 0 14px 34px rgba(31,30,29,.08); } .pcount { color: #1F1E1D; text-shadow: none; } .pcount small { color: #1F1E1D; }
.recipe { box-shadow: 0 30px 70px rgba(31,30,29,.16); border: 1px solid #E3DFD4; }
.ubar { background: #E7E3D8; } .ulab { color: #73726C; }
.tc { background: #FFFFFF; border-color: #E3DFD4; box-shadow: 0 30px 80px rgba(31,30,29,.08); } .tc b { color: #1F1E1D; font-size: 64px; } .tc span { color: #73726C; }
.cap.dk { color: #73726C; }
'''

ICONS = {"terminal": "M3 5h18v14H3z M7 9l3 3-3 3 M12 15h5", "folder": "M3 6h6l2 2h10v11H3z", "file": "M6 2h9l5 5v15H6z M15 2v5h5",
         "claude": "M12 3v18 M3 12h18 M5.6 5.6l12.8 12.8 M18.4 5.6L5.6 18.4", "browser": "M3 4h18v16H3z M3 9h18 M6 6.5h.01 M9 6.5h.01",
         "lock": "M6 11h12v10H6z M8 11V7a4 4 0 0 1 8 0v4", "mail": "M3 5h18v14H3z M3 6l9 7 9-7", "key": "M14 10a4 4 0 1 0-1 2.6L21 21 M17 17l2-2",
         "db": "M4 6c0-2 16-2 16 0v12c0 2-16 2-16 0z M4 6c0 2 16 2 16 0 M4 12c0 2 16 2 16 0", "alert": "M12 3L2 21h20z M12 10v5 M12 18h.01",
         "send": "M3 11l18-8-8 18-2-8z"}
def icon(n, size, col="#1F1E1D"):
    return f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="{col}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="{ICONS[n]}"/></svg>'
def vid(i, src, t0, start, dur, mstart=0.0, extra=""):
    return f'<video id="{i}" class="clip" src="assets/{src}" muted playsinline data-start="{start - t0:.3f}" data-duration="{dur:.3f}" data-media-start="{mstart:.2f}" data-track-index="2"{extra}></video>'
def win(I, idn, x, y, w, h, label, inner):
    return f'<div class="win" id="{I(idn)}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><div class="bar"><i></i><i></i><i></i><span class="lb">{H.escape(label)}</span></div><div class="wbody">{inner}</div></div>'
def rise(sel, at, P, y=50, dur=.35):
    return f'tl.fromTo("{sel}",{{y:{y},opacity:0}},{{y:0,opacity:1,duration:{dur},ease:"expo.out"}},{P(at)});'
def chip(I, idn, txt, col, at, P, extra=""):
    # never put text this low (the player bar covers it): chips stay at top <= 760
    extra = re.sub(r"top:(\d+)px", lambda m: f"top:{min(int(m.group(1)), 760)}px", extra)
    return (f'<div class="chip2 {col}" id="{I(idn)}" style="position:absolute;{extra}"><i></i>{H.escape(txt)}</div>',
            f'gsap.set("#{I(idn)}",{{opacity:0}});tl.fromTo("#{I(idn)}",{{opacity:0,y:24,scale:.9}},{{opacity:1,y:0,scale:1,duration:.3,ease:"back.out(1.7)"}},{P(at)});')

def k_pile(s, t, e, d, I, W, P, R, fx, t0):
    rnd = random.Random(4); n = s.get("n", 28); lab = s["label"]
    h = "".join(f'<div class="pcard" id="{I(f"c{q}")}" style="left:{rnd.randint(100, 1480)}px;top:{rnd.randint(100, 900)}px;transform:rotate({rnd.randint(-12, 12)}deg)"><i></i>{H.escape(lab)}</div>' for q in range(n))
    h += f'<div class="pcount" id="{I("n")}"><span id="{I("nv")}">0</span><small>{H.escape(s.get("small", "saved prompts"))}</small></div>'
    step = (d - .5) / n
    js = [f'gsap.set("#{I("")} .pcard",{{opacity:0}});tl.fromTo("#{I("n")}",{{opacity:0,scale:.8}},{{opacity:1,scale:1,duration:.3,ease:"back.out(1.6)"}},{P(t + .1)});',
          f'for(let q=0;q<{n};q++){{tl.fromTo("#{I("c")}"+q,{{opacity:0,y:-50}},{{opacity:1,y:0,duration:.2,ease:"power2.out"}},{R(t + .1):.3f}+q*{step:.3f});tl.set("#{I("nv")}",{{textContent:String(q+1)}},{R(t + .1):.3f}+q*{step:.3f});}}']
    return h, js

def k_chapter(s, t, e, d, I, W, P, R, fx, t0):
    h = f'<div class="tcard"><div class="no" id="{I("a")}">{s["no"]} / 03</div><div class="nm" id="{I("b")}">{H.escape(s["name"])}</div><div class="sb" id="{I("c")}">{H.escape(s["sub"])}</div></div>'
    js = [f'tl.fromTo(["#{I("a")}","#{I("b")}","#{I("c")}"],{{opacity:0,y:40}},{{opacity:1,y:0,duration:.4,ease:"expo.out",stagger:.12}},{P(t)});',
          f'tl.fromTo("#{I("b")}",{{scale:1}},{{scale:1.05,duration:{d:.2f},ease:"none"}},{P(t)});']
    return h, js

def k_bars2(s, t, e, d, I, W, P, R, fx, t0):
    # two bars compared: a=("label", value) grows first, b=("label", value) grows on b_at; widths follow the real values
    (la, va), (lb, vb) = s.get("a", ("small", 1)), s.get("b", ("big", 5)); mx = max(va, vb) or 1
    pr = W(s.get("b_at"), t + 1.6)
    h = (f'<div class="bar2l" style="top:300px" id="{I("la")}">{H.escape(la)}</div><div class="bar2" id="{I("a")}" style="top:370px;width:{max(40, round(1400 * va / mx))}px;background:linear-gradient(180deg,#EDE62A,#E8B000)"></div>'
         f'<div class="bar2l" style="top:580px" id="{I("lb")}">{H.escape(lb)}</div><div class="bar2" id="{I("b")}" style="top:650px;width:{max(40, round(1400 * vb / mx))}px;background:{"#E5484D" if s.get("b_bad", True) else "#1F1E1D"}"></div>'
         f'<div class="cap" style="left:260px;top:180px;text-align:left;color:#73726C">{H.escape(s.get("title", ""))}</div>')
    js = [f'gsap.set(["#{I("a")}","#{I("b")}"],{{scaleX:0}});tl.fromTo("#{I("la")}",{{opacity:0}},{{opacity:1,duration:.2}},{P(t)});tl.to("#{I("a")}",{{scaleX:1,duration:.5,ease:"power2.out"}},{P(t + .2)});',
          f'gsap.set("#{I("lb")}",{{opacity:0}});tl.to("#{I("lb")}",{{opacity:1,duration:.2}},{P(pr - .4)});tl.to("#{I("b")}",{{scaleX:1,duration:.9,ease:"power2.out"}},{P(pr - .3)});']
    fx(pr - .3, "pop")
    return h, js

REF_CSS = r'''
.nd { position: absolute; display: flex; align-items: center; gap: 18px; padding: 22px 34px; border-radius: 26px; background: #FFFFFF; border: 2px solid #E3DFD4; box-shadow: 0 24px 60px rgba(31,30,29,.08); font: 800 40px "Montserrat"; color: #1F1E1D; white-space: nowrap; transform: translate(-50%, -50%); }
.nd.c { padding: 34px; border-radius: 40px; border: 4px solid #F2C200; box-shadow: 0 0 70px rgba(242,194,0,.35), 0 30px 70px rgba(31,30,29,.1); }
.nd.sm { font: 600 26px "JetBrains Mono", monospace; padding: 14px 22px; border-radius: 16px; }
.nd.bad { border-color: #E5484D; box-shadow: 0 0 60px rgba(229,72,77,.3); }
.ndl { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; overflow: visible; }
.tok2 { position: absolute; width: 74px; height: 74px; border-radius: 18px; background: linear-gradient(180deg, #EDE62A, #E8B000); box-shadow: 0 10px 24px rgba(185,133,0,.25); }
.meterlab { position: absolute; left: 0; right: 0; text-align: center; font: 700 40px "JetBrains Mono", monospace; color: #73726C; }
.mcnt { position: absolute; left: 0; right: 0; top: 230px; text-align: center; font: 900 170px/1 "Montserrat"; color: #1F1E1D; }
.bigw { position: absolute; left: 0; right: 0; text-align: center; font: 900 150px/1 "Montserrat"; text-transform: uppercase; letter-spacing: -.03em; color: #1F1E1D; }
.bigw .ln2 { display: inline-block; position: relative; }
.strk { position: absolute; left: -2%; top: 52%; height: 18px; width: 104%; background: #E5484D; border-radius: 9px; transform-origin: 0 50%; }
.try { position: absolute; top: 300px; width: 300px; height: 380px; border-radius: 22px; background: #FFFFFF; border: 2px solid #E3DFD4; box-shadow: 0 24px 60px rgba(31,30,29,.08); padding: 26px; display: flex; flex-direction: column; gap: 14px; }
.try i { display: block; height: 16px; border-radius: 8px; background: #E7E3D8; } .try u { display: block; height: 120px; border-radius: 14px; background: #F1EEE6; margin-bottom: 6px; }
.try b { position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); width: 120px; height: 120px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font: 900 74px "Montserrat"; color: #fff; }
.try b.x { background: #E5484D; } .try b.ok { background: linear-gradient(180deg, #EDE62A, #E8B000); color: #1F1E1D; }
.try.on { border-color: #F2C200; box-shadow: 0 0 70px rgba(242,194,0,.35); }
.tryl { position: absolute; top: 720px; width: 300px; text-align: center; font: 700 30px "JetBrains Mono", monospace; color: #A3A199; }
'''
REF_CSS += r'''
.ytc { position: absolute; width: 420px; }
.ytc .th { width: 420px; height: 236px; border-radius: 16px; overflow: hidden; background: #DAD6CB; box-shadow: 0 16px 40px rgba(31,30,29,.14); }
.ytc .th img { width: 100%; height: 100%; object-fit: cover; display: block; }
.ytc .tt { margin-top: 14px; font: 700 22px/1.3 "Montserrat"; color: #1F1E1D; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.ytc .tt mark { background: #F2C200; color: #1F1E1D; padding: 0 4px; border-radius: 4px; }
.ytc .mt { margin-top: 6px; font: 500 19px "Montserrat"; color: #73726C; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
'''
KIT_CSS += REF_CSS

def k_nodes(s, t, e, d, I, W, P, R, fx, t0):
    """centre node + satellites joined by lines that draw on their cue word """
    cx, cy = s.get("center_xy", (960, 540)); items = s["items"]; bad = s.get("mode") == "tangle"
    h = f'<svg class="ndl" id="{I("svg")}">'
    for q, (lab, x, y, cue) in enumerate(items):
        h += f'<line id="{I(f"l{q}")}" x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="{"#E5484D" if bad else "#CFCBC0"}" stroke-width="4" stroke-dasharray="10 12"/>'
    h += '</svg>'
    h += f'<div class="nd c" id="{I("c")}" style="left:{cx}px;top:{cy}px">{icon("claude", 90, "#D97757")}</div>'
    for q, (lab, x, y, cue) in enumerate(items):
        h += f'<div class="nd{" sm" if bad else ""}" id="{I(f"n{q}")}" style="left:{x}px;top:{y}px">{H.escape(lab)}</div>'
    js = [f'tl.fromTo("#{I("c")}",{{opacity:0,scale:.5}},{{opacity:1,scale:1,duration:.4,ease:"back.out(1.7)"}},{P(t)});',
          f'tl.fromTo("#{I("c")}",{{scale:1}},{{scale:1.06,duration:.6,yoyo:true,repeat:{max(int(d / .6) - 1, 1)},ease:"sine.inOut"}},{P(t + .5)});']
    last = t + .2
    for q, (lab, x, y, cue) in enumerate(items):
        at = W(cue, last + .35) if cue else last + (.08 if bad else .5); at = max(at, last + (.05 if bad else .3)); last = at
        js.append(f'gsap.set(["#{I(f"n{q}")}","#{I(f"l{q}")}"],{{opacity:0}});tl.fromTo("#{I(f"l{q}")}",{{opacity:0}},{{opacity:1,duration:.25}},{P(at - .1)});'
                  f'tl.fromTo("#{I(f"n{q}")}",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.3,ease:"back.out(1.8)"}},{P(at)});')
        if not bad: fx(at, "pop")
    if bad:
        js.append(f'tl.to("#{I("c")}",{{borderColor:"#E5484D",boxShadow:"0 0 80px rgba(229,72,77,.45)",duration:.3}},{P(last + .3)});tl.to("#{I("")} .nd.sm",{{borderColor:"#E5484D",color:"#C0353A",duration:.25,stagger:.02}},{P(last + .3)});')
        fx(last + .3, "error_buzz") if s.get("buzz") else None
    js.append(f'tl.fromTo("#{I("")}",{{scale:1}},{{scale:1.05,duration:{d:.2f},ease:"none"}},{P(t)});')
    return h, js

def k_meter(s, t, e, d, I, W, P, R, fx, t0):
    """capacity meter: a row of token blocks . vanish = they disappear; fill = they pile up to the limit"""
    n = 16; mode = s.get("mode", "vanish"); h = ""
    for q in range(n):
        h += f'<div class="tok2" id="{I(f"k{q}")}" style="left:{230 + q * 92}px;top:500px"></div>'
    h += f'<div class="meterlab" style="top:620px">{H.escape(s.get("label", "tokens"))}</div>'
    js = []
    if mode == "low":   # a fresh chat: only a few blocks used, the rest of the day is still there
        js.append(f'gsap.set("#{I("")} .tok2",{{opacity:.18}});tl.to(["#{I("k0")}","#{I("k1")}","#{I("k2")}"],{{opacity:1,duration:.2,stagger:.12}},{P(t + .2)});')
        return h, js
    if mode == "vanish":
        js.append(f'tl.to("#{I("")} .tok2",{{opacity:0,y:-50,scale:.6,duration:.22,stagger:{{each:{min(.08, (d - .6) / n):.3f},from:"end"}}}},{P(t + .3)});')
        fx(t + .3, "whoosh")
    else:
        js.append(f'gsap.set("#{I("")} .tok2",{{opacity:0}});tl.to("#{I("")} .tok2",{{opacity:1,duration:.15,stagger:{(d - 1.0) / n:.3f}}},{P(t + .2)});')
        js.append(f'tl.to("#{I("")} .tok2",{{background:"#E5484D",duration:.25}},{P(e - .7)});'); fx(e - .7, "bass_hit")
    return h, js

def k_strike(s, t, e, d, I, W, P, R, fx, t0):
    """the old idea gets crossed out in red, the new one rises in gold"""
    old, new = s["old"], s["new"]; sc, nc = W(s["strike_at"], t + .9), W(s["new_at"], t + 2.4)
    h = (f'<div class="bigw" id="{I("a")}" style="top:330px;font-size:{s.get("size_old", 130)}px"><span class="ln2">{H.escape(old)}<i class="strk" id="{I("s")}"></i></span></div>'
         f'<div class="bigw" id="{I("b")}" style="top:560px;font-size:{s.get("size_new", 150)}px"><span class="goldg">{H.escape(new)}</span></div>')
    js = [f'tl.fromTo("#{I("a")}",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.35,ease:"expo.out"}},{P(t)});gsap.set("#{I("s")}",{{scaleX:0}});tl.to("#{I("s")}",{{scaleX:1,duration:.35,ease:"power2.inOut"}},{P(sc)});tl.to("#{I("a")}",{{opacity:.35,duration:.3}},{P(sc + .35)});',
          f'gsap.set("#{I("b")}",{{opacity:0}});tl.fromTo("#{I("b")}",{{opacity:0,y:60}},{{opacity:1,y:0,duration:.45,ease:"expo.out"}},{P(nc)});']
    fx(sc, "pop"); fx(nc, "impact_boom")
    return h, js

def k_tries(s, t, e, d, I, W, P, R, fx, t0):
    """kept testing: attempts fail (red X) one by one until one works (gold check) on the cue word"""
    n = 5; h = ""
    for q in range(n):
        x = 120 + q * 345
        h += f'<div class="try" id="{I(f"c{q}")}" style="left:{x}px"><u></u><i style="width:80%"></i><i style="width:60%"></i><i style="width:70%"></i><b class="{"ok" if q == n - 1 else "x"}" id="{I(f"b{q}")}">{"✓" if q == n - 1 else "✗"}</b></div><div class="tryl" style="left:{x}px">test {q + 1}</div>'
    ok = W(s.get("ok_at"), e - .8); step = max((ok - t - .4) / (n - 1), .25)
    if s.get("fast"): step = .16; ok = min(t + .4 + (n - 1) * step + .1, e - .3)
    js = [f'gsap.set("#{I("")} .try b",{{opacity:0,scale:.4}});tl.fromTo("#{I("")} .try",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.3,ease:"expo.out",stagger:.08}},{P(t)});']
    for q in range(n - 1):
        a = t + .4 + q * step; js.append(f'tl.to("#{I(f"b{q}")}",{{opacity:1,scale:1,duration:.22,ease:"back.out(2)"}},{P(a)});'); fx(a, "pop")
    js.append(f'tl.to("#{I(f"b{n - 1}")}",{{opacity:1,scale:1,duration:.3,ease:"back.out(2)"}},{P(ok)});tl.set("#{I(f"c{n - 1}")}",{{attr:{{class:"try on"}}}},{P(ok)});tl.to(["#{I("c0")}","#{I("c1")}","#{I("c2")}","#{I("c3")}"],{{opacity:.35,duration:.3}},{P(ok)});')
    fx(ok, "ding_sparkle")
    wa = W(s.get("win_at"), None) if s.get("win_label") else None
    if wa:   # the winning test grows to the middle, "the results I wanted" under it
        js.append(f'tl.to("#{I(f"c{n - 1}")}",{{x:-{120 + (n - 1) * 345 - 810},scale:1.35,duration:.5,ease:"power3.inOut"}},{P(wa - 1.0)});tl.to(["#{I("c0")}","#{I("c1")}","#{I("c2")}","#{I("c3")}","#{I("")} .tryl"],{{opacity:0,duration:.3}},{P(wa - 1.0)});')
        c_, j_ = chip(I, "w", s.get("win_label", ""), "green", wa - .2, P, "left:640px;top:880px"); h += c_; js.append(j_)
    return h, js

def k_ytwall(s, t, e, d, I, W, P, R, fx, t0):
    """a feed of REAL popular Claude videos (thumbnail, title, channel, views), flying in and scrolling like YouTube"""
    vids = YT_HYPE if s["set"] == "hype" else YT_TUTS; h = ""
    hot = re.compile(r"(insane|scary|cooked|too late|master|tutorial|getting started|full workflow|top 1%)", re.I)
    for q, (vid_, title, ch, views) in enumerate(vids):
        x, y = 30 + (q % 4) * 470, 40 + (q // 4) * 360
        tt = H.escape(title)   # no highlights on the titles
        vw = f"{views / 1e6:.1f}M" if views >= 1e6 else f"{views // 1000}K"
        h += f'<div class="ytc" id="{I(f"v{q}")}" style="left:{x}px;top:{y}px"><div class="th"><img src="assets/yt/{vid_}.jpg" alt="" /></div><div class="tt">{tt}</div><div class="mt">{H.escape(ch)} · {vw} views</div></div>'
    h = f'<div id="{I("feed")}" style="position:absolute;inset:0">{h}</div>'
    rows = (len(vids) + 3) // 4
    js = [f'gsap.set("#{I("")} .ytc",{{opacity:0}});tl.fromTo("#{I("")} .ytc",{{opacity:0,y:60,scale:.9}},{{opacity:1,y:0,scale:1,duration:.3,ease:"back.out(1.5)",stagger:{min(.07, (d - .6) / len(vids)):.3f}}},{P(t)});',
          f'tl.fromTo("#{I("feed")}",{{y:0}},{{y:{-max(rows * 360 - 1040, 0)},duration:{d:.2f},ease:"power1.inOut"}},{P(t)});']
    return h, js

LIMIT_CSS = r'''
.lim .cmsgs { justify-content: flex-start; }
.lim .ub.old { opacity: .55; } .lim .cl.old { opacity: .55; }
.limbar { position: absolute; left: 200px; right: 200px; bottom: 60px; height: 132px; border-radius: 22px; background: #2B2220; border: 2px solid #8A3B32; display: flex; align-items: center; gap: 26px; padding: 0 36px; }
.limbar .lt { font: 700 36px "Montserrat"; color: #F4DCD7; } .limbar .ls { font: 500 28px "Montserrat"; color: #C9A9A2; margin-top: 6px; }
.limbar .ug { margin-left: auto; padding: 18px 30px; border-radius: 14px; background: #D97757; color: #1E1E1D; font: 800 28px "Montserrat"; }
'''
KIT_CSS += LIMIT_CSS


REST_CSS = r"""
/* light-page colours for the kinds above */
.mate { background: #FFFFFF; border-color: #E3DFD4; color: #1F1E1D; box-shadow: 0 24px 60px rgba(31,30,29,.08); } .boss { border-color: #FFFFFF; box-shadow: 0 30px 80px rgba(31,30,29,.2); } .bosslab { color: #73726C; }
.ccard { background: #FFFFFF; border-color: #E3DFD4; } .ccard i { background: #E7E3D8; } .ccard u { background: #F1EEE6; }
.post { background: #FFFFFF; border-color: #E3DFD4; box-shadow: 0 30px 80px rgba(31,30,29,.1); } .post b { color: #1F1E1D; } .post .av, .post .ph i { background: #E3DFD4; } .post .ft i { background: #EFECE4; }
.fold { background: #FFFFFF; border-color: #E3DFD4; box-shadow: 0 30px 80px rgba(31,30,29,.08); } .fold .fh { color: #1F1E1D; } .fold .fr { color: #4A4945; }
.bar2l { color: #1F1E1D; }
.ck { background: #FFFFFF; border-color: #E3DFD4; box-shadow: 0 30px 80px rgba(31,30,29,.08); } .ck .cr { color: #1F1E1D; } .ck .bx { border-color: #CFCBC0; } .ck .ch { color: #73726C; }
.gp { background: #FFFFFF; border-color: #E3DFD4; box-shadow: 0 30px 80px rgba(31,30,29,.08); } .gp .pn { color: #1F1E1D; } .gp .ps { color: #4A4945; }
.msg { background: #E3DFD4; } .msg.c { background: #FFFFFF; border-color: #E3DFD4; } .mcount { color: #1F1E1D; } .mcount small, .srv { color: #73726C; }
.lnode { background: #FFFFFF; border-color: #E3DFD4; color: #1F1E1D; box-shadow: 0 20px 50px rgba(31,30,29,.07); } .lnode.red { border-color: #E5484D; color: #C0353A; }
.qm { color: #C99A00; } .neq { color: #E5484D; }
.rcard { background: #FFFFFF; border-color: #E3DFD4; box-shadow: 0 14px 34px rgba(31,30,29,.07); } .rcard b { background: #DAD6CB; } .rcard i { background: #EFECE4; }
.doc { position: absolute; left: 260px; top: 90px; width: 1400px; height: 900px; border-radius: 22px; overflow: hidden; background: #FFFFFF; box-shadow: 0 40px 100px rgba(31,30,29,.22), 0 0 0 1px rgba(31,30,29,.08); }
.doc .bar { background: #EFECE4; } .doc .bar .lb { color: #1F1E1D; font-size: 24px; }
.doc .dl { position: absolute; left: 0; right: 0; top: 56px; padding: 40px 60px; }
.doc .ln { position: relative; font: 500 31px/1.75 "JetBrains Mono", monospace; color: #3A3935; white-space: pre-wrap; padding: 0 12px; border-radius: 8px; }
.doc .ln.h { font-weight: 700; color: #1F1E1D; } .doc .ln.m { color: #A3A199; }
.doc .hlb { position: absolute; inset: 0; background: rgba(242,194,0,.38); border-radius: 8px; transform-origin: 0 50%; }
.ord { position: absolute; width: 330px; height: 170px; border-radius: 24px; background: #FFFFFF; border: 2px solid #E3DFD4; box-shadow: 0 24px 60px rgba(31,30,29,.08); display: flex; align-items: center; justify-content: center; gap: 18px; font: 800 46px "Montserrat"; color: #1F1E1D; }
.ord em { font: 700 36px "JetBrains Mono", monospace; font-style: normal; color: #C99A00; }
.ordq { position: absolute; font: 900 90px "Montserrat"; color: #C99A00; }
.qc { position: absolute; top: 330px; width: 300px; height: 220px; border-radius: 22px; background: #FFFFFF; border: 2px solid #E3DFD4; box-shadow: 0 24px 60px rgba(31,30,29,.08); display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 18px; }
.qc b { font: 900 60px "Montserrat"; color: #1F1E1D; } .qc span { font: 600 26px "JetBrains Mono", monospace; color: #73726C; }
.qc.on { border-color: #F2C200; } .qc i { position: absolute; right: 18px; top: 18px; width: 50px; height: 50px; border-radius: 50%; background: linear-gradient(180deg,#EDE62A,#E8B000); display: flex; align-items: center; justify-content: center; font: 900 30px "Montserrat"; font-style: normal; color: #1F1E1D; opacity: 0; }
.draft { position: absolute; left: 660px; top: 260px; width: 600px; height: 520px; border-radius: 26px; background: #FFFFFF; border: 4px solid #F2C200; box-shadow: 0 0 80px rgba(242,194,0,.35); padding: 40px; display: flex; flex-direction: column; gap: 18px; }
.draft b { font: 900 52px "Montserrat"; color: #1F1E1D; } .draft i { display: block; height: 18px; border-radius: 9px; background: #E7E3D8; }
.lc .cmsgs { justify-content: flex-start; } .lc .ub, .lc .cl { font-size: 32px; }
.lc .tagb { display: inline-block; margin-left: 14px; padding: 4px 14px; border-radius: 10px; background: #F2C200; color: #16171B; font: 800 24px "Montserrat"; vertical-align: middle; }
"""
KIT_CSS += REST_CSS

FILES = getattr(_S, "FILES", {})   # {"name": ("window title", ["line 1", "line 2", ...])}

def k_file(s, t, e, d, I, W, P, R, fx, t0):
    """a REAL file in a light window on the cream plate, slow scroll, the spoken line gets a gold highlight on its cue """
    title, lines = FILES[s["file"]]; body = ""
    for q, ln in enumerate(lines):
        cls = "h" if ln.startswith("#") or ln.startswith("name:") else ("m" if ln.strip() in ("---", "") else "")
        body += f'<div class="ln {cls}" id="{I(f"l{q}")}"><i class="hlb" id="{I(f"h{q}")}" style="transform:scaleX(0)"></i><span style="position:relative">{H.escape(ln) or "&nbsp;"}</span></div>'
    h = f'<div class="plate"></div><div class="doc" id="{I("c")}"><div class="bar"><i></i><i></i><i></i><span class="lb">{H.escape(title)}</span></div><div class="dl" id="{I("dl")}">{body}</div></div>'
    js = [f'tl.fromTo("#{I("c")}",{{y:50,opacity:0}},{{y:0,opacity:1,duration:.35,ease:"expo.out"}},{P(t)});tl.fromTo("#{I("c")}",{{scale:.95}},{{scale:1,duration:{d:.2f},ease:"none"}},{P(t)});',
          f'tl.fromTo("#{I("dl")}",{{y:0}},{{y:{-s.get("scroll", 40)},duration:{d:.2f},ease:"none"}},{P(t)});']
    for q, cue in s.get("marks", []):
        a = W(cue, t + .5) if cue else t + .5
        js.append(f'tl.to("#{I(f"h{q}")}",{{scaleX:1,duration:.35,ease:"power2.out"}},{P(a)});'); fx(a, "ding_sparkle")
    return h, js

HAMMER = '<svg viewBox="0 0 24 24" width="150" height="150" fill="none" stroke="#1F1E1D" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M14 4l6 6-3 3-6-6z M11 7L3 15l3 3 8-8"/></svg>'

GAUGE_CSS = r"""
.gauge { position: absolute; left: 510px; top: 170px; width: 900px; height: 520px; }
.glab { position: absolute; left: 0; right: 0; top: 700px; text-align: center; font: 900 64px "Montserrat"; text-transform: uppercase; letter-spacing: -.02em; color: #1F1E1D; }
"""
KIT_CSS += GAUGE_CSS

def k_gauge(s, t, e, d, I, W, P, R, fx, t0):
    """"what actually moves the needle": a gauge whose needle swings into the gold on "needle" """
    arc = ('<svg class="gauge" viewBox="0 0 900 520"><path d="M90 470 A360 360 0 0 1 810 470" fill="none" stroke="#E7E3D8" stroke-width="56" stroke-linecap="round"/>'
           f'<path id="{I("g")}" d="M90 470 A360 360 0 0 1 810 470" fill="none" stroke="#F2C200" stroke-width="56" stroke-linecap="round" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100"/>'
           f'<g id="{I("n")}"><line x1="450" y1="470" x2="450" y2="150" stroke="#1F1E1D" stroke-width="14" stroke-linecap="round"/></g>'
           '<circle cx="450" cy="470" r="34" fill="#1F1E1D"/></svg>')
    lab = s.get("label", ""); acc = s.get("accent_word", "")
    lab_h = " ".join(f'<span class="goldg">{H.escape(x)}</span>' if x == acc else H.escape(x) for x in lab.split())
    h = arc + f'<div class="glab" id="{I("l")}">{lab_h}</div>'
    nd = W(s.get("at_word"), t + 1.2)
    js = [f'gsap.set("#{I("n")}",{{rotation:-80,svgOrigin:"450 470"}});tl.fromTo("#{I("")} .gauge",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.35,ease:"expo.out"}},{P(t)});',
          f'tl.to("#{I("n")}",{{rotation:-55,duration:.6,ease:"sine.inOut",yoyo:true,repeat:1}},{P(t + .2)});',
          f'tl.to("#{I("n")}",{{rotation:68,duration:.7,ease:"back.out(1.4)"}},{P(nd - .2)});tl.to("#{I("g")}",{{strokeDashoffset:12,duration:.7,ease:"power2.out"}},{P(nd - .2)});',
          f'gsap.set("#{I("l")}",{{opacity:0}});tl.fromTo("#{I("l")}",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.3,ease:"expo.out"}},{P(nd - .1)});']
    fx(nd - .2, "ding_sparkle")
    return h, js

NEW = {"gauge": k_gauge, "file": k_file, "ytwall": k_ytwall, "nodes": k_nodes, "meter": k_meter, "strike2": k_strike, "tries": k_tries, "prompts": k_pile,
       "chapter": k_chapter, "bars2": k_bars2}

# --- Extended motion-graphics pack (all themed automatically by theme.py) ---
import math as _math, random as _rnd

_SW = 'fill="none" stroke="#1F1E1D" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"'
_CUR = '<svg viewBox="0 0 24 24" width="60" height="60"><path d="M4 2 L4 20 L9 15.5 L12.5 22 L15.5 20.4 L12 14 L19 14 Z" fill="#FFFFFF" stroke="#1F1E1D" stroke-width="1.8" stroke-linejoin="round"/></svg>'
_LINE_ICONS = {
    "film": '<rect x="10" y="14" width="44" height="36" rx="4"/><path d="M10 24h44M10 40h44M20 14v10M32 14v10M44 14v10M20 40v10M32 40v10M44 40v10"/>',
    "eye": '<path d="M6 32c8-12 18-18 26-18s18 6 26 18c-8 12-18 18-26 18S14 44 6 32z"/><circle cx="32" cy="32" r="8"/>',
    "font": '<path d="M12 50L26 14l14 36M17 38h18"/><path d="M44 30c2-3 5-4 8-4 4 0 6 3 6 7v17M58 42c-3 6-14 8-15 1-1-6 9-7 15-6"/>',
    "palette": '<path d="M32 8C18 8 8 18 8 30c0 12 10 20 20 20 4 0 5-3 3-6-2-4 1-7 5-7h6c8 0 14-5 14-12C56 15 45 8 32 8z"/><circle cx="20" cy="26" r="3"/><circle cx="30" cy="18" r="3"/><circle cx="42" cy="20" r="3"/>',
    "curve": '<path d="M8 54C24 54 24 10 56 10"/><circle cx="56" cy="10" r="3"/><path d="M8 8v46h48"/>',
    "cc": '<rect x="6" y="14" width="52" height="36" rx="6"/><path d="M28 26c-2-3-10-3-10 6s8 9 10 6M44 26c-2-3-10-3-10 6s8 9 10 6"/>',
    "wave": '<path d="M6 32h6l4-12 6 26 6-34 6 40 6-28 6 14 4-6h8"/>',
    "file": '<path d="M16 6h22l12 12v40H16z"/><path d="M38 6v12h12M22 30h20M22 38h20M22 46h14"/>',
    "brain": '<path d="M24 12c-6 0-10 5-9 10-5 2-6 9-2 12-3 4 0 10 5 11 1 5 7 8 12 5V14c-1-1-3-2-6-2zM40 12c6 0 10 5 9 10 5 2 6 9 2 12 3 4 0 10-5 11-1 5-7 8-12 5"/>',
    "doc": '<rect x="14" y="8" width="36" height="48" rx="4"/><path d="M22 20h20M22 28h20M22 36h20M22 44h12"/>',
    "list": '<path d="M24 16h30M24 32h30M24 48h30"/><circle cx="12" cy="16" r="3"/><circle cx="12" cy="32" r="3"/><circle cx="12" cy="48" r="3"/>',
    "image": '<rect x="8" y="12" width="48" height="40" rx="4"/><circle cx="22" cy="25" r="5"/><path d="M8 46l14-12 10 8 10-10 14 14"/>',
    "play": '<rect x="6" y="12" width="52" height="40" rx="8"/><path d="M27 23v18l15-9z"/>',
    "user": '<circle cx="32" cy="20" r="10"/><path d="M12 56c2-12 10-18 20-18s18 6 20 18"/>',
    "wand": '<path d="M10 54L42 22M38 18l8 8"/><path d="M48 6v8M44 10h8M54 26v6M51 29h6M26 8v6M23 11h6"/>',
    "grid": '<rect x="8" y="8" width="48" height="48"/><path d="M24 8v48M40 8v48M8 24h48M8 40h48"/>',
    "clock": '<circle cx="32" cy="34" r="22"/><path d="M32 34V20M32 34l10 6M26 6h12M32 6v6"/>',
    "camera": '<rect x="6" y="18" width="38" height="30" rx="5"/><path d="M44 28l14-8v26l-14-8"/>',
    "folder": '<path d="M6 16h18l6 6h28v30H6z"/>',
    "search": '<circle cx="26" cy="26" r="16"/><path d="M38 38l18 18"/>',
    "chat": '<path d="M8 12h48v30H26l-12 10V42H8z"/>',
    "check": '<path d="M12 34l12 12 28-28"/>',
    "x": '<path d="M14 14l36 36M50 14L14 50"/>',
    "dollar": '<path d="M32 6v52M44 18c-2-4-7-6-12-6-7 0-12 4-12 9 0 12 24 7 24 20 0 5-5 9-12 9-6 0-10-2-12-6"/>',
    "code": '<path d="M22 18L8 32l14 14M42 18l14 14-14 14M36 12l-8 40"/>',
    "card": '<rect x="6" y="10" width="52" height="44" rx="6"/><path d="M14 22h22M14 32h36M14 42h28"/>',
    "lock": '<rect x="12" y="28" width="40" height="28" rx="4"/><path d="M20 28v-8a12 12 0 0124 0v8"/>',
    "heart": '<path d="M32 54S8 40 8 24c0-8 6-14 13-14 5 0 9 3 11 7 2-4 6-7 11-7 7 0 13 6 13 14 0 16-24 30-24 30z"/>',
}

def _rough(pts, seed=1, j=3.0):
    r = _rnd.Random(seed); P = [(x + r.uniform(-j, j), y + r.uniform(-j, j)) for x, y in pts]
    d = f"M{P[0][0]:.1f} {P[0][1]:.1f}"
    for a, b in zip(P[1:], P[2:] + [None]):
        if b is None: d += f" L{a[0]:.1f} {a[1]:.1f}"
        else: d += f" Q{a[0]:.1f} {a[1]:.1f} {(a[0] + b[0]) / 2:.1f} {(a[1] + b[1]) / 2:.1f}"
    return d

def _rarrow(x1, y1, x2, y2, seed=1, bend=40):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2; dx, dy = x2 - x1, y2 - y1; L = _math.hypot(dx, dy) or 1
    cx, cy = mx - dy / L * bend, my + dx / L * bend
    pts = [(x1 + (cx - x1) * t * 2 if t < .5 else cx + (x2 - cx) * (t - .5) * 2, y1 + (cy - y1) * t * 2 if t < .5 else cy + (y2 - cy) * (t - .5) * 2) for t in (0, .25, .5, .75, 1)]
    ang = _math.atan2(y2 - pts[-2][1], x2 - pts[-2][0]); h = 22
    head = _rough([(x2 - h * _math.cos(ang - .5), y2 - h * _math.sin(ang - .5)), (x2, y2), (x2 - h * _math.cos(ang + .5), y2 - h * _math.sin(ang + .5))], seed + 7, 1.2)
    return _rough(pts, seed, 2.5), head

def _line_icon(name, iid, size=96):
    return f'<svg class="ico" id="{iid}" viewBox="0 0 64 64" width="{size}" height="{size}"><g {_SW}>{_LINE_ICONS.get(name, _LINE_ICONS["card"])}</g></svg>'

def _draw_on(js, P, sel, at, dur=.6):
    js.append(f'gsap.set("{sel} path, {sel} rect, {sel} circle",{{strokeDasharray:400,strokeDashoffset:400}});tl.to("{sel} path, {sel} rect, {sel} circle",{{strokeDashoffset:0,duration:{dur},ease:"power1.inOut",stagger:.04}},{P(at)});')

KIT_CSS += r'''
.ico { display: block; }
.pth { position: absolute; left: 0; top: 0; }
.pnode { position: absolute; width: 46px; height: 46px; margin: -23px 0 0 -23px; border-radius: 50%; background: #FFFFFF; border: 5px solid #CFCBC0; box-shadow: 0 6px 18px rgba(31,30,29,.12); display: flex; align-items: center; justify-content: center; font: 900 22px "Montserrat"; color: #FFFFFF; }
.pfg { position: absolute; inset: -5px; border-radius: 50%; background: linear-gradient(180deg, #EDE62A, #E8B000); display: flex; align-items: center; justify-content: center; font: 900 22px "Montserrat"; color: #1F1E1D; }
.pnode.cur { border-color: #E8B000; }
.plab { position: absolute; width: 300px; margin-left: -150px; text-align: center; font: 700 30px/1.15 "Montserrat"; color: #73726C; }
.plab b { display: block; font: 600 20px "JetBrains Mono", monospace; color: #B98500; margin-bottom: 6px; }
.plab.cur { color: #1F1E1D; font-weight: 900; }
.pcover { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; background: #F5F4EE; transform-origin: 100% 50%; }
.pthumb { position: absolute; width: 240px; height: 135px; margin-left: -120px; border: 6px solid #FFFFFF; border-radius: 10px; overflow: hidden; box-shadow: 0 14px 34px rgba(31,30,29,.2); opacity: 0; }
.pthumb img { width: 100%; height: 100%; object-fit: cover; display: block; }
.cards { position: absolute; left: 0; right: 0; display: flex; justify-content: center; align-items: flex-start; gap: 34px; }
.pc2 { position: relative; width: 300px; min-height: 330px; background: #FFFFFF; border-radius: 18px; padding: 34px 22px 26px; box-shadow: 0 22px 50px rgba(31,30,29,.14), 0 0 0 1px rgba(31,30,29,.05); display: flex; flex-direction: column; align-items: center; text-align: center; opacity: 0; }
.pc2.sm { width: 210px; min-height: 250px; padding: 26px 14px 20px; }
.pc2 .ct { font: 800 34px/1.15 "Montserrat"; color: #1F1E1D; margin-top: 22px; }
.pc2.sm .ct { font-size: 28px; margin-top: 16px; }
.pc2 .cs { font: 600 24px/1.3 "Montserrat"; color: #73726C; margin-top: 10px; }
.pc2 .cs.m { font: 600 22px "JetBrains Mono", monospace; }
.pc2 .stamp { position: absolute; left: 50%; top: 50%; width: 120px; height: 120px; margin: -60px 0 0 -60px; opacity: 0; }
.pc2 .badge { position: absolute; right: -14px; top: -14px; width: 52px; height: 52px; border-radius: 50%; background: linear-gradient(180deg, #EDE62A, #E8B000); display: flex; align-items: center; justify-content: center; font: 900 28px "Montserrat"; color: #1F1E1D; opacity: 0; box-shadow: 0 8px 20px rgba(232,176,0,.35); }
.ctitle { position: absolute; left: 0; right: 0; text-align: center; font: 900 68px "Montserrat"; text-transform: uppercase; letter-spacing: -.02em; color: #1F1E1D; opacity: 0; }
.carr { position: absolute; left: 0; top: 0; overflow: visible; }
.rcpt { position: absolute; left: 610px; top: 120px; width: 700px; background: #FFFFFF; padding: 50px 56px 60px; box-shadow: 0 30px 70px rgba(31,30,29,.18); font: 600 34px "JetBrains Mono", monospace; color: #1F1E1D; }
.rcpt::after { content: ""; position: absolute; left: 0; right: 0; bottom: -18px; height: 18px; background: radial-gradient(circle at 12px -2px, transparent 12px, #FFFFFF 13px) repeat-x; background-size: 24px 18px; }
.rcpt h4 { margin: 0 0 30px; font: 900 40px "Montserrat"; text-transform: uppercase; letter-spacing: .04em; text-align: center; }
.rl { display: flex; justify-content: space-between; padding: 14px 0; border-bottom: 2px dashed #E3DFD4; opacity: 0; }
.rl b { color: #B98500; }
.rtot { display: flex; justify-content: space-between; margin-top: 26px; font: 900 48px "Montserrat"; opacity: 0; }
.rstamp { position: absolute; right: -60px; bottom: 30px; padding: 10px 30px; border: 8px solid #E8B000; border-radius: 14px; font: 900 90px "Montserrat"; color: #E8B000; transform: rotate(-12deg); opacity: 0; background: rgba(255,255,255,.85); }
.wlogo { position: absolute; width: 240px; height: 240px; border-radius: 40px; background: #FFFFFF; box-shadow: 0 24px 60px rgba(31,30,29,.16), 0 0 0 1px rgba(31,30,29,.05); display: flex; align-items: center; justify-content: center; opacity: 0; font: 900 40px "Montserrat"; color: #1F1E1D; text-align: center; padding: 20px; }
.wlogo img { width: 140px; height: 140px; object-fit: contain; display: block; }
.lgcap { position: absolute; width: 360px; margin-left: -60px; text-align: center; font: 800 32px "Montserrat"; color: #1F1E1D; opacity: 0; }
.wbox { position: absolute; padding: 30px 46px; background: #1F1E1D; color: #F5F4EE; border-radius: 22px; font: 900 48px "Montserrat"; text-transform: uppercase; opacity: 0; box-shadow: 0 24px 60px rgba(31,30,29,.25); white-space: nowrap; }
.wmeter { position: absolute; width: 620px; opacity: 0; }
.wmeter .mt { font: 700 30px "Montserrat"; color: #73726C; margin-bottom: 14px; }
.wmeter .tr { height: 48px; border-radius: 24px; background: #E3DFD4; overflow: hidden; }
.wmeter .fl { height: 100%; width: 100%; border-radius: 24px; background: #4ADE80; transform-origin: 0 50%; transform: scaleX(0); }
.qmark { position: absolute; font: 900 160px "Montserrat"; color: #E8B000; opacity: 0; }
.wfold { position: absolute; width: 380px; padding: 24px 28px; background: #FFFFFF; border-radius: 18px; box-shadow: 0 22px 50px rgba(31,30,29,.16); display: flex; align-items: center; gap: 20px; font: 600 30px "JetBrains Mono", monospace; color: #1F1E1D; opacity: 0; }
.trk { position: absolute; left: 240px; width: 1440px; height: 96px; }
.trk .tn { position: absolute; left: 0; top: 30px; width: 220px; font: 700 30px "Montserrat"; color: #1F1E1D; }
.trk .tline { position: absolute; left: 240px; right: 0; top: 46px; height: 4px; background: #CFCBC0; border-radius: 2px; }
.kf { position: absolute; top: 30px; width: 36px; height: 36px; margin-left: -18px; transform: rotate(45deg); background: #1F1E1D; border-radius: 5px; opacity: 0; }
.kf.g { background: linear-gradient(180deg, #EDE62A, #E8B000); }
.kfl { position: absolute; top: -8px; font: 600 22px "JetBrains Mono", monospace; color: #73726C; margin-left: -40px; width: 120px; text-align: center; opacity: 0; }
.phead { position: absolute; top: 230px; width: 4px; height: 560px; background: #E5484D; border-radius: 2px; }
.fstrip { position: absolute; top: 400px; width: 220px; height: 124px; border-radius: 10px; background: #FFFFFF; border: 4px solid #1F1E1D; box-shadow: 0 14px 30px rgba(31,30,29,.14); opacity: 0; font: 600 22px "JetBrains Mono", monospace; display: flex; align-items: center; justify-content: center; color: #73726C; }
.mp4 { position: absolute; left: 1420px; top: 330px; width: 260px; height: 300px; opacity: 0; }
.cmp { position: absolute; top: 200px; width: 760px; background: #FFFFFF; border-radius: 26px; padding: 40px 50px 46px; box-shadow: 0 30px 80px rgba(31,30,29,.16); opacity: 0; }
.cmp .ch { display: flex; align-items: center; gap: 24px; font: 900 44px "Montserrat"; text-transform: uppercase; color: #1F1E1D; margin-bottom: 26px; }
.cmp .ch img { width: 70px; height: 70px; object-fit: contain; }
.cmp .cr { display: flex; align-items: center; gap: 18px; font: 700 38px "Montserrat"; color: #1F1E1D; padding: 14px 0; opacity: 0; }
.cmp .cr span { color: #E8B000; font-weight: 900; }
.ui2 { position: absolute; left: 0; right: 0; top: 430px; display: flex; justify-content: center; gap: 46px; }
.ubtn { position: relative; height: 120px; padding: 0 56px; border-radius: 60px; display: flex; align-items: center; gap: 20px; font: 900 48px "Montserrat"; background: #FFFFFF; color: #1F1E1D; box-shadow: 0 18px 40px rgba(31,30,29,.14), 0 0 0 2px #1F1E1D; opacity: 0; }
.ubtn .on { position: absolute; inset: 0; border-radius: 60px; display: flex; align-items: center; justify-content: center; gap: 20px; opacity: 0; }
.uhint { position: absolute; left: 0; right: 0; top: 340px; text-align: center; font: 700 34px "Montserrat"; color: #73726C; opacity: 0; }
.fcard { position: absolute; left: 330px; top: 170px; width: 1260px; background: #FFFFFF; border-radius: 22px; box-shadow: 0 30px 80px rgba(31,30,29,.16); overflow: hidden; opacity: 0; }
.fcard .fh { height: 70px; background: #EFECE4; display: flex; align-items: center; padding: 0 30px; gap: 16px; font: 600 28px "JetBrains Mono", monospace; color: #1F1E1D; }
.fcard .fl2 { font: 500 32px/1.5 "JetBrains Mono", monospace; color: #1F1E1D; padding: 14px 40px; opacity: 0; }
.fcard .fl2.new { background: rgba(242,194,0,.16); }
'''

def k_path(s, t, e, d, I, W, P, R, fx, t0):
    items = s.get("items") or getattr(_S, "ROAD", [])
    N = max(len(items), 2)
    xs_ = [200 + q * (1520 / (N - 1)) for q in range(N)]
    pts = [(x, 560 + 150 * _math.sin((x - 200) / (1520 / (N - 1)) * _math.pi - _math.pi / 2)) for x in range(120, 1820, 20)]
    ys_ = [560 + 150 * _math.sin(q * _math.pi - _math.pi / 2) for q in range(N)]
    h = f'<svg class="pth" width="1920" height="1080"><path d="{_rough(pts, 3, 2)}" fill="none" stroke="#CFCBC0" stroke-width="5" stroke-linecap="round" stroke-dasharray="2 18"/></svg>'
    act = s.get("act"); mode = s.get("mode", "intro" if act is None else "cb")
    blur_last = s.get("blur_last", False)
    if mode == "intro": h += f'<div class="pcover" id="{I("cv")}"></div>'
    js = []
    for q in range(N):
        done = act is not None and q < act
        cls = "pnode" + (" cur" if q == act else "")
        ly = ys_[q] + (60 if ys_[q] > 560 else -130)
        blur = ' style="filter:blur(10px)"' if blur_last and q == N - 1 and (mode == "intro" or (act is not None and act < N - 1) or mode == "recap") else ""
        h += f'<div class="{cls}" id="{I(f"n{q}")}" style="left:{xs_[q]:.0f}px;top:{ys_[q]:.0f}px"><div class="pfg" id="{I(f"g{q}")}" style="opacity:{1 if done else 0}">&#10003;</div></div>'
        h += f'<div class="plab{" cur" if q == act else ""}" id="{I(f"l{q}")}" style="left:{xs_[q]:.0f}px;top:{ly:.0f}px"{blur}><b>{q + 1:02d}</b>{H.escape(items[q])}</div>'
    if mode == "intro":
        js.append(f'tl.fromTo("#{I("cv")}",{{scaleX:1}},{{scaleX:0,duration:{max(d - .6, 1):.2f},ease:"none"}},{P(t)});')
        last = t; ats = s.get("ats", [""] * N)
        for q, wd in enumerate(ats[:N]):
            at = max(W(wd, last + .4), last + .25) if q and wd else (t + .15 + q * .45); last = at
            js.append(f'gsap.set(["#{I(f"n{q}")}","#{I(f"l{q}")}"],{{opacity:0}});tl.fromTo(["#{I(f"n{q}")}","#{I(f"l{q}")}"],{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.35,ease:"back.out(2)"}},{P(at)});'); fx(at, "pop")
        if blur_last and s.get("unblur_at"):
            ub = W(s["unblur_at"], last + .3)
            js.append(f'tl.to("#{I(f"l{N - 1}")}",{{filter:"blur(0px)",duration:.4}},{P(ub)});'); fx(ub, "ding_sparkle")
    elif mode == "cb":
        js.append(f'tl.fromTo("#{I("")} .pth, #{I("")} .pnode, #{I("")} .plab",{{opacity:0}},{{opacity:1,duration:.3}},{P(t)});')
        js.append(f'tl.fromTo("#{I(f"n{act}")}",{{scale:1}},{{scale:1.5,duration:.4,ease:"back.out(2.5)"}},{P(t + .3)});tl.fromTo("#{I(f"l{act}")}",{{scale:1}},{{scale:1.15,duration:.4,ease:"back.out(2)"}},{P(t + .3)});')
        if blur_last and act == N - 1: js.append(f'tl.to("#{I(f"l{act}")}",{{filter:"blur(0px)",duration:.4}},{P(t + .3)});'); fx(t + .3, "ding_sparkle")
        else: fx(t + .3, "whoosh")
    else:
        js.append(f'tl.fromTo("#{I("")} .pnode, #{I("")} .plab",{{opacity:0}},{{opacity:1,duration:.3}},{P(t)});')
        stills = s.get("stills", []); span = max((d - 1.0) / N, .5)
        for q in range(N):
            at = t + .4 + q * span; ty = ys_[q] + (-300 if ys_[q] < 560 else 120)
            if q < len(stills):
                h += f'<div class="pthumb" id="{I(f"p{q}")}" style="left:{xs_[q]:.0f}px;top:{ty:.0f}px"><img src="assets/{stills[q]}" alt="" /></div>'
                js.append(f'tl.fromTo("#{I(f"p{q}")}",{{opacity:0,y:20,rotation:-4}},{{opacity:1,y:0,rotation:{(-3 if q % 2 else 3)},duration:.35,ease:"back.out(1.8)"}},{P(at)});')
            js.append(f'tl.to("#{I(f"g{q}")}",{{opacity:1,duration:.15}},{P(at)});tl.fromTo("#{I(f"n{q}")}",{{scale:1.5}},{{scale:1,duration:.3}},{P(at)});')
            if blur_last and q == N - 1: js.append(f'tl.to("#{I(f"l{q}")}",{{filter:"blur(0px)",duration:.3}},{P(at)});')
            fx(at, "pop")
    return h, js

def k_cards(s, t, e, d, I, W, P, R, fx, t0):
    items = s["items"]; sm = len(items) > 4; top = s.get("top", 400 if not s.get("title") else 470)
    h = ""; js = []
    if s.get("title"):
        h += f'<div class="ctitle" id="{I("tt")}" style="top:{top - 170}px">{H.escape(s["title"])}</div>'
        js.append(f'tl.fromTo("#{I("tt")}",{{y:30,opacity:0}},{{y:0,opacity:1,duration:.4,ease:"expo.out"}},{P(t)});')
    h += f'<div class="cards" style="top:{top}px">'
    last = t; ats = []
    for q, it in enumerate(items):
        wd, ic, tt, sb, st = (list(it) + [None] * 5)[:5]
        at = (t + .15 if not s.get("title") else t + .5) if q == 0 else max(W(wd, last + .5), last + .3); last = at; ats.append(at)
        cid = I(f"c{q}"); rot = [-2, 1.5, -1, 2, -1.5, 1, -2][q % 7]
        sub = f'<div class="cs{" m" if "m" in (st or "") else ""}">{H.escape(sb)}</div>' if sb else ""
        stamp = f'<svg class="stamp" id="{cid}x" viewBox="0 0 64 64"><g fill="none" stroke="#E5484D" stroke-width="6" stroke-linecap="round">{_LINE_ICONS["x"]}</g></svg>' if st and "x" in st else ""
        badge = f'<div class="badge" id="{cid}b">&#10003;</div>' if st and "g" in st else ""
        ic_h = f'<img id="{cid}i" src="assets/{ic[4:]}" alt="" style="width:{74 if sm else 96}px;height:{74 if sm else 96}px;object-fit:contain" />' if ic.startswith("img:") else _line_icon(ic, cid + "i", 74 if sm else 96)
        h += f'<div class="pc2{" sm" if sm else ""}" id="{cid}" style="transform:rotate({rot}deg)">{ic_h}<div class="ct">{H.escape(tt)}</div>{sub}{stamp}{badge}</div>'
        js.append(f'tl.fromTo("#{cid}",{{y:40,opacity:0}},{{y:0,opacity:1,duration:.35,ease:"back.out(1.6)"}},{P(at)});')
        if not ic.startswith("img:"): _draw_on(js, P, "#" + cid + "i", at + .05, .5)
        if stamp: js.append(f'tl.fromTo("#{cid}x",{{opacity:0,scale:1.6}},{{opacity:.92,scale:1,duration:.25,ease:"back.out(2)"}},{P(at + .5)});tl.to("#{cid}",{{opacity:.55,duration:.3}},{P(at + .6)});')
        if badge: js.append(f'tl.fromTo("#{cid}b",{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:.3,ease:"back.out(2.5)"}},{P(at + .45)});')
        fx(at, "pop")
    h += "</div>"
    if s.get("arrows") and len(items) > 1:
        cw = (210 if sm else 300); gap = 34; n = len(items); x0 = 960 - (n * cw + (n - 1) * gap) / 2
        svg = '<svg class="carr" width="1920" height="1080">'
        for q in range(n - 1):
            xa = x0 + (q + 1) * cw + q * gap - 8; xb = xa + gap + 16; y = top + 130
            sh_, hd_ = _rarrow(xa, y, xb, y, seed=q + 4, bend=-14)
            svg += f'<g id="{I(f"a{q}")}"><path d="{sh_}" {_SW.replace("#1F1E1D", "#E8B000")}/><path d="{hd_}" {_SW.replace("#1F1E1D", "#E8B000")}/></g>'
        h += svg + "</svg>"
        for q in range(n - 1): _draw_on(js, P, "#" + I(f"a{q}"), ats[q + 1] - .25, .3)
    return h, js

def k_receipt(s, t, e, d, I, W, P, R, fx, t0):
    rows = "".join(f'<div class="rl" id="{I(f"r{q}")}"><span>{H.escape(nm)}</span><b>{H.escape(pr)}</b></div>' for q, (wd, nm, pr) in enumerate(s["lines"]))
    tot = s.get("total", "$0")
    h = f'<div class="rcpt" id="{I("c")}"><h4>{H.escape(s.get("head", "receipt"))}</h4>{rows}<div class="rtot" id="{I("tot")}"><span>TOTAL</span><span>{H.escape(tot)}</span></div><div class="rstamp" id="{I("st")}">{H.escape(tot)}</div></div>'
    js = [f'tl.fromTo("#{I("c")}",{{y:-500,opacity:1}},{{y:0,duration:.7,ease:"power2.out"}},{P(t)});']
    last = t + .5
    for q, (wd, nm, pr) in enumerate(s["lines"]):
        at = max(W(wd, last + .4), last + .3); last = at
        js.append(f'tl.fromTo("#{I(f"r{q}")}",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:.3}},{P(at)});'); fx(at, "typing_short" if q == 0 else "pop")
    tt_ = W(s["total_at"], last + .3) if s.get("total_at") else last + .4
    js.append(f'tl.to("#{I("tot")}",{{opacity:1,duration:.3}},{P(tt_)});tl.fromTo("#{I("st")}",{{opacity:0,scale:2.2}},{{opacity:1,scale:1,duration:.3,ease:"back.out(2)"}},{P(tt_ + .2)});'); fx(tt_ + .2, "bass_hit")
    return h, js

def _logo_inner(lg, fallback):
    return f'<img src="assets/{lg}" alt="" />' if lg else H.escape(fallback)

def k_workflow(s, t, e, d, I, W, P, R, fx, t0):
    ln, limg = s.get("left", ("Tool A", None)); rn, rimg = s.get("right", ("Tool B", None))
    res = s.get("result", "my workflow"); met = s.get("metric", "weekly limit"); clk = s.get("clock_label", "faster")
    h = (f'<div class="wlogo" id="{I("a")}" style="left:300px;top:200px">{_logo_inner(limg, ln)}</div><div class="lgcap" id="{I("ac")}" style="left:300px;top:460px">{H.escape(ln)}</div>'
         f'<div class="wlogo" id="{I("b")}" style="left:300px;top:560px">{_logo_inner(rimg, rn)}</div><div class="lgcap" id="{I("bc")}" style="left:300px;top:820px">{H.escape(rn)}</div>'
         f'<div class="wbox" id="{I("w")}" style="left:900px;top:470px">{H.escape(res)}</div>')
    a1 = _rarrow(560, 320, 890, 500, 11, 30); a2 = _rarrow(560, 680, 890, 540, 12, -30)
    h += f'<svg class="carr" width="1920" height="1080"><g id="{I("r1")}"><path d="{a1[0]}" {_SW.replace("#1F1E1D", "#E8B000")}/><path d="{a1[1]}" {_SW.replace("#1F1E1D", "#E8B000")}/></g><g id="{I("r2")}"><path d="{a2[0]}" {_SW.replace("#1F1E1D", "#E8B000")}/><path d="{a2[1]}" {_SW.replace("#1F1E1D", "#E8B000")}/></g></svg>'
    h += f'<div style="position:absolute;left:1380px;top:250px;opacity:0" id="{I("sw")}">{_line_icon("clock", I("swi"), 150)}<div style="font:800 34px Montserrat;color:#1F1E1D;text-align:center;margin-top:8px">{H.escape(clk)}</div></div>'
    h += f'<div class="wmeter" id="{I("m")}" style="left:1150px;top:740px"><div class="mt">{H.escape(met)}</div><div class="tr"><div class="fl" id="{I("mf")}"></div></div></div>'
    aw = W(s["start_at"], t + .1) if s.get("start_at") else t + .2
    ab = W(s["merge_at"], aw + .4) if s.get("merge_at") else aw + .8
    fa = W(s["fast_at"], ab + .5) if s.get("fast_at") else ab + 1.1
    la = W(s["meter_at"], fa + .4) if s.get("meter_at") else fa + .8
    js = [f'tl.fromTo(["#{I("a")}","#{I("ac")}"],{{x:-60,opacity:0}},{{x:0,opacity:1,duration:.4,ease:"expo.out"}},{P(aw)});tl.fromTo(["#{I("b")}","#{I("bc")}"],{{x:-60,opacity:0}},{{x:0,opacity:1,duration:.4,ease:"expo.out"}},{P(aw + .25)});']
    fx(aw, "pop")
    _draw_on(js, P, "#" + I("r1"), ab - .1, .4); _draw_on(js, P, "#" + I("r2"), ab + .05, .4)
    js.append(f'tl.fromTo("#{I("w")}",{{scale:.7,opacity:0}},{{scale:1,opacity:1,duration:.4,ease:"back.out(2)"}},{P(ab + .35)});'); fx(ab + .35, "pop")
    js.append(f'tl.fromTo("#{I("sw")}",{{y:30,opacity:0}},{{y:0,opacity:1,duration:.35,ease:"back.out(2)"}},{P(fa)});'); _draw_on(js, P, "#" + I("swi"), fa + .05, .5)
    js.append(f'tl.fromTo("#{I("swi")}",{{rotation:0}},{{rotation:360,duration:1.2,ease:"power2.inOut",transformOrigin:"50% 55%"}},{P(fa + .4)});'); fx(fa, "pop")
    js.append(f'tl.fromTo("#{I("m")}",{{y:30,opacity:0}},{{y:0,opacity:1,duration:.35,ease:"expo.out"}},{P(la)});tl.to("#{I("mf")}",{{scaleX:.18,duration:.8,ease:"power2.out"}},{P(la + .2)});'); fx(la, "pop")
    return h, js

def k_hfskill(s, t, e, d, I, W, P, R, fx, t0):
    an, aimg = s.get("app", ("App", None)); tn = s.get("target", "engine"); sk = s.get("skill", "skill folder")
    h = (f'<div class="wlogo" id="{I("a")}" style="left:360px;top:380px">{_logo_inner(aimg, an)}</div><div class="lgcap" id="{I("ac")}" style="left:360px;top:640px">{H.escape(an)}</div>'
         f'<div class="qmark" id="{I("q")}" style="left:860px;top:380px">?</div>'
         f'<div class="wlogo" id="{I("b")}" style="left:1280px;top:380px;flex-direction:column">&lt;/&gt;<span style="font:700 28px JetBrains Mono, monospace;margin-top:8px">{H.escape(tn)}</span></div>'
         f'<div class="wfold" id="{I("f")}" style="left:770px;top:760px">{_line_icon("folder", I("fi"), 64)}{H.escape(sk)}</div>')
    ta = W(s["target_at"], t + .4) if s.get("target_at") else t + .7
    qa = W(s["q_at"], ta + .2) if s.get("q_at") else ta + .5
    fa = W(s["skill_at"], qa + .5) if s.get("skill_at") else qa + 1.0
    js = [f'tl.fromTo(["#{I("a")}","#{I("ac")}"],{{y:40,opacity:0}},{{y:0,opacity:1,duration:.4,ease:"expo.out"}},{P(t + .1)});tl.fromTo("#{I("b")}",{{y:40,opacity:0}},{{y:0,opacity:1,duration:.4,ease:"expo.out"}},{P(ta)});',
          f'tl.fromTo("#{I("q")}",{{opacity:0,scale:.4,rotation:-20}},{{opacity:1,scale:1,rotation:0,duration:.35,ease:"back.out(2.5)"}},{P(qa)});']
    fx(qa, "pop")
    js.append(f'tl.fromTo("#{I("f")}",{{y:120,opacity:0}},{{y:0,opacity:1,duration:.45,ease:"back.out(1.6)"}},{P(fa)});tl.to("#{I("q")}",{{opacity:0,scale:.5,duration:.25}},{P(fa + .3)});')
    _draw_on(js, P, "#" + I("fi"), fa + .05, .4)
    js.append(f'tl.to("#{I("a")}",{{boxShadow:"0 0 0 8px #F2C200, 0 30px 80px rgba(242,194,0,.45)",duration:.35}},{P(fa + .5)});'); fx(fa, "whoosh"); fx(fa + .5, "ding_sparkle")
    return h, js

def k_tracks(s, t, e, d, I, W, P, R, fx, t0):
    rows = s["rows"]; h = ""; js = []
    for q, (nm, keys) in enumerate(rows):
        y = 260 + q * 130
        h += f'<div class="trk" style="top:{y}px"><div class="tn">{H.escape(nm)}</div><div class="tline"></div>'
        for r, (wd, x, lab, gold) in enumerate(keys):
            kid = I(f"k{q}_{r}")
            h += f'<div class="kf{" g" if gold else ""}" id="{kid}" style="left:{240 + x}px"></div><div class="kfl" id="{kid}l" style="left:{240 + x}px">{H.escape(lab)}</div>'
            at = W(wd, t + .2 + q * .4 + r * .2) if wd else (t + .3 + q * .4 + r * .2)
            js.append(f'tl.fromTo(["#{kid}","#{kid}l"],{{opacity:0,scale:.3}},{{opacity:1,scale:1,duration:.3,ease:"back.out(2.5)"}},{P(at)});')
            if r == 0: fx(at, "pop")
        h += "</div>"
        js.append(f'tl.fromTo("#{I("")} .trk:nth-of-type({q + 1})",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.35}},{P(t + q * .12)});')
    h += f'<div class="phead" id="{I("ph")}" style="left:480px"></div>'
    js.append(f'tl.fromTo("#{I("ph")}",{{x:0}},{{x:1180,duration:{max(d - .3, 1):.2f},ease:"none"}},{P(t + .2)});')
    return h, js

def k_filmstrip(s, t, e, d, I, W, P, R, fx, t0):
    h = ""; js = []
    for q in range(5):
        h += f'<div class="fstrip" id="{I(f"f{q}")}" style="left:{140 + q * 60}px;top:{340 + q * 18}px">frame {q + 1}</div>'
        js.append(f'tl.fromTo("#{I(f"f{q}")}",{{opacity:0,x:-80}},{{opacity:1,x:0,duration:.25,ease:"expo.out"}},{P(t + .15 + q * .25)});')
    out_lab = s.get("label", "MP4")
    h += f'<div class="mp4" id="{I("m")}">{_line_icon("play", I("mi"), 260)}<div style="font:900 56px Montserrat;color:#1F1E1D;text-align:center">{H.escape(out_lab)}</div></div>'
    a1 = _rarrow(720, 470, 1380, 470, 21, -40)
    h += f'<svg class="carr" width="1920" height="1080"><g id="{I("ar")}"><path d="{a1[0]}" {_SW.replace("#1F1E1D", "#E8B000")}/><path d="{a1[1]}" {_SW.replace("#1F1E1D", "#E8B000")}/></g></svg>'
    ma = W(s["out_at"], t + 1.0) if s.get("out_at") else t + 1.6
    _draw_on(js, P, "#" + I("ar"), ma - .4, .4)
    js.append(f'tl.fromTo("#{I("m")}",{{opacity:0,scale:.7}},{{opacity:1,scale:1,duration:.4,ease:"back.out(2)"}},{P(ma)});'); _draw_on(js, P, "#" + I("mi"), ma + .05, .5); fx(ma, "pop")
    if s.get("sub"):
        ca = W(s["sub_at"], ma + .4) if s.get("sub_at") else ma + .6
        h += f'<div class="lgcap" id="{I("pc")}" style="left:1390px;top:690px;opacity:0">{H.escape(s["sub"])}</div>'
        js.append(f'tl.to("#{I("pc")}",{{opacity:1,duration:.3}},{P(ca)});')
    return h, js

def k_webvideo(s, t, e, d, I, W, P, R, fx, t0):
    bx = _rough([(520, 260), (1400, 260), (1400, 800), (520, 800), (520, 260)], 31, 2.5)
    tb = _rough([(520, 320), (1400, 320)], 32, 1.5); pb = _rough([(600, 740), (1320, 740)], 33, 1.5)
    top_l = s.get("top", "a webpage"); bot_l = s.get("bottom", "that plays like a video")
    h = (f'<svg class="carr" width="1920" height="1080"><g id="{I("b")}"><path d="{bx}" {_SW}/><path d="{tb}" {_SW}/></g>'
         f'<g id="{I("p")}" transform="translate(895 470) scale(2.2)"><g {_SW}>{_LINE_ICONS["play"]}</g></g><path id="{I("pg")}" d="{pb}" fill="none" stroke="#E8B000" stroke-width="10" stroke-linecap="round"/></svg>'
         f'<div class="lgcap" id="{I("l1")}" style="left:720px;top:180px;width:480px;margin-left:0">{H.escape(top_l)}</div><div class="lgcap" id="{I("l2")}" style="left:720px;top:830px;width:480px;margin-left:0">{H.escape(bot_l)}</div>')
    js = []
    _draw_on(js, P, "#" + I("b"), t + .05, .6)
    js.append(f'tl.to("#{I("l1")}",{{opacity:1,duration:.3}},{P(t + .2)});')
    pa = W(s["play_at"], t + .6) if s.get("play_at") else t + 1.0
    _draw_on(js, P, "#" + I("p"), pa - .1, .4)
    js.append(f'gsap.set("#{I("pg")}",{{strokeDasharray:800,strokeDashoffset:800}});tl.to("#{I("pg")}",{{strokeDashoffset:0,duration:{max(e - pa - .2, .6):.2f},ease:"none"}},{P(pa + .2)});tl.to("#{I("l2")}",{{opacity:1,duration:.3}},{P(pa)});'); fx(pa - .1, "pop")
    return h, js

def k_compare(s, t, e, d, I, W, P, R, fx, t0):
    L = s.get("left", ("Option A", None, [])); R_ = s.get("right", ("Option B", None, []))
    if len(L) == 2: L = (L[0], None, L[1])
    if len(R_) == 2: R_ = (R_[0], None, R_[1])
    cols = [("L", 140, L[0], L[1], L[2]), ("R", 1020, R_[0], R_[1], R_[2])]
    h = ""; js = []
    for sd, x, nm, lg, rows in cols:
        hl = s.get("hl") == sd
        img_h = f'<img src="assets/{lg}" alt="" />' if lg else ""
        h += f'<div class="cmp" id="{I("c" + sd)}" style="left:{x}px{";box-shadow:0 0 0 6px #F2C200, 0 30px 80px rgba(242,194,0,.25)" if hl else ""}"><div class="ch">{img_h}{H.escape(nm)}</div>'
        for q, (wd, txt) in enumerate(rows):
            h += f'<div class="cr" id="{I(f"r{sd}{q}")}"><span>&#10003;</span>{H.escape(txt)}</div>'
        h += "</div>"
    js.append(f'tl.fromTo(["#{I("cL")}","#{I("cR")}"],{{y:40,opacity:0}},{{y:0,opacity:1,duration:.4,ease:"expo.out",stagger:.12}},{P(t)});')
    for sd, x, nm, lg, rows in cols:
        last = t + .3
        for q, (wd, txt) in enumerate(rows):
            rid = I(f"r{sd}{q}")
            if not s.get("hl") or sd == s.get("hl"):
                at = max(W(wd, last + .4), last + .25) if wd else last + .35; last = at
                js.append(f'tl.fromTo("#{rid}",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:.3}},{P(at)});'); fx(at, "pop")
            elif sd in s.get("show", []):
                js.append(f'gsap.set("#{rid}",{{opacity:1}});')
    if s.get("hl"):
        js.append(f'tl.fromTo("#{I("c" + s["hl"])}",{{scale:1}},{{scale:1.04,duration:.4,ease:"back.out(2)"}},{P(t + .1)});')
    return h, js

def k_subscribe(s, t, e, d, I, W, P, R, fx, t0):
    hint = s.get("hint", "if this is helping you...")
    h = (f'<div class="uhint" id="{I("hn")}">{H.escape(hint)}</div><div class="ui2">'
         f'<div class="ubtn" id="{I("lk")}">{_line_icon("heart", I("lki"), 60)}Like<div class="on" id="{I("lko")}" style="background:#F2C200">{_line_icon("heart", I("lkj"), 60)}Liked</div></div>'
         f'<div class="ubtn" id="{I("sb")}">Subscribe<div class="on" id="{I("sbo")}" style="background:#1F1E1D;color:#F5F4EE">Subscribed &#10003;</div></div></div>'
         f'<div class="cur" id="{I("cu")}" style="left:0;top:0;opacity:0">{_CUR}</div>')
    js = [f'tl.to("#{I("hn")}",{{opacity:1,duration:.3}},{P(t + .05)});tl.fromTo(["#{I("lk")}","#{I("sb")}"],{{y:30,opacity:0}},{{y:0,opacity:1,duration:.35,ease:"back.out(1.8)",stagger:.12}},{P(t + .2)});']
    sa = W(s["sub_at"], t + .8) if s.get("sub_at") else t + 1.5
    js.append(f'tl.fromTo("#{I("cu")}",{{opacity:0,x:1500,y:1000}},{{opacity:1,x:830,y:520,duration:.5,ease:"power2.inOut"}},{P(sa - .9)});tl.to("#{I("cu")}",{{scale:.85,duration:.08,yoyo:true,repeat:1}},{P(sa - .4)});tl.to("#{I("lko")}",{{opacity:1,duration:.15}},{P(sa - .35)});')
    js.append(f'tl.to("#{I("cu")}",{{x:1170,y:520,duration:.35,ease:"power2.inOut"}},{P(sa - .2)});tl.to("#{I("cu")}",{{scale:.85,duration:.08,yoyo:true,repeat:1}},{P(sa + .2)});tl.to("#{I("sbo")}",{{opacity:1,duration:.15}},{P(sa + .25)});')
    fx(sa - .4, "click_toggle"); fx(sa + .2, "click_toggle")
    return h, js

def k_filecard(s, t, e, d, I, W, P, R, fx, t0):
    rows = "".join(f'<div class="fl2{" new" if n_ else ""}" id="{I(f"l{q}")}">{H.escape(x)}</div>' for q, (wd, x, n_) in enumerate(s["lines"]))
    h = f'<div class="fcard" id="{I("c")}"><div class="fh">{_line_icon("file", I("fi"), 40)}{H.escape(s["title"])}</div>{rows}<div style="height:24px"></div></div>'
    js = [f'tl.fromTo("#{I("c")}",{{y:50,opacity:0}},{{y:0,opacity:1,duration:.4,ease:"expo.out"}},{P(t)});']
    last = t + .3
    for q, (wd, x, n_) in enumerate(s["lines"]):
        at = max(W(wd, last + .4), last + .3) if (n_ and wd) else (t + .3 + q * .15); last = max(last, at)
        js.append(f'tl.fromTo("#{I(f"l{q}")}",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:.3}},{P(at)});')
        if n_: fx(at, "typing_short")
    return h, js

NEW.update({
    "path": k_path, "cards": k_cards, "receipt": k_receipt, "workflow": k_workflow,
    "hfskill": k_hfskill, "skillconnect": k_hfskill, "tracks": k_tracks, "filmstrip": k_filmstrip,
    "webvideo": k_webvideo, "compare": k_compare, "subscribe": k_subscribe, "filecard": k_filecard,
})
