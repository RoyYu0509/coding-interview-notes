# 10 · Intervals 正文 (NeetCode 式讲法)。由 10_intervals.py 末尾 exec, 共用 CODE / FN / SLUG。
import nclib as nc
from counts import cnt

EX = os.path.join(d.ROOT, "docs", "svg", SLUG, "%s_examples.svg")
TEMPLATES = '''
# A. 按 start 排序, 只和 res[-1] 比        -> 合并 / 冲突检测 / 插入
intervals.sort(key=lambda x: x[0])
for s, e in intervals:
    if res and s <= res[-1][1]: res[-1][1] = max(res[-1][1], e)
    else:                       res.append([s, e])

# B. 按 end 排序, 贪心 (keep_end)          -> 最多保留几个 / 最少箭 / 最少删除
intervals.sort(key=lambda x: x[1])
for s, e in intervals:
    if s >= keep_end: keep_end = e          # 保留; 否则丢掉

# C. 拆成事件, 扫描线                      -> 同一时刻最多几个
events = [(s, 1) for s, e in iv] + [(e, -1) for s, e in iv]
events.sort()                               # 同一时刻 -1 排在 +1 前
for t, delta in events: cur += delta; best = max(best, cur)
'''

# ---------------------------------------------------------------- 例子图
assert FN["merge"]["merge"]([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
assert FN["merge"]["merge"]([[1, 4], [4, 5]]) == [[1, 5]]
nc.examples_svg(EX % "merge", "Merge Intervals examples", ["每个 interval 是 [start, end]。把所有重叠的 interval 合并, 返回合并后的结果"], [
    dict(title="Example 1:  [[1,3],[2,6],[8,10],[15,18]]  →  [[1,6],[8,10],[15,18]]",
         items=["[1,3]", "[2,6]", "[8,10]", "[15,18]"], cw=70, hl=[0, 1],
         extra=["[1,3] 和 [2,6] 重叠 (2 ≤ 3), 合并成 [1,6]。[8,10] 和 [15,18] 不和任何人重叠, 原样保留"]),
    dict(title="Example 2:  [[1,4],[4,5]]  →  [[1,5]]", items=["[1,4]", "[4,5]"], cw=70, hl=[0, 1],
         extra=["首尾相接 (4 = 4) 也算重叠"]),
    dict(title="Example 3:  [[1,4],[0,4]]  →  [[0,4]]", items=["[1,4]", "[0,4]"], cw=70, hl=[0, 1],
         extra=["输入不一定按 start 排好"])],
    legend=[("new", "要合并的")])

assert FN["insert"]["insert"]([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]) == [[1, 2], [3, 10], [12, 16]]
nc.examples_svg(EX % "insert", "Insert Interval examples",
                ["intervals 已经按 start 排好, 而且互不重叠。插入一个新的 interval, 有重叠就合并, 结果仍然有序、不重叠"], [
    dict(title="Example:  intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], new = [4,8]  →  [[1,2],[3,10],[12,16]]",
         items=["[1,2]", "[3,5]", "[6,7]", "[8,10]", "[12,16]"], cw=70, hl=[1, 2, 3],
         extra=["[4,8] 和 [3,5]、[6,7]、[8,10] 都重叠, 四个合并成 [3,10]", "[1,2] 在它左边不碰, [12,16] 在它右边不碰"])],
    legend=[("new", "和 new 重叠的")])

assert FN["erase"]["erase_overlap_intervals"]([[1, 2], [2, 3], [3, 4], [1, 3]]) == 1
assert FN["erase"]["erase_overlap_intervals"]([[1, 2], [1, 2], [1, 2]]) == 2
nc.examples_svg(EX % "erase", "Non-overlapping Intervals examples", ["最少删掉几个 interval, 能让剩下的互不重叠? (首尾相接不算重叠)"], [
    dict(title="Example 1:  [[1,2],[2,3],[3,4],[1,3]]  →  1", items=["[1,2]", "[2,3]", "[3,4]", "[1,3]"], cw=70,
         bad=[(3, 3, "删掉 [1,3]")], extra=["剩下 [1,2] [2,3] [3,4], 都是首尾相接, 不重叠"]),
    dict(title="Example 2:  [[1,2],[1,2],[1,2]]  →  2", items=["[1,2]", "[1,2]", "[1,2]"], cw=70,
         bad=[(1, 2, "三个完全一样, 只能留一个")])],
    legend=[("rem", "删掉的")])

assert FN["arrows"]["find_min_arrow_shots"]([[10, 16], [2, 8], [1, 6], [7, 12]]) == 2
nc.examples_svg(EX % "arrows", "Minimum Number of Arrows examples",
                ["每个气球占 x 轴上的 [start, end]。在 x 处竖直射一箭, 能射爆所有 start ≤ x ≤ end 的气球。最少几支箭能射爆全部"], [
    dict(title="Example:  [[10,16],[2,8],[1,6],[7,12]]  →  2", items=["[10,16]", "[2,8]", "[1,6]", "[7,12]"], cw=76,
         extra=["x = 6 射爆 [2,8] 和 [1,6];  x = 12 射爆 [10,16] 和 [7,12]"]),
    dict(title="Example 2:  [[1,2],[2,3],[3,4],[4,5]]  →  2", extra=["x = 2 射爆前两个, x = 4 射爆后两个。和上一题不同: 这里碰到边也算 (闭区间)"])],
    legend=[])

assert FN["rooms1"]["can_attend_meetings"]([[0, 30], [5, 10], [15, 20]]) is False
assert FN["rooms1"]["can_attend_meetings"]([[7, 10], [2, 4]]) is True
nc.examples_svg(EX % "rooms1", "Meeting Rooms examples", ["一个人能不能参加所有的会议? 也就是: 所有会议是不是两两不重叠 (首尾相接可以)"], [
    dict(title="Example 1:  [[0,30],[5,10],[15,20]]  →  False", items=["[0,30]", "[5,10]", "[15,20]"], cw=76,
         bad=[(0, 1, "[0,30] 和 [5,10] 撞了")]),
    dict(title="Example 2:  [[7,10],[2,4]]  →  True", items=["[7,10]", "[2,4]"], cw=76, extra=["2..4 开完再去 7..10, 不冲突"])],
    legend=[("rem", "冲突")])

assert FN["rooms2_heap"]["min_meeting_rooms"]([[0, 30], [5, 10], [15, 20]]) == 2
assert FN["rooms2_heap"]["min_meeting_rooms"]([[7, 10], [2, 4]]) == 1
nc.examples_svg(EX % "rooms2", "Meeting Rooms II examples", ["最少需要几间会议室, 才能让所有会议都开得成? 等价于: 同一时刻最多有几个会议在进行"], [
    dict(title="Example 1:  [[0,30],[5,10],[15,20]]  →  2", items=["[0,30]", "[5,10]", "[15,20]"], cw=76,
         extra=["房间 1: [0,30];  房间 2: 先开 [5,10], 结束后再开 [15,20]。同一时刻最多 2 个会"]),
    dict(title="Example 2:  [[7,10],[2,4]]  →  1", extra=["不重叠, 一间就够"])],
    legend=[])

assert FN["intersect"]["interval_intersection"]([[0, 2], [5, 10], [13, 23], [24, 25]], [[1, 5], [8, 12], [15, 24], [25, 26]]) == \
    [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]]
nc.examples_svg(EX % "intersect", "Interval List Intersections examples",
                ["两个列表, 各自按顺序排好、内部不重叠。求它们的交集 (两边都覆盖到的部分)"], [
    dict(title="Example:  A = [[0,2],[5,10],[13,23],[24,25]], B = [[1,5],[8,12],[15,24],[25,26]]", index=False, rows=[
        ("A", ["[0,2]", "[5,10]", "[13,23]", "[24,25]"], None), ("B", ["[1,5]", "[8,12]", "[15,24]", "[25,26]"], None),
        ("交集", ["[1,2]", "[5,5]", "[8,10]", "[15,23]", "[24,24]", "[25,25]"], ["new"] * 6)], cw=76,
         extra=["[5,5] 是一个点: A 的 [5,10] 和 B 的 [1,5] 只在 5 这一点重合"])],
    legend=[("new", "交集")])

nc.examples_svg(EX % "calendar", "My Calendar I examples",
                ["实现 book(start, end): 预订半开区间 [start, end)。如果和已有的预订重叠就拒绝 (返回 False), 否则记下并返回 True"], [
    dict(title="Example:  book(10,20) → True;  book(15,25) → False;  book(20,30) → True", index=False, rows=[
        ("已预订", ["[10,20)", "[20,30)"], ["new", "new"]), ("拒绝", ["[15,25)"], ["rem"])], cw=76,
         extra=["[15,25) 和 [10,20) 在 15..20 重叠, 拒绝", "[20,30) 和 [10,20) 首尾相接: 半开区间里 20 不属于 [10,20), 所以不重叠"])],
    legend=[("new", "成功预订"), ("rem", "被拒绝")])

# ================================================================ HTML
doc = d.Doc("10 · Intervals")
doc.h2("这篇讲什么")
doc.p("interval (区间) 就是一个 <code>[start, end]</code>, 比如一个会议从 9 点开到 11 点。这类题给你一堆区间, 问: 合并重叠的、最少删几个让它们不重叠、同一时刻最多有几个、两组区间的交集……")
doc.p("brute force 通常是把每两个区间都比一下, 看重不重叠, <code>O(n²)</code>。")
doc.p("几乎所有 interval 题的第一步都是<b>排序</b>。排好序之后, 每个区间只需要和\"刚处理过的那一个\"比较, 扫一遍就行, 总共 <code>O(n log n)</code>。整篇的关键问题是: <b>按 start 排还是按 end 排, 以及为什么</b>。")
doc.h3("先说清楚: 两个区间什么时候重叠")
doc.p("两个区间 a 和 b 重叠, 当且仅当 <code>a.start ≤ b.end</code> 并且 <code>b.start ≤ a.end</code>。反过来想更好记: 不重叠, 就是一个完全在另一个的左边 (<code>a.end < b.start</code> 或 <code>b.end < a.start</code>)。")
doc.p("重叠的部分是 <code>[max(两个 start), min(两个 end)]</code>。")
doc.p("还要看题目是闭区间还是半开区间: 闭区间 <code>[1,4]</code> 和 <code>[4,5]</code> 在 4 这一点碰到, 算重叠; 半开区间 <code>[1,4)</code> 和 <code>[4,5)</code> 不算。这决定了代码里写 <code>≤</code> 还是 <code><</code>。")
doc.svg(SLUG + "/overlap_core.svg", "四种位置关系都代入同一个式子。绿色是交集, 红色虚线是空隙。")
nc.table(doc, ["#", "题目", "考过的公司数", "相比上一题多了什么"], [
    ["1", "Merge Intervals", cnt("Merge Intervals"), "模板题: 按 start 排序, 合并"],
    ["2", "Insert Interval", cnt("Insert Interval"), "已经排好了, 插入一个新的"],
    ["3", "Non-overlapping Intervals", cnt("Non-overlapping Intervals"), "最少删几个: 改成按 end 排序"],
    ["4", "Minimum Number of Arrows", cnt("Minimum Number of Arrows to Burst Balloons"), "同一个 greedy, 改一个符号"],
    ["5", "Meeting Rooms", cnt("Meeting Rooms"), "能不能全参加: 只比相邻的"],
    ["6", "Meeting Rooms II", cnt("Meeting Rooms II"), "同一时刻最多几个: heap 或 sweep line"],
    ["7", "Interval List Intersections", cnt("Interval List Intersections"), "两个列表, 双指针"],
    ["8", "My Calendar I", cnt("My Calendar I"), "区间一个一个来, 每次判断"]])
doc.p("每道题的顺序: <b>题目在问什么 → 看例子 → brute force → intuition → 算法 → 手动走一遍 → 复杂度</b>。代码放在最后, 默认折叠。")

# ================================================================ 1
doc.h2("1. Merge Intervals")
doc.h3("题目在问什么")
doc.p("给一组区间 (没有排序), 把所有互相重叠的区间合并成一个, 返回合并之后的区间列表。")
doc.h3("看例子")
doc.svg(SLUG + "/merge_examples.svg", "三个例子。")
doc.h3("Brute force")
doc.p("反复扫描: 找到任意两个重叠的区间就合并, 直到找不到为止。每轮 <code>O(n²)</code> 比较, 可能要很多轮。")
doc.h3("Intuition: 按 start 排好, 只需要和最后一个合并结果比")
doc.p("先按 start 排序。然后从左往右, 一个一个放进结果 res。对当前的区间 cur:")
nc.bullets(doc, "如果 <code>cur.start ≤ res[-1].end</code>: 和 res 里最后一块重叠, 合并进去: <code>res[-1].end = max(res[-1].end, cur.end)</code>。",
           "否则: 不重叠, cur 自己成为新的一块。")
doc.p("为什么只看 res[-1] 就够了? 因为排了序, cur.start 比之前所有区间的 start 都大。如果它连 res[-1] 都够不到 (cur.start > res[-1].end), 那更早的块 (end 更小) 就更够不到了。")
doc.p("合并时一定要取 <code>max</code>: cur 可能整个被 res[-1] 包在里面 (比如 [1,10] 和 [2,3]), 直接写 <code>end = cur.end</code> 会把 10 缩成 3。")
doc.svg(SLUG + "/sort_core.svg", "排序之后, 和 res[-1] 比一次就能知道\"和前面有没有重叠\"。")
doc.h3("算法")
nc.steps(doc, "按 start 排序。", "对每个区间: 和 res[-1] 重叠就合并 (end 取 max), 否则 append。")
doc.svg(SLUG + "/merge_core.svg", "三种情况。第二行: cur 被 res[-1] 整个包住, 如果直接写 end = e 会把大块缩小, 必须取 max。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/merge_trace.svg", "5 个区间, 排序后扫一遍: 第 2 个和第 5 个被并进前一块, 第 3、4 个各自开新的一块。")
doc.h3("复杂度")
doc.p("Time <code>O(n log n)</code> (排序)。Space <code>O(n)</code>。")
nc.solution(doc, CODE["merge"])
doc.note("合并区间: 按 start 排序, 只和 res[-1] 比, 重叠就把 end 取 max。")

# ================================================================ 抽象
doc.h2("把第 1 题抽象一下: 按 start 排, 还是按 end 排")
doc.p("interval 题基本都是\"排序 + 扫一遍\", 区别在按什么排:")
nc.bullets(doc, "<b>按 start 排</b>: 要把区间<b>连起来、拼起来</b> (合并、插入、检查冲突)。排好之后, 后面的区间只可能和最后一块接上。",
           "<b>按 end 排</b>: 要<b>挑尽量多的、互不重叠的</b>区间 (最多保留几个、最少删几个、最少几支箭)。先结束的先选, 给后面留出最多的空间。第 3 题会解释为什么。",
           "<b>拆成事件</b>: 要知道<b>同一时刻有几个</b> (最少几间会议室)。每个 start 是 +1, 每个 end 是 -1, 按时间扫一遍。第 6 题会讲。")
nc.solution(doc, TEMPLATES, summary="三种写法的模板")
doc.note("拼接 → 按 start; 挑最多不重叠的 → 按 end; 同时有几个 → 拆成 +1 / -1 事件。")

# ================================================================ 2
doc.h2("2. Insert Interval")
doc.h3("题目在问什么")
doc.p("给一个已经<b>按 start 排好、互不重叠</b>的区间列表, 再给一个新区间 new。把 new 插进去, 有重叠就合并。返回的结果也要排好、不重叠。")
doc.h3("看例子")
doc.svg(SLUG + "/insert_examples.svg", "例子。")
doc.h3("Brute force")
doc.p("把 new 加进列表, 再做一遍第 1 题: 排序 + 合并。<code>O(n log n)</code>。浪费: 列表本来就排好了, 不需要再排。")
doc.h3("Intuition: 列表被 new 分成三段")
doc.p("因为原来的列表是有序、不重叠的, 所以它按和 new 的关系, 正好分成连续的三段:")
nc.steps(doc, "<b>完全在 new 左边</b> 的 (end < new.start): 原样放进结果。",
         "<b>和 new 重叠</b> 的: 全部并进 new。new 的 start 取最小、end 取最大。",
         "<b>完全在 new 右边</b> 的 (start > new.end): 先把合并好的 new 放进去, 再把它们原样放进去。")
doc.h3("算法")
nc.steps(doc, "i = 0。当 <code>intervals[i].end < new.start</code>: 放进结果, i += 1。",
         "当 <code>intervals[i].start ≤ new.end</code>: <code>new = [min(start), max(end)]</code>, i += 1。",
         "放进 new, 再放进剩下的所有区间。")
doc.svg(SLUG + "/insert_core.svg", "三段的分界线由 new.start 和 new.end 决定。红色的三个区间被 new 吞掉, 合成 [3,10]。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/insert_trace.svg", "new = [4,8]: [1,2] 在左边; [3,5]、[6,7]、[8,10] 依次被吞 (new 从 [4,8] 变成 [3,8] 再变成 [3,10]); [12,16] 在右边。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(n)</code>。")
nc.solution(doc, CODE["insert"])
doc.note("已经排好的列表插入新区间: 左边不碰的、重叠的、右边不碰的, 三段扫一遍。")

# ================================================================ 3
doc.h2("3. Non-overlapping Intervals")
doc.h3("题目在问什么")
doc.p("给一组区间。最少删掉几个, 能让剩下的区间<b>互不重叠</b>? 这题里首尾相接 (比如 [1,2] 和 [2,3]) 不算重叠。")
doc.p("等价的问法: 最多能<b>保留</b>几个互不重叠的区间? 答案 = 总数 - 最多保留数。")
doc.h3("看例子")
doc.svg(SLUG + "/erase_examples.svg", "两个例子。")
doc.h3("Brute force")
doc.p("枚举所有子集, 检查是否互不重叠, 找最大的。<code>O(2ⁿ · n)</code>。")
doc.h3("Intuition: 每次留下最先结束的那个")
doc.p("想象你要在一天里参加尽量多的、时间不冲突的活动。你会先选哪个? 选<b>最早结束</b>的那个。因为它结束得最早, 留给后面的时间最多。")
doc.p("为什么这样不会错? 假设最优解里第一个选的活动不是最早结束的那个 X, 而是 Y。把 Y 换成 X: X 结束得比 Y 早 (或一样), 所以 Y 后面能接的活动, X 后面也都能接。换完之后数量不变, 还是最优。所以选 X 不会吃亏。")
doc.p("那为什么不按 start 排? 反例: 一个很长的区间 [1,11] 最早开始, 但它挡住了后面三个短区间。按 start 选它, 就要删掉 3 个; 按 end 选, 只用删它 1 个。")
doc.h3("算法")
nc.steps(doc, "按 end 排序。<code>keep_end = -∞</code>, <code>removed = 0</code>。",
         "对每个区间: 如果 <code>start ≥ keep_end</code>, 不冲突, 保留它, <code>keep_end = end</code>。",
         "否则冲突, 删掉它 (<code>removed += 1</code>), keep_end 不变。")
doc.svg(SLUG + "/erase_core.svg", "同一组数据。按 start 排, 先选了长的 A (end = 11), 挡住 B、C、D, 删 3 个; 按 end 排, 先选 B, 后面 C、D 首尾相接, 只删 A。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/erase_trace.svg", "keep_end 是已保留的最后一个区间的 end (虚线)。start < keep_end 就删, 否则保留并更新 keep_end。")
doc.h3("复杂度")
doc.p("Time <code>O(n log n)</code>, Space <code>O(1)</code>。")
nc.solution(doc, CODE["erase"])
doc.note("最多保留几个不重叠 / 最少删几个: 按 end 排序, 每次保留最先结束的。")

# ================================================================ 4
doc.h2("4. Minimum Number of Arrows to Burst Balloons")
doc.h3("题目在问什么")
doc.p("每个气球在 x 轴上占一段 <code>[start, end]</code>。在某个 x 处竖直射一支箭, 能射爆所有 <code>start ≤ x ≤ end</code> 的气球。最少需要几支箭, 才能射爆所有气球?")
doc.h3("看例子")
doc.svg(SLUG + "/arrows_examples.svg", "两个例子。")
doc.h3("Brute force")
doc.p("枚举箭的位置组合, 指数级。")
doc.h3("Intuition: 和第 3 题是同一个 greedy")
doc.p("一支箭能射爆的一组气球, 就是一组<b>互相重叠</b>的气球。所以问题变成: 最少分成几组, 每组里的气球有公共点。")
doc.p("还是按 end 排序。第一支箭射在<b>第一个气球的 end</b> 上: 尽量往右射, 才能顺便射到更多后面的气球, 而又不会漏掉第一个。")
doc.p("之后每个气球: 如果它的 start ≤ 当前箭的位置, 已经被射爆了; 否则需要一支新箭, 射在它的 end 上。")
doc.p("和第 3 题只差一个符号: 这题是闭区间, 碰到边也算被射中, 所以判断\"需要新箭\"用 <code>start > arrow_x</code>; 第 3 题首尾相接不算重叠, 用 <code>start ≥ keep_end</code>。")
doc.h3("算法")
nc.steps(doc, "按 end 排序。<code>arrows = 0</code>, <code>arrow_x = -∞</code>。",
         "对每个气球: 如果 <code>start > arrow_x</code>, 新射一箭, <code>arrow_x = end</code>, arrows += 1。")
doc.svg(SLUG + "/arrows_core.svg", "x = 3 在 A 里面, 射中 A、B; 右移到 A 的 end = 6, 射中 A、B、C, 而且不会漏掉任何一个。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/arrows_trace.svg", "5 个气球按 end 排序, 一共开了 3 支箭。")
doc.h3("复杂度")
doc.p("Time <code>O(n log n)</code>, Space <code>O(1)</code>。")
nc.solution(doc, CODE["arrows"])
doc.note("最少几个点能覆盖所有区间: 按 end 排序, 点放在当前区间的 end 上。")

# ================================================================ 5
doc.h2("5. Meeting Rooms")
doc.h3("题目在问什么")
doc.p("给一组会议时间。一个人能不能参加所有会议? 也就是判断所有会议是不是两两都不重叠 (首尾相接可以)。")
doc.h3("看例子")
doc.svg(SLUG + "/rooms1_examples.svg", "两个例子。")
doc.h3("Brute force")
doc.p("每两个会议比一下, <code>O(n²)</code>。")
doc.h3("Intuition: 排好序之后, 只看相邻的两个")
doc.p("按 start 排序。如果有任何两个会议重叠, 那么一定有<b>相邻</b>的两个会议重叠。")
doc.p("为什么? 假设所有相邻的两个都不重叠: 第 1 个在第 2 个开始前结束, 第 2 个在第 3 个开始前结束……它们排成一条链, 一个接一个, 不可能有隔着的两个重叠。")
doc.p("所以只需要检查每对相邻的: <code>intervals[i].start < intervals[i-1].end</code> 就是冲突。")
doc.h3("算法")
nc.steps(doc, "按 start 排序。", "i 从 1 到 n-1: 如果 <code>start[i] < end[i-1]</code>, 返回 False。", "返回 True。")
doc.svg(SLUG + "/rooms1_core.svg", "上: 有重叠时, 相邻的一对一定会先暴露。下: 所有相邻的都首尾相接, 整条链排开, 没有隔着的重叠。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/rooms1_trace.svg", "排序后三对相邻的: 前两对没冲突; (10,13) 和 (12,15) 里 12 < 13, 冲突, 返回 False。")
doc.h3("复杂度")
doc.p("Time <code>O(n log n)</code>, Space <code>O(1)</code>。")
nc.solution(doc, CODE["rooms1"])
doc.note("判断有没有重叠: 按 start 排序, 只比较相邻的两个。")

# ================================================================ 6
doc.h2("6. Meeting Rooms II")
doc.h3("题目在问什么")
doc.p("给一组会议时间, 最少需要几间会议室, 才能让所有会议都开得成?")
doc.p("换个说法: <b>同一时刻, 最多有几个会议在同时进行?</b> 这个最大值就是需要的房间数。")
doc.h3("看例子")
doc.svg(SLUG + "/rooms2_examples.svg", "两个例子。")
doc.h3("Brute force")
doc.p("对每个时间点, 数有几个会议覆盖它, 取最大。时间点很多时很慢。或者每个会议的开始时刻, 数有几个会议正在进行, <code>O(n²)</code>。")
doc.h3("Intuition A: 用 heap 管\"正在用的房间什么时候空出来\"")
doc.p("按 start 排序, 一个一个会议地安排。对新来的会议, 问: 现在有没有房间已经空出来了?")
doc.p("最可能空出来的, 是<b>最早结束</b>的那个房间。所以用一个 min-heap 存每个正在用的房间的结束时间, 堆顶就是最早空出来的。")
nc.bullets(doc, "如果 <code>堆顶 ≤ 新会议的 start</code>: 那个房间已经空了, 复用它: pop 掉旧的结束时间, push 新会议的结束时间。",
           "否则: 没有空房间, 新开一间: 直接 push。",
           "最后 heap 的大小就是房间数。")
doc.svg(SLUG + "/rooms2_core.svg", "t = 17 时 [0,30]、[10,25]、[15,20] 同时在开, 3 场; t = 7 只有 2 场。所有时刻里最大的是 3。")
doc.svg(SLUG + "/rooms2_heap_trace.svg", "heap 画成 tree。每一行: 先 pop (虚线扔到左边, 写明原因), 再 push。")
doc.h3("Intuition B: sweep line (扫描线)")
doc.p("另一种更直接的想法: 把每个会议拆成两个事件, 开始时 +1, 结束时 -1。把所有事件按时间排序, 从左往右扫, 维护当前人数 cur, 记录 cur 的最大值。")
doc.p("同一时刻既有结束又有开始时, 要先算结束 (-1), 再算开始 (+1): 一个会 10 点结束、另一个 10 点开始, 可以用同一个房间。")
doc.svg(SLUG + "/rooms2_sweep_trace.svg", "上: 5 场会议和事件竖线。中: cur 的阶梯, 最高是 3。下: 排序后的 10 个事件, 每格一步; t = 10 处先 -1 再 +1。")
doc.p("两种做法都是 <code>O(n log n)</code>。sweep line 更容易推广 (比如\"最忙的时刻是什么时候\"); heap 做法能顺便知道每个会议分到了哪间房。")
doc.h3("复杂度")
doc.p("Time <code>O(n log n)</code>, Space <code>O(n)</code>。")
nc.solution(doc, CODE["rooms2_heap"], CODE["rooms2_sweep"])
doc.note("同一时刻最多几个: 拆成 +1 / -1 事件扫一遍 (同一时刻先 -1); 或者 min-heap 存结束时间。")

# ================================================================ 7
doc.h2("7. Interval List Intersections")
doc.h3("题目在问什么")
doc.p("两个区间列表 A 和 B, 各自按顺序排好、内部互不重叠。求它们的交集: 所有被 A 和 B 同时覆盖的部分。都是闭区间。")
doc.h3("看例子")
doc.svg(SLUG + "/intersect_examples.svg", "例子。")
doc.h3("Brute force")
doc.p("A 里每个区间和 B 里每个区间都算一下交集, <code>O(m·n)</code>。")
doc.h3("Intuition: 双指针, 先结束的那个往前走")
doc.p("两个列表都是有序的, 就像 02 里的 merge: 各放一个指针 i 和 j。")
nc.bullets(doc, "当前两个区间 A[i] 和 B[j] 的交集是 <code>[max(start), min(end)]</code>, 如果 lo ≤ hi 就是一段交集。",
           "然后, <b>先结束的那个</b>往前走。因为它已经结束了, 不可能再和对方的下一个区间相交 (对方的下一个区间开始得更晚)。")
doc.h3("算法")
nc.steps(doc, "<code>i = j = 0</code>。当两个都没走完:",
         "<code>lo = max(A[i].start, B[j].start)</code>, <code>hi = min(A[i].end, B[j].end)</code>。lo ≤ hi 就记下 [lo, hi]。",
         "<code>A[i].end < B[j].end</code> 则 i += 1, 否则 j += 1。")
doc.svg(SLUG + "/intersect_core.svg", "上: [5,10] 和 [8,12] 交于 [8,10]; A 的先结束, 它够不到 B 的下一个, i += 1。下: 没有交集, B 先结束, j += 1。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/intersect_trace.svg", "5 步走完。第 2 步交集是单点 [5,5] (闭区间, lo = hi 也算); 没有交集时指针照样往前走。")
doc.h3("复杂度")
doc.p("Time <code>O(m + n)</code>, Space <code>O(m + n)</code> (输出)。")
nc.solution(doc, CODE["intersect"])
doc.note("两个有序区间列表求交集: 双指针, 交集是 [max(start), min(end)], 先结束的往前走。")

# ================================================================ 8
doc.h2("8. My Calendar I")
doc.h3("题目在问什么")
doc.p("实现一个日历: <code>book(start, end)</code> 预订半开区间 <code>[start, end)</code>。如果和已有的任何预订重叠, 就拒绝 (返回 False); 否则记下来, 返回 True。")
doc.p("和前面不同, 这次区间是<b>一个一个来</b>的, 每来一个都要马上回答。")
doc.h3("看例子")
doc.svg(SLUG + "/calendar_examples.svg", "例子。")
doc.h3("Brute force")
doc.p("每次 book, 把新区间和已有的所有预订都比一下, 每次 <code>O(n)</code>, 共 <code>O(n²)</code>。")
doc.h3("Intuition: 只需要和左右两个邻居比")
doc.p("把已有的预订按 start 排好存起来 (它们互不重叠)。新区间来了, 用二分 (<code>bisect</code>) 找到它应该插在哪个位置。")
doc.p("它只可能和<b>左边的邻居</b> (start 比它小的最后一个) 或<b>右边的邻居</b> (start 比它大的第一个) 重叠。更远的预订被这两个邻居隔开了, 不可能碰到。")
nc.bullets(doc, "左邻居的 end 要 ≤ 新的 start。", "右邻居的 start 要 ≥ 新的 end。")
doc.h3("算法")
nc.steps(doc, "<code>i = bisect_left(starts, start)</code>。",
         "检查左邻居 i-1 和右邻居 i, 都不冲突就在 i 插入, 返回 True; 否则返回 False。")
doc.svg(SLUG + "/calendar_core.svg", "[32,38) 夹在 [22,30) 和 [40,45) 中间, 两个邻居都不冲突; [28,36) 的 28 < 左邻居的 end 30, 冲突。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/calendar_trace.svg", "连续 6 次调用。第 3 次左邻居的 end = 20 ≤ start = 20, 半开区间首尾相接, 可以; 第 5 次 [8,12) 和 [5,10) 冲突。")
doc.h3("复杂度")
doc.p("查找 <code>O(log n)</code>; Python list 的插入是 <code>O(n)</code>, 所以每次 book 是 <code>O(n)</code>。用平衡树 (比如 sortedcontainers) 可以做到 <code>O(log n)</code>。")
nc.solution(doc, CODE["calendar_brute"], CODE["calendar"])
doc.note("区间一个一个来、要判断冲突: 有序存储, 二分找位置, 只和左右两个邻居比。")

# ================================================================ 识别信号
doc.h2("9. 识别信号: 看到什么, 就想到这些做法")
nc.table(doc, ["题目特征", "做法", "complexity"], [
    ["合并重叠的区间", "按 start 排序, 和 res[-1] 比, end 取 max", "<code>O(n²)</code> → <code>O(n log n)</code>"],
    ["往有序、不重叠的列表插入", "三段扫描", "<code>O(n)</code>"],
    ["最多保留几个不重叠 / 最少删几个", "按 end 排序, greedy 保留最先结束的", "<code>O(2ⁿ)</code> → <code>O(n log n)</code>"],
    ["最少几个点覆盖所有区间", "按 end 排序, 点放在 end 上", "<code>O(n log n)</code>"],
    ["能不能全部参加 (有没有重叠)", "按 start 排序, 比相邻的", "<code>O(n²)</code> → <code>O(n log n)</code>"],
    ["同一时刻最多几个 / 最少几间房", "+1 / -1 事件扫描, 或 min-heap 存 end", "<code>O(n²)</code> → <code>O(n log n)</code>"],
    ["两个有序区间列表求交集", "双指针, 先结束的往前走", "<code>O(m·n)</code> → <code>O(m + n)</code>"],
    ["区间一个一个来, 判断冲突", "有序存储 + bisect, 比左右邻居", "每次 <code>O(n)</code> 比较 → <code>O(log n)</code> 查找"]])
doc.p("写之前先确认: 闭区间还是半开区间? 首尾相接算不算重叠? 这决定了 ≤ 还是 <。")

doc.h2("以后再学")
doc.p("Employee Free Time (多个人的空闲时间, 合并后找空隙)、Meeting Rooms III、My Calendar II / III (允许重叠 2 次 / 求最大重叠数, 用 sweep line)。")
doc.write("docs/10-intervals.html")
