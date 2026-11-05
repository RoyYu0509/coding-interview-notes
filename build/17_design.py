"""17 · Data Structure Design  ->  docs/17-design.html

所有代码块都是真的 Python: 先 exec 跑过 (含随机对拍), 再从真实运行的状态画 SVG,
所以图里的数字和代码的实际行为一致。
运行: cd build && python3 -I 17_design.py
"""
import html
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import doclib as d  # noqa: E402

SVG_DIR = os.path.join(d.ROOT, "docs", "svg", "17-design")
os.makedirs(SVG_DIR, exist_ok=True)

# ----------------------------------------------------------------------------
# 1. 代码 (doc 里展示的就是这些字符串; 下面会 exec 并测试)
# ----------------------------------------------------------------------------

CODE_TEMPLATE = '''
class Design:
    def __init__(self):
        self.index = {}      # 结构 A: 擅长 "按 key O(1) 找到东西"
        self.order = ...     # 结构 B: 擅长 "顺序 / 位置 / 最旧 / <= t"  (list, DLL, deque ...)

    def op(self, key):
        # 1) 用 A 在 O(1) 内定位     -> 拿到 B 里的位置 (node / index)
        # 2) 用 B 在 O(1) 内做顺序操作
        # 3) 回头把 A 也改掉          -> invariant: A 和 B 永远描述同一批元素
        ...
'''

CODE_LRU = '''
class Node:
    def __init__(self, key=0, val=0):
        self.key, self.val = key, val   # node 里也存 key: 踢人时要靠它去 del cache[key]
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.cache = {}                         # key -> Node     (O(1) 找 node)
        self.head, self.tail = Node(), Node()   # dummy: 永远存在, 摘/插都不用判 None
        self.head.next, self.tail.prev = self.tail, self.head
        # list 顺序:  head <-> LRU(最久没用) ... MRU(刚用过) <-> tail

    def _remove(self, node):                    # O(1): 有 prev 才能不扫描就摘下来
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_tail(self, node):               # O(1): 接到 tail 前面 = 变成 MRU
        last = self.tail.prev
        last.next, node.prev = node, last
        node.next, self.tail.prev = self.tail, node

    def get(self, key):
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)                      # 用过了: 摘下来 ...
        self._add_to_tail(node)                 # ... 放到 MRU 端
        return node.val

    def put(self, key, val):
        if key in self.cache:                   # 已存在: 更新值 + 变成 MRU
            node = self.cache[key]
            node.val = val
            self._remove(node)
            self._add_to_tail(node)
            return
        node = Node(key, val)
        self.cache[key] = node                  # dict 和 list 一起加 (同步)
        self._add_to_tail(node)
        if len(self.cache) > self.cap:          # 超过 capacity: 踢 LRU = head.next
            lru = self.head.next
            self._remove(lru)
            del self.cache[lru.key]             # dict 也要删 (同步) -> 所以 node 要存 key
'''

CODE_LRU_OD = '''
from collections import OrderedDict

class LRUCache:                                  # 面试速写版: OrderedDict = dict + DLL 已经帮你焊好
    def __init__(self, capacity):
        self.cap = capacity
        self.od = OrderedDict()                  # 左 = LRU, 右 = MRU

    def get(self, key):
        if key not in self.od:
            return -1
        self.od.move_to_end(key)                 # O(1): 变成 MRU
        return self.od[key]

    def put(self, key, val):
        self.od[key] = val
        self.od.move_to_end(key)                 # 新 key 本来就在最右, 旧 key 要挪过去
        if len(self.od) > self.cap:
            self.od.popitem(last=False)          # O(1): 弹最左 = 踢 LRU
'''

CODE_RS = '''
import random

class RandomizedSet:
    def __init__(self):
        self.nums = []        # 能 O(1) random.choice(nums)  <- 只有 list 能按 index O(1) 取
        self.pos = {}         # val -> 它在 nums 里的 index    <- 只有 dict 能按 val O(1) 找

    def insert(self, val):
        if val in self.pos:
            return False
        self.pos[val] = len(self.nums)        # 先记 index, 再 append
        self.nums.append(val)
        return True

    def remove(self, val):
        if val not in self.pos:
            return False
        i = self.pos[val]                     # 要删的 val 在哪
        last = self.nums[-1]                  # 末尾元素: list 只有删末尾才是 O(1)
        self.nums[i] = last                   # 把末尾搬到 i, 覆盖 val
        self.pos[last] = i                    # last 的 index 变了, dict 必须同步
        self.nums.pop()                       # 删尾巴 O(1)
        del self.pos[val]                     # 顺序不能反: val == last 时, 这行才会把它删干净
        return True

    def getRandom(self):
        return random.choice(self.nums)       # 每个 index 等概率
'''

CODE_TM = '''
from bisect import bisect_right
from collections import defaultdict

class TimeMap:
    def __init__(self):
        self.times = defaultdict(list)   # key -> [timestamp ...]  严格递增 (题目保证)
        self.vals = defaultdict(list)    # key -> [value ...]      和 times 同一个 index

    def set(self, key, value, timestamp):
        self.times[key].append(timestamp)    # 时间只增不减 -> append 之后天然有序, 不用 sort
        self.vals[key].append(value)

    def get(self, key, timestamp):
        ts = self.times.get(key)             # 用 .get: 避免 defaultdict 悄悄造一个空 list
        if not ts:
            return ""
        i = bisect_right(ts, timestamp) - 1  # 最后一个 <= t 的 idx; 全更大 -> -1
        return self.vals[key][i] if i >= 0 else ""
'''

CODE_HC = '''
from collections import deque

class HitCounter:
    def __init__(self):
        self.q = deque()                     # 时间戳, 左 = 最旧, 右 = 最新 (题目保证 timestamp 不减)

    def hit(self, timestamp):
        self.q.append(timestamp)             # 新的永远在右边

    def getHits(self, timestamp):            # 窗口: (timestamp - 300, timestamp]
        while self.q and self.q[0] <= timestamp - 300:
            self.q.popleft()                 # 过期的一定在最左边: 从左边出队, 每个时间戳只出一次
        return len(self.q)                   # 剩下的就是窗口内的
'''

CODE_LOGGER = '''
class Logger:                                # Logger Rate Limiter: 不用 deque, 一个 dict 就够
    def __init__(self):
        self.next_ok = {}                    # message -> 最早什么时候又可以打印

    def shouldPrintMessage(self, timestamp, message):
        if timestamp < self.next_ok.get(message, 0):
            return False                     # 还在 10 秒冷却里
        self.next_ok[message] = timestamp + 10
        return True
'''

CODE_SNAP = '''
from bisect import bisect_right

class SnapshotArray:
    def __init__(self, length):
        # hist[i] = [(snap_id, val), ...]  只记录 "index i 在哪个 snap_id 期间被改成了 val"
        self.hist = [[(0, 0)] for _ in range(length)]   # 初值 (0, 0): bisect 不会落到 -1
        self.snap_id = 0                                # 下一次 snap() 要返回的 id = 当前 "进行中" 的版本

    def set(self, index, val):
        h = self.hist[index]
        if h[-1][0] == self.snap_id:                    # 本版本里已经改过: 覆盖, 不重复记
            h[-1] = (self.snap_id, val)
        else:
            h.append((self.snap_id, val))               # snap_id 只增 -> h 天然按 snap_id 有序

    def snap(self):
        self.snap_id += 1                               # O(1): 不复制任何东西
        return self.snap_id - 1

    def get(self, index, snap_id):
        h = self.hist[index]
        i = bisect_right(h, (snap_id, float("inf"))) - 1   # 最后一个 <= snap_id 的记录
        return h[i][1]
'''

CODE_LFU = '''
from collections import defaultdict, OrderedDict

class LFUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.val = {}                            # key -> value
        self.freq = {}                           # key -> 访问次数
        self.bucket = defaultdict(OrderedDict)   # freq -> {key: None}, 左 = 最久没用
        self.min_freq = 0                        # 当前最小的 freq: 踢人去 bucket[min_freq] 的最左边

    def _touch(self, key):                       # key 被用了一次: 从 bucket[f] 搬到 bucket[f + 1]
        f = self.freq[key]
        del self.bucket[f][key]
        if not self.bucket[f]:
            del self.bucket[f]
            if self.min_freq == f:               # 最低的桶空了 -> 最小频率一定正好 +1
                self.min_freq += 1
        self.freq[key] = f + 1
        self.bucket[f + 1][key] = None           # 接到右边 = 这个频率里最新的

    def get(self, key):
        if key not in self.val:
            return -1
        self._touch(key)
        return self.val[key]

    def put(self, key, value):
        if self.cap == 0:
            return
        if key in self.val:
            self.val[key] = value
            self._touch(key)
            return
        if len(self.val) >= self.cap:            # 满了: 先踢 (频率最低里, 最久没用的)
            old, _ = self.bucket[self.min_freq].popitem(last=False)
            if not self.bucket[self.min_freq]:
                del self.bucket[self.min_freq]
            del self.val[old]
            del self.freq[old]
        self.val[key] = value
        self.freq[key] = 1
        self.bucket[1][key] = None
        self.min_freq = 1                        # 新 key freq = 1, 一定是最小的
'''


def load(src):
    ns = {}
    exec(src, ns)
    return ns


# ---------------------------------------------------------------- 测试 (对拍)
def test_all():
    from collections import OrderedDict
    rnd = random.Random(17)
    # LRU: DLL 版 vs OrderedDict 版 vs 朴素 list 版
    A, B = load(CODE_LRU)["LRUCache"], load(CODE_LRU_OD)["LRUCache"]
    for _ in range(300):
        cap = rnd.randint(1, 4)
        a, b = A(cap), B(cap)
        ref = []     # [(k, v)] 左 = LRU
        for _ in range(60):
            k = rnd.randint(0, 6)
            if rnd.random() < 0.5:
                exp = -1
                for i, (kk, vv) in enumerate(ref):
                    if kk == k:
                        exp = vv
                        ref.append(ref.pop(i))
                        break
                assert a.get(k) == exp == b.get(k)
            else:
                v = rnd.randint(0, 99)
                ref = [(kk, vv) for kk, vv in ref if kk != k] + [(k, v)]
                if len(ref) > cap:
                    ref.pop(0)
                a.put(k, v)
                b.put(k, v)
            order = []
            n = a.head.next
            while n is not a.tail:
                order.append((n.key, n.val))
                n = n.next
            assert order == ref == list(b.od.items()), (order, ref)
            assert set(a.cache) == {k for k, _ in ref}
    # RandomizedSet
    R = load(CODE_RS)["RandomizedSet"]
    for _ in range(300):
        r, ref = R(), set()
        for _ in range(80):
            v = rnd.randint(0, 8)
            op = rnd.choice("irg")
            if op == "i":
                assert r.insert(v) == (v not in ref)
                ref.add(v)
            elif op == "r":
                assert r.remove(v) == (v in ref)
                ref.discard(v)
            elif ref:
                assert r.getRandom() in ref
            assert sorted(r.nums) == sorted(ref)
            assert all(r.nums[i] == v for v, i in r.pos.items())
    # TimeMap
    T = load(CODE_TM)["TimeMap"]
    for _ in range(200):
        t, ref, now = T(), {}, 0
        for _ in range(60):
            k = rnd.choice("ab")
            if rnd.random() < 0.5:
                now += rnd.randint(1, 3)
                v = str(rnd.randint(0, 99))
                t.set(k, v, now)
                ref.setdefault(k, []).append((now, v))
            else:
                q = rnd.randint(0, now + 2)
                exp = ""
                for tt, vv in ref.get(k, []):
                    if tt <= q:
                        exp = vv
                assert t.get(k, q) == exp
    # HitCounter
    H = load(CODE_HC)["HitCounter"]
    for _ in range(200):
        h, hits, now = H(), [], 0
        for _ in range(60):
            now += rnd.randint(0, 120)
            if rnd.random() < 0.6:
                h.hit(now)
                hits.append(now)
            else:
                assert h.getHits(now) == sum(1 for x in hits if x > now - 300)
    # Logger
    L = load(CODE_LOGGER)["Logger"]
    for _ in range(200):
        lg, last, now = L(), {}, 0
        for _ in range(60):
            now += rnd.randint(0, 6)
            m = rnd.choice("xyz")
            exp = m not in last or now >= last[m] + 10
            if exp:
                last[m] = now
            assert lg.shouldPrintMessage(now, m) == exp
    # SnapshotArray
    S = load(CODE_SNAP)["SnapshotArray"]
    for _ in range(200):
        n = rnd.randint(1, 5)
        s, arr, snaps = S(n), [0] * n, []
        for _ in range(60):
            op = rnd.choice("ssgn")
            if op == "s":
                i, v = rnd.randrange(n), rnd.randint(0, 9)
                s.set(i, v)
                arr[i] = v
            elif op == "n":
                assert s.snap() == len(snaps)
                snaps.append(list(arr))
            elif snaps:
                i, sid = rnd.randrange(n), rnd.randrange(len(snaps))
                assert s.get(i, sid) == snaps[sid][i]
    # LFU vs 朴素实现
    F = load(CODE_LFU)["LFUCache"]
    for _ in range(300):
        cap = rnd.randint(0, 4)
        f = F(cap)
        ref = {}   # key -> [val, freq, last_used_time]
        clock = 0
        for _ in range(80):
            clock += 1
            k = rnd.randint(0, 6)
            if rnd.random() < 0.5:
                exp = -1
                if k in ref:
                    exp = ref[k][0]
                    ref[k][1] += 1
                    ref[k][2] = clock
                assert f.get(k) == exp
            else:
                v = rnd.randint(0, 99)
                f.put(k, v)
                if cap == 0:
                    continue
                if k in ref:
                    ref[k] = [v, ref[k][1] + 1, clock]
                else:
                    if len(ref) >= cap:
                        victim = min(ref, key=lambda x: (ref[x][1], ref[x][2]))
                        del ref[victim]
                    ref[k] = [v, 1, clock]
            assert set(f.val) == set(ref)
            assert all(f.freq[x] == ref[x][1] for x in ref)
    print("all design tests passed")


test_all()

# ----------------------------------------------------------------------------
# 2. SVG 小工具 (配色 / 字号严格按 STYLE_GUIDE B)
# ----------------------------------------------------------------------------
FONT = 'ui-sans-serif, system-ui, -apple-system, &quot;PingFang SC&quot;, sans-serif'
INK, SUB = "#0B0B0B", "#52514E"
ROLE = {   # fill, stroke, text
    "new": ("#E1F5EE", "#0F6E56", "#085041"),
    "gone": ("#FAECE7", "#993C1D", "#712B13"),
    "cur": ("#F1EFE8", "#5F5E5A", "#444441"),
    "none": ("#FFFFFF", "#B4B2A9", "#52514E"),
}
AMBER = "#EF9F27"


def tw(s, size=12):
    """估算文字宽度 (CJK 约 1em, 其余约 0.56em)"""
    return sum(size if ord(c) > 0x2E80 else size * 0.56 for c in s)


class Svg:
    def __init__(self, h, title, desc, w=680):
        self.w, self.h = w, h
        self.o = []
        self.title, self.desc = title, desc

    def t(self, x, y, s, size=12, fill=SUB, anchor="start", weight=400):
        self.o.append(
            '<text x="%s" y="%s" text-anchor="%s" dominant-baseline="central" '
            'font-size="%d" font-weight="%d" fill="%s">%s</text>'
            % (x, y, anchor, size, weight, fill, html.escape(str(s), quote=False)))

    def box(self, x, y, w, h, label, role="cur", sub=None, dashed=False, r=4, size=14):
        fill, stroke, txt = ROLE[role]
        dash = ' stroke-dasharray="4 3"' if dashed else ""
        self.o.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%d" fill="%s" '
                      'stroke="%s" stroke-width="1"%s/>' % (x, y, w, h, r, fill, stroke, dash))
        if sub is None:
            self.t(x + w / 2, y + h / 2, label, size, txt, "middle", 500)
        else:
            self.t(x + w / 2, y + h / 2 - 8, label, size, txt, "middle", 500)
            self.t(x + w / 2, y + h / 2 + 9, sub, 12, txt, "middle")

    def ring(self, x, y, w, h):
        self.o.append('<rect x="%s" y="%s" width="%s" height="%s" rx="6" fill="none" '
                      'stroke="%s" stroke-width="2.5"/>' % (x - 3, y - 3, w + 6, h + 6, AMBER))

    def line(self, x1, y1, x2, y2, color=SUB, dashed=False, width=1.5, head=True, tail=False):
        mk = "r" if color == "#D85A30" else "g"
        a = ' marker-end="url(#ar-%s)"' % mk if head else ""
        b = ' marker-start="url(#ar-%s)"' % mk if tail else ""
        dash = ' stroke-dasharray="5 4"' if dashed else ""
        self.o.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s%s%s/>'
                      % (x1, y1, x2, y2, color, width, dash, a, b))

    def path(self, dd, color=SUB, dashed=False, head=True):
        mk = "r" if color == "#D85A30" else "g"
        a = ' marker-end="url(#ar-%s)"' % mk if head else ""
        dash = ' stroke-dasharray="5 4"' if dashed else ""
        self.o.append('<path d="%s" fill="none" stroke="%s" stroke-width="1.5"%s%s/>'
                      % (dd, color, dash, a))

    def sep(self, y, x1=40, x2=640):
        self.o.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#B4B2A9" '
                      'stroke-width="0.8" stroke-dasharray="4 4"/>' % (x1, y, x2, y))

    def legend(self, y, items, x=40):
        for kind, label in items:
            if kind == "ring":
                self.o.append('<rect x="%s" y="%s" width="16" height="12" rx="3" fill="none" '
                              'stroke="%s" stroke-width="2.5"/>' % (x, y - 6, AMBER))
            else:
                fill, stroke, _ = ROLE[kind.replace("-d", "")]
                dash = ' stroke-dasharray="3 2"' if kind.endswith("-d") else ""
                self.o.append('<rect x="%s" y="%s" width="16" height="12" rx="3" fill="%s" '
                              'stroke="%s"%s/>' % (x, y - 6, fill, stroke, dash))
            self.t(x + 22, y, label, 12, SUB)
            x += 22 + tw(label) + 16

    def save(self, name):
        head = ('<svg width="100%%" viewBox="0 0 %d %d" role="img" xmlns="http://www.w3.org/2000/svg" '
                'font-family="%s">'
                '<title>%s</title><desc>%s</desc><defs>'
                '<marker id="ar-g" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" '
                'orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#52514E" '
                'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>'
                '<marker id="ar-r" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" '
                'orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#D85A30" '
                'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>\n'
                % (self.w, self.h, FONT, html.escape(self.title), html.escape(self.desc)))
        with open(os.path.join(SVG_DIR, name), "w", encoding="utf-8") as f:
            f.write(head + "\n".join(self.o) + "\n</svg>\n")


def dbl(s, x1, x2, y):
    """两个 box 之间的双向箭头 (x1 = 左 box 右边缘, x2 = 右 box 左边缘)"""
    s.line(x1 + 2, y, x2 - 2, y, head=True, tail=True, width=1.3)


# ----------------------------------------------------------------------------
# 3. SVG 0: 第一性原理 —— 操作 x 数据结构 能力对照
# ----------------------------------------------------------------------------
def svg_matrix():
    s = Svg(496, "操作 x 数据结构 能力对照",
            "每个单一数据结构只擅长一两个操作; design 题把擅长不同操作的结构组合起来。")
    s.t(40, 18, "design 题: 先列出每个操作要求的 complexity, 再看哪个结构能 O(1) / O(log n) 做它", 12)
    s.t(40, 38, "单个结构总有弱项 -> 组合两个, 每个操作交给擅长它的那个, 并让两者同步", 12)
    ops = ["按 key 查", "按 index 取", "删中间\n(已知位置)", "删最旧", "找 <= t\n最近的"]
    rows = [
        ("dict", ["O(1)", "x", "O(1)", "x", "x"], "g g b g b b".split()),
        ("list / array", ["O(n)", "O(1)", "O(n)", "O(n)", "O(n)"], None),
        ("doubly linked list", ["O(n)", "O(n)", "O(1)", "O(1)", "O(n)"], None),
        ("deque", ["O(n)", "O(n)", "O(n)", "O(1)", "O(n)"], None),
        ("sorted list + bisect", ["O(n)", "O(1)", "O(n)", "O(n)", "O(log n)"], None),
    ]
    x0, cw, ch, y0 = 190, 88, 36, 100
    for j, op in enumerate(ops):
        for k, ln in enumerate(op.split("\n")):
            n = len(op.split("\n"))
            s.t(x0 + j * cw + cw / 2, y0 - 22 + (k - (n - 1) / 2) * 15, ln, 12, INK, "middle")
    s.sep(y0 - 4)
    for i, (name, cells, _) in enumerate(rows):
        y = y0 + i * (ch + 6)
        s.t(40, y + ch / 2, name, 14, INK, "start", 500)
        for j, c in enumerate(cells):
            role = "new" if c.startswith("O(1)") or c == "O(log n)" else "gone" if c.startswith("O(n)") else "cur"
            lab = "不靠它" if c == "x" else c
            s.box(x0 + j * cw + 4, y, cw - 8, ch, lab, role, size=14 if c != "x" else 12)
    yb = y0 + 5 * (ch + 6) + 6
    s.sep(yb - 4)
    s.t(40, yb + 10, "组合 (A + B = 两个结构存同一批元素的两个视图, 每次 mutate 两边一起改):", 14, INK, "start", 500)
    combos = [
        ("LRU Cache", "按 key 查 + 删中间 + 删最旧", "dict + doubly linked list"),
        ("GetRandom O(1)", "按 key 查 + 按 index 取 + 删", "dict + list  (交换到末尾再 pop)"),
        ("Time Based KV", "按 key 查 + 找 <= t", "dict + sorted list  (append 天然有序)"),
        ("Hit Counter", "按序追加 + 删最旧", "只要 deque"),
    ]
    for i, (n, need, ans) in enumerate(combos):
        y = yb + 28 + i * 30
        s.t(40, y, n, 14, INK, "start", 500)
        s.t(170, y, need, 12, SUB)
        s.t(400, y, "= " + ans, 12, INK)
    s.legend(s.h - 18, [("new", "这个结构能 O(1) / O(log n) 做"), ("gone", "只能 O(n)"), ("cur", "不靠它")])
    s.save("first_principles_core.svg")


# ----------------------------------------------------------------------------
# 4. LRU: core + trace
# ----------------------------------------------------------------------------
def svg_lru_core():
    s = Svg(580, "LRU Cache: dict 加 doubly linked list",
            "dict 负责按 key 找到 node, doubly linked list 负责顺序; 两者通过 node 指针连在一起。")
    s.t(40, 18, "get 需要: 按 key 找到 + 移到最新 · put 满了需要: 找到最旧并删掉 · 三件事都要 O(1)", 12)
    s.t(40, 38, "dict 擅长第一件, list 擅长后两件 -> 两个结构存同一批 node, dict 的 value 就是 node 指针", 12)
    # 上: 链表
    s.t(130, 66, "LRU 端 (最久没用, 要踢的)", 12, SUB)
    s.t(450, 66, "MRU 端 (刚用过)", 12, SUB, "end")
    y, h = 80, 34
    xs = [(40, 50, "head", "cur"), (130, 80, "2:20", "cur"), (250, 80, "1:10", "cur"),
          (370, 80, "3:30", "cur"), (490, 50, "tail", "cur")]
    for x, w, lab, role in xs:
        s.box(x, y, w, h, lab, role)
    s.box(40, y, 50, h, "head", "none")
    s.box(490, y, 50, h, "tail", "none")
    for (xa, wa, _, _), (xb, _, _, _) in zip(xs, xs[1:]):
        dbl(s, xa + wa, xb, y + h / 2)
    s.ring(130, y, 80, h)
    s.t(40, y + h + 14, "dummy", 12, SUB)
    s.t(490, y + h + 14, "dummy", 12, SUB)
    # dict 与 node 对齐
    yd = 170
    s.t(40, yd + 17, "dict", 14, INK, "start", 500)
    for x, k in [(130, 2), (250, 1), (370, 3)]:
        s.box(x, yd, 80, 34, "%d" % k, "cur", size=14)
        s.line(x + 40, yd - 1, x + 40, y + h + 2)
    s.t(560, yd + 17, "dict 无序, 这里只是", 12, SUB)
    s.t(560, yd + 35, "对齐 node 来画", 12, SUB)
    s.sep(232)
    # 三条理由
    lines = [
        ("get(k)", "dict[k] 拿到 node (O(1)) -> 从 list 摘下 (O(1)) -> 接到 tail 前 (O(1))"),
        ("满了", "list 的 head.next 就是 LRU (O(1)) -> 摘掉, 再 del dict[node.key] (O(1))"),
        ("为什么 doubly", "摘 node 要改 node.prev.next · singly 找前驱要从头扫 O(n)"),
        ("为什么存 key", "踢 head.next 时手里只有 node, 要靠 node.key 去 del dict[key]"),
        ("为什么 dummy", "head / tail 永远在, 摘和插都不用判断 None 或 first / last"),
    ]
    for i, (a, b) in enumerate(lines):
        yy = 254 + i * 22
        s.t(40, yy, a, 12, INK, "start", 500)
        s.t(150, yy, b, 12, SUB)
    s.sep(372)
    # 摘 node 的指针重连
    s.t(40, 392, "_remove(node): 2 条赋值就把 node 从 list 里摘走, 不扫描", 14, INK, "start", 500)
    ya, yb = 420, 494
    s.box(200, ya - 17, 60, 34, "a", "cur")
    s.box(320, ya - 17, 80, 34, "node", "gone")
    s.box(460, ya - 17, 60, 34, "b", "cur")
    dbl(s, 260, 320, ya)
    dbl(s, 400, 460, ya)
    s.t(40, ya, "before", 12, SUB)
    s.t(40, yb, "after", 12, SUB)
    s.box(200, yb - 17, 60, 34, "a", "cur")
    s.box(460, yb - 17, 60, 34, "b", "cur")
    dbl(s, 260, 460, yb)
    s.t(360, yb - 28, "a.next = b   (即 node.prev.next = node.next)", 12, INK, "middle")
    s.t(360, yb + 34, "b.prev = a   (即 node.next.prev = node.prev)", 12, INK, "middle")
    s.legend(562, [("ring", "LRU 端 = 下一个被踢"), ("gone", "要摘下的 node")])
    s.save("lru_core.svg")


def lru_states():
    ns = load(CODE_LRU)
    c = ns["LRUCache"](2)

    def snap():
        order, n = [], c.head.next
        while n is not c.tail:
            order.append((n.key, n.val))
            n = n.next
        return order, list(c.cache)

    steps = [("put", 1, 10), ("put", 2, 20), ("get", 1, None), ("put", 3, 30),
             ("get", 2, None), ("put", 4, 40), ("get", 3, None)]
    out = []
    for op, k, v in steps:
        before_order, before_keys = snap()
        res = None
        if op == "get":
            res = c.get(k)
        else:
            c.put(k, v)
        order, keys = snap()
        gone = [x for x in before_order if x[0] not in keys]
        out.append(dict(op=op, k=k, v=v, res=res, order=order, keys=keys, gone=gone,
                        before=before_order, size_before=len(before_keys),
                        existed=k in before_keys))
    return out


def svg_lru_trace():
    rows = lru_states()
    s = Svg(100 + len(rows) * 82 + 80, "LRU Cache trace, capacity = 2",
            "每一步之后 doubly linked list 的顺序、dict 的内容, 以及被踢掉的 node。")
    s.t(40, 18, "capacity = 2 · list 左 = LRU (最久没用), 右 = MRU (刚用过) · head / tail 是 dummy", 12)
    s.t(40, 38, "每步: dict 找 node -> 摘下 + 接到 tail 前 -> 超过 capacity 就踢 head.next", 12)
    s.t(40, 62, "操作", 12)
    s.t(240, 62, "list (这一步之后)", 12)
    s.t(520, 62, "dict: key -> node", 12)
    s.sep(72)
    y0 = 80
    for r in rows:
        yc = y0 + 26
        op = "put(%d, %d)" % (r["k"], r["v"]) if r["op"] == "put" else "get(%d)" % r["k"]
        s.t(40, yc - 8, op, 14, INK, "start", 500)
        if r["op"] == "get":
            s.t(40, yc + 12, "-> %d" % r["res"], 12, SUB)
        # 被踢的 node: 虚线扔到左边
        if r["gone"]:
            gk, gv = r["gone"][0]
            s.box(150, yc - 15, 60, 30, "%d:%d" % (gk, gv), "gone", dashed=True)
            s.line(238, yc, 214, yc, "#D85A30", dashed=True)
        # list
        x = 240
        s.box(x, yc - 15, 40, 30, "head", "none", size=12)
        px = x + 40
        touched = r["k"] if (r["op"] == "put" or not r["res"] == -1) else None
        first = True
        for (k, v) in r["order"]:
            x = px + 20
            dbl(s, px, x, yc)
            role = "new" if k == touched else "cur"
            s.box(x, yc - 15, 60, 30, "%d:%d" % (k, v), role)
            if first:
                s.ring(x, yc - 15, 60, 30)
                first = False
            px = x + 60
        x = px + 20
        dbl(s, px, x, yc)
        s.box(x, yc - 15, 40, 30, "tail", "none", size=12)
        # dict
        dx = 520
        for k in r["keys"]:
            role = "new" if k == touched else "cur"
            s.box(dx, yc - 15, 46, 30, "%d" % k, role)
            dx += 54
        # 说明
        if r["op"] == "get" and r["res"] == -1:
            why = "key %d 不在 dict -> return -1, list 不动" % r["k"]
        elif r["op"] == "get":
            why = "dict[%d] 找到 node -> 摘下 -> 接到 tail 前 (变成 MRU)" % r["k"]
        elif r["existed"]:
            why = "key %d 已存在 -> 更新 val, 摘下再接到 tail 前" % r["k"]
        elif r["gone"]:
            why = ("size = %d + 1 = %d > capacity = 2 -> 踢 head.next = key %d, del dict[%d]"
                   % (r["size_before"], r["size_before"] + 1, r["gone"][0][0], r["gone"][0][0]))
        else:
            why = "新 node 接到 tail 前; size = %d ≤ capacity = 2, 不用踢" % (r["size_before"] + 1)
        s.t(240, yc + 38, why, 12, "#712B13" if r["gone"] else SUB)
        s.sep(y0 + 80)
        y0 += 82
    last = rows[-1]
    final = " ⇄ ".join("%d:%d" % kv for kv in last["order"])
    s.t(40, y0 + 14, "最终: head ⇄ %s ⇄ tail · dict = {%s} · key 2 和 key 1 先后被踢"
        % (final, ", ".join(str(k) for k in last["keys"])), 14, INK, "start", 500)
    s.legend(y0 + 44, [("new", "新进来 / 刚用过 (MRU)"), ("gone-d", "被踢出"),
                       ("ring", "LRU 端 = 下一个被踢"), ("cur", "其他")])
    s.save("lru_trace.svg")


# ----------------------------------------------------------------------------
# 5. GetRandom: core + trace
# ----------------------------------------------------------------------------
def svg_rs_core():
    s = Svg(486, "swap-pop: 把要删的换到末尾再 pop",
            "list 只有删末尾是 O(1); 所以先把末尾元素搬到要删的位置, 再 pop 尾巴。")
    s.t(40, 18, "要求: insert / remove / getRandom 全 O(1) · getRandom 要 list 按 index 取 · 找 val 要 dict", 12)
    s.t(40, 38, "list 的软肋是删中间。但 set 本来就没有顺序 -> 允许把顺序打乱 -> 删中间变成删末尾", 12)
    vals = [5, 7, 9, 4]
    bx, bw, gap = 150, 54, 8

    def arr(y, items, roles, idx=True):
        for i, (v, r) in enumerate(zip(items, roles)):
            x = bx + i * (bw + gap)
            if v is None:
                continue
            s.box(x, y, bw, 34, str(v), r)
            if idx:
                s.t(x + bw / 2, y + 48, "idx %d" % i, 12, SUB, "middle")

    # 上: 暴力
    s.t(40, 70, "暴力: 删 7 = pop(1)", 14, INK, "start", 500)
    s.t(40, 90, "后面的全部左移一格 -> O(n)", 12, SUB)
    arr(110, vals, ["cur", "gone", "cur", "cur"])
    s.t(40, 127, "before", 12, SUB)
    arr(190, [5, 9, 4, None], ["cur", "new", "new", "cur"], idx=False)
    s.t(40, 207, "after", 12, SUB)
    s.line(bx + 2 * (bw + gap) + bw / 2 - 10, 146, bx + (bw + gap) + bw / 2 - 10, 188, "#D85A30")
    s.line(bx + 3 * (bw + gap) + bw / 2 - 10, 146, bx + 2 * (bw + gap) + bw / 2 - 10, 188, "#D85A30")
    s.t(bx + 4 * (bw + gap) + 8, 170, "9, 4 各左移一格: 最坏搬 n - 1 个", 12, "#712B13")
    s.sep(246)
    # 下: swap-pop
    s.t(40, 270, "swap-pop: 删 7", 14, INK, "start", 500)
    s.t(40, 290, "末尾 4 搬到 idx 1, pop 尾巴 -> O(1)", 12, SUB)
    arr(330, vals, ["cur", "gone", "cur", "new"])
    s.t(40, 347, "before", 12, SUB)
    xl = bx + 3 * (bw + gap) + bw / 2
    xi = bx + (bw + gap) + bw / 2
    s.path("M %s 328 L %s 308 L %s 308 L %s 326" % (xl, xl, xi, xi))
    s.t((xl + xi) / 2, 297, "① nums[1] = last = 4", 12, INK, "middle")
    arr(410, [5, 4, 9, 4], ["cur", "new", "cur", "gone"], idx=False)
    s.box(bx + 3 * (bw + gap), 410, bw, 34, "4", "gone", dashed=True)
    s.t(40, 427, "after", 12, SUB)
    s.t(bx + 4 * (bw + gap) + 8, 420, "② nums.pop() 去掉尾巴", 12, "#712B13")
    s.t(bx + 4 * (bw + gap) + 8, 440, "③ pos[4] = 1 · del pos[7]", 12, INK)
    s.legend(470, [("new", "被搬动 / 位置变了"), ("gone", "被删除"), ("cur", "没动")])
    s.save("getrandom_core.svg")


def rs_states():
    ns = load(CODE_RS)
    r = ns["RandomizedSet"]()
    steps = [("insert", 5), ("insert", 7), ("insert", 9), ("remove", 5),
             ("insert", 4), ("remove", 7)]
    out = []
    for op, v in steps:
        before = list(r.nums)
        res = getattr(r, op)(v)
        i = before.index(v) if op == "remove" else None
        out.append(dict(op=op, v=v, res=res, before=before, idx=i,
                        nums=list(r.nums), pos=dict(r.pos)))
    return out


def svg_rs_trace():
    rows = rs_states()
    rh = 106
    s = Svg(100 + (len(rows) + 1) * rh + 70, "RandomizedSet trace",
            "每一步之后 nums 和 pos 的内容, 删除时被删值虚线扔到左边。")
    s.t(40, 18, "nums = list (按 index 取 random) · pos = dict, val -> 它在 nums 里的 index", 12)
    s.t(40, 38, "remove: 末尾元素搬到被删位置 -> 更新 pos[末尾元素] -> pop 尾巴 -> del pos[被删值]", 12)
    s.t(40, 62, "操作", 12)
    s.t(240, 62, "nums (这一步之后)", 12)
    s.t(440, 62, "pos: val -> idx", 12)
    s.sep(72)
    y0 = 80
    for r in rows:
        yc = y0 + 24
        s.t(40, yc - 6, "%s(%d)" % (r["op"], r["v"]), 14, INK, "start", 500)
        s.t(40, yc + 14, "-> True", 12, SUB)
        moved = None
        if r["op"] == "remove":
            s.box(150, yc - 15, 46, 30, str(r["v"]), "gone", dashed=True)
            s.line(236, yc, 200, yc, "#D85A30", dashed=True)
            if r["idx"] < len(r["nums"]):
                moved = r["idx"]
        for i, v in enumerate(r["nums"]):
            x = 240 + i * 48
            role = "new" if (r["op"] == "insert" and i == len(r["nums"]) - 1) or i == moved else "cur"
            s.box(x, yc - 15, 42, 30, str(v), role)
            s.t(x + 21, yc + 27, str(i), 12, SUB, "middle")
        px = 440
        for v, i in r["pos"].items():
            role = "new" if (r["op"] == "insert" and v == r["v"]) or i == moved else "cur"
            s.box(px, yc - 15, 62, 30, "%d→%d" % (v, i), role)
            px += 68
        if r["op"] == "insert":
            why = "pos[%d] = len(nums) = %d, 再 append" % (r["v"], len(r["nums"]) - 1)
            s.t(240, yc + 44, why, 12)
        else:
            i, last = r["idx"], r["before"][-1]
            if last == r["v"]:
                s.t(240, yc + 44, "%d 就在末尾 (idx %d): 不用搬, 直接 pop + del pos[%d]"
                    % (r["v"], i, r["v"]), 12, "#712B13")
            else:
                s.t(240, yc + 44, "pos[%d] = %d · 末尾 %d 搬到 idx %d · pos[%d] = %d"
                    % (r["v"], i, last, i, last, i), 12, "#712B13")
                s.t(240, yc + 60, "nums.pop() 去掉尾巴 · del pos[%d]" % r["v"], 12, "#712B13")
        s.sep(y0 + rh - 4)
        y0 += rh
    # getRandom
    yc = y0 + 24
    last = rows[-1]
    s.t(40, yc - 6, "getRandom()", 14, INK, "start", 500)
    s.t(40, yc + 14, "-> 例如 4", 12, SUB)
    for i, v in enumerate(last["nums"]):
        x = 240 + i * 48
        s.box(x, yc - 15, 42, 30, str(v), "cur")
        s.t(x + 21, yc + 24, str(i), 12, SUB, "middle")
    s.ring(240 + 48, yc - 15, 42, 30)
    s.t(240, yc + 44, "random.choice(nums): 每个 idx 概率都是 1 / %d" % len(last["nums"]), 12)
    y0 += rh
    s.t(40, y0 + 4, "最终: nums = %s · pos = %s" % (last["nums"], "{" + ", ".join(
        "%d: %d" % kv for kv in last["pos"].items()) + "}"), 14, INK, "start", 500)
    s.legend(y0 + 34, [("new", "新插入 / 被搬动"), ("gone-d", "被删除"), ("ring", "被抽中"), ("cur", "没动")])
    s.save("getrandom_trace.svg")


# ----------------------------------------------------------------------------
# 6. TimeMap: core + trace
# ----------------------------------------------------------------------------
def svg_tm_core():
    s = Svg(470, "Time Based KV: append 天然有序, 用 bisect 找 <= t",
            "每个 key 一条按时间递增的记录; get(t) 返回最后一个 timestamp <= t 的记录。")
    s.t(40, 18, "set 的 timestamp 严格递增 -> 每个 key 的 list 本来就是有序的 -> 不用 sort, 不用 heap", 12)
    s.t(40, 38, "get(key, t) = 在有序 list 里找 '最后一个 <= t' = bisect_right(times, t) - 1", 12)
    ax = lambda t: 70 + t * 54
    ya = 150
    s.line(50, ya, 630, ya, head=True, width=1.5)
    s.t(40, ya - 44, "times", 12, SUB)
    for t, v in [(1, "a"), (4, "b"), (7, "c")]:
        s.box(ax(t) - 25, ya - 62, 50, 36, v, "cur", sub="t=%d" % t)
        s.line(ax(t), ya - 26, ax(t), ya, SUB, head=False, width=1)
    for t in range(0, 11):
        s.o.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#B4B2A9" stroke-width="1"/>'
                   % (ax(t), ya - 4, ax(t), ya + 4))
        s.t(ax(t), ya + 16, str(t), 12, SUB, "middle")
    s.t(640, ya + 16, "t", 12, SUB, "end")
    # 段: 每个 query 落在哪一段
    yb = 200
    segs = [(0, 1, "''", "gone"), (1, 4, "a", "new"), (4, 7, "b", "new"), (7, 10.4, "c", "new")]
    for a, b, lab, role in segs:
        s.box(ax(a), yb, ax(b) - ax(a) - 3, 32, lab, role)
    s.t(40, yb + 16, "返回", 12, SUB)
    s.t(40, yb + 52, "t 落在哪一段 -> 返回这一段左端点那条记录的 value (t=4 正好踩在 b 的左端点 -> b)", 12)
    s.sep(284)
    s.t(40, 304, "get(k, t)", 12, INK, "start", 500)
    s.t(150, 304, "bisect_right(times, t)", 12, INK, "start", 500)
    s.t(350, 304, "- 1 = idx", 12, INK, "start", 500)
    s.t(470, 304, "返回", 12, INK, "start", 500)
    qs = [0, 3, 4, 9]
    times, vals = [1, 4, 7], ["a", "b", "c"]
    from bisect import bisect_right
    for i, t in enumerate(qs):
        y = 330 + i * 26
        p = bisect_right(times, t)
        s.t(40, y, "t = %d" % t, 12, SUB)
        s.t(150, y, "bisect_right([1, 4, 7], %d) = %d" % (t, p), 12, SUB)
        s.t(350, y, "%d - 1 = %d" % (p, p - 1), 12, SUB)
        s.t(470, y, "vals[%d] = %s" % (p - 1, vals[p - 1]) if p else "idx = -1 -> ''", 12, INK)
    s.legend(s.h - 14, [("new", "该段返回的记录"), ("gone", "还没有记录"), ("cur", "已 set 的记录")])
    s.save("timemap_core.svg")


def svg_tm_trace():
    ns = load(CODE_TM)
    t = ns["TimeMap"]()
    bisect_right = ns["bisect_right"]
    steps = [("set", "a", 1), ("set", "b", 4), ("set", "c", 7),
             ("get", None, 3), ("get", None, 4), ("get", None, 0), ("get", None, 9)]
    rh = 76
    s = Svg(110 + len(steps) * rh + 70, "TimeMap trace, key = 'k'",
            "每次 set 之后 list 的内容; 每次 get 用 bisect_right 找到的 idx。")
    s.t(40, 18, "key = 'k' · times[k] 和 vals[k] 同一个 idx · 每个格子: 上 = value, 下 = timestamp", 12)
    s.t(40, 38, "set: 两个 list 各 append 一个 (时间递增 -> 仍然有序) · get: bisect_right(times, t) - 1", 12)
    s.t(40, 62, "操作", 12)
    s.t(200, 62, "times[k] / vals[k] (这一步之后)", 12)
    s.t(430, 62, "计算", 12)
    s.sep(72)
    y0 = 80
    for op, v, tt in steps:
        yc = y0 + 28
        if op == "set":
            t.set("k", v, tt)
            s.t(40, yc - 6, "set('k','%s',%d)" % (v, tt), 14, INK, "start", 500)
        else:
            res = t.get("k", tt)
            s.t(40, yc - 6, "get('k', %d)" % tt, 14, INK, "start", 500)
            s.t(40, yc + 14, "-> '%s'" % res, 12, SUB)
        ts, vs = t.times["k"], t.vals["k"]
        pick = bisect_right(ts, tt) - 1 if op == "get" else None
        for i, (a, b) in enumerate(zip(ts, vs)):
            x = 200 + i * 60
            role = "new" if (op == "set" and i == len(ts) - 1) else "cur"
            s.box(x, yc - 20, 54, 40, b, role, sub="t=%d" % a)
            s.t(x + 27, yc + 30, "idx %d" % i, 12, SUB, "middle")
            if pick == i:
                s.ring(x, yc - 20, 54, 40)
        if op == "set":
            s.t(430, yc - 6, "times.append(%d) · vals.append('%s')" % (tt, v), 12)
            s.t(430, yc + 14, "%d 比前面都大 -> 仍然有序" % tt if len(ts) > 1 else "第一条记录", 12)
        else:
            p = bisect_right(ts, tt)
            s.t(430, yc - 12, "bisect_right(%s, %d) = %d" % (ts, tt, p), 12)
            if p:
                s.t(430, yc + 6, "idx = %d - 1 = %d -> vals[%d] = '%s'" % (p, p - 1, p - 1, vs[p - 1]), 12, INK)
            else:
                s.t(430, yc + 6, "idx = 0 - 1 = -1 -> 没有 <= %d 的记录" % tt, 12, INK)
                s.t(430, yc + 24, "return ''", 12, INK)
        s.sep(y0 + rh - 4)
        y0 += rh
    s.t(40, y0 + 6, "最终: times['k'] = [1, 4, 7] · vals['k'] = ['a', 'b', 'c'] · 每个 get 只做一次 bisect", 14, INK, "start", 500)
    s.legend(y0 + 36, [("new", "新 append 的记录"), ("ring", "bisect 选中的记录"), ("cur", "已有记录")])
    s.save("timemap_trace.svg")


# ----------------------------------------------------------------------------
# 7. HitCounter: core + trace
# ----------------------------------------------------------------------------
def svg_hc_core():
    s = Svg(380, "Hit Counter: 过期的一定在 deque 最左边",
            "时间戳只增不减, 所以 deque 左边最旧; 过期时从左边 popleft, 每个时间戳最多出队一次。")
    s.t(40, 18, "getHits(now) 只数 (now - 300, now] 内的 hit · 时间戳按到达顺序入队 -> deque 本身有序", 12)
    s.t(40, 38, "过期的 = 最旧的 = 一定连续地排在最左边 -> 从左边一个个 popleft 到不过期为止", 12)
    s.t(40, 66, "getHits(301): cutoff = 301 - 300 = 1 · 规则: q[0] <= cutoff 就过期", 14, INK, "start", 500)
    xs = [1, 2, 3, 300]
    x0, w = 150, 60
    s.t(40, 120, "q (左 = 最旧)", 12)
    for i, v in enumerate(xs):
        role = "gone" if v <= 1 else "cur"
        s.box(x0 + i * (w + 10), 100, w, 40, str(v), role, dashed=(v <= 1))
    # cutoff 线
    cx = x0 + w + 5
    s.o.append('<line x1="%s" y1="86" x2="%s" y2="156" stroke="#D85A30" stroke-width="1.5" stroke-dasharray="5 4"/>' % (cx, cx))
    s.t(cx + 6, 92, "cutoff = 1", 12, "#712B13")
    s.t(x0, 168, "1 <= 1 过期", 12, "#712B13")
    s.t(x0 + (w + 10), 168, "2 > 1 之后全部有效", 12, SUB)
    s.sep(190)
    s.t(40, 214, "popleft 后", 14, INK, "start", 500)
    s.box(40, 230, 70, 40, "1", "gone", dashed=True)
    s.line(146, 250, 114, 250, "#D85A30", dashed=True)
    for i, v in enumerate(xs[1:]):
        s.box(150 + i * (w + 10), 230, w, 40, str(v), "cur")
    s.t(150 + 3 * (w + 10) + 6, 250, "len(q) = 3 = 答案", 14, INK, "start", 500)
    s.sep(292)
    s.t(40, 312, "为什么是 O(1) amortized: 每个时间戳 append 一次、popleft 最多一次 -> n 次操作总共 O(n)", 12)
    s.t(40, 330, "不用 sorted / heap: 到达顺序 = 时间顺序, 数据本来就有序", 12)
    s.legend(364, [("gone-d", "过期, 出队"), ("cur", "窗口内的 hit")])
    s.save("hitcounter_core.svg")


def svg_hc_trace():
    ns = load(CODE_HC)
    h = ns["HitCounter"]()
    steps = [("hit", 1), ("hit", 2), ("hit", 3), ("get", 4), ("hit", 300), ("get", 301), ("get", 303)]
    rh = 74
    s = Svg(100 + len(steps) * rh + 80, "HitCounter trace, window = 300",
            "deque 里的时间戳每步的变化; 过期的从左边 popleft, 虚线扔到左边。")
    s.t(40, 18, "窗口 (now - 300, now] · q 左 = 最旧 · hit: 从右边 append · getHits: 从左边 popleft 过期的", 12)
    s.t(40, 38, "过期规则: q[0] <= cutoff, cutoff = now - 300", 12)
    s.t(40, 62, "操作", 12)
    s.t(250, 62, "q (这一步之后)", 12)
    s.t(470, 62, "计算", 12)
    s.sep(72)
    y0 = 80
    for op, ts in steps:
        yc = y0 + 26
        before = list(h.q)
        if op == "hit":
            h.hit(ts)
            s.t(40, yc - 6, "hit(%d)" % ts, 14, INK, "start", 500)
            popped = []
        else:
            res = h.getHits(ts)
            popped = before[:len(before) - len(h.q)]
            s.t(40, yc - 6, "getHits(%d)" % ts, 14, INK, "start", 500)
            s.t(40, yc + 14, "-> %d" % res, 12, SUB)
        for i, g in enumerate(popped):
            s.box(140 + i * 40, yc - 15, 34, 30, str(g), "gone", dashed=True, size=12)
        if popped:
            s.line(246, yc, 140 + (len(popped) - 1) * 40 + 38, yc, "#D85A30", dashed=True)
        for i, v in enumerate(h.q):
            role = "new" if (op == "hit" and i == len(h.q) - 1) else "cur"
            s.box(250 + i * 46, yc - 15, 40, 30, str(v), role)
        if op == "hit":
            s.t(470, yc, "append(%d) 到右边" % ts, 12)
        else:
            cut = ts - 300
            s.t(470, yc - 14, "cutoff = %d - 300 = %d" % (ts, cut), 12)
            if popped:
                s.t(470, yc + 4, "popleft: " + ", ".join("%d <= %d" % (g, cut) for g in popped), 12, "#712B13")
            else:
                s.t(470, yc + 4, "q[0] = %d > %d, 不用出队" % (before[0], cut), 12)
            s.t(470, yc + 22, "len(q) = %d" % len(h.q), 12, INK)
        s.sep(y0 + rh - 4)
        y0 += rh
    s.t(40, y0 + 8, "最终: q = %s · 1、2、3 都过期被 popleft · 300 仍在窗口里" % list(h.q), 14, INK, "start", 500)
    s.legend(y0 + 38, [("new", "新 append"), ("gone-d", "过期, popleft"), ("cur", "窗口内")])
    s.save("hitcounter_trace.svg")


# ----------------------------------------------------------------------------
# 8. SnapshotArray: core + trace
# ----------------------------------------------------------------------------
def svg_snap_core():
    s = Svg(456, "Snapshot Array: 只记录变化, 用 bisect 回溯",
            "暴力每次 snap 复制整个数组; 只记录 set 的变化, 再用 bisect 找到最近的一次变化。")
    s.t(40, 18, "例子: length = 3 · set(0,5) · snap() · set(0,6) · set(2,8) · snap() · 每格 = index i 在 snap s 时的值", 12)
    s.t(40, 38, "snap() 要 O(1): 不能复制数组 · get(i, s) 要 O(log): 在 i 自己的变化记录里 bisect", 12)
    cols = [("snap 0", 0), ("snap 1", 1)]
    full = [[5, 6], [0, 0], [0, 8]]
    stored = [[True, True], [True, False], [True, True]]

    def grid(x0, title, cells, mode):
        s.t(x0, 70, title, 14, INK, "start", 500)
        for j, (cn, _) in enumerate(cols):
            s.t(x0 + 70 + j * 70 + 31, 96, cn, 12, SUB, "middle")
        for i in range(3):
            y = 110 + i * 42
            s.t(x0, y + 17, "idx %d" % i, 12, SUB)
            for j in range(2):
                x = x0 + 70 + j * 70
                if mode == "full":
                    s.box(x, y, 62, 34, str(full[i][j]), "cur")
                elif stored[i][j]:
                    s.box(x, y, 62, 34, str(full[i][j]), "new", sub=None)
                else:
                    s.box(x, y, 62, 34, "同左", "none", dashed=True, size=12)

    grid(40, "暴力: 每次 snap 复制全部", None, "full")
    grid(350, "只存变化 hist[i]", None, "sparse")
    s.t(40, 250, "存 6 格 (= n x 次数)", 12, SUB)
    s.t(350, 250, "存 5 格 (每 index 一个初值 (0,0) + 每次 set 一条)", 12, SUB)
    s.t(40, 270, "snap() = O(n) 复制", 12, "#712B13")
    s.t(350, 270, "snap() = O(1) 只 snap_id += 1", 12, "#085041")
    s.sep(292)
    s.t(40, 312, "hist[i] = [(snap_id, val), ...] · snap_id 只增 -> 每个 hist[i] 天然有序", 14, INK, "start", 500)
    hist = [[(0, 5), (1, 6)], [(0, 0)], [(0, 0), (1, 8)]]
    for i, hh in enumerate(hist):
        y = 330 + i * 28
        s.t(40, y + 10, "hist[%d]" % i, 12, SUB)
        for j, (a, b) in enumerate(hh):
            s.box(110 + j * 90, y, 80, 22, "(%d, %d)" % (a, b), "new" if stored[i][j] and (i, j) != (1, 0) and not (i == 2 and j == 0) else "cur", size=12)
    s.t(310, 344, "get(0, 1): bisect_right(hist[0], (1, inf)) - 1 = 2 - 1 = 1 -> val 6", 12, INK)
    s.t(310, 372, "get(2, 0): bisect_right(hist[2], (0, inf)) - 1 = 1 - 1 = 0 -> val 0", 12, INK)
    s.t(310, 400, "(snap_id, inf): 让 snap_id 相同的记录排在它左边", 12, SUB)
    s.legend(440, [("new", "有记录"), ("none", "没记录, 沿用左边"), ("cur", "初值 / 复制出来的")])
    s.save("snapshot_core.svg")


def svg_snap_trace():
    ns = load(CODE_SNAP)
    sa = ns["SnapshotArray"](3)
    bisect_right = ns["bisect_right"]
    steps = [("set", 0, 5), ("snap", None, None), ("set", 0, 6), ("set", 2, 8),
             ("get", 0, 0), ("snap", None, None), ("get", 0, 1), ("get", 2, 0)]
    rh = 72
    s = Svg(110 + len(steps) * rh + 70, "SnapshotArray trace, length = 3",
            "每一步之后 snap_id 和三个 index 的 hist。")
    s.t(40, 18, "hist[i] = [(snap_id, val), ...] · 每格 (snap_id, val) · snap_id = 下一次 snap() 要返回的编号", 12)
    s.t(40, 38, "set: 本版本已有记录就覆盖, 否则 append · snap: snap_id += 1 · get: bisect_right - 1", 12)
    cx = [150, 214, 340, 466]
    s.t(40, 62, "操作", 12)
    s.t(cx[0], 62, "snap_id", 12)
    s.t(cx[1], 62, "hist[0]", 12)
    s.t(cx[2], 62, "hist[1]", 12)
    s.t(cx[3], 62, "hist[2]", 12)
    s.sep(72)
    y0 = 80
    prev = [list(h) for h in sa.hist]
    for op, i, v in steps:
        yc = y0 + 22
        note = None
        if op == "set":
            sa.set(i, v)
            label = "set(%d, %d)" % (i, v)
            note = "hist[%d] 里还没有 snap_id = %d 的记录 -> append (%d, %d)" % (i, sa.snap_id, sa.snap_id, v)
            if prev[i][-1][0] == sa.snap_id:
                note = "hist[%d] 已有 snap_id = %d 的记录 -> 覆盖成 (%d, %d)" % (i, sa.snap_id, sa.snap_id, v)
        elif op == "snap":
            r = sa.snap()
            label = "snap()"
            s.t(40, yc + 14, "-> %d" % r, 12, SUB)
            note = "只做 snap_id += 1 = %d, 没有复制任何东西" % sa.snap_id
        else:
            r = sa.get(i, v)
            label = "get(%d, %d)" % (i, v)
            s.t(40, yc + 14, "-> %d" % r, 12, SUB)
            h = sa.hist[i]
            p = bisect_right(h, (v, float("inf")))
            note = "bisect_right(hist[%d], (%d, inf)) = %d -> idx %d -> val %d" % (i, v, p, p - 1, h[p - 1][1])
        s.t(40, yc - 6, label, 14, INK, "start", 500)
        s.box(cx[0], yc - 14, 32, 28, str(sa.snap_id), "new" if op == "snap" else "cur")
        for k in range(3):
            for j, (a, b) in enumerate(sa.hist[k]):
                changed = j >= len(prev[k]) or prev[k][j] != (a, b)
                role = "new" if (changed and op == "set" and k == i) else "cur"
                x = cx[k + 1] + j * 62
                s.box(x, yc - 14, 56, 28, "%d,%d" % (a, b), role, size=12)
                if op == "get" and k == i and j == p - 1:
                    s.ring(x, yc - 14, 56, 28)
        s.t(cx[0], yc + 30, note, 12, SUB)
        prev = [list(h) for h in sa.hist]
        s.sep(y0 + rh - 4)
        y0 += rh
    s.t(40, y0 + 6, "最终: hist = %s" % sa.hist, 12, INK, "start", 500)
    s.legend(y0 + 34, [("new", "新写入 / 刚 snap"), ("ring", "bisect 选中"), ("cur", "已有记录")])
    s.save("snapshot_trace.svg")


# ----------------------------------------------------------------------------
# 9. LFU: 结构图
# ----------------------------------------------------------------------------
def svg_lfu_core():
    ns = load(CODE_LFU)
    c = ns["LFUCache"](4)
    for k, v in [("a", 1), ("b", 2), ("c", 3), ("d", 4)]:
        c.put(k, v)
    c.get("a")
    c.get("a")
    c.get("b")
    before = dict(val=dict(c.val), freq=dict(c.freq),
                  bucket={f: list(b) for f, b in c.bucket.items()}, mf=c.min_freq)
    c.put("e", 5)
    after = dict(val=dict(c.val), freq=dict(c.freq),
                 bucket={f: list(b) for f, b in c.bucket.items()}, mf=c.min_freq)
    assert before["bucket"] == {1: ["c", "d"], 2: ["b"], 3: ["a"]} and before["mf"] == 1
    assert after["bucket"] == {1: ["d", "e"], 2: ["b"], 3: ["a"]}
    s = Svg(486, "LFU Cache 的结构: LRU 按 freq 分层",
            "key -> (val, freq), freq -> OrderedDict(key), 以及 min_freq。")
    s.t(40, 18, "要求: get / put 都 O(1) · 踢 '访问次数最少' 的, 并列时踢 '最久没用' 的", 12)
    s.t(40, 38, "= LRU 再加一层: 每个 freq 一个 LRU 桶 (OrderedDict), min_freq 指向最低的非空桶", 12)
    s.t(40, 66, "put(e, 5) 之后的状态 (capacity = 4 已满, 踢了 c)", 14, INK, "start", 500)
    # 左: key -> val, freq
    s.t(40, 98, "val / freq (两个 dict)", 12, SUB)
    keys = ["a", "b", "d", "e"]
    for i, k in enumerate(keys):
        y = 110 + i * 40
        role = "new" if k == "e" else "cur"
        s.box(40, y, 180, 32, "%s  val=%d  freq=%d" % (k, after["val"][k], after["freq"][k]), role, size=14)
    # 右: freq -> bucket
    s.t(300, 98, "bucket: freq -> OrderedDict (左 = 最久没用)", 12, SUB)
    rows = [1, 2, 3]
    for i, f in enumerate(rows):
        y = 110 + i * 50
        s.t(300, y + 16, "freq=%d" % f, 14, INK, "start", 500)
        for j, k in enumerate(after["bucket"][f]):
            role = "new" if k == "e" else "cur"
            s.box(440 + j * 52, y, 44, 32, k, role)
        if f == 1:
            s.box(376, y, 44, 32, "c", "gone", dashed=True)
            s.line(436, y + 16, 424, y + 16, "#D85A30", dashed=True)
    s.ring(440, 110, 44, 32)
    s.t(300, 270, "min_freq = %d" % after["mf"], 14, INK, "start", 500)
    s.t(300, 290, "-> 桶 1 的最左边 (金圈) = 下一个被踢的", 12, SUB)
    s.t(40, 290, "key 同时在 3 个地方: val · freq · bucket[freq]", 12, SUB)
    s.t(40, 308, "每次 mutate 三处一起改 (同步)", 12, SUB)
    s.sep(322)
    s.t(40, 342, "get(k) / put 已有 key  ->  _touch(k)", 14, INK, "start", 500)
    s.t(40, 364, "1. f = freq[k] · del bucket[f][k]", 12, INK)
    s.t(40, 382, "2. bucket[f] 空了, 且 f == min_freq -> min_freq += 1  (k 马上去 f+1, 所以正好 +1)", 12, INK)
    s.t(40, 400, "3. freq[k] = f + 1 · bucket[f + 1][k] = None  (接到右边 = 这一层最新)", 12, INK)
    s.t(40, 422, "put 新 key 且满了: bucket[min_freq].popitem(last=False) = c  (频率最低 + 最久没用)", 12, "#712B13")
    s.t(40, 440, "然后 val[e] = 5 · freq[e] = 1 · bucket[1][e] = None · min_freq = 1", 12, INK)
    s.legend(470, [("new", "新进来"), ("gone-d", "被踢出 (c: freq=1, 桶 1 最左)"), ("ring", "下一个被踢"), ("cur", "其他")])
    s.save("lfu_core.svg")


def make_svgs():
    svg_matrix()
    svg_lru_core()
    svg_lru_trace()
    svg_rs_core()
    svg_rs_trace()
    svg_tm_core()
    svg_tm_trace()
    svg_hc_core()
    svg_hc_trace()
    svg_snap_core()
    svg_snap_trace()
    svg_lfu_core()


make_svgs()

# ----------------------------------------------------------------------------
# 10. 文档
# ----------------------------------------------------------------------------
import re as _re


def _tight(src):
    # 去掉行内注释前面的对齐空格, 避免长注释行横向溢出
    return "\n".join(_re.sub(r"(\S)\s{2,}#", r"\1  #", l) for l in src.split("\n"))


doc = d.Doc("17 · Data Structure Design")
_code = doc.code
doc.code = lambda src: _code(_tight(src))
doc.main("主线: design 题 = 先列出每个操作要求的 complexity, 再把 "
         "'擅长这个操作' 的数据结构组合起来, 并保证它们永远描述同一批元素 (同步)。")
doc.main("概念链: 第一性原理 → LRU Cache (dict + DLL) → GetRandom (dict + list, swap-pop) → "
         "Time Based KV (dict + sorted list + bisect) → Hit Counter / Logger (deque / dict) → "
         "Snapshot Array (只记变化 + bisect) → LFU Cache (LRU 的分层版)")

# ---- 0
doc.h2("0. 第一性原理: 没有一个结构什么都快, 所以要组合")
doc.p("Design 题给你一组 API, 每个都要求 O(1) 或 O(log n)。面试里它在考的不是某个技巧, 而是一个固定的推理流程:")
doc.p("① 把每个操作要求的 complexity 写出来 · ② 对每个操作问: 哪个结构能在这个 complexity 内做它 · "
      "③ 没有一个结构能全包 → 组合两个, 每个操作交给擅长它的那个 · ④ 想清楚两个结构之间的 <b>同步 invariant</b> (一边改了另一边必须跟着改)。")
doc.p("Brute force 是什么: 只用一个 list (或一个 dict) 硬做。浪费在哪里:")
doc.p("• 只用 list: 按 key 找要 O(n) 扫描, 删中间要 O(n) 搬动。 • 只用 dict: 没有'最旧 / 第 i 个 / ≤ t 的最近'这类顺序信息。"
      "每个结构单独都有它做不到的操作。")
doc.svg("17-design/first_principles_core.svg",
        "图 0: 操作 × 数据结构。绿 = 能 O(1) / O(log n), 红 = 只能 O(n)。下面四行是常见组合。")
doc.p("所以 design 题的本质是<b>分工</b>: 把操作按'需要什么能力'分类, 每类交给一个结构。"
      "组合之后新增的负担只有一个: 同步。每次 mutate (增 / 删 / 移动) 都要检查'另一个结构改了没有', 绝大多数 bug 出在这里。")
doc.code(CODE_TEMPLATE)
doc.note("先写出每个操作要的 complexity, 再用图 0 选结构。组合 = 分工 + 同步。同步 invariant 要能用一句话说出来。")

# ---- 1 LRU
doc.h2("1. LRU Cache: dict 按 key 找 node, doubly linked list 管新旧")
doc.p("题目: <code>get(key)</code> 返回值 (没有返回 -1); <code>put(key, val)</code> 写入, 超过 capacity 就踢掉<b>最久没用</b>的。"
      "get 和 put 都要 O(1)。例: capacity = 2, put(1,10), put(2,20), get(1), put(3,30) → 踢掉 key 2。")
doc.p("Brute force: 用 list 按使用顺序存 (key, val)。get 要扫描找 key O(n), 再 remove + append 也 O(n)。"
      "dict 能 O(1) 找到 key, 但它不知道谁最旧; list 知道顺序, 但按 key 找、删中间都慢。")
doc.p("关键观察: 要的三件事 ——按 key 找、把某个中间元素移到最新、删最旧—— "
      "dict 做第一件, <b>doubly linked list 做后两件</b> (只要手里有 node 指针, 摘下和接上都是 O(1))。"
      "让 dict 的 value 直接就是 node 指针, 两个结构就连起来了。")
doc.svg("17-design/lru_core.svg",
        "图 1.1: dict 负责找, list 负责顺序; 摘 node 只改两条指针。金圈 = head.next = LRU。")
doc.svg("17-design/lru_trace.svg",
        "图 1.2: capacity = 2 的 7 步。踢出的 node 虚线扔到左边, 原因写在这一行下面。")
doc.code(CODE_LRU)
doc.p("<b>Time</b> O(1): get / put 都是'一次 dict 查找 + 常数条指针赋值'。<b>Space</b> O(capacity): dict 和 list 各存 capacity 个 node (同一批对象, 不是两份数据)。")
doc.p("面试速写版: Python 的 <code>OrderedDict</code> 已经是 dict + doubly linked list。"
      "先问面试官'能不能用 OrderedDict', 能的话 10 行写完; 不能就写上面的版本。"
      "注意两个版本的对应: <code>move_to_end</code> = _remove + _add_to_tail, <code>popitem(last=False)</code> = 踢 head.next。")
doc.code(CODE_LRU_OD)
doc.note("LRU = dict(key→node) + doubly linked list(左 LRU 右 MRU)。用了就摘下接到右边, 满了踢 head.next, 同时 del dict。node 里存 key, 用 dummy head/tail。")

# ---- 2 GetRandom
doc.h2("2. Insert Delete GetRandom O(1): dict 找位置, list 取随机, 删除 = 换到末尾再 pop")
doc.p("题目: <code>insert(val)</code>、<code>remove(val)</code>、<code>getRandom()</code> 全部 O(1), getRandom 每个元素等概率。"
      "例: insert 5, 7, 9 → remove 5 → insert 4 → remove 7。")
doc.p("Brute force: 只用 list, insert 是 append O(1), 但 remove(val) 要先找 O(n) 再搬动 O(n)。只用 set, 删除 O(1), 但 getRandom 要 O(n) 才能抽 "
      "(set 不能按 index 取)。")
doc.p("相比上一题: 又是 dict + 一个顺序结构, 但这次顺序结构是 <b>list</b>, 要的能力是'按 index O(1) 取'。"
      "list 唯一的软肋是删中间; 但 set 本来就不要求顺序, 所以可以 <b>先把末尾元素搬到要删的位置, 再 pop 尾巴</b> —— 删中间变成删末尾。"
      "代价: 搬动的元素在 list 里的 index 变了, dict 必须同步。")
doc.svg("17-design/getrandom_core.svg",
        "图 2.1: 暴力删中间要左移后面全部 (O(n)); swap-pop 只动一个元素。")
doc.svg("17-design/getrandom_trace.svg",
        "图 2.2: 6 次操作 + getRandom。remove 时被删的值虚线扔到左边, 绿色 = 被搬动 / 新插入。")
doc.code(CODE_RS)
doc.p("<b>Time</b> 三个操作都是 O(1) (dict 查找 + list 末尾操作 + 一次赋值)。<b>Space</b> O(n): nums 和 pos 各 n 项。")
doc.p("变体 (Duplicates allowed): pos 改成 <code>val → set(indices)</code>, remove 时从 set 里取任意一个 index 来换; 其余完全一样。")
doc.note("list 要 O(1) 随机取, dict 要 O(1) 找位置。删中间 = 末尾搬过来覆盖 + pop 尾巴 + 同步 pos。val == last 时 del pos 必须放在最后。")

# ---- 3 TimeMap
doc.h2("3. Time Based Key-Value Store: dict of list, append 天然有序, bisect 找 ≤ t")
doc.p("题目: <code>set(key, value, timestamp)</code> 存一条; <code>get(key, timestamp)</code> 返回该 key 在 <b>timestamp 之前 (≤)</b> 最近一次 set 的 value, 没有则 \"\"。"
      "set 的 timestamp 严格递增。")
doc.p("Brute force: 每个 key 一个 list, get 时从后往前扫, O(n)。浪费在哪里: 扫描完全没用上'记录按时间有序'这个信息。")
doc.p("关键观察: 因为 timestamp 递增, <b>append 之后 list 自动有序</b>, 不需要 sort / heap。"
      "'有序 list 里找最后一个 ≤ t' 就是 <code>bisect_right(times, t) - 1</code>, O(log n)。")
doc.svg("17-design/timemap_core.svg",
        "图 3.1: 每个 t 落在哪一段, 就返回这一段左端点的 value。")
doc.svg("17-design/timemap_trace.svg",
        "图 3.2: 3 次 set + 4 次 get (含 t=4 正好命中、t=0 没有记录、t=9 在最后一段)。")
doc.code(CODE_TM)
doc.p("<b>Time</b> set O(1); get O(log n) (n = 该 key 的记录数)。<b>Space</b> O(总 set 次数)。")
doc.p("相比上一题: dict 仍然按 key 分流, 但 value 是<b>有序 list + bisect</b>, 要的能力从'按 index 取'变成'找 ≤ t 的最近'。"
      "如果 timestamp 不保证递增, 就要用 sortedcontainers 或 insort (O(n) 插入), 面试时说明即可。")
doc.note("Time-based / 版本 / 历史查询 = dict of 有序 list + bisect_right(...) - 1。bisect_right 找 ≤ t, bisect_left 找 < t。")

# ---- 4 HitCounter / Logger
doc.h2("4. Design Hit Counter / Logger Rate Limiter: 时间窗口 = deque 左边出队")
doc.p("Hit Counter: <code>hit(timestamp)</code> 记一次, <code>getHits(timestamp)</code> 返回过去 300 秒内 (timestamp - 300, timestamp] 的 hit 数。"
      "timestamp 不减。")
doc.p("Brute force: 存所有时间戳, getHits 时全部扫一遍数 O(n), 内存还无限增长。")
doc.p("关键观察: 到达顺序就是时间顺序, 所以 <b>最旧的永远在最左边</b>; 过期的是连续的一段前缀。"
      "用 deque, getHits 时从左边 popleft 到不过期为止, 剩下的数量就是答案。每个时间戳进一次、出最多一次, 均摊 O(1)。")
doc.svg("17-design/hitcounter_core.svg",
        "图 4.1: cutoff 把 deque 分成过期前缀和有效后缀; 过期的从左边出队。")
doc.svg("17-design/hitcounter_trace.svg",
        "图 4.2: 7 步。getHits(301) 踢掉 1, getHits(303) 一次踢掉 2 和 3。")
doc.code(CODE_HC)
doc.p("<b>Time</b> hit O(1), getHits 均摊 O(1)。<b>Space</b> O(窗口内 hit 数)。"
      "若同一秒有大量 hit: 改存 <code>(timestamp, count)</code> 并维护 total, 空间降到 O(300)。")
doc.p("Logger Rate Limiter (同一条 message 10 秒内只打印一次) 是更简单的变体: 不需要窗口, 只需要'每条 message 下一次可以打印的时间', 一个 dict 就够。"
      "(如果要求内存有界, 才需要 deque + set 过期清理。)")
doc.code(CODE_LOGGER)
doc.note("滑动时间窗口 = deque(时间戳) 从右 append、从左 popleft 过期的。单 key 限流 = dict(key→下次允许时间)。")

# ---- 5 Snapshot
doc.h2("5. Snapshot Array: 不复制数组, 每个 index 只记录变化, bisect 回溯")
doc.p("题目: <code>SnapshotArray(length)</code> 初值全 0; <code>set(i, v)</code>; <code>snap()</code> 返回 snap_id (从 0 递增); "
      "<code>get(i, snap_id)</code> 返回 snap 时刻 index i 的值。例: length = 3, set(0,5), snap()=0, set(0,6), set(2,8), get(0,0)=5。")
doc.p("Brute force: snap() 复制整个数组, O(n) 时间 + O(n) 空间 / 次。snap 很多次、n 很大时炸掉。浪费在哪里: 绝大多数 index 在两次 snap 之间根本没变, 却被一遍遍复制。")
doc.p("关键观察: 只有 set 才产生新信息。给<b>每个 index 一个变化记录 [(snap_id, val)]</b>, snap() 只是 snap_id += 1; "
      "snap_id 只增, 所以每个记录 list 天然有序, get 用 bisect 找'最后一个 snap_id' ≤ 查询的 snap_id'。"
      "这和上一题是同一个 pattern: 'timestamp' 换成 'snap_id', 'key' 换成 'index'。")
doc.svg("17-design/snapshot_core.svg",
        "图 5.1: 左 = 暴力复制; 右 = 只存变化, 没变的格子沿用左边。")
doc.svg("17-design/snapshot_trace.svg",
        "图 5.2: 8 步。注意 snap() 不动任何 hist, get(2, 0) 因为初值 (0, 0) 才不会落到 -1。")
doc.code(CODE_SNAP)
doc.p("<b>Time</b> set O(1), snap O(1), get O(log s) (s = 该 index 的变化次数)。<b>Space</b> O(length + set 次数)。")
doc.note("'历史 / 版本 / 回溯' = 每个对象只记变化 [(version, val)], get 时 bisect_right(h, (v, inf)) - 1。初值放一条 (0, 0) 避免 -1。")

# ---- 6 LFU
doc.h2("6. LFU Cache: 把 LRU 按 freq 分层 (只讲结构)")
doc.p("题目: 和 LRU 一样, 但踢<b>访问次数最少</b>的; 次数相同时踢最久没用的。get / put 仍要 O(1)。")
doc.p("Brute force: 每次踢人扫描所有 key 找 (freq, 最后使用时间) 最小的, O(n); 或用 heap, 每次 get 更新 freq 要 O(log n)。")
doc.p("关键观察: freq 每次只 +1, 所以<b>key 只会从桶 f 搬到桶 f + 1</b>。每个 freq 一个 LRU 桶 (OrderedDict, 左 = 最久没用), "
      "再记一个 min_freq 指向最低的非空桶 → 踢人就是 <code>bucket[min_freq].popitem(last=False)</code>。"
      "min_freq 的维护只有两种情况: 新 key 进来 → 1; 最低桶被搬空 → +1。")
doc.svg("17-design/lfu_core.svg",
        "图 6: LFU 的三处状态 (val / freq / bucket) 和 min_freq。这里是 put(e) 踢掉 c 之后的样子; 不画完整 trace。")
doc.code(CODE_LFU)
doc.p("<b>Time</b> get / put 都是 O(1) (几次 dict / OrderedDict 操作)。<b>Space</b> O(capacity)。")
doc.note("LFU = 三个 dict(val, freq, freq→OrderedDict) + min_freq。get 一次 = key 从桶 f 搬到桶 f+1; 踢 = 最低桶最左边; 新 key 把 min_freq 重置为 1。")

# ---- 识别信号
doc.h2("7. 识别信号: 看到什么 → 试什么")
doc.raw("""<table>
<tr><th>特征</th><th>做法</th><th>complexity</th></tr>
<tr><td>get / put 要 O(1) + '最久没用' 要被踢</td><td>LRU: dict + doubly linked list (或 OrderedDict)</td><td>O(n) 扫描 → O(1)</td></tr>
<tr><td>踢 '最少使用', 并列看最久没用</td><td>LFU: freq → OrderedDict 桶 + min_freq</td><td>O(n) / O(log n) → O(1)</td></tr>
<tr><td>O(1) 随机抽 + O(1) 删除 / 插入</td><td>list + dict(val→idx), 删除 = 末尾搬过来 + pop</td><td>删除 O(n) → O(1)</td></tr>
<tr><td>按 key 存 + 查 '某时刻之前最近的'</td><td>dict of list (append 有序) + bisect_right - 1</td><td>O(n) 扫描 → O(log n)</td></tr>
<tr><td>历史版本 / snapshot / 回溯</td><td>每个对象只记变化 [(version, val)] + bisect</td><td>snap O(n) → O(1), get O(log s)</td></tr>
<tr><td>最近 N 秒 / 滑动时间窗口, 时间只增</td><td>deque 存时间戳, 左边 popleft 过期的</td><td>每次 O(n) → 均摊 O(1)</td></tr>
<tr><td>同一个 key N 秒内只允许一次</td><td>dict: key → 下次允许时间</td><td>O(1)</td></tr>
<tr><td>多个 API 的 complexity 要求互相冲突</td><td>列 '操作 × 结构' 表 → 组合两个 → 写同步 invariant</td><td>把每个操作的瓶颈降到所需阶</td></tr>
<tr><td>面试时 O(1) 要求还没满足</td><td>问自己: 缺的是 '按 key 找' (dict)、'顺序 / 最旧' (DLL / deque)、'按 index' (list)、'≤ t' (bisect) 哪一个?</td><td>—</td></tr>
</table>""")
doc.h2("以后再学")
doc.p("Min Stack / Max Frequency Stack (见 06); Design Twitter / Leaderboard (heap + dict); Trie 类 design (Autocomplete, File System); "
      "Circular Queue / Memory Allocator (数组模拟, 没有通用 pattern); Skiplist 与线程安全的 LRU (只在系统设计追问时出现)。")

doc.write("docs/17-design.html")
