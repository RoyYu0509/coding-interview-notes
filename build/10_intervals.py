"""10 · Intervals 生成脚本。
运行: cd build && python3 -I 10_intervals.py
做三件事: (1) 文档里的每段代码都 exec 后和 brute force 随机对拍
(2) 用同一份逻辑模拟 trace, SVG 里的数字全部来自模拟结果 (3) 生成 HTML。
"""
import html
import os
import random
import sys
import heapq
import bisect
from math import inf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import doclib as d  # noqa: E402

SLUG = "10-intervals"
SVGDIR = os.path.join(d.ROOT, "docs", "svg", SLUG)
os.makedirs(SVGDIR, exist_ok=True)

# ====================================================================== 代码
CODE = {}

CODE["overlap"] = '''
def overlap(a, b):                    # a = [a_start, a_end], b = [b_start, b_end]
    return a[0] <= b[1] and b[0] <= a[1]
'''

CODE["merge"] = '''
def merge(intervals):
    intervals.sort(key=lambda x: x[0])        # 按 start 排序: 之后只和 res[-1] 比
    res = [list(intervals[0])]
    for s, e in intervals[1:]:
        if s <= res[-1][1]:                   # 重叠: s 没超过 "上一个合并结果" 的 end
            res[-1][1] = max(res[-1][1], e)   # 必须 max: cur 可能被整个包住
        else:
            res.append([s, e])                # 不重叠: 开一个新块
    return res
'''

CODE["insert"] = '''
def insert(intervals, new):                   # intervals 已排序且互不重叠
    res, i, n = [], 0, len(intervals)
    while i < n and intervals[i][1] < new[0]:     # 1. 左边: end 比 new 的 start 还小
        res.append(intervals[i])
        i += 1
    while i < n and intervals[i][0] <= new[1]:    # 2. 重叠: start 没超过 new 的 end
        new = [min(new[0], intervals[i][0]),      #    吞进 new, new 越吞越大
               max(new[1], intervals[i][1])]
        i += 1
    res.append(new)                               # new 此刻是最终形态, 放进去
    res.extend(intervals[i:])                     # 3. 右边: 原样接上
    return res
'''

CODE["erase"] = '''
def erase_overlap_intervals(intervals):
    intervals.sort(key=lambda x: x[1])        # 按 end 排序: 先看结束得最早的
    keep_end = -inf                           # 已保留的最后一个 interval 的 end
    removed = 0
    for s, e in intervals:
        if s >= keep_end:                     # 不重叠 (首尾相接 s == keep_end 也算不重叠)
            keep_end = e                      # 保留它, 它是目前 end 最小的选择
        else:
            removed += 1                      # 和已保留的重叠: 丢掉这个 (它的 end 更大)
    return removed
'''

CODE["arrows"] = '''
def find_min_arrow_shots(points):
    points.sort(key=lambda p: p[1])           # 按 end 排序
    arrows = 0
    arrow_x = -inf                            # 最近一支箭射在哪个 x
    for s, e in points:
        if s > arrow_x:                       # 箭射不到它 (首尾相接 s == arrow_x 能射到)
            arrows += 1
            arrow_x = e                       # 新箭射在它的 end: 尽量往右, 多串几个
    return arrows
'''

CODE["rooms1"] = '''
def can_attend_meetings(intervals):
    intervals.sort(key=lambda x: x[0])
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i - 1][1]:   # 下一个在上一个结束前就开始 (相接不算)
            return False
    return True
'''

CODE["rooms2_heap"] = '''
def min_meeting_rooms(intervals):
    intervals.sort(key=lambda x: x[0])        # 按 start 排序: 按开会顺序分配房间
    ends = []                                 # min-heap: 每个正在用的房间, 当前会议的 end
    for s, e in intervals:
        if ends and ends[0] <= s:             # 最早结束的房间已经空出来 (相接不算冲突)
            heapq.heappop(ends)               # 复用这个房间: 它的旧 end 出局
        heapq.heappush(ends, e)               # 复用或新开, 这场会议的 end 都要进 heap
    return len(ends)                          # heap 里有几个元素 = 同时用着几个房间
'''

CODE["rooms2_sweep"] = '''
def min_meeting_rooms(intervals):
    events = []
    for s, e in intervals:
        events.append((s, 1))                 # 开始: 同时进行的会议 +1
        events.append((e, -1))                # 结束: -1
    events.sort()                             # (t, -1) < (t, 1): 同一时刻先结束再开始
    cur = best = 0
    for t, delta in events:
        cur += delta                          # cur = 时刻 t 正在进行的会议数
        best = max(best, cur)
    return best
'''

CODE["intersect"] = '''
def interval_intersection(A, B):              # A, B 各自已排序, 各自内部不重叠
    i = j = 0
    res = []
    while i < len(A) and j < len(B):
        lo = max(A[i][0], B[j][0])            # 交集的左端 = 两个 start 里大的
        hi = min(A[i][1], B[j][1])            # 交集的右端 = 两个 end 里小的
        if lo <= hi:                          # 就是 overlap 条件
            res.append([lo, hi])
        if A[i][1] < B[j][1]:                 # end 小的那个不可能再和对方后面的相交
            i += 1
        else:
            j += 1
    return res
'''

CODE["calendar_brute"] = '''
class MyCalendar:
    def __init__(self):
        self.books = []
    def book(self, start, end):               # 半开区间 [start, end)
        for s, e in self.books:
            if start < e and s < end:         # overlap 条件 (半开区间: 用 < 不用 <=)
                return False
        self.books.append((start, end))
        return True
'''

CODE["calendar"] = '''
class MyCalendar:
    def __init__(self):
        self.starts = []                      # 已预订的 start, 保持有序
        self.ends = []                        # ends[i] 是 starts[i] 那场的 end
    def book(self, start, end):               # 半开区间 [start, end)
        i = bisect.bisect_left(self.starts, start)   # 新预订应插在第 i 个位置
        if i > 0 and self.ends[i - 1] > start:       # 前一场还没结束
            return False
        if i < len(self.starts) and self.starts[i] < end:   # 后一场在我结束前就开始
            return False
        self.starts.insert(i, start)
        self.ends.insert(i, end)
        return True
'''

NS = {"inf": inf, "heapq": heapq, "bisect": bisect}
FN = {}
for _k, _v in CODE.items():
    ns = dict(NS)
    exec(_v, ns)
    FN[_k] = ns


# ====================================================================== 测试 (和 brute force 对拍)
def rand_intervals(n, hi=30, minlen=1, maxlen=10):
    out = []
    for _ in range(n):
        s = random.randint(0, hi)
        out.append([s, s + random.randint(minlen, maxlen)])
    return out


def brute_merge(iv):
    iv = [list(x) for x in iv]
    changed = True
    while changed:
        changed = False
        for i in range(len(iv)):
            for j in range(i + 1, len(iv)):
                a, b = iv[i], iv[j]
                if a[0] <= b[1] and b[0] <= a[1]:
                    iv[i] = [min(a[0], b[0]), max(a[1], b[1])]
                    iv.pop(j)
                    changed = True
                    break
            if changed:
                break
    return sorted(iv)


def pts(iv):  # 把 interval 变成整点集合 (closed)
    return [set(range(s, e + 1)) for s, e in iv]


def brute_max_keep(iv):  # 最多保留几个互不重叠 (首尾相接允许), 枚举子集
    n = len(iv)
    best = 0
    for m in range(1 << n):
        ch = sorted([iv[i] for i in range(n) if m >> i & 1], key=lambda x: x[1])
        if all(ch[k][0] >= ch[k - 1][1] for k in range(1, len(ch))):
            best = max(best, len(ch))
    return best


def brute_arrows(iv):  # 枚举箭射在 0..40 的所有整数点, 最少几支覆盖所有气球
    n = len(iv)
    best = n
    xs = sorted({x for s, e in iv for x in (s, e)})
    for m in range(1 << len(xs)):
        ch = [xs[i] for i in range(len(xs)) if m >> i & 1]
        if len(ch) < best and all(any(s <= x <= e for x in ch) for s, e in iv):
            best = len(ch)
    return best


def brute_rooms(iv):
    best = 0
    for t in range(0, 60):
        best = max(best, sum(1 for s, e in iv if s <= t < e))
    return best


def run_tests():
    random.seed(10)
    for _ in range(400):
        iv = rand_intervals(random.randint(1, 7))
        assert FN["merge"]["merge"]([list(x) for x in iv]) == brute_merge(iv), iv
    for _ in range(300):
        # insert: 先造一份有序不重叠的
        base = FN["merge"]["merge"](rand_intervals(random.randint(0, 6)) or [[0, 0]])
        # merge 会合并首尾相接, 所以 base 里相邻块之间必有空隙
        new = rand_intervals(1)[0]
        got = FN["insert"]["insert"]([list(x) for x in base], list(new))
        want = brute_merge(base + [new])
        assert got == want, (base, new, got, want)
    for _ in range(300):
        iv = rand_intervals(random.randint(1, 8), hi=12, maxlen=5)
        got = FN["erase"]["erase_overlap_intervals"]([list(x) for x in iv])
        assert got == len(iv) - brute_max_keep(iv), iv
    for _ in range(200):
        iv = rand_intervals(random.randint(1, 8), hi=12, maxlen=5)
        got = FN["arrows"]["find_min_arrow_shots"]([list(x) for x in iv])
        assert got == brute_arrows(iv), iv
    for _ in range(400):
        iv = rand_intervals(random.randint(0, 7), hi=15, maxlen=6)
        got = FN["rooms1"]["can_attend_meetings"]([list(x) for x in iv])
        want = all(not (a[0] < b[1] and b[0] < a[1])
                   for i, a in enumerate(iv) for b in iv[i + 1:])
        assert got == want, iv
    for _ in range(400):
        iv = rand_intervals(random.randint(1, 8), hi=20, maxlen=8)
        w = brute_rooms(iv)
        assert FN["rooms2_heap"]["min_meeting_rooms"]([list(x) for x in iv]) == w, iv
        assert FN["rooms2_sweep"]["min_meeting_rooms"]([list(x) for x in iv]) == w, iv
    for _ in range(300):
        def mk():
            cuts = sorted(random.sample(range(0, 40), random.randint(0, 5) * 2))
            return [[cuts[i], cuts[i + 1]] for i in range(0, len(cuts), 2)]
        A, B = mk(), mk()
        want = []
        for a in A:
            for b in B:
                lo, hi = max(a[0], b[0]), min(a[1], b[1])
                if lo <= hi:
                    want.append([lo, hi])
        want.sort()
        assert FN["intersect"]["interval_intersection"](A, B) == want, (A, B)
    for _ in range(300):
        cals = [FN["calendar"]["MyCalendar"](), FN["calendar_brute"]["MyCalendar"]()]
        for _ in range(12):
            s = random.randint(0, 30)
            e = s + random.randint(1, 6)
            assert cals[0].book(s, e) == cals[1].book(s, e)
    print("all code tests passed")


run_tests()


# ====================================================================== SVG 工具
FONT = 'ui-sans-serif, system-ui, -apple-system, "PingFang SC", sans-serif'
INK, INK2 = "#0B0B0B", "#52514E"
ROLE = {  # fill, stroke, text
    "new": ("#E1F5EE", "#0F6E56", "#085041"),
    "gone": ("#FAECE7", "#993C1D", "#712B13"),
    "old": ("#F1EFE8", "#5F5E5A", "#444441"),
}
RING = "#EF9F27"
_fig_no = [0]


def esc(s):
    return html.escape(str(s), quote=False)


class Svg:
    def __init__(self, h, title, desc):
        _fig_no[0] += 1
        self.id = "f%d" % _fig_no[0]
        self.h, self.title, self.desc = h, title, desc
        self.o = []

    def add(self, s):
        self.o.append(s)

    def text(self, x, y, t, size=12, fill=INK2, anchor="start", weight=400):
        self.add('<text x="%s" y="%s" text-anchor="%s" dominant-baseline="central" '
                 'font-size="%d" font-weight="%d" fill="%s">%s</text>'
                 % (r(x), r(y), anchor, size, weight, fill, esc(t)))

    def rect(self, x, y, w, h, role=None, fill=None, stroke=None, sw=1, rx=4, dash=None):
        if role:
            fill, stroke, _ = ROLE[role]
        self.add('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" '
                 'stroke-width="%s"%s/>' % (r(x), r(y), r(w), r(h), rx, fill or "none",
                                            stroke or "none", sw,
                                            ' stroke-dasharray="%s"' % dash if dash else ""))

    def line(self, x1, y1, x2, y2, stroke="#B4B2A9", sw=1, dash=None, arrow=None):
        self.add('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s%s/>'
                 % (r(x1), r(y1), r(x2), r(y2), stroke, sw,
                    ' stroke-dasharray="%s"' % dash if dash else "",
                    ' marker-end="url(#%s-%s)"' % (self.id, arrow) if arrow else ""))

    def path(self, dstr, stroke=INK2, sw=1.5, dash=None, arrow=None):
        self.add('<path d="%s" fill="none" stroke="%s" stroke-width="%s"%s%s/>'
                 % (dstr, stroke, sw, ' stroke-dasharray="%s"' % dash if dash else "",
                    ' marker-end="url(#%s-%s)"' % (self.id, arrow) if arrow else ""))

    def circle(self, cx, cy, rad, role=None, fill=None, stroke=None, sw=1, dash=None):
        if role:
            fill, stroke, _ = ROLE[role]
        self.add('<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>'
                 % (r(cx), r(cy), rad, fill or "none", stroke or "none", sw,
                    ' stroke-dasharray="%s"' % dash if dash else ""))

    def dash_sep(self, y, x1=40, x2=640):
        self.line(x1, y, x2, y, "#B4B2A9", 0.8, "4 4")

    def out(self):
        defs = ('<defs>'
                '<marker id="%(i)s-g" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
                '<path d="M2 1L8 5L2 9" fill="none" stroke="#52514E" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>'
                '<marker id="%(i)s-r" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
                '<path d="M2 1L8 5L2 9" fill="none" stroke="#D85A30" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>'
                '<marker id="%(i)s-a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
                '<path d="M2 1L8 5L2 9" fill="none" stroke="#C07A0A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>'
                '<marker id="%(i)s-n" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
                '<path d="M2 1L8 5L2 9" fill="none" stroke="#0F6E56" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>'
                '</defs>' % {"i": self.id})
        return ('<svg width="100%%" viewBox="0 0 680 %d" role="img" xmlns="http://www.w3.org/2000/svg" '
                'font-family=\'%s\'><title>%s</title><desc>%s</desc>%s\n%s\n</svg>\n'
                % (self.h, FONT.replace('"', "&quot;"), esc(self.title), esc(self.desc), defs,
                   "\n".join(self.o)))

    def save(self, name):
        with open(os.path.join(SVGDIR, name), "w", encoding="utf-8") as f:
            f.write(self.out())


def r(v):
    return ("%.1f" % v).rstrip("0").rstrip(".")


class TL:
    """时间轴: 把 t 映射到 x。"""

    def __init__(self, x0, x1, lo, hi):
        self.x0, self.x1, self.lo, self.hi = x0, x1, lo, hi

    def x(self, t):
        return self.x0 + (t - self.lo) * (self.x1 - self.x0) / (self.hi - self.lo)


def axis(sv, tl, y, every=2, ticks=True, labels_below=True):
    """画时间轴: 基线 + 每个整数一条刻度 + 每 every 个标数字。"""
    sv.line(tl.x0, y, tl.x1, y, "#898781", 1)
    t = tl.lo
    while t <= tl.hi:
        big = (t - tl.lo) % every == 0
        sv.line(tl.x(t), y, tl.x(t), y + (6 if big else 3), "#898781", 1)
        if big:
            sv.text(tl.x(t), y + 15 if labels_below else y - 12, t, 12, INK2, "middle")
        t += 1


def grid(sv, tl, y0, y1, every=2):
    t = tl.lo
    while t <= tl.hi:
        if (t - tl.lo) % every == 0:
            sv.line(tl.x(t), y0, tl.x(t), y1, "#ECEAE2", 1)
        t += 1


def lab_w(lab):
    """12px 500 字重下标签的大致宽度 (逗号比数字窄)"""
    return sum(12 if ord(c) > 255 else (3.6 if c in ",. " else 6.8) for c in lab)


def bar(sv, tl, y, s, e, role="old", label=None, h=22, ring=False, dash=False, sw=1, text=True,
        label_fill=None):
    x0, x1 = tl.x(s), tl.x(e)
    if x1 - x0 < 2:  # 零长度 (点): 画成竖线
        sv.rect(x0 - 2, y, 4, h, role, rx=1, dash="3 2" if dash else None)
    else:
        sv.rect(x0, y, x1 - x0, h, role, sw=sw, dash="4 3" if dash else None)
    if ring:
        sv.rect(min(x0, x1 - 2) - 3, y - 3, max(x1 - x0, 4) + 6, h + 6, fill="none",
                stroke=RING, sw=2.5, rx=6)
    if text:
        lab = "%s,%s" % (s, e) if label is None else label
        if lab:
            need = lab_w(lab) + 6
            if x1 - x0 >= need:
                sv.text((x0 + x1) / 2, y + h / 2, lab, 12, label_fill or ROLE[role][2], "middle", 500)
            else:  # 横条太短: 标签放到右边
                sv.text(max(x1, x0 + 4) + 5, y + h / 2, lab, 12, ROLE[role][2], "start", 500)


def legend(sv, y, items, x=40):
    """items: (role|'ring'|'line', 文字)"""
    for kind, txt in items:
        if kind == "ring":
            sv.rect(x, y - 7, 16, 14, fill="#F1EFE8", stroke=RING, sw=2.5, rx=4)
        elif kind == "amberline":
            sv.line(x + 8, y - 8, x + 8, y + 8, "#C07A0A", 2, "4 3")
        else:
            sv.rect(x, y - 7, 16, 14, kind, sw=1, rx=3)
        sv.text(x + 22, y, txt, 12, INK2)
        x += 22 + 6.3 * sum(2 if ord(c) > 255 else 1 for c in txt) + 18
    return x


def head(sv, lines, y=18):
    for ln in lines:
        sv.text(40, y, ln, 12, INK2)
        y += 20
    return y


def foot(sv, y, answer, leg):
    sv.dash_sep(y)
    sv.text(40, y + 22, answer, 14, INK, "start", 500)
    legend(sv, y + 50, leg)
    return y + 66


# --------- 通用 trace: 一行一步, 列顺序固定: 当前输入 | 时间轴(状态) | 计算
def trace(name, title, desc, headlines, tl, rows, answer, leg, axis_every=2, rx=458,
          mid_title="时间轴 (横条 = interval)", right_title="计算", left_title="当前输入",
          vline_names=None):
    """rows[i] = dict(card=[(text,size,weight)...], lanes=[(label,[bars])], right=[(text,kind)],
    vlines=[(t,label)], sep=True)。bars: (s,e,role,label,opts)。"""
    # 先算每行高度
    LANE = 30
    heights = []
    for rw in rows:
        top = 22 if rw.get("vlines") else 10
        h = max(top + len(rw["lanes"]) * LANE + 6, 12 + len(rw["right"]) * 19 + 6, 70)
        heights.append((top, h))
    y0 = 20 * len(headlines) + 34  # 列标题所在 y
    H = int(y0 + 52 + sum(h for _, h in heights) + 90)
    sv = Svg(H, title, desc)
    head(sv, headlines)
    sv.text(40, y0, left_title, 12, INK2)
    sv.text(tl.x0, y0, mid_title, 12, INK2)
    sv.text(rx, y0, right_title, 12, INK2)
    axis(sv, tl, y0 + 28, axis_every, labels_below=False)
    sv.dash_sep(y0 + 36)
    y = y0 + 44
    for rw, (top, h) in zip(rows, heights):
        grid(sv, tl, y, y + h - 6, axis_every)
        # 左: 输入卡
        card = rw["card"]
        ch = 12 + 17 * len(card)
        sv.rect(40, y + (h - 6 - ch) / 2, 66, ch, rw.get("card_role", "new"), sw=0.8)
        cy = y + (h - 6 - ch) / 2 + 6 + 8.5
        for t, size, wt in card:
            sv.text(73, cy, t, size, ROLE[rw.get("card_role", "new")][2], "middle", wt)
            cy += 17
        # 中: vlines 先画 (在 bar 下面), 再画 lanes
        for vl in rw.get("vlines", []):
            t, lab = vl[0], vl[1]
            col = vl[2] if len(vl) > 2 else "#C07A0A"
            sv.line(tl.x(t), y + top - 8, tl.x(t), y + h - 8, col, 2, "4 3")
            if lab:
                sv.text(tl.x(t), y + 6, lab, 12, "#8A5200", "middle", 500)
        for li, (lab, bars) in enumerate(rw["lanes"]):
            ly = y + top + li * LANE
            sv.text(tl.x0 - 8, ly + 11, lab, 12, INK2, "end")
            for b in bars:
                s, e, role, label = b[:4]
                opts = b[4] if len(b) > 4 else {}
                # 横条太短、标签要放到右边时, 若会压到同一行的下一块, 就不画标签 (位置和前面几步一致)
                lab_ = "%s,%s" % (s, e) if label is None else label
                if lab_ and not opts.get("text") is False:
                    need_ = lab_w(lab_) + 6
                    if tl.x(e) - tl.x(s) < need_:
                        lx0, lx1 = max(tl.x(e), tl.x(s) + 4) + 5, max(tl.x(e), tl.x(s) + 4) + 5 + need_ - 6
                        if any(o is not b and tl.x(o[0]) < lx1 and tl.x(o[1]) > lx0 for o in bars):
                            label = ""
                bar(sv, tl, ly, s, e, role, label, **opts)
        # 右: 计算
        ry = y + 12
        for t, kind in rw["right"]:
            if kind == "sub":
                sv.text(rx, ry, t, 12, INK2)
            elif kind == "ok":
                sv.text(rx, ry, t, 14, ROLE["new"][2], "start", 500)
            elif kind == "bad":
                sv.text(rx, ry, t, 14, ROLE["gone"][2], "start", 500)
            else:
                sv.text(rx, ry, t, 14, INK, "start", 500)
            ry += 19
        y += h
        sv.dash_sep(y - 3)
    axis(sv, tl, y + 6, axis_every)
    foot(sv, y + 30, answer, leg)
    sv.save(name)
    return sv


def card_of(s, e=None, extra=()):
    c = [("[%s,%s]" % (s, e) if e is not None else s, 14, 500)]
    c += [(t, 12, 400) for t in extra]
    return c


# ====================================================================== 第 0 节图
def fig_overlap_core():
    tl = TL(150, 440, 0, 10)
    ov = FN["overlap"]["overlap"]
    cases = [("部分重叠", [1, 5], [3, 8]), ("包含", [1, 9], [3, 5]),
             ("首尾相接", [1, 4], [4, 8]), ("不重叠", [1, 3], [5, 8])]
    rows = []
    for nm, a, b in cases:
        lo, hi = max(a[0], b[0]), min(a[1], b[1])
        c1, c2 = a[0] <= b[1], b[0] <= a[1]
        assert ov(a, b) == (c1 and c2) == (lo <= hi)
        third = ([(lo, hi, "new", "%s,%s" % (lo, hi) if hi > lo else "", {})] if lo <= hi
                 else [(hi, lo, "gone", "空隙", {"dash": True})])
        rows.append(dict(
            card=[(nm, 14, 500)],
            card_role="new" if ov(a, b) else "gone",
            lanes=[("a", [(a[0], a[1], "old", None, {})]),
                   ("b", [(b[0], b[1], "old", None, {})]),
                   ("交集" if lo <= hi else "空隙", third)],
            right=[("a.start ≤ b.end:  %d ≤ %d  %s" % (a[0], b[1], "✓" if c1 else "✗"), "sub"),
                   ("b.start ≤ a.end:  %d ≤ %d  %s" % (b[0], a[1], "✓" if c2 else "✗"), "sub"),
                   ("→ 重叠" if ov(a, b) else "→ 不重叠", "ok" if ov(a, b) else "bad")]))
    trace("overlap_core.svg", "两个 interval 重叠的条件",
          "四种位置关系: 部分重叠、包含、首尾相接、不重叠, 逐个代入 a.start <= b.end and b.start <= a.end",
          ["不重叠只有两种: a 整个在 b 左边 (a.end < b.start), 或 a 整个在 b 右边 (b.end < a.start)",
           "两种都不是 = 重叠: a.start ≤ b.end 且 b.start ≤ a.end · 闭区间, 首尾相接也算重叠"],
          tl, rows,
          "overlap(a, b) = a.start ≤ b.end and b.start ≤ a.end",
          [("old", "a, b"), ("new", "交集 (共有的一段)"), ("gone", "空隙")],
          left_title="情况", mid_title="时间轴", right_title="代入")


def fig_sort_core():
    tl = TL(150, 440, 0, 20)
    res0 = [[1, 3], [5, 8], [10, 14]]

    def row(cur):
        s, e = cur
        last = res0[-1]
        if s <= last[1]:
            merged = [last[0], max(last[1], e)]
            res = res0[:-1] + [merged]
            lanes = [("res", [(a, b, "old", None, {}) for a, b in res0[:-1]] +
                      [(merged[0], merged[1], "new", None, {"ring": True})]),
                     ("cur", [(s, e, "gone", None, {})])]
            right = [("s = %d ≤ res[-1].end = %d" % (s, last[1]), "sub"),
                     ("→ 重叠, 合并成 [%d,%d]" % tuple(merged), "ok"),
                     ("end = max(%d, %d) = %d" % (last[1], e, merged[1]), "sub")]
            return dict(card=card_of(s, e, ["cur"]), card_role="gone", lanes=lanes, right=right,
                        vlines=[(last[1], "res[-1].end=%d" % last[1])])
        res = res0 + [[s, e]]
        lanes = [("res", [(a, b, "old", None, {}) for a, b in res0[:-1]] +
                  [(last[0], last[1], "old", None, {"ring": True}), (s, e, "new", None, {})]),
                 ("cur", [(s, e, "new", None, {})])]
        right = [("s = %d > res[-1].end = %d" % (s, last[1]), "sub"),
                 ("→ 不重叠, 开新块", "ok"),
                 ("前面的 end = %d, %d 更小" % (res0[0][1], res0[1][1]), "sub"),
                 ("→ 更不可能重叠", "sub")]
        return dict(card=card_of(s, e, ["cur"]), card_role="new", lanes=lanes, right=right,
                    vlines=[(last[1], "res[-1].end=%d" % last[1])])

    trace("sort_core.svg", "为什么排序后只和 res[-1] 比",
          "res 里的块已排好且互不重叠, cur.start 不小于之前所有 start, 所以只需比较 res[-1].end",
          ["已按 start 排序 · res = [1,3] [5,8] [10,14] 是处理完的结果: 互不重叠, 从左到右",
           "res[-1].end = 14 是 res 里最大的 end · cur 可能出现的两种情况:"],
          tl, [row([12, 17]), row([15, 18])],
          "不用和 res 里每一块比: 比 res[-1] 一次就够 → O(n²) 次比较降到 n - 1 次",
          [("old", "res 里已有的块"), ("new", "新块 / 合并后"), ("gone", "被吞掉的 cur"),
           ("ring", "res[-1]")],
          left_title="当前输入", right_title="判断")


fig_overlap_core()
fig_sort_core()


# ====================================================================== 1. Merge Intervals
def fig_merge_core():
    tl = TL(150, 440, 0, 12)
    rows = []
    # 1 部分重叠
    rows.append(dict(
        card=[("重叠", 14, 500), ("end 变大", 12, 400)], card_role="new",
        lanes=[("res[-1]", [(1, 3, "old", None, {"ring": True})]),
               ("cur", [(2, 6, "gone", None, {})]),
               ("合并后", [(1, 6, "new", None, {})])],
        right=[("s = 2 ≤ end = 3: 重叠", "sub"),
               ("end = max(3, 6) = 6", "ok"), ("→ res[-1] = [1,6]", "sub")]))
    # 2 被包住
    rows.append(dict(
        card=[("被包住", 14, 500), ("end 不变", 12, 400)], card_role="new",
        lanes=[("res[-1]", [(1, 10, "old", None, {"ring": True})]),
               ("cur", [(2, 3, "gone", None, {})]),
               ("max", [(1, 10, "new", None, {})]),
               ("只写 e", [(1, 3, "gone", None, {"dash": True})])],
        right=[("s = 2 ≤ end = 10: 重叠", "sub"),
               ("end = max(10, 3) = 10", "ok"),
               ("若写成 end = e = 3:", "sub"), ("[1,10] 被缩成 [1,3], 错", "bad")]))
    # 3 不重叠
    rows.append(dict(
        card=[("不重叠", 14, 500), ("开新块", 12, 400)], card_role="new",
        lanes=[("res[-1]", [(1, 3, "old", None, {"ring": True})]),
               ("cur", [(8, 11, "new", None, {})]),
               ("res", [(1, 3, "old", None, {}), (8, 11, "new", None, {})])],
        right=[("s = 8 > end = 3: 不重叠", "sub"),
               ("res.append([8, 11])", "ok"), ("res[-1] 不动", "sub")]))
    trace("merge_core.svg", "Merge Intervals 的三种情况",
          "cur 与 res[-1] 的三种关系: 部分重叠取 max、被包住 end 不变、不重叠 append",
          ["cur = [s, e] · 每一步只比较 s 和 res[-1].end",
           "重叠时一定用 max(res[-1].end, e): cur 可能整个被 res[-1] 包住"],
          tl, rows,
          "s ≤ res[-1].end → end = max(res[-1].end, e) · 否则 res.append([s, e])",
          [("old", "res[-1]"), ("gone", "被吞掉的 cur / 错误结果"), ("new", "合并后 / 新块"),
           ("ring", "比较对象")],
          left_title="情况", mid_title="时间轴", right_title="计算")


def sim_merge(iv):
    iv = sorted([list(x) for x in iv], key=lambda x: x[0])
    res = [list(iv[0])]
    steps = [dict(cur=list(iv[0]), kind="init", res=[list(x) for x in res], before=None)]
    for s, e in iv[1:]:
        last_end = res[-1][1]
        if s <= last_end:
            new_end = max(last_end, e)
            res[-1][1] = new_end
            steps.append(dict(cur=[s, e], kind="merge", res=[list(x) for x in res],
                              last_end=last_end, new_end=new_end))
        else:
            res.append([s, e])
            steps.append(dict(cur=[s, e], kind="new", res=[list(x) for x in res],
                              last_end=last_end))
    return iv, res, steps


def fig_merge_trace():
    raw = [[8, 10], [1, 3], [15, 18], [2, 6], [17, 20]]
    iv, res, steps = sim_merge(raw)
    assert res == FN["merge"]["merge"]([list(x) for x in raw])
    tl = TL(150, 440, 0, 20)
    rows = []
    for st in steps:
        s, e = st["cur"]
        rs = st["res"]
        if st["kind"] == "init":
            lanes = [("res", [(rs[0][0], rs[0][1], "new", None, {})]),
                     ("cur", [(s, e, "new", None, {})])]
            right = [("第一个: 直接放进 res", "ok"), ("res = [[%d,%d]]" % (s, e), "sub")]
            rows.append(dict(card=card_of(s, e, ["cur"]), card_role="new", lanes=lanes, right=right))
        elif st["kind"] == "merge":
            lanes = [("res", [(a, b, "old", None, {}) for a, b in rs[:-1]] +
                      [(rs[-1][0], rs[-1][1], "new", None, {"ring": True})]),
                     ("cur", [(s, e, "gone", None, {})])]
            right = [("s = %d ≤ res[-1].end = %d" % (s, st["last_end"]), "sub"),
                     ("end = max(%d, %d) = %d" % (st["last_end"], e, st["new_end"]), "ok"),
                     ("res[-1] = [%d,%d]" % tuple(rs[-1]), "sub")]
            rows.append(dict(card=card_of(s, e, ["cur"]), card_role="gone", lanes=lanes, right=right,
                             vlines=[(st["last_end"], "end=%d" % st["last_end"])]))
        else:
            lanes = [("res", [(a, b, "old", None, {}) for a, b in rs[:-1]] +
                      [(rs[-1][0], rs[-1][1], "new", None, {})]),
                     ("cur", [(s, e, "new", None, {})])]
            right = [("s = %d > res[-1].end = %d" % (s, st["last_end"]), "sub"),
                     ("res.append([%d, %d])" % (s, e), "ok"),
                     ("res 里现在 %d 块" % len(rs), "sub")]
            rows.append(dict(card=card_of(s, e, ["cur"]), card_role="new", lanes=lanes, right=right,
                             vlines=[(st["last_end"], "end=%d" % st["last_end"])]))
    trace("merge_trace.svg", "Merge Intervals 运行流程",
          "输入先按 start 排序, 逐个 interval 和 res[-1] 比较, 合并或新开一块",
          ["输入 [8,10] [1,3] [15,18] [2,6] [17,20] → 按 start 排序: " +
           " ".join("[%d,%d]" % tuple(x) for x in iv),
           "每一步: cur 和 res[-1].end 比 → 合并 (改 end) 或 新开一块 (append)"],
          tl, rows,
          "res = " + " ".join("[%d,%d]" % tuple(x) for x in res) + " · 5 个 interval 合成 %d 块" % len(res),
          [("old", "res 里已有的块"), ("new", "新块 / 合并后的块"), ("gone", "被吞掉的 cur"),
           ("ring", "res[-1]")],
          left_title="当前输入")


fig_merge_core()
fig_merge_trace()


# ====================================================================== 2. Insert Interval
INS_IV = [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]]
INS_NEW = [4, 8]


def sim_insert(intervals, new):
    res, i, n = [], 0, len(intervals)
    steps = []
    new = list(new)
    while i < n and intervals[i][1] < new[0]:
        res.append(list(intervals[i]))
        steps.append(dict(item=list(intervals[i]), phase="left", new=list(new), res=[list(x) for x in res],
                          why=(intervals[i][1], new[0])))
        i += 1
    while i < n and intervals[i][0] <= new[1]:
        old_new = list(new)
        new = [min(new[0], intervals[i][0]), max(new[1], intervals[i][1])]
        steps.append(dict(item=list(intervals[i]), phase="merge", new=list(new), old_new=old_new,
                          res=[list(x) for x in res], why=(intervals[i][0], old_new[1]),
                          prev_fail=(intervals[i][1], old_new[0])))
        i += 1
    res.append(list(new))
    rest = [list(x) for x in intervals[i:]]
    res.extend(rest)
    steps.append(dict(item=rest[0] if rest else None, phase="right", new=list(new), res=[list(x) for x in res],
                      why=(rest[0][0], new[1]) if rest else None))
    return res, steps


def fig_insert_core():
    tl = TL(150, 440, 0, 18)
    new = INS_NEW
    items = []
    for a, b in INS_IV:
        if b < new[0]:
            items.append((a, b, "old", None, {}))
        elif a <= new[1]:
            items.append((a, b, "gone", None, {}))
        else:
            items.append((a, b, "old", None, {}))
    zones = [(0, 3, "old", "① 左边", {}), (3, 10, "gone", "② 重叠", {}), (10, 18, "old", "③ 右边", {})]
    res, _ = sim_insert(INS_IV, INS_NEW)
    assert res == [[1, 2], [3, 10], [12, 16]]
    row = dict(
        card=[("new", 14, 500), ("[4,8]", 12, 400)], card_role="new",
        lanes=[("intervals", items), ("new", [(4, 8, "new", None, {"ring": True})]),
               ("三段", zones), ("结果", [(1, 2, "old", None, {}), (3, 10, "new", None, {}),
                                        (12, 16, "old", None, {})])],
        right=[("① end < new.start = 4", "sub"), ("   [1,2]: 2 < 4  原样放进 res", "sub"),
               ("② start ≤ new.end = 8", "sub"), ("   [3,5] [6,7] [8,10] 吞进 new", "sub"),
               ("   new = [3, 10]", "ok"),
               ("③ 剩下的 [12,16] 原样接上", "sub")],
        vlines=[(4, "start=4"), (8, "end=8")])
    trace("insert_core.svg", "Insert Interval 的三段",
          "已排序的 intervals 相对 new 分成左边、重叠、右边三段, 重叠的全部吞进 new",
          ["intervals 已排序且互不重叠 · new = [4,8]",
           "按 intervals 的顺序扫一遍, 只会经过三段, 每段一个 while (或一个 if)"],
          tl, [row],
          "res = [1,2] [3,10] [12,16] · ① 原样放 → ② 吞进 new, 放 new → ③ 原样放",
          [("old", "原样放进 res"), ("gone", "被 new 吞掉"), ("new", "new / 合并结果"),
           ("ring", "new")],
          left_title="输入", mid_title="时间轴", right_title="三段的条件")


def fig_insert_trace():
    res, steps = sim_insert(INS_IV, INS_NEW)
    tl = TL(150, 440, 0, 18)
    rows = []
    for st in steps:
        if st["phase"] == "left":
            a, b = st["item"]
            rows.append(dict(
                card=card_of(a, b, ["① 左边"]), card_role="new",
                lanes=[("item", [(a, b, "new", None, {})]),
                       ("new", [(INS_NEW[0], INS_NEW[1], "old", None, {"ring": True})]),
                       ("res", [(x, y, "new" if [x, y] == [a, b] else "old", None, {}) for x, y in st["res"]])],
                right=[("end = %d < new.start = %d" % st["why"], "sub"),
                       ("→ 完全在左边", "ok"), ("res.append([%d,%d])" % (a, b), "sub")]))
        elif st["phase"] == "merge":
            a, b = st["item"]
            on, nn = st["old_new"], st["new"]
            rows.append(dict(
                card=card_of(a, b, ["② 重叠"]), card_role="gone",
                lanes=[("item", [(a, b, "gone", None, {})]),
                       ("new", [(nn[0], nn[1], "new", None, {"ring": True})]),
                       ("res", [(x, y, "old", None, {}) for x, y in st["res"]])],
                right=[("start = %d ≤ new.end = %d" % st["why"], "sub"),
                       ("new = [min(%d,%d), max(%d,%d)]" % (on[0], a, on[1], b), "sub"),
                       ("    = [%d, %d]" % tuple(nn), "ok")]))
        else:
            a, b = st["item"]
            rows.append(dict(
                card=card_of(a, b, ["③ 右边"]), card_role="old",
                lanes=[("item", [(a, b, "old", None, {})]),
                       ("new", [(st["new"][0], st["new"][1], "new", None, {})]),
                       ("res", [(x, y, "new" if [x, y] == st["new"] else "old", None, {}) for x, y in st["res"]])],
                right=[("start = %d > new.end = %d" % st["why"], "sub"),
                       ("→ 重叠结束: 放 new", "ok"),
                       ("res.extend([[12,16]])", "sub")]))
    trace("insert_trace.svg", "Insert Interval 运行流程",
          "new=[4,8] 插入 5 个已排序 interval: 一个在左边, 三个被吞进 new, 一个在右边",
          ["intervals = [1,2] [3,5] [6,7] [8,10] [12,16] · new = [4,8]",
           "每步看一个 intervals[i]: 左边 → 放进 res · 重叠 → 吞进 new · 右边 → 先放 new, 再接上剩下的"],
          tl, rows,
          "res = " + " ".join("[%d,%d]" % tuple(x) for x in res),
          [("old", "原样的块"), ("new", "进 res 的块 / new"), ("gone", "被 new 吞掉"), ("ring", "new")],
          left_title="当前输入")


fig_insert_core()
fig_insert_trace()


# ====================================================================== 3. Non-overlapping Intervals
ER_RAW = [[1, 4], [2, 3], [3, 5], [4, 6], [1, 2]]


def sim_erase(iv):
    iv = sorted([list(x) for x in iv], key=lambda x: x[1])
    keep_end, removed, kept = -inf, 0, []
    steps = []
    for s, e in iv:
        before = keep_end
        if s >= keep_end:
            keep_end = e
            kept.append([s, e])
            steps.append(dict(cur=[s, e], ok=True, before=before, keep_end=keep_end, removed=removed,
                              kept=[list(x) for x in kept]))
        else:
            removed += 1
            steps.append(dict(cur=[s, e], ok=False, before=before, keep_end=keep_end, removed=removed,
                              kept=[list(x) for x in kept]))
    return iv, removed, steps


def fig_erase_core():
    tl = TL(150, 440, 0, 12)
    A, B, C, D = [1, 11], [2, 4], [4, 6], [6, 8]
    names = {"A": A, "B": B, "C": C, "D": D}

    def lanes(kept):
        return [(n, [(v[0], v[1], "new" if n in kept else "gone", None, {})]) for n, v in names.items()]
    rows = [
        dict(card=[("按 start", 14, 500), ("排序", 12, 400)], card_role="gone",
             lanes=lanes("A"),
             right=[("先选 start 最小的 A", "sub"), ("A 的 end = 11 挡住了 B C D", "sub"),
                    ("保留 1 个, 删 3 个", "bad")]),
        dict(card=[("按 end", 14, 500), ("排序", 12, 400)], card_role="new",
             lanes=lanes("BCD"),
             right=[("先选 end 最小的 B (4)", "sub"), ("C 从 4 开始, D 从 6 开始", "sub"),
                    ("保留 3 个, 删 1 个", "ok")]),
    ]
    trace("erase_core.svg", "为什么按 end 排序",
          "同一组 interval, 按 start 排会先选中长的 A 导致删 3 个, 按 end 排先选 B 只删 1 个",
          ["目标: 保留尽量多的互不重叠 interval (= 删最少) · A=[1,11] B=[2,4] C=[4,6] D=[6,8]",
           "贪心: 每次选 end 最小的 → 它占用的时间最短, 给后面留的空间最大 (start 小不代表占得少)"],
          tl, rows,
          "按 end 排序 → 保留 B C D, 删 A (首尾相接 4/4, 6/6 不算重叠)",
          [("new", "保留"), ("gone", "删掉")], axis_every=1,
          left_title="排序方式", mid_title="时间轴 (4 个 interval 各占一行)", right_title="结果")


def fig_erase_trace():
    iv, removed, steps = sim_erase(ER_RAW)
    assert removed == FN["erase"]["erase_overlap_intervals"]([list(x) for x in ER_RAW])
    tl = TL(150, 440, 0, 7)
    rows = []
    for st in steps:
        s, e = st["cur"]
        kb = st["before"]
        kb_s = "-inf" if kb == -inf else str(kb)
        lanes = [("cur", [(s, e, "new" if st["ok"] else "gone", None, {})]),
                 ("kept", [(a, b, "old", None, {}) for a, b in st["kept"][:-1]] +
                  ([(st["kept"][-1][0], st["kept"][-1][1], "new", None, {})] if st["ok"] and st["kept"] else
                   ([(st["kept"][-1][0], st["kept"][-1][1], "old", None, {})] if st["kept"] else [])))]
        if st["ok"]:
            right = [("s = %d ≥ keep_end = %s" % (s, kb_s), "sub"), ("→ 不重叠, 保留", "ok"),
                     ("keep_end = %d · removed = %d" % (st["keep_end"], st["removed"]), "sub")]
        else:
            right = [("s = %d < keep_end = %s" % (s, kb_s), "sub"), ("→ 重叠, 删掉它", "bad"),
                     ("removed = %d · keep_end = %d" % (st["removed"], st["keep_end"]), "sub")]
        vl = [(kb, "keep_end=%d" % kb)] if kb != -inf else []
        rows.append(dict(card=card_of(s, e, ["保留" if st["ok"] else "删掉"]),
                         card_role="new" if st["ok"] else "gone", lanes=lanes, right=right, vlines=vl))
    trace("erase_trace.svg", "Non-overlapping Intervals 运行流程",
          "按 end 排序后逐个比较 s 和 keep_end, 不小于就保留并更新 keep_end, 否则删掉",
          ["输入 " + " ".join("[%d,%d]" % tuple(x) for x in ER_RAW) + " → 按 end 排序: " +
           " ".join("[%d,%d]" % tuple(x) for x in iv),
           "每一步: s ≥ keep_end → 保留, keep_end = e · 否则 removed += 1"],
          tl, rows,
          "removed = %d · 保留 " % removed + " ".join("[%d,%d]" % tuple(x) for x in steps[-1]["kept"]),
          [("new", "保留"), ("gone", "删掉"), ("old", "之前保留的")], axis_every=1,
          left_title="当前输入")


fig_erase_core()
fig_erase_trace()


# ====================================================================== 4. Min Arrows
AR_RAW = [[10, 16], [2, 8], [1, 6], [15, 20], [7, 12]]


def sim_arrows(pts_):
    pts_ = sorted([list(x) for x in pts_], key=lambda p: p[1])
    arrows, ax = 0, -inf
    steps, xs = [], []
    for s, e in pts_:
        before = ax
        if s > ax:
            arrows += 1
            ax = e
            xs.append(e)
            steps.append(dict(cur=[s, e], new=True, before=before, ax=ax, arrows=arrows, xs=list(xs)))
        else:
            steps.append(dict(cur=[s, e], new=False, before=before, ax=ax, arrows=arrows, xs=list(xs)))
    return pts_, arrows, steps


def fig_arrows_core():
    tl = TL(150, 440, 0, 13)
    balloons = {"A": [1, 6], "B": [3, 8], "C": [5, 9], "D": [7, 12]}

    def lanes(x):
        return [(n, [(v[0], v[1], "gone" if v[0] <= x <= v[1] else "old", None, {})])
                for n, v in balloons.items()]
    rows = [
        dict(card=[("x = 3", 14, 500), ("A 的内部", 12, 400)], card_role="old", lanes=lanes(3),
             right=[("射中 A, B (3 在 [3,8] 里)", "sub"), ("没射中 C: 5 > 3", "sub"), ("射中 2 个", "bad")],
             vlines=[(3, "x=3", "#C07A0A")]),
        dict(card=[("x = 6", 14, 500), ("右移到 end", 12, 400)], card_role="new", lanes=lanes(6),
             right=[("射中 A, B, C", "sub"), ("A 是 end 最小的, 其他 end", "sub"),
                    ("都 ≥ 6, 之前射中的不会丢", "sub"), ("射中 3 个", "ok")],
             vlines=[(6, "x=6", "#C07A0A")]),
    ]
    trace("arrows_core.svg", "为什么箭射在 end 最小的 end 上",
          "把箭从 A 内部右移到 A.end: 之前射中的气球不会丢, 还可能多射中",
          ["气球 = 闭区间, 箭射在 x 处能射穿所有 start ≤ x ≤ end 的气球 · A 是 end 最小的",
           "任何射中 A 的箭 x ≤ A.end · 把 x 右移到 A.end: 其他气球的 end 都 ≥ A.end, 不会丢"],
          tl, rows,
          "所以先按 end 排序, 第一支箭一定射在 A.end · 后面 start ≤ A.end 的全被带走",
          [("gone", "被这支箭射穿"), ("old", "没射中")], axis_every=1,
          left_title="射法", mid_title="时间轴", right_title="结果")


def fig_arrows_trace():
    pts_, arrows, steps = sim_arrows(AR_RAW)
    assert arrows == FN["arrows"]["find_min_arrow_shots"]([list(x) for x in AR_RAW])
    tl = TL(150, 440, 0, 21)
    rows = []
    for st in steps:
        s, e = st["cur"]
        prev_b = "-inf" if st["before"] == -inf else str(st["before"])
        vl = [(x, "x=%d" % x if x == st["ax"] else "", "#C07A0A" if x == st["ax"] else "#B4B2A9")
              for x in st["xs"]]
        if st["new"]:
            right = [("s = %d > arrow_x = %s" % (s, prev_b), "sub"), ("→ 射不到, 新射一支", "ok"),
                     ("arrows = %d · arrow_x = %d" % (st["arrows"], st["ax"]), "sub")]
            lane = [("cur", [(s, e, "new", None, {})])]
            role = "new"
        else:
            right = [("s = %d ≤ arrow_x = %d" % (s, st["ax"]), "sub"), ("→ 已被这支箭射穿", "bad"),
                     ("arrows 不变 = %d" % st["arrows"], "sub")]
            lane = [("cur", [(s, e, "gone", None, {})])]
            role = "gone"
        rows.append(dict(card=card_of(s, e, ["新箭" if st["new"] else "已射穿"]), card_role=role,
                         lanes=lane, right=right, vlines=vl))
    trace("arrows_trace.svg", "Minimum Arrows 运行流程",
          "按 end 排序, arrow_x 记录最近一支箭的位置; s 超过 arrow_x 就新射一支, 射在这个气球的 end",
          ["输入 " + " ".join("[%d,%d]" % tuple(x) for x in AR_RAW) + " → 按 end 排序: " +
           " ".join("[%d,%d]" % tuple(x) for x in pts_),
           "每一步: s > arrow_x → arrows += 1, arrow_x = e · 否则这个气球已被射穿"],
          tl, rows,
          "arrows = %d · 箭射在 x = " % arrows + ", ".join(str(x) for x in steps[-1]["xs"]),
          [("new", "要新射一支的气球"), ("gone", "已被射穿的气球"), ("amberline", "当前这支箭 arrow_x"),
           ("old", "更早的箭")] if False else
          [("new", "要新射一支的气球"), ("gone", "已被射穿的气球"), ("amberline", "箭的位置 arrow_x")],
          left_title="当前输入", mid_title="时间轴 (虚线 = 箭)")


fig_arrows_core()
fig_arrows_trace()


# ====================================================================== 5. Meeting Rooms (能否全参加)
def fig_rooms1_core():
    tl = TL(150, 440, 0, 30)
    ex1 = [[0, 30], [5, 10], [15, 20]]
    ex2 = [[1, 3], [4, 6], [6, 9]]
    rows = []
    # 例 1: 有重叠
    rows.append(dict(
        card=[("有重叠", 14, 500), ("相邻暴露", 12, 400)],
        card_role="gone",
        lanes=[("1", [(0, 30, "gone", None, {})]), ("2", [(5, 10, "gone", None, {})]),
               ("3", [(15, 20, "old", None, {})])],
        right=[("[15,20] 和 [0,30] 也重叠,", "sub"), ("但不用比它: 相邻的 1 和 2", "sub"),
               ("5 < 30 已经重叠 → False", "bad")]))
    rows.append(dict(
        card=[("没重叠", 14, 500), ("首尾相接", 12, 400)], card_role="new",
        lanes=[("1", [(1, 3, "new", None, {})]), ("2", [(4, 6, "new", None, {})]),
               ("3", [(6, 9, "new", None, {})])],
        right=[("相邻都不重叠:", "sub"), ("4 ≥ 3, 6 ≥ 6", "sub"),
               ("→ 整条链从左到右排开", "ok"), ("→ 不可能有隔着的重叠", "sub")]))
    trace("rooms1_core.svg", "为什么只比较相邻的两个",
          "按 start 排序后, 如果所有相邻对都不重叠, 整条链首尾相接, 不可能有重叠",
          ["按 start 排序 · 相邻两个 intervals[i-1], intervals[i] 只看 intervals[i].start < intervals[i-1].end",
           "有重叠 → 总会在某个相邻对暴露 · 没有一个相邻对重叠 → 链条一路向右, 全部不重叠"],
          tl, rows,
          "排序 O(n log n) + 扫一遍 n - 1 对 · 相邻比较就够了",
          [("gone", "重叠的那对"), ("new", "首尾相接的链"), ("old", "不用再比")],
          axis_every=5, left_title="例子", mid_title="时间轴", right_title="结论")


def fig_rooms1_trace():
    raw = [[7, 10], [2, 4], [10, 13], [12, 15]]
    iv = sorted([list(x) for x in raw], key=lambda x: x[0])
    tl = TL(150, 440, 0, 16)
    rows = []
    verdict = True
    for i in range(1, len(iv)):
        a, b = iv[i - 1], iv[i]
        bad = b[0] < a[1]
        right = [("s = %d < prev.end = %d ?" % (b[0], a[1]), "sub")]
        if bad:
            right += [("%d < %d 成立 → 重叠" % (b[0], a[1]), "bad"), ("return False", "bad")]
        else:
            right += [("%d < %d 不成立" % (b[0], a[1]), "ok"),
                      ("相接也不算重叠" if b[0] == a[1] else "→ 继续看下一对", "sub")]
        rows.append(dict(
            card=card_of(b[0], b[1], ["i = %d" % i]), card_role="gone" if bad else "new",
            lanes=[("prev", [(a[0], a[1], "old", None, {"ring": True})]),
                   ("cur", [(b[0], b[1], "gone" if bad else "new", None, {})])],
            right=right, vlines=[(a[1], "prev.end=%d" % a[1])]))
        if bad:
            verdict = False
            break
    assert verdict == FN["rooms1"]["can_attend_meetings"]([list(x) for x in raw]) is False
    trace("rooms1_trace.svg", "Meeting Rooms 运行流程",
          "排序后逐个检查相邻对, 第三对发生重叠, 返回 False",
          ["输入 " + " ".join("[%d,%d]" % tuple(x) for x in raw) + " → 按 start 排序: " +
           " ".join("[%d,%d]" % tuple(x) for x in iv),
           "每一步比较 intervals[i].start 和 intervals[i-1].end (会议开始时间 < 上一场结束时间 → 冲突)"],
          tl, rows,
          "i = 3 时 12 < 13: 两场会议在 [12,13] 同时进行 → 不能全部参加 (False)",
          [("new", "cur 没冲突"), ("gone", "cur 冲突"), ("ring", "prev (比较对象)")],
          left_title="当前输入")


fig_rooms1_core()
fig_rooms1_trace()


# ====================================================================== 6. Meeting Rooms II
MR_RAW = [[0, 30], [5, 10], [15, 20], [10, 25], [22, 28]]


def fig_rooms2_core():
    tl = TL(150, 440, 0, 30)
    srt = sorted([list(x) for x in MR_RAW], key=lambda x: x[0])
    t = 17
    cut = [m for m in srt if m[0] <= t < m[1]]
    assert len(cut) == 3 and max(sum(1 for m in srt if m[0] <= u < m[1]) for u in range(31)) == 3
    lanes = [("%d" % (i + 1), [(m[0], m[1], "new" if m in cut else "old", None, {})])
             for i, m in enumerate(srt)]
    row = dict(card=[("答案", 14, 500), ("= 最大 cut", 12, 400)], card_role="new", lanes=lanes,
               right=[("竖线 t = 17 切到:", "sub"), ("[0,30] [10,25] [15,20]", "sub"),
                      ("3 场同时进行 → 要 3 间房", "ok"), ("t = 7 只切到 2 场", "sub"),
                      ("答案 = 所有 t 里最大的 cut", "sub")],
               vlines=[(17, "t=17"), (7, "t=7", "#B4B2A9")])
    trace("rooms2_core.svg", "房间数 = 同时进行的会议数的最大值",
          "一根竖线从左到右扫过时间轴, 它同时切到的横条数的最大值就是需要的房间数",
          ["5 场会议 [0,30] [5,10] [10,25] [15,20] [22,28] (已按 start 排序) · 每行一场",
           "任一时刻 t 正在进行的会议互相冲突, 必须各占一间房 → 房间数 ≥ 这个数 · 反过来取最大值就够用"],
          tl, [row],
          "两种算 '最大同时数' 的办法: min-heap 存各房间的 end · 或 扫描线 (start +1, end -1)",
          [("new", "t = 17 时正在进行"), ("old", "没被竖线切到")],
          axis_every=5, left_title="思路", mid_title="时间轴", right_title="竖线 t 切到几场")


def draw_heap(sv, cx, cy, arr, new_val=None, ring=True):
    """arr 是 heapq 的真实数组; 画成 tree, 堆顶加 ring, new_val 的节点画成绿色。"""
    pos = {0: (cx, cy), 1: (cx - 34, cy + 32), 2: (cx + 34, cy + 32),
           3: (cx - 51, cy + 64), 4: (cx - 17, cy + 64), 5: (cx + 17, cy + 64), 6: (cx + 51, cy + 64)}
    for i in range(1, len(arr)):
        px, py = pos[(i - 1) // 2]
        x, y = pos[i]
        sv.line(px, py + 14, x, y - 14, "#B4B2A9", 1)
    for i, v in enumerate(arr):
        x, y = pos[i]
        role = "new" if (new_val is not None and v == new_val) else "old"
        sv.circle(x, y, 14, role, sw=0.8)
        sv.text(x, y, v, 14, ROLE[role][2], "middle", 500)
    if arr and ring:
        sv.circle(cx, cy, 18, fill="none", stroke=RING, sw=2.5)


def sim_heap(iv):
    iv = sorted([list(x) for x in iv], key=lambda x: x[0])
    ends = []
    steps = []
    for s, e in iv:
        top = ends[0] if ends else None
        popped = None
        if ends and ends[0] <= s:
            popped = heapq.heappop(ends)
        after_pop = list(ends)
        heapq.heappush(ends, e)
        steps.append(dict(cur=[s, e], top=top, popped=popped, after_pop=after_pop, after_push=list(ends)))
    return iv, ends, steps


def fig_rooms2_heap_trace():
    iv, ends, steps = sim_heap(MR_RAW)
    assert len(ends) == FN["rooms2_heap"]["min_meeting_rooms"]([list(x) for x in MR_RAW]) == 3
    RH = 96
    H = 20 * 2 + 34 + 44 + RH * len(steps) + 90
    sv = Svg(H, "Meeting Rooms II 的 min-heap 运行流程",
             "按 start 排序后逐个会议: 最早结束的房间已空出来就 pop, 然后 push 这场会议的 end, heap 大小即房间数")
    y0 = head(sv, ["ends = min-heap, 存每个正在使用的房间里当前会议的 end · 画成 tree, 最上面的是最小的 (ring)",
                   "每一步: ends[0] ≤ s → 最早结束的房间空出来了, 先 pop → 再 push 这场会议的 end → rooms = len(ends)"]) + 14
    PX, QX = 205, 420
    sv.text(40, y0, "当前会议", 12, INK2)
    sv.text(121, y0, "pop 后", 12, INK2)
    sv.text(372, y0, "push 后", 12, INK2)
    sv.text(500, y0, "计算", 12, INK2)
    sv.dash_sep(y0 + 14)
    y = y0 + 22
    for st in steps:
        s, e = st["cur"]
        ty = y + 28  # tree root y
        # 输入卡
        sv.rect(40, y + 12, 66, 50, "new", sw=0.8)
        sv.text(73, y + 29, "[%d,%d]" % (s, e), 14, ROLE["new"][2], "middle", 500)
        sv.text(73, y + 48, "s = %d" % s, 12, ROLE["new"][2], "middle")
        # pop 后
        if st["after_pop"]:
            draw_heap(sv, PX, ty, st["after_pop"])
        else:
            sv.text(PX, ty, "(空)", 12, INK2, "middle")
        if st["popped"] is not None:
            sv.circle(135, ty, 14, "gone", sw=0.8, dash="3 2")
            sv.text(135, ty, st["popped"], 14, ROLE["gone"][2], "middle", 500)
            sv.line(PX - 22, ty, 153, ty, "#D85A30", 1.5, "4 3", arrow="r")
            sv.text(268, ty - 9, "ends[0] = %d" % st["top"], 12, INK2)
            sv.text(268, ty + 9, "≤ s = %d: pop %d" % (s, st["popped"]), 12, ROLE["gone"][2])
        elif st["top"] is None:
            sv.text(268, ty, "ends 为空", 12, INK2)
        else:
            sv.text(268, ty - 9, "ends[0] = %d" % st["top"], 12, INK2)
            sv.text(268, ty + 9, "> s = %d: 不 pop" % s, 12, INK2)
        # push 后
        draw_heap(sv, QX, ty, st["after_push"], new_val=e)
        sv.text(500, ty - 12, "push %d" % e, 12, INK2)
        sv.text(500, ty + 6, "rooms = len(ends) = %d" % len(st["after_push"]), 14, INK, "start", 500)
        y += RH
        if st is not steps[-1]:
            sv.dash_sep(y - 4)
    foot(sv, y - 2, "rooms = len(ends) = %d · 最后 heap 里的 end = %s" % (len(ends), ", ".join(str(v) for v in sorted(ends))),
         [("new", "新 push 进来的 end"), ("gone", "被 pop 的 end"), ("old", "heap 里其他的 end"),
          ("ring", "heap 顶")])
    sv.save("rooms2_heap_trace.svg")


def fig_rooms2_sweep_trace():
    tl = TL(60, 640, 0, 30)
    srt = sorted([list(x) for x in MR_RAW], key=lambda x: x[0])
    events = []
    for s, e in MR_RAW:
        events.append((s, 1))
        events.append((e, -1))
    events.sort()
    cur = best = 0
    cells = []
    for t, dl in events:
        cur += dl
        newbest = cur > best
        best = max(best, cur)
        cells.append((t, dl, cur, newbest))
    assert best == FN["rooms2_sweep"]["min_meeting_rooms"]([list(x) for x in MR_RAW]) == 3
    LANE = 28
    y_axis = 104
    lanes_y = y_axis + 14
    chart_top = lanes_y + LANE * len(srt) + 40
    unit = 22
    chart_base = chart_top + 3 * unit
    table_y = chart_base + 44
    H = table_y + 64 + 90
    sv = Svg(H, "Meeting Rooms II 的扫描线运行流程",
             "每个会议拆成 start 事件 +1 和 end 事件 -1, 排序后从左到右扫, cur 的最大值是答案")
    head(sv, ["events = 每场会议拆成 (start, +1) 和 (end, -1) · 排序: 同一时刻 -1 排在 +1 前 (先结束再开始)",
              "从左到右扫 events, cur += delta · cur = 此刻同时进行的会议数 · best = cur 出现过的最大值"])
    sv.text(40, 62, "时间轴 + 5 场会议 (已按 start 排序)", 12, INK2)
    axis(sv, tl, y_axis, 5, labels_below=False)
    grid(sv, tl, lanes_y - 4, chart_base, 5)
    # 事件竖线
    seen = {}
    for t, dl, c, nb in cells:
        seen.setdefault(t, []).append(dl)
    for t, dls in seen.items():
        col = "#0F6E56" if dls == [1] else ("#D85A30" if dls == [-1] else "#C07A0A")
        sv.line(tl.x(t), lanes_y - 4, tl.x(t), chart_base, col, 1, "2 3")
    for i, (a, b) in enumerate(srt):
        bar(sv, tl, lanes_y + i * LANE, a, b, "old", None, h=22)
    # 阶梯图
    sv.text(40, chart_top - 24, "cur = 同时进行的会议数 (下图的阶梯)", 12, INK2)
    sv.line(tl.x0, chart_base, tl.x1, chart_base, "#898781", 1)
    for v in range(1, 4):
        sv.line(tl.x0, chart_base - v * unit, tl.x1, chart_base - v * unit, "#ECEAE2", 1)
        sv.text(tl.x0 - 8, chart_base - v * unit, v, 12, INK2, "end")
    sv.text(tl.x0 - 8, chart_base, 0, 12, INK2, "end")
    pts_ = [(0, 0)]
    c_prev = 0
    for t, dl, c, nb in cells:
        pts_.append((t, c_prev))
        pts_.append((t, c))
        c_prev = c
    d_ = "M" + " L".join("%s %s" % (r(tl.x(t)), r(chart_base - v * unit)) for t, v in pts_)
    # 最大值区间高亮
    best_spans = []
    cur_t = None
    for k, (t, dl, c, nb) in enumerate(cells):
        if c == best and cur_t is None:
            cur_t = t
        if cur_t is not None and (k + 1 == len(cells) or cells[k + 1][2] != best or cells[k + 1][0] != t):
            if c == best:
                pass
        # 简化: 在 c == best 的事件到下一个事件之间高亮
    for k, (t, dl, c, nb) in enumerate(cells):
        if c == best:
            t2 = cells[k + 1][0]
            sv.rect(tl.x(t), chart_base - best * unit, tl.x(t2) - tl.x(t), best * unit, fill="#FFF4DB",
                    stroke=RING, sw=2, rx=2)
    sv.path(d_, "#444441", 2)
    for t, dl, c, nb in cells:
        pass
    # 事件表: 一格一步
    sv.text(40, table_y - 12, "events 排序后, 一格一步 (t, delta → cur):", 12, INK2)
    cw = 600 / len(cells)
    for k, (t, dl, c, nb) in enumerate(cells):
        x = 40 + k * cw
        role = "new" if dl == 1 else "gone"
        sv.rect(x + 1.5, table_y, cw - 3, 54, role, sw=0.8)
        sv.text(x + cw / 2, table_y + 11, "t=%d" % t, 12, ROLE[role][2], "middle")
        sv.text(x + cw / 2, table_y + 28, "%+d" % dl, 14, ROLE[role][2], "middle", 500)
        sv.text(x + cw / 2, table_y + 44, "cur=%d" % c, 12, ROLE[role][2], "middle", 500)
        if nb:
            sv.rect(x - 1.5, table_y - 3, cw + 3, 60, fill="none", stroke=RING, sw=2.5, rx=6)
    foot(sv, table_y + 66, "best = %d · t=15 首次到 3, t=22 再到 3 不刷新 · t=10 先 -1 再 +1" % best,
         [("new", "+1 start 事件"), ("gone", "-1 end 事件"), ("ring", "best 被刷新"),
          ("old", "会议")])
    sv.save("rooms2_sweep_trace.svg")


fig_rooms2_core()
fig_rooms2_heap_trace()
fig_rooms2_sweep_trace()


# ====================================================================== 7. Interval List Intersections
IA = [[0, 2], [5, 10], [13, 23]]
IB = [[1, 5], [8, 12], [15, 24]]


def sim_intersect(A, B):
    i = j = 0
    res, steps = [], []
    while i < len(A) and j < len(B):
        lo, hi = max(A[i][0], B[j][0]), min(A[i][1], B[j][1])
        hit = lo <= hi
        if hit:
            res.append([lo, hi])
        adv = "i" if A[i][1] < B[j][1] else "j"
        steps.append(dict(i=i, j=j, lo=lo, hi=hi, hit=hit, adv=adv, res=[list(x) for x in res]))
        if adv == "i":
            i += 1
        else:
            j += 1
    return res, steps


def fig_intersect_core():
    tl = TL(150, 440, 0, 26)
    rows = []
    # 行 1: a=[5,10], b=[8,12], 下一个 b'=[15,24]
    rows.append(dict(
        card=[("有交集", 14, 500), ("a 先结束", 12, 400)], card_role="new",
        lanes=[("a", [(5, 10, "old", None, {})]), ("b", [(8, 12, "old", None, {})]),
               ("b 后", [(15, 24, "old", None, {"dash": True})]),
               ("交集", [(8, 10, "new", None, {})])],
        right=[("lo = max(5, 8) = 8", "sub"), ("hi = min(10, 12) = 10", "sub"),
               ("lo ≤ hi → 交集 [8,10]", "ok"),
               ("a.end 10 < b.end 12 → i += 1", "sub"),
               ("a 够不到 b 后 (15 > 10)", "sub")]))
    rows.append(dict(
        card=[("无交集", 14, 500), ("b 先结束", 12, 400)], card_role="gone",
        lanes=[("a", [(13, 23, "old", None, {})]), ("b", [(8, 12, "old", None, {})]),
               ("交集", [(12, 13, "gone", "", {"dash": True})])],
        right=[("lo = max(13, 8) = 13", "sub"), ("hi = min(23, 12) = 12", "sub"),
               ("lo = 13 > hi = 12 → 不相交", "bad"),
               ("b.end 12 < a.end 23 → j += 1", "sub")]))
    trace("intersect_core.svg", "Interval List Intersections 的核心",
          "两个 interval 的交集是 [max(start), min(end)], 合法当且仅当 lo ≤ hi; end 小的那个再也碰不到对方后面的 interval",
          ["交集 = [lo, hi] = [两个 start 里大的, 两个 end 里小的] · lo ≤ hi 就是 overlap 条件",
           "两个列表各自已排序且内部不重叠 → end 小的那个, 对方后面的 interval 都在它右边, 可以放心丢掉"],
          tl, rows,
          "每步: 算 [lo, hi] → lo ≤ hi 就收下 → end 小的指针前进",
          [("old", "A / B 里的 interval"), ("new", "交集"), ("gone", "空隙")],
          axis_every=2, left_title="情况", mid_title="时间轴", right_title="计算")


def fig_intersect_trace():
    res, steps = sim_intersect(IA, IB)
    assert res == FN["intersect"]["interval_intersection"](IA, IB)
    tl = TL(150, 440, 0, 26)
    rows = []
    for k, st in enumerate(steps):
        i, j = st["i"], st["j"]
        a, b = IA[i], IB[j]

        def lane(L, idx, adv):
            out = []
            for t_, (x, y) in enumerate(L):
                if t_ == idx:
                    out.append((x, y, "gone" if adv else "old", None, {"ring": True}))
                else:
                    out.append((x, y, "old", None, {}))
            return out
        out_lane = [(x, y, "new" if (st["hit"] and [x, y] == [st["lo"], st["hi"]] and t_ == len(st["res"]) - 1) else "old",
                     None, {}) for t_, (x, y) in enumerate(st["res"])]
        right = [("lo = max(%d, %d) = %d" % (a[0], b[0], st["lo"]), "sub"),
                 ("hi = min(%d, %d) = %d" % (a[1], b[1], st["hi"]), "sub")]
        if st["hit"]:
            right.append(("%d ≤ %d → 收下 [%d,%d]" % (st["lo"], st["hi"], st["lo"], st["hi"]), "ok"))
        else:
            right.append(("%d > %d → 不相交" % (st["lo"], st["hi"]), "bad"))
        if st["adv"] == "i":
            right.append(("A.end %d < B.end %d: i += 1" % (a[1], b[1]), "sub"))
        else:
            right.append(("A.end %d ≥ B.end %d: j += 1" % (a[1], b[1]), "sub"))
        rows.append(dict(card=card_of("i=%d" % i, None, ["j=%d" % j]), card_role="new" if st["hit"] else "gone",
                         lanes=[("A", lane(IA, i, st["adv"] == "i")), ("B", lane(IB, j, st["adv"] == "j")),
                                ("res", out_lane)], right=right))
    trace("intersect_trace.svg", "Interval List Intersections 运行流程",
          "两个指针 i, j 各指一个列表; 每步算交集, 然后让 end 小的那个前进",
          ["A = " + " ".join("[%d,%d]" % tuple(x) for x in IA) + " · B = " + " ".join("[%d,%d]" % tuple(x) for x in IB),
           "ring = 指针当前指的 interval · 红色 = 这一步之后要前进 (end 较小) 的那个"],
          tl, rows,
          "res = " + " ".join("[%d,%d]" % tuple(x) for x in res) + " · 5 步, i 走到 3 结束",
          [("old", "interval"), ("gone", "end 小, 指针前进"), ("new", "新收下的交集"), ("ring", "指针位置")],
          axis_every=2, left_title="指针", mid_title="时间轴", right_title="计算")


fig_intersect_core()
fig_intersect_trace()


# ====================================================================== 8. My Calendar I
CAL_OPS = [(10, 20), (15, 25), (20, 30), (5, 10), (8, 12), (30, 35)]


def sim_calendar(ops):
    starts, ends = [], []
    steps = []
    for s, e in ops:
        i = bisect.bisect_left(starts, s)
        prev = (starts[i - 1], ends[i - 1]) if i > 0 else None
        nxt = (starts[i], ends[i]) if i < len(starts) else None
        reason = None
        if prev and prev[1] > s:
            ok, reason = False, "prev"
        elif nxt and nxt[0] < e:
            ok, reason = False, "next"
        else:
            ok = True
            starts.insert(i, s)
            ends.insert(i, e)
        steps.append(dict(s=s, e=e, i=i, prev=prev, nxt=nxt, ok=ok, reason=reason,
                          cal=list(zip(starts, ends))))
    return steps


def fig_calendar_core():
    tl = TL(150, 440, 0, 48)
    booked = [(5, 10), (12, 20), (22, 30), (40, 45)]
    rows = []
    for (s, e) in [(32, 38), (28, 36)]:
        starts = [b[0] for b in booked]
        i = bisect.bisect_left(starts, s)
        prev, nxt = booked[i - 1], booked[i]
        ok = not (prev[1] > s) and not (nxt[0] < e)
        lanes = [("已订", [(a, b, "old", None, {"ring": k in (i - 1, i)}) for k, (a, b) in enumerate(booked)]),
                 ("new", [(s, e, "new" if ok else "gone", None, {})])]
        right = [("bisect_left → i = %d" % i, "sub"),
                 ("prev = [%d,%d): end %d %s start %d" % (prev[0], prev[1], prev[1], ">" if prev[1] > s else "≤", s), "sub"),
                 ("next = [%d,%d): start %d %s end %d" % (nxt[0], nxt[1], nxt[0], "<" if nxt[0] < e else "≥", e), "sub"),
                 ("→ 可以预订" if ok else "→ 和 prev 冲突, False", "ok" if ok else "bad")]
        rows.append(dict(card=[("[%d,%d)" % (s, e), 14, 500), ("book", 12, 400)],
                         card_role="new" if ok else "gone", lanes=lanes, right=right))
    trace("calendar_core.svg", "My Calendar I: 只和左右两个邻居比",
          "已预订的 start 有序, bisect 找到新预订的位置 i, 只需检查 i-1 和 i 这两个邻居",
          ["半开区间 [start, end): 首尾相接不冲突 · 已预订的互不重叠, 按 start 有序",
           "新预订插在 i: 更左边的全在 prev 之前结束, 更右边的全在 next 之后开始, 不用比"],
          tl, rows,
          "冲突 = prev.end > start 或 next.start < end · 半开区间用严格不等号",
          [("old", "已预订"), ("ring", "prev 和 next"), ("new", "能订"), ("gone", "冲突")],
          axis_every=5, left_title="book", mid_title="时间轴", right_title="检查")


def fig_calendar_trace():
    steps = sim_calendar(CAL_OPS)
    tl = TL(150, 440, 0, 36)
    rows = []
    for st in steps:
        s, e = st["s"], st["e"]
        ok = st["ok"]
        cal_after = st["cal"]
        lanes = [("cal", [(a, b, "new" if (ok and (a, b) == (s, e)) else "old", None, {})
                          for a, b in cal_after]),
                 ("book", [(s, e, "new" if ok else "gone", None, {})])]
        right = [("bisect_left → i = %d" % st["i"], "sub")]
        if st["prev"] is None:
            right.append(("没有 prev (i = 0)", "sub"))
        else:
            right.append(("prev.end = %d %s start = %d" % (st["prev"][1], ">" if st["prev"][1] > s else "≤", s), "sub"))
        if st["nxt"] is None:
            right.append(("没有 next (i = len)", "sub"))
        else:
            right.append(("next.start = %d %s end = %d" % (st["nxt"][0], "<" if st["nxt"][0] < e else "≥", e), "sub"))
        right.append(("→ True, 插入" if ok else "→ False, 冲突", "ok" if ok else "bad"))
        rows.append(dict(card=[("[%d,%d)" % (s, e), 14, 500), ("True" if ok else "False", 12, 400)],
                         card_role="new" if ok else "gone", lanes=lanes, right=right))
    trace("calendar_trace.svg", "My Calendar I 运行流程",
          "连续 6 次 book: 每次 bisect 找位置, 只检查 prev.end 和 next.start",
          ["依次调用 book(10,20) book(15,25) book(20,30) book(5,10) book(8,12) book(30,35)",
           "cal = 已预订 (有序) · 冲突 = prev.end > start 或 next.start < end · 区间半开, 首尾相接可以"],
          tl, rows,
          "返回值: " + ", ".join(str(st["ok"]) for st in steps),
          [("new", "订成功 (插入 cal)"), ("gone", "冲突, 被拒绝"), ("old", "已订")],
          axis_every=5, left_title="当前调用", mid_title="时间轴 (半开区间)", right_title="检查")


fig_calendar_core()
fig_calendar_trace()


# ====================================================================== 文档里的小例子 (全部实跑)
assert FN["merge"]["merge"]([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
assert FN["merge"]["merge"]([[1, 4], [4, 5]]) == [[1, 5]]
assert FN["insert"]["insert"]([[1, 3], [6, 9]], [2, 5]) == [[1, 5], [6, 9]]
assert FN["erase"]["erase_overlap_intervals"]([[1, 2], [2, 3], [3, 4], [1, 3]]) == 1
assert FN["arrows"]["find_min_arrow_shots"]([[10, 16], [2, 8], [1, 6], [7, 12]]) == 2
assert FN["rooms1"]["can_attend_meetings"]([[0, 30], [5, 10], [15, 20]]) is False
assert FN["rooms1"]["can_attend_meetings"]([[7, 10], [2, 4]]) is True
assert FN["rooms2_heap"]["min_meeting_rooms"]([[0, 30], [5, 10], [15, 20]]) == 2
assert FN["rooms2_sweep"]["min_meeting_rooms"]([[0, 30], [5, 10], [15, 20]]) == 2
assert FN["intersect"]["interval_intersection"](
    [[0, 2], [5, 10], [13, 23], [24, 25]], [[1, 5], [8, 12], [15, 24], [25, 26]]) == \
    [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]]
_c = FN["calendar"]["MyCalendar"]()
assert [_c.book(*x) for x in CAL_OPS] == [True, False, True, True, False, True]
# "按 start 排会错" 的反例: A=[1,11] B=[2,4] C=[4,6] D=[6,8]
_iv = [[1, 11], [2, 4], [4, 6], [6, 8]]
assert FN["erase"]["erase_overlap_intervals"]([list(x) for x in _iv]) == 1


def _erase_by_start(iv):
    iv = sorted(iv)
    keep_end, removed = -inf, 0
    for s_, e_ in iv:
        if s_ >= keep_end:
            keep_end = e_
        else:
            removed += 1
    return removed


assert _erase_by_start(_iv) == 3
# Min arrows 和 Non-overlapping 的关系: 闭区间相接算重叠 => 一支箭 = 一个共点的组
print("doc examples ok")


# ====================================================================== 生成 HTML
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '10_intervals_doc.py'), encoding='utf-8').read())
