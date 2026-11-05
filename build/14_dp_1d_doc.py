# 14 · DP (1) 正文 (NeetCode 式讲法)。由 14_dp-1d.py 的 build_doc() exec, 共用 CODE。
import bisect
import nclib as nc
from counts import cnt

SL = "14-dp-1d"
EX = os.path.join(d.ROOT, "docs", "svg", SL, "%s_examples.svg")
EXS = SL + "/%s_examples.svg"
ns = {"bisect": bisect, "inf": float("inf")}
for k in ["climb", "rob", "rob2", "kadane", "prod", "stock", "coin", "change", "partition", "wordbreak", "lis", "lis_fast"]:
    exec(CODE[k], ns)

# ---------------------------------------------------------------- 例子图
assert ns["climbStairs"](2) == 2 and ns["climbStairs"](3) == 3
nc.examples_svg(EX % "climb", "Climbing Stairs examples", ["爬 n 级台阶, 每次可以爬 1 级或 2 级。一共有多少种不同的爬法"], [
    dict(title="Example 1:  n = 2  →  2", items=["1+1", "2"], cw=60, index=False, hl=[0, 1]),
    dict(title="Example 2:  n = 3  →  3", items=["1+1+1", "1+2", "2+1"], cw=70, index=False, hl=[0, 1, 2],
         extra=["1+2 和 2+1 是两种不同的爬法 (顺序不同)"])],
    legend=[("new", "每一种爬法")])

assert ns["rob"]([1, 2, 3, 1]) == 4 and ns["rob"]([2, 7, 9, 3, 1]) == 12
nc.examples_svg(EX % "rob", "House Robber examples", ["一排房子, nums[i] 是第 i 间的钱。不能偷相邻的两间 (会触发警报)。最多能偷多少"], [
    dict(title="Example 1:  nums = [1,2,3,1]  →  4", items=[1, 2, 3, 1], hl=[0, 2], ans_text="偷 0 和 2: 1 + 3 = 4"),
    dict(title="Example 2:  nums = [2,7,9,3,1]  →  12", items=[2, 7, 9, 3, 1], hl=[0, 2, 4], ans_text="偷 0, 2, 4: 2 + 9 + 1 = 12",
         bad=[(1, 1, "7 最大, 但偷了 7 就不能偷 2 和 9")])],
    legend=[("new", "偷的房子"), ("rem", "看起来像, 但不对")])

assert ns["rob2"]([2, 3, 2]) == 3 and ns["rob2"]([1, 2, 3, 1]) == 4
nc.examples_svg(EX % "rob2", "House Robber II examples", ["同上, 但房子围成一圈: 第一间和最后一间也算相邻"], [
    dict(title="Example:  nums = [2,3,2]  →  3", items=[2, 3, 2], hl=[1], bad=[(0, 2, "2 + 2 = 4, 但首尾相邻 ✗")],
         ans_text="只能偷 3")],
    legend=[("new", "偷的房子"), ("rem", "不允许")])

assert ns["maxSubArray"]([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
nc.examples_svg(EX % "kadane", "Maximum Subarray examples", ["找一段连续的 subarray (至少一个数), 和最大"], [
    dict(title="Example:  nums = [-2,1,-3,4,-1,2,1,-5,4]  →  6", items=[-2, 1, -3, 4, -1, 2, 1, -5, 4], ans=[(3, 6)],
         ans_text="4 - 1 + 2 + 1 = 6", extra=["中间有 -1 也值得带上, 因为后面的 2 + 1 能补回来"]),
    dict(title="Example 2:  nums = [-3,-1,-2]  →  -1", items=[-3, -1, -2], ans=[(1, 1)], ans_text="全是负数, 选最大的一个")])

assert ns["maxProduct"]([2, 3, -2, 4]) == 6 and ns["maxProduct"]([-2, 3, -4]) == 24
nc.examples_svg(EX % "prod", "Maximum Product Subarray examples", ["找一段连续的 subarray, 乘积最大"], [
    dict(title="Example 1:  nums = [2,3,-2,4]  →  6", items=[2, 3, -2, 4], ans=[(0, 1)], ans_text="2 × 3 = 6"),
    dict(title="Example 2:  nums = [-2,3,-4]  →  24", items=[-2, 3, -4], ans=[(0, 2)], ans_text="(-2) × 3 × (-4) = 24",
         extra=["两个负数相乘变正。所以一个很小的负数, 乘上下一个负数, 可能变成最大的"])])

assert ns["maxProfit"]([7, 1, 5, 3, 6, 4]) == 5 and ns["maxProfit"]([7, 6, 4, 3, 1]) == 0
nc.examples_svg(EX % "stock", "Best Time to Buy and Sell Stock examples", ["prices[i] 是第 i 天的股价。选一天买、之后的某一天卖 (只能交易一次)。最大利润是多少, 赚不到就是 0"], [
    dict(title="Example 1:  prices = [7,1,5,3,6,4]  →  5", items=[7, 1, 5, 3, 6, 4], hl=[1, 4], ans_text="第 1 天买 1, 第 4 天卖 6",
         bad=[(0, 1, "7 - 1 = 6 更大, 但这是先卖后买 ✗")]),
    dict(title="Example 2:  prices = [7,6,4,3,1]  →  0", items=[7, 6, 4, 3, 1], extra=["一直在跌, 不交易"])],
    legend=[("new", "买和卖"), ("rem", "看起来像, 但不对")])

assert ns["coinChange"]([1, 2, 5], 11) == 3 and ns["coinChange"]([2], 3) == -1 and ns["coinChange"]([1, 3, 4], 6) == 2
nc.examples_svg(EX % "coin", "Coin Change examples", ["coins 是硬币面额, 每种无限个。凑出 amount 最少要几枚? 凑不出返回 -1"], [
    dict(title="Example 1:  coins = [1,2,5], amount = 11  →  3", items=[5, 5, 1], hl=[0, 1, 2], index=False, ans_text="5 + 5 + 1"),
    dict(title="Example 2:  coins = [2], amount = 3  →  -1", extra=["只有 2, 凑不出奇数"]),
    dict(title="Example 3:  coins = [1,3,4], amount = 6  →  2", items=[3, 3], hl=[0, 1], index=False, ans_text="3 + 3",
         extra=["如果先拿最大的 4 (贪心), 得到 4 + 1 + 1 = 3 枚, 不是最少"])],
    legend=[("new", "用的硬币")])

assert ns["change"](5, [1, 2, 5]) == 4
nc.examples_svg(EX % "change", "Coin Change II examples", ["coins 每种无限个。凑出 amount 一共有几种<组合> (不看顺序: 1+2 和 2+1 算同一种)"], [
    dict(title="Example:  amount = 5, coins = [1,2,5]  →  4", items=["5", "2+2+1", "2+1+1+1", "1+1+1+1+1"], cw=86,
         index=False, hl=[0, 1, 2, 3], extra=["2+1+2 和 2+2+1 是同一种组合, 只算一次"])],
    legend=[("new", "每一种组合")])

assert ns["canPartition"]([1, 5, 11, 5]) and not ns["canPartition"]([1, 2, 3, 5])
nc.examples_svg(EX % "partition", "Partition Equal Subset Sum examples", ["能不能把数组分成两组, 两组的和相等? (每个数只能放进一组)"], [
    dict(title="Example 1:  nums = [1,5,11,5]  →  True", items=[1, 5, 11, 5], hl=[0, 1, 3], ans_text="[1,5,5] 和 [11], 都是 11"),
    dict(title="Example 2:  nums = [1,2,3,5]  →  False", items=[1, 2, 3, 5],
         extra=["总和 11 是奇数, 不可能分成两个相等的整数"])],
    legend=[("new", "第一组")])

assert ns["wordBreak"]("leetcode", ["leet", "code"]) and not ns["wordBreak"]("catsandog", ["cats", "dog", "sand", "and", "cat"])
nc.examples_svg(EX % "wordbreak", "Word Break examples", ["能不能把 s 切成若干段, 每一段都在字典 wordDict 里? (字典里的词可以重复使用)"], [
    dict(title="Example 1:  s = \"leetcode\", wordDict = [leet, code]  →  True", items=["leet", "code"], cw=60, index=False, hl=[0, 1]),
    dict(title="Example 2:  s = \"applepenapple\", wordDict = [apple, pen]  →  True", items=["apple", "pen", "apple"], cw=60,
         index=False, hl=[0, 1, 2], extra=["apple 用了两次"]),
    dict(title="Example 3:  s = \"catsandog\", wordDict = [cats, dog, sand, and, cat]  →  False",
         extra=["cats + and + og ✗;  cat + sand + og ✗。最后的 og 怎么都切不出来"])],
    legend=[("new", "切出来的段")])

assert ns["lengthOfLIS"]([10, 9, 2, 5, 3, 7, 101, 18]) == 4
nc.examples_svg(EX % "lis", "LIS examples", ["找最长的严格递增 subsequence (子序列: 可以跳着选, 但顺序不能变), 返回长度"], [
    dict(title="Example:  nums = [10,9,2,5,3,7,101,18]  →  4", items=[10, 9, 2, 5, 3, 7, 101, 18], hl=[2, 3, 5, 6],
         ans_text="2, 5, 7, 101", extra=["也可以是 2, 3, 7, 18。注意是子序列, 不要求连续"])],
    legend=[("new", "选中的数")])

# ================================================================ HTML
doc = d.Doc("14 · Dynamic Programming (1): 1D DP / Knapsack")
doc.h2("这篇讲什么")
doc.p("DP (dynamic programming, 动态规划) 用来解决这样的问题: 一个大问题可以拆成<b>几个更小的同类问题</b>, 而且这些小问题会被<b>反复用到</b>。")
doc.p("最直接的写法是 recursion: 大问题调用小问题, 小问题再调用更小的。问题是同一个小问题会被算很多很多遍, 时间是指数级的。DP 的想法很简单: <b>每个小问题只算一次, 把答案存起来, 下次直接用</b>。")
doc.p("所有 DP 题都按同样的四步来想:")
nc.steps(doc, "<b>state</b>: <code>dp[i]</code> 表示什么? (一定要用一句话说清楚)",
         "<b>transition</b>: <code>dp[i]</code> 怎么由更小的 dp 算出来? 通常是想\"最后一步做了什么\"。",
         "<b>base case</b>: 最小的那几个 dp 是多少?",
         "<b>计算顺序</b>: 从小往大填, 保证用到的值都已经算好。")
doc.p("这篇讲 1D DP: state 只需要一个下标 (第 i 个位置、金额 a、容量 c)。需要两个下标的 (两个字符串、grid) 在 15。")
nc.table(doc, ["#", "题目", "考过的公司数", "state 的形状 / 相比上一题多了什么"], [
    ["1", "Climbing Stairs", cnt("Climbing Stairs"), "模板题: 前 i 个"],
    ["2", "House Robber", cnt("House Robber"), "每一步\"选 / 不选\""],
    ["3", "House Robber II", cnt("House Robber II"), "环 = 两次线性"],
    ["4", "Maximum Subarray", cnt("Maximum Subarray"), "新的 state: 以 i 结尾"],
    ["5", "Maximum Product Subarray", cnt("Maximum Product Subarray"), "要同时记最大和最小"],
    ["6", "Best Time to Buy and Sell Stock", cnt("Best Time to Buy and Sell Stock"), "到目前为止的最小值"],
    ["7", "Coin Change", cnt("Coin Change"), "新的 state: 金额 a (unbounded knapsack)"],
    ["8", "Coin Change II", cnt("Coin Change II"), "数组合个数, 循环顺序很关键"],
    ["9", "Partition Equal Subset Sum", cnt("Partition Equal Subset Sum"), "每个数只能用一次 (0/1 knapsack)"],
    ["10", "Word Break", cnt("Word Break"), "前 i 个字符能不能切"],
    ["11", "Longest Increasing Subsequence", cnt("Longest Increasing Subsequence"), "以 i 结尾, 往回看所有 j"]])
doc.p("每道题的顺序: <b>题目在问什么 → 看例子 → brute force → intuition → 算法 → 手动走一遍 → 复杂度</b>。代码放在最后, 默认折叠。")

# ================================================================ 1
doc.h2("1. Climbing Stairs")
doc.h3("题目在问什么")
doc.p("要爬 n 级台阶, 每次可以爬 1 级或者 2 级。问: 爬到顶一共有多少种不同的方法? 顺序不同算不同的方法。")
doc.h3("看例子")
doc.svg(EXS % "climb", "两个例子。")
doc.h3("Brute force: recursion")
doc.p("想\"最后一步\": 到达第 n 级, 最后一步要么是从第 n-1 级爬 1 级上来, 要么是从第 n-2 级爬 2 级上来。所以 <code>ways(n) = ways(n-1) + ways(n-2)</code>。")
doc.p("直接写成 recursion 是对的, 但是很慢。画出 recursion tree 就能看到原因:")
doc.svg(SL + "/first_principles_core.svg", "左: recursion tree 里同一个子问题 (同色) 被算了很多遍。右: 每个子问题只算一次, 按顺序填表。")
doc.p("<code>ways(3)</code> 被算了 2 次, <code>ways(2)</code> 被算了 3 次……n 越大, 重复越多, 时间是 <code>O(2ⁿ)</code>。")
doc.h3("Intuition: 每个子问题只算一次")
doc.p("有两种办法消掉重复:")
nc.bullets(doc, "<b>memoization</b> (top-down): recursion 不变, 只是第一次算完 <code>ways(i)</code> 就存进 dict, 下次直接返回。Python 里加一行 <code>@cache</code>。",
           "<b>tabulation</b> (bottom-up): 不用 recursion, 直接从小到大填一个数组: <code>dp[0], dp[1], dp[2], ...</code>, 每一格只用到前面已经填好的格子。")
doc.p("再进一步: 填 <code>dp[i]</code> 只需要前两格, 更早的格子再也用不到了。所以不需要整个数组, 两个变量滚动就够了, 空间从 <code>O(n)</code> 降到 <code>O(1)</code>。")
doc.p("用四步来说: state <code>dp[i]</code> = 爬到第 i 级的方法数; transition <code>dp[i] = dp[i-1] + dp[i-2]</code>; base case <code>dp[0] = 1, dp[1] = 1</code>; 顺序是 i 从小到大。")
doc.h3("算法")
nc.steps(doc, "<code>a, b = 1, 1</code> (分别是 dp[i-2] 和 dp[i-1])。", "循环 n - 1 次: <code>a, b = b, a + b</code>。", "返回 b。")
doc.svg(SL + "/climb_core.svg", "最后一步只有两种, 直接相加; 只读前两格, 所以两个变量滚动就够。")
doc.h3("手动走一遍")
doc.svg(SL + "/climb_trace.svg", "n = 5: base 两格, 之后每一格 = 前两格相加, 最后 dp[5] = 8。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(1)</code>。")
nc.solution(doc, CODE["brute"], CODE["memo"], CODE["table"], CODE["rolling"], summary="代码: recursion → memo → 表格 → 两个变量, 四个版本对比")
nc.solution(doc, CODE["climb"])
doc.note("DP = recursion + 不重复算。先写出\"最后一步\"的 recursion, 再加 memo 或改成从小到大填表; 只依赖前几格就用变量滚动。")

doc.h2("把第 1 题抽象一下: 怎么想 DP")
doc.p("第 1 题的思路可以用在所有 DP 题上:")
nc.steps(doc, "先写出 brute force 的 recursion, 想清楚\"<b>最后一步有哪几种选择</b>\"。每种选择会留下一个更小的问题。",
         "看 recursion 的参数: 有几个参数在变, dp 就是几维的。这篇都是一个参数。",
         "把 recursion 改成从小到大填表。")
doc.p("state 常见的三种形状: <b>前 i 个</b> (第 1、2、10 题)、<b>以 i 结尾</b> (第 4、5、11 题)、<b>金额 / 容量</b> (第 7、8、9 题)。看到一道新题, 先试这三种。")
doc.note("DP 四步: state (dp[i] 是什么) / transition (最后一步) / base case / 计算顺序。")

# ================================================================ 2
doc.h2("2. House Robber")
doc.h3("题目在问什么")
doc.p("一排房子, <code>nums[i]</code> 是第 i 间里的钱。不能偷<b>相邻</b>的两间 (会触发警报)。问最多能偷多少钱。")
doc.h3("看例子")
doc.svg(EXS % "rob", "两个例子。")
doc.p("Example 2 说明, 每次挑最大的 (贪心) 是不对的。")
doc.h3("Brute force")
doc.p("每间房子偷或不偷, 枚举所有不相邻的组合, <code>O(2ⁿ)</code>。")
doc.h3("Intuition: 最后一间偷不偷")
doc.p("看前 i 间房子 (0 到 i), 只考虑最后一间 i:")
nc.bullets(doc, "<b>不偷</b> i: 那就是前 i-1 间能偷的最多, 也就是 <code>dp[i-1]</code>。",
           "<b>偷</b> i: 那 i-1 就不能偷, 只能加上前 i-2 间的最多: <code>dp[i-2] + nums[i]</code>。")
doc.p("两个里取大的: <code>dp[i] = max(dp[i-1], dp[i-2] + nums[i])</code>。")
doc.p("这就是 DP 里最常见的\"<b>选 / 不选</b>\"结构。又是只依赖前两格, 可以两个变量滚动。")
doc.h3("算法")
nc.steps(doc, "<code>prev2 = prev1 = 0</code>。", "对每个 x: <code>prev2, prev1 = prev1, max(prev1, prev2 + x)</code>。", "返回 prev1。")
doc.svg(SL + "/rob_core.svg", "dp[2] = max(dp[1], dp[0] + nums[2]) = max(3, 2 + 9) = 11: 两个选择覆盖了所有可能。")
doc.h3("手动走一遍")
doc.svg(SL + "/rob_trace.svg", "nums = [2,3,9,3,1]: 每一格的算式都写出来了, 橙色圈是它读取的两格。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(1)</code>。")
nc.solution(doc, CODE["rob"])
doc.note("每个元素\"选 / 不选\", 而且选了会影响邻居: dp[i] = max(不选, 选 + 前面能接上的)。")

# ================================================================ 3
doc.h2("3. House Robber II")
doc.h3("题目在问什么")
doc.p("和第 2 题一样, 但房子<b>围成一圈</b>: 第一间和最后一间也算相邻。")
doc.h3("看例子")
doc.svg(EXS % "rob2", "例子。")
doc.h3("Intuition: 把环拆成两条线")
doc.p("首尾不能同时偷。那就分两种情况: <b>不偷最后一间</b> (只看 nums[0..n-2]), 或者<b>不偷第一间</b> (只看 nums[1..n-1])。每种情况都是一条线, 直接用第 2 题。答案是两者里大的。")
doc.p("只有一间房子时要特判, 直接返回 nums[0]。")
doc.h3("算法")
nc.steps(doc, "n == 1 返回 nums[0]。", "返回 <code>max(rob(nums[:-1]), rob(nums[1:]))</code>。")
doc.svg(SL + "/rob2_core.svg", "把环切成两个线性问题: 红色的是这一轮不偷的那间。")
doc.h3("手动走一遍")
doc.svg(SL + "/rob2_trace.svg", "两次线性 DP: A = 11, B = 10, 答案 11。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(1)</code>。")
nc.solution(doc, CODE["rob2"])
doc.note("环形的问题: 拆成几种线性的情况分别做 (通常是\"不选第一个\"和\"不选最后一个\")。")

# ================================================================ 4
doc.h2("4. Maximum Subarray (Kadane)")
doc.h3("题目在问什么")
doc.p("找一段<b>连续</b>的 subarray (至少包含一个数), 让它的和最大。")
doc.h3("看例子")
doc.svg(EXS % "kadane", "两个例子。")
doc.h3("Brute force")
doc.p("枚举所有 (起点, 终点), 用 prefix sum 算和, <code>O(n²)</code>。")
doc.h3("Intuition: state 换成\"以 i 结尾\"")
doc.p("如果用\"前 i 个数里的最大 subarray\"当 state, 很难写 transition: 不知道最好的那段在哪, 新加的 nums[i] 能不能接上去。")
doc.p("换一个 state: <code>cur[i]</code> = <b>必须以 i 结尾</b>的 subarray 里, 最大的和。这样 transition 就很清楚了。以 i 结尾的 subarray 只有两种:")
nc.bullets(doc, "<b>接在前面</b>: 以 i-1 结尾的最好的那段, 再加上 nums[i]: <code>cur[i-1] + nums[i]</code>。",
           "<b>从 i 重新开始</b>: 只有 nums[i] 自己。")
doc.p("<code>cur[i] = max(cur[i-1] + nums[i], nums[i])</code>。直觉: 前面那段的和如果是负的, 接上它只会拖后腿, 不如重新开始。")
doc.p("最终答案是所有 cur[i] 里最大的, 因为最好的那段总要在某个位置结尾。")
doc.h3("算法")
nc.steps(doc, "<code>cur = best = nums[0]</code>。", "对后面每个 x: <code>cur = max(cur + x, x)</code>, <code>best = max(best, cur)</code>。", "返回 best。")
doc.svg(SL + "/kadane_core.svg", "cur[3]: 接在 cur[2] = -2 后面只有 2, 重新开始是 4, 取 4。")
doc.h3("手动走一遍")
doc.svg(SL + "/kadane_trace.svg", "9 个数的完整过程: cur 每步一格, best 记录出现过的最大值。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(1)</code>。")
nc.solution(doc, CODE["kadane"])
doc.note("连续 subarray 的最值: state 用\"以 i 结尾\", 选择是\"接上前面\"还是\"从这里重新开始\"。答案是所有 i 里最大的。")

# ================================================================ 5
doc.h2("5. Maximum Product Subarray")
doc.h3("题目在问什么")
doc.p("找一段连续的 subarray, 让它的<b>乘积</b>最大。")
doc.h3("看例子")
doc.svg(EXS % "prod", "两个例子。")
doc.h3("Brute force")
doc.p("枚举所有 (起点, 终点), <code>O(n²)</code>。")
doc.h3("Intuition: 负数会把最小的变成最大的")
doc.p("先试试照搬第 4 题: <code>mx[i] = max(mx[i-1] × nums[i], nums[i])</code>。在 Example 2 里会出错: 到 -4 时, 前面最好的是 3, 3 × (-4) = -12, 可是真正的答案是 (-2) × 3 × (-4) = 24。")
doc.p("问题在于, 乘一个负数会让大小颠倒: 前面<b>最小</b>的那个 (-6, 一个很负的数), 乘上 -4 反而变成最大。")
doc.p("所以要<b>同时记住以 i 结尾的最大乘积 mx 和最小乘积 mn</b>。新的 mx 和 mn 都从这三个候选里选: <code>nums[i]</code>、<code>mx × nums[i]</code>、<code>mn × nums[i]</code>。")
doc.h3("算法")
nc.steps(doc, "<code>mx = mn = best = nums[0]</code>。",
         "对后面每个 x: 三个候选 <code>(x, mx·x, mn·x)</code>, <code>mx = max(...)</code>, <code>mn = min(...)</code> (要用更新前的 mx 和 mn)。<code>best = max(best, mx)</code>。")
doc.svg(SL + "/prod_core.svg", "x < 0 时 mx 和 mn 交叉: 旧的 mn 乘上负数变成新的 mx。")
doc.h3("手动走一遍")
doc.svg(SL + "/prod_trace.svg", "每一步写出三个候选, mx 取最大, mn 取最小; 两者都用上一格的旧值算。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(1)</code>。")
nc.solution(doc, CODE["prod"])
doc.note("乘法 / 符号会翻转的问题: 同时记最大和最小两个 state。")

# ================================================================ 6
doc.h2("6. Best Time to Buy and Sell Stock")
doc.h3("题目在问什么")
doc.p("<code>prices[i]</code> 是第 i 天的股价。选某一天买, 之后的某一天卖, 只交易一次。最大利润是多少? 赚不到钱就返回 0。")
doc.h3("看例子")
doc.svg(EXS % "stock", "两个例子。")
doc.h3("Brute force")
doc.p("枚举所有 (买入日, 卖出日), 买入在前。<code>O(n²)</code>。")
doc.h3("Intuition: 固定卖出日, 最好的买入日就是之前的最低价")
doc.p("假设第 i 天卖。要让利润最大, 买入价越低越好, 而且必须在 i 之前。所以最好的买入价就是 <code>prices[0..i-1]</code> 里的<b>最小值</b>。")
doc.p("从左往右扫, 一边走一边记录\"到目前为止的最低价\" lo。每一天算一下\"今天卖能赚多少\" (<code>prices[i] - lo</code>), 取最大值。")
doc.p("也可以看成一个两状态的 DP: 每天结束时, 要么手里有股票 (hold), 要么没有 (cash)。<code>hold = max(hold, -price)</code> (继续拿着, 或者今天买); <code>cash = max(cash, hold + price)</code> (继续空仓, 或者今天卖)。这个写法能推广到可以交易多次、有冷却期、有手续费的变体。")
doc.h3("算法")
nc.steps(doc, "<code>lo = inf</code>, <code>best = 0</code>。", "每个 p: <code>lo = min(lo, p)</code>, <code>best = max(best, p - lo)</code>。")
doc.svg(SL + "/stock_core.svg", "左: 第 4 天卖, 最好的买入就是之前的最低价 1。右: 同一个问题的状态机写法。")
doc.h3("手动走一遍")
doc.svg(SL + "/stock_trace.svg", "lo 和 best 随着 i 推进, 每一步先用到昨天为止的 lo 算今天卖的利润。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(1)</code>。")
nc.solution(doc, CODE["stock"], CODE["stock_sm"])
doc.note("\"之前的某一个\" + \"现在\": 边扫边维护之前的最优 (最小值), 每一步 O(1) 更新答案。股票变体用 hold / cash 状态机。")

# ================================================================ 7
doc.h2("7. Coin Change")
doc.h3("题目在问什么")
doc.p("<code>coins</code> 是几种硬币的面额, 每种都有无限多个。要凑出总金额 <code>amount</code>, 最少要用几枚硬币? 凑不出来返回 -1。")
doc.h3("看例子")
doc.svg(EXS % "coin", "三个例子。")
doc.p("Example 3 说明贪心 (每次拿最大的面额) 不一定对。")
doc.h3("Brute force")
doc.p("recursion: 凑 amount, 最后一枚可以是任何一种硬币 c, 剩下要凑 <code>amount - c</code>。试所有 c, 取最少的。没有 memo 的话, 同一个剩余金额会被算很多次, 指数级。")
doc.h3("Intuition: state 是金额")
doc.p("recursion 里唯一在变的参数是\"还要凑多少钱\", 所以 state 就是金额: <code>dp[a]</code> = 凑出金额 a 最少要几枚。")
doc.p("transition 还是想最后一枚: 最后一枚是 c, 那之前要凑出 a - c, 最少 <code>dp[a - c]</code> 枚。<code>dp[a] = min(dp[a - c] + 1)</code>, 对所有 <code>c ≤ a</code> 取最小。")
doc.p("base case: <code>dp[0] = 0</code> (凑 0 元不用硬币)。其他先设成无穷大, 表示还凑不出。从 a = 1 往上填。")
doc.p("这类\"每种东西可以用无限次, 凑出某个总量\"的问题, 叫 <b>unbounded knapsack</b> (完全背包)。")
doc.h3("算法")
nc.steps(doc, "<code>dp = [0] + [inf] * amount</code>。",
         "a 从 1 到 amount: 对每个 <code>c ≤ a</code>: <code>dp[a] = min(dp[a], dp[a - c] + 1)</code>。",
         "返回 <code>dp[amount]</code>, 如果是 inf 就返回 -1。")
doc.svg(SL + "/coin_core.svg", "左: 贪心先拿 4 会错; 右: dp[6] 试遍 1 / 3 / 4 作为最后一枚, 取最小的 dp[6 - c] + 1。")
doc.h3("手动走一遍")
doc.svg(SL + "/coin_trace.svg", "amount 从 1 填到 6: 每一格读的格子数 = 不超过 a 的硬币种类数。")
doc.h3("复杂度")
doc.p("Time <code>O(amount × 硬币种类)</code>, Space <code>O(amount)</code>。")
nc.solution(doc, CODE["coin"])
doc.note("凑出某个总量, 每种可用无限次, 求最少 / 最多: dp[a] = 最优 (dp[a - c] + 1)。贪心不一定对时就想 DP。")

# ================================================================ 8
doc.h2("8. Coin Change II")
doc.h3("题目在问什么")
doc.p("同样每种硬币无限多个。这次问: 凑出 amount 一共有多少种<b>组合</b>? 组合不看顺序, 1+2 和 2+1 算同一种。")
doc.h3("看例子")
doc.svg(EXS % "change", "例子。")
doc.h3("Brute force")
doc.p("recursion 枚举所有组合。和 13 的 Combination Sum 一样, 用 start index 防止重复。")
doc.h3("Intuition: 外层循环硬币, 内层循环金额")
doc.p("先试试照搬第 7 题: <code>dp[a] = sum(dp[a - c])</code>, 外层循环 a, 内层循环 c。这样算出来的是<b>排列</b>的个数, 1+2 和 2+1 被算成两种: 填 dp[3] 时, \"最后一枚是 2\" 包含了 1+2, \"最后一枚是 1\" 包含了 2+1。")
doc.p("要算组合, 就要规定硬币的使用顺序, 比如\"先决定用几个 1, 再决定用几个 2, ……\"。写成循环就是: <b>外层循环硬币, 内层循环金额</b>。处理硬币 c 的时候, dp 里只包含用前面那些硬币的组合, 所以 2 永远出现在 1 之后, 不会有 2+1 这种顺序。")
doc.p("<code>dp[a]</code> = 用目前处理过的硬币, 凑出 a 的组合数。处理硬币 c 时: <code>dp[a] += dp[a - c]</code>。base case <code>dp[0] = 1</code> (凑 0 元有一种: 什么都不拿)。")
doc.h3("算法")
nc.steps(doc, "<code>dp = [1] + [0] * amount</code>。",
         "对每个 c (外层): a 从 c 到 amount (内层, 正序): <code>dp[a] += dp[a - c]</code>。",
         "返回 <code>dp[amount]</code>。")
doc.svg(SL + "/change_core.svg", "coins = [1, 2], amount = 3: 外层循环金额会数出 3 种 (含 1+2 和 2+1), 外层循环硬币数出 2 种。")
doc.h3("手动走一遍")
doc.svg(SL + "/change_trace.svg", "每一行是处理完一种硬币后的 dp 数组; 以 dp[5] 为例写出了算式。")
doc.h3("复杂度")
doc.p("Time <code>O(amount × 硬币种类)</code>, Space <code>O(amount)</code>。")
nc.solution(doc, CODE["change"])
doc.note("数组合 (不看顺序): 外层循环物品, 内层循环金额。数排列 (看顺序): 外层金额, 内层物品。")

# ================================================================ 9
doc.h2("9. Partition Equal Subset Sum")
doc.h3("题目在问什么")
doc.p("给一个正整数数组。能不能把它分成两组, 让两组的和相等? 每个数只能放进其中一组。")
doc.h3("看例子")
doc.svg(EXS % "partition", "两个例子。")
doc.h3("Brute force")
doc.p("每个数放第一组或第二组, <code>O(2ⁿ)</code>。")
doc.h3("Intuition: 变成\"能不能凑出 total / 2\"")
doc.p("两组的和相等, 每组都是 <code>total / 2</code>。所以问题等价于: <b>能不能从数组里选一些数, 和正好是 target = total / 2?</b> (total 是奇数就直接 False。)")
doc.p("这和第 7、8 题很像, 区别是<b>每个数只能用一次</b>。这叫 <b>0/1 knapsack</b>。")
doc.p("<code>dp[c]</code> = 用目前处理过的数, 能不能凑出 c。处理数 x 时: <code>dp[c] = dp[c] or dp[c - x]</code> (不用 x, 或者用 x)。")
doc.p("关键细节: 内层循环 c 要<b>从大到小</b>。为什么? 如果从小到大, 算 dp[c] 时读的 dp[c - x] 可能已经是这一轮刚更新过的, 也就是\"已经用过 x 了\", 再用一次就成了同一个数用两次。从大到小的话, dp[c - x] 一定还是上一轮的值 (没用 x)。")
doc.p("对比第 8 题: 那里每种硬币可以用无限次, 所以正好要从小到大 (允许重复用)。")
doc.h3("算法")
nc.steps(doc, "total 是奇数返回 False。<code>target = total // 2</code>, <code>dp = [True] + [False] * target</code>。",
         "对每个 x: c 从 target <b>倒着</b>到 x: <code>dp[c] = dp[c] or dp[c - x]</code>。",
         "返回 <code>dp[target]</code>。")
doc.svg(SL + "/partition_core.svg", "nums = [2], target = 4: 正序会把同一个 2 用两次 (dp[4] 错成 True); 倒序读到的都是旧值。")
doc.h3("手动走一遍")
doc.svg(SL + "/partition_trace.svg", "nums = [1,2,3,4], target = 5: 每个 x 倒着扫 c, 新变成 True 的格子都写出了依据。")
doc.h3("复杂度")
doc.p("Time <code>O(n × target)</code>, Space <code>O(target)</code>。")
nc.solution(doc, CODE["partition"])
doc.note("每个物品只能用一次 (0/1 knapsack): 一维 dp 时容量要倒序遍历。能用无限次 (unbounded): 正序。")

# ================================================================ 10
doc.h2("10. Word Break")
doc.h3("题目在问什么")
doc.p("给一个字符串 s 和一个字典 wordDict。能不能把 s 切成若干段, 每一段都是字典里的词? 字典里的词可以重复使用。")
doc.h3("看例子")
doc.svg(EXS % "wordbreak", "三个例子。")
doc.h3("Brute force")
doc.p("recursion: 试所有可能的第一段 (是字典里的词), 对剩下的部分递归。没有 memo 时, 同一个后缀会被反复检查, 最坏指数级。")
doc.h3("Intuition: dp[i] = 前 i 个字符能不能切")
doc.p("state: <code>dp[i]</code> = <code>s[:i]</code> (前 i 个字符) 能不能被完整地切分。")
doc.p("transition 想最后一段: 如果最后一段是 <code>s[j:i]</code>, 那它必须在字典里, 并且前面的 <code>s[:j]</code> 也必须能切, 也就是 <code>dp[j]</code> 为 True。试所有 j, 有一个满足就行。")
doc.p("base case: <code>dp[0] = True</code> (空字符串什么都不用切)。")
doc.h3("算法")
nc.steps(doc, "<code>words = set(wordDict)</code>, <code>dp = [True] + [False] * n</code>。",
         "i 从 1 到 n: 对每个 j < i: 如果 <code>dp[j]</code> 并且 <code>s[j:i] in words</code>, <code>dp[i] = True</code>, break。",
         "返回 <code>dp[n]</code>。")
doc.svg(SL + "/wordbreak_core.svg", "dp[7]: 最后一段是 \"and\" 配 dp[4], 或者最后一段是 \"sand\" 配 dp[3]; 有一个成立就是 True。")
doc.h3("手动走一遍")
doc.svg(SL + "/wordbreak_trace.svg", "i 从 1 到 7: 只试 dp[j] 为 True 的 j, 看切出来的最后一段在不在字典里。")
doc.h3("复杂度")
doc.p("Time <code>O(n² · L)</code> (切字符串和查表要 <code>O(L)</code>), 可以只试长度不超过最长单词的 j 来加速。Space <code>O(n)</code>。")
nc.solution(doc, CODE["wordbreak"])
doc.note("字符串能不能切成合法的段: dp[i] = 前 i 个能不能切, 试最后一段 s[j:i]。")

# ================================================================ 11
doc.h2("11. Longest Increasing Subsequence")
doc.h3("题目在问什么")
doc.p("找最长的<b>严格递增 subsequence</b> 的长度。subsequence (子序列) 可以跳着选元素, 但不能改变它们的先后顺序。")
doc.h3("看例子")
doc.svg(EXS % "lis", "例子。")
doc.h3("Brute force")
doc.p("枚举所有子序列 (每个元素选或不选), 检查是否递增。<code>O(2ⁿ · n)</code>。")
doc.h3("Intuition: 以 i 结尾, 往回看所有能接上的 j")
doc.p("和第 4 题一样, 用\"以 i 结尾\"当 state: <code>dp[i]</code> = 以 nums[i] 结尾的最长递增子序列的长度。")
doc.p("以 nums[i] 结尾的递增子序列, 它前一个元素可以是 i 前面<b>任何一个比 nums[i] 小</b>的 nums[j]。接在它后面, 长度是 <code>dp[j] + 1</code>。所以 <code>dp[i] = 1 + max(dp[j])</code>, 对所有 <code>j < i</code> 且 <code>nums[j] < nums[i]</code>。没有这样的 j 就是 1。")
doc.p("和第 4 题的区别: Kadane 只看前一个 (因为要连续), 这里要看前面<b>所有</b>的 j (因为可以跳着选), 所以是 <code>O(n²)</code>。")
doc.p("答案是所有 dp[i] 里最大的。")
doc.h3("算法")
nc.steps(doc, "<code>dp = [1] * n</code>。",
         "i 从 0 到 n-1, j 从 0 到 i-1: 如果 <code>nums[j] < nums[i]</code>, <code>dp[i] = max(dp[i], dp[j] + 1)</code>。",
         "返回 <code>max(dp)</code>。")
doc.svg(SL + "/lis_core.svg", "dp[5]: nums[2..4] 都比 7 小, 它们的 dp 是 1, 2, 2, 取 2, 加 1 = 3。")
doc.h3("手动走一遍")
doc.svg(SL + "/lis_trace.svg", "8 个元素逐个算 dp: 橙色圈是满足 nums[j] < nums[i] 的 dp[j], 箭头指向取到最大值的那个。")
doc.h3("复杂度")
doc.p("Time <code>O(n²)</code>, Space <code>O(n)</code>。另有 <code>O(n log n)</code> 的做法 (维护一个 tails 数组 + 二分), 代码里附上了, 面试能说出 O(n²) 的 DP 一般就够了。")
nc.solution(doc, CODE["lis"], CODE["lis_fast"])
doc.note("子序列 (可以跳着选) 的最优: 以 i 结尾, 往回看所有能接上的 j, O(n²)。")

# ================================================================ 识别信号
doc.h2("12. 识别信号: 看到什么, 就想到 DP")
nc.table(doc, ["题目特征", "state", "transition"], [
    ["\"有多少种方法\" 走到第 n 步", "dp[i] = 到 i 的方法数", "dp[i-1] + dp[i-2] (最后一步的几种选择)"],
    ["每个元素选或不选, 选了影响邻居", "dp[i] = 前 i 个的最优", "max(dp[i-1], dp[i-2] + x)"],
    ["环形", "拆成两条线", "两次线性 DP"],
    ["连续 subarray 的最大和 / 积", "以 i 结尾", "接上前面, 或重新开始; 乘法要同时记 max 和 min"],
    ["买卖股票", "到目前的最小值, 或 hold / cash", "每天更新"],
    ["凑总量, 无限次使用, 求最少", "dp[a] = 凑出 a 的最少个数", "min(dp[a - c] + 1)"],
    ["凑总量, 求组合个数", "dp[a]", "外层物品, 内层金额 (正序)"],
    ["每个物品只能用一次, 能不能凑出", "dp[c]", "容量倒序: dp[c] or dp[c - x]"],
    ["字符串能不能切成合法的段", "dp[i] = 前 i 个", "试最后一段 s[j:i]"],
    ["最长递增子序列 (可以跳着选)", "以 i 结尾", "往回看所有 j < i"]])
doc.p("什么时候想到 DP: 题目问<b>最多 / 最少 / 有多少种 / 能不能</b>, 而 brute force 的 recursion 里有<b>重复的子问题</b>。如果题目要的是\"列出所有方案\", 那是 backtracking (13), 不是 DP。")
doc.p("贪心看起来可以但不确定时, 找一个反例 (比如 Coin Change 的 [1,3,4], amount = 6), 贪心错了就用 DP。")

doc.h2("以后再学")
doc.p("股票系列的其他变体 (多次交易、冷却期、手续费, 都用 hold / cash 状态机)、Decode Ways、Perfect Squares、Jump Game 的 DP 写法、LIS 的 O(n log n) patience sorting。")
doc.write("docs/14-dp-1d.html")
