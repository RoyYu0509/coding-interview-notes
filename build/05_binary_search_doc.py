# 05 · Binary Search 正文 (NeetCode 式讲法)。由 05_binary_search.py 的 build_doc() exec。
import nclib as nc
from counts import cnt

EX = os.path.join(d.ROOT, "docs", "svg", SLUG, "%s_examples.svg")
ns = load_code()

# ---------------------------------------------------------------- 例子图
assert ns["search_range"]([5, 7, 7, 8, 8, 10], 8) == [3, 4]
assert ns["search_range"]([5, 7, 7, 8, 8, 10], 6) == [-1, -1]
nc.examples_svg(EX % "first_last", "Find First and Last Position examples",
                ["数组从小到大排好。找 target 第一次出现和最后一次出现的下标; 没有就返回 [-1, -1]。要求 O(log n)"], [
    dict(title="Example 1:  nums = [5,7,7,8,8,10], target = 8  →  [3, 4]", items=[5, 7, 7, 8, 8, 10], ans=[(3, 4)],
         ans_text="8 在 index 3 和 4"),
    dict(title="Example 2:  nums = [5,7,7,8,8,10], target = 6  →  [-1, -1]", items=[5, 7, 7, 8, 8, 10],
         extra=["6 不在数组里。如果要插入 6, 它应该放在 index 1 (7 的前面)"])],
    legend=[("new", "等于 target"), ("ring", "答案的范围")])

assert ns["find_min"]([3, 4, 5, 1, 2]) == 1 and ns["find_min"]([4, 5, 6, 7, 8, 9, 1, 2, 3]) == 1
nc.examples_svg(EX % "find_min", "Find Minimum in Rotated Sorted Array examples",
                ["一个排好序的数组, 被\"旋转\"过: 把开头的一段剪下来接到最后。元素不重复。找最小值, 要求 O(log n)"], [
    dict(title="Example 1:  nums = [3,4,5,1,2]  →  1", items=[3, 4, 5, 1, 2], hl=[3],
         ans_text="原数组 [1,2,3,4,5], 把 [1,2] 移到最后",
         extra=["旋转后是两段各自排好序的数组: [3,4,5] 和 [1,2]。最小值就是第二段的开头"]),
    dict(title="Example 2:  nums = [4,5,6,7,8,9,1,2,3]  →  1", items=[4, 5, 6, 7, 8, 9, 1, 2, 3], hl=[6],
         ans_text="两段: [4..9] 和 [1,2,3]"),
    dict(title="Example 3:  nums = [11,13,15,17]  →  11", items=[11, 13, 15, 17], hl=[0],
         ans_text="转了一整圈, 等于没转")],
    legend=[("new", "最小值")])

assert ns["search"]([4, 5, 6, 7, 0, 1, 2], 0) == 4 and ns["search"]([4, 5, 6, 7, 0, 1, 2], 3) == -1
nc.examples_svg(EX % "search_rotated", "Search in Rotated Sorted Array examples",
                ["同样是旋转过的排序数组 (元素不重复)。找 target 的下标, 没有返回 -1。要求 O(log n)"], [
    dict(title="Example 1:  nums = [4,5,6,7,0,1,2], target = 0  →  4", items=[4, 5, 6, 7, 0, 1, 2], hl=[4],
         ans_text="0 在 index 4"),
    dict(title="Example 2:  nums = [4,5,6,7,0,1,2], target = 3  →  -1", items=[4, 5, 6, 7, 0, 1, 2],
         extra=["3 比 2 大、比 4 小, 两段里都放不下它"])],
    legend=[("new", "target")])

assert ns["find_peak"]([1, 2, 3, 1]) == 2
nc.examples_svg(EX % "peak", "Find Peak Element examples",
                ["peak = 比左右两个邻居都大的元素 (数组两端外面当作 -∞)。相邻元素不相等。", "返回任意一个 peak 的下标, 要求 O(log n)"], [
    dict(title="Example 1:  nums = [1,2,3,1]  →  2", items=[1, 2, 3, 1], hl=[2], ans_text="3 > 2 且 3 > 1"),
    dict(title="Example 2:  nums = [1,2,1,3,5,6,4]  →  1 或 5", items=[1, 2, 1, 3, 5, 6, 4], hl=[1, 5],
         ans_text="2 和 6 都是 peak, 返回哪个都对"),
    dict(title="Example 3:  nums = [1,2,3,4]  →  3", items=[1, 2, 3, 4], hl=[3],
         ans_text="4 右边是 -∞, 所以 4 也是 peak")],
    legend=[("new", "peak")])

assert ns["min_eating_speed"]([3, 6, 7, 11], 8) == 4 and ns["min_eating_speed"]([30, 11, 23, 4, 20], 5) == 30
nc.examples_svg(EX % "koko", "Koko Eating Bananas examples",
                ["每小时选一堆吃 k 根; 这堆不够 k 根就吃完这堆, 这一小时也结束了。要在 h 小时内吃完所有堆, 求最小的 k"], [
    dict(title="Example 1:  piles = [3,6,7,11], h = 8  →  4", items=[3, 6, 7, 11],
         extra=["k = 4: 每堆要的小时数 1 + 2 + 2 + 3 = 8 ≤ 8 ✓",
                "k = 3: 1 + 2 + 3 + 4 = 10 > 8 ✗   所以最小是 4"]),
    dict(title="Example 2:  piles = [30,11,23,4,20], h = 5  →  30", items=[30, 11, 23, 4, 20],
         extra=["只有 5 小时、5 堆, 每小时必须吃完一整堆 → k 至少是最大的那堆 30"])],
    legend=[("keep", "每堆香蕉数")])

assert ns["ship_within_days"]([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5) == 15
nc.examples_svg(EX % "ship", "Capacity To Ship Packages examples",
                ["包裹按顺序装船, 每天一船, 一船最多装 cap 重。不能拆包裹, 不能换顺序。要在 days 天内运完, 求最小的 cap"], [
    dict(title="Example:  weights = [1,2,3,4,5,6,7,8,9,10], days = 5  →  15", items=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
         extra=["cap = 15: [1,2,3,4,5]=15 | [6,7]=13 | [8]=8 | [9]=9 | [10]=10 → 5 天 ✓",
                "cap = 14: [1..4]=10 | [5,6]=11 | [7]=7 | [8]=8 | [9]=9 | [10]=10 → 6 天 ✗"])],
    legend=[("keep", "包裹重量")])

assert ns["split_array"]([7, 2, 5, 10, 8], 2) == 18
nc.examples_svg(EX % "split", "Split Array Largest Sum examples",
                ["把数组切成 k 段连续的 subarray。每段有一个和, 取其中最大的。怎么切能让这个最大值最小"], [
    dict(title="Example:  nums = [7,2,5,10,8], k = 2  →  18", items=[7, 2, 5, 10, 8], ans=[(0, 2)],
         ans_text="[7,2,5] = 14 | [10,8] = 18 → 最大 18",
         extra=["其他切法: [7] | [2,5,10,8] → 最大 25;  [7,2] | [5,10,8] → 23;  [7,2,5,10] | [8] → 24",
                "18 是所有切法里\"最大段和\"最小的"])],
    legend=[("new", "第一段"), ("ring", "切法")])

assert ns["search_matrix"]([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3) is True
nc.examples_svg(EX % "matrix", "Search a 2D Matrix examples",
                ["每行从小到大; 每行的第一个数 > 上一行的最后一个数。判断 target 在不在矩阵里, 要求 O(log(m·n))"], [
    dict(title="Example:  target = 3  →  True;  target = 13  →  False", index=False, rows=[
        ("row 0", [1, 3, 5, 7], ["keep", "new", "keep", "keep"]), ("row 1", [10, 11, 16, 20], None),
        ("row 2", [23, 30, 34, 60], None)],
         extra=["按行连起来读: 1, 3, 5, 7, 10, 11, 16, 20, 23, 30, 34, 60 —— 就是一个排好序的一维数组"])],
    legend=[("new", "target = 3")])

assert ns["find_median"]([1, 3], [2]) == 2 and ns["find_median"]([1, 2], [3, 4]) == 2.5
nc.examples_svg(EX % "median", "Median of Two Sorted Arrays examples",
                ["两个排好序的数组, 求它们合并之后的中位数。要求 O(log(m + n))"], [
    dict(title="Example 1:  A = [1,3], B = [2]  →  2", rows=[("A", [1, 3], None), ("B", [2], None),
                                                          ("合并", [1, 2, 3], ["keep", "new", "keep"])],
         extra=["合并后 3 个数, 中间那个是 2"]),
    dict(title="Example 2:  A = [1,2], B = [3,4]  →  2.5", rows=[("合并", [1, 2, 3, 4], ["keep", "new", "new", "keep"])],
         extra=["4 个数, 中位数是中间两个的平均: (2 + 3) / 2 = 2.5"])],
    legend=[("new", "中位数")])

# ================================================================ HTML
doc = d.Doc("05 · Binary Search")
doc.h2("这篇讲什么")
doc.p("先想一个猜数字游戏: 我心里想一个 1 到 100 的数, 你每猜一次, 我告诉你\"大了\"还是\"小了\"。最笨的办法是从 1 开始一个一个猜, 最多 100 次。"
      "聪明的办法是先猜 50: 如果\"大了\", 1..50 以外的一半直接排除。每猜一次排除一半, 最多 7 次 (<code>log₂ 100 ≈ 7</code>)。")
doc.p("这就是 <b>Binary Search</b>。它能用的前提是: <b>问一次, 就能确定答案在哪一半</b>。排好序的数组满足这个前提, 但这篇会看到, 很多<b>没有排序</b>的问题也满足 (旋转数组、找 peak、二分答案)。")
doc.p("复杂度从 <code>O(n)</code> 降到 <code>O(log n)</code>。n = 10⁹ 时, 线性要 10 亿步, 二分只要 30 步。")
nc.table(doc, ["#", "题目", "考过的公司数", "相比上一题多了什么"], [
    ["1", "Find First and Last Position", cnt("Find First and Last Position of Element in Sorted Array"), "模板题: 排好序的数组, 找第一个、最后一个"],
    ["2", "Find Minimum in Rotated Sorted Array", cnt("Find Minimum in Rotated Sorted Array"), "数组被旋转了, 要自己找出\"能二分的条件\""],
    ["3", "Search in Rotated Sorted Array", cnt("Search in Rotated Sorted Array"), "旋转数组里找某个数"],
    ["4", "Find Peak Element", cnt("Find Peak Element"), "完全没排序, 只靠\"往上坡走\""],
    ["5", "Koko Eating Bananas", cnt("Koko Eating Bananas"), "二分的不是下标, 是<b>答案</b>"],
    ["6", "Capacity To Ship Packages", cnt("Capacity To Ship Packages Within D Days"), "同上, 验证方法换成贪心"],
    ["7", "Split Array Largest Sum", cnt("Split Array Largest Sum"), "\"最小的最大值\" 的标准形式"],
    ["8", "Search a 2D Matrix", cnt("Search a 2D Matrix"), "二维当一维"],
    ["9", "Median of Two Sorted Arrays", cnt("Median of Two Sorted Arrays"), "二分\"分割点\" (简述)"]])
doc.p("每道题的顺序: <b>题目在问什么 → 看例子 → brute force → intuition → 算法 → 手动走一遍 → 复杂度</b>。代码放在最后, 默认折叠。")
doc.p("二分最容易错的是边界 (<code>lo</code>、<code>hi</code>、<code>mid</code> 怎么更新, 会不会死循环)。这篇全程只用<b>一个</b>写法, 讲完第 1 题后会专门讲它, 之后每题只换\"条件\", 不换写法。")

# ================================================================ 1
doc.h2("1. Find First and Last Position of Element in Sorted Array")
doc.h3("题目在问什么")
doc.p("数组 <code>nums</code> 从小到大排好, 可能有重复。找 <code>target</code> 第一次出现和最后一次出现的下标。没有就返回 <code>[-1, -1]</code>。要求 <code>O(log n)</code>。")
doc.h3("看例子")
doc.svg(SLUG + "/first_last_examples.svg", "两个例子。")
doc.h3("Brute force")
doc.p("从左往右扫一遍, 记下第一个和最后一个等于 target 的位置。<code>O(n)</code>。浪费: 数组已经排好序, \"左边都小、右边都大\"这个信息完全没用上。")
doc.h3("Intuition: 把\"等于 target\"换成\"≥ target\"")
doc.p("直接问\"nums[i] 等于 target 吗\"没法二分: 结果是 <code>否 否 否 是 是 否</code>, 看到一个\"否\", 你不知道答案在左边还是右边。")
doc.p("换个问法: \"<b>nums[i] ≥ target 吗?</b>\" 对 <code>[5,7,7,8,8,10]</code>, target = 8, 结果是 <code>否 否 否 是 是 是</code>。"
      "前面一段全是\"否\", 后面一段全是\"是\", 中间只有一个分界点。这就可以二分了: 问一下中间, 是\"是\", 分界点在左边 (或就是这里); 是\"否\", 分界点在右边。")
doc.p("第一个\"是\"的位置, 就是 target 第一次出现的位置 (index 3)。")
doc.p("最后一次出现: 问 \"<b>nums[i] > target 吗?</b>\", 结果是 <code>否 否 否 否 否 是</code>。第一个\"是\"在 index 5, 减 1 就是 8 最后一次出现的位置 (index 4)。")
doc.p("如果第一个 ≥ target 的位置上的数不等于 target (或者越界了), 说明 target 不存在。")
doc.h3("算法")
nc.steps(doc, "找第一个满足 <code>nums[i] >= target</code> 的位置, 记为 left。",
         "如果 left 越界, 或者 <code>nums[left] != target</code>, 返回 <code>[-1, -1]</code>。",
         "找第一个满足 <code>nums[i] > target</code> 的位置, 记为 right。返回 <code>[left, right - 1]</code>。")
doc.p("\"找第一个满足条件的位置\" 怎么写, 下一节专门讲。")
doc.svg(SLUG + "/first_last_core.svg", "两次是同一个写法, 只差条件里的 >= 和 >。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/first_last_trace.svg", "同一个数组跑两遍, 每遍 3 步。红色格子是已经排除的。")
doc.h3("复杂度")
doc.p("Time <code>O(log n)</code>, 两次二分。Space <code>O(1)</code>。")
nc.solution(doc, CODE_FIRST_LAST)
doc.note("找\"等于 x\": 改成找\"第一个 ≥ x\", 再检查是不是 x。最后一个 x = 第一个 > x 的位置 - 1。")

# ================================================================ 抽象
doc.h2("把第 1 题抽象一下: 一个写法解决所有二分")
doc.p("第 1 题里, 我们做的事情都是同一件: 有一个条件 <code>pred(i)</code>, 它在 i 从小到大时是 <code>否 否 ... 否 是 是 ... 是</code>, 要找<b>第一个\"是\"</b>的位置。")
doc.p("这个条件可以是任何东西, 只要满足\"前面全否、后面全是\"。<b>这才是二分的本质, 不是\"数组排好序\"</b>。排好序只是让 <code>nums[i] >= x</code> 恰好满足这个形状。后面的题都是在找不同的 pred。")
doc.p("写法 (全篇只用这一个, 叫 <code>first_true</code>):")
nc.steps(doc, "在 <code>[lo, hi)</code> 里找 (左闭右开)。保持两件事一直成立: <b>lo 左边的都已确认是\"否\", hi 和 hi 右边的都已确认是\"是\"</b>。",
         "当 <code>lo < hi</code>: 取 <code>mid = (lo + hi) // 2</code>。",
         "<code>pred(mid)</code> 是\"是\": 答案在 mid 或 mid 左边, <code>hi = mid</code>。",
         "<code>pred(mid)</code> 是\"否\": 答案在 mid 右边, <code>lo = mid + 1</code>。",
         "结束时 <code>lo == hi</code>, 就是第一个\"是\"。如果全是\"否\", 返回的是原来的 hi (越界), 调用的地方要检查。")
doc.svg(SLUG + "/s0_first_true_core.svg", "lo 左边已知全是\"否\", hi 和右边已知全是\"是\"。每问一次 pred(mid), 范围缩小一半。")
doc.p("为什么不会死循环: 因为 <code>lo ≤ mid < hi</code>, 两个分支都让范围严格变小。如果写成 <code>lo = mid</code>, 当 hi = lo + 1 时 mid = lo, 就永远不动了。")
doc.p("Python 里 <code>bisect_left(a, x)</code> 就是 pred = <code>a[i] >= x</code> 的 first_true, <code>bisect_right(a, x)</code> 是 <code>a[i] > x</code>。")
nc.solution(doc, CODE_TEMPLATE, summary="first_true 模板代码")
doc.note("二分 = 找一个\"前面全否、后面全是\"的条件, 找第一个\"是\"。是: hi = mid; 否: lo = mid + 1; 返回 lo。")

# ================================================================ 2
doc.h2("2. Find Minimum in Rotated Sorted Array")
doc.h3("题目在问什么")
doc.p("一个从小到大排好序、元素不重复的数组, 被\"旋转\"了若干次: 把开头一段剪下来接到最后。比如 <code>[1,2,3,4,5]</code> 旋转后可能变成 <code>[3,4,5,1,2]</code>。找最小值, 要求 <code>O(log n)</code>。")
doc.h3("看例子")
doc.svg(SLUG + "/find_min_examples.svg", "三个例子。")
doc.p("旋转后的数组是<b>两段各自排好序</b>的数组拼起来的。左段的数都比右段大。最小值是右段的第一个。")
doc.h3("Brute force")
doc.p("<code>min(nums)</code>, <code>O(n)</code>。")
doc.h3("Intuition: 找一个\"前面全否、后面全是\"的条件")
doc.p("整个数组不是排好序的, 不能直接用 <code>nums[i] >= x</code>。但我们可以和<b>最后一个数</b> <code>last = nums[-1]</code> 比较:")
nc.bullets(doc, "左段的每个数都 > last (左段整体比右段大, last 是右段的最后一个)。",
           "右段的每个数都 ≤ last (右段是排好序的, last 是右段最大的)。")
doc.p("所以 <code>pred(i) = nums[i] <= last</code> 在左段全是\"否\", 在右段全是\"是\"。第一个\"是\"就是右段的开头, 也就是最小值。直接套 first_true。")
doc.h3("算法")
nc.steps(doc, "<code>last = nums[-1]</code>。", "<code>i = first_true(0, n, lambda i: nums[i] <= last)</code>。", "返回 <code>nums[i]</code>。")
doc.svg(SLUG + "/find_min_core.svg", "和 last 比较才满足\"前面全否、后面全是\"; 和 nums[lo] 比则不行 (lo 在哪一段不确定)。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/find_min_trace.svg", "[4,5,6,7,8,9,1,2,3]: 4 步, 最后 lo = hi = 6, nums[6] = 1。")
doc.h3("复杂度")
doc.p("Time <code>O(log n)</code>, Space <code>O(1)</code>。")
nc.solution(doc, CODE_FIND_MIN)
doc.note("旋转数组: 拿最后一个数当尺子, nums[i] <= nums[-1] 就是可以二分的条件。")

# ================================================================ 3
doc.h2("3. Search in Rotated Sorted Array")
doc.h3("题目在问什么")
doc.p("同样是旋转过的排序数组 (元素不重复)。这次找 <code>target</code> 的下标, 没有返回 -1。要求 <code>O(log n)</code>。")
doc.h3("看例子")
doc.svg(SLUG + "/search_rotated_examples.svg", "两个例子。")
doc.h3("Brute force")
doc.p("线性扫一遍, <code>O(n)</code>。")
doc.p("一个可行的 <code>O(log n)</code> 做法: 先用第 2 题找到最小值的位置 p, 数组就分成了两段排好序的 <code>[0, p)</code> 和 <code>[p, n)</code>, 再根据 target 的大小选一段做第 1 题的二分。两次二分。")
doc.h3("Intuition: 从 mid 切开, 总有一半是排好序的")
doc.p("面试里更常见的是一次二分的写法。关键观察: 从 mid 把当前范围切成左右两半, 旋转的那个\"断点\"只可能在其中一半里, 所以<b>另一半一定是排好序的</b>。")
doc.p("怎么知道哪一半是排好序的? 看 <code>nums[lo] <= nums[mid]</code>: 成立就是左半有序, 否则右半有序。")
doc.p("有序的那一半, 只看两个端点就知道 target 在不在里面。在, 就去这一半; 不在, 就去另一半。")
doc.h3("算法")
nc.steps(doc, "<code>lo = 0</code>, <code>hi = n - 1</code>。当 <code>lo ≤ hi</code>: 取 mid, 如果 <code>nums[mid] == target</code> 返回 mid。",
         "如果左半有序 (<code>nums[lo] <= nums[mid]</code>): target 在 <code>[nums[lo], nums[mid])</code> 里就 <code>hi = mid - 1</code>, 否则 <code>lo = mid + 1</code>。",
         "否则右半有序: target 在 <code>(nums[mid], nums[hi]]</code> 里就 <code>lo = mid + 1</code>, 否则 <code>hi = mid - 1</code>。",
         "循环结束返回 -1。")
doc.p("注意这题没有用 first_true 写法, 因为它不是\"找第一个满足条件的\", 而是\"找某个值\"。这里用的是闭区间, 不变的是\"target 如果存在, 一定在 [lo, hi] 里\"。")
doc.svg(SLUG + "/search_rotated_core.svg", "nums[lo] <= nums[mid] 表示左半有序, 否则右半有序。有序那半用两个端点判断 target 在不在。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/search_rotated_trace.svg", "3 步: 左半有序但 target 不在, 丢掉左半; 右半有序且 target 在, 丢掉左半; 命中。")
doc.h3("复杂度")
doc.p("Time <code>O(log n)</code>, Space <code>O(1)</code>。")
nc.solution(doc, CODE_SEARCH_ROTATED)
doc.note("旋转数组里找数: 从 mid 切开, 总有一半有序; target 在有序那半里就进去, 否则去另一半。")

# ================================================================ 4
doc.h2("4. Find Peak Element")
doc.h3("题目在问什么")
doc.p("peak 是比左右两个邻居都大的元素。数组两端的外面当作 -∞。相邻元素不相等。返回<b>任意一个</b> peak 的下标。要求 <code>O(log n)</code>。")
doc.h3("看例子")
doc.svg(SLUG + "/peak_examples.svg", "三个例子。")
doc.h3("Brute force")
doc.p("从左往右扫, 第一个 <code>nums[i] > nums[i+1]</code> 的就是 peak。<code>O(n)</code>。")
doc.h3("Intuition: 往上坡走, 一定能走到 peak")
doc.p("这个数组完全没有排序。但看 mid 和它右边的邻居 mid+1:")
nc.bullets(doc, "<b>上坡</b> (<code>nums[mid] < nums[mid+1]</code>): 从 mid+1 一直往右走。要么中途开始下坡, 下坡前的那个点就是 peak; 要么一直上坡到最后一个元素, 它右边是 -∞, 它也是 peak。所以<b>右边一定有 peak</b>, 去右边。",
           "<b>下坡</b> (<code>nums[mid] > nums[mid+1]</code>): 同理, mid 自己或者 mid 左边一定有 peak, 去左边 (保留 mid)。")
doc.p("用 first_true 的话, pred 就是 <code>nums[i] > nums[i+1]</code> (\"这里是下坡吗\")。它整体不一定是\"前面全否、后面全是\", 但每一步的判断都是对的: 上坡就往右, 下坡就往左, 最后停下的地方一定是 peak。")
doc.h3("算法")
nc.steps(doc, "<code>lo = 0</code>, <code>hi = n - 1</code>。当 <code>lo < hi</code>: 取 mid。",
         "<code>nums[mid] < nums[mid+1]</code> (上坡): <code>lo = mid + 1</code>。否则 (下坡): <code>hi = mid</code>。",
         "返回 lo。")
doc.svg(SLUG + "/peak_core.svg", "上坡往右 (lo = mid + 1), 下坡往左并保留 mid (hi = mid)。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/peak_trace.svg", "[1,2,3,5,4,6,7,9,8,3,1]: 4 步找到 index 7 的 9。index 3 的 5 也是 peak, 但二分没走到那边, 题目允许返回任意一个。")
doc.h3("复杂度")
doc.p("Time <code>O(log n)</code>, Space <code>O(1)</code>。")
nc.solution(doc, CODE_PEAK)
doc.note("没排序, 但能比较 mid 和邻居: 看坡度, 往上坡走一定有 peak。")

# ================================================================ 5
doc.h2("5. Koko Eating Bananas")
doc.h3("题目在问什么")
doc.p("<code>piles[i]</code> 是第 i 堆香蕉的数量。Koko 每小时选一堆吃 k 根; 这一堆不够 k 根, 就吃完这一堆, 这一小时也就结束了 (不会去吃下一堆)。要在 <code>h</code> 小时内吃完所有香蕉, 求最小的整数速度 k。")
doc.h3("看例子")
doc.svg(SLUG + "/koko_examples.svg", "两个例子。")
doc.p("一堆 p 根香蕉、速度 k, 要 <code>ceil(p / k)</code> 小时。总小时数就是每堆加起来。")
doc.h3("Brute force")
doc.p("从 k = 1 开始一个一个试: 算总小时数, 第一个 ≤ h 的 k 就是答案。每个 k 要 <code>O(n)</code>, 最多试 max(piles) 个。如果某堆有 10⁹ 根, 就跑不完了。")
doc.h3("Intuition: 二分答案")
doc.p("这道题没有一个可以二分的数组。但是看\"k 能不能在 h 小时内吃完\"这个问题:")
nc.bullets(doc, "k 越大, 吃得越快, 需要的小时数只会越少。",
           "所以如果 k 行, 比 k 大的都行; 如果 k 不行, 比 k 小的都不行。",
           "\"k 行不行\" 在 k = 1, 2, 3, ... 上就是 <code>否 否 ... 否 是 是 ... 是</code>。")
doc.p("这正是 first_true 要的形状。二分的对象不是数组下标, 而是<b>答案 k 本身</b>。这叫<b>二分答案</b>。")
doc.p("二分答案的三步:")
nc.steps(doc, "写一个 <code>feasible(k)</code>: 给定一个候选答案, 用 <code>O(n)</code> 判断它行不行。",
         "确定范围: 答案最小可能是多少, 最大可能是多少。这题 k 最小是 1, 最大是 max(piles) (每小时吃完最大的一堆, 一定够)。",
         "在这个范围上用 first_true 找第一个 feasible 的 k。")
doc.h3("算法")
nc.steps(doc, "<code>feasible(k) = sum(ceil(p / k) for p in piles) <= h</code>。",
         "<code>first_true(1, max(piles) + 1, feasible)</code>。")
doc.svg(SLUG + "/koko_core.svg", "总小时数随 k 增大而不增; feasible(k) = 小时数 ≤ h, 是\"前面全否、后面全是\"。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/koko_trace.svg", "piles = [3,6,7,11], h = 8: 在 [1, 11] 上 4 步, 每步写出小时数的加法, 和 8 比较。")
doc.h3("复杂度")
doc.p("Time <code>O(n log max(piles))</code>: 二分 <code>log max(piles)</code> 轮, 每轮 feasible 是 <code>O(n)</code>。Space <code>O(1)</code>。")
nc.solution(doc, CODE_KOKO)
doc.note("答案有范围, 能 O(n) 验证一个候选值, 而且候选值越大越容易满足: 对答案二分。")

# ================================================================ 6
doc.h2("6. Capacity To Ship Packages Within D Days")
doc.h3("题目在问什么")
doc.p("包裹 <code>weights</code> 按顺序装船, 每天开一船, 一船最多装 cap 的重量。不能拆包裹, 也不能改顺序。要在 <code>days</code> 天内运完, 求最小的 cap。")
doc.h3("看例子")
doc.svg(SLUG + "/ship_examples.svg", "例子: cap = 15 刚好 5 天, cap = 14 要 6 天。")
doc.h3("Brute force")
doc.p("从 cap = max(weights) 开始往上试, 每个 cap 模拟一遍装船 <code>O(n)</code>, 最多试到 sum(weights)。<code>O(n × sum)</code>。")
doc.h3("Intuition: 和第 5 题一样, 只换 feasible")
doc.p("cap 越大, 每船装得越多, 需要的天数只会越少。所以\"cap 行不行\"也是\"前面全否、后面全是\", 可以二分答案。")
doc.p("唯一不同的是 feasible 怎么写: 给定 cap, 最少要几天? 用贪心: 从头开始装, 当前这船装得下就装, 装不下就开下一船。这样用的天数一定最少。")
doc.p("范围: cap 至少是 max(weights) (最重的包裹要装得下), 最多是 sum(weights) (一天全运完)。")
doc.h3("算法")
nc.steps(doc, "<code>feasible(cap)</code>: 贪心装船, 数天数, 判断 ≤ days。",
         "<code>first_true(max(weights), sum(weights) + 1, feasible)</code>。")
doc.svg(SLUG + "/ship_core.svg", "cap = 14 要 6 天 (否), cap = 15 刚好 5 天 (是)。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/ship_trace.svg", "5 步, 每步写出每天装了哪些包裹、一共几天。")
doc.h3("复杂度")
doc.p("Time <code>O(n log(sum))</code>, Space <code>O(1)</code>。")
nc.solution(doc, CODE_SHIP)
doc.note("feasible 可以是任何 O(n) 的验证, 公式或者贪心。范围下限是\"单个元素必须放得下\", 上限是\"全部放在一起\"。")

# ================================================================ 7
doc.h2("7. Split Array Largest Sum")
doc.h3("题目在问什么")
doc.p("把数组 <code>nums</code> 切成 k 段连续的 subarray。每段有一个和, 其中最大的那个叫\"最大段和\"。怎么切能让最大段和最小? 返回这个最小值。")
doc.h3("看例子")
doc.svg(SLUG + "/split_examples.svg", "例子。")
doc.h3("Brute force")
doc.p("枚举所有切法: 在 n - 1 个空隙里选 k - 1 个切, 组合数很大。也可以用 DP, <code>O(k·n²)</code>。")
doc.p("浪费: 题目最后要的只是一个<b>数</b> (最小的最大段和), 却在枚举所有的切法。")
doc.h3("Intuition: 反过来问")
doc.p("把问题反过来: \"<b>如果每段的和都不能超过 x, 最少要切几段?</b>\" 这个可以贪心回答: 从头开始加, 加上下一个数会超过 x 就另起一段。")
doc.p("x 越大, 需要的段数只会越少。所以\"最少段数 ≤ k\" 在 x 上是\"前面全否、后面全是\"。第一个\"是\"的 x 就是答案。")
doc.p("你会发现这和第 6 题是<b>同一道题</b>: days 就是 k, cap 就是 x, weights 就是 nums。代码一行不差。")
doc.p("\"最小的最大值\" (minimize the maximum) 是二分答案最典型的信号。")
doc.h3("算法")
nc.steps(doc, "<code>feasible(x)</code>: 贪心切段, 段数 ≤ k 就是 True。",
         "<code>first_true(max(nums), sum(nums) + 1, feasible)</code>。")
doc.svg(SLUG + "/split_core.svg", "x = 17 要 3 段 (否), x = 18 要 2 段 (是), 答案 18。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/split_trace.svg", "在 [10, 32] 上 4 步, 每步贪心切段并写出每段的和。")
doc.p("反过来的\"最大的最小值\" (比如 Magnetic Force Between Two Balls): x 越大越难满足, 形状是\"前面全是、后面全否\", 要找<b>最后一个\"是\"</b>。用 <code>last_true</code> (代码里有)。")
doc.h3("复杂度")
doc.p("Time <code>O(n log(sum))</code>, 比 DP 的 <code>O(k·n²)</code> 快很多。Space <code>O(1)</code>。")
nc.solution(doc, CODE_SPLIT, CODE_LAST_TRUE)
doc.note("\"最小的最大值\": 二分这个最大值 x, 贪心验证。\"最大的最小值\": 同理, 找最后一个满足的。")

# ================================================================ 8
doc.h2("8. Search a 2D Matrix")
doc.h3("题目在问什么")
doc.p("m × n 的矩阵, 每行从小到大, 而且每行的第一个数大于上一行的最后一个数。判断 <code>target</code> 在不在矩阵里, 要求 <code>O(log(m·n))</code>。")
doc.h3("看例子")
doc.svg(SLUG + "/matrix_examples.svg", "例子。")
doc.h3("Brute force")
doc.p("全部扫一遍, <code>O(m·n)</code>。")
doc.h3("Intuition: 当成一维数组")
doc.p("题目的两个条件合起来, 意思是: 按行连起来读, 就是一个排好序的、长度 m·n 的一维数组。")
doc.p("不需要真的把它拼出来。一维的下标 i 对应矩阵的第 <code>i // n</code> 行、第 <code>i % n</code> 列。然后就是第 1 题的二分。")
doc.h3("算法")
nc.steps(doc, "在 <code>[0, m·n)</code> 上找第一个 <code>matrix[i // n][i % n] >= target</code> 的 i。",
         "i 没越界, 而且那个位置等于 target, 返回 True。")
doc.svg(SLUG + "/matrix_core.svg", "3 × 4 矩阵按行拼成长度 12 的一维数组; 一维下标 5 对应 (1, 1)。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/matrix_trace.svg", "target = 11: 4 步, 每步标出 mid 对应矩阵里的哪个格子。")
doc.h3("复杂度")
doc.p("Time <code>O(log(m·n))</code>, Space <code>O(1)</code>。")
doc.p("变体 Search a 2D Matrix II 只保证每行、每列各自排好序, 拼不成一维。那题不用二分: 从右上角出发, 当前数比 target 大就往左, 比 target 小就往下, <code>O(m + n)</code>。")
nc.solution(doc, CODE_MATRIX)
doc.note("每行排好序且行首 > 上一行行尾: 当成一维, 下标用 // n 和 % n 换算。")

# ================================================================ 9
doc.h2("9. Median of Two Sorted Arrays (简述)")
doc.h3("题目在问什么")
doc.p("两个排好序的数组 A 和 B, 求它们合并之后的中位数。要求 <code>O(log(m + n))</code>。")
doc.h3("看例子")
doc.svg(SLUG + "/median_examples.svg", "两个例子。")
doc.h3("Brute force")
doc.p("合并两个数组 (02 里的 merge), 取中间。<code>O(m + n)</code>。")
doc.h3("Intuition: 二分\"左半边从 A 拿几个\"")
doc.p("中位数只取决于一件事: 合并后的数组怎么分成\"左半\"和\"右半\"。左半一共要放 <code>half = (m + n + 1) // 2</code> 个数。")
doc.p("如果左半从 A 拿 i 个 (A 的前 i 个), 那从 B 就要拿 <code>j = half - i</code> 个。所以只有一个未知数 i。")
doc.p("i 对不对, 看交界处的 4 个数: 要求 <code>A[i-1] ≤ B[j]</code> 并且 <code>B[j-1] ≤ A[i]</code> (左半的最大值不超过右半的最小值)。"
      "如果 <code>A[i-1] > B[j]</code>, 说明 A 拿多了, i 要变小; 否则 i 可以变大。这又是一个可以二分的条件。")
doc.p("找到 i 之后, 中位数就是左半最大值 (总数是奇数时), 或者左半最大值和右半最小值的平均 (偶数时)。")
doc.svg(SLUG + "/median_core.svg", "分割点 i = 4, j = 2: 左半一共 6 个数, 只需要检查圈出来的 4 个数。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/median_trace.svg", "3 步找到 i = 4。")
doc.h3("复杂度")
doc.p("Time <code>O(log min(m, n))</code>: 在较短的数组上二分。Space <code>O(1)</code>。")
nc.solution(doc, CODE_MEDIAN)
doc.note("二分的对象可以是\"分割点\"。先把问题写成\"某个整数变量上的、前面全否后面全是的条件\", 剩下就是 first_true。")

# ================================================================ 识别信号
doc.h2("10. 识别信号: 看到什么, 就想到 Binary Search")
nc.table(doc, ["题目特征", "做法", "complexity"], [
    ["排好序的数组, 找值 / 插入位置 / 第一个、最后一个", "first_true, pred = nums[i] >= x 或 > x", "<code>O(n)</code> → <code>O(log n)</code>"],
    ["排好序的数组被旋转过", "和 nums[-1] 比; 或者判断哪半有序", "<code>O(n)</code> → <code>O(log n)</code>"],
    ["没排序, 但有上坡 / 下坡 (peak, mountain)", "比较 nums[mid] 和 nums[mid+1], 往上坡走", "<code>O(n)</code> → <code>O(log n)</code>"],
    ["<b>答案的范围很大 (到 10⁹)</b>, 但给一个候选值能 <code>O(n)</code> 验证", "二分答案: feasible(x) + first_true", "<code>O(n × range)</code> → <code>O(n log range)</code>"],
    ["<b>\"最小的最大值\"</b>: 切段、分天、分配", "二分最大值, 贪心验证", "DP <code>O(k·n²)</code> → <code>O(n log sum)</code>"],
    ["<b>\"最大的最小值\"</b>: 放球、放牛", "二分最小值, 贪心验证, 找最后一个满足的", "<code>O(n log range)</code>"],
    ["矩阵每行排好序且行首 > 上一行行尾", "拉成一维, // n 和 % n", "<code>O(m·n)</code> → <code>O(log(m·n))</code>"],
    ["两个排好序的数组, 求第 k 个 / 中位数", "对较短数组的分割点二分", "<code>O(m + n)</code> → <code>O(log min(m, n))</code>"]])
doc.p("写之前问自己三个问题: pred 是什么, 是\"前面全否、后面全是\"吗? 搜索范围是什么, 答案一定在里面吗? 要找的是第一个\"是\", 还是最后一个\"是\"?")

doc.h2("以后再学")
doc.p("浮点数二分 (固定迭代次数); Single Element in a Sorted Array (按下标奇偶二分); Kth Smallest Element in a Sorted Matrix (对值二分 + 数个数)。")
