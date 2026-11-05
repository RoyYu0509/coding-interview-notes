"""18 · String 基本功 + Trie  ->  docs/18-string-trie.html + docs/svg/18-string-trie/*.svg
运行: cd build && python3 -I 18_string_trie.py
trace 图里的数字都由本文件里真正跑过的代码算出来 (见 trace_* 函数和 assert)。
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import doclib as d  # noqa: E402

SLUG = "18-string-trie"
SVG_DIR = os.path.join(d.ROOT, "docs", "svg", SLUG)
os.makedirs(SVG_DIR, exist_ok=True)

# ---------------------------------------------------------------- SVG 工具
FONT = 'ui-sans-serif, system-ui, -apple-system, "PingFang SC", sans-serif'
ROLE = {  # fill, stroke, text
    "new": ("#E1F5EE", "#0F6E56", "#085041"),
    "old": ("#FAECE7", "#993C1D", "#712B13"),
    "plain": ("#F1EFE8", "#5F5E5A", "#444441"),
    "dim": ("#FFFFFF", "#B4B2A9", "#898781"),
}
RING = "#EF9F27"
GREY = "#52514E"
BLACK = "#0B0B0B"
SEP = "#B4B2A9"
RED_ARROW = "#D85A30"


def esc(s):
    return html.escape(str(s), quote=False)


class Svg:
    def __init__(self, title, desc=""):
        self.title, self.desc, self.e = title, desc, []

    def t(self, x, y, txt, size=12, fill=GREY, weight=400, anchor="start", mono=False):
        fam = ' font-family="ui-monospace, Menlo, Consolas, monospace"' if mono else ""
        self.e.append(
            '<text x="%s" y="%s" font-size="%d" fill="%s" font-weight="%d" text-anchor="%s"%s '
            'dominant-baseline="central">%s</text>' % (x, y, size, fill, weight, anchor, fam, esc(txt)))

    def rect(self, x, y, w, h, role="plain", rx=4, ring=False, dash=False):
        f, s, _ = ROLE[role]
        da = ' stroke-dasharray="4 3"' if (dash or role == "dim") else ""
        self.e.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" '
                      'stroke-width="1"%s/>' % (x, y, w, h, rx, f, s, da))
        if ring:
            self.e.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="none" '
                          'stroke="%s" stroke-width="2.5"/>' % (x - 3, y - 3, w + 6, h + 6, rx + 2, RING))

    def cell(self, x, y, w, h, label, role="plain", size=14, ring=False, weight=500, dash=False):
        self.rect(x, y, w, h, role, ring=ring, dash=dash)
        if label != "":
            self.t(x + w / 2, y + h / 2, label, size, ROLE[role][2], weight, "middle")

    def circ(self, cx, cy, r, label, role="plain", ring=False, size=14, dash=False):
        f, s, tc = ROLE[role]
        da = ' stroke-dasharray="4 3"' if (dash or role == "dim") else ""
        self.e.append('<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" stroke-width="1"%s/>'
                      % (cx, cy, r, f, s, da))
        if ring:
            self.e.append('<circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-width="2.5"/>'
                          % (cx, cy, r + 3.5, RING))
        if label != "":
            self.t(cx, cy, label, size, tc, 500, "middle")

    def line(self, x1, y1, x2, y2, color=SEP, w=1, dash=False):
        da = ' stroke-dasharray="4 3"' if dash else ""
        self.e.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s/>'
                      % (x1, y1, x2, y2, color, w, da))

    def arrow(self, x1, y1, x2, y2, color=GREY, dash=False, w=1.5):
        da = ' stroke-dasharray="5 4"' if dash else ""
        self.e.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s '
                      'marker-end="url(#arr)"/>' % (x1, y1, x2, y2, color, w, da))

    def path(self, d_, color=GREY, dash=False, w=1.5, arrow=True):
        da = ' stroke-dasharray="5 4"' if dash else ""
        m = ' marker-end="url(#arr)"' if arrow else ""
        self.e.append('<path d="%s" fill="none" stroke="%s" stroke-width="%s"%s%s/>' % (d_, color, w, da, m))

    def sep(self, y, x1=40, x2=640):
        self.line(x1, y, x2, y, SEP, 0.8, True)

    def legend(self, y, items, x=40):
        for kind, label in items:
            if kind == "ring":
                self.circ(x + 8, y, 6, "", "plain", ring=True)
                tx = x + 24
            else:
                self.rect(x, y - 7, 14, 14, kind)
                tx = x + 20
            self.t(tx, y, label, 12, GREY)
            x = tx + sum(12 if ord(c) > 127 else 6.6 for c in label) + 22

    def save(self, name, h):
        body = "\n".join(self.e)
        s = ('<svg width="100%%" viewBox="0 0 680 %d" role="img" xmlns="http://www.w3.org/2000/svg" '
             'font-family=\'%s\'><title>%s</title><desc>%s</desc>\n'
             '<defs><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" '
             'orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" '
             'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>\n%s\n</svg>\n'
             % (h, FONT.replace("'", ""), esc(self.title), esc(self.desc or self.title), body))
        with open(os.path.join(SVG_DIR, name + ".svg"), "w", encoding="utf-8") as f:
            f.write(s)
        return "%s/%s.svg" % (SLUG, name)


# ---- trie 画图: 布局 + 绘制
def build_trie(words):
    root = {}
    for w in words:
        n = root
        for c in w:
            n = n.setdefault(c, {})
    return root


def trie_layout(words, x0, y0, dx, dy):
    """返回 {prefix: (x, y)}; 叶子按顺序占 slot, 父亲居中。"""
    pos, slot = {}, [0]

    def rec(node, prefix, depth):
        if not node:
            x = slot[0]
            slot[0] += 1
        else:
            xs = [rec(ch, prefix + c, depth + 1) for c, ch in node.items()]
            x = (xs[0] + xs[-1]) / 2
        pos[prefix] = (x, depth)
        return x

    rec(build_trie(words), "", 0)
    return {p: (x0 + x * dx, y0 + dep * dy) for p, (x, dep) in pos.items()}


def draw_trie(s, pos, present, roles=None, ends=(), r=11, root_role="plain"):
    roles = roles or {}
    for p in sorted(present, key=len):
        if p and p[:-1] in present:
            (xa, ya), (xb, yb) = pos[p[:-1]], pos[p]
            s.line(xa, ya, xb, yb, "#898781", 1)
    for p in sorted(present, key=len):
        x, y = pos[p]
        if p == "":
            s.rect(x - 19, y - 10, 38, 20, roles.get("", root_role), rx=10)
            s.t(x, y, "root", 12, ROLE[roles.get("", root_role)][2], 500, "middle")
        else:
            s.circ(x, y, r, p[-1], roles.get(p, "plain"), ring=(p in ends))


def prefixes(words):
    out = {""}
    for w in words:
        for i in range(1, len(w) + 1):
            out.add(w[:i])
    return out


LEGEND_STD = [("new", "新进来的"), ("old", "被移除 / 死路"), ("plain", "已有的")]


# ---------------------------------------------------------------- 题目代码 (真正被执行并被 assert 的版本)
CODE_LCP = '''
def longestCommonPrefix(strs):
    first = strs[0]
    for j in range(len(first)):          # 一列一列往右走: 第 j 列
        c = first[j]                     # 以 strs[0] 这一列的字符当标准
        for s in strs[1:]:
            if j == len(s) or s[j] != c: # s 太短 或 字符不同 -> 第 j 列失败
                return first[:j]         # 前 j 列都过了, 答案就是 first[:j]
    return first                         # first 整个都是公共前缀
'''

CODE_ATOI = '''
def myAtoi(s):
    INT_MAX, INT_MIN = 2**31 - 1, -2**31
    i, n = 0, len(s)                           # i = parse 指针, 只向右走, 每个字符只看一次
    while i < n and s[i] == ' ':               # 阶段 1: 跳空格
        i += 1
    sign = 1
    if i < n and s[i] in '+-':                 # 阶段 2: 符号, 最多吃 1 个
        sign = -1 if s[i] == '-' else 1
        i += 1
    num = 0
    while i < n and '0' <= s[i] <= '9':        # 阶段 3: 数字, 遇到第一个非数字就停
        num = num * 10 + (ord(s[i]) - ord('0'))
        if sign * num > INT_MAX: return INT_MAX    # clamp: 一旦超界立刻返回,
        if sign * num < INT_MIN: return INT_MIN    # 后面的数字不用再看
        i += 1
    return sign * num
'''

CODE_REVERSE_ONE = '''
def reverseWords(s):
    return ' '.join(s.split()[::-1])   # split() 不带参数: 按连续空白切并丢掉空串
'''

CODE_REVERSE_SCAN = '''
def reverseWords(s):
    words, i = [], len(s) - 1                  # 同一个 parse 指针模板, 只是从右往左
    while i >= 0:
        while i >= 0 and s[i] == ' ':          # 阶段 1: 跳空格
            i -= 1
        if i < 0: break
        j = i                                  # j = 单词最后一个字符
        while i >= 0 and s[i] != ' ':          # 阶段 2: 吃一个单词
            i -= 1
        words.append(s[i + 1:j + 1])           # i 停在单词前一格, 单词 = s[i+1 .. j]
    return ' '.join(words)                     # 已经是倒序的了, join 一次
'''

CODE_S0 = '''
# str 不可变: s[0] = 'x' 会 TypeError, s += c 其实是 "新建一个 string"
res = ''
for c in s:
    res += c                  # 每次: 新 string = 旧 string 全部复制 + 1 个字符  -> 总共 O(n^2)

parts = []
for c in s:
    parts.append(c)           # list.append 摊销 O(1), 旧元素不动
res = ''.join(parts)          # 最后一次性分配 + 复制, O(n)
'''

CODE_S0_TOOLS = '''
"  a  b ".split()      # ['a', 'b']        不带参数: 连续空白当一个分隔符, 空串丢掉
"  a  b ".split(' ')   # ['', '', 'a', '', 'b', '']   带 ' ': 每个空格都切一刀, 留下空串
ord('d') - ord('a')    # 3   字母 -> 0..25, 拿来当 count[26] 的下标
c.isalnum()            # 字母或数字 (isdigit 对 '²' 之类也为 True, 要严格用 '0' <= c <= '9')
s[::-1]                # reverse, 返回新 string, O(n)
'''

CODE_TRIE = '''
class TrieNode:
    def __init__(self):
        self.children = {}        # char -> TrieNode
        self.is_end = False       # 有一个 word 刚好在这个 node 结束

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for c in word:
            if c not in node.children:      # 这条边不存在 -> 新建 node (图里的绿色)
                node.children[c] = TrieNode()
            node = node.children[c]         # 边已存在 -> 直接复用, 这就是 "共享前缀"
        node.is_end = True                  # 只在最后一个 node 标记

    def _walk(self, s):                     # 沿着 s 往下走, 走不通返回 None
        node = self.root
        for c in s:
            node = node.children.get(c)
            if node is None:
                return None
        return node

    def search(self, word):                 # 整个 word 存在吗
        node = self._walk(word)
        return node is not None and node.is_end    # 走得通还不够: "ap" 是前缀, 不一定是 word

    def startsWith(self, prefix):           # 有 word 以 prefix 开头吗
        return self._walk(prefix) is not None      # 走得通就够了
'''

CODE_SUGGEST = '''
class Node:
    def __init__(self):
        self.children = {}
        self.top3 = []                       # 经过这个 node 的 product 里, 字典序最小的 3 个

def suggestedProducts(products, searchWord):
    root = Node()
    for p in sorted(products):               # 先排序: 之后 append 的顺序天然就是字典序
        node = root
        for c in p:
            node = node.children.setdefault(c, Node())
            if len(node.top3) < 3:           # 已经满 3 个 -> 后来的更大, 直接忽略
                node.top3.append(p)
    res, node = [], root
    for c in searchWord:                     # 每敲一个字符, 往下走一步
        node = node.children.get(c) if node else None    # 走丢了 -> 之后每一步都是 []
        res.append(node.top3 if node else [])
    return res
'''

CODE_ADDSEARCH = '''
class WordDictionary:                         # TrieNode 同上
    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word):                  # 和 Trie.insert 一模一样
        node = self.root
        for c in word:
            node = node.children.setdefault(c, TrieNode())
        node.is_end = True

    def search(self, word):
        def dfs(node, i):                     # node = 已经匹配了 word[:i] 的 node
            if i == len(word):
                return node.is_end
            c = word[i]
            if c == '.':                      # 通配: 任何 child 都可能 -> 分叉, 有一条成功就行
                return any(dfs(ch, i + 1) for ch in node.children.values())
            ch = node.children.get(c)         # 普通字符: 只有一条路, O(1)
            return ch is not None and dfs(ch, i + 1)
        return dfs(self.root, 0)
'''

CODE_WS2 = '''
class Node:
    def __init__(self):
        self.children = {}
        self.word = None                      # 在这里结束的 word (存整个 word, 找到时直接用)

def findWords(board, words):
    root = Node()
    for w in words:                           # 先把所有 word 建成一棵 trie
        node = root
        for c in w:
            node = node.children.setdefault(c, Node())
        node.word = w
    R, C, res = len(board), len(board[0]), []

    def dfs(r, c, parent):
        ch = board[r][c]
        node = parent.children[ch]            # 调用前已保证 ch 在 parent.children 里
        if node.word:
            res.append(node.word)
            node.word = None                  # 找到后删 word: 不会重复收, 也让这个 node 可以被摘掉
        board[r][c] = '#'                     # choose: 标记已访问 ('#' 不在任何 children 里)
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and board[nr][nc] in node.children:
                dfs(nr, nc, node)             # 剪枝 1: trie 里没有这个字符 -> 根本不进去
        board[r][c] = ch                      # un-choose: 回溯
        if not node.children and node.word is None:
            del parent.children[ch]           # 剪枝 2: node 变成死胡同 -> 从 trie 摘掉

    for r in range(R):
        for c in range(C):
            if board[r][c] in root.children:
                dfs(r, c, root)
    return res
'''

# 把代码字符串真正 exec 出来, 后面的 trace 数据和 assert 用它们
NS = {}
for _name, _code in [("LCP", CODE_LCP), ("ATOI", CODE_ATOI), ("REV1", CODE_REVERSE_ONE),
                     ("REV2", CODE_REVERSE_SCAN), ("TRIE", CODE_TRIE), ("SUG", CODE_SUGGEST),
                     ("ADD", CODE_ADDSEARCH), ("WS2", CODE_WS2)]:
    NS[_name] = {}
    exec(_code, NS[_name])
# ADD 用到 TrieNode
NS["ADD"] = {"TrieNode": NS["TRIE"]["TrieNode"]}
exec(CODE_ADDSEARCH, NS["ADD"])

# ---- 正确性测试 (整个文件每次 build 都会跑)
_lcp = NS["LCP"]["longestCommonPrefix"]
assert _lcp(["flower", "flow", "flight"]) == "fl"
assert _lcp(["dog", "racecar", "car"]) == ""
assert _lcp(["interview", "internet", "interval", "intern"]) == "inter"
assert _lcp(["a"]) == "a" and _lcp(["ab", "a"]) == "a" and _lcp(["", "b"]) == ""

_atoi = NS["ATOI"]["myAtoi"]
for _s, _w in [("42", 42), ("   -042", -42), ("1337c0d3", 1337), ("0-1", 0), ("words and 987", 0),
               ("  -42x", -42), ("-91283472332", -2147483648), ("91283472332", 2147483647),
               ("+1", 1), ("+-12", 0), ("", 0), ("   ", 0), ("2147483647", 2147483647),
               ("-2147483648", -2147483648), ("2147483648", 2147483647), ("-2147483649", -2147483648)]:
    assert _atoi(_s) == _w, (_s, _atoi(_s), _w)

for _k in ("REV1", "REV2"):
    _f = NS[_k]["reverseWords"]
    for _s, _w in [("the sky is blue", "blue is sky the"), ("  hello world  ", "world hello"),
                   ("a good   example", "example good a"), ("  the sky  is blue ", "blue is sky the"),
                   ("x", "x"), ("   ", "")]:
        assert _f(_s) == _w, (_k, _s, _f(_s))

_T = NS["TRIE"]["Trie"]()
for _w in ["app", "apple", "apt", "bat"]:
    _T.insert(_w)
assert _T.search("app") and not _T.search("ap") and _T.startsWith("ap") and not _T.search("bar")
assert _T.search("apple") and not _T.startsWith("c") and not _T.search("apples")

_prods = ["mobile", "mouse", "moneypot", "monitor", "mousepad"]
_sug = NS["SUG"]["suggestedProducts"](_prods, "mouse")
assert _sug == [["mobile", "moneypot", "monitor"], ["mobile", "moneypot", "monitor"],
                ["mouse", "mousepad"], ["mouse", "mousepad"], ["mouse", "mousepad"]], _sug
assert NS["SUG"]["suggestedProducts"](["havana"], "tatiana") == [[]] * 7
assert NS["SUG"]["suggestedProducts"](["bags", "baggage", "banner", "box", "cloths"], "bags") == [
    ["baggage", "bags", "banner"], ["baggage", "bags", "banner"], ["baggage", "bags"], ["bags"]]
assert NS["SUG"]["suggestedProducts"](["havana"], "havanat") == [["havana"]] * 6 + [[]]

_W = NS["ADD"]["WordDictionary"]()
for _w in ["bad", "dad", "mad", "mid"]:
    _W.addWord(_w)
assert [_W.search(q) for q in ["pad", "bad", ".ad", "b..", ".id", "..d", "...", "....", "b.x", "m.d", "."]] == \
       [False, True, True, True, True, True, True, False, False, True, False]

_BOARD = [list("oaan"), list("etae"), list("ihkr"), list("iflv")]
_got = NS["WS2"]["findWords"]([r[:] for r in _BOARD], ["oath", "pea", "eat", "rain"])
assert _got == ["oath", "eat"], _got
assert NS["WS2"]["findWords"]([list("ab"), list("cd")], ["abcb"]) == []
assert sorted(NS["WS2"]["findWords"]([list("ab"), list("cd")], ["ab", "abdc", "acdb", "ba"])) == \
       ["ab", "abdc", "acdb", "ba"]
print("all code asserts passed")


# ================================================================ 图: 第 0 节 + LCP + atoi + Reverse Words
def fig_s0_core():
    n = 8
    s = Svg("s += c 与 list.append + join 的复制量对比",
            "n = 8, 左边每次 += 都复制旧内容, 右边 append 只写 1 格, join 最后复制一次")
    s.t(40, 18, "n = 8 · 每一行 = 循环里的一次操作 · 每个格子 = 一次字符的复制或写入", 12)
    s.t(40, 38, "str 不可变: s += c 要新建 string, 把旧内容全部复制过去; list.append 不动旧元素", 12)
    s.t(40, 64, "res += c", 14, BLACK, 500)
    s.t(360, 64, "parts.append(c), 最后 ''.join(parts)", 14, BLACK, 500)
    s.sep(76)
    y0, rh = 86, 24
    tot_l = 0
    for i in range(1, n + 1):
        y = y0 + (i - 1) * rh
        for k in range(i):
            s.cell(40 + k * 18, y, 16, 18, "", "new" if k == i - 1 else "old")
        s.t(196, y + 9, "复制 %d + 写 1 = %d" % (i - 1, i), 12)
        tot_l += i
        for k in range(i):
            s.cell(360 + k * 18, y, 16, 18, "", "new" if k == i - 1 else "plain")
        s.t(516, y + 9, "append: 只写 1", 12)
    assert tot_l == 36 == n * (n + 1) // 2
    yj = y0 + n * rh + 6
    s.sep(yj - 5)
    for k in range(n):
        s.cell(360 + k * 18, yj + 4, 16, 18, "", "plain")
    s.t(516, yj + 13, "join: 复制 8 (一次)", 12)
    s.t(40, yj + 13, "合计 1 + 2 + ... + 8 = 36 = n(n+1)/2", 14, BLACK, 500)
    s.t(40, yj + 36, "n 个字符 -> O(n^2)", 14, BLACK, 500)
    s.t(360, yj + 36, "8 次 append + join 8 = 8 + 8 = 16 -> O(n)", 14, BLACK, 500)
    s.legend(yj + 70, [("new", "这一步新写入的字符"), ("old", "被复制的旧字符 (浪费)"),
                       ("plain", "没被碰的字符")])
    return s.save("s0_core", yj + 90)


LCP_WORDS = ["interview", "internet", "interval", "intern"]


def fig_lcp_core():
    s = Svg("Longest Common Prefix: 纵向逐列比较", "第 0-4 列全相同, 第 5 列 v != n 停止")
    s.t(40, 18, "strs = [interview, internet, interval, intern] · 竖着一列一列比", 12)
    s.t(40, 38, "一整列全相同才进下一列; 前面的列已经确认过, 不回头", 12)
    x0, w, h, y0 = 130, 38, 30, 84
    for j in range(9):
        s.t(x0 + j * (w + 2) + w / 2, 62, "j=%d" % j, 12, GREY, 400, "middle")
    for r, word in enumerate(LCP_WORDS):
        y = y0 + r * 38
        s.t(40, y + h / 2, "strs[%d]" % r, 12)
        for j, ch in enumerate(word):
            role = "new" if j < 5 else "dim"
            if j == 5:
                role = "plain" if r == 0 else ("old" if r == 1 else "dim")
            s.cell(x0 + j * (w + 2), y, w, h, ch, role, ring=(j == 5 and r == 0))
    yb = y0 + 4 * 38 + 8
    xl, xr = x0, x0 + 4 * (w + 2) + w
    s.path("M%d %d L%d %d" % (xl, yb, xr, yb), "#0F6E56", arrow=False)
    s.t((xl + xr) / 2, yb + 18, "前 5 列全相同: prefix = 'inter'", 14, "#085041", 500, "middle")
    x5 = x0 + 5 * (w + 2) + w / 2
    s.path("M%d %d L%d %d" % (x5, yb + 10, x5 + 30, yb + 34), RED_ARROW, arrow=False)
    s.t(x5 + 36, yb + 44, "第 5 列: strs[1][5] = 'n' ≠ 'v' -> 立刻 return first[:5]", 12, "#712B13")
    s.t(40, yb + 78, "每个字符最多被看 1 次: 总共 O(n · m) = O(所有字符数 S), 已经是下界", 14, BLACK, 500)
    s.legend(yb + 108, [("new", "这一列全相同"), ("ring", "c = strs[0][5]"), ("old", "第一个不同的字符"), ("dim", "没看 (不用看)")])
    return s.save("lcp_core", yb + 128)


def lcp_trace_rows(strs):
    """模拟 longestCommonPrefix, 记录每一列看了哪些格子。"""
    rows, first = [], strs[0]
    for j in range(len(first)):
        c = first[j]
        checked = [(0, c)]
        for k, w in enumerate(strs[1:], 1):
            ch = w[j] if j < len(w) else None
            checked.append((k, ch))
            if ch != c:
                rows.append((j, c, checked, False))
                return rows, first[:j]
        rows.append((j, c, checked, True))
    return rows, first


def fig_lcp_trace():
    rows, ans = lcp_trace_rows(LCP_WORDS)
    assert ans == NS["LCP"]["longestCommonPrefix"](LCP_WORDS) == "inter" and len(rows) == 6
    s = Svg("LCP trace", "interview/internet/interval/intern 逐列比较")
    s.t(40, 18, "c = strs[0][j] · 依次拿 strs[1], strs[2], strs[3] 的 s[j] 和 c 比 · 全相等才 j += 1", 12)
    s.t(40, 38, "任何一个不等 (或 s 太短) 就停, 答案 = first[:j]", 12)
    cx = [130, 200, 270, 340]
    s.t(40, 64, "j", 12)
    for k, wd in enumerate(LCP_WORDS):
        s.t(cx[k] + 22, 64, wd, 12, GREY, 400, "middle")
    s.t(410, 64, "这一列的结果", 12)
    s.sep(76)
    y = 86
    for (j, c, checked, ok) in rows:
        s.t(40, y + 20, str(j), 16, BLACK, 500)
        done = {k: ch for k, ch in checked}
        for k in range(4):
            if k not in done:
                s.cell(cx[k], y + 4, 44, 32, "", "dim")
                continue
            ch = done[k]
            if k == 0:
                role = "plain"
            else:
                role = "new" if ch == c else "old"
            s.cell(cx[k], y + 4, 44, 32, ch if ch else "∅", role, ring=(k == 0))
        if ok:
            s.t(410, y + 12, "4 个都 == '%s'" % c, 12)
            s.t(410, y + 30, "prefix = '%s'" % LCP_WORDS[0][:j + 1], 14, BLACK, 500)
        else:
            bad = checked[-1]
            s.t(410, y + 12, "strs[%d][%d] = '%s' ≠ '%s'" % (bad[0], j, bad[1], c), 12, "#712B13")
            s.t(410, y + 30, "return first[:%d]" % j, 14, BLACK, 500)
        y += 46
        s.sep(y - 4)
    s.t(40, y + 12, "答案 = 'inter' (长度 5)", 16, BLACK, 500)
    s.legend(y + 40, [("ring", "c = strs[0][j] (标准)"), ("new", "和 c 相同"), ("old", "和 c 不同 -> 停"),
                      ("dim", "没检查")])
    return s.save("lcp_trace", y + 60)


ATOI_S = "  -42x"


def fig_atoi_core():
    s = Svg("atoi: parse 指针 i 的三个阶段", "指针 i 只向右走, 依次跳空格 -> 符号 -> 数字, 遇到非数字停")
    s.t(40, 18, "s = '  -42x' · i 是一根只向右走的 parse 指针, 每个字符只看一次", 12)
    s.t(40, 38, "每个阶段 = 一个 while / if, 条件不满足就把 i 留给下一个阶段", 12)
    x0, w, h, y0 = 150, 44, 34, 84
    roles = ["plain", "plain", "plain", "new", "new", "old"]
    for k, ch in enumerate(ATOI_S):
        x = x0 + k * (w + 2)
        s.t(x + w / 2, y0 - 14, "i=%d" % k, 12, GREY, 400, "middle")
        s.cell(x, y0, w, h, "␣" if ch == " " else ch, roles[k], ring=(k == 2), dash=(k < 2))
    # 阶段括号
    yb = y0 + h + 14
    xs = lambda a, b: (x0 + a * (w + 2), x0 + b * (w + 2) - 2)
    phases = [(0, 2, "阶段 1", "跳空格", "while s[i] == ' ': i += 1", "i: 0 -> 2"),
              (2, 3, "阶段 2", "符号", "sign = -1, i += 1", "i: 2 -> 3"),
              (3, 5, "阶段 3", "数字", "num = num*10 + d", "i: 3 -> 5"),
              (5, 6, "停", "非数字", "return sign * num", "i = 5")]
    for k, (a, b, name, what, rule, iv) in enumerate(phases):
        xa, xb = xs(a, b)
        s.path("M%d %d L%d %d" % (xa, yb, xb, yb), GREY, arrow=False)
    # 文字放在下面四行 (每个阶段一行, 避免挤)
    ty = yb + 28
    for k, (a, b, name, what, rule, iv) in enumerate(phases):
        yy = ty + k * 26
        s.rect(40, yy - 9, 100, 20, "new" if k == 2 else ("old" if k == 3 else "plain"), rx=3)
        s.t(90, yy + 1, name + " " + what if k < 3 else name, 12, ROLE["plain"][2], 500, "middle")
        s.t(152, yy + 1, rule, 12, BLACK)
        s.t(420, yy + 1, iv + "   (s[%d:%d] = '%s')" % (a, b, ATOI_S[a:b].replace(" ", "␣")), 12)
    s.t(40, ty + 4 * 26 + 12, "总共 O(n) 时间, O(1) 空间: 指针不回头, 也不 slice 出子串", 14, BLACK, 500)
    s.legend(ty + 4 * 26 + 44, [("ring", "当前 i (符号)"), ("new", "吃进 num 的数字"),
                                ("old", "停下的字符"), ("dim", "被跳过的空格")])
    return s.save("atoi_core", ty + 4 * 26 + 64)


def atoi_trace_rows(s_):
    """逐步模拟 CODE_ATOI, 返回每步 (i, 动作, sign, num)。"""
    INT_MAX, INT_MIN = 2**31 - 1, -2**31
    i, n = 0, len(s_)
    rows = []
    sign, num = 1, 0
    while i < n and s_[i] == " ":
        rows.append((i, "skip", sign, num))
        i += 1
    if i < n and s_[i] in "+-":
        sign = -1 if s_[i] == "-" else 1
        rows.append((i, "sign", sign, num))
        i += 1
    while i < n and "0" <= s_[i] <= "9":
        num = num * 10 + (ord(s_[i]) - ord("0"))
        rows.append((i, "digit", sign, num))
        i += 1
    rows.append((i, "stop", sign, num))
    return rows, sign * num


def fig_atoi_trace():
    rows, val = atoi_trace_rows(ATOI_S)
    assert val == -42 == NS["ATOI"]["myAtoi"](ATOI_S) and len(rows) == 6
    s = Svg("atoi trace", "  -42x 逐字符解析, 外加溢出 clamp 的例子")
    s.t(40, 18, "s = '  -42x' · 每一步看 s[i], 然后 i 向右走 1 格 · sign 初始 1, num 初始 0", 12)
    s.t(40, 38, "INT_MAX = 2147483647 · INT_MIN = -2147483648", 12)
    s.t(40, 64, "当前 s[i] (i 指针)", 12)
    s.t(300, 64, "sign", 12)
    s.t(360, 64, "num", 12)
    s.t(430, 64, "这一步做什么", 12)
    s.sep(76)
    y = 84
    x0, w = 40, 36
    txt = {"skip": "阶段 1: s[i] == ' ' -> i += 1", "sign": "阶段 2: s[i] == '-' -> sign = -1",
           "stop": "'x' 不是数字 -> 停, 返回 sign * num"}
    for (i, kind, sign, num) in rows:
        for k, ch in enumerate(ATOI_S):
            x = x0 + k * 40
            if k == i:
                role = {"skip": "old", "sign": "plain", "digit": "new", "stop": "old"}[kind]
                s.cell(x, y + 4, 36, 30, "␣" if ch == " " else ch, role, ring=True)
            else:
                s.cell(x, y + 4, 36, 30, "␣" if ch == " " else ch, "dim")
        s.t(40 + i * 40 + 18, y + 46, "↑ i=%d" % i, 12, GREY, 400, "middle")
        s.t(300, y + 19, str(sign), 14, BLACK, 500)
        s.t(360, y + 19, str(num), 14, BLACK, 500)
        if kind == "digit":
            prev = num // 10 if i > 3 else 0
            dig = int(ATOI_S[i])
            s.t(430, y + 19, "阶段 3: num = %d*10 + %d = %d, i += 1" % (prev, dig, num), 12, BLACK)
        elif kind == "stop":
            s.t(430, y + 11, txt[kind], 12, "#712B13")
            s.t(430, y + 29, "-1 × 42 = -42", 14, BLACK, 500)
        else:
            s.t(430, y + 19, txt[kind], 12, BLACK)
        y += 58
        s.sep(y - 4)
    # 溢出
    s.t(40, y + 10, "溢出例子: s = '-91283472332' (11 位数字)", 14, BLACK, 500)
    big = "-91283472332"
    # 用真代码走一遍, 找到溢出的那一位
    num, sign, hit = 0, -1, None
    for k, ch in enumerate(big[1:]):
        num = num * 10 + int(ch)
        if sign * num < -2**31:
            hit = (k, num)
            break
        before = num
    assert hit and hit[1] == 9128347233 and before == 912834723
    assert NS["ATOI"]["myAtoi"](big) == -2147483648
    s.t(40, y + 36, "前 9 位一路累加: num = 912834723, sign * num = -912834723 ≥ INT_MIN, 继续", 12, BLACK)
    s.t(40, y + 58, "第 10 位 '3': num = 912834723*10 + 3 = 9128347233", 12, BLACK)
    s.cell(40, y + 72, 520, 28, "", "old")
    s.t(50, y + 86, "sign * num = -9128347233 < INT_MIN = -2147483648 -> return INT_MIN", 12, ROLE["old"][2], 500)
    s.t(40, y + 118, "答案: ' -42x' -> -42 · '-91283472332' -> -2147483648", 14, BLACK, 500)
    s.legend(y + 146, [("ring", "当前 s[i]"), ("new", "数字 (进 num)"), ("old", "跳过 / 停下"),
                       ("dim", "别的字符")])
    return s.save("atoi_trace", y + 166)


REV_S = "  the sky  is blue "


def rev_trace_rows(s_):
    words, i, rows = [], len(s_) - 1, []
    while i >= 0:
        while i >= 0 and s_[i] == " ":
            i -= 1
        if i < 0:
            break
        j = i
        while i >= 0 and s_[i] != " ":
            i -= 1
        words.append(s_[i + 1:j + 1])
        rows.append((i, j, list(words)))
    return rows, " ".join(words)


def fig_rev_core():
    s = Svg("Reverse Words: split -> reversed -> join", "split() 吃掉连续空白; split(' ') 留下空串")
    s.t(40, 18, "s = '  the sky  is blue ' (19 个字符, 前后和中间都有多余空格)", 12)
    s.t(40, 38, "三步: split() 切成 words -> 倒序 -> ' '.join", 12)
    x0, w = 40, 30
    for k, ch in enumerate(REV_S):
        s.cell(x0 + k * 32, 54, w, 28, "␣" if ch == " " else ch, "dim" if ch == " " else "plain", size=14)
    # split() 之后
    lst = REV_S.split()
    assert lst == ["the", "sky", "is", "blue"]
    s.arrow(340, 90, 340, 114)
    s.t(350, 102, "s.split()", 14, BLACK, 500)
    xx = 40
    for wd in lst:
        ww = 14 * len(wd) + 18
        s.cell(xx, 120, ww, 28, wd, "new")
        xx += ww + 8
    s.t(xx + 4, 134, "4 个 word, 空串一个都没有", 12)
    s.arrow(340, 156, 340, 180)
    s.t(350, 168, "[::-1]", 14, BLACK, 500)
    xx = 40
    for wd in lst[::-1]:
        ww = 14 * len(wd) + 18
        s.cell(xx, 186, ww, 28, wd, "new")
        xx += ww + 8
    s.arrow(340, 222, 340, 246)
    s.t(350, 234, "' '.join(...)", 14, BLACK, 500)
    s.cell(40, 252, 160, 28, "blue is sky the", "new", size=14)
    # 对比 split(' ')
    s.sep(300)
    bad = REV_S.split(" ")
    assert bad == ["", "", "the", "sky", "", "is", "blue", ""]
    s.t(40, 318, "对比: s.split(' ') 每个空格切一刀 -> 8 项, 里面 4 个是空串 ''", 14, BLACK, 500)
    xx = 40
    for wd in bad:
        ww = 14 * max(len(wd), 1) + 18 if wd else 26
        s.cell(xx, 332, ww, 28, wd if wd else "''", "old" if wd == "" else "plain", size=12 if wd == "" else 14)
        xx += ww + 6
    s.t(40, 382, "join 之后会多出多余空格 -> 错. 记住: 要 '去掉多余空格' 就用不带参数的 split()", 12)
    s.legend(404, [("new", "有用的 word"), ("old", "空串 ''"), ("dim", "空格 (␣)")])
    return s.save("rev_core", 424)


def fig_rev_trace():
    rows, ans = rev_trace_rows(REV_S)
    assert ans == "blue is sky the" and len(rows) == 4
    assert [r[2][-1] for r in rows] == ["blue", "is", "sky", "the"]
    s = Svg("Reverse Words 从右往左扫描 trace", "i 从右往左, 跳空格, 吃一个单词, append")
    s.t(40, 18, "同一个 parse 指针模板, 只是从右往左 · j = 单词最后一格 · i 吃完单词后停在它的前一格", 12)
    s.t(40, 38, "单词 = s[i+1 .. j] · words 里已经是倒序", 12)
    s.t(40, 64, "s (19 格) 和指针", 12)
    s.t(420, 64, "append 之后 words", 12)
    s.sep(76)
    y = 84
    for (i, j, words) in rows:
        for k, ch in enumerate(REV_S):
            role = "new" if i < k <= j else "dim"
            s.cell(40 + k * 19, y + 4, 17, 26, "␣" if ch == " " else ch, role, size=12)
        s.t(40 + j * 19 + 8.5, y + 44, "j=%d" % j, 12, "#085041", 500, "middle")
        xi = 40 + max(i, 0) * 19 + 8.5
        s.t(xi, y + 44, "i=%d" % i, 12, "#712B13", 500, "middle")
        word = REV_S[i + 1:j + 1]
        s.t(420, y + 12, "s[%d:%d] = '%s'" % (i + 1, j + 1, word), 12)
        s.t(420, y + 32, "words = %s" % str(words).replace("'", "'"), 14, BLACK, 500)
        y += 66
        s.sep(y - 6)
    s.t(40, y + 10, "i = -1 -> 退出循环 · ' '.join(['blue', 'is', 'sky', 'the'])", 12)
    s.t(40, y + 34, "答案: 'blue is sky the'", 16, BLACK, 500)
    s.legend(y + 62, [("new", "这一步吃进来的单词"), ("dim", "别的字符 / 空格 (␣)")])
    return s.save("rev_trace", y + 82)



# ================================================================ 图: Trie
TRIE_WORDS = ["app", "apple", "apt", "bat"]


def trie_end_prefixes(words, upto):
    return set(words[:upto])


def fig_trie_core():
    words = TRIE_WORDS
    nodes = prefixes(words) - {""}
    assert sum(len(w) for w in words) == 14 and len(nodes) == 9
    s = Svg("Trie: 共享前缀只存一次", "list 里 ap 存 3 次, trie 里 a-p 两个 node 只存 1 次")
    s.t(40, 18, "words = [app, apple, apt, bat] · 它们的前缀 'ap' 一共出现了 3 次", 12)
    s.t(40, 38, "Trie 把相同前缀合并成同一条路径: 每个字符一个 node, 公共前缀的 node 只建一次", 12)
    s.t(40, 64, "list: 每个 word 单独存", 14, BLACK, 500)
    s.t(310, 64, "trie: 共享前缀合并", 14, BLACK, 500)
    s.sep(76)
    for r, w in enumerate(words):
        y = 92 + r * 40
        for k, ch in enumerate(w):
            role = "old" if (k < 2 and w.startswith("ap")) else "plain"
            s.cell(40 + k * 32, y, 30, 28, ch, role)
    pos = trie_layout(words, 400, 104, 52, 32)
    pres = prefixes(words)
    roles = {"a": "new", "ap": "new"}
    draw_trie(s, pos, pres, roles, ends=set(words))
    s.t(40, 304, "共 3+5+3+3 = 14 个字符", 14, BLACK, 500)
    s.t(310, 304, "共 a,p,p,l,e,t,b,a,t = 9 个 node", 14, BLACK, 500)
    s.t(40, 332, "startsWith('ap'): 扫 4 个 word,", 12)
    s.t(40, 350, "每个比 2 个字符 -> O(N · L)", 12)
    s.t(310, 332, "startsWith('ap'): 从 root 走 a -> p 两条边", 12)
    s.t(310, 350, "和 word 总数 N 无关 -> O(L)", 12)
    s.legend(386, [("old", "list 里重复存的 'ap'"), ("new", "trie 里只存 1 次的 a, p"),
                   ("ring", "is_end = True")])
    return s.save("trie_core", 406)


def trie_steps():
    """真正按 CODE_TRIE 的逻辑插入, 记录每步新建了哪些 node。"""
    seen, steps = {""}, []
    for k, w in enumerate(TRIE_WORDS):
        new = []
        for i in range(1, len(w) + 1):
            if w[:i] not in seen:
                seen.add(w[:i])
                new.append(w[:i])
        steps.append((w, new, set(seen), set(TRIE_WORDS[:k + 1])))
    return steps


def fig_trie_trace():
    steps = trie_steps()
    assert [len(x[1]) for x in steps] == [3, 2, 1, 3]
    # 再用真代码核对 node 总数
    tr = NS["TRIE"]["Trie"]()

    def count(n):
        return 1 + sum(count(c) for c in n.children.values())
    tot = []
    for w in TRIE_WORDS:
        tr.insert(w)
        tot.append(count(tr.root) - 1)
    assert tot == [3, 5, 6, 9]
    s = Svg("Trie insert trace", "依次 insert app, apple, apt, bat, 每步新建的 node 画成绿色")
    s.t(40, 18, "依次 insert: app, apple, apt, bat · 每个字符: 边已存在 -> 复用 · 不存在 -> 新建 node", 12)
    s.t(40, 38, "圈住的 node = is_end 为 True (有 word 在这里结束)", 12)
    s.t(40, 64, "insert", 12)
    s.t(180, 64, "insert 之后的 trie", 12)
    s.t(430, 64, "新建 / 复用", 12)
    s.sep(76)
    y = 84
    notes = [("新建 a, p, p (3 个)", "第 2 个 p: is_end = True", "总 node 数 = 3"),
             ("复用 a, p, p · 新建 l, e (2 个)", "e: is_end = True", "总 node 数 = 3 + 2 = 5"),
             ("复用 a, p · 新建 t (1 个)", "t: is_end = True", "总 node 数 = 5 + 1 = 6"),
             ("root 下没有 'b' -> 新建 b, a, t (3 个)", "t: is_end = True", "总 node 数 = 6 + 3 = 9")]
    for (w, new, seen, ends), (n1, n2, n3) in zip(steps, notes):
        depth = max(len(p) for p in seen)
        pos = trie_layout(TRIE_WORDS[:TRIE_WORDS.index(w) + 1], 215, 0, 48, 34)
        h = depth * 34 + 40
        yy = y + 20
        p2 = {k: (v[0], v[1] + yy) for k, v in pos.items()}
        s.t(40, yy + depth * 17, "insert('%s')" % w, 14, BLACK, 500)
        roles = {p: "new" for p in new}
        draw_trie(s, p2, seen, roles, ends)
        s.t(430, yy + depth * 17 - 18, n1, 12, BLACK)
        s.t(430, yy + depth * 17, n2, 12)
        s.t(430, yy + depth * 17 + 18, n3, 14, BLACK, 500)
        y += h
        s.sep(y - 4)
    # 查询
    s.t(40, y + 14, "在最终的 trie 上查询 (沿着字符往下走)", 14, BLACK, 500)
    tr2 = NS["TRIE"]["Trie"]()
    for w in TRIE_WORDS:
        tr2.insert(w)
    qs = [("search('app')", "a -> p -> p 走通, is_end = True", tr2.search("app"), True),
          ("search('ap')", "a -> p 走通, 但 is_end = False", tr2.search("ap"), False),
          ("startsWith('ap')", "a -> p 走通就够了", tr2.startsWith("ap"), True),
          ("search('bar')", "b -> a 走通, 'r' 不在 children 里", tr2.search("bar"), False)]
    yy = y + 40
    for q, why, got, want in qs:
        assert got == want
        s.t(40, yy, q, 12, BLACK, 500, mono=True)
        s.t(210, yy, why, 12)
        s.cell(560, yy - 11, 60, 22, str(got), "new" if got else "old", size=12)
        yy += 28
    s.legend(yy + 14, [("new", "这一步新建的 node"), ("plain", "已有的 node (复用)"), ("ring", "is_end = True")])
    return s.save("trie_trace", yy + 34)


# ---- Search Suggestions
def sug_tops():
    root = NS["SUG"]["Node"]()
    for p in sorted(_prods):
        node = root
        for c in p:
            node = node.children.setdefault(c, NS["SUG"]["Node"]())
            if len(node.top3) < 3:
                node.top3.append(p)

    def get(pref):
        n = root
        for c in pref:
            n = n.children[c]
        return n.top3
    return get


def fig_sug_core():
    get = sug_tops()
    srt = sorted(_prods)
    assert srt == ["mobile", "moneypot", "monitor", "mouse", "mousepad"]
    assert get("m") == get("mo") == ["mobile", "moneypot", "monitor"]
    assert get("mob") == ["mobile"] and get("mon") == ["moneypot", "monitor"]
    assert get("mou") == get("mous") == get("mouse") == ["mouse", "mousepad"]
    s = Svg("Search Suggestions: 每个 node 存 top 3", "先排序再 insert, 每个 node 的 top3 就是经过它的前 3 个 product")
    s.t(40, 18, "products 先 sorted, 再依次 insert · 沿路每个 node: 不足 3 个就 append (后来的更大, 不用比较)", 12)
    s.t(40, 38, "这样每个 node 里存的 top3, 就是 '以这个前缀开头' 的答案, 查询时不用再搜", 12)
    s.t(40, 64, "sorted:", 12)
    x = 96
    for k, p in enumerate(srt):
        w = 7 * len(p) + 16
        s.cell(x, 52, w, 24, p, "new" if k < 3 else "plain", size=12, weight=400)
        x += w + 8
    s.t(96, 96, "前 3 个先到, 把 m, o 的 top3 填满 -> mouse, mousepad 到 m, o 时已满, 被忽略", 12)
    # 截断的 trie
    P = {"": (150, 140), "m": (150, 184), "mo": (150, 228), "mob": (60, 272), "mon": (150, 272), "mou": (240, 272),
         "mone": (120, 316), "moni": (180, 316), "mous": (240, 316), "mouse": (240, 360)}
    present = set(P)
    draw_trie(s, P, present, {"mouse": "plain"})
    for pref, (x_, y_) in {"mob": P["mob"], "mone": P["mone"], "moni": P["moni"], "mouse": P["mouse"]}.items():
        s.circ(x_, y_ + 34, 11, "…", "dim")
        s.line(x_, y_ + 11, x_, y_ + 23, "#B4B2A9", 1, True)
    s.t(40, 424, "(只画到 depth 5, … = 后面还有字符)", 12, "#898781")
    # 表
    s.t(330, 140, "node (路径) 里存的 top3", 14, BLACK, 500)
    rows = [("m, o", get("mo")), ("m → o → b", get("mob")), ("m → o → n", get("mon")),
            ("m → o → u (→ s → e)", get("mouse"))]
    yy = 176
    for k, v in rows:
        s.t(330, yy, k, 12, GREY)
        s.cell(330, yy + 12, 300, 26, ", ".join(v), "new", size=12, weight=400)
        yy += 56
    s.t(330, yy + 4, "查询 O(L): 走 L 步, 每步直接读 node.top3", 14, BLACK, 500)
    s.legend(456, [("new", "先到的 3 个 / 存的 top3"), ("plain", "后到的 (被忽略)"), ("dim", "后面还有")])
    return s.save("sug_core", 476)


def fig_sug_trace():
    get = sug_tops()
    word = "mouse"
    out = NS["SUG"]["suggestedProducts"](_prods, word)
    s = Svg("Search Suggestions trace", "输入 mouse, 每敲一个字符往下走一步, 读 node.top3")
    s.t(40, 18, "searchWord = 'mouse' · 每敲 1 个字符 node 往下走 1 步 · 答案 = 走到的 node 里存的 top3", 12)
    s.t(40, 38, "走不通 (children 里没有这个字符) -> node = None, 之后每一步都是 []", 12)
    s.t(40, 64, "已敲", 12)
    s.t(110, 64, "node 沿着 root 往下走", 12)
    s.t(350, 64, "这一步的答案 = node.top3", 12)
    s.sep(76)
    y = 84
    chain = [""] + list("mouse")
    cx = [128, 190, 232, 274, 316, 358]
    for k in range(1, 6):
        pref = word[:k]
        top = get(pref)
        assert top == out[k - 1]
        s.t(40, y + 22, pref, 16, BLACK, 500)
        for idx in range(0, 6):
            x = cx[idx]
            lab = chain[idx]
            if idx > 0:
                s.arrow(cx[idx - 1] + (19 if idx == 1 else 12), y + 22, x - 13, y + 22,
                        "#898781" if idx <= k else "#B4B2A9", dash=(idx > k), w=1.2)
            role = "plain" if idx < k else ("new" if idx == k else "dim")
            if idx == 0:
                s.rect(x - 19, y + 12, 38, 20, role if k > 0 else "new", rx=10)
                s.t(x, y + 22, "root", 12, ROLE[role][2], 500, "middle")
            else:
                s.circ(x, y + 22, 11, lab, role, ring=(idx == k))
        s.t(400, y + 8, "走到 '%s': node.top3 =" % pref, 12)
        s.t(400, y + 32, ", ".join(top), 14, BLACK, 500)
        y += 52
        s.sep(y - 4)
    s.t(40, y + 12, "res = [[mobile, moneypot, monitor] × 2, [mouse, mousepad] × 3]  (5 步, 共 5 个 list)", 12)
    s.t(40, y + 34, "前两步 (m, mo) 的答案相同, 后三步 (mou, mous, mouse) 的答案相同", 12)
    s.t(40, y + 56, "若输入 'moz': 第 3 步 children 里没有 'z' -> node = None -> 这一步和之后都 append([])", 12)
    s.legend(y + 86, [("plain", "已经走过的 node"), ("new", "当前 node"), ("dim", "还没走到")])
    return s.save("sug_trace", y + 106)



# ---- Add and Search Words
ADD_WORDS = ["bad", "dad", "mad", "mid"]


def fig_add_core():
    s = Svg("Add and Search Words: '.' 通配 = DFS 分叉", "普通字符只有一条路, '.' 对所有 child 都试一次")
    s.t(40, 18, "同一棵 trie, 只有 search 不同: 普通字符沿 1 条边走, '.' 要把所有 child 都试一遍", 12)
    s.t(40, 38, "分叉 = 递归 (DFS), 只要有 1 条分支返回 True, 整体就是 True", 12)
    s.t(40, 64, "普通字符 c", 14, BLACK, 500)
    s.t(360, 64, "通配 '.'", 14, BLACK, 500)
    s.sep(76)
    s.rect(122, 96, 44, 22, "plain", rx=11)
    s.t(144, 107, "node", 12, ROLE["plain"][2], 500, "middle")
    s.arrow(144, 120, 144, 160)
    s.t(154, 140, "c", 14, BLACK, 500)
    s.circ(144, 176, 12, "c", "new")
    s.t(40, 214, "ch = node.children.get(c)", 12, BLACK, mono=True)
    s.t(40, 236, "只有 1 条路, O(1), 不分叉", 12)
    s.rect(478, 96, 44, 22, "plain", rx=11)
    s.t(500, 107, "node", 12, ROLE["plain"][2], 500, "middle")
    for cx, lab in [(420, "b"), (500, "d"), (580, "m")]:
        s.arrow(500, 120, cx, 160)
        s.circ(cx, 176, 12, lab, "new")
    s.t(536, 140, "'.'", 14, BLACK, 500)
    s.t(360, 208, "any(dfs(ch, i+1)", 12, BLACK, mono=True)
    s.t(360, 224, "    for ch in node.children.values())", 12, BLACK, mono=True)
    s.t(360, 246, "每个 child 都可能匹配, 最多 26 条路", 12)
    s.sep(262)
    s.t(40, 282, "pattern = 'b.d' 逐字符对应:", 14, BLACK, 500)
    for k, (ch, how) in enumerate([("b", "1 条路"), (".", "分叉"), ("d", "1 条路")]):
        x = 280 + k * 88
        s.cell(x, 268, 40, 28, ch, "plain", ring=(ch == "."))
        s.t(x + 20, 312, how, 12, GREY, 400, "middle")
    s.t(40, 344, "没有 '.': 和普通 Trie.search 一样 O(L)", 14, BLACK, 500)
    s.t(40, 368, "有 '.': 最坏会遍历整棵 trie, 上界 = trie 的 node 数 (≤ 所有 word 的总字符数)", 14, BLACK, 500)
    s.t(40, 392, "暴力对照: 把所有 word 放 list, 每次 search 逐个比 -> O(N · L), 跟有没有 '.' 无关", 12)
    s.legend(420, [("plain", "node"), ("new", "往下走的 child"), ("ring", "'.' 通配符")])
    return s.save("add_core", 440)


def add_trace_steps():
    """用真 trie (NS['ADD']) 的结构复核每一步的 children。"""
    w = NS["ADD"]["WordDictionary"]()
    for x in ADD_WORDS:
        w.addWord(x)
    root = w.root
    assert sorted(root.children) == ["b", "d", "m"]
    assert sorted(root.children["b"].children) == ["a"] and sorted(root.children["d"].children) == ["a"]
    assert sorted(root.children["m"].children) == ["a", "i"]
    assert root.children["m"].children["i"].children["d"].is_end
    assert w.search(".id") is True
    return True


def fig_add_trace():
    add_trace_steps()
    words = ADD_WORDS
    pos0 = trie_layout(words, 70, 0, 56, 32)
    pres = prefixes(words)
    s = Svg("Add and Search 的 DFS trace", "words = bad, dad, mad, mid; search('.id') 的 DFS 过程")
    s.t(40, 18, "trie 里有 bad, dad, mad, mid · search('.id') · dfs(node, i): node 已匹配 word[:i]", 12)
    s.t(40, 38, "绿色 = 这条路正在走 · 红色 = 死路 (return False), 回到 '.' 分叉点试下一个 child", 12)
    s.t(40, 64, "trie", 12)
    s.t(300, 64, "这一步在做什么", 12)
    s.sep(76)
    steps = [
        ({"b": "new", "d": "new", "m": "new"}, set(),
         "dfs(root, 0): word[0] = '.'", "分叉: root 的 3 个 child b, d, m 都要试"),
        ({"b": "old", "d": "plain", "m": "plain"}, set(),
         "试 b: word[1] = 'i', b.children = {a}", "没有 'i' -> return False (死路)"),
        ({"b": "old", "d": "old", "m": "plain"}, set(),
         "试 d: word[1] = 'i', d.children = {a}", "没有 'i' -> return False (死路)"),
        ({"b": "old", "d": "old", "m": "new", "mi": "new"}, set(),
         "试 m: word[1] = 'i', m.children = {a, i}", "有 'i' -> 走进去, i = 2"),
        ({"b": "old", "d": "old", "m": "new", "mi": "new", "mid": "new"}, {"mid"},
         "word[2] = 'd' 有 -> i = 3 = len(word)", "node.is_end = True -> return True"),
    ]
    y = 84
    for roles, ends, l1, l2 in steps:
        h = 3 * 32 + 44
        p2 = {k: (v[0], v[1] + y + 26) for k, v in pos0.items()}
        draw_trie(s, p2, pres, roles, ends)
        s.t(300, y + 64, l1, 12)
        s.t(300, y + 86, l2, 14, BLACK, 500)
        y += h
        s.sep(y - 4)
    s.t(40, y + 12, "答案: search('.id') = True · 'b', 'd' 两条分支白跑了, 但每条只走 1 步就死", 14, BLACK, 500)
    s.t(40, y + 36, "any(...) 是短路的: 找到第一条成功路径就停, 不会再试 m 之后的 child", 12)
    s.legend(y + 64, [("new", "正在走的路"), ("old", "死路 (False)"), ("plain", "还没试 / 没走到"),
                      ("ring", "is_end = True")])
    return s.save("add_trace", y + 84)


# ---- Word Search II
WS_WORDS = ["oath", "pea", "eat", "rain"]


def ws2_events():
    """跑真代码, 记录每次 del (摘枝) 之后 trie 还剩多少个 node, 并确认总顺序。"""
    def count(n):
        return 1 + sum(count(c) for c in n.children.values())
    code = CODE_WS2.replace("del parent.children[ch]", "del parent.children[ch]; events.append((ch, count(root) - 1))")
    ns = {"events": [], "count": count}
    exec(code, ns)
    res = ns["findWords"]([r[:] for r in _BOARD], WS_WORDS)
    assert res == ["oath", "eat"]
    return ns["events"]


def draw_board(s, x, y, board, marks, cell=20):
    for r, row in enumerate(board):
        for c, ch in enumerate(row):
            role, ring = marks.get((r, c), ("plain", False))
            s.cell(x + c * (cell + 2), y + r * (cell + 2), cell, cell, ch, role, size=12, ring=ring, weight=500)


def fig_ws2_core():
    ev = ws2_events()
    assert ev == [("h", 13), ("t", 12), ("a", 11), ("o", 10), ("t", 9), ("a", 8), ("e", 7)], ev
    s = Svg("Word Search II: board 和 trie 同步往下走", "DFS 同时在 board 和 trie 上走, trie 里没有的字符立刻剪枝")
    s.t(40, 18, "words = [oath, pea, eat, rain] 建成 1 棵 trie · 对 board 只跑 1 次 DFS", 12)
    s.t(40, 38, "DFS 每走一格, trie 也往下走一层: 这一格的字符不在 node.children 里 -> 这条路不可能是任何 word -> 剪枝", 12)
    s.t(40, 64, "board (从 (0,0) 出发)", 14, BLACK, 500)
    s.t(300, 64, "trie (4 个 word, 14 个 node)", 14, BLACK, 500)
    s.sep(76)
    marks = {(0, 0): ("new", False), (0, 1): ("new", False), (1, 1): ("new", False), (2, 1): ("new", True)}
    draw_board(s, 40, 92, _BOARD, marks, cell=30)
    s.t(40, 232, "oath: (0,0) -> (0,1) -> (1,1) -> (2,1)", 12)
    pos = trie_layout(WS_WORDS, 330, 100, 64, 30)
    pres = prefixes(WS_WORDS)
    roles = {"o": "new", "oa": "new", "oat": "new", "oath": "new"}
    draw_trie(s, pos, pres, roles, ends={"oath"})
    s.t(540, 120, "o -> a -> t -> h", 12, "#085041", 500)
    s.t(540, 140, "board 每一格都对应", 12)
    s.t(540, 158, "trie 的下一层", 12)
    s.sep(256)
    s.t(40, 278, "剪枝 1: board[nr][nc] not in node.children -> 不进 dfs", 14, BLACK, 500)
    s.t(40, 302, "例: (0,1) 'a' 起头, root.children = {o, p, e, r}, 没有 'a' -> 整棵 DFS 子树直接不要", 12)
    s.t(40, 330, "剪枝 2: 找到 word 后 node.word = None, 叶子变空就 del -> 同一个 word 不会重复搜", 14, BLACK, 500)
    s.t(40, 354, "oath 摘掉后 trie 14 -> 10 个 node, eat 摘掉后 10 -> 7 个 node", 12)
    s.t(40, 382, "暴力 (每个 word 跑一遍 Word Search I): 4 次完整搜索, 'o' 'e' 等共享前缀被重复走", 12)
    s.t(40, 402, "trie 版: 1 次搜索, 所有 word 共享前缀一起走", 12)
    s.legend(430, [("new", "DFS 当前路径 (board / trie)"), ("plain", "其他格子 / node"), ("ring", "node.word = 'oath'")])
    return s.save("ws2_core", 450)


def fig_ws2_trace():
    ev = ws2_events()
    assert [e[1] for e in ev] == [13, 12, 11, 10, 9, 8, 7]
    s = Svg("Word Search II trace", "board 上的 DFS 路径, 同步的 trie 状态, 以及被摘掉的分支")
    s.t(40, 18, "board 4×4 · words = [oath, pea, eat, rain] · 每一步: board 上的路径 + 此刻的 trie", 12)
    s.t(40, 38, "被摘掉的 node 虚线扔到左边 (node 数在右边写出来) · res 在右边累积", 12)
    s.t(40, 64, "board", 12)
    s.t(160, 64, "摘掉的", 12)
    s.t(300, 64, "trie (此刻)", 12)
    s.t(530, 64, "res / node 数", 12)
    s.sep(76)
    pos0 = trie_layout(WS_WORDS, 320, 0, 52, 24)
    full = prefixes(WS_WORDS)
    no_oath = {p for p in full if not p.startswith("o") or p == ""}
    no_eat = {p for p in no_oath if not (p.startswith("e"))}
    assert len(full) - 1 == 14 and len(no_oath) - 1 == 10 and len(no_eat) - 1 == 7
    pathO = {"o", "oa", "oat", "oath"}
    pathE = {"e", "ea", "eat"}
    G, P = ("new", False), ("plain", False)
    steps = [
        ("① 从 (0,0) 'o' 开始: o -> a -> t -> h, 每格的字符都在 trie 的下一层", None,
         {(0, 0): G, (0, 1): G, (1, 1): G, (2, 1): ("new", True)}, full, {p: "new" for p in pathO}, {"oath"},
         "res = [oath]", "word = oath, 记下后清空", None),
        ("② 回溯: h 没有 child 且 word 已清空 -> 摘掉 h; t, a, o 也空了, 依次摘掉", "oath",
         {}, no_oath, {}, set(), "res = [oath]", "node 数 14 -> 10", None),
        ("③ (0,1) 'a': root.children = {p, e, r}, 没有 'a' -> 剪枝, 不进 dfs", None,
         {(0, 1): ("old", False)}, no_oath, {}, set(), "res = [oath]", "node 数 = 10", None),
        ("④ (1,0) 'e' 在 root 里: 邻居 o, t, i 都不是 e.children 里的 'a' -> 死路", None,
         {(1, 0): G, (0, 0): ("old", False), (1, 1): ("old", False), (2, 0): ("old", False)}, no_oath,
         {"e": "new"}, set(), "res = [oath]", "node 数 = 10", None),
        ("⑤ (1,3) 'e' -> (1,2) 'a' -> (1,1) 't': 走到 eat 的末尾, 找到", None,
         {(1, 3): G, (1, 2): G, (1, 1): ("new", True)}, no_oath, {p: "new" for p in pathE}, {"eat"},
         "res = [oath, eat]", "word = eat, 记下后清空", None),
        ("⑥ 回溯: t, a, e 依次变空 -> 整条 eat 分支摘掉; 剩下 pea, rain 没有对应路径", "eat",
         {}, no_eat, {}, set(), "res = [oath, eat]", "node 数 10 -> 7", None),
    ]
    y = 84
    for title, removed, marks, present, roles, ends, r1, r2, _ in steps:
        s.t(40, y + 10, title, 12, BLACK)
        yy = y + 24
        draw_board(s, 40, yy, _BOARD, marks, cell=22)
        p2 = {k: (v[0], v[1] + yy + 12) for k, v in pos0.items()}
        # trie 里被摘掉的分支: 只画还在的 node
        draw_trie(s, p2, present, roles, ends, r=10)
        if removed:
            for k, ch in enumerate(removed):
                s.circ(190, yy + 8 + k * 24, 10, ch, "old")
                if k:
                    s.line(190, yy + 8 + (k - 1) * 24 + 10, 190, yy + 8 + k * 24 - 10, "#D85A30", 1, True)
            s.arrow(262, yy + 56, 214, yy + 56, RED_ARROW, dash=True)
        s.t(530, yy + 24, r1, 12, BLACK)
        s.t(530, yy + 46, r2, 12, GREY)
        y += 24 + 4 * 24 + 40
        s.sep(y - 6)
    s.t(40, y + 10, "答案: ['oath', 'eat'] · pea, rain 在 board 上没有对应路径, 留在 trie 里", 14, BLACK, 500)
    s.legend(y + 40, [("new", "当前 DFS 路径"), ("old", "剪掉 / 摘掉 / 死路"), ("plain", "其他"), ("ring", "word 的末尾")])
    return s.save("ws2_trace", y + 60)


ALL_FIGS = [fig_s0_core, fig_lcp_core, fig_lcp_trace, fig_atoi_core, fig_atoi_trace, fig_rev_core, fig_rev_trace,
            fig_trie_core, fig_trie_trace, fig_sug_core, fig_sug_trace, fig_add_core, fig_add_trace,
            fig_ws2_core, fig_ws2_trace]

if __name__ == "__main__" and "--figs-only" in sys.argv:
    for f in ALL_FIGS:
        print(f())
