from svglib import *
from gen_traces import save, OUT

def box(s, x, y, w, h, lines, role='norm', ring=False, dash=None, size=14, fill=None):
    s.rect(x, y, w, h, role, 4, 1, dash, fill=fill)
    if ring:
        s.el.append('<rect x="%s" y="%s" width="%s" height="%s" rx="6" fill="none" stroke="%s" stroke-width="2.5"/>' % (x - 4, y - 4, w + 8, h + 8, RING))
    t = ROLE[role][2]
    n = len(lines); step = 16
    y0 = y + h / 2 - (n - 1) * step / 2
    for i, l in enumerate(lines):
        s.text(x + w / 2, y0 + i * step, l, size, 'middle', t)

def txt(s, x, y, lines, size=14, fill=INK, step=22, bold_first=False):
    for i, l in enumerate(lines):
        s.text(x, y + i * step, l, size, 'start', fill, bold=(bold_first and i == 0))
    return y + step * len(lines)

# ------------------------------------------------------------------ 0 first principles
def heap_core():
    s = S('h0', 'Heap core: parent <= children, top is the minimum', 'tree and array views of a min-heap, push/pop cost, and comparison with list')
    s.text(40, 18, 'min-heap: 每个 parent ≤ 它的两个 children → 最小的永远在 top (index 0)', 14, 'start', INK)
    s.text(40, 38, 'tree 只是画法, 底层就是一个 list: index i 的 children = 2i+1, 2i+2', 14, 'start', SUB)
    arr = [1, 3, 2, 7, 4, 5, 6]
    s.tree([(str(v),) for v in arr], 170, 90, dxs=(0, 62, 30), ystep=52)
    # array
    for i, v in enumerate(arr):
        box(s, 30 + i * 42, 238, 42, 32, [str(v)], 'norm', ring=(i == 0))
        s.text(30 + i * 42 + 21, 286, str(i), 12, 'middle', SUB)
    s.text(30, 306, 'list = [1, 3, 2, 7, 4, 5, 6]   (heapq 里就是这个 list)', 12, 'start', SUB)
    # right text
    s.text(360, 78, '保证的', 14, 'start', INK, bold=True)
    txt(s, 360, 100, ['parent ≤ children → top 最小, 看一眼 O(1)'], 14)
    s.text(360, 140, '不保证的', 14, 'start', INK, bold=True)
    txt(s, 360, 162, ['同一层谁大谁小 (3 vs 2) 没有顺序', '→ 不是全序, 所以比 sort 便宜'], 14)
    s.text(360, 218, 'push / pop', 14, 'start', INK, bold=True)
    txt(s, 360, 240, ['push: 放末尾, 比 parent 小就往上换', 'pop: 取走 top, 末尾补到 top, 往下换', '树高 log n → 都是 O(log n)'], 14)
    s.sep(334)
    # table
    s.text(40, 358, '要反复拿最小的, 用什么存?', 14, 'start', INK, bold=True)
    cols = [40, 250, 380, 520]
    for x, t in zip(cols, ['结构', '拿最小的', '加一个数', '']):
        if t: s.text(x, 384, t, 14, 'start', SUB)
    rows = [('无序 list', 'O(n) 要扫一遍', 'O(1)'), ('有序 list (每次 sort)', 'O(1)', 'O(n) 要搬位置'), ('heap', 'O(1)', 'O(log n)')]
    for i, (a, b, c) in enumerate(rows):
        y = 408 + 24 * i
        s.text(cols[0], y, a, 14, 'start', INK, bold=(i == 2)); s.text(cols[1], y, b, 14, 'start', INK, bold=(i == 2)); s.text(cols[2], y, c, 14, 'start', INK, bold=(i == 2))
    s.sep(490)
    txt(s, 40, 512, ['heap 只要 "top", 不要全序: 取前 k 个 O(n log k), sort 是 O(n log n)', 'Python heapq 只有 min-heap; max-heap 存 -x, 图里一律画正数 (top = 最大)'], 14, SUB, 22)
    save(s, 564, 'heap_core.svg')

# ------------------------------------------------------------------ Kth core
def kth_core():
    s = S('kc0', 'Kth Largest: why a min-heap of size k', 'sorted nums with the top-k kept in the heap, top is the kth largest')
    s.text(40, 18, 'nums = [3, 2, 1, 5, 6, 4], k = 2 (下面按大小排好, 只为看清谁留下)', 14, 'start', INK)
    vals = [1, 2, 3, 4, 5, 6]
    for i, v in enumerate(vals):
        role = 'norm' if v >= 5 else 'pop'
        box(s, 40 + i * 54, 56, 46, 36, [str(v)], role, dash='4 3' if role == 'pop' else None, ring=(v == 5))
    txt(s, 40, 118, ['1, 2, 3, 4 : 已被 pop 掉'], 12, '#712B13')
    txt(s, 40 + 4 * 54, 118, [], 12)
    s.text(256, 118, '5, 6 : 最大的 k = 2 个, 留在 heap', 12, 'start', SUB)
    s.tree([('5',), ('6',)], 560, 80, dxs=(0, 34, 22), ystep=40)
    s.path('M364 74 L506 74', EDGE, 1.5)
    s.text(435, 58, '留下的 k 个 = min-heap', 12, 'middle', SUB)
    s.text(560, 150, 'top = 5 = 第 2 大', 14, 'middle', INK, bold=True)
    s.sep(176)
    s.text(40, 190, '为什么是 min-heap, 不是 max-heap', 14, 'start', INK, bold=True)
    txt(s, 40, 214, [
        '1. heap 里装 "目前最大的 k 个", 满了要踢一个, 踢的永远是里面最小的',
        '2. 要立刻拿到 "里面最小的" → 它放 top → min-heap',
        '3. 留下来的 k 个里最小的 = 整体第 k 大 → 答案就是 h[0]',
    ], 14)
    s.sep(290)
    s.text(40, 314, '新来的 x 和 top 比', 14, 'start', INK, bold=True)
    txt(s, 40, 338, ['x < top (例: x = 4 < 5): 进不了前 2 大 → push 完马上被 pop, 什么都没变',
                     'x > top: 挤掉 top, 新的 top 变大, 门槛抬高'], 14)
    s.sep(396)
    txt(s, 40, 418, ['brute force: sort 再取第 k 个 O(n log n) · min-heap 只留 k 个: O(n log k), 空间 O(k)'], 14, INK, bold_first=True)
    save(s, 440, 'kth_largest_core.svg')

# ------------------------------------------------------------------ Top K freq core
def topk_core():
    s = S('tk0', 'Top K Frequent: Counter then size-k heap on count', 'flow from nums to Counter to heap of (count, num)')
    s.text(40, 18, '和 Kth Largest 是同一个模板: 比较的 key 从 "值" 换成 "count"', 14, 'start', INK)
    box(s, 40, 70, 176, 64, ['nums =', '[1,1,1,2,2,3,4,4,4,4]'], 'norm', size=14)
    s.path('M216 102 L270 102', EDGE, 1.5)
    s.text(243, 84, 'Counter', 12, 'middle', SUB)
    box(s, 274, 70, 140, 64, ['1 → 3 次   2 → 2 次', '3 → 1 次   4 → 4 次'], 'norm', size=12)
    s.path('M414 102 L452 102', EDGE, 1.5)
    s.tree([('3', 'n=1'), ('4', 'n=4')], 556, 96, dxs=(0, 36, 22), ystep=46)
    s.text(556, 48, 'size k=2 的 min-heap', 12, 'middle', SUB)
    s.text(556, 176, 'node = (count, num)', 12, 'middle', SUB)
    s.text(556, 194, 'top = count 最小的 (门槛)', 12, 'middle', SUB)
    s.sep(214)
    s.text(40, 236, '三种做法, 差别只在 "怎么挑 count 最大的 k 个"', 14, 'start', INK, bold=True)
    s.text(40, 260, '(m = 不同数字的个数, m ≤ n)', 12, 'start', SUB)
    rows = [('全部按 count sort', 'O(m log m)', '最直接'),
            ('size-k min-heap', 'O(m log k)', '本节, k 小的时候省'),
            ('bucket: count 当 index', 'O(n)', 'count 最大 ≤ n, 不用比较')]
    for i, (a, b, c) in enumerate(rows):
        y = 290 + 26 * i
        s.text(40, y, a, 14, 'start', INK, bold=(i == 1)); s.text(250, y, b, 14, 'start', INK, bold=(i == 1)); s.text(370, y, c, 14, 'start', SUB)
    s.sep(382)
    txt(s, 40, 404, ['Top K Frequent Words: 同一个模板, 只是 count 相同时要按字典序, 把 key 换成 (count, word) 处理'], 12, SUB)
    save(s, 436, 'top_k_frequent_core.svg')

# ------------------------------------------------------------------ K Closest core
def closest_core():
    s = S('cc0', 'K Closest: keep-largest uses min-heap, keep-smallest uses max-heap', 'rule: heap top is the element to evict')
    s.text(40, 18, '规则: heap 里放 "留下的 k 个", top 放 "最该被踢掉的"', 14, 'start', INK, bold=True)
    s.rect(40, 36, 290, 196, 'norm', 6, 1, fill='#FFFFFF'); s.rect(350, 36, 290, 196, 'norm', 6, 1, fill='#FFFFFF')
    s.text(185, 56, 'Kth Largest', 14, 'middle', INK, bold=True)
    s.text(185, 76, '留下最大的 k 个 → 踢最小的', 12, 'middle', SUB)
    s.tree([('5',), ('6',)], 185, 118, dxs=(0, 34, 22), ystep=46)
    s.text(185, 208, 'top = 最小 → min-heap', 14, 'middle', INK)
    s.text(495, 56, 'K Closest Points', 14, 'middle', INK, bold=True)
    s.text(495, 76, '留下 d 最小的 k 个 → 踢 d 最大的', 12, 'middle', SUB)
    s.tree([('4',), ('2',)], 495, 118, dxs=(0, 34, 22), ystep=46)
    s.text(495, 208, 'top = 最大 → max-heap', 14, 'middle', INK)
    s.sep(252)
    txt(s, 40, 276, ['heapq 只有 min-heap, max-heap 的写法是存负数:',], 14, INK)
    txt(s, 40, 300, ['heappush(h, (-d, x, y))   # 存 -d, 所以 top 是 -d 最小 = d 最大', 'heappop(h)                 # 弹出 d 最大的', '图里一律画正数 d, 右边那棵 top = 4 就是 -4 最小'], 12, SUB, 20)
    s.sep(376)
    txt(s, 40, 398, ['d = x² + y², 不用开根号 (比大小等价)', 'sort 全部: O(n log n) · size-k heap: O(n log k)'], 14, INK)
    save(s, 450, 'k_closest_core.svg')

# ------------------------------------------------------------------ Merge core
def merge_core():
    s = S('mc0', 'Merge k Sorted Lists: heap holds one head per list', 'three lists, heads in heap')
    s.text(40, 18, 'heap 里每条 list 只放 1 个: 它当前的 head', 14, 'start', INK, bold=True)
    L = [[1, 4, 5], [1, 3, 4], [2, 6]]
    for r, l in enumerate(L):
        y = 88 + r * 50
        s.text(40, y, 'L%d' % r, 14, 'start', INK)
        for j, v in enumerate(l):
            x = 100 + j * 64
            s.node(x, y, 'norm' if j == 0 else 'out', str(v), r=18)
            if j + 1 < len(l):
                s.path('M%d %d L%d %d' % (x + 20, y, x + 64 - 22, y), EDGE, 1.2)
    s.text(100, 52, 'head', 12, 'middle', SUB)
    s.path('M300 138 L400 138', EDGE, 1.5)
    s.text(350, 120, 'push head', 12, 'middle', SUB)
    s.tree([('1', 'L0'), ('1', 'L1'), ('2', 'L2')], 520, 96, dxs=(0, 38), ystep=50)
    s.text(520, 192, 'min-heap, 大小 = k = 3', 12, 'middle', SUB)
    s.sep(222)
    s.text(40, 246, '为什么只要 head', 14, 'start', INK, bold=True)
    txt(s, 40, 270, ['每条 list 本身有序 → 全局最小的一定是某条 list 的 head',
                     'pop 出它 → 它的 next 成为这条 list 新的 head → push 回去',
                     'heap 里永远 ≤ k 个, 所以 pop / push 都是 O(log k)'], 14)
    s.sep(346)
    txt(s, 40, 368, ['N = 所有 node 总数', '全部倒出来 sort: O(N log N)', 'heap 每个 node 进出各 1 次: O(N log k)'], 14, INK, 22)
    s.text(40, 456, 'tuple 里放 i: val 相同时靠 i 决胜负, 不会去比较 ListNode (没有 < )', 12, 'start', SUB)
    save(s, 484, 'merge_k_lists_core.svg')

# ------------------------------------------------------------------ Median core
def median_core():
    s = S('mdc', 'Median: two heaps hold the two halves', 'sorted numbers split into lo and hi, tops are the middle numbers')
    s.text(40, 18, '把排好序的数从中间切开: 左半 lo, 右半 hi · 中位数只看切口两边的数', 14, 'start', INK, bold=True)
    vals = [1, 2, 3, 5, 8, 9]
    xs = [170, 222, 274, 366, 418, 470]
    for v, x in zip(vals, xs):
        box(s, x, 56, 46, 34, [str(v)], 'norm', ring=(v in (3, 5)))
    s.line(340, 50, 340, 98, '#5F5E5A', 1.5, '4 3')
    s.text(248, 40, 'lo: 较小的一半', 12, 'middle', SUB)
    s.text(441, 40, 'hi: 较大的一半', 12, 'middle', SUB)
    s.tree([('3',), ('2',), ('1',)], 200, 190, dxs=(0, 36), ystep=44)
    s.tree([('5',), ('9',), ('8',)], 480, 190, dxs=(0, 36), ystep=44)
    s.path('M297 94 L221 164', EDGE, 1.2); s.path('M389 94 L465 164', EDGE, 1.2)
    s.text(200, 262, 'lo = max-heap', 14, 'middle', INK); s.text(200, 280, 'top = 3 (lo 里最大)', 12, 'middle', SUB)
    s.text(480, 262, 'hi = min-heap', 14, 'middle', INK); s.text(480, 280, 'top = 5 (hi 里最小)', 12, 'middle', SUB)
    s.sep(302)
    txt(s, 40, 326, ['median = (lo.top + hi.top) / 2 = (3 + 5) / 2 = 4   (个数是奇数时 = lo.top)'], 14, INK, bold_first=True)
    s.text(40, 358, '两个 invariant (每次 add 后都要成立)', 14, 'start', INK, bold=True)
    txt(s, 40, 382, ['1. max(lo) ≤ min(hi)   → 两个 top 紧挨着切口', '2. len(lo) = len(hi) 或 len(lo) = len(hi) + 1   → 切口在正中间'], 14)
    s.sep(438)
    txt(s, 40, 460, ['每个数 add: O(log n) · 找 median: O(1)', 'brute force: 每次 find 都 sort O(n log n), 或者插入有序 list O(n)'], 14, SUB)
    save(s, 506, 'median_stream_core.svg')

# ------------------------------------------------------------------ Hire core
def hire_core():
    s = S('hc0', 'Hire K Workers: sort by rate, heap drops the biggest q', 'worker D is current, B has the biggest q and is dropped')
    s.text(40, 18, 'rate = wage / q · 每人 wage = rate × q · k = 3 · 现在处理到 D', 14, 'start', INK, bold=True)
    s.text(40, 38, '先按 rate 升序排好, 从左往右处理 (rate 越来越大)', 12, 'start', SUB)
    W = [('A', 10, 2, 'norm'), ('B', 20, 3, 'pop'), ('C', 5, 4, 'norm'), ('D', 8, 5, 'norm'), ('E', 9, 7, 'out')]
    for i, (n, q, r, role) in enumerate(W):
        x = 40 + i * 80
        box(s, x, 60, 66, 54, [n, 'q = %d' % q, 'rate = %d' % r], role, ring=(n == 'D'), dash='4 3' if role in ('pop', 'out') else None)
    s.text(40 + 4 * 80 + 33, 130, '还没处理', 12, 'middle', SUB)
    s.text(40 + 1 * 80 + 33, 130, 'q 最大, 被踢', 12, 'middle', '#712B13')
    s.tree([('10',), ('8',), ('5',)], 560, 78, dxs=(0, 38), ystep=40)
    s.text(560, 152, 'max-heap: group 的 q', 12, 'middle', SUB)
    s.sep(172)
    s.text(40, 194, '1. 为什么 rate 取当前这个 (D 的 rate = 5)', 14, 'start', INK, bold=True)
    txt(s, 40, 216, ['group 里每个人 wage = 5 × q, 而其他人的 rate ≤ 5 → 5 × q ≥ 他们的最低 wage, 都合法',
                     'rate 取当前这个就是 group 里最大的 rate, 不能再小 (D 自己的最低 wage 就要 rate = 5)'], 12, INK, 18)
    s.text(40, 270, '2. rate 固定后, 只能压 total_q', 14, 'start', INK, bold=True)
    txt(s, 40, 292, ['cost = rate × total_q → 从 A, B, C, D 里选 k = 3 个 q 最小的 → 踢 q 最大的 B (20)'], 12, INK, 18)
    s.text(40, 328, '3. 具体数字', 14, 'start', INK, bold=True)
    txt(s, 40, 350, ['total_q = 10 + 8 + 5 = 23', 'cost = rate × total_q = 5 × 23 = 115'], 14, INK, 22)
    s.sep(406)
    txt(s, 40, 428, ['brute force: 枚举 C(n, k) 个 group · 排序一维 (rate) + heap 管另一维 (q): O(n log n)'], 14, SUB)
    save(s, 460, 'min_cost_hire_core.svg')

# ------------------------------------------------------------------ Task core
def task_core():
    s = S('tc0', 'Task Scheduler: ready heap and cooldown queue', 'pop the most frequent ready task, it waits in cooldown, then returns to heap')
    s.text(40, 18, 'heap = 现在能做的 task (剩余次数最多的在 top) · cooldown = 刚做过, 还要等', 14, 'start', INK, bold=True)
    s.tree([('3', 'A'), ('2', 'B'), ('1', 'C')], 110, 90, dxs=(0, 40), ystep=46)
    s.text(110, 36, 'heap (max-heap)', 12, 'middle', SUB)
    for i, (t, c) in enumerate([('A', 2), ('B', 1)]):
        box(s, 440 + i * 100, 78, 84, 44, ['%s 剩 %d' % (t, c)], 'norm', size=14)
    s.text(530, 62, 'cooldown 队列 (先进先出)', 12, 'middle', SUB)
    s.path('M170 96 L432 96', EDGE, 1.5)
    s.text(300, 78, 'pop 一个 = 这个 slot 执行 1 次', 12, 'middle', INK)
    s.text(300, 114, '剩余 > 0 → 进 cooldown', 12, 'middle', SUB)
    s.path('M490 122 L490 190 L110 190 L110 150', EDGE, 1.5)
    s.text(300, 176, '过了 n 个 slot → push 回 heap', 12, 'middle', INK)
    s.sep(214)
    s.text(40, 238, '为什么每次 pop 剩余最多的 (greedy)', 14, 'start', INK, bold=True)
    txt(s, 40, 260, ['次数最多的 task 间隔要求最紧, 先做它, 才不会最后只剩它一个而被迫 idle',
                     'heap 空但 cooldown 非空 → 这个 slot idle, time 照样 +1'], 14)
    s.sep(318)
    s.text(40, 342, '只要答案时的公式 (不用模拟)', 14, 'start', INK, bold=True)
    txt(s, 40, 364, ['max(len(tasks), (max_count - 1) × (n + 1) + 有几种 task 达到 max_count)', '例: max(6, (3 - 1) × (2 + 1) + 1) = max(6, 7) = 7'], 14, INK)
    s.sep(420)
    txt(s, 40, 442, ['Reorganize String 同构: n = 1, 每次 pop 剩余最多的, 刚用过的先放一边, 下一步再 push 回来'], 12, SUB)
    save(s, 470, 'task_scheduler_core.svg')

if __name__ == '__main__':
    heap_core(); kth_core(); topk_core(); closest_core(); merge_core(); median_core(); hire_core(); task_core()
