# 16 · Greedy 正文 (NeetCode 式讲法)。由 16_greedy.py 末尾 exec, 共用 ns / CODE_* / d。
import nclib as nc
from counts import cnt

SL = "16-greedy"
EX = os.path.join(d.ROOT, "docs", "svg", SL, "%s_examples.svg")
EXS = SL + "/%s_examples.svg"

# ---------------------------------------------------------------- 例子图
assert ns["can_jump"]([2, 3, 1, 1, 4]) and not ns["can_jump"]([3, 2, 1, 0, 4])
nc.examples_svg(EX % "jump_game", "Jump Game examples", ["nums[i] 是在位置 i 最多能往前跳几格。从 index 0 出发, 能不能跳到最后一格"], [
    dict(title="Example 1:  nums = [2,3,1,1,4]  →  True", items=[2, 3, 1, 1, 4], hl=[0, 1, 4], ans_text="0 → 1 → 4"),
    dict(title="Example 2:  nums = [3,2,1,0,4]  →  False", items=[3, 2, 1, 0, 4], bad=[(3, 3, "不管怎么跳, 都会停在这个 0 上")],
         extra=["从 0、1、2 出发最远都只能到 index 3, 而 index 3 一步都跳不了"])],
    legend=[("new", "一种跳法"), ("rem", "卡住的地方")])

assert ns["jump"]([2, 3, 1, 1, 4]) == 2
nc.examples_svg(EX % "jump_game_ii", "Jump Game II examples", ["同上, 保证能跳到最后。问最少跳几次"], [
    dict(title="Example:  nums = [2,3,1,1,4]  →  2", items=[2, 3, 1, 1, 4], hl=[0, 1, 4], ans_text="0 → 1 → 4, 跳 2 次",
         extra=["0 → 2 → 3 → 4 也能到, 但要 3 次"])],
    legend=[("new", "最少的跳法")])

assert ns["can_complete_circuit"]([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]) == 3 and ns["can_complete_circuit"]([2, 3, 4], [3, 4, 3]) == -1
nc.examples_svg(EX % "gas_station", "Gas Station examples",
                ["环形公路上 n 个加油站。在站 i 能加 gas[i] 升, 从 i 开到 i+1 要 cost[i] 升。油箱一开始是空的。从哪一站出发能绕一圈? 没有就 -1"], [
    dict(title="Example:  gas = [1,2,3,4,5], cost = [3,4,5,1,2]  →  3", index=False, rows=[
        ("gas", [1, 2, 3, 4, 5], None), ("cost", [3, 4, 5, 1, 2], None),
        ("gas-cost", [-2, -2, -2, 3, 3], ["rem", "rem", "rem", "new", "new"])],
         extra=["从站 3 出发: 油箱 3 → 6 → 4 → 2 → 0, 一直不是负数, 能绕回站 3",
                "从站 0 出发: 加 1 升, 要花 3 升, 第一段就开不过去"])],
    legend=[("new", "净赚油"), ("rem", "净亏油")])

assert ns["max_profit"]([7, 1, 5, 3, 6, 4]) == 7
nc.examples_svg(EX % "stock_ii", "Stock II examples", ["可以交易任意多次 (但手里最多一股, 买之前要先卖掉)。最大总利润"], [
    dict(title="Example:  prices = [7,1,5,3,6,4]  →  7", items=[7, 1, 5, 3, 6, 4], hl=[1, 2, 3, 4],
         extra=["第 1 天买 1, 第 2 天卖 5 (+4);  第 3 天买 3, 第 4 天卖 6 (+3)  → 7",
                "只交易一次的话最多是 6 - 1 = 5, 不如分两次"])],
    legend=[("new", "两次交易")])

assert ns["candy"]([1, 0, 2]) == 5 and ns["candy"]([1, 2, 2]) == 4
nc.examples_svg(EX % "candy", "Candy examples", ["一排孩子, ratings 是评分。每人至少 1 颗糖; 评分比<相邻>的孩子高, 就要比他多拿。最少要几颗糖"], [
    dict(title="Example 1:  ratings = [1,0,2]  →  5", index=False, rows=[("ratings", [1, 0, 2], None), ("糖", [2, 1, 2], ["new"] * 3)],
         extra=["index 0 比右边高, 要比它多; index 2 比左边高, 也要多"]),
    dict(title="Example 2:  ratings = [1,2,2]  →  4", index=False, rows=[("ratings", [1, 2, 2], None), ("糖", [1, 2, 1], ["new"] * 3)],
         extra=["两个 2 评分相同, 没有要求, 最后一个只给 1 颗"])],
    legend=[])

assert ns["largest_number"]([10, 2]) == "210" and ns["largest_number"]([3, 30, 34, 5, 9]) == "9534330"
nc.examples_svg(EX % "largest_number", "Largest Number examples", ["把一组非负整数拼成一个字符串, 让它表示的数最大"], [
    dict(title="Example 1:  [10,2]  →  \"210\"", extra=["2 放前面: \"210\" > \"102\""]),
    dict(title="Example 2:  [3,30,34,5,9]  →  \"9534330\"", items=["9", "5", "34", "3", "30"], cw=50, index=False, hl=[0, 1, 2, 3, 4],
         extra=["3 要放在 30 前面: \"330\" > \"303\"。按字符串字典序排的话 30 会在 3 前面, 是错的"])],
    legend=[("new", "拼接顺序")])

assert ns["partition_labels"]("ababcbacadefegdehijhklij") == [9, 7, 8]
nc.examples_svg(EX % "partition_labels", "Partition Labels examples", ["把字符串切成尽量多的段, 要求每个字母只出现在其中一段里。返回每段的长度"], [
    dict(title="Example:  s = \"ababcbacadefegdehijhklij\"  →  [9,7,8]", items=list("ababcbacadefegdehijhklij"), cw=24,
         ans=[(0, 8), (9, 15), (16, 23)], index=False,
         extra=["\"ababcbaca\" | \"defegde\" | \"hijhklij\": a 只在第一段, d 和 e 只在第二段, ..."])],
    legend=[("new", "每一段")])

# ================================================================ HTML
doc = d.Doc("16 · Greedy")
doc.h2("这篇讲什么")
doc.p("<b>Greedy</b> (贪心) 的意思是: 每一步都做<b>当前看起来最好</b>的选择, 不回头, 不考虑以后。")
doc.p("它很快 (通常扫一遍 <code>O(n)</code>, 或者排序后扫一遍 <code>O(n log n)</code>), 但不一定对。greedy 题的难点从来不是代码, 而是<b>说明为什么\"每步选最好的\"不会错过全局最优</b>。")
doc.p("先看一个反例, 理解什么时候 greedy 会错:")
doc.svg(SL + "/greedy_core.svg", "同样是 Coin Change 先拿最大面额: [1,5,10,25] 可以, 因为大面额总能被换掉; [1,3,4] 凑 6 时先拿 4 得到 3 枚, 但 3 + 3 只要 2 枚。")
doc.p("证明 greedy 正确的常用方法叫 <b>exchange argument</b> (交换论证): 假设有一个最优解, 它在某一步没有按 greedy 选; 把那一步换成 greedy 的选择, 证明结果不会变差。那么 greedy 的结果也是最优的。")
doc.p("面试里不需要写严格的证明, 但要能用一两句话说出\"为什么这样选不会吃亏\"。说不出来, 或者能找到反例, 就换成 DP (14)。")
nc.solution(doc, CODE_COIN, CODE_TEMPLATE, summary="代码: Coin Change 的 DP 解法, 以及 greedy 的一般形式")
nc.table(doc, ["#", "题目", "考过的公司数", "greedy 的选择"], [
    ["1", "Jump Game", cnt("Jump Game"), "只记\"最远能到哪\""],
    ["2", "Jump Game II", cnt("Jump Game II"), "同上, 再按层数跳了几次"],
    ["3", "Gas Station", cnt("Gas Station"), "油箱变负就换起点"],
    ["4", "Best Time to Buy and Sell Stock II", cnt("Best Time to Buy and Sell Stock II"), "所有上涨都吃掉"],
    ["5", "Candy", cnt("Candy"), "两个方向的约束, 分两遍扫"],
    ["6", "Largest Number", cnt("Largest Number"), "自定义排序"],
    ["7", "Partition Labels", cnt("Partition Labels"), "用每个字母最后出现的位置当边界"]])
doc.p("每道题的顺序: <b>题目在问什么 → 看例子 → brute force → intuition → 算法 → 手动走一遍 → 复杂度</b>。代码放在最后, 默认折叠。")
doc.p("另外两类常见的 greedy 在别的篇: 区间按 end 排序 (10 · Intervals), greedy + heap (09 · Heap)。")

# ================================================================ 1
doc.h2("1. Jump Game")
doc.h3("题目在问什么")
doc.p("<code>nums[i]</code> 表示在位置 i 时<b>最多</b>能往前跳几格 (可以跳 1 到 nums[i] 格中的任意一个)。从 index 0 出发, 能不能到达最后一格?")
doc.h3("看例子")
doc.svg(EXS % "jump_game", "两个例子。")
doc.h3("Brute force")
doc.p("recursion: 从位置 i 出发, 试每一种跳法。指数级。加 memo 变成 DP: <code>can[i]</code> = 从 i 能不能到终点, 每个 i 要看 nums[i] 个后继, <code>O(n²)</code>。")
doc.h3("Intuition: 只记\"最远能到哪\"")
doc.p("关键观察: 如果能到达位置 x, 那 0 到 x 之间的每个位置都能到达 (跳的时候可以少跳几格)。所以\"能到达的位置\"永远是一个从 0 开始的连续区间 <code>[0, max_reach]</code>。")
doc.p("不需要知道具体怎么跳的, 只要维护 max_reach 这一个数: 从左往右扫, 每到一个能到达的位置 i, 就更新 <code>max_reach = max(max_reach, i + nums[i])</code>。")
doc.p("如果扫到的 i 已经超过了 max_reach, 说明 i 根本到不了, 后面也到不了, 返回 False。")
doc.h3("算法")
nc.steps(doc, "<code>max_reach = 0</code>。",
         "i 从 0 到 n-1: 如果 <code>i > max_reach</code>, 返回 False。否则 <code>max_reach = max(max_reach, i + nums[i])</code>。",
         "返回 True。")
doc.svg(SL + "/jump_game_core.svg", "invariant: 0..max_reach 全部可达。失败 = 扫到的 i 超过了 max_reach。")
doc.h3("手动走一遍")
doc.svg(SL + "/jump_game_trace.svg", "[2,3,1,1,4]: i = 0 时 max_reach = 2, i = 1 时推到 4, 之后一直够得着。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(1)</code>。")
nc.solution(doc, CODE_JUMP)
doc.note("能到达的位置是一个连续区间时, 只维护它的右端点 max_reach。")

# ================================================================ 2
doc.h2("2. Jump Game II")
doc.h3("题目在问什么")
doc.p("和第 1 题一样的规则, 这次保证一定能到最后一格。问<b>最少</b>跳几次。")
doc.h3("看例子")
doc.svg(EXS % "jump_game_ii", "例子。")
doc.h3("Brute force")
doc.p("DP: <code>dp[i]</code> = 到达 i 最少几步, 每个 i 往前看所有能跳到它的位置, <code>O(n²)</code>。或者把它当图, 用 BFS (12) 求最少步数。")
doc.h3("Intuition: 按\"跳几次能到\"分层, 和 BFS 一样")
doc.p("想象 BFS: 第 0 层是 index 0; 第 1 层是跳 1 次能到的所有位置; 第 2 层是跳 2 次能到的……由第 1 题的观察, 每一层都是一段<b>连续</b>的区间。")
doc.p("所以不需要真的用 queue, 只要两个数:")
nc.bullets(doc, "<code>cur_end</code>: 当前这一层的右端点。", "<code>farthest</code>: 扫描当前这一层时, 能跳到的最远位置, 也就是下一层的右端点。")
doc.p("从左往右扫, 每个位置都更新 farthest。扫到 <code>i == cur_end</code> 时, 当前这一层结束了, 必须再跳一次: <code>jumps += 1</code>, <code>cur_end = farthest</code>。")
doc.h3("算法")
nc.steps(doc, "<code>jumps = cur_end = farthest = 0</code>。",
         "i 从 0 到 n-2 (到了最后一格就不用再跳): <code>farthest = max(farthest, i + nums[i])</code>。如果 <code>i == cur_end</code>: jumps += 1, cur_end = farthest。",
         "返回 jumps。")
doc.svg(SL + "/jump_game_ii_core.svg", "每一层是一段连续区间; cur_end 是它的右端, farthest 是扫这一层时算出的下一层右端。")
doc.h3("手动走一遍")
doc.svg(SL + "/jump_game_ii_trace.svg", "[2,3,1,1,2,4,1]: 在 i = 0, 2, 4 三次走到层尾, jumps = 3。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(1)</code>。")
nc.solution(doc, CODE_JUMP2)
doc.note("最少几步 + 每一层是连续区间: 用 cur_end 和 farthest 模拟 BFS 分层, 不需要 queue。")

# ================================================================ 3
doc.h2("3. Gas Station")
doc.h3("题目在问什么")
doc.p("环形公路上有 n 个加油站。在站 i 可以加 <code>gas[i]</code> 升油, 从站 i 开到站 i+1 要花 <code>cost[i]</code> 升。油箱一开始是空的, 容量无限。从哪一站出发能绕一整圈回来? 有解的话答案唯一, 没有就返回 -1。")
doc.h3("看例子")
doc.svg(EXS % "gas_station", "例子。")
doc.p("每一站的净收益是 <code>gas[i] - cost[i]</code>。从某站出发, 一路累加净收益, 中途任何时候都不能变成负数。")
doc.h3("Brute force")
doc.p("每一站都试一次当起点, 模拟绕一圈。<code>O(n²)</code>。")
doc.h3("Intuition: 在哪里失败, 就从下一站重新开始")
doc.p("两个观察:")
nc.steps(doc, "<b>有没有解</b>: 如果所有站的净收益加起来 <code>total < 0</code>, 油总量不够, 从哪里出发都不行。反过来, total ≥ 0 就一定有解。",
         "<b>从哪里出发</b>: 假设从 start 出发, 开到站 i 时油箱变负了。那么 start 到 i 之间的任何一站当起点, 也都到不了 i+1。")
doc.p("为什么第 2 点成立? 从 start 出发, 到达中间某站 k 时油箱是 ≥ 0 的 (还没失败)。如果直接从 k 出发, 油箱是 0, 只会比\"从 start 出发到达 k\"更少。连多带了油的都过不去, 空着油箱的更过不去。")
doc.p("所以一失败, 直接把起点跳到 <code>i + 1</code>, 油箱清零。扫一遍就够了。")
doc.h3("算法")
nc.steps(doc, "<code>total = tank = start = 0</code>。",
         "i 从 0 到 n-1: <code>diff = gas[i] - cost[i]</code>, total 和 tank 都加上 diff。如果 <code>tank < 0</code>: <code>start = i + 1</code>, <code>tank = 0</code>。",
         "返回 <code>start if total >= 0 else -1</code>。")
doc.svg(SL + "/gas_station_core.svg", "net = [2,1,-5,3,1]: 起点 0、1、2 都会失败, 只有起点 3 走得完。")
doc.h3("手动走一遍")
doc.svg(SL + "/gas_station_trace.svg", "i = 1、2 时 tank 变负, start 依次被推到 2、3; 之后 tank 不再变负, total = 0 ≥ 0, 答案 3。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(1)</code>。")
nc.solution(doc, CODE_GAS)
doc.note("累计量变负就重置起点: 失败点之前的任何一个起点都不会更好。")

# ================================================================ 4
doc.h2("4. Best Time to Buy and Sell Stock II")
doc.h3("题目在问什么")
doc.p("<code>prices[i]</code> 是第 i 天的股价。可以交易<b>任意多次</b>, 但手里最多只能有一股 (买之前必须先卖掉)。最大总利润是多少?")
doc.h3("看例子")
doc.svg(EXS % "stock_ii", "例子。")
doc.h3("Brute force")
doc.p("枚举所有买卖方案, 指数级。或者用 14 里的 hold / cash 状态机 DP, <code>O(n)</code>。")
doc.h3("Intuition: 每一段上涨都吃掉")
doc.p("把价格曲线画出来, 它是一段一段的上涨和下跌。")
doc.p("任何一次\"第 i 天买、第 j 天卖\"的利润 <code>prices[j] - prices[i]</code>, 都等于中间每一天的涨跌加起来。其中下跌的那几天只会减少利润。")
doc.p("既然可以交易任意多次, 就只在上涨的那几天持有: <b>每一个 <code>prices[i] > prices[i-1]</code> 的地方, 都把这个差价赚到</b>。这等价于在每段上涨的底部买、顶部卖。")
doc.h3("算法")
nc.steps(doc, "<code>profit = 0</code>。", "i 从 1 到 n-1: <code>profit += max(0, prices[i] - prices[i-1])</code>。")
doc.svg(SL + "/stock_ii_core.svg", "绿色是上涨段 (+4, +3), 橙色虚线是下跌段。一直持有 1 → 6 只赚 5。")
doc.h3("手动走一遍")
doc.svg(SL + "/stock_ii_trace.svg", "每天只看和昨天的差: -6, +4, -2, +3, -2。profit 只在 +4 和 +3 时增加。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(1)</code>。")
nc.solution(doc, CODE_STOCK)
doc.note("可以交易任意多次: 所有正的相邻差价加起来。")

# ================================================================ 5
doc.h2("5. Candy")
doc.h3("题目在问什么")
doc.p("一排孩子, <code>ratings[i]</code> 是第 i 个孩子的评分。分糖果: 每个孩子至少 1 颗; 评分比<b>相邻</b>孩子高的, 必须比那个孩子拿得多。最少要准备几颗糖?")
doc.h3("看例子")
doc.svg(EXS % "candy", "两个例子。")
doc.h3("Brute force")
doc.p("先每人 1 颗, 然后反复扫, 发现不满足条件的就加 1, 直到所有条件都满足。最坏 <code>O(n²)</code>。")
doc.h3("Intuition: 左右两个约束, 分开处理")
doc.p("每个孩子有两个约束: 和左边比, 和右边比。同时考虑两边很乱, 那就<b>分开</b>:")
nc.steps(doc, "从左往右扫一遍, 只管左边的约束: 比左边评分高, 就 <code>left[i] = left[i-1] + 1</code>, 否则 1。",
         "从右往左扫一遍, 只管右边的约束: 比右边评分高, 就 <code>right[i] = right[i+1] + 1</code>, 否则 1。",
         "每个孩子要同时满足两个约束, 取 <code>max(left[i], right[i])</code>。")
doc.p("为什么取 max 就够了, 而且是最少的? 每个值都是满足那一侧约束的最小值, 取 max 刚好两边都满足, 没有多给。")
doc.h3("算法")
nc.steps(doc, "<code>left</code> 从左往右填, <code>right</code> 从右往左填。", "返回 <code>sum(max(left[i], right[i]))</code>。")
doc.svg(SL + "/candy_core.svg", "left 管左边的约束, right 管右边的约束, 逐个取 max 就是答案: 2 + 1 + 2 + 3 + 1 = 9。")
doc.h3("手动走一遍")
doc.svg(SL + "/candy_trace.svg", "A 段从左到右填 left, B 段从右到左填 right, C 段取 max 求和。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(n)</code>。")
nc.solution(doc, CODE_CANDY)
doc.note("每个元素同时受左右两边约束: 从左扫一遍、从右扫一遍, 再合并 (取 max)。")

# ================================================================ 6
doc.h2("6. Largest Number")
doc.h3("题目在问什么")
doc.p("给一组非负整数, 把它们重新排列后拼接成一个字符串, 让这个数最大。返回字符串。")
doc.h3("看例子")
doc.svg(EXS % "largest_number", "两个例子。")
doc.h3("Brute force")
doc.p("试所有排列, 拼起来比大小。<code>O(n! · n)</code>。")
doc.h3("Intuition: 两个数谁放前面, 拼一下比一比")
doc.p("直觉是\"大的放前面\", 但按数值排不对 (10 和 2, 应该是 2 在前); 按字符串字典序排也不对 (3 和 30, 字典序是 30 > 3, 但 \"330\" > \"303\", 应该 3 在前)。")
doc.p("正确的比较方法: 对两个数 a 和 b, 直接比较 <code>a + b</code> 和 <code>b + a</code> (字符串拼接)。<code>a + b</code> 更大, a 就放前面。")
doc.p("为什么这样排出来的就是最优? 用交换论证: 如果最优解里有相邻的两个 x, y 满足 <code>y + x > x + y</code>, 交换它们, 拼出来的数会更大, 矛盾。所以最优解里每一对相邻的都满足这个顺序, 也就是按这个规则排好序的结果。")
doc.p("Python 里用 <code>functools.cmp_to_key</code> 把比较函数变成排序的 key。最后注意全是 0 的情况, 要返回 \"0\" 而不是 \"000\"。")
doc.h3("算法")
nc.steps(doc, "转成字符串。", "按比较规则排序: a + b > b + a 的 a 排前面。", "拼接; 如果第一个是 \"0\", 返回 \"0\"。")
doc.svg(SL + "/largest_number_core.svg", "字典序会得到 303, 比较 a + b 和 b + a 得到 330。最优解里每一对相邻的都满足 x + y ≥ y + x。")
doc.h3("手动走一遍")
doc.svg(SL + "/largest_number_trace.svg", "逐个插入: 30 排在 3 后面 (303 < 330), 34 插到 3 前面 (343 > 334), 5 和 9 一路插到最前。")
doc.h3("复杂度")
doc.p("Time <code>O(n log n · L)</code>, L 是数字的位数。Space <code>O(n · L)</code>。")
nc.solution(doc, CODE_LARGEST)
doc.note("\"排列成最优\": 找出两个元素之间的比较规则 (常用 a+b vs b+a), 自定义排序。")

# ================================================================ 7
doc.h2("7. Partition Labels")
doc.h3("题目在问什么")
doc.p("把字符串 s 切成<b>尽量多</b>的段, 要求每个字母只出现在其中一段里。返回每一段的长度。")
doc.h3("看例子")
doc.svg(EXS % "partition_labels", "例子。")
doc.h3("Brute force")
doc.p("试所有切法, 检查每个字母是否只在一段里。指数级。")
doc.h3("Intuition: 一段至少要延伸到它里面每个字母最后出现的位置")
doc.p("第一段从 index 0 开始。第一个字母是 a, 那 a 所有出现的地方都必须在这一段里, 所以这一段至少要到 a <b>最后一次出现</b>的位置。")
doc.p("但在这个范围里, 又出现了别的字母 (比如 b), b 最后出现的位置可能更远, 那这一段就要延伸到那里。一直这样延伸, 直到扫到的位置 i 正好等于当前要求的右边界 end, 说明这一段里所有字母都不会再出现了, 在这里切一刀, 段数最多。")
doc.p("所以先扫一遍, 记下每个字母最后出现的位置 <code>last[c]</code>。")
doc.h3("算法")
nc.steps(doc, "<code>last = {c: i for i, c in enumerate(s)}</code>。",
         "<code>start = end = 0</code>。i 从 0 到 n-1: <code>end = max(end, last[s[i]])</code>。如果 <code>i == end</code>: 记录长度 <code>end - start + 1</code>, <code>start = i + 1</code>。")
doc.svg(SL + "/partition_labels_core.svg", "a 的 last = 2, b 的 last = 4: 第一段至少到 4。每段的右边界由段里所有字母的 last 决定。")
doc.h3("手动走一遍")
doc.svg(SL + "/partition_labels_trace.svg", "end 一路被推远, i 追上 end 的时候切一刀。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(26)</code>。这和 10 里的 Merge Intervals 是一回事: 每个字母对应一个区间 [第一次出现, 最后一次出现], 合并重叠的区间。")
nc.solution(doc, CODE_PART)
doc.note("每个元素必须在同一段: 记下最后出现的位置, 边扫边延伸右边界, 追上了就切。")

# ================================================================ 识别信号
doc.h2("8. 识别信号: 看到什么, 就想到 greedy")
nc.table(doc, ["题目特征", "做法", "complexity"], [
    ["能不能到达 / 能到达的范围是连续的", "只维护 max_reach", "<code>O(n²)</code> → <code>O(n)</code>"],
    ["最少几步, 每一层是连续区间", "cur_end + farthest 模拟 BFS 分层", "<code>O(n²)</code> → <code>O(n)</code>"],
    ["环形, 累计量不能为负", "变负就把起点重置到下一个; total 判断有没有解", "<code>O(n²)</code> → <code>O(n)</code>"],
    ["可以交易任意多次", "所有正的差价加起来", "<code>O(n)</code>"],
    ["每个元素受左右两边约束", "左扫一遍、右扫一遍, 再合并", "<code>O(n²)</code> → <code>O(n)</code>"],
    ["\"排列成最大 / 最小\"", "找两两比较的规则, 自定义排序", "<code>O(n!)</code> → <code>O(n log n)</code>"],
    ["切成尽量多的段, 某种元素不能跨段", "记 last, 边扫边延伸右边界", "<code>O(n)</code>"],
    ["区间: 最多保留几个不重叠", "按 end 排序 → 10", "<code>O(n log n)</code>"],
    ["每一步选\"当前最优\", 候选会变化", "greedy + heap → 09", "<code>O(n log n)</code>"]])
doc.p("用 greedy 之前, 先试着找反例。找不到反例, 并且能说出一句\"为什么这样选不会吃亏\", 才用。否则用 DP。")

doc.h2("以后再学")
doc.p("Huffman 编码、Dijkstra (本质也是 greedy, 见 12)、matroid 理论 (什么时候 greedy 一定对)。")
doc.write("docs/16-greedy.html")
