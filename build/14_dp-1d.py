"""14 · Dynamic Programming (1): 1D DP / Knapsack
运行: cd build && python3 -I 14_dp-1d.py
会先 selftest (所有文档里的代码 exec 后和 brute force 对拍), 再生成 SVG, 最后生成 HTML。
"""
import html
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import doclib as d  # noqa: E402

SLUG = "14-dp-1d"
SVGDIR = os.path.join(d.ROOT, "docs", "svg", SLUG)
os.makedirs(SVGDIR, exist_ok=True)

# ====================================================================
# 一、文档里出现的所有代码 (selftest 会 exec 它们)
# ====================================================================
CODE = {}

CODE["brute"] = '''
def f(n):                           # f(n) = 走到第 n 阶的方法数
    if n <= 1:
        return 1                    # base case: f(0) = f(1) = 1
    return f(n - 1) + f(n - 2)      # 最后一步: 从 n-1 走 1 阶, 或从 n-2 走 2 阶
'''

CODE["memo"] = '''
from functools import cache

@cache                              # 同一个 n 只算一次, 第二次直接查表
def f(n):
    if n <= 1:
        return 1
    return f(n - 1) + f(n - 2)      # 函数体一个字没改, 只加了 @cache
'''

CODE["table"] = '''
def f(n):
    dp = [1] * (n + 1)              # dp[i] 就是 f(i); base: dp[0] = dp[1] = 1
    for i in range(2, n + 1):       # 计算顺序: i 从小到大, 依赖的格子一定已经填好
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
'''

CODE["rolling"] = '''
def f(n):
    a, b = 1, 1                     # a = dp[i-2], b = dp[i-1]; transition 只看前两格
    for _ in range(2, n + 1):
        a, b = b, a + b             # 算出 dp[i], 窗口右移一格; 其余格子再也用不到
    return b                        # O(1) space
'''

CODE["climb"] = '''
def climbStairs(n):
    a, b = 1, 1                     # a = dp[i-2], b = dp[i-1]
    for _ in range(2, n + 1):
        a, b = b, a + b             # dp[i] = dp[i-1] + dp[i-2]
    return b
'''

CODE["rob"] = '''
def rob(nums):
    # dp[i] = 只看 nums[0..i] 时能偷到的最大金额
    # dp[i] = max(dp[i-1],              不偷 i: 直接继承
    #             dp[i-2] + nums[i])    偷 i: i-1 不能偷, 接在 dp[i-2] 后面
    prev2, prev1 = 0, 0             # dp[i-2], dp[i-1]; 把 dp[-2] = dp[-1] = 0 当 base
    for x in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    return prev1
'''

CODE["rob2"] = '''
def rob2(nums):
    if len(nums) == 1:              # 只有一间: 两种切法都是空的, 特判
        return nums[0]
    # 环: nums[0] 和 nums[-1] 相邻, 不能同时偷 -> 至少有一个不偷
    # 不偷最后一间 = 线性 nums[:-1]; 不偷第一间 = 线性 nums[1:]
    return max(rob(nums[:-1]), rob(nums[1:]))
'''

CODE["kadane"] = '''
def maxSubArray(nums):
    cur = best = nums[0]            # cur = 以 nums[i] 结尾 的最大 subarray sum
    for x in nums[1:]:
        cur = max(x, cur + x)       # 重新开始 (只取 x), 或接在 cur 后面; cur < 0 时重开更好
        best = max(best, cur)       # 最优 subarray 一定在某个 i 结束 -> 答案是所有 cur 的最大值
    return best
'''

CODE["prod"] = '''
def maxProduct(nums):
    mx = mn = best = nums[0]        # mx / mn = 以 nums[i] 结尾的最大 / 最小 product
    for x in nums[1:]:
        cands = (x, mx * x, mn * x)  # 重开, 接在 max 后, 接在 min 后 (x < 0 时 min 乘 x 会变 max)
        mx, mn = max(cands), min(cands)   # 两个都用 旧的 mx, mn 算, 所以先算 cands
        best = max(best, mx)
    return best
'''

CODE["stock"] = '''
def maxProfit(prices):
    lo, best = prices[0], 0         # lo = 到目前为止的最低价, best = 到目前为止的最大利润
    for p in prices[1:]:
        best = max(best, p - lo)    # 今天卖: 最佳买入日 = 之前的最低价, 不用再扫描
        lo = min(lo, p)
    return best
'''

CODE["stock_sm"] = '''
def maxProfit_sm(prices):
    hold, cash = -prices[0], 0      # hold: 手上有股票时的最大利润; cash: 没有股票时的最大利润
    for p in prices[1:]:
        hold = max(hold, -p)        # 继续拿着, 或今天买入 (只能买一次, 所以是 -p)
        cash = max(cash, hold + p)  # 继续空仓, 或今天卖出
    return cash
'''

CODE["coin"] = '''
def coinChange(coins, amount):
    INF = float("inf")
    dp = [0] + [INF] * amount       # dp[a] = 凑出 a 最少要几枚; dp[0] = 0, 其余先当不可达
    for a in range(1, amount + 1):  # 计算顺序: a 从小到大
        for c in coins:             # 枚举 "最后一枚" 是哪种 coin
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] != INF else -1
'''

CODE["change"] = '''
def change(amount, coins):
    dp = [1] + [0] * amount         # dp[a] = 凑出 a 的组合数; dp[0] = 1 (什么都不拿算 1 种)
    for c in coins:                 # 外层 coin: 每种 coin 只 "加入" 一次 -> 组合不分顺序
        for a in range(c, amount + 1):   # 内层 正序: 同一种 coin 可以重复用 (unbounded)
            dp[a] += dp[a - c]      # 凑 a = (不用 c 的旧 dp[a]) + (至少用一枚 c: dp[a-c])
    return dp[amount]
'''

CODE["partition"] = '''
def canPartition(nums):
    total = sum(nums)
    if total % 2:                   # 总和是奇数, 不可能平分
        return False
    target = total // 2             # 问题变成: 能不能挑出一些数, 和恰好 = target
    dp = [True] + [False] * target  # dp[c] = 当前处理过的数里, 能不能凑出和 c
    for x in nums:                  # 外层 每个数; 每个数只能用一次 (0/1)
        for c in range(target, x - 1, -1):   # 倒序! dp[c - x] 还是 "没用 x" 的旧值
            dp[c] = dp[c] or dp[c - x]
    return dp[target]
'''

CODE["wordbreak"] = '''
def wordBreak(s, wordDict):
    words = set(wordDict)           # set: 查 s[j:i] 在不在词典里是 O(1) (hash 要 O(长度))
    n = len(s)
    dp = [True] + [False] * n       # dp[i] = s 的前 i 个字符 s[:i] 能不能切成词典里的词; dp[0] = 空串 = True
    for i in range(1, n + 1):
        for j in range(i):          # 枚举 "最后一个词" s[j:i] 从哪里开始
            if dp[j] and s[j:i] in words:    # 前面 s[:j] 能切, 最后一块也是词
                dp[i] = True
                break               # 一种切法就够了
    return dp[n]
'''

CODE["lis"] = '''
def lengthOfLIS(nums):
    dp = [1] * len(nums)            # dp[i] = 以 nums[i] 结尾 的最长递增子序列长度; 至少是它自己
    for i in range(len(nums)):
        for j in range(i):          # 往回看所有 j < i
            if nums[j] < nums[i]:   # nums[i] 可以接在 nums[j] 后面
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)                  # 不一定以最后一个结尾 -> 取所有 dp 的最大值
'''

CODE["lis_fast"] = '''
from bisect import bisect_left

def lengthOfLIS_fast(nums):
    tails = []                      # tails[k] = 长度为 k+1 的递增子序列里, 最小的结尾值 (tails 恒递增)
    for x in nums:
        k = bisect_left(tails, x)   # 第一个 >= x 的位置: x 能接在 tails[k-1] 后面, 同时把 tails[k] 压得更小
        if k == len(tails):
            tails.append(x)
        else:
            tails[k] = x
    return len(tails)
'''


def _wrap_comments(code, limit=74):
    """行太长 (代码 + 行尾注释) 时, 把行尾注释挪到上一行, 避免横向滚动"""
    out = []
    for line in code.split("\n"):
        if "  # " in line and not line.strip().startswith("#"):
            body, _, cm = line.partition("  # ")
            w = sum(1.67 if ord(c) > 0x2E80 else 1 for c in line)
            if w > limit:
                indent = len(body) - len(body.lstrip())
                out.append(" " * indent + "# " + cm.strip())
                out.append(body.rstrip())
                continue
        out.append(line)
    return "\n".join(out)


for _k in list(CODE):
    CODE[_k] = _wrap_comments(CODE[_k])


# ====================================================================
# 二、selftest: 文档里的代码 vs brute force
# ====================================================================
def selftest():
    ns = {}
    for k in ["brute", "memo", "table", "rolling", "climb", "rob", "rob2", "kadane", "prod",
              "stock", "stock_sm", "coin", "change", "partition", "wordbreak", "lis", "lis_fast"]:
        # brute/memo/table/rolling 都叫 f, 分别测
        local = {}
        exec(CODE[k], local)
        ns[k] = local
    for k in ["brute", "memo", "table", "rolling"]:
        for n in range(0, 15):
            assert ns[k]["f"](n) == ns["table"]["f"](n)
    f = ns["table"]["f"]
    for n in range(1, 20):
        assert ns["climb"]["climbStairs"](n) == f(n)
    # 把需要的函数放到同一个全局里 (rob2 用 rob)
    g = {}
    for k in ["rob", "rob2", "kadane", "prod", "stock", "stock_sm", "coin", "change", "partition",
              "wordbreak", "lis", "lis_fast"]:
        exec(CODE[k], g)
    rnd = random.Random(14)

    def subsets(a):
        n = len(a)
        for m in range(1 << n):
            yield [a[i] for i in range(n) if m >> i & 1]

    for _ in range(400):
        n = rnd.randint(1, 9)
        a = [rnd.randint(0, 9) for _ in range(n)]
        # rob: 选的下标不相邻
        best = 0
        for m in range(1 << n):
            if m & (m >> 1):
                continue
            best = max(best, sum(a[i] for i in range(n) if m >> i & 1))
        assert g["rob"](a) == best, a
        # rob2: 环
        if n >= 2:
            best = 0
            for m in range(1 << n):
                if m & (m >> 1) or (m & 1 and m >> (n - 1) & 1):
                    continue
                best = max(best, sum(a[i] for i in range(n) if m >> i & 1))
            assert g["rob2"](a) == best, a
        else:
            assert g["rob2"](a) == a[0]
        b = [rnd.randint(-6, 6) for _ in range(n)]
        assert g["maxSubArray"](b) == max(sum(b[i:j]) for i in range(n) for j in range(i + 1, n + 1))
        def prod(x):
            r = 1
            for v in x:
                r *= v
            return r
        assert g["maxProduct"](b) == max(prod(b[i:j]) for i in range(n) for j in range(i + 1, n + 1)), b
        pr = [rnd.randint(1, 9) for _ in range(n)]
        bf = max([0] + [pr[j] - pr[i] for i in range(n) for j in range(i + 1, n)])
        assert g["maxProfit"](pr) == bf and g["maxProfit_sm"](pr) == bf, pr
        # LIS
        bl = 0
        for sub in subsets(b):
            if all(sub[i] < sub[i + 1] for i in range(len(sub) - 1)):
                bl = max(bl, len(sub))
        assert g["lengthOfLIS"](b) == bl and g["lengthOfLIS_fast"](b) == bl, b
        # partition
        c = [rnd.randint(1, 8) for _ in range(n)]
        ok = any(2 * sum(sub) == sum(c) for sub in subsets(c))
        assert g["canPartition"](c) == ok, c
    for _ in range(300):
        coins = rnd.sample(range(1, 8), rnd.randint(1, 3))
        amount = rnd.randint(0, 14)
        # coin change brute: BFS
        INF = 10 ** 9
        best = [0] + [INF] * amount
        for a in range(1, amount + 1):
            for cc in coins:
                if cc <= a and best[a - cc] + 1 < best[a]:
                    best[a] = best[a - cc] + 1
        exp = best[amount] if best[amount] < INF else -1
        # 递归枚举验证 (不用 dp)
        def rec(a):
            if a == 0:
                return 0
            r = INF
            for cc in coins:
                if cc <= a:
                    r = min(r, rec(a - cc) + 1)
            return r
        v = rec(amount)
        assert (v if v < INF else -1) == exp == g["coinChange"](coins, amount)
        # change: 枚举每种 coin 用几枚
        def count(i, a):
            if i == len(coins):
                return 1 if a == 0 else 0
            return sum(count(i + 1, a - k * coins[i]) for k in range(a // coins[i] + 1))
        assert g["change"](amount, coins) == count(0, amount), (amount, coins)
    words = ["a", "ab", "bc", "abc", "cd"]
    import itertools
    for L in range(1, 8):
        for t in itertools.product("abcd", repeat=L):
            s = "".join(t)
            def rb(i):
                return i == len(s) or any(s.startswith(w, i) and rb(i + len(w)) for w in words)
            assert g["wordBreak"](s, words) == rb(0), s
    print("selftest ok")


# ====================================================================
# 三、SVG 小库 (配色/字号严格按 STYLE_GUIDE B)
# ====================================================================
FONT = "ui-sans-serif, system-ui, -apple-system, 'PingFang SC', sans-serif"
TEXT, SUB, DASH, RING = "#0B0B0B", "#52514E", "#B4B2A9", "#EF9F27"
ROLE = {
    "new": ("#E1F5EE", "#0F6E56", "#085041"),
    "old": ("#F1EFE8", "#5F5E5A", "#444441"),
    "del": ("#FAECE7", "#993C1D", "#712B13"),
    "empty": ("#FFFFFF", "#B4B2A9", "#B4B2A9"),
}


def tw(t, size):
    return sum(size if ord(c) > 0x2E80 else size * 0.58 for c in t)


class S:
    def __init__(self, name):
        self.name = name
        self.p = []
        self.warn = []

    def text(self, x, y, t, size=14, fill=TEXT, bold=False, anchor="start"):
        w = tw(t, size)
        lo = x - (w if anchor == "end" else w / 2 if anchor == "middle" else 0)
        if lo < 6 or lo + w > 676:
            self.warn.append("%s: text may overflow: %r (x=%s)" % (self.name, t, lo))
        self.p.append('<text x="%s" y="%s" font-size="%d" font-weight="%d" fill="%s" text-anchor="%s" '
                      'dominant-baseline="central">%s</text>'
                      % (x, y, size, 600 if bold else 400, fill, anchor, html.escape(t)))

    def rect(self, x, y, w, h, role="old", rx=4, dash=False, sw=1):
        f, s, _ = ROLE[role]
        self.p.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>'
                      % (x, y, w, h, rx, f, s, sw, ' stroke-dasharray="3 3"' if (dash or role == "empty") else ""))

    def circle(self, cx, cy, r, role="old", sw=1):
        f, s, _ = ROLE[role]
        self.p.append('<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (cx, cy, r, f, s, sw))

    def ring(self, x, y, w, h, rx=6):
        self.p.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="none" stroke="%s" stroke-width="2.5"/>'
                      % (x - 3, y - 3, w + 6, h + 6, rx, RING))

    def ring_circle(self, cx, cy, r):
        self.p.append('<circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-width="2.5"/>' % (cx, cy, r + 4, RING))

    def cell(self, x, y, w, h, t, role="old", ring=False, size=14, bold=True):
        self.rect(x, y, w, h, role)
        if t != "":
            self.text(x + w / 2, y + h / 2, str(t), size, ROLE[role][2], bold, "middle")
        if ring:
            self.ring(x, y, w, h)

    def line(self, x1, y1, x2, y2, color=DASH, dash="4 4", sw=1):
        self.p.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s/>'
                      % (x1, y1, x2, y2, color, sw, ' stroke-dasharray="%s"' % dash if dash else ""))

    def sep(self, y):
        self.line(40, y, 640, y, DASH, "4 4", 0.8)

    def path(self, dstr, color=SUB, dash=None, marker="arr", sw=1.5):
        self.p.append('<path d="%s" fill="none" stroke="%s" stroke-width="%s"%s%s/>'
                      % (dstr, color, sw, ' stroke-dasharray="%s"' % dash if dash else "",
                         ' marker-end="url(#%s)"' % marker if marker else ""))

    def legend(self, y, items, x=40):
        for kind, label in items:
            if kind == "ring":
                self.rect(x, y - 8, 22, 16, "old")
                self.ring(x, y - 8, 22, 16, 4)
                x += 6
            elif kind == "del-dash":
                self.rect(x, y - 8, 22, 16, "del", dash=True)
            else:
                self.rect(x, y - 8, 22, 16, kind)
            self.text(x + 30, y, label, 12, SUB)
            x += 30 + tw(label, 12) + 22

    def save(self, h, title):
        defs = ('<defs>'
                '<marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
                '<path d="M2 1L8 5L2 9" fill="none" stroke="#52514E" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></marker>'
                '<marker id="arrR" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
                '<path d="M2 1L8 5L2 9" fill="none" stroke="#D85A30" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></marker>'
                '<marker id="arrG" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
                '<path d="M2 1L8 5L2 9" fill="none" stroke="#0F6E56" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></marker>'
                '</defs>')
        s = ('<svg width="100%%" viewBox="0 0 680 %d" role="img" xmlns="http://www.w3.org/2000/svg" '
             'font-family="%s"><title>%s</title>%s\n%s\n</svg>\n'
             % (h, FONT, html.escape(title), defs, "\n".join(self.p)))
        with open(os.path.join(SVGDIR, self.name + ".svg"), "w", encoding="utf-8") as f:
            f.write(s)
        for w in self.warn:
            print("WARN", w)


def arrow_below(s, ax, cw, ybot, src, dst, color=SUB, marker="arr"):
    """数组格子下方的弧形箭头: 从 src 格指向 dst 格 (dst 是新填的格子)"""
    xs = ax + src * cw + cw / 2
    xd = ax + dst * cw + cw / 2
    dist = abs(dst - src)
    dep = min(30, 10 + 6 * dist)
    xe = xd + (4 if src > dst else -4)
    s.path("M%s %s C%s %s %s %s %s %s" % (xs, ybot + 2, xs, ybot + dep, xe, ybot + dep, xe, ybot + 5), color, None, marker, 1.4)


def arrow_above(s, ax, cw, ytop, src, dst, color=SUB, marker="arr"):
    xs = ax + src * cw + cw / 2
    xd = ax + dst * cw + cw / 2
    dist = abs(dst - src)
    dep = min(30, 10 + 6 * dist)
    xe = xd + (4 if src > dst else -4)
    s.path("M%s %s C%s %s %s %s %s %s" % (xs, ytop - 2, xs, ytop - dep, xe, ytop - dep, xe, ytop - 5), color, None, marker, 1.4)


CH = 30  # 数组格子高度


def trace(fname, title, rows, ncols, ax, cw, hdr, cx=None, final=None, legend=None,
          head="dp 数组", calc_head="计算", step_head="step", names=False):
    """通用 trace 图: 一行 = 一步。列固定: step | 数组 | 计算
    rows: dict(label=[(text,size,bold)], arrays=[dict(name,cells=[(text,role)],ring=[idx],arrows=[(src,dst)])],
               calc=[(text,'b'|'s')])  或 dict(section=title, hdr=[...])
    hdr / section.hdr: [(name, [texts], size)]"""
    s = S(fname)
    cx = cx if cx is not None else ax + ncols * cw + 14
    for i, t in enumerate(title if isinstance(title, list) else [title]):
        s.text(40, 18 + 20 * i, t, 12, SUB)
    y = 18 + 20 * (len(title) if isinstance(title, list) else 1) + 8
    s.text(40, y + 6, step_head, 12, SUB)
    s.text(ax, y + 6, head, 12, SUB)
    s.text(cx, y + 6, calc_head, 12, SUB)
    s.sep(y + 18)
    cur = y + 26

    def draw_hdr(cur, hd, section=None):
        if section:
            s.text(40, cur + 8, section, 14, TEXT, True)
            cur += 22
        for name, texts, size in hd:
            s.text(40, cur + 8, name, 12, SUB)
            for i, t in enumerate(texts):
                if t != "":
                    s.text(ax + i * cw + cw / 2, cur + 8, str(t), size, SUB if size == 12 else TEXT, size == 14, "middle")
            cur += 20
        if hd or section:
            s.sep(cur + 2)
        return cur + 10

    cur = draw_hdr(cur, hdr)
    for r in rows:
        if "section" in r:
            cur = draw_hdr(cur, r["hdr"], r["section"])
            continue
        top = cur
        by = top + 6
        blocks = []
        for a in r["arrays"]:
            ah = CH + (26 if a.get("arrows") else 0) + 6
            blocks.append((by, ah))
            yb = by
            for i, (t, role) in enumerate(a["cells"]):
                s.cell(ax + i * cw + 1, yb, cw - 2, CH, t, role, False)
            for i in a.get("ring", []):
                s.ring(ax + i * cw + 1, yb, cw - 2, CH)
            for (src, dst) in a.get("arrows", []):
                arrow_below(s, ax, cw, yb + CH, src, dst)
            if a.get("name"):
                s.text(ax - 6, yb + CH / 2, a["name"], 12, SUB, False, "end")
            by += ah
        for k, (t, size, bold) in enumerate(r.get("label", [])):
            s.text(40, top + 6 + CH / 2 - 8 + 17 * k, t, size, TEXT if bold else SUB, bold)
        n = len(r.get("calc", []))
        for k, (t, kind) in enumerate(r.get("calc", [])):
            s.text(cx, top + 6 + 9 + 18 * k, t, 14 if kind == "b" else 12, TEXT if kind == "b" else SUB, kind == "b")
        h = max(sum(b[1] for b in blocks) + 8, 6 + 18 * n + 14)
        s.sep(top + h)
        cur = top + h + 8
    if final:
        for k, t in enumerate(final):
            s.text(40, cur + 12 + 22 * k, t, 14, TEXT, True)
        cur += 12 + 22 * len(final)
    legend = legend or [("new", "新填的格子"), ("old", "已有的格子"), ("ring", "被依赖 (橙色 ring)"), ("empty", "还没算")]
    s.legend(cur + 22, legend)
    H = cur + 46
    s.save(H, title[0] if isinstance(title, list) else title)
    return H


# ====================================================================
# 四、各题的 trace 数据 (从真实算法跑出来, 不手写数字)
# ====================================================================
def row_cells(vals, new=(), empty_from=None, fmt=str):
    out = []
    for i, v in enumerate(vals):
        if empty_from is not None and i >= empty_from:
            out.append(("", "empty"))
        else:
            out.append((fmt(v), "new" if i in new else "old"))
    return out


def tr_climb():
    n = 5
    dp = [1, 1]
    rows = [dict(label=[("base", 14, True)],
                 arrays=[dict(cells=row_cells(dp + [0] * (n - 1), new=(0, 1), empty_from=2))],
                 calc=[("dp[0] = dp[1] = 1", "b"), ("0 阶 / 1 阶: 只有 1 种走法", "s")])]
    for i in range(2, n + 1):
        dp.append(dp[i - 1] + dp[i - 2])
        rows.append(dict(
            label=[("i = %d" % i, 14, True)],
            arrays=[dict(cells=row_cells(dp + [0] * (n - i), new=(i,), empty_from=i + 1), ring=[i - 1, i - 2],
                         arrows=[(i - 1, i), (i - 2, i)])],
            calc=[("dp[i] = dp[i-1] + dp[i-2]", "s"),
                  ("dp[%d] = %d + %d = %d" % (i, dp[i - 1], dp[i - 2], dp[i]), "b")]))
    print("climb", dp)
    trace("climb_trace", ["n = 5 · dp[i] = 走到第 i 阶的方法数 (最后一步走 1 阶或 2 阶)",
                          "每一步: 填 dp[i] = dp[i-1] + dp[i-2]; 填完后 dp[i-2] 再也不会被用到"],
          rows, n + 1, 112, 44,
          [("i", list(range(n + 1)), 12)],
          final=["答案 = dp[5] = 8"], step_head="step")
    return dp


def tr_rob():
    nums = [2, 3, 9, 3, 1]
    n = len(nums)
    dp = [nums[0], max(nums[0], nums[1])]
    rows = [dict(label=[("base", 14, True)],
                 arrays=[dict(cells=row_cells(dp + [0] * (n - 2), new=(0, 1), empty_from=2), ring=[0], arrows=[(0, 1)])],
                 calc=[("dp[0] = nums[0] = 2", "b"), ("dp[1] = max(2, 3) = %d" % dp[1], "b")])]
    for i in range(2, n):
        take = dp[i - 2] + nums[i]
        skip = dp[i - 1]
        dp.append(max(skip, take))
        why = "偷 %d: %d + %d" % (nums[i], dp[i - 2], nums[i]) if take > skip else "不偷 %d: 继承 dp[%d]" % (nums[i], i - 1)
        rows.append(dict(
            label=[("i = %d" % i, 14, True), ("nums[%d] = %d" % (i, nums[i]), 12, False)],
            arrays=[dict(cells=row_cells(dp + [0] * (n - i - 1), new=(i,), empty_from=i + 1), ring=[i - 1, i - 2],
                         arrows=[(i - 1, i), (i - 2, i)])],
            calc=[("dp[i] = max(dp[i-1], dp[i-2] + nums[i])", "s"),
                  ("dp[%d] = max(%d, %d + %d) = %d" % (i, dp[i - 1], dp[i - 2], nums[i], dp[i]), "b"),
                  (why + " 更大" if take > skip else why + " (≥ 偷)", "s")]))
    print("rob", dp)
    trace("rob_trace", ["nums = [2, 3, 9, 3, 1] · dp[i] = 只看前 i+1 间房子 (nums[0..i]) 时的最大金额",
                        "每一步: 不偷 i 就继承 dp[i-1]; 偷 i 就是 dp[i-2] + nums[i]; 取较大者"],
          rows, n, 116, 44,
          [("i", list(range(n)), 12), ("nums", nums, 14)],
          cx=116 + n * 44 + 14, final=["答案 = dp[4] = %d" % dp[-1]])
    return dp


def rob_dp(nums):
    dp = [nums[0], max(nums[0], nums[1])]
    for i in range(2, len(nums)):
        dp.append(max(dp[i - 1], dp[i - 2] + nums[i]))
    return dp


def tr_rob2():
    nums = [2, 3, 9, 3, 1]
    a = nums[:-1]
    b = nums[1:]
    rows = []
    res = []
    for tag, arr, sec in (("A", a, "情况 A: 不偷最后一间 → 线性 nums[0..3] = %s" % a),
                          ("B", b, "情况 B: 不偷第一间 → 线性 nums[1..4] = %s" % b)):
        dp = rob_dp(arr)
        m = len(arr)
        rows.append(dict(section=sec, hdr=[("i", list(range(m)), 12), ("nums", arr, 14)]))
        rows.append(dict(label=[("base", 14, True)],
                         arrays=[dict(cells=row_cells(dp[:2] + [0] * (m - 2), new=(0, 1), empty_from=2), ring=[0], arrows=[(0, 1)])],
                         calc=[("dp[0] = %d" % arr[0], "b"), ("dp[1] = max(%d, %d) = %d" % (arr[0], arr[1], dp[1]), "b")]))
        for i in range(2, m):
            rows.append(dict(
                label=[("i = %d" % i, 14, True), ("nums[%d] = %d" % (i, arr[i]), 12, False)],
                arrays=[dict(cells=row_cells(dp[:i + 1] + [0] * (m - i - 1), new=(i,), empty_from=i + 1), ring=[i - 1, i - 2],
                             arrows=[(i - 1, i), (i - 2, i)])],
                calc=[("dp[%d] = max(%d, %d + %d) = %d" % (i, dp[i - 1], dp[i - 2], arr[i], dp[i]), "b")]))
        res.append(dp[-1])
    print("rob2", res)
    trace("rob2_trace", ["nums = [2, 3, 9, 3, 1] 排成一圈 · nums[0] 和 nums[4] 相邻, 不能同时偷",
                         "做两次和 House Robber 完全一样的线性 DP, 答案取较大者"],
          rows, 4, 116, 44, [], cx=116 + 4 * 44 + 14,
          final=["答案 = max(A, B) = max(%d, %d) = %d" % (res[0], res[1], max(res))])
    return res


def tr_kadane():
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    n = len(nums)
    cur = [nums[0]]
    best = [nums[0]]
    rows = [dict(label=[("base", 14, True)],
                 arrays=[dict(cells=row_cells(cur + [0] * (n - 1), new=(0,), empty_from=1))],
                 calc=[("cur[0] = nums[0] = -2", "b"), ("best = -2", "s")])]
    for i in range(1, n):
        x = nums[i]
        c = max(x, cur[i - 1] + x)
        cur.append(c)
        best.append(max(best[-1], c))
        how = "重开 (只取 x)" if x >= cur[i - 1] + x else "接在 cur[%d] 后面" % (i - 1)
        rows.append(dict(
            label=[("i = %d" % i, 14, True), ("x = %d" % x, 12, False)],
            arrays=[dict(cells=row_cells(cur + [0] * (n - i - 1), new=(i,), empty_from=i + 1), ring=[i - 1], arrows=[(i - 1, i)])],
            calc=[("cur = max(%d, %d + %s) = %d" % (x, cur[i - 1], ("(%d)" % x) if x < 0 else x, c), "b"),
                  ("%s · best = %d" % (how, best[-1]), "s")]))
    print("kadane", cur, best[-1])
    trace("kadane_trace", ["nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4] · cur[i] = 以 nums[i] 结尾的最大 subarray sum",
                           "每一步: cur[i] = max(x, cur[i-1] + x) (x = nums[i]); best = 所有 cur 里最大的"],
          rows, n, 112, 34, [("i", list(range(n)), 12), ("nums", nums, 14)],
          cx=112 + n * 34 + 12, final=["答案 = best = %d  (subarray [4, -1, 2, 1])" % best[-1]], head="cur 数组", calc_head="计算")
    return cur


def tr_prod():
    nums = [2, -3, -2, 4]
    n = len(nums)
    mx, mn = [nums[0]], [nums[0]]
    rows = [dict(label=[("base", 14, True)],
                 arrays=[dict(name="mx", cells=row_cells(mx + [0] * (n - 1), new=(0,), empty_from=1)),
                         dict(name="mn", cells=row_cells(mn + [0] * (n - 1), new=(0,), empty_from=1))],
                 calc=[("mx = mn = nums[0] = 2", "b"), ("只有它自己一个数", "s")])]
    best = nums[0]
    for i in range(1, n):
        x = nums[i]
        c = (x, mx[-1] * x, mn[-1] * x)
        nmx, nmn = max(c), min(c)
        rows.append(dict(
            label=[("i = %d" % i, 14, True), ("x = %d" % x, 12, False)],
            arrays=[dict(name="mx", cells=row_cells(mx + [nmx] + [0] * (n - i - 1), new=(i,), empty_from=i + 1), ring=[i - 1]),
                    dict(name="mn", cells=row_cells(mn + [nmn] + [0] * (n - i - 1), new=(i,), empty_from=i + 1), ring=[i - 1])],
            calc=[("候选 x, mx×x, mn×x: %d, (%d)×(%d) = %d, (%d)×(%d) = %d" % (x, mx[-1], x, mx[-1] * x, mn[-1], x, mn[-1] * x), "s"),
                  ("mx = max(%d, %d, %d) = %d" % (c[0], c[1], c[2], nmx), "b"),
                  ("mn = min(%d, %d, %d) = %d" % (c[0], c[1], c[2], nmn), "b")]))
        mx.append(nmx)
        mn.append(nmn)
        best = max(best, nmx)
    print("prod", mx, mn, best)
    trace("prod_trace", ["nums = [2, -3, -2, 4] · mx[i] / mn[i] = 以 nums[i] 结尾的最大 / 最小 product",
                         "每一步: 候选 = x, mx[i-1]×x, mn[i-1]×x; mx 取最大, mn 取最小 (两个都用上一格的旧值)"],
          rows, n, 128, 44, [("i", list(range(n)), 12), ("nums", nums, 14)], cx=128 + n * 44 + 12,
          final=["答案 = max(mx) = max(2, -3, 12, 48) = %d" % best], head="mx / mn 数组")
    return best


def tr_stock():
    prices = [7, 1, 5, 3, 6, 4]
    n = len(prices)
    lo, best = [prices[0]], [0]
    rows = [dict(label=[("base", 14, True)],
                 arrays=[dict(name="lo", cells=row_cells(lo + [0] * (n - 1), new=(0,), empty_from=1)),
                         dict(name="best", cells=row_cells(best + [0] * (n - 1), new=(0,), empty_from=1))],
                 calc=[("lo = prices[0] = 7", "b"), ("best = 0 (还没法卖)", "s")])]
    for i in range(1, n):
        p = prices[i]
        profit = p - lo[-1]
        nb = max(best[-1], profit)
        nl = min(lo[-1], p)
        rows.append(dict(
            label=[("i = %d" % i, 14, True), ("price = %d" % p, 12, False)],
            arrays=[dict(name="lo", cells=row_cells(lo + [nl] + [0] * (n - i - 1), new=(i,), empty_from=i + 1), ring=[i - 1]),
                    dict(name="best", cells=row_cells(best + [nb] + [0] * (n - i - 1), new=(i,), empty_from=i + 1), ring=[i - 1])],
            calc=[("今天卖: profit = %d - %d = %d" % (p, lo[-1], profit), "s"),
                  ("best = max(%d, %d) = %d" % (best[-1], profit, nb), "b"),
                  ("lo = min(%d, %d) = %d" % (lo[-1], p, nl), "b")]))
        lo.append(nl)
        best.append(nb)
    print("stock", lo, best)
    trace("stock_trace", ["prices = [7, 1, 5, 3, 6, 4] · lo[i] = 到第 i 天为止的最低价 · best[i] = 到第 i 天为止的最大利润",
                          "每一步: 先用昨天的 lo 算今天卖的 profit 更新 best, 再更新 lo"],
          rows, n, 140, 44, [("i", list(range(n)), 12), ("price", prices, 14)], cx=140 + n * 44 + 12,
          final=["答案 = best = %d  (第 1 天买 1, 第 4 天卖 6)" % best[-1]], head="lo / best 数组")
    return best[-1]


def tr_coin():
    coins, amount = [1, 3, 4], 6
    INF = 10 ** 9
    dp = [0] + [INF] * amount
    rows = [dict(label=[("base", 14, True)],
                 arrays=[dict(cells=row_cells([0] * (amount + 1), new=(0,), empty_from=1))],
                 calc=[("dp[0] = 0", "b"), ("凑出 0 元不需要 coin", "s")])]
    for a in range(1, amount + 1):
        opts = [(c, dp[a - c]) for c in coins if c <= a]
        dp[a] = min(v for _, v in opts) + 1
        best_c = [c for c, v in opts if v + 1 == dp[a]]
        rows.append(dict(
            label=[("a = %d" % a, 14, True)],
            arrays=[dict(cells=row_cells(dp[:a + 1] + [0] * (amount - a), new=(a,), empty_from=a + 1),
                         ring=[a - c for c, _ in opts], arrows=[(a - c, a) for c, _ in opts])],
            calc=[("最后一枚 %s → 看 %s" % (" / ".join(str(c) for c, _ in opts), ", ".join("dp[%d]" % (a - c) for c, _ in opts)), "s"),
                  ("dp[%d] = 1 + min(%s) = %d" % (a, ", ".join(str(v) for _, v in opts), dp[a]), "b")]))
    print("coin", dp)
    trace("coin_trace", ["coins = [1, 3, 4], amount = 6 · dp[a] = 凑出金额 a 最少要几枚 coin",
                         "每一步: 枚举最后一枚 coin c (c ≤ a): dp[a] = 1 + min(dp[a - c])"],
          rows, amount + 1, 108, 40, [("a", list(range(amount + 1)), 12)], cx=108 + (amount + 1) * 40 + 12,
          final=["答案 = dp[6] = %d  (3 + 3; 贪心 4 + 1 + 1 要 3 枚)" % dp[amount]])
    return dp


def tr_change():
    coins, amount = [1, 2, 5], 5
    dp = [1] + [0] * amount
    rows = [dict(label=[("base", 14, True)],
                 arrays=[dict(cells=[("1", "new")] + [("0", "old")] * amount)],
                 calc=[("dp[0] = 1", "b"), ("什么都不拿: 算 1 种组合", "s")])]
    combos = {1: "{1×5}", 2: "{1×5} {1×3,2} {1,2×2}", 5: "上面 3 种 + {5}"}
    for c in coins:
        old = dp[:]
        for a in range(c, amount + 1):
            dp[a] += dp[a - c]
        changed = tuple(a for a in range(amount + 1) if dp[a] != old[a])
        rows.append(dict(
            label=[("coin = %d" % c, 14, True), ("处理完后", 12, False)],
            arrays=[dict(cells=[(str(v), "new" if i in changed else "old") for i, v in enumerate(dp)], ring=[5 - c],
                         arrows=[(5 - c, 5)])],
            calc=[("dp[5] = dp[5] + dp[5-%d]  (旧值 + 用 %d 之后的)" % (c, c), "s"),
                  ("dp[5] = %d + %d = %d" % (old[5], dp[5 - c], dp[5]), "b"),
                  ("组合: " + combos[c], "s")]))
    print("change", dp)
    trace("change_trace", ["coins = [1, 2, 5], amount = 5 · dp[a] = 凑出金额 a 的组合数 · 外层 for coin, 内层 for a 正序",
                           "每一步: 一整轮处理一种 coin; 本轮改变的格子绿色; 以 dp[5] 为例看算式"],
          rows, amount + 1, 108, 40, [("a", list(range(amount + 1)), 12)], cx=108 + (amount + 1) * 40 + 12,
          final=["答案 = dp[5] = %d" % dp[amount]], head="dp 数组 (每轮结束后)")
    return dp


def tr_partition():
    nums = [1, 2, 3, 4]
    target = sum(nums) // 2
    dp = [True] + [False] * target
    rows = [dict(label=[("base", 14, True)],
                 arrays=[dict(cells=[("T", "new")] + [("F", "old")] * target)],
                 calc=[("dp[0] = True", "b"), ("空集的和是 0", "s")])]
    for x in nums:
        old = dp[:]
        steps = []
        for c in range(target, x - 1, -1):
            dp[c] = dp[c] or dp[c - x]
            if dp[c] and not old[c]:
                steps.append((c, c - x))
        new = tuple(c for c, _ in steps)
        rows.append(dict(
            label=[("x = %d" % x, 14, True), ("c: %d → %d" % (target, x), 12, False)],
            arrays=[dict(cells=[("T" if v else "F", "new" if i in new else "old") for i, v in enumerate(dp)],
                         ring=sorted({b for _, b in steps}), arrows=[(b, c) for c, b in steps])],
            calc=([("dp[c] = dp[c] or dp[c - %d]" % x, "s")] +
                  [("dp[%d] 变 True: dp[%d - %d] = dp[%d] 是 True" % (c, c, x, b), "b") for c, b in steps] +
                  ([("没有新的 True", "s")] if not steps else []))))
    print("partition", dp)
    trace("partition_trace", ["nums = [1, 2, 3, 4], total = 10, target = 5 · dp[c] = 处理过的数里能不能凑出和 c",
                              "每个 x: c 从 target 倒着走到 x; dp[c] |= dp[c - x]; 读的 dp[c-x] 都是处理 x 之前的旧值"],
          rows, target + 1, 108, 40, [("c", list(range(target + 1)), 12)], cx=108 + (target + 1) * 40 + 12,
          final=["答案 = dp[5] = %s  ({2,3} 或 {1,4})" % dp[target]], head="dp 数组 (每个 x 处理完后)")
    return dp


def tr_wordbreak():
    s = "catsand"
    words = {"cat", "cats", "and", "sand"}
    n = len(s)
    dp = [True] + [False] * n
    rows = [dict(label=[("base", 14, True)],
                 arrays=[dict(cells=[("T", "new")] + [("", "empty")] * n)],
                 calc=[("dp[0] = True", "b"), ("空串可以切 (0 个词)", "s")])]
    for i in range(1, n + 1):
        js = [j for j in range(i) if dp[j]]
        ok = [j for j in js if s[j:i] in words]
        dp[i] = bool(ok)
        shown = "  ".join("%s%s" % (s[j:i], "✓" if j in ok else "✗") for j in js)
        rows.append(dict(
            label=[("i = %d" % i, 14, True), ("'%s'" % s[:i], 12, False)],
            arrays=[dict(cells=[("T" if v else "F", "new" if k == i else "old") for k, v in enumerate(dp[:i + 1])] + [("", "empty")] * (n - i),
                         ring=ok, arrows=[(j, i) for j in ok])],
            calc=[("dp[j] = T 的 j: %s" % ", ".join(map(str, js)), "s"),
                  ("切出 " + shown, "s"),
                  ("dp[%d] = %s" % (i, dp[i]), "b")]))
    print("wordbreak", dp)
    trace("wordbreak_trace", ["s = \"catsand\", words = {cat, cats, and, sand} · dp[i] = 前 i 个字符 s[:i] 能不能切成词典里的词",
                              "每一步: 只试 dp[j] = True 的 j, 看最后一块 s[j:i] 在不在词典里; 有一个 ✓ 就是 True"],
          rows, n + 1, 104, 36,
          [("i", list(range(n + 1)), 12), ("s[i-1]", [""] + list(s), 14)], cx=104 + (n + 1) * 36 + 10,
          final=["答案 = dp[7] = True  (cat + sand 或 cats + and)"])
    return dp


def tr_lis():
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    n = len(nums)
    dp = [1] * n
    rows = []
    for i in range(n):
        js = [j for j in range(i) if nums[j] < nums[i]]
        if js:
            dp[i] = max(dp[j] for j in js) + 1
        bj = max(js, key=lambda j: dp[j]) if js else None
        calc = []
        if i == 0:
            calc = [("dp[0] = 1", "b"), ("前面没有元素", "s")]
        elif not js:
            calc = [("前面没有比 %d 小的" % nums[i], "s"), ("dp[%d] = 1" % i, "b")]
        else:
            contiguous = js == list(range(js[0], js[-1] + 1))
            jtxt = ("%d..%d" % (js[0], js[-1])) if (contiguous and len(js) > 3) else ", ".join(map(str, js))
            if len(js) > 3 and contiguous:
                mtxt = "dp[%d..%d]" % (js[0], js[-1])
                fml = "dp[%d] = 1 + max(%s) = 1 + %d = %d" % (i, mtxt, max(dp[j] for j in js), dp[i])
            else:
                fml = "dp[%d] = 1 + max(%s) = %d" % (i, ", ".join(str(dp[j]) for j in js), dp[i])
            calc = [("nums[j] < %d 的 j: %s" % (nums[i], jtxt), "s"), (fml, "b")]
        rows.append(dict(
            label=[("i = %d" % i, 14, True), ("x = %d" % nums[i], 12, False)],
            arrays=[dict(cells=row_cells(dp[:i + 1] + [0] * (n - i - 1), new=(i,), empty_from=i + 1),
                         ring=js, arrows=([(bj, i)] if js else []))],
            calc=calc))
    print("lis", dp)
    trace("lis_trace", ["nums = [10, 9, 2, 5, 3, 7, 101, 18] · dp[i] = 以 nums[i] 结尾的最长递增子序列长度",
                        "每一步: 往回看所有 j < i; 满足 nums[j] < nums[i] 的 dp[j] 里取最大 + 1 (箭头只画取最大的那个)"],
          rows, n, 104, 38, [("i", list(range(n)), 12), ("nums", nums, 14)], cx=104 + n * 38 + 12,
          final=["答案 = max(dp) = %d  (如 2, 3, 7, 18)" % max(dp)])
    return dp


# ====================================================================
# 五、core 图 (每题一张, 只表达一个结论)
# ====================================================================
def core_first():
    s = S("first_principles_core")
    s.text(40, 18, "f(n) = 走到第 n 阶的方法数 = f(n-1) + f(n-2) · f(0) = f(1) = 1", 12, SUB)
    s.text(40, 38, "左: 朴素递归树里同一个 f(k) 被反复展开 (红 = 已经算过一次的重复子问题) · 右: 每个 f(k) 只算一次", 12, SUB)
    s.text(40, 66, "递归 brute force: 15 次调用 → O(2ⁿ)", 14, TEXT, True)
    s.text(410, 66, "DP table: 6 个格子 → O(n)", 14, TEXT, True)
    # 递归树
    seen = set()
    nodes = []  # (n, level, x, parent_idx, repeated)
    leaf_i = [0]

    def build(n, lvl, parent):
        idx = len(nodes)
        rep = n in seen
        seen.add(n)
        nodes.append([n, lvl, None, parent, rep])
        if n >= 2:
            xs = [build(n - 1, lvl + 1, idx), build(n - 2, lvl + 1, idx)]
            nodes[idx][2] = sum(nodes[k][2] for k in xs) / 2
        else:
            nodes[idx][2] = 44 + leaf_i[0] * 44.5
            leaf_i[0] += 1
        return idx

    build(5, 0, None)
    y0, dy = 108, 54
    for n, lvl, x, par, rep in nodes:
        if par is not None:
            s.line(x, y0 + lvl * dy, nodes[par][2], y0 + (lvl - 1) * dy, "#B4B2A9", None, 1)
    for n, lvl, x, par, rep in nodes:
        s.circle(x, y0 + lvl * dy, 15, "del" if rep else "new")
        s.text(x, y0 + lvl * dy, "f%d" % n, 14, ROLE["del" if rep else "new"][2], True, "middle")
    total = len(nodes)
    cnt = {k: sum(1 for nd in nodes if nd[0] == k) for k in range(6)}
    assert total == 15 and cnt[3] == 2 and cnt[2] == 3
    ybt = y0 + 4 * dy + 38
        # 右: table
    ax, cw, ty = 420, 40, 120
    vals = [1, 1, 2, 3, 5, 8]
    for i, v in enumerate(vals):
        s.text(ax + i * cw + cw / 2, ty - 16, "dp[%d]" % i, 12, SUB, False, "middle")
        s.cell(ax + i * cw + 1, ty, cw - 2, 30, v, "new" if i == 5 else "old", False)
    s.ring(ax + 3 * cw + 1, ty, cw - 2, 30)
    s.ring(ax + 4 * cw + 1, ty, cw - 2, 30)
    arrow_below(s, ax, cw, ty + 30, 4, 5)
    arrow_below(s, ax, cw, ty + 30, 3, 5)
    s.text(ax, ty + 64, "dp[5] = dp[4] + dp[3] = 5 + 3 = 8", 14, TEXT, True)
    steps = [("① state", "dp[i] = 走到第 i 阶的方法数"),
             ("② transition", "dp[i] = dp[i-1] + dp[i-2]"),
             ("③ base case", "dp[0] = dp[1] = 1"),
             ("④ 计算顺序", "i 从小到大, 依赖的格子已填好")]
    for k, (a, b) in enumerate(steps):
        s.text(ax, ty + 96 + 36 * k, a, 12, SUB)
        s.text(ax, ty + 96 + 36 * k + 17, b, 14, TEXT, True)
    s.line(396, 84, 396, 352, DASH, "4 4", 0.8)
    s.text(40, 376, "f3 展开了 2 次, f2 展开了 3 次, f1 展开了 5 次 → 不同的子问题其实只有 6 个 (f0 … f5)", 12, SUB)
    s.legend(404, [("new", "第一次算 (要保留)"), ("del", "重复子问题 (浪费)"), ("ring", "dp[5] 依赖的格子")])
    s.save(428, "递归树里的重复子问题与 DP table")


def mini_cells(s, x, y, cw, vals, roles=None, ch=30, labels=None, size=14, rings=()):
    for i, v in enumerate(vals):
        r = roles[i] if roles else "old"
        s.cell(x + i * cw + 1, y, cw - 2, ch, v, r, False, size)
        if labels:
            s.text(x + i * cw + cw / 2, y - 14, labels[i], 12, SUB, False, "middle")
    for i in rings:
        s.ring(x + i * cw + 1, y, cw - 2, ch)


def core_climb():
    s = S("climb_core")
    s.text(40, 18, "到第 i 阶的最后一步只有两种, 互斥且穷尽 → 方法数直接相加", 12, SUB)
    s.text(40, 38, "dp[i] = 走到第 i 阶的方法数", 12, SUB)
    xs = [90, 270, 450]
    labs = ["dp[i-2]", "dp[i-1]", "dp[i]"]
    roles = ["old", "old", "new"]
    by = 112
    for k in range(3):
        s.rect(xs[k], by, 130, 44, roles[k])
        s.text(xs[k] + 65, by + 22, labs[k], 16, ROLE[roles[k]][2], True, "middle")
    s.ring(xs[0], by, 130, 44, 8)
    s.ring(xs[1], by, 130, 44, 8)
    s.path("M%s %s C%s %s %s %s %s %s" % (xs[0] + 65, by - 4, xs[0] + 65, by - 50, xs[2] + 65, by - 50, xs[2] + 65, by - 4))
    s.text((xs[0] + xs[2]) / 2 + 65, 66, "最后一步走 2 阶 (从 i-2 出发)", 12, SUB, False, "middle")
    s.path("M%s %s L%s %s" % (xs[1] + 134, by + 22, xs[2] - 6, by + 22))
    s.text(xs[1] + 134 + 24, by + 6, "走 1 阶", 12, SUB, False, "middle")
    s.text(40, 190, "dp[i] 只读前两格 → 更早的格子填完就再也用不到, 不用存整张表:", 14, TEXT, True)
    s.text(40, 232, "i 时", 12, SUB)
    s.text(40, 292, "i+1 时", 12, SUB)
    rows = [(214, [("a = dp[i-2]", "old"), ("b = dp[i-1]", "old")]),
            (274, [("a = 旧 b = dp[i-1]", "old"), ("b = 旧 a + 旧 b = dp[i]", "new")])]
    for y, items in rows:
        for k, (lab, role) in enumerate(items):
            s.rect(110 + k * 210, y, 190, 36, role)
            s.text(110 + k * 210 + 95, y + 18, lab, 14, ROLE[role][2], True, "middle")
    s.text(110, 332, "a, b = b, a + b", 16, TEXT, True)
    s.text(270, 332, "右边先算完整个表达式, 再同时赋值", 12, SUB)
    s.legend(362, [("new", "新算的"), ("ring", "被依赖的")])
    s.save(386, "Climbing Stairs 的 transition 与滚动变量")


def core_rob():
    s = S("rob_core")
    s.text(40, 18, "dp[i] = 只看 nums[0..i] 时的最大金额 · 对第 i 间房子只有两个选择", 12, SUB)
    s.text(40, 38, "例: nums = [2, 3, 9] → dp[0] = 2, dp[1] = 3, 现在算 dp[2]", 12, SUB)
    xs = [90, 270, 450]
    labs = [("dp[0] = 2", "nums[0] = 2"), ("dp[1] = 3", "nums[1] = 3"), ("dp[2] = ?", "nums[2] = 9")]
    roles = ["old", "old", "new"]
    by = 126
    for k in range(3):
        s.rect(xs[k], by, 130, 54, roles[k])
        s.text(xs[k] + 65, by + 19, labs[k][0], 14, ROLE[roles[k]][2], True, "middle")
        s.text(xs[k] + 65, by + 40, labs[k][1], 12, ROLE[roles[k]][2], False, "middle")
    s.ring(xs[0], by, 130, 54, 8)
    s.ring(xs[1], by, 130, 54, 8)
    s.path("M%s %s L%s %s" % (xs[1] + 134, by + 27, xs[2] - 6, by + 27))
    s.text(xs[1] + 134 + 24, by + 11, "不偷 9", 12, SUB, False, "middle")
    s.path("M%s %s C%s %s %s %s %s %s" % (xs[0] + 65, by - 4, xs[0] + 65, by - 56, xs[2] + 65, by - 56, xs[2] + 65, by - 4))
    s.text(xs[1] + 65, 72, "偷 9: 邻居 nums[1] 不能偷 → 跳过, 接在 dp[0] 后", 12, SUB, False, "middle")
    s.text(40, 222, "两个选择各自的值", 14, TEXT, True)
    s.text(40, 250, "不偷 nums[2]: 最好就是前两间的最优 = dp[1] = 3", 14, TEXT)
    s.text(40, 276, "偷 nums[2]:  dp[0] + nums[2] = 2 + 9 = 11", 14, TEXT)
    s.text(40, 312, "dp[2] = max(dp[1], dp[0] + nums[2]) = max(3, 2 + 9) = 11", 16, TEXT, True)
    s.text(40, 342, "不会漏掉最优: 最优方案要么没偷 i (子问题是 dp[i-1]), 要么偷了 i (子问题是 dp[i-2])", 12, SUB)
    s.legend(372, [("new", "要算的 dp[i]"), ("ring", "两个候选依赖的格子")])
    s.save(396, "House Robber 选或不选")


def core_rob2():
    s = S("rob2_core")
    s.text(40, 18, "环: nums[0] 和 nums[4] 相邻 → 它们至少有一个不偷", 12, SUB)
    s.text(40, 38, "把 \"环\" 拆成两个线性问题: 每个都是 House Robber, 最后取较大者", 12, SUB)
    nums = [2, 3, 9, 3, 1]
    cw = 56
    ax = 150
    for name, y, skip, lab in (("A", 80, 4, "不偷最后一间"), ("B", 176, 0, "不偷第一间")):
        s.text(40, y + 15, "情况 " + name, 14, TEXT, True)
        s.text(40, y + 36, lab, 12, SUB)
        for i in range(5):
            s.text(ax + i * cw + cw / 2, y - 12, "nums[%d]" % i, 12, SUB, False, "middle")
            if i == skip:
                s.rect(ax + i * cw + 1, y, cw - 2, 34, "del", dash=True)
                s.text(ax + i * cw + cw / 2, y + 17, str(nums[i]), 14, ROLE["del"][2], True, "middle")
                s.line(ax + i * cw + 6, y + 6, ax + i * cw + cw - 6, y + 28, "#D85A30", None, 1.5)
            else:
                s.cell(ax + i * cw + 1, y, cw - 2, 34, nums[i], "new", False)
    A = 11
    B = 10
    s.text(ax + 5 * cw + 16, 80 + 17, "= %d" % A, 16, TEXT, True)
    s.text(ax + 5 * cw + 16, 176 + 17, "= %d" % B, 16, TEXT, True)
    s.text(40, 262, "答案 = max(A, B) = max(11, 10) = 11", 16, TEXT, True)
    s.text(40, 292, "覆盖所有合法方案: 偷首不偷尾 ⊂ B 的反面…", 12, SUB)
    s.p.pop()
    s.text(40, 292, "所有合法方案 = 不偷尾 (A 覆盖) ∪ 不偷首 (B 覆盖); 首尾都不偷同时被 A、B 覆盖, 不影响取 max", 12, SUB)
    s.legend(322, [("new", "这一轮参与线性 DP 的房子"), ("del-dash", "被排除 (不偷) 的那间")])
    s.save(346, "House Robber II 把环拆成两个线性问题")


def core_kadane():
    s = S("kadane_core")
    s.text(40, 18, "cur[i] = 以 nums[i] 结尾 (必须包含 nums[i]) 的最大 subarray sum · 答案 = 所有 cur[i] 的最大值", 12, SUB)
    s.text(40, 38, "为什么要 \"以 i 结尾\": 一旦规定了结尾, 到 i 为止只剩两种形状, 状态才接得上", 12, SUB)
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    cw = 46
    ax = 130
    y = 96
    for i, v in enumerate(nums):
        s.text(ax + i * cw + cw / 2, y - 14, "i=%d" % i, 12, SUB, False, "middle")
        s.cell(ax + i * cw + 1, y, cw - 2, 32, v, "new" if i == 3 else "old", False)
    s.text(40, y + 16, "nums", 12, SUB)
    s.ring(ax + 3 * cw + 1, y, cw - 2, 32)

    def bracket(x1, x2, yy, color="#5F5E5A"):
        s.line(x1, yy, x2, yy, color, None, 1.5)
        s.line(x1, yy - 5, x1, yy, color, None, 1.5)
        s.line(x2, yy - 5, x2, yy, color, None, 1.5)
    yb1, yb2 = y + 58, y + 98
    bracket(ax + 1 * cw + 3, ax + 4 * cw - 3, yb1)
    s.text(40, yb1 + 2, "接在 cur[2] 后面", 14, TEXT, True)
    s.text(ax + 4 * cw + 10, yb1 + 2, "[1, -3, 4] = cur[2] + 4 = -2 + 4 = 2", 14, TEXT)
    bracket(ax + 3 * cw + 3, ax + 4 * cw - 3, yb2, "#0F6E56")
    s.text(40, yb2 + 2, "重新开始", 14, TEXT, True)
    s.text(ax + 4 * cw + 10, yb2 + 2, "[4] = 4  (更大)", 14, TEXT)
    s.text(40, y + 150, "cur[3] = max(x, cur[2] + x) = max(4, -2 + 4) = 4", 16, TEXT, True)
    s.text(40, y + 180, "cur[2] = -2 < 0 → 带着前面的只会拖后腿 → 重开。cur[i-1] ≥ 0 才接着走。", 14, TEXT)
    s.text(40, y + 208, "最优 subarray 一定在某个 i 结束 → 逐个 i 算出 cur[i], 取最大; 不是 cur[n-1]。", 12, SUB)
    s.legend(y + 238, [("new", "当前 i = 3"), ("ring", "被依赖的 cur[2]")])
    s.save(y + 262, "Kadane: 以 i 结尾的 state")


def core_prod():
    s = S("prod_core")
    s.text(40, 18, "mx / mn = 以 nums[i] 结尾的最大 / 最小 product · 乘负数会让最小变最大", 12, SUB)
    s.text(40, 38, "新 mx, mn 都是从旧 (mx, mn) 乘 x 得到; 箭头表示 \"哪个旧值乘 x 得到哪个新值\"", 12, SUB)
    panels = [(40, "x = 3 > 0: 平行", 3, False), (370, "x = -2 < 0: 交叉", -2, True)]
    for px, title, x, cross in panels:
        s.text(px, 76, title, 14, TEXT, True)
        pm, pn = 6, -4
        s.rect(px, 100, 100, 40, "old")
        s.text(px + 50, 120, "mx = %d" % pm, 14, ROLE["old"][2], True, "middle")
        s.rect(px, 170, 100, 40, "old")
        s.text(px + 50, 190, "mn = %d" % pn, 14, ROLE["old"][2], True, "middle")
        nm, nn = (pm * x, pn * x) if not cross else (pn * x, pm * x)
        s.rect(px + 170, 100, 100, 40, "new")
        s.text(px + 220, 120, "mx = %d" % nm, 14, ROLE["new"][2], True, "middle")
        s.rect(px + 170, 170, 100, 40, "new")
        s.text(px + 220, 190, "mn = %d" % nn, 14, ROLE["new"][2], True, "middle")
        if not cross:
            s.path("M%s 120 L%s 120" % (px + 102, px + 166))
            s.path("M%s 190 L%s 190" % (px + 102, px + 166))
        else:
            s.path("M%s 124 L%s 186" % (px + 102, px + 166))
            s.path("M%s 186 L%s 124" % (px + 102, px + 166))
        s.text(px + 135, 88, "× %d" % x, 12, SUB, False, "middle")
        if not cross:
            s.text(px, 236, "mx × 3 = 18", 14, TEXT)
            s.text(px, 258, "mn × 3 = -12", 14, TEXT)
        else:
            s.text(px, 236, "mn × (-2) = 8 → 新 mx", 14, TEXT)
            s.text(px, 258, "mx × (-2) = -12 → 新 mn", 14, TEXT)
    assert 6 * 3 == 18 and -4 * 3 == -12 and -4 * -2 == 8 and 6 * -2 == -12
    s.text(40, 304, "只记 mx 不够: mx 一遇到负数就变成最小, 原来的 mn 才是下一个负数翻身的机会", 14, TEXT, True)
    s.text(40, 330, "所以 state 要两个: 以 i 结尾的最大 和 最小。候选 = x (重开), mx × x, mn × x。", 12, SUB)
    s.legend(360, [("old", "上一格的 (mx, mn)"), ("new", "这一格的 (mx, mn)")])
    s.save(384, "Maximum Product Subarray 同时维护 max 和 min")


def core_stock():
    s = S("stock_core")
    s.text(40, 18, "每个 j 天卖出, 最佳买入日 = j 之前价格最低的那天 → 只需维护 lo = 到目前为止的最低价", 12, SUB)
    s.text(40, 38, "prices = [7, 1, 5, 3, 6, 4]", 12, SUB)
    prices = [7, 1, 5, 3, 6, 4]
    base, bw, gap, x0 = 230, 30, 10, 44
    sc = 20
    for i, p in enumerate(prices):
        x = x0 + i * (bw + gap)
        role = "new" if i == 1 else "old"
        s.rect(x, base - p * sc, bw, p * sc, role, 3)
        s.text(x + bw / 2, base - p * sc - 12, str(p), 14, TEXT, True, "middle")
        s.text(x + bw / 2, base + 14, "i=%d" % i, 12, SUB, False, "middle")
    s.ring(x0 + 4 * (bw + gap), base - 6 * sc, bw, 6 * sc)
    ylo = base - 1 * sc
    s.line(x0 + 1 * (bw + gap) + bw, ylo, x0 + 5 * (bw + gap) + bw + 6, ylo, "#0F6E56", "5 4", 1.5)
    s.text(x0 + 5 * (bw + gap) + bw + 12, ylo - 10, "lo = 1", 12, SUB)
    xa = x0 + 4 * (bw + gap) + bw + 5
    s.path("M%s %s L%s %s" % (xa, ylo, xa, base - 6 * sc + 2), "#0F6E56", None, "arrG", 1.5)
    s.text(xa + 20, 134, "profit = 6 - 1 = 5", 14, TEXT, True)
    cx0 = 440
    s.text(cx0, 76, "同一件事的状态机视角", 14, TEXT, True)
    s.rect(cx0, 110, 100, 44, "old")
    s.text(cx0 + 50, 132, "cash", 14, ROLE["old"][2], True, "middle")
    s.rect(cx0 + 120, 110, 100, 44, "new")
    s.text(cx0 + 170, 132, "hold", 14, ROLE["new"][2], True, "middle")
    s.path("M%s 122 L%s 122" % (cx0 + 102, cx0 + 116))
    s.path("M%s 142 L%s 142" % (cx0 + 118, cx0 + 104))
    s.text(cx0 + 110, 100, "buy: -p", 12, SUB, False, "middle")
    s.text(cx0 + 110, 166, "sell: +p", 12, SUB, False, "middle")
    s.text(cx0, 196, "hold = max(hold, -p)", 14, TEXT, True)
    s.text(cx0, 218, "cash = max(cash, hold + p)", 14, TEXT, True)
    s.text(cx0, 244, "只能买一次: hold = -lo", 12, SUB)
    s.text(40, 280, "brute force 对每个 j 重新往回扫一遍找最小值 → O(n²); 这个最小值是 prefix min, 一路带着走就是 O(n)。", 12, SUB)
    s.legend(310, [("new", "lo 所在日 (买)"), ("ring", "卖出日")])
    s.save(334, "Best Time to Buy and Sell Stock 的 prefix min 与状态机")


def core_coin():
    s = S("coin_core")
    s.text(40, 18, "coins = [1, 3, 4], amount = 6 · dp[a] = 凑出 a 最少要几枚 coin", 12, SUB)
    s.text(40, 38, "为什么要 DP: 贪心 (每次拿最大的) 会错; 要把 \"最后一枚拿哪个\" 全部试一遍", 12, SUB)
    s.text(40, 72, "贪心 4 → 1 → 1: 3 枚", 14, TEXT, True)
    for k, (v, role) in enumerate([(4, "del"), (1, "del"), (1, "del")]):
        s.circle(70 + k * 50, 112, 18, role)
        s.text(70 + k * 50, 112, str(v), 14, ROLE[role][2], True, "middle")
    s.text(40, 162, "最优 3 → 3: 2 枚", 14, TEXT, True)
    for k in range(2):
        s.circle(70 + k * 50, 202, 18, "new")
        s.text(70 + k * 50, 202, "3", 14, ROLE["new"][2], True, "middle")
    s.line(224, 60, 224, 330, DASH, "4 4", 0.8)
    s.text(246, 72, "dp[6] = 1 + min(dp[6-1], dp[6-3], dp[6-4])", 14, TEXT, True)
    ax, cw, y = 246, 58, 124
    vals = [0, 1, 2, 1, 1, 2, 2]
    # 7 cells * 58 = 406 -> 246..652
    for i, v in enumerate(vals):
        s.text(ax + i * cw + cw / 2, y - 14, "dp[%d]" % i, 12, SUB, False, "middle")
        s.cell(ax + i * cw + 1, y, cw - 2, 32, v, "new" if i == 6 else "old", False)
    for i in (5, 3, 2):
        s.ring(ax + i * cw + 1, y, cw - 2, 32)
    for src in (5, 3, 2):
        arrow_below(s, ax, cw, y + 32, src, 6)
    s.text(ax + 5.5 * cw, y + 62, "+1 (coin 1)", 12, SUB, False, "middle")
    s.text(ax + 3.7 * cw, y + 78, "+1 (coin 3)", 12, SUB, False, "middle")
    s.text(ax + 2.0 * cw, y + 62, "+1 (coin 4)", 12, SUB, False, "middle")
    s.text(246, 238, "dp[6] = 1 + min(2, 1, 2) = 2", 16, TEXT, True)
    s.text(246, 268, "每枚 coin 可以无限次用: dp[a-c] 里可能已经用过 c", 12, SUB)
    s.text(246, 288, "→ unbounded; 不用记 \"用过哪些\", 只记 \"凑出 a 的最少枚数\"", 12, SUB)
    s.legend(332, [("del", "贪心的选择"), ("new", "最优 / 要算的 dp[6]"), ("ring", "候选依赖的格子")])
    s.save(356, "Coin Change: 贪心错在哪, dp 试遍最后一枚")


def core_change():
    s = S("change_core")
    s.text(40, 18, "coins = [1, 2], amount = 3 · 组合 (combination) 不分顺序: 1+2 和 2+1 是同一种", 12, SUB)
    s.text(40, 38, "外层 for 谁, 决定了 \"同一个组合被数几次\"", 12, SUB)
    s.text(40, 72, "外层 amount → 数的是排列 (顺序不同算不同)", 14, TEXT, True)
    perms = ["1+1+1", "1+2", "2+1"]
    for k, t in enumerate(perms):
        role = "del" if t == "2+1" else "old"
        s.rect(60 + k * 130, 92, 110, 34, role)
        s.text(60 + k * 130 + 55, 109, t, 14, ROLE[role][2], True, "middle")
    s.text(60 + 3 * 130, 109, "= 3 种", 14, TEXT, True)
    s.text(60, 144, "1+2 和 2+1 被数了两次 (红)。每个 a 都把所有 coin 当 \"最后一枚\" → 顺序都被区分", 12, SUB)
    s.text(40, 192, "外层 coin → 数的是组合 (coin 的使用顺序固定: 先 1 后 2)", 14, TEXT, True)
    dp1 = [1, 1, 1, 1]
    dp2 = dp1[:]
    for a in range(2, 4):
        dp2[a] += dp2[a - 2]
    assert dp2 == [1, 1, 2, 2]
    ax, cw = 150, 52
    for i in range(4):
        s.text(ax + i * cw + cw / 2, 222, "dp[%d]" % i, 12, SUB, False, "middle")
    s.text(40, 252, "只用 coin 1", 12, SUB)
    mini_cells(s, ax, 236, cw, dp1, ["old"] * 4)
    s.ring(ax + 1, 236, cw - 2, 30)
    s.ring(ax + cw + 1, 236, cw - 2, 30)
    s.text(40, 322, "再加入 coin 2", 12, SUB)
    mini_cells(s, ax, 306, cw, dp2, ["old", "old", "new", "new"])
    s.path("M%s 268 L%s 304" % (ax + 26, ax + 2 * cw + 20))
    s.path("M%s 268 L%s 304" % (ax + cw + 26, ax + 3 * cw + 20))
    s.text(390, 252, "dp[2] = 1 + dp[0] = 2", 14, TEXT, True)
    s.text(390, 276, "dp[3] = 1 + dp[1] = 2", 14, TEXT, True)
    s.text(390, 322, "答案 dp[3] = 2: {1,1,1} {1,2}", 14, TEXT, True)
    s.text(40, 366, "coin 2 只会被加在 \"已经用完 coin 1\" 的方案后面, 不会出现 2+1 → 每个组合恰好数一次", 12, SUB)
    s.legend(396, [("old", "旧值"), ("new", "加入 coin 2 后更新"), ("del", "重复数的排列")])
    s.save(420, "Coin Change II: 为什么外层是 coin")


def core_partition():
    s = S("partition_core")
    s.text(40, 18, "nums = [2], target = 4 · dp[c] = 能不能凑出和 c · 正确答案: 只有一个 2, 凑不出 4 → dp[4] = F", 12, SUB)
    s.text(40, 38, "同一个 x 一轮里只能用一次 (0/1)。顺序决定 dp[c - x] 读到的是旧值还是已用过 x 的新值", 12, SUB)
    cw = 40
    yend = 0
    for px, title, order, bad in ((40, "正序 c = 2 → 4 (错)", [2, 3, 4], True), (360, "倒序 c = 4 → 2 (对)", [4, 3, 2], False)):
        s.text(px, 72, title, 14, TEXT, True)
        dp = [True, False, False, False, False]
        for i in range(5):
            s.text(px + 60 + i * cw + cw / 2, 94, "c=%d" % i, 12, SUB, False, "middle")
        y = 104
        s.text(px, y + 15, "init", 12, SUB)
        mini_cells(s, px + 60, y, cw, ["T" if v else "F" for v in dp], ["new" if v else "old" for v in dp], ch=30, size=14)
        y += 66
        for c in order:
            old = dp[:]
            src = c - 2
            before = dp[c]
            dp[c] = dp[c] or dp[src]
            ch = dp[c] and not before
            roles = ["old"] * 5
            if ch:
                roles[c] = "del" if (bad and c == 4) else "new"
            s.text(px, y + 15, "c = %d" % c, 12, SUB)
            mini_cells(s, px + 60, y, cw, ["T" if v else "F" for v in dp], roles, ch=30, size=14, rings=[src])
            s.text(px + 60, y + 46, "dp[%d] |= dp[%d] = %s" % (c, src, "T" if old[src] else "F"), 12, SUB)
            y += 74
        assert dp[4] == bad
        yend = y
    s.text(40, yend + 14, "正序: c=2 时 dp[2] 变 T (用了一个 2); c=4 时读 dp[2], 这个 T 已含 2 → 同一个 2 用了两次 (红)", 12, SUB)
    s.text(40, yend + 36, "倒序: c=4 时 dp[2] 还是 F (旧值, 没用过 x) → 每个 x 最多用一次", 12, SUB)
    s.text(40, yend + 58, "unbounded (Coin Change) 要的正是正序: 允许同一枚 coin 重复用。", 12, SUB)
    s.legend(yend + 92, [("new", "新变 True"), ("del", "错误的 True"), ("ring", "被读取的 dp[c - 2]")])
    s.save(yend + 116, "0/1 knapsack: 为什么倒序遍历 capacity")


def core_wordbreak():
    s = S("wordbreak_core")
    s.text(40, 18, "dp[i] = s 的前 i 个字符 s[:i] 能不能切成词典里的词 · 最后一个词 s[j:i] 的起点 j 全部试一遍", 12, SUB)
    s.text(40, 38, "s = \"catsand\", words = {cat, cats, and, sand} · 求 dp[7]", 12, SUB)
    s_ = "catsand"
    cw = 60
    ax = 100
    y = 92
    for i, ch in enumerate(s_):
        s.cell(ax + i * cw + 1, y, cw - 2, 34, ch, "old", False, 16)
    for i in range(8):
        s.text(ax + i * cw, y + 50, str(i), 12, SUB, False, "middle")
    s.text(40, y + 17, "s", 12, SUB)
    s.text(40, y + 50, "切点", 12, SUB)

    def seg(x1, x2, yy, label, role):
        s.rect(x1, yy, x2 - x1, 30, role)
        s.text((x1 + x2) / 2, yy + 15, label, 14, ROLE[role][2], True, "middle")
    yy = y + 78
    s.text(40, yy + 15, "j = 4", 14, TEXT, True)
    seg(ax + 2, ax + 4 * cw - 2, yy, "dp[4] = True  (cats)", "new")
    seg(ax + 4 * cw + 2, ax + 7 * cw - 2, yy, "\"and\" ∈ 词典", "old")
    s.ring(ax + 2, yy, 4 * cw - 4, 30)
    yy2 = yy + 54
    s.text(40, yy2 + 15, "j = 3", 14, TEXT, True)
    seg(ax + 2, ax + 3 * cw - 2, yy2, "dp[3] = True", "new")
    seg(ax + 3 * cw + 2, ax + 7 * cw - 2, yy2, "\"sand\" ∈ 词典", "old")
    s.ring(ax + 2, yy2, 3 * cw - 4, 30)
    s.text(40, yy2 + 66, "dp[7] = any(dp[j] and s[j:7] in words for j in range(7)) = True", 16, TEXT, True)
    s.text(40, yy2 + 96, "子问题是 \"前缀\" s[:j]: 前缀只有 n+1 个, 每个只判断一次。递归 brute force 会反复切同一段后缀。", 12, SUB)
    s.text(40, yy2 + 116, "brute force 每个切点 切/不切 → O(2ⁿ); dp: n 个 i × n 个 j × 子串 hash O(n) → O(n³), 限制词长后更快。", 12, SUB)
    s.legend(yy2 + 148, [("new", "前缀 s[:j] 能切"), ("old", "最后一块是词"), ("ring", "被依赖的 dp[j]")])
    s.save(yy2 + 172, "Word Break: dp[i] = 前 i 个字符能否切分")


def core_lis():
    s = S("lis_core")
    s.text(40, 18, "dp[i] = 以 nums[i] 结尾的 LIS 长度 · 和 Kadane 一样, 规定 \"以 i 结尾\" 才能接上前面的子问题", 12, SUB)
    s.text(40, 38, "nums[i] 前面可以接任何 j < i 且 nums[j] < nums[i] 的 LIS → 取 dp[j] 最大的 + 1", 12, SUB)
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    dp = [1, 1, 1, 2, 2, 3, 4, 4]
    cw = 54
    ax = 120
    y = 90
    s.text(40, y + 16, "nums", 12, SUB)
    s.text(40, y + 62, "dp", 12, SUB)
    for i in range(8):
        s.text(ax + i * cw + cw / 2, y - 14, "i=%d" % i, 12, SUB, False, "middle")
        s.cell(ax + i * cw + 1, y, cw - 2, 30, nums[i], "old", False)
        s.cell(ax + i * cw + 1, y + 46, cw - 2, 30, dp[i] if i <= 5 else "", "new" if i == 5 else ("old" if i < 5 else "empty"), False)
    for j in (2, 3, 4):
        s.ring(ax + j * cw + 1, y + 46, cw - 2, 30)
    for j in (2, 3, 4):
        arrow_below(s, ax, cw, y + 76, j, 5)
    s.text(ax, y + 118, "nums[2..4] = 2, 5, 3 都 < nums[5] = 7  →  它们的 dp = 1, 2, 2", 14, TEXT)
    s.text(ax, y + 142, "dp[5] = 1 + max(1, 2, 2) = 3", 16, TEXT, True)
    s.text(40, y + 176, "10, 9 > 7, 不能接: 递增要求 nums[j] < nums[i]。dp[i] 至少是 1 (只取自己)。", 12, SUB)
    s.text(40, y + 198, "最终答案是 max(dp), 因为 LIS 不一定以最后一个元素结尾。", 12, SUB)
    s.text(40, y + 220, "双层循环 → O(n²)。另有 patience / tails + binary search 的 O(n log n) 做法 (文末一句话)。", 12, SUB)
    s.legend(y + 252, [("new", "要算的 dp[5]"), ("ring", "nums[j] < nums[5] 的 dp[j]")])
    s.save(y + 276, "LIS: dp[i] = 以 i 结尾, 往回看所有 j")


def make_svgs():
    core_first()
    core_climb()
    core_rob()
    core_rob2()
    core_kadane()
    core_prod()
    core_stock()
    core_coin()
    core_change()
    core_partition()
    core_wordbreak()
    core_lis()
    tr_climb()
    tr_rob()
    tr_rob2()
    tr_kadane()
    tr_prod()
    tr_stock()
    tr_coin()
    tr_change()
    tr_partition()
    tr_wordbreak()
    tr_lis()


def build_doc():
    doc = d.Doc("14 · Dynamic Programming (1): 1D DP / Knapsack")
    doc.main("主线: DP = 带记忆的递归。大问题拆成少数几个更小的子问题, 同一个子问题只算一次。"
             "1D DP 的全部变化只有两处: state 怎么定义, transition 怎么写。")
    doc.main("概念链: Climbing Stairs (dp[i-1] + dp[i-2]) → House Robber (选 / 不选) → House Robber II (环 = 两次线性) "
             "→ Maximum Subarray (state = 以 i 结尾) → Maximum Product Subarray (同时维护 max 和 min) "
             "→ Best Time to Buy and Sell Stock (到目前为止的最小值 / 状态机) → Coin Change (unbounded, 求最少个数) "
             "→ Coin Change II (unbounded, 数组合: 外层 coin) → Partition Equal Subset Sum (0/1, 倒序) "
             "→ Word Break (dp[i] = 前 i 个字符) → Longest Increasing Subsequence (往回看所有 j)")

    # ---------------- 0
    doc.h2("0. 第一性原理: 递归在重复算同一件事, DP 让每个子问题只算一次")
    doc.p("从最朴素的写法开始。Climbing Stairs: 每次走 1 阶或 2 阶, 到第 n 阶有几种走法? "
          "最后一步只有两种 (从 n-1 走 1 阶, 或从 n-2 走 2 阶), 所以 <code>f(n) = f(n-1) + f(n-2)</code>。直接写成递归:")
    doc.code(CODE["brute"])
    doc.p("Brute force 的 complexity 是 O(2ⁿ): 每次调用拆成两个调用。浪费在哪里? 看递归树 (下图): "
          "f3 被展开了 2 次, f2 被展开了 3 次, f1 被展开了 5 次。"
          "<b>不同的子问题只有 n+1 个</b> (f0 … fn), 但调用次数是指数级。每个 f(k) 的值只取决于 k, 重复算只是在浪费。")
    doc.svg("14-dp-1d/first_principles_core.svg",
            "左: 递归树里红色节点是已经算过的重复子问题; 右: 同一个递归关系填成表, 每格只算一次, dp[5] 只读 dp[4] 和 dp[3]。")
    doc.p("消掉浪费有三步, 每一步都是上一步的小改动:")
    doc.h3("① memoization: 加 @cache")
    doc.code(CODE["memo"])
    doc.p("第一次算 f(k) 时把结果存起来, 之后直接查。不同的 k 只有 n+1 个, 每个 O(1) → O(n) time, O(n) space (cache + 递归栈)。")
    doc.h3("② bottom-up table: 把递归改写成循环")
    doc.code(CODE["table"])
    doc.p("memo 的递归其实是在 \"从大 n 往小 n 要答案\"; 改成从小到大先把依赖的格子填好, 就不需要递归栈了。这就是 DP 四步:")
    doc.p("<b>state</b> (dp[i] 代表什么) → <b>transition</b> (dp[i] 怎么由更小的 dp 得到) → <b>base case</b> (最小的格子是多少) → "
          "<b>计算顺序</b> (保证依赖的格子先填好)。写 DP 前先把这四句话说出来, 代码是自然的。")
    doc.h3("③ 滚动变量: 只依赖前几个值时 O(1) space")
    doc.code(CODE["rolling"])
    doc.p("dp[i] 只读 dp[i-1] 和 dp[i-2], 更早的格子永远不会再被读 → 用两个变量滚动。这个优化在本文里反复出现 (Robber, Kadane, Stock)。")
    doc.h3("1D DP 的 state 常见三种形状")
    doc.raw("<table><tr><th>state 形状</th><th>含义</th><th>本文的题</th></tr>"
            "<tr><td><code>dp[i]</code> = 前 i 个 / 到 i 为止的最优</td><td>到第 i 个为止, 不要求用到第 i 个</td><td>Climbing Stairs, House Robber, Word Break</td></tr>"
            "<tr><td><code>dp[i]</code> = 以 i 结尾的最优</td><td>必须包含第 i 个, 这样才能接上前面</td><td>Kadane, Max Product, LIS</td></tr>"
            "<tr><td><code>dp[a]</code> = 容量 / 金额 a 下的答案</td><td>下标不是位置, 是 \"还剩多少额度\"</td><td>Coin Change (I, II), Partition (knapsack)</td></tr></table>")
    doc.note("DP = 递归树里有重复子问题 + 子问题的个数是多项式。先写 recursion, 找出 state, 再决定 memo 还是 table, 最后看能不能滚动。")

    # ---------------- 1 Climbing
    doc.h2("1. Climbing Stairs: dp[i] = dp[i-1] + dp[i-2]")
    doc.p("题目: 一次走 1 或 2 阶, 到第 n 阶有几种走法? 例: n = 5 → 8。")
    doc.p("Brute force: 递归, O(2ⁿ), 浪费在重复子问题 (见第 0 节)。")
    doc.p("关键观察: 到第 i 阶的最后一步只有两种, 互斥且穷尽, 所以方法数相加。state 是 \"到第 i 阶的方法数\", 只依赖前两格。")
    doc.svg("14-dp-1d/climb_core.svg", "最后一步只有两种, 直接相加; 只读前两格, 所以两个变量滚动。")
    doc.svg("14-dp-1d/climb_trace.svg", "n = 5 的 trace: base 两格, 之后每一格 = 前两格相加, 最后 dp[5] = 8。")
    doc.code(CODE["climb"])
    doc.p("Time O(n): 循环 n-1 次。Space O(1): 只有 a, b 两个变量。")
    doc.note("相加型 transition: 最后一步有 k 种 (互斥且穷尽) → dp[i] = 各个来源之和。依赖前 k 个 → k 个变量滚动。")

    # ---------------- 2 Rob
    doc.h2("2. House Robber: 每一步 \"选 / 不选\"")
    doc.p("题目: 一排房子, 相邻的房子不能同时偷, 最多偷到多少钱? 例: nums = [2, 3, 9, 3, 1] → 12 (2 + 9 + 1)。")
    doc.p("Brute force: 每间房子偷 / 不偷, 2ⁿ 种, 检查相邻 → O(2ⁿ)。浪费: 决定了前面几间之后, 后面的最优和 \"前面具体偷了哪几间\" 无关, 只和 \"最后停在哪\" 有关, 却被重复求。")
    doc.p("相比上一题: transition 从 \"相加\" 变成 \"取较大者 max\", 多了一个选择。看第 i 间: 不偷就是 dp[i-1]; 偷就必须跳过 i-1, 接在 dp[i-2] 后面。")
    doc.svg("14-dp-1d/rob_core.svg", "dp[2] = max(dp[1], dp[0] + nums[2]) = max(3, 2 + 9) = 11: 两个选择覆盖了全部最优方案。")
    doc.svg("14-dp-1d/rob_trace.svg", "nums = [2, 3, 9, 3, 1] 的 trace: 每一格的算式都写出来, 橙色 ring 是它读取的两个格子。")
    doc.code(CODE["rob"])
    doc.p("Time O(n), Space O(1) (两个滚动变量)。")
    doc.note("选 / 不选 型: dp[i] = max(不选 i → dp[i-1], 选 i → dp[i-2] + 收益)。\"选了 i 就不能选 i-1\" 体现在跳到 i-2。")

    # ---------------- 3 Rob II
    doc.h2("3. House Robber II: 环 = 两次线性")
    doc.p("题目: 房子排成一圈, 第一间和最后一间也相邻。例: nums = [2, 3, 9, 3, 1] → 11。")
    doc.p("Brute force: 2ⁿ。相比上一题只多了一个条件: 首尾不能同时偷。")
    doc.p("关键观察: 首尾至少有一个不偷。不偷最后一间 → 线性问题 nums[:-1]; 不偷第一间 → 线性问题 nums[1:]。两个都是上一题, 取较大者。"
          "改动只有一行: 调用两次 rob。")
    doc.svg("14-dp-1d/rob2_core.svg", "把环切成两个线性问题: 红色的是这一轮不偷的那间。")
    doc.svg("14-dp-1d/rob2_trace.svg", "两次线性 DP: A = 11, B = 10, 答案 11。")
    doc.code(CODE["rob2"])
    doc.p("Time O(n) (两次扫描), Space O(1) (切片会拷贝 O(n), 想省的话传下标范围)。")
    doc.note("环 / 首尾相邻 → 拆成两个线性问题, 各排除一端, 取 max。不要去改 DP 本身。")

    # ---------------- 4 Kadane
    doc.h2("4. Maximum Subarray (Kadane): state = 以 i 结尾")
    doc.p("题目: 连续 subarray 的最大和。例: nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4] → 6 ([4, -1, 2, 1])。")
    doc.p("Brute force: 枚举所有 (i, j), 用 prefix sum 求和 → O(n²)。浪费: 以 j 结尾的各个 subarray 之间有大量重叠, 每次都从头加。")
    doc.p("关键观察: 如果规定 subarray <b>必须以 i 结尾</b>, 那它只有两种形状: 只有 nums[i] 自己 (重开), 或者接在以 i-1 结尾的最优 subarray 后面。"
          "和上一题不同: state 不是 \"前 i 个的最优\", 而是 \"以 i 结尾的最优\", 因为 subarray 必须连续, 没有 \"结尾\" 就接不上。答案要对所有 i 取最大。")
    doc.svg("14-dp-1d/kadane_core.svg", "cur[3]: 接在 cur[2] = -2 后面只有 2, 重开是 4 → 取 4。")
    doc.svg("14-dp-1d/kadane_trace.svg", "9 个数的完整 trace: cur 数组每步一格, best 记录出现过的最大值。")
    doc.code(CODE["kadane"])
    doc.p("Time O(n), Space O(1)。")
    doc.note("连续 subarray + 求最优 → state = \"以 i 结尾\", 要么接上, 要么重开; 答案是所有 i 里的最大, 不是最后一个。")

    # ---------------- 5 Max product
    doc.h2("5. Maximum Product Subarray: 同时维护 max 和 min")
    doc.p("题目: 连续 subarray 的最大乘积。例: nums = [2, -3, -2, 4] → 48 (整个数组)。")
    doc.p("Brute force: O(n²)。相比 Kadane: 把 + 换成 ×, 但乘法有个新问题 — 负数会翻转大小。")
    doc.p("关键观察: 以 i 结尾的最大乘积, 可能来自 \"以 i-1 结尾的最<b>小</b>乘积\" × 负数 x。所以 state 要两个: mx (以 i 结尾的最大) 和 mn (最小)。"
          "改动: Kadane 的一个 cur 变成 (mx, mn); 候选从 2 个变成 3 个 (x, mx × x, mn × x)。")
    doc.svg("14-dp-1d/prod_core.svg", "x < 0 时 mx 和 mn 交叉: 旧的 mn 乘负数变成新的 mx。")
    doc.svg("14-dp-1d/prod_trace.svg", "每一步写出三个候选, mx 取最大, mn 取最小; 两个数组都用上一格的旧值。")
    doc.code(CODE["prod"])
    doc.p("Time O(n), Space O(1)。遇到 0: 候选里有 x 本身 (重开), mx, mn 都会被重置成 0, 不需要特判。")
    doc.note("乘法 / 有符号的 DP: 最大值依赖最小值 → 同时维护 max 和 min。")

    # ---------------- 6 Stock
    doc.h2("6. Best Time to Buy and Sell Stock: 到目前为止的最小值")
    doc.p("题目: 买一次、卖一次 (先买后卖), 最大利润。例: prices = [7, 1, 5, 3, 6, 4] → 5 (1 买, 6 卖)。")
    doc.p("Brute force: 所有 (买日 i, 卖日 j > i) 对 → O(n²)。浪费: 对每个卖日 j, 最佳买日就是 j 之前最便宜的那天; 这个最小值每次都重新扫一遍。")
    doc.p("关键观察: \"j 之前的最小值\" 是 prefix min, 一路带着走即可。这也是 \"以 j 结尾\" 型: best[j] = max(best[j-1], prices[j] - lo)。")
    doc.svg("14-dp-1d/stock_core.svg", "左: 卖出日 6, 最佳买入就是之前的最低价 1; 右: 同一个问题的状态机写法 (hold / cash)。")
    doc.svg("14-dp-1d/stock_trace.svg", "lo 和 best 两个数组随 i 推进, 每步先用昨天的 lo 算今天卖的利润。")
    doc.code(CODE["stock"])
    doc.p("状态机写法 (为了以后的变体: 多次交易 / 冷冻期 / 手续费, 只改 transition 即可):")
    doc.code(CODE["stock_sm"])
    doc.p("Time O(n), Space O(1)。")
    doc.note("\"某个量之前的最小 / 最大\" 不用回头扫, 边走边维护。买卖股票类题统一用 hold / cash 状态机, 每个状态一个变量。")

    # ---------------- 7 Coin change
    doc.h2("7. Coin Change: unbounded knapsack, 求最少个数")
    doc.p("题目: coins 每种有无限枚, 凑出 amount 最少要几枚, 凑不出返回 -1。例: coins = [1, 3, 4], amount = 6 → 2 (3 + 3)。")
    doc.p("Brute force: 递归, 每一步试每种 coin → O(coins^amount) 级别。贪心 (先拿最大的) 是错的: 4 + 1 + 1 = 3 枚 > 3 + 3 = 2 枚。"
          "浪费: \"凑出 a 还需要最少几枚\" 只和 a 有关, 却被不同的路径重复算。")
    doc.p("关键观察: 这里的 state 是<b>金额</b> a (第三种形状)。枚举 \"最后一枚是哪种 coin c\": 剩下 a - c, 子问题 dp[a-c]。"
          "和 Robber 的 max 对应, 这里是 <code>1 + min</code>; 来源数量不是固定的 2 个, 而是 len(coins) 个。")
    doc.svg("14-dp-1d/coin_core.svg", "左: 贪心拿 4 会错; 右: dp[6] 试遍 coin 1 / 3 / 4 作为最后一枚, 取最小的 dp[6-c] + 1。")
    doc.svg("14-dp-1d/coin_trace.svg", "amount 从 1 填到 6: 每格读的格子数 = 不超过 a 的 coin 种数。")
    doc.code(CODE["coin"])
    doc.p("Time O(amount × len(coins)): 每个 a 试每种 coin。Space O(amount)。同一种 coin 可以重复用, 因为 dp[a-c] 里可能已经用过 c — 这就是 unbounded。")
    doc.note("无限件 + 求最小 / 最大个数: dp[amount] = 1 + min(dp[amount - c]); 不可达用 inf; 外层 amount, 内层 coin。")

    # ---------------- 8 Coin change II
    doc.h2("8. Coin Change II: 数组合, 为什么外层是 coin")
    doc.p("题目: 同样的 coins, 凑出 amount 有几种<b>组合</b> (不分顺序)。例: coins = [1, 2, 5], amount = 5 → 4。")
    doc.p("Brute force: 枚举所有组合, 指数级。相比上一题: 从求 min 变成<b>数个数</b>, transition 从 min 变成 +=; 同时 \"1+2 和 2+1 是同一种\" 会让循环顺序变得重要。")
    doc.p("关键观察: 如果外层循环 amount、内层循环 coin, 每个 amount 都把所有 coin 当作 \"最后一枚\" → 1+2 和 2+1 被数两次 (数的是排列)。"
          "把外层改成 coin: 每种 coin 在一整轮里统一 \"加入\", 使用顺序固定为 coins 的顺序 → 每个组合只数一次。")
    doc.svg("14-dp-1d/change_core.svg", "coins = [1, 2], amount = 3: 外层 amount 数出 3 (含 1+2 和 2+1), 外层 coin 数出 2。")
    doc.svg("14-dp-1d/change_trace.svg", "每一行是处理完一种 coin 后的 dp 数组; 以 dp[5] 为例写出算式和对应的组合。")
    doc.code(CODE["change"])
    doc.p("Time O(amount × len(coins)), Space O(amount)。内层是正序, 所以同一种 coin 可重复用 (unbounded)。")
    doc.note("数 \"组合\" → 外层 coin; 数 \"排列\" → 外层 amount。内层正序 = 同一件物品可重复用。")

    # ---------------- 9 Partition
    doc.h2("9. Partition Equal Subset Sum: 0/1 knapsack, 为什么倒序")
    doc.p("题目: 能否把数组分成两个和相等的子集? 例: nums = [1, 2, 3, 4] → True ({1, 4} 和 {2, 3})。")
    doc.p("Brute force: 每个数放 A / 放 B, O(2ⁿ)。先化简: 总和 total 是奇数就不可能; 否则问题变成 \"能不能挑出一些数, 和恰好 = total/2\"。")
    doc.p("关键观察: 这是 0/1 knapsack: 每个数只能用一次。state 是 dp[c] = 当前处理过的数里能不能凑出 c。"
          "和 Coin Change II 的结构几乎一样 (外层物品, 内层容量), 唯一的改动: <b>内层改成倒序</b>。")
    doc.svg("14-dp-1d/partition_core.svg", "nums = [2], target = 4: 正序会把同一个 2 用两次 (dp[4] 错成 T); 倒序读到的 dp[c-x] 还是旧值。")
    doc.svg("14-dp-1d/partition_trace.svg", "nums = [1, 2, 3, 4], target = 5: 每个 x 倒着扫 c, 新变 True 的格子都写出依赖的 dp[c-x]。")
    doc.code(CODE["partition"])
    doc.p("Time O(n × target), Space O(target)。这是 pseudo-polynomial: 和 target 的数值大小成正比, 不是和输入的位数。")
    doc.note("每件物品只能用一次 (0/1) → 内层 capacity 倒序; 可无限次 (unbounded) → 内层正序。dp[c - x] 要读 \"处理 x 之前\" 的旧值。")

    # ---------------- 10 Word break
    doc.h2("10. Word Break: dp[i] = 前 i 个字符能否切分")
    doc.p("题目: s 能否切成若干个词典里的词? 例: s = \"catsand\", words = [cat, cats, and, sand] → True。")
    doc.p("Brute force: 递归, 每个位置试每个前缀词, 一路切下去 → O(2ⁿ)。浪费: 后缀 s[j:] 能不能切, 和前面是怎么切到 j 的无关, 却被重复判断。")
    doc.p("关键观察: state 是前缀 dp[i] (第一种形状), 但 transition 不再是 \"前一两格\": 枚举<b>最后一个词</b> s[j:i] 的起点 j, "
          "要求前面 dp[j] 为 True 且 s[j:i] 在词典里。来源是任意个 j, 不是固定的 2 个, 所以没法滚动成 O(1) space。")
    doc.svg("14-dp-1d/wordbreak_core.svg", "dp[7]: 最后一块 \"and\" 配 dp[4], 或最后一块 \"sand\" 配 dp[3]; 任一成立即 True。")
    doc.svg("14-dp-1d/wordbreak_trace.svg", "i 从 1 到 7: 只试 dp[j] 为 True 的 j, 切出的最后一块在不在词典里。")
    doc.code(CODE["wordbreak"])
    doc.p("Time O(n²) 个 (j, i) 对, 每次切片 + hash 是 O(n) → O(n³) (限制 j 的范围到最长词长可降到 O(n × L²))。Space O(n) + 词典。")
    doc.note("\"能否切分 / 划分\" → dp[i] = 前 i 个能否; 枚举最后一块的起点 j, 子问题是前缀 dp[j]。")

    # ---------------- 11 LIS
    doc.h2("11. Longest Increasing Subsequence: 以 i 结尾 + 往回看所有 j")
    doc.p("题目: 最长严格递增子序列 (不要求连续) 的长度。例: nums = [10, 9, 2, 5, 3, 7, 101, 18] → 4。")
    doc.p("Brute force: 每个元素取 / 不取, 2ⁿ。相比 Kadane: subarray 必须连续, 所以只能接在 i-1 后面 (一个来源); "
          "subsequence 不连续, nums[i] 可以接在任何一个更小的 nums[j] 后面 (j 的个数是 i 个)。")
    doc.p("关键观察: 沿用 \"以 i 结尾\" 的 state: dp[i] = 以 nums[i] 结尾的 LIS 长度。transition: 往回看所有 j < i, 满足 nums[j] < nums[i] 的取 dp[j] 最大的 + 1。")
    doc.svg("14-dp-1d/lis_core.svg", "dp[5]: nums[2..4] 都比 7 小, 它们的 dp 是 1, 2, 2 → 取 2, 加 1 = 3。")
    doc.svg("14-dp-1d/lis_trace.svg", "8 个元素逐个算 dp: 橙色 ring 是满足 nums[j] < nums[i] 的 dp[j], 箭头指向取最大的那个。")
    doc.code(CODE["lis"])
    doc.p("Time O(n²): 双层循环。Space O(n)。另有 patience sorting 的 O(n log n) 做法, 一句话: tails[k] 维护 \"长度为 k+1 的递增子序列的最小结尾\", 对每个 x 用 binary search 找位置替换:")
    doc.code(CODE["lis_fast"])
    doc.note("子序列 (不连续) + 递增 / 有序关系 → dp[i] = 以 i 结尾, 往回扫所有 j; 想快就用 tails + bisect。")

    # ---------------- 识别信号
    doc.h2("识别信号: 看到什么 → 试什么")
    doc.raw("<table><tr><th>特征</th><th>做法</th><th>complexity</th></tr>"
            "<tr><td>求 最优 / 方法数 / 能不能, 暴力递归的子问题大量重复</td><td>找 state → memo 或 bottom-up table</td><td>O(2ⁿ) → O(state 数 × transition 数)</td></tr>"
            "<tr><td>dp[i] 只读 dp[i-1], dp[i-2]</td><td>滚动变量</td><td>space O(n) → O(1)</td></tr>"
            "<tr><td>相邻不能选 / 选或不选</td><td>dp[i] = max(dp[i-1], dp[i-2] + x); 环就切成两次线性</td><td>O(2ⁿ) → O(n)</td></tr>"
            "<tr><td>连续 subarray 的最优</td><td>state = 以 i 结尾: 接上或重开 (Kadane); 乘法加一个 min</td><td>O(n²) → O(n)</td></tr>"
            "<tr><td>某个量之前的最小 / 最大 (买卖股票)</td><td>prefix min 一路带着; 多种状态用 hold / cash 状态机</td><td>O(n²) → O(n)</td></tr>"
            "<tr><td>物品无限次, 求最少个数</td><td>dp[a] = 1 + min(dp[a-c]); 外层 a 内层 coin</td><td>指数 → O(amount × coins)</td></tr>"
            "<tr><td>物品无限次, 数组合</td><td>外层 coin, 内层 a 正序; 数排列则外层 a</td><td>指数 → O(amount × coins)</td></tr>"
            "<tr><td>物品只能用一次, 凑目标和 (subset sum)</td><td>外层物品, 内层 capacity 倒序</td><td>O(2ⁿ) → O(n × target)</td></tr>"
            "<tr><td>字符串 / 数组 能否划分成合法的块</td><td>dp[i] = 前 i 个能否; 枚举最后一块起点 j</td><td>O(2ⁿ) → O(n²)</td></tr>"
            "<tr><td>不连续的子序列 + 递增 / 有序</td><td>dp[i] = 以 i 结尾, 往回看 j; 更快用 tails + bisect</td><td>O(2ⁿ) → O(n²) → O(n log n)</td></tr></table>")
    doc.h2("以后再学")
    doc.p("2D DP (grid, 两个 string: LCS / Edit Distance) 在 15 doc; 带冷冻期 / 手续费 / 最多 k 次的股票题只是状态机多几个状态; "
          "bitmask DP、数位 DP、DP 优化 (单调队列 / convex hull) 不常考, 这里不展开。")
    doc.write("docs/%s.html" % SLUG)


if __name__ == "__main__":
    selftest()
    make_svgs()
    build_doc()
