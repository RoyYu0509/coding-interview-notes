"""04 · Prefix Sum  ->  docs/04-prefix-sum.html
SVG 由本脚本生成 (数字全部来自真实运行的算法), 写到 docs/svg/04-prefix-sum/*.svg。
文档里展示的每段代码都会在生成时 exec 并和暴力解对拍。
运行: cd build && python3 -I 04_prefix_sum.py
"""
import html
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import doclib as d

SLUG = "04-prefix-sum"
SVG_DIR = os.path.join(d.ROOT, "docs", "svg", SLUG)
os.makedirs(SVG_DIR, exist_ok=True)

# ---------------------------------------------------------------- svg kit
ROLE = {  # fill, stroke, text
    "new": ("#E1F5EE", "#0F6E56", "#085041"),
    "gone": ("#FAECE7", "#993C1D", "#712B13"),
    "other": ("#F1EFE8", "#5F5E5A", "#444441"),
    "plain": ("#FFFFFF", "#B4B2A9", "#444441"),
}
INK, SUB = "#0B0B0B", "#52514E"
FONT = 'ui-sans-serif, system-ui, -apple-system, "PingFang SC", sans-serif'


class Svg:
    def __init__(self, title, desc, w=680):
        self.w, self.title, self.desc = w, title, desc
        self.o = []

    def t(self, x, y, s, size=12, fill=SUB, anchor="start", weight=400):
        self.o.append(
            '<text x="%s" y="%s" font-size="%d" fill="%s" text-anchor="%s" '
            'font-weight="%d" dominant-baseline="central">%s</text>'
            % (x, y, size, fill, anchor, weight, html.escape(str(s))))

    def box(self, x, y, w, h, role, lines=(), ring=False, rx=4, dash=False):
        f, s, tc = ROLE[role]
        self.o.append(
            '<rect x="%s" y="%s" width="%s" height="%s" rx="%d" fill="%s" '
            'stroke="%s" stroke-width="%s"%s/>'
            % (x, y, w, h, rx, f, s, 1 if role != "plain" else 0.8,
               ' stroke-dasharray="4 3"' if dash else ""))
        if ring:
            self.ring(x, y, w, h)
        n = len(lines)
        for k, ln in enumerate(lines):
            txt, size, weight = (ln, 14, 500) if isinstance(ln, str) else (ln + (14, 500)[len(ln) - 1:])[:3]
            gap = 16
            cy = y + h / 2 + (k - (n - 1) / 2) * gap
            self.t(x + w / 2, cy, txt, size, tc, "middle", weight)

    def ring(self, x, y, w, h, pad=3):
        self.o.append(
            '<rect x="%s" y="%s" width="%s" height="%s" rx="6" fill="none" '
            'stroke="#EF9F27" stroke-width="2.5"/>'
            % (x - pad, y - pad, w + 2 * pad, h + 2 * pad))

    def circ(self, cx, cy, r, role, txt, ring=False):
        f, s, tc = ROLE[role]
        self.o.append('<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" stroke-width="1"/>'
                      % (cx, cy, r, f, s))
        if ring:
            self.o.append('<circle cx="%s" cy="%s" r="%s" fill="none" stroke="#EF9F27" stroke-width="2.5"/>'
                          % (cx, cy, r + 4))
        self.t(cx, cy, txt, 14, tc, "middle", 500)

    def sep(self, y, x1=40, x2=640):
        self.o.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#B4B2A9" '
                      'stroke-width="0.8" stroke-dasharray="4 4"/>' % (x1, y, x2, y))

    def line(self, x1, y1, x2, y2, color="#B4B2A9", w=1, dash=False):
        self.o.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s/>'
                      % (x1, y1, x2, y2, color, w, ' stroke-dasharray="4 4"' if dash else ""))

    def arrow(self, pts, color=SUB, dash=False, w=1.5):
        p = "M" + " L".join("%s %s" % q for q in pts)
        self.o.append('<path d="%s" fill="none" stroke="%s" stroke-width="%s"%s '
                      'marker-end="url(#ar%s)"/>'
                      % (p, color, w, ' stroke-dasharray="5 4"' if dash else "",
                         "r" if color == "#D85A30" else "g"))

    def toss(self, pts):  # 被移除: 虚线 + 橙红箭头
        self.arrow(pts, "#D85A30", True)

    def cells(self, x, y, vals, roles=None, cw=36, ch=30, rings=(), idx=None, idx_dy=-12):
        """一排数组格子; roles[i] in ROLE; idx 为格子上方的下标标签"""
        for i, v in enumerate(vals):
            r = roles[i] if roles else "other"
            self.box(x + i * cw, y, cw - 3, ch, r, [(str(v), 14, 500)], ring=(i in rings))
            if idx is not None:
                self.t(x + i * cw + (cw - 3) / 2, y + idx_dy, idx[i], 12, SUB, "middle")

    def chips(self, x, y, items, per_row, cw=52, ch=22, gx=4, gy=4, new=(), hit=()):
        """dict 画成 key:val 小格子"""
        for k, (kk, vv) in enumerate(items):
            r, c = divmod(k, per_row)
            role = "new" if kk in new else "other"
            self.box(x + c * (cw + gx), y + r * (ch + gy), cw, ch, role,
                     [("%s:%s" % (kk, vv), 12, 500)], ring=(kk in hit), rx=3)

    def legend(self, y, items):
        x = 40
        for role, label in items:
            if role == "ring":
                self.o.append('<rect x="%s" y="%s" width="14" height="14" rx="3" fill="none" '
                              'stroke="#EF9F27" stroke-width="2.5"/>' % (x, y - 7))
            else:
                f, s, _ = ROLE[role]
                self.o.append('<rect x="%s" y="%s" width="14" height="14" rx="3" fill="%s" stroke="%s"/>'
                              % (x, y - 7, f, s))
            self.t(x + 20, y, label, 12, SUB)
            x += 20 + sum(12 if ord(ch) > 255 else 6.6 for ch in label) + 28

    def save(self, name, h):
        defs = ('<defs>' + ''.join(
            '<marker id="ar%s" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" '
            'markerHeight="6" orient="auto"><path d="M2 1L8 5L2 9" fill="none" stroke="%s" '
            'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>'
            % (k, c) for k, c in (("g", SUB), ("r", "#D85A30"))) + '</defs>')
        s = ('<svg width="100%%" viewBox="0 0 %d %d" role="img" xmlns="http://www.w3.org/2000/svg" '
             'font-family=\'%s\'><title>%s</title><desc>%s</desc>%s\n%s\n</svg>\n'
             % (self.w, h, FONT, html.escape(self.title), html.escape(self.desc), defs, "\n".join(self.o)))
        with open(os.path.join(SVG_DIR, name), "w", encoding="utf-8") as f:
            f.write(s)


def hdr(sv, l1, l2=None):
    sv.t(40, 18, l1)
    if l2:
        sv.t(40, 38, l2)


# ---------------------------------------------------------------- 代码 (doc 里展示的原文, 同时被 exec 测试)
CODE = {}

CODE["template"] = '''
# prefix[i] = nums[0] + ... + nums[i-1]      prefix[0] = 0 (空前缀)
prefix = [0] * (len(nums) + 1)
for i, x in enumerate(nums):
    prefix[i + 1] = prefix[i] + x            # 每个元素只加一次: O(n)

def range_sum(i, j):                         # nums[i..j] 闭区间
    return prefix[j + 1] - prefix[i]         # 两次查表: O(1)
'''

CODE["hash_template"] = '''
# 空前缀 prefix = 0 出现过 1 次, 让 "从下标 0 开始" 的 subarray 也能被数到
count = {0: 1}
prefix = ans = 0
for x in nums:
    prefix += x
    need = prefix - k                        # 要找的起点 prefix 值
    ans += count.get(need, 0)                # 以当前位置结尾, 有多少个起点
    count[prefix] = count.get(prefix, 0) + 1   # 先查再放: 起点在当前位置之前
'''

CODE["pivot"] = '''
def pivotIndex(nums):
    total = sum(nums)
    left = 0                                 # nums[0..i-1] 之和 = prefix[i]
    for i, x in enumerate(nums):
        if left == total - left - x:         # right = total - left - nums[i]
            return i
        left += x                            # 处理完 i, left 变成 prefix[i+1]
    return -1
'''

CODE["subk"] = '''
def subarraySum(nums, k):
    count = {0: 1}                           # 别忘了: 空前缀 0 出现 1 次
    prefix = ans = 0
    for x in nums:
        prefix += x
        need = prefix - k
        ans += count.get(need, 0)            # 之前有多少个 prefix == need
        count[prefix] = count.get(prefix, 0) + 1   # 查完才放进去
    return ans
'''

CODE["divk"] = '''
def subarraysDivByK(nums, k):
    count = {0: 1}
    prefix = ans = 0
    for x in nums:
        # Python 的 % 对负数也返回 0..k-1, 不用额外处理
        prefix = (prefix + x) % k
        ans += count.get(prefix, 0)          # 余数相同的前缀两两配对
        count[prefix] = count.get(prefix, 0) + 1
    return ans

# Continuous Subarray Sum: 长度 >= 2, 和是 k 的倍数, 求 "存在"
def checkSubarraySum(nums, k):
    first = {0: -1}                          # 余数 0 出现在下标 -1 (空前缀)
    prefix = 0
    for i, x in enumerate(nums):
        prefix = (prefix + x) % k
        if prefix in first:
            if i - first[prefix] >= 2:       # 长度至少 2
                return True
        else:
            first[prefix] = i                # 只记第一次: 越早越长, 不覆盖
    return False
'''

CODE["contig"] = '''
def findMaxLength(nums):
    first = {0: -1}                          # first[s] = s 第一次出现的下标
    s = best = 0
    for i, x in enumerate(nums):
        # 0 看成 -1: 0 和 1 一样多 <=> 区间和为 0
        s += 1 if x == 1 else -1
        if s in first:
            best = max(best, i - first[s])   # 长度 = i - first[s]
        else:
            first[s] = i                     # 求最长: 只记最早, 不覆盖
    return best
'''

CODE["maxlen_k"] = '''
# Maximum Size Subarray Sum Equals k
def maxSubArrayLen(nums, k):
    first = {0: -1}
    prefix = best = 0
    for i, x in enumerate(nums):
        prefix += x
        if prefix - k in first:
            best = max(best, i - first[prefix - k])
        if prefix not in first:              # 先查后放, 且不覆盖
            first[prefix] = i
    return best
'''

CODE["product"] = '''
def productExceptSelf(nums):
    n = len(nums)
    out = [1] * n
    l = 1                                    # l = nums[0..i-1] 的乘积
    for i in range(n):
        out[i] = l                           # 先存 "左边所有数的乘积"
        l *= nums[i]
    r = 1                                    # r = nums[i+1..n-1] 的乘积
    for i in range(n - 1, -1, -1):
        out[i] *= r                          # 再乘 "右边所有数的乘积"
        r *= nums[i]
    return out                               # 额外空间 O(1) (out 是答案)
'''

CODE["matrix"] = '''
class NumMatrix:
    def __init__(self, matrix):
        m, n = len(matrix), len(matrix[0])
        # P[i][j] = matrix 左上角 i 行 j 列的和
        self.P = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m):
            for j in range(n):
                # P[i][j] 和 P[i+1][j] 重叠的部分加了两次, 减一次
                self.P[i + 1][j + 1] = (matrix[i][j] + self.P[i][j + 1]
                                        + self.P[i + 1][j] - self.P[i][j])

    def sumRegion(self, r1, c1, r2, c2):
        P = self.P
        return (P[r2 + 1][c2 + 1] - P[r1][c2 + 1]
                - P[r2 + 1][c1] + P[r1][c1])   # 左上角被减了两次, 加回来
'''

CODE["flights"] = '''
def corpFlightBookings(bookings, n):
    diff = [0] * (n + 1)                     # 多留一格: last 可能等于 n
    for first, last, seats in bookings:      # 航班编号从 1 开始
        diff[first - 1] += seats             # 从 first 开始, 每个位置 +seats
        diff[last] -= seats                  # 过了 last 就抵消掉
    ans, cur = [], 0
    for i in range(n):
        cur += diff[i]                       # 对 diff 做 prefix sum = 还原
        ans.append(cur)
    return ans

def carPooling(trips, capacity):
    diff = [0] * 1001
    for num, start, end in trips:
        diff[start] += num
        diff[end] -= num                     # end 站已下车: 区间 [start, end)
    cur = 0
    for dx in diff:
        cur += dx
        if cur > capacity:
            return False
    return True
'''

CODE["window_pos"] = '''
# 全是正数: sliding window
def minSubArrayLen(target, nums):
    left = total = 0
    best = len(nums) + 1
    for right, x in enumerate(nums):
        total += x                           # 右移: total 只会变大
        while total >= target:               # 够了就缩左边: total 只会变小
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return best if best <= len(nums) else 0
'''

CODE["window_neg"] = '''
# 错误示范: 把 window 套到 "有负数" 的 Subarray Sum Equals K
def wrong(nums, k):
    left = total = ans = 0
    for right, x in enumerate(nums):
        total += x
        while total > k and left <= right:   # 以为 "超过 k 就缩左边"
            total -= nums[left]              # 但后面的负数会把 total 拉回来
            left += 1
        if total == k:
            ans += 1
    return ans
'''


def run(name, fn):
    ns = {}
    exec(CODE[name], ns)
    return ns[fn]


def brute_sub(nums, k, pred):
    n, c = len(nums), 0
    for i in range(n):
        for j in range(i, n):
            if pred(sum(nums[i:j + 1]), j - i + 1):
                c += 1
    return c


def selftest():
    rnd = random.Random(7)
    ns = {}
    # template
    for _ in range(200):
        nums = [rnd.randint(-5, 5) for _ in range(rnd.randint(1, 9))]
        ns = {"nums": nums}
        exec(CODE["template"], ns)
        for i in range(len(nums)):
            for j in range(i, len(nums)):
                assert ns["range_sum"](i, j) == sum(nums[i:j + 1])
        k = rnd.randint(-4, 4)
        ns = {"nums": nums, "k": k}
        exec(CODE["hash_template"], ns)
        assert ns["ans"] == brute_sub(nums, k, lambda s, L: s == k)
    piv, sk, dk = run("pivot", "pivotIndex"), run("subk", "subarraySum"), run("divk", "subarraysDivByK")
    ns = {}
    exec(CODE["divk"], ns)
    chk = ns["checkSubarraySum"]
    mx = run("contig", "findMaxLength")
    ml = run("maxlen_k", "maxSubArrayLen")
    pe = run("product", "productExceptSelf")
    fb, cp = {}, {}
    exec(CODE["flights"], fb)
    mw = run("window_pos", "minSubArrayLen")
    wr = run("window_neg", "wrong")
    for _ in range(400):
        nums = [rnd.randint(-5, 5) for _ in range(rnd.randint(1, 9))]
        n = len(nums)
        want = [i for i in range(n) if sum(nums[:i]) == sum(nums[i + 1:])]
        assert piv(nums) == (want[0] if want else -1)
        k = rnd.randint(-6, 6)
        assert sk(nums, k) == brute_sub(nums, k, lambda s, L: s == k)
        kk = rnd.randint(1, 6)
        assert dk(nums, kk) == brute_sub(nums, kk, lambda s, L: s % kk == 0)
        assert chk(nums, kk) == (brute_sub(nums, kk, lambda s, L: L >= 2 and s % kk == 0) > 0)
        bits = [rnd.randint(0, 1) for _ in range(n)]
        bl = 0
        for i in range(n):
            for j in range(i, n):
                seg = bits[i:j + 1]
                if seg.count(0) == seg.count(1):
                    bl = max(bl, j - i + 1)
        assert mx(bits) == bl
        bl = 0
        for i in range(n):
            for j in range(i, n):
                if sum(nums[i:j + 1]) == k:
                    bl = max(bl, j - i + 1)
        assert ml(nums, k) == bl
        prod = []
        for i in range(n):
            q = 1
            for j in range(n):
                if j != i:
                    q *= nums[j]
            prod.append(q)
        assert pe(nums) == prod
        pos = [rnd.randint(1, 5) for _ in range(n)]
        tg = rnd.randint(1, 12)
        b = min([j - i + 1 for i in range(n) for j in range(i, n) if sum(pos[i:j + 1]) >= tg] or [0])
        assert mw(tg, pos) == b
    # 2D
    ns = {}
    exec(CODE["matrix"], ns)
    for _ in range(100):
        m, n = rnd.randint(1, 5), rnd.randint(1, 5)
        M = [[rnd.randint(-5, 5) for _ in range(n)] for _ in range(m)]
        nm = ns["NumMatrix"](M)
        r1, r2 = sorted((rnd.randrange(m), rnd.randrange(m)))
        c1, c2 = sorted((rnd.randrange(n), rnd.randrange(n)))
        assert nm.sumRegion(r1, c1, r2, c2) == sum(M[i][j] for i in range(r1, r2 + 1) for j in range(c1, c2 + 1))
    # flights / car pooling
    for _ in range(200):
        n = rnd.randint(1, 7)
        bk = []
        for _ in range(rnd.randint(0, 5)):
            a = rnd.randint(1, n)
            b = rnd.randint(a, n)
            bk.append([a, b, rnd.randint(1, 9)])
        want = [sum(s for a, b, s in bk if a <= i <= b) for i in range(1, n + 1)]
        assert fb["corpFlightBookings"](bk, n) == want
        trips = []
        for _ in range(rnd.randint(1, 4)):
            a = rnd.randint(0, 8)
            trips.append([rnd.randint(1, 5), a, rnd.randint(a + 1, 9)])
        cap = rnd.randint(1, 10)
        ok = all(sum(t[0] for t in trips if t[1] <= x < t[2]) <= cap for x in range(0, 10))
        assert fb["carPooling"](trips, cap) == ok
    assert wr([5, -2, 0], 3) == 0 and sk([5, -2, 0], 3) == 2
    print("selftest ok")


selftest()


# ---------------------------------------------------------------- SVG 0: 第一性原理
def prefix_of(nums):
    p = [0]
    for x in nums:
        p.append(p[-1] + x)
    return p


def svg_range_core():
    nums = [3, 1, 4, 1, 5]
    P = prefix_of(nums)
    i, j = 1, 3
    assert P[j + 1] - P[i] == sum(nums[i:j + 1]) == 6
    sv = Svg("sum(i..j) = prefix[j+1] - prefix[i]",
             "区间和等于两个前缀和之差，query 从 O(n) 变 O(1)")
    hdr(sv, "nums = [3, 1, 4, 1, 5] · query: sum(nums[1..3])",
        "prefix[k] = 前 k 个数之和 = nums[0] + ... + nums[k-1] · prefix[0] = 0")
    x0, cw = 70, 44
    sv.t(40, 66, "nums", 14, INK, weight=500)
    roles = ["new" if i <= t <= j else "other" for t in range(5)]
    sv.cells(x0, 80, nums, roles, cw=cw, idx=[str(t) for t in range(5)], idx_dy=-8)
    # brace 1: prefix[4]
    xe = x0 + 4 * cw - 3
    sv.line(x0, 128, xe, 128, "#0F6E56", 2)
    sv.t(xe + 14, 128, "prefix[4] = 3 + 1 + 4 + 1 = 9", 12, "#085041")
    sv.line(x0, 150, x0 + cw - 3, 150, "#D85A30", 2)
    sv.t(x0 + cw + 11, 150, "prefix[1] = 3 (这一段要减掉)", 12, "#712B13")
    sv.t(40, 190, "sum(nums[1..3]) = prefix[4] - prefix[1] = 9 - 3 = 6", 16, INK, weight=500)
    sv.t(40, 212, "相同的开头 nums[0] = 3 被减掉了, 剩下的正好是 1 + 4 + 1 = 6", 12)
    sv.sep(232)
    sv.t(40, 262, "prefix", 14, INK, weight=500)
    pr = ["other"] * 6
    pr[1], pr[4] = "gone", "new"
    sv.cells(x0, 276, P, pr, cw=cw, rings=(4,), idx=[str(t) for t in range(6)], idx_dy=-8)
    # 两栏对比
    sv.box(40, 322, 290, 66, "gone", [("brute force: 每次 query 从头加", 14, 500),
                                      ("1 + 4 + 1 → O(n) 每次", 12, 400),
                                      ("q 次 query: O(n · q)", 12, 400)])
    sv.box(350, 322, 290, 66, "new", [("prefix: 建表一次 O(n)", 14, 500),
                                      ("每次 query 查两个格子 → O(1)", 12, 400),
                                      ("q 次 query: O(n + q)", 12, 400)])
    sv.legend(412, [("new", "要的前缀 / 要的区间"), ("gone", "要减掉的前缀"), ("other", "其他")])
    sv.save("range_sum_core.svg", 430)


# ---------------------------------------------------------------- SVG 1: Find Pivot Index
def svg_pivot():
    nums = [1, 7, 3, 6, 5, 6]
    total = sum(nums)
    assert total == 28
    # core
    sv = Svg("Find Pivot Index 的 invariant", "left == total - left - nums[i]")
    hdr(sv, "nums = [1, 7, 3, 6, 5, 6] · total = 1 + 7 + 3 + 6 + 5 + 6 = 28",
        "pivot i: 左边所有数之和 == 右边所有数之和 (不含 nums[i])")
    x0, cw = 70, 70
    roles = ["other", "other", "other", "new", "plain", "plain"]
    sv.cells(x0, 80, nums, roles, cw=cw, ch=36, rings=(3,), idx=["i=%d" % t for t in range(6)], idx_dy=-9)
    sv.line(x0, 134, x0 + 3 * cw - 3, 134, "#5F5E5A", 2)
    sv.t(x0, 152, "left = prefix[3] = 1 + 7 + 3 = 11", 12, INK)
    sv.line(x0 + 4 * cw, 134, x0 + 6 * cw - 3, 134, "#5F5E5A", 2)
    sv.t(x0 + 4 * cw, 152, "right = 5 + 6 = 11", 12, INK)
    sv.t(x0 + 3 * cw + 32, 108 + 30, "x = 6", 12, "#085041", "middle", 500)
    sv.sep(176)
    sv.t(40, 204, "right 不用再加一遍: right = total - left - nums[i] = 28 - 11 - 6 = 11", 14, INK, weight=500)
    sv.t(40, 228, "所以判断条件是 left == total - left - nums[i]:  11 == 11 ✓", 14, INK, weight=500)
    sv.box(40, 252, 290, 62, "gone", [("brute force: 每个 i 重新加左右两边", 14, 500),
                                      ("每个 i 要 O(n) → 总共 O(n²)", 12, 400)])
    sv.box(350, 252, 290, 62, "new", [("prefix: left 边走边累加", 14, 500),
                                      ("right 用 total 减出来 → O(n)", 12, 400)])
    sv.legend(338, [("other", "left 区域"), ("new", "当前 nums[i]"), ("plain", "right 区域")])
    sv.save("pivot_core.svg", 356)

    # trace
    sv = Svg("Find Pivot Index trace", "每个 i 算 left 和 right 并比较")
    hdr(sv, "total = 1 + 7 + 3 + 6 + 5 + 6 = 28",
        "每一步: left = nums[0..i-1] 之和 → right = total - left - nums[i] → 比较")
    sv.t(40, 76, "nums[i]", 12); sv.t(134, 76, "数组", 12)
    sv.t(330, 76, "left / right", 12); sv.t(540, 76, "比较", 12)
    sv.sep(88)
    left = 0
    y = 98
    found = None
    for i, x in enumerate(nums):
        right = total - left - x
        lterm = " + ".join(str(v) for v in nums[:i]) or "空"
        eq = left == right
        roles = ["other" if t < i else "new" if t == i else "plain" for t in range(6)]
        sv.box(40, y + 4, 80, 48, "new", [("i = %d" % i, 14, 500), ("nums[i] = %d" % x, 12, 400)])
        sv.cells(134, y + 14, nums, roles, cw=30, ch=28, rings=(i,))
        sv.t(330, y + 4, ("left = %s = %d" % (lterm, left)) if i > 1 else ("left = %d" % left if i else "left = 0 (左边没有数)"), 12, INK)
        sv.t(330, y + 26, "right = 28 - %d - %d = %d" % (left, x, right), 12, INK)
        sv.t(330, y + 48, "", 12)
        sv.t(540, y + 14, "%d %s %d" % (left, "==" if eq else "≠", right), 14, "#085041" if eq else INK, weight=500)
        if eq:
            sv.t(540, y + 38, "pivot = %d" % i, 14, "#085041", weight=500)
            found = i
        else:
            sv.t(540, y + 38, "不是, left += %d" % x, 12)
        y += 66
        sv.sep(y - 8)
        if eq:
            break
        left += x
    sv.t(40, y + 14, "答案: pivot = %d (left = 1 + 7 + 3 = 11, right = 5 + 6 = 11)" % found, 14, INK, weight=500)
    sv.legend(y + 44, [("other", "已在 left 里"), ("new", "当前 nums[i]"), ("plain", "right 区域")])
    sv.save("pivot_trace.svg", y + 64)
    assert found == 3



# ---------------------------------------------------------------- SVG 2: Subarray Sum Equals K
SUBK_NUMS, SUBK_K = [3, 4, 7, 2, -3, 1, 4, 2], 7


def svg_subk():
    nums, k = SUBK_NUMS, SUBK_K
    P = prefix_of(nums)
    assert P == [0, 3, 7, 14, 16, 13, 14, 18, 20]
    sv = Svg("Subarray Sum Equals K 的核心", "以 j 结尾、和为 k 的 subarray 个数 = 之前有多少个 prefix == prefix_j - k")
    hdr(sv, "nums = [3, 4, 7, 2, -3, 1, 4, 2], k = 7 · prefix[t] = 前 t 个数之和",
        "nums[i..j-1] 的和 = prefix[j] - prefix[i] · 要它 == k  ⟺  prefix[i] == prefix[j] - k")
    x0, pitch, w = 42, 66, 56
    cx = lambda t: x0 + w / 2 + pitch * t
    sv.t(40, 66, "prefix (下标 t = 0..8)", 12, INK, weight=500)
    roles = []
    for t in range(9):
        roles.append("new" if t == 6 else "gone" if t == 2 else "other" if t < 6 else "plain")
    for t in range(9):
        sv.box(cx(t) - w / 2, 100, w, 32, roles[t], [(str(P[t]), 14, 500)], ring=(t == 6))
        sv.t(cx(t), 86, "t=%d" % t, 12, SUB, "middle")
    # nums between
    for t in range(8):
        r = "new" if 2 <= t <= 5 else "plain"
        sv.box(cx(t) + pitch / 2 - w / 2 + 6, 176, w - 12, 28, r, [(str(nums[t]), 14, 500)])
    sv.t(40, 160, "nums (夹在两个 prefix 之间)", 12, SUB)
    # brace over earlier prefixes
    sv.line(cx(0) - w / 2, 232, cx(5) + w / 2, 232, "#5F5E5A", 2)
    sv.t(cx(0) - w / 2, 250, "t = 0..5: 已经放进 count 的 prefix (j 之前的所有起点候选)", 12, INK)
    # arrow j -> i
    sv.arrow([(cx(6), 134), (cx(6), 150), (cx(2) + 8, 150), (cx(2) + 8, 134)], "#D85A30", True)
    sv.t((cx(6) + cx(2)) / 2 + 4, 144, "找 prefix[i] = 14 - 7 = 7", 12, "#712B13", "middle")
    sv.sep(268)
    sv.t(40, 292, "j = 6: prefix[6] = 14 · 要找 prefix[i] = 14 - 7 = 7 · count 里 7 出现 1 次 (t = 2)", 14, INK, weight=500)
    sv.t(40, 316, "=> 以 j 结尾有 1 个答案: nums[2..5] = 7 + 2 + (-3) + 1 = 7", 14, INK, weight=500)
    sv.t(40, 346, "为什么先查再放: 起点 i 必须在 j 之前, 当前 prefix 还没放进 count, 不会自己和自己配对", 12)
    sv.box(40, 366, 290, 62, "gone", [("brute force: 对每个 j 回头扫所有 i", 14, 500),
                                      ("n 个 j × n 个 i → O(n²)", 12, 400)])
    sv.box(350, 366, 290, 62, "new", [("count: prefix → 出现次数", 14, 500),
                                      ("查 count[prefix - k] 是 O(1) → O(n)", 12, 400)])
    sv.t(40, 452, "{0: 1} 的作用: prefix[0] = 0 是空前缀。t = 2 时 prefix = 7, need = 7 - 7 = 0, 靠它数到 [3, 4]", 12, INK)
    sv.legend(480, [("new", "当前 prefix[j]"), ("gone", "要找的 prefix[i]"), ("other", "j 之前"), ("plain", "还没到")])
    sv.save("subk_core.svg", 498)


def subk_steps():
    nums, k = SUBK_NUMS, SUBK_K
    count = {0: 1}
    prefix = ans = 0
    steps = []
    for i, x in enumerate(nums):
        prefix += x
        need = prefix - k
        got = count.get(need, 0)
        ans += got
        count[prefix] = count.get(prefix, 0) + 1
        steps.append(dict(i=i, x=x, prefix=prefix, need=need, got=got, ans=ans,
                          count=list(count.items())))
    return steps


def svg_subk_trace():
    steps = subk_steps()
    for s in steps:
        print("subk", s["i"], s["x"], s["prefix"], s["need"], s["got"], s["ans"], s["count"])
    assert steps[-1]["ans"] == 4
    sv = Svg("Subarray Sum Equals K trace", "count 与 ans 每一步的变化")
    hdr(sv, "k = 7 · count 初始 {0: 1} · 每一步: prefix += nums[i] → 查 count[prefix - k] 加进 ans → count[prefix] += 1",
        "count 里每个格子是 prefix: 出现次数")
    sv.t(40, 64, "nums[i]", 12); sv.t(154, 64, "查 count (先查)", 12)
    sv.t(318, 64, "ans", 12); sv.t(394, 64, "count (后放)", 12)
    sv.sep(74)
    y = 84
    prev_keys = {0}
    for s in steps:
        h = 64
        sv.box(40, y + 6, 100, 50, "new", [("nums[%d] = %d" % (s["i"], s["x"]), 14, 500),
                                          ("prefix = %d" % s["prefix"], 12, 400)])
        sv.t(154, y + 14, "need = %d - %d = %d" % (s["prefix"], SUBK_K, s["need"]), 12, INK)
        if s["got"]:
            sv.t(154, y + 34, "count[%d] = %d → 命中" % (s["need"], s["got"]), 12, "#085041", weight=500)
        else:
            sv.t(154, y + 34, "count[%d] 没有 → +0" % s["need"], 12, INK)
        sv.t(318, y + 14, "ans = %d" % s["ans"], 14, INK, weight=500)
        if s["got"]:
            sv.t(318, y + 36, "(+%d)" % s["got"], 12, "#085041")
        new = {s["prefix"]}
        hit = {s["need"]} if s["got"] else set()
        sv.chips(394, y + 4, s["count"], 4, cw=56, ch=22, new=new, hit=hit)
        y += h
        sv.sep(y + 2)
        y += 6
    sv.t(40, y + 16, "答案 ans = 4: [3, 4] · [7] · [7, 2, -3, 1] · [1, 4, 2]", 14, INK, weight=500)
    sv.legend(y + 46, [("new", "本步 prefix 放进 count (次数 +1)"), ("ring", "被查到的 key")])
    sv.save("subk_trace.svg", y + 64)


# ---------------------------------------------------------------- SVG 3: Subarray Sums Divisible by K
DIV_NUMS, DIV_K = [4, 5, 0, -2, -3, 1], 5


def svg_div():
    nums, k = DIV_NUMS, DIV_K
    P = prefix_of(nums)
    mods = [p % k for p in P]
    assert P == [0, 4, 9, 9, 7, 4, 5] and mods == [0, 4, 4, 4, 2, 4, 0]
    sv = Svg("余数相同的 prefix 两两配对", "prefix 对 k 取余后同桶的两个 prefix 之差是 k 的倍数")
    hdr(sv, "nums = [4, 5, 0, -2, -3, 1], k = 5 · prefix = [0, 4, 9, 9, 7, 4, 5] (P0..P6)",
        "(P[j] - P[i]) % 5 == 0  ⟺  P[j] % 5 == P[i] % 5 · 把 P 按 % 5 的余数分桶")
    bw, bh, bx = 112, 150, 40
    members = {r: [t for t in range(7) if mods[t] == r] for r in range(5)}
    for r in range(5):
        x = bx + r * (bw + 10) - (0 if r else 0)
        m = members[r]
        role = "other" if m else "plain"
        sv.box(x, 70, bw, bh, role, [])
        sv.t(x + bw / 2, 88, "余数 r = %d" % r, 14, INK, "middle", 500)
        for q, t in enumerate(m):
            rr, cc = divmod(q, 2)
            sv.circ(x + 32 + cc * 48, 124 + rr * 44, 18, "new" if len(m) > 1 else "other", "P%d" % t)
        pairs = len(m) * (len(m) - 1) // 2
        sv.t(x + bw / 2, 236, "%d 个 → C(%d,2) = %d 对" % (len(m), len(m), pairs) if m else "空", 12, INK, "middle")
    assert sum(len(m) * (len(m) - 1) // 2 for m in members.values()) == 7
    sv.sep(256)
    sv.t(40, 282, "每个 '同桶的一对' = 一个答案: ans = 1 + 6 + 0 = 7", 14, INK, weight=500)
    sv.t(40, 306, "边走边数: 新 prefix 放进桶之前, 桶里已有 c 个 → ans += c (c 就是 count[prefix])", 14, INK, weight=500)
    sv.t(40, 336, "和 Subarray Sum Equals K 的区别: 不再找 'prefix - k', 而是找 '同余数'; key 从 prefix 换成 prefix % k", 12)
    sv.t(40, 358, "桶的个数只有 k 个, count 最多 k 项", 12)
    sv.legend(386, [("new", "同桶有配对"), ("other", "桶里只有 1 个, 没有配对")])
    sv.save("divk_core.svg", 404)


def svg_div_trace():
    nums, k = DIV_NUMS, DIV_K
    count = {0: 1}
    prefix = ans = 0
    sv = Svg("Subarray Sums Divisible by K trace", "每步取余、查桶、放入桶")
    hdr(sv, "k = 5 · count 初始 {0: 1} · 每一步: prefix = (prefix + nums[i]) % 5 → ans += count[prefix] → count[prefix] += 1",
        "count 里每个格子是 余数: 出现次数")
    sv.t(40, 64, "nums[i]", 12); sv.t(154, 64, "取余", 12)
    sv.t(310, 64, "查桶 / ans", 12); sv.t(430, 64, "count (后放)", 12)
    sv.sep(74)
    y = 84
    for i, x in enumerate(nums):
        old = prefix
        prefix = (prefix + x) % k
        got = count.get(prefix, 0)
        ans += got
        count[prefix] = count.get(prefix, 0) + 1
        print("div", i, x, old, prefix, got, ans, list(count.items()))
        sv.box(40, y + 4, 100, 40, "new", [("nums[%d] = %d" % (i, x), 14, 500)])
        sv.t(154, y + 10, "(%d + %d) %% 5" % (old, x), 12, INK)
        sv.t(154, y + 30, "prefix = %d" % prefix, 14, INK, weight=500)
        sv.t(310, y + 10, "count[%d] = %d" % (prefix, got), 12, "#085041" if got else INK, weight=500 if got else 400)
        sv.t(310, y + 30, "ans = %d" % ans, 14, INK, weight=500)
        sv.chips(430, y + 12, list(count.items()), 5, cw=38, ch=22, gx=4, new={prefix}, hit={prefix} if got else set())
        y += 56
        sv.sep(y - 2)
    assert ans == 7
    sv.t(40, y + 16, "答案 ans = 7 (和上一张图里 1 + 6 对得上)", 14, INK, weight=500)
    sv.legend(y + 46, [("new", "本步 prefix 放进去 (次数 +1)"), ("ring", "查到的桶 (放之前已有 ≥ 1 个)")])
    sv.save("divk_trace.svg", y + 64)
    # 注: 被查到的桶也是刚放进去的桶, 所以 ring 和绿色重合


# ---------------------------------------------------------------- SVG 4: Contiguous Array
CON_NUMS = [0, 1, 1, 0, 1, 1, 1, 0]


def svg_contig():
    nums = CON_NUMS
    s, S = 0, [0]
    for x in nums:
        s += 1 if x == 1 else -1
        S.append(s)
    assert S == [0, -1, 0, 1, 0, 1, 2, 3, 2]
    sv = Svg("Contiguous Array: 0 看成 -1", "两个相同的前缀和之间 0 和 1 一样多")
    hdr(sv, "nums = [0, 1, 1, 0, 1, 1, 1, 0] · 0 看成 -1, 1 还是 +1 · s = 前 t 个数的和",
        "0 和 1 一样多 ⟺ 区间和为 0 ⟺ 两个 s 相等 · 求最长 → 每个 s 只记第一次出现的下标")
    X = lambda t: 60 + 70 * t
    Y = lambda v: 222 - (v + 1) * 34
    for v in range(-1, 4):
        sv.line(50, Y(v), 630, Y(v), "#E4E2DB", 1)
        sv.t(40, Y(v), str(v), 12, SUB, "end")
    pts = [(X(t), Y(S[t])) for t in range(9)]
    sv.o.append('<polyline points="%s" fill="none" stroke="#5F5E5A" stroke-width="1.5"/>'
                % " ".join("%s,%s" % p for p in pts))
    sv.line(X(0), Y(0), X(4), Y(0), "#0F6E56", 2, True)
    for t in range(9):
        role = "new" if t == 4 else "gone" if t == 0 else "other"
        sv.circ(X(t), Y(S[t]), 12, role, "", ring=(t == 4))
        sv.t(X(t), 246, "t=%d" % t, 12, SUB, "middle")
    for t in range(8):
        sv.t((X(t) + X(t + 1)) / 2, 268, "%d→%s" % (nums[t], "+1" if nums[t] else "-1"), 12, SUB, "middle")
    sv.t(40, 268, "", 12)
    sv.t(X(0) - 16, Y(0) - 26, "第一次 s = 0", 12, "#712B13", "start")
    sv.t(X(4) - 20, Y(0) - 32, "再次 s = 0", 12, "#085041", "start")
    sv.t(X(1), 100, "t = 2 的 s 也是 0, 但 first[0] 不覆盖 (越早越长)", 12, SUB, "start")
    sv.sep(286)
    sv.t(40, 310, "t = 0 和 t = 4 的 s 都是 0 → nums[0..3] = [0, 1, 1, 0], 长度 = 4 - 0 = 4", 14, INK, weight=500)
    sv.t(40, 334, "用 nums 的下标: s 在 i = -1 (空前缀) 出现过, 到 i = 3 又是 0: 长度 = 3 - (-1) = 4", 12, INK)
    sv.box(40, 352, 290, 62, "gone", [("brute force: 每个子数组数 0 和 1", 14, 500),
                                      ("O(n²) 个子数组 → O(n²) (或 O(n³))", 12, 400)])
    sv.box(350, 352, 290, 62, "new", [("first[s] = s 第一次出现的位置", 14, 500),
                                      ("一遍扫描 → O(n)", 12, 400)])
    sv.legend(438, [("gone", "第一次出现"), ("new", "再次出现, 长度 4"), ("other", "其他")])
    sv.save("contig_core.svg", 456)


def svg_contig_trace():
    nums = CON_NUMS
    first = {0: -1}
    s = best = 0
    sv = Svg("Contiguous Array trace", "first 字典与 best 的变化")
    hdr(sv, "first 初始 {0: -1} · 每一步: s += (1 或 -1) → s 见过就 best = max(best, i - first[s]) → 没见过就记 first[s] = i",
        "first 里每个格子是 s: 第一次出现的下标")
    sv.t(40, 64, "nums[i]", 12); sv.t(154, 64, "s 和 first", 12)
    sv.t(318, 64, "长度 / best", 12); sv.t(436, 64, "first (只放不覆盖)", 12)
    sv.sep(74)
    y = 84
    for i, x in enumerate(nums):
        old = s
        step = 1 if x == 1 else -1
        s += step
        seen = s in first
        cand = None
        if seen:
            cand = i - first[s]
            best = max(best, cand)
        else:
            first[s] = i
        print("contig", i, x, old, s, seen, cand, best, list(first.items()))
        sv.box(40, y + 4, 100, 44, "new", [("nums[%d] = %d" % (i, x), 14, 500), ("加 %s1" % ("+" if step > 0 else "-"), 12, 400)])
        sv.t(154, y + 10, "s = %d %s 1 = %d" % (old, "+" if step > 0 else "-", s), 12, INK)
        sv.t(154, y + 30, ("first[%d] = %d → 见过" % (s, first[s])) if seen else "first[%d] 没有 → 记下 %d" % (s, i),
             12, "#085041" if seen else INK, weight=500 if seen else 400)
        if seen:
            sv.t(318, y + 10, "%d - (%d) = %d" % (i, first[s], cand), 12, INK)
        else:
            sv.t(318, y + 10, "不算长度", 12, SUB)
        sv.t(318, y + 30, "best = %d" % best, 14, INK, weight=500)
        sv.chips(436, y + 12, list(first.items()), 5, cw=36, ch=22, gx=4,
                 new={s} if not seen else set(), hit={s} if seen else set())
        y += 56
        sv.sep(y - 2)
    assert best == 4
    sv.t(40, y + 16, "答案 best = 4 (nums[0..3] = [0, 1, 1, 0])", 14, INK, weight=500)
    sv.legend(y + 46, [("new", "新记下的 s"), ("ring", "再次遇到 → 算长度")])
    sv.save("contig_trace.svg", y + 64)



# ---------------------------------------------------------------- SVG 5: Product of Array Except Self
PNUMS = [1, 2, 3, 4]


def svg_product():
    nums = PNUMS
    n = len(nums)
    L, R = [1] * n, [1] * n
    for i in range(1, n):
        L[i] = L[i - 1] * nums[i - 1]
    for i in range(n - 2, -1, -1):
        R[i] = R[i + 1] * nums[i + 1]
    out = [a * b for a, b in zip(L, R)]
    assert L == [1, 1, 2, 6] and R == [24, 12, 4, 1] and out == [24, 12, 8, 6]
    sv = Svg("Product of Array Except Self 的核心", "out[i] = 左边所有数的积 × 右边所有数的积")
    hdr(sv, "nums = [1, 2, 3, 4] · 不能用除法 (有 0) · out[i] = nums[i] 左边所有数的积 × 右边所有数的积",
        "prefix 不只能是加法: 前缀积 / 后缀积 同理")
    X = lambda i: 200 + 96 * i
    rows = [("nums", 74), ("L[i] = nums[0..i-1] 的积", 130), ("R[i] = nums[i+1..3] 的积", 186), ("out[i] = L[i] × R[i]", 242)]
    for name, y in rows:
        sv.t(40, y + 15, name, 12, INK)
    for i in range(n):
        sv.t(X(i) + 36, 62, "i=%d" % i, 12, SUB, "middle")
        sv.box(X(i), 74, 72, 30, "gone" if i == 2 else "plain", [(str(nums[i]), 14, 500)])
        sv.box(X(i), 130, 72, 30, "new", [(str(L[i]), 14, 500)])
        sv.box(X(i), 186, 72, 30, "other", [(str(R[i]), 14, 500)])
        sv.box(X(i), 242, 72, 30, "plain", [(str(out[i]), 14, 500)], ring=(i == 2))
        sv.t(X(i) + 36, 288, "%d × %d" % (L[i], R[i]), 12, INK, "middle")
    sv.t(X(2) + 36, 118, "i=2 的 nums[2] = 3 被跳过", 12, "#712B13", "middle")
    sv.sep(308)
    sv.t(40, 332, "i = 2: 左边 1 × 2 = 2, 右边 4 → out[2] = 2 × 4 = 8 (3 自己不参与)", 14, INK, weight=500)
    sv.t(40, 356, "L[i] = L[i-1] × nums[i-1] 一个一个滚出来, R 从右往左同理, 每个元素只乘一次 → O(n)", 12)
    sv.box(40, 376, 290, 62, "gone", [("brute force: 每个 i 乘其余 n-1 个数", 14, 500),
                                      ("n × n → O(n²)", 12, 400)])
    sv.box(350, 376, 290, 62, "new", [("L 存进 out, R 用一个变量 r 滚", 14, 500),
                                      ("时间 O(n), 额外空间 O(1)", 12, 400)])
    sv.legend(462, [("new", "L (左边的积)"), ("other", "R (右边的积)"), ("gone", "被跳过的 nums[i]")])
    sv.save("product_core.svg", 480)


def svg_product_trace():
    nums = PNUMS
    n = len(nums)
    sv = Svg("Product of Array Except Self trace", "两遍扫描，out 和 l / r 的变化")
    hdr(sv, "out 初始 [1, 1, 1, 1]",
        "第 1 遍 (左→右): out[i] = l, 然后 l *= nums[i] · 第 2 遍 (右→左): out[i] *= r, 然后 r *= nums[i]")
    sv.t(40, 64, "nums[i]", 12); sv.t(160, 64, "out", 12); sv.t(340, 64, "计算", 12)
    sv.sep(74)
    y = 84
    out = [1] * n
    sv.t(40, y + 6, "第 1 遍 (左→右): out[i] = l = i 左边所有数的积", 12, INK, weight=500)
    y += 20
    l = 1
    for i in range(n):
        out[i] = l
        oldl = l
        l *= nums[i]
        roles = ["other" if t < i else "new" if t == i else "plain" for t in range(n)]
        sv.box(40, y + 2, 100, 38, "new", [("i = %d" % i, 14, 500), ("nums[i] = %d" % nums[i], 12, 400)])
        sv.cells(160, y + 6, out, roles, cw=40, ch=30, rings=(i,))
        sv.t(340, y + 10, "out[%d] = l = %d" % (i, oldl), 12, INK)
        sv.t(340, y + 30, "l = %d × %d = %d" % (oldl, nums[i], l), 14, INK, weight=500)
        print("prod1", i, list(out), l)
        y += 48
        sv.sep(y - 3)
    assert out == [1, 1, 2, 6]
    sv.t(40, y + 10, "第 2 遍 (右→左): out[i] 再乘上 r = i 右边所有数的积", 12, INK, weight=500)
    y += 24
    r = 1
    for i in range(n - 1, -1, -1):
        before = out[i]
        out[i] *= r
        oldr = r
        r *= nums[i]
        roles = ["new" if t >= i else "other" for t in range(n)]
        sv.box(40, y + 2, 100, 38, "new", [("i = %d" % i, 14, 500), ("nums[i] = %d" % nums[i], 12, 400)])
        sv.cells(160, y + 6, out, roles, cw=40, ch=30, rings=(i,))
        sv.t(340, y + 10, "out[%d] = %d × r = %d × %d = %d" % (i, before, before, oldr, out[i]), 12, INK)
        sv.t(340, y + 30, "r = %d × %d = %d" % (oldr, nums[i], r), 14, INK, weight=500)
        print("prod2", i, list(out), r)
        y += 48
        sv.sep(y - 3)
    assert out == [24, 12, 8, 6]
    sv.t(40, y + 14, "答案 out = [24, 12, 8, 6]", 14, INK, weight=500)
    sv.legend(y + 44, [("new", "本步写入 / 已是最终值"), ("other", "已有左积, 还没乘右积"), ("plain", "还没写")])
    sv.save("product_trace.svg", y + 62)


# ---------------------------------------------------------------- SVG 6: Range Sum Query 2D
MAT = [[3, 0, 1], [5, 6, 3], [1, 2, 0]]


def build_P(M):
    m, n = len(M), len(M[0])
    P = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            P[i + 1][j + 1] = M[i][j] + P[i][j + 1] + P[i + 1][j] - P[i][j]
    return P


def svg_matrix():
    M = MAT
    P = build_P(M)
    assert P == [[0, 0, 0, 0], [0, 3, 3, 4], [0, 8, 14, 18], [0, 9, 17, 21]]
    r1, c1, r2, c2 = 1, 1, 2, 2
    assert P[3][3] - P[1][3] - P[3][1] + P[1][1] == 11
    sv = Svg("Range Sum Query 2D 的核心", "inclusion-exclusion: 全部 - 上面 - 左边 + 左上角")
    hdr(sv, "matrix 3×3 · 求 (r1,c1) = (1,1) 到 (r2,c2) = (2,2) 的和 · P[i][j] = 左上角 i 行 j 列的和",
        "二维的 prefix: 减两次的部分要加回来 (inclusion-exclusion)")
    x0, y0, c = 50, 80, 56
    for i in range(3):
        for j in range(3):
            if i >= 1 and j >= 1:
                role = "new"
            else:
                role = "gone"
            sv.box(x0 + j * c, y0 + i * c, c - 4, c - 4, role, [(str(M[i][j]), 14, 500)], ring=(i == 0 and j == 0))
    for j in range(3):
        sv.t(x0 + j * c + c / 2 - 2, y0 - 10, "col %d" % j, 12, SUB, "middle")
    for i in range(3):
        sv.t(x0 - 8, y0 + i * c + c / 2 - 2, "row %d" % i, 12, SUB, "end")
    tx = 300
    sv.t(tx, 92, "全部 = P[3][3] = 21", 14, INK, weight=500)
    sv.t(tx, 124, "- 上面 = P[1][3] = 第 0 行 = 3 + 0 + 1 = 4", 14, "#712B13", weight=500)
    sv.t(tx, 156, "- 左边 = P[3][1] = 第 0 列 = 3 + 5 + 1 = 9", 14, "#712B13", weight=500)
    sv.t(tx, 188, "+ 左上角 = P[1][1] = 3", 14, "#085041", weight=500)
    sv.t(tx + 14, 206, "(上面和左边都减了它, 减了两次, 要加回一次)", 12)
    sv.line(tx, 220, 640, 220, "#B4B2A9", 1)
    sv.t(tx, 242, "= 21 - 4 - 9 + 3 = 11", 16, INK, weight=500)
    sv.t(tx, 266, "直接加: 6 + 3 + 2 + 0 = 11 ✓", 12)
    sv.sep(292)
    sv.t(40, 316, "P[i][j] 自己也是这样递推建出来的: P[i+1][j+1] = M[i][j] + P[i][j+1] + P[i+1][j] - P[i][j]", 12, INK)
    sv.box(40, 334, 290, 62, "gone", [("brute force: 每个 query 双重循环加", 14, 500),
                                      ("O(m · n) 每个 query", 12, 400)])
    sv.box(350, 334, 290, 62, "new", [("建 P 一次 O(m · n)", 14, 500),
                                      ("每个 query 读 4 个格子 → O(1)", 12, 400)])
    sv.legend(420, [("new", "要的区域"), ("gone", "要减掉的区域"), ("ring", "被减了两次的格子")])
    sv.save("matrix_core.svg", 438)


def svg_matrix_trace():
    M = MAT
    P = build_P(M)
    sv = Svg("Range Sum Query 2D trace", "逐行建 P，再用四个格子做 query")
    hdr(sv, "M = [[3, 0, 1], [5, 6, 3], [1, 2, 0]] · P 是 4×4, 第 0 行第 0 列全是 0",
        "建 P: P[i+1][j+1] = M[i][j] + P[i][j+1] + P[i+1][j] - P[i][j] · 每次建完一整行 (从左到右)")
    sv.t(40, 64, "步骤", 12); sv.t(150, 64, "P (4×4)", 12); sv.t(330, 64, "计算 (该行最后一格)", 12)
    sv.sep(74)
    y = 84
    cw, ch = 34, 26

    def grid(x, y0, filled_rows, new_row=None, marks=None):
        marks = marks or {}
        for i in range(4):
            for j in range(4):
                if i in filled_rows or i == 0 or j == 0:
                    v = str(P[i][j])
                    role = "new" if i == new_row and j > 0 else "other"
                else:
                    v, role = "", "plain"
                if (i, j) in marks:
                    role = marks[(i, j)]
                sv.box(x + j * cw, y0 + i * ch, cw - 3, ch - 3, role, [(v, 14, 500)] if v else [],
                       ring=((i, j) in marks and marks[(i, j)] == "ring"))
    # 3 build rows
    for i in range(3):
        m = M[i][2]
        a, b, cc = P[i][3], P[i + 1][2], P[i][2]
        val = m + a + b - cc
        assert val == P[i + 1][3]
        sv.box(40, y + 24, 90, 44, "new", [("建第 %d 行" % (i + 1), 14, 500), ("M[%d] = %s" % (i, M[i]), 12, 400)]) \
            if False else sv.box(40, y + 22, 96, 44, "new", [("建 P 第 %d 行" % (i + 1), 14, 500), ("用 M 第 %d 行" % i, 12, 400)])
        grid(150, y, set(range(1, i + 2)), new_row=i + 1)
        sv.t(330, y + 10, "P[%d][3] = M[%d][2] + P[%d][3] + P[%d][2] - P[%d][2]" % (i + 1, i, i, i + 1, i), 12, INK)
        sv.t(330, y + 32, "= %d + %d + %d - %d = %d" % (m, a, b, cc, val), 14, INK, weight=500)
        sv.t(330, y + 54, "(前面几格同样算出, 每格 O(1))", 12)
        print("mat build", i + 1, P[i + 1], "last cell", val)
        y += 116
        sv.sep(y - 6)
    # query
    marks = {(3, 3): "new", (1, 3): "gone", (3, 1): "gone", (1, 1): "new"}
    sv.box(40, y + 22, 96, 44, "new", [("query", 14, 500), ("(1,1) 到 (2,2)", 12, 400)])
    grid(150, y, {1, 2, 3}, marks=marks)
    for (i, j) in marks:
        sv.ring(150 + j * cw, y + i * ch, cw - 3, ch - 3, pad=2)
    sv.t(330, y + 8, "P[3][3] = %d" % P[3][3], 14, INK, weight=500)
    sv.t(330, y + 30, "- P[1][3] = - %d" % P[1][3], 14, "#712B13", weight=500)
    sv.t(330, y + 52, "- P[3][1] = - %d" % P[3][1], 14, "#712B13", weight=500)
    sv.t(330, y + 74, "+ P[1][1] = + %d" % P[1][1], 14, "#085041", weight=500)
    ans = P[3][3] - P[1][3] - P[3][1] + P[1][1]
    sv.t(480, y + 41, "= 21 - 4 - 9 + 3 = %d" % ans, 14, INK, weight=500)
    y += 116
    sv.sep(y - 6)
    assert ans == 11
    sv.t(40, y + 12, "答案 sumRegion(1, 1, 2, 2) = 11", 14, INK, weight=500)
    sv.legend(y + 42, [("new", "本步新算的格子 / 要加的"), ("gone", "要减的"), ("other", "已建好")])
    sv.save("matrix_trace.svg", y + 60)


# ---------------------------------------------------------------- SVG 7: difference array
BOOK = [[1, 2, 10], [2, 3, 20], [2, 5, 25]]
BN = 5


def svg_diff():
    sv = Svg("difference array 的核心", "区间加只改两个端点，最后一次 prefix sum 还原")
    hdr(sv, "区间加: 对 arr[l..r] 每个位置 +v · 只改 diff[l] += v 和 diff[r+1] -= v",
        "最后对 diff 做一次 prefix sum, 就得到每个位置的值 (和 prefix sum 互为逆运算)")
    diff = [10, 0, -10, 0, 0, 0]
    cur, vals = 0, []
    for v in diff[:5]:
        cur += v
        vals.append(cur)
    assert vals == [10, 10, 0, 0, 0]
    x0, cw = 170, 70
    sv.t(40, 66, "一个 booking [1, 2, 10]: 航班 1..2 各 +10 (数组下标 0..1)", 14, INK, weight=500)
    sv.t(40, 137, "diff", 14, INK, weight=500)
    roles = ["new", "plain", "gone", "plain", "plain", "plain"]
    sv.cells(x0, 120, diff, roles, cw=cw, ch=34, idx=["diff[%d]" % t for t in range(6)], idx_dy=-9)
    sv.t(x0 + 33, 170, "diff[0] += 10", 12, "#085041", "middle")
    sv.t(x0 + 2 * cw + 33, 170, "diff[2] -= 10", 12, "#712B13", "middle")
    sv.t(40, 217, "prefix sum 后", 14, INK, weight=500)
    sv.cells(x0, 200, vals, ["new", "new", "plain", "plain", "plain"], cw=cw, ch=34)
    sv.t(40, 262, "cur 从 diff[0] 起一直带着 +10: arr[0] = 10, arr[1] = 10", 12, "#085041")
    sv.t(40, 282, "走到 diff[2] = -10: cur = 10 + (-10) = 0, 抵消, 之后一直是 0", 12, "#712B13")
    sv.sep(302)
    sv.t(40, 326, "diff[last] 对应 arr[last+1]: 为 diff 多留 1 格 (n + 1 = 6 格), last = n 时不越界", 12, INK)
    sv.box(40, 346, 290, 62, "gone", [("brute force: 每个 booking 循环改区间", 14, 500),
                                      ("m 个 booking × n → O(m · n)", 12, 400)])
    sv.box(350, 346, 290, 62, "new", [("diff: 每个 booking 只改 2 个格子", 14, 500),
                                      ("m 次 O(1) + 一次 prefix sum → O(m + n)", 12, 400)])
    sv.legend(432, [("new", "+v 的位置 / 被抬高的区间"), ("gone", "-v 的位置 (抵消)"), ("plain", "其他")])
    sv.save("diff_core.svg", 450)


def svg_diff_trace():
    sv = Svg("Corporate Flight Bookings trace", "三次区间加后做一次 prefix sum")
    hdr(sv, "n = 5 · diff 有 n + 1 = 6 格, 初始全 0 · 每个 booking [first, last, seats]: diff[first-1] += seats, diff[last] -= seats",
        "最后 cur += diff[i] 依次还原 ans[0..4]")
    sv.t(40, 64, "booking", 12); sv.t(170, 64, "diff (更新后)", 12); sv.t(420, 64, "改了哪两格", 12)
    sv.sep(74)
    diff = [0] * (BN + 1)
    y = 84
    for first, last, seats in BOOK:
        diff[first - 1] += seats
        diff[last] -= seats
        sv.box(40, y + 2, 120, 44, "new", [("[%d, %d, %d]" % (first, last, seats), 14, 500),
                                           ("航班 %d..%d 各 +%d" % (first, last, seats), 12, 400)])
        roles = ["plain"] * 6
        roles[first - 1] = "new"
        roles[last] = "gone"
        sv.cells(170, y + 8, diff, roles, cw=40, ch=30, idx=None)
        sv.t(420, y + 12, "diff[%d] += %d" % (first - 1, seats), 12, "#085041", weight=500)
        sv.t(420, y + 34, "diff[%d] -= %d" % (last, seats), 12, "#712B13", weight=500)
        print("diff", first, last, seats, diff)
        y += 56
        sv.sep(y - 4)
    assert diff == [10, 45, -10, -20, 0, -25]
    sv.t(40, y + 10, "对 diff 做 prefix sum: cur += diff[i], ans[i] = cur", 12, INK, weight=500)
    y += 24
    cur = 0
    ans = []
    for i in range(BN):
        old = cur
        cur += diff[i]
        ans.append(cur)
        roles = ["new" if t <= i else "plain" for t in range(BN)]
        sv.box(40, y + 2, 120, 38, "other", [("i = %d" % i, 14, 500), ("diff[%d] = %d" % (i, diff[i]), 12, 400)])
        padded = ans + [""] * (BN - len(ans))
        sv.cells(170, y + 6, padded, roles, cw=40, ch=30, rings=(i,))
        sv.t(420, y + 10, "cur = %d + (%d)" % (old, diff[i]) if diff[i] < 0 else "cur = %d + %d" % (old, diff[i]), 12, INK)
        sv.t(420, y + 30, "= %d" % cur, 14, INK, weight=500)
        print("diff acc", i, ans)
        y += 46
        sv.sep(y - 3)
    assert ans == [10, 55, 45, 25, 25]
    sv.t(40, y + 14, "答案 ans = [10, 55, 45, 25, 25]", 14, INK, weight=500)
    sv.legend(y + 44, [("new", "+seats 的位置 / 已算出的 ans"), ("gone", "-seats 的位置"), ("plain", "没变 / 还没算")])
    sv.save("diff_trace.svg", y + 62)


# ---------------------------------------------------------------- SVG 8: prefix vs sliding window
def svg_window_core():
    sv = Svg("sliding window 与 prefix + hash 的分界", "有负数时 prefix 不单调, 窗口失效")
    hdr(sv, "sliding window 成立的前提: 加元素 → 和变大, 去元素 → 和变小 (单调)",
        "只要有负数, 这个单调性就没了 · prefix + hash 不依赖单调性")
    # left plot: positives
    def plot(x0, vals, title, subtitle, color):
        sv.t(x0, 66, title, 14, INK, weight=500)
        sv.t(x0, 86, subtitle, 12)
        top, base, sx, sy = 110, 250, 64, 11
        sv.line(x0, base, x0 + sx * (len(vals) - 1) + 20, base, "#B4B2A9", 1)
        pts = [(x0 + 10 + sx * t, base - v * sy) for t, v in enumerate(vals)]
        sv.o.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="1.5"/>'
                    % (" ".join("%s,%s" % p for p in pts), color))
        for t, (px, py) in enumerate(pts):
            sv.circ(px, py, 11, "other", "")
            sv.t(px, py - 22, str(vals[t]), 12, INK, "middle", 500)
            sv.t(px, base + 26, "t=%d" % t, 12, SUB, "middle")
    plot(40, [0, 1, 3, 6, 10], "全是正数: nums = [1, 2, 3, 4]", "prefix = [0, 1, 3, 6, 10] 一路往上", "#0F6E56")
    plot(370, [0, 5, 3, 3], "有负数: nums = [5, -2, 0]", "prefix = [0, 5, 3, 3] 升了又降", "#D85A30")
    sv.sep(290)
    sv.t(40, 314, "正数: 固定右端点, 满足条件的左端点是一段连续区间, left 只用往右走 → window, O(n)", 12, INK)
    sv.t(40, 336, "负数: 5 > k = 3 时把 5 丢掉, 但后面的 -2 会把和拉回 3 (5 + (-2) = 3) → 丢早了, 漏答案", 12, INK)
    sv.box(40, 356, 290, 62, "new", [("全正数 → sliding window", 14, 500),
                                      ("O(n) 时间, O(1) 空间", 12, 400)])
    sv.box(350, 356, 290, 62, "gone", [("有负数 → prefix + hash", 14, 500),
                                      ("O(n) 时间, O(n) 空间 (用空间换单调性)", 12, 400)])
    sv.legend(442, [("other", "prefix[t]")])
    sv.save("window_core.svg", 460)


def svg_window_trace():
    nums, k = [5, -2, 0], 3
    sv = Svg("window 失败 vs prefix + hash 成功", "同一个输入, 两种做法逐步对比")
    hdr(sv, "nums = [5, -2, 0], k = 3 · 真实答案 2: [5, -2] 和 [5, -2, 0]",
        "左: window (超过 k 就缩左边) · 右: prefix + hash")
    sv.t(40, 64, "nums[right]", 12); sv.t(150, 64, "window: left → right (错)", 12)
    sv.t(370, 64, "prefix + hash (对)", 12)
    sv.sep(74)
    sv.line(352, 80, 352, 80 + 3 * 100, "#B4B2A9", 1, True)
    y = 84
    left = total = wans = 0
    count = {0: 1}
    prefix = pans = 0
    for right, x in enumerate(nums):
        prev_total = total
        total += x
        before_total = total
        shrunk = []
        while total > k and left <= right:
            total -= nums[left]
            shrunk.append(nums[left])
            left += 1
        if total == k:
            wans += 1
        prefix += x
        need = prefix - k
        got = count.get(need, 0)
        pans += got
        count[prefix] = count.get(prefix, 0) + 1
        print("win", right, x, "total_before", before_total, "shrunk", shrunk, "left", left, "total", total, "wans", wans,
              "| prefix", prefix, "need", need, "got", got, "pans", pans, list(count.items()))
        sv.box(40, y + 10, 96, 44, "new", [("nums[%d] = %d" % (right, x), 14, 500), ("right = %d" % right, 12, 400)])
        # window cells
        for t in range(3):
            if t > right:
                role, v = "plain", ""
            elif t < left:
                role, v = "gone", str(nums[t])
            else:
                role, v = "new", str(nums[t])
            sv.box(150 + t * 40, y + 6, 36, 30, role, [(v, 14, 500)] if v else [], dash=(role == "gone"))
        sv.t(150, y + 52, "total = %d + (%d) = %d" % (prev_total, x, before_total) if x < 0 else
             "total = %d + %d = %d" % (prev_total, x, before_total), 12, INK)
        if shrunk:
            sv.t(150, y + 70, "%d > k = %d → 扔掉 %s" % (before_total, k, ", ".join(str(v) for v in shrunk)), 12, "#712B13")
            sv.t(150, y + 86, "total = %d (窗口 %s)" % (total, "空" if left > right else "[%d..%d]" % (left, right)), 12, "#712B13")
        else:
            sv.t(150, y + 70, "%d ≠ k = %d, 不缩" % (total, k), 12, INK)
        sv.t(290, y + 20, "ans = %d" % wans, 14, INK, weight=500)
        # hash col
        sv.t(370, y + 10, "prefix = %d, need = %d - %d = %d" % (prefix, prefix, k, need), 12, INK)
        sv.t(370, y + 30, ("count[%d] = %d → 命中" % (need, got)) if got else "count[%d] 没有 → +0" % need, 12,
             "#085041" if got else INK, weight=500 if got else 400)
        sv.t(370, y + 52, "ans = %d" % pans, 14, INK, weight=500)
        sv.chips(440, y + 40, list(count.items()), 4, cw=48, ch=22, new={prefix}, hit={need} if got else set()) if False else \
            sv.chips(370, y + 66, list(count.items()), 4, cw=56, ch=22, new={prefix}, hit={need} if got else set())
        y += 100
        sv.sep(y - 2)
    assert wans == 0 and pans == 2
    sv.t(40, y + 14, "window 答案 0 (错), prefix + hash 答案 2 (对)", 14, INK, weight=500)
    sv.legend(y + 44, [("new", "在 window 里 / 本步 prefix"), ("gone", "被 window 扔掉"), ("ring", "被查到的 key")])
    sv.save("window_trace.svg", y + 62)


for fn in (svg_range_core, svg_pivot, svg_subk, svg_subk_trace, svg_div, svg_div_trace,
           svg_contig, svg_contig_trace, svg_product, svg_product_trace, svg_matrix,
           svg_matrix_trace, svg_diff, svg_diff_trace, svg_window_core, svg_window_trace):
    fn()


# ---------------------------------------------------------------- 文档
doc = d.Doc("04 · Prefix Sum")
doc.main("主线: 区间和 = 两个前缀和之差。把 '每次重新加一遍' 换成 '建一次表, 之后 O(1) 查表'; "
         "再把 '找起点' 变成 Hash Table 里的一次查找。")
doc.main("概念链: Range Sum / Find Pivot Index → Subarray Sum Equals K (prefix + Hash Table, 核心) → "
         "Subarray Sums Divisible by K (余数) → Contiguous Array (0 看成 -1) → Product of Array Except Self (前缀积 / 后缀积) → "
         "Range Sum Query 2D → Corporate Flight Bookings (difference array) → 和 sliding window 的分界")

# ---- 0
doc.h2("0. 第一性原理: brute force 在浪费什么")
doc.p("题目: 数组 <code>nums</code> 不变, 有很多次 query, 每次问 <code>sum(nums[i..j])</code>。")
doc.p("Brute force: 每次 query 从 i 加到 j, 最坏 <code>O(n)</code>。q 次 query 就是 <code>O(n · q)</code>。")
doc.p("浪费在哪: 不同的 query 重叠很多。<code>sum(1..3)</code> 和 <code>sum(0..3)</code> 都要把 nums[1..3] 重新加一遍。"
      "每个元素被反复加了很多次。")
doc.p("消掉的办法: 每个元素只加一次, 把 '从头加到 k' 的结果存下来, 叫 <code>prefix[k]</code>。"
      "任何区间都是两个 prefix 之差。")
doc.svg(SLUG + "/range_sum_core.svg", "sum(i..j) = prefix[j+1] - prefix[i]: 两次查表代替一次循环")
doc.p("通用模板。<code>prefix</code> 比 <code>nums</code> 多一格, <code>prefix[0] = 0</code> 表示空前缀, 这样从下标 0 开始的区间也不需要特判:")
doc.code(CODE["template"])
doc.p("第二个模板是本 doc 的主角: 要的不是某个区间的和, 而是 '有多少个区间的和满足条件'。"
      "固定右端点 j, 区间和 = <code>prefix_j - prefix_i</code>, 所以满足条件就是对 <code>prefix_i</code> 提了一个要求。"
      "把之前所有的 <code>prefix_i</code> 放进 Hash Table, 这个要求就是一次查找 (下面第 2 节详细讲):")
doc.code(CODE["hash_template"])
doc.p("复杂度: 建表 <code>O(n)</code>, 每次 query <code>O(1)</code>; 数区间时从 <code>O(n²)</code> (枚举所有 i, j) 降到 <code>O(n)</code>。")
doc.note("prefix 的本质: 'sum(i..j) = prefix[j+1] - prefix[i]', 每个元素只加一次。prefix[0] = 0 (空前缀) 要记得放。")

# ---- 1
doc.h2("1. Find Pivot Index: 左边和 == 右边和, prefix 的最小用法")
doc.p("题目: 找最左的下标 <code>i</code>, 使 <code>nums[0..i-1]</code> 之和 == <code>nums[i+1..]</code> 之和。"
      "例: <code>[1, 7, 3, 6, 5, 6]</code> → 3。")
doc.p("Brute force: 每个 i 把左边加一遍、右边加一遍, <code>O(n²)</code>。浪费: 相邻两个 i 的左边只差一个元素, 却整个重算。")
doc.p("关键观察: 左边和就是 <code>prefix[i]</code>, 边走边累加即可; 右边和 = 总和 - 左边 - <code>nums[i]</code>, 不用再加。"
      "这题不用建整个 prefix 数组, 一个变量 <code>left</code> 就是滚动的 prefix。")
doc.svg(SLUG + "/pivot_core.svg", "invariant: left == total - left - nums[i]")
doc.svg(SLUG + "/pivot_trace.svg", "trace: 走到 i = 3 时 left = 11, right = 11")
doc.code(CODE["pivot"])
doc.p("Time <code>O(n)</code>: 一次求 total, 一次扫描。Space <code>O(1)</code>。")
doc.note("prefix 不一定要存成数组。只要 '只问当前位置的 prefix', 一个滚动变量就够。")

# ---- 2
doc.h2("2. Subarray Sum Equals K: prefix + Hash Table (核心)")
doc.p("题目: 数 <code>nums</code> 里有多少个连续 subarray 的和等于 <code>k</code>。数组里可以有负数。"
      "例: <code>nums = [3, 4, 7, 2, -3, 1, 4, 2], k = 7</code> → 4。")
doc.p("Brute force: 枚举起点 i 和终点 j, 区间和用 prefix 查表, 仍是 <code>O(n²)</code> 个 (i, j)。"
      "浪费: 固定 j 之后, 我们只想知道 '有几个 i 满足 <code>prefix[j] - prefix[i] == k</code>', 却把每个 i 都试了一遍。")
doc.p("关键观察: 条件移项, <code>prefix[i] == prefix[j] - k</code>。右边是已知数 (记作 <code>need</code>), "
      "所以问题变成 '之前出现过几次值为 <code>need</code> 的 prefix', 这正是 Hash Table 的一次查找。"
      "做法: 从左到右扫, 对每个 j 先 <code>ans += count[need]</code>, 再把当前 prefix 放进 <code>count</code>。")
doc.svg(SLUG + "/subk_core.svg", "以 j 结尾、和为 k 的个数 = 之前有多少个 prefix == prefix_j - k")
doc.p("两个细节。第一, <code>{0: 1}</code>: 空前缀 prefix = 0 也是一个起点, 不放它, 从下标 0 开始的 subarray 就漏了 "
      "(图里 [3, 4] 就是靠它数到的)。第二, 先查再放: 起点必须严格在终点之前。")
doc.svg(SLUG + "/subk_trace.svg", "trace: ans 在 i = 1, 2, 5, 7 各加 1, 共 4; count[14] 在 i = 5 变成 2")
doc.code(CODE["subk"])
doc.p("Time <code>O(n)</code>: 每个元素一次 Hash Table 查找和一次写入。Space <code>O(n)</code>: count 最多 n + 1 项。")
doc.note("'连续 subarray + 和 == k' → prefix + Hash Table, 先查 count[prefix - k], 再 count[prefix] += 1, 初始 {0: 1}。")

# ---- 3
doc.h2("3. Subarray Sums Divisible by K: 把 prefix 换成 prefix % k")
doc.p("题目: 数有多少个连续 subarray 的和是 <code>k</code> 的倍数。例: <code>[4, 5, 0, -2, -3, 1], k = 5</code> → 7。")
doc.p("相比上一题多了什么: 不要求和 == k, 而是和 % k == 0。模板只改一行, 不再找 <code>prefix - k</code>, 而是找 '余数相同的 prefix'。")
doc.p("为什么: <code>(prefix[j] - prefix[i]) % k == 0</code> 等价于 <code>prefix[j] % k == prefix[i] % k</code>。"
      "余数相同的 prefix 放进同一个桶, 同桶任意两个配成一个答案。")
doc.svg(SLUG + "/divk_core.svg", "按余数分桶: 同桶两两配对, ans = 1 + 6 + 0 = 7")
doc.svg(SLUG + "/divk_trace.svg", "trace: 每步先查桶里已有几个, 再放进去")
doc.p("下面还放了同一族的 Continuous Subarray Sum (长度至少 2, 求 '是否存在'): "
      "'存在' 只需要知道最早的下标, 所以 dict 存第一次出现的位置, 不再存次数。")
doc.code(CODE["divk"])
doc.p("Time <code>O(n)</code>。Space <code>O(k)</code> (余数只有 k 种, 也不会超过 n + 1)。")
doc.note("'和是 k 的倍数' → prefix % k 当 key。数个数存次数, 求存在 / 最长存最早下标。Python 的 % 对负数也给 0..k-1。")

# ---- 4
doc.h2("4. Contiguous Array: 把 0 看成 -1, 求最长")
doc.p("题目: 二进制数组, 找最长的连续 subarray, 里面 0 和 1 一样多, 返回长度。例: <code>[0, 1, 1, 0, 1, 1, 1, 0]</code> → 4。")
doc.p("相比上一题多了两个变化。一, 条件 '0 和 1 一样多' 不是和, 先变形: 0 看成 -1, 这样一样多 ⟺ 区间和 = 0 ⟺ 两个 prefix 相等 "
      "(就是第 2 节 k = 0)。二, 要最长而不是个数: 同一个 prefix 值出现多次时, 最早的那个起点最长, 所以只记第一次出现的下标, 不覆盖。")
doc.p("Brute force: 每个 subarray 数一遍 0 和 1, <code>O(n²)</code> (或 <code>O(n³)</code>)。")
doc.svg(SLUG + "/contig_core.svg", "s 回到同一个高度 = 中间 0 和 1 一样多; 最长就是第一次出现到现在")
doc.svg(SLUG + "/contig_trace.svg", "trace: i = 1 长度 2, i = 3 长度 4 (best), i = 4, 7 长度 2")
doc.code(CODE["contig"])
doc.p("Time <code>O(n)</code>, Space <code>O(n)</code>。同一模板还能解 Maximum Size Subarray Sum Equals k: "
      "<code>need = prefix - k</code> 去 <code>first</code> 里查, 查完再 '没有才放':")
doc.code(CODE["maxlen_k"])
doc.note("'两种东西一样多' → 一种记 +1, 另一种记 -1, 变成 '和为 0'。求最长: dict 存最早下标; 求个数: dict 存次数。")

# ---- 5
doc.h2("5. Product of Array Except Self: prefix 不只能是加法")
doc.p("题目: 返回 <code>out</code>, <code>out[i]</code> = 除 <code>nums[i]</code> 以外所有数的乘积, 不许用除法。"
      "例: <code>[1, 2, 3, 4]</code> → <code>[24, 12, 8, 6]</code>。")
doc.p("相比上一题多了什么: 不再问区间 '和', 而是 '除自己外的积'; 但结构一样, 把 + 换成 ×。"
      "Brute force: 每个 i 乘其余 n - 1 个数, <code>O(n²)</code>。浪费: 相邻两个 i 的积共享几乎所有因子。")
doc.p("关键观察: <code>out[i]</code> = (i 左边所有数的积) × (i 右边所有数的积)。左边的积是 prefix product, 右边的积是 suffix product。"
      "为什么不用除法: 有 0 时 '总积 / nums[i]' 不成立。")
doc.svg(SLUG + "/product_core.svg", "out[i] = L[i] × R[i]; i = 2 时 2 × 4 = 8")
doc.svg(SLUG + "/product_trace.svg", "trace: 第 1 遍把左积写进 out, 第 2 遍用 r 滚出右积再乘上去")
doc.code(CODE["product"])
doc.p("Time <code>O(n)</code>: 两遍扫描。Space <code>O(1)</code> 额外: 左积直接存进 <code>out</code> (答案本身), 右积只用一个变量 <code>r</code>。")
doc.note("'除自己以外' → 左边一遍, 右边一遍。左边的结果存进答案数组, 右边用一个滚动变量, 额外空间 O(1)。")

# ---- 6
doc.h2("6. Range Sum Query 2D: 二维 prefix, 要用 inclusion-exclusion")
doc.p("题目: 矩阵不变, 多次 query 子矩形 <code>(r1, c1)</code> 到 <code>(r2, c2)</code> 的和。")
doc.p("Brute force: 每次 query 双重循环, <code>O(m · n)</code> 每次。")
doc.p("相比一维多了什么: 一维只要减一个 prefix, 二维要减两块 (上面和左边), 左上角被减了两次, 要加回来。"
      "<code>P[i][j]</code> 定义为左上角 i 行 j 列的和。建表时用同样的 inclusion-exclusion。")
doc.svg(SLUG + "/matrix_core.svg", "全部 - 上面 - 左边 + 左上角 = 21 - 4 - 9 + 3 = 11")
doc.svg(SLUG + "/matrix_trace.svg", "trace: 逐行建 P, 然后 query 只读 4 个格子")
doc.code(CODE["matrix"])
doc.p("Time: 建表 <code>O(m · n)</code>, 每个 query <code>O(1)</code>。Space <code>O(m · n)</code>。")
doc.note("二维 prefix: P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1]。P 比 matrix 多一行一列 0, 和一维的 prefix[0] = 0 同理。")

# ---- 7
doc.h2("7. Corporate Flight Bookings: difference array, 区间加")
doc.p("题目: <code>n</code> 个航班, 每条 booking <code>[first, last, seats]</code> 表示航班 first..last 各订了 seats 个座位, 求每个航班的总座位数。"
      "例: <code>[[1,2,10],[2,3,20],[2,5,25]], n = 5</code> → <code>[10, 55, 45, 25, 25]</code>。")
doc.p("这题和前面方向相反: 前面是 '先建 prefix, 再查区间'; 这里是 '很多次区间修改, 最后读一遍'。"
      "Brute force: 每个 booking 循环改 last - first + 1 个位置, <code>O(m · n)</code>。浪费: 区间里每个位置都被同一个 +v 各改一次。")
doc.p("关键观察: 只记录 '变化的边界'。difference array <code>diff[i] = arr[i] - arr[i-1]</code>, "
      "区间 [l, r] 加 v 只影响两个边界: <code>diff[l] += v</code>, <code>diff[r+1] -= v</code>。最后对 diff 做 prefix sum 就还原 arr。"
      "difference 和 prefix sum 是互逆的。")
doc.svg(SLUG + "/diff_core.svg", "+v 往右一直带着, 走到 r+1 被 -v 抵消")
doc.svg(SLUG + "/diff_trace.svg", "trace: 3 个 booking 各改 2 个格子, 最后一遍 prefix sum 得到答案")
doc.code(CODE["flights"])
doc.p("Time <code>O(m + n)</code>: m 个 booking 各 O(1), 加一遍 prefix sum。Space <code>O(n)</code>。"
      "Car Pooling 是同一个模板: 每次上车 +num, 下车 -num, 扫一遍看 cur 有没有超过 capacity。")
doc.note("'很多次区间 +v, 最后才读结果' → diff[l] += v, diff[r+1] -= v, 最后 prefix sum。")

# ---- 8
doc.h2("8. 和 sliding window 的分界: 有负数时 window 为什么失效")
doc.p("同样是 '连续 subarray 的和', 什么时候用 window, 什么时候用 prefix + Hash Table? 看元素有没有负数。")
doc.p("Sliding window 成立的前提是单调: 右端点右移, 和只会变大; 左端点右移, 和只会变小。"
      "有了这个单调性, '和超过目标就缩左边' 是安全的, 因为再往右加只会更大, 被丢掉的左端点不可能再变成答案。"
      "全正数的 Minimum Size Subarray Sum 就是这个情形:")
doc.code(CODE["window_pos"])
doc.p("有负数时单调性没了: 后面的 -2 可以把和拉回来。下面把 window 套到 Subarray Sum Equals K 上, 在 <code>[5, -2, 0], k = 3</code> 上失败:")
doc.code(CODE["window_neg"])
doc.svg(SLUG + "/window_core.svg", "全正: prefix 单调上升; 有负数: prefix 升了又降, 窗口的 '只缩不回' 不成立")
doc.svg(SLUG + "/window_trace.svg", "trace: window 在 total = 5 > 3 时扔掉 5, 漏掉 [5, -2] 和 [5, -2, 0]; prefix + hash 两个都数到")
doc.p("prefix + Hash Table 不依赖单调性: 它不移动任何边界, 每个起点都留在 Hash Table 里, 随时可以查。代价是 Space 从 <code>O(1)</code> 变成 <code>O(n)</code>。")
doc.note("元素全为正 (和单调) → sliding window, O(1) 空间。有负数 → prefix + Hash Table, O(n) 空间。")

# ---- 9
doc.h2("9. 识别信号: 看到什么 → 试什么")
rows = [
    ("数组不变, 反复问区间和", "prefix 数组, sum = prefix[j+1] - prefix[i]", "O(n · q) → O(n + q)"),
    ("'左边和 == 右边和' / 找分割点", "total + 滚动的 left, right = total - left - nums[i]", "O(n²) → O(n)"),
    ("连续 subarray 和 == k, 数个数, 可能有负数", "prefix + Hash Table: count[prefix - k], 初始 {0: 1}", "O(n²) → O(n)"),
    ("连续 subarray 和是 k 的倍数 (divisible / multiple)", "prefix % k 做 key; 个数存次数, 存在 / 最长存最早下标", "O(n²) → O(n)"),
    ("两种东西一样多 / 平衡 (0 和 1, 左右括号数相等)", "一种 +1, 一种 -1, 变成 '和为 0', 同上", "O(n²) → O(n)"),
    ("最长 / 最短 subarray 满足 prefix 关系", "dict 存第一次出现的下标 (最长); 最短则覆盖成最新下标", "O(n²) → O(n)"),
    ("'除自己以外所有元素' 的积 / 和", "左边一遍 prefix, 右边一遍 suffix, 合在答案数组里", "O(n²) → O(n), 额外 O(1)"),
    ("矩阵子矩形和, 多次 query", "2D prefix, 减上面和左边, 加回左上角", "每次 O(m · n) → O(1)"),
    ("多次区间 +v, 最后才读结果", "difference array: diff[l] += v, diff[r+1] -= v, 最后 prefix sum", "O(m · n) → O(m + n)"),
    ("连续 subarray + 元素全为正 + 求最短 / 最长", "不用 prefix, 用 sliding window", "时间 O(n), 空间 O(1)"),
]
tbl = "<table><tr><th>特征</th><th>做法</th><th>complexity</th></tr>" + "".join(
    "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % tuple(html.escape(c) for c in r) for r in rows) + "</table>"
doc.raw(tbl)
doc.p("以后再学 (不常考, 本文不展开): 有负数且求 '最短 subarray 和 >= k' 要用 prefix + monotonic deque; "
      "带修改的区间和 (Range Sum Query Mutable) 用 Fenwick tree / segment tree。")

doc.write("docs/04-prefix-sum.html")
