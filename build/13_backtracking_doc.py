# 13 · Backtracking 正文 (NeetCode 式讲法)。由 13_backtracking.py 的 build_doc() exec, 共用 SRC / NS / rec_nqueens。
import nclib as nc
from counts import cnt

SL = "13-backtracking"
EX = os.path.join(d.ROOT, "docs", "svg", SL, "%s_examples.svg")
EXS = SL + "/%s_examples.svg"
nq8 = rec_nqueens(8)[0]
nq8_nodes = nq8.npush + 1

# ---------------------------------------------------------------- 例子图
assert sorted(map(sorted, NS["subsets_start"]([1, 2, 3]))) == sorted(map(sorted, [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]))
nc.examples_svg(EX % "subsets", "Subsets examples", ["数组里的数互不相同。返回所有子集 (包括空集和它自己), 顺序随意"], [
    dict(title="Example:  nums = [1,2,3]  →  8 个子集", index=False, rows=[
        ("0 个", ["[]"], ["new"]), ("1 个", ["[1]", "[2]", "[3]"], ["new"] * 3),
        ("2 个", ["[1,2]", "[1,3]", "[2,3]"], ["new"] * 3), ("3 个", ["[1,2,3]"], ["new"])], cw=70,
         extra=["每个数选或不选, 2 × 2 × 2 = 8 种。[2,1] 和 [1,2] 是同一个子集, 只算一次"])],
    legend=[])

assert len(NS["permute"]([1, 2, 3])) == 6
nc.examples_svg(EX % "permutations", "Permutations examples", ["数组里的数互不相同。返回所有排列 (每个数都用一次, 顺序不同就算不同)"], [
    dict(title="Example:  nums = [1,2,3]  →  6 个排列", items=["[1,2,3]", "[1,3,2]", "[2,1,3]", "[2,3,1]", "[3,1,2]", "[3,2,1]"],
         cw=76, index=False, extra=["第一个位置 3 种选法, 第二个 2 种, 第三个 1 种: 3 × 2 × 1 = 6。和子集不同, [1,2] 和 [2,1] 是两个排列"])],
    legend=[])

assert sorted(map(sorted, NS["combination_sum"]([2, 3, 6, 7], 7))) == [[2, 2, 3], [7]]
nc.examples_svg(EX % "combination_sum", "Combination Sum examples",
                ["candidates 互不相同。选一些数 (<同一个数可以选很多次>) 让和等于 target。返回所有不同的组合"], [
    dict(title="Example:  candidates = [2,3,6,7], target = 7  →  [[2,2,3],[7]]", index=False,
         rows=[("组合 1", [2, 2, 3], ["new"] * 3), ("组合 2", [7], ["new"])],
         extra=["2 用了两次。[2,3,2] 和 [2,2,3] 是同一个组合, 不能重复输出"])],
    legend=[])

f2 = NS.get("combination_sum2") or NS.get("combinationSum2")
if f2:
    assert sorted(map(sorted, f2([10, 1, 2, 7, 6, 1, 5], 8))) == sorted(map(sorted, [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]))
nc.examples_svg(EX % "combination_sum_ii", "Combination Sum II examples",
                ["candidates 里<可能有重复的数>。每个位置的数最多用一次。和等于 target 的所有不同组合"], [
    dict(title="Example:  candidates = [10,1,2,7,6,1,5], target = 8", index=False,
         rows=[("答案", ["[1,1,6]", "[1,2,5]", "[1,7]", "[2,6]"], ["new"] * 4)], cw=76,
         extra=["有两个 1。[1,7] 用第一个 1 或第二个 1 都能得到, 但只能输出一次",
                "[1,1,6] 是可以的: 两个 1 是不同位置的数, 各用一次"])],
    legend=[])

assert sorted(NS["generate_parenthesis"](3)) == sorted(["((()))", "(()())", "(())()", "()(())", "()()()"])
nc.examples_svg(EX % "generate_parentheses", "Generate Parentheses examples", ["给 n, 生成所有由 n 对括号组成的、合法的括号字符串"], [
    dict(title="Example:  n = 3  →  5 个", items=["((()))", "(()())", "(())()", "()(())", "()()()"], cw=80, index=False,
         extra=["合法: 从左往右读, 任何时候 ) 的个数都不超过 (; 最后两者相等", "\"())(()\" 不合法: 读到第 3 个字符时 ) 比 ( 多了"])],
    legend=[])

assert sorted(NS["letter_combinations"]("23")) == sorted(["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"])
nc.examples_svg(EX % "letter_combinations", "Letter Combinations examples",
                ["手机键盘上 2 对应 abc, 3 对应 def, ... 9 对应 wxyz。给一串数字, 返回所有可能的字母组合"], [
    dict(title="Example:  digits = \"23\"  →  9 个", index=False, rows=[
        ("2 → abc", ["a", "b", "c"], None), ("3 → def", ["d", "e", "f"], None),
        ("答案", ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"], ["new"] * 9)], cw=44,
         extra=["第一位从 abc 里选一个, 第二位从 def 里选一个: 3 × 3 = 9"])],
    legend=[])

b = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
assert NS["exist"]([r[:] for r in b], "ABCCED") and not NS["exist"]([r[:] for r in b], "ABCB")
nc.examples_svg(EX % "word_search", "Word Search examples",
                ["grid 里每个格子一个字母。能不能从某个格子出发, 每步走到上下左右相邻的格子, 拼出 word? 同一个格子不能用两次"], [
    dict(title="Example 1:  word = \"ABCCED\"  →  True", index=False, rows=[
        ("row 0", ["A", "B", "C", "E"], ["new", "new", "new", "keep"]),
        ("row 1", ["S", "F", "C", "S"], ["keep", "keep", "new", "keep"]),
        ("row 2", ["A", "D", "E", "E"], ["keep", "new", "new", "keep"])],
         extra=["A(0,0) → B(0,1) → C(0,2) → C(1,2) → E(2,2) → D(2,1)"]),
    dict(title="Example 2:  word = \"ABCB\"  →  False", extra=["A → B → C 之后, 下一个 B 只能是刚用过的 (0,1), 不允许重复使用"])],
    legend=[("new", "路径")])

assert len(NS["solve_n_queens"](4)) == 2
nc.examples_svg(EX % "n_queens", "N-Queens examples", ["在 n × n 的棋盘上放 n 个皇后, 让它们互相攻击不到 (同一行、同一列、同一条斜线都不能有两个)。返回所有放法"], [
    dict(title="Example:  n = 4  →  2 种放法 (下面是其中一种)", index=False, rows=[
        ("row 0", [".", "Q", ".", "."], ["keep", "new", "keep", "keep"]), ("row 1", [".", ".", ".", "Q"], ["keep", "keep", "keep", "new"]),
        ("row 2", ["Q", ".", ".", "."], ["new", "keep", "keep", "keep"]), ("row 3", [".", ".", "Q", "."], ["keep", "keep", "new", "keep"])],
         extra=["每行、每列、每条斜线都只有一个 Q。另一种放法是它的左右镜像"])],
    legend=[("new", "皇后")])

# ================================================================ HTML
doc = d.Doc("13 · Backtracking")
doc.h2("这篇讲什么")
doc.p("有一类题要你<b>列出所有的可能</b>: 所有子集、所有排列、所有和为 target 的组合、所有合法的括号、所有棋盘放法……答案本身就有指数多个, 所以没有\"更快\"的算法, 只能一个一个生成出来。")
doc.p("问题是怎么<b>系统地</b>生成, 不重复、不遗漏, 而且尽早放弃没有希望的方向。这就是 <b>backtracking</b> (回溯)。")
doc.p("想象你在走一个迷宫, 每到一个岔路口就选一条路走下去; 走不通 (或者到了终点) 就<b>退回</b>上一个岔路口, 换另一条路。所有的选择画出来是一棵树, 叫 decision tree。backtracking 就是在这棵树上做 DFS。")
doc.p("每道 backtracking 题都只要想清楚三件事:")
nc.bullets(doc, "<b>path</b>: 目前已经做了哪些选择。",
           "<b>choices</b>: 下一步还能选什么。",
           "<b>结束条件</b>: 什么时候 path 是一个完整的答案。")
doc.p("写法也固定: <b>做选择 (push) → 递归 → 撤销选择 (pop)</b>。")
nc.table(doc, ["#", "题目", "考过的公司数", "相比上一题多了什么"], [
    ["1", "Subsets", cnt("Subsets"), "模板题: 每个节点都是答案"],
    ["2", "Permutations", cnt("Permutations"), "顺序有关: 每层都从头选, 跳过用过的"],
    ["3", "Combination Sum", cnt("Combination Sum"), "同一个数可以重复选"],
    ["4", "Combination Sum II", cnt("Combination Sum II"), "输入有重复: 同一层去重"],
    ["5", "Generate Parentheses", cnt("Generate Parentheses"), "用约束剪枝, 只走合法的分支"],
    ["6", "Letter Combinations of a Phone Number", cnt("Letter Combinations of a Phone Number"), "每一层的选项不一样"],
    ["7", "Word Search", cnt("Word Search"), "在 grid 上回溯, 标记后要恢复"],
    ["8", "N-Queens", cnt("N-Queens"), "多个约束, 用几个 set 检查"]])
doc.p("每道题的顺序: <b>题目在问什么 → 看例子 → brute force → intuition → 算法 → 手动走一遍 → 复杂度</b>。代码放在最后, 默认折叠。")

# ================================================================ 1
doc.h2("1. Subsets")
doc.h3("题目在问什么")
doc.p("给一个数组, 里面的数互不相同。返回它<b>所有的子集</b> (包括空集和整个数组), 顺序随意, 但不能有重复的子集。")
doc.h3("看例子")
doc.svg(EXS % "subsets", "例子。")
doc.h3("Brute force")
doc.p("如果数组长度固定是 3, 可以写三层循环 (每层决定一个数选不选)。但长度是变量, 循环的层数写不死。")
doc.p("另一种想法是先生成所有\"可能的\"序列, 再去重。比如把每个排列都生成一遍再转成 set, 会生成大量重复, 很浪费。")
doc.h3("Intuition: 用 recursion 代替\"写不死的循环\"")
doc.p("recursion 的每一层就相当于一层循环, 层数可以是任意的。画出所有选择:")
doc.svg(SL + "/first_principles_core.svg", "左: brute force 的问题 (循环层数写不死 / 先生成再检查)。右: decision tree, 每个节点是一个 path, 每条边是一次选择。")
doc.p("为了不重复 (不让 [1,2] 和 [2,1] 都出现), 规定<b>只能往后选</b>: 选了第 i 个数之后, 下一个只能从 i+1 往后选。这样每个子集只会按\"下标从小到大\"的顺序被生成一次。")
doc.p("这棵树上的<b>每个节点</b>都是一个合法的子集 (不只是叶子), 所以每进入一个节点就把 path 记下来。")
doc.p("记下来的时候要 <code>path[:]</code> 复制一份: path 是同一个 list, 后面还会被修改; 不复制的话, 最后答案里全是同一个 (空的) list。")
doc.h3("算法")
nc.steps(doc, "<code>dfs(start)</code>: 先把 <code>path[:]</code> 加入答案。",
         "对 i 从 start 到 n-1: <code>path.append(nums[i])</code>, <code>dfs(i + 1)</code>, <code>path.pop()</code>。",
         "调用 <code>dfs(0)</code>。")
doc.svg(SL + "/subsets_core.svg", "start index 保证只往后选, 所以每个子集只出现一次。")
doc.h3("手动走一遍")
doc.svg(SL + "/subsets_trace.svg", "path 的 push / pop 随时间变化, 每一步都把当前 path 记进答案。")
doc.h3("复杂度")
doc.p("Time <code>O(n · 2ⁿ)</code>: 2ⁿ 个子集, 每个复制 <code>O(n)</code>。Space <code>O(n)</code> (recursion 深度, 不算输出)。")
doc.p("另一种写法: 每个数\"选或不选\", recursion 到第 n 层时记录。两种都对。")
nc.solution(doc, SRC["subsets"], SRC["subsets2"])
doc.note("列出所有子集 / 组合: start index 只往后选防重复; 每个节点都记录 path[:]。")

doc.h2("把第 1 题抽象一下: backtracking 模板")
doc.p("所有 backtracking 题都是这个形状, 只换三样东西: path 里放什么、choices 是什么、什么时候记录答案。")
doc.p("为什么一定要 pop (撤销选择)? 因为整个过程只用一个 path list。从一个分支退回来, 必须把这个分支加进去的东西拿掉, 才能去试下一个分支。")
doc.p("复杂度基本等于 decision tree 的节点数。所以优化的方向只有一个: <b>剪枝</b>, 尽早发现某个分支不可能有答案, 不往下走 (第 3、5、8 题)。")
nc.solution(doc, SRC["template"], summary="通用模板代码")
doc.note("backtracking = decision tree 上的 DFS。做选择 → 递归 → 撤销选择。记录答案时复制 path。")

# ================================================================ 2
doc.h2("2. Permutations")
doc.h3("题目在问什么")
doc.p("给一个数组, 里面的数互不相同。返回<b>所有的排列</b>: 每个数恰好用一次, 顺序不同就算不同的排列。")
doc.h3("看例子")
doc.svg(EXS % "permutations", "例子。")
doc.h3("Brute force")
doc.p("同样是循环层数写不死的问题。")
doc.h3("Intuition: 每一层都从头选, 跳过已经用过的")
doc.p("和 Subsets 的区别: 排列和顺序有关, [1,2] 和 [2,1] 是两个答案。所以不能再用 start index 规定\"只往后选\", <b>每一层都要从头看所有数</b>。")
doc.p("但同一个数不能用两次。用一个 <code>used</code> 数组记录哪些数已经在 path 里了, 选的时候跳过它们。")
doc.p("答案只在叶子上: path 的长度等于 n 时才是一个完整的排列。")
doc.h3("算法")
nc.steps(doc, "<code>dfs()</code>: 如果 <code>len(path) == n</code>, 记录 <code>path[:]</code>, 返回。",
         "对每个 i: 如果 used[i], 跳过。否则 <code>used[i] = True</code>, push, dfs(), pop, <code>used[i] = False</code>。")
doc.svg(SL + "/permutations_core.svg", "每一层都从头看所有数, 用 used 跳过已选的。")
doc.h3("手动走一遍")
doc.svg(SL + "/permutations_trace.svg", "path 和 used 随时间的变化; path 满了才记录。")
doc.h3("复杂度")
doc.p("Time <code>O(n · n!)</code>, Space <code>O(n)</code>。")
nc.solution(doc, SRC["permute"])
doc.note("排列: 每层从头选, used 跳过已选的; 长度满了才记录。")

# ================================================================ 3
doc.h2("3. Combination Sum")
doc.h3("题目在问什么")
doc.p("给一个数组 candidates (互不相同) 和 target。从中选一些数, 让它们的和等于 target。<b>同一个数可以选任意多次</b>。返回所有不同的组合 (组合不看顺序)。")
doc.h3("看例子")
doc.svg(EXS % "combination_sum", "例子。")
doc.h3("Brute force")
doc.p("生成所有可能的多重集合, 检查和。不知道每个数要选几次, 没法列举。")
doc.h3("Intuition: 和 Subsets 一样, 只改一个下标")
doc.p("组合不看顺序, 所以和 Subsets 一样用 start index 防止重复。")
doc.p("区别在于同一个数可以重复选: 选了 <code>candidates[i]</code> 之后, 下一层<b>仍然可以从 i 开始选</b> (而不是 i+1)。所以递归时传 i。")
doc.p("用 remain 记录还差多少。<code>remain == 0</code> 就找到一个答案; <code>remain < 0</code> 就没希望了, 直接返回。")
doc.p("剪枝: 先把 candidates 排序。如果当前的 <code>candidates[i] > remain</code>, 它后面的更大, 都不用试了, 直接 break。")
doc.h3("算法")
nc.steps(doc, "排序。<code>dfs(start, remain)</code>: remain == 0 就记录。",
         "对 i 从 start 开始: <code>candidates[i] > remain</code> 就 break。否则 push, <code>dfs(i, remain - candidates[i])</code>, pop。")
doc.svg(SL + "/combination_sum_core.svg", "递归传 i 而不是 i+1: 同一个数可以再选; 排序后超过 remain 的直接剪掉。")
doc.h3("手动走一遍")
doc.svg(SL + "/combination_sum_trace.svg", "path 和 remain 的变化; 被剪掉的分支标红。")
doc.h3("复杂度")
doc.p("Time 是 decision tree 的大小, 上界大约 <code>O(n^(target / min))</code>。Space <code>O(target / min)</code>。")
nc.solution(doc, SRC["comb"])
doc.note("可以重复选: 递归传 i; 不能重复选: 传 i + 1。排序后可以用 break 剪枝。")

# ================================================================ 4
doc.h2("4. Combination Sum II")
doc.h3("题目在问什么")
doc.p("和第 3 题类似, 但有两个不同: candidates 里<b>可能有重复的数</b>; 每个位置上的数<b>最多用一次</b>。返回所有不同的组合。")
doc.h3("看例子")
doc.svg(EXS % "combination_sum_ii", "例子。")
doc.p("难点: 数组里有两个 1, 用第一个 1 和用第二个 1 得到的组合是一样的, 只能输出一次。")
doc.h3("Brute force")
doc.p("像 Subsets 那样生成所有组合, 再用 set 去重。会生成很多重复的分支, 浪费时间。")
doc.h3("Intuition: 同一层不选两次同样的值")
doc.p("先排序, 让相同的数挨在一起。")
doc.p("重复是怎么产生的? 在 decision tree 的<b>同一层</b> (同一个位置上), 先选了第一个 1, 后来又选了第二个 1, 这两个分支下面长出来的东西完全一样。")
doc.p("所以规则是: <b>同一层里, 如果当前的数和前一个数相同, 就跳过</b>。写成代码就是 <code>if i > start and nums[i] == nums[i-1]: continue</code>。")
doc.p("注意是 <code>i > start</code>, 不是 <code>i > 0</code>: 不同层选同样的值是可以的, 比如 [1,1,6] 里两个 1 在不同的层。")
doc.p("每个数只能用一次, 所以递归传 i + 1。")
doc.h3("算法")
nc.steps(doc, "排序。<code>dfs(start, remain)</code>: remain == 0 就记录。",
         "对 i 从 start 开始: <code>i > start and nums[i] == nums[i-1]</code> 就 continue; <code>nums[i] > remain</code> 就 break。",
         "push, <code>dfs(i + 1, remain - nums[i])</code>, pop。")
doc.svg(SL + "/combination_sum_ii_core.svg", "同一层里第二个 1 被跳过 (它会长出和第一个 1 一样的子树); 不同层可以重复用值。")
doc.h3("手动走一遍")
doc.svg(SL + "/combination_sum_ii_trace.svg", "同层去重的过程。")
doc.h3("复杂度")
doc.p("Time <code>O(2ⁿ · n)</code> 上界, Space <code>O(n)</code>。Subsets II、Permutations II 都用同样的去重方法。")
nc.solution(doc, SRC["comb2"])
doc.note("输入有重复、输出要去重: 先排序, 同一层 if i > start and nums[i] == nums[i-1]: continue。")

# ================================================================ 5
doc.h2("5. Generate Parentheses")
doc.h3("题目在问什么")
doc.p("给 n, 生成所有由 n 对括号组成的<b>合法</b>括号字符串。合法: 每个 ( 都有对应的 ), 而且从左往右读的时候, 任何时刻 ) 的个数都不超过 (。")
doc.h3("看例子")
doc.svg(EXS % "generate_parentheses", "例子。")
doc.h3("Brute force")
doc.p("生成所有长度 2n 的 ( 和 ) 组成的字符串 (<code>2^(2n)</code> 个), 再一个一个检查是否合法。n = 3 时要生成 64 个, 只有 5 个合法。")
doc.h3("Intuition: 只往合法的方向走 (剪枝)")
doc.p("与其先生成再检查, 不如在生成的过程中就保证合法。每一步只有两种选择: 加 ( 或者加 )。")
nc.bullets(doc, "加 ( 的条件: 已经用的 ( 少于 n 个 (<code>open < n</code>)。",
           "加 ) 的条件: 已经用的 ) 少于 ( (<code>close < open</code>)。否则 ) 会比 ( 多, 一定不合法。")
doc.p("满足这两个条件, 生成出来的每个字符串都是合法的, 不需要再检查。这就是<b>剪枝</b>: 在走进一个分支之前就判断它有没有希望。")
doc.h3("算法")
nc.steps(doc, "<code>dfs(open, close)</code>: 长度到 2n, 记录。",
         "<code>open < n</code>: 加 (, dfs(open + 1, close), 撤销。",
         "<code>close < open</code>: 加 ), dfs(open, close + 1), 撤销。")
doc.svg(SL + "/generate_parentheses_core.svg", "两个条件把不合法的分支在生成之前就剪掉了。")
doc.h3("手动走一遍")
doc.svg(SL + "/generate_parentheses_trace.svg", "path 的变化; 被剪掉的分支标红并写了原因。")
doc.h3("复杂度")
doc.p("Time 和答案个数成正比 (Catalan 数, 大约 <code>4ⁿ / n^1.5</code>)。Space <code>O(n)</code>。")
nc.solution(doc, SRC["parens"])
doc.note("有约束的生成: 在 push 之前就检查约束, 只走合法的分支, 不要先生成再过滤。")

# ================================================================ 6
doc.h2("6. Letter Combinations of a Phone Number")
doc.h3("题目在问什么")
doc.p("手机键盘上, 2 对应 abc, 3 对应 def, ……, 9 对应 wxyz。给一串数字 (2–9), 返回它能表示的所有字母组合。")
doc.h3("看例子")
doc.svg(EXS % "letter_combinations", "例子。")
doc.h3("Brute force")
doc.p("每一位一层循环, 但位数不固定, 循环层数写不死。")
doc.h3("Intuition: 第 i 层的选项由第 i 个数字决定")
doc.p("这是最直接的 backtracking: decision tree 的第 i 层, 选项就是第 i 个数字对应的那几个字母。path 长度等于数字个数时, 就是一个答案。")
doc.p("和前面的题不同, 这里没有 start index, 也没有 used: 每一层的选项本来就不同, 不会重复。也不需要剪枝, 所有组合都是答案。")
doc.h3("算法")
nc.steps(doc, "<code>dfs(idx)</code>: idx == len(digits), 记录 path。",
         "对 <code>phone[digits[idx]]</code> 里的每个字母: push, dfs(idx + 1), pop。")
doc.svg(SL + "/letter_combinations_core.svg", "每一层的选项由当前的数字决定。")
doc.h3("手动走一遍")
doc.svg(SL + "/letter_combinations_trace.svg", "path 的变化。")
doc.h3("复杂度")
doc.p("Time <code>O(4ⁿ · n)</code>, Space <code>O(n)</code>。")
nc.solution(doc, SRC["letters"])
doc.note("每一层的选项不一样: 第 idx 层就从第 idx 组里选。")

# ================================================================ 7
doc.h2("7. Word Search")
doc.h3("题目在问什么")
doc.p("一个字母 grid 和一个单词 word。能不能从某个格子出发, 每一步走到上下左右相邻的格子, 依次拼出 word? <b>同一个格子在一条路径里只能用一次</b>。")
doc.h3("看例子")
doc.svg(EXS % "word_search", "两个例子。")
doc.h3("Brute force")
doc.p("从每个格子出发, 枚举所有可能的路径。不剪枝的话路径数量是指数级的。")
doc.h3("Intuition: grid 上的 backtracking")
doc.p("从每个格子出发试一次。每一步: 当前格子的字母必须等于 <code>word[i]</code>, 否则这条路不通, 立即返回 (这就是剪枝)。")
doc.p("相等的话, 往四个方向找 <code>word[i+1]</code>。")
doc.p("\"同一个格子不能用两次\": 走进一个格子时, 把它临时改成 <code>'#'</code>, 这样后面的路径不会再走进来。<b>退回时一定要恢复原来的字母</b>, 因为别的路径 (从别的方向来的) 可能还要用它。这就是 backtracking 的\"撤销选择\"。")
doc.p("和 12 里的 Number of Islands 对比: 那题淹掉之后不恢复, 因为每个格子只需要访问一次; 这题要恢复, 因为同一个格子可以出现在不同的路径里。")
doc.h3("算法")
nc.steps(doc, "<code>dfs(r, c, i)</code>: i == len(word) 返回 True。越界或者 <code>board[r][c] != word[i]</code>, 返回 False。",
         "<code>tmp = board[r][c]</code>, <code>board[r][c] = '#'</code>。",
         "四个方向有一个 <code>dfs(..., i + 1)</code> 返回 True, 结果就是 True。",
         "<code>board[r][c] = tmp</code> (恢复), 返回结果。对每个格子调用 dfs(r, c, 0)。")
doc.svg(SL + "/word_search_core.svg", "走进去时标 #, 退出来时恢复。")
doc.h3("手动走一遍")
doc.svg(SL + "/word_search_trace.svg", "path 和 board 的变化, 每一步都画出来了。")
doc.h3("复杂度")
doc.p("Time <code>O(m·n · 3^L)</code>, L 是单词长度 (除了第一步, 每步最多 3 个方向, 不能走回头)。Space <code>O(L)</code>。")
nc.solution(doc, SRC["wsearch"])
doc.note("grid 上的路径搜索、格子不能重复用: 进去时标记, 出来时恢复。")

# ================================================================ 8
doc.h2("8. N-Queens")
doc.h3("题目在问什么")
doc.p("在 n × n 的棋盘上放 n 个皇后, 让它们互相攻击不到。皇后能攻击同一行、同一列、同一条斜线 (两个方向) 上的任何棋子。返回所有的放法。")
doc.h3("看例子")
doc.svg(EXS % "n_queens", "例子。")
doc.h3("Brute force")
doc.p("在 n² 个格子里选 n 个放皇后, 再检查。n = 8 时组合数超过 40 亿。")
doc.h3("Intuition: 一行放一个, 用三个 set 检查冲突")
doc.p("每一行一定恰好有一个皇后 (不然有两个在同一行)。所以按行来: decision tree 的第 r 层, 决定第 r 行的皇后放在哪一列。")
doc.p("放之前检查会不会被攻击。如果每次都扫一遍已经放的皇后, 是 <code>O(n)</code>。用三个 set 可以 <code>O(1)</code>:")
nc.bullets(doc, "<code>cols</code>: 已经被占的列。",
           "<code>diag</code>: 已经被占的 \"\\\" 斜线。同一条这种斜线上 <code>r - c</code> 相同。",
           "<code>anti</code>: 已经被占的 \"/\" 斜线。同一条这种斜线上 <code>r + c</code> 相同。")
doc.p("放下皇后时把它的列、两条斜线加进三个 set; 退回时删掉。")
doc.p("剪枝的效果: 8 皇后实际只访问了 %d 个节点, 而不是 8⁸ ≈ 1677 万。" % nq8_nodes)
doc.h3("算法")
nc.steps(doc, "<code>dfs(r)</code>: r == n, 记录当前的棋盘。",
         "对每一列 c: c 在 cols、r - c 在 diag、r + c 在 anti, 有一个就跳过。",
         "否则三个 set 加进去, 记录 path[r] = c, dfs(r + 1), 再从三个 set 删掉。")
doc.svg(SL + "/n_queens_core.svg", "4 × 4 棋盘, 加上三个 set 的逐列检查。")
doc.h3("手动走一遍")
doc.svg(SL + "/n_queens_trace.svg", "path 和三个 set 的变化。")
doc.h3("复杂度")
doc.p("Time 上界 <code>O(n!)</code>, 实际因为剪枝小很多。Space <code>O(n)</code>。")
nc.solution(doc, SRC["nqueens"])
doc.note("多个约束: 每个约束一个 set, 放之前 O(1) 检查, 放下 add, 退回 remove。")

# ================================================================ 识别信号
doc.h2("9. 识别信号: 看到什么, 就想到 backtracking")
nc.table(doc, ["题目特征", "做法", "complexity"], [
    ["\"所有子集 / 所有组合\"", "start index 只往后选; 每个节点都记录", "<code>O(n · 2ⁿ)</code>"],
    ["\"所有排列\"", "每层从头选, used 跳过", "<code>O(n · n!)</code>"],
    ["和为 target 的组合, 可以重复选", "递归传 i (不是 i + 1), 排序后 break 剪枝", "decision tree 大小"],
    ["输入有重复, 输出要去重", "排序 + 同层 i > start and a[i] == a[i-1] 跳过", "去掉重复的子树"],
    ["生成所有合法的 xxx (括号、IP 地址)", "push 之前检查约束, 只走合法的分支", "只和答案个数有关"],
    ["每一位的选项来自不同的集合", "第 idx 层从第 idx 组里选", "<code>O(∏ 每组大小)</code>"],
    ["grid 上找路径, 格子不能重复用", "进去标记 #, 出来恢复", "<code>O(m·n · 3^L)</code>"],
    ["棋盘放置, 多个约束", "每个约束一个 set, O(1) 检查", "剪枝后远小于 <code>O(n!)</code>"],
    ["只要答案的个数 / 最优值, 不要列出来", "多半是 DP (见 14、15)", "指数 → 多项式"]])
doc.p("一句话: 题目要\"列出所有\", 就是 backtracking。先画出 decision tree, 想清楚 path、choices、结束条件, 再想哪些分支可以提前剪掉。")

doc.h2("以后再学")
doc.p("Sudoku Solver (行、列、九宫格三个 set)、Palindrome Partitioning 和 Restore IP Addresses (选项是\"下一段切多长\")、给 backtracking 加 memo 变成 DP。")
doc.write("docs/13-backtracking.html")
