"""Tiny SVG helpers following STYLE_GUIDE B."""
import html
import re

FONT = 'ui-sans-serif, system-ui, -apple-system, "PingFang SC", sans-serif'
NEW = ("#E1F5EE", "#0F6E56", "#085041")
OLD = ("#FAECE7", "#993C1D", "#712B13")
OTH = ("#F1EFE8", "#5F5E5A", "#444441")
RING = "#EF9F27"
ARROW = "#D85A30"
INK = "#0B0B0B"
SUB = "#52514E"
SEP = "#B4B2A9"


def esc(s):
    return html.escape(str(s), quote=False)


def text(x, y, s, size=12, fill=SUB, weight=400, anchor="start"):
    s = re.sub(r"(?:(?<=[\s\[(·,=])|^)-(?=\d)", "−", str(s))
    return ('<text x="%s" y="%s" font-size="%d" fill="%s" font-weight="%d" '
            'text-anchor="%s" dominant-baseline="central">%s</text>'
            % (x, y, size, fill, weight, anchor, esc(s)))


def rect(x, y, w, h, role=OTH, rx=4, dash=None, sw=1):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" '
            'stroke="%s" stroke-width="%s"%s/>' % (x, y, w, h, rx, role[0], role[1], sw, d))


def ring(x, y, w, h, rx=6):
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="none" '
            'stroke="%s" stroke-width="2.5"/>' % (x - 3, y - 3, w + 6, h + 6, rx, RING))


def cell(x, y, w, h, role, main, sub=None, ringed=False, dash=None):
    out = [rect(x, y, w, h, role, dash=dash)]
    cx = x + w / 2
    if sub is None:
        out.append(text(cx, y + h / 2, main, 14, role[2], 500, "middle"))
    else:
        out.append(text(cx, y + h / 2 - 7, main, 14, role[2], 500, "middle"))
        out.append(text(cx, y + h / 2 + 9, sub, 12, role[1], 400, "middle"))
    if ringed:
        out.append(ring(x, y, w, h))
    return "".join(out)


def line(x1, y1, x2, y2, color=SEP, dash="4 4", sw=1):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s/>'
            % (x1, y1, x2, y2, color, sw, d))


def arrow(x1, y1, x2, y2, color=SUB, dash=None, sw=1.5, mid="arr"):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    m = "arrR" if color == ARROW else "arrG"
    return ('<path d="M%s %s L%s %s" fill="none" stroke="%s" stroke-width="%s"%s '
            'marker-end="url(#%s-%s)"/>' % (x1, y1, x2, y2, color, sw, d, mid, m))


def path(d, color=SUB, dash=None, sw=1.5, marker=True, mid="arr"):
    dd = ' stroke-dasharray="%s"' % dash if dash else ""
    m = "arrR" if color == ARROW else "arrG"
    mk = ' marker-end="url(#%s-%s)"' % (mid, m) if marker else ""
    return '<path d="%s" fill="none" stroke="%s" stroke-width="%s"%s%s/>' % (d, color, sw, dd, mk)


def bucket(x, top, bottom, w):
    return ('<path d="M%s %s L%s %s L%s %s L%s %s" fill="none" stroke="%s" '
            'stroke-width="1.5" stroke-linejoin="round"/>'
            % (x, top, x, bottom, x + w, bottom, x + w, top, OTH[1]))


def svg_doc(name, title, desc, H, body):
    defs = ''
    for key, col in (("arrG", SUB), ("arrR", ARROW)):
        defs += ('<marker id="%s-%s" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" '
                 'markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" '
                 'stroke="%s" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
                 '</marker>' % ("arr", key, col))
    # unique ids per file
    defs = defs.replace('id="arr-', 'id="%s-' % name).replace('url(#arr-', 'url(#%s-' % name)
    font = "ui-sans-serif, system-ui, -apple-system, 'PingFang SC', sans-serif"
    return ('<svg width="100%%" viewBox="0 0 680 %d" role="img" xmlns="http://www.w3.org/2000/svg" '
            'font-family="%s"><title>%s</title><desc>%s</desc><defs>%s</defs>\n%s\n</svg>\n'
            % (H, font, esc(title), esc(desc), defs, "\n".join(body)))


def legend(y, items):
    """items: list of (kind, label). kind in new/old/oth/ring."""
    out = []
    x = 40
    for kind, label in items:
        if kind == "ring":
            out.append(rect(x, y - 8, 22, 16, OTH))
            out.append(ring(x, y - 8, 22, 16, 4))
            x += 30
        else:
            role = {"new": NEW, "old": OLD, "oth": OTH}[kind]
            out.append(rect(x, y - 8, 22, 16, role))
            x += 30
        out.append(text(x, y, label, 12, SUB))
        x += sum(12 if ord(c) > 255 else 6.4 for c in label) + 30
    return "".join(out)


# ---------------------------------------------------------------- trace
SLOT = 28
CW = 56   # cell width


def trace_svg(name, title, desc, hdr, colheads, rows, footer, leg, inp_w=64, ring_head=False, slot=None):
    SLOT = slot or 28
    """rows: dict(inp=[l1,l2], pre=[labels], pops=[(slot,label,reason,[calc lines])],
    keep=[(slot,label)], push=label|None, post=[labels], nopop=str|None, calc=[lines])"""
    n_slots = max(max(len(r["pre"]), len(r["post"])) for r in rows)
    wait_h = 30 if any(r.get("wait") is not None for r in rows) else 0
    rh = n_slots * SLOT + 26 + wait_h
    XA, XB, XC = 350, 432, 514
    body = []
    for i, h in enumerate(hdr):
        body.append(text(40, 18 + 20 * i, h, 12, SUB))
    hy = 18 + 20 * len(hdr) + 14
    xs = [40, 118, XA, XB, XC]
    for x, c in zip(xs, colheads):
        body.append(text(x, hy, c, 12, SUB))
    y = hy + 12
    body.append(line(40, y, 640, y))
    y += 6
    for r in rows:
        top = y
        bottom = top + rh - 10
        mid = (top + bottom) / 2
        # input box
        ih = 50
        body.append(rect(40, mid - ih / 2, inp_w, ih, NEW))
        l1, l2 = r["inp"]
        body.append(text(40 + inp_w / 2, mid - 9, l1, 14, NEW[2], 500, "middle"))
        body.append(text(40 + inp_w / 2, mid + 9, l2, 12, NEW[1], 400, "middle"))
        # bucket A / B
        btop = bottom - n_slots * SLOT - 4

        def sy(s):
            return bottom - SLOT * s - SLOT / 2 - 2
        for bx in (XA, XB):
            body.append(bucket(bx, btop, bottom, CW + 12))
        if r.get("wait") is not None:   # incoming element hovering above the stack, waiting to be pushed
            body.append(cell(XA + 6, btop - 28, CW, 24, NEW, r["wait"]))
        # A: remaining at original slots
        for k, (s, lab) in enumerate(r["keep"]):
            istop = (k == 0) if ring_head else (k == len(r["keep"]) - 1)
            body.append(cell(XA + 6, sy(s) - 12, CW, 24, OTH, lab, ringed=istop))
        # B: repacked
        for s, lab in enumerate(r["post"]):
            istop = (s == 0) if ring_head else (s == len(r["post"]) - 1)
            role = NEW if (r["push"] is not None and s == len(r["post"]) - 1) else OTH
            body.append(cell(XB + 6, sy(s) - 12, CW, 24, role, lab, ringed=istop))
        # pops thrown to the left
        for s, lab, reason, calc in r["pops"]:
            yy = sy(s)
            body.append(cell(118, yy - 12, 58, 24, OLD, lab))
            body.append(arrow(XA + 2, yy, 180, yy, ARROW, "5 3", 1.5, name))
            body.append(text(186, yy - 15, reason, 12, OLD[2]))
            if len(calc) == 1:
                body.append(text(XC, yy, calc[0], 12, INK, 500))
            elif calc:
                body.append(text(XC, yy - 7, calc[0], 12, SUB))
                body.append(text(XC, yy + 7, calc[1], 12, INK, 500))
        if r.get("nopop"):
            body.append(text(122, mid, r["nopop"], 12, SUB))
        for j, c in enumerate(r.get("calc", [])):
            n = len(r["calc"])
            cy = mid + (j - (n - 1) / 2) * 17
            body.append(text(XC, cy, c[0], 12, INK if c[1] else SUB, 500 if c[1] else 400))
        y = top + rh
        body.append(line(40, y, 640, y))
        y += 6
    y += 8
    for f in footer:
        body.append(text(40, y + 8, f[0], 14 if f[1] else 12, INK if f[1] else SUB, 500 if f[1] else 400))
        y += 24
    y += 6
    body.append(legend(y + 6, leg))
    H = y + 28
    return svg_doc(name, title, desc, H, body)
