"""11 · Binary Tree / BST   —   cd build && python3 -I 11_tree.py
文档里的每段代码都在这里被 exec 并断言; trace 图的数字来自对同一逻辑的插桩运行。
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import doclib as d  # noqa: E402

SLUG = "11-tree"
SVG_DIR = os.path.join(d.ROOT, "docs", "svg", SLUG)
os.makedirs(SVG_DIR, exist_ok=True)

# ---------------------------------------------------------------- tree basics


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def build(vals):
    """level-order list (None = 空) -> TreeNode"""
    if not vals:
        return None
    nodes = [None if v is None else TreeNode(v) for v in vals]
    kids = iter(nodes[1:])
    for n in nodes:
        if n is not None:
            n.left = next(kids, None)
            n.right = next(kids, None)
    return nodes[0]


def find(root, val):
    if not root:
        return None
    if root.val == val:
        return root
    return find(root.left, val) or find(root.right, val)


def layout(root, dx, dy):
    """inorder 下标 = x, depth = y  -> {val: (x, y, parent_val, side)}"""
    pos = {}
    cnt = [0]

    def go(n, depth, par, side):
        if not n:
            return
        go(n.left, depth + 1, n.val, "L")
        pos[n.val] = (cnt[0] * dx, depth * dy, par, side)
        cnt[0] += 1
        go(n.right, depth + 1, n.val, "R")
    go(root, 0, None, None)
    return pos


def depth_of(root):
    return 0 if not root else 1 + max(depth_of(root.left), depth_of(root.right))


# ---------------------------------------------------------------- svg helpers
INK, SUB = "#0B0B0B", "#52514E"
GREEN = ("#E1F5EE", "#0F6E56", "#085041")
RED = ("#FAECE7", "#993C1D", "#712B13")
PLAIN = ("#F1EFE8", "#5F5E5A", "#444441")
DONE = ("#D3D1C7", "#A9A79E", "#6B6A65")
TODO = ("#FFFFFF", "#5F5E5A", "#444441")
ORANGE = "#EF9F27"
SEP = "#B4B2A9"
FONT = 'ui-sans-serif, system-ui, -apple-system, "PingFang SC", sans-serif'


def esc(s):
    return html.escape(str(s), quote=False)


class Svg:
    def __init__(self, w, h, title, desc=""):
        self.w, self.h, self.title, self.desc = w, h, title, desc
        self.o = []

    def t(self, x, y, s, size=14, anchor="start", fill=INK, bold=False):
        self.o.append('<text x="%s" y="%s" font-size="%d" text-anchor="%s" fill="%s"%s '
                      'dominant-baseline="central">%s</text>'
                      % (x, y, size, anchor, fill, ' font-weight="600"' if bold else "", esc(s)))

    def line(self, x1, y1, x2, y2, stroke="#898781", sw=1.5, dash=None, marker=None):
        self.o.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s%s/>'
                      % (x1, y1, x2, y2, stroke, sw,
                         ' stroke-dasharray="%s"' % dash if dash else "",
                         ' marker-end="url(#%s)"' % marker if marker else ""))

    def path(self, dstr, stroke="#898781", sw=1.5, dash=None, marker=None, fill="none"):
        self.o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="%s"%s%s/>'
                      % (dstr, fill, stroke, sw,
                         ' stroke-dasharray="%s"' % dash if dash else "",
                         ' marker-end="url(#%s)"' % marker if marker else ""))

    def rect(self, x, y, w, h, role=PLAIN, ring=False, rx=4, sw=1, dash=None):
        f, s, _ = role
        self.o.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" '
                      'stroke-width="%s"%s/>' % (x, y, w, h, rx, f, s, sw,
                                                 ' stroke-dasharray="%s"' % dash if dash else ""))
        if ring:
            self.o.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="none" '
                          'stroke="%s" stroke-width="2.5"/>' % (x - 3, y - 3, w + 6, h + 6, rx + 2, ORANGE))

    def cell(self, x, y, w, h, label, role=PLAIN, ring=False, size=14, dash=None):
        self.rect(x, y, w, h, role, ring, dash=dash)
        self.t(x + w / 2, y + h / 2, label, size, "middle", role[2])

    def node(self, x, y, label, role=PLAIN, ring=False, r=15, dash=None):
        f, s, c = role
        self.o.append('<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" stroke-width="1"%s/>'
                      % (x, y, r, f, s, ' stroke-dasharray="%s"' % dash if dash else ""))
        if ring:
            self.o.append('<circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-width="2.5"/>'
                          % (x, y, r + 4, ORANGE))
        self.t(x, y, label, 14, "middle", c)

    def sep(self, y, x1=40, x2=640):
        self.line(x1, y, x2, y, SEP, 1, "4 4")

    def legend(self, y, items, x=40):
        """items: [(role, ring, text)]"""
        for role, ring, text in items:
            self.node(x + 8, y, "", role, ring, r=7)
            self.t(x + 24, y, text, 12, fill=SUB)
            x += 34 + 7 * len(text) + sum(6 for ch in text if ord(ch) > 255)

    def render(self):
        defs = ('<defs>'
                '<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
                '<path d="M2 1L8 5L2 9" fill="none" stroke="#5F5E5A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>'
                '<marker id="arrowO" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
                '<path d="M2 1L8 5L2 9" fill="none" stroke="#D85A30" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>'
                '<marker id="arrowG" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
                '<path d="M2 1L8 5L2 9" fill="none" stroke="#0F6E56" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>'
                '</defs>')
        return ('<svg width="100%%" viewBox="0 0 %d %d" role="img" xmlns="http://www.w3.org/2000/svg" '
                'font-family=\'%s\'><title>%s</title><desc>%s</desc>%s\n%s\n</svg>\n'
                % (self.w, self.h, FONT, esc(self.title), esc(self.desc), defs, "\n".join(self.o)))

    def save(self, name):
        with open(os.path.join(SVG_DIR, name), "w", encoding="utf-8") as f:
            f.write(self.render())


def draw_tree(s, root, ox, oy, dx, dy, state=None, labels=None, r=14, edge_color="#898781",
              default=TODO, tags=None, hot_edges=(), lab_size=12, edge_marker=None):
    """画 tree。state: {val: (role, ring)}; labels: {val: (text, color, bold)}; tags: {val: 'p'}
    hot_edges: 要加粗成 GREEN 的 (parent, child)。返回 {val: (x, y)} 绝对坐标。"""
    pos = layout(root, dx, dy)
    xy = {v: (ox + p[0], oy + p[1]) for v, p in pos.items()}
    state = state or {}
    labels = labels or {}
    tags = tags or {}
    for v, (x, y, par, side) in pos.items():
        if par is not None:
            px, py = xy[par]
            cx, cy = ox + x, oy + y
            hot = (par, v) in hot_edges
            s.line(px, py, cx, cy, "#0F6E56" if hot else edge_color, 3.5 if hot else 1.2)
    for v, (x, y, par, side) in pos.items():
        cx, cy = xy[v]
        role, ring = state.get(v, (default, False))
        s.node(cx, cy, v, role, ring, r=r)
        if v in labels:
            text, color, bold = labels[v]
            if side == "L":
                s.t(cx - r - 3, cy - r + 1, text, lab_size, "end", color, bold)
            else:
                s.t(cx + r + 3, cy - r + 1, text, lab_size, "start", color, bold)
        if v in tags:
            s.t(cx, cy + r + 9, tags[v], 12, "middle", "#993C1D", True)
    return xy


# ---------------------------------------------------------------- 文档里的代码 (会被 exec + 断言)
CODE_TEMPLATE = '''
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

# 模板 A: 自底向上 (post-order)。返回值 = 这棵子树的"摘要"
def solve(node):
    if not node:
        return BASE                    # None 的摘要: depth 0 / gain 0 / None
    L = solve(node.left)               # 假设: 左子树已经算好
    R = solve(node.right)              # 假设: 右子树已经算好
    return merge(node.val, L, R)       # 当前 node 只做合并: L、R -> 自己的摘要

# 模板 B: 自顶向下 (pre-order)。参数 = 祖先传下来的"约束"
def check(node, constraint):
    if not node:
        return True
    if violates(node, constraint):     # 先用约束检查自己
        return False
    return (check(node.left,  tighten(constraint, node, "L")) and
            check(node.right, tighten(constraint, node, "R")))   # 把更严的约束传给孩子
'''

CODE_DEPTH = '''
def maxDepth(root):
    if not root:
        return 0                                       # base: None 的深度是 0
    return 1 + max(maxDepth(root.left),                # 左子树已算好
                   maxDepth(root.right))               # 右子树已算好; +1 = 自己这层
'''

CODE_DIAMETER = '''
def diameterOfBinaryTree(root):
    best = 0                          # 答案: 全局记录, 不是递归的返回值
    def height(node):                 # 返回值: 以 node 为顶向下的最长链 (点数)
        nonlocal best
        if not node:
            return 0
        L = height(node.left)
        R = height(node.right)
        best = max(best, L + R)       # 拐点: 经过 node 的路径 = 左链 + 右链 (边数)
        return 1 + max(L, R)          # 给父亲: 路径不能分叉, 只能带一边上去
    height(root)
    return best
'''

CODE_MAXPATH = '''
def maxPathSum(root):
    best = float("-inf")              # 答案: 全局; 值可负, 初值是 -inf 不是 0
    def gain(node):                   # 返回值: 以 node 为顶、只往下走一条链的最大和
        nonlocal best
        if not node:
            return 0
        L = max(gain(node.left), 0)   # 改动 1: 负的链不如不要 (clamp 到 0)
        R = max(gain(node.right), 0)
        best = max(best, node.val + L + R)   # 拐点: 两边都用 -> 候选答案
        return node.val + max(L, R)          # 给父亲: 只能选一边
    gain(root)
    return best
'''

CODE_VALIDATE = '''
def isValidBST(root):
    def ok(node, low, high):                  # 参数: node 必须在开区间 (low, high) 内
        if not node:
            return True
        if not (low < node.val < high):       # 违反祖先传下来的约束
            return False
        return (ok(node.left,  low, node.val) and      # 向左: 上界收紧成 node.val
                ok(node.right, node.val, high))        # 向右: 下界收紧成 node.val
    return ok(root, float("-inf"), float("inf"))
'''

CODE_LEVEL = '''
from collections import deque

def levelOrder(root):
    res = []
    if not root:
        return res
    q = deque([root])
    while q:
        level = []
        for _ in range(len(q)):          # len(q) 只算一次 = 这一层的 node 数
            node = q.popleft()
            level.append(node.val)
            if node.left:  q.append(node.left)     # 孩子排在队尾 = 下一层
            if node.right: q.append(node.right)
        res.append(level)
    return res

def rightSideView(root):                 # 变体 1: 每层只留最后一个
    res = []
    if not root:
        return res
    q = deque([root])
    while q:
        last = None
        for _ in range(len(q)):
            node = q.popleft()
            last = node.val              # 改动: 不收集整层, 只记最后弹出的
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
        res.append(last)
    return res

def zigzagLevelOrder(root):              # 变体 2: 奇数层反转
    res = []
    if not root:
        return res
    q = deque([root])
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
        if len(res) % 2 == 1:            # 改动: 第 0 层不反转, 第 1 层反转 ...
            level.reverse()
        res.append(level)
    return res
'''

CODE_LCA = '''
def lowestCommonAncestor(root, p, q):
    # 返回值语义: root 子树里"找到的 p 或 q"; 两个都在 -> 它们的 LCA; 都不在 -> None
    if not root or root is p or root is q:
        return root                    # 遇到 p/q 直接返回 (另一个在下面则它就是 LCA)
    L = lowestCommonAncestor(root.left, p, q)
    R = lowestCommonAncestor(root.right, p, q)
    if L and R:                        # p、q 分居两侧: root 就是拐点
        return root
    return L or R                      # 只有一侧有: 原样往上传; 都没有: None

def lcaBST(root, p, q):                # BST 版: 大小关系直接告诉你往哪走
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root                # 分叉点
'''

CODE_KTH = '''
def kthSmallest(root, k):
    stack = []                         # 栈里是"还没处理自己、但已经在往左走的祖先"
    node = root
    while stack or node:
        while node:                    # 一路往左走到底, 路上的祖先全压栈
            stack.append(node)
            node = node.left
        node = stack.pop()             # 弹出 = inorder 的下一个 (比已弹出的都大)
        k -= 1
        if k == 0:
            return node.val            # 数到第 k 个就停, 不用遍历完
        node = node.right              # 处理完自己, 转去右子树
'''

CODE_CODEC = '''
class Codec:
    def serialize(self, root):
        out = []
        def dfs(node):                 # pre-order: 先写自己, 再写左, 再写右
            if not node:
                out.append("#")        # None 也写一个标记: 子树边界靠它确定
                return
            out.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
        dfs(root)
        return ",".join(out)

    def deserialize(self, data):
        it = iter(data.split(","))     # iterator: next() 消费一个 token, 共享读指针
        def build():
            v = next(it)
            if v == "#":
                return None
            node = TreeNode(int(v))
            node.left = build()        # 先建左 (吃掉左子树的所有 token) ...
            node.right = build()       # ... 剩下的 token 正好是右子树的
            return node
        return build()
'''

G = {"TreeNode": TreeNode}
for _c in (CODE_DEPTH, CODE_DIAMETER, CODE_MAXPATH, CODE_VALIDATE, CODE_LEVEL, CODE_LCA,
           CODE_KTH, CODE_CODEC):
    exec(_c, G)


def ser(root):
    return G["Codec"]().serialize(root)


# ---------------------------------------------------------------- 断言: 代码本身是对的
def _tests():
    import random
    t = build([3, 9, 20, None, None, 15, 7])
    assert G["maxDepth"](t) == 3 and G["maxDepth"](None) == 0
    t = build([1, 2, 3, 4, 5, None, None, 6, None, None, 7])
    assert G["diameterOfBinaryTree"](t) == 4
    assert G["maxPathSum"](build([-10, -5, 20, None, None, 15, 7])) == 42
    assert G["maxPathSum"](build([-3])) == -3
    assert G["maxPathSum"](build([1, -2, 3])) == 4
    assert G["isValidBST"](build([2, 1, 3])) and not G["isValidBST"](build([5, 1, 4, None, None, 3, 6]))
    bad = build([5, 3, 8, 2, 6, None, None, 1])
    assert not G["isValidBST"](bad)
    assert G["isValidBST"](build([5, 3, 8, 2, 4, 7, 9]))
    t = build([1, 2, 3, 4, 5, None, None, 6])
    assert G["levelOrder"](t) == [[1], [2, 3], [4, 5], [6]]
    assert G["rightSideView"](t) == [1, 3, 5, 6]
    assert G["zigzagLevelOrder"](t) == [[1], [3, 2], [4, 5], [6]]
    t = build([3, 5, 1, 6, 2])
    assert G["lowestCommonAncestor"](t, find(t, 6), find(t, 2)).val == 5
    assert G["lowestCommonAncestor"](t, find(t, 6), find(t, 1)).val == 3
    assert G["lowestCommonAncestor"](t, find(t, 5), find(t, 2)).val == 5
    b = build([6, 2, 8, 0, 4, 7, 9])
    assert G["lcaBST"](b, find(b, 2), find(b, 8)).val == 6
    assert G["lcaBST"](b, find(b, 2), find(b, 4)).val == 2
    k = build([5, 3, 6, 2, 4, None, None, 1])
    assert [G["kthSmallest"](k, i) for i in range(1, 7)] == [1, 2, 3, 4, 5, 6]
    c = G["Codec"]()
    t = build([1, 2, 3, None, None, 4, 5])
    s = c.serialize(t)
    assert s == "1,2,#,#,3,4,#,#,5,#,#", s
    assert c.serialize(c.deserialize(s)) == s
    assert c.deserialize("#") is None
    # 随机交叉验证
    def rnd(n):
        vals = [random.randint(-5, 9) for _ in range(n)]
        return build([v if random.random() > .25 or i == 0 else None for i, v in enumerate(vals)])
    random.seed(1)
    for _ in range(300):
        t = rnd(random.randint(1, 12))
        s = c.serialize(t)
        assert c.serialize(c.deserialize(s)) == s
        assert G["maxDepth"](t) == depth_of(t)
        lv = G["levelOrder"](t)
        assert len(lv) == depth_of(t)
_tests()

# ================================================================= TRACES (插桩)


def post_trace(root, step_fn, init=None):
    """通用 post-order 插桩: step_fn(node, Lrec, Rrec, state) -> (ret, text_lines, extra)"""
    rows, ret = [], {}
    state = dict(init or {})

    def go(n):
        if not n:
            return None
        lr = go(n.left)
        rr = go(n.right)
        val, lines = step_fn(n, lr, rr, state)
        ret[n.val] = val
        rows.append(dict(cur=n.val, ret=dict(ret), lines=lines, state=dict(state)))
        return val
    go(root)
    return rows, state


def role_for(row, v, visited_color=DONE):
    if v == row["cur"]:
        return (GREEN, True)
    if v in row["ret"]:
        return (visited_color, False)
    return (TODO, False)


HDR_Y = 64


def trace_frame(width, title, l1, l2, cols):
    s_h = 0
    return None


def run_trace(name, title, desc, root, rows, l1, l2, colx, colnames, row_draw, footer, legend,
              dx=32, dy=30, tree_x=100, min_rh=0, label_fn=None, state_fn=None, tags=None, extra_h=0):
    D = depth_of(root)
    rh = max((D - 1) * dy + 46, min_rh)
    H = 84 + rh * len(rows) + 14 + len(footer) * 22 + 30 + extra_h
    s = Svg(680, H, title, desc)
    s.t(40, 18, l1)
    s.t(40, 38, l2)
    for x, nm in zip(colx, colnames):
        s.t(x, HDR_Y, nm, 14, fill=SUB)
    s.sep(74)
    y = 84
    for i, row in enumerate(rows):
        top, mid = y, y + rh / 2
        s.t(40, mid - 9, "step %d" % (i + 1), 14, bold=True)
        s.t(40, mid + 9, "node %s" % row["cur"], 12, fill=SUB)
        st = {v: (state_fn(row, v) if state_fn else role_for(row, v)) for v in layout(root, 1, 1)}
        labels = label_fn(row) if label_fn else {}
        draw_tree(s, root, tree_x + 12, top + 26, dx, dy, st, labels, r=13, tags=tags)
        row_draw(s, row, top, rh)
        y += rh
        s.sep(y - 2)
    y += 8
    for ln in footer:
        txt, bold, col = ln
        s.t(40, y + 6, txt, 14, fill=col, bold=bold)
        y += 22
    s.legend(y + 14, legend)
    s.save(name)


def lines_draw(x0, per_line=None):
    def draw(s, row, top, rh):
        ls = row["lines"]
        n = len(ls)
        gap = 20
        y0 = top + rh / 2 - (n - 1) * gap / 2
        for i, ln in enumerate(ls):
            txt, bold, col = ln
            s.t(x0, y0 + i * gap, txt, 14 if bold else 12 if len(txt) > 30 else 14, fill=col, bold=bold)
    return draw


def fmt(v):
    return "-inf" if v == float("-inf") else str(v)


# ----------------------------------------------------------- trace: max depth
T_DEPTH = build([3, 9, 20, None, None, 15, 7])


def depth_step(n, lr, rr, st):
    l, r = lr or 0, rr or 0
    v = 1 + max(l, r)
    ls = "左 = %d%s" % (l, " (None)" if not n.left else "")
    rs = "右 = %d%s" % (r, " (None)" if not n.right else "")
    return v, [(ls + " · " + rs, False, SUB),
               ("return 1 + max(%d, %d) = %d" % (l, r, v), True, GREEN[2])]


rows, _ = post_trace(T_DEPTH, depth_step)
assert rows[-1]["ret"][3] == 3 and [r["cur"] for r in rows] == [9, 15, 7, 20, 3]
run_trace("max_depth_trace.svg", "Maximum Depth 的 post-order trace",
          "tree [3, 9, 20, None, None, 15, 7]; 每一行是一个 node 返回的时刻",
          T_DEPTH, rows,
          "每一步: 左、右子树的深度已经算好 → 当前 node 合并 → return 给父亲",
          "return 1 + max(左深度, 右深度) · None 的深度是 0 · 箭头旁的数字 = 该 node 返回的值",
          [40, 100, 380], ["step", "tree (灰 = 已返回, 橙圈 = 当前)", "当前 node 的合并"],
          lines_draw(380),
          [("答案 = 根 node 3 的返回值 = 3", True, INK)],
          [(GREEN, True, "当前 node"), (DONE, False, "已返回"), (TODO, False, "还没访问")],
          dx=34, dy=32, tree_x=122,
          label_fn=lambda row: {v: ("→%s" % r, GREEN[2] if v == row["cur"] else "#6B6A65", v == row["cur"])
                                for v, r in row["ret"].items()})

# ----------------------------------------------------------- trace: diameter
T_DIAM = build([1, 2, 3, 4, 5, None, None, 6, None, None, 7])


def diam_step(n, lr, rr, st):
    l, r = lr or 0, rr or 0
    old = st["best"]
    st["best"] = max(old, l + r)
    v = 1 + max(l, r)
    changed = st["best"] != old
    return v, [("L = %d, R = %d" % (l, r), False, SUB),
               ("best = max(%d, %d + %d) = %d" % (old, l, r, st["best"]), changed,
                GREEN[2] if changed else INK),
               ("return 1 + max(%d, %d) = %d" % (l, r, v), False, INK)]


rows, st = post_trace(T_DIAM, diam_step, {"best": 0})
assert st["best"] == 4 and [r["cur"] for r in rows] == [6, 4, 7, 5, 2, 3, 1]


def diam_draw(s, row, top, rh):
    lines_draw(380)(s, row, top, rh)
    s.t(560, top + rh / 2, "best = %d" % row["state"]["best"], 14, fill=SUB)


run_trace("diameter_trace.svg", "Diameter of Binary Tree 的 post-order trace",
          "tree [1, 2, 3, 4, 5, None, None, 6, None, None, 7]; 答案 4 = 路径 6-4-2-5-7, 拐点在 node 2",
          T_DIAM, rows,
          "L、R = 左、右子树的 height (点数) · best = 目前见过的最长路径 (边数) · 初值 0",
          "每步: 先更新 best (经过本 node 的路径 = L + R), 再 return 1 + max(L, R) 给父亲",
          [40, 100, 380, 560], ["step", "tree (灰 = 已返回, 橙圈 = 当前)", "当前 node 的合并", "全局"],
          diam_draw,
          [("答案 = best = 4 (在 step 5 的 node 2 更新, 不是根)", True, INK),
           ("根 node 1: L + R = 3 + 1 = 4, 也是 4, 没有超过, best 不变", False, SUB)],
          [(GREEN, True, "当前 node"), (DONE, False, "已返回"), (TODO, False, "还没访问")],
          dx=30, dy=30, tree_x=106,
          label_fn=lambda row: {v: ("→%s" % r, GREEN[2] if v == row["cur"] else "#6B6A65", v == row["cur"])
                                for v, r in row["ret"].items()})

# ----------------------------------------------------------- trace: max path sum
T_PATH = build([-10, -5, 20, None, None, 15, 7])
NEG = float("-inf")


def path_step(n, lr, rr, st):
    lg = max(lr or 0, 0)
    rg = max(rr or 0, 0)
    old = st["best"]
    cand = n.val + lg + rg
    st["best"] = max(old, cand)
    v = n.val + max(lg, rg)
    changed = st["best"] != old
    lraw = "None" if not n.left else str(lr)
    rraw = "None" if not n.right else str(rr)
    return v, [("L = max(%s, 0) = %d, R = max(%s, 0) = %d" % (lraw, lg, rraw, rg), False, SUB),
               ("best = max(%s, %d + %d + %d) = %s" % (fmt(old), n.val, lg, rg, fmt(st["best"])),
                changed, GREEN[2] if changed else INK),
               ("return %d + max(%d, %d) = %d" % (n.val, lg, rg, v), False, INK)]


rows, st = post_trace(T_PATH, path_step, {"best": NEG})
assert st["best"] == 42 and [r["cur"] for r in rows] == [-5, 15, 7, 20, -10]
assert rows[3]["ret"][20] == 35 and rows[4]["ret"][-10] == 25


def path_draw(s, row, top, rh):
    lines_draw(364)(s, row, top, rh)


run_trace("max_path_sum_trace.svg", "Binary Tree Maximum Path Sum 的 post-order trace",
          "tree [-10, -5, 20, None, None, 15, 7]; 答案 42 = 15 + 20 + 7, 拐点在 node 20",
          T_PATH, rows,
          "gain(node) = 以 node 为顶、只往下走一条链的最大和 (返回值) · best = 答案 (初值 -inf)",
          "L、R = 左右 gain, 负的取 0 · best 看 node.val + L + R (两边都用) · return 只带一边",
          [40, 100, 364], ["step", "tree (灰 = 已返回, 橙圈 = 当前)", "当前 node 的合并"],
          path_draw,
          [("答案 = best = 42 (step 4 的 node 20: 20 + 15 + 7)", True, INK),
           ("返回值 35 / 25 只是\"能带给父亲的单链\", 都不是答案", False, SUB)],
          [(GREEN, True, "当前 node"), (DONE, False, "已返回"), (TODO, False, "还没访问")],
          dx=34, dy=32, tree_x=124,
          label_fn=lambda row: {v: ("→%s" % r, GREEN[2] if v == row["cur"] else "#6B6A65", v == row["cur"])
                                for v, r in row["ret"].items()})

# ----------------------------------------------------------- trace: validate BST (pre-order, 传参数)
T_VAL = build([5, 3, 8, 2, 6, None, None, 1])
val_rows = []
_seen = {}


def val_go(n, low, high):
    if not n:
        return True
    ok = low < n.val < high
    _seen[n.val] = (low, high)
    val_rows.append(dict(cur=n.val, ret=dict((k, 1) for k in _seen), ok=ok, low=low, high=high,
                         lines=[]))
    if not ok:
        return False
    return val_go(n.left, low, n.val) and val_go(n.right, n.val, high)


assert val_go(T_VAL, NEG, float("inf")) is False
assert [r["cur"] for r in val_rows] == [5, 3, 2, 1, 6]
for r in val_rows:
    lo, hi = fmt(r["low"]), fmt(r["high"]).replace("inf", "inf")
    hi = "inf" if r["high"] == float("inf") else hi
    lo = "-inf" if r["low"] == NEG else lo
    n = r["cur"]
    if r["ok"]:
        r["lines"] = [("(low, high) = (%s, %s)" % (lo, hi), False, SUB),
                      ("%s < %d < %s ? 是" % (lo, n, hi), True, GREEN[2]),
                      ("左 (%s, %d) · 右 (%d, %s)" % (lo, n, n, hi), False, SUB)]
    else:
        r["lines"] = [("(low, high) = (%s, %s)" % (lo, hi), False, SUB),
                      ("%s < %d < %s ? 否" % (lo, n, hi), True, RED[2]),
                      ("return False, 一路 and 回去", False, RED[2])]

run_trace("validate_bst_trace.svg", "Validate BST 的 top-down trace",
          "tree [5, 3, 8, 2, 6, None, None, 1]; 6 在 3 的右边 (6 > 3), 但在 5 的左边 (6 > 5 违规)",
          T_VAL, val_rows,
          "pre-order: 先用 (low, high) 检查自己 → 再把更严的区间传给孩子 · 初值 (-inf, inf)",
          "向左: high = node.val · 向右: low = node.val · 只比较 parent 的局部检查会漏掉 6",
          [40, 100, 364], ["step", "tree (灰 = 已检查通过, 橙圈 = 当前)", "当前 node 的区间检查"],
          lines_draw(364),
          [("返回 False: node 6 不在 (3, 5) 内, node 8 根本不用看 (短路)", True, INK)],
          [(GREEN, True, "当前 node"), (RED, True, "违规"), (DONE, False, "已检查通过"), (TODO, False, "还没访问")],
          dx=34, dy=30, tree_x=94,
          state_fn=lambda row, v: ((RED, True) if (v == row["cur"] and not row["ok"]) else role_for(row, v)),
          label_fn=lambda row: {})

# ----------------------------------------------------------- trace: BFS
T_BFS = build([1, 2, 3, 4, 5, None, None, 6])
bfs_rows = []
_q = [T_BFS]
_done = set()
_lv = 0
_right, _zig = [], []
while _q:
    n_ = len(_q)
    start = [x.val for x in _q]
    level = [x.val for x in _q]
    nxt = []
    for x in _q:
        if x.left:
            nxt.append(x.left)
        if x.right:
            nxt.append(x.right)
    zig = level[::-1] if _lv % 2 == 1 else level[:]
    _right.append(level[-1])
    _zig.append(zig)
    bfs_rows.append(dict(cur=level[0], level_nodes=level, done=set(_done), start=start,
                         nxt=[x.val for x in nxt], n=n_, level=level, zig=zig, lv=_lv,
                         right=list(_right)))
    _done |= set(level)
    _q = nxt
    _lv += 1
assert [r["level"] for r in bfs_rows] == G["levelOrder"](T_BFS)
assert _right == G["rightSideView"](T_BFS) and _zig == G["zigzagLevelOrder"](T_BFS)


def bfs_state(row, v):
    if v in row["level_nodes"]:
        return (GREEN, True)
    if v in row["done"]:
        return (DONE, False)
    return (TODO, False)


def bfs_draw(s, row, top, rh):
    mid = top + rh / 2
    cw, ch = 28, 26
    # q 开始
    x = 262
    s.t(x, mid - 32, "len(q) = %d" % row["n"], 12, fill=SUB)
    for i, v in enumerate(row["start"]):
        s.cell(x + i * cw, mid - 14, cw, ch, str(v), GREEN)
    # push 后的下一层
    x2 = 372
    s.t(x2, mid - 32, "弹出 %d 个 · push 孩子" % row["n"], 12, fill=SUB)
    if row["nxt"]:
        for i, v in enumerate(row["nxt"]):
            s.cell(x2 + i * cw, mid - 14, cw, ch, str(v), PLAIN)
    else:
        s.t(x2, mid, "q 空 → 结束", 12, fill=SUB)
    # 输出
    x3 = 500
    s.t(x3, mid - 24, "level = %s" % row["level"], 14, bold=True, fill=GREEN[2])
    s.t(x3, mid, "right += %d" % row["level"][-1], 14, fill=INK)
    s.t(x3, mid + 24, "zigzag: %s%s" % (row["zig"], " (反转)" if row["lv"] % 2 and len(row["level"]) > 1 else ""),
        14 if len(row["level"]) < 2 else 12, fill=INK)


run_trace("level_order_trace.svg", "Level Order / Right Side View / Zigzag 的 BFS trace",
          "tree [1, 2, 3, 4, 5, None, None, 6]; 每一行 = 一层 = 外层 while 的一轮",
          T_BFS, bfs_rows,
          "q = deque · 每轮先记下 n = len(q), 恰好弹出 n 个 = 这一层; 它们的孩子排到队尾 = 下一层",
          "level = 这层的值 · right += level[-1] (右视图) · zigzag: 第 1、3 层反转",
          [40, 96, 262, 372, 500], ["step", "tree (橙圈 = 本层)", "本轮开始的 q", "本轮结束的 q", "输出"],
          bfs_draw,
          [("levelOrder = [[1], [2, 3], [4, 5], [6]]", True, INK),
           ("rightSideView = [1, 3, 5, 6]  (5 和 6 来自左子树, 因为右边没有人挡住)", False, INK),
           ("zigzag = [[1], [3, 2], [4, 5], [6]]", False, INK)],
          [(GREEN, True, "本层 / 队列里的 node"), (PLAIN, False, "下一层"), (DONE, False, "已处理")],
          dx=28, dy=30, tree_x=88, min_rh=100,
          state_fn=bfs_state, label_fn=lambda row: {})
for rr_ in bfs_rows:
    rr_["cur"] = rr_["cur"]

# ----------------------------------------------------------- trace: LCA
T_LCA = build([3, 5, 1, 6, 2])
P_, Q_ = find(T_LCA, 6), find(T_LCA, 2)


def lca_step(n, lr, rr, st):
    # 与 CODE_LCA 同逻辑, 但在 p/q 处不再下探 (这里的 p=6, q=2 都是叶子, 没区别)
    name = lambda x: "None" if x is None else str(x)
    if n is P_ or n is Q_:
        return n.val, [("node %d 就是 %s" % (n.val, "p" if n is P_ else "q"), False, SUB),
                       ("return %d (不再往下)" % n.val, True, GREEN[2])]
    if lr is not None and rr is not None:
        return n.val, [("L = %s, R = %s" % (name(lr), name(rr)), False, SUB),
                       ("L 和 R 都不是 None → p、q 分居两侧", True, GREEN[2]),
                       ("return root = %d  ★ LCA" % n.val, True, GREEN[2])]
    v = lr if lr is not None else rr
    return v, [("L = %s, R = %s" % (name(lr), name(rr)), False, SUB),
               ("return L or R = %s" % name(v), True, INK)]


def lca_post(root):
    rows, ret = [], {}

    def go(n):
        if not n:
            return None
        if n is P_ or n is Q_:
            v, lines = lca_step(n, None, None, None)
        else:
            lr = go(n.left)
            rr = go(n.right)
            v, lines = lca_step(n, lr, rr, None)
        ret[n.val] = v
        rows.append(dict(cur=n.val, ret=dict(ret), lines=lines))
        return v
    go(root)
    return rows


rows = lca_post(T_LCA)
assert [r["cur"] for r in rows] == [6, 2, 5, 1, 3] and rows[-1]["ret"][3] == 5
assert G["lowestCommonAncestor"](T_LCA, P_, Q_).val == 5
run_trace("lca_trace.svg", "Lowest Common Ancestor 的 post-order trace",
          "tree [3, 5, 1, 6, 2], p = 6, q = 2; 返回值 = 这棵子树里找到的 p/q, 没找到就是 None",
          T_LCA, rows,
          "p、q 在树上标出 · 遇到 p 或 q 直接 return 它自己 · 左右都找到 → 当前 node 就是 LCA",
          "否则 return L or R, 即把找到的那一个原样往上传 · 箭头旁的数字 = 返回值",
          [40, 100, 364], ["step", "tree (灰 = 已返回, 橙圈 = 当前)", "当前 node 的合并"],
          lines_draw(364),
          [("答案 = 5: node 5 是第一个左右都非 None 的 node", True, INK),
           ("之后 node 3 只是把 5 原样传到根: L = 5, R = None → return L or R = 5", False, SUB)],
          [(GREEN, True, "当前 node"), (DONE, False, "已返回"), (TODO, False, "还没访问")],
          dx=40, dy=32, tree_x=118, tags={6: "p", 2: "q"}, min_rh=124,
          label_fn=lambda row: {v: ("→%s" % r, GREEN[2] if v == row["cur"] else "#6B6A65", v == row["cur"])
                                for v, r in row["ret"].items()})

# ----------------------------------------------------------- trace: kth smallest
T_KTH = build([5, 3, 6, 2, 4, None, None, 1])
kth_rows = []
_stack, _node, _k, _vis = [], T_KTH, 3, []
_first = True
while _stack or _node:
    pushed = []
    while _node:
        _stack.append(_node)
        pushed.append(_node.val)
        _node = _node.left
    if _first and pushed:
        kth_rows.append(dict(cur=_stack[-1].val, stack=[x.val for x in _stack], vis=list(_vis), k=_k,
                             kind="push", pushed=pushed, ret={}))
        _first = False
    _node = _stack.pop()
    _k0 = _k
    _k -= 1
    _vis.append(_node.val)
    kth_rows.append(dict(cur=_node.val, stack=[x.val for x in _stack], vis=list(_vis), k0=_k0, k=_k,
                         kind="pop", right=_node.right.val if _node.right else None, ret={}))
    if _k == 0:
        break
    _node = _node.right
assert kth_rows[-1]["cur"] == 3 and G["kthSmallest"](T_KTH, 3) == 3
assert [r["cur"] for r in kth_rows] == [1, 1, 2, 3], [r["cur"] for r in kth_rows]


def kth_state(row, v):
    if v == row["cur"] and row["kind"] == "pop":
        return (GREEN, True)
    if v == row["cur"]:
        return (PLAIN, True)
    if v in row["vis"]:
        return (DONE, False)
    if v in row["stack"]:
        return (PLAIN, False)
    return (TODO, False)


def kth_draw(s, row, top, rh):
    # 竖直的 stack
    bx, cw, ch = 262, 36, 22
    base = top + rh - 14
    s.t(bx + cw / 2, top + 10, "stack", 12, "middle", SUB)
    s.line(bx - 4, base, bx + cw + 4, base, "#5F5E5A", 1.5)
    for i, v in enumerate(row["stack"]):
        top_ = (i == len(row["stack"]) - 1)
        s.cell(bx, base - (i + 1) * ch, cw, ch, str(v), PLAIN, ring=False)
    if row["stack"]:
        s.t(bx + cw + 8, base - len(row["stack"]) * ch + ch / 2, "← top", 12, fill=SUB)
    x = 372
    mid = top + rh / 2
    if row["kind"] == "push":
        s.t(x, mid - 10, "往左走到底, 一路 push", 14, bold=True)
        s.t(x, mid + 12, "push %s" % ", ".join(str(v) for v in row["pushed"]), 14, fill=GREEN[2])
        s.t(x, mid + 32, "node = None, k = %d" % row["k"], 12, fill=SUB)
    else:
        s.t(x, mid - 22, "pop → %d (第 %d 小)" % (row["cur"], 3 - row["k"]), 14, bold=True, fill=GREEN[2])
        s.t(x, mid, "k = %d - 1 = %d" % (row["k0"], row["k"]), 14, bold=row["k"] == 0,
            fill=RED[2] if row["k"] == 0 else INK)
        if row["k"] == 0:
            s.t(x, mid + 22, "k == 0 → return %d" % row["cur"], 14, bold=True, fill=RED[2])
        else:
            s.t(x, mid + 22, "node = %d.right = %s" % (row["cur"], row["right"] if row["right"] else "None"), 12,
                fill=SUB)


run_trace("kth_smallest_trace.svg", "Kth Smallest in BST 的 iterative inorder trace",
          "BST [5, 3, 6, 2, 4, None, None, 1], k = 3; inorder 依次弹出 1, 2, 3, ...",
          T_KTH, kth_rows,
          "stack = 往左走的路上还没处理的祖先 · 每次 pop 出来的 = inorder 的下一个 = 下一个更大的数",
          "pop 一个就 k -= 1; k 变成 0 就是第 k 小, 立刻返回 · 右子树 4、6 根本没访问",
          [40, 94, 262, 372], ["step", "tree", "stack (底→顶)", "操作"],
          kth_draw,
          [("答案 = 3: 第 3 次 pop 出来的数 (pop 顺序 1, 2, 3 = 从小到大)", True, INK)],
          [(GREEN, True, "刚 pop 的"), (DONE, False, "已 pop"), (PLAIN, False, "在 stack 里")],
          dx=30, dy=30, tree_x=84, min_rh=122, state_fn=kth_state, label_fn=lambda row: {})

# ----------------------------------------------------------- trace: serialize
T_SER = build([1, 2, 3, None, None, 4, 5])
ser_rows, _out = [], []


def ser_go(n):
    if not n:
        _out.append("#")
        return
    start = len(_out)
    _out.append(str(n.val))
    if not n.left and not n.right:
        _out.extend(["#", "#"])
        ser_rows.append(dict(cur=n.val, out=list(_out), new=len(_out) - start, ret={}, leaf=True))
        return
    ser_rows.append(dict(cur=n.val, out=list(_out), new=1, ret={}, leaf=False))
    if n.left:
        ser_go(n.left)
    else:
        _out.append("#")
    if n.right:
        ser_go(n.right)
    else:
        _out.append("#")


ser_go(T_SER)
for i, r in enumerate(ser_rows):
    r["ret"] = {x["cur"]: 1 for x in ser_rows[:i + 1]}
assert ",".join(_out) == ser(T_SER) == "1,2,#,#,3,4,#,#,5,#,#"
assert [r["cur"] for r in ser_rows] == [1, 2, 3, 4, 5]
assert [r["new"] for r in ser_rows] == [1, 3, 1, 3, 3]
for r in ser_rows:
    if r["cur"] == 3:
        r["out"] = r["out"][:5]
SER_DESC = {1: "visit 1: 写 \"1\", 然后进左子树",
            2: "visit 2: 写 \"2\"; 左、右都是 None → 写 \"#\" \"#\"",
            3: "visit 3: 写 \"3\", 然后进左子树 (4)",
            4: "visit 4: 写 \"4\"; 左、右都是 None → 写 \"#\" \"#\"",
            5: "visit 5: 写 \"5\"; 左、右都是 None → 写 \"#\" \"#\""}


def ser_draw(s, row, top, rh):
    mid = top + rh / 2
    cw, ch = 28, 26
    x0 = 262
    s.t(x0, mid - 34, "out (token 序列)", 12, fill=SUB)
    n = len(row["out"])
    for i, tok in enumerate(row["out"]):
        new = i >= n - row["new"]
        s.cell(x0 + i * cw, mid - 20, cw - 2, ch, tok, GREEN if new else PLAIN)
    s.t(x0, mid + 22, SER_DESC[row["cur"]], 12, fill=SUB)


run_trace("serialize_trace.svg", "Serialize 的 pre-order trace",
          "tree [1, 2, 3, None, None, 4, 5]; 绿色 token = 这一步新写进去的",
          T_SER, ser_rows,
          "pre-order: 先写自己, 再递归左、再递归右 · None 也写一个 \"#\" · 每行 = 访问一个 node",
          "out 越写越长, 最后 11 个 token = 5 个 node + 6 个 \"#\" (n 个 node 恰好有 n + 1 个 None)",
          [40, 94, 262], ["step", "tree", "out (token 序列)"],
          ser_draw,
          [("serialize = \"1,2,#,#,3,4,#,#,5,#,#\"  (11 个 token = 5 + 6)", True, INK),
           ("deserialize: 同样顺序 next() 读 token: 1 → 左 build → 2 → # # 回来 → 右 build ...", False, SUB)],
          [(GREEN, True, "当前 node / 新 token"), (DONE, False, "已访问"), (PLAIN, False, "已写的 token")],
          dx=30, dy=30, tree_x=84, min_rh=92,
          state_fn=lambda row, v: (GREEN, True) if v == row["cur"] else (DONE, False) if v in row["ret"] else (TODO, False),
          label_fn=lambda row: {})


# ================================================================= CORE 图
import math  # noqa: E402


def edge_arrow(s, p, c, r=14, up=False, color="#0F6E56", marker="arrowG"):
    (px, py), (cx, cy) = p, c
    L = math.hypot(cx - px, cy - py)
    ux, uy = (cx - px) / L, (cy - py) / L
    a = (px + ux * (r + 2), py + uy * (r + 2))
    b = (cx - ux * (r + 5), cy - uy * (r + 5))
    if up:
        a, b = (cx - ux * (r + 2), cy - uy * (r + 2)), (px + ux * (r + 5), py + uy * (r + 5))
    s.line(a[0], a[1], b[0], b[1], color, 2, marker=marker)
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)


# ---- core 0: 第一性原理
s = Svg(680, 352, "tree 题的两种信息流向", "pre-order 往下传参数, post-order 往上传返回值")
T0 = build([3, 9, 20, None, None, 15, 7])
for ox, up in ((70, False), (400, True)):
    pos = layout(T0, 54, 56)
    xy = draw_tree(s, T0, ox, 108, 54, 56, default=PLAIN, r=15)
    for v, (x, y, par, side) in pos.items():
        if par is None:
            continue
        depth = {9: 2, 20: 2, 15: 3, 7: 3}[v]
        height = {9: 1, 20: 2, 15: 1, 7: 1}[v]
        mx, my = edge_arrow(s, xy[par], xy[v], 15, up=up, color="#D85A30" if up else "#0F6E56",
                            marker="arrowO" if up else "arrowG")
        txt = ("返回 %d" % height) if up else ("depth=%d" % depth)
        col = RED[2] if up else GREEN[2]
        if side == "L":
            s.t(mx - 8, my - 6, txt, 12, "end", col, True)
        else:
            s.t(mx + 8, my - 6, txt, 12, "start", col, True)
s.t(40, 20, "同一棵树 [3, 9, 20, None, None, 15, 7], 信息有两种流向: 看 node 需要谁告诉它", 14, bold=True)
s.t(40, 44, "左: 自顶向下 (pre-order)", 14, fill=GREEN[2], bold=True)
s.t(370, 44, "右: 自底向上 (post-order)", 14, fill=RED[2], bold=True)
s.t(40, 64, "箭头 = 祖先 → 孩子, 传的是参数", 12, fill=SUB)
s.t(370, 64, "箭头 = 孩子 → 父亲, 传的是返回值 (此处 = height)", 12, fill=SUB)
s.sep(236, 40, 640)
s.t(40, 256, "node 需要祖先告诉它什么? → 写成参数", 14, bold=True)
s.t(40, 278, "例: depth、(low, high)、path 上的和", 12, fill=SUB)
s.t(40, 296, "流程: 先检查自己 → 再把更新后的参数传给孩子", 12, fill=SUB)
s.t(370, 256, "node 需要子树告诉它什么? → 写成返回值", 14, bold=True)
s.t(370, 278, "例: height、gain、\"找到的 p 或 q\"", 12, fill=SUB)
s.t(370, 296, "流程: 假设 L、R 已经算好 → 当前 node 只做合并", 12, fill=SUB)
s.sep(314, 40, 640)
s.t(40, 334, "两者可以同时用: 参数往下传约束, 返回值往上传摘要 (本文每题只用其中一种, 最清楚)", 12, fill=SUB)
s.save("first_principles_core.svg")

# ---- core 1: max depth
s = Svg(680, 262, "Maximum Depth 的核心: 假设子树已经算好", "node 只合并两个数")
s.t(40, 20, "不用想子树里面长什么样: 左、右子树的深度已经是对的数, 当前 node 只做一步合并", 14, bold=True)
s.node(170, 78, "node", PLAIN, True, r=22)
for cx, ax, nm, val in ((105, 120, "左子树", 2), (235, 220, "右子树", 1)):
    s.path("M%d 120 L%d 188 L%d 188 Z" % (cx, cx - 52, cx + 52), "#5F5E5A", 1.2, fill="#F1EFE8")
    ux, uy = (cx - 170), (122 - 78)
    Ln = math.hypot(ux, uy)
    s.line(cx - ux / Ln * 4, 120 - uy / Ln * 4, 170 + ux / Ln * 26, 78 + uy / Ln * 26, "#0F6E56", 2, marker="arrowG")
    s.t(cx + (-10 if cx < 170 else 10), 108, str(val), 14, "end" if cx < 170 else "start", GREEN[2], True)
    s.t(cx, 158, nm + " (已算好)", 12, "middle", PLAIN[2])
    s.t(cx, 176, "深度 = %d" % val, 14, "middle", GREEN[2], True)
s.t(330, 60, "当前 node 要做的只有一步:", 14, bold=True)
s.t(330, 86, "depth(node) = 1 + max(2, 1) = 3", 16, fill=GREEN[2], bold=True)
s.t(330, 112, "1 = node 自己这一层", 12, fill=SUB)
s.t(330, 134, "max(2, 1) = 左右两边深的那个", 12, fill=SUB)
s.t(330, 160, "base case: None → 0 (空树没有层)", 12, fill=SUB)
s.t(330, 182, "每个 node 恰好算一次 → O(n)", 12, fill=SUB)
s.sep(204, 40, 640)
s.t(40, 226, "这就是 post-order 的全部: 先拿 L、R, 再 return merge(node, L, R)", 14, bold=True)
s.t(40, 246, "以后每一题只是把\"摘要\"换了 (深度 → 单边链 → 找到的 node), 骨架不变", 12, fill=SUB)
s.save("max_depth_core.svg")

# ---- core 2: diameter, brute vs one pass
s = Svg(680, 340, "Diameter: 暴力重算 height vs 一次 post-order", "每个 node 被走过的次数")
T2 = T_DIAM
s.t(40, 20, "同一棵树, 数一数每个 node 被 height() 走过几次 (×k)", 14, bold=True)
s.t(40, 44, "暴力: 每个 node 重新调 height()", 14, fill=RED[2], bold=True)
s.t(370, 44, "一次 post-order: height 顺手更新 best", 14, fill=GREEN[2], bold=True)
for ox, brute in ((70, True), (400, False)):
    pos = layout(T2, 36, 38)
    labs = {}
    for v, (x, y, par, side) in pos.items():
        k = y // 38 + 1 if brute else 1
        labs[v] = ("×%d" % k, RED[2] if k > 1 else GREEN[2], True)
    draw_tree(s, T2, ox, 100, 36, 38, state={v: ((RED if (brute and pos[v][1] > 0) else GREEN), False) for v in pos},
              labels=labs, r=13, default=PLAIN)
s.t(40, 236, "×k = 这个 node 被 height() 走过的次数 = 深度 + 1", 12, fill=SUB)
s.t(40, 258, "总数 = 1 + 2 + 2 + 3 + 3 + 4 + 4 = 19 (n = 7)", 14, fill=RED[2], bold=True)
s.t(40, 280, "链状 (skewed) 的树: 1 + 2 + … + n → O(n²)", 12, fill=SUB)
s.t(370, 236, "每个 node 只走 ×1: 总数 = 7 = n", 14, fill=GREEN[2], bold=True)
s.t(370, 258, "子树的 height 作为返回值被直接复用", 12, fill=SUB)
s.t(370, 280, "不再重新往下数 → O(n)", 12, fill=SUB)
s.sep(298, 40, 640)
s.t(40, 320, "浪费的是: 父亲算过的 height, 子节点又从头数一遍. 返回值把它带上来, 就不用再数", 12, fill=SUB)
s.save("diameter_core.svg")

# ---- core 3: max path sum — 答案 vs 返回值
s = Svg(680, 372, "Max Path Sum: 拐点更新答案, 返回值只带一边", "同一个 node 20, 两个不同的用途")
s.t(40, 20, "同一个 node 20 (L = 15, R = 7), 做两件不同的事", 14, bold=True)
T3 = T_PATH
s.t(40, 46, "① 答案 best: 两边都用", 14, fill=GREEN[2], bold=True)
s.t(370, 46, "② 返回值: 只带一边给父亲", 14, fill=RED[2], bold=True)
for ox, hot, kind in ((50, {(20, 15), (20, 7)}, "A"), (380, {(-10, 20), (20, 15)}, "B")):
    st = {}
    if kind == "A":
        st = {20: (GREEN, True), 15: (GREEN, False), 7: (GREEN, False)}
    else:
        st = {-10: (RED, False), 20: (GREEN, True), 15: (GREEN, False)}
    draw_tree(s, T3, ox, 92, 52, 46, state=st, default=DONE, hot_edges=hot, r=15)
s.t(40, 226, "路径 15 - 20 - 7 呈 ∧ 形, 在 20 拐弯", 12, fill=SUB)
s.t(40, 248, "best = max(best, 20 + 15 + 7) = 42", 14, fill=GREEN[2], bold=True)
s.t(40, 268, "拐点 = 路径最高的那个 node, 只此一处能\"两边都用\"", 12, fill=SUB)
s.t(370, 226, "父亲 -10 要往下接, 路径不能分叉", 12, fill=SUB)
s.t(370, 248, "return 20 + max(15, 7) = 35", 14, fill=RED[2], bold=True)
s.t(370, 268, "只能带 15 那一边; 带 7 不会更大", 12, fill=SUB)
s.sep(288, 40, 640)
s.t(40, 312, "clamp: 负的链不如不接. -10 看左边: L = max(-5, 0) = 0", 14, bold=True)
s.t(40, 334, "所以递归的返回值 (35) ≠ 答案 (42): 答案放在 nonlocal 的 best 里, 在每个 node 的拐点处更新", 12, fill=SUB)
s.t(40, 354, "初值 best = -inf, 因为全部为负时答案是\"最大的那个负数\", 不是 0", 12, fill=SUB)
s.save("max_path_sum_core.svg")

# ---- core 4: validate BST
s = Svg(680, 330, "Validate BST: 约束是从所有祖先累积下来的", "区间 (low, high) 向下传递")
T4 = build([5, 3, 8, 2, 6])
iv = {5: "(-inf, inf)", 3: "(-inf, 5)", 8: "(5, inf)", 2: "(-inf, 3)", 6: "(3, 5)"}
s.t(40, 20, "node 的合法范围由所有祖先决定, 不只是 parent: 把它压成 (low, high) 往下传", 14, bold=True)
labs = {v: (t, RED[2] if v == 6 else SUB, v == 6) for v, t in iv.items()}
draw_tree(s, T4, 120, 84, 58, 62, state={6: (RED, True), 5: (PLAIN, False), 3: (PLAIN, False), 8: (PLAIN, False),
                                       2: (PLAIN, False)}, labels=labs, r=15, default=PLAIN)
s.t(452, 84, "向左走: high = node.val", 14, fill=GREEN[2], bold=True)
s.t(452, 106, "(左子树必须比 node 小)", 12, fill=SUB)
s.t(452, 134, "向右走: low = node.val", 14, fill=GREEN[2], bold=True)
s.t(452, 156, "(右子树必须比 node 大)", 12, fill=SUB)
s.t(452, 188, "node 6 在 (3, 5) 之外", 14, fill=RED[2], bold=True)
s.t(452, 210, "→ return False", 14, fill=RED[2], bold=True)
s.sep(236, 40, 640)
s.t(40, 258, "只做局部检查 (left < node < right) 会漏掉它:", 14, bold=True)
s.t(40, 280, "3 < 6 局部成立, 但 6 在 5 的左子树里, 必须 < 5. 5 这条约束只能由祖先一路传下来", 12, fill=SUB)
s.t(40, 300, "暴力做法: 每个 node 去扫整棵左、右子树找 max/min → O(n²). 传区间: 每个 node 比一次 → O(n)", 12, fill=SUB)
s.save("validate_bst_core.svg")

# ---- core 5: BFS len(q) 快照
s = Svg(680, 300, "BFS 分层: for _ in range(len(q))", "len(q) 在每轮开始时只算一次")
s.t(40, 20, "tree [1, 2, 3, 4, 5]: 第 2 轮开始时 q = [2, 3]", 14, bold=True)
s.t(40, 42, "range(len(q)) 的 len(q) 只在循环开始时算一次 = 2, 之后 q 变长也不影响", 12, fill=SUB)
rowsy = [(86, "① 每轮开始, n = 2"), (156, "② popleft 2, push 4, 5"), (226, "③ popleft 3, 没有孩子")]
for y, nm in rowsy:
    s.t(40, y + 14, nm, 14, bold=True)
cw = 40
x0 = 280
# row 1
for i, v in enumerate((2, 3)):
    s.cell(x0 + i * cw, 86, cw - 4, 28, str(v), GREEN)
s.t(x0 + 2 * cw + 10, 100, "← 这 2 个 = 这一层", 12, fill=SUB)
# row 2
s.cell(x0 - 70, 156, cw - 4, 28, "2", RED, dash="4 3")
s.line(x0 - 6, 170, x0 - 28, 170, "#D85A30", 1.5, "4 3", "arrowO")
s.t(x0 - 70, 198, "popleft", 12, fill=RED[2])
s.cell(x0, 156, cw - 4, 28, "3", GREEN)
s.line(x0 + cw - 2, 150, x0 + cw - 2, 190, "#5F5E5A", 1, "4 4")
s.cell(x0 + cw + 4, 156, cw - 4, 28, "4", PLAIN)
s.cell(x0 + 2 * cw + 4, 156, cw - 4, 28, "5", PLAIN)
s.t(x0 + 3 * cw + 14, 170, "← 4、5 是下一层, 排在队尾", 12, fill=SUB)
# row 3
s.cell(x0 - 70, 226, cw - 4, 28, "3", RED, dash="4 3")
s.line(x0 - 6, 240, x0 - 28, 240, "#D85A30", 1.5, "4 3", "arrowO")
s.t(x0 - 70, 268, "popleft", 12, fill=RED[2])
s.line(x0 - 2, 220, x0 - 2, 260, "#5F5E5A", 1, "4 4")
s.cell(x0 + 4, 226, cw - 4, 28, "4", PLAIN)
s.cell(x0 + cw + 4, 226, cw - 4, 28, "5", PLAIN)
s.t(x0 + 2 * cw + 14, 240, "← 本层弹完 2 次, for 结束; level = [2, 3]", 12, fill=SUB)
s.legend(288, [(GREEN, False, "本层"), (PLAIN, False, "下一层"), (RED, False, "弹出")])
s.save("level_order_core.svg")

# ---- core 6: LCA 三种情况
s = Svg(680, 318, "LCA 的返回值语义", "三种合并情况")
s.t(40, 20, "返回值 = 这棵子树里\"找到的 p 或 q\" (什么都没找到 = None). 当前 node 只有三种情况:", 14, bold=True)
cases = [(30, "① p、q 分居两侧", ("p", "q"), "return root", "if L and R: return root", "root 是拐点 = LCA"),
         (250, "② 只有一侧找到", (None, "q"), "return R", "return L or R", "原样往上传"),
         (470, "③ node 自己就是 p", None, "return root", "if root is p or q: return root", "不用再往下看")]
for x, title, kids, res, code, why in cases:
    cx = x + 90
    s.t(x, 54, title, 14, fill=GREEN[2], bold=True)
    s.node(cx, 100, "node", GREEN if kids and None not in kids else PLAIN, kids is None, r=22)
    if kids:
        for dx_, k, nm in ((-48, kids[0], "L"), (48, kids[1], "R")):
            role = GREEN if k else TODO
            s.line(cx + dx_ * 0.4, 118, cx + dx_, 148, "#898781", 1.2)
            s.node(cx + dx_, 160, nm, role, False, r=14, dash=None if k else "3 3")
            s.t(cx + dx_, 192, ("→ " + k) if k else "→ None", 12, "middle", GREEN[2] if k else SUB, bool(k))
    else:
        for dx_, nm in ((-48, "L"), (48, "R")):
            s.line(cx + dx_ * 0.4, 118, cx + dx_, 148, "#B4B2A9", 1.2, "3 3")
            s.node(cx + dx_, 160, nm, TODO, False, r=14, dash="3 3")
        s.t(cx, 192, "(不递归)", 12, "middle", SUB)
    s.t(x, 226, res, 14, fill=GREEN[2], bold=True)
    s.t(x, 248, why, 12, fill=SUB)
    s.t(x, 270, code, 12, fill=SUB)
s.sep(286, 40, 640)
s.t(40, 304, "第 ③ 种的依据: 若 q 在 p 下面, p 就是 LCA; 若 q 不在下面, 也会由别处的非 None 在更上层汇合", 12, fill=SUB)
s.save("lca_core.svg")

# ---- core 7: kth smallest
s = Svg(680, 352, "BST 的 inorder = 排好序", "左 < node < 右, 所以 左→自己→右 依次读出来是升序")
T7 = build([5, 3, 6, 2, 4, None, None, 1])
ox, oy, dx_, dy_ = 150, 70, 46, 44
xy = draw_tree(s, T7, ox, oy, dx_, dy_, state={3: (GREEN, True)}, default=PLAIN, r=14)
s.t(40, 20, "BST: 每个 node 的左子树全部 < node < 右子树全部. inorder = 左 → 自己 → 右", 14, bold=True)
cy = 70 + 3 * 44 + 40
s.t(40, cy + 14, "inorder:", 14, bold=True)
for i, v in enumerate(range(1, 7)):
    x = xy[v][0]
    s.line(x, xy[v][1] + 15, x, cy - 2, "#B4B2A9", 1, "3 3")
    s.cell(x - 19, cy, 38, 28, str(v), GREEN if v == 3 else PLAIN, ring=(v == 3))
x1, x4 = xy[1][0] - 19, xy[4][0] + 19
s.line(x1, cy + 40, x4, cy + 40, "#0F6E56", 2)
s.t((x1 + x4) / 2, cy + 58, "5 的左子树: 全部 < 5", 12, "middle", GREEN[2])
s.line(xy[6][0] - 19, cy + 40, xy[6][0] + 19, cy + 40, "#993C1D", 2)
s.t(xy[6][0] + 22, cy + 58, "右子树: > 5", 12, "end", RED[2])
s.t(430, 84, "k = 3 → 数到第 3 个就停", 14, bold=True)
s.t(430, 108, "橙圈 = 第 3 个 = 3", 12, fill=SUB)
s.t(430, 140, "暴力: 全部收集 → sort", 12, fill=RED[2])
s.t(430, 160, "O(n log n) 时间, O(n) 空间", 12, fill=RED[2])
s.t(430, 190, "利用 BST 性质: 不用 sort", 12, fill=GREEN[2])
s.t(430, 210, "且能提前停: O(h + k)", 12, fill=GREEN[2])
s.t(40, 338, "node 的虚线 = 它在 inorder 序列里的位置: 画 tree 时按 inorder 排 x 坐标, 同一列就是同一个数", 12, fill=SUB)
s.save("kth_smallest_core.svg")

# ---- core 8: serialize
s = Svg(680, 340, "Serialize: pre-order + None 标记", "token 序列 = 递归结构的拍平")
toks = ser(T_SER).split(",")
s.t(40, 20, "tree [1, 2, 3, None, None, 4, 5] → 11 个 token. 每棵子树都是一段连续的 token", 14, bold=True)
x0, cw = 54, 52
for i, tk in enumerate(toks):
    s.cell(x0 + i * cw, 44, cw - 6, 30, tk, DONE if tk == "#" else PLAIN)
def span(a, b, y, text, role):
    xa, xb = x0 + a * cw, x0 + b * cw + cw - 6
    s.rect(xa, y, xb - xa, 26, role)
    s.t((xa + xb) / 2, y + 13, text, 12, "middle", role[2])
span(0, 0, 92, "根 1", GREEN)
span(1, 3, 92, "左子树: 2 # #", PLAIN)
span(4, 10, 92, "右子树: 3 4 # # 5 # #", PLAIN)
span(4, 4, 134, "根 3", GREEN)
span(5, 7, 134, "左: 4 # #", PLAIN)
span(8, 10, 134, "右: 5 # #", PLAIN)
s.sep(180, 40, 640)
s.t(40, 202, "serialize: dfs(node) = 写 node, dfs(左), dfs(右); None 写 \"#\"", 14, bold=True)
s.t(40, 226, "deserialize: build() 读一个 token; \"#\" → None, 否则建 node", 14, bold=True)
s.t(40, 248, "left = build() 会吃掉左子树的全部 token, 剩下的正好是右子树的", 12, fill=SUB)
s.t(40, 268, "为什么要 \"#\": 没有它, \"1,2,3\" 对应多种形状; 有了它, 每棵子树的长度由 token 自己决定", 12, fill=SUB)
s.t(40, 288, "为什么用 iterator: 两次 build() 共享同一个读指针, 谁先调用谁先吃", 12, fill=SUB)
s.t(40, 308, "对比: 层序 + 下标 (2i+1, 2i+2) 要为每个空位置留格子, 链状 tree 需要 O(2^h) 空间", 12, fill=SUB)
s.save("serialize_core.svg")

# ================================================================= HTML
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '11_tree_doc.py'), encoding='utf-8').read())
