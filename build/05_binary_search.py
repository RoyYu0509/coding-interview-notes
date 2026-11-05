"""05 · Binary Search 的生成脚本。
运行: cd build && python3 -I 05_binary_search.py
- CODE_* 是文档里展示的代码, 原样 exec 过并和暴力解对拍 (见 selftest)。
- 所有 SVG 里的数字都来自真实运行 (trace_* 函数), 不是手填的。
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import doclib as d  # noqa: E402

SLUG = "05-binary-search"
SVG_DIR = os.path.join(d.ROOT, "docs", "svg", SLUG)

# ============================================================ 文档里的代码
CODE_TEMPLATE = '''
def first_true(lo, hi, pred):
    """在 [lo, hi) 里找第一个 pred 为 True 的位置, 都是 False 就返回 hi。
    前提: pred 在 [lo, hi) 上是 False...False True...True (单调)。"""
    while lo < hi:                 # invariant: < lo 全是 False, >= hi 全是 True
        mid = (lo + hi) // 2       # lo <= mid < hi, 所以 mid 一定在区间里
        if pred(mid):
            hi = mid               # mid 是 True: 分界点在 mid 或 mid 左边, mid 留着
        else:
            lo = mid + 1           # mid 是 False: 分界点一定在 mid 右边, mid 丢掉
    return lo                      # lo == hi: 就是分界点
'''

CODE_FIRST_LAST = '''
def search_range(nums, target):
    n = len(nums)
    left = first_true(0, n, lambda i: nums[i] >= target)   # bisect_left
    right = first_true(0, n, lambda i: nums[i] > target)   # bisect_right
    if left == right:              # 两个分界点重合 = 中间没有 == target 的数
        return [-1, -1]
    return [left, right - 1]       # [left, right) 里全是 target
'''

CODE_FIND_MIN = '''
def find_min(nums):
    last = nums[-1]
    # 左段 (旋转前较大的那段) 全 > last, 右段全 <= last: False...False True...True
    i = first_true(0, len(nums), lambda i: nums[i] <= last)
    return nums[i]
'''

CODE_SEARCH_ROTATED = '''
def search(nums, target):
    lo, hi = 0, len(nums)          # invariant: target 如果存在, 一定在 [lo, hi) 里
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:                 # 左半 [lo, mid] 有序
            if nums[lo] <= target < nums[mid]:    # target 在有序的左半里
                hi = mid
            else:
                lo = mid + 1
        else:                                     # 否则右半 [mid, hi-1] 有序
            if nums[mid] < target <= nums[hi - 1]:  # target 在有序的右半里
                lo = mid + 1
            else:
                hi = mid
    return -1
'''

CODE_PEAK = '''
def find_peak(nums):
    n = len(nums)
    # pred(i): "i 右边更低"。nums[n] 当作 -inf, 所以 pred(n-1) 一定是 True
    return first_true(0, n, lambda i: i == n - 1 or nums[i] > nums[i + 1])
'''

CODE_KOKO = '''
def min_eating_speed(piles, h):
    def feasible(k):                    # 速度 k 能不能在 h 小时内吃完
        # (p + k - 1) // k = ceil(p / k): 这堆要吃几小时
        return sum((p + k - 1) // k for p in piles) <= h
    return first_true(1, max(piles) + 1, feasible)   # 答案在 [1, max(piles)]
'''

CODE_SHIP = '''
def ship_within_days(weights, days):
    def feasible(cap):                  # 载重 cap 能不能在 days 天内运完
        need, load = 1, 0               # need = 已经用了几天, load = 今天已装多少
        for w in weights:
            if load + w > cap:          # 今天装不下了: 另起一天
                need += 1
                load = 0
            load += w
        return need <= days
    # 答案在 [max(weights), sum(weights)]
    return first_true(max(weights), sum(weights) + 1, feasible)
'''

CODE_SPLIT = '''
def split_array(nums, k):
    def feasible(x):                    # 每段和都 <= x, 最少要切几段? 够不够 k 段
        pieces, cur = 1, 0
        for v in nums:
            if cur + v > x:             # 当前段再加 v 就超 x: 另起一段
                pieces += 1
                cur = 0
            cur += v
        return pieces <= k
    # 答案在 [max(nums), sum(nums)]
    return first_true(max(nums), sum(nums) + 1, feasible)
'''

CODE_LAST_TRUE = '''
def last_true(lo, hi, pred):
    """pred 是 True...True False...False 时, 找最后一个 True; 没有就返回 lo - 1。"""
    return first_true(lo, hi, lambda x: not pred(x)) - 1
'''

CODE_MATRIX = '''
def search_matrix(matrix, target):
    m, n = len(matrix), len(matrix[0])
    # 把 m x n 看成长度 m*n 的 sorted 数组: 下标 i <-> (i // n, i % n)
    i = first_true(0, m * n, lambda i: matrix[i // n][i % n] >= target)
    return i < m * n and matrix[i // n][i % n] == target
'''

CODE_MEDIAN = '''
def find_median(A, B):
    if len(A) > len(B):
        A, B = B, A                    # 在短的那个上二分: A 里取 i 个放进左半
    m, n = len(A), len(B)
    half = (m + n + 1) // 2            # 左半共 half 个: A 取 i, B 取 j = half - i
    INF = float("inf")

    def cut_too_small(i):              # pred(i): A 取得够多了吗? F...F T...T
        # i == m: A 全进左半; 否则 A[i] (在右半) 不能比 B[j-1] (在左半) 小
        return i == m or A[i] >= B[half - i - 1]
    i = first_true(max(0, half - n), m + 1, cut_too_small)
    j = half - i
    left_max = max(A[i - 1] if i > 0 else -INF, B[j - 1] if j > 0 else -INF)
    right_min = min(A[i] if i < m else INF, B[j] if j < n else INF)
    if (m + n) % 2:
        return left_max
    return (left_max + right_min) / 2
'''

ALL_CODE = [CODE_TEMPLATE, CODE_FIRST_LAST, CODE_FIND_MIN, CODE_SEARCH_ROTATED,
            CODE_PEAK, CODE_KOKO, CODE_SHIP, CODE_SPLIT, CODE_LAST_TRUE,
            CODE_MATRIX, CODE_MEDIAN]


def load_code():
    ns = {}
    for c in ALL_CODE:
        exec(c, ns)
    return ns


# ============================================================ trace 用的"带记录"版本
def trace_first_true(lo, hi, pred):
    steps = []
    while lo < hi:
        mid = (lo + hi) // 2
        r = pred(mid)
        steps.append(dict(lo=lo, hi=hi, mid=mid, r=r))
        if r:
            hi = mid
        else:
            lo = mid + 1
    return lo, steps


def trace_search(nums, target):
    lo, hi = 0, len(nums)
    steps = []
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            steps.append(dict(lo=lo, hi=hi, mid=mid, kind="found"))
            return mid, steps
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                steps.append(dict(lo=lo, hi=hi, mid=mid, kind="L-in"))
                hi = mid
            else:
                steps.append(dict(lo=lo, hi=hi, mid=mid, kind="L-out"))
                lo = mid + 1
        else:
            if nums[mid] < target <= nums[hi - 1]:
                steps.append(dict(lo=lo, hi=hi, mid=mid, kind="R-in"))
                lo = mid + 1
            else:
                steps.append(dict(lo=lo, hi=hi, mid=mid, kind="R-out"))
                hi = mid
    return -1, steps


# ============================================================ SVG 小工具
FONT = 'ui-sans-serif, system-ui, -apple-system, "PingFang SC", sans-serif'
ROLE = {
    "norm": ("#F1EFE8", "#5F5E5A", "#444441"),
    "new": ("#E1F5EE", "#0F6E56", "#085041"),
    "gone": ("#FAECE7", "#993C1D", "#712B13"),
    "none": ("#FFFFFF", "#B4B2A9", "#52514E"),
}
INK, SUB, RING, SEP = "#0B0B0B", "#52514E", "#EF9F27", "#B4B2A9"
DISCARD_TXT = "#712B13"
OK_TXT = "#085041"


def esc(s):
    return html.escape(str(s), quote=False)


class Svg:
    def __init__(self, title, desc, w=680):
        self.w = w
        self.title, self.desc = title, desc
        self.e = []

    def t(self, x, y, s, size=14, fill=INK, anchor="start", bold=False):
        self.e.append('<text x="%s" y="%s" font-size="%d" fill="%s" text-anchor="%s"%s>%s</text>'
                      % (x, y, size, fill, anchor, ' font-weight="600"' if bold else "", esc(s)))

    def rect(self, x, y, w, h, fill="none", stroke="none", sw=1, rx=4, dash=None):
        self.e.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>'
                      % (x, y, w, h, rx, fill, stroke, sw, ' stroke-dasharray="%s"' % dash if dash else ""))

    def line(self, x1, y1, x2, y2, stroke=SEP, sw=1, dash=None, marker=None):
        self.e.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s%s/>'
                      % (x1, y1, x2, y2, stroke, sw,
                         ' stroke-dasharray="%s"' % dash if dash else "",
                         ' marker-end="url(#%s)"' % marker if marker else ""))

    def path(self, dd, stroke=SUB, sw=1.5, fill="none", dash=None, marker=None):
        self.e.append('<path d="%s" fill="%s" stroke="%s" stroke-width="%s"%s%s/>'
                      % (dd, fill, stroke, sw, ' stroke-dasharray="%s"' % dash if dash else "",
                         ' marker-end="url(#%s)"' % marker if marker else ""))

    def circle(self, cx, cy, r, fill="none", stroke="none", sw=1):
        self.e.append('<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" stroke-width="%s"/>'
                      % (cx, cy, r, fill, stroke, sw))

    def sep(self, y):
        self.line(20, y, self.w - 20, y, SEP, 1, "4 4")

    def cell(self, x, y, w, h, label, role="norm", ring=False, size=16, dashed=False):
        f, s, tx = ROLE[role]
        self.rect(x, y, w, h, f, s, 1, 4, "3 3" if dashed else None)
        if ring:
            self.rect(x - 3, y - 3, w + 6, h + 6, "none", RING, 2.5, 6)
        self.t(x + w / 2, y + h / 2 + size * 0.36, label, size, tx, "middle")

    def legend(self, y, items, x=24):
        for role, ring, label in items:
            if role:
                f, s, _ = ROLE[role]
                self.rect(x, y - 12, 18, 18, f, s, 1, 4)
            if ring:
                self.rect(x - 3, y - 15, 24, 24, "none", RING, 2.5, 6)
            self.t(x + 28, y + 2, label, 12, SUB)
            x += 28 + 7 * len(label) + 30 if label.isascii() else 28 + 12 * len(label) + 24

    def render(self, h):
        defs = ('<defs>'
                '<marker id="ag" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
                '<path d="M2 1L8 5L2 9" fill="none" stroke="#5F5E5A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>'
                '<marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
                '<path d="M2 1L8 5L2 9" fill="none" stroke="#D85A30" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>'
                '<marker id="agr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
                '<path d="M2 1L8 5L2 9" fill="none" stroke="#0F6E56" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>'
                '</defs>')
        return ('<svg width="100%%" viewBox="0 0 %d %d" role="img" xmlns="http://www.w3.org/2000/svg" '
                'font-family=\'%s\'><title>%s</title><desc>%s</desc>%s%s</svg>\n'
                % (self.w, h, FONT.replace("'", ""), esc(self.title), esc(self.desc), defs, "".join(self.e)))

    def save(self, name, h):
        os.makedirs(SVG_DIR, exist_ok=True)
        with open(os.path.join(SVG_DIR, name), "w", encoding="utf-8") as f:
            f.write(self.render(h))


def header(s, line1, line2, y1=22, y2=42):
    s.t(20, y1, line1, 12, SUB)
    if line2:
        s.t(20, y2, line2, 12, SUB)


# ---------------------------------------------------------- 通用: 数组上的二分 trace
def array_trace(name, title, line1, line2, arr, sections, legend, cw=None, ax=132,
                right_head="比较 → 动作", left_head="lo / hi / mid"):
    """sections: [ (header_text or None, [step, ...]) ]
    step: dict(lo, hi, mid(None 表示结束行), lines=[(text,size,fill)], ans=下标或None)"""
    n = len(arr)
    cw = cw or min(40, (430 - ax) // n)
    rx = ax + n * cw + 16
    s = Svg(title, line2 or line1)
    header(s, line1, line2)
    s.t(20, 72, left_head, 12, SUB)
    s.t(ax, 72, "数组 (上面是下标)", 12, SUB)
    s.t(rx, 72, right_head, 12, SUB)
    y = 82
    for sec_head, steps in sections:
        s.sep(y)
        if sec_head:
            s.t(20, y + 22, sec_head, 14, INK, bold=True)
            y += 34
        # 下标行
        for i in range(n):
            s.t(ax + i * cw + cw / 2, y + 16, i, 12, SUB, "middle")
        y += 22
        for st in steps:
            top = y
            lo, hi, mid, ans = st["lo"], st["hi"], st.get("mid"), st.get("ans")
            for i, v in enumerate(arr):
                role = "norm"
                if i < lo or i >= hi:
                    role = "gone"
                if ans is not None and i == ans:
                    role = "new"
                s.cell(ax + i * cw, top + 8, cw - 2, 32, v, role,
                       ring=(i == mid) or (ans is not None and i == ans), size=14 if cw < 34 else 16)
            s.t(20, top + 28, "lo=%d  hi=%d" % (lo, hi), 14, INK)
            if mid is not None:
                s.t(20, top + 48, "mid=(%d+%d)//2=%d" % (lo, hi, mid), 12, SUB)
            ty = top + 22
            for text, size, fill in st["lines"]:
                s.t(rx, ty, text, size, fill)
                ty += 19
            y = top + st.get("h", 66)
            s.sep(y)
            y += 4
    y += 14
    return s, y


def finish_with_legend(s, y, legend, final_lines=()):
    for ln in final_lines:
        s.t(20, y, ln[0], ln[1], ln[2], bold=ln[1] == 16)
        y += 24
    y += 6
    s.legend(y, legend)
    return y + 22


# ---------------------------------------------------------- 通用: 答案空间上的二分 trace
def space_trace(name, title, line1, line2, L, R, steps, final_lines, legend,
                bx=140, bw=190):
    """steps: dict(lo,hi,mid, lines=[(text,size,fill)])  L,R: 整个答案范围 [L, R)"""
    s = Svg(title, line2 or line1)
    header(s, line1, line2)
    rx = bx + bw + 22
    s.t(20, 72, "lo / hi / mid", 12, SUB)
    s.t(bx, 72, "答案范围 [%d, %d) 里还剩哪段" % (L, R), 12, SUB)
    s.t(rx, 72, "feasible(mid) → 动作", 12, SUB)
    y = 82

    def X(v):
        return bx + (v - L) / (R - L) * bw
    for st in steps:
        s.sep(y)
        top = y
        lo, hi, mid = st["lo"], st["hi"], st.get("mid")
        by = top + 22
        s.rect(bx, by, bw, 22, "#FAECE7", "#993C1D", 1, 3)
        s.rect(X(lo), by, max(X(hi) - X(lo), 1.5), 22, "#F1EFE8", "#5F5E5A", 1, 3)
        if mid is not None:
            mx = X(mid + 0.5)
            s.line(mx, by - 6, mx, by + 28, RING, 2.5)
        s.t(bx, by + 42, str(L), 12, SUB, "start")
        s.t(bx + bw, by + 42, str(R), 12, SUB, "end")
        s.t(20, top + 32, "lo=%d  hi=%d" % (lo, hi), 14, INK)
        if mid is not None:
            s.t(20, top + 52, "mid=(%d+%d)//2=%d" % (lo, hi, mid), 12, SUB)
        ty = top + 26
        for text, size, fill in st["lines"]:
            s.t(rx, ty, text, size, fill)
            ty += 19
        if st.get("ans") is not None:
            s.rect(X(st["ans"]), by, max(bw / (R - L), 3), 22, "#E1F5EE", "#0F6E56", 1.5, 3)
        y = top + st.get("h", 84 if mid is not None else 76)
    s.sep(y)
    y += 30
    return s, finish_with_legend(s, y, legend, final_lines)


GRAY_LEG = [("norm", False, "仍在 [lo, hi) 里"), ("gone", False, "已排除"),
            ("new", False, "答案"), (None, True, "mid")]


# ============================================================ 各张图
def fig_s0_core():
    a = [1, 3, 5, 7, 9, 11, 13]
    t = 8
    n = len(a)
    pred = lambda i: a[i] >= t
    ans, steps = trace_first_true(0, n, pred)
    s = Svg("first_true 的 invariant", "pred 单调, lo 左边全是 False, hi 及右边全是 True")
    header(s, "nums = [1, 3, 5, 7, 9, 11, 13] · pred(i) = nums[i] >= 8 · 答案 = 第一个 True 的下标",
           "invariant: 下标 < lo 的已知 False (红), 下标 >= hi 的已知 True (绿), [lo, hi) 里还不知道 (灰)")
    x0, w = 84, 44
    y = 66
    s.t(20, y + 22, "idx", 12, SUB)
    s.t(20, y + 48, "nums", 12, SUB)
    s.t(20, y + 90, "pred", 12, SUB)
    for i in range(n + 1):
        s.t(x0 + i * w + w / 2, y + 16, i if i < n else "n=7", 12, SUB, "middle")
    for i in range(n):
        s.cell(x0, y + 28, w - 2, 30, a[i], "norm") if False else s.cell(x0 + i * w, y + 28, w - 2, 30, a[i], "norm")
        ok = pred(i)
        s.cell(x0 + i * w, y + 70, w - 2, 30, "True" if ok else "False", "new" if ok else "gone",
               ring=(i == ans), size=12)
    s.cell(x0 + n * w, y + 70, w - 2, 30, "True", "none", dashed=True, size=12)
    s.t(x0 + n * w + w / 2 - 1, y + 118, "虚拟的 True", 12, SUB, "middle")
    s.t(x0 + ans * w + w / 2, y + 118, "分界点 = 4", 12, SUB, "middle")
    s.sep(y + 128)
    y = y + 140
    s.t(20, y + 10, "二分: 每问一次 pred(mid), 就能确定 mid 一侧的全部", 14, INK, bold=True)
    y += 24
    for st in steps + [dict(lo=ans, hi=ans, mid=None)]:
        lo, hi, mid = st["lo"], st["hi"], st["mid"]
        s.t(20, y + 22, "lo=%d hi=%d" % (lo, hi), 12, SUB)
        for i in range(n + 1):
            role = "norm"
            if i < lo:
                role = "gone"
            elif i >= hi:
                role = "new"
            s.cell(x0 + i * w, y + 4, w - 2, 28, "" if i != n else "", role, ring=(i == mid), dashed=(i == n))
        if mid is not None:
            r = st["r"]
            if r:
                txt = "pred(%d) = nums[%d] = %d >= 8 → True" % (mid, mid, a[mid])
                act = "hi = mid = %d: %d 及右边全是 True" % (mid, mid)
            else:
                txt = "pred(%d) = nums[%d] = %d >= 8 → False" % (mid, mid, a[mid])
                act = "lo = mid + 1 = %d: %d 及左边全是 False" % (mid + 1, mid)
            rx = x0 + (n + 1) * w + 8
            s.t(rx, y + 16, txt, 12, INK)
            s.t(rx, y + 32, act, 12, DISCARD_TXT)
        else:
            s.t(x0 + (n + 1) * w + 8, y + 22, "lo == hi == %d: 分界点" % ans, 14, OK_TXT, bold=True)
        y += 52
    s.t(20, y + 12, "每轮区间缩小一半, 但 invariant 一直成立, 所以 lo == hi 时就是第一个 True。", 14, INK)
    y += 40
    s.legend(y, [("gone", False, "已知 False"), ("new", False, "已知 True"),
                 ("norm", False, "还不知道"), (None, True, "mid / 分界点")])
    s.save("s0_first_true_core.svg", y + 24)


def fig_first_last_core():
    a = [5, 7, 7, 8, 8, 8, 10, 12]
    n = len(a)
    left = trace_first_true(0, n, lambda i: a[i] >= 8)[0]
    right = trace_first_true(0, n, lambda i: a[i] > 8)[0]
    left9 = trace_first_true(0, n, lambda i: a[i] >= 9)[0]
    right9 = trace_first_true(0, n, lambda i: a[i] > 9)[0]
    assert (left, right, left9, right9) == (3, 6, 6, 6)
    s = Svg("first/last 的两个分界点", "bisect_left 与 bisect_right 是同一个模板, 只差 >= 和 >")
    header(s, "同一个 first_true, 只换 pred: >= target 的分界点是 left, > target 的分界点是 right",
           "[left, right) 里恰好全是 target")
    x0, w = 100, 48
    y = 60

    def block(y, target, lv, rv, tag):
        s.t(20, y + 22, "idx", 12, SUB)
        s.t(20, y + 48, "nums", 12, SUB)
        s.t(20, y + 82, ">= %d" % target, 12, SUB)
        s.t(20, y + 118, "> %d" % target, 12, SUB)
        for i in range(n):
            s.t(x0 + i * w + w / 2, y + 16, i, 12, SUB, "middle")
            s.cell(x0 + i * w, y + 28, w - 2, 28, a[i], "new" if a[i] == target else "norm")
            p1 = a[i] >= target
            p2 = a[i] > target
            s.cell(x0 + i * w, y + 64, w - 2, 28, "T" if p1 else "F", "new" if p1 else "gone", ring=(i == lv))
            s.cell(x0 + i * w, y + 100, w - 2, 28, "T" if p2 else "F", "new" if p2 else "gone", ring=(i == rv))
        rx = x0 + n * w + 14
        s.t(rx, y + 83, "left = %d" % lv, 14, INK)
        s.t(rx, y + 119, "right = %d" % rv, 14, INK)

    block(y, 8, left, right, "")
    s.t(20, y + 150, "target = 8: [left, right) = [3, 6), 有 3 个 8, 最后一个的下标 = right - 1 = 5", 14, INK)
    s.sep(y + 164)
    y += 176
    s.t(20, y + 6, "target = 9 (不存在): 两个分界点撞在一起", 14, INK, bold=True)
    y += 12
    block(y, 9, left9, right9, "")
    s.t(20, y + 150, "left = right = 6: [6, 6) 是空区间, 返回 [-1, -1]", 14, INK)
    y += 176
    s.legend(y, [("new", False, "True / 等于 target"), ("gone", False, "False"), (None, True, "分界点 (第一个 True)")])
    s.save("first_last_core.svg", y + 24)


def fig_first_last_trace():
    a = [5, 7, 7, 8, 8, 8, 10, 12]
    n = len(a)
    secs = []
    for tag, op, pr in (("① left = first_true(nums[i] >= 8)", ">=", lambda i: a[i] >= 8),
                        ("② right = first_true(nums[i] > 8)", ">", lambda i: a[i] > 8)):
        ans, st = trace_first_true(0, n, pr)
        steps = []
        for x in st:
            m = x["mid"]
            if x["r"]:
                lines = [("nums[%d] = %d %s 8 → True" % (m, a[m], op), 14, INK),
                         ("hi = mid = %d" % m, 12, DISCARD_TXT),
                         ("[%d, %d) 已知全是 True" % (m, x["hi"]), 12, SUB)]
            else:
                lines = [("nums[%d] = %d %s 8 → False" % (m, a[m], op), 14, INK),
                         ("lo = mid + 1 = %d" % (m + 1), 12, DISCARD_TXT),
                         ("[%d, %d] 已知全是 False" % (x["lo"], m), 12, SUB)]
            steps.append(dict(lo=x["lo"], hi=x["hi"], mid=m, lines=lines))
        res = "left" if op == ">=" else "right"
        steps.append(dict(lo=ans, hi=ans, mid=None, ans=ans if ans < n else None, h=60,
                          lines=[("lo == hi == %d" % ans, 14, OK_TXT),
                                 ("%s = %d" % (res, ans), 14, OK_TXT)]))
        secs.append((tag, steps))
    s, y = array_trace("", "first/last trace", "target = 8 · 每步: 算 pred(mid) → True 丢右半 (hi = mid), False 丢左半 (lo = mid + 1)",
                       "同一个数组跑两遍, 只有 pred 里的 >= 和 > 不同", a, secs, GRAY_LEG)
    y = finish_with_legend(s, y, GRAY_LEG, [("left = 3, right = 6 → 答案 [left, right - 1] = [3, 5]", 16, INK)])
    s.save("first_last_trace.svg", y)


def fig_find_min_core():
    a = [4, 5, 6, 7, 8, 9, 1, 2, 3]
    n = len(a)
    last = a[-1]
    ans, _ = trace_first_true(0, n, lambda i: a[i] <= last)
    assert ans == 6
    s = Svg("rotated 数组里的单调 predicate", "和最后一个元素比, 得到 False...False True...True")
    header(s, "旋转前 sorted [1,2,3,4,5,6,7,8,9] 被转成下面这样: 左段大 (4..9), 右段小 (1..3)",
           "last = nums[-1] = 3 · pred(i) = nums[i] <= last")
    x0, w = 84, 54
    y = 60
    s.t(20, y + 22, "idx", 12, SUB)
    s.t(20, y + 48, "nums", 12, SUB)
    s.t(20, y + 84, "pred", 12, SUB)
    for i in range(n):
        s.t(x0 + i * w + w / 2, y + 16, i, 12, SUB, "middle")
        s.cell(x0 + i * w, y + 28, w - 2, 30, a[i], "norm")
        ok = a[i] <= last
        s.cell(x0 + i * w, y + 66, w - 2, 30, "True" if ok else "False", "new" if ok else "gone",
               ring=(i == ans), size=12)
    # 左段 / 右段 括号
    s.line(x0, y + 112, x0 + 6 * w - 4, y + 112, SUB, 1.5)
    s.t(x0 + 3 * w, y + 132, "左段: 全 > last = 3", 12, SUB, "middle")
    s.line(x0 + 6 * w, y + 112, x0 + 9 * w - 4, y + 112, SUB, 1.5)
    s.t(x0 + 7.5 * w, y + 132, "右段: 全 <= last", 12, SUB, "middle")
    s.sep(y + 146)
    s.t(20, y + 170, "第一个 True 的下标 = 6, nums[6] = 1 就是最小值。", 14, INK)
    s.t(20, y + 194, "为什么和 last 比, 不和 nums[lo] 比?", 14, INK, bold=True)
    s.t(20, y + 216, "和 last 比: 左段 (4..9) 一定都比 3 大, 右段 (1, 2, 3) 一定都 <= 3, 所以是单调的。", 12, SUB)
    s.t(20, y + 236, "和 nums[lo] 比: lo 落在哪一段不确定, 同一个比较在不同位置含义不同, 不单调。", 12, SUB)
    s.t(20, y + 256, "(数组没被旋转时 last 是最大值, pred 全是 True, 分界点 = 0, 也对。)", 12, SUB)
    s.legend(y + 290, [("new", False, "nums[i] <= last (True)"), ("gone", False, "nums[i] > last (False)"),
                       (None, True, "分界点")])
    s.save("find_min_core.svg", y + 314)


def fig_find_min_trace():
    a = [4, 5, 6, 7, 8, 9, 1, 2, 3]
    n = len(a)
    last = a[-1]
    ans, st = trace_first_true(0, n, lambda i: a[i] <= last)
    steps = []
    for x in st:
        m = x["mid"]
        if x["r"]:
            lines = [("nums[%d] = %d <= last = %d → True" % (m, a[m], last), 14, INK),
                     ("hi = mid = %d" % m, 12, DISCARD_TXT),
                     ("%d 可能就是最小值, 留着" % m, 12, SUB)]
        else:
            lines = [("nums[%d] = %d <= last = %d → False" % (m, a[m], last), 14, INK),
                     ("lo = mid + 1 = %d" % (m + 1), 12, DISCARD_TXT),
                     ("最小值在 %d 右边" % m, 12, SUB)]
        steps.append(dict(lo=x["lo"], hi=x["hi"], mid=m, lines=lines))
    steps.append(dict(lo=ans, hi=ans, mid=None, ans=ans, h=60,
                      lines=[("lo == hi == %d" % ans, 14, OK_TXT), ("nums[%d] = %d" % (ans, a[ans]), 14, OK_TXT)]))
    s, y = array_trace("", "find min trace", "last = nums[-1] = 3 · pred(i) = nums[i] <= last",
                       "每步: 算 pred(mid) → True 丢右半 (hi = mid), False 丢左半 (lo = mid + 1)",
                       a, [(None, steps)], GRAY_LEG)
    y = finish_with_legend(s, y, GRAY_LEG, [("最小值 = nums[6] = 1", 16, INK)])
    s.save("find_min_trace.svg", y)


def fig_rotated_core():
    a = [4, 5, 6, 7, 8, 9, 1, 2, 3]
    n = len(a)
    s = Svg("哪一半有序", "把 [lo, hi) 从 mid 切开, 总有一半是有序的")
    header(s, "旋转点 (9 → 1 那个下降) 只可能在 mid 的一侧, 所以另一侧一定有序",
           "有序的那一半可以用两个端点 O(1) 判断 target 在不在里面")
    x0, w = 60, 56
    target = 3
    cases = [
        (0, 9, 4, "step 1: lo=0 hi=9 mid=4, target = 3"),
        (5, 9, 7, "step 2: lo=5 hi=9 mid=7, target = 3"),
    ]
    y = 60
    for lo, hi, mid, ttl in cases:
        s.t(20, y + 12, ttl, 14, INK, bold=True)
        for i in range(n):
            s.t(x0 + i * w + w / 2, y + 30, i, 12, SUB, "middle")
            s.cell(x0 + i * w, y + 38, w - 2, 30, a[i], "gone" if (i < lo or i >= hi) else "norm", ring=(i == mid))
        if a[lo] <= a[mid]:
            s.line(x0 + lo * w, y + 84, x0 + (mid + 1) * w - 4, y + 84, "#0F6E56", 3)
            s.t(x0 + (lo + mid + 1) * w / 2, y + 104, "左半有序: nums[lo]=%d <= nums[mid]=%d" % (a[lo], a[mid]),
                12, OK_TXT, "middle")
            ok = a[lo] <= target < a[mid]
            s.t(20, y + 130, "target 在里面吗? nums[lo] <= target < nums[mid] → %d <= %d < %d → %s" % (a[lo], target, a[mid], ok),
                14, INK)
            s.t(20, y + 152, "不在 → 丢掉有序的左半: lo = mid + 1 = %d" % (mid + 1), 14, DISCARD_TXT)
        else:
            s.line(x0 + mid * w, y + 84, x0 + hi * w - 4, y + 84, "#0F6E56", 3)
            s.t(x0 + (mid + hi) * w / 2, y + 104, "右半有序: nums[mid]=%d <= nums[hi-1]=%d" % (a[mid], a[hi - 1]),
                12, OK_TXT, "middle")
            ok = a[mid] < target <= a[hi - 1]
            s.t(20, y + 130, "target 在里面吗? nums[mid] < target <= nums[hi-1] → %d < %d <= %d → %s" % (a[mid], target, a[hi - 1], ok),
                14, INK)
            s.t(20, y + 152, "在 → 去有序的右半找: lo = mid + 1 = %d" % (mid + 1), 14, DISCARD_TXT)
        s.sep(y + 168)
        y += 182
    s.t(20, y + 8, "判断 \"哪半有序\": 左半有序 ⇔ nums[lo] <= nums[mid] (元素不重复)。target 在有序那半就进去, 否则去另一半。", 12, SUB)
    s.legend(y + 38, [("norm", False, "仍在 [lo, hi) 里"), ("gone", False, "已排除"), (None, True, "mid")])
    s.save("search_rotated_core.svg", y + 62)


def fig_rotated_trace():
    a = [4, 5, 6, 7, 8, 9, 1, 2, 3]
    target = 3
    ans, st = trace_search(a, target)
    assert ans == 8
    steps = []
    for x in st:
        lo, hi, m, k = x["lo"], x["hi"], x["mid"], x["kind"]
        if k == "found":
            lines = [("nums[%d] = %d == target" % (m, a[m]), 14, OK_TXT), ("return %d" % m, 14, OK_TXT)]
        elif k.startswith("L"):
            lines = [("nums[lo]=%d <= nums[mid]=%d: 左半有序" % (a[lo], a[m]), 12, SUB),
                     ("%d <= %d < %d ? %s" % (a[lo], target, a[m], k == "L-in"), 14, INK),
                     (("hi = mid = %d (丢右半)" % m) if k == "L-in" else ("lo = mid + 1 = %d (丢左半)" % (m + 1)), 12, DISCARD_TXT)]
        else:
            lines = [("nums[lo]=%d > nums[mid]=%d: 右半有序" % (a[lo], a[m]), 12, SUB),
                     ("%d < %d <= %d ? %s" % (a[m], target, a[hi - 1], k == "R-in"), 14, INK),
                     (("lo = mid + 1 = %d (丢左半)" % (m + 1)) if k == "R-in" else ("hi = mid = %d (丢右半)" % m, 12, DISCARD_TXT)[0], 12, DISCARD_TXT)]
        steps.append(dict(lo=lo, hi=hi, mid=m, lines=lines, ans=m if k == "found" else None, h=66))
    s, y = array_trace("", "rotated search trace", "target = 3 · 每步先看 nums[lo] <= nums[mid] 判断哪半有序, 再看 target 在不在有序那半",
                       "invariant: target 如果存在, 一定在 [lo, hi) 里 (红色格子已经排除)",
                       a, [(None, steps)], GRAY_LEG, cw=30, ax=124, right_head="哪半有序 → target 在不在 → 动作")
    y = finish_with_legend(s, y, GRAY_LEG, [("3 步找到: return 8", 16, INK)])
    s.save("search_rotated_trace.svg", y)


PEAK = [1, 2, 3, 5, 4, 6, 7, 9, 8, 3, 1]


def fig_peak_core():
    a = PEAK
    n = len(a)
    s = Svg("peak 的局部单调", "mid 上坡则右边必有 peak, 下坡则 mid 或左边必有 peak")
    header(s, "nums 不 sorted, 但相邻元素不相等, 且 nums[-1] = nums[n] = -inf (两端都当作掉下悬崖)",
           "pred(i) = nums[i] > nums[i+1] (i 处是下坡): 只要看 mid 往哪边走, 就知道哪一侧一定藏着 peak")
    x0, dx = 50, 54
    base, sc = 270, 16
    pts = [(x0 + i * dx, base - a[i] * sc) for i in range(n)]
    s.path("M" + " L".join("%d %d" % p for p in pts), "#5F5E5A", 2)
    for i, (px, py) in enumerate(pts):
        s.circle(px, py, 5, "#F1EFE8", "#5F5E5A", 1.5)
        s.t(px, base + 20, i, 12, SUB, "middle")
        s.t(px, py - 12, a[i], 12, SUB, "middle")
    s.t(20, base + 20, "idx", 12, SUB)
    # mid = 5 : 上坡
    px, py = pts[5]
    s.circle(px, py, 9, "none", RING, 2.5)
    s.path("M%d %d L%d %d" % (px + 2, py + 24, px + 70, py + 24), "#0F6E56", 2, marker="agr")
    s.t(px + 2, py + 42, "mid=5", 12, OK_TXT)
    # mid = 8 : 下坡
    px2, py2 = pts[8]
    s.circle(px2, py2, 9, "none", RING, 2.5)
    s.path("M%d %d L%d %d" % (px2 + 2, py2 + 24, px2 - 66, py2 + 24), "#0F6E56", 2, marker="agr")
    s.t(px2 - 66, py2 + 42, "mid=8", 12, OK_TXT)
    ty = base + 52
    s.t(20, ty, "mid=5: nums[5]=6 < nums[6]=7, 上坡 → 往右走", 14, INK)
    s.t(20, ty + 20, "右边一定有 peak → lo = mid + 1", 12, DISCARD_TXT)
    s.t(344, ty, "mid=8: nums[8]=8 > nums[9]=3, 下坡 → 往左", 14, INK)
    s.t(344, ty + 20, "mid 自己或左边一定有 peak → hi = mid", 12, DISCARD_TXT)
    base2 = base + 34
    s.sep(base + 84)
    base = base + 48
    s.t(20, base + 62, "为什么: 往上坡方向一直走, 要么遇到下坡 (那里就是 peak), 要么走到尽头 (尽头外是 -inf, 最后一个就是 peak)。", 12, SUB)
    s.t(20, base + 82, "整个数组不单调, 但每一步都能丢掉一半且保证 \"peak 还在剩下的里面\", 二分只需要这个。", 12, SUB)
    s.t(20, base + 108, "(图里 idx 3 的 5 和 idx 7 的 9 都是 peak, 题目允许返回任意一个。)", 12, SUB)
    s.save("peak_core.svg", base + 124)


def fig_peak_trace():
    a = PEAK
    n = len(a)
    pred = lambda i: i == n - 1 or a[i] > a[i + 1]
    ans, st = trace_first_true(0, n, pred)
    assert ans == 7
    steps = []
    for x in st:
        m = x["mid"]
        if x["r"]:
            lines = [("nums[%d]=%d > nums[%d]=%d → 下坡" % (m, a[m], m + 1, a[m + 1]), 14, INK),
                     ("hi = mid = %d" % m, 12, DISCARD_TXT), ("peak 在 [lo, %d] 里" % m, 12, SUB)]
        else:
            lines = [("nums[%d]=%d < nums[%d]=%d → 上坡" % (m, a[m], m + 1, a[m + 1]), 14, INK),
                     ("lo = mid + 1 = %d" % (m + 1), 12, DISCARD_TXT), ("peak 在 [%d, hi) 里" % (m + 1), 12, SUB)]
        steps.append(dict(lo=x["lo"], hi=x["hi"], mid=m, lines=lines))
    steps.append(dict(lo=ans, hi=ans, mid=None, ans=ans, h=60,
                      lines=[("lo == hi == %d" % ans, 14, OK_TXT), ("nums[%d] = %d 是 peak" % (ans, a[ans]), 14, OK_TXT)]))
    s, y = array_trace("", "peak trace", "pred(i) = nums[i] > nums[i+1] (i 处是下坡) · 下坡 → hi = mid, 上坡 → lo = mid + 1",
                       "invariant: [lo, hi) 里一定有一个 peak", a, [(None, steps)], GRAY_LEG, cw=26, ax=120,
                       right_head="看 mid 和 mid+1 → 动作", left_head="lo / hi / mid")
    y = finish_with_legend(s, y, GRAY_LEG, [("peak = nums[7] = 9 (另一个 peak nums[3] = 5 被二分绕过去了, 也合法)", 14, INK)])
    s.save("peak_trace.svg", y)


# ---------------- Koko
KOKO_P, KOKO_H = [3, 6, 7, 11], 8


def koko_hours(k):
    return [(p + k - 1) // k for p in KOKO_P]


def fig_koko_core():
    n = 11
    s = Svg("Koko 的 feasible 单调", "速度越大, 吃完需要的小时越少")
    header(s, "piles = [3, 6, 7, 11], h = 8 · hours(k) = ceil(3/k) + ceil(6/k) + ceil(7/k) + ceil(11/k)",
           "feasible(k) = hours(k) <= h = 8 · k 越大 hours 只会变小, 所以 feasible 是 False...False True...True")
    x0, w = 84, 52
    y = 60
    s.t(20, y + 22, "k", 12, SUB)
    s.t(20, y + 48, "hours", 12, SUB)
    s.t(20, y + 84, "<= 8 ?", 12, SUB)
    ans = None
    for k in range(1, n + 1):
        hrs = sum(koko_hours(k))
        ok = hrs <= KOKO_H
        if ok and ans is None:
            ans = k
        i = k - 1
        s.t(x0 + i * w + w / 2, y + 16, k, 12, SUB, "middle")
        s.cell(x0 + i * w, y + 28, w - 2, 30, hrs, "norm")
        s.cell(x0 + i * w, y + 66, w - 2, 30, "True" if ok else "False", "new" if ok else "gone", ring=(k == ans), size=12)
    assert ans == 4
    s.sep(y + 114)
    s.t(20, y + 138, "k = 3: hours = ceil(3/3) + ceil(6/3) + ceil(7/3) + ceil(11/3) = 1 + 2 + 3 + 4 = 10 > 8 → False", 14, INK)
    s.t(20, y + 162, "k = 4: hours = ceil(3/4) + ceil(6/4) + ceil(7/4) + ceil(11/4) = 1 + 2 + 2 + 3 = 8 <= 8 → True", 14, INK)
    s.t(20, y + 192, "答案 = 第一个 True = 4。不需要 piles sorted: 单调的是 k 和 hours 的关系, 不是输入数组。", 14, INK)
    s.t(20, y + 216, "k 的范围: 最小 1; 最大 max(piles) = 11 (再快也是一小时吃一堆), 所以搜 [1, 11]。", 12, SUB)
    s.legend(y + 250, [("new", False, "feasible = True"), ("gone", False, "feasible = False"), (None, True, "答案")])
    s.save("koko_core.svg", y + 274)


def fig_koko_trace():
    ans, st = trace_first_true(1, 12, lambda k: sum(koko_hours(k)) <= KOKO_H)
    assert ans == 4
    steps = []
    for x in st:
        m = x["mid"]
        hs = koko_hours(m)
        tot = sum(hs)
        expr = " + ".join(str(v) for v in hs)
        lines = [("k = %d: hours = %s = %d" % (m, expr, tot), 14, INK),
                 ("%d %s h = 8 → %s" % (tot, "<=" if x["r"] else ">", x["r"]), 14, INK)]
        if x["r"]:
            lines.append(("hi = mid = %d (答案 <= %d)" % (m, m), 12, DISCARD_TXT))
        else:
            lines.append(("lo = mid + 1 = %d (答案 > %d)" % (m + 1, m), 12, DISCARD_TXT))
        steps.append(dict(x, lines=lines))
    steps.append(dict(lo=ans, hi=ans, mid=None, lines=[("lo == hi == 4", 14, OK_TXT), ("最小速度 = 4", 14, OK_TXT)], ans=ans))
    s, y = space_trace("", "koko trace", "piles = [3, 6, 7, 11], h = 8 · 搜 k ∈ [1, 11], 每步: 算 hours(mid) 和 h 比",
                       "hours 里每一项 = ceil(pile / mid), 灰色 = 还在 [lo, hi) 里, 红色 = 已排除",
                       1, 12, steps, [("min speed = 4", 16, INK)],
                       [("norm", False, "仍在 [lo, hi) 里"), ("gone", False, "已排除"), (None, True, "mid")])
    s.save("koko_trace.svg", y)


# ---------------- Capacity
SHIP_W, SHIP_D = list(range(1, 11)), 5


def ship_groups(cap):
    groups, cur = [], []
    for w in SHIP_W:
        if sum(cur) + w > cap:
            groups.append(cur)
            cur = []
        cur.append(w)
    groups.append(cur)
    return groups


def group_expr(g):
    return " + ".join(map(str, g)) + (" = %d" % sum(g) if len(g) > 1 else "")


def fig_ship_core():
    s = Svg("capacity 的贪心 feasible", "从左到右装, 装不下就另起一天, 数天数")
    header(s, "weights = [1..10] (必须按顺序装), days = 5 · feasible(cap) = 贪心装完用的天数 <= days",
           "贪心: 今天装得下就装, 装不下才开新的一天 (对固定 cap 这样天数最少)")
    x0, w = 40, 60
    y = 58
    for cap, tag in ((14, "cap = 14"), (15, "cap = 15")):
        gs = ship_groups(cap)
        s.t(20, y + 16, tag + ": 装 %d 天" % len(gs) + (" > days = 5 → False" if len(gs) > 5 else " <= days = 5 → True"), 14, INK, bold=True)
        for i, v in enumerate(SHIP_W):
            s.cell(x0 + i * w, y + 28, w - 4, 28, v, "norm")
        pos = 0
        for di, g in enumerate(gs):
            gx = x0 + pos * w
            gw = len(g) * w - 4
            s.rect(gx, y + 64, gw, 26, "#E1F5EE", "#0F6E56", 1, 4)
            s.t(gx + gw / 2, y + 82, group_expr(g), 12, OK_TXT, "middle")
            s.t(gx + gw / 2, y + 106, "第 %d 天" % (di + 1), 12, SUB, "middle")
            pos += len(g)
        y += 124
        s.sep(y)
        y += 8
    s.t(20, y + 20, "cap = 14: 1+2+3+4 = 10, 再装 5 = 15 > 14, 另起一天; 最后被迫装成 6 天 → False。", 12, SUB)
    s.t(20, y + 40, "cap = 15: 1+2+3+4+5 = 15 刚好装满, 后面 6+7, 8, 9, 10 共 5 天 → True。", 12, SUB)
    s.t(20, y + 66, "cap 变大, 每天只会装得更多, 天数不会变多: feasible 单调, 答案 = 15。", 14, INK)
    s.t(20, y + 88, "cap 范围: 下限 max(weights) = 10 (最重的包裹必须装得下), 上限 sum = 55 (一天全装)。", 12, SUB)
    s.save("ship_core.svg", y + 104)


def fig_ship_trace():
    lo0, hi0 = max(SHIP_W), sum(SHIP_W) + 1
    ans, st = trace_first_true(lo0, hi0, lambda c: len(ship_groups(c)) <= SHIP_D)
    assert ans == 15
    steps = []
    for x in st:
        m = x["mid"]
        gs = ship_groups(m)
        txt = " | ".join(group_expr(g) for g in gs)
        # 分成最多两行, 每行 <= 44 字符
        l1, l2 = "", ""
        parts = [group_expr(g) for g in gs]
        cur = ""
        rows = []
        for p in parts:
            if cur and len(cur) + 3 + len(p) > 40:
                rows.append(cur)
                cur = p
            else:
                cur = p if not cur else cur + " | " + p
        rows.append(cur)
        lines = [("cap = %d: %s" % (m, rows[0]) if len(rows) == 1 else "cap = %d:" % m, 12, SUB)]
        if len(rows) > 1:
            lines = [("cap = %d: %s" % (m, rows[0]), 12, SUB)] + [(r, 12, SUB) for r in rows[1:]]
        lines.append(("%d 天 %s days = 5 → %s" % (len(gs), "<=" if x["r"] else ">", x["r"]), 14, INK))
        lines.append(("hi = mid = %d" % m if x["r"] else "lo = mid + 1 = %d" % (m + 1), 12, DISCARD_TXT))
        steps.append(dict(x, lines=lines, h=max(84, 26 + 19 * len(lines) + 10)))
    steps.append(dict(lo=ans, hi=ans, mid=None, lines=[("lo == hi == 15", 14, OK_TXT), ("最小载重 = 15", 14, OK_TXT)], ans=ans))
    s, y = space_trace("", "ship trace", "weights = [1..10], days = 5 · 搜 cap ∈ [10, 55] · 每步: 贪心分组, 数天数 (一个 | 是一天)",
                       "每组写出具体的相加: 1 + 2 + 3 = 6 表示这一天装了 1, 2, 3 三个包裹, 共 6",
                       lo0, hi0, steps, [("min capacity = 15", 16, INK)],
                       [("norm", False, "仍在 [lo, hi) 里"), ("gone", False, "已排除"), (None, True, "mid")])
    s.save("ship_trace.svg", y)


# ---------------- Split array
SPL_N, SPL_K = [7, 2, 5, 10, 8], 2


def split_groups(x):
    groups, cur = [], []
    for v in SPL_N:
        if sum(cur) + v > x:
            groups.append(cur)
            cur = []
        cur.append(v)
    groups.append(cur)
    return groups


def fig_split_core():
    s = Svg("split array 的 feasible", "和 Capacity 同一个 feasible")
    header(s, "nums = [7, 2, 5, 10, 8], k = 2 · 切成 k 段, 让 \"最大的那段和\" 尽量小 (最小的最大值)",
           "反过来问: 每段和 <= x 的话, 最少要切几段? 如果 <= k 段, x 就是 feasible")
    x0, w = 60, 100
    y = 58
    for x, in ((17,), (18,)):
        gs = split_groups(x)
        ok = len(gs) <= SPL_K
        s.t(20, y + 16, "x = %d: 切成 %d 段 %s k = 2 → %s" % (x, len(gs), "<=" if ok else ">", ok), 14, INK, bold=True)
        for i, v in enumerate(SPL_N):
            s.cell(x0 + i * w, y + 28, w - 6, 28, v, "norm")
        pos = 0
        for gi, g in enumerate(gs):
            gx = x0 + pos * w
            gw = len(g) * w - 6
            s.rect(gx, y + 64, gw, 26, "#E1F5EE", "#0F6E56", 1, 4)
            s.t(gx + gw / 2, y + 82, group_expr(g), 12, OK_TXT, "middle")
            s.t(gx + gw / 2, y + 106, "第 %d 段" % (gi + 1), 12, SUB, "middle")
            pos += len(g)
        y += 124
        s.sep(y)
        y += 8
    s.t(20, y + 20, "x = 17: 7 + 2 + 5 = 14, 再加 10 = 24 > 17, 另起一段; 10 + 8 = 18 > 17, 再起一段 → 3 段 → False。", 12, SUB)
    s.t(20, y + 40, "x = 18: 7 + 2 + 5 = 14, 10 + 8 = 18 <= 18 → 2 段 → True。", 12, SUB)
    s.t(20, y + 66, "x 越大, 每段能装更多, 段数不会变多: 单调。答案 = 18。", 14, INK)
    s.t(20, y + 88, "x 范围: 下限 max(nums) = 10, 上限 sum = 32。feasible 的写法和 Capacity 逐行相同 (days → k, cap → x)。", 12, SUB)
    s.save("split_core.svg", y + 104)


def fig_split_trace():
    lo0, hi0 = max(SPL_N), sum(SPL_N) + 1
    ans, st = trace_first_true(lo0, hi0, lambda x: len(split_groups(x)) <= SPL_K)
    assert ans == 18
    steps = []
    for x in st:
        m = x["mid"]
        gs = split_groups(m)
        parts = [group_expr(g) for g in gs]
        lines = [("x = %d:" % m, 12, SUB)]
        lines[0] = ("x = %d: %s" % (m, " | ".join(parts)), 12, SUB)
        lines.append(("%d 段 %s k = 2 → %s" % (len(gs), "<=" if x["r"] else ">", x["r"]), 14, INK))
        lines.append(("hi = mid = %d" % m if x["r"] else "lo = mid + 1 = %d" % (m + 1), 12, DISCARD_TXT))
        steps.append(dict(x, lines=lines))
    steps.append(dict(lo=ans, hi=ans, mid=None, lines=[("lo == hi == 18", 14, OK_TXT), ("最小的最大段和 = 18", 14, OK_TXT)], ans=ans))
    s, y = space_trace("", "split trace", "nums = [7, 2, 5, 10, 8], k = 2 · 搜 x ∈ [10, 32] · 每步: 贪心切段, 一个 | 是一段",
                       "每段写出具体的相加: 7 + 2 + 5 = 14 表示这一段是 7, 2, 5, 和为 14",
                       lo0, hi0, steps, [("min largest sum = 18", 16, INK)],
                       [("norm", False, "仍在 [lo, hi) 里"), ("gone", False, "已排除"), (None, True, "mid")])
    s.save("split_trace.svg", y)


# ---------------- 2D matrix
MAT = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
MAT_T = 11


def fig_matrix_core():
    m, n = 3, 4
    flat = [v for r in MAT for v in r]
    s = Svg("2D 当 1D", "行优先拼接后是 sorted 数组, 下标 i 对应 (i // n, i % n)")
    header(s, "每行 sorted, 且每行第一个数 > 上一行最后一个数 → 按行拼起来就是一个 sorted 的长数组",
           "不用真的拼: 下标 i 对应 matrix[i // n][i % n], n = 列数 = 4")
    gx, gy, cw, ch = 40, 66, 56, 46
    for r in range(m):
        for c in range(n):
            i = r * n + c
            x, y = gx + c * cw, gy + r * ch
            f, st, tx = ROLE["norm"]
            s.rect(x, y, cw - 2, ch - 2, f, st, 1, 4)
            if i == 5:
                s.rect(x - 3, y - 3, cw + 4, ch + 4, "none", RING, 2.5, 6)
            s.t(x + 6, y + 14, "i=%d" % i, 12, SUB)
            s.t(x + cw / 2 - 1, y + 35, MAT[r][c], 16, tx, "middle")
    s.t(gx, gy + m * ch + 16, "matrix (3 行 x 4 列)", 12, SUB)
    fx, fw = 290, 29
    s.t(fx, gy + 4, "拼成一维 (只是想象, 不用真建)", 12, SUB)
    for i, v in enumerate(flat):
        s.cell(fx + i * fw - (0), gy + 16 + (0), fw - 2, 30, v, "norm", ring=(i == 5), size=12)
        s.t(fx + i * fw + fw / 2 - 1, gy + 62, i, 12, SUB, "middle")
    s.t(fx, gy + 84, "mid = 5 的例子:", 14, INK, bold=True)
    s.t(fx, gy + 106, "row = 5 // 4 = 1", 14, INK)
    s.t(fx, gy + 128, "col = 5 % 4 = 1", 14, INK)
    s.t(fx, gy + 150, "matrix[1][1] = 11 = flat[5]", 14, INK)
    y = gy + m * ch + 40
    s.sep(y)
    s.t(20, y + 26, "二分的对象从 \"数组\" 换成 \"下标 0..m*n-1\", 其余和 first_true 完全一样。", 14, INK)
    s.t(20, y + 48, "pred(i) = matrix[i // n][i % n] >= target, 仍是 False...False True...True。", 12, SUB)
    s.save("matrix_core.svg", y + 70)


def fig_matrix_trace():
    flat = [v for r in MAT for v in r]
    n = 4
    M = len(flat)
    ans, st = trace_first_true(0, M, lambda i: flat[i] >= MAT_T)
    assert ans == 5 and flat[ans] == MAT_T
    steps = []
    for x in st:
        m = x["mid"]
        r, c = divmod(m, n)
        lines = [("matrix[%d][%d] = %d" % (r, c, MAT[r][c]), 14, INK),
                 ("%d >= %d → %s" % (MAT[r][c], MAT_T, x["r"]), 14, INK),
                 (("hi = mid = %d" % m) if x["r"] else ("lo = mid + 1 = %d" % (m + 1)), 12, DISCARD_TXT)]
        steps.append(dict(lo=x["lo"], hi=x["hi"], mid=m, lines=lines))
    steps.append(dict(lo=ans, hi=ans, mid=None, ans=ans, h=60,
                      lines=[("lo == hi == %d" % ans, 14, OK_TXT), ("matrix[1][1] = 11 == target", 14, OK_TXT)]))
    s, y = array_trace("", "matrix trace", "target = 11 · 数组是 matrix 按行拼接的 12 个数 · mid → (mid // 4, mid % 4)",
                       "pred(i) = matrix[i // 4][i % 4] >= 11", flat, [(None, steps)], GRAY_LEG, cw=28, ax=128,
                       right_head="mid 对应哪格 → 比较 → 动作")
    y = finish_with_legend(s, y, GRAY_LEG, [("lo = 5, matrix[5 // 4][5 % 4] = matrix[1][1] = 11 == 11 → True", 14, INK)])
    s.save("matrix_trace.svg", y)


# ---------------- Median
MA, MB = [1, 3, 8, 9, 15], [7, 11, 18, 19, 21, 25]


def fig_median_core():
    A, B = MA, MB
    m, n = len(A), len(B)
    half = (m + n + 1) // 2
    i = 4
    j = half - i
    s = Svg("median 的分割点", "在较短数组上二分 A 里取几个放左半")
    header(s, "A = [1, 3, 8, 9, 15], B = [7, 11, 18, 19, 21, 25] · m + n = 11 · 左半放 half = (11 + 1) // 2 = 6 个",
           "二分的是分割点 i (A 里放 i 个进左半), B 里放 j = half - i 个进左半")
    cw = 52
    ax = 60
    y = 60

    def row(y, arr, cut, label, hl):
        s.t(20, y + 24, label, 14, INK, bold=True)
        for k, v in enumerate(arr):
            s.cell(ax + k * cw + (6 if k >= cut else 0), y + 8, cw - 4, 30, v,
                   "new" if k < cut else "norm", ring=(k in hl))
        cx = ax + cut * cw + 1
        s.line(cx, y, cx, y + 46, "#993C1D", 2, "5 3")
    row(y, A, i, "A", {i - 1, i})
    row(y + 64, B, j, "B", {j - 1, j})
    s.t(ax, y + 128, "绿色 = 左半 (A 取 i = 4 个, B 取 j = 6 - 4 = 2 个, 共 6 个) · 虚线 = 分割线", 12, SUB)
    s.sep(y + 142)
    yy = y + 168
    s.t(20, yy, "分割对不对, 只看分割线两侧紧挨着的 4 个数 (圈出来的):", 14, INK, bold=True)
    s.t(20, yy + 26, "A[i-1] = 9 <= B[j] = 18   且   B[j-1] = 11 <= A[i] = 15", 14, INK)
    s.t(20, yy + 48, "两个数组各自本来就 sorted, 所以只要交叉的两个比较成立, 左半的每个数 <= 右半的每个数。", 12, SUB)
    s.t(20, yy + 74, "对了就结束: 11 个数, 奇数个 → 中位数 = 左半最大 = max(A[i-1], B[j-1]) = max(9, 11) = 11。", 14, INK)
    s.t(20, yy + 96, "偶数个则 = (左半最大 + 右半最小) / 2。", 12, SUB)
    s.t(20, yy + 124, "i 切小了 (A[i] < B[j-1]) → 把 i 调大; 切大了 → 调小。这是对 i 的二分, 范围 [0, m]。", 12, SUB)
    s.save("median_core.svg", yy + 142)


def fig_median_trace():
    A, B = MA, MB
    m, n = len(A), len(B)
    half = (m + n + 1) // 2
    lo0 = max(0, half - n)
    pred = lambda i: i == m or A[i] >= B[half - i - 1]
    ans, st = trace_first_true(lo0, m + 1, pred)
    assert ans == 4
    steps = []
    for x in st:
        i = x["mid"]
        j = half - i
        if i == m:
            lines = [("i = %d = m, j = %d - %d = %d" % (i, half, i, j), 12, SUB),
                     ("A 全部进左半, 不用比 → True", 14, INK),
                     ("hi = mid = %d" % i, 12, DISCARD_TXT)]
        else:
            lines = [("i = %d, j = %d - %d = %d" % (i, half, i, j), 12, SUB),
                     ("A[%d] = %d >= B[%d] = %d → %s" % (i, A[i], j - 1, B[j - 1], x["r"]), 14, INK),
                     (("hi = mid = %d" % i) if x["r"] else ("lo = mid + 1 = %d (A 取少了)" % (i + 1)), 12, DISCARD_TXT)]
        steps.append(dict(x, lines=lines))
    steps.append(dict(lo=ans, hi=ans, mid=None, ans=ans,
                      lines=[("i = 4, j = 2", 14, OK_TXT),
                             ("左半 = 1, 3, 8, 9 + 7, 11 (6 个)", 12, OK_TXT),
                             ("max(9, 11) = 11", 14, OK_TXT)]))
    s, y = space_trace("", "median trace", "A = [1, 3, 8, 9, 15], B = [7, 11, 18, 19, 21, 25] · half = 6 · 搜 i ∈ [0, 5] (i = 5 当作 True)",
                       "pred(i) = A[i] >= B[j-1] (j = half - i): 切小了是 False, 够了是 True",
                       lo0, m + 1, steps, [("median = 11", 16, INK)],
                       [("norm", False, "仍在 [lo, hi) 里"), ("gone", False, "已排除"), (None, True, "mid = i")])
    s.save("median_trace.svg", y)


def make_figs():
    fig_s0_core()
    fig_first_last_core()
    fig_first_last_trace()
    fig_find_min_core()
    fig_find_min_trace()
    fig_rotated_core()
    fig_rotated_trace()
    fig_peak_core()
    fig_peak_trace()
    fig_koko_core()
    fig_koko_trace()
    fig_ship_core()
    fig_ship_trace()
    fig_split_core()
    fig_split_trace()
    fig_matrix_core()
    fig_matrix_trace()
    fig_median_core()
    fig_median_trace()


# ============================================================ 自测
def selftest():
    import bisect
    import random
    ns = load_code()
    ft = ns["first_true"]
    rnd = random.Random(5)
    for _ in range(3000):
        n = rnd.randint(0, 12)
        a = sorted(rnd.randint(0, 8) for _ in range(n))
        x = rnd.randint(-1, 9)
        assert ft(0, n, lambda i: a[i] >= x) == bisect.bisect_left(a, x)
        assert ft(0, n, lambda i: a[i] > x) == bisect.bisect_right(a, x)
        exp = [i for i, v in enumerate(a) if v == x]
        assert ns["search_range"](a, x) == ([exp[0], exp[-1]] if exp else [-1, -1])
        if n:
            assert bisect.bisect_left(range(0, n), True, key=lambda i: a[i] >= x) == bisect.bisect_left(a, x)
        # 旋转
        if n:
            b = sorted(set(a))
            r = rnd.randrange(len(b))
            rot = b[r:] + b[:r]
            assert ns["find_min"](rot) == b[0]
            for t in range(-1, 10):
                assert ns["search"](rot, t) == (rot.index(t) if t in rot else -1)
        # peak
        pk = []
        while len(pk) < max(n, 1):
            v = rnd.randint(0, 20)
            if not pk or pk[-1] != v:
                pk.append(v)
        i = ns["find_peak"](pk)
        assert (i == 0 or pk[i - 1] < pk[i]) and (i == len(pk) - 1 or pk[i] > pk[i + 1])
    # answer-space
    import math
    for _ in range(1500):
        piles = [rnd.randint(1, 15) for _ in range(rnd.randint(1, 6))]
        h = rnd.randint(len(piles), len(piles) + 12)
        exp = next(k for k in range(1, max(piles) + 1) if sum(math.ceil(p / k) for p in piles) <= h)
        assert ns["min_eating_speed"](piles, h) == exp
        w = [rnd.randint(1, 9) for _ in range(rnd.randint(1, 7))]
        dd = rnd.randint(1, len(w))
        assert ns["ship_within_days"](w, dd) == next(c for c in range(max(w), sum(w) + 1) if len(_greedy(w, c)) <= dd)
        assert ns["split_array"](w, dd) == _brute_split(w, dd)
    # last_true
    assert ns["last_true"](0, 10, lambda x: x * x <= 50) == 7
    assert ns["last_true"](0, 10, lambda x: False) == -1
    # matrix
    for _ in range(1500):
        mm, nn = rnd.randint(1, 4), rnd.randint(1, 4)
        vals = sorted(rnd.sample(range(0, 40), mm * nn))
        mat = [vals[r * nn:(r + 1) * nn] for r in range(mm)]
        t = rnd.randint(-1, 41)
        assert ns["search_matrix"](mat, t) == (t in vals)
    # median
    for _ in range(4000):
        A = sorted(rnd.randint(0, 20) for _ in range(rnd.randint(0, 7)))
        B = sorted(rnd.randint(0, 20) for _ in range(rnd.randint(0, 7)))
        if not A and not B:
            continue
        c = sorted(A + B)
        L = len(c)
        exp = c[L // 2] if L % 2 else (c[L // 2 - 1] + c[L // 2]) / 2
        assert ns["find_median"](A, B) == exp, (A, B)
    # 文档例子
    assert ns["search_range"]([5, 7, 7, 8, 8, 8, 10, 12], 8) == [3, 5]
    assert ns["find_min"]([4, 5, 6, 7, 8, 9, 1, 2, 3]) == 1
    assert ns["search"]([4, 5, 6, 7, 8, 9, 1, 2, 3], 3) == 8
    assert ns["find_peak"](PEAK) == 7
    assert ns["min_eating_speed"](KOKO_P, KOKO_H) == 4
    assert ns["ship_within_days"](SHIP_W, SHIP_D) == 15
    assert ns["split_array"](SPL_N, SPL_K) == 18
    assert ns["search_matrix"](MAT, 11) is True and ns["search_matrix"](MAT, 13) is False
    assert ns["find_median"](MA, MB) == 11
    print("selftest ok")


def _greedy(w, cap):
    gs, cur = [], 0
    n = 1
    for x in w:
        if cur + x > cap:
            n += 1
            cur = 0
        cur += x
    return [0] * n


def _brute_split(nums, k):
    from functools import lru_cache
    n = len(nums)

    @lru_cache(None)
    def f(i, parts):
        if parts == 1:
            return sum(nums[i:])
        best = float("inf")
        for j in range(i + 1, n - parts + 2):
            best = min(best, max(sum(nums[i:j]), f(j, parts - 1)))
        return best
    k = min(k, n)
    # 段数可以 < k 时答案不会更小, 取 <= k 段的最小
    return min(f(0, p) for p in range(1, k + 1))


# ============================================================ 文档
def build_doc():
    g = dict(globals())
    exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "05_binary_search_doc.py"), encoding="utf-8").read(), g)
    return g["doc"]


if __name__ == "__main__":
    selftest()
    make_figs()
    doc = build_doc()
    doc.write("docs/%s.html" % SLUG)
    print("wrote docs/%s.html" % SLUG)
