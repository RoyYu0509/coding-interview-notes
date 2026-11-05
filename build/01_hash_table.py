"""01 · Hash Table / Counting  ——  生成 docs/01-hash-table.html 和 docs/svg/01-hash-table/*.svg
运行: cd build && python3 -I 01_hash_table.py
trace 图里的每个数字都来自下面 simulate_* 函数的真实运行, 并且和题解函数的返回值做 assert。
"""
import html
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import doclib as d  # noqa: E402

SLUG = "01-hash-table"
SVG_DIR = os.path.join(d.ROOT, "docs", "svg", SLUG)
os.makedirs(SVG_DIR, exist_ok=True)

# ============================================================
# 1. 文档里展示的代码 (字符串) —— 同时 exec 出来跑测试
# ============================================================
CODE = {}

CODE["template"] = '''
# 模板 A: complement lookup —— 边走边查 "我要的另一半见过没"
seen = {}                          # seen: 已经走过的东西 (key -> 需要的信息, 比如下标)
for i, x in enumerate(nums):
    need = f(x)                    # 由当前 x 算出 "另一半" 长什么样
    if need in seen:               # O(1) 查表, 取代 O(n) 的内层扫描
        ...                        # 命中: 用 seen[need] 和 i 算答案
    seen[x] = i                    # 查完再存: 保证 seen 里只有 i 之前的元素

# 模板 B: 频率表 —— 数一遍, 之后随便问 "x 出现几次"
cnt = Counter(s)                   # 或 [0] * 26 (key 只有小写字母时)

# 模板 C: canonical key 分组 —— 同一组的东西算出同一个 key
groups = defaultdict(list)
for w in words:
    groups[key(w)].append(w)       # key(w) 必须 hashable: str / tuple, 不能是 list

# 模板 D: set 换掉排序 —— 只问 "在不在", 不关心顺序
s = set(nums)
if x - 1 in s: ...                 # O(1)
'''

CODE["two_sum"] = '''
def two_sum(nums, target):
    seen = {}                       # seen: 值 -> 下标, 只装 nums[0..i-1]
    for i, x in enumerate(nums):
        need = target - x           # 我需要的另一半
        if need in seen:            # 另一半之前见过 -> 答案
            return [seen[need], i]
        seen[x] = i                 # 先查后存: 否则 x 会把自己当成另一半
    return []
'''

CODE["cd2"] = '''
def contains_nearby_duplicate(nums, k):
    last = {}                       # last: 值 -> 它最近一次出现的下标
    for i, x in enumerate(nums):
        if x in last and i - last[x] <= k:   # 最近的一次都不够近, 更老的更不行
            return True
        last[x] = i                 # 不管有没有命中, 都覆盖成最新下标
    return False
'''

CODE["anagram"] = '''
def is_anagram(s, t):
    if len(s) != len(t):            # 长度不同, 一定不是
        return False
    cnt = [0] * 26                  # 小写字母: 下标 = ord(ch) - 97, 不需要 hash
    for ch in s:
        cnt[ord(ch) - 97] += 1      # s 里的字符 +1
    for ch in t:
        cnt[ord(ch) - 97] -= 1      # t 里的字符 -1: 同样多就刚好抵消
    return not any(cnt)             # 全部抵消成 0 <=> 频率表相同

# 字符集不固定 (Unicode / 任意 hashable): 换成 Counter
# return Counter(s) == Counter(t)
'''

CODE["first_uniq"] = '''
def first_uniq_char(s):
    cnt = Counter(s)                # pass 1: 全局频率 (等价于逐字符 cnt[ch] += 1)
    for i, ch in enumerate(s):      # pass 2: 必须按原顺序扫, 才能拿到 "第一个"
        if cnt[ch] == 1:
            return i
    return -1
'''

CODE["group"] = '''
def group_anagrams(strs):
    groups = defaultdict(list)      # key -> 这一组的所有词
    for w in strs:
        key = "".join(sorted(w))    # canonical key: anagram 排序后一定相同
        groups[key].append(w)
    return list(groups.values())

# key 的另一种写法, O(k) 而不是 O(k log k):
#   cnt = [0] * 26
#   for ch in w: cnt[ord(ch) - 97] += 1
#   key = tuple(cnt)               # list 不能当 key, 转成 tuple
'''

CODE["lcs"] = '''
def longest_consecutive(nums):
    s = set(nums)                   # O(1) membership, 取代排序
    best = 0
    for x in s:                     # 遍历 set 去重, 重复的数不会重复起步
        if x - 1 in s:              # x 前面还有数 -> x 不是序列起点, 交给起点去数
            continue
        y = x                       # x 是起点: 一路往右数
        while y + 1 in s:
            y += 1
        best = max(best, y - x + 1)
    return best
'''

CODE["defaultdict_pitfall"] = '''
from collections import defaultdict
d = defaultdict(int)
if d["a"] == 0:                     # 只是 "读" 了一下...
    pass
len(d)                              # 1: 读取也把 "a" 插进去了!
# 只想查、不想插: 用 "a" in d 或 d.get("a")
'''

ns = {"Counter": Counter, "defaultdict": defaultdict}
for _k in ("two_sum", "cd2", "anagram", "first_uniq", "group", "lcs"):
    exec(CODE[_k], ns)

# ============================================================
# 2. 正确性测试 (对拍暴力解)
# ============================================================
def _selftest():
    import random
    random.seed(1)
    two_sum, cd2 = ns["two_sum"], ns["contains_nearby_duplicate"]
    ana, fu = ns["is_anagram"], ns["first_uniq_char"]
    ga, lc = ns["group_anagrams"], ns["longest_consecutive"]
    for _ in range(3000):
        n = random.randint(0, 8)
        nums = [random.randint(-4, 6) for _ in range(n)]
        t = random.randint(-6, 10)
        r = two_sum(nums, t)
        ok = any(nums[i] + nums[j] == t for i in range(n) for j in range(i + 1, n))
        assert (r != []) == ok
        if r:
            assert r[0] != r[1] and nums[r[0]] + nums[r[1]] == t
        k = random.randint(0, 5)
        br = any(nums[i] == nums[j] and j - i <= k for i in range(n) for j in range(i + 1, n))
        assert cd2(nums, k) == br
        assert lc(nums) == _lcs_brute(nums)
        a = "".join(random.choice("abc") for _ in range(random.randint(0, 6)))
        b = "".join(random.choice("abc") for _ in range(random.randint(0, 6)))
        assert ana(a, b) == (sorted(a) == sorted(b))
        exp = next((i for i, ch in enumerate(a) if a.count(ch) == 1), -1)
        assert fu(a) == exp
        words = ["".join(random.choice("abc") for _ in range(random.randint(0, 3))) for _ in range(6)]
        got = sorted(sorted(g) for g in ga(words))
        exp = {}
        for w in words:
            exp.setdefault("".join(sorted(w)), []).append(w)
        assert got == sorted(sorted(g) for g in exp.values())
    assert two_sum([3, 3], 6) == [0, 1] and two_sum([3], 6) == []
    assert lc([100, 4, 200, 1, 3, 2]) == 4
    assert cd2([1, 2, 3, 1, 3], 2) is True
    # 模板与 pitfall 代码也要能跑
    exec(CODE["defaultdict_pitfall"], {})


def _lcs_brute(nums):
    best, S = 0, set(nums)
    for x in S:
        y = x
        while y + 1 in S:
            y += 1
        best = max(best, y - x + 1)
    return best


_selftest()

# ============================================================
# 3. trace 模拟 (图里的数字全部来自这里)
# ============================================================
def sim_two_sum(nums, target):
    seen, rows = {}, []
    for i, x in enumerate(nums):
        need = target - x
        hit = need in seen
        row = dict(i=i, x=x, need=need, hit=hit, hit_idx=seen.get(need))
        if not hit:
            seen[x] = i
        row["seen"] = list(seen.items())
        rows.append(row)
        if hit:
            break
    return rows


def sim_cd2(nums, k):
    last, rows = {}, []
    for i, x in enumerate(nums):
        old = last.get(x)
        dist = None if old is None else i - old
        hit = old is not None and dist <= k
        row = dict(i=i, x=x, old=old, dist=dist, hit=hit)
        if not hit:
            last[x] = i
        row["last"] = list(last.items())
        rows.append(row)
        if hit:
            break
    return rows


def sim_anagram(s, t):
    cnt, rows, order = {}, [], []
    for ph, w, delta in (("s", s, 1), ("t", t, -1)):
        for j, ch in enumerate(w):
            if ch not in order:
                order.append(ch)
            cnt[ch] = cnt.get(ch, 0) + delta
            rows.append(dict(ph=ph, j=j, ch=ch, delta=delta, val=cnt[ch],
                             cnt=[(c, cnt.get(c, 0)) for c in order]))
    return rows, [(c, cnt[c]) for c in order]


def sim_first_uniq(s):
    cnt, rows = {}, []
    for ch in s:
        cnt[ch] = cnt.get(ch, 0) + 1
        rows.append(dict(ph=1, ch=ch, val=cnt[ch], cnt=list(cnt.items())))
    full = list(cnt.items())
    for i, ch in enumerate(s):
        hit = cnt[ch] == 1
        rows.append(dict(ph=2, i=i, ch=ch, val=cnt[ch], hit=hit, cnt=full))
        if hit:
            break
    return rows


def sim_group(words):
    groups, rows = {}, []
    for w in words:
        key = "".join(sorted(w))
        new_key = key not in groups
        groups.setdefault(key, []).append(w)
        rows.append(dict(w=w, key=key, new_key=new_key,
                         groups=[(k, list(v)) for k, v in groups.items()]))
    return rows


def sim_lcs(nums):
    s = set(nums)
    rows, best = [], 0
    for x in s:
        if x - 1 in s:
            rows.append(dict(x=x, start=False, walk=[], best=best))
            continue
        y = x
        walk = [x]
        while y + 1 in s:
            y += 1
            walk.append(y)
        best = max(best, len(walk))
        rows.append(dict(x=x, start=True, walk=walk, best=best))
    return list(s), rows


TS_NUMS, TS_T = [3, 8, 5, 2, 7], 9
CD_NUMS, CD_K = [1, 2, 3, 1, 3], 2
AN_S, AN_T = "rat", "car"
FU_S = "aabc"
GA_WORDS = ["eat", "tea", "tan", "ate", "nat", "bat"]
LC_NUMS = [100, 4, 200, 1, 3, 2]

ts_rows = sim_two_sum(TS_NUMS, TS_T)
assert ts_rows[-1]["hit"] and [ts_rows[-1]["hit_idx"], ts_rows[-1]["i"]] == ns["two_sum"](TS_NUMS, TS_T) == [3, 4]
cd_rows = sim_cd2(CD_NUMS, CD_K)
assert cd_rows[-1]["hit"] and ns["contains_nearby_duplicate"](CD_NUMS, CD_K) is True
an_rows, an_final = sim_anagram(AN_S, AN_T)
assert ns["is_anagram"](AN_S, AN_T) is False and any(v for _, v in an_final)
fu_rows = sim_first_uniq(FU_S)
assert fu_rows[-1]["hit"] and fu_rows[-1]["i"] == ns["first_uniq_char"](FU_S) == 2
ga_rows = sim_group(GA_WORDS)
assert sorted(sorted(v) for _, v in ga_rows[-1]["groups"]) == sorted(sorted(g) for g in ns["group_anagrams"](GA_WORDS))
lc_order, lc_rows = sim_lcs(LC_NUMS)
assert max(r["best"] for r in lc_rows) == ns["longest_consecutive"](LC_NUMS) == 4

print("== trace states (图里的数字就是这些) ==")
for r in ts_rows:
    print("two_sum", r)
for r in cd_rows:
    print("cd2", r)
for r in an_rows:
    print("anagram", r)
print("anagram final", an_final)
for r in fu_rows:
    print("first_uniq", r)
for r in ga_rows:
    print("group", r)
print("lcs set order", lc_order)
for r in lc_rows:
    print("lcs", r)

# ============================================================
# 4. 极简 SVG 工具 (配色/字号/版式 = STYLE_GUIDE B)
# ============================================================
FONT = 'ui-sans-serif, system-ui, -apple-system, "PingFang SC", sans-serif'
ROLE = {
    "new": ("#E1F5EE", "#0F6E56", "#085041"),
    "gone": ("#FAECE7", "#993C1D", "#712B13"),
    "base": ("#F1EFE8", "#5F5E5A", "#444441"),
}
INK, SUB, LINE, RING = "#0B0B0B", "#52514E", "#B4B2A9", "#EF9F27"


def tw(t, size):
    """文字宽度估算 (CJK 记满宽, 其余约 0.58)"""
    w = 0.0
    for ch in t:
        w += size if ord(ch) > 0x2E80 else size * 0.58
    return w


def esc(t):
    return html.escape(str(t), quote=False)


class Svg:
    def __init__(self, h, title, desc):
        self.h, self.title, self.desc = h, title, desc
        self.e = []

    def add(self, s):
        self.e.append(s)

    def text(self, x, y, t, size=12, fill=SUB, anchor="start", weight=400):
        self.add('<text x="%s" y="%s" font-size="%d" fill="%s" text-anchor="%s" '
                 'dominant-baseline="central" font-weight="%d">%s</text>'
                 % (x, y, size, fill, anchor, weight, esc(t)))

    def rect(self, x, y, w, h, role="base", dash=False, rx=4):
        f, s, _ = ROLE[role]
        self.add('<rect x="%s" y="%s" width="%s" height="%s" rx="%d" fill="%s" stroke="%s" '
                 'stroke-width="1"%s/>' % (x, y, w, h, rx, f, s,
                                           ' stroke-dasharray="4 3"' if dash else ""))

    def box(self, x, y, w, h, role, lines, dash=False):
        """lines: [(text, size, weight)], 垂直居中"""
        self.rect(x, y, w, h, role, dash)
        tc = ROLE[role][2]
        gap = 16
        top = y + h / 2 - gap * (len(lines) - 1) / 2
        for k, (t, sz, wt) in enumerate(lines):
            self.text(x + w / 2, top + k * gap, t, sz, tc, "middle", wt)

    def chip(self, x, y, label, role="base", h=28, w=None, dash=False):
        w = w or max(44, round(tw(label, 14) + 16))
        self.box(x, y, w, h, role, [(label, 14, 500)], dash)
        return w

    def chips(self, x, y, items, gap=4, limit=640):
        for label, role in items:
            w = self.chip(x, y, label, role)
            x += w + gap
        assert x - gap <= limit, ("chips overflow", x, items)
        return x

    def ring(self, x, y, w, h):
        self.add('<rect x="%s" y="%s" width="%s" height="%s" rx="6" fill="none" stroke="%s" '
                 'stroke-width="2.5"/>' % (x - 3, y - 3, w + 6, h + 6, RING))

    def path(self, d, color="grey", dash=False, marker=True):
        col = {"grey": "#5F5E5A", "red": "#D85A30", "green": "#0F6E56"}[color]
        self.add('<path d="%s" fill="none" stroke="%s" stroke-width="1.5"%s%s/>'
                 % (d, col, ' stroke-dasharray="5 4"' if dash else "",
                    ' marker-end="url(#a_%s)"' % color if marker else ""))

    def hr(self, y, x1=40, x2=640):
        self.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1" '
                 'stroke-dasharray="4 4"/>' % (x1, y, x2, y, LINE))

    def vline(self, x, y1, y2):
        self.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1" '
                 'stroke-dasharray="4 4"/>' % (x, y1, x, y2, LINE))

    def legend(self, y, items):
        x = 40
        for role, label, extra in items:
            if role == "ring":
                self.add('<rect x="%d" y="%d" width="16" height="12" rx="3" fill="none" '
                         'stroke="%s" stroke-width="2.5"/>' % (x, y - 6, RING))
            else:
                self.rect(x, y - 6, 16, 12, role, dash=(extra == "dash"), rx=3)
            self.text(x + 22, y, label, 12, SUB)
            x += 22 + tw(label, 12) + 24
        assert x - 24 <= 640, ("legend overflow", x)

    def render(self):
        defs = "".join(
            '<marker id="a_%s" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" '
            'orient="auto"><path d="M2 1L8 5L2 9" fill="none" stroke="%s" stroke-width="1.5" '
            'stroke-linecap="round" stroke-linejoin="round"/></marker>' % (n, c)
            for n, c in (("grey", "#5F5E5A"), ("red", "#D85A30"), ("green", "#0F6E56")))
        return ('<svg width="100%%" viewBox="0 0 680 %d" role="img" xmlns="http://www.w3.org/2000/svg" '
                'style="font-family:%s">\n<title>%s</title><desc>%s</desc>\n<defs>%s</defs>\n%s\n</svg>\n'
                % (self.h, html.escape(FONT, quote=True), esc(self.title), esc(self.desc), defs,
                   "\n".join(self.e)))

    def save(self, name):
        path = os.path.join(SVG_DIR, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.render())


def trace_header(s, line1, line2, cols):
    s.text(40, 18, line1, 12, SUB)
    s.text(40, 38, line2, 12, SUB)
    for x, label in cols:
        s.text(x, 64, label, 12, SUB)
    s.hr(74)


STD_LEGEND = [("new", "新写入 / 计数 +1", None), ("gone", "被覆盖 / 计数 −1", "dash"),
              ("base", "结构里已有的", None), ("ring", "关键 / 命中", None)]

# ============================================================
# 5. SVG: 第 0 节 core
# ============================================================
def svg_principle():
    s = Svg(372, "brute force 内层扫描 vs 一次查表",
            "同一个 Two Sum 例子: 左边每个 x 重新扫描前面所有元素, 右边把前面见过的存进 seen, 一次 lookup 找到另一半。")
    s.text(40, 18, "nums = [3, 8, 5, 2, 7] · target = 9 · 现在轮到 i = 4, x = 7, 要找另一半 need = 9 − 7 = 2", 12, SUB)
    s.text(40, 52, "brute force: 内层循环扫描", 14, INK, weight=500)
    s.text(360, 52, "Hash Table: 内层循环变成一次查表", 14, INK, weight=500)
    s.vline(340, 40, 300)
    for base in (50, 370):
        for j, v in enumerate(TS_NUMS):
            role = "new" if j == 4 else "base"
            s.box(base + j * 44, 78, 40, 32, role, [(str(v), 14, 500)])
            s.text(base + j * 44 + 20, 124, str(j), 12, SUB, "middle")
        s.ring(base + 4 * 44, 78, 40, 32)
    # 左: 逐个比较
    s.text(50, 152, "x = 7 要和前面每个数比一次:", 12, SUB)
    for k, (v, mark) in enumerate([(3, "= 10 ≠ 9"), (8, "= 15 ≠ 9"), (5, "= 12 ≠ 9"), (2, "= 9 ✓")]):
        y = 176 + k * 24
        ok = mark.endswith("✓")
        s.box(50, y - 10, 150, 20, "new" if ok else "gone", [("7 + %d %s" % (v, mark), 12, 400)])
    s.text(50, 282, "每个 x 最多比 n − 1 次", 14, INK, weight=500)
    s.text(50, 304, "n × n = O(n²) · 额外空间 O(1)", 14, INK, weight=500)
    # 右: seen
    s.text(370, 152, "seen (值 → 下标), 只装 i 前面的:", 12, SUB)
    xs = 370
    pos = {}
    for v, i in [(3, 0), (8, 1), (5, 2), (2, 3)]:
        w = s.chip(xs, 166, "%d→%d" % (v, i), "base")
        pos[v] = (xs, w)
        xs += w + 4
    s.ring(pos[2][0], 166, pos[2][1], 28)
    s.text(370, 218, "need = 9 − 7 = 2", 14, INK, weight=500)
    s.text(370, 240, "2 in seen?  是 → seen[2] = 3", 14, INK, weight=500)
    s.text(370, 262, "只做 1 次 lookup", 12, SUB)
    s.text(370, 282, "每个 x 查 1 次", 14, INK, weight=500)
    s.text(370, 304, "n × 1 = O(n) · 额外空间 O(n)", 14, INK, weight=500)
    s.hr(322)
    s.text(40, 346, "本质: 用 O(n) 空间记住 \"见过什么\", 把内层 \"找\" 的循环换成一次 O(1) 的查表", 14, INK, weight=500)
    s.save("principle_core.svg")


# ============================================================
# 6. SVG: Two Sum
# ============================================================
def svg_two_sum_core():
    s = Svg(392, "Two Sum: seen 的 invariant 和先查后存",
            "进入第 i 轮时 seen 恰好装着 nums[0..i-1]; 先查再存才不会让 x 匹配自己。")
    s.text(40, 18, "nums = [3, 8, 5, 2, 7] · target = 9 · 此刻 i = 4", 12, SUB)
    s.text(40, 38, "invariant: 进入第 i 轮时, seen 恰好装着 nums[0..i−1]", 12, SUB)
    for j, v in enumerate(TS_NUMS):
        role = "new" if j == 4 else "base"
        s.box(50 + j * 62, 62, 56, 36, role, [(str(v), 14, 500)])
        s.text(50 + j * 62 + 28, 112, "i=%d" % j, 12, SUB, "middle")
    s.ring(50 + 4 * 62, 62, 56, 36)
    s.add('<path d="M50 126 L50 132 L286 132 L286 126" fill="none" stroke="#5F5E5A" stroke-width="1"/>')
    s.text(168, 148, "i 前面的 4 个数: 都已经在 seen 里", 12, SUB, "middle")
    s.box(400, 56, 220, 48, "new", [("x = 7", 14, 500), ("need = 9 − 7 = 2", 14, 500)])
    s.path("M362 80 L398 80", "green")
    xs, pos = 50, {}
    for v, i in [(3, 0), (8, 1), (5, 2), (2, 3)]:
        w = s.chip(xs, 184, "%d→%d" % (v, i), "base")
        pos[v] = (xs, w)
        xs += w + 4
    s.ring(pos[2][0], 184, pos[2][1], 28)
    cx = pos[2][0] + pos[2][1] / 2
    s.path("M510 106 L510 166 L%s 166 L%s 180" % (cx, cx), "green")
    s.text(310, 198, "seen[2] = 3  →  答案 [3, 4]", 14, INK, weight=500)
    s.text(540, 150, "查 2", 12, SUB, "middle")
    s.hr(244)
    s.text(40, 266, "为什么要先查后存? nums = [3], target = 6", 14, INK, weight=500)
    s.box(40, 282, 280, 56, "gone", [("先存后查", 14, 500), ("seen = {3→0} → need = 3 → 命中 → [0, 0]", 12, 400)])
    s.box(340, 282, 300, 56, "new", [("先查后存", 14, 500), ("seen = {} → need = 3 不在 → 再存 3→0 → 无解", 12, 400)])
    s.text(40, 358, "先存后查会把 x 自己当成另一半, 同一个元素用了两次。", 12, SUB)
    s.text(40, 378, "先查后存: 命中的永远是 i 之前的元素, 所以 nums = [3, 3] 也能得到 [0, 1]。", 12, SUB)
    s.save("two_sum_core.svg")


def svg_two_sum_trace():
    rows = ts_rows
    H = 84 + len(rows) * 64 + 96
    s = Svg(H, "Two Sum 运行流程", "每步: 算 need, 查 seen, 没找到就把 x 存进 seen, 直到命中。")
    trace_header(s, "target = 9 · 每一步: need = target − x → 查 seen → 没命中才把 x→i 存进去",
                 "seen: 值 → 下标 (只装当前 i 前面的元素)",
                 [(40, "当前"), (136, "先查"), (380, "后存: seen 现在有")])
    for r_i, r in enumerate(rows):
        y = 84 + r_i * 64
        s.box(40, y, 76, 48, "new", [("i = %d" % r["i"], 12, 400), ("x = %d" % r["x"], 14, 500)])
        s.path("M116 %d L134 %d" % (y + 24, y + 24), "grey")
        s.text(142, y + 12, "need = %d − %d = %d" % (TS_T, r["x"], r["need"]), 14, INK, weight=500)
        if r["hit"]:
            s.text(142, y + 34, "%d in seen? 是 → seen[%d] = %d" % (r["need"], r["need"], r["hit_idx"]),
                   12, "#085041", weight=500)
        else:
            s.text(142, y + 34, "%d in seen? 否 → 存 %d→%d" % (r["need"], r["x"], r["i"]), 12, SUB)
        xs = 380
        for v, i in r["seen"]:
            newly = (not r["hit"]) and v == r["x"] and i == r["i"]
            w = s.chip(xs, y + 10, "%d→%d" % (v, i), "new" if newly else "base")
            if r["hit"] and v == r["need"]:
                s.ring(xs, y + 10, w, 28)
            xs += w + 4
        assert xs - 4 <= 640
        if r_i < len(rows) - 1:
            s.hr(y + 56)
    yb = 84 + len(rows) * 64 + 8
    last = rows[-1]
    s.text(40, yb + 10, "答案: return [%d, %d]    因为 nums[%d] + nums[%d] = %d + %d = %d"
           % (last["hit_idx"], last["i"], last["hit_idx"], last["i"], TS_NUMS[last["hit_idx"]], last["x"], TS_T),
           14, INK, weight=500)
    s.text(40, yb + 34, "整个过程 seen 只增不减; 最后一步命中就返回, 所以没有再存 7。", 12, SUB)
    s.legend(yb + 64, [("new", "新写入 seen", None), ("base", "seen 里已有的", None), ("ring", "命中的另一半", None)])
    s.save("two_sum_trace.svg")


# ============================================================
# 7. SVG: Contains Duplicate II
# ============================================================
def svg_cd2_core():
    s = Svg(352, "Contains Duplicate II: 只记最近一次",
            "同一个值只需要比最近一次出现的下标; 老下标只会更远, 所以覆盖即可。")
    s.text(40, 18, "nums = [1, 2, 3, 1, 3] · k = 2 · 要找: 两个相同的值, 下标之差 ≤ k", 12, SUB)
    base_x = 70
    cw = 80
    vals = CD_NUMS
    for j, v in enumerate(vals):
        role = "new" if v == 3 else "base"
        s.box(base_x + j * cw, 110, 60, 36, role, [(str(v), 14, 500)])
        s.text(base_x + j * cw + 30, 160, "i=%d" % j, 12, SUB, "middle")
    cx = lambda j: base_x + j * cw + 30
    # 上方: 两个 1 (距离 3 > k)
    s.path("M%d 108 C%d 62 %d 62 %d 108" % (cx(0), cx(0), cx(3), cx(3)), "red", dash=True)
    s.text((cx(0) + cx(3)) / 2, 62, "1 和 1: dist = 3 − 0 = 3 > k = 2, 不算", 12, "#712B13", "middle")
    # 下方: 两个 3 (距离 2 <= k)
    s.path("M%d 174 C%d 212 %d 212 %d 174" % (cx(2), cx(2), cx(4), cx(4)), "green")
    s.text((cx(2) + cx(4)) / 2, 216, "3 和 3: dist = 4 − 2 = 2 ≤ k = 2 ✓", 12, "#085041", "middle", 500)
    s.hr(226)
    s.text(40, 248, "为什么 last 只存最近一次?", 14, INK, weight=500)
    s.text(40, 270, "i = 3 再次看到 1: 旧的 1→0 已经没用 (3 − 0 > k), 以后只会更远; 覆盖成 1→3。", 12, SUB)
    s.chip(40, 290, "1→0", "gone", dash=True)
    s.path("M92 304 L146 304", "red", dash=True)
    s.chip(150, 290, "1→3", "new")
    s.text(210, 304, "last[1] 覆盖: 后面的 1 只需要和最近的 1 比", 12, SUB)
    s.text(40, 336, "对比 Two Sum: 那里每个值存第一次下标 (任一个都行); 这里存最近一次 (距离最短)。", 12, SUB)
    s.save("cd2_core.svg")


def svg_cd2_trace():
    rows = cd_rows
    rh = 72
    H = 84 + len(rows) * rh + 100
    s = Svg(H, "Contains Duplicate II 运行流程", "last 记录每个值最近一次的下标; 命中条件是 i − last[x] ≤ k; 旧值被覆盖。")
    trace_header(s, "k = 2 · 每一步: 查 last[x] → 算 dist = i − last[x] → ≤ k 就返回 True, 否则覆盖成 i",
                 "last: 值 → 最近一次出现的下标",
                 [(40, "当前"), (136, "先查"), (444, "后存: last 现在有")])
    for r_i, r in enumerate(rows):
        y = 84 + r_i * rh
        s.box(40, y + 4, 76, 48, "new", [("i = %d" % r["i"], 12, 400), ("x = %d" % r["x"], 14, 500)])
        s.path("M116 %d L134 %d" % (y + 28, y + 28), "grey")
        if r["old"] is None:
            s.text(142, y + 16, "last 里没有 %d" % r["x"], 14, INK, weight=500)
            s.text(142, y + 38, "→ 存 %d→%d" % (r["x"], r["i"]), 12, SUB)
        else:
            s.text(142, y + 12, "last[%d] = %d" % (r["x"], r["old"]), 12, SUB)
            s.text(142, y + 30, "dist = %d − %d = %d %s k = %d" % (r["i"], r["old"], r["dist"],
                                                                "≤" if r["hit"] else ">", CD_K), 14, INK, weight=500)
            if r["hit"]:
                s.text(142, y + 50, "命中 → return True", 12, "#085041", weight=500)
            else:
                s.text(142, y + 50, "太远, 不算 → 覆盖 last[%d] = %d" % (r["x"], r["i"]), 12, SUB)
        xs = 444
        for v, i in r["last"]:
            newly = (not r["hit"]) and v == r["x"] and i == r["i"]
            w = s.chip(xs, y + 14, "%d→%d" % (v, i), "new" if newly else "base")
            if r["hit"] and v == r["x"]:
                s.ring(xs, y + 14, w, 28)
            if newly and r["old"] is not None:
                # 旧值被覆盖: 虚线扔到左边
                s.chip(352, y + 14, "%d→%d" % (v, r["old"]), "gone", dash=True)
                s.path("M%s %d L%s %d" % (xs, y + 28, 352 + 50, y + 28), "red", dash=True)
                s.text(352, y + 52, "旧值被覆盖", 12, "#712B13")
            xs += w + 4
        assert xs - 4 <= 640
        if r_i < len(rows) - 1:
            s.hr(y + rh - 4)
    yb = 84 + len(rows) * rh + 4
    s.text(40, yb + 8, "答案: return True    nums[2] = nums[4] = 3, 4 − 2 = 2 ≤ k = 2", 14, INK, weight=500)
    s.text(40, yb + 32, "i = 3 的 1 距离太远没命中, 但 last[1] 仍然要更新成 3 (为以后的 1 服务)。", 12, SUB)
    s.legend(yb + 62, [("new", "新写入 last", None), ("gone", "被覆盖的旧值", "dash"),
                       ("base", "last 里已有的", None), ("ring", "命中", None)])
    s.save("cd2_trace.svg")


# ============================================================
# 8. SVG: Valid Anagram
# ============================================================
def svg_anagram_core():
    s = Svg(396, "Valid Anagram: anagram 就是频率表相同",
            "顺序不重要, 两个字符串映射到同一个频率表; 小写字母时用 26 格数组, 下标就是字母。")
    s.text(40, 18, "anagram: 两个字符串用同样的字符、同样的次数, 顺序可以不同", 12, SUB)
    s.box(40, 40, 110, 34, "base", [('s = "rat"', 14, 500)])
    s.box(40, 90, 110, 34, "base", [('t = "tar"', 14, 500)])
    s.box(250, 38, 390, 88, "new", [("频率表 (顺序被丢掉了)", 12, 400), ("a:1   r:1   t:1", 14, 500)])
    s.path("M150 57 L248 70", "grey")
    s.path("M150 107 L248 96", "grey")
    s.text(250, 144, "两个字符串得到同一张表  ⇔  anagram, 所以不需要 sort 来 \"对齐顺序\"", 12, SUB)
    s.hr(162)
    s.text(40, 184, "小写字母: 用 [0] * 26, 字母直接当下标 (不需要 hash)", 14, INK, weight=500)
    letters = "abcdefghijklmnopqrstuvwxyz"
    cnt = {"a": 1, "r": 1, "t": 1}
    for j, ch in enumerate(letters):
        x = 40 + j * 23
        s.text(x + 10.5, 210, ch, 12, SUB, "middle")
        on = ch in cnt
        s.box(x, 222, 21, 28, "new" if on else "base", [(str(cnt.get(ch, 0)), 12, 500)])
    s.text(40, 270, "下标 = ord(ch) − 97:   ord('a') − 97 = 0,   ord('r') − 97 = 17,   ord('t') − 97 = 19", 12, SUB)
    s.hr(288)
    s.text(40, 310, "sorted(s) == sorted(t)", 14, INK, weight=500)
    s.text(300, 310, "O(n log n) 时间", 14, INK)
    s.text(40, 334, "数组计数 cnt", 14, INK, weight=500)
    s.text(300, 334, "O(n) 时间 · 固定 26 格 = O(1) 空间", 14, INK)
    s.text(40, 366, "字符集不固定 (Unicode 等): 26 格数组放不下, 换回 dict / Counter, 思路完全一样。", 12, SUB)
    s.save("anagram_core.svg")


def svg_anagram_trace():
    rows = an_rows
    rh = 60
    H = 84 + len(rows) * rh + 100
    s = Svg(H, "Valid Anagram 运行流程", "s 的字符让 cnt +1, t 的字符让 cnt −1; 最后看 cnt 是否全 0。")
    trace_header(s, 's = "rat", t = "car" · cnt = [0] * 26, 图里只画碰到过的格子 (letter:count)',
                 "第一个循环: s 的每个字符 cnt +1 · 第二个循环: t 的每个字符 cnt −1",
                 [(40, "当前字符"), (146, "操作"), (380, "cnt 现在是")])
    for r_i, r in enumerate(rows):
        y = 84 + r_i * rh
        role = "new" if r["ph"] == "s" else "gone"
        s.box(40, y + 4, 90, 44, role, [("%s[%d]" % (r["ph"], r["j"]), 12, 400), ("'%s'" % r["ch"], 14, 500)])
        s.path("M130 %d L144 %d" % (y + 26, y + 26), "grey")
        before = r["val"] - r["delta"]
        sign = "+= 1" if r["delta"] > 0 else "-= 1"
        s.text(152, y + 16, "cnt['%s'] %s" % (r["ch"], sign), 14, INK, weight=500)
        s.text(152, y + 38, "%d → %d" % (before, r["val"]), 12, SUB)
        xs = 380
        for c, v in r["cnt"]:
            changed = c == r["ch"]
            rl = ("new" if r["delta"] > 0 else "gone") if changed else "base"
            xs += s.chip(xs, y + 10, "%s:%d" % (c, v), rl, w=54) + 4
        assert xs - 4 <= 640
        if r_i < len(rows) - 1:
            s.hr(y + rh - 4, 40, 640)
    yb = 84 + len(rows) * rh + 8
    nz = ", ".join("%s:%d" % (c, v) for c, v in an_final if v)
    s.text(40, yb + 8, "最后: cnt 里还有 %s 不是 0  →  any(cnt) 为 True  →  return False" % nz, 14, INK, weight=500)
    s.text(40, yb + 32, "a、r 刚好抵消成 0; t 多了一个, c 少了一个, 所以 \"rat\" 和 \"car\" 不是 anagram。", 12, SUB)
    s.legend(yb + 62, [("new", "s 的字符 +1", None), ("gone", "t 的字符 −1", None), ("base", "没变的格子", None)])
    s.save("anagram_trace.svg")


# ============================================================
# 9. SVG: First Unique Character
# ============================================================
def svg_first_uniq_core():
    s = Svg(344, "First Unique Character: 先数完再按顺序找",
            "一遍扫描不知道后面还会不会出现同一个字符, 所以 pass 1 数全局频率, pass 2 按原顺序找第一个 cnt == 1。")
    s.text(40, 18, 's = "aabc" · 要找第一个只出现一次的字符的下标', 12, SUB)
    s.text(40, 50, "pass 1: 数全局频率 (不管顺序)", 14, INK, weight=500)
    chars = list(FU_S)
    for j, ch in enumerate(chars):
        s.box(50 + j * 52, 68, 46, 34, "base", [(ch, 14, 500)])
    xs = 330
    s.text(330, 56, "cnt", 12, SUB)
    full = fu_rows[len(FU_S) - 1]["cnt"]
    for c, v in full:
        xs += s.chip(xs, 70, "%s:%d" % (c, v), "base", w=54) + 4
    s.path("M262 85 L324 85", "grey")
    s.hr(122)
    s.text(40, 144, "pass 2: 按原顺序再扫, 第一个 cnt == 1 的就是答案", 14, INK, weight=500)
    marks = ["cnt = 2", "cnt = 2", "cnt = 1 ✓", "没扫到"]
    for j, ch in enumerate(chars):
        role = "base"
        x = 50 + j * 52
        if j == 2:
            role = "new"
        s.box(x, 162, 46, 34, role, [(ch, 14, 500)])
        if j == 2:
            s.ring(x, 162, 46, 34)
        s.text(x + 23, 214, marks[j], 12, "#085041" if j == 2 else SUB, "middle", 500 if j == 2 else 400)
    s.text(330, 170, "i = 0, 1: cnt = 2, 跳过", 12, SUB)
    s.text(330, 190, "i = 2: cnt = 1, return 2", 14, INK, weight=500)
    s.hr(236)
    s.text(40, 258, "为什么一遍不够?", 14, INK, weight=500)
    s.text(40, 280, "扫到 'b' (i = 2) 时, 一遍扫描回答不了 \"后面还会不会再出现 b\"。", 12, SUB)
    s.text(40, 300, "答案依赖全局信息 → 先数完 (O(n)), 再按原顺序查表 (O(n)), 合起来仍是 O(n)。", 12, SUB)
    s.text(40, 324, "不能直接遍历 cnt 找 == 1: 要的是 \"在原串里最靠前\", 不是 cnt 里最靠前 (dict 的顺序是首次出现顺序, 可行但不通用)。", 12, SUB)
    s.save("first_uniq_core.svg")


def svg_first_uniq_trace():
    rows = fu_rows
    rh = 54
    H = 84 + len(rows) * rh + 30 + 96
    s = Svg(H, "First Unique Character 运行流程", "pass 1 逐字符计数, pass 2 按原顺序检查 cnt, 遇到第一个 cnt == 1 就返回下标。")
    trace_header(s, 's = "aabc" · pass 1: 每个字符 cnt += 1 · pass 2: 按下标顺序看 cnt[ch] 是不是 1',
                 "cnt: 字符 → 出现次数",
                 [(40, "当前字符"), (146, "操作 / 判断"), (380, "cnt 现在是")])
    y = 84
    for r_i, r in enumerate(rows):
        if r["ph"] == 2 and (r_i == 0 or rows[r_i - 1]["ph"] == 1):
            s.text(40, y + 6, "pass 2: cnt 已经固定, 下面只查表、不再修改", 12, SUB)
            y += 22
            s.hr(y)
            y += 6
        if r["ph"] == 1:
            s.box(40, y, 90, 44, "new", [("pass 1", 12, 400), ("'%s'" % r["ch"], 14, 500)])
            s.path("M130 %d L144 %d" % (y + 22, y + 22), "grey")
            s.text(152, y + 14, "cnt['%s'] += 1" % r["ch"], 14, INK, weight=500)
            s.text(152, y + 34, "%d → %d" % (r["val"] - 1, r["val"]), 12, SUB)
            xs = 380
            for c, v in r["cnt"]:
                xs += s.chip(xs, y + 8, "%s:%d" % (c, v), "new" if c == r["ch"] else "base", w=54) + 4
        else:
            role = "new" if r["hit"] else "base"
            s.box(40, y, 90, 44, role, [("s[%d]" % r["i"], 12, 400), ("'%s'" % r["ch"], 14, 500)])
            s.path("M130 %d L144 %d" % (y + 22, y + 22), "grey")
            s.text(152, y + 14, "cnt['%s'] = %d" % (r["ch"], r["val"]), 14, INK, weight=500)
            if r["hit"]:
                s.text(152, y + 34, "== 1 → return %d" % r["i"], 12, "#085041", weight=500)
            else:
                s.text(152, y + 34, "≠ 1 → 跳过", 12, SUB)
            xs = 380
            for c, v in r["cnt"]:
                w = s.chip(xs, y + 8, "%s:%d" % (c, v), "base", w=54)
                if c == r["ch"]:
                    s.ring(xs, y + 8, w, 28)
                xs += w + 4
        assert xs - 4 <= 640
        y += rh
        if r_i < len(rows) - 1 and rows[r_i + 1]["ph"] == rows[r_i]["ph"]:
            s.hr(y - 5)
    s.text(40, y + 14, "答案: return 2    's[2] = b' 是第一个 cnt == 1 的字符", 14, INK, weight=500)
    s.text(40, y + 38, "'c' 的 cnt 也是 1, 但 pass 2 在 'b' 就返回了, 不会扫到它。", 12, SUB)
    s.legend(y + 68, [("new", "计数 +1 / 命中", None), ("base", "cnt 里已有的", None), ("ring", "pass 2 正在检查的", None)])
    s.save("first_uniq_trace.svg")


# ============================================================
# 10. SVG: Group Anagrams
# ============================================================
def svg_group_core():
    s = Svg(414, "Group Anagrams: canonical key",
            "两两比较要 O(n^2) 次; 给每个词算一个 canonical key, 同组的词 key 相同, 一次遍历用 dict 分桶。")
    s.text(40, 18, 'strs = ["eat", "tea", "tan", "ate", "nat", "bat"]', 12, SUB)
    s.text(40, 52, "brute force: 两两比较", 14, INK, weight=500)
    s.text(370, 52, "canonical key: 算 key → 放进同一个桶", 14, INK, weight=500)
    s.vline(350, 40, 264)
    s.text(40, 82, "6 个词 → C(6, 2) = 15 对", 12, SUB)
    s.text(40, 104, "每一对都要比一次 (sorted 或 Counter)", 12, SUB)
    s.text(40, 126, "eat vs tea ✓   eat vs tan ✗", 12, SUB)
    s.text(40, 146, "eat vs ate ✓   eat vs nat ✗", 12, SUB)
    s.text(40, 166, "eat vs bat ✗   tea vs tan ✗ ...", 12, SUB)
    s.text(40, 210, "n 个词 → n² 对", 14, INK, weight=500)
    s.text(40, 232, "O(n² · k log k)", 14, INK, weight=500)
    s.text(40, 254, "浪费: 同组的词被反复比较", 12, "#712B13")
    buckets = [("aet", ["eat", "tea", "ate"]), ("ant", ["tan", "nat"]), ("abt", ["bat"])]
    for r_i, (key, ws) in enumerate(buckets):
        y = 76 + r_i * 62
        s.box(370, y, 56, 36, "new", [(key, 14, 500)])
        s.path("M428 %d L446 %d" % (y + 18, y + 18), "grey")
        xs = 450
        for w in ws:
            xs += s.chip(xs, y + 4, w, "base", w=44) + 4
        assert xs <= 640
    s.text(370, 268, "key = sorted(w): \"eat\" → \"aet\", \"tea\" → \"aet\"", 12, SUB)
    s.hr(288)
    s.text(40, 310, "对 key 的要求", 14, INK, weight=500)
    s.text(40, 332, "同组 → key 相同;  不同组 → key 不同;  key 必须 hashable (str / tuple, 不能是 list)", 12, SUB)
    s.text(40, 356, "sorted 当 key: O(k log k)", 14, INK, weight=500)
    s.text(300, 356, "26 格计数 tuple 当 key: O(k)", 14, INK, weight=500)
    s.text(40, 380, "n 个词, 每个词算一次 key + 一次 dict 操作 → 总共 O(n · k log k) 或 O(n · k)", 12, SUB)
    s.save("group_core.svg")


def svg_group_trace():
    rows = ga_rows
    heights = [max(72, 30 * len(r["groups"]) + 12) for r in rows]
    H = 84 + sum(heights) + 100
    s = Svg(H, "Group Anagrams 运行流程", "每个词算 key = sorted(w), 放进 groups[key]; 没见过的 key 自动新建一个桶。")
    trace_header(s, "key = sorted(w) 拼成字符串 · groups[key].append(w)",
                 "groups: key → 这一组的词",
                 [(40, "当前词"), (130, "算 key"), (320, "groups 现在有")])
    y = 84
    for r_i, r in enumerate(rows):
        h = heights[r_i]
        s.box(40, y + 6, 70, 40, "new", [(r["w"], 14, 500)])
        s.path("M110 %d L128 %d" % (y + 26, y + 26), "grey")
        s.text(136, y + 14, "sorted('%s')" % r["w"], 12, SUB)
        s.text(136, y + 34, "key = '%s'" % r["key"], 14, INK, weight=500)
        if r["new_key"]:
            s.text(136, y + 52, "新 key, 新建桶", 12, "#085041")
        for g_i, (k, ws) in enumerate(r["groups"]):
            gy = y + 6 + g_i * 30
            s.text(320, gy + 14, "'%s' →" % k, 14, INK, weight=500 if k == r["key"] else 400)
            xs = 396
            for w_i, w in enumerate(ws):
                newly = k == r["key"] and w_i == len(ws) - 1
                xs += s.chip(xs, gy, w, "new" if newly else "base", w=44, h=26) + 4
            assert xs - 4 <= 640
        y += h
        if r_i < len(rows) - 1:
            s.hr(y - 4)
    final = rows[-1]["groups"]
    s.text(40, y + 10, "答案: " + ", ".join("[" + ", ".join(ws) + "]" for _, ws in final), 14, INK, weight=500)
    s.text(40, y + 34, "3 个 key → 3 组; 每个词只算一次 key, 没有任何 \"两两比较\"。", 12, SUB)
    s.legend(y + 64, [("new", "刚放进桶的词", None), ("base", "桶里已有的词", None)])
    s.save("group_trace.svg")


# ============================================================
# 11. SVG: Longest Consecutive Sequence
# ============================================================
def svg_lcs_core():
    s = Svg(484, "Longest Consecutive Sequence: 只从序列起点开始数",
            "每个数都往右数会重复走同一段, 总共 O(n^2); 只有 x-1 不在 set 里的数才是起点, 才开始数, 每段只走一遍。")
    s.text(40, 18, "一个序列 {1, 2, 3, 4} (其余数 100, 200 同理, 各是长度 1 的序列)", 12, SUB)
    s.text(40, 50, "每个数都往右数 (set 只当 O(1) 查询用)", 14, INK, weight=500)
    cw, x0 = 54, 60
    for j, v in enumerate([1, 2, 3, 4]):
        s.text(x0 + j * cw + 23, 74, str(v), 12, SUB, "middle")
    for r_i in range(4):
        y = 86 + r_i * 32
        for j in range(r_i, 4):
            s.box(x0 + j * cw, y, 46, 26, "gone", [(str(j + 1), 14, 500)])
        s.text(x0 + 4 * cw + 10, y + 13, "从 %d 出发, 走 %d 步" % (r_i + 1, 4 - r_i), 12, SUB)
    s.text(40, 226, "4 + 3 + 2 + 1 = 10 步, 一般 n 个连续数是 n(n+1)/2 = O(n²)", 14, INK, weight=500)
    s.text(40, 246, "红色格子 = 重复走的路: 2、3、4 被走了好几遍", 12, "#712B13")
    s.hr(266)
    s.text(40, 288, "只从起点数: 先问 x − 1 in s?", 14, INK, weight=500)
    for j, v in enumerate([1, 2, 3, 4]):
        s.text(x0 + j * cw + 23, 312, str(v), 12, SUB, "middle")
    for r_i in range(4):
        y = 322 + r_i * 32
        if r_i == 0:
            for j in range(4):
                s.box(x0 + j * cw, y, 46, 26, "new", [(str(j + 1), 14, 500)])
            s.ring(x0, y, 46, 26)
            s.text(x0 + 4 * cw + 10, y + 13, "0 不在 s → 起点, 走 4 步", 12, "#085041", weight=500)
        else:
            s.box(x0 + r_i * cw, y, 46, 26, "base", [(str(r_i + 1), 14, 500)])
            s.text(x0 + 4 * cw + 10, y + 13, "%d 在 s → 不是起点, 跳过" % r_i, 12, SUB)
    s.text(40, 464, "每个数最多被 \"起点\" 走一次, 加上每个数一次判断: O(n)", 14, INK, weight=500)
    s.save("lcs_core.svg")


def svg_lcs_trace():
    rows = lc_rows
    rh = 68
    H = 108 + len(rows) * rh + 100
    s = Svg(H, "Longest Consecutive Sequence 运行流程", "遍历 set; x−1 在 set 里就跳过, 否则从 x 往右数; best 记录最长长度。")
    s.text(40, 18, "nums = [100, 4, 200, 1, 3, 2] · s = set(nums), 下面按 Python 遍历 s 的真实顺序", 12, SUB)
    s.text(40, 38, "每一步: x − 1 in s? 在 → 跳过; 不在 → 是起点, 往右一直数到断开", 12, SUB)
    s.text(40, 66, "s =", 12, SUB)
    xs = 70
    for v in lc_order:
        xs += s.chip(xs, 52, str(v), "base", h=26) + 4
    for x, label in ((40, "当前"), (130, "先问"), (330, "往右数 (在 s 里连续的数)"), (590, "best")):
        s.text(x, 92, label, 12, SUB)
    s.hr(102)
    for r_i, r in enumerate(rows):
        y = 110 + r_i * rh
        s.box(40, y + 4, 62, 44, "new" if r["start"] else "base", [("x", 12, 400), (str(r["x"]), 14, 500)])
        s.path("M102 %d L120 %d" % (y + 26, y + 26), "grey")
        s.text(128, y + 14, "%d − 1 = %d" % (r["x"], r["x"] - 1), 14, INK, weight=500)
        if r["start"]:
            s.text(128, y + 36, "%d in s? 否 → 起点" % (r["x"] - 1), 12, "#085041", weight=500)
            xs = 330
            for k, v in enumerate(r["walk"]):
                xs += s.chip(xs, y + 10, str(v), "new", w=40) + 4
            s.text(330, y + 52, "len = %d  (从 %d 数到 %d)" % (len(r["walk"]), r["walk"][0], r["walk"][-1]), 12, SUB)
            if len(r["walk"]) > 1:
                s.ring(330, y + 10, 40, 28)
            assert xs <= 580
        else:
            s.text(128, y + 36, "%d in s? 是 → 不是起点, 跳过" % (r["x"] - 1), 12, SUB)
            s.text(330, y + 26, "不数", 12, SUB)
        s.text(590, y + 26, str(r["best"]), 14, INK, weight=500)
        if r_i < len(rows) - 1:
            s.hr(y + rh - 4)
    yb = 110 + len(rows) * rh + 4
    total = sum(len(r["walk"]) for r in rows)
    s.text(40, yb + 8, "答案: best = 4    序列 1, 2, 3, 4", 14, INK, weight=500)
    s.text(40, yb + 32, "往右数的格子总数 = 4 + 1 + 1 = %d = n: 每个数只被它所在序列的起点数过一次。" % total, 12, SUB)
    s.legend(yb + 62, [("new", "起点 / 往右数到的", None), ("base", "set 里的数 / 被跳过", None), ("ring", "最长的一段", None)])
    s.save("lcs_trace.svg")


for fn in (svg_principle, svg_two_sum_core, svg_two_sum_trace, svg_cd2_core, svg_cd2_trace,
           svg_anagram_core, svg_anagram_trace, svg_first_uniq_core, svg_first_uniq_trace,
           svg_group_core, svg_group_trace, svg_lcs_core, svg_lcs_trace):
    fn()

exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '01_hash_table_doc.py'), encoding='utf-8').read())
