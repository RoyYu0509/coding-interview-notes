"""03 · Sliding Window 生成脚本。
运行: cd build && python3 -I 03_sliding_window.py
做三件事: (1) 对文档里的每段代码做随机测试 (和 brute force 对拍)
(2) 用同一份逻辑模拟 trace, 生成 SVG (3) 生成 HTML。
"""
import html
import os
import random
import sys
from collections import Counter, defaultdict
from math import inf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import doclib as d  # noqa: E402

SVGDIR = os.path.join(d.ROOT, "docs", "svg", "03-sliding-window")
SLUG = "03-sliding-window"

# ---------------------------------------------------------------- 代码 (文档里原样展示, 同时被测试)
CODE = {}

CODE["template"] = '''
def window_longest(arr):
    left = 0
    state = ...                      # window 内的统计量 (计数 / 和 / 积 ...)
    best = 0
    for right, x in enumerate(arr):  # right 只增不减
        # 1. x 进 window: 更新 state
        while window 不合法:          # 2. 不合法 -> 缩 left, 直到重新合法
            # 把 arr[left] 移出 state
            left += 1                # left 也只增不减
        best = max(best, right - left + 1)   # 3. 此刻 window 合法, 更新答案
    return best
'''

CODE["template_short"] = '''
def window_shortest(arr):
    left = 0
    best = inf
    for right, x in enumerate(arr):
        # x 进 window
        while window 合法:            # 合法了: 先记答案, 再尽量缩短
            best = min(best, right - left + 1)
            # 把 arr[left] 移出 state
            left += 1
    return best
'''

CODE["longest"] = '''
def length_of_longest_substring(s):
    cnt = defaultdict(int)        # window 里每个字符出现几次
    left = best = 0
    for right, ch in enumerate(s):
        cnt[ch] += 1              # ch 进 window
        while cnt[ch] > 1:        # 不合法: ch 重复 (进来之前合法, 所以只可能是 ch)
            cnt[s[left]] -= 1     # 最左边的字符出 window
            left += 1
        best = max(best, right - left + 1)
    return best
'''

CODE["ones"] = '''
def longest_ones(nums, k):
    zeros = 0                     # window 里 0 的个数 = 需要翻转的次数
    left = best = 0
    for right, x in enumerate(nums):
        if x == 0:
            zeros += 1
        while zeros > k:          # 不合法: 要翻的 0 超过预算 k
            if nums[left] == 0:
                zeros -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
'''

CODE["replace"] = '''
def character_replacement(s, k):
    cnt = defaultdict(int)
    left = best = 0
    for right, ch in enumerate(s):
        cnt[ch] += 1
        # window 长度 - 出现最多的字符数 = 需要替换的字符数
        while (right - left + 1) - max(cnt.values()) > k:
            cnt[s[left]] -= 1     # 注意: 不 del, 值变 0 不影响 max
            left += 1
        best = max(best, right - left + 1)
    return best
'''

CODE["perm"] = '''
def check_inclusion(s1, s2):
    m = len(s1)
    need = [0] * 26               # s1 里每个字母要几个
    win = [0] * 26                # 当前 window 里每个字母有几个
    for ch in s1:
        need[ord(ch) - 97] += 1
    for right, ch in enumerate(s2):
        win[ord(ch) - 97] += 1                 # 右边进一个
        if right >= m:                         # window 变成 m + 1 了
            win[ord(s2[right - m]) - 97] -= 1  # 左边出一个 (left = right - m)
        if win == need:                        # 长度恒为 m 且计数相同 = permutation
            return True
    return False
'''

CODE["anagrams"] = '''
def find_anagrams(s, p):
    m = len(p)
    need, win, res = [0] * 26, [0] * 26, []
    for ch in p:
        need[ord(ch) - 97] += 1
    for right, ch in enumerate(s):
        win[ord(ch) - 97] += 1
        if right >= m:
            win[ord(s[right - m]) - 97] -= 1
        if win == need:
            res.append(right - m + 1)          # 唯一区别: 不 return, 记下起点
    return res
'''

CODE["minlen"] = '''
def min_subarray_len(target, nums):
    total = 0                     # window 里所有数相加 (nums 全是正数)
    left = 0
    best = inf
    for right, x in enumerate(nums):
        total += x
        while total >= target:    # 合法 (够大了): 先记答案, 再试着缩短
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return 0 if best == inf else best
'''

CODE["minwin"] = '''
def min_window(s, t):
    need = Counter(t)             # >0: 还缺; =0: 刚好; <0: window 里多了
    missing = len(t)              # 还缺的字符总个数 (重复的字符按个数算)
    left = 0
    best_len, best_start = inf, 0
    for right, ch in enumerate(s):
        if need[ch] > 0:          # ch 是"缺的", 才让 missing 减 1
            missing -= 1
        need[ch] -= 1
        while missing == 0:       # 合法: window 覆盖了 t
            if right - left + 1 < best_len:
                best_len, best_start = right - left + 1, left
            need[s[left]] += 1    # s[left] 出 window
            if need[s[left]] > 0: # 出去之后变成"缺"了 -> 不合法
                missing += 1
            left += 1
    return "" if best_len == inf else s[best_start:best_start + best_len]
'''

CODE["prod"] = '''
def num_subarray_product_less_than_k(nums, k):
    if k <= 1:                    # 正整数的乘积 >= 1, 一个都不合法
        return 0
    prod = 1                      # window 里所有数相乘
    left = ans = 0
    for right, x in enumerate(nums):
        prod *= x
        while prod >= k:          # 不合法: 乘积太大
            prod //= nums[left]
            left += 1
        ans += right - left + 1   # 以 right 结尾的合法 subarray 数 (起点 left..right)
    return ans
'''

CODE["kdistinct"] = '''
def subarrays_with_k_distinct(nums, k):
    def at_most(k):               # 最多 k 种不同数字的 subarray 个数
        cnt = defaultdict(int)
        left = total = 0
        for right, x in enumerate(nums):
            cnt[x] += 1
            while len(cnt) > k:   # 不合法: 种类超过 k
                cnt[nums[left]] -= 1
                if cnt[nums[left]] == 0:
                    del cnt[nums[left]]   # 必须 del: len(cnt) 就是种类数
                left += 1
            total += right - left + 1     # 以 right 结尾的合法 subarray 数
        return total
    return at_most(k) - at_most(k - 1)    # exactly k = (<= k) - (<= k-1)
'''

NS = {"defaultdict": defaultdict, "Counter": Counter, "inf": inf}
for key in ["longest", "ones", "replace", "perm", "anagrams", "minlen",
            "minwin", "prod", "kdistinct"]:
    exec(CODE[key], NS)


# ---------------------------------------------------------------- 随机对拍
def _bf_longest(s):
    best = 0
    for i in range(len(s)):
        for j in range(i, len(s)):
            if len(set(s[i:j + 1])) == j - i + 1:
                best = max(best, j - i + 1)
    return best


def _bf_ones(a, k):
    best = 0
    for i in range(len(a)):
        for j in range(i, len(a)):
            if a[i:j + 1].count(0) <= k:
                best = max(best, j - i + 1)
    return best


def _bf_replace(s, k):
    best = 0
    for i in range(len(s)):
        for j in range(i, len(s)):
            w = s[i:j + 1]
            if len(w) - max(Counter(w).values()) <= k:
                best = max(best, len(w))
    return best


def _bf_perm(s1, s2):
    m = len(s1)
    return any(sorted(s2[i:i + m]) == sorted(s1) for i in range(len(s2) - m + 1))


def _bf_anag(s, p):
    m = len(p)
    return [i for i in range(len(s) - m + 1) if sorted(s[i:i + m]) == sorted(p)]


def _bf_minlen(t, a):
    best = inf
    for i in range(len(a)):
        for j in range(i, len(a)):
            if sum(a[i:j + 1]) >= t:
                best = min(best, j - i + 1)
    return 0 if best == inf else best


def _bf_minwin(s, t):
    best = None
    for i in range(len(s)):
        for j in range(i, len(s)):
            if not (Counter(t) - Counter(s[i:j + 1])):
                if best is None or j - i < len(best) - 1:
                    best = s[i:j + 1]
    return best or ""


def _bf_prod(a, k):
    c = 0
    for i in range(len(a)):
        p = 1
        for j in range(i, len(a)):
            p *= a[j]
            if p < k:
                c += 1
    return c


def _bf_kd(a, k):
    return sum(1 for i in range(len(a)) for j in range(i, len(a))
               if len(set(a[i:j + 1])) == k)


random.seed(7)
for _ in range(1500):
    n = random.randint(1, 9)
    s = "".join(random.choice("abc") for _ in range(n))
    assert NS["length_of_longest_substring"](s) == _bf_longest(s)
    b = [random.randint(0, 1) for _ in range(n)]
    k = random.randint(0, 3)
    assert NS["longest_ones"](b, k) == _bf_ones(b, k)
    s2 = "".join(random.choice("AB C".replace(" ", "")) for _ in range(n))
    assert NS["character_replacement"](s2, k) == _bf_replace(s2, k)
    p = "".join(random.choice("abc") for _ in range(random.randint(1, 3)))
    assert NS["check_inclusion"](p, s) == _bf_perm(p, s)
    assert NS["find_anagrams"](s, p) == _bf_anag(s, p)
    pos = [random.randint(1, 5) for _ in range(n)]
    tg = random.randint(1, 15)
    assert NS["min_subarray_len"](tg, pos) == _bf_minlen(tg, pos)
    t = "".join(random.choice("abc") for _ in range(random.randint(1, 3)))
    w = NS["min_window"](s, t)
    bw = _bf_minwin(s, t)
    assert len(w) == len(bw) and (w == "" or not (Counter(t) - Counter(w))), (s, t, w, bw)
    pk = random.randint(0, 30)
    assert NS["num_subarray_product_less_than_k"](pos, pk) == _bf_prod(pos, pk)
    kd = [random.randint(1, 3) for _ in range(n)]
    k2 = random.randint(1, 3)
    assert NS["subarrays_with_k_distinct"](kd, k2) == _bf_kd(kd, k2)
print("random tests OK")

# ---------------------------------------------------------------- SVG 工具
FONT = 'ui-sans-serif, system-ui, -apple-system, "PingFang SC", sans-serif'
NEW = ("#E1F5EE", "#0F6E56", "#085041")
REM = ("#FAECE7", "#993C1D", "#712B13")
KEEP = ("#F1EFE8", "#5F5E5A", "#444441")
OUT = ("#FFFFFF", "#D3D1C7", "#B4B2A9")
INK, SUB, LINE, RING, ARR = "#0B0B0B", "#52514E", "#B4B2A9", "#EF9F27", "#D85A30"
ROLE = {"new": NEW, "rem": REM, "keep": KEEP, "out": OUT}


class Svg:
    def __init__(self, title, w=680):
        self.w = w
        self.title = title
        self.p = []

    def t(self, x, y, s, size=12, fill=SUB, anchor="start", weight=400):
        self.p.append('<text x="%s" y="%s" font-size="%d" fill="%s" text-anchor="%s" '
                      'font-weight="%d" dominant-baseline="central">%s</text>'
                      % (x, y, size, fill, anchor, weight, html.escape(str(s))))

    def rect(self, x, y, w, h, role="keep", rx=4, dash=False, ring=False):
        f, s, _ = ROLE[role] if isinstance(role, str) else role
        self.p.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" '
                      'stroke="%s" stroke-width="%s"%s/>'
                      % (x, y, w, h, rx, f, s, 1 if dash else 0.8,
                         ' stroke-dasharray="3 2"' if dash else ""))
        if ring:
            self.ring(x, y, w, h)

    def ring(self, x, y, w, h, rx=6):
        self.p.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="none" '
                      'stroke="%s" stroke-width="2.5"/>' % (x - 3, y - 3, w + 6, h + 6, rx, RING))

    def cell(self, x, y, w, h, label, role="keep", size=14, ring=False):
        c = ROLE[role]
        self.rect(x, y, w, h, role, rx=3, dash=(role == "rem"), ring=ring)
        self.t(x + w / 2, y + h / 2 + 1, label, size, c[2], "middle", 500)

    def line(self, x1, y1, x2, y2, dash=True, color=LINE, sw=1):
        self.p.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s/>'
                      % (x1, y1, x2, y2, color, sw, ' stroke-dasharray="4 4"' if dash else ""))

    def arrow(self, pts, color=SUB, dash=False, sw=1.5):
        dd = "M" + " L".join("%s %s" % p for p in pts)
        self.p.append('<path d="%s" fill="none" stroke="%s" stroke-width="%s"%s '
                      'marker-end="url(#arr_%s)"/>'
                      % (dd, color, sw, ' stroke-dasharray="4 3"' if dash else "",
                         color[1:]))

    def array(self, x, y, items, roles, cw=22, ch=26, size=14, ring_idx=()):
        for i, (it, r) in enumerate(zip(items, roles)):
            self.cell(x + i * cw, y, cw, ch, it, r, size, ring=(i in ring_idx))

    def ptrs(self, x, y, marks, cw=22):
        """marks: {index: 'L'} ; 同一格多个标记合并"""
        by = defaultdict(list)
        for i, m in marks:
            by[i].append(m)
        for i, ms in by.items():
            self.t(x + i * cw + cw / 2, y, "=".join(ms), 12, SUB, "middle", 500)

    def legend(self, y, items):
        x = 40
        for role, text in items:
            if role == "ring":
                self.p.append('<rect x="%s" y="%s" width="14" height="14" rx="3" fill="none" '
                              'stroke="%s" stroke-width="2.5"/>' % (x - 7, y - 7, RING))
            else:
                self.rect(x - 7, y - 7, 14, 14, role, rx=3, dash=(role == "rem"))
            self.t(x + 14, y, text, 12, SUB)
            x += 14 + sum(12 if ord(c) > 255 else 6.6 for c in text) + 22

    def save(self, name, h):
        cols = sorted({ARR, SUB, "#898781"})
        defs = "".join('<marker id="arr_%s" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" '
                       'markerHeight="6" orient="auto"><path d="M2 1L8 5L2 9" fill="none" '
                       'stroke="%s" stroke-width="1.5" stroke-linecap="round" '
                       'stroke-linejoin="round"/></marker>' % (c[1:], c) for c in cols)
        s = ('<svg width="100%%" viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" '
             'role="img" font-family=\'%s\'><title>%s</title><defs>%s</defs>%s</svg>\n'
             % (self.w, h, FONT.replace("'", ""), html.escape(self.title), defs, "\n".join(self.p)))
        with open(os.path.join(SVGDIR, name), "w", encoding="utf-8") as f:
            f.write(s)


def window_roles(n, l0, l1, r, new_idx):
    roles = ["out"] * n
    for i in range(l0, l1):
        roles[i] = "rem"
    for i in range(l1, r + 1):
        roles[i] = "keep"
    if new_idx is not None:
        roles[new_idx] = "new"
    return roles


def trace_svg(name, title, head, heads, arr, steps, foot, legend_items, cw=22, rowh=88):
    """通用 window trace: 一行一步, 列: 当前输入 | 扩 right 之后 | 缩 left 之后 | 计算
    step 里 mode == "two" 时, 第 2/3 列各自画自己的 (l0, l1) (用于 atMost(K) 和 atMost(K-1))"""
    n = len(arr)
    COL = [40, 112, 112 + n * cw + 28, 112 + 2 * (n * cw + 28)]
    S = Svg(title)
    for i, h in enumerate(head):
        S.t(40, 18 + 20 * i, h, 12, SUB)
    y0 = 18 + 20 * len(head) + 14
    for c, h in zip(COL, heads):
        S.t(c, y0, h, 12, SUB)
    y = y0 + 10
    S.line(40, y, 640, y)
    for st in steps:
        r = st["right"]
        for j, (txt, sz, wt, col) in enumerate(st["c1"]):
            S.t(COL[0], y + 22 + 20 * j, txt, sz, col, "start", wt)
        if st.get("mode") == "two":
            (a0, a1), (b0, b1) = st["w2"], st["w3"]
        else:
            (a0, a1), (b0, b1) = (st["l0"], st["l0"]), (st["l0"], st["l1"])
        for (c, l0, l1, note, key) in ((COL[1], a0, a1, st["n2"], "ring2"), (COL[2], b0, b1, st["n3"], "ring3")):
            two = st.get("mode") == "two"
            new_idx = r if (key == "ring2" or two) else None
            S.array(c, y + 10, arr, window_roles(n, l0, l1, r, new_idx), cw, 26)
            if st.get(key) and r >= l1:
                S.ring(c + l1 * cw, y + 10, (r - l1 + 1) * cw, 26)
            S.ptrs(c, y + 50, [(l1 if (two or key == "ring3") else l0, "L"), (r, "R")], cw)
            for j_, ln_ in enumerate(note.split("\n")):
                S.t(c, y + 68 + 15 * j_, ln_, 12, SUB)
        lines = st["c4"]
        sp, off = (20, 20) if len(lines) <= 3 else (17, 12)
        for j, (txt, sz, wt, col) in enumerate(lines):
            S.t(COL[3], y + off + sp * j, txt, sz, col, "start", wt)
        y += rowh
        S.line(40, y - 4, 640, y - 4)
    S.t(40, y + 14, foot, 14, INK, "start", 500)
    S.legend(y + 44, legend_items)
    S.save(name, y + 66)


def stepinfo(label_right, label_ch):
    return [("right = %d" % label_right, 14, 500, INK), (label_ch, 12, 400, SUB)]


LEG = [("new", "新进 window 的"), ("rem", "移出 window 的"), ("keep", "window 里其他的"),
       ("out", "window 外"), ("ring", "当前最优 window")]
LEG_NR = [("new", "新进 window 的"), ("rem", "移出 window 的"), ("keep", "window 里其他的"),
          ("out", "window 外")]


# ================================================================ 第 0 节 core: 为什么 left 不用回退
def core_template():
    s = "pwwkew"
    n = len(s)

    def valid(l, r):
        return len(set(s[l:r + 1])) == r - l + 1

    S = Svg("brute force 看所有 (left, right); sliding window 只沿着合法边界走")
    S.t(40, 18, "例: s = \"pwwkew\" · window s[left..right] 合法 = 没有重复字符 · 每一格 = 一个 (left, right)", 12, SUB)
    S.t(40, 38, "合法性对\"缩小 window\"封闭: [left..right] 合法 → 它的任何子区间也合法", 12, SUB)
    gx, gy, g = 100, 100, 34
    S.t(gx + n * g / 2, 64, "right →", 12, SUB, "middle")
    for r in range(n):
        S.t(gx + r * g + g / 2, 84, "%d:%s" % (r, s[r]), 12, INK, "middle", 500)
    S.t(40, gy - 8, "left ↓", 12, SUB)
    for l in range(n):
        S.t(gx - 8, gy + l * g + g / 2, "%d:%s" % (l, s[l]), 12, INK, "end", 500)
        for r in range(n):
            if l > r:
                S.rect(gx + r * g, gy + l * g, g, g, "out", rx=0)
                continue
            v = valid(l, r)
            S.cell(gx + r * g, gy + l * g, g, g, "✓" if v else "✗", "new" if v else "rem", 14)
    path = []
    left = 0
    cnt = defaultdict(int)
    for right, ch in enumerate(s):
        cnt[ch] += 1
        path.append((left, right))
        while cnt[ch] > 1:
            cnt[s[left]] -= 1
            left += 1
            path.append((left, right))
    assert len(path) == 9, path
    for (l, r) in path:
        S.ring(gx + r * g + 3, gy + l * g + 3, g - 6, g - 6, rx=4)
    tx = 340
    S.t(tx, 110, "brute force: 试遍所有 (left, right)", 14, INK, "start", 500)
    S.t(tx, 130, "= 上三角全部 %d 格 → O(n²) 个 window" % (n * (n + 1) // 2), 12, SUB)
    S.t(tx, 150, "每个 window 还要重新检查一遍 → O(n²) ~ O(n³)", 12, SUB)
    S.t(tx, 190, "sliding window: 只走有 ring 的 %d 格" % len(path), 14, INK, "start", 500)
    S.t(tx, 210, "路径: " + " → ".join("(%d,%d)" % p for p in path[:5]), 12, SUB)
    S.t(tx, 226, "         " + " → ".join("(%d,%d)" % p for p in path[5:]), 12, SUB)
    S.t(tx, 252, "right 只往右, left 只往下, 从不回头", 12, SUB)
    S.t(tx, 290, "为什么 left 不用回退:", 14, INK, "start", 500)
    S.t(tx, 310, "(left=1, right=2) 已经 ✗, right 再往右,", 12, SUB)
    S.t(tx, 326, "(left=1, right=3..5) 一定也 ✗ (超集更差)", 12, SUB)
    S.t(tx, 342, "→ 小于等于当前 left 的起点不会再合法", 12, SUB)
    S.t(tx, 358, "→ left 只需要向右走, 总共最多 n 步", 12, SUB)
    S.t(tx, 394, "每个 right 对应的最小合法 left", 12, SUB)
    S.t(tx, 410, "随 right 单调不减 → 双指针共 2n 步", 12, SUB)
    S.legend(446, [("new", "合法"), ("rem", "不合法"), ("ring", "sliding window 走过的格")])
    S.save("template_core.svg", 470)


core_template()


# ================================================================ P1 Longest Substring Without Repeating
def trace_longest():
    s = "pwwkew"
    cnt = defaultdict(int)
    left = best = 0
    steps = []
    for right, ch in enumerate(s):
        cnt[ch] += 1
        l0 = left
        n2 = "cnt[%s] = %d %s" % (ch, cnt[ch], "✗ 重复" if cnt[ch] > 1 else "✓")
        removed = []
        while cnt[ch] > 1:
            cnt[s[left]] -= 1
            removed.append(s[left])
            left += 1
        l1 = left
        L = right - left + 1
        old = best
        best = max(best, L)
        n3 = ("pop %s → left %d→%d" % (",".join(removed), l0, l1)) if removed else "不需要缩"
        c4 = [("window = \"%s\"" % s[l1:right + 1], 12, 400, SUB),
              ("len = %d - %d + 1 = %d" % (right, l1, L), 14, 500, INK),
              ("best = max(%d, %d) = %d" % (old, L, best), 14, 500, INK)]
        steps.append(dict(right=right, l0=l0, l1=l1, c1=stepinfo(right, "ch = '%s'" % ch),
                          n2=n2, n3=n3, c4=c4, ring3=(L == best and L > old)))
    assert best == NS["length_of_longest_substring"](s) == 3
    trace_svg("longest_substring_trace.svg", "Longest Substring Without Repeating Characters trace",
              ["s = \"pwwkew\" · 每一步: ch 进 window → cnt[ch] > 1 就缩 left → 更新 best",
               "cnt = window 里每个字符出现的次数 · len = right - left + 1"],
              ["当前输入", "ch 进 window 之后", "缩 left 之后", "计算"],
              list(s), steps, "答案: best = 3 (\"wke\" 或 \"kew\")", LEG)


trace_longest()


def core_longest():
    S = Svg("为什么只有新进来的 ch 可能重复")
    S.t(40, 18, "s = \"pwwkew\", right = 5, ch = 'w' · 进来之前 window = s[2..4] = \"wke\" 是合法的", 12, SUB)
    S.t(40, 38, "旧 window 没有重复 → 新出现的重复一定涉及 ch → 只检查 cnt[ch] > 1", 12, SUB)
    s = "pwwkew"
    xa = 200
    rows = [
        (70, "① 进来之前", ["out", "out", "keep", "keep", "keep", "out"], "合法, 长度 3", [(2, "L"), (4, "R")]),
        (150, "② 'w' 进来", ["out", "out", "keep", "keep", "keep", "new"], "cnt['w'] = 2 > 1, 不合法", [(2, "L"), (5, "R")]),
        (230, "③ pop s[left]", ["out", "out", "rem", "keep", "keep", "keep"], "cnt['w'] = 1, 重新合法", [(3, "L"), (5, "R")]),
    ]
    for y, lab, roles, note, mk in rows:
        S.t(40, y + 13, lab, 14, INK, "start", 500)
        S.array(xa, y, list(s), roles)
        S.ptrs(xa, y + 40, mk)
        S.t(xa + 6 * 22 + 20, y + 13, note, 12, SUB)
    S.arrow([(xa + 2 * 22 + 11, 262), (xa + 2 * 22 + 11, 290)], ARR, dash=True)
    S.t(xa + 2 * 22 + 22, 298, "被踢掉的 'w' = 重复的那个, left 2 → 3", 12, "#712B13")
    S.t(40, 336, "invariant (每次更新 best 时都成立): s[left..right] 没有重复字符", 14, INK, "start", 500)
    S.t(40, 358, "left 停在\"刚好让 ch 不重复\"的位置: 再多缩只会让 window 更短", 12, SUB)
    S.legend(388, LEG_NR)
    S.save("longest_substring_core.svg", 412)


core_longest()


# ================================================================ P2 Max Consecutive Ones III
def trace_ones():
    nums, k = [1, 1, 0, 0, 1, 1, 0], 2
    zeros = 0
    left = best = 0
    steps = []
    for right, x in enumerate(nums):
        if x == 0:
            zeros += 1
        l0 = left
        n2 = "zeros = %d %s k = %d" % (zeros, "≤" if zeros <= k else ">", k)
        rem = []
        while zeros > k:
            if nums[left] == 0:
                zeros -= 1
            rem.append(nums[left])
            left += 1
        l1 = left
        L = right - left + 1
        old = best
        best = max(best, L)
        n3 = ("pop %s → zeros = %d" % (",".join(map(str, rem)), zeros)) if rem else "不需要缩"
        c4 = [("window 有 %d 个 0, 全翻成 1" % zeros, 12, 400, SUB),
              ("len = %d - %d + 1 = %d" % (right, l1, L), 14, 500, INK),
              ("best = max(%d, %d) = %d" % (old, L, best), 14, 500, INK)]
        steps.append(dict(right=right, l0=l0, l1=l1, c1=stepinfo(right, "x = %d" % x),
                          n2=n2, n3=n3, c4=c4, ring3=(L == best and L > old)))
    assert best == NS["longest_ones"](nums, k)
    return nums, k, steps, best


def svg_ones():
    nums, k, steps, best = trace_ones()
    trace_svg("max_consecutive_ones_iii_trace.svg", "Max Consecutive Ones III trace",
              ["nums = [1,1,0,0,1,1,0], k = 2 · 每一步: x 进 window → zeros > k 就缩 left → 更新 best",
               "zeros = window 里 0 的个数 (= 需要翻转的次数, 预算是 k)"],
              ["当前输入", "x 进 window 之后", "缩 left 之后", "计算"],
              [str(x) for x in nums], steps, "答案: best = %d" % best, LEG)
    return best


ONES_BEST = svg_ones()


def core_ones():
    S = Svg("Max Consecutive Ones III 的合法条件")
    S.t(40, 18, "把\"最多翻 k 个 0\"翻译成 window 的合法条件: window 里 0 的个数 ≤ k", 12, SUB)
    S.t(40, 38, "nums = [1,1,0,0,1,1,0], k = 2 · 最长的合法 window = nums[0..5]", 12, SUB)
    nums = [1, 1, 0, 0, 1, 1, 0]
    x0 = 150
    y = 70
    S.t(40, y + 15, "window 内容", 14, INK, "start", 500)
    S.array(x0, y, [str(v) for v in nums], ["keep"] * 6 + ["out"], cw=30, ch=30)
    S.ring(x0, y, 6 * 30, 30)
    S.ptrs(x0, y + 46, [(0, "L"), (5, "R")], cw=30)
    y = 160
    S.t(40, y + 15, "翻转后", 14, INK, "start", 500)
    S.array(x0, y, ["1"] * 6 + ["0"], ["new" if nums[i] == 0 else "keep" for i in range(6)] + ["out"], cw=30, ch=30)
    S.t(x0, y + 48, "两个 0 被翻成 1 (绿色) → 6 个连续的 1", 12, SUB)
    S.arrow([(x0 + 3 * 30 + 15, 116), (x0 + 3 * 30 + 15, 154)], SUB)
    S.t(40, 246, "monotone: right 往右扩, zeros 只增不减 → 超预算就一定要缩 left", 14, INK, "start", 500)
    S.t(40, 268, "缩 left 时 zeros 只在 nums[left] == 0 才 -1, 所以 while 里要判断一下", 12, SUB)
    S.t(40, 288, "和上一题的差别: 合法条件从\"没有重复\"换成\"zeros <= k\", 状态从 cnt 换成一个整数 zeros", 12, SUB)
    S.legend(322, [("keep", "原本就是 1"), ("new", "被翻成 1 的 0"), ("out", "window 外"), ("ring", "最长 window")])
    S.save("max_consecutive_ones_iii_core.svg", 346)


core_ones()


# ================================================================ P3 Longest Repeating Character Replacement
def trace_replace():
    s, k = "AABABBA", 1
    cnt = defaultdict(int)
    left = best = 0
    steps = []
    for right, ch in enumerate(s):
        cnt[ch] += 1
        l0 = left
        L0 = right - left + 1
        mx = max(cnt.values())
        n2 = "A:%d B:%d  %d-%d=%d %s %d" % (cnt["A"], cnt["B"], L0, mx, L0 - mx,
                                           "≤" if L0 - mx <= k else ">", k)
        rem = []
        while (right - left + 1) - max(cnt.values()) > k:
            cnt[s[left]] -= 1
            rem.append(s[left])
            left += 1
        l1 = left
        L = right - left + 1
        mx2 = max(cnt.values())
        old = best
        best = max(best, L)
        n3 = ("pop %s: A:%d B:%d" % (",".join(rem), cnt["A"], cnt["B"])) if rem else "不需要缩"
        c4 = [("需替换 %d-%d=%d ≤ k=%d" % (L, mx2, L - mx2, k), 12, 400, SUB),
              ("len = %d - %d + 1 = %d" % (right, l1, L), 14, 500, INK),
              ("best = max(%d, %d) = %d" % (old, L, best), 14, 500, INK)]
        steps.append(dict(right=right, l0=l0, l1=l1, c1=stepinfo(right, "ch = '%s'" % ch),
                          n2=n2, n3=n3, c4=c4, ring3=(L == best and L > old)))
    assert best == NS["character_replacement"](s, k) == 4
    return s, k, steps, best


def svg_replace():
    s, k, steps, best = trace_replace()
    trace_svg("char_replacement_trace.svg", "Longest Repeating Character Replacement trace",
              ["s = \"AABABBA\", k = 1 · 每一步: ch 进 window → (len - max) > k 就缩 left → 更新 best",
               "len - max = 需替换数 = window 长度 - 出现最多的字符个数 (max = max(cnt.values()))"],
              ["当前输入", "ch 进 window 之后", "缩 left 之后", "计算"],
              list(s), steps, "答案: best = %d" % best, LEG)


svg_replace()


def core_replace():
    S = Svg("Longest Repeating Character Replacement 的合法条件")
    S.t(40, 18, "window 里出现最多的字符保持不动, 其余字符都替换成它 → 需替换数 = len - max", 12, SUB)
    S.t(40, 38, "合法 ⇔ len - max ≤ k  (k = 1)", 14, INK, "start", 500)
    x0 = 130
    rows = [
        (70, ["A", "A", "B", "A"], ["keep"] * 4, "len = 4, max = A:3", "需替换 = 4 - 3 = 1 ≤ k = 1, 合法", False),
        (140, ["A", "A", "B", "A", "B"], ["keep"] * 4 + ["new"], "len = 5, max = A:3", "需替换 = 5 - 3 = 2 > k = 1, 不合法", True),
    ]
    for y, items, roles, a, b, bad in rows:
        S.t(40, y + 16, "window", 14, INK, "start", 500)
        S.array(x0, y, items, roles, cw=34, ch=32)
        S.t(x0 + 5 * 34 + 20, y + 6, a, 12, SUB)
        S.t(x0 + 5 * 34 + 20, y + 26, b, 12, "#712B13" if bad else INK, "start", 500)
    S.arrow([(x0 + 17, 180), (x0 + 17, 214)], ARR, dash=True)
    S.t(x0 + 30, 224, "不合法 → pop 最左的 A, left 右移 1", 12, "#712B13")
    S.t(40, 268, "monotone: right 往右扩, len - max 只增不减 (len 加 1, max 最多加 1)", 14, INK, "start", 500)
    S.t(40, 290, "所以不合法了只能缩 left, 不用回头试更小的 left", 12, SUB)
    S.t(40, 310, "和上一题的差别: 合法条件要用\"window 里的最大频率\", 用 max(cnt.values()), 最多 26 项, 仍是 O(n)", 12, SUB)
    S.t(40, 330, "(另有一种 max_freq 只增不减的省略写法, 面试不需要, 这里不展开)", 12, SUB)
    S.legend(360, LEG_NR)
    S.save("char_replacement_core.svg", 384)


core_replace()


# ================================================================ P4 Permutation in String (fixed size)
def cnt_str(win, keys=None):
    items = sorted((c, v) for c, v in win.items() if v > 0)
    return " ".join("%s:%d" % (c, v) for c, v in items) or "(空)"


def trace_perm():
    s1, s2 = "ab", "eidbaoo"
    m = len(s1)
    need = Counter(s1)
    win = Counter()
    steps = []
    found = None
    for right, ch in enumerate(s2):
        win[ch] += 1
        l0 = max(0, right - m)          # 踢人之前的 left
        n2 = "win: " + cnt_str(win)
        rem = None
        if right >= m:
            rem = s2[right - m]
            win[rem] -= 1
        l1 = right - m + 1 if right >= m else 0
        n3 = ("len %d > m = %d → pop %s" % (m + 1, m, rem)) if rem else "len %d ≤ m = %d, 不用 pop" % (right + 1, m)
        eq = all(win[c] == need[c] for c in set(win) | set(need))
        c4 = [("need: " + cnt_str(need), 12, 400, SUB),
              ("win:  " + cnt_str(win), 12, 400, SUB),
              ("win == need ? " + ("是" if eq else "否"), 14, 500, INK)]
        steps.append(dict(right=right, l0=l0, l1=l1, c1=stepinfo(right, "ch = '%s'" % ch),
                          n2=n2, n3=n3, c4=c4, ring3=eq))
        if eq:
            found = right - m + 1
            break
    assert found == 3 and NS["check_inclusion"](s1, s2) is True
    trace_svg("permutation_in_string_trace.svg", "Permutation in String trace",
              ["s1 = \"ab\" (m = 2), s2 = \"eidbaoo\" · 每一步: 右边进一个 → 满了 m+1 个就左边出一个 → win == need ?",
               "window 长度固定 = m = 2, 不需要 while; need = s1 里每个字母的个数, win = window 里每个字母的个数"],
              ["当前输入", "右边进一个之后", "左边出一个之后", "比较"],
              list(s2), steps, "答案: right = 4 时 win == need → return True (window = s2[3..4] = \"ba\")", LEG, rowh=88)


trace_perm()


def core_perm():
    S = Svg("固定长度 window: 每滑一步 O(1) 更新")
    s2 = "eidbaoo"
    m = 2
    S.t(40, 18, "s1 = \"ab\", m = 2 · need = {a:1, b:1} · s2 = \"eidbaoo\"", 12, SUB)
    S.t(40, 38, "window 长度恒为 m: 每滑一格 = 右边进 1 个 + 左边出 1 个, 不用重新数 m 个字符", 12, SUB)
    x0 = 40
    wins = [(0, "e i", "+ e"), (1, "i d", "+ d, - e"), (2, "d b", "+ b, - i"), (3, "b a", "+ a, - d")]
    ys = 72
    for idx, (l, _, op) in enumerate(wins):
        y = ys + idx * 58
        roles = ["out"] * len(s2)
        for i in range(l, l + m):
            roles[i] = "keep"
        roles[l + m - 1] = "new"
        S.array(x0, y, list(s2), roles)
        win = Counter(s2[l:l + m])
        eq = win == Counter("ab")
        S.ring(x0 + l * 22, y, m * 22, 26) if eq else None
        S.t(x0 + 7 * 22 + 20, y + 6, "window = s2[%d..%d]  %s" % (l, l + m - 1, cnt_str(win)), 12, SUB)
        S.t(x0 + 7 * 22 + 20, y + 24, ("win == need ✓" if eq else "win != need"), 12, INK if eq else SUB, "start", 500 if eq else 400)
        if idx:
            S.t(x0 + 7 * 22 + 200, y + 6, "更新: " + op, 12, "#712B13" if "-" in op else SUB)
    S.t(40, 318, "invariant: window 永远是 s2[right-m+1..right], 长度 m", 14, INK, "start", 500)
    S.t(40, 340, "识别: 题目说\"长度恰好是 m\" 或 \"连续 m 个\" → 固定窗口, 不是 while 缩 left, 而是 if right >= m 踢一个", 12, SUB)
    S.t(40, 360, "Find All Anagrams in a String: 完全同一个模板, 把 return True 换成 res.append(right - m + 1)", 12, SUB)
    S.legend(392, LEG_NR[:3] + [("ring", "win == need 的 window")])
    S.save("permutation_in_string_core.svg", 416)


core_perm()


# ================================================================ P5 Minimum Size Subarray Sum
def trace_minlen():
    target, nums = 7, [2, 3, 1, 2, 4, 3]
    total = 0
    left = 0
    best = inf
    steps = []
    for right, x in enumerate(nums):
        total += x
        l0 = left
        win_vals = nums[l0:right + 1]
        head = "total = " + " + ".join(map(str, win_vals)) + " = %d" % total if len(win_vals) > 1 else "total = %d" % total
        c4 = [(head, 14, 500, INK)]
        removed = []
        n2 = "total = %d %s target = %d" % (total, "≥" if total >= target else "<", target)
        improved = False
        while total >= target:
            L = right - left + 1
            old = best
            best = min(best, L)
            improved = improved or L < old
            c4.append(("%d ≥ %d: best = min(%s, %d) = %d" % (total, target, "∞" if old == inf else old, L, best), 12, 400, SUB))
            total -= nums[left]
            removed.append(nums[left])
            c4.append(("pop %d → total = %d" % (nums[left], total), 12, 400, "#712B13"))
            left += 1
        if not removed:
            c4.append(("total < target, 继续扩", 12, 400, SUB))
        n3 = ("pop %s → total = %d" % (",".join(map(str, removed)), total)) if removed else "不需要缩"
        steps.append(dict(right=right, l0=l0, l1=left, c1=stepinfo(right, "x = %d" % x),
                          n2=n2, n3=n3, c4=c4, ring3=False))
        steps[-1]["_best"] = best
    assert best == NS["min_subarray_len"](target, nums) == 2
    return steps, best


def svg_minlen():
    steps, best = trace_minlen()
    # 最短 window 出现时 (记答案那一刻) 的 window 不是 "缩 left 之后", 在 c4 里写清楚; 这里不画 ring
    trace_svg("min_subarray_len_trace.svg", "Minimum Size Subarray Sum trace",
              ["target = 7, nums = [2,3,1,2,4,3] · 每一步: x 进 window → total ≥ target 就 (记答案, 缩 left) 重复",
               "total = window 里所有数相加 · 合法 = total ≥ target"],
              ["当前输入", "x 进 window 之后", "缩 left 之后", "计算 (total ≥ target 就记答案)"],
              [str(x) for x in [2, 3, 1, 2, 4, 3]], steps,
              "答案: best = %d (window [4,3], total = 7)" % best, LEG_NR, rowh=96)


svg_minlen()


def core_minlen():
    S = Svg("求最长 vs 求最短: 记答案的位置不同")
    S.t(40, 18, "两种模板只差一件事: while 条件是\"不合法\"还是\"合法\", 以及记答案放在 while 的外面还是里面", 12, SUB)
    for x, title, lines, clr in (
            (40, "最长: 合法时记答案", ["for right ...:", "    x 进 window", "    while 不合法:", "        移 left", "    best = max(best, len)   # 外面", ], NEW),
            (360, "最短: 合法时先记答案, 再缩", ["for right ...:", "    x 进 window", "    while 合法:", "        best = min(best, len)   # 里面", "        移 left"], REM)):
        S.rect(x, 50, 280, 132, clr, rx=6)
        S.t(x + 14, 70, title, 14, clr[2], "start", 500)
        for i, ln in enumerate(lines):
            S.t(x + 14, 96 + i * 18, ln.replace(" ", " "), 12, INK)
    S.t(40, 206, "为什么最短是\"合法才缩\":", 14, INK, "start", 500)
    S.t(40, 228, "nums 全是正数 → total 随 right 增大, 随 left 增大而减小 (单调)", 12, SUB)
    S.t(40, 246, "window 合法 (total >= target) 时, 缩 left 只会让 window 更短, 是下一个候选;", 12, SUB)
    S.t(40, 264, "缩到刚好不合法, 说明 left 再往右没有意义 (此 right 的最短 window 已找到)", 12, SUB)
    S.t(40, 296, "例: right = 4, window [3,1,2,4] total = 10 ≥ 7", 12, SUB)
    xa = 40
    arr = ["2", "3", "1", "2", "4", "3"]
    rows = [(1, True, "len = 4, total = 3+1+2+4 = 10 ≥ 7: best = 4, pop 3"),
            (2, True, "len = 3, total = 1+2+4 = 7 ≥ 7: best = 3, pop 1"),
            (3, False, "len = 2, total = 2+4 = 6 < 7: 不合法, 停")]
    for i, (l, popped, txt) in enumerate(rows):
        y = 312 + i * 40
        roles = ["out"] * 6
        for j in range(l, 5):
            roles[j] = "keep"
        if popped:
            roles[l] = "rem"
        S.array(xa, y, arr, roles)
        S.t(xa + 6 * 22 + 16, y + 14, txt, 12, SUB if popped else "#712B13")
    S.legend(448, LEG_NR[1:3] + [("out", "window 外")])
    S.save("min_subarray_len_core.svg", 472)


core_minlen()


# ================================================================ P6 Minimum Window Substring
def need_str(need, seen):
    return " ".join("%s:%d" % (c, need[c]) for c in seen)


def trace_minwin():
    s, t = "ABAECBA", "ABC"
    need = Counter(t)
    missing = len(t)
    seen = list(dict.fromkeys(t))
    left = 0
    best_len, best_start = inf, 0
    steps = []
    for right, ch in enumerate(s):
        if ch not in seen:
            seen.append(ch)
        m_before = missing
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        l0 = left
        n2 = "need " + need_str(need, seen)
        c4 = [("missing: %d → %d" % (m_before, missing), 14, 500, INK)]
        rem = []
        improved = False
        while missing == 0:
            L = right - left + 1
            if L < best_len:
                best_len, best_start = L, left
                improved = True
            c = s[left]
            need[c] += 1
            mm = missing
            if need[c] > 0:
                missing += 1
            rem.append(c)
            c4.append(("len=%d best=%d, pop %s" % (L, best_len, c), 12, 400, SUB))
            c4.append(("need[%s]=%d%s" % (c, need[c], (" > 0, missing=%d" % missing) if need[c] > 0 else " 不缺, 仍合法"), 12, 400, "#712B13"))
            left += 1
        if not rem:
            c4.append(("missing > 0: 还不合法", 12, 400, SUB))
        n3 = ("pop %s · " % ",".join(rem) + "need " + need_str(need, seen)) if rem else "need " + need_str(need, seen)
        steps.append(dict(right=right, l0=l0, l1=left, c1=stepinfo(right, "ch = '%s'" % ch),
                          n2=n2, n3=n3, c4=c4))
    ans = NS["min_window"](s, t)
    assert ans == s[best_start:best_start + best_len] == "CBA", ans
    return s, t, steps, ans


def svg_minwin():
    s, t, steps, ans = trace_minwin()
    trace_svg("min_window_trace.svg", "Minimum Window Substring trace",
              ["s = \"ABAECBA\", t = \"ABC\", missing 起始 = len(t) = 3 · 每一步: ch 进 → missing == 0 就 (记答案, 缩 left) 重复",
               "need[c] > 0: 还缺 c · = 0: 刚好 · < 0: window 里多了 · missing = 还缺的字符总个数"],
              ["当前输入", "ch 进 window 之后", "缩 left 之后", "计算"],
              list(s), steps, "答案: best_len = 3, 起点 4 → \"%s\"" % ans,
              [("new", "新进 window 的"), ("rem", "移出 window 的"), ("keep", "window 里其他的"), ("out", "window 外")],
              rowh=96)


svg_minwin()


def core_minwin():
    S = Svg("need / missing: 怎么 O(1) 判断 window 覆盖了 t")
    S.t(40, 18, "t = \"ABC\" → need 起始 = {A:1, B:1, C:1}, missing = 3 · 每进一个字符 need[ch] -= 1, 每出一个 need[ch] += 1", 12, SUB)
    S.t(40, 38, "不用每次比较两个 Counter: 只在\"缺的\"字符进来时 missing -1, \"不缺\"的字符出去时 missing 不变", 12, SUB)

    def panel(x, title, window_txt, vals, miss, notes):
        S.rect(x, 60, 290, 230, "out", rx=6)
        S.t(x + 14, 82, title, 14, INK, "start", 500)
        S.t(x + 14, 102, window_txt, 12, SUB)
        for i, (c, v) in enumerate(vals):
            y = 120 + i * 32
            S.t(x + 14, y + 14, "need[%s]" % c, 14, INK, "start", 500)
            role = "rem" if v > 0 else ("new" if v == 0 else "keep")
            S.cell(x + 80, y, 38, 28, str(v), role, 14)
            S.t(x + 128, y + 14, notes[i], 12, SUB)
        S.t(x + 14, 262, miss, 14, INK, "start", 500)

    panel(40, "window = \"ABAEC\" (s[0..4])", "A, B, C 都进来了, 合法",
          [("A", -1), ("B", 0), ("C", 0), ("E", -1)], "missing = 0, 合法",
          ["多 1 个 (window 里有 2 个 A)", "刚好", "刚好", "t 里没有, 一律是多余的"])
    panel(350, "pop 'A', 'B' 之后: \"AEC\"", "pop A: 0, 不缺, 仍合法 → pop B: 变成 1", 
          [("A", 0), ("B", 1), ("C", 0), ("E", -1)], "missing = 1, 不合法",
          ["刚好", "缺 1 个 → missing + 1", "刚好", "多余"])
    S.arrow([(334, 175), (346, 175)], SUB)
    S.t(40, 322, "need[c] > 0 才说明 c 是\"缺\"的 → 只有这时进/出才改变 missing; 其余情况 need 在 0 以下上下浮动不影响合法性", 12, SUB)
    S.t(40, 342, "missing == 0 ⇔ t 里每个字符 (含重复次数) window 都够了 → 判断合法只要 O(1)", 14, INK, "start", 500)
    S.legend(376, [("rem", "还缺 (> 0)"), ("new", "刚好 (= 0)"), ("keep", "多出来 (< 0)")])
    S.save("min_window_core.svg", 400)


core_minwin()


# ================================================================ P7 Subarray Product Less Than K
def trace_prod():
    nums, k = [10, 5, 2, 6, 1, 3], 100
    prod = 1
    left = ans = 0
    steps = []
    for right, x in enumerate(nums):
        prod *= x
        l0 = left
        pv = nums[l0:right + 1]
        p_expr = " × ".join(map(str, pv))
        n2 = "prod = %d %s k = %d" % (prod, "<" if prod < k else "≥", k)
        rem = []
        while prod >= k:
            prod //= nums[left]
            rem.append(nums[left])
            left += 1
        l1 = left
        add = right - left + 1
        subs = " ".join("[" + ",".join(map(str, nums[i:right + 1])) + "]" for i in range(right, left - 1, -1))
        old = ans
        ans += add
        n3 = ("pop %s → prod = %d" % (",".join(map(str, rem)), prod)) if rem else "不需要缩"
        c4 = [("prod = %d" % prod, 14, 500, INK),
              ("+%d 个: %s" % (add, subs), 12, 400, SUB),
              ("ans = %d + %d = %d" % (old, add, ans), 14, 500, INK)]
        steps.append(dict(right=right, l0=l0, l1=l1, c1=stepinfo(right, "x = %d" % x),
                          n2=n2, n3=n3, c4=c4))
    assert ans == NS["num_subarray_product_less_than_k"](nums, k) == 16
    return nums, k, steps, ans


def svg_prod():
    nums, k, steps, ans = trace_prod()
    trace_svg("product_less_than_k_trace.svg", "Subarray Product Less Than K trace",
              ["nums = [10,5,2,6,1,3], k = 100 · 每一步: x 进 (prod *= x) → prod ≥ k 就缩 left (prod //= nums[left])",
               "ans += right - left + 1 = 以 right 结尾的合法 subarray 个数 (起点 left..right 各一个)"],
              ["当前输入", "x 进 window 之后", "缩 left 之后", "计算"],
              [str(x) for x in nums], steps, "答案: ans = %d" % ans, LEG_NR, rowh=88)


svg_prod()


def core_prod():
    S = Svg("计数: 以 right 结尾的合法 subarray 个数 = right - left + 1")
    S.t(40, 18, "nums = [10,5,2,6], k = 100, right = 3 (x = 6), 缩完之后 left = 1 · window = [5,2,6], prod = 60", 12, SUB)
    S.t(40, 38, "固定右端点 right, 合法的起点是连续的一段 left..right (起点越靠左乘积越大, 单调)", 12, SUB)
    x0 = 70
    nums = ["10", "5", "2", "6"]
    S.array(x0, 70, nums, ["out", "keep", "keep", "new"], cw=40, ch=30)
    for i in range(4):
        S.t(x0 + i * 40 + 20, 112, "idx %d" % i, 12, SUB, "middle")
    rows = [(3, "[6]", "prod = 6 < 100", True), (2, "[2,6]", "prod = 2 × 6 = 12 < 100", True),
            (1, "[5,2,6]", "prod = 5 × 2 × 6 = 60 < 100", True), (0, "[10,5,2,6]", "prod = 10 × 5 × 2 × 6 = 600 ≥ 100", False)]
    for i, (st, lab, txt, ok) in enumerate(rows):
        y = 134 + i * 38
        S.rect(x0 + st * 40 + 2, y + 6, (4 - st) * 40 - 4, 18, "new" if ok else "rem", rx=4, dash=not ok)
        S.t(x0 + st * 40 + (4 - st) * 20, y + 15, lab if ok else "", 12, NEW[2], "middle", 500)
        S.t(x0 + 4 * 40 + 20, y + 15, txt + ("  ✓" if ok else "  ✗ (left = 0 已被缩掉)"), 12, INK if ok else "#712B13")
    S.t(40, 304, "→ 以 right = 3 结尾的合法 subarray 有 3 个 = right - left + 1 = 3 - 1 + 1", 14, INK, "start", 500)
    S.t(40, 326, "每个 subarray 只按它的右端点数一次 → 不重不漏; 把每个 right 的个数相加就是答案", 12, SUB)
    S.t(40, 346, "和前面的差别: 前面是 best = max(...) 只关心最大的 window; 这里每一步 ans += (个数)", 12, SUB)
    S.t(40, 366, "注意: 只在 nums 全是正数时 prod 才单调. 有 0 或负数就不能用", 12, SUB)
    S.legend(398, [("keep", "window 里 (合法起点)"), ("new", "新进来的 6"), ("out", "已被缩掉")])
    S.save("product_less_than_k_core.svg", 422)


core_prod()


# ================================================================ P8 Subarrays with K Different Integers
def trace_kdistinct():
    nums, k = [1, 2, 1, 2, 3], 2

    def run(kk):
        cnt = defaultdict(int)
        left = 0
        res = []
        for right, x in enumerate(nums):
            cnt[x] += 1
            l0 = left
            ndist = len(cnt)
            while len(cnt) > kk:
                cnt[nums[left]] -= 1
                if cnt[nums[left]] == 0:
                    del cnt[nums[left]]
                left += 1
            res.append((l0, left, right - left + 1, dict(cnt), ndist, kk))
        return res

    ra, rb = run(k), run(k - 1)
    steps = []
    ta = tb = 0
    for r in range(len(nums)):
        (a0, a1, a, ca, da, ka), (b0, b1, b, cb, db, kb) = ra[r], rb[r]
        ta += a
        tb += b

        def fmt(c):
            return " ".join("%d:%d" % (key, c[key]) for key in sorted(c))
        def note(l0, l1, d, kk, c):
            top = ("%d 种 > %d → pop %s" % (d, kk, ",".join(str(v) for v in nums[l0:l1]))) if l1 > l0 else "%d 种 ≤ %d, 不用 pop" % (d, kk)
            return top + "\n" + "cnt " + fmt(c)
        n2 = note(a0, a1, da, ka, ca)
        n3 = note(b0, b1, db, kb, cb)
        c4 = [("a2 = %d - %d + 1 = %d" % (r, a1, a), 12, 400, SUB),
              ("a1 = %d - %d + 1 = %d" % (r, b1, b), 12, 400, SUB),
              ("a2 - a1 = %d" % (a - b), 14, 500, INK)]
        steps.append(dict(mode="two", right=r, w2=(a0, a1), w3=(b0, b1), c1=stepinfo(r, "x = %d" % nums[r]),
                          n2=n2, n3=n3, c4=c4))
    assert ta == 12 and tb == 5
    assert NS["subarrays_with_k_distinct"](nums, k) == ta - tb == 7
    return nums, k, steps, ta, tb


def svg_kdistinct():
    nums, k, steps, ta, tb = trace_kdistinct()
    trace_svg("k_distinct_trace.svg", "Subarrays with K Different Integers trace",
              ["nums = [1,2,1,2,3], k = 2 · 同一个 right 同时跑两个 window: 最多 2 种 (atMost(2)) 和 最多 1 种 (atMost(1))",
               "a2 = 以 right 结尾、最多 2 种的 subarray 数 · a1 = 最多 1 种 · 恰好 2 种 = a2 - a1"],
              ["当前输入", "atMost(2) 的 window", "atMost(1) 的 window", "以 right 结尾的个数"],
              [str(x) for x in nums], steps,
              "答案: atMost(2) = 1+2+3+4+2 = %d, atMost(1) = 1+1+1+1+1 = %d, 12 - 5 = %d" % (ta, tb, ta - tb),
              LEG_NR, cw=26, rowh=100)


svg_kdistinct()


def core_kdistinct():
    S = Svg("exactly K = atMost(K) - atMost(K-1)")
    S.t(40, 18, "nums = [1,2,1,2,3], k = 2 · 全部 subarray 里, 按\"不同数字的种类数\"分类", 12, SUB)
    S.t(40, 38, "\"恰好 K 种\" 本身不单调, 不能直接滑: window 扩大可能 K → K+1, 缩小可能 K → K-1, 两个方向都会破坏", 12, SUB)
    S.t(40, 56, "\"最多 K 种\" 单调: 扩大只会让种类变多 → 超了就缩 left, 是标准模板", 12, SUB)
    x0, y0, u = 40, 104, 40
    S.t(x0, y0 - 14, "atMost(2) = 12 个 subarray (种类数 ≤ 2)", 14, INK, "start", 500)
    S.cell(x0, y0, 5 * u, 34, "种类 ≤ 1: 5 个 = atMost(1)", "keep", 14)
    S.cell(x0 + 5 * u, y0, 7 * u, 34, "种类 = 2: 7 个 = 要的答案", "new", 14)
    S.ring(x0 + 5 * u, y0, 7 * u, 34)
    S.t(x0, y0 + 56, "→ 恰好 2 种 = atMost(2) - atMost(1) = 12 - 5 = 7", 14, INK, "start", 500)
    S.t(x0, y0 + 90, "7 个 subarray 是: [1,2] [2,1] [1,2] [1,2,1] [2,1,2] [1,2,1,2] [2,3]", 12, SUB)
    S.t(x0, y0 + 108, "(位置不同但内容相同的算多个, 按起止下标数)", 12, SUB)
    S.t(x0, y0 + 148, "同一套 at_most(k) 函数调两次, 每次 O(n) → 总共 O(n)", 12, SUB)
    S.t(x0, y0 + 168, "这个技巧可以推广到任何\"恰好 K\": Binary Subarrays With Sum, Count Number of Nice Subarrays", 12, SUB)
    S.legend(y0 + 200, [("keep", "种类 ≤ K-1"), ("new", "种类恰好 K"), ("ring", "答案")])
    S.save("k_distinct_core.svg", y0 + 224)


core_kdistinct()


exec(open(os.path.join(HERE, '03_sliding_window_doc.py'), encoding='utf-8').read())
