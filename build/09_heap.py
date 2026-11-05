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
    g = dict(globals())
    exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "09_heap_doc.py"), encoding="utf-8").read(), g)


if __name__ == "__main__":
    build()
