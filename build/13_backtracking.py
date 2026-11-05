"""13 · Backtracking: 生成 docs/13-backtracking.html 和 docs/svg/13-backtracking/*.svg
运行: cd build && python3 -I 13_backtracking.py
所有展示的代码都在本文件里被 exec 并对照暴力解测试; trace 图的数字来自带记录的同逻辑版本。
"""
import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT_DIR = os.path.dirname(HERE)
import doclib as d

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

# ===================================================================== 被讲解的代码 (单一来源: 展示 = 测试)
SRC = {}

SRC["template"] = '''
def backtrack(path, choices):
    if is_done(path):                 # 1. 结束条件: path 已经是一个完整答案
        res.append(path[:])           #    必须 copy: path 还会继续被改
        return
    for c in choices:                 # 2. choices: 此刻还能选什么
        if not valid(path, c):        #    约束剪枝: 这个选择一定走不通, 不进去
            continue
        path.append(c)                # 3. 做选择
        backtrack(path, next_choices(path, c))   # 4. 递归: 树往下一层
        path.pop()                    # 5. 撤销选择: path 回到 "做选择之前"
'''

SRC["subsets"] = '''
def subsets(nums):
    res, path = [], []
    def dfs(start):
        res.append(path[:])                  # 每个节点都是答案; 要 copy, path 之后还会变
        for i in range(start, len(nums)):    # 只选 start 之后的: 有 [1,2], 没有 [2,1]
            path.append(nums[i])             # 做选择
            dfs(i + 1)                       # 递归: 下一层只能选 i 之后的
            path.pop()                       # 撤销: 兄弟分支要看到干净的 path
    dfs(0)
    return res
'''

SRC["subsets2"] = '''
def subsets(nums):                   # 另一种写法: 每个元素 "选 / 不选" (二叉树)
    res, path = [], []
    def dfs(i):
        if i == len(nums):           # 每个元素都决定完了, 才是叶子
            res.append(path[:])
            return
        dfs(i + 1)                   # 不选 nums[i]: path 不变
        path.append(nums[i])         # 选 nums[i]
        dfs(i + 1)
        path.pop()                   # 撤销
    dfs(0)
    return res
'''

SRC["permute"] = '''
def permute(nums):
    res, path = [], []
    used = [False] * len(nums)               # used[i]: nums[i] 已在 path 里, O(1) 判断
    def dfs():
        if len(path) == len(nums):           # 每个位置都填好了
            res.append(path[:])
            return
        for i in range(len(nums)):           # 每一层都从头看: 排列允许先选后面的元素
            if used[i]:                      # 剪枝: 已经用过的不能再用
                continue
            used[i] = True                   # 做选择: 两个状态一起改 (path 和 used)
            path.append(nums[i])
            dfs()
            path.pop()                       # 撤销: 两个状态一起还原
            used[i] = False
    dfs()
    return res
'''

SRC["comb"] = '''
def combination_sum(candidates, target):
    candidates.sort()                        # 排序: 一旦 c > remain, 后面更大的也不行, 可以 break
    res, path = [], []
    def dfs(start, remain):                  # remain = target - sum(path), 不用每次重算 sum
        if remain == 0:                      # 结束条件: 刚好凑够
            res.append(path[:])
            return
        for i in range(start, len(candidates)):
            c = candidates[i]
            if c > remain:                   # 剪枝: 超了; 排过序, 后面的更大, 直接 break
                break
            path.append(c)
            dfs(i, remain - c)               # 关键: 传 i (不是 i+1) => 同一个数可以重复选
            path.pop()
    dfs(0, target)
    return res
'''

SRC["comb2"] = '''
def combination_sum2(candidates, target):
    candidates.sort()                        # 排序: 相同的数挨在一起, 才能 "和前一个比" 去重
    res, path = [], []
    def dfs(start, remain):
        if remain == 0:
            res.append(path[:])
            return
        for i in range(start, len(candidates)):
            if i > start and candidates[i] == candidates[i - 1]:
                continue                     # 同一层已试过这个值, 子树一样
            c = candidates[i]
            if c > remain:
                break
            path.append(c)
            dfs(i + 1, remain - c)           # 每个数只能用一次 => 传 i + 1
            path.pop()
    dfs(0, target)
    return res
'''

SRC["parens"] = '''
def generate_parenthesis(n):
    res, path = [], []
    def dfs(open_, close):                   # open_ / close: path 里已有的 ( 和 ) 的个数
        if len(path) == 2 * n:
            res.append("".join(path))
            return
        if open_ < n:                        # 剪枝 1: ( 最多 n 个
            path.append("(")
            dfs(open_ + 1, close)
            path.pop()
        if close < open_:                    # 剪枝 2: ) 不能比 ( 多, 否则前缀已经不合法
            path.append(")")
            dfs(open_, close + 1)
            path.pop()
    dfs(0, 0)
    return res
'''

SRC["letters"] = '''
def letter_combinations(digits):
    if not digits:
        return []
    PHONE = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
             "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
    res, path = [], []
    def dfs(idx):                            # idx: 正在决定第几位数字
        if idx == len(digits):
            res.append("".join(path))
            return
        for ch in PHONE[digits[idx]]:        # choices 由层数 idx 决定, 不用 start
            path.append(ch)
            dfs(idx + 1)
            path.pop()
    dfs(0)
    return res
'''

SRC["wsearch"] = '''
def exist(board, word):
    R, C = len(board), len(board[0])
    def dfs(r, c, k):                        # k: 已经匹配了 word[:k]; 现在要让 (r, c) 匹配 word[k]
        if k == len(word):                   # 结束条件: word 全部匹配
            return True
        if not (0 <= r < R and 0 <= c < C) or board[r][c] != word[k]:
            return False                     # 剪枝: 越界 / 字母不对 / 已经被标记成 "#"
        board[r][c] = "#"                    # 做选择: 原地标记, 当作 used[] (字母里不会有 "#")
        found = (dfs(r + 1, c, k + 1) or dfs(r - 1, c, k + 1) or
                 dfs(r, c + 1, k + 1) or dfs(r, c - 1, k + 1))
        board[r][c] = word[k]                # 撤销: 恢复原字母; 找到了也要恢复, 不能留着改过的 board
        return found
    return any(dfs(r, c, 0) for r in range(R) for c in range(C))
'''

SRC["nqueens"] = '''
def solve_n_queens(n):
    res, path = [], []                       # path[r] = 第 r 行皇后所在的列
    # 三个 set: 已占用的 列 / r - c (\\ 对角线) / r + c (/ 对角线)
    cols, diag, anti = set(), set(), set()
    def dfs(r):
        if r == n:                           # n 行都放好了
            res.append(["." * c + "Q" + "." * (n - c - 1) for c in path])
            return
        for c in range(n):
            if c in cols or (r - c) in diag or (r + c) in anti:
                continue                     # 剪枝: 同列或同一条对角线
            # 做选择: 三个 set 各 add 一个值, path 也要 append
            cols.add(c); diag.add(r - c); anti.add(r + c)
            path.append(c)
            dfs(r + 1)
            # 撤销: 三个 set 和 path 全部还原
            path.pop()
            cols.remove(c); diag.remove(r - c); anti.remove(r + c)
    dfs(0)
    return res
'''

import re as _re


def _tidy(code):
    """把每行的注释对齐到该代码块里最长的代码行之后 (缩短横向宽度)。"""
    lines = code.strip("\n").split("\n")
    parts = []
    for l in lines:
        m = _re.search(r"\s{2,}# ", l)
        if m:
            parts.append((l[:m.start()].rstrip(), l[m.start():].strip()))
        else:
            parts.append((l, None))
    width = max(len(c) for c, cm in parts if cm) + 2
    out = []
    for c, cm in parts:
        out.append(c.ljust(width) + cm if cm else c)
    return "\n" + "\n".join(out) + "\n"


for _k in list(SRC):
    if _k != "template":
        SRC[_k] = _tidy(SRC[_k])

NS = {}
for _k, _v in SRC.items():
    if _k == "template":
        continue
    exec(_v, NS)
    if _k == "subsets2":
        NS["subsets_bin"] = NS["subsets"]
    if _k == "subsets":
        NS["subsets_start"] = NS["subsets"]
# subsets2 覆盖了 subsets: 分别取回
exec(SRC["subsets"], NS)
NS["subsets_start"] = NS["subsets"]
exec(SRC["subsets2"], NS)
NS["subsets_bin"] = NS["subsets"]

# ===================================================================== 正确性测试 (对照 itertools / 暴力)
import itertools


def _test():
    for nums in ([], [1], [1, 2, 3], [4, 5, 6, 7]):
        want = sorted(sorted(c) for r in range(len(nums) + 1)
                      for c in itertools.combinations(nums, r))
        assert sorted(sorted(x) for x in NS["subsets_start"](nums)) == want
        assert sorted(sorted(x) for x in NS["subsets_bin"](nums)) == want
        assert len(NS["subsets_start"](nums)) == 2 ** len(nums)
    for nums in ([1], [1, 2], [1, 2, 3], [1, 2, 3, 4]):
        got = NS["permute"](nums)
        assert sorted(got) == sorted(list(p) for p in itertools.permutations(nums))
    def brute_cs(c, t):
        out = set()
        for counts in itertools.product(*[range(t // x + 1) for x in c]):
            if sum(a * b for a, b in zip(counts, c)) == t:
                out.add(tuple(sorted(x for x, k in zip(c, counts) for _ in range(k))))
        return out
    for c, t in (([2, 3, 5], 8), ([2, 3, 6, 7], 7), ([2], 1), ([3, 5, 8], 11)):
        got = NS["combination_sum"](list(c), t)
        assert {tuple(x) for x in got} == brute_cs(c, t) and len(got) == len({tuple(x) for x in got})
    def brute_cs2(c, t):
        out = set()
        for r in range(len(c) + 1):
            for comb in itertools.combinations(c, r):
                if sum(comb) == t:
                    out.add(tuple(sorted(comb)))
        return out
    for c, t in (([10, 1, 2, 7, 6, 1, 5], 8), ([2, 5, 2, 1, 2], 5), ([1, 2, 2, 3], 5), ([1, 1, 1], 2)):
        got = NS["combination_sum2"](list(c), t)
        assert {tuple(x) for x in got} == brute_cs2(c, t) and len(got) == len({tuple(x) for x in got})
    def valid(s):
        b = 0
        for ch in s:
            b += 1 if ch == "(" else -1
            if b < 0:
                return False
        return b == 0
    for n in range(1, 8):
        got = NS["generate_parenthesis"](n)
        want = [s for s in ("".join(p) for p in itertools.product("()", repeat=2 * n)) if valid(s)]
        assert sorted(got) == sorted(want)
    assert len(NS["generate_parenthesis"](3)) == 5
    PH = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl", "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
    for d in ("", "2", "23", "79"):
        got = NS["letter_combinations"](d)
        want = ["".join(p) for p in itertools.product(*[PH[x] for x in d])] if d else []
        assert got == want
    def brute_ws(board, word):
        R, C = len(board), len(board[0])
        def go(r, c, k, seen):
            if board[r][c] != word[k]:
                return False
            if k == len(word) - 1:
                return True
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and (nr, nc) not in seen:
                    if go(nr, nc, k + 1, seen | {(nr, nc)}):
                        return True
            return False
        return any(go(r, c, 0, {(r, c)}) for r in range(R) for c in range(C))
    import random
    random.seed(7)
    for _ in range(400):
        R, C = random.randint(1, 3), random.randint(1, 3)
        b = [[random.choice("ABC") for _ in range(C)] for _ in range(R)]
        w = "".join(random.choice("ABC") for _ in range(random.randint(1, 5)))
        b0 = [r[:] for r in b]
        assert NS["exist"](b, w) == brute_ws(b0, w)
        assert b == b0                       # 撤销做对了: board 原样
    for n, cnt in ((1, 1), (2, 0), (3, 0), (4, 2), (5, 10), (6, 4), (8, 92)):
        assert len(NS["solve_n_queens"](n)) == cnt
    assert NS["solve_n_queens"](4) == [[".Q..", "...Q", "Q...", "..Q."], ["..Q.", "Q...", "...Q", ".Q.."]]
    # 模板: 用最简单的 "n 位二进制串" 实例化, 确认骨架能跑
    res = []
    def is_done(p): return len(p) == 3
    def valid_(p, c): return True
    def next_choices(p, c): return [0, 1]
    def backtrack(path, choices):
        if is_done(path):
            res.append(path[:]); return
        for c in choices:
            if not valid_(path, c): continue
            path.append(c)
            backtrack(path, next_choices(path, c))
            path.pop()
    backtrack([], [0, 1])
    assert len(res) == 8 and res[0] == [0, 0, 0] and res[-1] == [1, 1, 1]
    print("all tests passed")


_test()

# ===================================================================== 带记录的版本 (逻辑与上面完全一致, 只多了 rec.* 调用)
def F(p):
    return "[" + ",".join(str(x) for x in p) + "]"


def rec_subsets(nums):
    R = Rec("[]")
    res, path = [], []

    def dfs(start):
        res.append(path[:])
        R.record(path, F(path), "res 多一个答案")
        for i in range(start, len(nums)):
            path.append(nums[i])
            R.push(nums[i], path, F(path), why="start=%d, i=%d" % (start, i))
            dfs(i + 1)
            before = F(path)
            path.pop()
            R.pop(nums[i], path, "%s 的子树走完" % before)
    dfs(0)
    return R, res


def rec_permute(nums):
    R = Rec("[]")
    res, path = [], []
    used = [False] * len(nums)

    def dfs():
        if len(path) == len(nums):
            res.append(path[:])
            R.record(path, F(path), "len(path) == %d" % len(nums), dict(used=list(used)))
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            R.push(nums[i], path, F(path), dict(used=list(used)), "used[%d] = True" % i)
            dfs()
            path.pop()
            used[i] = False
            R.pop(nums[i], path, "used[%d] = False" % i, dict(used=list(used)))
    dfs()
    return R, res


def rec_comb(candidates, target):
    candidates = sorted(candidates)
    R = Rec("[]")
    res, path = [], []

    def dfs(start, remain):
        if remain == 0:
            res.append(path[:])
            R.record(path, F(path), "remain == 0", dict(remain=remain))
            return
        for i in range(start, len(candidates)):
            c = candidates[i]
            if c > remain:
                R.prune(c, path, F(path + [c]), "%d>%d" % (c, remain),
                        "%d > remain %d, break" % (c, remain), dict(remain=remain))
                break
            path.append(c)
            R.push(c, path, F(path), dict(remain=remain - c), "%d <= remain %d" % (c, remain))
            dfs(i, remain - c)
            path.pop()
            R.pop(c, path, "%d 的子树走完" % c, dict(remain=remain))
    dfs(0, target)
    return R, res


def rec_comb2(candidates, target):
    candidates = sorted(candidates)
    R = Rec("[]")
    res, path = [], []

    def dfs(start, remain):
        if remain == 0:
            res.append(path[:])
            R.record(path, F(path), "remain == 0", dict(remain=remain))
            return
        for i in range(start, len(candidates)):
            c = candidates[i]
            if i > start and c == candidates[i - 1]:
                R.prune(c, path, F(path + [c]), "同层重复",
                        "i=%d>start=%d, %d==%d" % (i, start, c, candidates[i - 1]),
                        dict(remain=remain))
                continue
            if c > remain:
                R.prune(c, path, F(path + [c]), "%d>%d" % (c, remain),
                        "%d > remain %d, break" % (c, remain), dict(remain=remain))
                break
            path.append(c)
            R.push(c, path, F(path), dict(remain=remain - c), "i=%d, start=%d" % (i, start))
            dfs(i + 1, remain - c)
            path.pop()
            R.pop(c, path, "%d 的子树走完" % c, dict(remain=remain))
    dfs(0, target)
    return R, res


def rec_parens(n):
    R = Rec('""')
    res, path = [], []

    def S():
        return "".join(path)

    def dfs(o, c):
        if len(path) == 2 * n:
            res.append("".join(path))
            R.record(path, S(), "len(path) == %d" % (2 * n), dict(o=o, c=c))
            return
        if o < n:
            path.append("(")
            R.push("(", path, S(), dict(o=o + 1, c=c), "open_ %d < n %d" % (o, n))
            dfs(o + 1, c)
            path.pop()
            R.pop("(", path, "子树走完", dict(o=o, c=c))
        else:
            R.prune("(", path, S() + "(", "open_=n", "open_ = n = %d" % n, dict(o=o, c=c))
        if c < o:
            path.append(")")
            R.push(")", path, S(), dict(o=o, c=c + 1), "close %d < open_ %d" % (c, o))
            dfs(o, c + 1)
            path.pop()
            R.pop(")", path, "子树走完", dict(o=o, c=c))
        else:
            R.prune(")", path, S() + ")", "close\n>= open_", "close %d >= open_ %d" % (c, o),
                    dict(o=o, c=c))
    dfs(0, 0)
    return R, res


PHONE = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
         "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}


def rec_letters(digits):
    R = Rec('""')
    res, path = [], []

    def dfs(idx):
        if idx == len(digits):
            res.append("".join(path))
            R.record(path, "".join(path), "idx == %d" % len(digits), dict(idx=idx))
            return
        for ch in PHONE[digits[idx]]:
            path.append(ch)
            R.push(ch, path, "".join(path), dict(idx=idx + 1), "digits[%d]=%s" % (idx, digits[idx]))
            dfs(idx + 1)
            path.pop()
            R.pop(ch, path, "子树走完", dict(idx=idx))
    dfs(0)
    return R, res


def rec_wsearch(board, word):
    board = [r[:] for r in board]
    R = Rec("")
    path = []
    Rn, Cn = len(board), len(board[0])
    ans = {}

    def snap():
        return dict(grid=[r[:] for r in board])

    def dfs(r, c, k):
        if k == len(word):
            R.record(path, "".join(path), "k == len(word)", snap())
            return True
        if not (0 <= r < Rn and 0 <= c < Cn):
            R.prune("x", path, "x", "越界", "(%d,%d) 越界" % (r, c), snap())
            return False
        if board[r][c] != word[k]:
            why = ("(%d,%d) 是 # 用过了" % (r, c)) if board[r][c] == "#" else \
                  ("%s != word[%d]=%s" % (board[r][c], k, word[k]))
            R.prune(board[r][c], path, "x", "", why, snap())
            return False
        board[r][c] = "#"
        path.append(word[k])
        R.push(word[k], path, "x", snap(), "mark (%d,%d) -> #" % (r, c))
        found = (dfs(r + 1, c, k + 1) or dfs(r - 1, c, k + 1) or
                 dfs(r, c + 1, k + 1) or dfs(r, c - 1, k + 1))
        board[r][c] = word[k]
        path.pop()
        R.pop(word[k], path, "恢复 (%d,%d) = %s" % (r, c, word[k]), snap())
        return found
    out = any(dfs(r, c, 0) for r in range(Rn) for c in range(Cn))
    return R, out


def rec_nqueens(n):
    R = Rec("[]")
    res, path = [], []
    cols, diag, anti = set(), set(), set()

    def sets():
        return dict(cols=sorted(cols), diag=sorted(diag), anti=sorted(anti))

    def dfs(r):
        if r == n:
            res.append(list(path))
            R.record(path, F(path), "r == n", sets())
            return
        for c in range(n):
            if c in cols or (r - c) in diag or (r + c) in anti:
                if c in cols:
                    why = "col %d 在 cols 里" % c
                elif (r - c) in diag:
                    why = "r-c=%d 在 diag 里" % (r - c)
                else:
                    why = "r+c=%d 在 anti 里" % (r + c)
                R.prune(c, path, F(path + [c]), "", why, sets())
                continue
            cols.add(c); diag.add(r - c); anti.add(r + c)
            path.append(c)
            R.push(c, path, F(path), sets(), "place (%d,%d)" % (r, c))
            dfs(r + 1)
            path.pop()
            cols.remove(c); diag.remove(r - c); anti.remove(r + c)
            R.pop(c, path, "撤销 (%d,%d)" % (r, c), sets())
    dfs(0)
    return R, res


# 一致性: 带记录版本的答案 == 展示的版本的答案
assert rec_subsets([1, 2, 3])[1] == NS["subsets_start"]([1, 2, 3])
assert rec_permute([1, 2, 3])[1] == NS["permute"]([1, 2, 3])
assert rec_comb([2, 3, 5], 8)[1] == NS["combination_sum"]([2, 3, 5], 8)
assert rec_comb2([1, 2, 2, 3], 5)[1] == NS["combination_sum2"]([1, 2, 2, 3], 5)
assert rec_parens(2)[1] == NS["generate_parenthesis"](2)
assert rec_parens(3)[1] == NS["generate_parenthesis"](3)
assert rec_letters("23")[1] == NS["letter_combinations"]("23")
assert [[r for r in range(4)] for _ in range(1)]
assert [["." * c + "Q" + "." * (3 - c) for c in sol] for sol in rec_nqueens(4)[1]] == NS["solve_n_queens"](4)

# ===================================================================== SVG
import os
import json
SVGDIR = os.path.join(ROOT_DIR, "docs", "svg", "13-backtracking")
os.makedirs(SVGDIR, exist_ok=True)


def save(s):
    with open(os.path.join(SVGDIR, s.name + ".svg"), "w", encoding="utf-8") as f:
        f.write(s.out())


# ---------- trace 右侧列 (每题一个) ----------
def res_line(s, x, y, e):
    if e["kind"] == "record":
        txt = "res += %s (共 %d)" % (e["val"], e["nres"])
        w = tw(txt, 12) + 12
        s.rect(x - 4, y - 9, w, 18, NEW)
        s.t(x + 2, y, txt, 12, NEW[2], "start", 500, maxw=176)
    else:
        s.t(x, y, "res 共 %d 个" % e["nres"], 12, SUB)


def ex_res(s, x, top, rh, e):
    res_line(s, x, top + rh / 2, e)


def mk_ex_perm(nums):
    def fn(s, x, top, rh, e):
        used = e["extra"]["used"]
        for j, u in enumerate(used):
            s.cell(x + j * 25, top + 4, 23, 20, str(nums[j]), NEW if u else OTH, size=12)
        s.t(x + 3 * 25 + 4, top + 14, "← used", 12, SUB)
        res_line(s, x, top + rh - 12, e)
    return fn


def mk_ex_remain(target):
    def fn(s, x, top, rh, e):
        if e["kind"] == "record":
            rem = 0
        else:
            rem = e["extra"]["remain"]
        p = e["path"]
        if e["kind"] == "prune":
            sm = "+".join(str(v) for v in p) or "0"
        else:
            sm = "+".join(str(v) for v in p) or "0"
        s.t(x, top + 13, "remain = %d - (%s) = %d" % (target, sm, target - sum(p)), 12, INK,
            "start", 400, maxw=176)
        res_line(s, x, top + rh - 12, e)
    return fn


def ex_parens(s, x, top, rh, e):
    o, c = e["extra"]["o"], e["extra"]["c"]
    s.t(x, top + 13, "open_ = %d, close = %d" % (o, c), 12, INK)
    res_line(s, x, top + rh - 12, e)


def mk_ex_letters(n):
    def fn(s, x, top, rh, e):
        s.t(x, top + 13, "idx = %d / %d" % (e["extra"]["idx"], n), 12, INK)
        res_line(s, x, top + rh - 12, e)
    return fn


def ex_ws(s, x, top, rh, e):
    g = e["extra"]["grid"]
    cs = 18
    gy = top + (rh - cs * len(g)) / 2
    for r, row in enumerate(g):
        for c, ch in enumerate(row):
            s.cell(x + c * (cs + 2), gy + r * (cs + 2) - (r * 0), cs, cs, ch,
                   NEW if ch == "#" else OTH, size=12)
    nh = sum(ch == "#" for row in g for ch in row)
    s.t(x + len(g[0]) * (cs + 2) + 8, top + rh / 2 - 7, "# 个数 = %d" % nh, 12, INK)
    s.t(x + len(g[0]) * (cs + 2) + 8, top + rh / 2 + 9, "len(path) = %d" % len(e["path"]), 12, INK)


def ex_nq(s, x, top, rh, e):
    ex = e["extra"]
    fmt = lambda a: "{" + ", ".join(str(v) for v in a) + "}"
    s.t(x, top + 9, "cols = " + fmt(ex["cols"]), 12, INK)
    s.t(x, top + 24, "diag = " + fmt(ex["diag"]), 12, INK)
    s.t(x, top + 39, "anti = " + fmt(ex["anti"]), 12, INK)
    if e["kind"] == "record":
        s.rect(x + 108, top + 14, 66, 20, NEW)
        s.t(x + 113, top + 24, "res 共 %d 个" % e["nres"], 12, NEW[2], "start", 500)


# ---------- core: decision tree ----------
def core_tree(name, title, desc, lines, R, bottom, legend_extra=None, level_h=66,
              label_size=13):
    y0 = 18 + 20 * len(lines) + 34
    # 先画到一个临时 Svg 拿到 bottom 高度
    tmp = Svg(name, 100, title, desc)
    b = draw_tree(tmp, R.root, y0, level_h=level_h, label_size=label_size)
    H = int(b + 14 + 22 * len(bottom) + 40)
    s = Svg(name, H, title, desc)
    for i, ln in enumerate(lines):
        s.t(40, 18 + i * 20, ln, 12, SUB)
    draw_tree(s, R.root, y0, level_h=level_h, label_size=label_size)
    y = b + 6
    for i, ln in enumerate(bottom):
        s.t(40, y + 10 + i * 22, ln, 14 if i == 0 else 12, INK if i == 0 else SUB,
            "start", 500 if i == 0 else 400)
    y += 22 * len(bottom) + 18
    items = [(NEW, False, "收集到的答案"), (OTH, False, "普通节点 (path)")]
    if R.nprune:
        items.append((REM, True, "被剪枝的分支 (写原因)"))
    if legend_extra:
        items += legend_extra
    s.legend(y, items)
    return s


# ---------- 第 0 节 core ----------
def svg_core0():
    R, _ = rec_subsets([1, 2])
    s = Svg("first_principles_core", 520, "Backtracking = decision tree 上的 DFS",
            "nums=[1,2] 的 decision tree, 以及 DFS 过程中 path 这个共用 list 的 push/pop 时间线。")
    s.t(40, 18, "nums = [1, 2] · 节点 = 一个 path 状态 · 边 = 一次选择 · DFS 往下走 = push, 往回走 = pop", 12, SUB)
    s.t(40, 38, "左: decision tree (绿箭头 push, 红虚线 pop) · 右: 同一个 path list 随时间 t 的变化", 12, SUB)
    nodes = {"": (150, 100), "1": (84, 176), "2": (216, 176), "12": (84, 252)}
    labels = {"": "[]", "1": "[1]", "2": "[2]", "12": "[1,2]"}
    for k, (cx, cy) in nodes.items():
        pass
    # 边 (down 绿实线 / up 红虚线), 偏移 5px 并排
    def edge(a, b, dx):
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        s.line(x1 - dx, y1 + 13, x2 - dx, y2 - 13, NEW[1], None, 1.5, "arrowG")
        s.line(x2 + dx, y2 - 13, x1 + dx, y1 + 13, ARROW_RED, "4 3", 1.5, "arrowR")
    edge("", "1", 5)
    edge("", "2", 5)
    edge("1", "12", 5)
    for k, (cx, cy) in nodes.items():
        role = NEW
        w = 54 if k == "12" else 44
        s.node(cx, cy, w, 26, labels[k], role)
    # 边上的 t 标签
    s.t(104, 128, "t1 push 1", 12, NEW[2], "end", 500)
    s.t(122, 150, "t4 pop 1", 12, REM[2], "start", 500)
    s.t(196, 120, "t5 push 2", 12, NEW[2], "start", 500)
    s.t(236, 150, "t6 pop 2", 12, REM[2], "start", 500)
    s.t(98, 202, "t2 push 2", 12, NEW[2], "start", 500)
    s.t(98, 224, "t3 pop 2", 12, REM[2], "start", 500)
    s.t(40, 296, "path 上每个节点都已是答案 (绿): 节点数 = 4 = 2^2", 12, SUB)
    # 右: 时间线
    tx = 340
    s.t(tx, 62, "t", 12, SUB)
    s.t(tx + 26, 62, "动作", 12, SUB)
    s.t(tx + 90, 62, "被撤销", 12, SUB)
    s.t(tx + 146, 62, "path (同一个 list)", 12, SUB)
    s.sep(72, tx, 640)
    ev = [e for e in R.ev if e["kind"] in ("push", "pop")]
    rows = [dict(kind="init", val="", path=[])] + ev
    y = 80
    cw = 30
    for t, e in enumerate(rows):
        s.t(tx, y + 17, "t%d" % t, 12, SUB)
        k = e["kind"]
        if k == "init":
            s.t(tx + 26, y + 17, "开始", 14, INK, "start", 500)
        else:
            s.t(tx + 26, y + 17, "%s %s" % (k, e["val"]), 14,
                NEW[2] if k == "push" else REM[2], "start", 500)
        p = e["path"]
        px = tx + 146
        for j, v in enumerate(p):
            s.cell(px + j * (cw + 2), y + 3, cw, 28, str(v), NEW if (k == "push" and j == len(p) - 1) else OTH)
        if p:
            s.ring(px + (len(p) - 1) * (cw + 2), y + 3, cw, 28)
        else:
            s.t(px, y + 17, "[ ] 空", 12, SUB)
        if k == "pop":
            s.cell(tx + 90, y + 3, cw, 28, str(e["val"]), REM, True)
            sx = px + len(p) * (cw + 2)
            s.path("M%g %g L%g %g L%g %g L%g %g" % (sx + cw / 2, y + 3, sx + cw / 2, y - 1,
                                                  tx + 90 + cw / 2, y - 1, tx + 90 + cw / 2, y + 2),
                   ARROW_RED, "4 3", 1.5, "arrowR")
        y += 36
        s.sep(y - 2, tx, 640)
    # 底部: 三件事 + 为什么要 pop
    yb = 352
    s.t(40, yb, "backtracking 的三件事", 14, INK, "start", 500)
    s.t(40, yb + 24, "path = 已做的选择 (从 root 走到当前节点的路), 一个共用的 list · 此刻 t2: path = [1, 2]", 12, SUB)
    s.t(40, yb + 44, "choices = 还能选什么 (nums[start:]), 每个选择是一条往下的边 · t2: start = 2, 没有可选 => 往回走", 12, SUB)
    s.t(40, yb + 64, "结束条件 = 什么时候收集答案 / 不能再往下 · 这里: 进入每个节点就收集 path[:]", 12, SUB)
    s.t(40, yb + 90, "为什么必须 pop", 14, INK, "start", 500)
    s.t(40, yb + 114, "path 只有一个 list。t3、t4 如果不 pop, t5 push 2 之后 path = [1, 2, 2], 而不是 [2]。", 12, SUB)
    s.t(40, yb + 134, "收集时也要 copy: res.append(path) 存的是同一个 list, 最后 res 里全是 [] (t6 之后 path 为空)。", 12, SUB)
    s.t(40, yb + 160, "complexity = decision tree 的节点数 × 每个节点的工作: 4 个节点 × copy path", 14, INK, "start", 500)
    s.legend(yb + 192, [(NEW, False, "push / 新选择 / 答案"), (REM, True, "pop 撤销")])
    s.rect(330, yb + 185, 16, 14, OTH, fill="none", stroke=RING, sw=2.5)
    s.t(352, yb + 192, "path 栈顶", 12, SUB)
    s.h = yb + 192 + 28
    return s


def svg_ws_core(board, word):
    R, ok = rec_wsearch(board, word)
    grids = [("进入 dfs 前", [r[:] for r in board], None),
             ("t2: 走了 A→B", R.ev[1]["extra"]["grid"], (1, 0)),
             ("t7: pop B 之后", R.ev[6]["extra"]["grid"], (1, 0)),
             ("t13: 找到 ABAD", R.ev[12]["extra"]["grid"], (1, 2))]
    caps = [["原始 board", "A B A / B B D"],
            ["(0,0) (1,0) 变成 #", "# 个数 = len(path) = 2"],
            ["(1,0) 变回 B", "(0,0) 仍是 #"],
            ["4 个 # = ABAD", "return True 之前"]]
    s = Svg("word_search_core", 360, "Word Search: 用 board 本身当 used[]",
            "同一个 board 在 DFS 不同时刻的四个快照: 标记 # 和恢复。")
    s.t(40, 18, "board = A B A / B B D · word = ABAD · 做选择 = 把格子改成 #, 撤销 = 改回原字母", 12, SUB)
    s.t(40, 38, "# 的位置 = path 走过的格子, 所以 \"同一格不能用两次\" 不需要额外的 used 或 set", 12, SUB)
    cs = 36
    for gi, (ttl, g, cur) in enumerate(grids):
        gx = 40 + gi * 150
        s.t(gx, 66, ttl, 14, INK, "start", 500)
        for r, row in enumerate(g):
            for c, ch in enumerate(row):
                s.cell(gx + c * (cs + 2), 82 + r * (cs + 2), cs, cs, ch,
                       NEW if ch == "#" else OTH)
        if cur and g[cur[0]][cur[1]] == "#":
            s.ring(gx + cur[1] * (cs + 2), 82 + cur[0] * (cs + 2), cs, cs)
        if gi == 2:
            s.cell(gx + 0 * (cs + 2), 82 + 1 * (cs + 2), cs, cs, "B", OTH)
            s.ring(gx + 0 * (cs + 2), 82 + 1 * (cs + 2), cs, cs)
        for j, ln in enumerate(caps[gi]):
            s.t(gx, 82 + 2 * (cs + 2) + 14 + j * 16, ln, 12, SUB, maxw=140)
    y = 82 + 2 * (cs + 2) + 66
    s.t(40, y, "三步写法 (一定成对出现)", 14, INK, "start", 500)
    s.t(40, y + 24, "1. board[r][c] = \"#\"        做选择: 当前格子标记为已用", 12, SUB)
    s.t(40, y + 44, "2. found = dfs(上) or dfs(下) or dfs(左) or dfs(右)        递归: 往 4 个方向走", 12, SUB)
    s.t(40, y + 64, "3. board[r][c] = word[k]    撤销: 改回原字母 (找到了也要改回, 否则调用者的 board 被破坏)", 12, SUB)
    s.t(40, y + 92, "忘了第 3 步: (1,0) 永远是 #, 之后从别的起点或别的路线都经过不了它, 会漏掉答案", 12, SUB)
    s.legend(y + 124, [(NEW, False, "# = 在 path 里 (已用)"), (OTH, False, "原字母")])
    s.rect(330, y + 117, 16, 14, OTH, fill="none", stroke=RING, sw=2.5)
    s.t(352, y + 124, "当前 / 刚恢复的格子", 12, SUB)
    s.h = y + 124 + 28
    return s


def svg_nq_core():
    s = Svg("n_queens_core", 470, "N-Queens: 三个 set 把 \"是否冲突\" 变成 O(1)",
            "n=4, 前两行已放皇后, 第 2 行每一列的检查过程。")
    s.t(40, 18, "n = 4 · 已放: (0,1) 和 (1,3) · 现在要放第 r = 2 行 · 每行恰好一个皇后, 所以 path[r] = 列", 12, SUB)
    s.t(40, 38, "同一列: c 相同 · 同一条 \\ 对角线: r - c 相同 · 同一条 / 对角线: r + c 相同", 12, SUB)
    cs, bx, by = 44, 40, 62
    queens = [(0, 1), (1, 3)]
    # 先画红色虚线: 皇后的攻击线 (列 + 两条对角线), 画在格子下面
    for r in range(4):
        for c in range(4):
            s.rect(bx + c * cs, by + r * cs, cs, cs, OTH, fill="#FFFFFF" if (r + c) % 2 == 0 else "#F1EFE8",
                   stroke="#B4B2A9", sw=1, rx=0)
    def center(r, c):
        return bx + c * cs + cs / 2, by + r * cs + cs / 2
    for (qr, qc) in queens:
        # 列
        x1, y1 = center(0, qc); x2, y2 = center(3, qc)
        s.line(x1, y1, x2, y2, ARROW_RED, "4 3", 1.2)
        # \ 对角线 r-c 相同
        pts = [(r, r - (qr - qc)) for r in range(4) if 0 <= r - (qr - qc) < 4]
        (ar, ac), (br, bc) = pts[0], pts[-1]
        x1, y1 = center(ar, ac); x2, y2 = center(br, bc)
        s.line(x1, y1, x2, y2, ARROW_RED, "4 3", 1.2)
        # / 对角线 r+c 相同
        pts = [(r, (qr + qc) - r) for r in range(4) if 0 <= (qr + qc) - r < 4]
        (ar, ac), (br, bc) = pts[0], pts[-1]
        x1, y1 = center(ar, ac); x2, y2 = center(br, bc)
        s.line(x1, y1, x2, y2, ARROW_RED, "4 3", 1.2)
    for (qr, qc) in queens:
        cx, cy = center(qr, qc)
        s.circ(cx, cy, 15, NEW, False, 1.5)
        s.t(cx, cy, "Q", 14, NEW[2], "middle", 500)
    # 第 2 行的四个候选: 标记
    marks = {0: ("ok", "OK"), 1: ("x", "x"), 2: ("x", "x"), 3: ("x", "x")}
    for c, (k, txt) in marks.items():
        cx, cy = center(2, c)
        if k == "ok":
            s.ring(bx + c * cs + 3, by + 2 * cs + 3, cs - 6, cs - 6)
            s.t(cx, cy, "OK", 14, NEW[2], "middle", 500)
        else:
            s.rect(bx + c * cs + 5, by + 2 * cs + 5, cs - 10, cs - 10, REM, True)
            s.t(cx, cy, "x", 14, REM[2], "middle", 500)
    for c in range(4):
        s.t(bx + c * cs + cs / 2, by - 8, "c=%d" % c, 12, SUB, "middle")
    for r in range(4):
        s.t(bx - 6, by + r * cs + cs / 2, "r=%d" % r, 12, SUB, "end")
    # 右: 三个 set + 第 2 行逐列检查
    rx = 262
    s.t(rx, 66, "三个 set (已放 (0,1) 和 (1,3))", 14, INK, "start", 500)
    s.t(rx, 90, "cols = {1, 3}", 14, INK, "start", 500)
    s.t(rx + 130, 90, "= 已占用的列", 12, SUB)
    s.t(rx, 112, "diag = {-1, -2}", 14, INK, "start", 500)
    s.t(rx + 130, 112, "= r - c: 0-1, 1-3", 12, SUB)
    s.t(rx, 134, "anti = {1, 4}", 14, INK, "start", 500)
    s.t(rx + 130, 134, "= r + c: 0+1, 1+3", 12, SUB)
    s.sep(148, rx, 640)
    s.t(rx, 164, "第 r = 2 行, 逐列检查 (只查 3 次 set, O(1))", 14, INK, "start", 500)
    rows = [
        (NEW, "c=0: 0 不在 cols, 2-0=2 不在 diag, 2+0=2 不在 anti", "放"),
        (REM, "c=1: 1 在 cols => 剪枝", ""),
        (REM, "c=2: 2+2=4 在 anti => 剪枝", ""),
        (REM, "c=3: 3 在 cols => 剪枝", ""),
    ]
    for i, (role, txt, _) in enumerate(rows):
        yy = 190 + i * 24
        s.rect(rx, yy - 9, 14, 14, role, role is REM)
        s.t(rx + 22, yy, txt, 12, role[2] if role is REM else INK, "start", 400, maxw=360)
    s.t(rx, 296, "做选择: 三个 set 各 add 一个值 + path.append(c)", 12, SUB)
    s.t(rx, 316, "撤销: 三个 set 各 remove 同一个值 + path.pop()", 12, SUB)
    s.t(rx, 336, "漏掉一个 remove => 后面的分支会被 \"幽灵皇后\" 误剪", 12, SUB)
    s.t(40, 262, "红色虚线 = 已有皇后的", 12, SUB)
    s.t(40, 280, "攻击线 (列 / 两条对角线)", 12, SUB)
    s.t(40, 302, "第 2 行只有 c=0 安全", 12, SUB)
    s.t(40, 320, "=> 只剩一个选择", 12, SUB)
    s.t(40, 380, "没有 set 的话: 每放一个皇后要扫已有皇后 O(n) 次 => 总共 O(n) × 节点数", 14, INK, "start", 500)
    s.t(40, 404, "有了 set: 每次检查 O(1), 同一个 decision tree 少一个 n 的因子", 12, SUB)
    s.legend(436, [(NEW, False, "皇后 / 可以放"), (REM, True, "被攻击 => 剪枝")])
    return s


# ---------- 把所有图生成出来 ----------
def build_svgs():
    out = {}
    s = svg_core0(); save(s); out["core0"] = s

    # 1 Subsets
    R, res = rec_subsets([1, 2, 3])
    s = core_tree("subsets_core", "Subsets 的 decision tree",
                  "nums=[1,2,3], 每个节点都是答案, 共 8 个。",
                  ["nums = [1, 2, 3] · 节点 = path · 子节点 = path + [nums[i]], i 只能取 start 之后的",
                   "每个节点都收集 => 没有剪枝, 也没有 \"废节点\""],
                  R, ["节点数 = 2^3 = 8 => 8 个答案 (每个节点收集一次)",
                      "[2,1] 不会出现: 选了 2 之后 start = 2, 只能再选 3"])
    save(s)
    ex = ex_res
    s = trace_svg("subsets_trace", "Subsets 的 path 变化",
                  "nums=[1,2,3] 前 13 步 push/pop。",
                  ["nums = [1, 2, 3] · 每个节点: 先收集 path[:], 再逐个 push → 递归 → pop",
                   "'被撤销' 列 = 刚 pop 掉的元素 (虚线扔到左边); 原因写在左边动作下面"],
                  R.ev, 13, "res (收集到的答案)", ex,
                  ["最终 res = %s" % str(res).replace(" ", ""),
                   "共 %d 个 = 2^3; 前 13 步已经走完 [1] 整棵子树, 第 14 步 push 2 开始 [2] 子树" % len(res)])
    save(s)

    # 2 Permutations
    R, res = rec_permute([1, 2, 3])
    s = core_tree("permutations_core", "Permutations 的 decision tree",
                  "nums=[1,2,3], 6 个叶子。",
                  ["nums = [1, 2, 3] · 每层都从头看 3 个数, used[i] 为真的跳过 (没有画出)",
                   "每层的 choices = 还没用的数: 第 1 层 3 个, 第 2 层 2 个, 第 3 层 1 个"],
                  R, ["节点数 = 1 + 3 + 3×2 + 3×2×1 = 16 · 叶子 = 3! = 6 个答案",
                      "只有叶子是答案 (len(path) == 3); 中间节点只是 partial path"])
    save(s)
    s = trace_svg("permutations_trace", "Permutations 的 path / used 变化",
                  "nums=[1,2,3] 前 12 步。",
                  ["nums = [1, 2, 3] · push: used[i] = True 且 path.append · pop: 两个一起还原",
                   "'used' 列: 绿色 = 在 path 里的数, 灰色 = 还能选的数"],
                  R.ev, 12, "used / res", mk_ex_perm([1, 2, 3]),
                  ["最终 res = %s" % str(res).replace(" ", ""),
                   "共 %d 个 = 3!; 第 5、6 步 pop 之后 used 变回灰色, 第 7 步才能选 3" % len(res)])
    save(s)

    # 3 Combination Sum
    R, res = rec_comb([2, 3, 5], 6)
    s = core_tree("combination_sum_core", "Combination Sum 的 decision tree",
                  "candidates=[2,3,5], target=6。",
                  ["candidates = [2, 3, 5] · target = 6 · 子节点 = 从 candidates[start:] 里选一个, 可以和父节点同值",
                   "剪枝: c > remain => break (排序后, 后面更大的也不行, 所以不画 [2,2,5] 这类节点)"],
                  R, ["答案 %s · 节点数 %d (含 %d 个被剪掉的)" % (str(res).replace(" ", ""), count_nodes(R.root), R.nprune),
                      "dfs(i, ...) 传 i: [2,2] 的下一层仍可选 2; 如果传 i+1, 每个数只能用一次, [2,2,2] 和 [3,3] 都出不来"])
    save(s)
    s = trace_svg("combination_sum_trace", "Combination Sum 的 path / remain 变化",
                  "candidates=[2,3,5], target=6 前 14 步。",
                  ["candidates = [2, 3, 5] · target = 6 · remain = target - sum(path)",
                   "每次 push c: remain 减 c · c > remain 就剪枝 (红色虚线格子 = 想选但不能选)"],
                  R.ev, 14, "remain / res", mk_ex_remain(6),
                  ["最终 res = %s" % str(res).replace(" ", ""),
                   "[3,3] 里的第二个 3 来自 dfs(i, ...): 同一个下标可以重复选"])
    save(s)

    # 4 Combination Sum II
    R, res = rec_comb2([1, 2, 2, 3], 5)
    s = core_tree("combination_sum_ii_core", "Combination Sum II 的 decision tree",
                  "candidates=[1,2,2,3], target=5, 同层去重。",
                  ["candidates 排序后 = [1, 2, 2, 3] · target = 5 · 每个数最多用一次 => dfs(i+1, ...)",
                   "同一层第二个 2 (i > start 且 与前一个相等) 的子树和第一个 2 完全相同 => 剪掉"],
                  R, ["答案 %s · 节点数 %d (含 %d 个被剪掉的)" % (str(res).replace(" ", ""), count_nodes(R.root), R.nprune),
                      "[1,2,2] 里两个 2 都留着: 第二个 2 在下一层 (i == start), 不是同一层"])
    save(s)
    s = trace_svg("combination_sum_ii_trace", "Combination Sum II 的同层去重",
                  "candidates=[1,2,2,3], target=5 前 12 步。",
                  ["candidates = [1, 2, 2, 3] (下标 0..3) · target = 5 · 去重条件: i > start 且 c == candidates[i-1]",
                   "第 8 步: 在 path=[1] 这一层, i=2 的 2 和 i=1 的 2 相同, 子树重复 => 剪枝"],
                  R.ev, 12, "remain / res", mk_ex_remain(5),
                  ["最终 res = %s" % str(res).replace(" ", ""),
                   "第 3 步 [1,2,2] 允许: 那是下一层, i=2 == start=2, 不触发去重条件"])
    save(s)

    # 5 Generate Parentheses
    R, res = rec_parens(2)
    s = core_tree("generate_parentheses_core", "Generate Parentheses 的 decision tree",
                  "n=2, 两个剪枝条件。",
                  ["n = 2 · 每个节点最多两个选择: 加 \"(\" (需要 open_ < n) 或 加 \")\" (需要 close < open_)",
                   "红色虚线 = 被两个条件挡住的选择; 剩下的每个叶子都合法"],
                  R, ["答案 %s · 节点数 %d (含 %d 个被剪掉的)" % (json.dumps(res).replace(" ", ""), count_nodes(R.root), R.nprune),
                      "没有剪枝要枚举 2^4 = 16 个串再检查; 剪枝后只展开了 %d 个节点, 叶子全是答案" % (count_nodes(R.root) - R.nprune)])
    save(s)
    s = trace_svg("generate_parentheses_trace", "Generate Parentheses 的 path 变化",
                  "n=2 前 12 步。",
                  ["n = 2 · push \"(\" 要 open_ < n · push \")\" 要 close < open_ · path 的长度到 2n = 4 就收集",
                   "红色虚线格子 = 想加但被条件挡住 (原因写在左边)"],
                  R.ev, 12, "open_ / close / res", ex_parens,
                  ["最终 res = %s" % json.dumps(res).replace(" ", ""),
                   "n = 3 时共 5 个答案 (Catalan 数: 1, 2, 5, 14, ...)"])
    save(s)

    # 6 Letter Combinations
    R, res = rec_letters("23")
    s = core_tree("letter_combinations_core", "Letter Combinations 的 decision tree",
                  "digits=23, 3×3=9 个叶子。",
                  ["digits = \"23\" · 第 1 层从 \"abc\" 选一个, 第 2 层从 \"def\" 选一个",
                   "每层的 choices 由层数 idx 决定, 和 path 里选了什么无关 => 不需要 start / used"],
                  R, ["节点数 = 1 + 3 + 3×3 = 13 · 叶子 = 3 × 3 = 9 个答案",
                      "没有剪枝: 这是纯粹的笛卡尔积, backtracking 只是把 \"层数不固定的嵌套 for\" 写成递归"])
    save(s)
    s = trace_svg("letter_combinations_trace", "Letter Combinations 的 path 变化",
                  "digits=23 前 12 步。",
                  ["digits = \"23\" · idx = 正在决定第几个数字 · 到 idx == 2 收集",
                   "每个叶子 push 一次、收集一次、pop 一次; 第 11 步 pop a, 回到空 path 试 b"],
                  R.ev, 12, "idx / res", mk_ex_letters(2),
                  ["最终 res = %s" % json.dumps(res).replace(" ", ""),
                   "共 %d 个 = 3 × 3" % len(res)])
    save(s)

    # 7 Word Search
    board = [list("ABA"), list("BBD")]
    word = "ABAD"
    s = svg_ws_core(board, word); save(s)
    R, ok = rec_wsearch(board, word)
    s = trace_svg("word_search_trace", "Word Search 的 path / board 变化",
                  "board=ABA/BBD, word=ABAD 全部 18 步。",
                  ["board = A B A / B B D · word = ABAD · 方向顺序: 下 上 右 左 · 从 (0,0) 开始",
                   "push = 标记成 # · pop = 恢复原字母 · 红色虚线格子 = 这一步走不通 (越界 / 字母不对 / 已用)"],
                  R.ev, 18, "board (# = 已用) / 不变量", ex_ws,
                  ["结果 exist = %s · 路径 (0,0) A → (0,1) B → (0,2) A → (1,2) D" % ok,
                   "第 2-7 步: 先走下 (1,0) 的 B, 四个方向都不行, pop 恢复; 第 9 步改走右 (0,1)"],
                  row_h=42, cw=34)
    save(s)

    # 8 N-Queens
    s = svg_nq_core(); save(s)
    R, res = rec_nqueens(4)
    s = trace_svg("n_queens_trace", "N-Queens 的 path / 三个 set 变化",
                  "n=4 前 17 步。",
                  ["n = 4 · path[r] = 第 r 行的列 · 每步先查 3 个 set, 冲突就剪枝, 不冲突就 push 并同时 add 到 3 个 set",
                   "红色虚线格子 = 想放的列被挡住 (原因写在左边); pop 时三个 set 一起还原"],
                  R.ev, 17, "三个 set", ex_nq,
                  ["最终 n=4 共 %d 个解: %s" % (len(res), str(res).replace(" ", "")),
                   "[0,2] 在第 2 行无处可放, [0,3,1] 在第 3 行无处可放 (死路, 回溯); 全树共 %d 个事件, 解在第 31、48 步" % len(R.ev)],
                  row_h=48, path_title="path (path[r] = 列)")
    save(s)
    return out

# ===================================================================== HTML
def build_doc():
    nq8 = rec_nqueens(8)[0]
    nq8_nodes = nq8.npush + 1
    nq4 = rec_nqueens(4)[0]
    nq4_nodes = nq4.npush + 1
    doc = d.Doc("13 · Backtracking")
    doc.main("主线: backtracking = 在 decision tree 上做 DFS。节点 = 一个 partial path, 边 = 一次选择。"
             "做选择 → 递归 → 撤销选择; 一定走不通的分支, 进去之前就剪掉。")
    doc.main("概念链: Subsets (模板) → Permutations (+ used) → Combination Sum (+ 重复选, + remain 剪枝) → "
             "Combination Sum II (+ 同层去重) → Generate Parentheses (约束剪枝) → "
             "Letter Combinations (每层候选不同) → Word Search (grid, 原地标记) → N-Queens (多个约束 set)")

    # ---------------------------------------------------------------- 0
    doc.h2("0. 第一性原理: 暴力在浪费什么, backtracking 怎么消掉")
    doc.p("题目要的是 <b>所有</b> 组合 / 排列 / 路径。答案个数本身就是指数级, 所以输出大小就是 time complexity 的下限。"
          "能优化的只有一件事: <b>不要展开一定没有答案的分支</b>。")
    doc.p("最直接的暴力是 n 层嵌套 <code>for</code>, 每层选一个, 最后检查合法。它有两个问题。")
    doc.p("① n 是 input, 嵌套层数写不出来。解法: 一层递归 = 一层 <code>for</code>, 递归深度 = 层数。")
    doc.p("② 先生成完整候选, 再检查。以 3 对括号为例: 一共 2^6 = 64 个串, 合法的只有 5 个。"
          "前缀是 <code>)</code> 的串一开始就注定不合法, 却还要把后面 5 位全展开 (2^5 = 32 个)。"
          "backtracking 在每一步选择之前就检查约束, 一旦违反就不进这个分支。")
    doc.p("把所有选择画成树就是 <b>decision tree</b>: 根 = 什么都没选; 每个节点 = 已做的选择 (path); "
          "每条边 = 一个选择。backtracking 就是在这棵树上做 DFS: 往下走 = 做选择, 往回走 = 撤销选择。")
    doc.svg("13-backtracking/first_principles_core.svg",
            "图 0: nums=[1,2] 的 decision tree (左) 和 path 这个共用 list 在 DFS 过程中随时间的 push/pop (右)。"
            "t3、t4 的 pop 保证了 t5 从 [] 开始, 而不是从 [1,2] 开始。")
    doc.h3("三件事")
    doc.p("<b>path</b>: 已经做过的选择, 一个共用的 list。<b>choices</b>: 此刻还能选什么 "
          "(每个选择是一条往下的边)。<b>结束条件</b>: path 什么时候是一个完整答案。")
    doc.h3("为什么必须撤销")
    doc.p("path 只有一个 list, 递归的每一层都在改同一个对象。回到上一层之后, 兄弟分支要看到的是 "
          "<b>做选择之前</b> 的 path。不 pop, 兄弟分支就带着上一个分支的选择 (图 0: path 会变成 [1,2,2])。"
          "收集答案要 <code>path[:]</code> 复制一份, 否则 <code>res</code> 里存的全是同一个 list 的引用, 最后都变成空 list。")
    doc.p("另一种写法是每次传新 list (<code>path + [c]</code>), 不用撤销, 代价是每个节点多 O(n) 的复制。面试默认写 mutate + undo。")
    doc.h3("通用模板")
    doc.code(SRC["template"])
    doc.h3("Complexity 怎么算")
    doc.p("time = decision tree 的节点数 × 每个节点的工作 (通常是 <code>path[:]</code> 的 O(n))。"
          "space = 树的深度 (递归栈 + path), 不算输出。"
          "剪枝的价值就是让节点数从 \"所有候选\" 降到 \"接近答案数\"。")
    doc.note("backtracking = 树上 DFS。path 是共用 list: 做选择 push, 回来 pop; 收集要 copy。complexity 数节点。")

    # ---------------------------------------------------------------- 1 Subsets
    doc.h2("1. Subsets: 每个节点都是答案, start index 防重复")
    doc.p("题: <code>nums = [1,2,3]</code> (无重复), 返回所有子集, 共 8 个: "
          "<code>[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]</code>。")
    doc.p("Brute force: 枚举 bitmask 0 … 2^n−1, 每个 mask 扫 n 位, O(n·2^n)。这其实已经和输出大小一样大, 没有浪费; "
          "但 bitmask 一遇到 \"和等于 target\" \"去重\" 这类约束就没法剪枝。所以先用这题把 backtracking 的骨架学会。")
    doc.p("关键观察: 子集 = 每个元素选 / 不选。为了不生成 <code>[1,2]</code> 和 <code>[2,1]</code> 两个相同的子集, "
          "规定只能往后选: 选了 <code>nums[i]</code> 之后, 下一层从 <code>i+1</code> 开始。这个 <code>start</code> 就是 choices。")
    doc.svg("13-backtracking/subsets_core.svg",
            "图 1a: decision tree。每个节点都是一个答案 (绿); 子节点只能加 start 之后的元素。8 个节点 = 8 个子集。")
    doc.svg("13-backtracking/subsets_trace.svg",
            "图 1b: 前 13 步。进入节点先收集; push 往下, pop 往回, pop 掉的元素虚线扔到左边。")
    doc.code(SRC["subsets"])
    doc.p("等价的 \"选 / 不选\" 写法 (二叉树, 只有叶子是答案), 适合元素有额外状态的题:")
    doc.code(SRC["subsets2"])
    doc.p("Time O(n·2^n): 2^n 个节点, 每个节点 <code>path[:]</code> 复制 O(n)。Space O(n): 递归深度 + path (不算输出)。")
    doc.note("子集 / 组合: 每层只往后选 (<code>range(start, n)</code>, 递归传 <code>i+1</code>); 每个节点都可能是答案。")

    # ---------------------------------------------------------------- 2 Permutations
    doc.h2("2. Permutations: 每层从头看, 用 used[] 跳过已选")
    doc.p("题: <code>nums = [1,2,3]</code>, 返回所有排列, 共 3! = 6 个。")
    doc.p("Brute force: 每个位置从 n 个数里选, 共 n^n = 27 个序列, 再过滤出没有重复数字的, O(n^n · n)。"
          "浪费: 第 2 层又选了 path 里已有的数, 整棵子树都是废的。")
    doc.p("关键观察: 相比 Subsets, 顺序有意义 (<code>[1,2]</code> 和 <code>[2,1]</code> 是两个答案), "
          "所以不能再 \"只往后选\", 每层都要从头看。改两处: <code>range(start, n)</code> → <code>range(n)</code>; "
          "加 <code>used[i]</code> 跳过 path 里已有的数。只有叶子 (<code>len(path) == n</code>) 是答案。")
    doc.svg("13-backtracking/permutations_core.svg",
            "图 2a: decision tree。第 1 层 3 个选择, 第 2 层 2 个, 第 3 层 1 个; 叶子 3! = 6 个。")
    doc.svg("13-backtracking/permutations_trace.svg",
            "图 2b: path 和 used[] 同步变化。push 时 used 变绿, pop 时 used 变回灰色。")
    doc.code(SRC["permute"])
    doc.p("Time O(n·n!): 叶子 n! 个, 节点总数约 e·n!, 每个叶子复制 O(n)。Space O(n): path + used + 递归栈。")
    doc.note("排列: 每层 <code>range(n)</code> + <code>used[]</code>; 做选择改两个状态 (path, used), 撤销也要改两个。")

    # ---------------------------------------------------------------- 3 Combination Sum
    doc.h2("3. Combination Sum: 可重复选 => 递归传 i, 不是 i+1")
    doc.p("题: <code>candidates = [2,3,5]</code>, <code>target = 6</code>, 每个数可以用任意多次, 返回和为 target 的所有组合 "
          "(顺序不同算同一个)。答案: <code>[[2,2,2],[3,3]]</code>。")
    doc.p("Brute force: 每个数枚举用 0 … target/c 次, 共 (6/2+1)·(6/3+1)·(6/5+1) = 4·3·2 = 24 种, 每种求和检查。"
          "浪费: 2 已经用了 4 次 (和 8 &gt; 6), 却还要继续枚举 3 和 5 的次数。")
    doc.p("关键观察: 这是 Subsets 加两处改动。① 同一个数能再选: 递归传 <code>i</code> "
          "(下一层仍可选 <code>candidates[i]</code>), 而不是 <code>i+1</code>; "
          "<code>start</code> 仍然保证不会出现 <code>[3,2]</code>。② 剪枝: 维护 <code>remain = target − sum(path)</code>, "
          "排序后一旦 <code>c &gt; remain</code>, 后面更大的数也不行, 直接 <code>break</code>。")
    doc.svg("13-backtracking/combination_sum_core.svg",
            "图 3a: decision tree。红色虚线 = 选了就超过 target, break。[2,2,2] 和 [3,3] 是绿色答案。")
    doc.svg("13-backtracking/combination_sum_trace.svg",
            "图 3b: 每步写出 remain = target − sum(path) 的具体数字。")
    doc.code(SRC["comb"])
    doc.p("Time: 树深最多 target/min(c) 层, 每层最多 n 个分支, 上界 O(n^(target/min)), 实际因为剪枝和 start 小得多。"
          "Space O(target/min): 递归深度。")
    doc.note("元素可重复用: 递归传 <code>i</code>; 每个数只能用一次: 传 <code>i+1</code>。有和的约束: sort + <code>c &gt; remain</code> 就 break。")

    # ---------------------------------------------------------------- 4 Combination Sum II
    doc.h2("4. Combination Sum II: 排序 + 同层去重")
    doc.p("题: <code>candidates = [1,2,2,3]</code>, <code>target = 5</code>, 每个数最多用一次, 候选里有重复值, "
          "答案不能有重复组合。答案: <code>[[1,2,2],[2,3]]</code>。")
    doc.p("Brute force: 枚举 2^4 = 16 个子集, 筛出和为 5 的, 再用 set 去重, O(n·2^n)。"
          "浪费: 选第一个 2 和选第二个 2 生成的是完全相同的子树, 白白展开了两遍, 最后还要靠 set 去重。")
    doc.p("关键观察: 先排序, 相同的值就挨在一起。在 <b>同一层</b> (同一个 <code>for</code> 循环里), "
          "如果 <code>candidates[i] == candidates[i-1]</code>, 说明这个值在这一层已经试过, 子树会一模一样, 跳过。"
          "但 <code>i == start</code> 时是 \"下一层的第一个\", 不是同一层, 必须允许 — 否则 <code>[1,2,2]</code> 出不来。"
          "所以条件是 <code>i &gt; start and candidates[i] == candidates[i-1]</code>。")
    doc.p("相比上一题改两行: 递归传 <code>i+1</code> (每个数只用一次); 加这一行去重。")
    doc.svg("13-backtracking/combination_sum_ii_core.svg",
            "图 4a: decision tree。\"同层重复\" 的红色分支是第二个 2 (i=2, start=1 或 0), 子树和第一个 2 一样, 剪掉。")
    doc.svg("13-backtracking/combination_sum_ii_trace.svg",
            "图 4b: 第 8 步 path=[1], i=2 > start=1 且 2 == 2, 剪枝; 第 3 步 path=[1,2,2] 允许, 因为 i=2 == start=2。")
    doc.code(SRC["comb2"])
    doc.p("Time O(2^n) 上界 (每个元素选 / 不选), 去重后实际更少, 不再需要 set。Space O(n)。")
    doc.note("有重复元素又要去重: 先 sort, 循环里加 <code>if i &gt; start and nums[i] == nums[i-1]: continue</code>。"
             "Subsets II 同样一行。")

    # ---------------------------------------------------------------- 5 Parentheses
    doc.h2("5. Generate Parentheses: 约束剪枝, 只生成合法前缀")
    doc.p("题: 给 <code>n</code>, 生成所有 n 对合法括号。<code>n = 2</code>: <code>[\"(())\", \"()()\"]</code>。")
    doc.p("Brute force: 2^(2n) 个由 <code>(</code> <code>)</code> 组成的串, 逐个检查合法, O(n·4^n)。"
          "n = 3 时 64 个串里只有 5 个合法。")
    doc.p("关键观察: 一个串合法 ⟺ 每个前缀里 <code>)</code> 的个数 ≤ <code>(</code> 的个数, 且最后各 n 个。"
          "所以不用事后检查, 每一步只加 \"不会破坏前缀\" 的字符: "
          "<code>(</code> 要 <code>open_ &lt; n</code>; <code>)</code> 要 <code>close &lt; open_</code>。"
          "两个 <code>if</code> 就是约束剪枝, 树上每个叶子都是答案, 没有一个废叶子。")
    doc.svg("13-backtracking/generate_parentheses_core.svg",
            "图 5a: n=2 的 decision tree。红色虚线 = 被两个条件挡住的选择, 写明哪个条件。")
    doc.svg("13-backtracking/generate_parentheses_trace.svg",
            "图 5b: 前 12 步。第 3、5 步 open_ = n 挡住 \"(\"; 根节点的 \")\" 要到第 21 步才被挡 (close=0 ≥ open_=0)。")
    doc.code(SRC["parens"])
    doc.p("Time O(4^n / √n) 量级 (Catalan 数个答案 × 每个 O(n) 的 join); Space O(n)。")
    doc.note("构造的串有 \"前缀合法性\": 把条件写成 <code>if</code> 挡在 push 之前, 不要先生成再检查。")

    # ---------------------------------------------------------------- 6 Letters
    doc.h2("6. Letter Combinations of a Phone Number: 每层候选不同")
    doc.p("题: <code>digits = \"23\"</code>, 每个数字对应几个字母, 返回所有字母组合。<code>\"2\"→abc</code>, <code>\"3\"→def</code>, 共 3×3 = 9 个。")
    doc.p("Brute force: 嵌套 for / <code>itertools.product</code>。问题是 <code>digits</code> 的长度是 input, 嵌套层数写不出来。"
          "这里没有任何东西可以剪枝 — 它是纯粹的笛卡尔积。")
    doc.p("关键观察: 相比前面几题, choices 不再是 \"从 start 往后\" 或 \"没用过的\", 而是由 <b>层数 idx</b> 决定: "
          "第 idx 层的候选 = <code>PHONE[digits[idx]]</code>, 和 path 里选了什么无关。"
          "所以不需要 start 也不需要 used, 只要一个 <code>idx</code>。backtracking 在这里只是把 \"层数不固定的嵌套 for\" 写成递归。")
    doc.svg("13-backtracking/letter_combinations_core.svg",
            "图 6a: decision tree。每层的分支数固定 (3 和 3), 没有被剪的分支; 9 个叶子 = 9 个答案。")
    doc.svg("13-backtracking/letter_combinations_trace.svg",
            "图 6b: 前 12 步。每个叶子: push → 收集 → pop。pop 到空 path 之后换第一个字母。")
    doc.code(SRC["letters"])
    doc.p("Time O(4^n · n): n = <code>len(digits)</code>, 每位最多 4 个字母, 叶子 ≤ 4^n 个, 每个 join 花 O(n)。Space O(n)。")
    doc.note("每一位有各自的候选集: 递归的参数是层数 <code>idx</code>, choices = 第 idx 层的候选; 层数固定 = 笛卡尔积。")

    # ---------------------------------------------------------------- 7 Word Search
    doc.h2("7. Word Search: grid 上的 backtracking, 原地标记再恢复")
    doc.p("题: 在字符 grid 里找 <code>word</code>, 路径是相邻格子 (上下左右), 同一个格子不能用两次。"
          "例: board = <code>ABA / BBD</code>, word = <code>ABAD</code> → True。")
    doc.p("Brute force: 从每个格子出发枚举所有长度为 L 的路径, 每步 4 个方向, O(R·C·4^L), 最后才比较字母。"
          "浪费有两处: 字母不对了还继续走; 每一步都允许走回头路。")
    doc.p("关键观察: 这是 Permutations 的 grid 版本。path = 走过的格子序列, \"同一格不能用两次\" 就是 <code>used[]</code>。"
          "grid 里可以直接把 board 当 used: 做选择时把 <code>board[r][c]</code> 改成 <code>\"#\"</code>, "
          "撤销时改回原字母。没有额外的 visited set。剪枝: 越界 / 字母不对 / 已经是 <code>#</code> 都在同一个 <code>if</code> 里返回 False。")
    doc.svg("13-backtracking/word_search_core.svg",
            "图 7a: 同一个 board 在 DFS 不同时刻的四个快照。# 的个数始终等于 len(path)。")
    doc.svg("13-backtracking/word_search_trace.svg",
            "图 7b: 全部 18 步。第 2-7 步走进 (1,0) 的死路再恢复; 第 9 步换方向, 第 14 步找到。右列是 board 的实时状态。")
    doc.code(SRC["wsearch"])
    doc.p("Time O(R·C·3^L): R·C 个起点, 每个起点最多 L 层, 除第一步外每步最多 3 个方向 (第 4 个是来的方向, 已经是 #)。"
          "Space O(L): 只有递归栈, 原地标记不需要 O(R·C) 的 visited。")
    doc.note("grid + 路径不能重复用: 原地改成 <code>#</code> 当 used, 递归之后改回。找到答案也要先恢复再 return。")

    # ---------------------------------------------------------------- 8 N-Queens
    doc.h2("8. N-Queens: 多个约束 => 多个 set")
    doc.p("题: n×n 棋盘放 n 个皇后, 互相不能同行、同列、同一条对角线。返回所有摆法。<code>n = 4</code> 有 2 个解。")
    doc.p("Brute force: 从 16 格里选 4 个, C(16,4) = 1820 种, 逐一检查。每行恰好放一个后是 4^4 = 256 种; "
          "再要求列不重复就是 4! = 24 种 (和 Permutations 一样); 对角线冲突则要靠剪枝在中途发现。")
    doc.p("关键观察: 一行放一个皇后, 所以 path[r] = 第 r 行的列, 层数 = 行数, 这就是 Permutations (列不能重复) 再加两个约束。"
          "同一条 <code>\\</code> 对角线上所有格子 <code>r − c</code> 相同; 同一条 <code>/</code> 对角线上 <code>r + c</code> 相同。"
          "所以用三个 set (<code>cols</code> / <code>diag</code> / <code>anti</code>) 记录已占用的值, 检查一个格子只要 3 次 O(1) 查询。"
          "做选择要往三个 set 各 add, 撤销要各 remove。")
    doc.svg("13-backtracking/n_queens_core.svg",
            "图 8a: 前两行已放 (0,1) 和 (1,3); 第 2 行四列里只有 c=0 通过三个 set 的检查。")
    doc.svg("13-backtracking/n_queens_trace.svg",
            "图 8b: 前 17 步。右列是三个 set 的实时内容; 红色虚线格子 = 被某个 set 挡住的列。")
    doc.code(SRC["nqueens"])
    doc.p("Time O(n!) 上界 (第 r 行至多还有 n−r 列可选)。实际远小: n = 4 只访问 %d 个节点 (4! = 24 个叶子位置); "
          "n = 8 访问 %d 个节点, 而 8! = 40320。Space O(n): path + 三个 set + 递归栈。" % (nq4_nodes, nq8_nodes))
    doc.note("放置类约束题: 把每条约束写成一个 set (key = 它禁止的东西), 检查 O(1); 撤销时所有 set 同步还原。")

    # ---------------------------------------------------------------- 识别信号
    doc.h2("9. 识别信号: 看到什么 → 试什么")
    rows = [
        ("要 <b>所有</b> 组合 / 排列 / 子集 / 路径 (输出是指数级)", "backtracking 模板: path + 做选择 / 递归 / 撤销",
         "下限是输出大小; 剪枝把节点数从 \"所有候选\" 降到 \"接近答案数\""),
        ("无序, 每个元素选或不选 (Subsets, Combinations)", "<code>range(start, n)</code>, 递归传 <code>i+1</code>",
         "n^n 或带重复 → 2^n, 没有 [1,2] / [2,1] 重复"),
        ("有序, 元素不可重复用 (Permutations)", "每层 <code>range(n)</code> + <code>used[]</code>",
         "n^n → n!"),
        ("元素可重复用, 要凑 target (Combination Sum)", "sort + 递归传 <code>i</code> + <code>remain</code>, <code>c &gt; remain</code> 就 break",
         "每个数的次数全枚举 → 超过 target 的分支全部不展开"),
        ("候选有重复值, 答案要去重 (Combination Sum II, Subsets II)", "sort + 同层 <code>i &gt; start and a[i] == a[i-1]</code> 跳过",
         "生成再用 set 去重 → 重复子树根本不展开"),
        ("构造的串 / 序列有前缀合法性 (括号)", "把条件写成 push 之前的 <code>if</code>",
         "2^(2n) 个串逐个检查 → Catalan(n) 个叶子, 无废叶子"),
        ("每一位有各自的候选集 (电话号码)", "递归参数 = 层数 <code>idx</code>, 无剪枝",
         "嵌套 for 层数不固定 → 递归; 复杂度 = 候选数的乘积"),
        ("grid 上找路径, 格子不能重复用 (Word Search)", "原地改成 <code>#</code>, 递归后改回; 不匹配立刻 return",
         "visited set O(R·C) → 原地 O(1) 额外空间; 4^L → 3^L"),
        ("放置问题, 约束可写成 \"某个值不能重复\" (N-Queens, Sudoku)", "每条约束一个 set, 做选择 add / 撤销 remove",
         "检查冲突 O(n) → O(1)"),
        ("只问 <b>能不能</b> / <b>有几个</b> / 最优值, 且子问题会重复", "不是 backtracking: 加 memo 变 DP",
         "指数 → 多项式 (状态数)"),
    ]
    tbl = ["<table><tr><th>特征</th><th>做法</th><th>complexity 从 X 降到 Y</th></tr>"]
    for a, b, c in rows:
        tbl.append("<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (a, b, c))
    tbl.append("</table>")
    doc.raw("".join(tbl))
    doc.note("题目要 \"列出所有\" → 画 decision tree, 问自己三件事: path 是什么, choices 是什么, 什么时候收集; "
             "再问: 哪些分支可以在 push 之前就判死刑?")

    doc.h2("以后再学")
    doc.p("Sudoku Solver (N-Queens 的 rows / cols / boxes 三个 set)、Palindrome Partitioning 和 Restore IP Addresses "
          "(choices = 下一段切多长)、bitmask 版 N-Queens、给 backtracking 加 memo 变成 DP。思路都已经在上面的模板里。")
    doc.write("docs/13-backtracking.html")


build_svgs()
for w in WARN:
    print("WARN", w)
build_doc()
