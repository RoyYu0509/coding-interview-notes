# 07 · Monotonic Stack / Queue 正文 (NeetCode 式讲法)。由 07_monotonic-stack.py exec。
import nclib as nc
from counts import cnt

SV = "07-monotonic-stack/"
EX = os.path.join(d.ROOT, "docs", "svg", "07-monotonic-stack", "%s_examples.svg")
ns = {}
for _s in SNIPPETS:
    exec(_s, ns)

# ---------------------------------------------------------------- 例子图
assert ns["daily_temperatures"]([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
nc.examples_svg(EX % "daily_temperatures", "Daily Temperatures examples",
                ["temperatures[i] 是第 i 天的温度。对每一天, 要等几天才会遇到更暖和的一天? 一直没有就填 0"], [
    dict(title="Example:  [73,74,75,71,69,72,76,73]  →  [1,1,4,2,1,1,0,0]", index=True, rows=[
        ("温度", [73, 74, 75, 71, 69, 72, 76, 73], ["keep", "keep", "new", "keep", "keep", "keep", "rem", "keep"]),
        ("答案", [1, 1, 4, 2, 1, 1, 0, 0], ["keep", "keep", "new", "keep", "keep", "keep", "rem", "keep"])],
         extra=["第 2 天 75 度: 往后 71、69、72 都更冷, 第 6 天 76 才更暖 → 等 6 - 2 = 4 天",
                "第 6 天 76 度: 后面没有更暖的 → 0"])],
    legend=[("new", "例: 第 2 天"), ("rem", "例: 第 6 天")])

assert ns["next_greater_elements"]([1, 2, 1]) == [2, -1, 2]
assert ns["next_greater_elements"]([1, 2, 3, 4, 3]) == [2, 3, 4, -1, 4]
nc.examples_svg(EX % "next_greater_ii", "Next Greater Element II examples",
                ["数组是循环的: 最后一个元素的下一个是第一个。对每个元素, 找它往后 (可以绕回开头) 第一个更大的数, 没有就是 -1"], [
    dict(title="Example 1:  [1,2,1]  →  [2,-1,2]", items=[1, 2, 1], hl=[2],
         extra=["最后一个 1: 往后绕回开头, 先遇到 1 (不大), 再遇到 2 → 2", "2 绕一整圈都没有更大的 → -1"]),
    dict(title="Example 2:  [1,2,3,4,3]  →  [2,3,4,-1,4]", items=[1, 2, 3, 4, 3], hl=[4],
         extra=["最后一个 3 绕回开头: 1、2 都不大, 3 也不大, 4 更大 → 4"])],
    legend=[("new", "需要绕回开头的元素")])

assert ns["largest_rectangle_area"]([2, 1, 5, 6, 2, 3]) == 10
nc.examples_svg(EX % "largest_rectangle", "Largest Rectangle in Histogram examples",
                ["heights 是一排宽度为 1 的柱子。在柱子里面画一个矩形 (必须完全在柱子内), 求最大面积"], [
    dict(title="Example 1:  heights = [2,1,5,6,2,3]  →  10", items=[2, 1, 5, 6, 2, 3], ans=[(2, 3)],
         ans_text="高 5, 宽 2 (index 2..3) → 10",
         bad=[(0, 5, "整排: 最矮是 1, 高 1 × 宽 6 = 6")],
         extra=["一个矩形的高, 一定等于它覆盖的柱子里最矮的那根。index 2..3 最矮是 5"]),
    dict(title="Example 2:  heights = [2,4]  →  4", items=[2, 4], ans=[(1, 1)], ans_text="高 4 宽 1 = 4 (高 2 宽 2 也是 4)")])

assert ns["remove_k_digits"]("1432219", 3) == "1219" and ns["remove_k_digits"]("10200", 1) == "200"
assert ns["remove_k_digits"]("10", 2) == "0"
nc.examples_svg(EX % "remove_k_digits", "Remove K Digits examples",
                ["num 是一个用字符串表示的非负整数。删掉其中 k 位数字 (剩下的顺序不变), 让结果最小。去掉开头的 0"], [
    dict(title="Example 1:  num = \"1432219\", k = 3  →  \"1219\"", items=list("1432219"),
         bad=[(1, 3, "删掉 4, 3, 2")], extra=["剩下 1, 2, 1, 9 → \"1219\""]),
    dict(title="Example 2:  num = \"10200\", k = 1  →  \"200\"", items=list("10200"), bad=[(0, 0, "删掉 1")],
         extra=["剩下 \"0200\", 去掉开头的 0 → \"200\""]),
    dict(title="Example 3:  num = \"10\", k = 2  →  \"0\"", extra=["全删光了, 返回 \"0\""])],
    legend=[("rem", "删掉的数字")])

assert ns["max_sliding_window"]([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
nc.examples_svg(EX % "sliding_window_max", "Sliding Window Maximum examples",
                ["一个长度为 k 的窗口从左往右滑, 每次移动一格。输出每个位置的窗口里的最大值"], [
    dict(title="Example:  nums = [1,3,-1,-3,5,3,6,7], k = 3  →  [3,3,5,5,6,7]", index=False, rows=[
        ("窗口 1", [1, 3, -1, -3, 5, 3, 6, 7], ["new", "new", "new"] + ["keep"] * 5),
        ("窗口 2", [1, 3, -1, -3, 5, 3, 6, 7], ["keep", "new", "new", "new"] + ["keep"] * 4),
        ("窗口 3", [1, 3, -1, -3, 5, 3, 6, 7], ["keep", "keep", "new", "new", "new"] + ["keep"] * 3)],
         extra=["窗口 1 = [1,3,-1] 最大 3;  窗口 2 = [3,-1,-3] 最大 3;  窗口 3 = [-1,-3,5] 最大 5;  ... 一共 n - k + 1 = 6 个窗口"])],
    legend=[("new", "当前窗口")])

# ================================================================ HTML
doc = d.Doc("07 · Monotonic Stack / Queue")
doc.h2("这篇讲什么")
doc.p("这一类题都在问同一件事的变形: <b>对每个元素, 找它右边 (或左边) 第一个比它大 (或小) 的元素</b>。比如\"要等几天才会更暖\"、\"这根柱子往左右能延伸多远\"。")
doc.p("brute force 是每个元素都往右扫, 直到找到更大的, <code>O(n²)</code>。")
doc.p("<b>Monotonic stack</b> (单调栈) 是一个特殊的 stack (见 06): 栈里的元素从底到顶<b>保持单调</b> (比如一直递减)。新元素来的时候, 把栈顶比它小的全部 pop 掉。"
      "神奇的地方在于: <b>被 pop 的那一刻, 正好就是它找到答案的那一刻</b>。每个元素只进出一次, 所以是 <code>O(n)</code>。")
doc.p("如果窗口会滑动 (旧元素会过期), 就把 stack 换成两头都能 pop 的 deque, 叫 monotonic queue。")
nc.table(doc, ["#", "题目", "考过的公司数", "相比上一题多了什么"], [
    ["1", "Daily Temperatures", cnt("Daily Temperatures"), "模板题: 右边第一个更大的"],
    ["2", "Next Greater Element II", cnt("Next Greater Element II"), "数组变成循环的"],
    ["3", "Largest Rectangle in Histogram", cnt("Largest Rectangle in Histogram"), "pop 时同时得到左右两个边界"],
    ["4", "Remove K Digits", cnt("Remove K Digits"), "栈本身就是答案 (greedy)"],
    ["5", "Sliding Window Maximum", cnt("Sliding Window Maximum"), "窗口会过期, 换成 deque"]])
doc.p("每道题的顺序: <b>题目在问什么 → 看例子 → brute force → intuition → 算法 → 手动走一遍 → 复杂度</b>。代码放在最后, 默认折叠。")
doc.p("前置知识: 06 · Stack。")

# ================================================================ 1
doc.h2("1. Daily Temperatures")
doc.h3("题目在问什么")
doc.p("<code>temperatures[i]</code> 是第 i 天的温度。对每一天, 问: 要再等几天, 才会遇到一个<b>更暖和</b>的天? 如果之后都没有更暖的, 填 0。")
doc.p("换句话说: 对每个元素, 找它<b>右边第一个比它大的</b>元素, 返回下标之差。")
doc.h3("看例子")
doc.svg(SV + "daily_temperatures_examples.svg", "例子。")
doc.h3("Brute force")
doc.p("每一天 i, 从 i+1 开始往右扫, 遇到第一个更暖的就停。最坏 (温度一直下降) 每天都扫到最后, <code>O(n²)</code>。")
doc.svg(SV + "first_principles_core.svg", "左: brute force 每个 i 都重新往右扫。右: 一个大的数来了, 栈里等答案的数一次性全部结算, 每个数只进出一次。")
doc.p("浪费在哪: 看温度 <code>75, 71, 69, 72</code>。brute force 里, 71 往右扫看到 69、72; 69 往右扫又看到 72。72 被反复看了好几次。")
doc.h3("Intuition: 让\"还在等答案\"的天排队, 来了一个暖的就一起结算")
doc.p("换个方向想: 不是每一天去找答案, 而是每来一个新的温度, 看看它<b>能当谁的答案</b>。")
nc.steps(doc, "从左往右扫。还没找到更暖的那些天, 先放进一个 stack 里\"等着\"。",
         "来了新的一天 x。栈顶的那一天如果比 x 冷, 那 x 就是它等的那个更暖的天! 结算它的答案, pop 掉。",
         "继续看新的栈顶, 只要比 x 冷就一直 pop、一直结算。直到栈顶比 x 暖 (或者栈空了)。",
         "最后把 x 自己 push 进去, 它也要开始等。")
doc.p("这样栈里的温度从底到顶一定是<b>递减</b>的 (比 x 冷的都被 pop 了, x 才放上去)。所以叫 monotonic stack。")
doc.p("为什么被 pop 的元素可以扔掉? 因为它已经找到答案了, 以后再也用不到。每个元素最多 push 一次、pop 一次, 总共 <code>O(n)</code>。")
doc.p("一个细节: 答案要的是\"等几天\", 所以栈里存<b>下标</b>, 不存温度。温度用 <code>temperatures[下标]</code> 去查。")
doc.h3("算法")
nc.steps(doc, "<code>ans = [0] * n</code>, <code>stack = []</code> (存下标)。",
         "i 从 0 到 n-1: 当栈不空且 <code>T[stack[-1]] < T[i]</code>: <code>j = stack.pop()</code>, <code>ans[j] = i - j</code>。",
         "<code>stack.append(i)</code>。",
         "最后还在栈里的, 答案保持 0。")
doc.svg(SV + "daily_temperatures_core.svg", "i = 5 (72 度) 来了: 栈里 69、71 都比 72 冷, pop 并结算; 75 不比 72 冷, 停。")
doc.h3("手动走一遍")
doc.svg(SV + "daily_temperatures_trace.svg", "8 天的完整运行。i = 5 一次 pop 两个, i = 6 一次 pop 两个; 每次 pop 都确定了一个答案。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>: 每个下标最多 push 一次、pop 一次。Space <code>O(n)</code>。")
nc.solution(doc, S_DT, S_BRUTE, S_TEMPLATE)
doc.note("找右边第一个更大的: 维护递减栈 (存下标)。新元素比栈顶大就 pop, pop 的那一刻就是栈顶找到答案的时候。")

doc.h2("把第 1 题抽象一下: 递增栈还是递减栈")
doc.p("第 1 题的规律可以总结成两句:")
nc.bullets(doc, "<b>找更大的 → 维护递减栈</b> (来了一个大的, 就把比它小的 pop 掉)。<b>找更小的 → 维护递增栈</b>。",
           "<b>右边</b>的答案在 pop 的时候拿到 (pop 它的那个新元素就是答案)。<b>左边</b>的答案在 pop 完之后看栈顶 (新元素 push 之前, 栈顶就是它左边第一个更大 / 更小的)。")
doc.p("所以一次扫描可以同时拿到左右两边的答案, 第 3 题就要用到这一点。")
nc.solution(doc, S_BOTH, summary="代码: 一次扫描同时得到左边、右边第一个更小的")
doc.note("找更大用递减栈, 找更小用递增栈。右边的答案 pop 时拿, 左边的答案 push 前看栈顶。")

# ================================================================ 2
doc.h2("2. Next Greater Element II")
doc.h3("题目在问什么")
doc.p("和第 1 题一样找\"右边第一个更大的数\", 但数组是<b>循环</b>的: 最后一个元素后面接着第一个元素。没有更大的返回 -1。这题返回的是那个数的值, 不是距离。")
doc.h3("看例子")
doc.svg(SV + "next_greater_ii_examples.svg", "两个例子。")
doc.h3("Brute force")
doc.p("每个元素往后走 n-1 步 (用 <code>% n</code> 绕回开头), 找第一个更大的。<code>O(n²)</code>。")
doc.h3("Intuition: 把数组走两遍")
doc.p("循环数组的常用技巧: 想象把数组复制一份接在后面, <code>[1,2,1]</code> 变成 <code>[1,2,1,1,2,1]</code>。在这个两倍长的数组上做第 1 题, 前 n 个元素的答案就是循环数组的答案。")
doc.p("不用真的复制: 循环 i 从 0 到 2n-1, 用 <code>nums[i % n]</code> 取值。第二圈的元素只负责\"给别人当答案\"(pop 别人), 不需要 push 自己, 因为它们的答案在第一圈已经处理过了。")
doc.h3("算法")
nc.steps(doc, "<code>ans = [-1] * n</code>。i 从 0 到 2n-1, <code>x = nums[i % n]</code>。",
         "当栈不空且 <code>nums[stack[-1]] < x</code>: <code>ans[stack.pop()] = x</code>。",
         "如果 <code>i < n</code>, push i。")
doc.svg(SV + "next_greater_ii_core.svg", "拼成两份之后, index 2 (值 1) 在第二圈遇到了 2; index 1 (值 3) 绕一圈都没有更大的。")
doc.h3("手动走一遍")
doc.svg(SV + "next_greater_ii_trace.svg", "6 步 (2n)。第二圈 (i = 3, 4, 5) 不 push, 只结算: i = 3 把 1 pop 掉, 得到 ans[2] = 2。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(n)</code>。")
nc.solution(doc, S_NGE2)
doc.note("循环数组: 循环 2n 次, 用 i % n 取值; 第二圈只 pop 不 push。")

# ================================================================ 3
doc.h2("3. Largest Rectangle in Histogram")
doc.h3("题目在问什么")
doc.p("<code>heights</code> 是一排相邻的柱子, 每根宽 1。在这些柱子里面画一个矩形 (矩形不能超出柱子), 求最大面积。")
doc.h3("看例子")
doc.svg(SV + "largest_rectangle_examples.svg", "两个例子。")
doc.p("关键观察: 一个矩形的高, 一定等于它覆盖的那些柱子里<b>最矮</b>的那根。")
doc.h3("Brute force")
doc.p("枚举所有区间 [l, r], 找区间里最矮的柱子 h, 面积 = h × (r - l + 1)。<code>O(n²)</code> 个区间 (边扩边维护最小值)。")
doc.h3("Intuition: 以每根柱子为\"最矮\", 它能延伸多宽?")
doc.p("换个枚举方式: 对每根柱子 i, 假设矩形的高就是 <code>heights[i]</code>。那么矩形可以往左右延伸, 直到碰到一根<b>比它矮</b>的柱子为止。")
doc.p("所以要知道: i 的<b>左边第一个比它矮的</b>在哪 (L), <b>右边第一个比它矮的</b>在哪 (R)。宽度 = <code>R - L - 1</code>, 面积 = <code>heights[i] × (R - L - 1)</code>。")
doc.p("\"左右第一个更小的\" 正是上一节说的: 维护<b>递增栈</b>, 一次扫描同时拿到两边:")
nc.bullets(doc, "新柱子 i 比栈顶矮时, pop 栈顶 top。i 就是 top 右边第一个比它矮的 (R = i)。",
           "pop 之后的新栈顶, 就是 top 左边第一个比它矮的 (L = 新栈顶)。栈空了就是 L = -1。",
           "所以 pop 的那一刻, top 的面积就能算出来了。")
doc.p("最后在 heights 末尾加一根高度 0 的柱子 (哨兵)。它比所有柱子都矮, 会把栈里剩下的全部 pop 出来结算。")
doc.h3("算法")
nc.steps(doc, "<code>heights.append(0)</code>, <code>stack = []</code>, <code>best = 0</code>。",
         "i 从 0 到 n: 当栈不空且 <code>heights[stack[-1]] > heights[i]</code>: <code>h = heights[stack.pop()]</code>; <code>L = stack[-1] if stack else -1</code>; <code>best = max(best, h × (i - L - 1))</code>。",
         "push i。")
doc.svg(SV + "largest_rectangle_core.svg", "高 5 的柱子在 i = 4 被 pop: 右边界 = 4, 左边界 = 新栈顶 index 1, 宽 = 4 - 1 - 1 = 2, 面积 10。")
doc.h3("手动走一遍")
doc.svg(SV + "largest_rectangle_trace.svg", "heights + [0] 共 7 步。每次 pop 都写出宽度和面积, 最后一步哨兵 0 把栈清空。")
doc.p("变体 Maximal Rectangle (0/1 矩阵里最大的全 1 矩形): 一行一行往下, 把每一列\"连续的 1 有多高\"当成柱子, 每一行都做一次这道题。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(n)</code>。")
nc.solution(doc, S_LRH, S_MAXRECT)
doc.note("以每个元素为最小值能延伸多远: 递增栈, pop 时右边界 = 当前 i, 左边界 = 新栈顶。末尾加哨兵 0。")

# ================================================================ 4
doc.h2("4. Remove K Digits")
doc.h3("题目在问什么")
doc.p("<code>num</code> 是一个用字符串表示的非负整数。从中删掉 k 位数字, 剩下的数字<b>保持原来的顺序</b>, 让得到的数最小。结果去掉开头的 0, 全删光就返回 \"0\"。")
doc.h3("看例子")
doc.svg(SV + "remove_k_digits_examples.svg", "三个例子。")
doc.h3("Brute force")
doc.p("枚举所有删法 (从 n 位里选 k 位删), 比较大小。组合数 <code>C(n, k)</code>, 指数级。")
doc.p("稍好一点的 greedy: 每次删一位, 试所有位置, 选结果最小的, 重复 k 次。<code>O(n·k)</code>。")
doc.h3("Intuition: 高位越小越好")
doc.p("剩下的位数是固定的 (n - k 位), 所以比较大小就是从最高位开始比。要让结果最小, <b>高位要尽量小</b>。")
doc.p("看 \"1432\" 删 1 位: 从左往右, 第一个\"比它后面那位大\"的数字是 4 (4 > 3)。删掉它, 3 就补到了它的位置, 高位变小了。删 4 得到 132, 是最小的。")
doc.p("推广: 从左往右扫, 维护一个<b>递增栈</b>。新数字 d 比栈顶小, 而且还有删除额度 (k > 0), 就 pop 栈顶 (删掉它), k 减 1。然后 push d。")
doc.p("这次栈里留下的东西<b>就是答案</b>, 不是用来查别人的。扫完之后 k 还没用完, 就从末尾删 (此时栈是递增的, 末尾最大)。")
doc.h3("算法")
nc.steps(doc, "对每个数字 d: 当 <code>k > 0</code> 且栈顶 > d: pop, k 减 1。然后 push d。",
         "如果 k 还有剩, 删掉栈末尾的 k 个。",
         "拼起来, 去掉开头的 0; 空了返回 \"0\"。")
doc.svg(SV + "remove_k_digits_core.svg", "位数一样时先比高位。\"1432\" 删掉 4 得到 132 最小: 从左往右第一个比后一位大的数字 (4 > 3), 删掉最划算。")
doc.h3("手动走一遍")
doc.svg(SV + "remove_k_digits_trace.svg", "\"1432219\", k = 3: d = 3、2、1 各 pop 一个比它大的前一位 (共 3 次, k 从 3 到 0); 之后 d = 9 直接 push。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(n)</code>。")
nc.solution(doc, S_RKD)
doc.note("删 / 选 k 个让结果的字典序最小 (顺序不能变): greedy + 递增栈, 栈就是答案, pop 次数受 k 限制。")

# ================================================================ 5
doc.h2("5. Sliding Window Maximum")
doc.h3("题目在问什么")
doc.p("一个长度为 k 的窗口从数组最左边开始, 每次往右滑一格。输出每个位置上窗口里的最大值。一共 <code>n - k + 1</code> 个答案。")
doc.h3("看例子")
doc.svg(SV + "sliding_window_max_examples.svg", "例子: 前三个窗口。")
doc.h3("Brute force")
doc.p("每个窗口都扫一遍求 max, <code>O(n·k)</code>。浪费: 相邻两个窗口有 k - 1 个元素是一样的, 却重新比较。")
doc.p("用 heap (见 09) 可以做到 <code>O(n log n)</code>, 但要处理\"堆顶已经滑出窗口\"的情况。")
doc.h3("Intuition: 又小又早过期的元素, 永远不会是最大值")
doc.p("看窗口里的两个元素 a 和 b, a 在 b 的左边, 而且 a ≤ b。那么从现在开始, 只要 a 还在窗口里, b 也一定在 (b 更晚离开), 而 b 更大。所以 <b>a 永远不可能是最大值</b>, 可以直接扔掉。")
doc.p("于是维护一个队列, 只保留\"有可能成为最大值\"的元素。扔掉之后, 剩下的从队头到队尾一定是<b>递减</b>的, 队头就是当前窗口的最大值。")
doc.p("和前面的 stack 不同, 这里元素会从两头离开:")
nc.bullets(doc, "<b>队尾</b>: 新元素 x 来了, 队尾比 x 小 (或相等) 的都 pop 掉 (它们又小又早过期)。这和 monotonic stack 一样。",
           "<b>队头</b>: 队头的下标如果已经滑出窗口了, 也要 pop 掉。这是 stack 做不到的, 所以用 <code>deque</code>。")
doc.h3("算法")
nc.steps(doc, "<code>dq = deque()</code> (存下标)。",
         "i 从 0 到 n-1: 如果 <code>dq[0] <= i - k</code> (队头过期), popleft。",
         "当 dq 不空且 <code>nums[dq[-1]] <= nums[i]</code>: pop。然后 append i。",
         "如果 <code>i >= k - 1</code> (窗口满了), 输出 <code>nums[dq[0]]</code>。")
doc.svg(SV + "sliding_window_max_core.svg", "i = 4, x = 5 来了: index 1 滑出窗口 (队头过期); -1、-3 又小又早过期 (被 5 压住), 都不可能再是最大值。")
doc.h3("手动走一遍")
doc.svg(SV + "sliding_window_max_trace.svg", "k = 3, 8 步。i = 4 一次出队 3 个 (队头过期 1 个 + 队尾 2 个); 从 i = 2 开始每步输出 nums[队头]。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>: 每个下标最多进出 deque 一次。Space <code>O(k)</code>。")
nc.solution(doc, S_SWM)
doc.note("固定长度窗口的最大 / 最小值: monotonic deque。队尾 pop 掉比新元素小的, 队头 pop 掉过期的, 队头就是答案。")

# ================================================================ 识别信号
doc.h2("6. 识别信号: 看到什么, 就想到 monotonic stack / queue")
nc.table(doc, ["题目特征", "做法", "complexity"], [
    ["每个元素找右边 / 左边<b>第一个更大 / 更小</b>的数或距离", "单调栈, 存下标, pop 时结算", "<code>O(n²)</code> → <code>O(n)</code>"],
    ["数组是循环的", "循环 2n 次, i % n, 第二圈只 pop", "<code>O(n²)</code> → <code>O(n)</code>"],
    ["以每个元素为最大 / 最小值能延伸多远 (矩形面积)", "单调栈, pop 时右边界 = i, 左边界 = 新栈顶", "<code>O(n²)</code> → <code>O(n)</code>"],
    ["0/1 矩阵里最大的全 1 矩形", "逐行变成柱子, 套第 3 题", "<code>O(rows·cols)</code>"],
    ["删 / 选 k 个使结果最小, 顺序不变", "greedy + 单调栈, 栈就是答案", "指数 → <code>O(n)</code>"],
    ["固定长度窗口的 max / min", "单调 deque: 队头过期出, 队尾小的出", "<code>O(n·k)</code> → <code>O(n)</code>"]])
doc.p("选方向的口诀: <b>找更大 → 递减栈; 找更小 → 递增栈</b>。窗口会过期 → deque。")

doc.h2("以后再学")
doc.p("Car Fleet (按位置排序后从后往前用栈)、132 Pattern、Sum of Subarray Minimums (第 3 题的思路, 每个元素当最小值贡献多少)。")
doc.write("docs/07-monotonic-stack.html")
