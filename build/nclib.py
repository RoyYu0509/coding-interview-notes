"""NeetCode 式讲法的共用工具: 例子图 (examples_svg) 和 HTML 小工具。

每道题的顺序: 题目在问什么 → 看例子 → brute force → intuition → 算法 (文字步骤)
→ 手动走一遍 (trace 图) → 复杂度 → 参考代码 (折叠)。
"""
import html
import os

FONT = 'ui-sans-serif, system-ui, -apple-system, PingFang SC, sans-serif'
NEW = ("#E1F5EE", "#0F6E56", "#085041")
REM = ("#FAECE7", "#993C1D", "#712B13")
KEEP = ("#F1EFE8", "#5F5E5A", "#444441")
INK, SUB, LINE, RING, ARR = "#0B0B0B", "#52514E", "#B4B2A9", "#EF9F27", "#D85A30"


def _w(s, size):
    return sum(size if ord(c) > 255 else size * 0.55 for c in str(s))


class _S:
    def __init__(self):
        self.p = []

    def t(self, x, y, s, size=12, fill=SUB, anchor="start", weight=400):
        self.p.append('<text x="%s" y="%s" font-size="%d" fill="%s" text-anchor="%s" font-weight="%d" '
                      'dominant-baseline="central" style="white-space:pre">%s</text>' % (x, y, size, fill, anchor, weight, html.escape(str(s))))

    def line(self, x1, y1, x2, y2):
        self.p.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-dasharray="4 4"/>'
                      % (x1, y1, x2, y2, LINE))

    def cell(self, x, y, w, h, label, role, size=15):
        f, s, c = {"new": NEW, "rem": REM, "keep": KEEP}[role]
        self.p.append('<rect x="%s" y="%s" width="%s" height="%s" rx="3" fill="%s" stroke="%s" stroke-width="0.8"/>'
                      % (x, y, w, h, f, s))
        self.t(x + w / 2, y + h / 2 + 1, label, size, c, "middle", 500)

    def ring(self, x, y, w, h):
        self.p.append('<rect x="%s" y="%s" width="%s" height="%s" rx="6" fill="none" stroke="%s" stroke-width="2.5"/>'
                      % (x - 3, y - 3, w + 6, h + 6, RING))


def examples_svg(path, title, head, blocks, legend=None):
    """画 "看例子" 图。每个 block 是一个 example:
      title    第一行, 例: 'Example 1:  nums = [2,7,11,15], target = 9  →  [0,1]'
      items    一行格子 (数组 / 字符串); 可省略 (纯文字例子)
      cw       格子宽 (默认 34)
      ans      [(l, r)] 答案区间 → 绿色格子 + 橙色 ring
      hl       [i] 额外标成绿色的单个格子 (不加 ring)
      ans_text 格子右边的绿色说明
      bad      [(l, r, text)] 看起来像但不对 → 上方红色虚线括号 + 右侧原因
      extra    下面的说明行 (灰色)
      rows     额外的格子行: [(label, items, roles)] 用于画两个数组 / 多行
    """
    S = _S()
    y = 18
    for h in head:
        S.t(40, y, h, 12, SUB)
        y += 20
    y += 4
    for b in blocks:
        S.line(40, y, 640, y)
        S.t(40, y + 20, b["title"], 14, INK, "start", 500)
        yy = y + 40
        rows = []
        if "items" in b:
            rows.append((None, b["items"], None))
        rows += b.get("rows", [])
        first = True
        for (label, items, roles) in rows:
            n = len(items)
            cw = b.get("cw", 34)
            x0 = 40 + (64 if label else 0)
            if label:
                pass
            top = yy
            cy = top + (22 if (first and b.get("bad")) else 6)
            if label:
                S.t(40, cy + 15, label, 12, SUB)
            if roles is None:
                roles = ["keep"] * n
                if first:
                    for (l, r) in b.get("ans", []):
                        for k in range(l, r + 1):
                            roles[k] = "new"
                    for k in b.get("hl", []):
                        roles[k] = "new"
            for k in range(n):
                S.cell(x0 + k * cw, cy, cw, 30, items[k], roles[k])
                if b.get("index", True):
                    S.t(x0 + k * cw + cw / 2, cy + 42, str(k), 11, SUB, "middle")
            tx = x0 + n * cw + 24
            if first:
                for (l, r, text) in b.get("bad", []):
                    x1, x2 = x0 + l * cw + 3, x0 + (r + 1) * cw - 3
                    S.p.append('<path d="M%s %s L%s %s L%s %s L%s %s" fill="none" stroke="%s" stroke-width="1.5" '
                               'stroke-dasharray="4 3"/>' % (x1, top + 14, x1, top + 6, x2, top + 6, x2, top + 14, ARR))
                    S.t(tx, top + 8, text, 12, REM[2])
                for (l, r) in b.get("ans", []):
                    S.ring(x0 + l * cw, cy, (r - l + 1) * cw, 30)
                if b.get("ans_text"):
                    S.t(tx, cy + 15, b["ans_text"], 14, NEW[2], "start", 500)
            yy = cy + (56 if b.get("index", True) else 40)
            first = False
        if b.get("extra") and rows:
            yy += 6
        for line in b.get("extra", []):
            S.t(40, yy, line, 12, SUB)
            yy += 18
        y = yy + 6
    S.line(40, y, 640, y)
    leg = legend or [("new", "答案"), ("ring", "答案的范围"), ("rem", "看起来像, 但不对")]
    x = 40
    for role, text in leg:
        if role == "ring":
            S.p.append('<rect x="%s" y="%s" width="14" height="14" rx="3" fill="none" stroke="%s" stroke-width="2.5"/>'
                       % (x - 7, y + 15, RING))
        else:
            f, s, _ = {"new": NEW, "rem": REM, "keep": KEEP}[role]
            S.p.append('<rect x="%s" y="%s" width="14" height="14" rx="3" fill="%s" stroke="%s"%s/>'
                       % (x - 7, y + 15, f, s, ' stroke-dasharray="3 2"' if role == "rem" else ""))
        S.t(x + 14, y + 22, text, 12, SUB)
        x += 14 + _w(text, 12) + 26
    h = y + 44
    svg = ('<svg width="100%%" viewBox="0 0 680 %d" xmlns="http://www.w3.org/2000/svg" role="img" '
           'font-family="%s"><title>%s</title>%s</svg>\n' % (h, FONT, html.escape(title), "\n".join(S.p)))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)


def steps(doc, *lines):
    doc.raw("<ol>%s</ol>" % "".join("<li>%s</li>" % x for x in lines))


def bullets(doc, *lines):
    doc.raw("<ul>%s</ul>" % "".join("<li>%s</li>" % x for x in lines))


def solution(doc, *codes, summary="参考代码 (先自己按上面的算法步骤写, 写不出来再展开)"):
    doc.raw('<details><summary>%s</summary>' % summary)
    for c in codes:
        doc.code(c)
    doc.raw('</details>')


def table(doc, header, rows):
    h = "".join("<th>%s</th>" % x for x in header)
    r = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in row) for row in rows)
    doc.raw("<table><tr>%s</tr>%s</table>" % (h, r))
