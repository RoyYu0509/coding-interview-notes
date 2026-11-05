# 04 · Prefix Sum 正文 (NeetCode 式讲法)。由 04_prefix_sum.py 末尾 exec, 共用 CODE / run / SLUG。
import nclib as nc
from counts import cnt

EX = os.path.join(d.ROOT, "docs", "svg", SLUG, "%s_examples.svg")

# ---------------------------------------------------------------- 例子图
assert run("pivot", "pivotIndex")([1, 7, 3, 6, 5, 6]) == 3
assert run("pivot", "pivotIndex")([1, 2, 3]) == -1
nc.examples_svg(EX % "pivot", "Find Pivot Index examples",
                ["找一个位置 i: 它左边所有数的和 = 它右边所有数的和 (都不含 nums[i] 自己)。有多个取最左的, 没有返回 -1"], [
    dict(title="Example 1:  nums = [1,7,3,6,5,6]  →  3", items=[1, 7, 3, 6, 5, 6], hl=[3],
         ans_text="左边 1+7+3 = 11, 右边 5+6 = 11"),
    dict(title="Example 2:  nums = [1,2,3]  →  -1", items=[1, 2, 3],
         extra=["i = 0: 左 0, 右 5;  i = 1: 左 1, 右 3;  i = 2: 左 3, 右 0  → 都不相等"]),
    dict(title="Example 3:  nums = [2,1,-1]  →  0", items=[2, 1, -1], hl=[0],
         ans_text="左边什么都没有, 和是 0; 右边 1 + (-1) = 0")],
    legend=[("new", "pivot")])

f = run("subk", "subarraySum")
assert f([1, 1, 1], 2) == 2 and f([1, 2, 3], 3) == 2 and f([3, 4, 7, 2, -3, 1, 4, 2], 7) == 4
nc.examples_svg(EX % "subk", "Subarray Sum Equals K examples",
                ["数一数: 有多少段连续的 subarray, 加起来正好等于 k。数组里可以有负数"], [
    dict(title="Example 1:  nums = [1,1,1], k = 2  →  2", items=[1, 1, 1],
         extra=["[1,1] (index 0..1) 和 [1,1] (index 1..2), 内容一样但位置不同, 算两段"]),
    dict(title="Example 2:  nums = [1,2,3], k = 3  →  2", items=[1, 2, 3],
         extra=["[1,2] 和 [3]"]),
    dict(title="Example 3:  nums = [3,4,7,2,-3,1,4,2], k = 7  →  4", items=[3, 4, 7, 2, -3, 1, 4, 2],
         extra=["[3,4]   [7]   [7,2,-3,1]   [1,4,2]  —— 第三段里有 -3, 说明有负数时和会变小 (后面会用这个例子走一遍)"])],
    legend=[("keep", "数组")])

f = run("divk", "subarraysDivByK")
assert f([4, 5, 0, -2, -3, 1], 5) == 7 and f([5], 9) == 0
nc.examples_svg(EX % "divk", "Subarray Sums Divisible by K examples",
                ["数一数: 有多少段连续的 subarray, 和是 k 的倍数 (0 也算倍数)"], [
    dict(title="Example 1:  nums = [4,5,0,-2,-3,1], k = 5  →  7", items=[4, 5, 0, -2, -3, 1],
         extra=["[4,5,0,-2,-3,1]=5   [5]   [5,0]   [5,0,-2,-3]=0   [0]   [0,-2,-3]=-5   [-2,-3]=-5"]),
    dict(title="Example 2:  nums = [5], k = 9  →  0", items=[5])],
    legend=[("keep", "数组")])

f = run("contig", "findMaxLength")
assert f([0, 1]) == 2 and f([0, 1, 0]) == 2 and f([0, 1, 1, 0, 1, 1, 1, 0]) == 4
nc.examples_svg(EX % "contig", "Contiguous Array examples",
                ["数组只有 0 和 1。找最长的一段连续 subarray, 里面 0 和 1 的个数一样多, 返回长度"], [
    dict(title="Example 1:  nums = [0,1,0]  →  2", items=[0, 1, 0], ans=[(0, 1)], ans_text="[0,1] 或 [1,0]",
         bad=[(0, 2, "[0,1,0]: 两个 0 一个 1 ✗")]),
    dict(title="Example 2:  nums = [0,1,1,0,1,1,1,0]  →  4", items=[0, 1, 1, 0, 1, 1, 1, 0], ans=[(0, 3)],
         ans_text="[0,1,1,0]: 两个 0 两个 1")])

f = run("product", "productExceptSelf")
assert f([1, 2, 3, 4]) == [24, 12, 8, 6] and f([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
nc.examples_svg(EX % "product", "Product of Array Except Self examples",
                ["对每个位置 i, 算出除了 nums[i] 以外所有数的乘积。不能用除法"], [
    dict(title="Example 1:  nums = [1,2,3,4]  →  [24,12,8,6]", rows=[
        ("nums", [1, 2, 3, 4], ["keep", "keep", "new", "keep"]), ("out", [24, 12, 8, 6], ["keep", "keep", "new", "keep"])],
         extra=["out[2] = 1 × 2 × 4 = 8, 就是除了 3 以外的所有数相乘"]),
    dict(title="Example 2:  nums = [-1,1,0,-3,3]  →  [0,0,9,0,0]", items=[-1, 1, 0, -3, 3], cw=40,
         extra=["有一个 0: 除了 0 自己, 其他位置的乘积都包含这个 0。所以不能用 \"总积 ÷ nums[i]\" (总积是 0, 也不能除以 0)"])],
    legend=[("new", "例: i = 2")])

nm = run("matrix", "NumMatrix")([[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]])
assert nm.sumRegion(2, 1, 4, 3) == 8 and nm.sumRegion(1, 1, 2, 2) == 11
nc.examples_svg(EX % "matrix", "Range Sum Query 2D examples",
                ["矩阵不变。会被问很多次: 左上角 (r1, c1) 到右下角 (r2, c2) 这个子矩形里所有数的和"], [
    dict(title="Example:  sumRegion(1, 1, 2, 2)  →  11", index=False, rows=[
        ("row 0", [3, 0, 1, 4, 2], None), ("row 1", [5, 6, 3, 2, 1], ["keep", "new", "new", "keep", "keep"]),
        ("row 2", [1, 2, 0, 1, 5], ["keep", "new", "new", "keep", "keep"]), ("row 3", [4, 1, 0, 1, 7], None),
        ("row 4", [1, 0, 3, 0, 5], None)],
         extra=["绿色子矩形: 6 + 3 + 2 + 0 = 11。如果有 10⁴ 次 query, 每次都把格子加一遍就太慢了"])],
    legend=[("new", "要求和的子矩形")])

f = run("flights", "corpFlightBookings")
assert f([[1, 2, 10], [2, 3, 20], [2, 5, 25]], 5) == [10, 55, 45, 25, 25]
nc.examples_svg(EX % "diff", "Corporate Flight Bookings examples",
                ["航班编号 1..n。每条 booking [first, last, seats]: 航班 first 到 last 每一班都订了 seats 个座位。求每班的总数"], [
    dict(title="Example:  bookings = [[1,2,10],[2,3,20],[2,5,25]], n = 5", index=False, rows=[
        ("航班", [1, 2, 3, 4, 5], ["keep"] * 5),
        ("[1,2,10]", [10, 10, "", "", ""], ["new", "new", "keep", "keep", "keep"]),
        ("[2,3,20]", ["", 20, 20, "", ""], ["keep", "new", "new", "keep", "keep"]),
        ("[2,5,25]", ["", 25, 25, 25, 25], ["keep", "new", "new", "new", "new"]),
        ("合计", [10, 55, 45, 25, 25], ["keep"] * 5)],
         extra=["每条 booking 是给一段连续的航班都加同一个数。答案 = 每一列加起来"])],
    legend=[("new", "这条 booking 加到的航班")])

# ================================================================ HTML
doc = d.Doc("04 · Prefix Sum")
doc.h2("这篇讲什么")
doc.p("这一类题都和<b>区间和</b>有关: 数组里一段连续的数加起来是多少, 或者有多少段连续的数, 加起来满足某个条件。")
doc.p("最直接的做法是每次都把那一段重新加一遍。问题是, 不同的区间重叠很多, 同一个数会被加很多次。")
doc.p("<b>Prefix Sum</b> (前缀和) 的想法是: 先花 <code>O(n)</code> 算出\"从开头加到每个位置\"的和, 存起来。之后任何一段的和都能用<b>两个前缀和相减</b>得到, 只要 <code>O(1)</code>。")
doc.p("它最重要的用法是和 Hash Table 配合, 把\"数有多少段的和等于 k\"从 <code>O(n²)</code> 降到 <code>O(n)</code>。这也是本篇的核心 (第 2 题)。")
nc.table(doc, ["#", "题目", "考过的公司数", "相比上一题多了什么"], [
    ["1", "Find Pivot Index", cnt("Find Pivot Index"), "前缀和最简单的用法: 左边和 vs 右边和"],
    ["2", "Subarray Sum Equals K", cnt("Subarray Sum Equals K"), "<b>核心</b>: 前缀和 + Hash Table, 数有多少段"],
    ["3", "Subarray Sums Divisible by K", cnt("Subarray Sums Divisible by K"), "\"等于 k\" 换成 \"是 k 的倍数\": 看余数"],
    ["4", "Contiguous Array", cnt("Contiguous Array"), "先把题目变形成\"和为 0\"; 求最长而不是个数"],
    ["5", "Product of Array Except Self", cnt("Product of Array Except Self"), "加法换成乘法, 左边一遍、右边一遍"],
    ["6", "Range Sum Query 2D", cnt("Range Sum Query 2D - Immutable"), "一维换成二维"],
    ["7", "Corporate Flight Bookings", cnt("Corporate Flight Bookings"), "反过来: 很多次区间修改 (difference array)"],
    ["8", "和 sliding window 的分界", "", "什么时候用 sliding window, 什么时候用 prefix sum"]])
doc.p("每道题的顺序: <b>题目在问什么 → 看例子 → brute force → intuition → 算法 → 手动走一遍 → 复杂度</b>。代码放在最后, 默认折叠。")
doc.p("前置知识: 01 · Hash Table 里 \"边扫边查\" 的思路 (Two Sum)。")

# ================================================================ 0 -> 前缀和本身
doc.h2("先认识 prefix sum: 区间和 = 两个前缀和相减")
doc.p("先看最基础的问题 (Range Sum Query): 数组 <code>nums</code> 不会变, 但会被问很多次 \"<code>nums[i..j]</code> 的和是多少\"。")
doc.p("Brute force: 每次从 i 加到 j, <code>O(n)</code>。q 次就是 <code>O(n·q)</code>。浪费: <code>sum(1..3)</code> 和 <code>sum(0..3)</code> 都把 nums[1..3] 重新加了一遍。")
doc.p("办法: 先算 <code>prefix[k]</code> = 前 k 个数的和 (<code>nums[0] + ... + nums[k-1]</code>)。那么 <code>nums[i..j]</code> 的和 = 前 j+1 个数的和 - 前 i 个数的和 = <code>prefix[j+1] - prefix[i]</code>。")
doc.p("<code>prefix</code> 比 nums 多一格, <code>prefix[0] = 0</code> 表示\"一个数都不取\"。有了它, 从下标 0 开始的区间也能直接相减, 不用特判。")
doc.svg(SLUG + "/range_sum_core.svg", "sum(i..j) = prefix[j+1] - prefix[i]: 两次查表代替一次循环。")
nc.solution(doc, CODE["template"], summary="代码: 建 prefix 数组 + 查区间和")
doc.note("sum(i..j) = prefix[j+1] - prefix[i], prefix[0] = 0。建表 O(n), 之后每次 O(1)。")

# ================================================================ 1
doc.h2("1. Find Pivot Index")
doc.h3("题目在问什么")
doc.p("找一个下标 i, 使得 i <b>左边</b>所有数的和等于 i <b>右边</b>所有数的和 (都不包括 nums[i] 自己)。有多个就返回最左边的, 没有返回 -1。")
doc.h3("看例子")
doc.svg(SLUG + "/pivot_examples.svg", "三个例子。")
doc.p("Example 3 说明: 下标 0 的左边什么都没有, 和算作 0。")
doc.h3("Brute force")
doc.p("每个 i, 把左边加一遍, 右边加一遍, 比较。<code>O(n²)</code>。浪费: i 往右走一格, 左边的和只多了一个数, 却整个重算。")
doc.h3("Intuition")
doc.p("左边的和就是前缀和, 从左往右走的时候边走边加就行, 一个变量 <code>left</code> 够了。")
doc.p("右边的和不用再加: 先算出总和 <code>total</code>, 那么右边 = <code>total - left - nums[i]</code>。")
doc.h3("算法")
nc.steps(doc, "<code>total = sum(nums)</code>, <code>left = 0</code>。",
         "i 从左往右: 如果 <code>left == total - left - nums[i]</code>, 返回 i。否则 <code>left += nums[i]</code>。",
         "走完都没有, 返回 -1。")
doc.svg(SLUG + "/pivot_core.svg", "检查的条件: left == total - left - nums[i]。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/pivot_trace.svg", "[1,7,3,6,5,6]: 走到 i = 3 时 left = 11, right = 28 - 11 - 6 = 11, 相等。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(1)</code>。")
nc.solution(doc, CODE["pivot"])
doc.note("前缀和不一定要存成数组。只需要当前位置的前缀和时, 一个边走边加的变量就够。")

# ================================================================ 2
doc.h2("2. Subarray Sum Equals K (本篇核心)")
doc.h3("题目在问什么")
doc.p("给一个整数数组 <code>nums</code> 和整数 <code>k</code>。数一数: 有多少段<b>连续的</b> subarray, 加起来正好等于 k。数组里<b>可能有负数</b>。")
doc.h3("看例子")
doc.svg(SLUG + "/subk_examples.svg", "三个例子。")
doc.p("Example 3 里有负数, 这一点很重要。它意味着这题不能用 sliding window (03), 因为往右加一个数, 和可能变大也可能变小。最后一节会专门对比。")
doc.h3("Brute force")
doc.p("枚举所有起点 i 和终点 j, 用前缀和 <code>O(1)</code> 算出区间和, 等于 k 就计数。一共 <code>O(n²)</code> 对 (i, j)。")
doc.p("浪费在哪: 固定终点 j 之后, 我们其实只想知道\"有几个起点 i 能让 <code>prefix[j+1] - prefix[i] == k</code>\", 却把所有 i 一个一个试了。")
doc.h3("Intuition: 把条件移项, 变成查表")
doc.p("把 <code>prefix[j+1] - prefix[i] == k</code> 移项, 得到 <code>prefix[i] == prefix[j+1] - k</code>。")
doc.p("右边是已知的数。所以问题变成: <b>在 j 前面, 有多少个前缀和恰好等于 <code>prefix[j+1] - k</code>?</b>")
doc.p("这和 01 里的 Two Sum 一模一样: 边走边把看过的前缀和存进 dict (key 是前缀和的值, value 是出现了几次), 每到一个新位置, 先查 dict 里有几个\"我需要的那个值\", 再把自己存进去。")
doc.p("两个细节:")
nc.bullets(doc, "dict 一开始要放 <code>{0: 1}</code>。它代表空前缀 (一个数都不取, 和为 0)。不放它, 从下标 0 开始的 subarray 就数不到。比如 Example 3 的 [3, 4], 就是靠它数到的。",
           "先查再存。起点必须在终点之前。")
doc.h3("算法")
nc.steps(doc, "<code>count = {0: 1}</code>, <code>prefix = 0</code>, <code>ans = 0</code>。",
         "从左往右, 每个数 x: <code>prefix += x</code>。",
         "<code>ans += count[prefix - k]</code> (之前有几个前缀和等于 prefix - k, 就有几段以当前位置结尾、和为 k 的 subarray)。",
         "<code>count[prefix] += 1</code>。")
doc.svg(SLUG + "/subk_core.svg", "以 j 结尾、和为 k 的 subarray 个数 = 之前有多少个前缀和等于 prefix_j - k。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/subk_trace.svg", "[3,4,7,2,-3,1,4,2], k = 7: ans 在 i = 1, 2, 5, 7 各加 1, 共 4。count[14] 在 i = 5 变成 2。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>: 每个数一次查表、一次写入。Space <code>O(n)</code>: count 最多 n + 1 项。")
nc.solution(doc, CODE["subk"], CODE["hash_template"])
doc.note("连续 subarray + 和等于 k (可能有负数): 前缀和 + Hash Table。先查 count[prefix - k], 再 count[prefix] += 1, 初始 {0: 1}。")

# ================================================================ 3
doc.h2("3. Subarray Sums Divisible by K")
doc.h3("题目在问什么")
doc.p("数一数: 有多少段连续的 subarray, 和是 <code>k</code> 的倍数 (包括 0 和负数倍)。")
doc.h3("看例子")
doc.svg(SLUG + "/divk_examples.svg", "两个例子。")
doc.h3("Brute force")
doc.p("和第 2 题一样, 枚举所有 (i, j), <code>O(n²)</code>。")
doc.h3("Intuition: 和是 k 的倍数 ⇔ 两个前缀和的余数相同")
doc.p("区间和 = <code>prefix[j+1] - prefix[i]</code>。它是 k 的倍数, 等价于两个前缀和除以 k 的<b>余数相同</b>。比如 k = 5, 前缀和 9 和 4 的余数都是 4, 相减 5 是倍数。")
doc.p("所以只要把第 2 题的 key 从\"前缀和\"换成\"前缀和 % k\", 查的也从 <code>prefix - k</code> 换成\"和我余数相同的\"。")
doc.p("Python 的 <code>%</code> 对负数也返回 0..k-1 (比如 <code>-2 % 5 == 3</code>), 所以不用特殊处理负数。")
doc.h3("算法")
nc.steps(doc, "<code>count = {0: 1}</code>。从左往右累加 prefix。",
         "<code>r = prefix % k</code>。<code>ans += count[r]</code>, 然后 <code>count[r] += 1</code>。")
doc.svg(SLUG + "/divk_core.svg", "按余数分桶: 同一个桶里的前缀和两两配对, 每一对都是一段答案。1 + 6 + 0 = 7。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/divk_trace.svg", "每一步先查桶里已经有几个, 再把自己放进去。")
doc.p("变体 Continuous Subarray Sum: 问\"是否存在长度 ≥ 2、和是 k 的倍数的 subarray\"。只问存在、还有长度要求, 所以 dict 不存次数, 存这个余数<b>第一次出现的下标</b>。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(k)</code>。")
nc.solution(doc, CODE["divk"])
doc.note("和是 k 的倍数: 用 prefix % k 当 key。数个数存次数; 问存在 / 最长存第一次出现的下标。")

# ================================================================ 4
doc.h2("4. Contiguous Array")
doc.h3("题目在问什么")
doc.p("数组只有 0 和 1。找<b>最长</b>的一段连续 subarray, 里面 0 和 1 的个数一样多, 返回长度。")
doc.h3("看例子")
doc.svg(SLUG + "/contig_examples.svg", "两个例子。")
doc.h3("Brute force")
doc.p("枚举所有段, 数 0 和 1, <code>O(n²)</code>。")
doc.h3("Intuition: 先把题目变成\"和为 0\"")
doc.p("\"0 和 1 一样多\" 不是一个和。但如果把 <b>0 看成 -1</b>, 一样多就等价于这一段的和是 0。")
doc.p("和为 0 就是第 2 题 k = 0 的情况: 两个前缀和相等。")
doc.p("和第 2 题的区别是这题要<b>最长</b>, 不是个数。同一个前缀和值出现了好几次时, 用最早的那次当起点, 段最长。所以 dict 存的是每个前缀和<b>第一次出现的下标</b>, 之后再出现不覆盖。")
doc.p("起始放 <code>{0: -1}</code>, 表示空前缀在下标 -1 的位置, 这样从下标 0 开始的段长度也能算对。")
doc.h3("算法")
nc.steps(doc, "<code>first = {0: -1}</code>, <code>s = 0</code>。",
         "从左往右, 遇到 1 则 <code>s += 1</code>, 遇到 0 则 <code>s -= 1</code>。",
         "s 在 first 里: 用 <code>i - first[s]</code> 更新最长。s 不在: <code>first[s] = i</code>。")
doc.svg(SLUG + "/contig_core.svg", "s 回到同一个高度, 说明中间 0 和 1 一样多; 最长的就是第一次到这个高度的位置到现在。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/contig_trace.svg", "[0,1,1,0,1,1,1,0]: i = 1 得到长度 2, i = 3 得到长度 4 (最长)。")
doc.p("同样的模板可以做 Maximum Size Subarray Sum Equals k: 查 <code>prefix - k</code> 第一次出现的位置。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(n)</code>。")
nc.solution(doc, CODE["contig"], CODE["maxlen_k"])
doc.note("\"两种东西一样多\": 一种记 +1, 一种记 -1, 变成和为 0。求最长: dict 存第一次出现的下标。")

# ================================================================ 5
doc.h2("5. Product of Array Except Self")
doc.h3("题目在问什么")
doc.p("返回一个数组 <code>out</code>, <code>out[i]</code> = nums 里除了 <code>nums[i]</code> 以外所有数的乘积。<b>不能用除法</b>, 要求 <code>O(n)</code>。")
doc.h3("看例子")
doc.svg(SLUG + "/product_examples.svg", "两个例子。")
doc.p("Example 2 解释了为什么不能用除法: 数组里有 0 时, \"总积 ÷ nums[i]\" 算不出来。")
doc.h3("Brute force")
doc.p("每个 i, 把其他 n - 1 个数乘一遍。<code>O(n²)</code>。浪费: 相邻两个位置要乘的数几乎一样。")
doc.h3("Intuition: 左边的积 × 右边的积")
doc.p("\"除了 i 以外的所有数\" = i <b>左边</b>的所有数 + i <b>右边</b>的所有数。所以 <code>out[i]</code> = (左边所有数的积) × (右边所有数的积)。")
doc.p("左边的积就是\"前缀积\", 从左往右一遍边乘边记。右边的积是\"后缀积\", 从右往左一遍。这就是 prefix sum 的思路, 只是把加法换成了乘法。")
doc.p("省空间的做法: 第一遍把左边的积直接写进 out; 第二遍从右往左, 用一个变量 r 记右边的积, 乘到 out 上。除了答案数组, 只用了一个变量。")
doc.h3("算法")
nc.steps(doc, "第一遍 (从左往右): <code>out[i]</code> = nums[0..i-1] 的积。out[0] = 1。",
         "第二遍 (从右往左): <code>r = 1</code>。每个 i: <code>out[i] *= r</code>, 然后 <code>r *= nums[i]</code>。")
doc.svg(SLUG + "/product_core.svg", "out[i] = 左边的积 × 右边的积。例如 i = 2 时是 2 × 4 = 8。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/product_trace.svg", "第 1 遍把左边的积写进 out; 第 2 遍用 r 滚出右边的积再乘上去。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, 两遍。额外 Space <code>O(1)</code> (答案数组不算)。")
nc.solution(doc, CODE["product"])
doc.note("\"除了自己以外的所有\": 左边一遍、右边一遍。左边的结果存进答案, 右边用一个变量。")

# ================================================================ 6
doc.h2("6. Range Sum Query 2D")
doc.h3("题目在问什么")
doc.p("一个矩阵不会变。会被问很多次: 左上角 <code>(r1, c1)</code> 到右下角 <code>(r2, c2)</code> 的子矩形里所有数的和。")
doc.h3("看例子")
doc.svg(SLUG + "/matrix_examples.svg", "例子。")
doc.h3("Brute force")
doc.p("每次两层循环把子矩形加一遍, 每次 <code>O(m·n)</code>。")
doc.h3("Intuition: 一维的前缀和推广到二维")
doc.p("定义 <code>P[i][j]</code> = 矩阵左上角 i 行 j 列 (也就是第 0..i-1 行、第 0..j-1 列) 所有数的和。")
doc.p("要算一个子矩形, 先拿右下角对应的大矩形 <code>P[r2+1][c2+1]</code>, 减掉上面多出来的一块 <code>P[r1][c2+1]</code>, 再减掉左边多出来的一块 <code>P[r2+1][c1]</code>。"
      "但左上角那一小块被减了两次, 要加回来一次 <code>P[r1][c1]</code>。")
doc.p("建 P 的时候也是同样的道理: 当前格 + 上面 + 左边 - 左上角。")
doc.h3("算法")
nc.steps(doc, "建表: <code>P[i+1][j+1] = matrix[i][j] + P[i][j+1] + P[i+1][j] - P[i][j]</code>。",
         "查询: <code>P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1]</code>。")
doc.svg(SLUG + "/matrix_core.svg", "全部 - 上面 - 左边 + 左上角 = 21 - 4 - 9 + 3 = 11。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/matrix_trace.svg", "逐行建 P, 然后每次查询只读 4 个格子。")
doc.h3("复杂度")
doc.p("建表 <code>O(m·n)</code>, 每次查询 <code>O(1)</code>。Space <code>O(m·n)</code>。")
nc.solution(doc, CODE["matrix"])
doc.note("二维前缀和: 大矩形 - 上面 - 左边 + 左上角。P 比矩阵多一行一列 0。")

# ================================================================ 7
doc.h2("7. Corporate Flight Bookings (difference array)")
doc.h3("题目在问什么")
doc.p("有 n 个航班, 编号 1 到 n。每条 booking <code>[first, last, seats]</code> 表示: 航班 first 到 last, 每一班都订了 seats 个座位。返回每个航班一共订了多少座位。")
doc.h3("看例子")
doc.svg(SLUG + "/diff_examples.svg", "例子。")
doc.p("这题和前面方向相反。前面是\"数组不变, 问很多次区间和\"; 这里是\"<b>很多次给一个区间加一个数</b>, 最后读一次结果\"。")
doc.h3("Brute force")
doc.p("每条 booking, 循环把 first..last 每个位置加 seats。m 条 booking, 每条最多 n 个位置, <code>O(m·n)</code>。")
doc.h3("Intuition: 只记录变化的边界")
doc.p("一条 booking 给 [l, r] 每个位置加 v。换个角度看: 从左往右走, 走到 l 时数值<b>开始</b>多 v, 走过 r 之后又<b>不再</b>多 v。")
doc.p("所以只需要在两个边界做记号: <code>diff[l] += v</code> (从这里开始加), <code>diff[r+1] -= v</code> (从这里开始不加)。最后从左往右做一遍前缀和, 每个位置累计到的值就是答案。")
doc.p("这个 diff 数组叫 <b>difference array</b> (差分数组)。它和前缀和是互逆的: 对 diff 做前缀和, 得到原数组。")
doc.h3("算法")
nc.steps(doc, "<code>diff = [0] * (n + 1)</code>。",
         "每条 booking: <code>diff[first-1] += seats</code>, <code>diff[last] -= seats</code> (编号从 1 开始, 换成下标要减 1)。",
         "对 diff 的前 n 项做前缀和, 就是答案。")
doc.svg(SLUG + "/diff_core.svg", "+v 从 l 开始一直往右带着, 走到 r+1 被 -v 抵消。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/diff_trace.svg", "3 条 booking 各改 2 个格子, 最后一遍前缀和得到 [10, 55, 45, 25, 25]。")
doc.p("Car Pooling 是同一个模板: 乘客上车的位置 +num, 下车的位置 -num, 扫一遍看车上人数有没有超过 capacity。")
doc.h3("复杂度")
doc.p("Time <code>O(m + n)</code>, Space <code>O(n)</code>。")
nc.solution(doc, CODE["flights"])
doc.note("很多次区间 +v, 最后才读: diff[l] += v, diff[r+1] -= v, 最后做一遍前缀和。")

# ================================================================ 8
doc.h2("8. 什么时候用 sliding window, 什么时候用 prefix sum")
doc.p("03 · Sliding Window 和这篇都在处理\"连续 subarray 的和\"。到底用哪个, 只看一件事: <b>数组里有没有负数</b>。")
doc.p("sliding window 成立的前提是: 右边加一个数, 和只会变大; 左边去掉一个数, 和只会变小。这样\"和太大就缩左边\"才是安全的。全是正数时成立, 比如 Minimum Size Subarray Sum。")
doc.p("有负数时这个前提没了: 后面的一个负数可以把和拉回来。下面的例子里, window 在和太大时扔掉了开头的 5, 结果漏掉了以 5 开头的答案:")
doc.svg(SLUG + "/window_core.svg", "全是正数: 前缀和一直上升; 有负数: 前缀和升了又降, window \"缩了就不回来\" 不成立。")
doc.svg(SLUG + "/window_trace.svg", "[5,-2,0], k = 3: window 在和为 5 > 3 时扔掉 5, 漏掉了 [5,-2] 和 [5,-2,0]; 前缀和 + Hash Table 两个都数到了。")
doc.p("前缀和 + Hash Table 不需要这个前提, 因为它不移动边界, 所有起点都留在 dict 里, 随时可以查。代价是空间从 <code>O(1)</code> 变成 <code>O(n)</code>。")
nc.solution(doc, CODE["window_pos"], CODE["window_neg"], summary="代码: 全正数时的 window, 以及有负数时 window 的错误写法")
doc.note("全是正数 → sliding window, O(1) 空间。有负数 → 前缀和 + Hash Table, O(n) 空间。")

# ================================================================ 识别信号
doc.h2("9. 识别信号: 看到什么, 就想到 prefix sum")
nc.table(doc, ["题目特征", "做法", "complexity"], [
    ["数组不变, 反复问区间和", "prefix 数组, prefix[j+1] - prefix[i]", "<code>O(n·q)</code> → <code>O(n + q)</code>"],
    ["\"左边和 = 右边和\" / 找分割点", "total + 边走边加的 left", "<code>O(n²)</code> → <code>O(n)</code>"],
    ["连续 subarray 和等于 k, 数个数, 可能有负数", "前缀和 + Hash Table, 查 count[prefix - k], 初始 {0: 1}", "<code>O(n²)</code> → <code>O(n)</code>"],
    ["和是 k 的倍数", "prefix % k 当 key", "<code>O(n²)</code> → <code>O(n)</code>"],
    ["两种东西一样多", "一种 +1, 一种 -1, 变成和为 0", "<code>O(n²)</code> → <code>O(n)</code>"],
    ["最长的满足条件的 subarray", "dict 存第一次出现的下标", "<code>O(n²)</code> → <code>O(n)</code>"],
    ["除了自己以外的积 / 和", "左边一遍, 右边一遍", "<code>O(n²)</code> → <code>O(n)</code>"],
    ["矩阵子矩形和, 多次查询", "二维前缀和", "每次 <code>O(m·n)</code> → <code>O(1)</code>"],
    ["很多次区间 +v, 最后读结果", "difference array", "<code>O(m·n)</code> → <code>O(m + n)</code>"],
    ["连续 subarray, 全是正数, 求最长 / 最短", "不用前缀和, 用 sliding window", "空间 <code>O(1)</code>"]])

doc.h2("以后再学")
doc.p("有负数、求\"和 ≥ k 的最短 subarray\": 前缀和 + monotonic deque。数组会被修改的区间和: Fenwick tree / segment tree。")
doc.write("docs/04-prefix-sum.html")
