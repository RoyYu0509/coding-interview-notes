# 17 · Design 正文 (NeetCode 式讲法)。由 17_design.py 末尾 exec, 共用 CODE_* / load。
import nclib as nc
from counts import cnt

SL = "17-design"
EX = os.path.join(d.ROOT, "docs", "svg", SL, "%s_examples.svg")
EXS = SL + "/%s_examples.svg"

# ---------------------------------------------------------------- 例子图 (先用代码验证)
L = load(CODE_LRU)["LRUCache"](2)
L.put(1, 1); L.put(2, 2)
assert L.get(1) == 1
L.put(3, 3)
assert L.get(2) == -1
L.put(4, 4)
assert L.get(1) == -1 and L.get(3) == 3 and L.get(4) == 4
nc.examples_svg(EX % "lru", "LRU Cache examples",
                ["容量固定的 cache。get(key): 有就返回 value, 没有返回 -1。put(key, value): 放进去; 满了就先踢掉<最久没被用过>的那个。都要 O(1)"], [
    dict(title="Example:  capacity = 2", index=False, rows=[
        ("put(1) put(2)", ["1", "2"], ["keep", "new"]),
        ("get(1) = 1", ["2", "1"], ["keep", "new"]),
        ("put(3)", ["1", "3"], ["keep", "new"]),
        ("get(2) = -1", ["1", "3"], None)], cw=50,
         extra=["每一行从左 (最久没用) 到右 (最近用过)。get(1) 让 1 变成最近用过的",
                "put(3) 时满了, 踢掉最久没用的 2。所以之后 get(2) 返回 -1"])],
    legend=[("new", "刚被用过的")])

nc.examples_svg(EX % "getrandom", "Insert Delete GetRandom examples",
                ["设计一个 set: insert(val)、remove(val)、getRandom() (等概率返回一个元素)。三个操作都要平均 O(1)"], [
    dict(title="Example:  insert(1) insert(2) insert(3) remove(2) getRandom()", index=False, rows=[
        ("insert 后", [1, 2, 3], None), ("remove(2)", [1, 3], None)],
         extra=["getRandom 在 {1, 3} 里等概率返回一个。难点: dict 能 O(1) 增删, 但不能 O(1) 随机取; list 能随机取, 但删中间要 O(n)"])],
    legend=[])

T = load(CODE_TM)["TimeMap"]()
T.set("foo", "bar", 1)
assert T.get("foo", 1) == "bar" and T.get("foo", 3) == "bar"
T.set("foo", "bar2", 4)
assert T.get("foo", 4) == "bar2" and T.get("foo", 5) == "bar2" and T.get("foo", 0) == ""
nc.examples_svg(EX % "timemap", "Time Based Key-Value Store examples",
                ["set(key, value, timestamp) 记录一个带时间的值。get(key, t): 返回 timestamp ≤ t 的最新那个值, 没有就返回 \"\"。timestamp 严格递增"], [
    dict(title="Example:  set(foo, bar, 1)  set(foo, bar2, 4)", index=False, rows=[
        ("foo 的历史", ["t=1 bar", "t=4 bar2"], None)], cw=90,
         extra=["get(foo, 1) = bar;  get(foo, 3) = bar (3 之前最新的是 t=1);  get(foo, 5) = bar2;  get(foo, 0) = \"\""])],
    legend=[])

H = load(CODE_HC)["HitCounter"]()
for t in (1, 2, 3):
    H.hit(t)
assert H.getHits(4) == 3
H.hit(300)
assert H.getHits(300) == 4 and H.getHits(301) == 3
nc.examples_svg(EX % "hitcounter", "Design Hit Counter examples",
                ["hit(t): 在时刻 t 有一次访问。getHits(t): 返回过去 300 秒内 (t-300, t] 的访问次数。t 单调不减"], [
    dict(title="Example:  hit(1) hit(2) hit(3) hit(300)", items=["1", "2", "3", "300"], cw=50, index=False,
         extra=["getHits(300) = 4: 1..300 都在 (0, 300] 里", "getHits(301) = 3: 窗口变成 (1, 301], t=1 那次过期了"])],
    legend=[])

nc.examples_svg(EX % "snapshot", "Snapshot Array examples",
                ["长度为 n 的数组, 初始全 0。set(index, val)、snap() 拍一张快照并返回编号 snap_id (从 0 开始)、get(index, snap_id) 查某张快照里的值"], [
    dict(title="Example:  n = 3", index=False, rows=[
        ("set(0,5)", [5, 0, 0], ["new", "keep", "keep"]), ("snap() = 0", [5, 0, 0], None),
        ("set(0,6)", [6, 0, 0], ["new", "keep", "keep"])],
         extra=["get(0, snap_id=0) = 5: 快照 0 拍的时候 index 0 还是 5", "难点: snap 可能调用很多次, 每次都复制整个数组太慢"])],
    legend=[("new", "刚改的")])

nc.examples_svg(EX % "lfu", "LFU Cache examples",
                ["和 LRU 一样有容量, 但满了要踢掉<使用次数最少>的; 次数一样时, 踢最久没用的。get / put 都要 O(1)"], [
    dict(title="Example:  capacity = 2:  put(1) put(2) get(1) put(3)",
         extra=["get(1) 之后: key 1 用了 2 次, key 2 用了 1 次", "put(3) 时满了, 踢掉次数最少的 2"])],
    legend=[])

# ================================================================ HTML
doc = d.Doc("17 · Data Structure Design")
doc.h2("这篇讲什么")
doc.p("design 题让你实现一个 class, 有几个方法, 而且<b>每个方法都有复杂度要求</b> (通常是 <code>O(1)</code>)。比如 LRU Cache: get 和 put 都要 <code>O(1)</code>。")
doc.p("难点是: 没有任何一个单独的数据结构能把所有操作都做快。dict 查找快但没有顺序; list 能按位置取但删除中间很慢; linked list 删除快但查找慢……")
doc.p("所以 design 题的套路是: <b>列出每个操作要什么 → 看每种数据结构能 O(1) 做什么 → 把两个结构组合起来, 每个操作交给擅长它的那个, 同时保证两个结构的内容一直同步</b>。")
doc.svg(SL + "/first_principles_core.svg", "操作 × 数据结构的能力对照: 每种结构都有做不快的事, 组合起来互补。")
nc.solution(doc, CODE_TEMPLATE, summary="design 题的一般写法")
nc.table(doc, ["#", "题目", "考过的公司数", "组合"], [
    ["1", "LRU Cache", cnt("LRU Cache"), "dict + doubly linked list。总榜第 2"],
    ["2", "Insert Delete GetRandom O(1)", cnt("Insert Delete GetRandom O(1)"), "dict + list"],
    ["3", "Time Based Key-Value Store", cnt("Time Based Key-Value Store"), "dict of list + 二分"],
    ["4", "Design Hit Counter / Logger Rate Limiter", "%d / %d" % (cnt("Design Hit Counter"), cnt("Logger Rate Limiter")), "deque 当时间窗口"],
    ["5", "Snapshot Array", cnt("Snapshot Array"), "每个位置只记变化 + 二分"],
    ["6", "LFU Cache", cnt("LFU Cache"), "LRU 按使用次数分层 (只讲结构)"]])
doc.p("每道题的顺序: <b>题目在问什么 → 看例子 → brute force → intuition → 算法 → 手动走一遍 → 复杂度</b>。代码放在最后, 默认折叠。")

# ================================================================ 1
doc.h2("1. LRU Cache")
doc.h3("题目在问什么")
doc.p("实现一个容量为 capacity 的 cache:")
nc.bullets(doc, "<code>get(key)</code>: key 存在就返回 value, 否则返回 -1。",
           "<code>put(key, value)</code>: 放进去 (已存在就更新)。如果放进去之后超过了容量, 就踢掉<b>最久没被用过</b> (least recently used) 的那个。",
           "get 和 put 都算\"用过\"。两个操作都要 <code>O(1)</code>。")
doc.h3("看例子")
doc.svg(EXS % "lru", "例子。")
doc.h3("Brute force")
doc.p("用一个 list 按\"最近用过\"的顺序存 key, 最久没用的在最前面。get 时要在 list 里找到 key 并移到最后, <code>O(n)</code>; 踢人是删掉第一个, 也是 <code>O(n)</code> (list 删头要移动所有元素)。")
doc.h3("Intuition: dict 负责找, linked list 负责排顺序")
doc.p("需要两种能力:")
nc.bullets(doc, "<b>按 key 找到它</b>: dict, <code>O(1)</code>。",
           "<b>维护\"谁最久没用\"的顺序, 并且能把任意一个元素 O(1) 地移到\"最新\"的位置、O(1) 删掉\"最旧\"的</b>: doubly linked list (双向链表)。只要手里有 node 的引用, 删除它和插到末尾都是 <code>O(1)</code>。")
doc.p("组合起来: dict 存 <code>key → node</code>, node 在链表里。链表头部是最久没用的, 尾部是最近用的。")
nc.bullets(doc, "get: dict 找到 node, 把它从链表里拿出来, 放到尾部, 返回 value。",
           "put: 已存在就更新 value 并移到尾部; 不存在就新建 node 放到尾部、加进 dict; 超过容量就删掉头部的 node, 并且<b>从 dict 里也删掉它的 key</b> (两边要同步, 所以 node 里也要存 key)。")
doc.p("一个写链表的技巧: 用两个假的 dummy node 当头和尾, 这样插入和删除都不用判断\"是不是空链表\"、\"是不是第一个\"。")
doc.h3("算法")
nc.steps(doc, "<code>head</code>、<code>tail</code> 两个 dummy node, 中间是真正的 node。<code>cache = {}</code> 存 key → node。",
         "两个辅助函数: <code>remove(node)</code> 把 node 从链表里摘掉; <code>add_to_end(node)</code> 插到 tail 前面。",
         "get: 不在就 -1; 在就 remove + add_to_end, 返回值。",
         "put: 在就先 remove; 新建或更新 node, add_to_end, 存进 cache。如果 <code>len(cache) > capacity</code>: 删掉 <code>head.next</code>, 并 <code>del cache[它的 key]</code>。")
doc.svg(SL + "/lru_core.svg", "dict 按 key 直接找到 node; 链表从旧到新排列, head.next 就是下一个要被踢掉的。")
doc.h3("手动走一遍")
doc.svg(SL + "/lru_trace.svg", "capacity = 2 的 7 步。每一步都画出了链表顺序和 dict 的内容; 被踢掉的 node 用虚线扔到左边, 写明了原因。")
doc.h3("复杂度")
doc.p("get 和 put 都是 Time <code>O(1)</code>。Space <code>O(capacity)</code>。")
doc.p("面试时如果允许用库, Python 的 <code>OrderedDict</code> 本身就是 dict + 双向链表: <code>move_to_end(key)</code> 移到最新, <code>popitem(last=False)</code> 踢掉最旧。但面试官通常想看你自己写链表。")
nc.solution(doc, CODE_LRU, CODE_LRU_OD)
doc.note("要 O(1) 查找 + O(1) 维护顺序 (移到最新、删掉最旧): dict + doubly linked list, dummy head / tail。")

doc.h2("把第 1 题抽象一下: design 题怎么想")
nc.steps(doc, "列出每个操作和它的复杂度要求。",
         "对每个操作, 想\"哪种数据结构能 O(1) 做到\"。",
         "如果一个结构做不完所有操作, 就组合两个。<b>想清楚每次修改时, 两个结构要怎么同步</b> (LRU 里删 node 时也要删 dict 里的 key)。")
doc.p("常见的组合: dict + linked list (要顺序), dict + list (要随机取或按下标), dict + heap (要最值), dict + 有序 list + 二分 (要按时间 / 版本查)。")
doc.note("design 题 = 每个操作交给擅长它的结构 + 保持两个结构同步。")

# ================================================================ 2
doc.h2("2. Insert Delete GetRandom O(1)")
doc.h3("题目在问什么")
doc.p("设计一个 set, 支持 <code>insert(val)</code> (不存在才插入)、<code>remove(val)</code> (存在才删除)、<code>getRandom()</code> (等概率返回一个元素)。三个操作都要平均 <code>O(1)</code>。")
doc.h3("看例子")
doc.svg(EXS % "getrandom", "例子。")
doc.h3("Brute force")
doc.p("只用 set: insert / remove 是 <code>O(1)</code>, 但 getRandom 要先转成 list, <code>O(n)</code>。只用 list: getRandom 是 <code>random.choice</code>, <code>O(1)</code>, 但 remove 要先找到它、再删中间, <code>O(n)</code>。")
doc.h3("Intuition: list 存元素, dict 记它在 list 里的位置")
doc.p("getRandom 需要\"按位置随机取\", 只能用 list。问题是 list 删中间很慢。")
doc.p("技巧: <b>删除时, 把要删的元素和 list 最后一个元素交换, 然后 pop 最后一个</b>。pop 末尾是 <code>O(1)</code>。顺序乱了没关系, set 本来就不关心顺序。")
doc.p("但要和最后一个交换, 先得知道要删的元素在哪个位置。所以再用一个 dict 记 <code>val → 它在 list 里的下标</code>。交换之后, 被换过来的那个元素位置变了, dict 里也要更新它的下标。")
doc.h3("算法")
nc.steps(doc, "insert: 已经在 dict 里就返回 False。否则 <code>pos[val] = len(arr)</code>, <code>arr.append(val)</code>。",
         "remove: 不在就返回 False。<code>i = pos[val]</code>, <code>last = arr[-1]</code>; 把 last 放到位置 i: <code>arr[i] = last</code>, <code>pos[last] = i</code>; 然后 <code>arr.pop()</code>, <code>del pos[val]</code>。",
         "getRandom: <code>random.choice(arr)</code>。")
doc.svg(SL + "/getrandom_core.svg", "删除 = 把最后一个搬到要删的位置, 再 pop 末尾; dict 里同步更新被搬动的那个元素的下标。")
doc.h3("手动走一遍")
doc.svg(SL + "/getrandom_trace.svg", "每一步画出 list 和 dict; 删除时被搬动的元素和它的新下标都标了出来。")
doc.h3("复杂度")
doc.p("三个操作都是平均 Time <code>O(1)</code>。Space <code>O(n)</code>。")
nc.solution(doc, CODE_RS)
doc.note("要 O(1) 删除 + O(1) 随机取: list + dict(val → index), 删除时和最后一个交换再 pop。")

# ================================================================ 3
doc.h2("3. Time Based Key-Value Store")
doc.h3("题目在问什么")
doc.p("<code>set(key, value, timestamp)</code> 记录 key 在某个时刻的值。<code>get(key, t)</code> 返回 key 在 <b>timestamp ≤ t 里最新</b>的那个值, 没有就返回空字符串。题目保证同一个 key 的 set 调用, timestamp 是严格递增的。")
doc.h3("看例子")
doc.svg(EXS % "timemap", "例子。")
doc.h3("Brute force")
doc.p("每个 key 存一个 (timestamp, value) 的 list。get 时从后往前扫, 找第一个 timestamp ≤ t 的。<code>O(n)</code> 每次。")
doc.h3("Intuition: list 本来就是排好序的, 用二分")
doc.p("timestamp 严格递增, 所以 set 时直接 append, list 天然就是按时间排好序的。")
doc.p("get 时要找\"最后一个 timestamp ≤ t 的位置\"。这正是 05 里的二分: <code>bisect_right(times, t) - 1</code>。结果是 -1 表示所有记录都比 t 晚, 返回空字符串。")
doc.h3("算法")
nc.steps(doc, "<code>data = defaultdict(list)</code>, 每个 key 对应 [(timestamp, value), ...]。",
         "set: append。",
         "get: 在 key 的 list 上二分, 找最后一个 ≤ t 的, 返回它的 value。")
doc.svg(SL + "/timemap_core.svg", "dict of list; append 天然有序, bisect 找 ≤ t 的最后一个。")
doc.h3("手动走一遍")
doc.svg(SL + "/timemap_trace.svg", "每个 get 写出二分的结果下标。")
doc.h3("复杂度")
doc.p("set <code>O(1)</code>, get <code>O(log n)</code>。Space <code>O(n)</code>。")
nc.solution(doc, CODE_TM)
doc.note("按时间 / 版本查\"某时刻之前最新的\": 按时间 append 的 list + bisect_right - 1。")

# ================================================================ 4
doc.h2("4. Design Hit Counter / Logger Rate Limiter")
doc.h3("题目在问什么")
doc.p("<b>Hit Counter</b>: <code>hit(t)</code> 记录时刻 t 的一次访问; <code>getHits(t)</code> 返回过去 300 秒 <code>(t - 300, t]</code> 里的访问次数。所有调用的 t 都是单调不减的。")
doc.p("<b>Logger Rate Limiter</b>: <code>shouldPrintMessage(t, msg)</code>: 同一条 message 在 10 秒内只打印一次。")
doc.h3("看例子")
doc.svg(EXS % "hitcounter", "Hit Counter 的例子。")
doc.h3("Brute force")
doc.p("把所有 hit 的时间存进 list, getHits 时扫一遍数有几个在窗口里。list 会越来越长, 每次 <code>O(总访问数)</code>。")
doc.h3("Intuition: 窗口外的记录永远没用了, 从左边扔掉")
doc.p("时间是单调增加的。一条记录一旦滑出了 300 秒的窗口, 以后的查询只会更晚, 它再也不会回到窗口里。所以可以直接扔掉。")
doc.p("最老的记录在最左边, 用 <code>deque</code>: 新的 hit 从右边 append, 查询时把左边过期的 popleft 掉, 剩下的个数就是答案。和 03 里 sliding window 是同一个思路。")
doc.p("Logger 更简单: 只需要 dict 记每条 message 上次打印的时间, 距离现在 ≥ 10 秒才打印并更新。")
doc.h3("算法")
nc.steps(doc, "hit(t): <code>q.append(t)</code>。",
         "getHits(t): 当 <code>q[0] <= t - 300</code>: popleft。返回 <code>len(q)</code>。")
doc.svg(SL + "/hitcounter_core.svg", "deque 从左到右按时间排列; 过期的从左边出队。")
doc.h3("手动走一遍")
doc.svg(SL + "/hitcounter_trace.svg", "每次 getHits 先清掉过期的, 再数剩下的。")
doc.h3("复杂度")
doc.p("每个记录只进出一次, 平均 <code>O(1)</code>。Space 是窗口里的记录数。如果同一秒访问特别多, 可以存 (时间, 次数) 压缩。")
nc.solution(doc, CODE_HC, CODE_LOGGER)
doc.note("时间窗口里的计数, 时间单调: deque, 右边进、左边出过期的。")

# ================================================================ 5
doc.h2("5. Snapshot Array")
doc.h3("题目在问什么")
doc.p("一个长度为 n 的数组, 初始全是 0。支持 <code>set(index, val)</code>、<code>snap()</code> (拍一张快照, 返回快照编号, 从 0 开始)、<code>get(index, snap_id)</code> (返回第 snap_id 张快照里 index 位置的值)。")
doc.h3("看例子")
doc.svg(EXS % "snapshot", "例子。")
doc.h3("Brute force")
doc.p("每次 snap 都把整个数组复制一份存起来。snap 是 <code>O(n)</code>, 调用很多次时内存和时间都爆了。")
doc.p("浪费: 两次 snap 之间可能只改了一两个位置, 却把整个数组都复制了。")
doc.h3("Intuition: 每个位置只记\"什么时候改成了什么\"")
doc.p("不复制整个数组。对每个 index, 只记录它的修改历史: <code>[(snap_id, val), ...]</code>, 意思是\"在第 snap_id 张快照的时候 (还没拍之前), 它被改成了 val\"。")
doc.p("snap 只需要把当前的编号加 1, <code>O(1)</code>。")
doc.p("get(index, snap_id): 在 index 的修改历史里, 找 <b>snap_id ≤ 要查的编号</b>的最后一条记录。这和第 3 题一模一样, 用二分。")
doc.h3("算法")
nc.steps(doc, "<code>hist[i] = [(-1, 0)]</code> (初始值 0), <code>snap_id = 0</code>。",
         "set: 如果 hist[index] 最后一条的编号就是当前 snap_id, 直接覆盖; 否则 append <code>(snap_id, val)</code>。",
         "snap: <code>snap_id += 1</code>, 返回 <code>snap_id - 1</code>。",
         "get: 在 hist[index] 上二分找最后一个编号 ≤ snap_id 的, 返回它的值。")
doc.svg(SL + "/snapshot_core.svg", "不复制数组; 每个 index 只记录变化, 查询时二分回溯。")
doc.h3("手动走一遍")
doc.svg(SL + "/snapshot_trace.svg", "每一步画出每个 index 的修改历史。")
doc.h3("复杂度")
doc.p("set、snap <code>O(1)</code>, get <code>O(log 修改次数)</code>。Space 和修改次数成正比。")
nc.solution(doc, CODE_SNAP)
doc.note("版本 / 快照: 不复制整体, 每个位置记 (版本, 值) 的历史, 查询时二分。")

# ================================================================ 6
doc.h2("6. LFU Cache (只讲结构)")
doc.h3("题目在问什么")
doc.p("和 LRU 一样有容量, get / put 都要 <code>O(1)</code>。区别是满了要踢掉<b>使用次数最少</b>的 key; 使用次数一样的, 踢最久没用的那个。")
doc.h3("看例子")
doc.svg(EXS % "lfu", "例子。")
doc.h3("Intuition: 按使用次数分组, 每组内部就是一个 LRU")
doc.p("需要同时知道\"次数最少的是哪一组\", 以及\"这一组里最久没用的是谁\"。结构:")
nc.bullets(doc, "<code>key → (value, freq)</code>: 按 key 查。",
           "<code>freq → OrderedDict</code>: 每个使用次数对应一组 key, 组内按最近使用排序 (就是一个小的 LRU)。",
           "<code>min_freq</code>: 当前最小的使用次数。")
doc.p("一个 key 被使用时: 从 freq 组里删掉, freq + 1, 加到新的组的末尾。如果旧组空了而且它是 min_freq, min_freq 加 1。新 key 进来时 freq = 1, min_freq 设成 1。踢人时从 min_freq 组的最前面踢。")
doc.svg(SL + "/lfu_core.svg", "按 freq 分层, 每层是一个 LRU; min_freq 指向要踢的那一层。")
doc.h3("复杂度")
doc.p("get、put 都是 <code>O(1)</code>。")
nc.solution(doc, CODE_LFU)
doc.note("LFU = 按使用次数分组的 LRU, 加一个 min_freq 指向最少的那组。")

# ================================================================ 识别信号
doc.h2("7. 识别信号: 看到什么, 就想到什么组合")
nc.table(doc, ["题目特征", "组合", "复杂度"], [
    ["O(1) 查找 + 维护最近使用的顺序 (LRU)", "dict + doubly linked list (或 OrderedDict)", "<code>O(n)</code> → <code>O(1)</code>"],
    ["O(1) 删除 + O(1) 随机取", "list + dict(val → index), 删除时和最后一个交换", "<code>O(n)</code> → <code>O(1)</code>"],
    ["按时间 / 版本查之前最新的值", "按时间 append 的 list + bisect", "<code>O(n)</code> → <code>O(log n)</code>"],
    ["最近 T 秒内的计数, 时间单调", "deque, 左边出过期的", "均摊 <code>O(1)</code>"],
    ["快照 / 多版本", "每个位置记 (版本, 值) 历史 + 二分", "snap <code>O(n)</code> → <code>O(1)</code>"],
    ["按次数淘汰 (LFU)", "dict + freq → OrderedDict + min_freq", "<code>O(1)</code>"],
    ["O(1) 拿到最小值的 stack", "每个元素存 (val, min) → 06", "<code>O(1)</code>"],
    ["数据流里随时求中位数", "两个 heap → 09", "<code>O(log n)</code>"]])
doc.p("一句话: 先列出每个操作的要求, 再给每个操作找一个能 O(1) 做它的结构, 最后想清楚修改时怎么同步。")

doc.h2("以后再学")
doc.p("Design Twitter (dict + heap 合并 k 个 feed)、All O(1) Data Structure、Design Underground System、各种 iterator 设计 (Flatten Nested List Iterator)。")
doc.write("docs/17-design.html")
