# 15 · DP (2) 正文 (NeetCode 式讲法)。由 15_dp-2d.py 的 build_doc() exec, 共用 CODE / SLUG。
import nclib as nc
from counts import cnt

EX = os.path.join(d.ROOT, "docs", "svg", SLUG, "%s_examples.svg")
EXS = SLUG + "/%s_examples.svg"
ns = {}
for k in ["unique_paths", "min_path_sum", "maximal_square", "lcs", "edit_distance", "lps_expand", "lps_dp", "count_sub", "regex"]:
    exec(CODE[k], ns)

# ---------------------------------------------------------------- 例子图
assert ns["unique_paths"](3, 7) == 28 and ns["unique_paths"](3, 2) == 3
nc.examples_svg(EX % "unique_paths", "Unique Paths examples", ["m × n 的 grid, 从左上角走到右下角, 每一步只能往右或往下。一共有多少条不同的路径"], [
    dict(title="Example:  m = 3, n = 2  →  3", index=False, rows=[("row 0", ["S", ""], ["new", "keep"]), ("row 1", ["", ""], None),
                                                               ("row 2", ["", "E"], ["keep", "new"])],
         extra=["右 → 下 → 下;  下 → 右 → 下;  下 → 下 → 右  → 3 条"]),
    dict(title="Example 2:  m = 3, n = 7  →  28")],
    legend=[("new", "起点 S / 终点 E")])

g = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
assert ns["min_path_sum"]([r[:] for r in g]) == 7
nc.examples_svg(EX % "min_path_sum", "Minimum Path Sum examples", ["grid 里每格有一个非负数。从左上走到右下, 只能往右或往下, 路径上的数加起来最小是多少"], [
    dict(title="Example:  grid = [[1,3,1],[1,5,1],[4,2,1]]  →  7", index=False,
         rows=[("row 0", [1, 3, 1], ["new", "new", "new"]), ("row 1", [1, 5, 1], ["keep", "keep", "new"]), ("row 2", [4, 2, 1], ["keep", "keep", "new"])],
         extra=["1 → 3 → 1 → 1 → 1 = 7"])],
    legend=[("new", "最优路径")])

m = [list("10100"), list("10111"), list("11111"), list("10010")]
assert ns["maximal_square"]([r[:] for r in m]) == 4
nc.examples_svg(EX % "maximal_square", "Maximal Square examples", ["0/1 矩阵里, 找只包含 1 的最大正方形, 返回面积"], [
    dict(title="Example:  →  4", index=False, rows=[
        ("row 0", list("10100"), None), ("row 1", list("10111"), ["keep", "keep", "new", "new", "keep"]),
        ("row 2", list("11111"), ["keep", "keep", "new", "new", "keep"]), ("row 3", list("10010"), None)],
         extra=["边长 2 的正方形 (绿色), 面积 4。row 1..2, col 3..4 也是一个"])],
    legend=[("new", "最大正方形")])

assert ns["longest_common_subsequence"]("abcde", "ace") == 3 and ns["longest_common_subsequence"]("abc", "def") == 0
nc.examples_svg(EX % "lcs", "LCS examples", ["两个字符串的最长公共子序列 (common subsequence) 有多长。子序列可以跳着选, 但顺序不能变"], [
    dict(title="Example 1:  text1 = \"abcde\", text2 = \"ace\"  →  3", index=False,
         rows=[("text1", list("abcde"), ["new", "keep", "new", "keep", "new"]), ("text2", list("ace"), ["new", "new", "new"])],
         extra=["\"ace\" 同时是两个字符串的子序列"]),
    dict(title="Example 2:  \"abc\" 和 \"def\"  →  0", extra=["没有共同的字母"])],
    legend=[("new", "公共子序列")])

assert ns["min_distance"]("horse", "ros") == 3
nc.examples_svg(EX % "edit_distance", "Edit Distance examples", ["把 word1 变成 word2, 每一步可以: 插入一个字符 / 删除一个字符 / 替换一个字符。最少几步"], [
    dict(title="Example:  word1 = \"horse\", word2 = \"ros\"  →  3",
         extra=["horse → rorse (把 h 换成 r)", "rorse → rose (删掉 r)", "rose → ros (删掉 e)"])],
    legend=[])

assert ns["longest_palindrome"]("babad") in ("bab", "aba") and ns["longest_palindrome"]("cbbd") == "bb"
nc.examples_svg(EX % "lps", "Longest Palindromic Substring examples", ["找最长的 palindrome substring (连续的, 正着读和反着读一样)"], [
    dict(title="Example 1:  s = \"babad\"  →  \"bab\" (或 \"aba\")", items=list("babad"), ans=[(0, 2)], ans_text="\"bab\""),
    dict(title="Example 2:  s = \"cbbd\"  →  \"bb\"", items=list("cbbd"), ans=[(1, 2)], ans_text="偶数长度, 中心在两个 b 之间")])

assert ns["count_substrings"]("aaa") == 6 and ns["count_substrings"]("abc") == 3
nc.examples_svg(EX % "count_sub", "Palindromic Substrings examples", ["数一数: 有多少个 substring 是 palindrome (位置不同就算不同)"], [
    dict(title="Example 1:  s = \"abc\"  →  3", extra=["\"a\", \"b\", \"c\""]),
    dict(title="Example 2:  s = \"aaa\"  →  6", extra=["\"a\" × 3,  \"aa\" × 2,  \"aaa\" × 1"])],
    legend=[])

assert ns["is_match"]("aa", "a*") and not ns["is_match"]("aa", "a") and ns["is_match"]("aab", "c*a*b")
nc.examples_svg(EX % "regex", "Regular Expression Matching examples",
                ["pattern p 里: '.' 匹配任意一个字符; 'x*' 匹配 0 个或多个 x。判断 p 能不能匹配<整个> s"], [
    dict(title="Example 1:  s = \"aa\", p = \"a\"  →  False", extra=["a 只能匹配一个字符, s 有两个"]),
    dict(title="Example 2:  s = \"aa\", p = \"a*\"  →  True", extra=["a* 匹配两个 a"]),
    dict(title="Example 3:  s = \"aab\", p = \"c*a*b\"  →  True", extra=["c* 匹配 0 个 c, a* 匹配两个 a, b 匹配 b"])],
    legend=[])

# ================================================================ HTML
doc = d.Doc("15 · Dynamic Programming (2): Grid / Two Strings / Interval")
doc.h2("这篇讲什么")
doc.p("14 里的 DP, state 只需要一个下标。这篇的题, 一个子问题需要<b>两个下标</b>才能描述清楚, 所以 dp 是一个二维表格 <code>dp[i][j]</code>。常见的有三种:")
nc.bullets(doc, "<b>grid</b>: <code>dp[i][j]</code> 表示走到格子 (i, j) 的答案。",
           "<b>两个字符串</b>: <code>dp[i][j]</code> 表示第一个字符串的前 i 个字符和第二个字符串的前 j 个字符的答案。",
           "<b>一个字符串的区间</b>: <code>dp[i][j]</code> 表示子串 <code>s[i..j]</code> 的答案。")
doc.p("思考方法和 14 一样: 先想\"最后一步做了什么\", 推出 transition。新的难点是<b>填表的顺序</b>: 要保证填 <code>dp[i][j]</code> 的时候, 它依赖的格子都已经填好了。画出依赖的方向, 顺序就清楚了。")
doc.svg(SLUG + "/general_core.svg", "什么时候需要 2D、怎么从\"最后一步\"推出 transition、依赖的方向决定填表顺序。")
nc.solution(doc, CODE["template"], summary="2D DP 通用模板")
nc.table(doc, ["#", "题目", "考过的公司数", "相比上一题多了什么"], [
    ["1", "Unique Paths", cnt("Unique Paths"), "模板题: grid, 上 + 左"],
    ["2", "Minimum Path Sum", cnt("Minimum Path Sum"), "相加换成取 min"],
    ["3", "Maximal Square", cnt("Maximal Square"), "依赖三个邻居"],
    ["4", "Longest Common Subsequence", cnt("Longest Common Subsequence"), "换成两个字符串"],
    ["5", "Edit Distance", cnt("Edit Distance"), "三种操作, 三个方向"],
    ["6", "Longest Palindromic Substring", cnt("Longest Palindromic Substring"), "一个字符串的区间"],
    ["7", "Palindromic Substrings", cnt("Palindromic Substrings"), "同上, 改成计数"],
    ["8", "Regular Expression Matching", cnt("Regular Expression Matching"), "* 有两种选择"]])
doc.p("每道题的顺序: <b>题目在问什么 → 看例子 → brute force → intuition → 算法 → 手动走一遍 → 复杂度</b>。代码放在最后, 默认折叠。")
doc.p("前置知识: 14 · DP (1) 的四步思路。")

# ================================================================ 1
doc.h2("1. Unique Paths")
doc.h3("题目在问什么")
doc.p("一个 m × n 的 grid, 机器人从左上角出发, 每一步只能往<b>右</b>或往<b>下</b>走。走到右下角一共有多少条不同的路径?")
doc.h3("看例子")
doc.svg(EXS % "unique_paths", "例子。")
doc.h3("Brute force")
doc.p("recursion: 到达 (i, j) 的最后一步, 要么从上面 (i-1, j) 下来, 要么从左边 (i, j-1) 过来。所以 <code>f(i, j) = f(i-1, j) + f(i, j-1)</code>。直接 recursion 会重复计算, 指数级。")
doc.h3("Intuition: 两个参数 → 二维表")
doc.p("recursion 有两个参数 i 和 j, 所以 state 是二维的: <code>dp[i][j]</code> = 走到 (i, j) 的路径数。")
doc.p("transition: <code>dp[i][j] = dp[i-1][j] + dp[i][j-1]</code>。base case: 第一行和第一列都只有一种走法 (一直往右或一直往下), 都是 1。")
doc.p("填表顺序: 每个格子依赖<b>上面</b>和<b>左边</b>, 所以一行一行、从左往右填, 用到的格子一定已经填好了。")
doc.p("省空间: 每一行只依赖上一行和本行左边, 所以只留一行数组就够了: <code>row[j] += row[j-1]</code> (加号左边的 row[j] 是上一行的值, row[j-1] 是本行刚更新的值)。")
doc.h3("算法")
nc.steps(doc, "<code>dp</code> 全部初始化为 1 (第一行、第一列都是 1)。",
         "i 从 1 到 m-1, j 从 1 到 n-1: <code>dp[i][j] = dp[i-1][j] + dp[i][j-1]</code>。",
         "返回 <code>dp[m-1][n-1]</code>。")
doc.svg(SLUG + "/unique_paths_core.svg", "recursion 里 f(1,2) 被算了两遍; dp 表每个格子只算一次。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/unique_paths_trace.svg", "m = 3, n = 4: 逐格填表, 每格 = 上面 + 左边。")
doc.h3("复杂度")
doc.p("Time <code>O(m·n)</code>, Space <code>O(n)</code> (一行)。")
nc.solution(doc, CODE["unique_paths"])
doc.note("grid 上只能往右 / 往下: dp[i][j] 由上面和左边推出, 一行一行填, 可以压成一行。")

# ================================================================ 2
doc.h2("2. Minimum Path Sum")
doc.h3("题目在问什么")
doc.p("grid 里每格有一个非负整数。从左上走到右下, 只能往右或往下。求路径上所有数加起来的<b>最小值</b>。")
doc.h3("看例子")
doc.svg(EXS % "min_path_sum", "例子。")
doc.h3("Brute force")
doc.p("枚举所有路径, 和第 1 题一样是指数级的。")
doc.h3("Intuition: 和第 1 题一样, 相加换成 min")
doc.p("到达 (i, j) 还是只能从上面或左边来。这次要的是最小和, 所以选两者里小的那个, 再加上自己: <code>dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])</code>。")
doc.p("base case: 第一行只能从左边来, 第一列只能从上面来, 都是一路累加。")
doc.h3("算法")
nc.steps(doc, "第一行、第一列做累加。", "其他格子: <code>dp[i][j] = grid[i][j] + min(上, 左)</code>。", "返回右下角。")
doc.svg(SLUG + "/min_path_sum_core.svg", "dp[1][1] 在上面和左边里选小的那个。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/min_path_sum_trace.svg", "3 × 3 grid 逐格填表, 每格写出了 min 和加法。")
doc.h3("复杂度")
doc.p("Time <code>O(m·n)</code>, Space <code>O(n)</code> 或者直接在 grid 上改 <code>O(1)</code>。")
nc.solution(doc, CODE["min_path_sum"])
doc.note("同一个依赖方向, 换一个运算: 计数用 +, 最优用 min / max。")

# ================================================================ 3
doc.h2("3. Maximal Square")
doc.h3("题目在问什么")
doc.p("一个只有 0 和 1 的矩阵, 找出<b>只包含 1</b> 的最大正方形, 返回它的面积。")
doc.h3("看例子")
doc.svg(EXS % "maximal_square", "例子。")
doc.h3("Brute force")
doc.p("枚举每个格子作为正方形的左上角, 再枚举边长, 检查里面是不是全是 1。<code>O((m·n)²)</code> 左右。")
doc.h3("Intuition: 以 (i, j) 为右下角的最大正方形")
doc.p("state: <code>dp[i][j]</code> = 以 (i, j) 为<b>右下角</b>的、全是 1 的最大正方形的边长。")
doc.p("如果 matrix[i][j] 是 0, dp 就是 0。如果是 1, 它能形成多大的正方形, 取决于三个邻居: 上面 <code>dp[i-1][j]</code>、左边 <code>dp[i][j-1]</code>、左上 <code>dp[i-1][j-1]</code>。")
doc.p("<code>dp[i][j] = min(上, 左, 左上) + 1</code>。为什么是 min? 想象要在 (i, j) 拼一个边长 k 的正方形, 需要它上面、左边、左上这三个方向都至少有边长 k - 1 的正方形。三个里最小的那个, 决定了能拼多大。")
doc.p("答案是所有 dp 里最大的边长, 平方就是面积。")
doc.h3("算法")
nc.steps(doc, "多开一行一列 0 当边界。",
         "matrix[i][j] == '1' 时: <code>dp[i+1][j+1] = min(dp[i][j+1], dp[i+1][j], dp[i][j]) + 1</code>, 更新最大边长。",
         "返回最大边长的平方。")
doc.svg(SLUG + "/maximal_square_core.svg", "三个邻居里最小的决定边长; 左上角的 0 把对角方向限制成 1。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/maximal_square_trace.svg", "4 × 5 矩阵, 补一圈 0 之后逐格填表。")
doc.h3("复杂度")
doc.p("Time <code>O(m·n)</code>, Space <code>O(m·n)</code> (可以压成一行)。")
nc.solution(doc, CODE["maximal_square"])
doc.note("以 (i, j) 为右下角的最大正方形: min(上, 左, 左上) + 1。")

# ================================================================ 4
doc.h2("4. Longest Common Subsequence")
doc.h3("题目在问什么")
doc.p("两个字符串 text1 和 text2, 求它们最长的<b>公共子序列</b>的长度。子序列可以跳着选字符, 但不能改变顺序。")
doc.h3("看例子")
doc.svg(EXS % "lcs", "两个例子。")
doc.h3("Brute force")
doc.p("枚举 text1 的所有子序列 (<code>2^m</code> 个), 检查是不是 text2 的子序列。指数级。")
doc.h3("Intuition: 比较两个前缀的最后一个字符")
doc.p("两个字符串, 子问题就是\"两个前缀\": <code>dp[i][j]</code> = <code>text1[:i]</code> 和 <code>text2[:j]</code> 的 LCS 长度。")
doc.p("transition 看两个前缀的<b>最后一个字符</b> <code>text1[i-1]</code> 和 <code>text2[j-1]</code>:")
nc.bullets(doc, "<b>相同</b>: 这个字符一定可以放进 LCS 里。去掉两个末尾, 剩下的问题是 <code>dp[i-1][j-1]</code>, 再加 1。",
           "<b>不同</b>: 这两个字符不可能都在 LCS 的末尾。至少有一个要丢掉: 丢 text1 的末尾 (<code>dp[i-1][j]</code>), 或者丢 text2 的末尾 (<code>dp[i][j-1]</code>), 取大的。")
doc.p("base case: 任何一个前缀是空的, LCS 是 0, 所以 dp 第 0 行、第 0 列都是 0。")
doc.p("依赖: 左上、上、左。所以还是一行一行、从左往右填。")
doc.h3("算法")
nc.steps(doc, "<code>dp</code> 是 (m+1) × (n+1), 全 0。",
         "i 从 1 到 m, j 从 1 到 n: 相同则 <code>dp[i][j] = dp[i-1][j-1] + 1</code>; 不同则 <code>max(dp[i-1][j], dp[i][j-1])</code>。",
         "返回 <code>dp[m][n]</code>。")
doc.svg(SLUG + "/lcs_core.svg", "最后一个字符相同 → 左上 + 1; 不同 → 丢掉一个字符, 取 max(上, 左)。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/lcs_trace.svg", "\"abcde\" vs \"ace\": 字符相同的格子只依赖左上, 不同的依赖上和左。")
doc.h3("复杂度")
doc.p("Time <code>O(m·n)</code>, Space <code>O(m·n)</code> (可以压成两行)。")
nc.solution(doc, CODE["lcs"])
doc.note("两个字符串的 DP: dp[i][j] = 前 i 个和前 j 个; 看两个末尾字符相同还是不同。")

# ================================================================ 5
doc.h2("5. Edit Distance")
doc.h3("题目在问什么")
doc.p("把 word1 变成 word2, 每一步可以做三种操作之一: <b>插入</b>一个字符、<b>删除</b>一个字符、<b>替换</b>一个字符。最少需要几步?")
doc.h3("看例子")
doc.svg(EXS % "edit_distance", "例子。")
doc.h3("Brute force")
doc.p("recursion 试所有操作序列, 指数级。")
doc.h3("Intuition: 和 LCS 一样看末尾, 三种操作对应三个方向")
doc.p("state: <code>dp[i][j]</code> = 把 <code>word1[:i]</code> 变成 <code>word2[:j]</code> 的最少步数。")
doc.p("看两个末尾字符:")
nc.bullets(doc, "<b>相同</b>: 不用动, <code>dp[i][j] = dp[i-1][j-1]</code>。",
           "<b>不同</b>: 最后一步是三种操作之一, 取最少的再加 1:",
           "　替换 word1 的末尾成 word2 的末尾 → 剩下 <code>dp[i-1][j-1]</code> (左上)",
           "　删掉 word1 的末尾 → 剩下 <code>dp[i-1][j]</code> (上)",
           "　在 word1 末尾插入 word2 的末尾 → 剩下 <code>dp[i][j-1]</code> (左)")
doc.p("base case: <code>dp[i][0] = i</code> (删掉 i 个字符), <code>dp[0][j] = j</code> (插入 j 个字符)。")
doc.h3("算法")
nc.steps(doc, "初始化第 0 行、第 0 列。",
         "相同: <code>dp[i][j] = dp[i-1][j-1]</code>; 不同: <code>1 + min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1])</code>。",
         "返回 <code>dp[m][n]</code>。")
doc.svg(SLUG + "/edit_distance_core.svg", "替换 = 左上, 删除 = 上, 插入 = 左。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/edit_distance_trace.svg", "\"horse\" → \"ros\": 字符相同时直接拿左上, 不同时 1 + min(三个)。")
doc.h3("复杂度")
doc.p("Time <code>O(m·n)</code>, Space <code>O(m·n)</code>。")
nc.solution(doc, CODE["edit_distance"])
doc.note("编辑距离: 末尾相同直接拿左上; 不同则 1 + min(替换 = 左上, 删除 = 上, 插入 = 左)。")

# ================================================================ 6
doc.h2("6. Longest Palindromic Substring")
doc.h3("题目在问什么")
doc.p("找 s 里最长的 palindrome <b>substring</b> (连续的, 正着读和反着读一样)。")
doc.h3("看例子")
doc.svg(EXS % "lps", "两个例子。")
doc.h3("Brute force")
doc.p("枚举所有 substring (<code>O(n²)</code> 个), 每个检查是不是 palindrome (<code>O(n)</code>)。<code>O(n³)</code>。")
doc.h3("Intuition 1: 从中心往两边扩")
doc.p("palindrome 是左右对称的, 有一个中心。所以反过来: <b>枚举中心, 从中心往两边扩</b>, 两边字符相同就继续扩, 不同就停。")
doc.p("中心有两种: 一个字符 (奇数长度, 比如 \"aba\"), 或者两个字符之间 (偶数长度, 比如 \"abba\")。一共 <code>2n - 1</code> 个中心, 每个最多扩 <code>O(n)</code>, 总共 <code>O(n²)</code>, 空间 <code>O(1)</code>。这是面试里最实用的写法。")
doc.svg(SLUG + "/longest_palindromic_substring_core.svg", "babad 里几个中心的扩展; 两端不同或者越界就停。")
nc.solution(doc, CODE["lps_expand"], summary="代码: 中心扩展")
doc.h3("Intuition 2: 区间 DP")
doc.p("也可以用 DP: <code>dp[i][j]</code> = <code>s[i..j]</code> 是不是 palindrome。它是 palindrome, 当且仅当两端相同 <code>s[i] == s[j]</code>, 并且里面的 <code>s[i+1..j-1]</code> 也是 palindrome。")
doc.p("<code>dp[i][j]</code> 依赖 <code>dp[i+1][j-1]</code> (左下方的格子)。所以 i 要<b>从大到小</b>填 (从下往上), j 从小到大。这是区间 DP 典型的填表顺序: 短的区间先算, 长的后算。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/longest_palindromic_substring_trace.svg", "babad 的 dp 表, 从下往上填, 只用上三角。")
doc.h3("复杂度")
doc.p("两种都是 Time <code>O(n²)</code>。中心扩展 Space <code>O(1)</code>, DP 是 <code>O(n²)</code>。")
nc.solution(doc, CODE["lps_dp"], summary="代码: 区间 DP")
doc.note("回文子串: 优先用中心扩展 (2n - 1 个中心)。区间 DP 的 dp[i][j] 依赖 dp[i+1][j-1], 所以 i 从大到小填。")

# ================================================================ 7
doc.h2("7. Palindromic Substrings")
doc.h3("题目在问什么")
doc.p("数一数 s 里有多少个 substring 是 palindrome。位置不同的算不同的。")
doc.h3("看例子")
doc.svg(EXS % "count_sub", "两个例子。")
doc.h3("Intuition: 第 6 题的中心扩展, 改成计数")
doc.p("每个 palindrome 都有唯一的中心。从每个中心往外扩, 每扩成功一次, 就多找到一个 palindrome, count 加 1。")
doc.h3("算法")
nc.steps(doc, "对每个中心 (2n - 1 个): l, r 从中心开始, 当 <code>s[l] == s[r]</code>: count += 1, l -= 1, r += 1。")
doc.svg(SLUG + "/palindromic_substrings_core.svg", "aba 的 4 个 palindrome 分别属于哪个中心。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/palindromic_substrings_trace.svg", "aba 的 5 个中心逐个扩展, count 一步步变成 4。")
doc.h3("复杂度")
doc.p("Time <code>O(n²)</code>, Space <code>O(1)</code>。")
nc.solution(doc, CODE["count_sub"])
doc.note("数回文子串: 中心扩展, 每扩成功一次 count + 1。")

# ================================================================ 8
doc.h2("8. Regular Expression Matching")
doc.h3("题目在问什么")
doc.p("实现一个简单的正则匹配: pattern p 里, <code>.</code> 匹配任意一个字符, <code>x*</code> 匹配 0 个或多个 x (* 总是跟在一个字符后面)。判断 p 能不能匹配<b>整个</b> s。")
doc.h3("看例子")
doc.svg(EXS % "regex", "三个例子。")
doc.h3("Brute force")
doc.p("recursion: 遇到 x* 就试匹配 0 个、1 个、2 个……, 分支很多, 指数级。")
doc.h3("Intuition: 两个字符串的 DP, 难点只在 *")
doc.p("和第 4、5 题一样: <code>dp[i][j]</code> = <code>s[:i]</code> 能不能被 <code>p[:j]</code> 完全匹配。看 p 的最后一个字符 <code>p[j-1]</code>:")
nc.bullets(doc, "<b>普通字符或 .</b>: 和 s 的最后一个字符匹配 (相同或者是 .), 并且前面也匹配: <code>dp[i-1][j-1]</code>。",
           "<b>*</b>: 它和前一个字符 x 一起算 (<code>x*</code>)。有两种选择:",
           "　匹配 0 次: 把 x* 整个扔掉 → <code>dp[i][j-2]</code> (往左跳两格)。",
           "　匹配至少 1 次: s 的最后一个字符要能和 x 匹配, 吃掉它, 但 x* 保留 (还可以继续吃) → <code>dp[i-1][j]</code> (往上一格)。",
           "　两个选择有一个成立就行。")
doc.p("base case: <code>dp[0][0] = True</code>。空的 s 也可能被 p 匹配, 比如 <code>a*b*</code>, 所以第 0 行要按 * 的规则填: <code>dp[0][j] = dp[0][j-2]</code> (p[j-1] 是 * 时)。")
doc.h3("算法")
nc.steps(doc, "dp 是 (m+1) × (n+1)。<code>dp[0][0] = True</code>, 按 * 填第 0 行。",
         "p[j-1] 不是 *: <code>dp[i][j] = 匹配(s[i-1], p[j-1]) and dp[i-1][j-1]</code>。",
         "p[j-1] 是 *: <code>dp[i][j] = dp[i][j-2] or (匹配(s[i-1], p[j-2]) and dp[i-1][j])</code>。",
         "返回 <code>dp[m][n]</code>。")
doc.svg(SLUG + "/regex_core.svg", "* 要么匹配 0 次 (往左跳 2 格), 要么吃掉一个字符并保留自己 (往上 1 格)。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/regex_trace.svg", "s = aab, p = c*a*b: 每个 * 的格子都写出了两种选择。")
doc.h3("复杂度")
doc.p("Time <code>O(m·n)</code>, Space <code>O(m·n)</code>。")
nc.solution(doc, CODE["regex"])
doc.note("x*: 匹配 0 次 → dp[i][j-2]; 匹配至少 1 次 → 当前字符能配 x 并且 dp[i-1][j]。")

# ================================================================ 识别信号
doc.h2("9. 识别信号: 看到什么, 就想到 2D DP")
nc.table(doc, ["题目特征", "state", "transition / 填表顺序"], [
    ["grid 上只能往右 / 往下, 数路径或求最优", "dp[i][j] = 到 (i, j)", "上 + 左 (或 min); 一行一行填"],
    ["0/1 矩阵最大正方形", "以 (i, j) 为右下角的边长", "min(上, 左, 左上) + 1"],
    ["两个字符串: 公共子序列、编辑距离、匹配", "dp[i][j] = 前 i 个和前 j 个", "看两个末尾字符; 左上 / 上 / 左"],
    ["回文子串 (最长 / 个数)", "中心扩展; 或 dp[i][j] = s[i..j] 是否回文", "dp[i+1][j-1]; i 从大到小"],
    ["正则 / 通配符匹配", "dp[i][j] = 前 i 个能否被前 j 个匹配", "* 两种选择: 0 次 / 至少 1 次"],
    ["区间上的最优 (戳气球、合并石头)", "dp[i][j] = 区间 [i, j] 的最优", "枚举最后一步 k; 按区间长度从短到长"]])
doc.p("判断 dp 是几维: 看 brute force recursion 里有几个参数在变。两个字符串几乎一定是 dp[i][j]。")

doc.h2("以后再学")
doc.p("Burst Balloons (区间 DP, 枚举最后一个戳的)、Distinct Subsequences、Interleaving String、Wildcard Matching (和第 8 题几乎一样)。")
doc.write("docs/15-dp-2d.html")
