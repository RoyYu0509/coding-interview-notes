# 09 · Heap / Top-K 正文 (NeetCode 式讲法)。由 09_heap.py 的 build() exec。
import heapq
import nclib as nc
from collections import Counter, deque
from counts import cnt

EX = os.path.join(d.ROOT, "docs", "svg", "09-heap", "%s_examples.svg")
ns = {"heapq": heapq, "Counter": Counter, "deque": deque}
for _c in (C_KTH, C_TOPK, C_CLOSEST, C_MEDIAN, C_HIRE, C_TASK):
    exec(_c, ns)

# ---------------------------------------------------------------- 例子图
assert ns["findKthLargest"]([3, 2, 1, 5, 6, 4], 2) == 5 and ns["findKthLargest"]([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
nc.examples_svg(EX % "kth_largest", "Kth Largest examples", ["找数组里第 k 大的数 (按排好序之后的位置算, 重复的数也各占一个位置)"], [
    dict(title="Example 1:  nums = [3,2,1,5,6,4], k = 2  →  5", items=[3, 2, 1, 5, 6, 4], hl=[3],
         extra=["从大到小排: 6, 5, 4, 3, 2, 1 → 第 2 个是 5"]),
    dict(title="Example 2:  nums = [3,2,3,1,2,4,5,5,6], k = 4  →  4", items=[3, 2, 3, 1, 2, 4, 5, 5, 6], hl=[5],
         extra=["从大到小排: 6, 5, 5, 4, ... → 第 4 个是 4。两个 5 各算一个"])],
    legend=[("new", "答案")])

assert sorted(ns["topKFrequent"]([1, 1, 1, 2, 2, 3], 2)) == [1, 2]
nc.examples_svg(EX % "top_k_frequent", "Top K Frequent examples", ["返回出现次数最多的 k 个数 (顺序随意)"], [
    dict(title="Example:  nums = [1,1,1,2,2,3], k = 2  →  [1, 2]", items=[1, 1, 1, 2, 2, 3], hl=[0, 1, 2, 3, 4],
         extra=["1 出现 3 次, 2 出现 2 次, 3 出现 1 次 → 次数最多的两个是 1 和 2"])],
    legend=[("new", "答案里的数")])

assert sorted(ns["kClosest"]([[3, 3], [5, -1], [-2, 4]], 2)) == [[-2, 4], [3, 3]]
nc.examples_svg(EX % "k_closest", "K Closest Points examples", ["平面上一些点, 返回离原点 (0, 0) 最近的 k 个 (顺序随意)。距离用 x² + y² 比较就行, 不用开根号"], [
    dict(title="Example:  points = [[3,3],[5,-1],[-2,4]], k = 2  →  [[3,3],[-2,4]]", items=["(3,3)", "(5,-1)", "(-2,4)"],
         cw=70, hl=[0, 2], extra=["距离²: 9 + 9 = 18;  25 + 1 = 26;  4 + 16 = 20 → 最小的两个是 18 和 20"])],
    legend=[("new", "答案")])

nc.examples_svg(EX % "merge_k_lists", "Merge k Sorted Lists examples", ["k 条各自排好序的 linked list, 合并成一条排好序的 linked list"], [
    dict(title="Example:  [[1,4,5],[1,3,4],[2,6]]  →  [1,1,2,3,4,4,5,6]", index=False, rows=[
        ("list 0", [1, 4, 5], None), ("list 1", [1, 3, 4], None), ("list 2", [2, 6], None),
        ("结果", [1, 1, 2, 3, 4, 4, 5, 6], ["new"] * 8)])],
    legend=[("new", "合并后")])

mf = ns["MedianFinder"]()
mf.addNum(1); mf.addNum(2)
assert mf.findMedian() == 1.5
mf.addNum(3)
assert mf.findMedian() == 2
nc.examples_svg(EX % "median_stream", "Find Median from Data Stream examples",
                ["数一个一个地进来 (addNum), 随时可能被问\"目前所有数的中位数是多少\" (findMedian)"], [
    dict(title="Example:  addNum(1), addNum(2), findMedian → 1.5, addNum(3), findMedian → 2", index=False, rows=[
        ("有 2 个数", [1, 2], ["new", "new"]), ("有 3 个数", [1, 2, 3], ["keep", "new", "keep"])],
         extra=["偶数个: 中间两个的平均 (1 + 2) / 2 = 1.5;  奇数个: 正中间那个 2",
                "难点: 数一直在增加, 每次 findMedian 都排序太慢"])],
    legend=[("new", "决定中位数的数")])

assert ns["mincostToHireWorkers"]([10, 20, 5], [70, 50, 30], 2) == 105
assert ns["mincostToHireWorkers"]([10, 20, 5, 8, 9], [20, 60, 20, 40, 63], 3) == 115
nc.examples_svg(EX % "min_cost_hire", "Minimum Cost to Hire K Workers examples",
                ["每个 worker 有 quality q 和最低工资 wage。雇 k 个人, 规则: 1) 每人工资和 q 成正比 (同一个 rate);",
                 "2) 每人拿到的不低于自己的 wage。求最少要付多少钱"], [
    dict(title="Example:  quality = [10,20,5], wage = [70,50,30], k = 2  →  105",
         items=["q=10 w=70", "q=20 w=50", "q=5 w=30"], cw=100, hl=[0, 2],
         extra=["每人的 rate = wage / q: 7, 2.5, 6。雇 0 和 2: 要满足 0 号, rate 至少 7",
                "付 7 × 10 + 7 × 5 = 7 × (10 + 5) = 105。雇 0 和 1: 7 × 30 = 210;  雇 1 和 2: 6 × 25 = 150"])],
    legend=[("new", "雇的人")])

assert ns["leastInterval"](list("AAABBB"), 2) == 8 and ns["leastInterval"](list("AAABBC"), 2) == 7
nc.examples_svg(EX % "task_scheduler", "Task Scheduler examples",
                ["CPU 每个时间单位做一个 task 或者 idle。同一种 task 两次之间至少隔 n 个单位。求做完所有 task 最少要多少单位"], [
    dict(title="Example 1:  tasks = [A,A,A,B,B,B], n = 2  →  8", items=["A", "B", "idle", "A", "B", "idle", "A", "B"],
         cw=44, extra=["A 和 A 之间隔了 2 个单位。B 也一样。中间没别的可做, 只好 idle"]),
    dict(title="Example 2:  tasks = [A,A,A,B,B,C], n = 2  →  7", items=["A", "B", "C", "A", "B", "idle", "A"], cw=44,
         extra=["C 填进了第一个空当"])],
    legend=[])

# ================================================================ HTML
doc = d.Doc("09 · Heap / Top-K")
doc.h2("这篇讲什么")
doc.p("很多题需要<b>反复拿出当前最小 (或最大) 的那一个</b>, 或者只关心\"前 k 大\"。最直接的做法是排序, <code>O(n log n)</code>; 如果数据不断变化, 每次都重新排序就更慢。")
doc.p("<b>Heap</b> (堆, Python 里是 <code>heapq</code>) 是专门干这件事的数据结构。它只保证一件事: <b>堆顶是最小的</b>。其他元素之间的顺序它不管。正因为管得少, 所以快:")
nc.bullets(doc, "看堆顶: <code>h[0]</code>, <code>O(1)</code>", "放一个进去: <code>heappush</code>, <code>O(log n)</code>", "拿走堆顶: <code>heappop</code>, <code>O(log n)</code>")
doc.p("你可以把 heap 画成一棵 tree: 每个节点都比它的子节点小, 所以最上面的根就是最小的。")
doc.svg(SV + "heap_core.svg", "heap 保证 top 最小, 不保证全序; push / pop 只沿一条路径换位置, 所以是 O(log n)。")
doc.p("Python 的 heapq 只有 min-heap。要 max-heap, 就存 <code>-x</code>, 拿出来再取负。图里一律画原来的正数。")
nc.solution(doc, C_TEMPLATE, summary="heapq 常用写法")
nc.table(doc, ["#", "题目", "考过的公司数", "相比上一题多了什么"], [
    ["1", "Kth Largest Element in an Array", cnt("Kth Largest Element in an Array"), "模板题: 只留 k 个"],
    ["2", "Top K Frequent Elements", cnt("Top K Frequent Elements"), "比较的东西换成出现次数"],
    ["3", "K Closest Points to Origin", cnt("K Closest Points to Origin"), "要留最小的 k 个, 方向反过来"],
    ["4", "Merge k Sorted Lists", cnt("Merge k Sorted Lists"), "heap 里只放每条 list 的头"],
    ["5", "Find Median from Data Stream", cnt("Find Median from Data Stream"), "两个 heap 各管一半"],
    ["6", "Minimum Cost to Hire K Workers", cnt("Minimum Cost to Hire K Workers"), "一个维度排序, 另一个维度用 heap"],
    ["7", "Task Scheduler", cnt("Task Scheduler"), "greedy: 每次选剩得最多的, 用过的要冷却"]])
doc.p("每道题的顺序: <b>题目在问什么 → 看例子 → brute force → intuition → 算法 → 手动走一遍 → 复杂度</b>。代码放在最后, 默认折叠。")

# ================================================================ 1
doc.h2("1. Kth Largest Element in an Array")
doc.h3("题目在问什么")
doc.p("给一个整数数组 <code>nums</code> 和 k, 返回第 k 大的数。\"第 k 大\" 是按从大到小排好之后的第 k 个, 重复的数也各占一个位置。")
doc.h3("看例子")
doc.svg(SV + "kth_largest_examples.svg", "两个例子。")
doc.h3("Brute force")
doc.p("排序, 取 <code>nums[-k]</code>。<code>O(n log n)</code>。")
doc.p("浪费在哪: 排序把所有 n 个数的顺序都排出来了, 但我们只关心最大的 k 个, 而且这 k 个之间的顺序也不重要, 只要知道其中最小的那个。")
doc.h3("Intuition: 只留最大的 k 个, 用 min-heap")
doc.p("从左往右扫, 手里只留\"目前见过的最大的 k 个数\"。扫完之后, 这 k 个里<b>最小</b>的那个就是第 k 大。")
doc.p("每来一个新数, 怎么更新手里的 k 个? 先放进来, 变成 k + 1 个, 再把最小的那个扔掉。")
doc.p("\"扔掉最小的\" 和 \"看最小的\" 正是 <b>min-heap</b> 擅长的: 堆顶就是最小的。")
doc.p("这里容易糊涂: 求的是\"大\", 用的却是 min-heap。原因是 heap 的堆顶应该是<b>下一个要被扔掉的</b>。要留下大的, 就扔小的, 所以堆顶要是最小的。")
doc.h3("算法")
nc.steps(doc, "<code>h = []</code>。", "每个 x: <code>heappush(h, x)</code>; 如果 <code>len(h) > k</code>, <code>heappop(h)</code>。", "返回 <code>h[0]</code>。")
doc.svg(SV + "kth_largest_core.svg", "为什么是 min-heap: 堆顶 = 留下的 k 个里最小的 = 第 k 大, 也是下一个要被踢掉的。")
doc.h3("手动走一遍")
doc.svg(SV + "kth_largest_trace.svg", "k = 2: 每步 push, 超过 2 个就 pop 最小的, heap 里一直是目前最大的 2 个。")
doc.h3("复杂度")
doc.p("Time <code>O(n log k)</code>: n 次 push / pop, heap 最多 k + 1 个元素。Space <code>O(k)</code>。k 远小于 n 时比排序快很多。")
doc.p("另有 quickselect, 平均 <code>O(n)</code>, 但最坏 <code>O(n²)</code>, 面试里提一句就行。")
nc.solution(doc, C_KTH)
doc.note("求最大的 k 个 / 第 k 大: 用大小为 k 的 min-heap。堆顶是\"下一个要被踢掉的\"。")

doc.h2("把第 1 题抽象一下: 什么时候用 heap, 用哪个方向")
doc.p("第 1 题的规律:")
nc.bullets(doc, "<b>只关心最值, 不关心全部顺序</b>, 或者<b>数据在不断变化, 要反复取最值</b>, 就用 heap 代替排序。",
           "要<b>留下最大的 k 个</b>, 就扔最小的, 用 <b>min-heap</b>。要<b>留下最小的 k 个</b>, 就扔最大的, 用 <b>max-heap</b>。",
           "一句话: 堆顶永远放\"最该被扔掉的那个\"。")
doc.note("heap 的方向: 堆顶 = 最该被扔掉的。留大的 → min-heap; 留小的 → max-heap。")

# ================================================================ 2
doc.h2("2. Top K Frequent Elements")
doc.h3("题目在问什么")
doc.p("返回数组里<b>出现次数最多</b>的 k 个数。顺序随意。")
doc.h3("看例子")
doc.svg(SV + "top_k_frequent_examples.svg", "例子。")
doc.h3("Brute force")
doc.p("用 Counter 数出每个数的次数, 按次数排序, 取前 k 个。<code>O(m log m)</code>, m 是不同的数的个数。")
doc.h3("Intuition: 先数次数, 再套第 1 题")
doc.p("数完次数之后, 问题就变成: 在 <code>(次数, 数)</code> 这些 pair 里, 找次数最大的 k 个。这正是第 1 题, 只是比较的东西从\"数本身\"换成了\"次数\"。")
doc.p("Python 的 tuple 从左往右比较, 所以把 <code>(count, num)</code> 放进 heap, 就是按 count 比。")
doc.h3("算法")
nc.steps(doc, "<code>c = Counter(nums)</code>。", "对每个 <code>(num, count)</code>: push <code>(count, num)</code>, 超过 k 个就 pop。", "返回 heap 里所有的 num。")
doc.svg(SV + "top_k_frequent_core.svg", "Counter 把问题变成\"在 count 上找最大的 k 个\", 和第 1 题一样。")
doc.h3("手动走一遍")
doc.svg(SV + "top_k_frequent_trace.svg", "4 个不同的数, k = 2, 每步 pop 掉 count 最小的。")
doc.h3("复杂度")
doc.p("Time <code>O(n + m log k)</code>, Space <code>O(m)</code>。另有 bucket sort 的 <code>O(n)</code> 做法: 次数最多是 n, 开 n + 1 个桶, 按次数放进桶, 从后往前取。")
nc.solution(doc, C_TOPK)
doc.note("Top K 按某个属性: 先算出属性 (Counter), 再用 (属性, 元素) 进 heap。")

# ================================================================ 3
doc.h2("3. K Closest Points to Origin")
doc.h3("题目在问什么")
doc.p("平面上有一些点, 返回离原点最近的 k 个。距离只用来比较大小, 所以用 <code>x² + y²</code> 就行, 不用开根号。")
doc.h3("看例子")
doc.svg(SV + "k_closest_examples.svg", "例子。")
doc.h3("Brute force")
doc.p("按距离排序, 取前 k 个, <code>O(n log n)</code>。")
doc.h3("Intuition: 方向反过来, 用 max-heap")
doc.p("这次要留<b>最小</b>的 k 个 (最近的)。按上一节的规律: 留小的 → 扔大的 → 堆顶要是最大的 → <b>max-heap</b>。")
doc.p("Python 里存 <code>(-距离², x, y)</code>, 这样最远的点在堆顶, 超过 k 个就把它 pop 掉。")
doc.h3("算法")
nc.steps(doc, "每个点: push <code>(-(x² + y²), x, y)</code>; 超过 k 个就 pop。", "返回 heap 里的点。")
doc.svg(SV + "k_closest_core.svg", "同一条规则两个方向: 要留大的 → 踢最小的 → min-heap; 要留小的 → 踢最大的 → max-heap。")
doc.h3("手动走一遍")
doc.svg(SV + "k_closest_trace.svg", "k = 2: heap 里画的是正的距离 d, 堆顶是最大的 d (代码里存的是 -d)。")
doc.h3("复杂度")
doc.p("Time <code>O(n log k)</code>, Space <code>O(k)</code>。")
nc.solution(doc, C_CLOSEST)
doc.note("留最小的 k 个: max-heap (Python 里存负数)。")

# ================================================================ 4
doc.h2("4. Merge k Sorted Lists")
doc.h3("题目在问什么")
doc.p("给 k 条 linked list, 每条都已经从小到大排好。把它们合并成一条排好序的 linked list。")
doc.h3("看例子")
doc.svg(SV + "merge_k_lists_examples.svg", "例子。")
doc.h3("Brute force")
doc.p("把所有节点的值收集起来, 排序, 再串成一条 list。N 是节点总数, <code>O(N log N)</code>。")
doc.p("另一种: 每次扫一遍 k 条 list 的头, 找最小的接到结果后面。每接一个要扫 k 个, <code>O(N·k)</code>。")
doc.h3("Intuition: 下一个最小的, 一定是某条 list 的头")
doc.p("因为每条 list 自己是排好序的, 所以所有剩下的节点里最小的那个, 一定是某条 list 当前的<b>头</b>。")
doc.p("所以只需要在 k 个头里找最小的。上面第二种 brute force 每次扫 k 个太慢; 用 heap 存这 k 个头, 每次 pop 就是 <code>O(log k)</code>。")
doc.p("pop 出一个节点之后, 它所在的那条 list 的下一个节点成为新的头, push 进 heap。heap 里始终最多 k 个元素。")
doc.h3("算法")
nc.steps(doc, "把每条 list 的头 push 进 heap, 存 <code>(val, i, node)</code>。i 是 list 的编号, 用来在 val 相同时比较 (node 本身不能比大小)。",
         "当 heap 不空: pop 出最小的, 接到结果后面; 如果它有 next, 把 next push 进去。")
doc.svg(SV + "merge_k_lists_core.svg", "heap 里只有每条 list 的头, 每个节点进出 heap 各一次。")
doc.h3("手动走一遍")
doc.svg(SV + "merge_k_lists_trace.svg", "先 push 3 个头, 每步 pop 最小的接到结果, 再 push 它的 next。")
doc.h3("复杂度")
doc.p("Time <code>O(N log k)</code>, Space <code>O(k)</code>。")
nc.solution(doc, C_MERGE)
doc.note("k 路归并: heap 里只放每一路当前的头, pop 一个就 push 它的下一个。")

# ================================================================ 5
doc.h2("5. Find Median from Data Stream")
doc.h3("题目在问什么")
doc.p("设计一个数据结构: <code>addNum(x)</code> 加入一个数, <code>findMedian()</code> 返回目前所有数的中位数。两个操作会交替调用很多次。")
doc.h3("看例子")
doc.svg(SV + "median_stream_examples.svg", "例子。")
doc.h3("Brute force")
doc.p("用 list 存所有数, findMedian 时排序取中间, <code>O(n log n)</code>。或者每次 addNum 用插入保持有序, 插入是 <code>O(n)</code>。")
doc.h3("Intuition: 中位数只取决于中间那两个数")
doc.p("把所有数分成两半: 较小的一半和较大的一半。中位数只和\"较小一半的最大值\"与\"较大一半的最小值\"有关。")
doc.p("所以用两个 heap:")
nc.bullets(doc, "<code>lo</code>: 较小的一半, 用 <b>max-heap</b>, 堆顶是这一半的最大值。",
           "<code>hi</code>: 较大的一半, 用 <b>min-heap</b>, 堆顶是这一半的最小值。",
           "保持 lo 的个数等于 hi, 或者比 hi 多 1。")
doc.p("中位数: 总数是奇数, 就是 lo 的堆顶; 偶数, 就是两个堆顶的平均。")
doc.p("加一个数时, 要保证 lo 里所有数都 ≤ hi 里所有数。简单的办法: 先放进 lo, 再把 lo 的最大值移到 hi; 如果 hi 比 lo 多了, 再把 hi 的最小值移回 lo。")
doc.h3("算法")
nc.steps(doc, "addNum(x): push x 进 lo; 把 lo 的堆顶 pop 出来 push 进 hi; 如果 <code>len(hi) > len(lo)</code>, 把 hi 的堆顶移回 lo。",
         "findMedian: lo 多一个就返回 lo 的堆顶, 否则返回两个堆顶的平均。")
doc.svg(SV + "median_stream_core.svg", "lo 和 hi 各管一半, 两个堆顶就是正中间的那两个数。")
doc.h3("手动走一遍")
doc.svg(SV + "median_stream_trace.svg", "每一步绿色的节点是这一步换了 heap 的元素; 最后一列是当前的中位数。")
doc.h3("复杂度")
doc.p("addNum <code>O(log n)</code>, findMedian <code>O(1)</code>。Space <code>O(n)</code>。")
nc.solution(doc, C_MEDIAN)
doc.note("动态的中位数: 两个 heap, 较小的一半用 max-heap, 较大的一半用 min-heap, 个数差不超过 1。")

# ================================================================ 6
doc.h2("6. Minimum Cost to Hire K Workers")
doc.h3("题目在问什么")
doc.p("每个 worker 有 quality <code>q</code> 和最低工资 <code>wage</code>。要雇 k 个人, 两条规则: (1) 每个人的工资和他的 q <b>成正比</b>, 也就是大家用同一个单价 rate, 工资 = rate × q; (2) 每个人拿到的不能低于他自己的 wage。求最少要付多少钱。")
doc.h3("看例子")
doc.svg(SV + "min_cost_hire_examples.svg", "例子。")
doc.p("从例子里能看出: 一组人选定之后, rate 必须满足组里<b>要求最高</b>的那个人, 也就是组里最大的 <code>wage / q</code>。总工资 = <code>rate × total_q</code>, total_q 是组里所有人的 q 相加。")
doc.h3("Brute force")
doc.p("枚举所有 k 人组合, 每组算 <code>max(rate) × total_q</code>, 取最小。组合数 <code>C(n, k)</code>, 指数级。")
doc.p("难在两个量互相牵制: 想让 rate 小, 就要挑 rate 小的人; 想让 total_q 小, 就要挑 q 小的人。这两件事经常冲突。")
doc.h3("Intuition: 先固定一个维度")
doc.p("先把所有人按 rate 从小到大排序。然后从左往右, 依次考虑\"<b>让当前这个人当 rate 最高的那个</b>\"。")
doc.p("当前这个人的 rate 是 r, 那组里其他人只能从他左边 (rate 更小的) 挑。rate 已经固定为 r 了, 总工资 = r × total_q, 要让它最小, 就只能让 total_q 最小。")
doc.p("所以问题变成: <b>在目前见过的人里, 挑 q 最小的 k 个</b>。这是第 3 题: 留最小的 k 个 → 用 max-heap 存 q, 超过 k 个就 pop 掉最大的 q。")
doc.p("每一步, heap 里是 q 最小的 k 个人, total_q 是 heap 里所有 q 相加, 算一次 <code>r × total_q</code>, 取所有步里的最小值。")
doc.h3("算法")
nc.steps(doc, "按 <code>wage / q</code> 从小到大排序。",
         "从左往右, 对每个人: push 他的 q 进 max-heap, <code>total_q += q</code>。",
         "如果 heap 超过 k 个: pop 最大的 q, <code>total_q -= 它</code>。",
         "如果 heap 正好 k 个: <code>ans = min(ans, rate × total_q)</code>。")
doc.svg(SV + "min_cost_hire_core.svg", "按 rate 排序, 固定一个维度; heap 里留 q 最小的 k 个, 压低 total_q。")
doc.h3("手动走一遍")
doc.svg(SV + "min_cost_hire_trace.svg", "quality = [10,20,5,8,9], wage = [20,60,20,40,63], k = 3: A 到 E 按 rate 升序。每步 push, 超过 3 个就 pop 最大的 q; total_q 写成 heap 里所有 q 相加。最小 115。")
doc.h3("复杂度")
doc.p("Time <code>O(n log n)</code> (排序 + heap)。Space <code>O(n)</code>。")
doc.p("同样的套路 (\"按一个量排序, 往前推进时把现在可选的放进 heap, 堆顶决定选谁\"):")
nc.bullets(doc, "Maximum Number of Events That Can Be Attended: 按开始时间排序, heap 存结束时间, 每天参加结束最早的。",
           "IPO: 按需要的本钱排序, heap 存利润, 每次在做得起的项目里挑利润最大的。")
nc.solution(doc, C_HIRE, C_EVENTS, C_IPO)
doc.note("两个维度互相牵制: 排序固定一个维度, heap 管另一个维度。")

# ================================================================ 7
doc.h2("7. Task Scheduler")
doc.h3("题目在问什么")
doc.p("一串 task (用字母表示), CPU 每个时间单位做一个 task 或者 idle (什么都不做)。<b>同一种 task 两次之间至少要隔 n 个时间单位</b>。task 的顺序可以随便排。求做完所有 task 最少需要多少个时间单位。")
doc.h3("看例子")
doc.svg(SV + "task_scheduler_examples.svg", "两个例子。")
doc.h3("Brute force")
doc.p("枚举所有排列, 检查间隔, 指数级。")
doc.h3("Intuition: 每次做剩得最多的那种")
doc.p("剩得最多的那种 task 最\"危险\": 它需要的间隔最多, 如果拖到最后, 就只剩它一种, 中间只能 idle。所以 greedy: <b>每个时间单位, 都做当前能做的里剩得最多的</b>。")
doc.p("\"能做的里剩得最多的\" 就是 max-heap 的堆顶 (按剩余次数)。")
doc.p("但这次有一个新问题: 做完一种 task 之后, 它要等 n 个单位才能再做。所以不能直接 push 回 heap, 而是放进一个<b>冷却队列</b>, 记下它什么时候可以回来。时间到了再 push 回 heap。")
doc.p("如果某个时间单位 heap 是空的, 但冷却队列里还有, 这个单位就只能 idle。")
doc.h3("算法")
nc.steps(doc, "数每种 task 的次数, 全部放进 max-heap。<code>time = 0</code>, 冷却队列 <code>cool = deque()</code>。",
         "当 heap 或 cool 不空: <code>time += 1</code>。heap 不空就 pop 一个, 次数减 1, 还有剩就放进 cool, 记录 <code>(剩余次数, time + n)</code>。",
         "如果 cool 的队头到时间了 (<code>== time</code>), 把它 push 回 heap。",
         "返回 time。")
doc.svg(SV + "task_scheduler_core.svg", "heap = 现在能做的; cool = 刚做过的; 每个时间单位做 heap 里剩得最多的。")
doc.h3("手动走一遍")
doc.svg(SV + "task_scheduler_trace.svg", "AAABBC, n = 2: 第 6 个单位 heap 空了, 只能 idle 等 A 回来, 一共 7 个单位。")
doc.h3("复杂度")
doc.p("Time <code>O(T log 26)</code>, T 是总时间单位数。Space <code>O(26)</code>。")
doc.p("这题也有公式解: <code>max(len(tasks), (max_count - 1) × (n + 1) + 次数等于 max_count 的种类数)</code>。Reorganize String (相邻字符不能相同) 是 n = 1 的同一个结构。")
nc.solution(doc, C_TASK)
doc.note("每一步选当前最优, 而且候选会变化: greedy + heap。用过的要等一阵才能再用: 再加一个冷却队列。")

# ================================================================ 识别信号
doc.h2("8. 识别信号: 看到什么, 就想到 heap")
nc.table(doc, ["题目特征", "做法", "complexity"], [
    ["第 k 大 / 前 k 个 / 最大的 k 个", "大小为 k 的 min-heap", "<code>O(n log n)</code> → <code>O(n log k)</code>"],
    ["最小的 k 个 / 最近的 k 个", "大小为 k 的 max-heap (存负数)", "<code>O(n log n)</code> → <code>O(n log k)</code>"],
    ["按出现次数 / 某个属性取 top k", "Counter + (属性, 元素) 进 heap", "<code>O(n log k)</code>"],
    ["合并 k 个有序的序列", "heap 里放每一路的头", "<code>O(N·k)</code> → <code>O(N log k)</code>"],
    ["数据流的中位数", "两个 heap 各管一半", "每次 <code>O(n log n)</code> → <code>O(log n)</code>"],
    ["两个维度互相牵制 (rate 和 q、开始和结束)", "排序一维, heap 管另一维", "指数 → <code>O(n log n)</code>"],
    ["每一步选\"当前最优\", 候选在变化", "greedy + heap (+ 冷却队列)", "<code>O(n log n)</code>"],
    ["图上的最短路 (边有权重)", "Dijkstra, heap 存 (距离, 节点) → 12", "<code>O(E log V)</code>"]])

doc.h2("以后再学")
doc.p("quickselect (平均 O(n) 的第 k 大)、lazy delete (Sliding Window Median)、sweep line + heap (The Skyline Problem)。")
doc.write("docs/09-heap.html")
