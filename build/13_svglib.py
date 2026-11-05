"""13 · Backtracking 专用的 SVG 小工具 (只被 13_backtracking.py 使用)。
配色/字号/版式按 STYLE_GUIDE B。"""
from xml.sax.saxutils import escape

FONT = 'ui-sans-serif, system-ui, -apple-system, "PingFang SC", sans-serif'
# (fill, stroke, text)
NEW = ("#E1F5EE", "#0F6E56", "#085041")
REM = ("#FAECE7", "#993C1D", "#712B13")
OTH = ("#F1EFE8", "#5F5E5A", "#444441")
RING = "#EF9F27"
INK = "#0B0B0B"
SUB = "#52514E"
SEP = "#B4B2A9"
ARROW_RED = "#D85A30"

WARN = []


def tw(s, size=12, bold=False):
    """粗略估计文字宽度。"""
    w = 0.0
    for ch in s:
        if ord(ch) > 0x2E80:
            w += size
        elif ch in "il.,:;'| ()[]{}!":
            w += size * 0.36
        elif ch in "mwMW":
            w += size * 0.85
        else:
            w += size * (0.62 if bold else 0.58)
    return w


class Svg:
    def __init__(self, name, height, title, desc):
        self.name = name
        self.h = height
        self.title = title
        self.desc = desc
        self.o = []

    def t(self, x, y, s, size=12, fill=SUB, anchor="start", weight=400,
          maxw=None):
        w = tw(s, size, weight >= 500)
        if maxw is not None and w > maxw:
            WARN.append("%s: text too wide (%.0f>%.0f): %s" % (self.name, w, maxw, s))
        if anchor == "start":
            lo, hi = x, x + w
        elif anchor == "middle":
            lo, hi = x - w / 2, x + w / 2
        else:
            lo, hi = x - w, x
        if lo < 2 or hi > 678:
            WARN.append("%s: text out of 680 (%.0f..%.0f): %s" % (self.name, lo, hi, s))
        self.o.append(
            '<text x="%g" y="%g" font-size="%d" fill="%s" font-weight="%d" '
            'text-anchor="%s" dominant-baseline="central">%s</text>'
            % (x, y, size, fill, weight, anchor, escape(s)))

    def rect(self, x, y, w, h, role=OTH, dash=False, sw=1, rx=4, fill=None,
             stroke=None):
        f = fill or role[0]
        s = stroke or role[1]
        self.o.append(
            '<rect x="%g" y="%g" width="%g" height="%g" rx="%d" fill="%s" '
            'stroke="%s" stroke-width="%g"%s/>'
            % (x, y, w, h, rx, f, s, sw,
               ' stroke-dasharray="5 3"' if dash else ""))

    def circ(self, cx, cy, r, role=OTH, dash=False, sw=1):
        self.o.append(
            '<circle cx="%g" cy="%g" r="%g" fill="%s" stroke="%s" '
            'stroke-width="%g"%s/>'
            % (cx, cy, r, role[0], role[1], sw,
               ' stroke-dasharray="5 3"' if dash else ""))

    def ring(self, x, y, w, h, rx=6):
        self.o.append(
            '<rect x="%g" y="%g" width="%g" height="%g" rx="%d" fill="none" '
            'stroke="%s" stroke-width="2.5"/>' % (x - 3, y - 3, w + 6, h + 6, rx, RING))

    def line(self, x1, y1, x2, y2, stroke=SEP, dash=None, sw=1, marker=None):
        self.o.append(
            '<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="%g"%s%s/>'
            % (x1, y1, x2, y2, stroke, sw,
               (' stroke-dasharray="%s"' % dash) if dash else "",
               (' marker-end="url(#%s)"' % marker) if marker else ""))

    def path(self, d, stroke=SUB, dash=None, sw=1.5, marker=None):
        self.o.append(
            '<path d="%s" fill="none" stroke="%s" stroke-width="%g"%s%s/>'
            % (d, stroke, sw, (' stroke-dasharray="%s"' % dash) if dash else "",
               (' marker-end="url(#%s)"' % marker) if marker else ""))

    def sep(self, y, x1=40, x2=640):
        self.line(x1, y, x2, y, SEP, "4 4", 1)

    def cell(self, x, y, w, h, label, role=OTH, dash=False, size=14):
        self.rect(x, y, w, h, role, dash)
        self.t(x + w / 2, y + h / 2, label, size, role[2], "middle", 500)

    def node(self, cx, cy, w, h, label, role=OTH, dash=False, size=13):
        self.rect(cx - w / 2, cy - h / 2, w, h, role, dash, rx=6)
        self.t(cx, cy, label, size, role[2], "middle", 500)

    def legend(self, y, items):
        """items: [(role, dash, text)]"""
        x = 40
        for role, dash, text in items:
            self.rect(x, y - 7, 18, 14, role, dash)
            self.t(x + 24, y, text, 12, SUB)
            x += 24 + tw(text, 12) + 22

    def out(self):
        defs = (
            '<defs>'
            '<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" '
            'markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" '
            'stroke="#52514E" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>'
            '<marker id="arrowG" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" '
            'markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" '
            'stroke="#0F6E56" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>'
            '<marker id="arrowR" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" '
            'markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" '
            'stroke="#D85A30" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>'
            '</defs>')
        return ('<svg width="100%%" viewBox="0 0 680 %d" role="img" '
                'xmlns="http://www.w3.org/2000/svg" font-family=\'%s\'>'
                '<title>%s</title><desc>%s</desc>%s\n%s\n</svg>\n'
                % (self.h, FONT.replace("'", ""), escape(self.title),
                   escape(self.desc), defs, "\n".join(self.o)))


# ------------------------------------------------------------------ 记录器
class Rec:
    """记录 DFS 过程: 事件序列 (给 trace 图) + decision tree (给 core 图)。"""

    def __init__(self, root_label):
        self.ev = []
        self.root = dict(label=root_label, kind="n", reason="", kids=[])
        self.stack = [self.root]
        self.nres = 0
        self.npush = 0
        self.nprune = 0

    def _node(self, label, kind, reason=""):
        n = dict(label=label, kind=kind, reason=reason, kids=[])
        self.stack[-1]["kids"].append(n)
        return n

    def push(self, val, path, label, extra=None, why=""):
        n = self._node(label, "n")
        self.stack.append(n)
        self.npush += 1
        self.ev.append(dict(kind="push", val=val, path=list(path), why=why,
                            nres=self.nres, extra=extra or {}))

    def pop(self, val, path, why, extra=None):
        self.stack.pop()
        self.ev.append(dict(kind="pop", val=val, path=list(path), why=why,
                            nres=self.nres, extra=extra or {}))

    def record(self, path, label, why="", extra=None):
        self.stack[-1]["kind"] = "ans"
        self.nres += 1
        self.ev.append(dict(kind="record", val=label, path=list(path), why=why,
                            nres=self.nres, extra=extra or {}))

    def prune(self, val, path, label, short, why, extra=None):
        self._node(label, "prune", short)
        self.nprune += 1
        self.ev.append(dict(kind="prune", val=val, path=list(path), why=why,
                            nres=self.nres, extra=extra or {}))


def count_nodes(n):
    return 1 + sum(count_nodes(k) for k in n["kids"])


# ------------------------------------------------------------------ decision tree 图
def draw_tree(s, root, y0, x_lo=40, x_hi=640, level_h=66, node_h=26,
              label_size=13):
    leaves = []

    def collect(n):
        if not n["kids"]:
            leaves.append(n)
        for k in n["kids"]:
            collect(k)
    collect(root)
    pitch = (x_hi - x_lo) / len(leaves)
    state = {"i": 0, "maxd": 0}

    def place(n, d):
        n["d"] = d
        state["maxd"] = max(state["maxd"], d)
        if not n["kids"]:
            n["x"] = x_lo + pitch * (state["i"] + 0.5)
            state["i"] += 1
        else:
            for k in n["kids"]:
                place(k, d + 1)
            n["x"] = (n["kids"][0]["x"] + n["kids"][-1]["x"]) / 2
        n["w"] = max(30, tw(n["label"], label_size, True) + 14)
        if n["w"] > pitch - 4 and not n["kids"]:
            WARN.append("%s: node too wide for pitch: %s (%.0f>%.0f)"
                        % (s.name, n["label"], n["w"], pitch))
    place(root, 0)

    def edges(n):
        for k in n["kids"]:
            x1, y1 = n["x"], y0 + n["d"] * level_h + node_h / 2
            x2, y2 = k["x"], y0 + k["d"] * level_h - node_h / 2
            if k["kind"] == "prune":
                s.line(x1, y1, x2, y2, ARROW_RED, "4 3", 1.2)
            else:
                s.line(x1, y1, x2, y2, "#8A8984", None, 1.2)
            edges(k)
    edges(root)

    def nodes(n):
        cy = y0 + n["d"] * level_h
        role = {"n": OTH, "ans": NEW, "prune": REM}[n["kind"]]
        s.node(n["x"], cy, n["w"], node_h, n["label"], role,
               n["kind"] == "prune", label_size)
        if n["kind"] == "prune":
            for j, ln in enumerate(n["reason"].split("\n")):
                s.t(n["x"], cy + node_h / 2 + 11 + j * 14, ln, 12, REM[2],
                    "middle", 400, maxw=pitch + 14)
        for k in n["kids"]:
            nodes(k)
    nodes(root)
    bottom = y0 + state["maxd"] * level_h + node_h / 2 + 34
    return bottom


# ------------------------------------------------------------------ 事件 trace 图
def cells_w(n, cw):
    return n * (cw + 2)


def trace_svg(name, title, desc, lines, ev, nshow, col4_title, extra_fn,
              final, legend_extra=None, row_h=48, cw=34, path_title="path"):
    shown = ev[:nshow]
    omitted = len(ev) - len(shown)
    H = 92 + row_h * len(shown) + (26 if omitted > 0 else 0) + 80 + 20 * len(final)
    s = Svg(name, H, title, desc)
    for i, ln in enumerate(lines):
        s.t(40, 18 + i * 20, ln, 12, SUB)
    ytop = 18 + 20 * len(lines) + 12
    s.t(40, ytop, "动作 / 原因", 12, SUB)
    s.t(206, ytop, "被撤销", 12, SUB)
    s.t(262, ytop, path_title, 12, SUB)
    s.t(468, ytop, col4_title, 12, SUB)
    s.sep(ytop + 10)
    y = ytop + 18
    PX = 262
    for idx, e in enumerate(shown):
        top = y
        cy = top + (row_h - 28) / 2 + 2
        s.t(40, cy + 14, str(idx + 1), 12, SUB)
        k = e["kind"]
        label = {"push": "push", "pop": "pop", "record": "收集", "prune": "剪枝"}[k]
        if k in ("push", "pop", "prune"):
            act = "%s %s" % (label, e["val"])
        else:
            act = "收集 %s" % e["val"]
        col = {"push": NEW[2], "pop": REM[2], "record": NEW[2], "prune": REM[2]}[k]
        s.t(62, top + row_h / 2 - 8, act, 14, col, "start", 500, maxw=140)
        if e["why"]:
            s.t(62, top + row_h / 2 + 10, e["why"], 12, SUB, "start", 400, maxw=146)
        path = e["path"]
        # path 数组
        for j, v in enumerate(path):
            is_new = (k == "push" and j == len(path) - 1)
            s.cell(PX + j * (cw + 2), cy, cw, 28, str(v),
                   NEW if is_new else OTH)
        if path:
            lx = PX + (len(path) - 1) * (cw + 2)
            s.ring(lx, cy, cw, 28)
        else:
            s.t(PX, cy + 14, "[ ] 空", 12, SUB)
        slot_x = PX + len(path) * (cw + 2)
        if k == "pop":
            # 被撤销的元素: 虚线红框, 扔到左边
            s.cell(206, cy, cw, 28, str(e["val"]), REM, True)
            s.rect(slot_x, cy, cw, 28, REM, True, 0.8, fill="none")
            s.path("M%g %g L%g %g L%g %g L%g %g" %
                   (slot_x + cw / 2, cy, slot_x + cw / 2, top + 5, 206 + cw / 2,
                    top + 5, 206 + cw / 2, cy - 1),
                   ARROW_RED, "4 3", 1.5, "arrowR")
        elif k == "prune":
            s.cell(slot_x, cy, cw, 28, str(e["val"]), REM, True)
        extra_fn(s, 468, top, row_h, e)
        s.sep(top + row_h)
        y += row_h
    if omitted > 0:
        s.t(40, y + 12, "... 省略后面 %d 步 (规律完全相同), 直接看最终结果" % omitted,
            12, SUB)
        y += 26
    y += 10
    for i, ln in enumerate(final):
        s.t(40, y + 10 + i * 20, ln, 14 if i == 0 else 12, INK if i == 0 else SUB,
            "start", 500 if i == 0 else 400)
    y += 20 * len(final) + 12
    items = [(NEW, False, "push / 收集答案"), (REM, True, "pop 撤销 / 剪枝")]
    if legend_extra:
        items += legend_extra
    s.legend(y + 6, items)
    s.rect(560, y - 1, 16, 14, OTH, fill="none", stroke=RING, sw=2.5)
    s.t(582, y + 6, "path 栈顶", 12, SUB)
    return s
