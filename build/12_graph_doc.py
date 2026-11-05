# 12 · Graph 正文 (NeetCode 式讲法)。由 12_graph.py 的 build_doc(F) exec, 共用 F / CODE / NS / SLUG。
import nclib as nc
from counts import cnt

EX = os.path.join(d.ROOT, "docs", "svg", SLUG, "%s_examples.svg")
EXS = SLUG + "/%s_examples.svg"


def grid_rows(g, roles_fn):
    return [("row %d" % r, row, [roles_fn(r, c, v) for c, v in enumerate(row)]) for r, row in enumerate(g)]


# ---------------------------------------------------------------- 例子图
g1 = [["1", "1", "0", "0", "0"], ["1", "1", "0", "0", "0"], ["0", "0", "1", "0", "0"], ["0", "0", "0", "1", "1"]]
assert NS["numIslands"]([r[:] for r in g1]) == 3
nc.examples_svg(EX % "islands", "Number of Islands examples",
                ["grid 里 '1' 是陆地, '0' 是水。上下左右相连的陆地算同一个 island (斜着不算)。数一共有几个 island"], [
    dict(title="Example:  →  3", index=False, rows=grid_rows(g1, lambda r, c, v: "new" if v == "1" else "keep"),
         extra=["左上角 4 个 1 连成一块; 中间 1 个自己一块; 右下 2 个连成一块 → 3 个", "(2,2) 和 (3,3) 是斜着挨的, 不算相连"])],
    legend=[("new", "陆地 '1'"), ("keep", "水 '0'")])

g2 = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]
assert NS["orangesRotting"]([r[:] for r in g2]) == 4
assert NS["orangesRotting"]([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1
nc.examples_svg(EX % "rotting", "Rotting Oranges examples",
                ["0 空格, 1 新鲜橘子, 2 烂橘子。每过 1 分钟, 烂橘子会让上下左右的新鲜橘子也烂掉。求全部烂掉要几分钟, 做不到返回 -1"], [
    dict(title="Example 1:  [[2,1,1],[1,1,0],[0,1,1]]  →  4", index=False,
         rows=grid_rows(g2, lambda r, c, v: "rem" if v == 2 else ("new" if v == 1 else "keep")),
         extra=["第 1 分钟: (0,1)(1,0) 烂;  第 2 分钟: (0,2)(1,1);  第 3 分钟: (2,1);  第 4 分钟: (2,2) → 4"]),
    dict(title="Example 2:  [[2,1,1],[0,1,1],[1,0,1]]  →  -1", index=False,
         rows=grid_rows([[2, 1, 1], [0, 1, 1], [1, 0, 1]], lambda r, c, v: "rem" if v == 2 else ("new" if v == 1 else "keep")),
         extra=["左下角 (2,0) 的橘子四周不是边界就是空格, 永远烂不到 → -1"])],
    legend=[("rem", "烂橘子 2"), ("new", "新鲜 1"), ("keep", "空格 0")])

assert NS["ladderLength"]("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]) == 5
assert NS["ladderLength"]("hit", "cog", ["hot", "dot", "dog", "lot", "log"]) == 0
nc.examples_svg(EX % "ladder", "Word Ladder examples",
                ["从 beginWord 变到 endWord, 每一步只能改一个字母, 而且每一步得到的词必须在 wordList 里。", "最少经过几个词 (包括头尾)"], [
    dict(title="Example 1:  hit → cog,  wordList = [hot,dot,dog,lot,log,cog]  →  5",
         items=["hit", "hot", "dot", "dog", "cog"], cw=60, hl=[0, 1, 2, 3, 4],
         extra=["hit → hot → dot → dog → cog, 每一步改一个字母, 共 5 个词 (也可以 hot → lot → log → cog)"]),
    dict(title="Example 2:  同上, 但 wordList 里没有 cog  →  0", extra=["终点不在 wordList 里, 到不了"])],
    legend=[("new", "最短的变换序列")])

assert NS["canFinish"](2, [[1, 0]]) and not NS["canFinish"](2, [[1, 0], [0, 1]])
nc.examples_svg(EX % "canfinish", "Course Schedule examples",
                ["n 门课, prerequisites[i] = [a, b] 表示上 a 之前必须先上完 b。问能不能把所有课都上完"], [
    dict(title="Example 1:  n = 2, prerequisites = [[1,0]]  →  True", items=["0", "→", "1"], cw=44, hl=[0, 2], index=False,
         extra=["先上 0, 再上 1"]),
    dict(title="Example 2:  n = 2, prerequisites = [[1,0],[0,1]]  →  False", items=["0", "⇄", "1"], cw=44, bad=[(0, 2, "互相等对方: 环")],
         index=False, extra=["上 1 要先上 0, 上 0 又要先上 1, 谁都上不了 → 有环就做不到"])],
    legend=[("new", "能上的课"), ("rem", "环")])

o = NS["findOrder"](4, [[1, 0], [2, 0], [3, 1], [3, 2]])
assert o.index(0) < o.index(1) < o.index(3) and o.index(2) < o.index(3)
nc.examples_svg(EX % "findorder", "Course Schedule II examples", ["同上, 但要返回一个可行的上课顺序; 做不到返回 []"], [
    dict(title="Example:  n = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]  →  [0,1,2,3] 或 [0,2,1,3]",
         items=["0", "1", "2", "3"], index=False,
         extra=["0 没有前置课, 最先上; 1 和 2 都只要 0; 3 要 1 和 2 都上完。答案不唯一"])],
    legend=[])

nc.examples_svg(EX % "clone", "Clone Graph examples",
                ["给一个无向图里的一个 node, 返回整个图的深拷贝 (deep copy): 每个 node 都是新建的, 连接关系和原来完全一样"], [
    dict(title="Example:  adjList = [[2,4],[1,3],[2,4],[1,3]]", items=["1", "2", "3", "4"], index=False,
         extra=["node 1 连着 2 和 4, node 2 连着 1 和 3, ... 四个点围成一个环 1-2-3-4-1",
                "新图里不能有任何一个 node 是原来的对象, 只是值和连接一样"])],
    legend=[])

assert NS["findCircleNum"]([[1, 1, 0], [1, 1, 0], [0, 0, 1]]) == 2
nc.examples_svg(EX % "uf", "Number of Provinces examples",
                ["n 个城市, isConnected[i][j] = 1 表示 i 和 j 直接相连。", "相连 (直接或间接) 的城市属于同一个 province。数有几个 province"], [
    dict(title="Example:  isConnected = [[1,1,0],[1,1,0],[0,0,1]]  →  2", index=False,
         rows=[("城市 0", [1, 1, 0], ["new", "new", "keep"]), ("城市 1", [1, 1, 0], ["new", "new", "keep"]),
               ("城市 2", [0, 0, 1], ["keep", "keep", "new"])],
         extra=["0 和 1 相连, 是一个 province; 2 自己一个 → 2"])],
    legend=[("new", "相连 (1)")])

assert NS["networkDelayTime"]([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2) == 2
nc.examples_svg(EX % "dijkstra", "Network Delay Time examples",
                ["n 个节点, times[i] = (u, v, w): 信号从 u 传到 v 要 w 时间。从 k 发出信号, 多久之后所有节点都收到? 有收不到的返回 -1"], [
    dict(title="Example:  times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2  →  2", items=["2→1: 1", "2→3: 1", "3→4: 1"], cw=80,
         index=False, extra=["节点 1 在时刻 1 收到, 3 在时刻 1, 4 在时刻 1 + 1 = 2。最后一个收到的是 4 → 2",
                             "也就是: 从 k 到每个节点的最短路径, 取其中最大的"])],
    legend=[])

# ================================================================ HTML
doc = d.Doc("12 · Graph: BFS / DFS / Topological Sort / Union-Find / Dijkstra")
doc.h2("这篇讲什么")
doc.p("graph (图) 由 node (点) 和 edge (边) 组成。tree 是一种特殊的 graph (没有环)。面试里的 graph 很多时候是<b>藏起来</b>的:")
nc.bullets(doc, "<b>grid</b>: 每个格子是一个 node, 上下左右相邻的格子之间有边。",
           "<b>隐式图</b>: 比如单词, 改一个字母能变成的另一个单词就是邻居。",
           "<b>依赖关系</b>: 课程 a 依赖课程 b, 就是一条 b → a 的边。")
doc.p("所有 graph 题的基础都是<b>遍历</b>: 从某个点出发, 把能到达的点都走一遍。和 tree 最大的不同是: graph 里可能有<b>环</b>, 或者多条路走到同一个点。所以必须记录 <code>visited</code>, 保证每个点只处理一次。这样总共是 <code>O(V + E)</code> (点数 + 边数)。")
doc.svg(F["first"], "没有 visited: 汇合点被重复处理, 13 次; 有 visited: 每个点 1 次, 共 7 次, 重复到达的边被挡掉 (红色虚线)。")
doc.p("遍历有两种方式, 用途不同:")
nc.bullets(doc, "<b>DFS</b> (depth-first, 深度优先): 一条路走到底再回头, 用 recursion 写。适合\"把连在一起的都找出来\"。",
           "<b>BFS</b> (breadth-first, 广度优先): 一层一层往外扩, 用 queue 写。<b>BFS 的层数就是最短距离</b> (每条边长度都是 1 时)。适合\"最少几步\"。")
nc.solution(doc, CODE["template"], summary="BFS / DFS / grid 邻居 的模板代码")
nc.table(doc, ["#", "题目", "考过的公司数", "相比上一题多了什么"], [
    ["1", "Number of Islands", cnt("Number of Islands"), "模板题: grid 上的 DFS, 数连通块"],
    ["2", "Rotting Oranges", cnt("Rotting Oranges"), "BFS 按层扩散, 多个起点同时出发"],
    ["3", "Word Ladder", cnt("Word Ladder"), "图是隐式的, BFS 求最短路"],
    ["4", "Course Schedule", cnt("Course Schedule"), "有方向的依赖关系: 拓扑排序判断有没有环"],
    ["5", "Course Schedule II", cnt("Course Schedule II"), "同上, 输出顺序"],
    ["6", "Clone Graph", cnt("Clone Graph"), "遍历的同时复制, 用 dict 记 old → new"],
    ["7", "Number of Provinces", cnt("Number of Provinces"), "Union-Find: 合并集合"],
    ["8", "Network Delay Time", cnt("Network Delay Time"), "边有长度: Dijkstra"]])
doc.p("每道题的顺序: <b>题目在问什么 → 看例子 → brute force → intuition → 算法 → 手动走一遍 → 复杂度</b>。代码放在最后, 默认折叠。")

# ================================================================ 1
doc.h2("1. Number of Islands")
doc.h3("题目在问什么")
doc.p("一个 grid, <code>'1'</code> 是陆地, <code>'0'</code> 是水。上下左右相连的陆地属于同一个 island (斜着挨着不算)。问一共有几个 island。")
doc.h3("看例子")
doc.svg(EXS % "islands", "例子。")
doc.h3("Brute force")
doc.p("这题本身就没有比 <code>O(m·n)</code> 更好的做法, 每个格子至少要看一次。难点不是优化, 而是\"怎么知道哪些 1 是连在一起的\"。")
doc.h3("Intuition: 找到一块陆地, 就把整个 island 淹掉")
doc.p("从左上到右下扫每个格子。遇到一个 <code>'1'</code>, 说明发现了一个新 island, count 加 1。")
doc.p("然后从这个格子出发做 DFS: 往上下左右四个方向走, 只要是 '1' 就继续走, 把这个 island 上所有的格子都走一遍, 并且<b>把走过的格子改成 '0'</b> (淹掉)。")
doc.p("淹掉有两个作用: 一是当作 visited, 防止走回头路; 二是之后继续扫描时, 这个 island 的其他格子已经是 0 了, 不会被重复计数。")
doc.h3("算法")
nc.steps(doc, "遍历每个格子 (r, c)。如果是 '1': count += 1, 调用 <code>dfs(r, c)</code>。",
         "<code>dfs(r, c)</code>: 越界、或者不是 '1', 直接返回。否则把它改成 '0', 再对上下左右四个邻居调用 dfs。")
doc.svg(F["isl_core"], "grid 的 4 个方向就是 4 条边; dfs 入口的三个检查 (越界、是水、已淹掉) 里, \"已淹掉\"就是 visited。")
doc.h3("手动走一遍")
doc.svg(F["isl_tr"], "每次扫描遇到 1 → count += 1 → dfs 把整块淹掉; 触发 3 次 = 3 个 island。")
doc.h3("复杂度")
doc.p("Time <code>O(m·n)</code>: 每个格子最多被淹一次。Space <code>O(m·n)</code>: 最坏 recursion 深度 (全是陆地)。")
doc.p("变体 Max Area of Island: dfs 返回这一块的格子数 (<code>1 + 四个方向的和</code>), 取最大值。")
nc.solution(doc, CODE["islands"], CODE["maxarea"])
doc.note("数连通块: 扫一遍, 遇到没访问过的就 count += 1, 再 DFS 把整块标记掉。grid 上可以直接改格子当 visited。")

# ================================================================ 2
doc.h2("2. Rotting Oranges")
doc.h3("题目在问什么")
doc.p("grid 里 0 是空格, 1 是新鲜橘子, 2 是烂橘子。每过一分钟, 每个烂橘子会让它上下左右的新鲜橘子也烂掉。问: 最少几分钟后所有橘子都烂了? 如果有橘子永远烂不到, 返回 -1。")
doc.h3("看例子")
doc.svg(EXS % "rotting", "两个例子。")
doc.h3("Brute force")
doc.p("模拟: 每一分钟扫一遍整个 grid, 把所有烂橘子旁边的新鲜橘子标成烂的, 直到没有变化。每分钟 <code>O(m·n)</code>, 最多 <code>m·n</code> 分钟, <code>O((m·n)²)</code>。")
doc.p("浪费: 每一分钟都重新扫整个 grid, 但真正会变化的只有\"刚烂掉的那一批\"的邻居。")
doc.h3("Intuition: BFS 的一层就是一分钟")
doc.p("BFS 是一层一层往外扩的。第 0 层是起点, 第 1 层是离起点 1 步的点, 第 2 层是 2 步的……这和\"每分钟往外烂一格\"完全一样。")
doc.p("特别的是, 这题有<b>好几个起点</b> (一开始就烂的橘子都是起点), 它们同时开始扩散。做法很简单: 一开始把所有烂橘子<b>一起</b>放进 queue, 当作第 0 层。这叫 multi-source BFS。")
doc.p("然后每一轮处理一整层 (和 11 里 level order 一样, 先记下 <code>len(q)</code>), 每处理完一层, 分钟数加 1。")
doc.p("同时数一下新鲜橘子的个数 fresh。每烂一个就减 1。最后 fresh 还大于 0, 说明有烂不到的, 返回 -1。")
doc.h3("算法")
nc.steps(doc, "扫一遍 grid: 所有 2 放进 queue, 数出 fresh。",
         "当 queue 不空且 <code>fresh > 0</code>: 处理一整层。对每个烂橘子, 看四个邻居, 是 1 就改成 2、fresh 减 1、放进 queue。这一层处理完, <code>minutes += 1</code>。",
         "返回 <code>minutes if fresh == 0 else -1</code>。")
doc.svg(F["rot_core"], "multi-source BFS = 想象一个虚拟起点连到所有烂橘子; 层与层之间正好差 1 分钟。")
doc.h3("手动走一遍")
doc.svg(F["rot_tr"], "每一行 = 一分钟: 取出一整层, 新烂的放进 queue, fresh 减去新烂的个数。")
doc.h3("复杂度")
doc.p("Time <code>O(m·n)</code>, Space <code>O(m·n)</code>。")
nc.solution(doc, CODE["rotting"])
doc.note("从多个地方同时扩散、问几步 / 几分钟: multi-source BFS, 所有起点一起放进 queue 当第 0 层。")

# ================================================================ 3
doc.h2("3. Word Ladder")
doc.h3("题目在问什么")
doc.p("从 <code>beginWord</code> 变到 <code>endWord</code>, 每一步只能改一个字母, 而且每一步变出来的词必须在 <code>wordList</code> 里。求最短的变换序列有几个词 (包括头和尾)。变不到返回 0。")
doc.h3("看例子")
doc.svg(EXS % "ladder", "两个例子。")
doc.h3("Brute force")
doc.p("DFS 枚举所有变换路径, 取最短的。路径数量是指数级的。")
doc.h3("Intuition: 这是一个图, 求最短路就用 BFS")
doc.p("把每个单词看成一个 node。两个单词只差一个字母, 它们之间就有一条边。问题就变成: 在这个图上, 从 beginWord 到 endWord 的<b>最短路径</b>。")
doc.p("每条边的长度都是 1 (改一个字母算一步), 所以 BFS 第一次到达 endWord 时的层数, 就是答案。")
doc.p("这个图不用提前建出来。要找一个词的邻居, 就把它的每个位置换成 a 到 z, 看换出来的词在不在 wordList 里 (用 set, <code>O(1)</code>)。")
doc.p("visited 的处理: 一个词一旦被放进 queue, 就从 set 里删掉, 这样它不会再被访问。")
doc.h3("算法")
nc.steps(doc, "<code>words = set(wordList)</code>。queue 放进 <code>(beginWord, 1)</code>。",
         "每次取出 (word, level)。是 endWord 就返回 level。",
         "对 word 的每个位置、每个字母 a–z: 换出来的 new 在 words 里, 就从 words 删掉, 放进 queue (level + 1)。",
         "queue 空了还没找到, 返回 0。")
doc.svg(F["lad_core"], "隐式图按层展开: 层号 = 路径上的单词数; 同一层之间的边 (灰色虚线) 两端都已经访问过, 不会走。")
doc.h3("手动走一遍")
doc.svg(F["lad_tr"], "每一行 = 一层: 取出整层, 找到的新词从 words 里删掉并放进 queue; cog 在第 5 层被取出。")
doc.h3("复杂度")
doc.p("Time <code>O(N·L·26)</code>, N 是单词数, L 是单词长度 (每个词有 L × 26 个候选, 每个候选拼字符串还要 <code>O(L)</code>)。Space <code>O(N·L)</code>。")
nc.solution(doc, CODE["ladder"])
doc.note("\"最少几步\" + 每一步代价相同: BFS。图可以是隐式的, 需要时再生成邻居。")

# ================================================================ 4
doc.h2("4. Course Schedule")
doc.h3("题目在问什么")
doc.p("一共 n 门课, 编号 0 到 n-1。<code>prerequisites[i] = [a, b]</code> 表示: 上 a 之前必须先上完 b。问能不能把所有课都上完。")
doc.h3("看例子")
doc.svg(EXS % "canfinish", "两个例子。")
doc.p("把每门课看成一个 node, \"b 是 a 的前置课\"画成一条 <code>b → a</code> 的有向边。上不完的唯一原因是<b>有环</b>: 几门课互相等对方。")
doc.h3("Brute force")
doc.p("从每个点出发做 DFS, 看能不能走回自己。每个点 <code>O(V + E)</code>, 共 <code>O(V·(V + E))</code>。")
doc.h3("Intuition: 先上没有前置课的, 上完就把它从图里去掉")
doc.p("想想现实里你会怎么排课: 先上那些<b>没有前置课</b>的。上完一门, 依赖它的那些课就少了一个前置要求。如果某门课的前置要求全部满足了, 它就可以上了。一直这样, 直到没有可以上的课。")
doc.p("如果最后所有课都上了, 就没有环; 如果还有课剩下, 剩下的那些一定是在互相等, 有环。")
doc.p("用一个数组 <code>indegree[v]</code> 记录 v 还有几门前置课没上。indegree 为 0 的课放进 queue。每上完一门 u, 把它所有的后继 v 的 indegree 减 1, 减到 0 就放进 queue。这个方法叫 <b>Kahn 算法</b>, 得到的顺序叫<b>拓扑排序</b> (topological sort)。")
doc.h3("算法")
nc.steps(doc, "建图: 每个 <code>[a, b]</code>, 加边 <code>b → a</code>, <code>indegree[a] += 1</code>。",
         "所有 indegree 为 0 的课放进 queue。",
         "每次取出 u, 计数 taken += 1。对 u 的每个后继 v: <code>indegree[v] -= 1</code>, 变成 0 就放进 queue。",
         "返回 <code>taken == n</code>。")
doc.svg(F["cs_core"], "indegree[2] 从 2 减到 0 的过程: 0 和 1 都上完之后, 2 的前置课才全部上完, 它才能进 queue。")
doc.h3("手动走一遍")
doc.svg(F["cs_tr"], "每一行: 取出 u → u 的后继 indegree 减 1 → 变 0 的放进 queue → order 加上 u。6 门课全部取出 = 没有环。")
doc.h3("复杂度")
doc.p("Time <code>O(V + E)</code>, Space <code>O(V + E)</code>。")
nc.solution(doc, CODE["canfinish"])
doc.note("有依赖关系 / 先后顺序 / 判断有向图有没有环: 拓扑排序 (Kahn)。indegree 为 0 的先处理。")

# ================================================================ 5
doc.h2("5. Course Schedule II")
doc.h3("题目在问什么")
doc.p("和第 4 题一样, 但要返回<b>一个可行的上课顺序</b>。上不完就返回空数组。")
doc.h3("看例子")
doc.svg(EXS % "findorder", "例子。")
doc.h3("Intuition: 记下取出的顺序")
doc.p("第 4 题里, 课从 queue 里被取出的顺序, 就是一个合法的上课顺序: 每门课被取出时, 它的前置课都已经被取出过了。所以只要把 taken 计数换成一个 list, 记下顺序。")
doc.p("最后 order 的长度不等于 n, 说明有环, 返回 []。")
doc.h3("算法")
nc.steps(doc, "和第 4 题一样, 每取出一个 u, 加到 order 里。", "返回 <code>order if len(order) == n else []</code>。")
doc.svg(F["fo_core"], "环 1 ⇄ 2: 两个点的 indegree 都是 1, 谁也等不到对方先上 → 卡住; order 只有 3 个。")
doc.h3("手动走一遍")
doc.svg(F["fo_tr"], "0 → 3 → 4 顺利取出; queue 空了, 1 和 2 的 indegree 还是 1 (红色), len(order) = 3 < 5 → 返回 []。")
doc.h3("复杂度")
doc.p("Time <code>O(V + E)</code>, Space <code>O(V + E)</code>。")
doc.p("Alien Dictionary 是同一个模板: 从相邻两个单词的第一个不同字母得到一条边 (哪个字母在前), 再做拓扑排序。")
nc.solution(doc, CODE["findorder"])
doc.note("要输出顺序: Kahn 算法里取出的顺序就是拓扑序。长度不够 n 就是有环。")

# ================================================================ 6
doc.h2("6. Clone Graph")
doc.h3("题目在问什么")
doc.p("给一个连通的无向图里的一个 node, 返回整个图的<b>深拷贝</b> (deep copy): 每个 node 都要新建, 新图的连接关系和原图完全一样, 但新图里不能有任何一个原来的 node 对象。")
doc.h3("看例子")
doc.svg(EXS % "clone", "例子。")
doc.h3("Brute force")
doc.p("先遍历一遍, 为每个旧 node 新建一个副本; 再遍历一遍, 把边连上。需要两遍, 而且第二遍要能从旧 node 找到对应的新 node, 所以还是要一个 dict。")
doc.h3("Intuition: 用 dict 记住\"这个 node 已经复制过了\"")
doc.p("用一个 dict <code>old2new</code>: key 是旧 node, value 是它的副本。它同时有两个作用: 从旧 node 找到副本, 以及当作 visited。")
doc.p("DFS 复制一个 node: 如果它已经在 old2new 里, 直接返回副本 (这一步切断了环, 否则会无限递归)。否则新建副本, <b>先登记进 old2new</b>, 再递归复制它的每个邻居, 把邻居的副本加进副本的邻居列表。")
doc.p("\"先登记再递归\"的顺序很重要: 图里有环, 递归可能会绕回来找自己。如果还没登记, 就会再建一个副本, 无限循环。")
doc.h3("算法")
nc.steps(doc, "<code>old2new = {}</code>。<code>dfs(node)</code>: 在 old2new 里就返回 <code>old2new[node]</code>。",
         "<code>copy = Node(node.val)</code>, <code>old2new[node] = copy</code>。",
         "对每个邻居 nb: <code>copy.neighbors.append(dfs(nb))</code>。返回 copy。")
doc.svg(F["cl_core"], "先登记再递归: 绕一圈回到 1 时已经在 old2new 里, 直接返回 1', 环被切断; 先递归后登记会无限递归。")
doc.h3("手动走一遍")
doc.svg(F["cl_tr"], "9 次 dfs 调用: 4 次没找到 (新建 + 登记 + 递归), 5 次找到 (直接返回已有的副本); old2new 最后有 4 项。")
doc.h3("复杂度")
doc.p("Time <code>O(V + E)</code>, Space <code>O(V)</code>。")
nc.solution(doc, CODE["clone"])
doc.note("复制带环的结构 (图、带 random 指针的 list): dict 记 old → new, 先登记再递归。")

# ================================================================ 7
doc.h2("7. Number of Provinces (Union-Find)")
doc.h3("题目在问什么")
doc.p("n 个城市, <code>isConnected[i][j] = 1</code> 表示城市 i 和 j 直接相连。直接或间接相连的城市属于同一个 province。问一共有几个 province。")
doc.h3("看例子")
doc.svg(EXS % "uf", "例子。")
doc.h3("Brute force")
doc.p("这题用第 1 题的 DFS 数连通块就能做, <code>O(n²)</code>。这里借它介绍另一个工具: <b>Union-Find</b>。它在\"边一条一条给出来, 随时问两个点是否相连\"的场景下特别好用。")
doc.h3("Intuition: 每个集合选一个\"代表\"")
doc.p("Union-Find (也叫 DSU) 维护一堆不相交的集合。每个集合用一棵树表示, 树根就是这个集合的代表。<code>parent[x]</code> 是 x 的父节点, 根的 parent 是自己。")
nc.bullets(doc, "<code>find(x)</code>: 顺着 parent 一直往上走, 找到根。两个点的根相同, 就在同一个集合。",
           "<code>union(a, b)</code>: 找到两个根, 如果不同, 把一个根接到另一个根下面, 两个集合就合并了。")
doc.p("不优化的话, 树可能变成一条长链, find 是 <code>O(n)</code>。两个优化:")
nc.bullets(doc, "<b>union by size</b>: 合并时把小的树接到大的树下面, 树不会变得太高。",
           "<b>path compression</b>: find 的时候, 把一路经过的点直接接到根上, 下次就一步到位。")
doc.p("两个优化一起用, 每次操作几乎是 <code>O(1)</code>。")
doc.p("这道题: 一开始每个城市自己一个集合, count = n。每条相连的边做一次 union, 真的合并了 (两个根不同) 就 count 减 1。")
doc.h3("算法")
nc.steps(doc, "<code>parent = list(range(n))</code>, <code>size = [1] * n</code>, <code>count = n</code>。",
         "对每个 <code>isConnected[i][j] == 1</code> (i < j): union(i, j), 合并成功就 count -= 1。",
         "返回 count。")
doc.svg(F["uf_core"], "不优化: 一条链, find 要 O(n); union by size 让树变矮; path compression 把走过的路径拍平。")
doc.h3("手动走一遍")
doc.svg(F["uf_tr"], "5 次 union: 前 4 次是合并; 第 5 次 find(3) 顺手把 parent[3] 从 2 压缩成 0; count 从 7 变成 2。")
doc.h3("复杂度")
doc.p("Time <code>O(n² · α(n))</code>, α 是一个增长极慢的函数, 可以当成常数。Space <code>O(n)</code>。")
doc.p("变体 Accounts Merge: 同一个邮箱出现在两个账户里, 就 union 这两个账户, 最后按根分组输出。")
nc.solution(doc, CODE["dsu"], CODE["provinces"], CODE["accounts"])
doc.note("动态地合并集合、问两个元素是否在同一组: Union-Find, 加上 union by size 和 path compression。")

# ================================================================ 8
doc.h2("8. Network Delay Time (Dijkstra)")
doc.h3("题目在问什么")
doc.p("n 个节点, 有向边 <code>(u, v, w)</code> 表示信号从 u 到 v 要 w 的时间。从节点 k 发出信号, 多久之后<b>所有</b>节点都收到? 有节点收不到就返回 -1。")
doc.p("换句话说: 求 k 到每个节点的最短路径, 再取其中最大的。")
doc.h3("看例子")
doc.svg(EXS % "dijkstra", "例子。")
doc.h3("Brute force")
doc.p("BFS 不能直接用了: BFS 的层数是\"经过几条边\", 但这里每条边的长度不一样, 边少的路径不一定短。")
doc.p("最直接的做法是反复\"放松\": 对所有边, 如果 <code>dist[u] + w < dist[v]</code> 就更新 dist[v], 重复 V - 1 轮 (Bellman-Ford)。<code>O(V·E)</code>。")
doc.h3("Intuition: 每次确定\"目前离起点最近\"的那个点")
doc.p("Dijkstra 的想法: 维护一个\"已确定\"区域, 里面每个点的最短距离都已经算好了。每一步, 在所有还没确定的点里, 选<b>当前距离最小</b>的那个, 它的距离就确定了。")
doc.p("为什么它的距离一定是最终的? 因为所有边的长度都 ≥ 0。任何其他路径要到达它, 都得先走出已确定区域, 而走出去的那一步就已经 ≥ 它当前的距离了, 后面只会更长。")
doc.p("\"选当前距离最小的\" 正是 heap 擅长的 (见 09)。heap 里放 <code>(距离, 节点)</code>。确定一个点 u 之后, 用它更新它的邻居: <code>dist[u] + w < dist[v]</code> 就把新的 <code>(dist[v], v)</code> 放进 heap。")
doc.p("同一个点可能被放进 heap 好几次 (距离被更新过)。取出来时如果它已经确定过了, 就跳过这个过期的记录。")
doc.h3("算法")
nc.steps(doc, "建邻接表。<code>dist = {}</code>, heap = [(0, k)]。",
         "当 heap 不空: 取出 (d, u)。u 已经在 dist 里就跳过。否则 <code>dist[u] = d</code>。",
         "对 u 的每条边 (v, w): v 不在 dist 里就 push <code>(d + w, v)</code>。",
         "dist 的个数 < n 返回 -1, 否则返回 <code>max(dist.values())</code>。")
doc.svg(F["dj_core"], "已确定区域 {1, 3}; heap 顶 (3, 2) 是最小的候选, 别的路径出了这个区域都至少是 3, 所以 dist[2] = 3 是最终值。")
doc.h3("手动走一遍")
doc.svg(F["dj_tr"], "8 行: 6 次有效取出 + 2 次过期记录被跳过; dist 最终 [0, 3, 1, 4, 7], 答案 7。")
doc.h3("复杂度")
doc.p("Time <code>O(E log V)</code>, Space <code>O(V + E)</code>。")
doc.p("变体 Cheapest Flights Within K Stops: 限制最多经过 k 站, Dijkstra 不好处理, 用 Bellman-Ford 只跑 k + 1 轮。")
nc.solution(doc, CODE["dijkstra"], CODE["flights"])
doc.note("边有长度 (非负) 的最短路: Dijkstra, heap 存 (距离, 节点), 取出时已确定的就跳过。")

# ================================================================ 识别信号
doc.h2("9. 识别信号: 看到什么, 就想到哪种图算法")
nc.table(doc, ["题目特征", "做法", "complexity"], [
    ["grid 上数连通块 / 面积 / 填充", "DFS (或 BFS), 改格子当 visited", "<code>O(m·n)</code>"],
    ["最少几步, 每步代价相同", "BFS, 层数 = 步数", "<code>O(V + E)</code>"],
    ["从多个地方同时扩散", "multi-source BFS, 所有起点一起入队", "<code>O(V + E)</code>"],
    ["状态之间可以一步转换 (单词、密码锁)", "隐式图 BFS, 需要时生成邻居", "<code>O(状态数 × 每个状态的邻居数)</code>"],
    ["依赖关系 / 先后顺序 / 有向图有没有环", "拓扑排序 (Kahn)", "<code>O(V + E)</code>"],
    ["复制带环的结构", "DFS + dict old → new, 先登记再递归", "<code>O(V + E)</code>"],
    ["动态合并、问是否同一组、数连通块", "Union-Find", "几乎 <code>O(1)</code> 每次"],
    ["边有非负长度的最短路", "Dijkstra (heap)", "<code>O(E log V)</code>"],
    ["最短路 + 限制边数 / 有负边", "Bellman-Ford", "<code>O(k·E)</code>"]])
doc.p("一句话: 先想清楚 node 是什么、边是什么。剩下的就是选遍历方式: 连通 → DFS, 最短步数 → BFS, 依赖 → 拓扑, 带权 → Dijkstra。")

doc.h2("以后再学")
doc.p("Floyd-Warshall (所有点对的最短路)、最小生成树 (Kruskal / Prim)、Tarjan (强连通分量 / 桥)、A* 搜索。")
doc.write("docs/12-graph.html")
