# 11 · Binary Tree / BST 正文 (NeetCode 式讲法)。由 11_tree.py 末尾 exec, 共用 G / build / find / CODE_* / SLUG。
import nclib as nc
from counts import cnt

EX = os.path.join(d.ROOT, "docs", "svg", SLUG, "%s_examples.svg")
N = None
LEG = [("new", "答案相关的 node"), ("rem", "出问题的 node"), ("ring", "答案")]

# ---------------------------------------------------------------- 例子图 (数字先用代码验证)
assert G["maxDepth"](build([3, 9, 20, N, N, 15, 7])) == 3 and G["maxDepth"](build([1, N, 2])) == 2
nc.tree_examples_svg(EX % "max_depth", "Maximum Depth examples", ["depth = 从 root 走到最远的叶子, 一路经过几个 node"], [
    dict(title="Example 1:  root = [3,9,20,null,null,15,7]  →  3", tree=[3, 9, 20, N, N, 15, 7], hl=[0, 2, 3], hl_edges=[2, 3],
         side_text=["最长的一条: 3 → 20 → 15", "(3 → 20 → 7 也一样长)", "→ 经过 3 个 node"]),
    dict(title="Example 2:  root = [1,null,2]  →  2", tree=[1, N, 2], hl=[0, 1], hl_edges=[1],
         side_text=["只有右孩子: 1 → 2", "→ 2"])],
    legend=[("new", "最长的路径")])

assert G["diameterOfBinaryTree"](build([1, 2, 3, 4, 5])) == 3
nc.tree_examples_svg(EX % "diameter", "Diameter examples", ["diameter = 任意两个 node 之间最长的路径, 有几条边。这条路径不一定经过 root"], [
    dict(title="Example:  root = [1,2,3,4,5]  →  3", tree=[1, 2, 3, 4, 5], hl=[3, 1, 0, 2], hl_edges=[3, 1, 2],
         side_text=["最长: 4 → 2 → 1 → 3", "(5 → 2 → 1 → 3 也一样)", "→ 3 条边"],
         extra=["路径可以\"拐弯\": 从左子树上来, 经过某个 node, 再下到右子树"])],
    legend=[("new", "最长的路径")])

assert G["maxPathSum"](build([-10, 9, 20, N, N, 15, 7])) == 42 and G["maxPathSum"](build([1, 2, 3])) == 6
nc.tree_examples_svg(EX % "max_path_sum", "Max Path Sum examples", ["path = 沿着边走的一串 node, 每个 node 最多经过一次, 可以拐弯, 不必经过 root。求 node 值之和最大的 path"], [
    dict(title="Example 1:  root = [1,2,3]  →  6", tree=[1, 2, 3], hl=[0, 1, 2], hl_edges=[1, 2], side_text=["2 → 1 → 3", "→ 2 + 1 + 3 = 6"]),
    dict(title="Example 2:  root = [-10,9,20,null,null,15,7]  →  42", tree=[-10, 9, 20, N, N, 15, 7], hl=[2, 3, 4], hl_edges=[3, 4],
         bad=[0], side_text=["15 → 20 → 7", "→ 15 + 20 + 7 = 42", "", "经过 root 反而更小:", "9 + (-10) + 20 + 15 = 34"])],
    legend=[("new", "最大的 path"), ("rem", "负数, 不值得经过")])

assert G["isValidBST"](build([2, 1, 3])) and not G["isValidBST"](build([5, 1, 4, N, N, 3, 6]))
assert not G["isValidBST"](build([5, 4, 6, N, N, 3, 7]))
nc.tree_examples_svg(EX % "validate_bst", "Validate BST examples", ["BST: 每个 node 的左子树里<所有> node 都比它小, 右子树里<所有> node 都比它大"], [
    dict(title="Example 1:  [2,1,3]  →  True", tree=[2, 1, 3], hl=[0, 1, 2], side_text=["1 < 2 < 3 ✓"]),
    dict(title="Example 2:  [5,1,4,null,null,3,6]  →  False", tree=[5, 1, 4, N, N, 3, 6], bad=[2],
         side_text=["4 在 5 的右边, 但 4 < 5 ✗"]),
    dict(title="Example 3:  [5,4,6,null,null,3,7]  →  False", tree=[5, 4, 6, N, N, 3, 7], bad=[3],
         side_text=["3 < 6, 和它的 parent 比没问题", "但 3 在 5 的右子树里, 必须 > 5 ✗", "→ 只和 parent 比是不够的"])],
    legend=[("new", "合法"), ("rem", "违反规则")])

r = build([3, 9, 20, N, N, 15, 7])
assert G["levelOrder"](r) == [[3], [9, 20], [15, 7]] and G["rightSideView"](r) == [3, 20, 7]
assert G["zigzagLevelOrder"](r) == [[3], [20, 9], [15, 7]]
nc.tree_examples_svg(EX % "level_order", "Level Order examples", ["按层输出: 第 0 层、第 1 层……每层从左到右"], [
    dict(title="Example:  root = [3,9,20,null,null,15,7]", tree=[3, 9, 20, N, N, 15, 7], ring=[0, 2, 4],
         side_text=["Level Order → [[3], [9,20], [15,7]]", "Right Side View → [3, 20, 7]", "   (每层最右边的, 橙圈)",
                    "Zigzag → [[3], [20,9], [15,7]]", "   (第 1 层反过来)"])],
    legend=[("ring", "每层最右边的 node")])

root = build([3, 5, 1, 6, 2, 0, 8, N, N, 7, 4])
assert G["lowestCommonAncestor"](root, find(root, 5), find(root, 1)).val == 3
assert G["lowestCommonAncestor"](root, find(root, 5), find(root, 4)).val == 5
nc.tree_examples_svg(EX % "lca", "LCA examples", ["LCA (最近公共祖先) = 同时是 p 和 q 的祖先的 node 里, 最深的那个。一个 node 也算自己的祖先"], [
    dict(title="Example 1:  p = 5, q = 1  →  3", tree=[3, 5, 1, 6, 2, 0, 8, N, N, 7, 4], hl=[1, 2], ring=[0], width=340,
         side_text=["5 和 1 分别在 3 的左右两边", "→ 3"]),
    dict(title="Example 2:  p = 5, q = 4  →  5", tree=[3, 5, 1, 6, 2, 0, 8, N, N, 7, 4], hl=[1, 8], ring=[1], width=340,
         side_text=["4 在 5 的子树里", "5 是自己的祖先", "→ 5"])],
    legend=[("new", "p 和 q"), ("ring", "LCA")])

assert G["kthSmallest"](build([3, 1, 4, N, 2]), 1) == 1 and G["kthSmallest"](build([5, 3, 6, 2, 4, N, N, 1]), 3) == 3
nc.tree_examples_svg(EX % "kth_smallest", "Kth Smallest examples", ["给一个 BST, 返回第 k 小的值 (k 从 1 开始)"], [
    dict(title="Example:  root = [5,3,6,2,4,null,null,1], k = 3  →  3", tree=[5, 3, 6, 2, 4, N, N, 1], ring=[1],
         side_text=["从小到大: 1, 2, 3, 4, 5, 6", "→ 第 3 个是 3"])],
    legend=[("ring", "答案")])

assert G["Codec"]().serialize(build([1, 2, 3, N, N, 4, 5])) == "1,2,#,#,3,4,#,#,5,#,#"
nc.tree_examples_svg(EX % "serialize", "Serialize examples", ["serialize: 把 tree 变成一个字符串; deserialize: 把字符串变回原来的 tree。格式自己定, 只要能还原"], [
    dict(title="Example:  root = [1,2,3,null,null,4,5]", tree=[1, 2, 3, N, N, 4, 5],
         side_text=["一种格式 (pre-order, # 表示空):", "\"1,2,#,#,3,4,#,#,5,#,#\"", "",
                    "deserialize 之后要得到", "一模一样的 tree"])],
    legend=[])

# ================================================================ HTML
doc = d.Doc("11 · Binary Tree / BST")
doc.h2("这篇讲什么")
doc.p("binary tree (二叉树) 的每个 node 最多有两个孩子: left 和 right。面试里的 tree 题, 几乎都能用 <b>recursion</b> (递归) 解决, 而且写法很固定。")
doc.p("关键的思路是: <b>不要去想整棵树。只想一个 node: 假设它的左子树、右子树的答案已经算好了, 当前这个 node 要怎么用这两个答案, 算出自己的答案?</b> 剩下的交给 recursion。")
doc.p("信息在 tree 里只有两种流向:")
nc.bullets(doc, "<b>自底向上 (post-order)</b>: 先算孩子, 孩子把结果<b>返回</b>给 parent。比如高度、子树的和。本篇大部分题是这种。",
           "<b>自顶向下 (pre-order)</b>: parent 把信息当成<b>参数</b>传给孩子。比如\"你的值必须在 (low, high) 之间\"。")
doc.svg(SLUG + "/first_principles_core.svg", "两种信息流向: 返回值往上走 (post-order), 参数往下走 (pre-order)。")
doc.p("另外一种是一层一层地处理, 用 BFS (queue), 第 5 题会讲。")
nc.table(doc, ["#", "题目", "考过的公司数", "相比上一题多了什么"], [
    ["1", "Maximum Depth of Binary Tree", cnt("Maximum Depth of Binary Tree"), "模板题: 返回值往上走"],
    ["2", "Diameter of Binary Tree", cnt("Diameter of Binary Tree"), "返回值和最终答案不一样"],
    ["3", "Binary Tree Maximum Path Sum", cnt("Binary Tree Maximum Path Sum"), "同上, 还有负数"],
    ["4", "Validate Binary Search Tree", cnt("Validate Binary Search Tree"), "换成参数往下传"],
    ["5", "Level Order / Right Side View / Zigzag", "%d / %d / %d" % (cnt("Binary Tree Level Order Traversal"), cnt("Binary Tree Right Side View"), cnt("Binary Tree Zigzag Level Order Traversal")), "一层一层处理: BFS"],
    ["6", "Lowest Common Ancestor", cnt("Lowest Common Ancestor of a Binary Tree"), "返回值的含义要自己设计"],
    ["7", "Kth Smallest Element in a BST", cnt("Kth Smallest Element in a BST"), "BST 的 inorder 是排好序的"],
    ["8", "Serialize and Deserialize", cnt("Serialize and Deserialize Binary Tree"), "把 tree 写成字符串再还原"]])
doc.p("每道题的顺序: <b>题目在问什么 → 看例子 → brute force → intuition → 算法 → 手动走一遍 → 复杂度</b>。代码放在最后, 默认折叠。")
doc.p("例子里的 <code>[3,9,20,null,null,15,7]</code> 是 LeetCode 表示 tree 的方式: 按层从左到右列出 node, null 表示这个位置没有 node。")

# ================================================================ 1
doc.h2("1. Maximum Depth of Binary Tree")
doc.h3("题目在问什么")
doc.p("给一棵 binary tree, 求它的最大深度: 从 root 走到最远的叶子, 一路上经过几个 node (包括 root 和叶子)。")
doc.h3("看例子")
doc.svg(SLUG + "/max_depth_examples.svg", "两个例子。")
doc.h3("Brute force")
doc.p("列出从 root 到每个叶子的所有路径, 取最长的。这其实已经是 <code>O(n)</code> 了 (每个 node 走一次), 但写起来要维护路径, 很麻烦。这题重点不在优化, 而在学会 recursion 的思考方式。")
doc.h3("Intuition: 只想一个 node")
doc.p("站在某个 node 上想: 如果我已经知道左子树的深度是 L, 右子树的深度是 R, 那么以我为根的这棵树, 深度是多少?")
doc.p("答案是 <code>1 + max(L, R)</code>: 我自己算 1 层, 再加上更深的那一边。")
doc.p("至于 L 和 R 怎么来的, 不用管, 它们就是对左、右孩子调用同一个函数。recursion 会负责把它们算出来。")
doc.p("最后要想清楚最简单的情况 (base case): 空树的深度是 0。")
doc.h3("算法")
nc.steps(doc, "<code>maxDepth(node)</code>: 如果 node 是 None, 返回 0。",
         "否则返回 <code>1 + max(maxDepth(node.left), maxDepth(node.right))</code>。")
doc.svg(SLUG + "/max_depth_core.svg", "假设左、右子树的深度已经是对的: 当前 node 只做 1 + max(2, 1)。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/max_depth_trace.svg", "post-order 走一遍: 叶子先返回 1, 然后 20 返回 2, root 返回 3。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>: 每个 node 访问一次。Space <code>O(h)</code>: recursion 的深度是树高 h, 最坏 (一条链) 是 <code>O(n)</code>。")
nc.solution(doc, CODE_DEPTH)
doc.note("tree recursion: 假设左右子树的答案已经算好, 只想当前 node 怎么合并。别忘了 base case (None)。")

doc.h2("把第 1 题抽象一下: tree recursion 的模板")
doc.p("每道 tree 题写之前, 先回答三个问题:")
nc.steps(doc, "<b>函数返回什么?</b> (第 1 题: 这棵子树的深度)",
         "<b>当前 node 怎么用左右孩子的返回值?</b> (第 1 题: 1 + max(L, R))",
         "<b>空 node 返回什么?</b> (第 1 题: 0)")
doc.p("如果信息是从上往下传的 (比如第 4 题的范围), 就把它写成函数的参数。")
nc.solution(doc, CODE_TEMPLATE, summary="两种模板的代码")
doc.note("写 tree recursion 前先定三件事: 返回什么、怎么合并、空 node 返回什么。")

# ================================================================ 2
doc.h2("2. Diameter of Binary Tree")
doc.h3("题目在问什么")
doc.p("diameter (直径) 是 tree 里<b>任意两个 node</b> 之间最长的路径, 用<b>边</b>的条数来算。这条路径不一定经过 root。")
doc.h3("看例子")
doc.svg(SLUG + "/diameter_examples.svg", "例子。")
doc.p("注意路径可以\"拐弯\": 从左子树往上走到某个 node, 再往下走到右子树。")
doc.h3("Brute force")
doc.p("对每个 node, 都把它当成拐弯的点: 算它左子树的深度 L 和右子树的深度 R, 经过它的最长路径是 <code>L + R</code>。取所有 node 里最大的。")
doc.p("如果每个 node 都单独调用第 1 题去算深度, 每次是 <code>O(n)</code>, 总共 <code>O(n²)</code>。浪费: 下面的 node 的深度被反复算了很多次。")
doc.h3("Intuition: 算深度的同时, 顺便更新答案")
doc.p("第 1 题的 recursion 本来就会对每个 node 算出 L 和 R。那就在算的时候, 顺便看一下 <code>L + R</code>, 更新一个全局的最大值 best。")
doc.p("这里出现了一个很重要的区别: <b>函数返回的东西 (深度), 和最终要的答案 (直径), 不是同一个东西</b>。")
nc.bullets(doc, "返回给 parent 的是深度 <code>1 + max(L, R)</code>: parent 只能接上其中<b>一边</b>, 路径不能分叉。",
           "答案是在当前 node 拐弯的路径 <code>L + R</code>: 两边都用上。它不返回, 只用来更新 best。")
doc.h3("算法")
nc.steps(doc, "<code>best = 0</code>。<code>height(node)</code>: None 返回 0。",
         "<code>L = height(left)</code>, <code>R = height(right)</code>。<code>best = max(best, L + R)</code>。",
         "返回 <code>1 + max(L, R)</code>。调用 <code>height(root)</code>, 返回 best。")
doc.svg(SLUG + "/diameter_core.svg", "brute force: 每个 node 被走过很多次 (共 19 次); 一次 post-order: 每个 node 只走 1 次 (共 7 次)。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/diameter_trace.svg", "第 5 步 node 2 把 best 更新到 4; root 的 L + R 也是 4, 没变。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(h)</code>。")
nc.solution(doc, CODE_DIAMETER)
doc.note("返回值 ≠ 答案: 返回给 parent 的只能是一边 (不能分叉); 在当前 node 拐弯的路径用两边, 用来更新全局 best。")

# ================================================================ 3
doc.h2("3. Binary Tree Maximum Path Sum")
doc.h3("题目在问什么")
doc.p("path 是沿着边走的一串 node, 每个 node 最多经过一次, 可以拐弯, 不必经过 root。求 node 值加起来最大的 path。node 的值可能是<b>负数</b>。")
doc.h3("看例子")
doc.svg(SLUG + "/max_path_sum_examples.svg", "两个例子。")
doc.h3("Brute force")
doc.p("枚举所有两个 node 之间的路径, <code>O(n²)</code> 条, 每条求和。")
doc.h3("Intuition: 和第 2 题一模一样的结构")
doc.p("还是\"返回一边, 答案用两边\":")
nc.bullets(doc, "函数返回: 从当前 node 往下走 (只走一边) 能得到的最大和, 叫 gain。",
           "答案: 在当前 node 拐弯 = <code>node.val + 左边的 gain + 右边的 gain</code>, 用来更新 best。")
doc.p("新问题是负数: 如果某一边的 gain 是负的, 接上它只会更小, 不如不接。所以用 <code>max(gain, 0)</code>, 负的就当 0 (不走那边)。")
doc.p("best 的初始值要是 <code>-∞</code>, 不能是 0: 如果所有 node 都是负数, 答案是最大的那个负数。")
doc.h3("算法")
nc.steps(doc, "<code>best = -inf</code>。<code>gain(node)</code>: None 返回 0。",
         "<code>L = max(gain(left), 0)</code>, <code>R = max(gain(right), 0)</code>。",
         "<code>best = max(best, node.val + L + R)</code>。返回 <code>node.val + max(L, R)</code>。")
doc.svg(SLUG + "/max_path_sum_core.svg", "同一个 node 20: 答案用两边 (15 + 20 + 7 = 42), 返回值只带一边 (20 + 15 = 35)。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/max_path_sum_trace.svg", "答案 42 在第 4 步的 node 20 产生; root 的返回值 25 和答案无关。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(h)</code>。")
nc.solution(doc, CODE_MAXPATH)
doc.note("path 类的 tree 题: 返回\"单边最大\", 在拐弯处用两边更新答案。负的贡献用 max(·, 0) 去掉, best 从 -inf 开始。")

# ================================================================ 4
doc.h2("4. Validate Binary Search Tree")
doc.h3("题目在问什么")
doc.p("判断一棵 binary tree 是不是 BST (binary search tree)。BST 的规则: 每个 node 的<b>左子树里所有 node</b> 都比它小, <b>右子树里所有 node</b> 都比它大。")
doc.h3("看例子")
doc.svg(SLUG + "/validate_bst_examples.svg", "三个例子。")
doc.p("Example 3 是最容易错的地方: 3 和它的 parent 6 比没问题 (3 < 6), 但 3 在 5 的右子树里, 必须大于 5。所以<b>只和 parent 比是不够的</b>。")
doc.h3("Brute force")
doc.p("对每个 node, 找出它左子树的最大值和右子树的最小值, 检查是否满足规则。每个 node 都要扫一遍子树, <code>O(n²)</code>。")
doc.h3("Intuition: 往下传一个\"合法范围\"")
doc.p("换个角度: 每个 node 的值都必须落在一个范围 <code>(low, high)</code> 里, 这个范围是由它所有的祖先决定的。")
nc.bullets(doc, "root 的范围是 <code>(-∞, +∞)</code>。",
           "往左走: 孩子必须比当前 node 小, 所以上界变成当前值: <code>(low, node.val)</code>。",
           "往右走: 孩子必须比当前 node 大, 所以下界变成当前值: <code>(node.val, high)</code>。")
doc.p("这次信息是<b>从上往下</b>流的, 所以把范围写成函数的参数 (pre-order)。和前三题的方向相反。")
doc.h3("算法")
nc.steps(doc, "<code>ok(node, low, high)</code>: None 返回 True。",
         "如果 <code>not (low < node.val < high)</code>, 返回 False。",
         "返回 <code>ok(left, low, node.val) and ok(right, node.val, high)</code>。调用 <code>ok(root, -inf, inf)</code>。")
doc.svg(SLUG + "/validate_bst_core.svg", "(low, high) 往下传: 6 的合法范围是 (3, 5), 不只是看 parent 3。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/validate_bst_trace.svg", "pre-order 走到 6 时范围是 (3, 5), 6 不在里面, 直接返回 False。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(h)</code>。另一种做法: BST 的 inorder 一定是严格递增的 (见第 7 题), 检查 inorder 是否递增也可以。")
nc.solution(doc, CODE_VALIDATE)
doc.note("约束来自所有祖先, 而不只是 parent: 把约束写成参数, 从上往下传。")

# ================================================================ 5
doc.h2("5. Binary Tree Level Order Traversal (+ Right Side View, Zigzag)")
doc.h3("题目在问什么")
doc.p("<b>Level Order</b>: 按层输出 node 的值, 每层从左到右, 返回一个 list of list。")
doc.p("两个常见变体: <b>Right Side View</b> (从右边看过去, 每层只能看到最右边的那个); <b>Zigzag</b> (第一层从左到右, 第二层从右到左, 交替)。")
doc.h3("看例子")
doc.svg(SLUG + "/level_order_examples.svg", "同一棵树的三种输出。")
doc.h3("Brute force")
doc.p("用 recursion 记录每个 node 的深度, 按深度分组。可以做, 但\"一层一层\"本身就是 BFS 的天然顺序, 用 queue 更直接。")
doc.h3("Intuition: BFS, 每一轮处理一整层")
doc.p("BFS (breadth-first search, 广度优先) 用一个 queue: 先放进 root; 每次从队头取一个 node, 把它的孩子放到队尾。这样 node 出队的顺序就是一层一层、从左到右的。")
doc.p("但我们还需要知道\"一层在哪里结束\"。技巧是: 每一轮开始时, 先记下 <code>len(q)</code>, 它正好是这一层的 node 数。然后只 pop 这么多个, 这一轮 pop 出来的就是完整的一层。这一轮里新加进去的孩子, 留给下一轮。")
doc.p("有了\"一层\"之后, 两个变体都很简单: Right Side View 只取每层的最后一个; Zigzag 把奇数层反过来。")
doc.h3("算法")
nc.steps(doc, "<code>q = deque([root])</code>。",
         "当 q 不空: <code>size = len(q)</code>, <code>level = []</code>。循环 size 次: popleft 一个 node, 值放进 level, 把它的孩子 append 到 q。",
         "把 level 放进结果。")
doc.svg(SLUG + "/level_order_core.svg", "len(q) 在每一轮开始时算一次: pop 出 2 个 = 这一层, 新 push 的 4、5 留给下一轮。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/level_order_trace.svg", "每一行是一层: 同时给出 level order、right side view、zigzag 三种输出。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(w)</code>, w 是最宽那一层的 node 数。")
nc.solution(doc, CODE_LEVEL)
doc.note("按层处理: BFS + 每轮先记 len(q)。右视图取每层最后一个, zigzag 把奇数层反转。")

# ================================================================ 6
doc.h2("6. Lowest Common Ancestor of a Binary Tree")
doc.h3("题目在问什么")
doc.p("给一棵 binary tree (不是 BST) 和其中两个 node p、q。找它们的 LCA (lowest common ancestor, 最近公共祖先): 同时是 p 和 q 的祖先的 node 里, 最深的那个。一个 node 也算是它自己的祖先。")
doc.h3("看例子")
doc.svg(SLUG + "/lca_examples.svg", "同一棵树的两个例子。")
doc.p("Example 2 里 q = 4 在 p = 5 的子树里, 所以 LCA 就是 p 自己。")
doc.h3("Brute force")
doc.p("分别找出从 root 到 p 和到 q 的路径 (两次 DFS), 然后比较两条路径, 最后一个相同的 node 就是 LCA。<code>O(n)</code> 时间, 但要存两条路径。")
doc.h3("Intuition: 让每个子树报告\"我这里有没有 p 或 q\"")
doc.p("设计函数的返回值: <code>lca(node)</code> 在 node 这棵子树里找 p 和 q, 返回:")
nc.bullets(doc, "如果 node 本身就是 p 或 q, 返回 node。",
           "否则看左右孩子的返回值。<b>两边都不是 None</b>: p 和 q 分别在左右两边, 当前 node 就是 LCA, 返回 node。",
           "<b>只有一边不是 None</b>: 把那一边的结果原样往上传。",
           "两边都是 None: 返回 None。")
doc.p("返回值的意思是\"这棵子树里找到的 p、q 或者 LCA\"。第一次出现\"两边都不是 None\"的那个 node, 就是 LCA, 之后它会被一路原样传到 root。")
doc.h3("算法")
nc.steps(doc, "node 是 None、p 或 q: 返回 node。",
         "<code>L = lca(left)</code>, <code>R = lca(right)</code>。",
         "L 和 R 都有: 返回 node。否则返回 <code>L or R</code>。")
doc.svg(SLUG + "/lca_core.svg", "三种合并情况: 分在两边 / 只在一边 / node 自己就是 p 或 q。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/lca_trace.svg", "第 3 步 node 5 第一次左右都不是 None, 它就是 LCA; 之后只是被原样往上传。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(h)</code>。如果是 BST, 可以直接比大小: p、q 都比当前小就往左, 都大就往右, 否则当前就是 LCA, <code>O(h)</code>。")
nc.solution(doc, CODE_LCA)
doc.note("返回值的含义可以自己设计。LCA: 子树里找到了 p / q 就返回它; 左右都找到了, 当前 node 就是答案。")

# ================================================================ 7
doc.h2("7. Kth Smallest Element in a BST")
doc.h3("题目在问什么")
doc.p("给一棵 BST 和整数 k, 返回第 k 小的值 (k 从 1 开始)。")
doc.h3("看例子")
doc.svg(SLUG + "/kth_smallest_examples.svg", "例子。")
doc.h3("Brute force")
doc.p("遍历所有 node, 收集值, 排序, 取第 k 个。<code>O(n log n)</code>。浪费: BST 本身已经包含了大小顺序。")
doc.h3("Intuition: BST 的 inorder 就是从小到大")
doc.p("inorder (中序) 遍历的顺序是: 先左子树, 再当前 node, 再右子树。")
doc.p("在 BST 里, 左子树都比当前小, 右子树都比当前大。所以 inorder 访问的顺序<b>正好是从小到大</b>。第 k 个访问到的就是答案, 访问到就可以停, 不用遍历完。")
doc.p("用 stack 写 iterative 的 inorder, 方便在第 k 个时停下: 一路往左走, 把经过的 node 都 push; 走到底就 pop 一个 (这就是下一个最小的), 然后转去它的右子树。")
doc.h3("算法")
nc.steps(doc, "<code>stack = []</code>, <code>cur = root</code>。",
         "当 cur 或 stack 不空: 一路往左, 把 cur push 进 stack, <code>cur = cur.left</code>。",
         "pop 出一个 node, k 减 1; k 变成 0 就返回 node.val。否则 <code>cur = node.right</code>。")
doc.svg(SLUG + "/kth_smallest_core.svg", "虚线把 tree 上的 node 对应到 inorder 序列: 左子树全部在 5 的左边, 右子树在右边。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/kth_smallest_trace.svg", "stack 里存\"往左走的路上还没处理的祖先\"; 第 3 次 pop 出来的 3 就是答案。")
doc.h3("复杂度")
doc.p("Time <code>O(h + k)</code>: 先往左走到底 h 步, 再 pop k 次。Space <code>O(h)</code>。")
nc.solution(doc, CODE_KTH)
doc.note("BST + 第 k 小 / 有序 / 检查合法: 用 inorder, 它就是从小到大的顺序。")

# ================================================================ 8
doc.h2("8. Serialize and Deserialize Binary Tree")
doc.h3("题目在问什么")
doc.p("设计两个函数: <code>serialize</code> 把一棵 tree 变成一个字符串, <code>deserialize</code> 把这个字符串变回<b>一模一样</b>的 tree。字符串的格式由你自己决定。")
doc.h3("看例子")
doc.svg(SLUG + "/serialize_examples.svg", "例子。")
doc.h3("Brute force")
doc.p("只记录值的遍历顺序 (比如只有 pre-order) 是不够的: 不同形状的 tree 可能得到同样的序列, 没法还原。比如 [1,2] (2 是左孩子) 和 [1,null,2] (2 是右孩子) 的 pre-order 都是 1, 2。")
doc.h3("Intuition: pre-order, 并且把空的位置也写出来")
doc.p("问题出在不知道哪里是空的。只要把空 node 也写下来 (用 <code>#</code>), 序列就唯一确定了 tree 的形状。")
doc.p("用 pre-order 写: 先写当前 node, 再写整个左子树, 再写整个右子树。空 node 写 #。")
doc.p("还原的时候按同样的顺序读: 读到一个值, 就新建 node; 然后<b>递归地</b>读出它的左子树 (左子树的 token 正好接在后面), 再读出右子树。读到 # 就返回 None。")
doc.h3("算法")
nc.steps(doc, "serialize(node): None 写 #; 否则写 node.val, 再 serialize(left), serialize(right)。用逗号连起来。",
         "deserialize: 把字符串切成 token, 用一个 iterator 一个一个读。<code>build()</code>: 读一个 token, 是 # 返回 None; 否则新建 node, <code>node.left = build()</code>, <code>node.right = build()</code>。")
doc.svg(SLUG + "/serialize_core.svg", "token 序列就是 recursion 结构拍平: root 1 + 左子树 (2 # #) + 右子树 (3 4 # # 5 # #)。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/serialize_trace.svg", "serialize 的 5 步: 绿色 token 是每一步新写的; 一个叶子一步写 3 个 token (值 + 两个 #)。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(n)</code>。也可以用 BFS (level order) 写, 就是 LeetCode 自己用的格式。")
nc.solution(doc, CODE_CODEC)
doc.note("要能唯一还原 tree: 遍历时把空 node 也记下来。pre-order + # 最好写, 还原时按同样的 recursion 顺序读。")

# ================================================================ 识别信号
doc.h2("9. 识别信号: 看到什么, 就想到什么写法")
nc.table(doc, ["题目特征", "做法", "complexity"], [
    ["高度、节点数、子树和、是否平衡", "post-order, 返回值往上", "<code>O(n)</code>"],
    ["路径可以拐弯 (直径、最大路径和)", "返回单边, 在拐弯处用两边更新全局 best", "<code>O(n²)</code> → <code>O(n)</code>"],
    ["约束来自祖先 (BST 合法范围、从 root 来的路径和)", "pre-order, 参数往下传", "<code>O(n²)</code> → <code>O(n)</code>"],
    ["按层输出、每层最右、最小深度", "BFS + 每轮记 len(q)", "<code>O(n)</code>"],
    ["两个 node 的最近公共祖先", "返回\"子树里找到的 p / q\", 两边都有就是答案", "<code>O(n)</code>"],
    ["BST + 有序 / 第 k 小 / 检查合法", "inorder = 从小到大", "<code>O(n log n)</code> → <code>O(h + k)</code>"],
    ["tree 变字符串再还原", "pre-order + 空标记", "<code>O(n)</code>"]])
doc.p("一句话: 先想清楚信息往哪个方向流。往上 → 返回值; 往下 → 参数; 一层一层 → BFS。")

doc.h2("以后再学")
doc.p("Construct Binary Tree from Preorder and Inorder、Path Sum III (从上往下的 prefix sum + Hash Table)、Morris traversal (O(1) 空间的 inorder)。")
doc.write("docs/11-tree.html")
