"""12 · Graph 生成脚本。
运行: cd build && python3 -I 12_graph.py
所有 SVG 由下面的 sim_* 函数实际跑算法后生成 (图里的数字 = 代码实际跑出来的数字),
写到 docs/svg/12-graph/*.svg, 再内联进 docs/12-graph.html。
"""
import heapq
import html as _html
import os
import sys
from collections import deque, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import doclib as d  # noqa: E402

SLUG = "12-graph"
SVG_DIR = os.path.join(d.ROOT, "docs", "svg", SLUG)
os.makedirs(SVG_DIR, exist_ok=True)

# ---------------------------------------------------------------- SVG toolkit
FONT = 'ui-sans-serif, system-ui, -apple-system, "PingFang SC", sans-serif'
ROLE = {  # fill, stroke, text
    "new": ("#E1F5EE", "#0F6E56", "#085041"),
    "rem": ("#FAECE7", "#993C1D", "#712B13"),
    "oth": ("#F1EFE8", "#5F5E5A", "#444441"),
    "plain": ("#FFFFFF", "#B4B2A9", "#444441"),
    "water": ("#FFFFFF", "#D3D1C7", "#B4B2A9"),
}
INK, SUB = "#0B0B0B", "#52514E"
ARROW = {"gray": "#5F5E5A", "red": "#D85A30", "green": "#0F6E56"}


def esc(s):
    return _html.escape(str(s), quote=False)


class Svg:
    def __init__(self, h, title, desc=""):
        self.h = h
        self.title = title
        self.desc = desc
        self.b = []

    def text(self, x, y, t, size=12, fill=SUB, w=400, anchor="start"):
        self.b.append(
            '<text x="%s" y="%s" font-size="%d" font-weight="%d" fill="%s" '
            'text-anchor="%s" dominant-baseline="central">%s</text>'
            % (x, y, size, w, fill, anchor, esc(t)))

    def rect(self, x, y, w, h, role="oth", rx=4, dash=False, sw=1):
        f, s, _ = ROLE[role]
        self.b.append(
            '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" '
            'stroke="%s" stroke-width="%s"%s/>'
            % (x, y, w, h, rx, f, s, sw,
               ' stroke-dasharray="4 3"' if dash else ""))

    def box(self, x, y, w, h, label, role="oth", size=14, key=False,
            dash=False, bold=True):
        self.rect(x, y, w, h, role, dash=dash)
        self.text(x + w / 2, y + h / 2, label, size, ROLE[role][2],
                  500 if bold else 400, "middle")
        if key:
            self.b.append(
                '<rect x="%s" y="%s" width="%s" height="%s" rx="6" fill="none" '
                'stroke="#EF9F27" stroke-width="2.5"/>'
                % (x - 3, y - 3, w + 6, h + 6))

    def node(self, cx, cy, label, role="oth", r=16, key=False, size=14,
             dash=False):
        f, s, t = ROLE[role]
        self.b.append(
            '<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" '
            'stroke-width="1"%s/>'
            % (cx, cy, r, f, s, ' stroke-dasharray="4 3"' if dash else ""))
        self.text(cx, cy, label, size, t, 500, "middle")
        if key:
            self.b.append(
                '<circle cx="%s" cy="%s" r="%s" fill="none" stroke="#EF9F27" '
                'stroke-width="2.5"/>' % (cx, cy, r + 3))

    def line(self, x1, y1, x2, y2, color="#898781", dash=False, arrow=None,
             sw=1.5):
        m = ' marker-end="url(#ar-%s)"' % arrow if arrow else ""
        self.b.append(
            '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" '
            'stroke-width="%s"%s%s/>'
            % (x1, y1, x2, y2, color, sw,
               ' stroke-dasharray="4 3"' if dash else "", m))

    def path(self, dstr, color="#898781", dash=False, arrow=None, sw=1.5):
        m = ' marker-end="url(#ar-%s)"' % arrow if arrow else ""
        self.b.append(
            '<path d="%s" fill="none" stroke="%s" stroke-width="%s"%s%s/>'
            % (dstr, color, sw, ' stroke-dasharray="4 3"' if dash else "", m))

    def edge(self, a, b, r1=16, r2=16, color="#898781", dash=False,
             arrow=None, sw=1.5, bend=0):
        """a, b 是圆心坐标。bend != 0 时画成二次曲线 (给双向边用)。"""
        (x1, y1), (x2, y2) = a, b
        dx, dy = x2 - x1, y2 - y1
        L = (dx * dx + dy * dy) ** 0.5
        ux, uy = dx / L, dy / L
        if bend:
            nx, ny = -uy, ux
            cx, cy = (x1 + x2) / 2 + nx * bend, (y1 + y2) / 2 + ny * bend
            # 起终点沿切线方向缩短
            sx, sy = cx - x1, cy - y1
            sl = (sx * sx + sy * sy) ** 0.5
            ex, ey = cx - x2, cy - y2
            el = (ex * ex + ey * ey) ** 0.5
            p1 = (x1 + sx / sl * r1, y1 + sy / sl * r1)
            p2 = (x2 + ex / el * (r2 + (4 if arrow else 0)),
                  y2 + ey / el * (r2 + (4 if arrow else 0)))
            self.path("M%.1f %.1f Q%.1f %.1f %.1f %.1f"
                      % (p1[0], p1[1], cx, cy, p2[0], p2[1]),
                      color, dash, arrow, sw)
            return
        pad = 4 if arrow else 0
        self.line(round(x1 + ux * r1, 1), round(y1 + uy * r1, 1),
                  round(x2 - ux * (r2 + pad), 1), round(y2 - uy * (r2 + pad), 1),
                  color, dash, arrow, sw)

    def hsep(self, y, x1=40, x2=640):
        self.line(x1, y, x2, y, "#B4B2A9", dash=True, sw=0.8)

    def legend(self, y, items, x=40, maxx=640):
        """items: [(role, label)] 每项: 色块 + 文字, 放不下就换行。返回最后一行的 y"""
        cx = x
        for role, label in items:
            tw = sum(12 if ord(ch) > 127 else 6.6 for ch in label)
            if cx + 20 + tw > maxx and cx > x:
                cx, y = x, y + 22
            if role == "key":
                self.b.append(
                    '<rect x="%s" y="%s" width="14" height="14" rx="3" '
                    'fill="none" stroke="#EF9F27" stroke-width="2.5"/>'
                    % (cx, y - 7))
            else:
                self.rect(cx, y - 7, 14, 14, role, rx=3)
            self.text(cx + 20, y, label, 12, SUB)
            cx += 20 + tw + 22
        return y

    def out(self, name):
        defs = "".join(
            '<marker id="ar-%s" viewBox="0 0 10 10" refX="8" refY="5" '
            'markerWidth="6" markerHeight="6" orient="auto">'
            '<path d="M2 1L8 5L2 9" fill="none" stroke="%s" stroke-width="1.6" '
            'stroke-linecap="round" stroke-linejoin="round"/></marker>'
            % (k, v) for k, v in ARROW.items())
        s = ('<svg width="100%%" viewBox="0 0 680 %d" role="img" '
             'xmlns="http://www.w3.org/2000/svg" font-family=\'%s\'>'
             '<title>%s</title><desc>%s</desc><defs>%s</defs>%s</svg>\n'
             % (self.h, FONT, esc(self.title), esc(self.desc or self.title),
                defs, "\n".join(self.b)))
        with open(os.path.join(SVG_DIR, name), "w", encoding="utf-8") as f:
            f.write(s)
        return "%s/%s" % (SLUG, name)


def grid_cells(s, x, y, grid, roles, cw=30, ch=28, labels=None, keys=()):
    """画一个 grid。roles[r][c] in ROLE 的 key; labels[r][c] 为格内文字"""
    for r, row in enumerate(grid):
        for c, _ in enumerate(row):
            role = roles[r][c]
            lab = labels[r][c] if labels else ""
            s.box(x + c * cw, y + r * ch, cw, ch, lab, role, size=14,
                  key=(r, c) in keys)

# ------------------------------------------------------------ solution code
# 文档里展示的代码 = 下面这些字符串; 同一份字符串会被 exec 后用例子验证。
CODE = {}

CODE["template"] = '''
from collections import deque

# ---- BFS: 从 start 一层一层往外扩 (无权图最短路) ----
def bfs(start, neighbors):
    visited = {start}               # 入队时就标记 (不是出队时), 否则同一点会重复入队
    q = deque([start])
    while q:
        u = q.popleft()
        for v in neighbors(u):      # neighbors(u): 邻接表 / grid 四个方向 / 改一个字母
            if v not in visited:
                visited.add(v)      # 每个点只会入队一次 → 总工作量 O(V + E)
                q.append(v)

# ---- DFS: 沿一条路走到底, 走不动再回头 ----
def dfs(u, neighbors, visited):
    visited.add(u)                  # 进来就标记
    for v in neighbors(u):
        if v not in visited:
            dfs(v, neighbors, visited)

# ---- grid 是隐式 graph: 格子 = 点, 上下左右 = 边, 不用建邻接表 ----
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))
def grid_neighbors(r, c, m, n):
    for dr, dc in DIRS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < m and 0 <= nc < n:     # 出界 = 没有这条边
            yield nr, nc
'''

CODE["islands"] = '''
def numIslands(grid):                       # grid[r][c] 是 "1" (陆) 或 "0" (水)
    m, n = len(grid), len(grid[0])

    def dfs(r, c):
        if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] != "1":
            return                          # 出界 / 水 / 已经 sink 过, 都不用再走
        grid[r][c] = "0"                    # 进来先 sink: 这一行就是 visited 标记
        for dr, dc in DIRS:                 # 4 个方向 = 4 条边
            dfs(r + dr, c + dc)

    count = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] == "1":           # 遇到还没处理的陆地 = 发现一个新 island
                count += 1                  # 每个 island 只会在它的第一个格子触发一次
                dfs(r, c)                   # 把整块 island sink 掉, 之后扫描不会再碰到它
    return count
'''

CODE["maxarea"] = '''
def maxAreaOfIsland(grid):
    m, n = len(grid), len(grid[0])

    def dfs(r, c):                          # 返回: 从 (r, c) 能走到的陆地格数
        if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] != 1:
            return 0
        grid[r][c] = 0
        return 1 + sum(dfs(r + dr, c + dc) for dr, dc in DIRS)   # 改动: void → 返回面积

    return max(dfs(r, c) for r in range(m) for c in range(n))
'''

CODE["rotting"] = '''
def orangesRotting(grid):                   # 0 空, 1 新鲜, 2 烂
    m, n = len(grid), len(grid[0])
    q, fresh = deque(), 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 2:
                q.append((r, c))            # 所有初始烂橘子一起入队 = 第 0 层 (multi-source)
            elif grid[r][c] == 1:
                fresh += 1
    minutes = 0
    while q and fresh:
        for _ in range(len(q)):             # 只处理"当前这一层", 新入队的留给下一分钟
            r, c = q.popleft()
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                    grid[nr][nc] = 2        # 变烂 = 标记 visited
                    fresh -= 1
                    q.append((nr, nc))
        minutes += 1                        # 一层 = 一分钟
    return -1 if fresh else minutes         # 还有新鲜的 = 被墙/空格隔开, 永远烂不到
'''

CODE["ladder"] = '''
def ladderLength(beginWord, endWord, wordList):
    words = set(wordList)                   # 同时充当 "没访问过的点集合"
    if endWord not in words:
        return 0
    q, level = deque([beginWord]), 1        # level = 路径上的单词个数
    while q:
        for _ in range(len(q)):             # 一层一层: 同层的单词离 beginWord 一样远
            w = q.popleft()
            if w == endWord:
                return level                # BFS 第一次碰到 endWord 就是最短
            for i in range(len(w)):         # 邻居 = 改一个字母后还在词典里的词
                for ch in "abcdefghijklmnopqrstuvwxyz":
                    nw = w[:i] + ch + w[i + 1:]
                    if nw in words:
                        words.remove(nw)    # remove = 标记 visited, 之后不会再入队
                        q.append(nw)
        level += 1
    return 0
'''

CODE["canfinish"] = '''
def canFinish(numCourses, prerequisites):   # prerequisites[i] = [course, pre]: 先 pre 后 course
    graph = [[] for _ in range(numCourses)]
    indegree = [0] * numCourses             # indegree[v] = v 还有几门前置课没上完
    for course, pre in prerequisites:
        graph[pre].append(course)           # 边 pre → course
        indegree[course] += 1
    q = deque(i for i in range(numCourses) if indegree[i] == 0)   # 没有前置的先上
    done = 0
    while q:
        u = q.popleft()
        done += 1                           # u 上完了
        for v in graph[u]:
            indegree[v] -= 1                # v 少了一门前置
            if indegree[v] == 0:            # 前置全上完 → v 可以上了
                q.append(v)
    return done == numCourses               # 有环 → 环上的点 indegree 永远 > 0 → done 不够
'''

CODE["findorder"] = '''
def findOrder(numCourses, prerequisites):
    graph = [[] for _ in range(numCourses)]
    indegree = [0] * numCourses
    for course, pre in prerequisites:
        graph[pre].append(course)
        indegree[course] += 1
    q = deque(i for i in range(numCourses) if indegree[i] == 0)
    order = []                              # 改动 1: done 计数 → 记录 pop 的顺序
    while q:
        u = q.popleft()
        order.append(u)
        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                q.append(v)
    return order if len(order) == numCourses else []    # 改动 2: 有环就没有合法顺序
'''

CODE["clone"] = '''
def cloneGraph(node):                       # Node 有 .val 和 .neighbors (list[Node])
    if not node:
        return None
    old2new = {}                            # Hash Table: 原节点 → 它的副本 (同时当 visited)

    def dfs(old):
        if old in old2new:                  # 已经复制过 → 直接返回副本, 不再递归
            return old2new[old]
        copy = Node(old.val)
        old2new[old] = copy                 # 必须在递归 neighbor 之前登记, 否则环会无限递归
        for nb in old.neighbors:
            copy.neighbors.append(dfs(nb))  # 副本的 neighbor 也必须是副本
        return copy

    return dfs(node)
'''

CODE["dsu"] = '''
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))        # parent[x] == x 表示 x 是所在集合的 root
        self.size = [1] * n                 # size[root] = 集合大小 (只对 root 有意义)

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # path compression (halving): 爷爷接管
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                    # 已经在同一集合 → 这条边没有合并任何东西
        if self.size[ra] < self.size[rb]:   # union by size: 小树挂到大树的 root 下
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True
'''

CODE["provinces"] = '''
def findCircleNum(isConnected):             # isConnected[i][j] == 1: i 和 j 直接相连
    n = len(isConnected)
    dsu = DSU(n)
    count = n                               # 开始: 每个人自己一个 province
    for i in range(n):
        for j in range(i + 1, n):
            if isConnected[i][j] and dsu.union(i, j):
                count -= 1                  # 每成功合并一次, 集合数少 1
    return count
'''

CODE["accounts"] = '''
def accountsMerge(accounts):                # accounts[i] = [name, email1, email2, ...]
    dsu = DSU(len(accounts))
    owner = {}                              # email → 第一次见到它的 account 下标
    for i, acc in enumerate(accounts):
        for email in acc[1:]:
            if email in owner:
                dsu.union(i, owner[email])  # 共用 email → 同一个人
            else:
                owner[email] = i
    groups = defaultdict(set)
    for email, i in owner.items():
        groups[dsu.find(i)].add(email)      # 按 root 归并 email
    return [[accounts[r][0]] + sorted(es) for r, es in groups.items()]
'''

CODE["dijkstra"] = '''
def networkDelayTime(times, n, k):          # times[i] = [u, v, w]: u → v 耗时 w
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))
    INF = float("inf")
    dist = [INF] * (n + 1)                  # dist[v] = 目前已知从 k 到 v 的最短时间
    dist[k] = 0
    heap = [(0, k)]                         # min-heap, 按 (dist, node) 排: 先拿"当前最近"的
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:                     # 这是个过期记录: u 之后找到了更短的路
            continue
        for v, w in graph[u]:               # relax: 经过 u 到 v 会不会更短?
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))   # 不删旧记录, 只加新的 (lazy deletion)
    ans = max(dist[1:])
    return -1 if ans == INF else ans        # 有点到不了 → -1
'''

CODE["flights"] = '''
def findCheapestPrice(n, flights, src, dst, k):    # 最多 k 次中转 = 最多 k+1 条边
    dist = [float("inf")] * n
    dist[src] = 0
    for _ in range(k + 1):                  # Bellman-Ford: 一轮 = 多允许走 1 条边
        nxt = dist[:]                       # 用上一轮的 dist 算, 防止一轮里连走多条边
        for u, v, w in flights:
            if dist[u] + w < nxt[v]:
                nxt[v] = dist[u] + w
        dist = nxt
    return -1 if dist[dst] == float("inf") else dist[dst]
'''

# ------------------------------------------------------------ verify
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


def _ns():
    ns = {"deque": deque, "defaultdict": defaultdict, "heapq": heapq,
          "Node": Node}
    exec(CODE["template"], ns)
    for k in ["islands", "maxarea", "rotting", "ladder", "canfinish",
              "findorder", "clone", "dsu", "provinces", "accounts",
              "dijkstra", "flights"]:
        exec(CODE[k], ns)
    return ns


NS = _ns()

# --- islands
ISLAND_GRID = ["11000", "10010", "00110", "00001"]
assert NS["numIslands"]([list(r) for r in ISLAND_GRID]) == 3
assert NS["maxAreaOfIsland"]([[int(x) for x in r] for r in ISLAND_GRID]) == 3
# --- rotting
ROT_GRID = [[2, 1, 1, 1, 1], [1, 1, 0, 1, 1], [0, 1, 1, 1, 2]]
assert NS["orangesRotting"]([r[:] for r in ROT_GRID]) == 3
assert NS["orangesRotting"]([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
assert NS["orangesRotting"]([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1
# --- ladder
LADDER = ("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"])
assert NS["ladderLength"](*LADDER) == 5
assert NS["ladderLength"]("hit", "cog", ["hot", "dot", "dog", "lot", "log"]) == 0
# --- courses
CS1_N = 6
CS1_PRE = [[2, 0], [2, 1], [3, 2], [4, 2], [5, 3], [5, 4]]
CS2_N = 5
CS2_PRE = [[1, 0], [2, 1], [1, 2], [3, 0], [4, 3]]
assert NS["canFinish"](CS1_N, CS1_PRE) is True
assert NS["canFinish"](CS2_N, CS2_PRE) is False
assert NS["findOrder"](CS1_N, CS1_PRE) == [0, 1, 2, 3, 4, 5]
assert NS["findOrder"](CS2_N, CS2_PRE) == []
assert NS["canFinish"](2, [[1, 0], [0, 1]]) is False
# --- clone
def _mk_square():
    ns = [Node(i) for i in (1, 2, 3, 4)]
    for a, b in ((0, 1), (1, 2), (2, 3), (3, 0)):
        ns[a].neighbors.append(ns[b])
        ns[b].neighbors.append(ns[a])
    return ns[0]
_o = _mk_square()
_c = NS["cloneGraph"](_o)
assert _c is not _o and _c.val == 1
_seen = {}
def _walk(x, y):
    if id(x) in _seen:
        return
    _seen[id(x)] = y
    assert x is not y and x.val == y.val
    assert [n.val for n in x.neighbors] == [n.val for n in y.neighbors]
    for a, b in zip(x.neighbors, y.neighbors):
        assert a is not b
        _walk(a, b)
_walk(_o, _c)
assert len(_seen) == 4
# --- provinces
assert NS["findCircleNum"]([[1, 1, 0], [1, 1, 0], [0, 0, 1]]) == 2
assert NS["findCircleNum"]([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) == 3
_acc = [["John", "a@x", "b@x"], ["John", "b@x", "c@x"], ["Mary", "m@x"],
        ["John", "j@x"]]
_r = sorted(NS["accountsMerge"](_acc))
assert _r == [["John", "a@x", "b@x", "c@x"], ["John", "j@x"], ["Mary", "m@x"]]
# --- dijkstra
DJ_TIMES = [[1, 2, 4], [1, 3, 1], [3, 2, 2], [2, 4, 1], [3, 4, 5], [4, 5, 3]]
assert NS["networkDelayTime"](DJ_TIMES, 5, 1) == 7
assert NS["networkDelayTime"]([[1, 2, 1]], 2, 2) == -1
assert NS["networkDelayTime"]([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2) == 2
assert NS["findCheapestPrice"](4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 3, 1) == 700
assert NS["findCheapestPrice"](3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1) == 200
assert NS["findCheapestPrice"](3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0) == 500
# brute-force cross-check of dijkstra vs Bellman-Ford on random graphs
import random
random.seed(1)
for _ in range(200):
    n = random.randint(2, 7)
    ts = [[random.randint(1, n), random.randint(1, n), random.randint(1, 9)]
          for _ in range(random.randint(0, 12))]
    ts = [t for t in ts if t[0] != t[1]]
    k = random.randint(1, n)
    dd = [float("inf")] * (n + 1)
    dd[k] = 0
    for _i in range(n):
        for u, v, w in ts:
            dd[v] = min(dd[v], dd[u] + w)
    exp = max(dd[1:])
    exp = -1 if exp == float("inf") else exp
    assert NS["networkDelayTime"](ts, n, k) == exp
print("all solution asserts OK")

# ------------------------------------------------------------ simulations
def sim_islands():
    g = [list(r) for r in ISLAND_GRID]
    m, n = len(g), len(g[0])
    sunk = {}          # (r,c) -> (island_id, order)
    rows = []
    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))
    count = 0

    def dfs(r, c, order, iid):
        if r < 0 or r >= m or c < 0 or c >= n or g[r][c] != "1":
            return
        g[r][c] = "0"
        order.append((r, c))
        sunk[(r, c)] = (iid, len(order))
        for dr, dc in dirs:
            dfs(r + dr, c + dc, order, iid)

    for r in range(m):
        for c in range(n):
            if g[r][c] == "1":
                count += 1
                order = []
                dfs(r, c, order, count)
                rows.append(dict(start=(r, c), order=order, count=count,
                                 sunk=dict(sunk)))
    assert count == 3
    return rows


def sim_rotting():
    g = [r[:] for r in ROT_GRID]
    m, n = len(g), len(g[0])
    q = deque()
    fresh = 0
    for r in range(m):
        for c in range(n):
            if g[r][c] == 2:
                q.append((r, c))
            elif g[r][c] == 1:
                fresh += 1
    minute_of = {p: 0 for p in q}
    steps = [dict(minute=0, layer=list(q), new=[], fresh=fresh,
                  grid=[r[:] for r in g], minute_of=dict(minute_of))]
    minutes = 0
    while q and fresh:
        layer = list(q)
        new = []
        for _ in range(len(q)):
            r, c = q.popleft()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and g[nr][nc] == 1:
                    g[nr][nc] = 2
                    fresh -= 1
                    q.append((nr, nc))
                    new.append((nr, nc))
        minutes += 1
        for p in new:
            minute_of[p] = minutes
        steps.append(dict(minute=minutes, layer=layer, new=new, fresh=fresh,
                          grid=[r[:] for r in g], minute_of=dict(minute_of),
                          queue=list(q)))
    assert minutes == 3 and fresh == 0
    return steps



# ------------------------------------------------------------ figures (part 1)
def head(s, l1, l2=None):
    s.text(40, 18, l1, 12, SUB)
    if l2:
        s.text(40, 38, l2, 12, SUB)


def fig_first_core():
    # 菱形链: S → A,B → M → C,D → T。无 visited 时 M 处理 2 次, T 处理 4 次。
    names = ["S", "A", "B", "M", "C", "D", "T"]
    edges = [("S", "A"), ("S", "B"), ("A", "M"), ("B", "M"),
             ("M", "C"), ("M", "D"), ("C", "T"), ("D", "T")]
    # 无 visited: 每个点被处理的次数 = 从 S 到它的路径数 (DAG 上 DP)
    cnt = {"S": 1}
    for v in ["A", "B", "M", "C", "D", "T"]:
        cnt[v] = sum(cnt[a] for a, b in edges if b == v)
    total = sum(cnt.values())
    assert cnt == dict(S=1, A=1, B=1, M=2, C=2, D=2, T=4) and total == 13
    s = Svg(392, "没有 visited 与有 visited 的对比")
    head(s, "同一张图: S → A,B → M → C,D → T。两层 diamond: 不记 visited 时, 汇合点被重复处理",
         "数字 ×k = 这个点被处理了 k 次")
    s.text(40, 66, "没有 visited", 14, INK, 500)
    s.text(370, 66, "有 visited (入队/进入时标记)", 14, INK, 500)
    pos = {"S": (0, 105), "A": (-50, 160), "B": (50, 160), "M": (0, 215),
           "C": (-50, 270), "D": (50, 270), "T": (0, 325)}
    for ox, with_vis in ((150, False), (480, True)):
        P = {k: (ox + v[0], v[1]) for k, v in pos.items()}
        skipped = {("B", "M"), ("D", "T")}
        for a, b in edges:
            if with_vis and (a, b) in skipped:
                s.edge(P[a], P[b], 16, 16, ARROW["red"], dash=True, arrow="red")
            else:
                s.edge(P[a], P[b], 16, 16, ARROW["gray"], arrow="gray")
        for k in names:
            x, y = P[k]
            if with_vis:
                s.node(x, y, k, "oth")
                s.text(x + 24, y, "×1", 12, SUB)
            else:
                role = "rem" if cnt[k] > 1 else "oth"
                s.node(x, y, k, role)
                s.text(x + 24, y, "×%d" % cnt[k], 12,
                       ROLE["rem"][2] if cnt[k] > 1 else SUB, 500 if cnt[k] > 1 else 400)
    s.text(150, 355, "共处理 1+1+1+2+2+2+4 = %d 次" % total, 14, INK, 500, "middle")
    s.text(150, 375, "再加一层 diamond 就翻倍: 2^k", 12, SUB, 400, "middle")
    s.text(480, 355, "共处理 7 次 = V", 14, INK, 500, "middle")
    s.text(480, 375, "红虚线: 看到 visited 就跳过 → O(V + E)", 12, SUB, 400, "middle")
    s.line(330, 56, 330, 380, "#B4B2A9", dash=True, sw=0.8)
    return s.out("first_principles_core.svg")


def fig_islands_core():
    s = Svg(300, "grid 是隐式 graph: 4 个方向 = 4 条边")
    head(s, "格子 = 点, 上下左右 = 边。不用建邻接表, 邻居靠 (dr, dc) 算出来",
         "DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))")
    cw, ch, ox, oy = 62, 46, 56, 70
    # 3x3 小 grid, 中心 (1,1)
    for r in range(3):
        for c in range(3):
            role = "new" if (r, c) == (1, 1) else "oth"
            lab = "(r,c)" if (r, c) == (1, 1) else "(r%+d,c%+d)" % (r - 1, c - 1)
            s.box(ox + c * cw, oy + r * ch, cw, ch, lab, role, size=12,
                  key=(r, c) == (1, 1))
    cx, cy = ox + cw * 1.5, oy + ch * 1.5
    s.text(ox + 1.5 * cw, oy + 3 * ch + 18, "中心格的 4 个邻居: (r±1, c) 和 (r, c±1)", 12, SUB, 400, "middle")
    # 右侧: DFS 三道防线
    rx = 330
    s.text(rx, 78, "进入 dfs(r, c) 先过三关, 任何一关不过就 return:", 14, INK, 500)
    lines = [
        ("1. 出界", "r < 0 或 r >= m 或 c < 0 或 c >= n", "没有这条边"),
        ("2. 是水", "grid[r][c] == \"0\"", "不是陆地"),
        ("3. 已 sink", "走过的格子被改成 \"0\"", "和第 2 关同一个判断"),
    ]
    y = 108
    for t, a, b in lines:
        s.box(rx, y - 13, 70, 26, t, "rem", 12)
        s.text(rx + 80, y - 6, a, 12, INK)
        s.text(rx + 80, y + 10, b, 12, SUB)
        y += 44
    s.text(rx, 246, "第 3 关就是 visited: 进来先改 \"0\", 每格最多展开一次。", 12, INK)
    s.text(rx, 266, "不 sink: (0,0) → (0,1) → (0,0) → ... 无限递归。", 12, SUB)
    s.text(rx, 286, "island 数 = 外层扫描里\"遇到 1\"的次数, 总工作 O(m·n)。", 12, SUB)
    return s.out("islands_core.svg")


def fig_islands_trace():
    rows = sim_islands()
    m, n = 4, 5
    cw, ch = 30, 28
    gh = m * ch
    rh = gh + 28
    top = 86
    H = top + rh * (len(rows) + 1) + 90
    s = Svg(H, "Number of Islands 运行流程")
    head(s, "外层按行扫描: 遇到 \"1\" → count += 1 → dfs 把整块 island sink 掉 (格内数字 = 本次 dfs 的访问顺序)",
         "DIRS 顺序: 下 → 上 → 右 → 左 · dfs 进入时 grid[r][c] 从 \"1\" 改成 \"0\"")
    s.text(40, 62, "扫描到", 12, SUB)
    s.text(170, 62, "dfs 之后的 grid", 12, SUB)
    s.text(350, 62, "dfs 访问顺序 · count", 12, SUB)
    s.hsep(72)
    y = top - 4

    def draw_grid(y0, sunk, cur):
        for r in range(m):
            for c in range(n):
                land = ISLAND_GRID[r][c] == "1"
                if (r, c) in sunk:
                    iid, order = sunk[(r, c)]
                    role = "new" if iid == cur else "oth"
                    lab = str(order)
                elif land:
                    role, lab = "plain", "1"
                else:
                    role, lab = "water", "0"
                s.box(170 + c * cw, y0 + r * ch, cw, ch, lab, role, 14)

    # 初始行
    s.text(40, y + gh / 2 - 10, "开始", 14, INK, 500)
    s.text(40, y + gh / 2 + 10, "count = 0", 12, SUB)
    draw_grid(y, {}, 0)
    s.text(350, y + gh / 2 - 10, "3 块陆地, 还没人处理", 12, SUB)
    s.text(350, y + gh / 2 + 10, "白 1 = 还没处理的陆地", 12, SUB)
    y += rh
    s.hsep(y - 12)
    for k, row in enumerate(rows):
        r0, c0 = row["start"]
        s.box(40, y + gh / 2 - 26, 96, 24, "(%d,%d) 是 1" % (r0, c0), "new", 12)
        s.text(40, y + gh / 2 + 18, "→ 新 island", 12, SUB)
        draw_grid(y, row["sunk"], row["count"])
        order = row["order"]
        ys = y + 10
        s.text(350, ys, "访问: " + " → ".join("(%d,%d)" % p for p in order[:3]), 12, INK, 500)
        if len(order) > 3:
            s.text(350, ys + 18, "     " + " → ".join("(%d,%d)" % p for p in order[3:]), 12, INK, 500)
        s.text(350, y + gh / 2 + 12, "count = %d" % row["count"], 16, INK, 500)
        s.text(350, y + gh / 2 + 36, "本块 %d 格, 之后扫描到它们 → 当成水跳过" % len(order), 12, SUB)
        y += rh
        if k < len(rows) - 1:
            s.hsep(y - 12)
    s.hsep(y - 12)
    s.text(40, y + 12, "答案: count = 3", 16, INK, 500)
    s.text(40, y + 34, "(Max Area of Island: 同样的 dfs, 让它返回格数, 取 max)", 12, SUB)
    s.legend(y + 62, [("new", "本次 dfs 刚 sink"), ("oth", "之前 sink 的"),
                      ("plain", "没处理的陆地 1"), ("water", "水 0")])
    s.h = y + 80
    return s.out("islands_trace.svg")


def fig_rotting_core(steps):
    s = Svg(300, "multi-source BFS: 所有初始烂橘子同时入队")
    head(s, "单源 BFS: 一个起点 → 层数 = 距离。多源: 加一个虚拟起点 S* 连到所有烂橘子 (距离 0)",
         "S* 不用真建, 直接把所有源点一起放进 queue 当作第 0 层")
    # 虚拟源
    s.node(70, 150, "S*", "oth", r=20, dash=True)
    x = 150
    prev_cx = None
    layers = [("第 0 层", steps[0]["layer"], "minute 0")]
    for st in steps[1:]:
        layers.append(("第 %d 层" % st["minute"], st["new"], "minute %d" % st["minute"]))
    colw = 100
    cxs = []
    for i, (name, cells, mn) in enumerate(layers):
        cx = 150 + i * 128
        cxs.append(cx)
        h = 22 * len(cells) + 12
        y0 = 150 - h / 2 + 6
        role = "new"
        s.rect(cx - 36, y0, 72, h, "new" if i == 0 else "oth", rx=6)
        for j, p in enumerate(cells):
            s.text(cx, y0 + 18 + 22 * j, "(%d,%d)" % p, 12, ROLE["new" if i == 0 else "oth"][2], 500, "middle")
        s.text(cx, 40 + 28, name, 14, INK, 500, "middle")
        s.text(cx, 40 + 28 + 18, "%d 个 cell" % len(cells), 12, SUB, 400, "middle")
    s.edge((70, 150), (cxs[0] - 36, 156), 20, 0, ARROW["gray"], dash=True, arrow="gray")
    for i in range(len(cxs) - 1):
        s.line(cxs[i] + 38, 156, cxs[i + 1] - 38, 156, ARROW["gray"], arrow="gray")
    s.text(70, 186, "距离 0", 12, SUB, 400, "middle")
    s.text(40, 262, "层数 = 最近的烂橘子要几分钟烂到这里。BFS 同时从所有源点往外扩, 每层 +1 分钟。", 12, INK)
    s.text(40, 282, "最后一个新烂的橘子所在的层 = 答案; 烂不到的 (被空格隔开) 在 fresh 里剩下 → -1。", 12, SUB)
    s.h = 300
    return s.out("rotting_core.svg")


def fig_rotting_trace(steps):
    m, n = 3, 5
    cw, ch = 28, 28
    gh = m * ch
    rh = gh + 40
    top = 88
    H = top + rh * len(steps) + 100
    s = Svg(H, "Rotting Oranges 运行流程")
    head(s, "每一分钟: popleft 本层所有 cell → 感染 4 邻居里的新鲜橘子 → 新烂的 push 进 queue (= 下一层)",
         "fresh = 还没烂的橘子数 · 格内数字 = 这个橘子在第几分钟烂的")
    s.text(40, 62, "minute", 12, SUB)
    s.text(100, 62, "popleft (本层)", 12, SUB)
    s.text(300, 62, "感染后的 grid", 12, SUB)
    s.text(450, 62, "queue (下一层)", 12, SUB)
    s.hsep(72)
    y = top - 6
    for i, st in enumerate(steps):
        g = st["grid"]
        mo = st["minute_of"]
        newset = set(st["new"]) if i else set(st["layer"])
        s.text(40, y + gh / 2, "%d" % st["minute"], 16, INK, 500)
        # pop 列
        if i == 0:
            s.text(100, y + 14, "初始: 所有 2 一起入队", 12, SUB)
        else:
            for j, p in enumerate(st["layer"]):
                s.box(100 + j * 36, y, 34, 24, "(%d,%d)" % p, "rem", 12, bold=False)
            s.text(100, y + 40, "len(q) = %d → 只处理这 %d 个" % (len(st["layer"]), len(st["layer"])), 12, SUB)
        # grid
        for r in range(m):
            for c in range(n):
                p = (r, c)
                if g[r][c] == 0:
                    role, lab = "water", "·"
                elif g[r][c] == 1:
                    role, lab = "plain", "1"
                else:
                    role = "new" if p in newset else "oth"
                    lab = str(mo[p])
                s.box(300 + c * cw - 0, y + r * ch, cw, ch, lab, role, 14)
        # queue 列 (操作后的 queue)
        q = st["layer"] if i == 0 else st["new"]
        for j, p in enumerate(q):
            s.box(450 + j * 36, y, 34, 24, "(%d,%d)" % p, "new", 12, bold=False)
        # fresh 算式
        if i == 0:
            s.text(450, y + 40, "fresh = %d" % st["fresh"], 12, INK, 500)
        else:
            prev = steps[i - 1]["fresh"]
            s.text(450, y + 40, "fresh = %d - %d = %d" % (prev, len(st["new"]), st["fresh"]), 12, INK, 500)
        y += rh
        s.hsep(y - 14)
    s.text(40, y + 8, "答案: 最后一次有橘子变烂是 minute 3, 且 fresh = 0 → minutes = 3", 16, INK, 500)
    s.text(40, y + 30, "若只有 (0,0) 是烂的 (把 (2,4) 改成 1), 同一个 grid 要 6 分钟; 两个源同时扩散 → 3 分钟", 12, SUB)
    s.legend(y + 58, [("new", "新烂 / push 进 queue"), ("rem", "popleft 取出"),
                      ("oth", "之前烂的"), ("plain", "新鲜 1")])
    s.h = y + 76
    return s.out("rotting_trace.svg")

# ------------------------------------------------------------ sims (part 2)
def sim_ladder():
    begin, end, wl = LADDER
    words = set(wl)
    q, level = deque([begin]), 1
    levels = []
    ans = 0
    while q:
        layer = list(q)
        recs = []
        found = None
        for _ in range(len(q)):
            w = q.popleft()
            if w == end:
                recs.append((w, [], True))
                found = level
                break
            new = []
            for i in range(len(w)):
                for ch in "abcdefghijklmnopqrstuvwxyz":
                    nw = w[:i] + ch + w[i + 1:]
                    if nw in words:
                        words.remove(nw)
                        q.append(nw)
                        new.append(nw)
            recs.append((w, new, False))
        levels.append(dict(level=level, layer=layer, recs=recs,
                           queue=list(q), left=sorted(words)))
        if found:
            ans = found
            break
        level += 1
    assert ans == 5
    return levels


def sim_kahn(n, pre):
    graph = [[] for _ in range(n)]
    indeg = [0] * n
    for c, p in pre:
        graph[p].append(c)
        indeg[c] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    steps = [dict(u=None, changes=[], indeg=indeg[:], queue=list(q),
                  order=[], popped=set())]
    popped = set()
    while q:
        u = q.popleft()
        order.append(u)
        popped.add(u)
        ch = []
        for v in graph[u]:
            ch.append((v, indeg[v], indeg[v] - 1))
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
        steps.append(dict(u=u, changes=ch, indeg=indeg[:], queue=list(q),
                          order=order[:], popped=set(popped)))
    return steps


# ------------------------------------------------------------ figures (part 2)
def fig_ladder_core():
    s = Svg(330, "Word Ladder: 隐式图 + 按层 BFS")
    head(s, "点 = 单词, 边 = 只差一个字母。graph 没有存起来: 邻居现算 (把某一位换成 a-z, 看在不在词典里)",
         "beginWord = hit → endWord = cog · 层数 = 最短路径上的单词个数")
    cols = [("level 1", ["hit"]), ("level 2", ["hot"]), ("level 3", ["dot", "lot"]),
            ("level 4", ["dog", "log"]), ("level 5", ["cog"])]
    P = {}
    for i, (name, ws) in enumerate(cols):
        cx = 80 + i * 130
        s.text(cx, 66, name, 14, INK, 500, "middle")
        for j, w in enumerate(ws):
            cy = 175 if len(ws) == 1 else 135 + j * 80
            P[w] = (cx, cy)
    tree = [("hit", "hot"), ("hot", "dot"), ("hot", "lot"), ("dot", "dog"),
            ("lot", "log"), ("dog", "cog"), ("log", "cog")]
    for a, b in tree:
        s.edge(P[a], P[b], 24, 24, ARROW["gray"], arrow="gray")
    # 同层边 (真实存在, 但 BFS 不会用到)
    for a, b in (("dot", "lot"), ("dog", "log")):
        s.line(P[a][0], P[a][1] + 16, P[b][0], P[b][1] - 16, "#B4B2A9", dash=True, sw=1.2)
    for w, (x, y) in P.items():
        role = "new" if w == "cog" else "oth"
        s.box(x - 24, y - 16, 48, 32, w, role, 14, key=(w == "hit"))
    s.text(40, 252, "灰虚线: 同层之间也差一个字母, 但两端都已 visited, BFS 不会走它。", 12, SUB)
    s.text(40, 274, "为什么是最短: 层 k 的词离 hit 恰好 k-1 步; 一层一层扩, 第一次碰到 cog 就是最少步。", 12, INK)
    s.text(40, 296, "不要先 O(N²·L) 两两比较建 graph: 每个词直接枚举 L 位 × 26 字母 = 26L 个候选, 查 set O(1)。", 12, SUB)
    return s.out("ladder_core.svg")


def fig_ladder_trace(levels):
    rh = 84
    top = 88
    H = top + rh * len(levels) + 110
    s = Svg(H, "Word Ladder 运行流程")
    head(s, "words = set(wordList) = 还没访问的词 · 每层: popleft → 枚举改一位 → 在 words 里就 remove 并入队",
         "beginWord = hit, endWord = cog, wordList = [hot, dot, dog, lot, log, cog]")
    s.text(40, 62, "level", 12, SUB)
    s.text(100, 62, "popleft → 找到的新词 (remove)", 12, SUB)
    s.text(430, 62, "queue (下一层) · words 剩余", 12, SUB)
    s.hsep(72)
    y = top - 6
    init_left = sorted(LADDER[2])
    for lv in levels:
        s.text(40, y + 22, "%d" % lv["level"], 16, INK, 500)
        for j, (w, new, hit) in enumerate(lv["recs"]):
            yy = y + j * 30
            s.box(100, yy, 44, 24, w, "rem", 12, bold=False)
            if hit:
                s.text(156, yy + 12, "w == endWord → return level = %d" % lv["level"], 14, INK, 500)
            elif new:
                s.text(156, yy + 12, "→ " + ", ".join(new) + "  (remove)", 12, INK)
            else:
                s.text(156, yy + 12, "→ 没有新词 (邻居都已 remove)", 12, SUB)
        if lv["queue"]:
            for j, w in enumerate(lv["queue"]):
                s.box(430 + j * 48, y, 44, 24, w, "new", 12, bold=False)
        else:
            s.text(430, y + 12, "queue 为空, 已 return", 12, SUB)
        left = lv["left"]
        s.text(430, y + 40, "words 剩余 %d: {%s}" % (len(left), ",".join(left)), 12, SUB)
        y += rh
        s.hsep(y - 14)
    s.text(40, y + 8, "答案: cog 在 level 5 → ladderLength = 5 (hit → hot → dot → dog → cog)", 16, INK, 500)
    s.text(40, y + 30, "level 4 里 log 取出时, cog 已被 dog 抢先 remove: 同一个词不会入队两次", 12, SUB)
    s.legend(y + 58, [("rem", "popleft 取出"), ("new", "新入队 (已从 words remove)")])
    s.h = y + 76
    return s.out("ladder_trace.svg")


def fig_cs_core():
    s = Svg(290, "indegree 的含义")
    head(s, "indegree[v] = v 还有几门前置课没上完。= 0 ⇔ 前置课全上完 ⇔ v 可以入队",
         "只看 v = 2 (前置课 0 和 1)")
    panels = [(40, "开始", False, False, 2), (250, "pop 0: indegree[2] -= 1", True, False, 1),
              (460, "pop 1: indegree[2] -= 1", True, True, 0)]
    for x0, title, d0, d1, val in panels:
        s.text(x0, 66, title, 14, INK, 500)
        p0, p1, p2 = (x0 + 25, 120), (x0 + 25, 190), (x0 + 135, 155)
        s.edge(p0, p2, 16, 16, ARROW["red"] if d0 else ARROW["gray"], dash=d0, arrow="red" if d0 else "gray")
        s.edge(p1, p2, 16, 16, ARROW["red"] if d1 else ARROW["gray"], dash=d1, arrow="red" if d1 else "gray")
        s.node(p0[0], p0[1], "0", "oth" if d0 else "new", key=not d0 and False)
        s.node(p1[0], p1[1], "1", "oth" if d1 else "new")
        s.node(p2[0], p2[1], "2", "new" if val == 0 else "plain", key=val == 0)
        s.box(x0 + 40, 222, 130, 30, "indegree[2] = %d" % val, "new" if val == 0 else "plain", 14)
    s.text(40, 190 - 12, "", 12)
    s.text(40, 276, "红虚线 = 这条边已经\"用掉\"。每条边恰好被减一次 → 整个过程 O(V + E)。", 12, SUB)
    s.h = 292
    return s.out("canfinish_core.svg")


def graph_panel(s, pos, edges, ytop, roles=None, bends=None):
    roles = roles or {}
    bends = bends or {}
    for a, b in edges:
        s.edge(pos[a], pos[b], 16, 16, ARROW["gray"], arrow="gray", bend=bends.get((a, b), 0))
    for k, (x, y) in pos.items():
        s.node(x, y, str(k), roles.get(k, "oth"))


def topo_trace(name, title, n, pre, pos, edges, steps, final_text, sub_text,
               panel_h=150, bends=None, stuck=(), side=None):
    nrow = len(steps)
    rhs = [66 if len(st["changes"]) < 2 else 80 for st in steps]
    top = 40 + panel_h + 52
    H = top + sum(rhs) + 120
    s = Svg(H, title)
    head(s, "queue 里是 indegree = 0 的点 · 每步: pop u → u 加入 order → 对 u 的每个邻居 v: indegree[v] -= 1, 变 0 就 push",
         "prerequisites = %s" % (pre,))
    graph_panel(s, pos, edges, 40, bends=bends, roles={k: "rem" for k in stuck})
    if side:
        for i, t in enumerate(side):
            s.text(520, 70 + i * 22, t, 12, SUB if i else INK, 400 if i else 500)
    y0 = 40 + panel_h + 6
    s.text(40, y0 + 8, "pop u", 12, SUB)
    s.text(160, y0 + 8, "indegree 表 (下标 = 课号)", 12, SUB)
    s.text(392, y0 + 8, "queue", 12, SUB)
    s.text(476, y0 + 8, "order", 12, SUB)
    for i in range(n):
        s.text(160 + i * 34 + 17, y0 + 26, "[%d]" % i, 12, SUB, 400, "middle")
    s.hsep(y0 + 36)
    y = top - 6 + 6
    for st, rh in zip(steps, rhs):
        if st["u"] is None:
            s.text(40, y + 12, "开始", 14, INK, 500)
            s.text(40, y + 36, "indegree=0 的先入队", 12, SUB)
        else:
            s.box(40, y, 34, 24, str(st["u"]), "rem", 14)
            s.text(84, y + 12, "pop %d" % st["u"], 12, SUB)
            for j, (v, a, b) in enumerate(st["changes"]):
                s.text(40, y + 38 + 15 * j, "indegree[%d]: %d → %d" % (v, a, b), 12, INK)
            if not st["changes"]:
                s.text(40, y + 38, "没有出边", 12, SUB)
        changed = {v for v, a, b in st["changes"]}
        for i, val in enumerate(st["indeg"]):
            if st["u"] is None:
                role = "new" if val == 0 else "plain"
            elif i in st["popped"]:
                role = "oth"
            elif i in changed:
                role = "new"
            else:
                role = "plain"
            if i in stuck and st is steps[-1]:
                role = "rem"
            s.box(160 + i * 34, y, 34, 26, str(val), role, 14)
        for j, v in enumerate(st["queue"]):
            s.box(392 + j * 30, y, 28, 26, str(v), "new", 14)
        if not st["queue"]:
            s.text(392, y + 13, "空", 12, SUB)
        for j, v in enumerate(st["order"]):
            s.box(476 + j * 28, y, 26, 26, str(v), "oth", 14, bold=False)
        if not st["order"]:
            s.text(476, y + 13, "[ ]", 12, SUB)
        y += rh
        s.hsep(y - 14)
    for t_i, t in enumerate(final_text):
        s.text(40, y + 8 + t_i * 22, t, 16 if t_i == 0 else 12, INK if t_i == 0 else SUB, 500 if t_i == 0 else 400)
    yl = y + 8 + len(final_text) * 22 + 20
    items = [("rem", "pop 取出" + (" / 环上卡住的点" if stuck else "")),
             ("new", "indegree 刚变 / 在 queue"), ("oth", "已处理 (已进 order)"),
             ("plain", "还在等前置课")]
    yl = s.legend(yl, items)
    s.h = yl + 20
    return s.out(name)

# ------------------------------------------------------------ CS II / clone / UF
CS2_POS = {0: (70, 125), 3: (210, 80), 4: (350, 80), 1: (210, 170), 2: (350, 170)}
CS2_EDGES = [(p, c) for c, p in CS2_PRE]
CS2_BENDS = {(1, 2): 14, (2, 1): 14}


def fig_findorder_core():
    st = sim_kahn(CS2_N, CS2_PRE)
    last = st[-1]
    assert last["order"] == [0, 3, 4] and last["indeg"] == [0, 1, 1, 0, 0]
    s = Svg(300, "有环时 Kahn 会卡住")
    head(s, "同一个算法, order 记下 pop 的顺序。有环 → 环上的点 indegree 永远 > 0 → 永远进不了 queue",
         "prerequisites = %s · 0 → 1, 1 ⇄ 2 (环), 0 → 3 → 4" % (CS2_PRE,))
    pos = {k: (x, y + 20) for k, (x, y) in CS2_POS.items()}
    graph_panel(s, pos, CS2_EDGES, 40, roles={1: "rem", 2: "rem"}, bends=CS2_BENDS)
    s.text(pos[1][0], pos[1][1] + 28, "indegree = 1", 12, ROLE["rem"][2], 400, "middle")
    s.text(pos[2][0], pos[2][1] + 28, "indegree = 1", 12, ROLE["rem"][2], 400, "middle")
    s.text(430, 90, "Kahn 跑完后:", 14, INK, 500)
    s.text(430, 114, "order = [0, 3, 4]  (3 个)", 14, INK, 500)
    s.text(430, 138, "numCourses = 5", 12, SUB)
    s.text(430, 168, "1 在等 2 先上, 2 在等 1 先上", 12, SUB)
    s.text(430, 188, "→ 谁的 indegree 都减不到 0", 12, SUB)
    s.text(40, 254, "len(order) = 3 < numCourses = 5 → 有环 → 返回 []", 14, INK, 500)
    s.text(40, 276, "(另一种做法: DFS 三色标记, 走到\"正在访问\"的点 = 有环。Kahn 不用递归, 面试里更好写。)", 12, SUB)
    return s.out("findorder_core.svg")


def fig_findorder_trace():
    steps = sim_kahn(CS2_N, CS2_PRE)
    return topo_trace(
        "findorder_trace.svg", "Course Schedule II 有环时的运行流程", CS2_N, CS2_PRE,
        {k: (x, y + 20) for k, (x, y) in CS2_POS.items()}, CS2_EDGES, steps,
        ["答案: queue 空了, 但 len(order) = 3 ≠ numCourses = 5 → 返回 []",
         "卡住的 1、2: indegree 还是 1 (红), 它们互相在等对方"],
        "", bends=CS2_BENDS, stuck=(1, 2), panel_h=170,
        side=["indegree 初值", "0:0  1:2", "2:1  3:1", "4:1"])


# ---- Clone Graph
def sim_clone():
    # 方形: 1-2, 2-3, 3-4, 4-1; neighbors 顺序同 _mk_square()
    nb = {1: [2, 4], 2: [1, 3], 3: [2, 4], 4: [3, 1]}
    d = {}
    stack = []
    rows = []

    def dfs(v, frm):
        if v in d:
            rows.append(dict(v=v, frm=frm, hit=True, stack=list(stack), d=dict(d)))
            return
        d[v] = True
        stack.append(v)
        rows.append(dict(v=v, frm=frm, hit=False, stack=list(stack), d=dict(d)))
        for w in nb[v]:
            dfs(w, v)
        stack.pop()

    dfs(1, None)
    assert len(rows) == 9 and len(d) == 4
    return rows, nb


def fig_clone_core():
    s = Svg(330, "Clone Graph: 先登记再递归")
    head(s, "图里有环: 1 → 2 → 3 → 4 → 1。old2new 记录\"谁已经复制过\", 一定要在递归 neighbor 之前写入",
         "这和 visited 是同一件事, 只是顺便存了 副本 是谁")
    s.text(40, 66, "先递归, 后登记 (错)", 14, INK, 500)
    s.text(370, 66, "先登记 old2new[old] = copy, 再递归 (对)", 14, INK, 500)
    for ox, ok in ((90, False), (420, True)):
        P = {1: (ox, 120), 2: (ox + 120, 120), 3: (ox + 120, 215), 4: (ox, 215)}
        for a, b in ((1, 2), (2, 3), (3, 4)):
            s.edge(P[a], P[b], 16, 16, ARROW["gray"], arrow="gray")
        if ok:
            s.edge(P[4], P[1], 16, 16, ARROW["red"], dash=True, arrow="red")
        else:
            s.edge(P[4], P[1], 16, 16, ARROW["red"], arrow="red")
        for k, (x, y) in P.items():
            s.node(x, y, str(k), "oth" if ok or k != 1 else "rem")
    s.text(155, 255, "走到 4 → 又看到 1: dict 里还没有 1'", 12, SUB, 400, "middle")
    s.text(155, 275, "→ 又 Node(1), 再走 2, 3, 4 ... 无限递归", 12, ROLE["rem"][2], 500, "middle")
    s.text(485, 255, "走到 4 → 又看到 1: 已在 old2new", 12, SUB, 400, "middle")
    s.text(485, 275, "→ 直接返回 1', 环在这里被切断", 12, ROLE["new"][2], 500, "middle")
    s.text(40, 306, "副本的 neighbor 必须也是副本: copy.neighbors.append(dfs(nb)) 返回的是 old2new[nb], 不是 nb 本身。", 12, SUB)
    s.line(340, 56, 340, 290, "#B4B2A9", dash=True, sw=0.8)
    return s.out("clone_core.svg")


def fig_clone_trace():
    rows, nb = sim_clone()
    rh = 48
    top = 88
    H = top + rh * len(rows) + 110
    s = Svg(H, "Clone Graph 运行流程")
    head(s, "square: 1-2-3-4-1 · neighbors: 1:[2,4]  2:[1,3]  3:[2,4]  4:[3,1] · old2new 里 k→k' 表示 old 节点 k 的副本",
         "每行 = 一次 dfs 调用 · miss: 新建副本、登记、再递归 · hit: 已登记, 直接返回副本")
    s.text(40, 62, "调用", 12, SUB)
    s.text(160, 62, "递归栈 (miss 的调用)", 12, SUB)
    s.text(290, 62, "old2new (登记的 old → 副本)", 12, SUB)
    s.text(500, 62, "结果", 12, SUB)
    s.hsep(72)
    y = top - 8
    seen = set()
    for r in rows:
        v = r["v"]
        role = "rem" if r["hit"] else "new"
        s.box(40, y, 62, 26, "dfs(%d)" % v, role, 14)
        s.text(108, y + 13, "from %s" % r["frm"] if r["frm"] else "入口", 12, SUB)
        for j, k in enumerate(r["stack"]):
            s.box(160 + j * 30, y, 28, 26, str(k), "oth", 14, key=(j == len(r["stack"]) - 1 and not r["hit"]))
        for j, k in enumerate(r["d"]):
            new = (k not in seen) and not r["hit"]
            s.box(290 + j * 50, y, 46, 26, "%d→%d'" % (k, k), "new" if new else "oth", 12, bold=False)
        seen |= set(r["d"])
        if r["hit"]:
            s.text(500, y + 6, "已登记 → return %d'" % v, 12, ROLE["rem"][2], 500)
            s.text(500, y + 24, "不再递归", 12, SUB)
        else:
            s.text(500, y + 6, "新建 %d', 登记" % v, 12, ROLE["new"][2], 500)
            s.text(500, y + 24, "再递归 neighbors %s" % (nb[v],), 12, SUB)
        y += rh
        s.hsep(y - 10)
    s.text(40, y + 8, "答案: old2new 有 4 项 = 4 个 miss; 其余 5 次调用都是 hit", 16, INK, 500)
    s.text(40, y + 30, "dfs 调用 9 次 = 1 (入口) + 8 (neighbors 列表总长 = 2E) → O(V + E)", 12, SUB)
    s.legend(y + 58, [("new", "miss: 新建并登记"), ("rem", "hit: 已登记, 直接返回"), ("oth", "递归栈 / 已登记")])
    s.h = y + 76
    return s.out("clone_trace.svg")


# ---- Union-Find
UF_N = 7
UF_EDGES = [(0, 1), (2, 3), (0, 2), (4, 5), (3, 5)]


def sim_uf():
    parent = list(range(UF_N))
    size = [1] * UF_N
    count = UF_N
    ev = []

    def find(x):
        comp = []
        while parent[x] != x:
            old = parent[x]
            parent[x] = parent[parent[x]]
            if parent[x] != old:
                comp.append((x, old, parent[x]))
            x = parent[x]
        ev.extend(comp)
        return x

    steps = [dict(edge=None, parent=parent[:], size=size[:], count=count,
                  comp=[], link=None, roots=None, old_parent=None)]
    for a, b in UF_EDGES:
        ev.clear()
        ra, rb = find(a), find(b)
        comp = list(ev)
        assert ra != rb
        sa, sb = size[ra], size[rb]
        swapped = False
        if size[ra] < size[rb]:
            ra, rb = rb, ra
            swapped = True
        parent[rb] = ra
        size[ra] += size[rb]
        count -= 1
        steps.append(dict(edge=(a, b), parent=parent[:], size=size[:], count=count,
                          comp=comp, link=(rb, ra), roots=None,
                          sizes=(sa, sb), swapped=swapped))
    # 与 DSU 类实现对照
    dsu = NS["DSU"](UF_N)
    for a, b in UF_EDGES:
        dsu.union(a, b)
    assert dsu.parent == parent and dsu.size == size
    return steps


def forest_layout(parent, x0, x1, y0, dy=30):
    n = len(parent)
    kids = defaultdict(list)
    roots = []
    for v in range(n):
        if parent[v] == v:
            roots.append(v)
        else:
            kids[parent[v]].append(v)
    leaves = {}

    def cnt(v):
        leaves[v] = 1 if not kids[v] else sum(cnt(c) for c in kids[v])
        return leaves[v]
    for r in roots:
        cnt(r)
    total = sum(leaves[r] for r in roots)
    gap = min(30, (x1 - x0 - 6 * (len(roots) - 1)) / max(total, 1))
    pos = {}
    cur = [x0 + gap / 2]

    def place(v, depth):
        if not kids[v]:
            pos[v] = (cur[0], y0 + depth * dy)
            cur[0] += gap
        else:
            for c in kids[v]:
                place(c, depth + 1)
            xs = [pos[c][0] for c in kids[v]]
            pos[v] = ((min(xs) + max(xs)) / 2, y0 + depth * dy)
    for r in roots:
        place(r, 0)
        cur[0] += 6
    return pos


def fig_uf_core():
    s = Svg(340, "Union-Find 两个优化")
    head(s, "find(x) = 顺着 parent 走到 root。root 相同 = 同一个集合。不优化时 find 可以退化成 O(n)",
         "两个优化让 find / union 几乎 O(1) (摊还 O(α(n)), α 是反 Ackermann, 实际 ≤ 4)")
    s.text(40, 66, "无优化: 总是 find(a) 挂到 find(b)", 14, INK, 500)
    s.text(40, 85, "union(1,0), union(2,1), union(3,2), union(4,3)", 12, SUB)
    for i in range(5):
        x = 60 + i * 54
        s.node(x, 135, str(i), "rem" if i == 4 else "oth", r=15)
        if i:
            s.edge((x, 135), (x - 54, 135), 15, 15, ARROW["gray"], arrow="gray")
    s.text(40, 175, "退化成一条链 · find(4) 要走 4 步", 12, ROLE["rem"][2], 500)
    s.text(40, 195, "n 个点 → find 要 O(n)", 12, SUB)
    s.text(370, 66, "优化 1: union by size", 14, INK, 500)
    s.text(370, 85, "小树挂到大树的 root 下 → 高度 ≤ log₂ n", 12, SUB)
    # by size: 星形
    cx = 480
    s.node(cx, 120, "1", "new", r=15)
    for nm, dx in zip(("0", "2", "3", "4"), (-60, -20, 20, 60)):
        s.node(cx + dx, 170, nm, "oth", r=15)
        s.edge((cx + dx, 170), (cx, 120), 15, 15, ARROW["gray"], arrow="gray")
    s.text(370, 205, "同样的 union 序列 → 高度 1 (root 是 1)", 12, ROLE["new"][2], 500)
    # 优化 2
    s.hsep(222)
    s.text(40, 244, "优化 2: path compression — find 的时候顺手把路径上的点直接挂到 root 上", 14, INK, 500)
    for i in range(4):
        x = 70 + i * 44
        s.node(x, 288, str(i), "new" if i == 0 else "oth", r=14)
        if i:
            s.edge((x, 288), (x - 44, 288), 14, 14, ARROW["gray"], arrow="gray")
    s.text(40, 322, "find(3) 前: 3 → 2 → 1 → 0, 走 3 步", 12, SUB)
    s.text(250, 288, "find(3) 之后 →", 14, INK, 500)
    cx = 470
    s.node(cx, 272, "0", "new", r=14)
    for dx, nm in ((-60, "1"), (0, "2"), (60, "3")):
        s.node(cx + dx, 318, nm, "oth", r=14)
        s.edge((cx + dx, 318), (cx, 272), 14, 14, ARROW["green"], arrow="green")
    s.text(370, 346, "1, 2, 3 都直接指向 0 · 下次 find 一步到位", 12, SUB)
    s.h = 360
    return s.out("uf_core.svg")


def fig_uf_trace():
    steps = sim_uf()
    rh = 108
    top = 90
    H = top + rh * len(steps) + 110
    s = Svg(H, "Union-Find 运行流程")
    head(s, "n = 7 · union(a, b): find 两端的 root, 相同就跳过; 不同 → 小树的 root 挂到大树 root 下 (平局: b 挂到 a 下)",
         "森林里每个箭头 = parent 指针 (child → parent) · count = 当前集合数 = 森林里树的棵数")
    s.text(40, 62, "操作", 12, SUB)
    s.text(180, 62, "森林 (parent 指针)", 12, SUB)
    s.text(400, 62, "parent 数组 [0..6]", 12, SUB)
    s.text(596, 62, "count", 12, SUB)
    s.hsep(72)
    y = top - 10
    prev = None
    for k, st in enumerate(steps):
        par = st["parent"]
        pos = forest_layout(par, 175, 392, y + 14)
        changed = set()
        if prev is not None:
            changed = {i for i in range(UF_N) if par[i] != prev["parent"][i]}
        # 画边
        for v in range(UF_N):
            if par[v] != v:
                col = ARROW["green"] if v in changed else ARROW["gray"]
                s.edge(pos[v], pos[par[v]], 11, 11, col, arrow="green" if v in changed else "gray", sw=1.4)
        for (x, oldp, newp) in st["comp"]:
            # 被压缩掉的旧边: 虚线 (旧 parent 仍在森林里)
            s.edge(pos[x], pos[oldp], 11, 11, ARROW["red"], dash=True, sw=1.3, bend=-20)
        for v in range(UF_N):
            is_root = par[v] == v
            role = "oth"
            if st["link"] and v == st["link"][0]:
                role = "new"
            s.node(round(pos[v][0], 1), round(pos[v][1], 1), str(v), role, r=11, size=12,
                   key=(prev is not None and is_root and v == st["link"][1]))
        # 文字
        if st["edge"] is None:
            s.text(40, y + 14, "开始", 14, INK, 500)
            s.text(40, y + 34, "每个点自己一棵树", 12, SUB)
            s.text(40, y + 52, "size 全是 1", 12, SUB)
        else:
            a, b = st["edge"]
            s.text(40, y + 14, "union(%d, %d)" % (a, b), 14, INK, 500)
            yy = y + 34
            for c in st["comp"]:
                s.text(40, yy, "压缩 parent[%d]: %d→%d" % c, 12, ROLE["rem"][2], 500)
                yy += 16
            sa, sb = st["sizes"]
            rb, ra = st["link"]
            ra0, rb0 = (rb, ra) if st["swapped"] else (ra, rb)
            s.text(40, yy, "roots: %d, %d" % (ra0, rb0), 12, SUB)
            yy += 16
            s.text(40, yy, "size %d %s %d" % (sa, ">" if sa > sb else ("<" if sa < sb else "="), sb) +
                   (" 平局" if sa == sb else ""), 12, SUB)
            yy += 16
            s.text(40, yy, "→ %d 挂到 %d 下" % (rb, ra), 12, ROLE["new"][2], 500)
        # parent 数组
        for i in range(UF_N):
            role = "new" if i in changed else "plain"
            s.box(400 + i * 26, y + 4, 26, 26, str(par[i]), role, 14)
        s.text(400, y + 46, "size[root]: " + " ".join("%d:%d" % (i, st["size"][i]) for i in range(UF_N) if par[i] == i), 12, SUB)
        # count
        if prev is None:
            s.text(596, y + 18, "%d" % st["count"], 16, INK, 500)
        else:
            s.text(596, y + 18, "%d → %d" % (prev["count"], st["count"]), 16, INK, 500)
        prev = st
        y += rh
        s.hsep(y - 10)
    s.text(40, y + 8, "答案: count = 2 → 0..5 是一个集合, 6 是单独的一个 (node 6 从头到尾没被 union)", 16, INK, 500)
    s.text(40, y + 30, "Number of Provinces: 外层双循环里 isConnected[i][j] == 1 就 union(i, j); union 成功才 count -= 1", 12, SUB)
    s.legend(y + 58, [("new", "刚被挂到别人下面的 root"), ("key", "合并后的 root"),
                      ("oth", "其他节点")])
    s.h = y + 76
    return s.out("uf_trace.svg")

# ------------------------------------------------------------ Dijkstra
DJ_POS = {1: (60, 123), 2: (200, 72), 3: (200, 176), 4: (340, 123), 5: (480, 123)}
INF = float("inf")


def sim_dijkstra():
    graph = defaultdict(list)
    for u, v, w in DJ_TIMES:
        graph[u].append((v, w))
    n, k = 5, 1
    dist = [INF] * (n + 1)
    dist[k] = 0
    heap = [(0, k)]
    steps = [dict(pop=None, stale=False, relax=[], dist=dist[1:], heap=list(heap),
                  changed=set())]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            steps.append(dict(pop=(d, u), stale=True, relax=[], dist=dist[1:],
                              heap=list(heap), changed=set(), cur=dist[u]))
            continue
        relax, changed = [], set()
        for v, w in graph[u]:
            nd = d + w
            old = dist[v]
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
                relax.append((u, v, d, w, nd, old, True))
                changed.add(v)
            else:
                relax.append((u, v, d, w, nd, old, False))
        steps.append(dict(pop=(d, u), stale=False, relax=relax, dist=dist[1:],
                          heap=list(heap), changed=changed))
    for st in steps:
        st["dist"] = list(st["dist"])
    assert dist[1:] == [0, 3, 1, 4, 7] and max(dist[1:]) == 7
    return steps


def fmt_d(x):
    return "∞" if x == INF else str(x)


def edge_label(s, a, b, w, dx=0, dy=-12):
    mx, my = (a[0] + b[0]) / 2 + dx, (a[1] + b[1]) / 2 + dy
    s.b.append('<rect x="%s" y="%s" width="18" height="16" rx="3" fill="#fff"/>' % (mx - 9, my - 8))
    s.text(mx, my, str(w), 12, INK, 500, "middle")


def fig_dijkstra_core():
    s = Svg(350, "Dijkstra 的 invariant")
    head(s, "heap 的 top = 所有\"候选距离\"里最小的。它一弹出, dist 就是最终答案 (前提: 所有边权 ≥ 0)",
         "例: 起点 1 · 已确定 {1, 3} · 待确定的候选在 heap 里")
    # 已确定区域
    s.b.append('<rect x="40" y="70" width="230" height="190" rx="16" fill="#F1EFE8" stroke="#5F5E5A" stroke-width="1" stroke-dasharray="4 3"/>')
    s.text(56, 88, "已确定 (popped): dist 不会再变", 12, ROLE["oth"][2], 500)
    P = {1: (100, 170), 3: (200, 170), 2: (400, 130), 4: (400, 230)}
    s.edge(P[1], P[3], 16, 16, ARROW["gray"], arrow="gray")
    s.node(*P[1], "1", "oth")
    s.node(*P[3], "3", "oth")
    s.text(100, 196, "dist = 0", 12, ROLE["oth"][2], 400, "middle")
    s.text(200, 196, "dist = 1", 12, ROLE["oth"][2], 400, "middle")
    edge_label(s, P[1], P[3], 1, 0, -12)
    s.node(*P[2], "2", "new", key=True)
    s.node(*P[4], "4", "plain")
    # 跨界边 (候选)
    s.edge(P[1], P[2], 16, 16, ARROW["gray"], arrow="gray", bend=-30)
    s.edge(P[3], P[2], 16, 16, ARROW["green"], arrow="green")
    s.edge(P[3], P[4], 16, 16, ARROW["gray"], arrow="gray")
    s.text(290, 108, "0 + 4 = 4", 12, SUB, 400, "middle")
    s.text(330, 166, "1 + 2 = 3", 12, ROLE["new"][2], 500, "middle")
    s.text(318, 222, "1 + 5 = 6", 12, SUB, 400, "middle")
    # heap
    s.text(500, 78, "heap (候选)", 14, INK, 500)
    s.box(500, 92, 100, 28, "(3, 2)", "new", 14, key=True)
    s.box(500, 128, 100, 28, "(4, 2)", "plain", 14)
    s.box(500, 164, 100, 28, "(6, 4)", "plain", 14)
    s.text(500, 210, "(dist, node) · 最小的 (3, 2)", 12, SUB)
    s.text(500, 228, "先弹出", 12, SUB)
    s.text(40, 286, "为什么 dist[2] = 3 已经是最短: 要到 2 就必须从\"已确定\"区域走出来, 出来的第一步候选 ≥ 3 (heap 最小),", 12, INK)
    s.text(40, 306, "之后每条边权 ≥ 0, 只会更长。所以不可能有比 3 更短的路。", 12, INK)
    s.text(40, 328, "有负边: 先花 6 走到 4, 再走一条 -5 的边到 2 → 1 < 3, 这个论证就破了 → 改用 Bellman-Ford。", 12, SUB)
    return s.out("dijkstra_core.svg")


def heap_tree(s, cx, y0, heap, key=True):
    P = {}
    for i, (d_, v) in enumerate(heap):
        lvl = 0
        while (1 << (lvl + 1)) - 1 <= i:
            lvl += 1
        j = i - ((1 << lvl) - 1)
        slots = 1 << lvl
        x = cx + (j - (slots - 1) / 2) * (96 / slots) * (1 if lvl else 0) if lvl < 2 else cx + (j - 1.5) * 38
        if lvl == 1:
            x = cx + (j - 0.5) * 78
        P[i] = (x, y0 + 16 + lvl * 34)
    for i in P:
        if i:
            s.edge(P[(i - 1) // 2], P[i], 15, 15, "#B4B2A9", sw=1.2)
    for i, (d_, v) in enumerate(heap):
        s.node(round(P[i][0], 1), P[i][1], "%d,%d" % (d_, v), "new" if False else "oth", r=15, size=12,
               key=(i == 0 and key))
    return P


def fig_dijkstra_trace():
    steps = sim_dijkstra()
    rh = 104
    top = 262
    H = top + rh * len(steps) + 110
    s = Svg(H, "Network Delay Time (Dijkstra) 运行流程")
    head(s, "k = 1 · heap 存 (dist, node) · pop 最小的 → 过期就 skip → 否则 relax 每条出边: nd = d + w, nd < dist[v] 才更新并 push",
         "图: u → v 边上的数字 = 耗时 w")
    pos = DJ_POS
    for u, v, w in DJ_TIMES:
        s.edge((pos[u][0], pos[u][1] + 0), (pos[v][0], pos[v][1]), 16, 16, ARROW["gray"], arrow="gray")
    for (u, v, w), (dx, dy) in zip(DJ_TIMES, [(-6, -10), (-6, 12), (-12, 0), (0, -12), (0, 12), (0, -12)]):
        edge_label(s, pos[u], pos[v], w, dx, dy)
    for k_, (x, y) in pos.items():
        s.node(x, y + 0, str(k_), "oth")
    s.text(540, 62, "n = 5, k = 1", 12, INK, 500)
    s.text(540, 82, "times =", 12, SUB)
    for i, t in enumerate(DJ_TIMES):
        s.text(540 + (i % 2) * 52, 100 + (i // 2) * 18, str(t).replace(" ", ""), 12, SUB)
    y0 = 208
    s.text(40, y0, "pop (d, u)", 12, SUB)
    s.text(160, y0, "dist 表 [1..5]", 12, SUB)
    s.text(340, y0, "heap (tree, 顶 = 最小)", 12, SUB)
    s.text(490, y0, "relax / 判断", 12, SUB)
    for i in range(5):
        s.text(160 + i * 32 + 16, y0 + 18, "[%d]" % (i + 1), 12, SUB, 400, "middle")
    s.hsep(y0 + 28)
    y = top - 14
    prevdist = None
    for st in steps:
        dist = st["dist"]
        if st["pop"] is None:
            s.text(40, y + 14, "开始", 14, INK, 500)
            s.text(40, y + 36, "push (0, 1)", 12, SUB)
        else:
            d_, u = st["pop"]
            s.box(40, y, 62, 26, "(%d,%d)" % (d_, u), "rem", 14)
            if st["stale"]:
                s.text(40, y + 42, "%d > dist[%d]=%d" % (d_, u, st["cur"]), 12, ROLE["rem"][2], 500)
                s.text(40, y + 58, "过期, skip", 12, ROLE["rem"][2])
            else:
                s.text(40, y + 42, "%d = dist[%d]" % (d_, u), 12, SUB)
                s.text(40, y + 58, "有效, relax", 12, SUB)
        for i, val in enumerate(dist):
            role = "new" if (i + 1) in st["changed"] else "plain"
            s.box(160 + i * 32, y, 32, 26, fmt_d(val), role, 14)
        heap_tree(s, 392, y - 2, st["heap"])
        if not st["heap"]:
            s.text(392, y + 14, "空 → 结束", 12, SUB, 400, "middle")
        if st["pop"] is None:
            s.text(490, y + 14, "dist[1] = 0", 12, SUB)
        elif st["stale"]:
            s.text(490, y + 14, "不 relax, 直接 continue", 12, SUB)
        else:
            for j, (u, v, d_, w, nd, old, ok) in enumerate(st["relax"]):
                if ok:
                    s.text(490, y + 12 + j * 18, "%d→%d: %d+%d=%d < %s ✓ push" % (u, v, d_, w, nd, fmt_d(old)), 12, ROLE["new"][2], 500)
                else:
                    s.text(490, y + 12 + j * 18, "%d→%d: %d+%d=%d ≥ %s ✗" % (u, v, d_, w, nd, fmt_d(old)), 12, SUB)
            if not st["relax"]:
                s.text(490, y + 12, "没有出边", 12, SUB)
        y += rh
        s.hsep(y - 14)
    s.text(40, y + 8, "答案: dist[1..5] = [0, 3, 1, 4, 7] → max = 7 (所有点都到得了, 最晚是 5)", 16, INK, 500)
    s.text(40, y + 30, "(0,1) 先 push (4,2); 之后经 3 找到更短的 (3,2) → (4,2) 留在 heap 里变成过期记录, 弹出时被 skip", 12, SUB)
    s.legend(y + 58, [("rem", "pop 取出"), ("new", "dist 刚更新"), ("oth", "heap 里的 (dist, node)"), ("key", "heap top")])
    s.h = y + 76
    return s.out("dijkstra_trace.svg")

def build_figs():
    F = {}
    rs = sim_rotting()
    F["first"] = fig_first_core()
    F["isl_core"] = fig_islands_core()
    F["isl_tr"] = fig_islands_trace()
    F["rot_core"] = fig_rotting_core(rs)
    F["rot_tr"] = fig_rotting_trace(rs)
    lv = sim_ladder()
    F["lad_core"] = fig_ladder_core()
    F["lad_tr"] = fig_ladder_trace(lv)
    F["cs_core"] = fig_cs_core()
    pos1 = {0: (70, 95), 1: (70, 155), 2: (200, 125), 3: (330, 95), 4: (330, 155), 5: (460, 125)}
    ed1 = [(p, c) for c, p in CS1_PRE]
    F["cs_tr"] = topo_trace("canfinish_trace.svg", "Course Schedule 运行流程", CS1_N, CS1_PRE, pos1, ed1,
        sim_kahn(CS1_N, CS1_PRE),
        ["答案: queue 空了, done = 6 == numCourses = 6 → True", "pop 的顺序 [0, 1, 2, 3, 4, 5] 就是一个合法上课顺序 (Course Schedule II 要的)"],
        "", side=["indegree 初值", "0:0  1:0", "2:2  3:1", "4:1  5:2"])
    F["fo_core"] = fig_findorder_core()
    F["fo_tr"] = fig_findorder_trace()
    F["cl_core"] = fig_clone_core()
    F["cl_tr"] = fig_clone_trace()
    F["uf_core"] = fig_uf_core()
    F["uf_tr"] = fig_uf_trace()
    F["dj_core"] = fig_dijkstra_core()
    F["dj_tr"] = fig_dijkstra_trace()
    return F




# ------------------------------------------------------------ the document
def build_doc(F):
    doc = d.Doc("12 · Graph: BFS / DFS / Topological Sort / Union-Find / Dijkstra")
    doc.main("主线: graph 遍历 = 从已知的点出发, 用 visited 保证每个点只处理一次 → O(V + E)。"
             "BFS 按层扩 = 无权最短路; 入度归零 = 拓扑序; Union-Find 回答\"连没连通\"; heap 贪心 = 带权最短路。")
    doc.main("概念链: Number of Islands (grid DFS) → Rotting Oranges (multi-source BFS) → "
             "Word Ladder (隐式图 BFS 最短路) → Course Schedule (Kahn 拓扑排序) → Course Schedule II (拓扑顺序 + 有环) → "
             "Clone Graph (DFS + Hash Table) → Number of Provinces (Union-Find) → Network Delay Time (Dijkstra)")

    # ---------------------------------------------------------------- 0
    doc.h2("0. 第一性原理: 不记 visited, 就是在重复劳动")
    doc.p("<b>Brute force:</b> 从 start 出发, 对每个邻居递归 (或入队), 不记走过哪里。"
          "图里有环 → 永远走不完; 即使没有环, 多条路汇合到同一个点时, 那个点和它后面的整片区域会被重复处理。"
          "上图: 两层 diamond 就有 13 次处理, 每多一层翻一倍 → $O(2^k)$。")
    doc.p("<b>浪费在哪:</b> 同一个点被处理多次。点的结果只和\"它是谁\"有关, 和\"从哪条路来的\"无关, 第二次处理是白做。")
    doc.p("<b>消掉它:</b> 一个 visited 集合。点第一次出现就标记, 之后看到就跳过 → 每个点只处理一次, 每条边只检查一次 → $O(V + E)$。"
          "grid 是隐式 graph: 格子是点, 上下左右是边, 邻居靠 <code>(dr, dc)</code> 现算, 不用建邻接表。")
    doc.svg(F["first"], "没有 visited: 汇合点被重复处理, 13 次 vs 7 次; 有 visited: 每个点 1 次, 重复到达的边被红虚线挡掉。")
    doc.p("<b>BFS vs DFS 怎么选:</b> 只要\"最少几步 / 最短路 (边权相同)\" 就用 BFS: queue 里永远只有相邻两层, "
          "第 k 层的点离起点正好 k 条边, 第一次碰到目标就是最短。"
          "只要\"有没有 / 有几块 / 复制 / 收集\" 两个都行, DFS 写起来更短。")
    doc.code(CODE["template"])
    doc.note("visited 是 graph 题的第一反应。BFS 在<b>入队时</b>标记, DFS 在<b>进入时</b>标记。点数 V, 边数 E, 总是 O(V + E)。")

    # ---------------------------------------------------------------- 1
    doc.h2("1. Number of Islands: grid DFS flood fill, 进来先 sink")
    doc.p("<b>题目:</b> grid 里 \"1\" 是陆地, \"0\" 是水, 上下左右相连的陆地算一个 island, 数有几个。"
          "例: <code>[\"11000\",\"10010\",\"00110\",\"00001\"]</code> → 3。")
    doc.p("<b>Brute force:</b> 对每个陆地格子各跑一次搜索, 各自找出它的连通块, 再给连通块去重 → 最坏 $O((mn)^2)$。"
          "<b>浪费:</b> 同一个 island 里的每个格子都把整块 island 重新搜一遍。")
    doc.p("<b>关键观察:</b> 搜过的格子就不会再有新信息。让所有搜索<b>共享一份 visited</b> (直接把 \"1\" 改成 \"0\"), "
          "那么扫描时遇到的 \"1\" 一定属于一个没见过的 island, 一次 dfs 把整块吃掉。")
    doc.svg(F["isl_core"], "grid 的 4 个方向就是 4 条边; dfs 入口的三道防线里, \"已 sink\"就是 visited 检查。")
    doc.svg(F["isl_tr"], "每次扫描遇到 1 → count += 1 → dfs 把整块 sink; 3 次触发 = 3 个 island。")
    doc.code(CODE["islands"])
    doc.p("<b>Time</b> $O(mn)$: 外层扫描每格一次; dfs 每个陆地格只会\"真正展开\"一次 (进入即 sink), 每格检查 4 个邻居。"
          "<b>Space</b> $O(mn)$: 整个 grid 是一个 island 时递归栈最深 $mn$。"
          "Python 默认递归深度 1000, grid 很大时换成显式 stack 或 BFS, 逻辑不变。")
    doc.p("<b>变体 Max Area of Island:</b> 同样的 dfs, 让它返回\"这块有多少格\", 外层取 max。只改一行:")
    doc.code(CODE["maxarea"])
    doc.note("grid 连通块 = 外层扫描 + dfs 原地标记。数块数: 触发次数; 求面积: dfs 返回格数。")

    # ---------------------------------------------------------------- 2
    doc.h2("2. Rotting Oranges: multi-source BFS, 所有源点一起入队")
    doc.p("<b>题目:</b> 0 空, 1 新鲜, 2 烂。每分钟烂橘子把上下左右的新鲜橘子变烂。问全部变烂要几分钟, 不可能返回 -1。"
          "和上一题的区别: 起点不止一个, 而且要\"最短时间\"。")
    doc.p("<b>Brute force:</b> 每分钟把整个 grid 扫一遍, 让烂橘子感染邻居, 直到没变化 → 每分钟 $O(mn)$, 最多 $mn$ 分钟 → $O((mn)^2)$。"
          "<b>浪费:</b> 每分钟都重新扫所有格子, 但真正会传染的只有\"刚变烂的\"那一圈, 烂了很久的早就没有新鲜邻居了。")
    doc.p("<b>关键观察:</b> 只保留\"刚变烂的那一圈\" = BFS 的一层。每一层 = 1 分钟, <code>len(q)</code> 就是这一层的大小。"
          "多个源点怎么办? 想象一个虚拟起点连到所有烂橘子, 距离 0 → 实际上就是<b>把所有初始烂橘子一起放进 queue</b> 当作第 0 层。")
    doc.svg(F["rot_core"], "multi-source BFS = 虚拟源点 S* 连到所有源点; 层与层之间正好差 1 分钟。")
    doc.svg(F["rot_tr"], "每一行 = 一分钟: popleft 一整层, 新烂的 push 进 queue, fresh 减去新烂的个数。")
    doc.code(CODE["rotting"])
    doc.p("<b>Time</b> $O(mn)$: 每个橘子变烂时入队一次、出队一次。<b>Space</b> $O(mn)$: queue 最大是一层的大小。")
    doc.note("\"离最近的 X 有多远\" / \"同时扩散\" → 所有源点一起入队。层数 = 距离。分层写法: <code>for _ in range(len(q))</code>。")

    # ---------------------------------------------------------------- 3
    doc.h2("3. Word Ladder: 隐式图上的 BFS 最短路")
    doc.p("<b>题目:</b> 每次只能改一个字母, 且改完的词必须在词典里。求 beginWord 变到 endWord 的最短序列长度 (单词个数)。"
          "例: hit → cog, 词典 [hot, dot, dog, lot, log, cog] → 5 (hit → hot → dot → dog → cog)。"
          "和上一题的区别: 没有 grid, 点是单词, 邻居\"改一个字母\"要自己生成。")
    doc.p("<b>Brute force:</b> DFS 枚举所有变换路径取最短 → 指数级。或者先两两比较建 graph, $O(N^2 L)$, 再 BFS。"
          "<b>浪费:</b> 枚举路径是在重复探索同一个词; 两两比较则为了建一张只用一次的图付了 $N^2$。")
    doc.p("<b>关键观察:</b> 无权最短路 → BFS。邻居不用预先建图: 对当前词的每一位换 26 个字母, 在不在词典里直接查 set, 一个词有 $26L$ 个候选。"
          "把 <code>words</code> 当作\"没访问过的词\", 找到一个就 remove → remove 就是 visited。")
    doc.svg(F["lad_core"], "隐式图按层展开: 层号 = 路径上的单词数; 同层之间的边 (灰虚线) 两端都已 visited, 不会走。")
    doc.svg(F["lad_tr"], "每一行 = 一层: popleft 整层, 找到的新词从 words 里 remove 并入队; cog 在 level 5 被取出。")
    doc.code(CODE["ladder"])
    doc.p("<b>Time</b> $O(N \\cdot L \\cdot 26 \\cdot L)$: 每个词最多出队一次 (入队前已 remove), 每个词 $26L$ 个候选, 每个候选拼字符串 + 查 set 是 $O(L)$。"
          "<b>Space</b> $O(NL)$。")
    doc.p("<b>变体 Open the Lock:</b> 点 = 4 位数字串 \"0000\"..\"9999\", 邻居 = 某一位 ±1 (8 个), deadends 一开始就放进 visited。其余和这题一模一样。")
    doc.note("状态本身当节点 (单词 / 密码锁 / 位置+钥匙) + 无权最短路 → 隐式图 BFS。邻居现算, visited 存状态, 层数 = 答案。")

    # ---------------------------------------------------------------- 4
    doc.h2("4. Course Schedule: 拓扑排序 (Kahn), indegree 归零才入队")
    doc.p("<b>题目:</b> numCourses 门课, <code>[a, b]</code> 表示上 a 之前必须先上 b。问能不能全部上完 (有环就不行)。"
          "例: n = 6, prerequisites = [[2,0],[2,1],[3,2],[4,2],[5,3],[5,4]] → True。"
          "和上一题的区别: 边有方向, 问的是\"依赖是否满足\", 不是最短路。")
    doc.p("<b>Brute force:</b> 每一轮扫描所有课, 找\"前置课都上完了\"的课去上, 直到没有可上的 → 每轮 $O(V + E)$, 最多 $V$ 轮 → $O(V(V+E))$。"
          "<b>浪费:</b> 每轮都在重新数每门课还差几门前置课, 而上完一门课只会影响它的后继。")
    doc.p("<b>关键观察:</b> 维护 <code>indegree[v]</code> = v 还没上完的前置课数。上完 u 时, 只给 u 的后继 −1; 减到 0 就入队。"
          "每条边恰好减一次 → $O(V + E)$。")
    doc.svg(F["cs_core"], "indegree[2] 从 2 减到 0 的过程: 0 和 1 都 pop 之后, 2 的前置课才算全部上完, 它才可以入队。")
    doc.svg(F["cs_tr"], "每一行: pop u → 对 u 的后继 indegree 减 1 → 变 0 的 push → order 追加 u。6 门课全部 pop = 无环。")
    doc.code(CODE["canfinish"])
    doc.p("<b>Time</b> $O(V + E)$: 建图 $O(V + E)$, 每个点入队一次, 每条边减一次。<b>Space</b> $O(V + E)$: 邻接表 + indegree + queue。")
    doc.note("有依赖顺序 / 能不能完成 / 编译顺序 → 拓扑排序。入度为 0 的先入队, 每 pop 一个就把后继的入度减 1。")

    # ---------------------------------------------------------------- 5
    doc.h2("5. Course Schedule II: 同一个模板, 记下 pop 的顺序")
    doc.p("<b>题目:</b> 和上一题一样, 但要返回一个合法的上课顺序; 有环返回 <code>[]</code>。"
          "<b>改哪里:</b> 把 <code>done</code> 计数换成 <code>order</code> 列表, 最后检查 <code>len(order) == numCourses</code>。")
    doc.p("<b>Brute force:</b> 枚举 $V!$ 种排列逐个检查依赖 → 指数级。"
          "<b>关键观察:</b> Kahn 里每个点\"入队 ⇔ 所有前置课都已经在 order 里\", 所以 pop 的顺序本身就是合法顺序, 不用额外生成。"
          "有环时, 环上的点互相等对方, indegree 永远减不到 0, 永远进不了 queue → order 不够长。")
    doc.svg(F["fo_core"], "环 1 ⇄ 2: 两个点的 indegree 都是 1, 谁也等不到对方先上 → 卡住; order 只有 3 个。")
    doc.svg(F["fo_tr"], "0 → 3 → 4 顺利 pop; queue 空了, 1 和 2 的 indegree 还是 1 (红), len(order) = 3 < 5 → 返回 []。")
    doc.code(CODE["findorder"])
    doc.p("<b>Time</b> $O(V + E)$, <b>Space</b> $O(V + E)$。")
    doc.p("<b>同模板的题:</b> Alien Dictionary — 先比较相邻两个单词, 第一个不同的字母给出一条边 a → b, 再对字母图跑 Kahn。"
          "另一种有环检测: DFS 三色标记 (未访问 / 访问中 / 已完成), 走到\"访问中\"的点就是有环。")
    doc.note("Kahn 的 pop 顺序 = 拓扑序; <code>len(order) &lt; n</code> = 有环。要字典序最小就把 queue 换成 heap。")

    # ---------------------------------------------------------------- 6
    doc.h2("6. Clone Graph: DFS + Hash Table (old → new)")
    doc.p("<b>题目:</b> 给一个无向连通图的一个节点 (有 <code>.val</code> 和 <code>.neighbors</code>), 返回整个图的深拷贝。"
          "和前面的区别: 遍历的同时要<b>构造</b>一个新图, 还需要记住\"这个旧节点对应哪个新节点\"。")
    doc.p("<b>Brute force:</b> 走到哪就 <code>Node(old.val)</code> 新建一个, 再递归复制 neighbors, 不记录。"
          "环 → 无限递归; 就算没有死循环, 同一个旧节点被不同的邻居走到时会生成多个副本, 图的结构就错了。"
          "<b>浪费 / 丢掉的信息:</b> 没记住\"这个旧节点已经有副本了, 副本是谁\"。")
    doc.p("<b>关键观察:</b> Hash Table <code>old2new</code> 同时扮演两个角色: visited (有没有复制过) + 副本查找 (它的副本是谁)。"
          "关键顺序: <b>先登记, 再递归 neighbors</b>。")
    doc.svg(F["cl_core"], "先登记再递归: 绕一圈回到 1 时已在 old2new, 直接返回 1', 环被切断; 先递归后登记会无限递归。")
    doc.svg(F["cl_tr"], "9 次 dfs 调用: 4 次 miss (新建 + 登记 + 递归), 5 次 hit (直接返回已有副本); old2new 最终 4 项。")
    doc.code(CODE["clone"])
    doc.p("<b>Time</b> $O(V + E)$: 每个节点复制一次, 每条边 (neighbors 列表项) 处理一次。<b>Space</b> $O(V)$: old2new + 递归栈。")
    doc.note("复制 / 序列化带环的结构 → <code>old2new</code> 字典, 创建后<b>立刻</b>登记, 再递归。同样适用于 Copy List with Random Pointer。")

    # ---------------------------------------------------------------- 7
    doc.h2("7. Number of Provinces: Union-Find (path compression + union by size)")
    doc.p("<b>题目:</b> n 个城市, <code>isConnected[i][j] == 1</code> 表示直接相连 (相连关系可以传递)。问有几个 province (连通块)。"
          "例 (trace): n = 7, 边 (0,1) (2,3) (0,2) (4,5) (3,5) → 2 个 (0..5 一块, 6 一块)。")
    doc.p("<b>Brute force:</b> 这一题用 DFS/BFS 数连通块一次就是 $O(V + E)$, 没问题。"
          "但如果<b>边是一条条加进来、随时问\"a 和 b 连通吗\"</b>, 每次问都重新 BFS 就是 $O(V + E)$ 一次。"
          "<b>浪费:</b> 上一次已经算出的连通信息没有保存。")
    doc.p("<b>关键观察:</b> 只需要保存\"谁和谁在同一个集合\": 每个集合选一个 root, 每个点存 <code>parent</code>, 顺着 parent 走到 root。"
          "<code>find(a) == find(b)</code> 就是连通。两个优化让它几乎 $O(1)$: "
          "<b>union by size</b> (小树挂大树, 树高 ≤ $\\log n$), <b>path compression</b> (find 时把路径上的点直接挂到 root)。")
    doc.svg(F["uf_core"], "无优化: 链, find 要 O(n); union by size 让树变矮; path compression 把走过的路径拍平。")
    doc.svg(F["uf_tr"], "5 次 union: 前 4 次是合并; 第 5 次 find(3) 顺手压缩 parent[3] 2→0; count 7 → 2。")
    doc.code(CODE["dsu"])
    doc.code(CODE["provinces"])
    doc.p("<b>Time</b> $O(n^2 \\cdot \\alpha(n))$ (要读完整个矩阵 $n^2$; 若输入是边列表则是 $O((n + E)\\,\\alpha(n))$, $\\alpha$ 是反 Ackermann, 实际 ≤ 4)。"
          "<b>Space</b> $O(n)$。")
    doc.p("<b>变体 Accounts Merge:</b> 点 = account 下标, 两个 account 共用一个 email 就 union; 最后按 root 把 email 归并、排序。"
          "只多了一个 <code>email → 第一次见到它的 account</code> 的字典:")
    doc.code(CODE["accounts"])
    doc.note("\"连通块 / 合并集合 / 动态加边问连不连通 / 无向图有没有环\" → Union-Find。"
             "<code>union</code> 返回 False = 这条边的两端早已连通 = 成环 (Graph Valid Tree)。")

    # ---------------------------------------------------------------- 8
    doc.h2("8. Network Delay Time: Dijkstra (heap)")
    doc.p("<b>题目:</b> n 个点, <code>times[i] = [u, v, w]</code> 表示 u → v 耗时 w。从 k 发信号, 问所有点都收到至少要多久, 收不到返回 -1。"
          "例: n = 5, k = 1, 6 条边 (见图) → 7。"
          "和前面的区别: 边有<b>权重</b>, BFS 的\"层数\"不再等于距离。")
    doc.p("<b>Brute force:</b> Bellman-Ford: 对所有边重复松弛 $V - 1$ 轮 → $O(VE)$。"
          "<b>浪费:</b> 每一轮都把所有边再松弛一遍, 但绝大多数边的起点 dist 这一轮根本没变。")
    doc.p("<b>关键观察 (贪心):</b> 所有候选距离里<b>最小的那个一定已经是最终答案</b> (边权 ≥ 0, 绕路只会更长)。"
          "所以用 min-heap 每次取出当前最近的点, 只对它的出边松弛一次。"
          "heap 里的旧记录不删, 弹出时发现 <code>d &gt; dist[u]</code> 就跳过 (lazy deletion)。")
    doc.svg(F["dj_core"], "已确定区域 {1, 3}; heap 顶 (3, 2) 是最小候选, 任何别的路径出了这个区域都至少 3, 所以 dist[2] = 3 是最终值。")
    doc.svg(F["dj_tr"], "8 行: 6 次有效弹出 + 2 次过期记录 (4,2) 和 (6,4) 被 skip; dist 最终 [0, 3, 1, 4, 7] → 答案 7。")
    doc.code(CODE["dijkstra"])
    doc.p("<b>Time</b> $O(E \\log V)$: 每条边最多 push 一次, heap 操作 $O(\\log)$。<b>Space</b> $O(V + E)$。")
    doc.p("<b>变体 Cheapest Flights Within K Stops:</b> 限制最多 k 次中转 = 最多 k+1 条边。"
          "Dijkstra 的\"最小的就是最终\"在有边数限制时不成立 (便宜但绕远的路可能把边数用光), "
          "改用 <b>Bellman-Ford 只松弛 k+1 轮</b> (或 BFS, 状态带\"已用边数\"):")
    doc.code(CODE["flights"])
    doc.note("边权不同 + 非负 → Dijkstra: heap 存 (dist, node), 弹出时过期就 skip, 对出边 relax。边权全 1 → 普通 BFS 就够。有边数限制 → Bellman-Ford 跑 k+1 轮。")

    # ---------------------------------------------------------------- signals
    doc.h2("9. 识别信号: 看到什么 → 试什么")
    rows = [
        ("grid / 矩阵 + 连通区域 (数块数、面积、sink)", "grid DFS (或 BFS) + 原地标记 visited", "每格被重复搜索 O((mn)²) → O(mn)"),
        ("最少步 / 最短路, 边权相同 (grid 最短路、单词变换、开锁)", "BFS 按层, 层数 = 距离", "枚举所有路径 指数 → O(V + E)"),
        ("同时从多个源点扩散 / 离最近的 X 多远", "multi-source BFS: 所有源点一起入队", "每个源点各跑一次 O(k(V + E)) → O(V + E)"),
        ("状态本身是节点 (词、密码锁、(位置, 钥匙))", "隐式图 BFS: 邻居现算, visited 存状态", "预先建整张图 O(N²) → 按需生成邻居"),
        ("先后依赖 / 排课 / 编译顺序 / 有没有环", "拓扑排序 Kahn: indegree + queue", "每轮重扫找可上的课 O(V(V + E)) → O(V + E)"),
        ("复制 / 序列化带环的图", "DFS + old2new Hash Table, 先登记再递归", "无限递归 / 重复副本 → O(V + E)"),
        ("连通块 / 合并集合 / 动态加边问连通 / 无向图判环", "Union-Find (path compression + union by size)", "每次查询 BFS O(V + E) → 近 O(1)"),
        ("非负权重最短路", "Dijkstra: min-heap 存 (dist, node)", "Bellman-Ford O(VE) → O(E log V)"),
        ("最短路 + 最多 k 次中转 / 带边数限制", "Bellman-Ford 跑 k+1 轮, 或 BFS 状态带层数", "Dijkstra 不再适用; O(k·E)"),
        ("有负权边", "Bellman-Ford (不能用 Dijkstra)", "O(VE)"),
    ]
    t = ['<table><tr><th>特征</th><th>做法</th><th>complexity 从 → 到</th></tr>']
    for a, b, c in rows:
        t.append("<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (a, b, c))
    t.append("</table>")
    doc.raw("".join(t))
    doc.note("先问三件事: 边有没有权重? 要不要最短? 有没有方向 / 依赖? "
             "无权最短 → BFS; 有权 → Dijkstra; 有依赖 → 拓扑; 只问连不连通 → DFS 或 Union-Find。")

    doc.h2("以后再学")
    doc.p("Tarjan SCC / 桥; Floyd-Warshall (全源最短路); MST (Kruskal 用本篇的 Union-Find, Prim 用 heap); "
          "Hierholzer 欧拉路径 (Reconstruct Itinerary); 双向 BFS; A*; 二分图染色 (BFS/DFS 两种颜色交替)。")
    doc.write("docs/%s.html" % SLUG)


if __name__ == "__main__":
    build_doc(build_figs())
