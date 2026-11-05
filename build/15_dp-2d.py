"""15 · Dynamic Programming (2): Grid / Two Strings / Interval
运行: cd build && python3 -I 15_dp-2d.py
同时生成 docs/svg/15-dp-2d/*.svg (数字全部由真实 dp 计算得到) 和 docs/15-dp-2d.html
"""
import html as _html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import doclib as d  # noqa: E402

SLUG = "15-dp-2d"
SVG_DIR = os.path.join(d.ROOT, "docs", "svg", SLUG)

# ----------------------------------------------------------------------------
# 文档里出现的所有代码 (测试脚本会 exec 这些字符串, 和暴力解对拍)
# ----------------------------------------------------------------------------
CODE = {}

CODE["template"] = '''
def solve(A, B):                       # A, B: 两个 string / 一个 grid 的行列
    m, n = len(A), len(B)
    # dp[i][j] = 只看 A 的前 i 个、B 的前 j 个时, 子问题的答案  (两个 index → 2D)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    # base: dp[0][*] 和 dp[*][0] = 其中一边为空时的答案 (先填好)
    for i in range(1, m + 1):          # 填表顺序 = 依赖的反方向:
        for j in range(1, n + 1):      #   dp[i][j] 依赖 (i-1, j) (i, j-1) (i-1, j-1)
            # 问 "最后一步做了什么"? 每种选择 → 一个更小的子问题 → 取 min / max / sum
            dp[i][j] = f(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[m][n]                    # 答案在右下角

# 滚动数组: dp[i] 只读 dp[i-1] → 只留 prev, cur 两行, space O(m*n) → O(n)
'''

CODE["unique_paths"] = '''
def unique_paths(m, n):
    dp = [[1] * n for _ in range(m)]          # 第 0 行 / 第 0 列只有 1 种走法 (一直直走)
    for i in range(1, m):
        for j in range(1, n):
            # 最后一步要么从上面 (i-1, j) 下来, 要么从左边 (i, j-1) 过来
            # 两类路径互不重叠, 而且已经包含了所有路径 → 相加
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[m - 1][n - 1]

def unique_paths_1row(m, n):                  # 滚动数组: 只依赖上一行 → 一维就够
    row = [1] * n                             # row 当前代表 "上一行"
    for _ in range(m - 1):
        for j in range(1, n):
            row[j] += row[j - 1]              # row[j] 旧值 = 上面, row[j-1] 新值 = 左边
    return row[-1]
'''

CODE["min_path_sum"] = '''
def min_path_sum(grid):
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = grid[0][0]
    for j in range(1, n):                     # 第 0 行: 只能从左边来
        dp[0][j] = dp[0][j - 1] + grid[0][j]
    for i in range(1, m):                     # 第 0 列: 只能从上面来
        dp[i][0] = dp[i - 1][0] + grid[i][0]
    for i in range(1, m):
        for j in range(1, n):
            # 改的就是这一行: 相加 → min。到 (i, j) 的最小和 = 两个来路里小的那个 + 自己
            dp[i][j] = min(dp[i - 1][j], dp[i][j - 1]) + grid[i][j]
    return dp[m - 1][n - 1]

def min_path_sum_1row(grid):                  # 滚动数组: inf 当哨兵, 不用单独处理第 0 行
    n = len(grid[0])
    row = [float("inf")] * n
    row[0] = 0
    for r in grid:
        row[0] += r[0]                        # 第 0 列: 只能从上面来
        for j in range(1, n):
            row[j] = min(row[j], row[j - 1]) + r[j]   # 旧 row[j] = 上, row[j-1] = 左
    return row[-1]
'''

CODE["maximal_square"] = '''
def maximal_square(matrix):                   # matrix 里是 "0" / "1" 字符
    m, n = len(matrix), len(matrix[0])
    # dp[i][j] = 以 matrix[i-1][j-1] 为右下角的全 1 正方形, 最大边长
    dp = [[0] * (n + 1) for _ in range(m + 1)]    # 多一圈 0 当边界, 省掉 if i == 0
    best = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if matrix[i - 1][j - 1] == "1":
                # 上 / 左 / 左上 三个邻居里最小的那个, 决定先撞墙的方向 → 边长 = 最小 + 1
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
                best = max(best, dp[i][j])
            # 是 "0" 就保持 0: 这个格子不能当任何正方形的右下角
    return best * best                        # 题目要面积
'''

CODE["lcs"] = '''
def longest_common_subsequence(text1, text2):
    m, n = len(text1), len(text2)
    # dp[i][j] = text1[:i] 和 text2[:j] 的 LCS 长度
    dp = [[0] * (n + 1) for _ in range(m + 1)]    # dp[0][*] = dp[*][0] = 0: 有一边是空串
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                # 最后一个字符相同 → 一定可以配对, 去掉这一对, 看左上角
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                # 不同 → 至少有一个字符没用上: 丢 text1 的最后一个, 或丢 text2 的最后一个
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]

def lcs_2rows(text1, text2):                  # 滚动数组: 只留上一行 prev 和当前行 cur
    n = len(text2)
    prev = [0] * (n + 1)
    for ch in text1:
        cur = [0] * (n + 1)
        for j in range(1, n + 1):
            if ch == text2[j - 1]:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = max(prev[j], cur[j - 1])
        prev = cur
    return prev[n]
'''

CODE["edit_distance"] = '''
def min_distance(word1, word2):
    m, n = len(word1), len(word2)
    # dp[i][j] = word1[:i] 变成 word2[:j] 的最少操作数
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i                          # word1[:i] → "": 删 i 次
    for j in range(n + 1):
        dp[0][j] = j                          # "" → word2[:j]: 插 j 次
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]   # 最后一个字符已经一样: 不用操作, 白拿左上角
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j - 1],         # replace: 改成 word2[j-1], 两边各缩 1
                    dp[i - 1][j],             # delete:  删掉 word1[i-1], word1 缩短 1
                    dp[i][j - 1],             # insert:  在末尾补上 word2[j-1], word2 缩短 1
                )
    return dp[m][n]
'''

CODE["lps_expand"] = '''
def longest_palindrome(s):
    start, end = 0, 0                         # 当前最长 palindrome 的闭区间 [start, end]

    def expand(l, r):                         # 从中心往两边扩, 直到越界或两端不同
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        return l + 1, r - 1                   # 循环停下时 l, r 已经多走了一步, 退回来

    for c in range(len(s)):                   # 2n-1 个中心: n 个字符 + n-1 个缝
        for l, r in (expand(c, c), expand(c, c + 1)):   # 奇数长度 / 偶数长度
            if r - l > end - start:
                start, end = l, r
    return s[start:end + 1]
'''

CODE["lps_dp"] = '''
def longest_palindrome_dp(s):
    n = len(s)
    # dp[i][j] = s[i..j] (闭区间) 是不是 palindrome
    dp = [[False] * n for _ in range(n)]
    start, best = 0, 1
    for i in range(n - 1, -1, -1):            # i 从大到小: dp[i+1][j-1] 在 "下一行"
        for j in range(i, n):
            # 两端相同 + 里面 s[i+1..j-1] 也是 palindrome; 长度 <= 2 时里面是空的, 直接成立
            if s[i] == s[j] and (j - i < 2 or dp[i + 1][j - 1]):
                dp[i][j] = True
                if j - i + 1 > best:
                    start, best = i, j - i + 1
    return s[start:start + best]
'''

CODE["count_sub"] = '''
def count_substrings(s):
    count = 0
    for c in range(len(s)):
        for l, r in ((c, c), (c, c + 1)):     # 奇数中心 / 偶数中心
            while l >= 0 and r < len(s) and s[l] == s[r]:
                count += 1                    # 每成功扩一步 = 发现一个新的 palindrome
                l -= 1
                r += 1
    return count
'''

CODE["regex"] = '''
def is_match(s, p):
    m, n = len(s), len(p)
    # dp[i][j] = s[:i] 能不能被 p[:j] 完整匹配
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True                           # 空 pattern 匹配空 string
    for j in range(2, n + 1):                 # s 为空: 只有 "a*b*" 这类全匹配 0 次的能过
        if p[j - 1] == "*":
            dp[0][j] = dp[0][j - 2]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == "*":               # p[j-2] 是被 * 修饰的字符, 比如 "a*" 里的 a
                dp[i][j] = dp[i][j - 2]       # 选择 1: a* 匹配 0 次 → 把 "a*" 整个去掉
                if p[j - 2] in (s[i - 1], "."):
                    # 选择 2: a* 匹配 s[i-1] 这一个, 但 pattern 保留 (还能继续匹配更多)
                    dp[i][j] = dp[i][j] or dp[i - 1][j]
            elif p[j - 1] in (s[i - 1], "."):
                dp[i][j] = dp[i - 1][j - 1]   # 普通字符 / "." 匹配: 各吃一个
    return dp[m][n]
'''

# ----------------------------------------------------------------------------
# SVG 小工具
# ----------------------------------------------------------------------------
FONT = 'ui-sans-serif, system-ui, -apple-system, "PingFang SC", sans-serif'
C = dict(
    new=("#E1F5EE", "#0F6E56", "#085041"),
    rm=("#FAECE7", "#993C1D", "#712B13"),
    old=("#F1EFE8", "#5F5E5A", "#444441"),
    empty=("#FFFFFF", "#B4B2A9", "#B4B2A9"),
)
INK, SUB, RING, SEP = "#0B0B0B", "#52514E", "#EF9F27", "#B4B2A9"


def esc(s):
    return _html.escape(str(s), quote=False)


class S:
    def __init__(self, title, desc):
        self.title, self.desc = title, desc
        self.p = []

    def t(self, x, y, s, size=12, bold=False, fill=SUB, anchor="start"):
        w = ' font-weight="500"' if bold else ""
        a = "" if anchor == "start" else ' text-anchor="%s"' % anchor
        self.p.append('<text x="%s" y="%s" font-size="%d"%s%s fill="%s" '
                      'dominant-baseline="central">%s</text>'
                      % (x, y, size, w, a, fill, esc(s)))

    def rect(self, x, y, w, h, role="old", sw=0.5, rx=4, dash=None):
        f, s, _ = C[role]
        da = ' stroke-dasharray="%s"' % dash if dash else ""
        self.p.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" '
                      'stroke="%s" stroke-width="%s"%s/>' % (x, y, w, h, rx, f, s, sw, da))

    def ring(self, x, y, w, h, pad=3):
        self.p.append('<rect x="%s" y="%s" width="%s" height="%s" rx="6" fill="none" '
                      'stroke="%s" stroke-width="2.5"/>'
                      % (x - pad, y - pad, w + 2 * pad, h + 2 * pad, RING))

    def circle(self, cx, cy, r, role="old"):
        f, s, _ = C[role]
        self.p.append('<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" stroke-width="0.5"/>'
                      % (cx, cy, r, f, s))

    def line(self, x1, y1, x2, y2, color=SEP, sw=0.5, dash="4 4", arrow=False):
        da = ' stroke-dasharray="%s"' % dash if dash else ""
        mk = ' marker-end="url(#arrow)"' if arrow else ""
        self.p.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s%s/>'
                      % (x1, y1, x2, y2, color, sw, da, mk))

    def arrow(self, x1, y1, x2, y2, color=SUB, dash=None, sw=1.5):
        da = ' stroke-dasharray="%s"' % dash if dash else ""
        self.p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s '
                      'marker-end="url(#arrow)"/>' % (x1, y1, x2, y2, color, sw, da))

    def path(self, dstr, color=SUB, dash=None, sw=1.5, arrow=True):
        da = ' stroke-dasharray="%s"' % dash if dash else ""
        mk = ' marker-end="url(#arrow)"' if arrow else ""
        self.p.append('<path d="%s" fill="none" stroke="%s" stroke-width="%s"%s%s/>'
                      % (dstr, color, sw, da, mk))

    def cell(self, x, y, w, h, text, role="old", size=14, sub=None, bold=True):
        self.rect(x, y, w, h, role, dash="3 3" if role == "empty" else None)
        _, _, tc = C[role]
        if sub is None:
            self.t(x + w / 2, y + h / 2 + 1, text, size, bold, tc, "middle")
        else:
            self.t(x + 5, y + 8, sub, 12, False, tc, "start")
            self.t(x + w / 2 + 4, y + h - 10, text, size, bold, tc, "middle")

    def legend(self, y, items):
        x = 40
        for kind, label in items:
            if kind == "ring":
                self.p.append('<rect x="%s" y="%s" width="18" height="14" rx="3" fill="#F1EFE8" '
                              'stroke="%s" stroke-width="2.5"/>' % (x, y - 7, RING))
            elif kind == "arrow":
                self.arrow(x, y, x + 20, y)
                x += 4
            else:
                self.rect(x, y - 7, 18, 14, kind, rx=3)
            self.t(x + 26, y, label, 12, False, SUB)
            x += 26 + 12 * len(label) * 0.95 + 22

    def render(self, height):
        head = ('<svg width="100%%" viewBox="0 0 680 %d" role="img" xmlns="http://www.w3.org/2000/svg" '
                'font-family=\'%s\'>\n<title>%s</title><desc>%s</desc>\n'
                '<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" '
                'markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" '
                'stroke="#52514E" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
                '</marker></defs>\n' % (height, FONT, esc(self.title), esc(self.desc)))
        return head + "\n".join(self.p) + "\n</svg>\n"

    def save(self, name, height):
        os.makedirs(SVG_DIR, exist_ok=True)
        with open(os.path.join(SVG_DIR, name), "w", encoding="utf-8") as f:
            f.write(self.render(height))


LEG_TRACE = [("new", "这一步新填的"), ("old", "已经填好的"), ("ring", "依赖的格子"),
             ("arrow", "依赖方向")]


# ----------------------------------------------------------------------------
# 表格 trace 图 (所有 2D 表格题共用)
# ----------------------------------------------------------------------------
class Table:
    """rows × cols 个格子; labels 是 (idx, char) 元组。"""

    def __init__(self, x0, y0, rl, cl, px, py, cw, ch, hdrw=46, hdrh=38):
        self.x0, self.y0, self.rl, self.cl = x0, y0, rl, cl
        self.px, self.py, self.cw, self.ch, self.hdrw, self.hdrh = px, py, cw, ch, hdrw, hdrh
        self.R, self.Cn = len(rl), len(cl)

    @property
    def width(self):
        return self.hdrw + (self.Cn - 1) * self.px + self.cw

    @property
    def height(self):
        return self.hdrh + (self.R - 1) * self.py + self.ch

    def pos(self, i, j):
        return (self.x0 + self.hdrw + j * self.px, self.y0 + self.hdrh + i * self.py)

    def center(self, i, j):
        x, y = self.pos(i, j)
        return x + self.cw / 2, y + self.ch / 2

    def draw(self, s, vals, role_of, subs=None, deps=(), new=None):
        # 列标题: idx 在上 (灰, 12), char 在下 (14)
        for j, (idx, ch) in enumerate(self.cl):
            x, _ = self.pos(0, j)
            if ch == "":
                s.t(x + self.cw / 2, self.y0 + 22, idx, 12, False, SUB, "middle")
            else:
                s.t(x + self.cw / 2, self.y0 + 8, idx, 12, False, SUB, "middle")
                s.t(x + self.cw / 2, self.y0 + 26, ch, 14, True, INK, "middle")
        for i, (idx, ch) in enumerate(self.rl):
            _, y = self.pos(i, 0)
            if ch == "":
                s.t(self.x0 + self.hdrw - 14, y + self.ch / 2, idx, 12, False, SUB, "end")
            else:
                s.t(self.x0 + 6, y + self.ch / 2, idx, 12, False, SUB, "start")
                s.t(self.x0 + self.hdrw - 14, y + self.ch / 2, ch, 14, True, INK, "end")
        for i in range(self.R):
            for j in range(self.Cn):
                x, y = self.pos(i, j)
                role = role_of(i, j)
                if role == "none":
                    continue
                txt = vals[i][j] if role != "empty" else ""
                sub = subs[i][j] if (subs and role != "empty") else None
                s.cell(x, y, self.cw, self.ch, txt, role, sub=sub)
        # 依赖: 橙色 ring + 箭头 (箭头走格子之间的缝)
        for (i, j) in deps:
            x, y = self.pos(i, j)
            s.ring(x, y, self.cw, self.ch)
        if new is not None:
            ni, nj = new
            for (i, j) in deps:
                self._arrow(s, (i, j), new)

    def _arrow(self, s, a, b):
        ax, ay = self.pos(*a)
        bx, by = self.pos(*b)
        if a[0] == b[0] and abs(b[1] - a[1]) == 2:
            # 跨一格的横向依赖: 从缝里绕过去, 不压住中间那格的数字
            yb = ay + self.ch
            s.path("M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f"
                   % (ax + self.cw / 2, yb + 3, ax + self.cw / 2, yb + 7,
                      bx + self.cw / 2, yb + 7, bx + self.cw / 2, yb + 1), color="#8A6D1E", sw=1.6)
            return
        di, dj = b[0] - a[0], b[1] - a[1]
        gx, gy = self.px - self.cw, self.py - self.ch
        # 起点: a 格子朝 b 的那条边 / 角; 终点: b 格子朝 a 的边 / 角 (中间隔着一条缝)
        sx = ax + (self.cw if dj > 0 else 0 if dj < 0 else self.cw / 2)
        sy = ay + (self.ch if di > 0 else 0 if di < 0 else self.ch / 2)
        ex = bx + (0 if dj > 0 else self.cw if dj < 0 else self.cw / 2)
        ey = by + (0 if di > 0 else self.ch if di < 0 else self.ch / 2)
        # ring 外扩 3, 起点终点各让开 3 以免被 ring 盖住
        ux = (ex - sx)
        uy = (ey - sy)
        L = (ux * ux + uy * uy) ** 0.5
        k = 3.0 / L if L else 0
        s.arrow(sx + ux * k, sy + uy * k, ex - ux * k, ey - uy * k, color="#8A6D1E", sw=1.6)


def trace_svg(name, title, sub1, sub2, table_kw, col_titles, vals, base, order, steps, final,
              subs=None, roles_hidden=None, right_x=None, line_h=18, min_block=0, final2=None):
    """
    vals: 完整的最终 dp 表 (字符串)。base: 一开始就填好的格子集合。
    order: 其余格子的填表顺序。steps: [{new, deps, lines:[(text, kind)]}]
    某一步的状态 = base + order 里 new 之前 (含 new) 的所有格子。
    """
    rl, cl = table_kw["rl"], table_kw["cl"]
    s = S(title, sub1 + " " + sub2)
    T0 = Table(40, 0, rl, cl, table_kw["px"], table_kw["py"], table_kw["cw"], table_kw["ch"])
    rx = right_x or (40 + T0.width + 34)
    s.t(40, 18, sub1, 12)
    s.t(40, 38, sub2, 12)
    s.t(40, 64, col_titles[0], 12)
    s.t(rx, 64, col_titles[1], 12)
    y = 74
    s.line(40, y, 640, y)
    y += 10
    for st in steps:
        k = order.index(st["new"])
        filled = set(base) | set(order[:k + 1])
        tbl = Table(40, y, rl, cl, T0.px, T0.py, T0.cw, T0.ch)
        newc = st["new"]

        def role_of(i, j, filled=filled, newc=newc):
            if (i, j) == newc:
                return "new"
            if (i, j) in filled:
                return "old"
            if roles_hidden and (i, j) in roles_hidden:
                return "none"
            return "empty"
        tbl.draw(s, vals, role_of, subs=subs, deps=st["deps"], new=newc)
        ty = y + 8
        for text, kind in st["lines"]:
            if kind == "h":
                s.t(rx, ty + 8, text, 14, True, INK)
            elif kind == "f":
                s.t(rx, ty + 8, text, 14, True, INK)
            else:
                s.t(rx, ty + 8, text, 12, False, SUB)
            ty += line_h
        blk = max(tbl.height, ty - y, min_block)
        y += blk + 12
        s.line(40, y, 640, y)
        y += 10
    y += 8
    s.t(40, y, final, 14, True, INK)
    if final2:
        y += 20
        s.t(40, y, final2, 12, False, SUB)
    y += 28
    s.legend(y, LEG_TRACE)
    s.save(name, y + 22)


def cells_order(m, n, start=1):
    return [(i, j) for i in range(start, m) for j in range(start, n)]


def lab(chars, zero=True):
    """行 / 列标签: [(idx, char)]"""
    out = [("0", "ε")] if zero else []
    base = 1 if zero else 0
    return out + [(str(k + base), c) for k, c in enumerate(chars)]


# ----------------------------------------------------------------------------
# 每道题的 dp (和文档里的代码同一逻辑, 数字用来画图)
# ----------------------------------------------------------------------------
def dp_unique(m, n):
    dp = [[1] * n for _ in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp


def dp_minpath(g):
    m, n = len(g), len(g[0])
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = g[0][0]
    for j in range(1, n):
        dp[0][j] = dp[0][j - 1] + g[0][j]
    for i in range(1, m):
        dp[i][0] = dp[i - 1][0] + g[i][0]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = min(dp[i - 1][j], dp[i][j - 1]) + g[i][j]
    return dp


def dp_square(mat):
    m, n = len(mat), len(mat[0])
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if mat[i - 1][j - 1] == "1":
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
    return dp


def dp_lcs(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i - 1][j - 1] + 1 if a[i - 1] == b[j - 1] else max(dp[i - 1][j], dp[i][j - 1])
    return dp


def dp_edit(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1])
    return dp


def dp_pal(s):
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j] and (j - i < 2 or dp[i + 1][j - 1]):
                dp[i][j] = True
    return dp


def dp_regex(s, p):
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    for j in range(2, n + 1):
        if p[j - 1] == "*":
            dp[0][j] = dp[0][j - 2]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == "*":
                dp[i][j] = dp[i][j - 2]
                if p[j - 2] in (s[i - 1], "."):
                    dp[i][j] = dp[i][j] or dp[i - 1][j]
            elif p[j - 1] in (s[i - 1], "."):
                dp[i][j] = dp[i - 1][j - 1]
    return dp


def strs(M):
    return [[str(v) for v in row] for row in M]


# ----------------------------------------------------------------------------
# 图 0: 第一性原理 core
# ----------------------------------------------------------------------------
def svg_core_general():
    s = S("2D DP 的骨架", "state 需要两个 index,依赖上 左 左上,填表顺序,滚动数组")
    s.t(40, 18, "dp[i][j] = 前缀 A[:i] 和前缀 B[:j] 的答案  ·  两个 index 才能说清子问题 → 2D 表", 12)
    s.t(40, 38, "想 transition: 问 \"最后一步做了什么\", 每种做法 = 一个更小的 (i', j')", 12)
    rl = [("i-2", ""), ("i-1", ""), ("i", "")]
    cl = [("j-2", ""), ("j-1", ""), ("j", ""), ("j+1", "")]
    T = Table(40, 56, rl, cl, 62, 52, 48, 36, hdrw=44, hdrh=34)
    new, deps = (2, 2), [(1, 1), (1, 2), (2, 1)]

    def role_of(i, j):
        if (i, j) == new:
            return "new"
        if i == 0:
            return "rm"
        if i == 1:
            return "old"
        return "old" if j < 2 else "empty"
    vals = [["" for _ in range(4)] for _ in range(3)]
    vals[2][2] = "?"
    T.draw(s, vals, role_of, deps=deps, new=new)
    # 注释
    s.t(T.x0 + T.width + 22, T.pos(0, 0)[1] + 18, "更早的行: 不会再被读 → 可以丢", 12, False, "#993C1D")
    s.t(T.x0 + T.width + 22, T.pos(1, 0)[1] + 18, "prev 行: 只需要保留这一行", 12, False, INK)
    s.t(T.x0 + T.width + 22, T.pos(2, 0)[1] + 18, "cur 行: 从左到右边填边用", 12, False, INK)
    # 右侧三条规则
    y0 = 56 + T.height + 28
    s.line(40, y0 - 14, 640, y0 - 14)
    rows = [
        ("① 填表顺序", "dp[i][j] 要读 上 / 左 / 左上 → 这三个必须已经填好", "→ i 从上到下, j 从左到右 (依赖指向的反方向)"),
        ("② 滚动数组", "dp[i][*] 只读 dp[i-1][*] 和同一行左边的格子", "→ 只留 prev, cur 两行, space O(m*n) → O(n)"),
        ("③ base case", "第 0 行 / 第 0 列 = 一边是空时的答案", "→ 先填好, 循环从 1 开始, 不用写 if i == 0"),
    ]
    y = y0 + 6
    for h, a, b in rows:
        s.t(40, y, h, 14, True, INK)
        s.t(150, y, a, 12, False, SUB)
        s.t(150, y + 18, b, 12, False, SUB)
        y += 46
    s.legend(y + 4, [("new", "要填的 dp[i][j]"), ("old", "已填好"), ("rm", "不再需要"),
                     ("ring", "依赖的格子"), ("arrow", "依赖方向")])
    s.save("general_core.svg", y + 30)


# ----------------------------------------------------------------------------
# 题 1: Unique Paths
# ----------------------------------------------------------------------------
def svg_unique_core():
    s = S("Unique Paths: 暴力递归重复算同一格", "f(2,3) 展开后 f(1,2) 出现两次;dp 表每格只算一次")
    s.t(40, 18, "f(i, j) = 从起点走到 (i, j) 的路径数 = f(i-1, j) + f(i, j-1)  ·  这里 m = 3, n = 4, 求 f(2, 3)", 12)
    s.t(40, 38, "暴力递归: 每个格子拆成两个子问题 → 2^(m+n) 级别, 但不同的 (i, j) 只有 m*n 个", 12)

    def node(cx, cy, label, role="old"):
        s.rect(cx - 26, cy - 15, 52, 30, role)
        s.t(cx, cy + 1, label, 14, True, C[role][2], "middle")

    def edge(x1, y1, x2, y2):
        s.line(x1, y1, x2, y2, color="#B4B2A9", sw=1, dash=None)
    # 树
    nodes = {
        "f23": (215, 80), "f13": (105, 150), "f22": (325, 150),
        "f03": (50, 220), "f12a": (160, 220), "f12b": (285, 220), "f21": (365, 220),
        "f02": (130, 290), "f11a": (190, 290), "f02b": (255, 290), "f11b": (315, 290),
    }
    edges = [("f23", "f13"), ("f23", "f22"), ("f13", "f03"), ("f13", "f12a"),
             ("f22", "f12b"), ("f22", "f21"), ("f12a", "f02"), ("f12a", "f11a"),
             ("f12b", "f02b"), ("f12b", "f11b")]
    for a, b in edges:
        edge(nodes[a][0], nodes[a][1] + 15, nodes[b][0], nodes[b][1] - 15)
    labels = {"f23": "f(2,3)", "f13": "f(1,3)", "f22": "f(2,2)", "f03": "f(0,3)",
              "f12a": "f(1,2)", "f12b": "f(1,2)", "f21": "f(2,1)", "f02": "f(0,2)",
              "f11a": "f(1,1)", "f02b": "f(0,2)", "f11b": "f(1,1)"}
    for k, (cx, cy) in nodes.items():
        role = "rm" if k in ("f12a", "f12b", "f02", "f11a", "f02b", "f11b") else "old"
        node(cx, cy, labels[k], role)
    s.t(40, 328, "红色: 同一个子树被算了两遍 (f(1,2) 下面整棵树都重复)", 12, False, "#993C1D")
    # 右: dp 表
    s.t(430, 70, "dp 表: 每格只算一次, 之后直接读", 14, True, INK)
    T = Table(430, 90, [("0", ""), ("1", ""), ("2", "")],
              [("0", ""), ("1", ""), ("2", ""), ("3", "")], 48, 44, 40, 34, hdrw=30, hdrh=26)
    dp = dp_unique(3, 4)
    T.draw(s, strs(dp), lambda i, j: "new" if (i, j) == (2, 3) else "old")
    s.t(430, 90 + T.height + 24, "dp[2][3] = dp[1][3] + dp[2][2]", 14, True, INK)
    s.t(430, 90 + T.height + 44, "= 4 + 6 = 10", 14, True, INK)
    s.t(430, 90 + T.height + 68, "m*n = 12 格, 每格 O(1) → O(m*n)", 12)
    s.t(430, 90 + T.height + 86, "f(1,2) 在表里是 dp[1][2] = 3, 读两次", 12)
    s.save("unique_paths_core.svg", 350)


def svg_unique_trace():
    dp = dp_unique(3, 4)
    rl = [(str(i), "") for i in range(3)]
    cl = [(str(j), "") for j in range(4)]
    base = {(0, j) for j in range(4)} | {(i, 0) for i in range(3)}
    order = cells_order(3, 4)

    def ln(i, j):
        a, b = dp[i - 1][j], dp[i][j - 1]
        return [("填 dp[%d][%d]" % (i, j), "h"),
                ("dp[%d][%d] = dp[%d][%d] + dp[%d][%d]" % (i, j, i - 1, j, i, j - 1), "n"),
                ("= %d + %d = %d" % (a, b, a + b), "f"),
                ("上面来 %d 条, 左边来 %d 条" % (a, b), "n")]
    steps = [dict(new=c, deps=[(c[0] - 1, c[1]), (c[0], c[1] - 1)], lines=ln(*c)) for c in order]
    trace_svg("unique_paths_trace.svg", "Unique Paths trace",
              "m = 3, n = 4 · dp[i][j] = 从 (0,0) 走到第 i 行第 j 列的路径数 · 第 0 行 / 第 0 列预先填 1",
              "每一步: 读 上面 dp[i-1][j] 和 左边 dp[i][j-1] → 相加", dict(rl=rl, cl=cl, px=56, py=44, cw=44, ch=34),
              ("dp 表 (这一步之后)", "怎么算"), strs(dp), base, order, steps,
              "答案 dp[2][3] = dp[1][3] + dp[2][2] = 4 + 6 = %d" % dp[2][3])


# ----------------------------------------------------------------------------
# 题 2: Minimum Path Sum
# ----------------------------------------------------------------------------
GRID = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]


def svg_minpath_core():
    dp = dp_minpath(GRID)
    s = S("Minimum Path Sum: 最后一步 + 前缀最优", "dp[1][1] 取上面和左边里小的")
    s.t(40, 18, "dp[i][j] = 从 (0,0) 走到 (i,j) 的最小路径和  ·  最后一步只能来自上面或左边", 12)
    s.t(40, 38, "为什么只看两个邻居的 dp 值就够: 走到 (i,j) 的最优路径, 它的前缀一定也是走到那个邻居的最优路径", 12)
    # 三格: top, left, cur
    cx, cy = 150, 80
    s.cell(cx, cy, 90, 44, str(dp[0][1]), "old", sub="top (0,1)")
    s.cell(cx - 100, cy + 64, 90, 44, str(dp[1][0]), "old", sub="left (1,0)")
    s.cell(cx, cy + 64, 90, 44, "?", "new", sub="cur (1,1)")
    s.ring(cx, cy, 90, 44)
    s.ring(cx - 100, cy + 64, 90, 44)
    s.arrow(cx + 45, cy + 47, cx + 45, cy + 62, color="#8A6D1E")
    s.arrow(cx - 8, cy + 86, cx - 1, cy + 86, color="#8A6D1E")
    s.t(300, cy + 8, "top  = dp[0][1] = %d" % dp[0][1], 14, True, INK)
    s.t(300, cy + 30, "left = dp[1][0] = %d" % dp[1][0], 14, True, INK)
    s.t(300, cy + 66, "min(top, left) = min(%d, %d) = %d  ← 选这条" % (dp[0][1], dp[1][0], min(dp[0][1], dp[1][0])), 14, True, INK)
    s.t(300, cy + 90, "dp[1][1] = %d + grid[1][1] = %d + %d = %d" % (min(dp[0][1], dp[1][0]), min(dp[0][1], dp[1][0]), GRID[1][1], dp[1][1]), 14, True, INK)
    s.t(300, cy + 112, "没选的那条 (%d) 更大, 以后也不会翻身: 后面只加正数" % max(dp[0][1], dp[1][0]), 12)
    s.t(40, cy + 150, "和 Unique Paths 的区别只有一行: 相加 → 取 min, 并且多加自己这格的 grid 值", 12, False, "#993C1D")
    s.legend(cy + 182, [("new", "要填的格子"), ("old", "已经填好"), ("ring", "候选来路")])
    s.save("min_path_sum_core.svg", cy + 205)


def svg_minpath_trace():
    dp = dp_minpath(GRID)
    rl = [(str(i), "") for i in range(3)]
    cl = [(str(j), "") for j in range(3)]
    base = {(0, 0)} | {(0, j) for j in range(1, 3)} | {(i, 0) for i in range(1, 3)}
    order = cells_order(3, 3)
    subs = [["g=%d" % GRID[i][j] for j in range(3)] for i in range(3)]

    def ln(i, j):
        a, b = dp[i - 1][j], dp[i][j - 1]
        mn = min(a, b)
        who = "上面" if a <= b else "左边"
        return [("填 dp[%d][%d]" % (i, j), "h"),
                ("top = dp[%d][%d] = %d · left = dp[%d][%d] = %d" % (i - 1, j, a, i, j - 1, b), "n"),
                ("min(%d, %d) + g = %d + %d" % (a, b, mn, GRID[i][j]), "n"),
                ("= %d" % dp[i][j], "f"),
                ("取%s那条 (%d 更小)" % (who, mn), "n")]
    steps = [dict(new=c, deps=[(c[0] - 1, c[1]), (c[0], c[1] - 1)], lines=ln(*c)) for c in order]
    trace_svg("min_path_sum_trace.svg", "Minimum Path Sum trace",
              "grid = [[1,3,1],[1,5,1],[4,2,1]] · 格子左上角的 g = grid 值, 大数字 = dp 值",
              "第 0 行 / 第 0 列已按累加预先填好 · 每一步: dp[i][j] = min(top, left) + g", dict(rl=rl, cl=cl, px=64, py=50, cw=52, ch=40),
              ("dp 表 (这一步之后)", "怎么算"), strs(dp), base, order, steps,
              "答案 dp[2][2] = min(dp[1][2], dp[2][1]) + g = min(%d, %d) + 1 = %d" % (dp[1][2], dp[2][1], dp[2][2]),
              subs=subs, right_x=300, min_block=0,
              final2="路径 1→3→1→1→1 = 7 (右, 右, 下, 下)")


# ----------------------------------------------------------------------------
# 题 3: Maximal Square
# ----------------------------------------------------------------------------
MAT = ["10100", "10111", "11111", "10010"]


def svg_square_core():
    s = S("Maximal Square: min(上, 左, 左上) + 1", "三个邻居里最小的决定边长")
    s.t(40, 18, "dp[i][j] = 以 (i,j) 为右下角的最大全 1 正方形边长 · 把当前格当右下角, 向左上长一圈", 12)
    s.t(40, 38, "下面 3×3 小块里, 左上角是 0。当前格 (右下角) 周围三个邻居各自能撑起的正方形:", 12)
    patch = [["0", "1", "1"], ["1", "1", "1"], ["1", "1", "1"]]
    # (title, rect(i0,j0,size), ok, note)
    panels = [
        ("top", (0, 1, 2), True, "边长 2 ✓"),
        ("left", (1, 0, 2), True, "边长 2 ✓"),
        ("diag", (0, 0, 2), False, "只有 1 ✗"),
        ("cur", (1, 1, 2), True, "min(2,2,1)+1 = 2"),
    ]
    cw = 30
    x0, gap = 40, 150
    for k, (name, (i0, j0, sz), ok, note) in enumerate(panels):
        px = x0 + k * gap
        py = 74
        s.t(px, py - 6, name, 14, True, INK)
        for i in range(3):
            for j in range(3):
                role = "old"
                s.cell(px + j * cw, py + 8 + i * cw, cw, cw, patch[i][j], role, size=14)
        col = "#0F6E56" if ok else "#993C1D"
        if name == "cur":
            s.p.append('<rect x="%s" y="%s" width="%s" height="%s" fill="none" stroke="%s" stroke-width="3" rx="3"/>'
                       % (px + j0 * cw, py + 8 + i0 * cw, sz * cw, sz * cw, col))
        else:
            s.p.append('<rect x="%s" y="%s" width="%s" height="%s" fill="none" stroke="%s" '
                       'stroke-width="2.5" stroke-dasharray="5 3" rx="3"/>'
                       % (px + j0 * cw, py + 8 + i0 * cw, sz * cw, sz * cw, col))
        s.t(px, py + 8 + 3 * cw + 16, note, 12, False, col)
        # 当前格标记
    s.t(40, 210, "为什么是 min: 要把当前格补成 (k+1)×(k+1) 的正方形, 上 / 左 / 左上三块都得至少是 k×k。", 12, False, INK)
    s.t(40, 230, "三块里最小的那块先 \"撞墙\" (这里左上角的 0 把 diag 限制成 1), 所以边长 = 最小 + 1。", 12, False, INK)
    s.t(40, 250, "当前格是 0 时 dp = 0: 它不能当任何正方形的右下角。", 12)
    s.save("maximal_square_core.svg", 270)


def svg_square_trace():
    dp = dp_square(MAT)
    m, n = len(MAT), len(MAT[0])
    rl = [("0", "")] + [(str(i + 1), "") for i in range(m)]
    cl = [("0", "")] + [(str(j + 1), "") for j in range(n)]
    base = {(0, j) for j in range(n + 1)} | {(i, 0) for i in range(m + 1)}
    order = cells_order(m + 1, n + 1)
    subs = [["" for _ in range(n + 1)] for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            subs[i][j] = "m=" + MAT[i - 1][j - 1]
    pick = [(1, 1), (1, 3), (2, 3), (2, 4), (2, 5), (3, 5)]

    def ln(i, j):
        t, l_, g = dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]
        if MAT[i - 1][j - 1] == "0":
            return [("填 dp[%d][%d]" % (i, j), "h"), ("matrix[%d][%d] = 0" % (i - 1, j - 1), "n"),
                    ("不能当右下角 → dp = 0", "f")]
        return [("填 dp[%d][%d]" % (i, j), "h"),
                ("matrix[%d][%d] = 1" % (i - 1, j - 1), "n"),
                ("top = %d · left = %d · diag = %d" % (t, l_, g), "n"),
                ("min(%d, %d, %d) + 1 = %d + 1" % (t, l_, g, min(t, l_, g)), "n"),
                ("= %d" % dp[i][j], "f")]
    steps = [dict(new=c, deps=[(c[0] - 1, c[1]), (c[0], c[1] - 1), (c[0] - 1, c[1] - 1)], lines=ln(*c))
             for c in pick]
    best = max(max(r) for r in dp)
    trace_svg("maximal_square_trace.svg", "Maximal Square trace",
              "matrix = [10100, 10111, 11111, 10010] · 格子左上角 m = 原矩阵的值, 大数字 = dp (边长)",
              "第 0 行 / 第 0 列是补的一圈 0 · 只挑 6 个有代表性的格子, 其余格子照同一公式填 (灰色里的数字是真实结果)",
              dict(rl=rl, cl=cl, px=50, py=46, cw=40, ch=38),
              ("dp 表 (这一步之后)", "怎么算"), strs(dp), base, order, steps,
              "答案: 表里最大的 dp = %d → 面积 = %d × %d = %d" % (best, best, best, best * best),
              subs=subs, right_x=412,
              final2="最大的 2 出现在 dp[3][4] 和 dp[3][5] (其余格子我们没展开, 但照同一公式填), 各对应 matrix 里一个 2×2 的全 1 方块")


# ----------------------------------------------------------------------------
# 题 4: LCS
# ----------------------------------------------------------------------------
def svg_lcs_core():
    s = S("LCS: 看最后一个字符", "相同则左上+1,不同则丢一个字符")
    s.t(40, 18, "dp[i][j] = text1[:i] 和 text2[:j] 的 LCS 长度 · 比较两个前缀的最后一个字符 text1[i-1], text2[j-1]", 12)

    def word(x, y, chars, roles):
        for k, ch in enumerate(chars):
            s.cell(x + k * 30, y, 30, 30, ch, roles[k])
    # case 1
    s.t(40, 60, "case 1 · 最后一个字符相同", 14, True, INK)
    s.t(40, 84, "text1[:i] =", 12)
    word(120, 70, "abc", ["old", "old", "new"])
    s.t(40, 124, "text2[:j] =", 12)
    word(120, 110, "ac", ["old", "new"])
    s.t(240, 85, "c == c → 这一对一定能配上", 12, False, INK)
    s.t(240, 125, "去掉这一对, 剩下 \"ab\" vs \"a\"", 12, False, INK)
    s.t(240, 155, "dp[i][j] = dp[i-1][j-1] + 1", 14, True, INK)
    s.line(40, 172, 640, 172)
    # case 2
    s.t(40, 196, "case 2 · 最后一个字符不同", 14, True, INK)
    s.t(40, 220, "text1[:i] =", 12)
    word(120, 206, "abd", ["old", "old", "rm"])
    s.t(40, 260, "text2[:j] =", 12)
    word(120, 246, "ac", ["old", "rm"])
    s.t(240, 215, "d != c → 它们不可能同时出现在 LCS 的末尾", 12, False, INK)
    s.t(240, 235, "要么丢掉 d:  \"ab\" vs \"ac\"  → dp[i-1][j]", 12, False, INK)
    s.t(240, 255, "要么丢掉 c:  \"abd\" vs \"a\"  → dp[i][j-1]", 12, False, INK)
    s.t(240, 285, "dp[i][j] = max(dp[i-1][j], dp[i][j-1])", 14, True, INK)
    s.t(40, 320, "两个 index 各自只会 \"缩短一个字符\" → 子问题永远是 (前缀, 前缀), 总共 (m+1)(n+1) 个", 12)
    s.legend(344, [("new", "比较的最后字符 (相同)"), ("rm", "被丢掉的字符"), ("old", "其余字符")])
    s.save("lcs_core.svg", 366)


def svg_lcs_trace():
    a, b = "abcde", "ace"
    dp = dp_lcs(a, b)
    m, n = len(a), len(b)
    rl, cl = lab(a), lab(b)
    base = {(0, j) for j in range(n + 1)} | {(i, 0) for i in range(m + 1)}
    order = cells_order(m + 1, n + 1)
    pick = [(1, 1), (1, 2), (2, 1), (2, 2), (3, 2), (3, 3), (5, 3)]

    def ln(i, j):
        x, y = a[i - 1], b[j - 1]
        if x == y:
            return [("填 dp[%d][%d]" % (i, j), "h"),
                    ("text1[%d] = '%s' == text2[%d] = '%s'  相同" % (i - 1, x, j - 1, y), "n"),
                    ("dp[%d][%d] + 1 = %d + 1" % (i - 1, j - 1, dp[i - 1][j - 1]), "n"),
                    ("= %d  (左上 + 1)" % dp[i][j], "f")]
        return [("填 dp[%d][%d]" % (i, j), "h"),
                ("text1[%d] = '%s' != text2[%d] = '%s'  不同" % (i - 1, x, j - 1, y), "n"),
                ("max(top = %d, left = %d)" % (dp[i - 1][j], dp[i][j - 1]), "n"),
                ("= %d" % dp[i][j], "f")]
    steps = []
    for c in pick:
        i, j = c
        deps = [(i - 1, j - 1)] if a[i - 1] == b[j - 1] else [(i - 1, j), (i, j - 1)]
        steps.append(dict(new=c, deps=deps, lines=ln(i, j)))
    trace_svg("lcs_trace.svg", "LCS trace",
              "text1 = \"abcde\" (行), text2 = \"ace\" (列) · dp[i][j] = text1[:i] 与 text2[:j] 的 LCS 长度",
              "第 0 行 / 第 0 列 = 0 (空串) · 挑 7 个格子; 相同 → 只依赖左上, 不同 → 依赖上 + 左",
              dict(rl=rl, cl=cl, px=56, py=36, cw=44, ch=30),
              ("dp 表 (这一步之后)", "怎么算"), strs(dp), base, order, steps,
              "答案 dp[5][3] = dp[4][2] + 1 = 2 + 1 = %d  (LCS = \"ace\")" % dp[5][3],
              right_x=320)


# ----------------------------------------------------------------------------
# 题 5: Edit Distance
# ----------------------------------------------------------------------------
def svg_edit_core():
    s = S("Edit Distance: 三种操作 = 三个方向", "replace 左上,delete 上,insert 左")
    s.t(40, 18, "dp[i][j] = word1[:i] 变成 word2[:j] 的最少操作数 · 看最后一步操作了什么", 12)
    rl = [("i-1", ""), ("i", "")]
    cl = [("j-1", ""), ("j", "")]
    T = Table(40, 44, rl, cl, 100, 80, 88, 44, hdrw=40, hdrh=34)
    T.draw(s, [["dp[i-1][j-1]", "dp[i-1][j]"], ["dp[i][j-1]", "?"]],
           lambda i, j: "new" if (i, j) == (1, 1) else "old", deps=[(0, 0), (0, 1), (1, 0)], new=(1, 1))
    # 重画小字号: 上面 cell 字号 14 放不下长文本, 覆盖一层
    rx = 350
    items = [
        ("左上 dp[i-1][j-1] + 1", "replace", "word1[i-1] 改成 word2[j-1]; 两边各缩短 1 个字符"),
        ("上面 dp[i-1][j] + 1", "delete", "删掉 word1[i-1]; word1 缩短 1, word2 不变"),
        ("左边 dp[i][j-1] + 1", "insert", "在末尾补一个 word2[j-1]; word2 缩短 1, word1 不变"),
    ]
    y = 56
    for f, nm, ex in items:
        s.t(rx, y, nm, 14, True, INK)
        s.t(rx + 70, y, f, 14, True, INK)
        s.t(rx, y + 20, ex, 12)
        y += 52
    s.line(40, 228, 640, 228)
    s.t(40, 250, "最后一个字符已经相同 (word1[i-1] == word2[j-1])  →  不用任何操作: dp[i][j] = dp[i-1][j-1]", 14, True, INK)
    s.t(40, 274, "不同  →  三种操作各试一次, 取最小: dp[i][j] = 1 + min(左上, 上, 左)", 14, True, INK)
    s.t(40, 298, "和 LCS 的区别: LCS 不同时是 max(上, 左) 且不加 1; 这里多了 \"左上\" 这个选项 (replace), 求最小所以加 1", 12, False, "#993C1D")
    s.legend(326, [("new", "要填的 dp[i][j]"), ("old", "三个来路"), ("ring", "依赖"), ("arrow", "依赖方向")])
    s.save("edit_distance_core.svg", 350)


def svg_edit_trace():
    a, b = "horse", "ros"
    dp = dp_edit(a, b)
    m, n = len(a), len(b)
    rl, cl = lab(a), lab(b)
    base = {(0, j) for j in range(n + 1)} | {(i, 0) for i in range(m + 1)}
    order = cells_order(m + 1, n + 1)
    pick = [(1, 1), (2, 2), (2, 3), (3, 3), (4, 3), (5, 3)]

    def ln(i, j):
        x, y = a[i - 1], b[j - 1]
        r, dl, ins = dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1]
        head = ("填 dp[%d][%d]" % (i, j), "h")
        if x == y:
            return [head, ("word1[%d] = '%s' == word2[%d] = '%s'  相同" % (i - 1, x, j - 1, y), "n"),
                    ("不用操作: 白拿左上 dp[%d][%d]" % (i - 1, j - 1), "n"), ("= %d" % dp[i][j], "f")]
        return [head, ("'%s' != '%s'  三种操作取最小" % (x, y), "n"),
                ("replace 左上 %d · delete 上 %d · insert 左 %d" % (r, dl, ins), "n"),
                ("1 + min(%d, %d, %d)" % (r, dl, ins), "n"), ("= 1 + %d = %d" % (min(r, dl, ins), dp[i][j]), "f")]
    steps = []
    for c in pick:
        i, j = c
        deps = [(i - 1, j - 1)] if a[i - 1] == b[j - 1] else [(i - 1, j - 1), (i - 1, j), (i, j - 1)]
        steps.append(dict(new=c, deps=deps, lines=ln(i, j)))
    trace_svg("edit_distance_trace.svg", "Edit Distance trace",
              "word1 = \"horse\" (行) → word2 = \"ros\" (列) · dp[i][j] = word1[:i] 变成 word2[:j] 的最少操作数",
              "第 0 行 = 0,1,2,3 (全插入) · 第 0 列 = 0..5 (全删除) · 挑 6 个格子",
              dict(rl=rl, cl=cl, px=56, py=38, cw=44, ch=30),
              ("dp 表 (这一步之后)", "怎么算"), strs(dp), base, order, steps,
              "答案 dp[5][3] = 1 + min(dp[4][2], dp[4][3], dp[5][2]) = 1 + min(%d, %d, %d) = %d" % (
                  dp[4][2], dp[4][3], dp[5][2], dp[5][3]),
              right_x=320,
              final2="horse → rorse (replace h→r) → rose (delete r) → ros (delete e): 3 步")


# ----------------------------------------------------------------------------
# 题 6: Longest Palindromic Substring
# ----------------------------------------------------------------------------
def svg_lps_core():
    s = S("Longest Palindromic Substring: expand around center", "从中心往两边扩")
    s.t(40, 18, "palindrome 一定有一个中心。枚举 2n-1 个中心 (n 个字符 + n-1 个缝), 从中心往两边扩, 直到两端不同", 12)
    ss = "babad"
    cw = 40
    x0 = 150

    def row(y, label, l, r, hit, note, role_new=()):
        s.t(40, y + 15, label, 12, False, INK)
        for k, ch in enumerate(ss):
            if l <= k <= r and hit:
                role = "new"
            elif k in (l, r):
                role = "rm" if not hit else "new"
            else:
                role = "old"
            s.cell(x0 + k * cw, y, cw, 30, ch, role)
        s.t(x0 + 5 * cw + 16, y + 15, note, 12, False, INK)
    s.t(x0 - 10, 52, "s = \"babad\"", 12)
    row(64, "中心 s[1]='a'", 1, 1, True, "l=r=1 'a'=='a' ✓  长度 1")
    row(104, "  扩一步", 0, 2, True, "l=0, r=2 'b'=='b' ✓  \"bab\" 长度 3")
    row(144, "  再扩一步", -1, 3, False, "l=-1 越界 → 停, 结果 \"bab\"")
    # 第三行: 越界, 画 l=-1 的说明; 高亮 s[3]
    s.line(40, 188, 640, 188)
    row(200, "缝 (0,1) b|a", 0, 1, False, "'b' != 'a' ✗  偶数中心立刻停")
    row(240, "缝 (3,4) a|d", 3, 4, False, "'a' != 'd' ✗  停")
    s.line(40, 284, 640, 284)
    s.t(40, 306, "每个中心最多扩 O(n) 步, 共 2n-1 个中心 → O(n²) time, O(1) space", 14, True, INK)
    s.t(40, 328, "DP 版 dp[i][j] 也是 O(n²), 还要 O(n²) space; 它的价值是 \"填表顺序\" 这个思路, 下面的 trace 展示", 12)
    s.legend(354, [("new", "还在匹配的区间"), ("rm", "两端不同 → 停"), ("old", "没碰到")])
    s.save("longest_palindromic_substring_core.svg", 376)


def svg_lps_trace():
    ss = "babad"
    n = len(ss)
    dp = dp_pal(ss)
    vals = [["T" if dp[i][j] else "F" for j in range(n)] for i in range(n)]
    rl = [(str(i), c) for i, c in enumerate(ss)]
    cl = [(str(j), c) for j, c in enumerate(ss)]
    order = [(i, j) for i in range(n - 1, -1, -1) for j in range(i, n)]
    hidden = {(i, j) for i in range(n) for j in range(i)}
    pick = [(4, 4), (3, 4), (2, 3), (1, 3), (0, 2), (0, 3)]

    def ln(i, j):
        head = ("填 dp[%d][%d]  = s[%d..%d] = \"%s\"" % (i, j, i, j, ss[i:j + 1]), "h")
        if ss[i] != ss[j]:
            return [head, ("s[%d] = '%s' != s[%d] = '%s'" % (i, ss[i], j, ss[j]), "n"), ("→ False", "f")]
        if j - i < 2:
            return [head, ("s[%d] = s[%d] = '%s', 长度 <= 2" % (i, j, ss[i]), "n"),
                    ("里面是空的 → True", "f")]
        return [head, ("s[%d] = s[%d] = '%s'  两端相同" % (i, j, ss[i]), "n"),
                ("里面 dp[%d][%d] = %s" % (i + 1, j - 1, "True" if dp[i + 1][j - 1] else "False"), "n"),
                ("→ %s" % ("True" if dp[i][j] else "False"), "f")]
    steps = []
    for c in pick:
        i, j = c
        deps = []
        if ss[i] == ss[j] and j - i >= 2:
            deps = [(i + 1, j - 1)]
        steps.append(dict(new=c, deps=deps, lines=ln(i, j)))
    # 自定义: dp[i][j] 依赖 (i+1, j-1) —— 在下一行的左边, 需要自己的箭头; Table._arrow 用 di,dj 方向通用
    trace_svg("longest_palindromic_substring_trace.svg", "Longest Palindromic Substring dp trace",
              "s = \"babad\" · dp[i][j] = s[i..j] 是不是 palindrome (闭区间) · 只有 j >= i 的上三角有意义",
              "填表顺序: i 从 4 到 0 (下 → 上), 每行 j 从 i 到 4 (左 → 右), 因为 dp[i][j] 要读下一行 dp[i+1][j-1]",
              dict(rl=rl, cl=cl, px=56, py=38, cw=44, ch=30),
              ("dp 表 (这一步之后)", "怎么算"), vals, set(), order, steps,
              "最长: dp[0][2] = True → \"bab\" (长度 3) · dp[1][3] = True → \"aba\" (长度 3), 任取一个",
              roles_hidden=hidden, right_x=395,
              final2="先填 dp[4][4] 再填 dp[0][2]: 依赖的 dp[1][1] 在 \"下一行\", 所以必须从下往上")


# ----------------------------------------------------------------------------
# 题 7: Palindromic Substrings
# ----------------------------------------------------------------------------
def svg_pcount_core():
    s = S("Palindromic Substrings: 一个 palindrome 一个中心", "s = aba 的 4 个 palindrome")
    s.t(40, 18, "每个 palindrome 恰好有一个中心 → 按中心统计, 不重不漏。扩展时每成功一步 = 多一个 palindrome", 12)
    ss = "aba"
    cw = 40
    s.t(40, 56, "s = \"aba\"", 14, True, INK)
    for k, ch in enumerate(ss):
        s.cell(150 + k * cw, 40, cw, 30, ch, "old")
    items = [
        ("中心 s[0]", "\"a\"", 1),
        ("缝 (0,1)", "—  (a != b)", 0),
        ("中心 s[1]", "\"b\", \"aba\"", 2),
        ("缝 (1,2)", "—  (b != a)", 0),
        ("中心 s[2]", "\"a\"", 1),
    ]
    y = 100
    s.t(40, y - 14, "中心", 12)
    s.t(150, y - 14, "在这个中心发现的 palindrome", 12)
    s.t(420, y - 14, "count 增加", 12)
    s.line(40, y - 4, 640, y - 4)
    tot = 0
    for nm, found, c in items:
        tot += c
        s.t(40, y + 14, nm, 14, True, INK)
        s.t(150, y + 14, found, 14, False, INK)
        s.t(420, y + 14, "+%d  (累计 %d)" % (c, tot), 14, True, INK)
        y += 30
    s.line(40, y + 4, 640, y + 4)
    s.t(40, y + 26, "共 %d 个。dp 版也能做: 数 dp 表里 True 的个数, 但要 O(n²) space; 中心扩展 O(1) space。" % tot, 12, False, INK)
    s.t(40, y + 46, "和上一题的区别: 不记最长的, 每扩一步 count += 1。", 12, False, "#993C1D")
    s.save("palindromic_substrings_core.svg", y + 66)


def svg_pcount_trace():
    ss = "aba"
    n = len(ss)
    s = S("Palindromic Substrings trace", "s = aba, 5 个中心逐个扩展")
    s.t(40, 18, "s = \"aba\" · 每个中心: l, r 从中心出发 → 两端相同就 count += 1 并向外扩一步, 不同 / 越界就停", 12)
    s.t(40, 38, "count = 目前为止发现的 palindrome 个数 · 方框里 l 和 r 标出当前比较的两个位置", 12)
    s.t(40, 64, "中心", 12)
    s.t(150, 64, "s 与 (l, r)", 12)
    s.t(360, 64, "比较", 12)
    s.t(540, 64, "count", 12)
    s.line(40, 74, 640, 74)
    # 手动模拟
    rows = []
    count = 0
    for c in range(n):
        for (l, r) in ((c, c), (c, c + 1)):
            name = "奇数中心 s[%d]" % c if l == r else "偶数中心 (%d,%d)" % (c, c + 1)
            attempts = []
            while True:
                if l < 0 or r >= n:
                    attempts.append((l, r, None, count))
                    break
                if ss[l] == ss[r]:
                    count += 1
                    attempts.append((l, r, True, count))
                    l -= 1
                    r += 1
                else:
                    attempts.append((l, r, False, count))
                    break
            rows.append((name, attempts))
    y = 84
    cw = 34
    for name, atts in rows:
        s.t(40, y + 15, name, 14, True, INK)
        for (l, r, ok, cnt) in atts:
            # 画字符串
            for k, ch in enumerate(ss):
                if ok is True and k in (l, r):
                    role = "new"
                elif ok is False and k in (l, r):
                    role = "rm"
                else:
                    role = "old"
                s.cell(150 + k * cw, y, cw, 28, ch, role, size=14)
            # l r 标记
            if l == r:
                s.t(150 + l * cw + cw / 2, y + 40, "l=r", 12, True, INK, "middle")
            else:
                if 0 <= l < n:
                    s.t(150 + l * cw + cw / 2, y + 40, "l", 12, True, INK, "middle")
                if 0 <= r < n:
                    s.t(150 + r * cw + cw / 2, y + 40, "r", 12, True, INK, "middle")
            if ok is True:
                txt = "s[%d]=s[%d]='%s' ✓" % (l, r, ss[l])
                s.t(360, y + 15, txt, 12, False, INK)
                s.t(540, y + 15, "count = %d" % cnt, 14, True, INK)
            elif ok is False:
                s.t(360, y + 15, "s[%d]='%s' != s[%d]='%s' ✗ 停" % (l, ss[l], r, ss[r]), 12, False, "#993C1D")
                s.t(540, y + 15, "count = %d" % cnt, 14, False, SUB)
            else:
                s.t(360, y + 15, "l=%d 或 r=%d 越界 → 停" % (l, r), 12, False, "#993C1D")
                s.t(540, y + 15, "count = %d" % cnt, 14, False, SUB)
            y += 56
        y += 0
        s.line(40, y - 4, 640, y - 4)
        y += 6
    s.t(40, y + 10, "答案 count = %d  (\"a\", \"b\", \"a\", \"aba\")" % count, 14, True, INK)
    s.legend(y + 40, [("new", "两端相同 ✓ → count += 1"), ("rm", "两端不同 ✗ → 停"), ("old", "没参与")])
    s.save("palindromic_substrings_trace.svg", y + 64)
    return count


# ----------------------------------------------------------------------------
# 题 8: Regular Expression Matching
# ----------------------------------------------------------------------------
RS, RP = "aab", "c*a*b"


def svg_regex_core():
    s = S("Regular Expression Matching: * 的两种选择", "匹配 0 次或匹配一个并保留 pattern")
    s.t(40, 18, "dp[i][j] = s[:i] 能不能被 p[:j] 完整匹配 · p[j-1] 是 '*' 时, 它和前一个字符 p[j-2] 是一个整体 (如 \"a*\")", 12)
    s.t(40, 54, "选择 1 · 匹配 0 次: 把 \"a*\" 整个当作不存在", 14, True, INK)
    s.t(40, 78, "s[:i]  =", 12)
    for k, (ch, r) in enumerate([("a", "old"), ("a", "old")]):
        s.cell(110 + k * 32, 66, 32, 28, ch, r)
    s.t(40, 112, "p[:j]  =", 12)
    for k, (ch, r) in enumerate([("c", "old"), ("*", "old"), ("a", "rm"), ("*", "rm")]):
        s.cell(110 + k * 32, 100, 32, 28, ch, r)
    s.t(260, 82, "p 末尾的 \"a*\" 一个字符也不吃 (红色被划掉)", 12, False, INK)
    s.t(260, 114, "dp[i][j] = dp[i][j-2]   (往左跳 2 格)", 14, True, INK)
    s.line(40, 140, 640, 140)
    s.t(40, 164, "选择 2 · 匹配 1 次, 但 pattern 保留: 条件 p[j-2] == s[i-1] 或 p[j-2] == '.'", 14, True, INK)
    s.t(40, 188, "s[:i]  =", 12)
    for k, (ch, r) in enumerate([("a", "old"), ("a", "rm")]):
        s.cell(110 + k * 32, 176, 32, 28, ch, r)
    s.t(40, 222, "p[:j]  =", 12)
    for k, (ch, r) in enumerate([("c", "old"), ("*", "old"), ("a", "new"), ("*", "new")]):
        s.cell(110 + k * 32, 210, 32, 28, ch, r)
    s.t(260, 190, "s 的最后一个 a 被 \"a*\" 吃掉 (红), 但 \"a*\" 还留着", 12, False, INK)
    s.t(260, 208, "(因为它还可能继续吃前面的 a)", 12, False, INK)
    s.t(260, 234, "dp[i][j] = dp[i-1][j]   (往上跳 1 格, j 不动)", 14, True, INK)
    s.line(40, 256, 640, 256)
    s.t(40, 280, "两种选择只要有一个成立就行 → or。普通字符 / '.' : dp[i][j] = dp[i-1][j-1] (各吃一个)", 12, False, INK)
    s.t(40, 300, "'*' 不能单独存在, 所以 dp[i][j-1] 这种 \"只丢 * 不丢字符\" 的转移是错的。", 12)
    s.legend(326, [("new", "被 * 修饰的字符"), ("rm", "被匹配掉 / 被去掉"), ("old", "其余")])
    s.save("regex_core.svg", 348)


def svg_regex_trace():
    s_, p_ = RS, RP
    dp = dp_regex(s_, p_)
    m, n = len(s_), len(p_)
    vals = [["T" if dp[i][j] else "F" for j in range(n + 1)] for i in range(m + 1)]
    rl, cl = lab(s_), lab(p_)
    base = {(0, j) for j in range(n + 1)} | {(i, 0) for i in range(m + 1)}
    order = cells_order(m + 1, n + 1)
    pick = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 5)]

    def B(v):
        return "T" if v else "F"

    def ln(i, j):
        head = ("填 dp[%d][%d]  s[:%d]=\"%s\" vs p[:%d]=\"%s\"" % (i, j, i, s_[:i], j, p_[:j]), "h")
        if p_[j - 1] == "*":
            star = p_[j - 2]
            zero = dp[i][j - 2]
            ok = star in (s_[i - 1], ".")
            out = [head, ("p[%d] = '*', 前一个是 '%s'" % (j - 1, star), "n"),
                   ("选择 1 (0 次): dp[%d][%d] = %s" % (i, j - 2, B(zero)), "n")]
            if ok:
                out.append(("选择 2 (1 次): '%s' == s[%d]='%s', dp[%d][%d] = %s" % (star, i - 1, s_[i - 1], i - 1, j, B(dp[i - 1][j])), "n"))
            else:
                out.append(("选择 2 不行: '%s' != s[%d]='%s'" % (star, i - 1, s_[i - 1]), "n"))
            out.append(("%s or %s = %s" % (B(zero), B(ok and dp[i - 1][j]) if ok else "—", B(dp[i][j])) if ok else
                        "= %s" % B(dp[i][j]), "f"))
            return out
        eq = p_[j - 1] in (s_[i - 1], ".")
        return [head, ("普通字符 p[%d] = '%s' %s s[%d] = '%s'" % (j - 1, p_[j - 1], "==" if eq else "!=", i - 1, s_[i - 1]), "n"),
                ("dp[%d][%d] = %s" % (i - 1, j - 1, B(dp[i - 1][j - 1])) if eq else "不匹配", "n"),
                ("= %s" % B(dp[i][j]), "f")]
    steps = []
    for c in pick:
        i, j = c
        if p_[j - 1] == "*":
            deps = [(i, j - 2)]
            if p_[j - 2] in (s_[i - 1], "."):
                deps.append((i - 1, j))
        else:
            deps = [(i - 1, j - 1)] if p_[j - 1] in (s_[i - 1], ".") else []
        steps.append(dict(new=c, deps=deps, lines=ln(i, j)))
    trace_svg("regex_trace.svg", "Regular Expression Matching trace",
              "s = \"aab\" (行), p = \"c*a*b\" (列) · dp[i][j] = s[:i] 能否被 p[:j] 完整匹配 · T = True, F = False",
              "第 0 行 = 空 s: \"c*\" 匹配 0 次 → T, \"c*a*\" → T · 第 0 列 = 空 p: 只有 dp[0][0] = T · 挑 6 个格子",
              dict(rl=rl, cl=cl, px=46, py=40, cw=36, ch=32),
              ("dp 表 (这一步之后)", "怎么算"), vals, base, order, steps,
              "答案 dp[3][5] = dp[2][4] = True  (\"aab\" 匹配 \"c*a*b\": c* 吃 0 个, a* 吃 aa, b 吃 b)",
              right_x=360, line_h=17)


# ----------------------------------------------------------------------------
# 构建
# ----------------------------------------------------------------------------
def build_svgs():
    svg_core_general()
    svg_unique_core(); svg_unique_trace()
    svg_minpath_core(); svg_minpath_trace()
    svg_square_core(); svg_square_trace()
    svg_lcs_core(); svg_lcs_trace()
    svg_edit_core(); svg_edit_trace()
    svg_lps_core(); svg_lps_trace()
    svg_pcount_core(); svg_pcount_trace()
    svg_regex_core(); svg_regex_trace()


def build_doc():
    doc = d.Doc("15 · Dynamic Programming (2): Grid / Two Strings / Interval")
    doc.main("主线: state 需要<b>两个 index</b> 才能描述子问题时, 用 2D 表 <code>dp[i][j]</code>。"
             "问 \"最后一步做了什么\" 得到 transition, 依赖方向决定填表顺序, 只依赖上一行就能滚动数组。")
    doc.main("概念链: Unique Paths → Minimum Path Sum → Maximal Square → Longest Common Subsequence → "
             "Edit Distance → Longest Palindromic Substring → Palindromic Substrings → Regular Expression Matching。"
             "(1D 的 Climbing Stairs / House Robber / Coin Change / knapsack 在 14 号文档。)")

    # ---------------- 0 ----------------
    doc.h2("0. 第一性原理: 为什么需要 2D, 怎么推 transition")
    doc.p("<b>Brute force 在浪费什么。</b>以 Unique Paths 为例: 从 (0,0) 走到 (m-1,n-1), 暴力递归 "
          "<code>f(i,j) = f(i-1,j) + f(i,j-1)</code>, 每个格子拆成两个子问题, 时间 O(2^(m+n))。"
          "但是不同的 <code>(i, j)</code> 一共只有 m*n 个: 同一个 <code>f(1,2)</code> 被反复重新算。"
          "<b>DP 就是给每个 (i, j) 一个格子, 只算一次, 之后直接读。</b>")
    doc.p("<b>为什么是 2D。</b>子问题的 state 要用<b>两个</b> index 才说得清: 走到第 i 行第 j 列; "
          "text1 的前 i 个字符和 text2 的前 j 个字符; s[i..j] 这一段。只用一个 index 描述不了, 所以表是 2D 的。"
          "1D DP (一个数组 / 一个序列) 在 14 号文档。")
    doc.p("<b>怎么推 transition。</b>固定三步:")
    doc.p("① 写下 state 的<b>含义</b>(一句话, 包括 i、j 是 \"前 i 个\" 还是 \"第 i 个\"); "
          "② 问<b>\"最后一步做了什么\"</b>: 最后一步有几种做法, 每种做法把问题缩成哪个更小的 (i', j'); "
          "③ 把几种做法用题目要的方式合起来 (求方案数用 +, 求最小用 min, 求能不能用 or)。")
    doc.svg(SLUG + "/general_core.svg",
            "图 0: dp[i][j] 依赖上 / 左 / 左上, 所以 i 从上到下、j 从左到右; 只读上一行, 所以更早的行可以丢掉")
    doc.p("<b>填表顺序。</b>不用背: 画出 dp[i][j] 依赖哪些格子, 这些格子必须先填好。依赖上 / 左 / 左上, 就是行从上到下、列从左到右。"
          "如果依赖的是<b>下一行</b>(第 6 题的 dp[i+1][j-1]), 就要从下往上填。")
    doc.p("<b>滚动数组。</b>如果 dp[i] 只读 dp[i-1] (和同一行左边), 只需要两行 prev / cur, 甚至一行原地更新, "
          "space 从 O(m*n) 降到 O(n)。代价: 丢了整张表, 如果要 <b>还原方案</b>(比如打印出 LCS 本身)就不能滚动。")
    doc.code(CODE["template"])
    doc.note("2D DP = 定义 dp[i][j] 的含义 → 问最后一步做了什么 → 依赖方向定填表顺序 → 只读上一行就滚动。")

    # ---------------- 1 ----------------
    doc.h2("1. Unique Paths: 最后一步从上或从左, 相加")
    doc.p("<b>题目。</b>m × n 的格子, 机器人从左上角走到右下角, 每次只能向右或向下, 有多少条不同路径? "
          "例: m = 3, n = 4 → 10。")
    doc.p("<b>Brute force。</b>递归 <code>f(i,j) = f(i-1,j) + f(i,j-1)</code>, O(2^(m+n)) time。浪费: 同一个格子被重复展开 (见图)。")
    doc.p("<b>关键观察。</b>到 (i,j) 的最后一步只可能从上面或左边来, 这两类路径不重叠、也没有遗漏 → 相加。"
          "第 0 行 / 第 0 列只有一种走法。")
    doc.svg(SLUG + "/unique_paths_core.svg", "图 1-1: 暴力递归里 f(1,2) 被算两遍; dp 表每格只算一次")
    doc.svg(SLUG + "/unique_paths_trace.svg", "图 1-2: m = 3, n = 4, 逐格填表, 每格 = 上面 + 左边")
    doc.code(CODE["unique_paths"])
    doc.p("<b>Complexity。</b>Time O(m*n): 每格 O(1)。Space O(m*n); 滚动成一行后 O(n)。")
    doc.note("grid 路径计数: dp[i][j] = 上 + 左, 第 0 行 / 列 = 1。")

    # ---------------- 2 ----------------
    doc.h2("2. Minimum Path Sum: 相加变 min, 多加自己")
    doc.p("<b>题目。</b>grid 每格有非负数, 从左上走到右下 (只能右 / 下), 求路径上数字之和的最小值。"
          "例: [[1,3,1],[1,5,1],[4,2,1]] → 7。")
    doc.p("<b>Brute force。</b>枚举所有路径 (Unique Paths 的那 C(m+n-2, m-1) 条), 每条求和。浪费: 不同路径共享大量前缀。")
    doc.p("<b>关键观察。</b>相比上一题, 改两处: ① 不再数路径条数, 而是求最小和, 所以 <b>+ 变 min</b>; "
          "② 每格有自己的代价, 所以要<b>加上 grid[i][j]</b>。"
          "之所以只看邻居的 dp 值就够, 是因为 optimal substructure: 到 (i,j) 的最优路径, 去掉最后一格后, 一定是到某个邻居的最优路径。")
    doc.svg(SLUG + "/min_path_sum_core.svg", "图 2-1: dp[1][1] 在 top 和 left 里选小的")
    doc.svg(SLUG + "/min_path_sum_trace.svg", "图 2-2: 3×3 grid 逐格填表, 每格写出 min 和加法")
    doc.code(CODE["min_path_sum"])
    doc.p("<b>Complexity。</b>Time O(m*n); Space O(m*n), 滚动后 O(n)。")
    doc.note("路径最小和: dp[i][j] = min(上, 左) + grid[i][j]。从 Unique Paths 改一行。")

    # ---------------- 3 ----------------
    doc.h2("3. Maximal Square: min(上, 左, 左上) + 1")
    doc.p("<b>题目。</b>0/1 矩阵, 找只含 1 的最大正方形, 返回面积。例: [\"10100\",\"10111\",\"11111\",\"10010\"] → 4。")
    doc.p("<b>Brute force。</b>枚举每个格子当左上角, 再枚举边长 k, 检查 k×k 是否全 1: O(m*n*min(m,n)²) (检查也要算)。"
          "浪费: 检查 k×k 全 1 时, 又把 (k-1)×(k-1) 检查了一遍。")
    doc.p("<b>关键观察。</b>改 state: <code>dp[i][j]</code> = 以 (i,j) 为<b>右下角</b>的最大全 1 正方形边长。"
          "当前格是 1 时, 想长成 (k+1)×(k+1), 它的上、左、左上三个邻居都必须能撑起 k×k。三个里最小的先撞墙, 所以边长 = 最小 + 1。"
          "这里依赖<b>三个</b>邻居, 是本文档里第一次用到左上。")
    doc.svg(SLUG + "/maximal_square_core.svg", "图 3-1: 三个邻居里最小的决定边长, 左上角的 0 把 diag 限制成 1")
    doc.svg(SLUG + "/maximal_square_trace.svg", "图 3-2: 4×5 矩阵, 补一圈 0 后逐格填表")
    doc.code(CODE["maximal_square"])
    doc.p("<b>Complexity。</b>Time O(m*n); Space O(m*n), 滚动成两行后 O(n)。答案是整张表的最大值 (不是右下角), 因为正方形可以在任何位置。")
    doc.note("最大正方形: 当前格是 1 → dp = min(上, 左, 左上) + 1; 答案取全表最大值再平方。")

    # ---------------- 4 ----------------
    doc.h2("4. Longest Common Subsequence: 比较两个前缀的最后一个字符")
    doc.p("<b>题目。</b>两个 string, 求最长公共子序列 (不要求连续) 的长度。例: \"abcde\", \"ace\" → 3 (\"ace\")。")
    doc.p("<b>Brute force。</b>枚举 text1 的所有子序列 (2^m 个), 逐个判断是不是 text2 的子序列, "
          "O(2^m * n)。浪费: 子序列的前半段被无数次重复判断。")
    doc.p("<b>关键观察。</b>从 grid 过渡到两个 string: <code>dp[i][j]</code> 看 <code>text1[:i]</code> 和 <code>text2[:j]</code>, "
          "i 和 j 分别是两个 string 的指针。最后一步: 看 text1[i-1] 和 text2[j-1]。相同 → 配对, 去掉这一对看左上; "
          "不同 → 至少有一个字符没用, 丢一个, 看上或左, 取 max。")
    doc.svg(SLUG + "/lcs_core.svg", "图 4-1: 最后字符相同 → 左上 + 1; 不同 → 丢一个字符, 取 max(上, 左)")
    doc.svg(SLUG + "/lcs_trace.svg", "图 4-2: \"abcde\" vs \"ace\", 相同的格子只依赖左上, 不同的依赖上 + 左")
    doc.code(CODE["lcs"])
    doc.p("<b>Complexity。</b>Time O(m*n); Space O(m*n), 滚动后 O(min(m,n)) (让短的当列)。")
    doc.note("两个 string 求最优: dp[i][j] 看两个前缀, 比最后一个字符: 相同 → 左上, 不同 → 丢一个。")

    # ---------------- 5 ----------------
    doc.h2("5. Edit Distance: 三种操作对应三个方向")
    doc.p("<b>题目。</b>把 word1 变成 word2, 每步可以 insert / delete / replace 一个字符, 求最少步数。"
          "例: \"horse\" → \"ros\" = 3。")
    doc.p("<b>Brute force。</b>每个位置试三种操作的递归, O(3^max(m,n))。浪费: 不同操作顺序会走到同一个 (i, j) 状态。")
    doc.p("<b>关键观察。</b>state 和 LCS 完全一样 (两个前缀), 变的是 transition 和 base:"
          "① 最后字符相同 → 白拿左上, 不加 1; ② 不同 → 三种操作, 对应<b>三个方向</b>:"
          "replace = 左上, delete = 上, insert = 左, 取 min 再 +1; "
          "③ base 不是 0: 第 0 行 / 第 0 列是 0, 1, 2, ... (全插入 / 全删除)。")
    doc.svg(SLUG + "/edit_distance_core.svg", "图 5-1: replace = 左上, delete = 上, insert = 左")
    doc.svg(SLUG + "/edit_distance_trace.svg", "图 5-2: \"horse\" → \"ros\", 相同时白拿左上, 不同时 1 + min(三个)")
    doc.code(CODE["edit_distance"])
    doc.p("<b>Complexity。</b>Time O(m*n); Space O(m*n), 滚动后 O(n)。")
    doc.note("Edit Distance = LCS 的 state + 三个方向 (替换 / 删 / 插) 取 min + 1, base 是 0..n。")

    # ---------------- 6 ----------------
    doc.h2("6. Longest Palindromic Substring: 先中心扩展, 再看 interval 填表")
    doc.p("<b>题目。</b>求 s 的最长回文子串 (连续)。例: \"babad\" → \"bab\" (\"aba\" 也对)。")
    doc.p("<b>Brute force。</b>枚举所有子串 O(n²), 每个检查是不是 palindrome O(n), 共 O(n³)。"
          "浪费: 检查 s[i..j] 时又把里面的 s[i+1..j-1] 检查了一遍。")
    doc.p("<b>最实用的解: 中心扩展。</b>palindrome 一定对称, 有一个中心。枚举 2n-1 个中心从中心往外扩, "
          "O(n²) time, O(1) space, 代码短、不容易错。面试首选这个。")
    doc.svg(SLUG + "/longest_palindromic_substring_core.svg", "图 6-1: babad 里几个中心的扩展; 两端不同或越界就停")
    doc.code(CODE["lps_expand"])
    doc.p("<b>Interval DP 版。</b>state 变成一段区间: <code>dp[i][j]</code> = s[i..j] 是不是 palindrome。"
          "最后一步: 看两端。<code>s[i] == s[j]</code> 且里面 <code>dp[i+1][j-1]</code> 也是 → True。"
          "<b>填表顺序是关键</b>: dp[i][j] 依赖下一行 (i+1) 的左边一格 (j-1), 所以 i 必须从大到小; "
          "按长度从短到长填也行, 这是 interval DP 的通用顺序。")
    doc.svg(SLUG + "/longest_palindromic_substring_trace.svg", "图 6-2: babad 的 dp 表, 从下往上填, 只用上三角")
    doc.code(CODE["lps_dp"])
    doc.p("<b>Complexity。</b>中心扩展: Time O(n²), Space O(1)。DP: Time O(n²), Space O(n²)。"
          "(另有 Manacher 算法 O(n), 面试不需要。)")
    doc.p("<b>Interval DP 的模板</b>(dp[i][j] 描述一段区间, 由更短的区间推出): "
          "<code>for length in range(2, n+1): for i in range(n-length+1): j = i+length-1</code>。"
          "最难的 Burst Balloons 就是这个套路, 在区间里枚举 \"最后一个\" 被戳的气球 k, 合并 dp[i][k] 和 dp[k][j]; 这里一句话带过, 不展开。")
    doc.note("最长回文子串: 面试写中心扩展 (O(n²), O(1))。interval DP 记住: 依赖更短的区间 → 从下往上 / 按长度填。")

    # ---------------- 7 ----------------
    doc.h2("7. Palindromic Substrings: 同一套中心, 改成计数")
    doc.p("<b>题目。</b>数 s 里有多少个回文子串 (位置不同算不同)。例: \"aba\" → 4。")
    doc.p("<b>Brute force。</b>O(n³), 同上一题。")
    doc.p("<b>关键观察。</b>相比上一题, 只改一件事: 不记最长, 而是<b>每扩一步成功 count += 1</b>。"
          "每个 palindrome 恰好有一个中心, 所以不重不漏。(DP 版也行: 数 dp 表里 True 的个数。)")
    doc.svg(SLUG + "/palindromic_substrings_core.svg", "图 7-1: aba 的 4 个 palindrome 分别属于哪个中心")
    doc.svg(SLUG + "/palindromic_substrings_trace.svg", "图 7-2: aba 的 5 个中心逐个扩展, count 一步步变成 4")
    doc.code(CODE["count_sub"])
    doc.p("<b>Complexity。</b>Time O(n²) (最坏全是同一个字符, 每个中心扩 O(n)); Space O(1)。")
    doc.note("数回文子串: 中心扩展, 每成功一步 count += 1。")

    # ---------------- 8 ----------------
    doc.h2("8. Regular Expression Matching: '*' 的两种选择")
    doc.p("<b>题目。</b>实现 <code>.</code> (任意一个字符) 和 <code>*</code> (前一个字符重复 0 次或多次) 的匹配, 要求<b>整个</b> s 被匹配。"
          "例: s = \"aab\", p = \"c*a*b\" → True。")
    doc.p("<b>Brute force。</b>递归: 遇到 '*' 就枚举吃几个, 最坏指数级。浪费: 同一对 (s 的位置, p 的位置) 被反复匹配。")
    doc.p("<b>关键观察。</b>state 和 LCS 一样 (两个前缀), 难在 <b>'*' 的 transition</b>。普通字符 / '.' : 各吃一个, 看左上。"
          "遇到 'x*' 有两种选择, 任一成立即可 (or):")
    doc.p("① <b>匹配 0 次</b>: 把 \"x*\" 整个去掉 → <code>dp[i][j-2]</code>; "
          "② <b>匹配 1 次并保留 pattern</b>: 前提 x 能匹配 s[i-1], s 去掉一个字符, 但 \"x*\" 还留着 → <code>dp[i-1][j]</code>。"
          "\"保留\" 是关键: 因为 x* 还可以继续吃前面的字符, 这样就不用枚举到底吃几个。")
    doc.svg(SLUG + "/regex_core.svg", "图 8-1: * 要么匹配 0 次 (往左跳 2 格), 要么吃掉一个字符并保留自己 (往上跳 1 格)")
    doc.svg(SLUG + "/regex_trace.svg", "图 8-2: s = aab, p = c*a*b, 每个 * 格子都写出两种选择")
    doc.code(CODE["regex"])
    doc.p("<b>Complexity。</b>Time O(m*n); Space O(m*n), 可滚动成 O(n)。")
    doc.note("正则 / 通配符匹配: dp[i][j] = s[:i] 匹配 p[:j]; '*' = (匹配 0 次: dp[i][j-2]) or (吃一个保留: dp[i-1][j])。")

    # ---------------- N ----------------
    doc.h2("9. 识别信号: 看到什么 → 试什么")
    doc.raw("""<table>
<tr><th>题目特征</th><th>做法</th><th>Complexity</th></tr>
<tr><td>grid 从左上走到右下, 只能右 / 下, 数方案 / 求最小和</td><td>dp[i][j] = 上 + 左 (数方案) 或 min(上, 左) + 自己 (最小和)</td><td>O(2^(m+n)) → O(m*n), 滚动后 space O(n)</td></tr>
<tr><td>0/1 矩阵里找最大的正方形</td><td>dp = 以 (i,j) 为右下角的边长 = min(上, 左, 左上) + 1</td><td>O(m*n*min(m,n)²) → O(m*n)</td></tr>
<tr><td>两个 string, 问公共 / 最长 / 最少操作</td><td>dp[i][j] 看 a[:i] 和 b[:j], 比较最后一个字符</td><td>指数 → O(m*n)</td></tr>
<tr><td>"最少 insert / delete / replace 几次"</td><td>Edit Distance: 左上 / 上 / 左 三个方向 + 1</td><td>O(3^n) → O(m*n)</td></tr>
<tr><td>子序列 (不连续) 对比两个 string</td><td>LCS 的变体: 不同时取 max(上, 左)</td><td>O(2^m) → O(m*n)</td></tr>
<tr><td>回文子串 (连续), 最长 / 计数</td><td>中心扩展, 2n-1 个中心。DP 备用: dp[i][j] = 两端相同 and dp[i+1][j-1]</td><td>O(n³) → O(n²), 中心扩展 space O(1)</td></tr>
<tr><td>pattern 匹配带 '*' / '?' / '.'</td><td>dp[i][j] = s[:i] 匹配 p[:j]; '*' 分两种选择 (0 次 / 吃一个保留)</td><td>指数 → O(m*n)</td></tr>
<tr><td>区间 [i, j] 由更短的区间合成 (戳气球、石子合并)</td><td>interval DP: 按长度从短到长填, 枚举分割点 k (Burst Balloons: 枚举最后戳哪个)</td><td>指数 → O(n³)</td></tr>
<tr><td>dp[i] 只读 dp[i-1]</td><td>滚动数组, 只留 prev / cur 两行</td><td>space O(m*n) → O(n)</td></tr>
</table>""")
    doc.p("<b>从 1D 过渡的例子: Decode Ways</b>(\"226\" → 3)。dp[i] = s 前 i 个字符的解码方式数, 最后一步 \"解一位\" 或 \"解两位\": "
          "<code>dp[i] = dp[i-1](末位 1-9) + dp[i-2](末两位 10-26)</code>。state 只需一个 index, 所以是 1D, 放在 14 号文档; "
          "但 \"问最后一步做了什么\" 的推法和本文档一模一样。")
    doc.h2("以后再学")
    doc.p("Manacher (最长回文子串 O(n))、Wildcard Matching ('*' 匹配任意串, 和 Regex 同一张表, '*' 只有 dp[i-1][j] 和 dp[i][j-1] 两个转移)、"
          "Burst Balloons / Strange Printer 等 interval DP、LCS 的 O(n log n) 变体 (转成 LIS)、还原具体方案 (从右下角沿 dp 表回溯)。")
    doc.write("docs/15-dp-2d.html")


def main():
    build_svgs()
    build_doc()


if __name__ == "__main__":
    main()
