"""09 · Heap / Top-K  —— 运行: cd build && python3 -I 09_heap.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import doclib as d  # noqa: E402

# ---------------------------------------------------------------- code snippets
C_TEMPLATE = '''
import heapq

h = []
heapq.heappush(h, x)           # O(log n)
top = h[0]                     # O(1), 只看 top, 不拿走
x = heapq.heappop(h)           # O(log n), 拿走最小的
heapq.heapify(arr)             # O(n), 原地把 list 变成 heap

# max-heap: heapq 只有 min-heap, 存 -x, 取出来再取负
heapq.heappush(h, -x)
biggest = -heapq.heappop(h)

# tuple 从左到右比大小: (count, num) 先比 count, 再比 num
pairs = []
heapq.heappush(pairs, (count, num))

# 固定大小 k 的模板: heap 里永远只留 "最该留下的 k 个"
for x in stream:
    heapq.heappush(h, x)
    if len(h) > k:
        heapq.heappop(h)       # 弹出的是 "最该被踢掉的", 它在 top
'''

C_KTH = '''
def findKthLargest(nums, k):
    h = []                          # min-heap, 永远只留 "目前最大的 k 个"
    for x in nums:
        heapq.heappush(h, x)
        if len(h) > k:
            heapq.heappop(h)        # 弹掉最小的, 它一定不在前 k 大里
    return h[0]                     # k 个里最小的 = 第 k 大
'''

C_TOPK = '''
def topKFrequent(nums, k):
    count = Counter(nums)                 # O(n): num -> 出现次数
    h = []                                # min-heap of (count, num)
    for num, c in count.items():          # 只遍历不同的 num: m 个
        heapq.heappush(h, (c, num))
        if len(h) > k:
            heapq.heappop(h)              # count 最小的踢掉 (和上一题唯一的区别)
    return [num for c, num in h]          # 顺序不限
'''

C_CLOSEST = '''
def kClosest(points, k):
    h = []                                 # max-heap (存 -d), 留 "最近的 k 个"
    for x, y in points:
        d = x * x + y * y                  # 不开根号, 比大小等价
        heapq.heappush(h, (-d, x, y))      # -d 最小 = d 最大, 在 top
        if len(h) > k:
            heapq.heappop(h)               # 踢掉 d 最大的 (最远的)
    return [[x, y] for _, x, y in h]
'''

C_MERGE = '''
def mergeKLists(lists):
    h = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(h, (node.val, i, node))   # (val, i, node)
            # i 用来在 val 相同时决胜负, 否则会去比较 ListNode (不能比)
    dummy = tail = ListNode()
    while h:
        val, i, node = heapq.heappop(h)    # 全局最小一定是某条 list 的 head
        tail.next = node
        tail = node
        if node.next:                      # 这条 list 的新 head 补进来
            heapq.heappush(h, (node.next.val, i, node.next))
    return dummy.next
'''

C_MEDIAN = '''
class MedianFinder:
    def __init__(self):
        self.lo = []        # max-heap (存 -x): 较小的一半, top = 这一半最大
        self.hi = []        # min-heap:         较大的一半, top = 这一半最小

    def addNum(self, num):
        heapq.heappush(self.lo, -num)
        # 先进 lo, 再把 lo 最大的交给 hi -> 保证 max(lo) <= min(hi)
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        if len(self.hi) > len(self.lo):    # lo 允许比 hi 多 1 个, hi 不许多
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self):
        if len(self.lo) > len(self.hi):    # 总数奇数
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2
'''

C_HIRE = '''
def mincostToHireWorkers(quality, wage, k):
    # rate = wage / q. 按 rate 升序排: 处理到某个 worker 时, 他的 rate 就是 group 里最大的
    workers = sorted(zip(quality, wage), key=lambda w: w[1] / w[0])
    h = []                          # max-heap (存 -q): group 里 q 最大的在 top
    total_q = 0                     # group 里所有 q 相加
    best = float("inf")
    for q, w in workers:
        rate = w / q
        heapq.heappush(h, -q)
        total_q += q
        if len(h) > k:
            total_q += heapq.heappop(h)     # 弹出的是 -q_max, 加上它 = 减去 q_max
        if len(h) == k:
            best = min(best, rate * total_q)   # cost = rate x total_q
    return best
'''

C_EVENTS = '''
def maxEvents(events):                      # events[i] = [start, end]
    events.sort()                           # 排序一维: start
    h = []                                  # min-heap of end: 今天能参加的活动
    day = i = res = 0
    while i < len(events) or h:
        if not h:
            day = max(day, events[i][0])    # 没得参加, 跳到下一个 start
        while i < len(events) and events[i][0] <= day:
            heapq.heappush(h, events[i][1]) # start 到了的活动, 记下 end
            i += 1
        while h and h[0] < day:
            heapq.heappop(h)                # end 已过, 参加不了
        if h:
            heapq.heappop(h)                # 今天参加 end 最早的 (最急的)
            res += 1
        day += 1
    return res
'''

C_IPO = '''
def findMaximizedCapital(k, w, profits, capital):
    projects = sorted(zip(capital, profits))   # 排序一维: capital
    h = []                                     # max-heap (存 -profit): 做得起的
    i = 0
    for _ in range(k):
        while i < len(projects) and projects[i][0] <= w:
            heapq.heappush(h, -projects[i][1]) # capital <= w 的都进 heap
            i += 1
        if not h:
            break
        w -= heapq.heappop(h)                  # 做 profit 最大的, w 变大
    return w
'''

C_TASK = '''
def leastInterval(tasks, n):
    heap = [(-c, t) for t, c in Counter(tasks).items()]   # max-heap: 剩余次数
    heapq.heapify(heap)
    cooldown = deque()          # (回来的 slot, -剩余次数, task), 回来时间递增
    time = 0
    while heap or cooldown:
        time += 1               # 每个 slot 无论做不做事, time 都 +1
        if heap:
            c, t = heapq.heappop(heap)      # 剩余最多的, 这个 slot 做它
            if c + 1:                       # c 是负数, c + 1 != 0 说明还有剩
                cooldown.append((time + n, c + 1, t))
        if cooldown and cooldown[0][0] == time:   # 冷却完了, 下个 slot 可以做
            _, c, t = cooldown.popleft()
            heapq.heappush(heap, (c, t))
    return time
'''

CODES = dict(template=C_TEMPLATE, kth=C_KTH, topk=C_TOPK, closest=C_CLOSEST, merge=C_MERGE,
             median=C_MEDIAN, hire=C_HIRE, events=C_EVENTS, ipo=C_IPO, task=C_TASK)

SV = "09-heap/"


def build():
    doc = d.Doc("09 · Heap / Top-K")
    doc.main("主线: heap 只保证 top 是最小 (或最大) 的那一个, push / pop 都是 O(log n)。"
             "只要 \"反复拿最值\" 或 \"只要前 k 个\", 就别全排序, 用 heap 把 O(n log n) 降到 O(n log k)。")
    doc.main("概念链: Kth Largest (size-k min-heap) → Top K Frequent (key 换成 count) → "
             "K Closest Points (方向反过来: max-heap) → Merge k Sorted Lists (heap 里放 k 个 head) → "
             "Find Median (两个 heap) → Min Cost Hire K Workers (排序一维 + heap 管另一维) → "
             "Task Scheduler (greedy + heap + cooldown)")

    # ------------------------------------------------------------ 0
    doc.h2("0. 第一性原理: 要最值, 不要全序")
    doc.p("题目只问 \"最大的 k 个\" 或 \"下一个最小的\"。brute force 是 sort 一遍, O(n log n)。"
          "浪费在哪: sort 把 <b>所有</b> 元素的相对顺序都排好了, 可是答案只用到最前面 k 个, 后面 n - k 个的顺序白排了。"
          "反过来, 如果每次都扫一遍找最小值, 是 O(n) 一次, 反复找就是 O(n²)。")
    doc.p("heap 的做法: 只维护一条规则 \"parent ≤ children\" (min-heap)。这条规则够把最小的顶到 top, "
          "又足够松, 插入和删除只需要沿着一条路径往上或往下换, 路径长度是树高 log n。"
          "所以 heap 是 \"拿最小\" 和 \"加一个数\" 两头都不太差的结构。")
    doc.svg(SV + "heap_core.svg", "heap 保证 top 最小, 不保证全序; push / pop 沿一条路径换位, O(log n)")
    doc.p("固定大小 k 的 heap 是本章 80% 的题: 数据一个个进来, heap 里永远只留 \"最该留下的 k 个\", "
          "满了就踢 top。每个元素最多进出一次, 一次 O(log k), 总共 O(n log k)。")
    doc.code(C_TEMPLATE)
    doc.note("heapq 是 min-heap。max-heap 存 -x。top 放的是 \"最该被踢掉的\", 不是 \"最想要的\"。"
             "(heapq.nlargest(k, nums) 是现成的, 内部就是这个 heap; 面试里要会手写。)")

    # ------------------------------------------------------------ 1
    doc.h2("1. Kth Largest Element in an Array: 留下最大的 k 个, 用 min-heap")
    doc.p("题目: 无序数组 <code>nums</code>, 返回第 k 大的数。例: <code>nums = [3,2,1,5,6,4], k = 2</code> → 5。")
    doc.p("Brute force: sort 后取 <code>nums[-k]</code>, O(n log n)。浪费: 前 n - k 小的数的顺序没人用。")
    doc.p("关键观察: 只留 \"目前最大的 k 个\"。满了要踢一个, 踢的永远是这 k 个里最小的 → 要立刻拿到最小的 → <b>min-heap</b>。"
          "留下来的 k 个里最小的 (top) 恰好就是整体第 k 大。")
    doc.svg(SV + "kth_largest_core.svg", "为什么是 min-heap: top = 留下的 k 个里最小的 = 第 k 大, 也是下一个要被踢的")
    doc.svg(SV + "kth_largest_trace.svg", "trace: k = 2, 每步 push, 超过 k 个就 pop 最小的, heap 里始终是最大的 2 个")
    doc.code(C_KTH)
    doc.p("Time: 每个数一次 push + 至多一次 pop, 都是 O(log k), 共 O(n log k)。Space: heap O(k)。"
          "另有 quickselect 平均 O(n), 面试里一句话提一下即可。")
    doc.note("留最大的 k 个 → min-heap, top 是门槛; 第 k 大 = h[0]。")

    # ------------------------------------------------------------ 2
    doc.h2("2. Top K Frequent Elements: 同一个模板, 比较的 key 换成 count")
    doc.p("题目: 返回出现次数最多的 k 个数。例: <code>nums = [1,1,1,2,2,3,4,4,4,4], k = 2</code> → [1, 4]。")
    doc.p("相比上一题多了什么: 要先数次数 (Counter), 然后 \"按 count 找最大的 k 个\"。改的只有 heap 里放什么: 放 <code>(count, num)</code>, 比较自然按 count。"
          "Brute force: 对所有不同的 num 按 count sort, O(m log m) (m = 不同数字个数)。heap 只留 k 个, O(m log k)。")
    doc.svg(SV + "top_k_frequent_core.svg", "Counter 把问题变成 \"在 count 上找最大的 k 个\", 和 Kth Largest 同构")
    doc.svg(SV + "top_k_frequent_trace.svg", "trace: 4 个不同的 num, k = 2, 每步 pop count 最小的")
    doc.code(C_TOPK)
    doc.p("Time: Counter O(n) + heap O(m log k)。Space: O(m)。"
          "bucket sort (count 当 index 的 list) 可以做到 O(n), 记住有这个办法。"
          "Top K Frequent Words 一样, 只是 count 相同要按字典序, key 改成 <code>(count, word)</code> 并处理好大小顺序。")
    doc.note("\"按某个量找前 k\" → size-k heap, heap 里放 (这个量, 本体)。")

    # ------------------------------------------------------------ 3
    doc.h2("3. K Closest Points to Origin: 留最小的 k 个, 方向反过来, 用 max-heap")
    doc.p("题目: 返回离原点最近的 k 个点。例: <code>points = [[3,3],[5,-1],[-2,4],[1,1],[0,2]], k = 2</code> → [[1,1],[0,2]]。")
    doc.p("相比第 1 题: 留下的是 <b>最小的</b> k 个 (d 最小), 要踢的是 d 最大的 → top 必须是最大值 → <b>max-heap</b>, Python 里存 <code>-d</code>。"
          "第 1 题是 min-heap 留最大, 这题是 max-heap 留最小, 判断规则只有一条: top 放 \"最该被踢掉的\"。"
          "Brute force: 按 d sort, O(n log n)。")
    doc.svg(SV + "k_closest_core.svg", "同一条规则两个方向: 要留大的 → 踢最小的 → min-heap; 要留小的 → 踢最大的 → max-heap")
    doc.svg(SV + "k_closest_trace.svg", "trace: k = 2, heap 里画的是正数 d, top = 最大的 d (代码里存 -d)")
    doc.code(C_CLOSEST)
    doc.p("Time: O(n log k)。Space: O(k)。")
    doc.note("留小的 → max-heap (存负数), 留大的 → min-heap。d = x² + y² 不用开根号。")

    # ------------------------------------------------------------ 4
    doc.h2("4. Merge k Sorted Lists: heap 里只放 k 个 head")
    doc.p("题目: 合并 k 条有序链表。例: <code>L0 = 1→4→5, L1 = 1→3→4, L2 = 2→6</code> → 1→1→2→3→4→4→5→6。")
    doc.p("Brute force: 所有 node 倒进一个 list 再 sort, O(N log N) (N = node 总数), 浪费: 每条 list 本来就有序, 这个信息被丢掉了。"
          "关键观察: 每条 list 有序 → 全局最小的一定是某条 list 的 <b>head</b>。所以 heap 里每条 list 只放当前的 head, 一共 k 个, "
          "pop 出最小的, 把它的 next 补进来。")
    doc.p("相比前几题: heap 不再是 \"留下 k 个\" 的筛子, 而是 \"k 路里下一个该走谁\" 的选择器; 元素是 <code>(val, i, node)</code>。")
    doc.svg(SV + "merge_k_lists_core.svg", "heap 里只有每条 list 的 head, 每个 node 进出 heap 各一次")
    doc.svg(SV + "merge_k_lists_trace.svg", "trace: 先 push 3 个 head, 每步 pop 最小的接到 output, 再 push 它的 next")
    doc.code(C_MERGE)
    doc.p("Time: N 个 node 各进出一次, heap 大小 ≤ k, O(N log k)。Space: 额外 O(k) (node 是原地接起来的)。"
          "同一个套路: Kth Smallest in Sorted Matrix (每行是一条有序 list), Find K Pairs with Smallest Sums, Smallest Range Covering K Lists。")
    doc.note("k 路有序 → heap 放每一路的当前头, pop 一个补一个; tuple 里加 i 防止比较 node。")

    # ------------------------------------------------------------ 5
    doc.h2("5. Find Median from Data Stream: 两个 heap, 各管一半")
    doc.p("题目: 数据流, 随时 addNum, 随时 findMedian。例: 依次加 5, 2, 8, 3, 9, 1 → median 依次 5, 3.5, 5, 4, 5, 4。")
    doc.p("Brute force: 每次 find 都 sort, O(n log n); 或者维护有序 list, 每次插入 O(n) (搬位置)。"
          "关键观察: 中位数只看 \"正中间那一两个数\", 不需要整体有序。把排好序的数从中间切开, 左半 lo 要快速拿到最大, 右半 hi 要快速拿到最小。")
    doc.p("相比前几题: 一个 heap 不够, 要 <b>两个 heap</b>: lo 是 max-heap, hi 是 min-heap。两个 invariant: "
          "max(lo) ≤ min(hi); len(lo) = len(hi) 或 len(hi) + 1。每次 add 都用 \"先进 lo, 再把 lo 的 top 交给 hi, 不平衡再还回来一个\" 修好。")
    doc.svg(SV + "median_stream_core.svg", "lo / hi 各管一半, 两个 top 就是正中间那两个数")
    doc.svg(SV + "median_stream_trace.svg", "trace: 每步绿色节点 = 这一步换了 heap 的元素; 最后一列是当前 median")
    doc.code(C_MEDIAN)
    doc.p("Time: add O(log n), find O(1)。Space: O(n)。"
          "Sliding Window Median 是它的加强版 (要删元素, 需要 lazy delete), 先把这题写熟。")
    doc.note("中位数 = 两个 heap 的 top: 左半 max-heap, 右半 min-heap, 大小差 ≤ 1。")

    # ------------------------------------------------------------ 6
    doc.h2("6. Minimum Cost to Hire K Workers: 排序一维, heap 管另一维")
    doc.p("题目: 每个 worker 有 quality q 和最低 wage。雇 k 个, 工资必须和 q 成正比 (同一个 rate = wage / q), 每人工资不低于自己的最低 wage。求最小总工资。"
          "例: <code>quality = [10,20,5,8,9], wage = [20,60,20,40,63], k = 3</code> → 115 (雇 A, C, D)。")
    doc.p("Brute force: 枚举 C(n, k) 个 group, 对每个 group 取最大的 rate, cost = rate × total_q。浪费: 两个维度 (rate 和 q) 同时变, 没法剪。")
    doc.p("关键观察: 先把一个维度固定住。按 rate 升序排, 处理到某个 worker 时, 他的 rate 是 group 里最大的, 其他人 rate 更小, 按这个 rate 付工资大家都合法。"
          "rate 固定后 cost = rate × total_q, 只能压 total_q → 在已经见过的 worker 里留 q 最小的 k 个 → 满了就踢 q 最大的 (max-heap)。"
          "这是 \"排序一维 + heap 管另一维\" 的典型。")
    doc.svg(SV + "min_cost_hire_core.svg", "按 rate 排序固定一维; heap 里留 q 最小的 k 个压低 total_q")
    doc.svg(SV + "min_cost_hire_trace.svg", "trace: A–E 按 rate 升序, k = 3, heap 存 q, 每步 pop 最大的 q, total_q 为 heap 里所有 q 相加")
    doc.code(C_HIRE)
    doc.p("Time: sort O(n log n) + heap O(n log k) = O(n log n)。Space: O(n)。")
    doc.h3("同一个套路的两道变体")
    doc.p("Maximum Number of Events: 排序 start, heap 存 end, 每天参加 end 最早的 (最急的)。"
          "IPO: 排序 capital, heap 存 profit, 做得起的项目里挑 profit 最大的 (max-heap)。形状一样: 按一个量排序, 往前推进时把 \"现在可选的\" 放进 heap, heap 的 top 决定选谁。")
    doc.code(C_EVENTS)
    doc.code(C_IPO)
    doc.note("两个维度互相牵制 → 排序一维, heap 管另一维; total_q 就是 heap 里所有 q 相加。")

    # ------------------------------------------------------------ 7
    doc.h2("7. Task Scheduler: greedy + heap, 加一个 cooldown 队列")
    doc.p("题目: 一串 task (字母), 同一种 task 两次执行之间至少隔 n 个 slot, 可以 idle。求最少需要多少 slot。例: <code>tasks = AAABBC, n = 2</code> → 7 (A B C A B idle A)。")
    doc.p("Brute force: 枚举所有执行顺序, 指数级。关键观察 (greedy): 剩余次数最多的 task 间隔要求最紧, 每个 slot 都做 \"当前能做的里剩余最多的\", 不会被迫在最后只剩它一个而 idle。"
          "\"当前能做的里剩余最多\" 就是 max-heap 的 top。刚做过的 task 不能马上再做, 先放进 cooldown 队列, 过了 n 个 slot 再 push 回 heap。")
    doc.p("相比前几题: heap 里元素会 <b>回来</b> (不是 pop 就扔掉), 要配一个 FIFO 队列管冷却时间。heap 为空但 cooldown 非空 → 这个 slot 是 idle。")
    doc.svg(SV + "task_scheduler_core.svg", "heap = 现在能做的; cooldown = 刚做过; 每个 slot 做 heap 里剩余最多的")
    doc.svg(SV + "task_scheduler_trace.svg", "trace: slot 6 heap 空, 只能 idle 等 A 回来, 总共 7 个 slot")
    doc.code(C_TASK)
    doc.p("Time: 每个 slot O(log m) (m = task 种类数, 至多 26), slot 总数 T, 共 O(T log m)。Space: O(m)。"
          "只要答案有公式: <code>max(len(tasks), (max_count - 1) * (n + 1) + 达到 max_count 的 task 种类数)</code>。"
          "Reorganize String 是同一个结构 (n = 1): 每次 pop 剩余最多的字符, 上一个用过的先放一边, 下一步再 push 回来。")
    doc.note("\"每步选当前最优\" + 候选会变化 → greedy + heap; 用过要等一阵 → 再加 cooldown 队列。")

    # ------------------------------------------------------------ 8
    doc.h2("8. 识别信号: 看到什么 → 试什么")
    doc.raw('''<table>
<tr><th>题目特征</th><th>做法</th><th>complexity</th></tr>
<tr><td>第 k 大 / 前 k 大 / 前 k 个出现最多</td><td>size-k min-heap, top 是门槛</td><td>O(n log n) → O(n log k)</td></tr>
<tr><td>前 k 小 / 离某点最近的 k 个</td><td>size-k max-heap (存负数), 踢最大的</td><td>O(n log n) → O(n log k)</td></tr>
<tr><td>k 条有序 list / 矩阵每行有序, 要合并或第 k 小</td><td>heap 放每条的当前头, pop 一个补一个</td><td>O(N log N) → O(N log k)</td></tr>
<tr><td>数据流, 随时要中位数</td><td>两个 heap: lo (max) + hi (min), 大小差 ≤ 1</td><td>每次 O(n) 或 O(n log n) → add O(log n), find O(1)</td></tr>
<tr><td>两个维度互相牵制, 求最小/最大 cost 或个数</td><td>排序一维, heap 管另一维 (Hire Workers, Events, IPO)</td><td>O(n^k) 枚举 → O(n log n)</td></tr>
<tr><td>每步选 "当前最优", 候选会变, 用过要冷却</td><td>greedy + heap, 加 cooldown 队列 (Task Scheduler, Reorganize String)</td><td>指数 → O(T log m)</td></tr>
<tr><td>反复取最大再放回 (Last Stone Weight)</td><td>max-heap, pop 两个, 差值 push 回</td><td>每轮 O(n) 找最大 → O(log n)</td></tr>
<tr><td>只要一个 top, 不要全序</td><td>先问自己: 是不是不用 sort 全部</td><td>O(n log n) → O(n log k)</td></tr>
</table>''')
    doc.p("选 min 还是 max 的一条规则: top 放 \"最该被踢掉的\"。留大的 → 踢小的 → min-heap; 留小的 → 踢大的 → max-heap。")

    doc.h2("以后再学")
    doc.p("quickselect (平均 O(n) 的第 k 大)、lazy delete (Sliding Window Median 里删元素)、indexed heap / decrease-key (Dijkstra 的变体)、Skyline / Car Pooling 的 sweep line + heap。")
    doc.write("docs/09-heap.html")


if __name__ == "__main__":
    build()
