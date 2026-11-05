"""19 · Matrix / Simulation / Math / Bit / Sorting  ->  docs/19-matrix-math-bit.html
SVG 由本脚本生成, 所有数字来自真实运行的算法 (instrumented 版本, 并和文档里的代码对拍)。
文档里展示的每段代码都会在生成时 exec 并测试。
运行: cd build && python3 -I 19_matrix-math-bit.py
"""
import html
import os
import random
import sys
from copy import deepcopy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import doclib as d

SLUG = "19-matrix-math-bit"
SVG_DIR = os.path.join(d.ROOT, "docs", "svg", SLUG)
os.makedirs(SVG_DIR, exist_ok=True)

# ================================================================ 文档里的代码 (生成时 exec + 测试)
SPIRAL = '''
def spiralOrder(matrix):
    res = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:   # 区域还没缩没
        for c in range(left, right + 1):     # 1. 走上边 →
            res.append(matrix[top][c])
        top += 1                             # 上边用完, 上边界下移
        for r in range(top, bottom + 1):     # 2. 走右边 ↓
            res.append(matrix[r][right])
        right -= 1
        if top <= bottom:                    # 守卫: 只剩 1 行时不能再倒着走
            for c in range(right, left - 1, -1):   # 3. 走下边 ←
                res.append(matrix[bottom][c])
            bottom -= 1
        if left <= right:                    # 守卫: 只剩 1 列时不能再往上走
            for r in range(bottom, top - 1, -1):   # 4. 走左边 ↑
                res.append(matrix[r][left])
            left += 1
    return res
'''

ROTATE = '''
def rotate(matrix):                    # 顺时针 90 度, 原地
    n = len(matrix)
    for i in range(n):                 # 第 1 步: transpose, (i, j) → (j, i)
        for j in range(i + 1, n):      # 只走上三角, 每一对只换一次
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for row in matrix:                 # 第 2 步: 每行 reverse, (j, i) → (j, n-1-i)
        row.reverse()
'''

ZEROES = '''
def setZeroes(matrix):
    m, n = len(matrix), len(matrix[0])
    # 第一行 / 第一列要拿来当 flag, 先记住它们自己原本有没有 0
    row0 = any(matrix[0][j] == 0 for j in range(n))
    col0 = any(matrix[i][0] == 0 for i in range(m))
    for i in range(1, m):                # pass 1: 扫内部, 遇到 0 就留言
        for j in range(1, n):
            if matrix[i][j] == 0:
                matrix[i][0] = 0         # 留言: 第 i 行要清零
                matrix[0][j] = 0         # 留言: 第 j 列要清零
    for i in range(1, m):                # pass 2: 内部按留言清零
        for j in range(1, n):            # (留言区这时不能动, 还要读)
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0
    if row0:                             # 最后才处理留言区本身
        for j in range(n):
            matrix[0][j] = 0
    if col0:
        for i in range(m):
            matrix[i][0] = 0
'''

POW = '''
def myPow(x, n):
    if n < 0:                  # x^(-n) = (1/x)^n
        x, n = 1 / x, -n
    res = 1.0
    while n:                   # 每轮处理 n 的一个 bit, 共 log2(n) 轮
        if n & 1:              # 这一位是 1 → 乘上当前的 x (= 原 x 的 2^k 次方)
            res *= x
        x *= x                 # x 平方: x^1 → x^2 → x^4 → x^8 ...
        n >>= 1                # 看下一位
    return res
'''

PALIN = '''
def isPalindrome(x):
    if x < 0 or (x % 10 == 0 and x != 0):   # 负数不是; 末位 0 反过来有前导 0
        return False
    rev = 0
    while x > rev:             # 只反转后半: rev 追上 x 就停
        rev = rev * 10 + x % 10    # x % 10 取末位, 接到 rev 末尾
        x //= 10                   # x // 10 丢掉末位
    return x == rev or x == rev // 10   # 偶数位: x == rev; 奇数位: rev 多一位中间数
'''

XOR = '''
def singleNumber(nums):
    res = 0
    for x in nums:
        res ^= x        # a^a = 0, a^0 = a, 顺序无所谓 → 成对的全部抵消
    return res

def missingNumber(nums):     # nums 是 0..n 少一个数, 长度 n
    res = len(nums)          # 下标只有 0..n-1, 先把 n 放进来
    for i, x in enumerate(nums):
        res ^= i ^ x         # 下标 i 和值 x 各一次, 没缺的数都出现两次
    return res
'''

BITS = '''
def hammingWeight(n):
    cnt = 0
    while n:
        n &= n - 1       # 消掉最低位的 1: 每个 1 恰好被消一次
        cnt += 1
    return cnt
'''

MINDIFF = '''
def minimumAbsDifference(arr):
    arr.sort()                               # O(n log n): 预处理
    best, res = float("inf"), []
    for a, b in zip(arr, arr[1:]):           # 只看相邻: n - 1 对
        diff = b - a
        if diff < best:                      # 更小: 重置
            best, res = diff, [[a, b]]
        elif diff == best:                   # 一样小: 追加
            res.append([a, b])
    return res
'''

LARGEST = '''
from functools import cmp_to_key

def largestNumber(nums):
    strs = [str(x) for x in nums]
    # a 排前面当且仅当 a+b > b+a (拼起来更大); 返回负数 = a 排前
    strs.sort(key=cmp_to_key(lambda a, b: -1 if a + b > b + a else 1))
    ans = "".join(strs)
    return "0" if ans[0] == "0" else ans
'''

ROMAN = '''
def romanToInt(s):
    val = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    for i, ch in enumerate(s):
        if i + 1 < len(s) and val[ch] < val[s[i + 1]]:   # 左小右大 → 减
            total -= val[ch]
        else:
            total += val[ch]
    return total
'''


def load(src):
    ns = {}
    exec(src, ns)
    return ns


# ---- 测试: 每段代码都和暴力解对拍 ----
random.seed(7)


def t_spiral():
    f = load(SPIRAL)["spiralOrder"]

    def brute(mat):  # visited + 方向表
        m, n = len(mat), len(mat[0])
        seen = [[False] * n for _ in range(m)]
        out, r, c, k = [], 0, 0, 0
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for _ in range(m * n):
            out.append(mat[r][c])
            seen[r][c] = True
            nr, nc = r + dirs[k][0], c + dirs[k][1]
            if not (0 <= nr < m and 0 <= nc < n) or seen[nr][nc]:
                k = (k + 1) % 4
                nr, nc = r + dirs[k][0], c + dirs[k][1]
            r, c = nr, nc
        return out
    for m in range(1, 7):
        for n in range(1, 7):
            mat = [[i * n + j + 1 for j in range(n)] for i in range(m)]
            assert f(deepcopy(mat)) == brute(mat), (m, n)
    assert f([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]) == [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]


def t_rotate():
    f = load(ROTATE)["rotate"]
    for n in range(1, 8):
        mat = [[random.randint(0, 99) for _ in range(n)] for _ in range(n)]
        want = [[mat[n - 1 - j][i] for j in range(n)] for i in range(n)]  # 顺时针
        got = deepcopy(mat)
        f(got)
        assert got == want, n


def t_zeroes():
    f = load(ZEROES)["setZeroes"]
    for _ in range(300):
        m, n = random.randint(1, 5), random.randint(1, 5)
        mat = [[random.choice([0, 1, 2, 3, 4, 5]) for _ in range(n)] for _ in range(m)]
        zr = {i for i in range(m) for j in range(n) if mat[i][j] == 0}
        zc = {j for i in range(m) for j in range(n) if mat[i][j] == 0}
        want = [[0 if (i in zr or j in zc) else mat[i][j] for j in range(n)] for i in range(m)]
        got = deepcopy(mat)
        f(got)
        assert got == want, mat


def t_pow():
    f = load(POW)["myPow"]
    for x in (2.0, 3.0, 0.5, -2.0, 1.5):
        for n in range(-12, 13):
            assert abs(f(x, n) - x ** n) <= 1e-9 * max(1, abs(x ** n)), (x, n)
    assert f(2.0, 10) == 1024.0


def t_palin():
    f = load(PALIN)["isPalindrome"]
    for x in list(range(-20, 3000)) + [random.randint(0, 10 ** 9) for _ in range(2000)]:
        assert f(x) == (x >= 0 and str(x) == str(x)[::-1]), x


def t_xor():
    ns = load(XOR)
    for _ in range(300):
        n = random.randint(1, 9)
        arr = random.sample(range(0, 50), n)
        nums = [v for v in arr for _ in range(2)] + [random.choice(range(50, 90))]
        random.shuffle(nums)
        assert ns["singleNumber"](nums) == [v for v in nums if nums.count(v) == 1][0]
        full = list(range(n + 1))
        miss = random.choice(full)
        lst = [v for v in full if v != miss]
        random.shuffle(lst)
        assert ns["missingNumber"](lst) == miss
    assert ns["singleNumber"]([4, 1, 2, 1, 2]) == 4
    assert ns["missingNumber"]([3, 0, 1]) == 2


def t_bits():
    f = load(BITS)["hammingWeight"]
    for n in list(range(0, 1000)) + [random.randint(0, 2 ** 32 - 1) for _ in range(500)]:
        assert f(n) == bin(n).count("1")


def t_mindiff():
    f = load(MINDIFF)["minimumAbsDifference"]
    for _ in range(300):
        arr = random.sample(range(-30, 60), random.randint(2, 9))
        best = min(abs(a - b) for i, a in enumerate(arr) for b in arr[i + 1:])
        want = sorted([a, b] for i, a in enumerate(sorted(arr)) for b in sorted(arr)[i + 1:] if b - a == best)
        assert f(list(arr)) == want
    assert load(LARGEST)["largestNumber"]([3, 30, 34, 5, 9]) == "9534330"
    assert load(LARGEST)["largestNumber"]([0, 0]) == "0"
    assert load(LARGEST)["largestNumber"]([10, 2]) == "210"


def t_roman():
    f = load(ROMAN)["romanToInt"]

    def to_roman(num):
        out = ""
        for v, s in [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
                     (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]:
            while num >= v:
                out += s
                num -= v
        return out
    for k in range(1, 4000):
        assert f(to_roman(k)) == k, k
    assert f("MCMXCIV") == 1994


for fn in (t_spiral, t_rotate, t_zeroes, t_pow, t_palin, t_xor, t_bits, t_mindiff, t_roman):
    fn()
print("all code tests passed")

# ================================================================ svg kit
ROLE = {  # fill, stroke, text
    "new": ("#E1F5EE", "#0F6E56", "#085041"),
    "gone": ("#FAECE7", "#993C1D", "#712B13"),
    "old": ("#F1EFE8", "#5F5E5A", "#444441"),
    "blank": ("#FFFFFF", "#B4B2A9", "#52514E"),
}
INK, SUB = "#0B0B0B", "#52514E"
ARROW = {"g": "#52514E", "r": "#D85A30", "n": "#0F6E56", "o": "#EF9F27"}
FONT = 'ui-sans-serif, system-ui, -apple-system, "PingFang SC", sans-serif'
_n = [0]


def esc(s):
    return html.escape(str(s), quote=False)


def est(s, size=12):
    """估算文字宽度 (CJK 满宽, ASCII 约 0.55)"""
    return sum(size if ord(c) > 255 else size * 0.55 for c in str(s))


class Svg:
    def __init__(self, name, h, title, desc):
        _n[0] += 1
        self.name, self.h, self.title, self.desc = name, h, title, desc
        self.pid = "f%d" % _n[0]
        self.o = []

    def t(self, x, y, s, size=12, fill=SUB, anchor="start", weight=400):
        self.o.append('<text x="%s" y="%s" font-size="%d" fill="%s" text-anchor="%s" font-weight="%d" '
                      'dominant-baseline="central">%s</text>' % (x, y, size, fill, anchor, weight, esc(s)))

    def rect(self, x, y, w, h, role="old", rx=4, dash=False, sw=1.0):
        f, s, _ = ROLE[role]
        self.o.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%d" fill="%s" stroke="%s" '
                      'stroke-width="%s"%s/>' % (x, y, w, h, rx, f, s, sw, ' stroke-dasharray="4 3"' if dash else ""))

    def ring(self, x, y, w, h, pad=3, rx=6):
        self.o.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%d" fill="none" stroke="#EF9F27" '
                      'stroke-width="2.5"/>' % (x - pad, y - pad, w + 2 * pad, h + 2 * pad, rx))

    def cell(self, x, y, w, h, txt, role="old", ring=False, size=14, weight=500, dash=False, rx=4):
        self.rect(x, y, w, h, role, rx=rx, dash=dash)
        if ring:
            self.ring(x, y, w, h)
        if txt != "":
            self.t(x + w / 2, y + h / 2, txt, size, ROLE[role][2], "middle", weight)

    def line(self, x1, y1, x2, y2, color="#B4B2A9", dash="4 4", w=0.8):
        self.o.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s/>'
                      % (x1, y1, x2, y2, color, w, ' stroke-dasharray="%s"' % dash if dash else ""))

    def sep(self, y):
        self.line(40, y, 640, y)

    def arrow(self, x1, y1, x2, y2, kind="g", dash=False, w=1.5):
        self.o.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s marker-end="url(#%s-%s)"/>'
                      % (x1, y1, x2, y2, ARROW[kind], w, ' stroke-dasharray="5 4"' if dash else "", self.pid, kind))

    def path(self, dpath, kind="g", dash=False, w=1.5, arrow=True):
        self.o.append('<path d="%s" fill="none" stroke="%s" stroke-width="%s"%s%s/>'
                      % (dpath, ARROW[kind], w, ' stroke-dasharray="5 4"' if dash else "",
                         ' marker-end="url(#%s-%s)"' % (self.pid, kind) if arrow else ""))

    def head(self, l1, l2, cols):
        self.t(40, 18, l1)
        if l2:
            self.t(40, 38, l2)
        for x, lab in cols:
            self.t(x, 64, lab)
        self.sep(74)

    def legend(self, y, items):
        x = 40
        for role, label in items:
            if role == "ring":
                self.o.append('<rect x="%s" y="%s" width="14" height="14" rx="3" fill="#fff" stroke="#EF9F27" '
                              'stroke-width="2.5"/>' % (x, y - 7))
            else:
                self.rect(x, y - 7, 14, 14, role, rx=3)
            self.t(x + 20, y, label)
            x += 20 + est(label) + 22

    def render(self):
        defs = "".join(
            '<marker id="%s-%s" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" '
            'orient="auto"><path d="M2 1L8 5L2 9" fill="none" stroke="%s" stroke-width="1.5" '
            'stroke-linecap="round" stroke-linejoin="round"/></marker>' % (self.pid, k, c) for k, c in ARROW.items())
        return ('<svg width="100%%" viewBox="0 0 680 %d" role="img" xmlns="http://www.w3.org/2000/svg" '
                'font-family=\'%s\'><title>%s</title><desc>%s</desc><defs>%s</defs>'
                '<rect x="0" y="0" width="680" height="%d" fill="#fff"/>\n%s\n</svg>\n'
                % (self.h, FONT, esc(self.title), esc(self.desc), defs, self.h, "\n".join(self.o)))

    def save(self):
        with open(os.path.join(SVG_DIR, self.name + ".svg"), "w", encoding="utf-8") as f:
            f.write(self.render())


def grid(s, x, y, mat, cw, ch, roles=None, size=14, ring=None, default="old"):
    """画矩阵; roles[(i,j)] 指定角色; ring 是要加圈的 (i,j) 集合"""
    roles = roles or {}
    ring = ring or set()
    for i, row in enumerate(mat):
        for j, v in enumerate(row):
            s.cell(x + j * cw, y + i * ch, cw, ch, v, roles.get((i, j), default), ring=(i, j) in ring, size=size)


def bits(n, w):
    return format(n, "0%db" % w)

# ================================================================ 图 0: 第一性原理 core
def fig_intro_core():
    s = Svg("intro_core", 372, "杂项题的共同点",
            "四类题,暴力解各自浪费什么,以及用题目自身结构消掉浪费后 complexity 的变化")
    s.t(40, 18, "这个 doc 的题没有统一的数据结构 · 共同点: 暴力解在重复做或多存一份东西,")
    s.t(40, 38, "而题目自身的结构 (边界 / 二进制 / 配对 / 有序) 可以把它消掉")
    s.t(40, 64, "暴力解浪费什么")
    s.t(370, 64, "利用什么结构消掉")
    s.sep(74)
    rows = [
        ("矩阵 Spiral / Set Zeroes", "visited[m][n] 或复制一份矩阵", "space O(mn)",
         "4 个边界整数 / 矩阵自己的第一行第一列", "space O(1)"),
        ("Pow(x, n)", "n 个 x 连乘, 每个 x 都乘一次", "time O(n)",
         "n 的二进制拆分: 平方 + 按 bit 选择", "time O(log n)"),
        ("Single Number", "Hash Table 给每个数计数", "space O(n)",
         "XOR: a^a = 0, 成对的自己抵消", "space O(1)"),
        ("Min Absolute Difference", "所有 pair 两两比较", "time O(n^2)",
         "先 sort, 最近的一定是相邻的", "time O(n log n)"),
    ]
    y = 86
    for name, brute, bc, trick, tc in rows:
        s.t(40, y + 6, name, 14, INK, weight=500)
        s.cell(40, y + 20, 270, 40, "", "old")
        s.t(52, y + 33, brute, 12, ROLE["old"][2])
        s.t(52, y + 50, bc, 12, ROLE["old"][2], weight=500)
        s.arrow(314, y + 40, 360, y + 40, "g")
        s.cell(370, y + 20, 270, 40, "", "new")
        s.t(382, y + 33, trick, 12, ROLE["new"][2])
        s.t(382, y + 50, tc, 12, ROLE["new"][2], weight=500)
        y += 70
        if y < 360:
            s.sep(y - 6)
    s.legend(y + 2, [("old", "暴力解 / 浪费"), ("new", "利用结构后")])
    s.h = y + 24
    s.save()


# ================================================================ 1. Spiral Matrix
SP_M = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]


def spiral_steps(mat):
    """instrumented 版 spiralOrder: 每条边记一个 entry"""
    res = []
    top, bottom, left, right = 0, len(mat) - 1, 0, len(mat[0]) - 1
    ent = []

    def rec(name, rng, coords, bounds_note, skipped=False):
        ent.append(dict(name=name, rng=rng, coords=coords, vals=[mat[r][c] for r, c in coords],
                        b=(top, bottom, left, right), note=bounds_note, skipped=skipped))
    while top <= bottom and left <= right:
        coords = [(top, c) for c in range(left, right + 1)]
        rng = "row %d, c = %d..%d" % (top, left, right)
        res += [mat[r][c] for r, c in coords]
        top += 1
        rec("top", rng, coords, "top += 1")
        coords = [(r, right) for r in range(top, bottom + 1)]
        rng = "col %d, r = %d..%d" % (right, top, bottom)
        res += [mat[r][c] for r, c in coords]
        right -= 1
        rec("right", rng, coords, "right -= 1")
        if top <= bottom:
            coords = [(bottom, c) for c in range(right, left - 1, -1)]
            rng = "row %d, c = %d..%d" % (bottom, right, left)
            res += [mat[r][c] for r, c in coords]
            bottom -= 1
            rec("bottom", rng, coords, "bottom -= 1")
        else:
            rec("bottom", "", [], "top > bottom, 跳过", True)
        if left <= right:
            coords = [(r, left) for r in range(bottom, top - 1, -1)]
            rng = "col %d, r = %d..%d" % (left, bottom, top)
            res += [mat[r][c] for r, c in coords]
            left += 1
            rec("left", rng, coords, "left += 1")
        else:
            rec("left", "", [], "left > right, 跳过", True)
    return res, ent


def fig_spiral_core():
    s = Svg("spiral_core", 400, "Spiral Matrix 核心",
            "四个边界圈出还没走过的区域,每走完一条边收缩一次;走完一圈后区域缩成内层")
    s.t(40, 18, "top / bottom / left / right 四个边界圈出「还没走过」的区域")
    s.t(40, 38, "每走完一条边, 对应的边界向里收缩 1 · 图中数字 = 走的顺序")
    n = 4
    order = [[0] * n for _ in range(n)]
    t, b, l, r, k = 0, n - 1, 0, n - 1, 1
    while t <= b and l <= r:
        for c in range(l, r + 1): order[t][c] = k; k += 1
        t += 1
        for rr in range(t, b + 1): order[rr][r] = k; k += 1
        r -= 1
        if t <= b:
            for c in range(r, l - 1, -1): order[b][c] = k; k += 1
            b -= 1
        if l <= r:
            for rr in range(b, t - 1, -1): order[rr][l] = k; k += 1
            l += 1
    assert order == [[1, 2, 3, 4], [12, 13, 14, 5], [11, 16, 15, 6], [10, 9, 8, 7]]
    x0, y0, cw, ch = 110, 100, 44, 36
    roles = {(i, j): ("new" if i in (0, 3) or j in (0, 3) else "blank") for i in range(4) for j in range(4)}
    grid(s, x0, y0, order, cw, ch, roles)
    s.t(x0 + 2 * cw, 86, "top = 0", 12, INK, "middle", 500)
    s.t(x0 + 2 * cw, y0 + 4 * ch + 14, "bottom = 3", 12, INK, "middle", 500)
    s.t(x0 - 8, y0 + 2 * ch, "left = 0", 12, INK, "end", 500)
    s.t(x0 + 4 * cw + 8, y0 + 2 * ch, "right = 3", 12, INK, "start", 500)
    s.o.append('<rect x="%s" y="%s" width="%s" height="%s" rx="4" fill="none" stroke="#EF9F27" '
               'stroke-width="2.5" stroke-dasharray="6 4"/>' % (x0 + cw - 3, y0 + ch - 3, 2 * cw + 6, 2 * ch + 6))
    s.t(x0 + 2 * cw, y0 + 4 * ch + 36, "收缩 4 次后: top=1 bottom=2 left=1 right=2", 12, SUB, "middle")
    s.t(x0 + 2 * cw, y0 + 4 * ch + 54, "(橙色虚线 = 剩下的 2×2, 同样的 4 步再走一圈)", 12, SUB, "middle")
    xr = 390
    steps = [
        ("① → 走上边 matrix[top][left..right]", "走完 top += 1"),
        ("② ↓ 走右边 matrix[top..bottom][right]", "走完 right -= 1"),
        ("③ ← 走下边 matrix[bottom][right..left]", "先检查 top <= bottom · 走完 bottom -= 1"),
        ("④ ↑ 走左边 matrix[bottom..top][left]", "先检查 left <= right · 走完 left += 1"),
    ]
    y = 104
    for a, bb in steps:
        s.t(xr - 10, y, a, 12, INK, weight=500)
        s.t(xr - 10, y + 18, bb, 12, SUB)
        y += 48
    s.sep(y - 8)
    s.t(xr - 10, y + 10, "为什么要两个守卫: 走完上边 top += 1 后,", 12, SUB)
    s.t(xr - 10, y + 28, "如果只剩 1 行, top 已经 > bottom,", 12, SUB)
    s.t(xr - 10, y + 46, "再走下边就是把同一行倒着重复一遍", 12, SUB)
    s.legend(386, [("new", "这一圈 (先走)"), ("blank", "内层 (后走)")])
    s.h = 400
    s.save()


def fig_spiral_trace():
    res, ent = spiral_steps(SP_M)
    assert res == [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
    rows = ent[:5] + [None]
    assert all(not e["coords"] for e in ent[5:]) and len(ent) == 8
    H = 88 + 6 * 88 + 84
    s = Svg("spiral_trace", H, "Spiral Matrix 运行流程",
            "3x4 矩阵,每走一条边画一行:当前矩阵、边界收缩、加入 res 的元素")
    s.head("matrix 3×4 · 每一行 = 走一条边 · 绿色 = 这一步新走过的格子, 灰色 = 之前走过的, 白色 = 还没走",
           "每走完一条边, 对应边界收缩 1 · 四个边界始终圈着「还没走过」的区域",
           [(40, "走哪条边"), (170, "走完后的矩阵"), (300, "边界收缩"), (480, "本步加入 res")])
    visited = set()
    names = {"top": "① 上边 →", "right": "② 右边 ↓", "bottom": "③ 下边 ←", "left": "④ 左边 ↑"}
    total = 0
    y = 82
    for idx, e in enumerate(rows):
        if e is None:
            coords, vals = [], []
            lab, rng = "右 / 下 / 左边", "全是空或跳过"
            b = ent[7]["b"]
            l1 = "top = 2 > bottom = 1"
            l2 = "top=%d bottom=%d left=%d right=%d" % b
            l3 = "while 条件不成立 → 结束"
        else:
            coords, vals = e["coords"], e["vals"]
            lab, rng = names[e["name"]] + (" (第 2 圈)" if idx == 4 else ""), e["rng"]
            if idx == 4:
                lab = "① 上边 → (第 2 圈)"
            b = e["b"]
            l1 = e["note"] + "  →  %s = %d" % (e["name"], b[{"top": 0, "right": 3, "bottom": 1, "left": 2}[e["name"]]])
            l2 = "top=%d bottom=%d left=%d right=%d" % b
            l3 = ""
        roles = {}
        for (i, j) in visited:
            roles[(i, j)] = "old"
        for c in coords:
            roles[c] = "new"
        # 每格的数字就是 matrix 的值; 没走过的画白色
        grid(s, 170, y + 8, SP_M, 28, 22, {**{(i, j): "blank" for i in range(3) for j in range(4)}, **roles}, size=12)
        s.t(40, y + 22, lab, 14, INK, weight=500)
        s.t(40, y + 42, rng, 12, SUB)
        s.t(300, y + 22, l1, 12, INK, weight=500)
        s.t(300, y + 40, l2, 12, SUB)
        if l3:
            s.t(300, y + 58, l3, 12, SUB)
        total += len(vals)
        if vals:
            s.t(480, y + 22, "  ".join(str(v) for v in vals), 14, ROLE["new"][2], weight=500)
            s.t(480, y + 42, "len(res) = %d" % total, 12, SUB)
        else:
            s.t(480, y + 22, "(没有新元素)", 12, SUB)
            s.t(480, y + 42, "len(res) = %d" % total, 12, SUB)
        visited |= set(coords)
        y += 88
        s.sep(y - 4)
    s.t(40, y + 14, "最终: res = [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]  (12 个 = 3 × 4, 每格恰好走一次)", 14, INK, weight=500)
    s.legend(y + 44, [("new", "本步新走过"), ("old", "之前走过"), ("blank", "还没走")])
    s.save()


# ================================================================ 2. Rotate Image
RM = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


def rotate_steps(mat):
    mat = deepcopy(mat)
    n = len(mat)
    steps = []
    for i in range(n):
        for j in range(i + 1, n):
            a, b = mat[i][j], mat[j][i]
            mat[i][j], mat[j][i] = b, a
            steps.append(dict(kind="swap", i=i, j=j, a=a, b=b, grid=deepcopy(mat)))
    for i, row in enumerate(mat):
        before = row[:]
        row.reverse()
        steps.append(dict(kind="rev", i=i, before=before, after=row[:], grid=deepcopy(mat)))
    return mat, steps


def fig_rotate_core():
    mat, steps = rotate_steps(RM)
    ref = deepcopy(RM)
    load(ROTATE)["rotate"](ref)
    assert mat == ref == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
    tr = [steps[2]["grid"]][0]  # transpose 之后
    assert tr == [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    s = Svg("rotate_core", 372, "Rotate Image 核心", "顺时针旋转 = transpose + 每行 reverse,用坐标变换解释")
    s.t(40, 18, "顺时针 90 度: 原来的 (i, j) 去到 (j, n-1-i)  ·  n = 3")
    s.t(40, 38, "拆成两步: transpose (i, j) → (j, i), 再每行 reverse (j, i) → (j, n-1-i)")
    gx = [50, 295, 540]
    gy = 100
    cw, ch = 30, 26
    mats = [RM, tr, mat]
    caps = ["原矩阵", "transpose 之后", "每行 reverse 之后"]
    for k in range(3):
        roles = {}
        for i in range(3):
            for j in range(3):
                roles[(i, j)] = "old"
        # 跟踪 3 和 2
        for val, ring in ((3, True), (2, False)):
            for i in range(3):
                for j in range(3):
                    if mats[k][i][j] == val:
                        roles[(i, j)] = "new"
                        if ring:
                            pass
        grid(s, gx[k], gy, mats[k], cw, ch, roles, ring={(i, j) for i in range(3) for j in range(3) if mats[k][i][j] == 3})
        s.t(gx[k] + 45, gy - 16, caps[k], 12, INK, "middle", 500)
    pos3 = [(0, 2), (2, 0), (2, 2)]
    pos2 = [(0, 1), (1, 0), (1, 2)]
    for k in range(3):
        i, j = pos3[k]
        assert mats[k][i][j] == 3
        i2, j2 = pos2[k]
        assert mats[k][i2][j2] == 2
        s.t(gx[k] + 45, gy + 3 * ch + 18, "3 在 (%d, %d)" % pos3[k], 12, INK, "middle", 500)
        s.t(gx[k] + 45, gy + 3 * ch + 36, "2 在 (%d, %d)" % pos2[k], 12, SUB, "middle")
    for k, lab in enumerate(["transpose", "reverse"]):
        xa = gx[k] + 3 * cw + 8
        xb = gx[k + 1] - 8
        s.arrow(xa, gy + 39, xb, gy + 39, "g")
    s.t((gx[0] + 90 + gx[1]) / 2, gy + 22, "(i,j)→(j,i)", 12, SUB, "middle")
    s.t((gx[1] + 90 + gx[2]) / 2, gy + 22, "(j,i)→(j,2-i)", 12, SUB, "middle")
    s.sep(gy + 3 * ch + 56)
    y = gy + 3 * ch + 76
    s.t(40, y, "代入验证: 3 在 (0, 2) → transpose → (2, 0) → reverse → (2, 3-1-0) = (2, 2) ✓ 对应 (j, n-1-i) = (2, 2)", 12, INK)
    s.t(40, y + 22, "直觉: 原来的第 i 行 → transpose 变成第 i 列 → reverse 把第 i 列挪到第 n-1-i 列", 12, SUB)
    s.t(40, y + 40, "所以最上面一行 [1, 2, 3] 变成最右边一列 (从上往下读 1, 2, 3)", 12, SUB)
    s.legend(y + 84, [("new", "跟踪的元素 3 / 2"), ("old", "其他")])
    s.h = y + 106
    s.save()


def fig_rotate_trace():
    mat, steps = rotate_steps(RM)
    s = Svg("rotate_trace", 88 + 6 * 88 + 90, "Rotate Image 运行流程",
            "3x3 矩阵:先 transpose 的 3 次 swap,再 3 行 reverse,每步之后的矩阵")
    s.head("n = 3 · 每一行 = 一次操作 · 绿色 = 这一步被改动的格子",
           "第一阶段 transpose: 只换上三角的 3 对 (对角线不动) · 第二阶段: 每行 reverse",
           [(40, "操作"), (210, "操作后的矩阵"), (350, "发生了什么")])
    y = 82
    for k, st in enumerate(steps):
        if st["kind"] == "swap":
            i, j = st["i"], st["j"]
            roles = {(i, j): "new", (j, i): "new"}
            lab, lab2 = "swap (%d,%d) ↔ (%d,%d)" % (i, j, j, i), "transpose · i=%d, j=%d" % (i, j)
            l1 = "matrix[%d][%d] = %d  与  matrix[%d][%d] = %d 交换" % (i, j, st["a"], j, i, st["b"])
            l2 = "→ matrix[%d][%d] = %d, matrix[%d][%d] = %d" % (i, j, st["b"], j, i, st["a"])
        else:
            i = st["i"]
            roles = {(i, j): "new" for j in range(3)}
            lab, lab2 = "reverse 第 %d 行" % i, "row.reverse()"
            l1 = "row %d: %s  →  %s" % (i, st["before"], st["after"])
            l2 = "列 0 ↔ 列 2: (j, i) → (j, n-1-i)"
        grid(s, 210, y + 8, st["grid"], 30, 24, {**{(a, b): "old" for a in range(3) for b in range(3)}, **roles}, size=14)
        s.t(40, y + 26, lab, 14, INK, weight=500)
        s.t(40, y + 46, lab2, 12, SUB)
        s.t(350, y + 28, l1, 12, INK, weight=500)
        if l2:
            s.t(350, y + 48, l2, 12, SUB)
        y += 88
        s.sep(y - 4)
    s.t(40, y + 14, "最终: [[7, 4, 1], [8, 5, 2], [9, 6, 3]]  ·  3 次 swap + 3 次 reverse, 没有开新矩阵", 14, INK, weight=500)
    s.legend(y + 44, [("new", "本步改动"), ("old", "没变")])
    s.save()


# ================================================================ 3. Set Matrix Zeroes
ZM = [[1, 2, 3, 4], [5, 0, 7, 8], [9, 10, 11, 0]]


def zeroes_steps(mat):
    mat = deepcopy(mat)
    m, n = len(mat), len(mat[0])
    st = []
    row0 = any(mat[0][j] == 0 for j in range(n))
    col0 = any(mat[i][0] == 0 for i in range(m))
    st.append(dict(kind="init", grid=deepcopy(mat), row0=row0, col0=col0))
    for i in range(1, m):
        for j in range(1, n):
            if mat[i][j] == 0:
                mat[i][0] = 0
                mat[0][j] = 0
                st.append(dict(kind="flag", at=(i, j), grid=deepcopy(mat)))
    before = deepcopy(mat)
    changed = []
    for i in range(1, m):
        for j in range(1, n):
            if mat[i][0] == 0 or mat[0][j] == 0:
                if mat[i][j] != 0:
                    changed.append((i, j))
                mat[i][j] = 0
    st.append(dict(kind="fill", grid=deepcopy(mat), changed=changed))
    if row0:
        for j in range(n):
            mat[0][j] = 0
    if col0:
        for i in range(m):
            mat[i][0] = 0
    st.append(dict(kind="last", grid=deepcopy(mat), row0=row0, col0=col0))
    return mat, st


def fig_zeroes_core():
    s = Svg("zeroes_core", 360, "Set Matrix Zeroes 核心", "第一行当列 flag,第一列当行 flag,三个阶段的顺序")
    s.t(40, 18, "要记「哪些行 / 列要清零」: 开 rows[m] + cols[n] 要 O(m + n) 空间")
    s.t(40, 38, "借用矩阵自己的第一行 / 第一列当 flag → O(1)")
    x0, y0, cw, ch = 50, 100, 52, 38
    for i in range(3):
        for j in range(4):
            if i == 0 and j == 0:
                s.cell(x0, y0, cw, ch, "★", "blank", ring=True, size=14)
            elif i == 0:
                s.cell(x0 + j * cw, y0, cw, ch, "col %d" % j, "new", size=12)
            elif j == 0:
                s.cell(x0, y0 + i * ch, cw, ch, "row %d" % i, "new", size=12)
            else:
                s.cell(x0 + j * cw, y0 + i * ch, cw, ch, "内部", "old", size=12)
    s.t(x0, y0 - 18, "matrix[0][j] = 第 j 列要不要清零", 12, INK, weight=500)
    s.t(x0, y0 + 3 * ch + 16, "matrix[i][0] = 第 i 行要不要清零 (最左一列)", 12, INK, weight=500)
    xr = 300
    y = 98
    items = [
        ("① 先记 row0 / col0", "第一行 / 第一列自己原本有没有 0, 因为马上会被当 flag 覆盖"),
        ("② pass 1: 扫内部 (i ≥ 1, j ≥ 1)", "遇到 0 → matrix[i][0] = 0 和 matrix[0][j] = 0 (留言)"),
        ("③ pass 2: 内部按留言清零", "matrix[i][0] == 0 或 matrix[0][j] == 0 → 这格清零"),
        ("④ 最后才处理第一行 / 第一列", "row0 为真 → 整个第一行清零; col0 为真 → 整个第一列清零"),
    ]
    for a, b in items:
        s.t(xr, y, a, 14, INK, weight=500)
        s.t(xr, y + 20, b, 12, SUB)
        y += 50
    s.sep(y)
    s.t(40, y + 20, "顺序不能错: 留言区 (第一行 / 第一列) 在 pass 2 里还要被读, 所以必须最后才清零;", 12, SUB)
    s.t(40, y + 38, "★ matrix[0][0] 在 pass 1 里不会被写 (循环从 1 开始); 第一行 / 第一列「原本有没有 0」由 row0 / col0 单独记", 12, SUB)
    s.legend(y + 66, [("new", "flag 区 (留言)"), ("old", "内部"), ("ring", "matrix[0][0]")])
    s.h = y + 88
    s.save()


def fig_zeroes_trace():
    mat, st = zeroes_steps(ZM)
    ref = deepcopy(ZM)
    load(ZEROES)["setZeroes"](ref)
    assert mat == ref == [[1, 0, 3, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    assert [x["kind"] for x in st] == ["init", "flag", "flag", "fill", "last"]
    assert st[0]["row0"] is False and st[0]["col0"] is False
    s = Svg("zeroes_trace", 88 + 5 * 92 + 90, "Set Matrix Zeroes 运行流程",
            "3x4 矩阵,两个内部 0 先在第一行第一列留言,再按留言清零")
    s.head("matrix 3×4 · 内部 (i ≥ 1, j ≥ 1) 有两个 0: (1,1) 和 (2,3)",
           "绿色 = 这一步写下的留言 · 红色 = 被清零的格子 · 橙圈 = 当前扫到的 0",
           [(40, "阶段"), (200, "之后的矩阵"), (340, "发生了什么")])
    rows = []
    g0 = st[0]
    rows.append(("① 起手", "row0 / col0", g0["grid"], {}, set(),
                 ["row0 = any(第一行 == 0) = False", "col0 = any(第一列 == 0) = False", "→ 第一行 / 第一列原本都没有 0"]))
    f1 = st[1]
    rows.append(("② pass 1", "扫到 (1,1) = 0", f1["grid"], {(1, 0): "new", (0, 1): "new"}, {(1, 1)},
                 ["matrix[1][1] == 0", "→ matrix[1][0] = 0   (留言: 第 1 行清零)", "→ matrix[0][1] = 0   (留言: 第 1 列清零)"]))
    f2 = st[2]
    rows.append(("② pass 1", "扫到 (2,3) = 0", f2["grid"], {(2, 0): "new", (0, 3): "new"}, {(2, 3)},
                 ["matrix[2][3] == 0", "→ matrix[2][0] = 0   (留言: 第 2 行清零)", "→ matrix[0][3] = 0   (留言: 第 3 列清零)"]))
    fl = st[3]
    ch = {c: "gone" for c in fl["changed"]}
    assert sorted(fl["changed"]) == [(1, 2), (1, 3), (2, 1), (2, 2)]
    rows.append(("③ pass 2", "内部按留言清零", fl["grid"], ch, set(),
                 ["内部 6 格里 matrix[i][0] == 0 (i = 1, 2)", "→ 全清零, 其中 4 格本来非 0 (红)", "(1,1) 和 (2,3) 本来就是 0"]))
    la = st[4]
    rows.append(("④ 最后", "第一行 / 第一列", la["grid"], {}, set(),
                 ["row0 = False → 第一行不整行清零", "col0 = False → 第一列不整列清零", "留言区原样保留: 第一行 = [1, 0, 3, 0]"]))
    y = 82
    for lab, lab2, g, roles, rg, lines in rows:
        full = {(a, b): "old" for a in range(3) for b in range(4)}
        full.update(roles)
        grid(s, 200, y + 10, g, 30, 24, full, size=14, ring=rg)
        s.t(40, y + 26, lab, 14, INK, weight=500)
        s.t(40, y + 46, lab2, 12, SUB)
        for k, ln in enumerate(lines):
            s.t(340, y + 18 + k * 20, ln, 12, INK if k == 0 else SUB, weight=500 if k == 0 else 400)
        y += 92
        s.sep(y - 4)
    s.t(40, y + 14, "最终: [[1, 0, 3, 0], [0, 0, 0, 0], [0, 0, 0, 0]]  ·  额外空间只有 row0 / col0 两个 bool", 14, INK, weight=500)
    s.legend(y + 44, [("new", "写下的留言"), ("gone", "被清零"), ("old", "其他"), ("ring", "当前扫到的 0")])
    s.save()


# ================================================================ 4. Pow(x, n)
def pow_steps(x, n):
    res = 1.0
    out = []
    while n:
        n0, x0, r0 = n, x, res
        bit = n & 1
        if bit:
            res *= x
        x *= x
        n >>= 1
        out.append(dict(n0=n0, bit=bit, x0=x0, r0=r0, res=res, x1=x, n1=n))
    return res, out


def fig_pow_core():
    s = Svg("pow_core", 360, "Pow(x, n) 核心", "n=10 的二进制拆分:x^10 = x^8 * x^2,每个 bit 对应一个 x 的 2^k 次方")
    s.t(40, 18, "x^10 = 10 个 x 连乘, 9 次乘法 · 但 10 = 8 + 2 (二进制 1010), 所以 x^10 = x^8 × x^2")
    s.t(40, 38, "x^1 → x^2 → x^4 → x^8 每个只需把前一个平方一次 · 用哪几个 = n 的哪几个 bit 是 1")
    cw = 18
    bx = 180
    y = 70
    s.t(40, y + 4, "n 的 bit", 12, INK, weight=500)
    s.t(bx, y + 4, "x 的几个相乘 (每格 = 一个 x)", 12, INK, weight=500)
    y += 28
    # bit k = 0..3
    bit_of = lambda k: (10 >> k) & 1
    for k in range(4):
        cnt = 2 ** k
        used = bit_of(k) == 1
        role = "new" if used else "old"
        s.t(40, y + 14, "bit %d = %d" % (k, bit_of(k)), 14, INK, weight=500)
        s.t(110, y + 14, "x^%d" % cnt, 12, SUB)
        for c in range(cnt):
            s.cell(bx + c * cw, y, cw - 2, 28, "", role, rx=3)
        s.t(bx + cnt * cw + 8, y + 14, "bit = 1 → 乘进答案" if used else "bit = 0 → 跳过", 12, ROLE[role][2])
        y += 40
    s.sep(y - 4)
    s.t(40, y + 14, "n = 10 = 8 + 2  →  x^10 = x^8 × x^2", 14, INK, weight=500)
    s.t(40, y + 38, "平方 4 次 (bit 数 = log2(10) 向上取整 = 4), 乘 2 次 (1 的个数) · 总共 O(log n), 不是 O(n)", 12, SUB)
    s.t(40, y + 56, "n 是负数: x^(-n) = (1/x)^n, 先把 x 取倒数再把 n 变成正数", 12, SUB)
    s.legend(y + 84, [("new", "该 bit = 1, 乘进答案"), ("old", "该 bit = 0, 跳过")])
    s.h = y + 108
    s.save()


def fig_pow_trace():
    r, steps = pow_steps(2.0, 10)
    ref = load(POW)["myPow"](2.0, 10)
    assert r == ref == 1024.0 and len(steps) == 4
    assert [(t["n0"], t["bit"], t["x0"], t["res"], t["x1"], t["n1"]) for t in steps] == [
        (10, 0, 2.0, 1.0, 4.0, 5), (5, 1, 4.0, 4.0, 16.0, 2), (2, 0, 16.0, 4.0, 256.0, 1), (1, 1, 256.0, 1024.0, 65536.0, 0)]
    s = Svg("pow_trace", 88 + 4 * 92 + 120, "Pow(x, n) 运行流程", "x=2, n=10:每轮看 n 的最低位,是 1 就乘进 res,然后 x 平方、n 右移")
    s.head("x = 2, n = 10 · 每一轮: 看 n 的最低位 → 是 1 才 res *= x → x 平方 → n 右移一位",
           "res 从 1 开始 · 每轮开始时 x = 2^(2^k) (k = 第几轮, 从 0 数)",
           [(40, "这一轮开始时的 n"), (190, "最低位 n & 1"), (320, "res"), (480, "x 平方 · n 右移")])
    y = 82
    for k, t in enumerate(steps):
        nb = bits(t["n0"], 4)
        for q, ch in enumerate(nb):
            last = q == 3
            s.cell(40 + q * 26, y + 10, 24, 28, ch, "new" if t["bit"] and last else "old", ring=last, size=14)
        s.t(40, y + 56, "n = %d = %s (二进制)" % (t["n0"], nb.lstrip("0") or "0"), 12, SUB)
        s.t(190, y + 24, "n & 1 = %d" % t["bit"], 14, INK, weight=500)
        s.t(190, y + 44, "是 1: res *= x" if t["bit"] else "是 0: 跳过", 12, SUB)
        if t["bit"]:
            s.t(320, y + 24, "res = %d × %d = %d" % (t["r0"], t["x0"], t["res"]), 14, ROLE["new"][2], weight=500)
            s.t(320, y + 44, "x = %d 是 2^%d" % (t["x0"], 2 ** k), 12, SUB)
        else:
            s.t(320, y + 24, "res = %d (不变)" % t["res"], 14, INK, weight=500)
            s.t(320, y + 44, "x = %d 是 2^%d, 不用" % (t["x0"], 2 ** k), 12, SUB)
        s.t(480, y + 24, "x = %d × %d = %d" % (t["x0"], t["x0"], t["x1"]), 14, INK, weight=500)
        s.t(480, y + 44, "n >>= 1  →  n = %d" % t["n1"], 12, SUB)
        y += 92
        s.sep(y - 4)
    s.t(40, y + 14, "n = 0, 循环结束 · res = 1 × 4 × 256 = 1024 = 2^2 × 2^8 = 2^10 ✓", 14, INK, weight=500)
    s.t(40, y + 38, "只循环 4 轮 (10 的二进制有 4 位), 暴力要 10 次乘法 · n = 10^9 时是 30 轮 vs 10^9 次", 12, SUB)
    s.legend(y + 68, [("new", "最低位 = 1, 乘进 res"), ("old", "n 的其他 bit"), ("ring", "当前看的最低位")])
    s.h = y + 90
    s.save()


# ================================================================ 5. Palindrome Number
def palin_steps(x0):
    x, rev = x0, 0
    out = []
    while x > rev:
        xb, rb = x, rev
        dgt = x % 10
        rev = rev * 10 + dgt
        x //= 10
        out.append(dict(xb=xb, rb=rb, d=dgt, rev=rev, x=x))
    final = dict(x=x, rev=rev, eq=(x == rev), eq2=(x == rev // 10), res=(x == rev or x == rev // 10))
    return out, final


def digs(n):
    return list(str(n))


def fig_palin_core():
    s = Svg("palin_core", 392, "Palindrome Number 核心", "只反转后半部分:x 和 rev 相遇时停,奇数位时 rev 多一位中间数")
    s.t(40, 18, "整个数反转: 位数多时可能溢出 (如 Reverse Integer 要检查 32-bit)· 回文只需要反转「后一半」")
    s.t(40, 38, "x % 10 取末位, 接到 rev 的末尾; x // 10 丢掉末位 · 循环到 x <= rev 就是转完一半了")
    cw, ch = 40, 32
    # 奇数
    y = 70
    s.t(40, y + 16, "x = 12321", 14, INK, weight=500)
    s.t(40, y + 36, "奇数位", 12, SUB)
    for q, c in enumerate(digs(12321)):
        s.cell(150 + q * cw, y, cw - 4, ch, c, "old" if q < 2 else "new", ring=(q == 2))
    s.t(150 + 5 * cw + 10, y + 8, "前 2 位留在 x", 12, ROLE["old"][2])
    s.t(150 + 5 * cw + 10, y + 26, "后 3 位 (含中间的 3) 移进 rev", 12, ROLE["new"][2])
    y += 60
    s.t(40, y + 16, "停下时:", 12, SUB)
    s.t(110, y + 16, "x =", 14, INK, weight=500)
    for q, c in enumerate(digs(12)):
        s.cell(150 + q * cw, y, cw - 4, ch, c, "old")
    s.t(150 + 3 * cw, y + 16, "rev =", 14, INK, weight=500)
    for q, c in enumerate(digs(123)):
        s.cell(230 + 3 * cw // 2 + q * cw + 24, y, cw - 4, ch, c, "new")
    xr = 230 + 3 * cw // 2 + 3 * cw + 36
    s.t(xr, y + 8, "rev 多了中间数 3", 12, SUB)
    s.t(xr, y + 26, "x == rev // 10 → 12 == 12 ✓", 12, INK, weight=500)
    s.sep(y + 50)
    # 偶数
    y += 66
    s.t(40, y + 16, "x = 1221", 14, INK, weight=500)
    s.t(40, y + 36, "偶数位", 12, SUB)
    for q, c in enumerate(digs(1221)):
        s.cell(150 + q * cw, y, cw - 4, ch, c, "old" if q < 2 else "new")
    s.t(150 + 4 * cw + 10, y + 8, "前 2 位留在 x", 12, ROLE["old"][2])
    s.t(150 + 4 * cw + 10, y + 26, "后 2 位移进 rev", 12, ROLE["new"][2])
    y += 60
    s.t(40, y + 16, "停下时:", 12, SUB)
    s.t(110, y + 16, "x =", 14, INK, weight=500)
    for q, c in enumerate(digs(12)):
        s.cell(150 + q * cw, y, cw - 4, ch, c, "old")
    s.t(150 + 3 * cw, y + 16, "rev =", 14, INK, weight=500)
    for q, c in enumerate(digs(12)):
        s.cell(230 + 3 * cw // 2 + q * cw + 24, y, cw - 4, ch, c, "new")
    s.t(xr, y + 16, "x == rev → 12 == 12 ✓", 12, INK, weight=500)
    s.sep(y + 50)
    y += 66
    s.t(40, y, "rev 里是后半段倒过来的 · 回文 ⟺ 前半段 == 倒过来的后半段 · 位数一半, 也不会溢出", 12, SUB)
    s.t(40, y + 20, "边界: 负数不是回文; 末位是 0 的数 (如 10, 120) 反过来会有前导 0, 只有 0 本身是回文", 12, SUB)
    s.legend(y + 48, [("old", "留在 x 的前半"), ("new", "移进 rev 的后半")])
    s.h = y + 70
    s.save()


def fig_palin_trace():
    s1, f1 = palin_steps(12321)
    s2, f2 = palin_steps(1221)
    assert [(a["d"], a["rev"], a["x"]) for a in s1] == [(1, 1, 1232), (2, 12, 123), (3, 123, 12)]
    assert f1["res"] and f1["eq2"] and not f1["eq"]
    assert [(a["d"], a["rev"], a["x"]) for a in s2] == [(1, 1, 122), (2, 12, 12)] and f2["eq"]
    f = load(PALIN)["isPalindrome"]
    assert f(12321) and f(1221)
    H = 82 + 4 * 70 + 36 + 3 * 70 + 100
    s = Svg("palin_trace", H, "Palindrome Number 运行流程", "x=12321 和 x=1221 两个例子,每轮取末位接到 rev、x 丢掉末位")
    s.head("每一轮: 取走 x 的末位 d → 接到 rev 末尾 → x 丢掉末位 · 循环条件 x > rev",
           "红色 = x 里被取走的末位 · 绿色 = rev 里新接上的数字",
           [(40, "while x > rev ?"), (170, "x (红 = 要取走的末位)"), (320, "rev (绿 = 新接的)"), (440, "公式")])
    y = 82

    def block(title, steps, fin, x0):
        nonlocal y
        s.t(40, y + 6, title, 14, INK, weight=500)
        y += 22
        for st in steps:
            ds = digs(st["xb"])
            for q, c in enumerate(ds):
                s.cell(170 + q * 24, y + 8, 22, 26, c, "gone" if q == len(ds) - 1 else "old", size=14)
            rs = digs(st["rev"])
            for q, c in enumerate(rs):
                s.cell(320 + q * 24, y + 8, 22, 26, c, "new" if q == len(rs) - 1 else "old", size=14)
            s.t(40, y + 14, "%d > %d ✓ 进入" % (st["xb"], st["rb"]), 12, INK, weight=500)
            s.t(40, y + 32, "还没转到一半", 12, SUB)
            s.t(440, y + 8, "d = %d %% 10 = %d" % (st["xb"], st["d"]), 12, INK, weight=500)
            s.t(440, y + 24, "rev = %d × 10 + %d = %d" % (st["rb"], st["d"], st["rev"]), 12, INK)
            s.t(440, y + 40, "x = %d // 10 = %d" % (st["xb"], st["x"]), 12, INK)
            y += 58
            s.sep(y - 6)
        # 停止行
        s.t(40, y + 14, "%d > %d ? 否 → 停" % (fin["x"], fin["rev"]), 12, INK, weight=500)
        for q, c in enumerate(digs(fin["x"])):
            s.cell(170 + q * 24, y + 4, 22, 26, c, "old", size=14)
        for q, c in enumerate(digs(fin["rev"])):
            s.cell(320 + q * 24, y + 4, 22, 26, c, "old", size=14)
        if fin["eq"]:
            s.t(440, y + 8, "x == rev → %d == %d ✓" % (fin["x"], fin["rev"]), 12, INK, weight=500)
            s.t(440, y + 26, "偶数位 · 返回 True", 12, SUB)
        else:
            s.t(440, y + 8, "x == rev ? %d ≠ %d" % (fin["x"], fin["rev"]), 12, SUB)
            s.t(440, y + 26, "x == rev // 10 ? %d == %d ✓" % (fin["x"], fin["rev"] // 10), 12, INK, weight=500)
            s.t(440, y + 44, "奇数位 · 返回 True", 12, SUB)
        y += 62
        s.sep(y - 6)
    block("x = 12321  (奇数位)", s1, f1, 12321)
    block("x = 1221  (偶数位)", s2, f2, 1221)
    s.t(40, y + 12, "Reverse Integer 同一套: rev = rev * 10 + x % 10 反转整个数, 额外检查 32-bit 溢出和符号", 12, SUB)
    s.t(40, y + 32, "最终: isPalindrome(12321) = True, isPalindrome(1221) = True", 14, INK, weight=500)
    s.legend(y + 62, [("gone", "x 被取走的末位"), ("new", "rev 新接的数字"), ("old", "其他")])
    s.h = y + 84
    s.save()


# ================================================================ 6. XOR
def xor_steps_single(nums):
    res = 0
    out = []
    for x in nums:
        r0 = res
        res ^= x
        out.append(dict(x=x, val=x, r0=r0, r1=res))
    return res, out


def xor_steps_missing(nums):
    res = len(nums)
    out = [dict(i=None, x=None, val=None, r0=None, r1=res)]
    for i, x in enumerate(nums):
        r0 = res
        res ^= i ^ x
        out.append(dict(i=i, x=x, val=i ^ x, r0=r0, r1=res))
    return res, out


def fig_xor_core():
    s = Svg("xor_core", 420, "XOR 核心", "a^a=0 让成对出现的数抵消,Single Number 与 Missing Number 都是配对后落单")
    s.t(40, 18, "XOR 三条性质:  a ^ a = 0  ·  a ^ 0 = a  ·  a ^ b = b ^ a (顺序无所谓, 也满足结合律)")
    s.t(40, 38, "所以一串数 XOR 起来, 出现两次的互相抵消成 0, 只剩落单的")
    cw = 52
    y = 70
    s.t(40, y, "Single Number: nums = [4, 1, 2, 1, 2]", 14, INK, weight=500)
    y += 20
    vals = [4, 1, 2, 1, 2]
    x0 = 90
    for q, v in enumerate(vals):
        role = "new" if v == 4 else "gone"
        s.cell(x0 + q * cw, y, cw - 8, 34, v, role, ring=(v == 4))
    # 弧线: 1(1)-1(3) 低, 2(2)-2(4) 高
    def cx(q):
        return x0 + q * cw + (cw - 8) / 2
    s.path("M%s %s Q%s %s %s %s" % (cx(1), y + 34, (cx(1) + cx(3)) / 2, y + 50, cx(3), y + 34), "r", dash=True, arrow=False)
    s.path("M%s %s Q%s %s %s %s" % (cx(2), y + 34, (cx(2) + cx(4)) / 2, y + 90, cx(4), y + 34), "r", dash=True, arrow=False)
    s.t(x0 + 5 * cw + 10, y + 10, "1 ^ 1 = 0", 12, ROLE["gone"][2], weight=500)
    s.t(x0 + 5 * cw + 10, y + 28, "2 ^ 2 = 0", 12, ROLE["gone"][2], weight=500)
    s.t(x0 + 5 * cw + 10, y + 50, "4 落单 → 答案", 12, ROLE["new"][2], weight=500)
    y += 80
    s.t(40, y, "4 ^ 1 ^ 2 ^ 1 ^ 2  =  4 ^ (1 ^ 1) ^ (2 ^ 2)  =  4 ^ 0 ^ 0  =  4", 14, INK, weight=500)
    y += 26
    s.sep(y)
    y += 20
    s.t(40, y, "Missing Number: nums = [3, 0, 1] (应该是 0..3, 缺一个) · res = n ^ (0^3) ^ (1^0) ^ (2^1)", 14, INK, weight=500)
    y += 26
    # 按数值对齐的四列 0 1 2 3
    colx = lambda v: 200 + v * 56
    for v in range(4):
        s.t(colx(v) + 22, y, "数值 %d" % v, 12, SUB, "middle")
    y += 14
    rows = [("n = len(nums) = 3", [3]), ("下标 i = 0..n-1", [0, 1, 2]), ("nums 里的值 x", [3, 0, 1])]
    for lab, vs in rows:
        s.t(40, y + 15, lab, 12, INK, weight=500)
        for v in vs:
            alone = (v == 2)
            s.cell(colx(v), y, 44, 30, v, "new" if alone else "gone", ring=alone)
        y += 38
    s.t(colx(3) + 70, y - 76, "0, 1, 3 各出现两次 → 抵消", 12, ROLE["gone"][2], weight=500)
    s.t(colx(3) + 70, y - 58, "2 只出现一次 → 剩下 = 缺的数", 12, ROLE["new"][2], weight=500)
    s.t(40, y + 14, "同样思路的另一种写法: n*(n+1)//2 - sum(nums) · 差别: XOR 不会溢出 (别的语言), 且「落单」的思路可迁移", 12, SUB)
    s.legend(y + 44, [("gone", "成对 → 抵消成 0"), ("new", "落单 = 答案")])
    s.h = y + 66
    s.save()


def fig_xor_trace():
    r1, a = xor_steps_single([4, 1, 2, 1, 2])
    r2, b = xor_steps_missing([3, 0, 1])
    ns = load(XOR)
    assert r1 == ns["singleNumber"]([4, 1, 2, 1, 2]) == 4
    assert r2 == ns["missingNumber"]([3, 0, 1]) == 2
    assert [t["r1"] for t in a] == [4, 5, 7, 6, 4] and [t["r1"] for t in b] == [3, 0, 1, 2]
    H = 82 + 30 + 5 * 42 + 30 + 4 * 42 + 100
    s = Svg("xor_trace", H, "XOR 运行流程", "Single Number [4,1,2,1,2] 和 Missing Number [3,0,1],res 用 3 位二进制画出")
    s.head("res 用 3 位二进制画 (最左 = 4 那一位) · 每一步 res ^= 右边的数: 对应位相同 → 0, 不同 → 1",
           "绿色 = 这个数里为 1 的位 (会翻转 res 的对应位)",
           [(40, "读入"), (150, "要异或的数"), (236, "res 之前"), (326, "res 之后"), (440, "说明")])

    def rowdraw(y, lab, val, r0, r1, note, note2=""):
        s.t(40, y + 16, lab, 12, INK, weight=500)
        if val is not None:
            for q, ch in enumerate(bits(val, 3)):
                s.cell(150 + q * 22, y + 3, 20, 26, ch, "new" if ch == "1" else "blank", size=14)
            s.t(150 + 3 * 22 + 4, y + 16, "^", 14, SUB)
        if r0 is not None:
            for q, ch in enumerate(bits(r0, 3)):
                s.cell(236 + q * 22, y + 3, 20, 26, ch, "old", size=14)
            s.t(236 + 3 * 22 + 4, y + 16, "=", 14, SUB)
        flipped = (val or 0)
        for q, ch in enumerate(bits(r1, 3)):
            on = bool(flipped & (1 << (2 - q)))
            s.cell(326 + q * 22 + (0 if r0 is not None else 0), y + 3, 20, 26, ch, "new" if on else "old", size=14)
        s.t(440, y + 10, note, 12, INK, weight=500)
        if note2:
            s.t(440, y + 26, note2, 12, SUB)
    y = 82
    s.t(40, y + 8, "Single Number · nums = [4, 1, 2, 1, 2]", 14, INK, weight=500)
    y += 24
    seen = set()
    for t in a:
        again = t["x"] in seen
        seen.add(t["x"])
        rowdraw(y, "x = %d" % t["x"], t["x"], t["r0"], t["r1"], "res = %d ^ %d = %d" % (t["r0"], t["x"], t["r1"]),
                "%d 第 2 次出现 → 抵消" % t["x"] if again else "%d 第 1 次出现" % t["x"])
        y += 42
        s.sep(y - 5)
    s.t(40, y + 10, "返回 res = 4", 14, INK, weight=500)
    y += 34
    s.sep(y - 5)
    s.t(40, y + 8, "Missing Number · nums = [3, 0, 1], n = 3", 14, INK, weight=500)
    y += 24
    for k, t in enumerate(b):
        if k == 0:
            rowdraw(y, "起手", None, None, t["r1"], "res = len(nums) = 3", "n 先放进来 (下标只到 n-1)")
        else:
            rowdraw(y, "i=%d, x=%d" % (t["i"], t["x"]), t["val"], t["r0"], t["r1"],
                    "res = %d ^ (%d ^ %d) = %d" % (t["r0"], t["i"], t["x"], t["r1"]),
                    "i ^ x = %d ^ %d = %d" % (t["i"], t["x"], t["val"]))
        y += 42
        s.sep(y - 5)
    s.t(40, y + 10, "返回 res = 2 (0b010) · 0..3 里缺的就是 2", 14, INK, weight=500)
    s.legend(y + 40, [("new", "为 1 的位 / 被翻转"), ("old", "res 其他位"), ("blank", "为 0 的位")])
    s.h = y + 62
    s.save()


# ================================================================ 7. Number of 1 Bits
def bits_steps(n):
    cnt = 0
    out = []
    while n:
        nb = n
        n &= n - 1
        cnt += 1
        out.append(dict(n=nb, m=nb - 1, r=n, cnt=cnt))
    return cnt, out


def fig_bits_core():
    s = Svg("bits_core", 392, "n & (n-1) 核心", "n-1 把最低位的 1 变 0、右边的 0 变 1,与 n 相与后最低位 1 消失")
    s.t(40, 18, "n - 1 对 n 做了什么: 最低位的那个 1 变 0, 它右边的 0 全变 1, 左边完全不变")
    s.t(40, 38, "所以 n & (n-1): 左边相同的位原样保留, 最低位的 1 及右边全是 (1 & 0) 或 (0 & 1) = 0")
    cw, ch = 44, 34
    x0 = 190
    n, m = 44, 43
    for q in range(6):
        s.t(x0 + q * cw + cw / 2 - 2, 70, "bit %d" % (5 - q), 12, SUB, "middle")
    rows = [("n = 44", bits(n, 6)), ("n - 1 = 43", bits(m, 6)), ("n & (n - 1) = 40", bits(n & m, 6))]
    y = 84
    for k, (lab, b) in enumerate(rows):
        s.t(40, y + 17, lab, 14, INK, weight=500)
        for q, c in enumerate(b):
            if k == 0:
                role = "gone" if q == 3 else ("old" if q < 3 and c == "1" else "blank")
            elif k == 1:
                role = "new" if q >= 3 else ("old" if c == "1" else "blank")
            else:
                role = "gone" if q == 3 else ("old" if c == "1" else "blank")
            s.cell(x0 + q * cw, y, cw - 4, ch, c, role, ring=(k == 0 and q == 3))
        y += 54
    assert bits(n, 6) == "101100" and bits(m, 6) == "101011" and bits(n & m, 6) == "101000"
    s.t(x0 + 6 * cw + 6, 84 + 17, "← 最低位的 1 (bit 2)", 12, ROLE["gone"][2], weight=500)
    s.t(x0 + 6 * cw + 6, 84 + 54 + 17, "← bit 2 变 0, bit 1,0 变 1", 12, ROLE["new"][2], weight=500)
    s.t(x0 + 6 * cw + 6, 84 + 108 + 17, "← 这个 1 消失了", 12, ROLE["gone"][2], weight=500)
    y += 6
    s.sep(y)
    items = [
        "数 1 的个数: 每轮 n &= n - 1 消掉一个 1, 循环次数 = 1 的个数 (<= 32), 不是固定 32 轮",
        "n & (n - 1) == 0  →  n 只有一个 1  →  n 是 2 的幂 (n > 0)",
        "n & -n  →  只留下最低位的 1 (如 44 & -44 = 4)",
        "Python: bin(n).count(\"1\") 或 n.bit_count() (3.10+) 面试里先写 n &= n - 1 的版本",
    ]
    assert 44 & -44 == 4
    for k, it in enumerate(items):
        s.t(40, y + 20 + k * 20, it, 12, SUB if k else INK, weight=400 if k else 500)
    y += 20 + len(items) * 20 + 12
    s.legend(y, [("gone", "最低位的 1 (被消掉)"), ("new", "被翻转的位"), ("old", "不变的 1")])
    s.h = y + 24
    s.save()


def fig_bits_trace():
    cnt, steps = bits_steps(44)
    assert cnt == 3 == load(BITS)["hammingWeight"](44)
    assert [(t["n"], t["m"], t["r"]) for t in steps] == [(44, 43, 40), (40, 39, 32), (32, 31, 0)]
    H = 82 + 3 * 70 + 70 + 100
    s = Svg("bits_trace", H, "Number of 1 Bits 运行流程", "n=44 (101100) 三轮 n &= n-1,每轮消掉最低位的 1")
    s.head("n = 44 = 0b101100 · 每一轮: n &= n - 1 (消掉最低位的 1), cnt += 1",
           "红色 = n 里最低位的 1 (这一轮要消掉的) · 绿色 = n - 1 里被翻转的位",
           [(40, "n"), (206, "n - 1"), (372, "n & (n - 1) = 新 n"), (540, "cnt")])
    y = 82
    for t in steps:
        nb, mb, rb = bits(t["n"], 6), bits(t["m"], 6), bits(t["r"], 6)
        low = max(q for q, c in enumerate(nb) if c == "1")
        for q in range(6):
            s.cell(40 + q * 24, y + 8, 22, 28, nb[q], "gone" if q == low else ("old" if nb[q] == "1" else "blank"), size=14)
            s.cell(206 + q * 24, y + 8, 22, 28, mb[q], "new" if q >= low else ("old" if mb[q] == "1" else "blank"), size=14)
            s.cell(372 + q * 24, y + 8, 22, 28, rb[q], "gone" if q == low else ("old" if rb[q] == "1" else "blank"), size=14)
        s.t(40 + 72, y + 52, "n = %d" % t["n"], 12, SUB, "middle")
        s.t(206 + 72, y + 52, "n - 1 = %d" % t["m"], 12, SUB, "middle")
        s.t(372 + 72, y + 52, "%d & %d = %d" % (t["n"], t["m"], t["r"]), 12, SUB, "middle")
        s.t(190, y + 22, "&", 14, SUB, "middle")
        s.t(356, y + 22, "=", 14, SUB, "middle")
        s.t(540, y + 14, "cnt = %d" % t["cnt"], 14, INK, weight=500)
        s.t(540, y + 34, "消掉 bit %d" % (5 - low), 12, SUB)
        y += 70
        s.sep(y - 6)
    s.t(40, y + 10, "n = 0 → 循环结束, 返回 cnt = 3 · 44 = 0b101100 里确实有 3 个 1 ✓", 14, INK, weight=500)
    s.t(40, y + 34, "只转 3 轮 = 1 的个数; 逐位检查 (n & 1; n >>= 1) 要转 6 轮 (所有 bit)", 12, SUB)
    s.legend(y + 62, [("gone", "最低位的 1 (消掉)"), ("new", "n - 1 里翻转的位"), ("old", "不变的 1"), ("blank", "0")])
    s.h = y + 84
    s.save()


# ================================================================ 8. Minimum Absolute Difference
MD = [8, 1, 12, 5, 10, 9]


def mindiff_steps(arr):
    arr = sorted(arr)
    best, res = float("inf"), []
    out = []
    for k, (a, b) in enumerate(zip(arr, arr[1:])):
        diff = b - a
        old = best
        if diff < best:
            best, res = diff, [[a, b]]
            act = "reset"
        elif diff == best:
            res.append([a, b])
            act = "append"
        else:
            act = "skip"
        out.append(dict(k=k, a=a, b=b, diff=diff, old=old, best=best, act=act, res=deepcopy(res)))
    return arr, out, res


def fig_mindiff_core():
    arr, steps, res = mindiff_steps(MD)
    assert res == load(MINDIFF)["minimumAbsDifference"](list(MD)) == [[8, 9], [9, 10]]
    s = Svg("mindiff_core", 420, "排序后只看相邻", "sort 之后任何非相邻的 pair 距离都不小于夹在中间的相邻距离,所以只比较 n-1 对")
    s.t(40, 18, "暴力: 所有 pair 两两比较 = C(6,2) = 15 对, O(n^2)")
    s.t(40, 38, "sort 之后: a < b < c 时 c - a = (b - a) + (c - b) >= b - a, 跨过 b 的 pair 永远不比相邻的更近")
    lo, hi = arr[0], arr[-1]
    px = lambda v: 60 + (v - lo) / (hi - lo) * 560
    yl = 190
    s.line(40, yl, 640, yl, "#B4B2A9", None, 1)
    # 非相邻弧 (1 → 8)
    s.path("M%s %s Q%s %s %s %s" % (px(1), yl - 16, (px(1) + px(8)) / 2, yl - 96, px(8), yl - 16), "r", dash=True)
    s.t((px(1) + px(8)) / 2, yl - 112, "1 → 8:  8 - 1 = 7 = 4 + 3", 12, ROLE["gone"][2], "middle", 500)
    s.t((px(1) + px(8)) / 2, yl - 94, "跨过 5, 一定比 1→5 和 5→8 都长", 12, ROLE["gone"][2], "middle")
    # 相邻弧
    for t in steps:
        xa, xb = px(t["a"]), px(t["b"])
        best = t["diff"] == min(u["diff"] for u in steps)
        s.path("M%s %s Q%s %s %s %s" % (xa, yl + 16, (xa + xb) / 2, yl + 46, xb, yl + 16), "n" if best else "g", arrow=False, w=1.5)
        s.t((xa + xb) / 2, yl + 50, "%d" % t["diff"], 12, ROLE["new"][2] if best else SUB, "middle", 500)
    for v in arr:
        s.cell(px(v) - 16, yl - 14, 32, 28, v, "old", rx=14)
    s.t(40, yl + 80, "相邻距离: 4, 3, 1, 1, 2 · 最小 = 1 (绿色), 有两对", 12, INK, weight=500)
    s.sep(yl + 98)
    y = yl + 120
    s.t(40, y, "通用思想: sort 作为预处理 · 花 O(n log n) 把「谁和谁最近 / 谁和谁冲突」变成「看相邻」", 14, INK, weight=500)
    s.t(40, y + 24, "Meeting Rooms: 按 start 排序, 只检查 intervals[i].start < intervals[i-1].end", 12, SUB)
    s.t(40, y + 42, "Merge Intervals / Closest pair / Valid Triangle: 都是先 sort, 再只看相邻 (或双指针)", 12, SUB)
    s.legend(y + 72, [("old", "sort 后的元素")])
    s.h = y + 96
    s.save()


def fig_mindiff_trace():
    arr, steps, res = mindiff_steps(MD)
    assert [t["act"] for t in steps] == ["reset", "reset", "reset", "append", "skip"]
    assert [t["diff"] for t in steps] == [4, 3, 1, 1, 2]
    assert steps[-1]["res"] == [[8, 9], [9, 10]]
    H = 82 + 5 * 66 + 100
    s = Svg("mindiff_trace", H, "Minimum Absolute Difference 运行流程",
            "arr=[8,1,12,5,10,9] 排序后扫 5 对相邻,best 和 res 的变化")
    s.head("arr = [8, 1, 12, 5, 10, 9]  →  arr.sort()  →  [1, 5, 8, 9, 10, 12]",
           "每一行 = 看一对相邻 (a, b) · diff = b - a · 绿色 = 当前这一对",
           [(40, "当前这一对 (a, b)"), (240, "diff = b - a"), (340, "和 best 比较")])
    y = 82
    for t in steps:
        for q, v in enumerate(arr):
            s.cell(40 + q * 29, y + 8, 27, 28, v, "new" if q in (t["k"], t["k"] + 1) else "old", size=12)
        s.t(40, y + 50, "a = %d, b = %d" % (t["a"], t["b"]), 12, SUB)
        s.t(240, y + 22, "%d - %d = %d" % (t["b"], t["a"], t["diff"]), 14, INK, weight=500)
        old = "inf" if t["old"] == float("inf") else str(t["old"])
        if t["act"] == "reset":
            c1 = "%d < best = %s" % (t["diff"], old)
            c2 = "→ 重置  best = %d, res = %s" % (t["best"], t["res"])
        elif t["act"] == "append":
            c1 = "%d == best = %s" % (t["diff"], old)
            c2 = "→ 追加  res = %s" % (t["res"],)
        else:
            c1 = "%d > best = %s" % (t["diff"], old)
            c2 = "→ 跳过  res 不变"
        s.t(340, y + 14, c1, 12, INK, weight=500)
        s.t(340, y + 34, c2, 12, SUB)
        y += 66
        s.sep(y - 6)
    s.t(40, y + 10, "返回 res = [[8, 9], [9, 10]] · 最小差 = 1", 14, INK, weight=500)
    s.t(40, y + 34, "只比较 5 对 (n - 1), 暴力要 15 对 · 总 time 由 sort 决定: O(n log n)", 12, SUB)
    s.legend(y + 62, [("new", "当前这一对"), ("old", "其他元素")])
    s.h = y + 84
    s.save()


# ================================================================ 9. Roman to Integer
VAL = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def roman_steps(s_):
    total = 0
    out = []
    for i, ch in enumerate(s_):
        right = s_[i + 1] if i + 1 < len(s_) else None
        neg = right is not None and VAL[ch] < VAL[right]
        t0 = total
        total += -VAL[ch] if neg else VAL[ch]
        out.append(dict(i=i, ch=ch, right=right, neg=neg, t0=t0, t1=total))
    return total, out


def fig_roman_core():
    s = Svg("roman_core", 372, "Roman to Integer 核心", "同一个字符的符号由右邻决定:左小右大则减,否则加")
    s.t(40, 18, "查表 + 一遍扫描: 每个字符先当作加上它的值, 唯一的例外是「左边比右边小」→ 减")
    s.t(40, 38, "减法只有 6 种: IV IX XL XC CD CM, 都是「小的紧挨着大的」前面")
    x = 40
    for k, v in VAL.items():
        s.rect(x, 56, 80, 42, "old")
        s.t(x + 40, 71, k, 14, ROLE["old"][2], "middle", 500)
        s.t(x + 40, 88, str(v), 12, ROLE["old"][2], "middle")
        x += 86
    s.sep(116)
    ex = [("VI", [("V", 5, "new", "+5"), ("I", 1, "new", "+1")], "V(5) 不比右邻 I(1) 小 → 加", "5 + 1 = 6"),
          ("IV", [("I", 1, "gone", "-1"), ("V", 5, "new", "+5")], "I(1) < 右邻 V(5): 左小右大 → 减", "-1 + 5 = 4")]
    y = 134
    for name, cells, why, calc in ex:
        s.t(40, y + 18, name, 14, INK, weight=500)
        for q, (ch, v, role, sg) in enumerate(cells):
            s.cell(100 + q * 70, y, 60, 36, "%s  %s" % (ch, sg), role, size=14)
        s.t(260, y + 8, why, 12, INK, weight=500)
        s.t(260, y + 26, calc, 12, SUB)
        y += 54
    s.sep(y)
    s.t(40, y + 20, "为什么只看右邻一个字符: 罗马数字里减法只出现在相邻两个字符之间 (没有 IIV 这种)", 12, SUB)
    s.t(40, y + 40, "最后一个字符没有右邻 → 一定是加", 12, SUB)
    s.legend(y + 68, [("new", "加"), ("gone", "减 (左小右大)"), ("old", "字符表")])
    s.h = y + 90
    s.save()


def fig_roman_trace():
    total, steps = roman_steps("MCMXCIV")
    assert total == load(ROMAN)["romanToInt"]("MCMXCIV") == 1994
    assert [t["t1"] for t in steps] == [1000, 900, 1900, 1890, 1990, 1989, 1994]
    H = 82 + 7 * 52 + 90
    s = Svg("roman_trace", H, "Roman to Integer 运行流程", "MCMXCIV 逐字符,和右邻比较决定加减,total 的变化")
    s.head("s = \"MCMXCIV\" · 每一行 = 一个字符 · 和右邻比: val[ch] < val[右邻] ? 减 : 加",
           "total 从 0 开始, 每一步把「当前字符的值 (加或减)」写成具体算式",
           [(40, "字符 s[i]"), (130, "和右邻比较"), (360, "符号"), (440, "total")])
    y = 82
    for t in steps:
        s.cell(40, y + 8, 40, 32, t["ch"], "gone" if t["neg"] else "new", ring=True, size=14)
        s.t(88, y + 24, "i=%d" % t["i"], 12, SUB)
        if t["right"] is None:
            s.t(130, y + 16, "没有右邻 (最后一个)", 12, INK, weight=500)
            s.t(130, y + 34, "→ 加", 12, SUB)
        else:
            vc, vr = VAL[t["ch"]], VAL[t["right"]]
            s.t(130, y + 16, "%s=%d  vs  右邻 %s=%d" % (t["ch"], vc, t["right"], vr), 12, INK, weight=500)
            s.t(130, y + 34, ("%d < %d 左小右大 → 减" if t["neg"] else "%d >= %d → 加") % (vc, vr), 12, SUB)
        sg = ("-%d" if t["neg"] else "+%d") % VAL[t["ch"]]
        s.cell(360, y + 10, 62, 28, sg, "gone" if t["neg"] else "new", size=14)
        s.t(440, y + 16, "total = %d %s %d" % (t["t0"], "-" if t["neg"] else "+", VAL[t["ch"]]), 12, SUB)
        s.t(440, y + 34, "= %d" % t["t1"], 14, INK, weight=500)
        y += 52
        s.sep(y - 4)
    s.t(40, y + 14, "返回 1994 = 1000 + 900 + 90 + 4  (CM = -100 + 1000, XC = -10 + 100, IV = -1 + 5)", 14, INK, weight=500)
    s.legend(y + 44, [("new", "加"), ("gone", "减"), ("ring", "当前字符")])
    s.h = y + 66
    s.save()


for fn in (fig_intro_core, fig_spiral_core, fig_spiral_trace, fig_rotate_core, fig_rotate_trace, fig_zeroes_core,
           fig_zeroes_trace, fig_pow_core, fig_pow_trace, fig_palin_core, fig_palin_trace, fig_xor_core,
           fig_xor_trace, fig_bits_core, fig_bits_trace, fig_mindiff_core, fig_mindiff_trace, fig_roman_core,
           fig_roman_trace):
    fn()
print("svgs written")
