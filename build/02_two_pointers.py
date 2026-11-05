"""02 · Two Pointers  —  生成 docs/02-two-pointers.html 和 docs/svg/02-two-pointers/*.svg

运行: cd build && python3 -I 02_two_pointers.py

结构:
  1. CODE: 文档里展示的每段代码都是字符串, 这里 exec 之后和 brute force 对拍。
  2. TRACE: 用和 CODE 同样逻辑的 instrumented 版本, 打印每一步状态并直接生成 trace 图,
     最后 assert 它的结果 == CODE 的结果, 所以图里的数字就是跑出来的数字。
  3. SVG helper + 每张图。
  4. 文档正文。
"""
import html
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import doclib as d  # noqa: E402

SLUG = "02-two-pointers"
SVG_DIR = os.path.join(d.ROOT, "docs", "svg", SLUG)
os.makedirs(SVG_DIR, exist_ok=True)

# ----------------------------------------------------------------------------
# 1. 代码 (展示用 = 测试用)
# ----------------------------------------------------------------------------
CODE = {}

CODE["two_sum"] = '''
def two_sum_sorted(nums, target):          # nums 已排序
    l, r = 0, len(nums) - 1
    while l < r:
        s = nums[l] + nums[r]
        if s == target:
            return [l, r]                  # LeetCode 167 要求 1-indexed, 返回时各 +1
        if s < target:
            l += 1     # nums[l] 配 r 以及 r 左边所有数, 和都 <= s < target -> l 没用了
        else:
            r -= 1     # nums[r] 配 l 以及 l 右边所有数, 和都 >= s > target -> r 没用了
    return []
'''

CODE["three_sum"] = '''
def three_sum(nums):
    nums.sort()                                      # 排序 O(n log n), 换来 "能丢一批"
    res = []
    for i in range(len(nums) - 2):
        if nums[i] > 0:
            break                                    # 最小的数都 > 0, 和不可能 = 0
        if i > 0 and nums[i] == nums[i - 1]:
            continue                                 # 去重 1: 同一个值只当一次 i
        l, r = i + 1, len(nums) - 1                  # 里层 = Two Sum II
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if s < 0:
                l += 1
            elif s > 0:
                r -= 1
            else:
                res.append([nums[i], nums[l], nums[r]])
                l += 1
                r -= 1
                while l < r and nums[l] == nums[l - 1]:   # 去重 2: l 跳过同值
                    l += 1
                while l < r and nums[r] == nums[r + 1]:   # 去重 2: r 跳过同值
                    r -= 1
    return res
'''

CODE["container"] = '''
def max_area(height):
    l, r = 0, len(height) - 1
    best = 0
    while l < r:
        h = min(height[l], height[r])          # 水位由矮的那面墙决定
        best = max(best, h * (r - l))          # 面积 = 水位 x 宽度
        if height[l] < height[r]:
            l += 1     # 矮墙 l: 宽度只会更小, 高度仍 <= height[l] -> l 不可能更好, 丢掉
        else:
            r -= 1     # 矮墙 r (或一样高): 同理丢 r
    return best
'''

CODE["trap"] = '''
def trap(height):
    l, r = 0, len(height) - 1
    # lmax = height[0..l] 的最大值, rmax = height[r..n-1] 的最大值
    lmax, rmax = height[l], height[r]
    water = 0
    while l < r:
        if lmax < rmax:
            # 右边至少有 rmax 比 lmax 高 -> min(左最高, 右最高) 一定是 lmax
            l += 1
            lmax = max(lmax, height[l])
            water += lmax - height[l]      # 这一格的水 = lmax - h (h 是新高则为 0)
        else:
            r -= 1                         # 对称: 左边至少有 lmax >= rmax
            rmax = max(rmax, height[r])
            water += rmax - height[r]
    return water
'''

CODE["move_zeroes"] = '''
def move_zeroes(nums):
    w = 0                                  # w = 下一个要写入 "非零" 的位置
    for r in range(len(nums)):             # r = 读到哪了
        if nums[r] != 0:
            # 非零放到 w; 原来在 w 的一定是 0 (或 w == r)
            nums[w], nums[r] = nums[r], nums[w]
            w += 1
    # invariant: nums[:w] 全是非零 (相对顺序不变), nums[w:r] 全是 0
'''

CODE["remove_dup"] = '''
def remove_duplicates(nums):
    if not nums:
        return 0
    w = 1                                  # nums[:w] 是 "已读部分去重后的结果"
    for r in range(1, len(nums)):
        if nums[r] != nums[w - 1]:         # 重复的一定挨着, 只和 "最后保留的" 比
            nums[w] = nums[r]
            w += 1
    return w                               # 新长度; nums[:w] 就是答案
'''

CODE["remove_dup_k"] = '''
def remove_duplicates_k(nums, k=2):        # Remove Duplicates II: 每个值最多保留 k 个
    w = 0
    for x in nums:
        if w < k or x != nums[w - k]:      # 只改这一行: 和 "倒数第 k 个保留的" 比
            nums[w] = x
            w += 1
    return w
'''

CODE["sort_colors"] = '''
def sort_colors(nums):
    lo, i, hi = 0, 0, len(nums) - 1
    # [0, lo) 全是 0 | [lo, i) 全是 1 | [i, hi] 未知 | (hi, n) 全是 2
    while i <= hi:
        if nums[i] == 0:
            # 换过来的是 1 (在 [lo, i) 里), 已经看过, 所以 i 可以前进
            nums[lo], nums[i] = nums[i], nums[lo]
            lo += 1
            i += 1
        elif nums[i] == 2:
            # 换过来的是 "未知" 区的数, 还没看过 -> i 不动
            nums[i], nums[hi] = nums[hi], nums[i]
            hi -= 1
        else:
            i += 1
'''

CODE["merge"] = '''
def merge(nums1, m, nums2, n):             # nums1 长度 m + n, 后 n 格是空位
    # i: nums1 最后一个有效数, j: nums2 最后一个数, k: 写入位置
    i, j, k = m - 1, n - 1, m + n - 1
    while j >= 0:                          # nums2 用完就结束, nums1 剩下的本来就在原位
        if i >= 0 and nums1[i] > nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1                             # k 永远 >= i, 不会盖掉没读的 nums1
'''

CODE["palin"] = '''
def is_palindrome(s):
    l, r = 0, len(s) - 1
    while l < r:
        if not s[l].isalnum():
            l += 1                         # 跳过标点/空格
        elif not s[r].isalnum():
            r -= 1
        elif s[l].lower() != s[r].lower():
            return False
        else:
            l += 1
            r -= 1
    return True
'''

CODE["palin2"] = '''
def valid_palindrome_ii(s):                # 最多删掉一个字符
    def ok(l, r):                          # s[l..r] 本身是不是回文 (就是上面那个循环)
        while l < r:
            if s[l] != s[r]:
                return False
            l += 1
            r -= 1
        return True

    l, r = 0, len(s) - 1
    while l < r:
        if s[l] != s[r]:                   # 第一次失配: 只有两种删法, 删 s[l] 或删 s[r]
            return ok(l + 1, r) or ok(l, r - 1)
        l += 1
        r -= 1
    return True
'''

NS = {}
for _k, _src in CODE.items():
    exec(_src, NS)


def brute_two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return True
    return False


def brute_3sum(nums):
    s = set()
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if nums[i] + nums[j] + nums[k] == 0:
                    s.add(tuple(sorted((nums[i], nums[j], nums[k]))))
    return s


def brute_area(h):
    return max(min(h[i], h[j]) * (j - i) for i in range(len(h)) for j in range(i + 1, len(h)))


def brute_trap(h):
    return sum(max(0, min(max(h[:i + 1]), max(h[i:])) - h[i]) for i in range(len(h)))


def brute_pal2(s):
    if s == s[::-1]:
        return True
    return any((s[:i] + s[i + 1:]) == (s[:i] + s[i + 1:])[::-1] for i in range(len(s)))


def run_tests():
    random.seed(7)
    for _ in range(3000):
        n = random.randint(2, 9)
        a = sorted(random.randint(-5, 9) for _ in range(n))
        t = random.randint(-5, 15)
        r = NS["two_sum_sorted"](a, t)
        assert bool(r) == brute_two_sum(a, t)
        if r:
            assert r[0] < r[1] and a[r[0]] + a[r[1]] == t
        a = [random.randint(-4, 4) for _ in range(random.randint(0, 9))]
        got = NS["three_sum"](list(a))
        assert len(got) == len(set(map(tuple, got))), "3sum 有重复"
        assert set(map(tuple, got)) == brute_3sum(a), a
        h = [random.randint(0, 6) for _ in range(random.randint(2, 9))]
        assert NS["max_area"](h) == brute_area(h)
        assert NS["trap"](h) == brute_trap(h)
        a = [random.randint(0, 3) for _ in range(random.randint(0, 9))]
        b = list(a)
        NS["move_zeroes"](b)
        assert b == [x for x in a if x] + [0] * a.count(0)
        a = sorted(random.randint(0, 4) for _ in range(random.randint(0, 10)))
        b = list(a)
        w = NS["remove_duplicates"](b)
        assert b[:w] == sorted(set(a))
        for k in (1, 2, 3):
            b = list(a)
            w = NS["remove_duplicates_k"](b, k)
            exp = []
            for x in a:
                if exp.count(x) < k:
                    exp.append(x)
            assert b[:w] == exp
        a = [random.randint(0, 2) for _ in range(random.randint(0, 10))]
        b = list(a)
        NS["sort_colors"](b)
        assert b == sorted(a)
        m, n = random.randint(0, 5), random.randint(0, 5)
        a1 = sorted(random.randint(0, 9) for _ in range(m))
        a2 = sorted(random.randint(0, 9) for _ in range(n))
        b = a1 + [0] * n
        NS["merge"](b, m, list(a2), n)
        assert b == sorted(a1 + a2)
        s = "".join(random.choice("ab ,Ab") for _ in range(random.randint(0, 8)))
        t = [c.lower() for c in s if c.isalnum()]
        assert NS["is_palindrome"](s) == (t == t[::-1])
        s = "".join(random.choice("abc") for _ in range(random.randint(0, 8)))
        assert NS["valid_palindrome_ii"](s) == brute_pal2(s), s
    print("tests ok")


run_tests()

# ----------------------------------------------------------------------------
# 2. SVG helper (规则见 STYLE_GUIDE B)
# ----------------------------------------------------------------------------
FONT = 'ui-sans-serif, system-ui, -apple-system, "PingFang SC", sans-serif'
INK = "#0B0B0B"
INK2 = "#52514E"
SEP = "#B4B2A9"
ROLE = {
    "new": ("#E1F5EE", "#0F6E56", "#085041"),
    "gone": ("#FAECE7", "#993C1D", "#712B13"),
    "other": ("#F1EFE8", "#5F5E5A", "#444441"),
    "plain": ("#FFFFFF", "#B4B2A9", "#444441"),
}
RING = "#EF9F27"
RED_ARROW = "#D85A30"


def esc(s):
    return html.escape(str(s), quote=False)


class Svg:
    def __init__(self, w=680):
        self.w = w
        self.b = []

    def t(self, x, y, txt, size=12, fill=INK2, anchor="start", weight=400):
        self.b.append(
            '<text x="%s" y="%s" text-anchor="%s" dominant-baseline="central" '
            'font-size="%s" font-weight="%s" fill="%s">%s</text>'
            % (x, y, anchor, size, weight, fill, esc(txt)))

    def rect(self, x, y, w, h, role="other", rx=4, dash=False, sw=1):
        f, s, _ = ROLE[role]
        self.b.append(
            '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" '
            'stroke-width="%s"%s/>' % (x, y, w, h, rx, f, s, sw, ' stroke-dasharray="4 3"' if dash else ""))

    def ring(self, x, y, w, h):
        self.b.append(
            '<rect x="%s" y="%s" width="%s" height="%s" rx="6" fill="none" stroke="%s" stroke-width="2.5"/>'
            % (x - 3, y - 3, w + 6, h + 6, RING))

    def line(self, x1, y1, x2, y2, color=SEP, dash="4 4", sw=0.8):
        self.b.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s/>'
                      % (x1, y1, x2, y2, color, sw, ' stroke-dasharray="%s"' % dash if dash else ""))

    def path(self, dd, color=INK2, dash=False, arrow=True, sw=1.5):
        mk = ""
        if arrow:
            mk = ' marker-end="url(#%s)"' % ("arR" if color == RED_ARROW else "arG")
        self.b.append('<path d="%s" fill="none" stroke="%s" stroke-width="%s"%s%s/>'
                      % (dd, color, sw, ' stroke-dasharray="5 4"' if dash else "", mk))

    def tri(self, cx, y, color=INK):
        self.b.append('<path d="M%s %s L%s %s L%s %s Z" fill="%s"/>' % (cx, y, cx - 5, y + 8, cx + 5, y + 8, color))

    def cell(self, x, y, w, h, txt, role, size=14, ring=False):
        self.rect(x, y, w, h, role, rx=4, sw=1)
        self.t(x + w / 2, y + h / 2, txt, size, ROLE[role][2], "middle", 500)
        if ring:
            self.ring(x, y, w, h)

    def legend(self, y, items, x=40):
        """items: (role | 'ring', label)"""
        for kind, label in items:
            if kind == "ring":
                self.rect(x, y - 7, 14, 14, "plain", rx=3)
                self.ring(x, y - 7, 14, 14)
            else:
                self.rect(x, y - 7, 14, 14, kind, rx=3)
            self.t(x + 22, y, label, 12, INK2)
            x += 22 + 13 * len(label) + 18

    def out(self, h, title, desc, fname):
        head = ('<svg width="100%%" viewBox="0 0 %d %d" role="img" xmlns="http://www.w3.org/2000/svg" '
                'font-family=\'%s\'><title>%s</title><desc>%s</desc>'
                '<defs>'
                '<marker id="arG" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
                '<path d="M2 1L8 5L2 9" fill="none" stroke="%s" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>'
                '<marker id="arR" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
                '<path d="M2 1L8 5L2 9" fill="none" stroke="%s" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>'
                '</defs>' % (self.w, h, FONT, esc(title), esc(desc), INK2, RED_ARROW))
        s = head + "\n" + "\n".join(self.b) + "\n</svg>\n"
        with open(os.path.join(SVG_DIR, fname), "w", encoding="utf-8") as f:
            f.write(s)
        return h


LINE_STYLE = {
    "sub": (12, INK2, 400),
    "val": (14, INK, 500),
    "gone": (12, "#712B13", 400),
    "new": (12, "#085041", 400),
}


def draw_array(g, x, y, arr, cw=34, name=None, name_w=0):
    """arr: dict(cells=[(txt, role)], ptrs={idx: label}, rings=[idx], idx0=0)
    返回 block 高度 70。y 是 block 顶。"""
    cells = arr["cells"]
    ptrs = arr.get("ptrs", {})
    rings = set(arr.get("rings", []))
    x0 = x + name_w
    if name:
        g.t(x, y + 29, name, 12, INK2)
    for k, (txt, role) in enumerate(cells):
        cx = x0 + k * cw
        g.t(cx + cw / 2, y + 6, k, 12, "#898781", "middle")
        g.cell(cx, y + 14, cw - 2, 30, txt, role, ring=(k in rings))
    for k, lab in ptrs.items():
        cx = x0 + k * cw + (cw - 2) / 2
        g.tri(cx, y + 47)
        g.t(cx, y + 64, lab, 14, INK, "middle", 500)
    return 70


def trace_svg(fname, title, desc, top, heads, rows, final, legend, cw=34, name_w=0, notes_x=360, gap=14):
    """一行 = 一步。rows: dict(arrays=[...], lines=[(txt, kind)])"""
    g = Svg()
    for k, line in enumerate(top):
        g.t(40, 18 + 20 * k, line, 12, INK2)
    hy = 18 + 20 * len(top) + 12
    g.t(40, hy, heads[0], 12, INK2)
    g.t(notes_x, hy, heads[1], 12, INK2)
    y = hy + 10
    g.line(40, y, 640, y)
    y += 10
    for row in rows:
        yy = y
        for arr in row["arrays"]:
            draw_array(g, 40, yy, arr, cw, arr.get("name"), name_w)
            yy += 70 + (12 if len(row["arrays"]) > 1 else 0)
        bh = 70 * len(row["arrays"]) + (12 * len(row["arrays"]) if len(row["arrays"]) > 1 else 0)
        lines = row["lines"]
        ly = y + (bh - 18 * len(lines)) / 2 + 9 + (4 if len(row["arrays"]) == 1 else 0)
        for k, (txt, kind) in enumerate(lines):
            size, col, wt = LINE_STYLE[kind]
            g.t(notes_x, ly + 18 * k, txt, size, col, "start", wt)
        y += bh + gap
        g.line(40, y - gap / 2 - 2, 640, y - gap / 2 - 2)
    y += 8
    for k, line in enumerate(final):
        g.t(40, y + 20 * k, line, 14, INK, "start", 500)
    y += 20 * len(final) + 10
    g.legend(y + 6, legend)
    return g.out(int(y + 30), title, desc, fname)


def A(cells, ptrs=None, rings=(), name=None):
    return {"cells": cells, "ptrs": ptrs or {}, "rings": list(rings), "name": name}


# ----------------------------------------------------------------------------
# 3. Trace 数据 (instrumented, 和 CODE 逻辑一致, 并 assert 结果相同)
# ----------------------------------------------------------------------------
def trace_two_sum(nums, target):
    rows = []
    l, r = 0, len(nums) - 1
    while l < r:
        s = nums[l] + nums[r]
        cells = [(nums[k], "gone" if (k < l or k > r) else "other") for k in range(len(nums))]
        ptrs = {l: "l", r: "r"}
        print("  l=%d r=%d  %d + %d = %d  (target %d)" % (l, r, nums[l], nums[r], s, target))
        if s == target:
            cells[l] = (nums[l], "new")
            cells[r] = (nums[r], "new")
            rows.append(dict(arrays=[A(cells, ptrs, [l, r])], lines=[
                ("%d + %d = %d" % (nums[l], nums[r], s), "val"),
                ("== target = %d" % target, "sub"),
                ("找到, return [%d, %d]" % (l, r), "new")]))
            return rows, [l, r]
        if s < target:
            rows.append(dict(arrays=[A(cells, ptrs, [l, r])], lines=[
                ("%d + %d = %d" % (nums[l], nums[r], s), "val"),
                ("%d < target = %d  ->  l += 1" % (s, target), "sub"),
                ("丢掉 nums[%d] = %d:" % (l, nums[l]), "gone"),
                ("它配 r 及 r 左边的数, 和都 <= %d" % s, "gone")]))
            l += 1
        else:
            rows.append(dict(arrays=[A(cells, ptrs, [l, r])], lines=[
                ("%d + %d = %d" % (nums[l], nums[r], s), "val"),
                ("%d > target = %d  ->  r -= 1" % (s, target), "sub"),
                ("丢掉 nums[%d] = %d:" % (r, nums[r]), "gone"),
                ("它配 l 及 l 右边的数, 和都 >= %d" % s, "gone")]))
            r -= 1
    return rows, []


def trace_three_sum(nums):
    nums = sorted(nums)
    n = len(nums)
    rows, res = [], []

    def cells_for(i, l, r):
        out = []
        for k in range(n):
            if k < i:
                role = "plain"
            elif k == i:
                role = "new"
            elif k < l or k > r:
                role = "gone"
            else:
                role = "other"
            out.append((nums[k], role))
        return out

    for i in range(n - 2):
        if nums[i] > 0:
            break
        if i > 0 and nums[i] == nums[i - 1]:
            c = [(nums[k], "plain" if k < i else ("gone" if k == i else "other")) for k in range(n)]
            rows.append(dict(arrays=[A(c, {i: "i"}, [i])], lines=[
                ("nums[%d] = %d == nums[%d]" % (i, nums[i], i - 1), "val"),
                ("同一个值已经当过 \"第一个数\"", "sub"),
                ("continue, 跳过这个 i", "gone")]))
            print("  i=%d skip dup" % i)
            continue
        l, r = i + 1, n - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            print("  i=%d l=%d r=%d  %d + %d + %d = %d" % (i, l, r, nums[i], nums[l], nums[r], s))
            expr = "%d + %d + %d = %d" % (nums[i], nums[l], nums[r], s)
            c = cells_for(i, l, r)
            if s < 0:
                rows.append(dict(arrays=[A(c, {i: "i", l: "l", r: "r"}, [l, r])], lines=[
                    (expr, "val"), ("%d < 0  ->  l += 1" % s, "sub"),
                    ("丢掉 nums[%d] = %d" % (l, nums[l]), "gone")]))
                l += 1
            elif s > 0:
                rows.append(dict(arrays=[A(c, {i: "i", l: "l", r: "r"}, [l, r])], lines=[
                    (expr, "val"), ("%d > 0  ->  r -= 1" % s, "sub"),
                    ("丢掉 nums[%d] = %d" % (r, nums[r]), "gone")]))
                r -= 1
            else:
                triple = [nums[i], nums[l], nums[r]]
                res.append(triple)
                l0, r0 = l, r
                l += 1
                r -= 1
                while l < r and nums[l] == nums[l - 1]:
                    l += 1
                while l < r and nums[r] == nums[r + 1]:
                    r -= 1
                c2 = cells_for(i, l, r)
                c[l0] = (nums[l0], "new")
                c[r0] = (nums[r0], "new")
                rows.append(dict(arrays=[A(c, {i: "i", l0: "l", r0: "r"}, [l0, r0])], lines=[
                    (expr, "val"), ("== 0  ->  记录 %s" % triple, "new"),
                    ("然后 l += 1, r -= 1", "sub")]))
                dups = []
                if l != l0 + 1:
                    dups.append("l 跳过同值: %d -> %d" % (l0 + 1, l))
                if r != r0 - 1:
                    dups.append("r 跳过同值: %d -> %d" % (r0 - 1, r))
                if dups:
                    pass
                print("   found %s -> l=%d r=%d" % (triple, l, r))
                rows.append(dict(arrays=[A(c2, {i: "i", l: "l", r: "r"} if l != r else {i: "i", l: "l,r"},
                                           [l, r])], lines=[
                    ("l += 1 -> %d, r -= 1 -> %d" % (l0 + 1, r0 - 1), "sub"),
                    ("nums[%d] == nums[%d]: l 跳过 -> %d" % (l0 + 1, l0, l), "sub"),
                    ("l == r == %d, 里层结束" % l if l >= r else "继续", "val")]))
    return rows, res


def trace_container(h):
    n = len(h)
    rows = []
    l, r = 0, n - 1
    best = 0
    while l < r:
        m = min(h[l], h[r])
        area = m * (r - l)
        best = max(best, area)
        c = [(h[k], "gone" if (k < l or k > r) else "other") for k in range(n)]
        if h[l] < h[r]:
            move = "height[l] = %d < height[r] = %d  ->  l += 1" % (h[l], h[r])
            drop = "丢掉 l: 宽度只会 < %d, 高度 <= %d" % (r - l, h[l])
        else:
            move = "height[l] = %d >= height[r] = %d  ->  r -= 1" % (h[l], h[r])
            drop = "丢掉 r: 宽度只会 < %d, 高度 <= %d" % (r - l, h[r])
        print("  l=%d r=%d  min(%d,%d) x %d = %d  best=%d" % (l, r, h[l], h[r], r - l, area, best))
        rows.append(dict(arrays=[A(c, {l: "l", r: "r"}, [l, r])], lines=[
            ("min(%d, %d) x (%d - %d) = %d x %d = %d" % (h[l], h[r], r, l, m, r - l, area), "val"),
            ("best = %d" % best, "new" if area == best else "sub"),
            (move, "sub"), (drop, "gone")]))
        if h[l] < h[r]:
            l += 1
        else:
            r -= 1
    return rows, best


def trace_trap(h):
    n = len(h)
    rows = []
    l, r = 0, n - 1
    lmax, rmax = h[l], h[r]
    water = 0
    steps = []

    def cells(l, r, hl=None):
        out = []
        for k in range(n):
            role = "new" if k <= l or k >= r else "other"
            out.append((h[k], role))
        return out

    c = cells(l, r)
    rows.append(dict(arrays=[A(c, {l: "l", r: "r"}, [l, r])], lines=[
        ("开始: lmax = height[0] = %d" % lmax, "val"),
        ("rmax = height[%d] = %d" % (r, rmax), "val"),
        ("water = 0", "sub")]))
    print("  start l=%d r=%d lmax=%d rmax=%d" % (l, r, lmax, rmax))
    while l < r:
        if lmax < rmax:
            side = "l"
            l += 1
            lmax = max(lmax, h[l])
            add = lmax - h[l]
            water += add
            pos = l
            cond = "lmax = %d < rmax = %d  ->  l += 1" % (lmax if False else (lmax if h[l] <= lmax else lmax), rmax)
        else:
            side = "r"
            r -= 1
            rmax = max(rmax, h[r])
            add = rmax - h[r]
            water += add
            pos = r
        steps.append((side, pos, lmax, rmax, add, water))
        print("  %s -> pos=%d lmax=%d rmax=%d add=%d water=%d" % (side, pos, lmax, rmax, add, water))
    # 重新按步骤画 (需要每步 "比较前" 的 lmax/rmax)
    rows = rows[:1]
    l, r = 0, n - 1
    lm, rm = h[l], h[r]
    w = 0
    for side, pos, lmax2, rmax2, add, water2 in steps:
        if side == "l":
            cond = "lmax = %d < rmax = %d  ->  l += 1" % (lm, rm)
            l += 1
            newl = max(lm, h[l])
            line2 = "lmax = max(%d, height[%d] = %d) = %d" % (lm, l, h[l], newl)
            lm = newl
            line3 = "water += %d - %d = %d" % (lm, h[l], add)
        else:
            cond = "lmax = %d >= rmax = %d  ->  r -= 1" % (lm, rm)
            r -= 1
            newr = max(rm, h[r])
            line2 = "rmax = max(%d, height[%d] = %d) = %d" % (rm, r, h[r], newr)
            rm = newr
            line3 = "water += %d - %d = %d" % (rm, h[r], add)
        w += add
        c = cells(l, r)
        ptrs = {l: "l", r: "r"} if l != r else {l: "l,r"}
        rows.append(dict(arrays=[A(c, ptrs, [pos])], lines=[
            (cond, "sub"), (line2, "sub"), (line3, "val"), ("water = %d" % w, "new" if add else "sub")]))
    assert w == water
    return rows, water


def trace_move_zeroes(nums):
    nums = list(nums)
    n = len(nums)
    rows = []
    w = 0

    def cells(r):
        out = []
        for k in range(n):
            if k < w:
                role = "new"
            elif k < r:
                role = "gone"
            else:
                role = "plain"
            out.append((nums[k], role))
        return out

    for r in range(n):
        ptrs = {}
        if w == r:
            ptrs[w] = "w,r"
        else:
            ptrs[w] = "w"
            ptrs[r] = "r"
        c = cells(r)
        if nums[r] != 0:
            if w == r:
                lines = [("nums[%d] = %d != 0" % (r, nums[r]), "val"),
                         ("swap(nums[%d], nums[%d]) 是自己换自己" % (w, r), "sub"),
                         ("w += 1  ->  %d" % (w + 1), "new")]
            else:
                lines = [("nums[%d] = %d != 0" % (r, nums[r]), "val"),
                         ("swap(nums[w=%d], nums[r=%d])" % (w, r), "sub"),
                         ("nums[%d] = 0 被换到 r;  w += 1  ->  %d" % (w, w + 1), "new")]
            rows.append(dict(arrays=[A(c, ptrs, [r])], lines=lines))
            print("  r=%d w=%d %s -> swap" % (r, w, nums))
            nums[w], nums[r] = nums[r], nums[w]
            w += 1
        else:
            rows.append(dict(arrays=[A(c, ptrs, [r])], lines=[
                ("nums[%d] = 0" % r, "val"), ("不动, w 不变 (w = %d)" % w, "sub"),
                ("r += 1, 这个 0 留在 [w, r) 里", "gone")]))
            print("  r=%d w=%d %s -> skip" % (r, w, nums))
    c = [(nums[k], "new" if k < w else "gone") for k in range(n)]
    rows.append(dict(arrays=[A(c, {w: "w"} if w < n else {}, [])], lines=[
        ("r 走完, 结束", "val"), ("nums[:%d] 非零, 顺序没变" % w, "new"), ("nums[%d:] 全是 0" % w, "gone")]))
    print("  final", nums)
    return rows, nums


def trace_remove_dup(nums):
    nums = list(nums)
    n = len(nums)
    rows = []
    w = 1

    def cells(r):
        out = []
        for k in range(n):
            role = "new" if k < w else ("gone" if k < r else "plain")
            out.append((nums[k], role))
        return out

    for r in range(1, n):
        c = cells(r)
        ptrs = {w - 1: "w-1", r: "r"} if w - 1 != r else {r: "r"}
        if nums[r] != nums[w - 1]:
            lines = [("nums[r] = %d  vs  nums[w-1] = %d" % (nums[r], nums[w - 1]), "val"),
                     ("不同 -> 新的值", "sub"),
                     ("nums[w=%d] = %d;  w += 1  ->  %d" % (w, nums[r], w + 1), "new")]
            print("  r=%d w=%d %s write" % (r, w, nums))
            rows.append(dict(arrays=[A(c, ptrs, [r])], lines=lines))
            nums[w] = nums[r]
            w += 1
        else:
            lines = [("nums[r] = %d  vs  nums[w-1] = %d" % (nums[r], nums[w - 1]), "val"),
                     ("相同 -> 重复", "sub"),
                     ("跳过, w 不变 (w = %d)" % w, "gone")]
            print("  r=%d w=%d %s skip" % (r, w, nums))
            rows.append(dict(arrays=[A(c, ptrs, [r])], lines=lines))
    c = [(nums[k], "new" if k < w else "gone") for k in range(n)]
    rows.append(dict(arrays=[A(c, {w: "w"} if w < n else {}, [])], lines=[
        ("r 走完, return w = %d" % w, "val"), ("答案 = nums[:%d] = %s" % (w, nums[:w]), "new"),
        ("后面 %d 格是没用的残留" % (n - w), "gone")]))
    print("  final", nums, "w =", w)
    return rows, (w, nums)


def trace_sort_colors(nums):
    nums = list(nums)
    n = len(nums)
    rows = []
    lo, i, hi = 0, 0, n - 1

    def cells():
        out = []
        for k in range(n):
            if k < lo:
                role = "new"
            elif k < i:
                role = "other"
            elif k <= hi:
                role = "plain"
            else:
                role = "gone"
            out.append((nums[k], role))
        return out

    def ptrs():
        p = {}
        for name, v in (("lo", lo), ("i", i), ("hi", hi)):
            if 0 <= v < n:
                p[v] = (p[v] + "," + name) if v in p else name
        return p

    while i <= hi:
        c = cells()
        pt = ptrs()
        print("  lo=%d i=%d hi=%d %s" % (lo, i, hi, nums))
        if nums[i] == 0:
            same = (lo == i)
            lines = [("nums[i] = 0", "val"),
                     ("swap(nums[lo=%d], nums[i=%d])%s" % (lo, i, " (同一格)" if same else ""), "sub"),
                     ("lo += 1, i += 1", "new")]
            rows.append(dict(arrays=[A(c, pt, [i])], lines=lines))
            nums[lo], nums[i] = nums[i], nums[lo]
            lo += 1
            i += 1
        elif nums[i] == 2:
            lines = [("nums[i] = 2", "val"),
                     ("swap(nums[i=%d], nums[hi=%d])" % (i, hi), "sub"),
                     ("hi -= 1;  i 不动, 换来的没看过", "gone")]
            rows.append(dict(arrays=[A(c, pt, [i, hi])], lines=lines))
            nums[i], nums[hi] = nums[hi], nums[i]
            hi -= 1
        else:
            lines = [("nums[i] = 1", "val"), ("已经在 1 区的位置", "sub"), ("i += 1", "new")]
            rows.append(dict(arrays=[A(c, pt, [i])], lines=lines))
            i += 1
    c = cells()
    rows.append(dict(arrays=[A(c, ptrs(), [])], lines=[
        ("i = %d > hi = %d, 结束" % (i, hi), "val"), ("未知区空了", "sub"), ("nums = %s" % nums, "new")]))
    print("  final", nums)
    return rows, nums


def trace_merge(nums1, m, nums2, n):
    nums1 = list(nums1)
    rows = []
    i, j, k = m - 1, n - 1, m + n - 1
    L1 = len(nums1)

    def arrs(show_ring=True):
        c1 = []
        for t in range(L1):
            if t > k:
                role = "new"
            elif t <= i:
                role = "other"
            else:
                role = "plain"
            c1.append((nums1[t] if (t <= i or t > k) else "_", role))
        c2 = [(nums2[t], "other" if t <= j else "gone") for t in range(n)]
        p1 = {}
        for name, v in (("i", i), ("k", k)):
            if 0 <= v < L1:
                p1[v] = (p1[v] + "," + name) if v in p1 else name
        p2 = {j: "j"} if j >= 0 else {}
        r1 = [i] if (i >= 0 and show_ring) else []
        r2 = [j] if (j >= 0 and show_ring) else []
        return [A(c1, p1, r1, "nums1"), A(c2, p2, r2, "nums2")]

    while j >= 0:
        a = arrs()
        if i >= 0 and nums1[i] > nums2[j]:
            lines = [("nums1[%d] = %d  vs  nums2[%d] = %d" % (i, nums1[i], j, nums2[j]), "val"),
                     ("%d > %d  ->  大的是 nums1[i]" % (nums1[i], nums2[j]), "sub"),
                     ("nums1[k=%d] = %d;  i -= 1" % (k, nums1[i]), "new")]
            rows.append(dict(arrays=a, lines=lines))
            print("  k=%d take nums1[%d]=%d" % (k, i, nums1[i]))
            nums1[k] = nums1[i]
            i -= 1
        else:
            cmp = ("nums1[%d] = %d  vs  nums2[%d] = %d" % (i, nums1[i], j, nums2[j]))
            lines = [(cmp, "val"),
                     ("%d <= %d  ->  大的是 nums2[j]" % (nums1[i], nums2[j]), "sub"),
                     ("nums1[k=%d] = %d;  j -= 1" % (k, nums2[j]), "new")]
            rows.append(dict(arrays=a, lines=lines))
            print("  k=%d take nums2[%d]=%d" % (k, j, nums2[j]))
            nums1[k] = nums2[j]
            j -= 1
        k -= 1
        print("   nums1 =", nums1)
    a = arrs(False)
    rows.append(dict(arrays=a, lines=[
        ("j = -1, nums2 用完, 结束", "val"),
        ("nums1[0..i] 本来就在正确位置", "sub"),
        ("nums1 = %s" % nums1, "new")]))
    return rows, nums1


def trace_palin(s):
    n = len(s)
    rows = []
    l, r = 0, n - 1
    matched, skipped = set(), set()

    def cells():
        out = []
        for k in range(n):
            role = "new" if k in matched else ("gone" if k in skipped else "other")
            out.append((s[k], role))
        return out

    while l < r:
        pt = {l: "l", r: "r"}
        c = cells()
        if not s[l].isalnum():
            rows.append(dict(arrays=[A(c, pt, [l, r])], lines=[
                ("s[l] = '%s' 不是字母/数字" % s[l], "val"), ("l += 1", "sub"), ("跳过它", "gone")]))
            skipped.add(l)
            l += 1
        elif not s[r].isalnum():
            rows.append(dict(arrays=[A(c, pt, [l, r])], lines=[
                ("s[r] = '%s' 不是字母/数字" % s[r], "val"), ("r -= 1", "sub"), ("跳过它", "gone")]))
            skipped.add(r)
            r -= 1
        elif s[l].lower() != s[r].lower():
            rows.append(dict(arrays=[A(c, pt, [l, r])], lines=[("不等", "val"), ("return False", "gone")]))
            return rows, False
        else:
            rows.append(dict(arrays=[A(c, pt, [l, r])], lines=[
                ("'%s'.lower() == '%s'.lower()" % (s[l], s[r]), "val"), ("相等", "sub"),
                ("l += 1, r -= 1", "new")]))
            matched.add(l)
            matched.add(r)
            l += 1
            r -= 1
        print("  l=%d r=%d" % (l, r))
    c = cells()
    if l == r:
        matched.add(l)
        c = cells()
    rows.append(dict(arrays=[A(c, {l: "l,r"} if l == r else {}, [])], lines=[
        ("l == r == %d, 循环结束" % l, "val"), ("中间不用配对", "sub"), ("return True", "new")]))
    return rows, True


def trace_palin2(s):
    n = len(s)
    rows = []
    l, r = 0, n - 1
    matched = set()

    def cells(extra=None):
        out = []
        for k in range(n):
            role = "new" if k in matched else "other"
            if extra and k in extra:
                role = extra[k]
            out.append((s[k], role))
        return out

    while l < r:
        if s[l] != s[r]:
            c = cells()
            rows.append(dict(arrays=[A(c, {l: "l", r: "r"}, [l, r])], lines=[
                ("s[%d] = '%s'  !=  s[%d] = '%s'" % (l, s[l], r, s[r]), "val"),
                ("第一次失配: 必须删 s[l] 或 s[r]", "sub"),
                ("两种都试, 只试这两种", "sub")]))
            a_ok = NS_ok(s, l + 1, r)
            b_ok = NS_ok(s, l, r - 1)
            ca = cells({l: "gone"})
            rows.append(dict(arrays=[A(ca, {l + 1: "l", r: "r"}, [l + 1, r])], lines=[
                ("试 A: 删 s[%d] = '%s'" % (l, s[l]), "val"),
                ("检查 s[%d..%d] = '%s'" % (l + 1, r, s[l + 1:r + 1]), "sub"),
                ("%s" % ("是回文" if a_ok else "不是回文 (%s != %s)" % (s[l + 1], s[r])), "new" if a_ok else "gone")]))
            cb = cells({r: "gone"})
            rows.append(dict(arrays=[A(cb, {l: "l", r - 1: "r"}, [l, r - 1])], lines=[
                ("试 B: 删 s[%d] = '%s'" % (r, s[r]), "val"),
                ("检查 s[%d..%d] = '%s'" % (l, r - 1, s[l:r]), "sub"),
                ("%s" % ("是回文" if b_ok else "不是回文"), "new" if b_ok else "gone")]))
            print("  mismatch at l=%d r=%d  A=%s B=%s" % (l, r, a_ok, b_ok))
            return rows, (a_ok or b_ok), (l, r, a_ok, b_ok)
        c = cells()
        rows.append(dict(arrays=[A(c, {l: "l", r: "r"}, [l, r])], lines=[
            ("s[%d] = '%s'  ==  s[%d] = '%s'" % (l, s[l], r, s[r]), "val"), ("相等", "sub"),
            ("l += 1, r -= 1", "new")]))
        matched.add(l)
        matched.add(r)
        l += 1
        r -= 1
    return rows, True, None


def NS_ok(s, l, r):
    while l < r:
        if s[l] != s[r]:
            return False
        l += 1
        r -= 1
    return True


# ----------------------------------------------------------------------------
# 4. 画图
# ----------------------------------------------------------------------------
def core_grid():
    """第 0 节: Two Sum II 的 (i, j) pair 网格, 一次比较排除一整行/一整列"""
    nums, target = [1, 3, 4, 6, 9, 12, 14], 16
    n = len(nums)
    status = {}   # (i, j) -> ('visit', step) | ('elim', step)
    l, r, step = 0, n - 1, 0
    visit = []
    while l < r:
        step += 1
        s = nums[l] + nums[r]
        status[(l, r)] = ("visit", step, s)
        visit.append((l, r, s))
        if s == target:
            break
        if s < target:
            for j in range(l + 1, r + 1):
                status.setdefault((l, j), ("elim", step, None))
            l += 1
        else:
            for i in range(l, r):
                status.setdefault((i, r), ("elim", step, None))
            r -= 1
    print("  grid visits:", visit)
    total = n * (n - 1) // 2
    nv = sum(1 for v in status.values() if v[0] == "visit")
    ne = sum(1 for v in status.values() if v[0] == "elim")
    print("  pairs total=%d visited=%d eliminated=%d untouched=%d" % (total, nv, ne, total - nv - ne))
    g = Svg()
    g.t(40, 18, "nums = %s · target = %d · 每个格子 (i, j) = 一个 pair, 只画 i < j" % (nums, target), 12, INK2)
    g.t(40, 38, "绿 = pointer 真正比较过的 pair · 红 = 被 \"丢掉一整行/一整列\" 顺带排除的 pair (数字 = 第几步排除)", 12, INK2)
    x0, y0, cs = 100, 92, 38
    g.t(x0 + n * cs / 2, 62, "j (= r 的位置)", 12, INK2, "middle")
    for j in range(n):
        g.t(x0 + j * cs + cs / 2 - 1, 80, "%d" % nums[j], 14, INK, "middle", 500)
    g.t(60, y0 - 4, "i (= l)", 12, INK2, "middle")
    for i in range(n):
        g.t(x0 - 10, y0 + i * cs + cs / 2 + 18, "%d" % nums[i], 14, INK, "end", 500)
        for j in range(n):
            x, y = x0 + j * cs, y0 + 14 + i * cs
            if i >= j:
                continue
            st = status.get((i, j))
            if st is None:
                g.cell(x, y, cs - 2, cs - 2, "", "other")
            elif st[0] == "visit":
                g.cell(x, y, cs - 2, cs - 2, st[2], "new", 14, ring=(True))
            else:
                g.cell(x, y, cs - 2, cs - 2, st[1], "gone", 12)
    rx = x0 + n * cs + 30
    lines = [
        ("共 %d 个 pair (i < j)" % total, 14, INK, 500),
        ("brute force: 每个都算一遍 -> O(n²)", 12, INK2, 400),
        ("", 12, INK2, 400),
        ("双指针只比较了 %d 个 pair" % nv, 14, "#085041", 500),
        ("(%d 步, 每步 l 或 r 走一格)" % nv, 12, INK2, 400),
        ("", 12, INK2, 400),
        ("剩下的 %d 个红格没算, 也不用算:" % ne, 14, "#712B13", 500),
        ("第 1 步 1+14 = 15 < 16", 12, "#712B13", 400),
        ("-> 整行 i=0 都 <= 15, 全排除", 12, "#712B13", 400),
        ("第 2 步 3+14 = 17 > 16", 12, "#712B13", 400),
        ("-> 整列 j=6 都 >= 17, 全排除", 12, "#712B13", 400),
    ]
    yy = 108
    for txt, sz, col, wt in lines:
        if txt:
            g.t(rx, yy, txt, sz, col, "start", wt)
        yy += 20
    # 第 3 步说明
    g.t(rx, yy, "第 3 步同理排除整行 i=1", 12, "#712B13")
    hh = y0 + 14 + n * cs + 22
    g.legend(hh, [("new", "比较过"), ("gone", "被排除"), ("other", "没碰过 (不需要)")])
    g.t(40, hh + 28, "O(n²) 个 pair -> O(n) 步: 每一步丢掉一整行或一整列", 14, INK, "start", 500)
    return g.out(hh + 50, "pair 网格", "双指针每一步排除一整行或一整列的 pair", "template_core.svg")


def core_two_sum():
    nums = [1, 3, 4, 6, 9, 12, 14]
    target = 16
    g = Svg()
    g.t(40, 18, "nums = %s · target = %d · 为什么 \"丢掉一个 pointer\" 不会错过答案" % (nums, target), 12, INK2)
    cw = 52

    def panel(y, l, r, title, big):
        s = nums[l] + nums[r]
        g.t(40, y, title, 14, INK, "start", 500)
        cells = []
        for k in range(len(nums)):
            if k == (r if big else l):
                role = "gone"
            else:
                role = "other"
            cells.append((nums[k], role))
        arr = A(cells, {l: "l", r: "r"}, [l, r])
        draw_array(g, 40, y + 14, arr, cw)
        # 与被丢掉的那个数配对的所有和
        keep = r if big else l
        others = range(l, r) if big else range(l + 1, r + 1)
        yy = y + 14 + 70 + 4
        last = max(others)
        for k in others:
            cx = 40 + k * cw
            sm = nums[k] + nums[keep]
            g.path("M%s %s L%s %s" % (cx + cw / 2 - 1, yy + 6, cx + cw / 2 - 1, yy + 32), RED_ARROW, True, True, 1.2)
            g.cell(cx, yy + 36, cw - 2, 30, sm, "gone", 14)
        g.t(40 + (last + 1) * cw + 8, yy + 51, "<- %d 配这些的和" % nums[keep], 12, "#712B13")
        g.t(40, yy + 84, "全部 %s %d = target, 没有一个能成" % (">" if big else "<", target), 14, "#712B13", "start", 500)
        print("  panel", title, [nums[k] + nums[keep] for k in others])
        return yy + 104

    y = panel(50, 1, 6, "情况 1: nums[l] + nums[r] = 3 + 14 = 17 > 16  ->  r 没用了", True)
    y = panel(y + 14, 0, 6, "情况 2: nums[l] + nums[r] = 1 + 14 = 15 < 16  ->  l 没用了", False)
    g.t(40, y + 4, "sorted 是关键: 换一个更靠里的搭档, 和只会更小 (情况 1) / 更大 (情况 2)", 14, INK, "start", 500)
    g.legend(y + 34, [("other", "还在候选区"), ("gone", "被丢掉的数 / 配对结果"), ("ring", "当前 l, r")])
    return g.out(y + 56, "Two Sum II 核心", "丢掉一个 pointer 为什么安全", "two_sum_ii_core.svg")


def core_three_sum():
    nums = [-2, -2, 0, 0, 2, 2]
    g = Svg()
    g.t(40, 18, "nums = %s (已排序) · 同值的数一定挨在一起 -> 去重 = 跳过 \"和前一个相同\" 的位置" % nums, 12, INK2)
    cw = 56
    # 去重 1
    g.t(40, 52, "去重 1: i 只在每组同值的第一个位置当 \"第一个数\"", 14, INK, "start", 500)
    cells = []
    for k, v in enumerate(nums):
        cells.append((v, "new" if (k == 0 or nums[k] != nums[k - 1]) else "gone"))
    draw_array(g, 40, 66, A(cells, {}, []), cw)
    for k in range(len(nums)):
        cx = 40 + k * cw + (cw - 2) / 2
        if k == 0 or nums[k] != nums[k - 1]:
            g.t(cx, 150, "试", 12, "#085041", "middle", 500)
        else:
            g.t(cx, 150, "continue", 12, "#712B13", "middle")
    g.t(40, 176, "nums[i] == nums[i-1] 说明这个值已经当过 \"第一个数\", 它能凑出的三元组上一次全找过了", 12, INK2)
    # 去重 2
    g.t(40, 214, "去重 2: 找到答案后, l 和 r 各自跳过同值", 14, INK, "start", 500)
    g.t(40, 240, "例: i = 0 (值 -2), l = 2, r = 5 时找到 -2 + 0 + 2 = 0:", 12, INK2)
    draw_array(g, 40, 252, A([(-2, "new"), (-2, "plain"), (0, "new"), (0, "gone"), (2, "gone"), (2, "new")],
                              {0: "i", 2: "l", 5: "r"}, [2, 5]), cw)
    g.t(40, 336, "如果只做 l += 1, r -= 1, 会落到 nums[3] = 0 和 nums[4] = 2 (红色), 又得到一模一样的 [-2, 0, 2]。", 12, INK2)
    g.t(40, 356, "所以找到之后要继续跳过和刚用过的值相同的位置:", 12, INK2)
    g.t(40, 380, "while nums[l] == nums[l-1]: l += 1", 14, INK, "start", 500)
    g.t(360, 380, "while nums[r] == nums[r+1]: r -= 1", 14, INK, "start", 500)
    g.legend(412, [("new", "这次用到的数 / 每组第一个"), ("gone", "同值, 跳过"), ("ring", "当前 l, r")])
    return g.out(436, "3Sum 去重", "两处去重规则", "three_sum_core.svg")


def core_container():
    h = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    l, r = 1, 8
    g = Svg()
    g.t(40, 18, "height = %s · 当前 l = %d (高 %d), r = %d (高 %d) · 面积 = min(%d, %d) x (%d - %d) = %d"
        % (h, l, h[l], r, h[r], h[l], h[r], r, l, min(h[l], h[r]) * (r - l)), 12, INK2)
    g.t(40, 38, "矮的是 r (高 7)。问: 保留 r, 把 l 换成更靠里的墙 i, 能比 49 大吗?", 12, INK2)
    u, bw, gp = 15, 30, 8
    base = 50 + 8 * u + 24
    x0 = 50
    xl = x0 + l * (bw + gp) + bw
    xr = x0 + r * (bw + gp)
    g.rect(xl, base - 7 * u, xr - xl, 7 * u, "new", rx=2, dash=True)
    for k, v in enumerate(h):
        x = x0 + k * (bw + gp)
        g.rect(x, base - v * u, bw, v * u, "other", rx=2)
        g.t(x + bw / 2, base + 14, v, 12, INK, "middle")
        g.t(x + bw / 2, base + 30, k, 12, "#898781", "middle")
    g.t((xl + xr) / 2, base - 3.5 * u - 30, "面积 = 7 x 7 = 49", 14, "#085041", "middle", 500)
    g.line(x0 - 6, base - 7 * u, x0 + 9 * (bw + gp), base - 7 * u, RED_ARROW, "5 4", 1.2)
    g.t(40, 60, "换掉 l 之后, 高度最多 = height[r] = 7 (红色虚线, 再高也被 r 挡住)", 12, "#712B13")
    g.ring(x0 + l * (bw + gp), base - h[l] * u, bw, h[l] * u)
    g.ring(x0 + r * (bw + gp), base - h[r] * u, bw, h[r] * u)
    g.tri(x0 + l * (bw + gp) + bw / 2, base + 34)
    g.tri(x0 + r * (bw + gp) + bw / 2, base + 34)
    g.t(x0 + l * (bw + gp) + bw / 2, base + 50, "l", 14, INK, "middle", 500)
    g.t(x0 + r * (bw + gp) + bw / 2, base + 50, "r", 14, INK, "middle", 500)
    y = base + 76
    g.t(40, y, "新的 l' > l  ->  宽度 = r - l' <= 6 < 7", 14, "#712B13", "start", 500)
    g.t(40, y + 22, "高度 <= 7  ->  面积 <= 7 x 6 = 42 < 49", 14, "#712B13", "start", 500)
    g.t(40, y + 50, "所以 \"保留矮墙 r, 换 l\" 的所有候选都不可能超过当前面积, r 可以放心丢掉。", 14, INK, "start", 500)
    g.t(40, y + 72, "(矮的是 l 时对称: 丢 l。一样高时丢哪个都行。)", 12, INK2)
    g.legend(y + 100, [("new", "当前容器"), ("other", "墙"), ("ring", "当前 l, r")])
    print("  container core: bound", 7 * 6)
    return g.out(y + 122, "Container 核心", "为什么丢较矮的墙", "container_core.svg")


def core_trap(h):
    n = len(h)
    lm = [max(h[:i + 1]) for i in range(n)]
    rm = [max(h[i:]) for i in range(n)]
    wt = [min(lm[i], rm[i]) - h[i] for i in range(n)]
    total = sum(wt)
    print("  trap table h", h, "lmax", lm, "rmax", rm, "water", wt, total)
    g = Svg()
    g.t(40, 18, "height = %s · 第 i 格的水 = min(左边最高, 右边最高) - height[i]" % h, 12, INK2)
    g.t(40, 38, "lmax[i] = height[0..i] 的最大值 · rmax[i] = height[i..n-1] 的最大值 · min = min(lmax, rmax) · water = min - height", 12, INK2)
    u = 16
    top = max(h)
    bw = 44
    x0 = 150
    base = 56 + top * u + 16
    for k in range(n):
        x = x0 + k * bw
        g.rect(x, base - h[k] * u, bw - 4, h[k] * u, "other", rx=2)
        if wt[k] > 0:
            g.rect(x, base - (h[k] + wt[k]) * u, bw - 4, wt[k] * u, "new", rx=2, dash=True)
        g.t(x + (bw - 4) / 2, base + 14, k, 12, "#898781", "middle")
    # 表
    rows = [("height", h), ("lmax", lm), ("rmax", rm),
            ("min", [min(a, b) for a, b in zip(lm, rm)]), ("water", wt)]
    y = base + 40
    for name, vals in rows:
        g.t(40, y + 15, name.split(" ")[0] if not name.startswith("min") else "min", 12, INK2)
        for k, v in enumerate(vals):
            role = "new" if name.startswith("water") and v > 0 else "plain"
            g.cell(x0 + k * bw, y, bw - 4, 30, v, role, 14)
        y += 36
    for k, v in enumerate(["height", "lmax", "rmax", "min", "water"]):
        pass
    g.t(x0 + n * bw + 6, y - 21, "= %s" % " + ".join(str(v) for v in wt if v) if False else "", 12, INK2)
    g.t(40, y + 14, "total = %s = %d" % (" + ".join(str(v) for v in wt), total), 14, INK, "start", 500)
    y += 50
    g.t(40, y, "O(n) 空间: 先扫两遍把 lmax[], rmax[] 存下来。双指针把这两个数组换成两个变量:", 14, INK, "start", 500)
    g.t(40, y + 24, "lmax < rmax 时, 位置 l 的 \"右边最高\" >= rmax > lmax, 所以 min(...) 一定是 lmax", 12, INK2)
    g.t(40, y + 44, "-> 这一格的水只看 lmax 就能算, 完全不用知道右边具体是多少, 然后 l 前进。反之对称。", 12, INK2)
    g.legend(y + 74, [("new", "水"), ("other", "墙"), ("plain", "辅助数组")])
    return g.out(y + 96, "Trapping Rain Water 核心", "每格水 = min(lmax, rmax) - h", "trap_core.svg")


def core_zone(fname, title, nums, w, r, labels, left_name, mid_name, caption, extra_arc=False, lines2=None):
    """同向 read/write 的 invariant 图: [0,w) 答案区 | [w,r) 残留区 | [r,n) 未读区"""
    n = len(nums)
    cw = 52
    g = Svg()
    g.t(40, 18, labels[0], 12, INK2)
    g.t(40, 38, labels[1], 12, INK2)
    cells = []
    for k, v in enumerate(nums):
        cells.append((v, "new" if k < w else ("gone" if k < r else "plain")))
    ptrs = {}
    for name, v in (("w", w), ("r", r)):
        ptrs[v] = name
    y = 64
    if extra_arc:
        y = 92
        # r 去和 w-1 比
        x1 = 40 + r * cw + (cw - 2) / 2
        x2 = 40 + (w - 1) * cw + (cw - 2) / 2
        g.path("M%s %s C %s %s, %s %s, %s %s" % (x1, y - 4, x1, y - 40, x2, y - 40, x2, y - 4),
               INK2, False, True, 1.5)
        g.t((x1 + x2) / 2, y - 40, "nums[r] 和 nums[w-1] 比", 12, INK2, "middle")
    draw_array(g, 40, y, A(cells, ptrs, [r]), cw)
    by = y + 80
    # 括号
    def brace(a, b, txt, col):
        xa = 40 + a * cw
        xb = 40 + b * cw - 2
        g.line(xa, by, xb, by, col, None, 2)
        g.line(xa, by - 5, xa, by, col, None, 2)
        g.line(xb, by - 5, xb, by, col, None, 2)
        g.t((xa + xb) / 2, by + 16, txt, 12, col, "middle")
    brace(0, w, "[0, w)", "#085041")
    if r > w:
        brace(w, r, "[w, r)", "#712B13")
    brace(r, n, "[r, n)", INK2)
    y2 = by + 40
    for k, ln in enumerate(lines2 or []):
        g.t(40, y2 + 22 * k, ln[0], ln[1], INK if ln[1] == 14 else INK2, "start", 500 if ln[1] == 14 else 400)
    y2 += 22 * len(lines2 or []) + 10
    g.legend(y2, [("new", left_name[1]), ("gone", mid_name[1]), ("plain", "[r, n) 没读"), ("ring", "r")])
    return g.out(y2 + 24, title, caption, fname)


def core_sort_colors():
    nums = [0, 0, 1, 1, 2, 0, 1, 2, 2]
    lo, i, hi = 2, 4, 6
    n = len(nums)
    cw = 52
    g = Svg()
    g.t(40, 18, "某一刻的状态 (示意): lo = %d, i = %d, hi = %d · 四个区, 三个 pointer 是区的分界线" % (lo, i, hi), 12, INK2)
    cells = []
    for k, v in enumerate(nums):
        role = "new" if k < lo else ("other" if k < i else ("plain" if k <= hi else "gone"))
        cells.append((v, role))
    y = 50
    draw_array(g, 40, y, A(cells, {lo: "lo", i: "i", hi: "hi"}, [i]), cw)
    by = y + 80

    def brace(a, b, txt, col):
        xa = 40 + a * cw
        xb = 40 + b * cw - 2
        g.line(xa, by, xb, by, col, None, 2)
        g.line(xa, by - 5, xa, by, col, None, 2)
        g.line(xb, by - 5, xb, by, col, None, 2)
        g.t((xa + xb) / 2, by + 16, txt, 12, col, "middle")
    brace(0, lo, "[0, lo): 全是 0", "#085041")
    brace(lo, i, "[lo, i): 全是 1", INK2)
    brace(i, hi + 1, "[i, hi]: 未知", INK2)
    brace(hi + 1, n, "(hi, n): 全是 2", "#712B13")
    y = by + 44
    g.t(40, y, "看 nums[i], 三种情况都要保持上面四个区不被破坏:", 14, INK, "start", 500)
    g.t(40, y + 26, "== 0: 和 nums[lo] 交换。换过来的是 [lo, i) 里的 1 (或 lo == i), 所以 lo += 1, i += 1", 12, INK2)
    g.t(40, y + 46, "== 2: 和 nums[hi] 交换。换过来的是未知区的数, 还没看过, 所以只 hi -= 1, i 不动", 12, INK2)
    g.t(40, y + 66, "== 1: 它本来就该在 1 区的末尾, i += 1", 12, INK2)
    g.t(40, y + 96, "每一步 i 前进或 hi 后退, 未知区缩小 1 格 -> n 步, 一遍扫描", 14, INK, "start", 500)
    g.legend(y + 126, [("new", "0 区"), ("other", "1 区"), ("plain", "未知区"), ("gone", "2 区"), ("ring", "i")])
    return g.out(y + 148, "Sort Colors 核心", "四个区的 invariant", "sort_colors_core.svg")


def core_merge():
    g = Svg()
    g.t(40, 18, "nums1 = [4, 5, 6, _, _, _] (m = 3, 后 3 格是空位) · nums2 = [1, 2, 3] · 从哪头开始写?", 12, INK2)
    cw = 52
    g.t(40, 50, "从前往后: 第一个最小值 1 要写到 k = 0", 14, INK, "start", 500)
    c1 = [(4, "gone"), (5, "other"), (6, "other"), ("_", "plain"), ("_", "plain"), ("_", "plain")]
    draw_array(g, 40, 60, A(c1, {0: "k"}, [0]), cw, None, 0)
    g.t(40, 138, "nums1[0] = 4 还没读就被盖掉了 -> 只能先把 4, 5, 6 往后挪, 又变成 O(m·n)", 14, "#712B13", "start", 500)
    g.line(40, 164, 640, 164)
    g.t(40, 190, "从后往前: 最大值要写到 k = 5, 那里是空位", 14, INK, "start", 500)
    c2 = [(4, "other"), (5, "other"), (6, "other"), ("_", "plain"), ("_", "plain"), ("_", "new")]
    draw_array(g, 40, 200, A(c2, {2: "i", 5: "k"}, [2]), cw, None, 0)
    g.t(40, 278, "k = i + j + 1 >= i: 写入位置永远在 i 的右边 (或和 i 重合, 此时 j = -1 已经结束),", 14, INK, "start", 500)
    g.t(40, 300, "写进去的格子要么是空位, 要么是 nums1 已经读过 (搬走) 的格子, 不会盖掉没读的数。", 14, INK, "start", 500)
    g.legend(332, [("other", "还没读的 nums1"), ("gone", "被误盖掉的"), ("plain", "空位"), ("new", "写入")])
    return g.out(356, "Merge 核心", "为什么要从后往前写", "merge_core.svg")


def core_palin():
    s = "A,bxB;a"
    n = len(s)
    cw = 52
    g = Svg()
    g.t(40, 18, "s = \"%s\" · 回文 = 从两端向中间一对一对配, 每对必须相等 · l, r 向中间走" % s, 12, INK2)
    g.t(40, 48, "Valid Palindrome: 只比字母/数字, 非字母数字先跳过", 14, INK, "start", 500)
    cells = [("A", "new"), (",", "gone"), ("b", "other"), ("x", "other"), ("B", "other"), (";", "gone"), ("a", "new")]
    draw_array(g, 40, 62, A(cells, {2: "l", 4: "r"}, [2, 4]), cw)
    g.t(40, 150, "invariant: s[0..l) 和 s(r..n) 去掉标点后已经一一配对相等, 现在配 s[l] 和 s[r]", 12, INK2)
    g.line(40, 172, 640, 172)
    g.t(40, 198, "Valid Palindrome II (最多删 1 个): 第一次失配时, 只有 2 种删法", 14, INK, "start", 500)
    s2 = "cbbcc"
    cells = [("c", "new"), ("b", "other"), ("b", "other"), ("c", "other"), ("c", "new")]
    draw_array(g, 40, 212, A(cells, {1: "l", 3: "r"}, [1, 3]), cw)
    g.t(40, 298, "s[1] = b != s[3] = c: 要让它们配上, 必须删掉 s[1] 或 s[3] (删别的位置, 这对还是 b, c)", 12, INK2)
    g.t(40, 318, "删 s[l]: 检查 s[l+1..r];  删 s[r]: 检查 s[l..r-1]。每个检查是一次 O(n) 的普通回文判断", 12, INK2)
    g.t(40, 342, "只有 2 个分支, 不会指数爆炸: 总共 O(n) + 2 次 O(n) 检查 = O(n)", 14, INK, "start", 500)
    g.legend(374, [("new", "已配对"), ("gone", "跳过"), ("other", "待配"), ("ring", "当前 l, r")])
    return g.out(398, "Valid Palindrome 核心", "向中间配对, II 只有两个分支", "valid_palindrome_core.svg")


# ----------------------------------------------------------------------------
# 5. 生成所有图
# ----------------------------------------------------------------------------
print("== grid core")
core_grid()
print("== two sum II")
core_two_sum()
rows, ans = trace_two_sum([1, 3, 4, 6, 9, 12, 14], 16)
assert ans == NS["two_sum_sorted"]([1, 3, 4, 6, 9, 12, 14], 16) == [2, 5]
trace_svg("two_sum_ii_trace.svg", "Two Sum II trace", "l, r 相向", [
    "nums = [1, 3, 4, 6, 9, 12, 14] · target = 16 · l = 0, r = 6",
    "每一步: 算 nums[l] + nums[r] 和 target 比 -> 太小丢 l, 太大丢 r, 相等就找到了"],
    ("状态 (红 = 已丢掉的数)", "计算 -> 决定"), rows,
    ["答案: l = 2, r = 5  (nums[2] + nums[5] = 4 + 12 = 16)", "只比了 4 对, brute force 最坏要比 21 对"],
    [("other", "候选区 [l, r]"), ("gone", "丢掉"), ("new", "答案"), ("ring", "当前 l, r")])

print("== three sum")
core_three_sum()
rows, ans = trace_three_sum([-2, -2, 0, 0, 2, 2])
assert ans == NS["three_sum"]([-2, -2, 0, 0, 2, 2]) == [[-2, 0, 2]]
trace_svg("three_sum_trace.svg", "3Sum trace", "外层 i 加里层 l, r", [
    "nums = [-2, -2, 0, 0, 2, 2] (已排序) · 外层固定 i, 里层 l = i + 1, r = n - 1 找 nums[l] + nums[r] = -nums[i]",
    "每一步: 三数之和 s 和 0 比 -> 太小 l += 1, 太大 r -= 1; 同值的 i, l, r 跳过去重"],
    ("状态 (绿 = i, 灰 = [l, r], 红 = 已丢掉)", "计算 -> 决定"), rows,
    ["答案: [[-2, 0, 2]]  (只有一个, 没有重复)"],
    [("new", "i / 答案"), ("other", "候选区"), ("gone", "丢掉 / 重复"), ("ring", "当前 l, r")], cw=34)

print("== container")
core_container()
rows, best = trace_container([1, 8, 6, 2, 5, 4, 8, 3, 7])
assert best == NS["max_area"]([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
trace_svg("container_trace.svg", "Container trace", "l, r 相向, 丢矮墙", [
    "height = [1, 8, 6, 2, 5, 4, 8, 3, 7] · l = 0, r = 8 · 面积 = min(height[l], height[r]) x (r - l)",
    "每一步: 先算面积更新 best -> 再丢掉较矮的那面墙 (一样高丢 r)"],
    ("状态 (红 = 已丢掉)", "计算 -> 决定"), rows,
    ["答案: best = 49  (l = 1, r = 8: min(8, 7) x (8 - 1) = 7 x 7)"],
    [("other", "候选区 [l, r]"), ("gone", "丢掉"), ("ring", "当前 l, r")], cw=32, notes_x=350)

print("== trap")
H = [2, 0, 1, 3, 0, 1, 2]
core_trap(H)
rows, water = trace_trap(H)
assert water == NS["trap"](H) == brute_trap(H) == 6
trace_svg("trap_trace.svg", "Trapping Rain Water trace", "双指针 lmax rmax", [
    "height = %s · l = 0, r = %d · lmax = height[0], rmax = height[%d]" % (H, len(H) - 1, len(H) - 1),
    "每一步: lmax < rmax 就推进 l (水由 lmax 决定), 否则推进 r (水由 rmax 决定); 先更新 max 再累加水"],
    ("状态 (绿 = 已经算过水的格子)", "计算 -> 决定"), rows,
    ["答案: water = 2 + 1 + 2 + 1 = 6  (空间 O(1), 没有 lmax[], rmax[] 数组)"],
    [("other", "还没算的"), ("new", "算完了"), ("ring", "这一步刚算的格子")], cw=34, notes_x=330)

print("== move zeroes")
core_zone("move_zeroes_core.svg", "Move Zeroes 核心", [1, 3, 0, 0, 5, 7], 2, 4,
          ["r 一路读过去, w 只在\"遇到要保留的\"时才走 · 两个 pointer 同向, 速度不同",
           "某一刻 (示意): w = 2, r = 4  ->  [0, w) 非零, [w, r) 全是 0, [r, n) 没读"],
          ("", "[0, w) 非零, 顺序没变"), ("", "[w, r) 全是 0"),
          "三个区", False,
          [("nums[r] != 0 时, 把它和 nums[w] 交换: nums[w] 一定是 0 (或 w == r), 交换后区间仍然成立。", 12),
           ("nums[r] == 0 时什么都不做, r 前进, 这个 0 自然并入 [w, r)。", 12),
           ("w <= r 永远成立, 所以 nums[w] 在 r 之前, 写入不会盖掉没读的数据。", 14)])
rows, res = trace_move_zeroes([0, 1, 0, 3, 12])
b = [0, 1, 0, 3, 12]
NS["move_zeroes"](b)
assert res == b == [1, 3, 12, 0, 0]
trace_svg("move_zeroes_trace.svg", "Move Zeroes trace", "w, r 同向", [
    "nums = [0, 1, 0, 3, 12] · w = 0 (下一个非零该放的位置) · r 从 0 扫到 4",
    "每一步: nums[r] 非零 -> 和 nums[w] 交换, w += 1; 是 0 -> 什么都不做"],
    ("状态 (绿 = [0, w), 红 = [w, r) 的 0, 白 = 没读)", "判断 -> 动作"), rows,
    ["答案: nums = [1, 3, 12, 0, 0]  (非零的相对顺序没变, 只写了 2 次)"],
    [("new", "[0, w) 非零"), ("gone", "[w, r) 的 0"), ("plain", "[r, n) 没读"), ("ring", "r")], cw=40, notes_x=300)

print("== remove duplicates")
core_zone("remove_dup_core.svg", "Remove Duplicates 核心", [0, 1, 1, 1, 2, 2, 3], 2, 4,
          ["sorted -> 重复的值一定挨在一起, 所以只要和\"最后一个保留的\" nums[w-1] 比",
           "某一刻 (示意): w = 2, r = 4  ->  nums[:2] = [0, 1] 是 \"已读部分去重后的结果\""],
          ("", "[0, w) 去重后的结果"), ("", "[w, r) 残留 (没用)"),
          "去重区", True,
          [("nums[r] = 2 != nums[w-1] = 1  ->  新值: nums[w] = 2, w += 1", 14),
           ("nums[r] == nums[w-1]  ->  重复, 什么都不做。", 12),
           ("Remove Duplicates II (每个值最多 2 个): 只改比较的位置, 改成和 nums[w-2] 比。", 12)])
rows, (w, res) = trace_remove_dup([0, 0, 1, 1, 2, 2, 3])
b = [0, 0, 1, 1, 2, 2, 3]
assert NS["remove_duplicates"](b) == w and b == res and res[:w] == [0, 1, 2, 3]
trace_svg("remove_dup_trace.svg", "Remove Duplicates trace", "w, r 同向", [
    "nums = [0, 0, 1, 1, 2, 2, 3] · w = 1 (nums[0] 一定保留) · r 从 1 扫到 6",
    "每一步: nums[r] 和 nums[w-1] (最后一个保留的) 比 -> 不同才写到 nums[w], w += 1"],
    ("状态 (绿 = [0, w), 红 = 残留, 白 = 没读)", "比较 -> 动作"), rows,
    ["答案: return w = 4,  nums[:4] = [0, 1, 2, 3]"],
    [("new", "[0, w) 答案"), ("gone", "[w, r) 残留"), ("plain", "[r, n) 没读"), ("ring", "r")], cw=40, notes_x=330)

print("== sort colors")
core_sort_colors()
rows, res = trace_sort_colors([2, 0, 2, 1, 1, 0])
b = [2, 0, 2, 1, 1, 0]
NS["sort_colors"](b)
assert res == b == [0, 0, 1, 1, 2, 2]
trace_svg("sort_colors_trace.svg", "Sort Colors trace", "lo i hi", [
    "nums = [2, 0, 2, 1, 1, 0] · lo = 0, i = 0, hi = 5 · 四个区: 0 区 | 1 区 | 未知 | 2 区",
    "每一步看 nums[i]: 0 -> 换到 lo 区末尾; 2 -> 换到 hi 区开头; 1 -> 不用动"],
    ("状态 (绿 0 区, 灰 1 区, 白 未知, 红 2 区)", "判断 -> 动作"), rows,
    ["答案: nums = [0, 0, 1, 1, 2, 2]  (一遍扫描, 每一步 i 前进或 hi 后退)"],
    [("new", "0 区"), ("other", "1 区"), ("plain", "未知区"), ("gone", "2 区"), ("ring", "i / 被换的格子")],
    cw=40, notes_x=330)

print("== merge")
core_merge()
rows, res = trace_merge([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3)
b = [1, 2, 3, 0, 0, 0]
NS["merge"](b, 3, [2, 5, 6], 3)
assert res == b == [1, 2, 2, 3, 5, 6]
trace_svg("merge_trace.svg", "Merge Sorted Array trace", "i j k 从后往前", [
    "nums1 = [1, 2, 3, _, _, _] (m = 3) · nums2 = [2, 5, 6] (n = 3) · i = 2, j = 2, k = 5",
    "每一步: 比较 nums1[i] 和 nums2[j] 谁大 -> 大的写到 nums1[k], 对应指针和 k 都 -1"],
    ("状态 (绿 = 已写好, 红 = nums2 已用掉)", "比较 -> 动作"), rows,
    ["答案: nums1 = [1, 2, 2, 3, 5, 6]  (nums2 用完就停, nums1 剩下的 1, 2 本来就在原位)"],
    [("other", "还没读"), ("plain", "空位 _"), ("new", "已写好 (从后往前)"), ("gone", "nums2 已用掉"), ("ring", "正在比的两个数")],
    cw=40, name_w=52, notes_x=330)

print("== palindrome")
core_palin()
rows, ok = trace_palin("A,bxB;a")
assert ok is True and NS["is_palindrome"]("A,bxB;a") is True
trace_svg("valid_palindrome_trace.svg", "Valid Palindrome trace", "l, r 向中间", [
    's = "A,bxB;a" · l = 0, r = 6 · 只比较字母和数字, 忽略大小写',
    "每一步: s[l] 不是字母数字 -> l += 1; s[r] 不是 -> r -= 1; 都是 -> 比较, 相等则两边各走一步"],
    ("状态 (绿 = 已配对, 红 = 跳过)", "判断 -> 动作"), rows,
    ["答案: return True  (A-a 配对, b-B 配对, x 在正中间)"],
    [("new", "已配对"), ("gone", "跳过 (非字母数字)"), ("other", "待配"), ("ring", "当前 l, r")], cw=40, notes_x=350)
rows, ok, info = trace_palin2("cbbcc")
assert ok is True and NS["valid_palindrome_ii"]("cbbcc") is True and NS["valid_palindrome_ii"]("abcaa") is False
assert info == (1, 3, False, True)
trace_svg("valid_palindrome_ii_trace.svg", "Valid Palindrome II trace", "失配后两个分支", [
    's = "cbbcc" · 最多删一个字符 · 先照常向中间走, 第一次失配时再分叉',
    "分叉: 删 s[l] -> 检查 s[l+1..r];  删 s[r] -> 检查 s[l..r-1]; 只要有一个是回文就行"],
    ("状态 (绿 = 已配对, 红 = 被删的那个)", "判断 -> 动作"), rows,
    ["答案: return True  (删掉 s[3] = 'c', 剩下 \"cbbc\" 是回文)"],
    [("new", "已配对"), ("gone", "被删"), ("other", "待配"), ("ring", "检查范围的两端")], cw=40, notes_x=350)

# ----------------------------------------------------------------------------
# 6. 文档
# ----------------------------------------------------------------------------
doc = d.Doc("02 · Two Pointers")


def _fx(t):
    return t.replace("$", "").replace("\\log", "log")


for _m in ("p", "raw", "note", "main"):
    _o = getattr(doc, _m)
    setattr(doc, _m, (lambda o: (lambda t: o(_fx(t))))(_o))
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '02_two_pointers_doc.py'), encoding='utf-8').read())
