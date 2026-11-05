"""08 · Linked List —— 生成 docs/08-linked-list.html 和 docs/svg/08-linked-list/*.svg
运行: cd build && python3 -I 08_linked_list.py
trace 图里每一步的状态都来自下面 sim_* 函数的真实运行, 并和题解函数的结果 assert。
"""
import html
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import doclib as d  # noqa: E402
import nclib as nc  # noqa: E402
from counts import cnt  # noqa: E402

SLUG = "08-linked-list"
SVG_DIR = os.path.join(d.ROOT, "docs", "svg", SLUG)
os.makedirs(SVG_DIR, exist_ok=True)

# ============================================================ 代码 (文档里展示, 同时 exec 出来测试)
CODE = {}
CODE["node"] = '''
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
'''
CODE["reverse"] = '''
def reverseList(head):
    prev, curr = None, head
    while curr:
        nxt = curr.next       # 1. 先存下一个, 否则改完 next 就找不到了
        curr.next = prev      # 2. 把箭头掉头, 指向前一个
        prev = curr           # 3. prev 前进
        curr = nxt            # 4. curr 前进
    return prev               # curr 走到 None 时, prev 是新的 head
'''
CODE["merge"] = '''
def mergeTwoLists(l1, l2):
    dummy = tail = ListNode()   # dummy: 假的头, 省掉 "结果为空" 的特判
    while l1 and l2:
        if l1.val <= l2.val:
            tail.next, l1 = l1, l1.next
        else:
            tail.next, l2 = l2, l2.next
        tail = tail.next        # tail 永远是结果的最后一个 node
    tail.next = l1 or l2        # 剩下的一条直接接上
    return dummy.next
'''
CODE["cycle"] = '''
def hasCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next          # 一次走 1 步
        fast = fast.next.next     # 一次走 2 步
        if slow is fast:          # 有环: fast 一定会从后面追上 slow
            return True
    return False                  # fast 走到了尽头: 没有环
'''
CODE["middle"] = '''
def middleNode(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow                   # fast 走完时, slow 正好在中间
'''
CODE["remove_nth"] = '''
def removeNthFromEnd(head, n):
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n + 1):        # fast 先走 n + 1 步, 和 slow 拉开 n + 1 的距离
        fast = fast.next
    while fast:                   # 一起走, 直到 fast 走出末尾
        fast, slow = fast.next, slow.next
    slow.next = slow.next.next    # slow 停在要删的 node 的前一个
    return dummy.next
'''
CODE["add"] = '''
def addTwoNumbers(l1, l2):
    dummy = tail = ListNode()
    carry = 0
    while l1 or l2 or carry:
        s = carry
        if l1:
            s, l1 = s + l1.val, l1.next
        if l2:
            s, l2 = s + l2.val, l2.next
        carry, digit = divmod(s, 10)   # 进位, 当前位
        tail.next = ListNode(digit)
        tail = tail.next
    return dummy.next
'''
CODE["reverse_k"] = '''
def reverseKGroup(head, k):
    dummy = ListNode(0, head)
    group_prev = dummy                 # 上一组的最后一个 node
    while True:
        kth = group_prev
        for _ in range(k):             # 往后数 k 个, 不够 k 个就结束
            kth = kth.next
            if not kth:
                return dummy.next
        group_next = kth.next
        prev, curr = group_next, group_prev.next   # 和 reverseList 一样, 只是 prev 从 group_next 开始
        while curr is not group_next:
            nxt = curr.next
            curr.next = prev
            prev, curr = curr, nxt
        first = group_prev.next        # 反转前的第一个, 现在是这一组的最后一个
        group_prev.next = kth          # 上一组接到这一组的新头 (原来的第 k 个)
        group_prev = first
'''
CODE["copy"] = '''
class Node:
    def __init__(self, x, next=None, random=None):
        self.val, self.next, self.random = x, next, random

def copyRandomList(head):
    old2new = {None: None}           # 原 node -> 新 node
    cur = head
    while cur:                       # 第 1 遍: 只建新 node
        old2new[cur] = Node(cur.val)
        cur = cur.next
    cur = head
    while cur:                       # 第 2 遍: 连 next 和 random
        old2new[cur].next = old2new[cur.next]
        old2new[cur].random = old2new[cur.random]
        cur = cur.next
    return old2new[head]
'''
CODE["palindrome"] = '''
def isPalindrome(head):
    slow = fast = head                 # 1. 快慢指针找中点
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    prev = None                        # 2. 反转后半段 (就是 reverseList)
    while slow:
        slow.next, prev, slow = prev, slow, slow.next
    left, right = head, prev           # 3. 两头往中间比
    while right:
        if left.val != right.val:
            return False
        left, right = left.next, right.next
    return True
'''
NS = {}
for k in ["node", "reverse", "merge", "cycle", "middle", "remove_nth", "add", "reverse_k", "palindrome"]:
    exec(CODE[k], NS)
CNS = {}
exec(CODE["copy"], CNS)
ListNode = NS["ListNode"]


def build(vals):
    dummy = ListNode()
    t = dummy
    for v in vals:
        t.next = ListNode(v)
        t = t.next
    return dummy.next


def tolist(h, limit=100):
    out = []
    while h and limit:
        out.append(h.val)
        h = h.next
        limit -= 1
    return out


# ---- 对拍
random.seed(3)
for _ in range(500):
    a = [random.randint(0, 9) for _ in range(random.randint(0, 8))]
    assert tolist(NS["reverseList"](build(a))) == a[::-1]
    b = sorted(random.randint(0, 9) for _ in range(random.randint(0, 6)))
    s = sorted(a)
    assert tolist(NS["mergeTwoLists"](build(s), build(b))) == sorted(s + b)
    if a:
        assert NS["middleNode"](build(a)).val == a[len(a) // 2]
        n = random.randint(1, len(a))
        exp = a[:len(a) - n] + a[len(a) - n + 1:]
        assert tolist(NS["removeNthFromEnd"](build(a), n)) == exp
        k = random.randint(1, 4)
        exp2 = []
        for i in range(0, len(a), k):
            g = a[i:i + k]
            exp2 += g[::-1] if len(g) == k else g
        assert tolist(NS["reverseKGroup"](build(a), k)) == exp2
        assert NS["isPalindrome"](build(a)) == (a == a[::-1])
    x, y = random.randint(0, 99999), random.randint(0, 99999)
    r = NS["addTwoNumbers"](build([int(c) for c in str(x)[::-1]]), build([int(c) for c in str(y)[::-1]]))
    assert int("".join(map(str, tolist(r)[::-1]))) == x + y
h = build([1, 2, 3, 4])
assert not NS["hasCycle"](h)
h.next.next.next.next = h.next
assert NS["hasCycle"](h)
print("all tests passed")

# ============================================================ SVG: linked list 画法
FONT = nc.FONT
NEW, REM, KEEP, INK, SUB, LINE, RING, ARR = nc.NEW, nc.REM, nc.KEEP, nc.INK, nc.SUB, nc.LINE, nc.RING, nc.ARR
BW, BH, GAP = 40, 30, 26     # node 宽, 高, 间距


class S:
    def __init__(self):
        self.p = []

    def t(self, x, y, s, size=12, fill=SUB, anchor="start", weight=400):
        self.p.append('<text x="%s" y="%s" font-size="%d" fill="%s" text-anchor="%s" font-weight="%d" '
                      'dominant-baseline="central" style="white-space:pre">%s</text>'
                      % (x, y, size, fill, anchor, weight, html.escape(str(s))))

    def line(self, y):
        self.p.append('<line x1="40" y1="%s" x2="640" y2="%s" stroke="%s" stroke-dasharray="4 4"/>' % (y, y, LINE))

    def node(self, x, y, label, role="keep", ring=False):
        f, s, c = {"new": NEW, "rem": REM, "keep": KEEP}[role]
        self.p.append('<rect x="%s" y="%s" width="%s" height="%s" rx="4" fill="%s" stroke="%s"%s/>'
                      % (x, y, BW, BH, f, s, ' stroke-dasharray="3 2"' if role == "rem" else ""))
        if ring:
            self.p.append('<rect x="%s" y="%s" width="%s" height="%s" rx="6" fill="none" stroke="%s" stroke-width="2.5"/>'
                          % (x - 3, y - 3, BW + 6, BH + 6, RING))
        self.t(x + BW / 2, y + BH / 2 + 1, label, 14, c, "middle", 500)

    def arrow(self, x1, y1, x2, y2, color="#898781", dash=False, curve=0, width=1.4):
        mid = "Q%s %s " % ((x1 + x2) / 2, min(y1, y2) - curve) if curve else "L"
        if curve:
            dpath = "M%s %s %s%s %s" % (x1, y1, mid, x2, y2)
        else:
            dpath = "M%s %s L%s %s" % (x1, y1, x2, y2)
        self.p.append('<path d="%s" fill="none" stroke="%s" stroke-width="%s"%s marker-end="url(#a%s)"/>'
                      % (dpath, color, width, ' stroke-dasharray="4 3"' if dash else "", color[1:]))

    def save(self, name, title, h):
        cols = ["#898781", NEW[1], ARR, RING]
        defs = "".join('<marker id="a%s" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" '
                       'orient="auto"><path d="M2 1L8 5L2 9" fill="none" stroke="%s" stroke-width="1.5"/></marker>'
                       % (c[1:], c) for c in cols)
        svg = ('<svg width="100%%" viewBox="0 0 680 %d" xmlns="http://www.w3.org/2000/svg" role="img" font-family="%s">'
               '<title>%s</title><defs>%s</defs>%s</svg>\n' % (h, FONT, html.escape(title), defs, "\n".join(self.p)))
        with open(os.path.join(SVG_DIR, name), "w", encoding="utf-8") as f:
            f.write(svg)


def draw_list(s, x0, y, labels, nxt, roles=None, rings=(), ptrs=None, green=(), red=(), none_label=True):
    """labels: node 的文字; nxt[i] = 指向的 node 下标 / None; ptrs: {名字: 下标} 画在 node 下面;
    green: 新改的边 (i), red: 刚被断开的边 (i, 旧目标) 画红虚线。"""
    roles = roles or ["keep"] * len(labels)
    X = [x0 + i * (BW + GAP) for i in range(len(labels))]
    for i, lab in enumerate(labels):
        s.node(X[i], y, lab, roles[i], i in rings)
    for i, t in enumerate(nxt):
        col = NEW[1] if i in green else "#898781"
        w = 2.2 if i in green else 1.4
        if t is None:
            if none_label and i in green:
                s.t(X[i] + BW / 2, y - 12, "→ None", 11, NEW[2], "middle")
            continue
        if t == i + 1:
            s.arrow(X[i] + BW, y + BH / 2, X[t] - 2, y + BH / 2, col, width=w)
        elif t == i - 1:
            s.arrow(X[i], y + 8, X[t] + BW + 2, y + 8, col, width=w)
        else:
            s.arrow(X[i] + BW / 2, y, X[t] + BW / 2, y - 2, col, curve=28, width=w)
    for (i, t) in red:
        s.arrow(X[i] + BW, y + BH - 6, X[t] - 2, y + BH - 6, ARR, dash=True)
    if ptrs:
        by = {}
        for name, i in ptrs.items():
            by.setdefault(i, []).append(name)
        for i, names in by.items():
            xx = X[i] + BW / 2 if 0 <= i < len(X) else (X[-1] + BW + GAP + 10 if i >= len(X) else x0 - 30)
            s.t(xx, y + BH + 14, " / ".join(names), 12, "#B5700F", "middle", 500)
    return X


def trace_svg(name, title, head, cols, rows, final, legend, row_h=86):
    """一行一步: 左边 '这一步做什么', 中间 list 的状态, 右边计算 / 说明。"""
    s = S()
    y = 18
    for h0 in head:
        for h in nc._wrap(h0, 12):
            s.t(40, y, h, 12, SUB)
            y += 20
    y += 6
    for x, c in cols:
        s.t(x, y, c, 12, SUB)
    y += 10
    s.line(y)
    for r in rows:
        for j, (txt, sz, col) in enumerate(r["left"]):
            s.t(40, y + 24 + j * 18, txt, sz, col, "start", 500 if sz >= 14 else 400)
        r["draw"](s, y + 26)
        for j, txt in enumerate(r.get("right", [])):
            s.t(r.get("rx", 470), y + 22 + j * 18, txt, 12 if j else 13, INK if j == 0 else SUB, "start", 500 if j == 0 else 400)
        y += r.get("h", row_h)
        s.line(y)
    for j, f in enumerate(final):
        s.t(40, y + 22 + j * 20, f, 14, INK, "start", 500)
    y += 32 + 20 * len(final)
    x = 40
    for role, text in legend:
        if role == "ring":
            s.p.append('<rect x="%s" y="%s" width="14" height="14" rx="3" fill="none" stroke="%s" stroke-width="2.5"/>' % (x - 7, y - 7, RING))
        elif role == "gedge":
            s.p.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="2.2"/>' % (x - 8, y, x + 8, y, NEW[1]))
        elif role == "redge":
            s.p.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-dasharray="4 3" stroke-width="1.4"/>' % (x - 8, y, x + 8, y, ARR))
        else:
            f, st, _ = {"new": NEW, "rem": REM, "keep": KEEP}[role]
            s.p.append('<rect x="%s" y="%s" width="14" height="14" rx="3" fill="%s" stroke="%s"/>' % (x - 7, y - 7, f, st))
        s.t(x + 14, y, text, 12, SUB)
        x += 14 + nc._w(text, 12) + 26
    s.save(name, title, y + 20)


# ============================================================ SVG 1: 第一性原理 (dummy + 改 next 前先存)
def fig_core():
    s = S()
    s.t(40, 18, "linked list 只能顺着 next 往后走。所有操作的本质: 改某个 node 的 next 之前, 先把以后还要用的 node 存下来", 12, SUB)
    s.t(40, 44, "错误: 直接改 curr.next = prev", 14, REM[2], "start", 500)
    draw_list(s, 60, 70, ["1", "2", "3"], [None, None, None], roles=["keep", "keep", "keep"], ptrs={"prev": 0, "curr": 1}, green=(), red=[(1, 2)])
    s.arrow(60 + BW + GAP + 4, 78, 60 + BW - 2, 78, NEW[1], width=2.2)
    s.t(300, 85, "2 的 next 改成指向 1 之后, 再也找不到 3 了 (红虚线断了)", 12, REM[2])
    s.line(128)
    s.t(40, 150, "正确: 先 nxt = curr.next, 再改", 14, NEW[2], "start", 500)
    draw_list(s, 60, 176, ["1", "2", "3"], [None, 0, None], ptrs={"prev": 0, "curr": 1, "nxt": 2}, green=(1,))
    s.t(300, 191, "nxt 记住了 3, 改完 2 的 next 还能继续往后走", 12, NEW[2])
    s.line(234)
    s.t(40, 256, "dummy node: 在 head 前面放一个假的 node", 14, INK, "start", 500)
    draw_list(s, 60, 282, ["D", "1", "2", "3"], [1, 2, 3, None], roles=["new", "keep", "keep", "keep"], ptrs={"dummy": 0, "head": 1})
    s.t(370, 290, "删掉 / 换掉第一个 node 时, 不用特判 \"head 变了\"", 12, SUB)
    s.t(370, 308, "最后返回 dummy.next 就是新的 head", 12, SUB)
    s.save("core.svg", "Linked list first principles", 346)


# ============================================================ SVG 2: Reverse trace
def fig_reverse_trace():
    vals = [1, 2, 3, 4]
    n = len(vals)
    nxt = [1, 2, 3, None]
    prev, curr = None, 0
    rows = []
    step = 0
    while curr is not None:
        step += 1
        nx = nxt[curr]
        old = nxt[curr]
        nxt[curr] = prev
        p_old, c_old = prev, curr
        prev, curr = curr, nx
        state = list(nxt)
        roles = ["new" if i <= c_old else "keep" for i in range(n)]
        ptrs = {"prev": prev, "curr": curr if curr is not None else n}

        def drawer(s, y, state=state, roles=roles, ptrs=ptrs, c_old=c_old, old=old):
            red = [(c_old, old)] if old is not None else []
            draw_list(s, 150, y, [str(v) for v in vals], state, roles, ptrs=ptrs, green=(c_old,), red=red)
            if ptrs["curr"] == n:
                s.t(150 + n * (BW + GAP) + 4, y + BH / 2, "None", 12, SUB)
        rows.append(dict(left=[("step %d" % step, 14, INK), ("curr = %d" % vals[c_old], 12, SUB)], draw=drawer,
                         right=["%d.next: %s → %s" % (vals[c_old], vals[old] if old is not None else "None",
                                                      vals[p_old] if p_old is not None else "None"),
                                "nxt 先存了 %s" % (vals[old] if old is not None else "None"),
                                "prev = %d, curr = %s" % (vals[prev], vals[curr] if curr is not None else "None")], rx=470))
    head = NS["reverseList"](build(vals))
    assert tolist(head) == [4, 3, 2, 1]
    trace_svg("reverse_trace.svg", "Reverse Linked List trace",
              ["head = 1 → 2 → 3 → 4 · 每一步: nxt = curr.next → curr.next = prev → prev = curr → curr = nxt"],
              [(40, "这一步"), (150, "改完之后的 list"), (470, "计算")],
              rows, ["curr 走到 None, 返回 prev = 4:  4 → 3 → 2 → 1"],
              [("new", "已经反转的部分"), ("gedge", "刚改的 next"), ("redge", "刚断开的 next")])


# ============================================================ SVG 3: Merge trace
def fig_merge_trace():
    A, B = [1, 2, 4], [1, 3, 4]
    i = j = 0
    out = []
    rows = []
    while i < len(A) and j < len(B):
        av, bv = A[i], B[j]
        if av <= bv:
            pick, src = av, "l1"
            i += 1
            cmp = "%d ≤ %d → 取 l1 的 %d" % (av, bv, av)
        else:
            pick, src = bv, "l2"
            j += 1
            cmp = "%d > %d → 取 l2 的 %d" % (av, bv, bv)
        out.append((pick, src))
        a_, b_, o_ = i, j, list(out)

        def drawer(s, y, a_=a_, b_=b_, o_=o_):
            for k, v in enumerate(A):
                s.node(130 + k * 46, y - 14, str(v), "rem" if k < a_ else "keep", k == a_)
            for k, v in enumerate(B):
                s.node(130 + k * 46, y + 22, str(v), "rem" if k < b_ else "keep", k == b_)
            s.t(114, y + 1, "l1", 11, SUB, "end")
            s.t(114, y + 37, "l2", 11, SUB, "end")
            for k, (v, sr) in enumerate(o_):
                s.node(300 + k * 30, y + 4, str(v), "new" if k == len(o_) - 1 else "keep")
        rows.append(dict(left=[("取 %d" % pick, 14, INK), ("来自 %s" % src, 12, SUB)], draw=drawer, h=96,
                         right=["头: l1 = %d, l2 = %d" % (av, bv), cmp], rx=500))
    rest = A[i:] + B[j:]
    assert tolist(NS["mergeTwoLists"](build(A), build(B))) == [v for v, _ in out] + rest
    trace_svg("merge_trace.svg", "Merge Two Sorted Lists trace",
              ["l1 = 1 → 2 → 4, l2 = 1 → 3 → 4 · 每一步: 比较两个头, 小的接到结果后面, 那条 list 往后走一个"],
              [(40, "这一步"), (130, "两条输入 (橙圈 = 下一轮的头)"), (300, "结果"), (500, "比较")],
              rows, ["l1 走完了, 把 l2 剩下的 %s 直接接上:  %s" % (rest, " → ".join(str(v) for v in [v for v, _ in out] + rest))],
              [("rem", "已经取走的"), ("ring", "下一轮要比较的头"), ("new", "这一步接上的")])


# ============================================================ SVG 4: fast/slow (middle + cycle)
def fig_fastslow_trace():
    vals = [1, 2, 3, 4, 5]
    rows = []
    slow = fast = 0
    rows_state = [(slow, fast)]
    while fast < len(vals) and fast + 1 < len(vals):
        slow, fast = slow + 1, fast + 2
        rows_state.append((slow, fast))
    assert NS["middleNode"](build(vals)).val == vals[slow]
    for k, (sl, fa) in enumerate(rows_state):
        def drawer(s, y, sl=sl, fa=fa):
            roles = ["new" if i == sl else "keep" for i in range(len(vals))]
            draw_list(s, 150, y, [str(v) for v in vals], [1, 2, 3, 4, None], roles, rings=(fa,) if fa < len(vals) else (),
                      ptrs={"slow": sl, "fast": fa})
        stop = not (fa < len(vals) and fa + 1 < len(vals))
        rows.append(dict(left=[("开始" if k == 0 else "第 %d 轮" % k, 14, INK)], draw=drawer, h=78,
                         right=["slow 走了 %d 步, fast 走了 %d 步" % (sl, fa), "fast.next 是 None → 停" if stop else "fast 后面还有 → 继续"], rx=470))
    trace_svg("fastslow_trace.svg", "Middle of the Linked List trace",
              ["1 → 2 → 3 → 4 → 5 · slow 一次走 1 步, fast 一次走 2 步; fast 走到末尾时, slow 只走了一半"],
              [(40, "轮次"), (150, "slow (绿) 和 fast (橙圈) 的位置"), (470, "计算")],
              rows, ["返回 slow = 3, 正好在中间"], [("new", "slow"), ("ring", "fast")])


def fig_cycle_trace():
    vals = [1, 2, 3, 4, 5, 6]
    nxt = [1, 2, 3, 4, 5, 2]     # 6 -> 3, 环是 3 4 5 6
    slow = fast = 0
    rows = []
    k = 0
    while True:
        slow, fast = nxt[slow], nxt[nxt[fast]]
        k += 1
        meet = slow == fast

        def drawer(s, y, sl=slow, fa=fast):
            roles = ["new" if i == sl else "keep" for i in range(6)]
            draw_list(s, 120, y, [str(v) for v in vals], nxt, roles, rings=(fa,), ptrs={"slow": sl, "fast": fa})
        rows.append(dict(left=[("第 %d 轮" % k, 14, INK)], draw=drawer, h=86,
                         right=["slow = %d, fast = %d" % (vals[slow], vals[fast]), "相遇! 有环" if meet else "还没相遇"], rx=520))
        if meet:
            break
    h = build(vals)
    nodes = []
    t = h
    while t:
        nodes.append(t)
        t = t.next
    nodes[-1].next = nodes[2]
    assert NS["hasCycle"](h)
    trace_svg("cycle_trace.svg", "Linked List Cycle trace",
              ["1 → 2 → 3 → 4 → 5 → 6 → 回到 3 · 进了环之后, fast 每轮比 slow 多走 1 步, 两者的距离每轮缩小 1, 一定会相遇"],
              [(40, "轮次"), (120, "slow (绿) 和 fast (橙圈)"), (520, "计算")],
              rows, ["第 %d 轮相遇 → return True" % k], [("new", "slow"), ("ring", "fast")])


# ============================================================ SVG 5: remove nth
def fig_remove_trace():
    vals = ["D", "1", "2", "3", "4", "5"]
    n = 2
    nxt = [1, 2, 3, 4, 5, None]
    rows = []
    fast = slow = 0
    for _ in range(n + 1):
        fast += 1

    def mk(sl, fa, label, right, done=False):
        def drawer(s, y):
            st = list(nxt)
            red = []
            green = ()
            roles = ["new"] + ["keep"] * 5
            if done:
                st[sl] = sl + 2
                red = []
                green = (sl,)
                roles[sl + 1] = "rem"
            draw_list(s, 130, y, vals, st, roles, rings=(fa,) if fa < 6 else (), ptrs={"slow": sl, "fast": fa})
            if fa >= 6:
                s.t(130 + 6 * (BW + GAP) - 4, y + BH / 2, "None", 12, SUB)
        rows.append(dict(left=label, draw=drawer, right=right, rx=575, h=92))
    mk(slow, fast, [("fast 先走", 13, INK), ("n+1 = 3 步", 12, SUB)], ["隔了 3 格", "slow 在 D"])
    while fast < 6:
        fast += 1
        slow += 1
    mk(slow, fast, [("一起走到", 13, INK), ("fast = None", 12, SUB)], ["slow 停在 3", "要删 slow.next"])
    mk(slow, fast, [("跳过 4", 13, INK), ("slow.next =", 12, SUB), ("slow.next.next", 12, SUB)], ["3 → 5", "4 被删掉"], done=True)
    assert tolist(NS["removeNthFromEnd"](build([1, 2, 3, 4, 5]), 2)) == [1, 2, 3, 5]
    trace_svg("remove_trace.svg", "Remove Nth Node From End trace",
              ["1 → 2 → 3 → 4 → 5, n = 2 (删倒数第 2 个, 也就是 4) · D 是 dummy"],
              [(40, "这一步"), (130, "list (fast = 橙圈)"), (575, "计算")],
              rows, ["返回 dummy.next:  1 → 2 → 3 → 5"], [("new", "dummy"), ("ring", "fast"), ("rem", "被删的"), ("gedge", "改过的 next")])


# ============================================================ SVG 6: add two numbers
def fig_add_trace():
    A, B = [2, 4, 3], [5, 6, 4]
    carry = 0
    rows = []
    out = []
    for k in range(3):
        s_ = carry + A[k] + B[k]
        c0 = carry
        carry, dg = divmod(s_, 10)
        out.append(dg)
        o_ = list(out)

        def drawer(s, y, k=k, o_=o_):
            for i, v in enumerate(A):
                s.node(130 + i * 46, y - 14, str(v), "new" if i == k else "keep")
            for i, v in enumerate(B):
                s.node(130 + i * 46, y + 22, str(v), "new" if i == k else "keep")
            s.t(114, y + 1, "l1", 11, SUB, "end")
            s.t(114, y + 37, "l2", 11, SUB, "end")
            for i, v in enumerate(o_):
                s.node(300 + i * 46, y + 4, str(v), "new" if i == len(o_) - 1 else "keep")
        rows.append(dict(left=[("第 %d 位" % k, 14, INK)], draw=drawer, h=96,
                         right=["s = carry + %d + %d = %d + %d + %d = %d" % (A[k], B[k], c0, A[k], B[k], s_),
                                "digit = %d, carry = %d" % (dg, carry)], rx=450))
    assert tolist(NS["addTwoNumbers"](build(A), build(B))) == out
    trace_svg("add_trace.svg", "Add Two Numbers trace",
              ["l1 = 2 → 4 → 3 (表示 342), l2 = 5 → 6 → 4 (表示 465) · 数字是倒着存的, 所以从头开始就是从个位开始加"],
              [(40, "这一步"), (130, "两条输入 (绿 = 当前位)"), (300, "结果"), (450, "计算")],
              rows, ["结果 7 → 0 → 8, 表示 807 = 342 + 465"], [("new", "当前处理的位")])


# ============================================================ SVG 7: reverse k group
def fig_revk_trace():
    vals = [1, 2, 3, 4, 5]
    k = 2
    rows = []
    groups = [[1, 2], [3, 4]]
    cur = list(vals)
    states = [list(vals)]
    for gi in range(2):
        a = gi * k
        cur[a:a + k] = cur[a:a + k][::-1]
        states.append(list(cur))
    labels = ["初始", "反转第 1 组 [1,2]", "反转第 2 组 [3,4]"]
    rights = [["k = 2, 每 2 个一组", "5 不够一组, 不动"], ["组内 = reverseList", "dummy 接到新头 2"],
              ["1 接到新头 4", "只剩 5, 不够 k, 结束"]]
    for i, st in enumerate(states):
        def drawer(s, y, st=st, i=i):
            roles = ["keep"] * 5
            if i >= 1:
                for t in range(2 * i):
                    roles[t] = "new"
            draw_list(s, 170, y, [str(v) for v in st], [1, 2, 3, 4, None], roles)
        rows.append(dict(left=[(labels[i], 13, INK)], draw=drawer, right=rights[i], rx=520, h=74))
    assert tolist(NS["reverseKGroup"](build(vals), k)) == states[-1]
    trace_svg("revk_trace.svg", "Reverse Nodes in k-Group trace",
              ["1 → 2 → 3 → 4 → 5, k = 2 · 每次往后数 k 个; 够了就把这一段反转, 再把它接回前后"],
              [(40, "这一步"), (170, "list"), (520, "说明")],
              rows, ["结果 2 → 1 → 4 → 3 → 5"], [("new", "已经反转好的组")])


# ============================================================ SVG 8: copy random
def fig_copy_trace():
    s = S()
    s.t(40, 18, "原 list: 7 → 13 → 11, random: 7→None, 13→7, 11→13 · 两遍: 先建所有新 node, 再按 old2new 连 next 和 random", 12, SUB)
    s.t(40, 48, "原 list", 13, INK, "start", 500)
    X = draw_list(s, 130, 40, ["7", "13", "11"], [1, 2, None])
    for i, t in [(1, 0), (2, 1)]:
        s.arrow(X[i] + BW / 2, 40 + BH, X[t] + BW / 2 + 6, 40 + BH + 2, ARR, curve=-24)
    s.t(420, 55, "橙色弯箭头 = random", 12, "#B5700F")
    s.line(110)
    s.t(40, 134, "第 1 遍", 13, INK, "start", 500)
    for i, v in enumerate(["7'", "13'", "11'"]):
        s.node(130 + i * (BW + GAP), 122, v, "new")
    s.t(420, 130, "old2new = {7: 7', 13: 13', 11: 11'}", 12, INK)
    s.t(420, 148, "只建 node, 不连任何箭头", 12, SUB)
    s.line(176)
    s.t(40, 200, "第 2 遍", 13, INK, "start", 500)
    X2 = draw_list(s, 130, 190, ["7'", "13'", "11'"], [1, 2, None], roles=["new"] * 3, green=(0, 1))
    for i, t in [(1, 0), (2, 1)]:
        s.arrow(X2[i] + BW / 2, 190 + BH, X2[t] + BW / 2 + 6, 190 + BH + 2, ARR, curve=-24)
    s.t(420, 198, "13'.random = old2new[13.random]", 12, INK)
    s.t(420, 216, "         = old2new[7] = 7'", 12, INK)
    s.t(420, 236, "next 同理", 12, SUB)
    s.line(276)
    s.t(40, 298, "为什么要两遍: 连 13'.random 的时候, 7' 必须已经存在。第 1 遍先把所有新 node 建好, 第 2 遍查表一定查得到", 12, INK)
    s.save("copy_trace.svg", "Copy List with Random Pointer trace", 322)
    h = CNS["Node"](7)
    b = CNS["Node"](13)
    c = CNS["Node"](11)
    h.next, b.next = b, c
    b.random, c.random = h, b
    r = CNS["copyRandomList"](h)
    assert r is not h and r.next.random is r and r.next.next.random is r.next


# ============================================================ SVG 9: palindrome
def fig_pal_trace():
    vals = [1, 2, 3, 2, 1]
    rows = []

    def r1(s, y):
        draw_list(s, 150, y, [str(v) for v in vals], [1, 2, 3, 4, None], ["keep", "keep", "new", "keep", "keep"], rings=(4,),
                  ptrs={"slow": 2, "fast": 4})
    rows.append(dict(left=[("1. 找中点", 13, INK)], draw=r1, right=["快慢指针 (第 3 题)", "slow 停在中间的 3"], rx=500))

    def r2(s, y):
        draw_list(s, 150, y, [str(v) for v in vals], [1, 2, None, 2, 3], ["keep", "keep", "new", "new", "new"], green=(3, 4),
                  ptrs={"left": 0, "right": 4})
    rows.append(dict(left=[("2. 反转后半段", 13, INK)], draw=r2, right=["3 ← 2 ← 1, right = 最后的 1", "就是 reverseList (第 1 题)"], rx=500))

    def r3(s, y):
        draw_list(s, 150, y, [str(v) for v in vals], [1, 2, None, 2, 3], ["new", "new", "keep", "new", "new"], ptrs={"left": 0, "right": 4})
    rows.append(dict(left=[("3. 两头往中间比", 13, INK)], draw=r3, right=["1 = 1, 2 = 2, 3 = 3", "right 走到 None → True"], rx=500))
    assert NS["isPalindrome"](build(vals))
    trace_svg("pal_trace.svg", "Palindrome Linked List trace",
              ["1 → 2 → 3 → 2 → 1 · 三步: 找中点 → 反转后半段 → 两头一起往中间比"],
              [(40, "这一步"), (150, "list"), (500, "说明")], rows, ["return True"],
              [("new", "这一步用到的 node"), ("gedge", "反转后的 next")])


for f in (fig_core, fig_reverse_trace, fig_merge_trace, fig_fastslow_trace, fig_cycle_trace, fig_remove_trace,
          fig_add_trace, fig_revk_trace, fig_copy_trace, fig_pal_trace):
    f()

exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "08_linked_list_doc.py"), encoding="utf-8").read())
