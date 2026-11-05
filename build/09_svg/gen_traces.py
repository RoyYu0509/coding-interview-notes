import os, heapq
from collections import Counter, deque
from svglib import *
OUT = '/home/user/coding-interview-notes/docs/svg/09-heap'
os.makedirs(OUT, exist_ok=True)

def header(s, l1, l2, titles):
    s.text(40, 18, l1, 14, 'start', INK)
    s.text(40, 38, l2, 14, 'start', SUB)
    for x, t in titles: s.text(x, 64, t, 14, 'start', INK, bold=True)
    s.sep(74)
    return 74

def save(s, H, name):
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(s.render(H))
    print('wrote', name, H)

def footer(s, y, lines, leg, leg_y_gap=26):
    y += 22
    for t in lines:
        s.text(40, y, t, 14, 'start', INK, bold=True); y += 22
    y += 10
    legend(s, y, leg)
    return y + 20

# ---------------------------------------------------------------- Kth Largest
def kth_trace():
    s = S('kth', 'Kth Largest Element: min-heap of size k trace', 'nums=[3,2,1,5,6,4], k=2')
    y = header(s, 'k = 2 · min-heap · 每一步: push 进 heap → 超过 k 个就 pop 最小的',
               'heap 里永远是 "目前最大的 k 个" · top = 其中最小的 = 目前的第 k 大',
               [(40, 'x'), (160, 'push 后'), (290, 'pop 后'), (440, '计算')])
    nums = [3, 2, 1, 5, 6, 4]; k = 2; h = []; rows = []
    for i, x in enumerate(nums):
        heapq.heappush(h, x); pushed = list(h); p = None
        if len(h) > k: p = heapq.heappop(h)
        row = dict(box=['x = %d' % x, 'i = %d' % i], items1=[(str(v),) for v in pushed], new1=[pushed.index(x)])
        top_line = ['heap 里 (最大的 %d 个):' % k, ', '.join(map(str, sorted(h)))]
        if p is not None:
            row['popped'] = dict(node=(str(p),), lines=['len = %d > k = %d' % (len(pushed), k), 'pop 最小的 %d' % p])
            row['items2'] = [(str(v),) for v in h]
            row['calc'] = top_line + [('第 %d 大 = top = %d' % (k, h[0]), True)]
        else:
            row['noop'] = ['len = %d %s k = %d' % (len(h), '≤' if len(h) <= k else '>', k), '不需要 pop']
            row['calc'] = top_line + ([('第 %d 大 = top = %d' % (k, h[0]), True)] if len(h) == k else ['len < k, 还没有第 %d 大' % k])
        rows.append(row)
    y = trace_rows(s, y, rows)
    assert h == [5, 6]
    H = footer(s, y, ['答案: 最后 heap 的 top = 5   (排序验证: 6, 5, 4, 3, 2, 1 的第 2 个 = 5)'],
               [('new', '新 push 进来的', 120), ('pop', '被 pop 的', 100), ('ring', 'heap top (最小的)', 140), ('norm', 'heap 里其他的', 120)])
    save(s, H, 'kth_largest_trace.svg')

# ---------------------------------------------------------------- Top K Frequent
def topk_trace():
    s = S('tkf', 'Top K Frequent Elements trace', 'nums=[1,1,1,2,2,3,4,4,4,4], k=2')
    y = header(s, 'k = 2 · Counter 之后 · min-heap 存 (count, num), 按 count 比大小',
               'node 上面的数字 = count, 下面 n = num · 每一步: push → 超过 k 个就 pop count 最小的',
               [(40, 'num : count'), (160, 'push 后'), (290, 'pop 后'), (440, '计算')])
    nums = [1, 1, 1, 2, 2, 3, 4, 4, 4, 4]; k = 2; h = []; rows = []
    cnt = Counter(nums); assert dict(cnt) == {1: 3, 2: 2, 3: 1, 4: 4}
    lab = lambda t: (str(t[0]), 'n=%d' % t[1])
    for num, c in cnt.items():
        heapq.heappush(h, (c, num)); pushed = list(h); p = None
        if len(h) > k: p = heapq.heappop(h)
        row = dict(box=['num = %d' % num, 'c = %d' % c], items1=[lab(t) for t in pushed], new1=[pushed.index((c, num))])
        keep = '  '.join('(%d,%d)' % t for t in sorted(h, reverse=True))
        if p:
            row['popped'] = dict(node=lab(p), lines=['len = %d > k = %d' % (len(pushed), k), 'pop count 最小的 %d' % p[0]])
            row['items2'] = [lab(t) for t in h]
        else:
            row['noop'] = ['len = %d ≤ k = %d' % (len(h), k), '不需要 pop']
        row['calc'] = ['heap 里 (count, num):', keep] + ([('count 最大的 %d 个: num = %s' % (k, ', '.join(str(t[1]) for t in sorted(h, reverse=True))), True)] if p else ['len ≤ k, 都留着'])
        rows.append(row)
    y = trace_rows(s, y, rows)
    assert sorted(h) == [(3, 1), (4, 4)]
    H = footer(s, y, ['答案: heap 里剩 (3, 1) 和 (4, 4) → num = [1, 4]'],
               [('new', '新 push 进来的', 120), ('pop', '被 pop 的', 100), ('ring', 'heap top (最小的 count)', 170), ('norm', 'heap 里其他的', 120)])
    save(s, H, 'top_k_frequent_trace.svg')

# ---------------------------------------------------------------- K Closest
def closest_trace():
    s = S('kc', 'K Closest Points to Origin trace', 'points=[[3,3],[5,-1],[-2,4],[1,1],[0,2]], k=2')
    y = header(s, 'k = 2 · max-heap (最大的 d 在 top) · 每一步: push → 超过 k 个就 pop 最大的 d',
               'd = x² + y² (不开根号) · heap 里永远是 "目前离原点最近的 k 个"',
               [(40, 'point'), (160, 'push 后'), (290, 'pop 后'), (440, '计算')])
    pts = [[3, 3], [5, -1], [-2, 4], [1, 1], [0, 2]]; k = 2; h = []; rows = []
    lab = lambda t: (str(t[0]), 'P%d' % (t[1] + 1))
    for i, (x, yy) in enumerate(pts):
        d = x * x + yy * yy
        heapq.heappush(h, (-d, i)); pushed = [(-a, b) for a, b in h]; p = None
        if len(h) > k:
            a, b = heapq.heappop(h); p = (-a, b)
        row = dict(box=['P%d' % (i + 1), '(%d, %d)' % (x, yy), 'd = %d' % d], items1=[lab(t) for t in pushed], new1=[pushed.index((d, i))])
        cur = [(-a, b) for a, b in h]
        if p:
            row['popped'] = dict(node=lab(p), lines=['len = %d > k = %d' % (len(pushed), k), 'pop 最大的 d = %d' % p[0]])
            row['items2'] = [lab(t) for t in cur]
        else:
            row['noop'] = ['len = %d ≤ k = %d' % (len(h), k), '不需要 pop']
        row['calc'] = ['d = %d² + %d² = %d' % (abs(x), abs(yy), d), 'heap 里最近的 %s 个:' % len(h) if False else '最近的 %d 个: %s' % (len(h), ', '.join('P%d' % (b + 1) for a, b in sorted(cur)))]
        rows.append(row)
    y = trace_rows(s, y, rows)
    assert sorted((-a, b) for a, b in h) == [(2, 3), (4, 4)]
    H = footer(s, y, ['答案: heap 里剩 P4 (d = 2), P5 (d = 4) → [[1, 1], [0, 2]]'],
               [('new', '新 push 进来的', 120), ('pop', '被 pop 的', 100), ('ring', 'heap top (最大的 d)', 150), ('norm', 'heap 里其他的', 120)])
    save(s, H, 'k_closest_trace.svg')

# ---------------------------------------------------------------- Merge k lists
def merge_trace():
    s = S('mk', 'Merge k Sorted Lists trace', 'L0=1,4,5  L1=1,3,4  L2=2,6')
    y = header(s, 'L0 = 1→4→5 · L1 = 1→3→4 · L2 = 2→6 · heap 存 (val, i, node), 按 val 比 · 最小的在 top',
               'heap 里每条 list 只放 1 个 (当前的 head) · 每一步: pop 最小的 → 接到 output → push 它的 next',
               [(40, 'step'), (160, 'pop 前'), (290, 'push next 后'), (440, 'output')])
    L = [[1, 4, 5], [1, 3, 4], [2, 6]]
    h = [(l[0], i, 0) for i, l in enumerate(L)]; heapq.heapify(h)
    lab = lambda t: (str(t[0]), 'L%d' % t[1])
    rows = [dict(box=['init'], items1=[], items2=[lab(t) for t in h], new2=[0, 1, 2],
                 noop=None, calc=['每条 list 的 head', 'push 进 heap', 'heap 大小 = k = 3'], pushonly=True)]
    out = []
    for step in range(1, 6):
        pre = list(h)
        v, i, j = heapq.heappop(h); out.append(v)
        nxt = None
        if j + 1 < len(L[i]):
            nxt = (L[i][j + 1], i, j + 1); heapq.heappush(h, nxt)
        row = dict(box=['step %d' % step], items1=[lab(t) for t in pre],
                   popped=dict(node=lab((v, i)), lines=['pop 最小的 %d (L%d)' % (v, i), '接到 output']),
                   items2=[lab(t) for t in h], new2=[h.index(nxt)] if nxt else [],
                   calc=['output: ' + ' → '.join(map(str, out)), 'push next: %s' % ('%d (L%d 的下一个)' % (nxt[0], nxt[1]) if nxt else '无')])
        rows.append(row)
    # init row special: draw only post tree with green nodes
    y0 = y
    y = trace_rows(s, y, rows, in_arrow=False)
    assert out == [1, 1, 2, 3, 4]
    H = footer(s, y, ['继续 pop 到 heap 空: output = 1→1→2→3→4→4→5→6 (8 个 node, 每个进出 heap 各 1 次)'],
               [('new', '新 push 进来的', 120), ('pop', '被 pop 的', 100), ('ring', 'heap top (最小的 val)', 160), ('norm', 'heap 里其他的', 120)])
    save(s, H, 'merge_k_lists_trace.svg')

# ---------------------------------------------------------------- Min cost hire
def hire_trace():
    s = S('hw', 'Minimum Cost to Hire K Workers: max-heap trace', 'k=3 workers A..E sorted by rate')
    y = header(s, 'k = 3 · 每一步: push 进 heap → 超过 k 个就 pop 最大的 q → 算 cost',
               'total_q = 当前 group (heap 里所有节点) 的 q 全部相加 · cost = rate × total_q',
               [(40, 'worker'), (160, 'push 后'), (290, 'pop 后'), (440, '计算')])
    q = [10, 20, 5, 8, 9]; w = [20, 60, 20, 40, 63]; k = 3
    ws = sorted(zip(q, w), key=lambda t: t[1] / t[0]); names = 'ABCDE'
    assert [t[0] for t in ws] == q
    h = []; tot = 0; rows = []; costs = []
    for idx, (qq, ww) in enumerate(ws):
        rate = ww // qq; assert ww == rate * qq
        heapq.heappush(h, -qq); tot += qq; pushed = [-a for a in h]; p = None
        if len(h) > k:
            p = -heapq.heappop(h); tot -= p
        cur = [-a for a in h]
        row = dict(box=[names[idx], 'q = %d' % qq, 'rate = %d' % rate], items1=[(str(v),) for v in pushed], new1=[pushed.index(qq)])
        if p:
            row['popped'] = dict(node=(str(p),), lines=['len = %d > k = %d' % (len(pushed), k), 'pop 最大的 %d' % p])
            row['items2'] = [(str(v),) for v in cur]
        else:
            row['noop'] = ['len = %d ≤ k = %d' % (len(h), k), '不需要 pop']
        ssum = ' + '.join(str(v) for v in sorted(cur, reverse=True))
        calc = [('total_q (group 里所有 q 相加):'), (ssum + ' = %d' % tot if len(cur) > 1 else '%d' % tot)]
        if len(cur) == k:
            calc += ['cost = rate × total_q', '%d × %d = %d' % (rate, tot, rate * tot)]; costs.append(rate * tot)
        else:
            calc += ['len < k, skip']
        row['calc'] = calc
        rows.append(row)
    assert costs == [140, 115, 154]
    y = trace_rows(s, y, rows)
    H = footer(s, y, ['min_cost = min(140, 115, 154) = 115'],
               [('new', '新 push 进来的', 120), ('pop', '被 pop 的', 100), ('ring', 'heap top (最大的 q)', 150), ('norm', 'heap 里其他的', 120)])
    save(s, H, 'min_cost_hire_trace.svg')

# ---------------------------------------------------------------- Median
def median_trace():
    s = S('md', 'Find Median from Data Stream: two heaps trace', 'stream 5,2,8,3,9,1')
    s.text(40, 18, 'lo = max-heap (较小的一半, top = 最大) · hi = min-heap (较大的一半, top = 最小)', 14, 'start', INK)
    s.text(40, 38, '每个 num: 先 push 进 lo → lo 的 top 移到 hi → hi 比 lo 多就把 hi 的 top 移回 lo', 14, 'start', SUB)
    for x, t in [(40, 'num'), (130, 'lo (max-heap)'), (270, 'hi (min-heap)'), (400, '这一步发生了什么')]:
        s.text(x, 64, t, 14, 'start', INK, bold=True)
    s.sep(74)
    lo = []; hi = []; y = 74
    for num in [5, 2, 8, 3, 9, 1]:
        heapq.heappush(lo, -num)
        m = -heapq.heappop(lo); heapq.heappush(hi, m)
        back = None
        if len(hi) > len(lo):
            back = heapq.heappop(hi); heapq.heappush(lo, -back)
        assert len(lo) - len(hi) in (0, 1) and -lo[0] <= hi[0] if hi else True
        med = -lo[0] if len(lo) > len(hi) else (-lo[0] + hi[0]) / 2
        L = [-a for a in lo]; Hh = list(hi)
        # green = elements that moved this step
        newlo = [L.index(num if back is None and m != num else (back if back is not None else num))] if True else []
        # lo-new: either num (stayed) or back (moved from hi)
        lo_new = back if back is not None else (num if m != num else None)
        hi_new = m if (back is None or m != back) else None
        if m == num and back is None: lo_new = None  # cannot happen
        row_lo_new = [L.index(lo_new)] if lo_new is not None else []
        row_hi_new = [Hh.index(hi_new)] if hi_new is not None else []
        y0 = y; cy = y0 + 60
        h_row = 130
        s.rect(40, y0 + 8, 64, 50, 'norm', 4, 1, fill='#FFFFFF')
        s.text(72, y0 + 25, 'num', 12, 'middle', SUB); s.text(72, y0 + 42, str(num), 16, 'middle', INK)
        if L:
            s.tree([(str(v),) for v in L], 190, cy, new=row_lo_new, dxs=(0, 30, 20, 14))
        s.path('M104 %d L%d %d' % (y0 + 33, 190 - 24, cy) if False else 'M104 %d L%d %d L%d %d' % (y0 + 33, 190, y0 + 33, 190, cy - 24), EDGE, 1.5)
        if Hh:
            s.tree([(str(v),) for v in Hh], 330, cy, new=row_hi_new, dxs=(0, 30, 20, 14))
        else:
            s.text(330, cy, '空', 14, 'middle', SUB)
        lines = []
        if m == num:
            lines.append('push %d → lo, lo 最大的 %d → hi' % (num, m))
        else:
            lines.append('push %d → lo, lo 最大的 %d → hi' % (num, m))
        if back is not None:
            lines.append('len(hi) > len(lo) → hi 最小的 %d → lo' % back)
        else:
            lines.append('len(hi) ≤ len(lo), 不用再移')
        if len(L) > len(Hh):
            lines.append('median = lo.top = %d' % med)
        else:
            lines.append('median = (%d + %d) / 2 = %s' % (L[0], Hh[0], ('%g' % med)))
        s.text(400, y0 + 28, lines[0], 12, 'start', INK)
        s.text(400, y0 + 48, lines[1], 12, 'start', INK)
        s.text(400, y0 + 78, lines[2], 14, 'start', INK, bold=True)
        y = y0 + h_row; s.sep(y)
    meds = None
    H = footer(s, y, ['median 依次 = 5, 3.5, 5, 4, 5, 4   (每步 O(log n), 不用排序)'],
               [('new', '这一步移进来的', 120), ('ring', 'heap top', 80), ('norm', 'heap 里其他的', 120)])
    save(s, H, 'median_stream_trace.svg')

# ---------------------------------------------------------------- Task Scheduler
def task_trace():
    s = S('ts', 'Task Scheduler: heap + cooldown queue trace', 'tasks=AAABBC, n=2')
    y = header(s, 'tasks = A,A,A,B,B,C · n = 2 · max-heap 存 (剩余次数, 任务) · 每个 slot 执行 1 次 (pop)',
               '执行完还有剩 → 进 cooldown, 过 n 个 slot 才能回 heap · heap 空但 cooldown 非空 → idle',
               [(40, 'slot'), (160, 'slot 开始'), (290, '执行 + 回来后'), (440, 'cooldown 队列')])
    heap = [(-c, t) for t, c in Counter('AAABBC').items()]; heapq.heapify(heap)
    cd = deque(); time = 0; n = 2; rows = []
    lab = lambda t: (str(-t[0]), t[1])
    while heap or cd:
        time += 1; pre = list(heap); pp = None; ret = None
        if heap:
            c, t = heapq.heappop(heap); pp = (c, t); c += 1
            if c: cd.append((time + n, c, t))
        if cd and cd[0][0] == time:
            r = cd.popleft(); ret = r; heapq.heappush(heap, (r[1], r[2]))
        row = dict(box=['slot %d' % time])
        if pre:
            row['items1'] = [lab(t) for t in pre]
        else:
            row['empty1'] = 'heap 空 → idle'
        if pp:
            new_c = -(pp[0] + 1)
            if new_c:
                why = '执行 %s: 剩 %d → %d' % (pp[1], -pp[0], new_c)
                why2 = '进 cooldown, slot %d 后回来' % (time + n)
            else:
                why = '执行 %s: 剩 %d → 0' % (pp[1], -pp[0]); why2 = '做完了, 不进 cooldown'
            row['popped'] = dict(node=lab(pp), lines=[why, why2])
        else:
            row['noop'] = None
        row['items2'] = [lab(t) for t in heap]
        if not heap: row['empty2'] = '空'
        if ret: row['new2'] = [heap.index((ret[1], ret[2]))]
        q = ', '.join('%s×%d @%d' % (t, c, rt) for rt, c, t in [(a, -b, cc) for a, b, cc in cd]) if False else ', '.join('%s×%d (slot %d 后)' % (t, -c, rt) for rt, c, t in cd)
        lines = ['cooldown: ' + ('空' if not cd else '')]
        for rt, c, t in cd: lines.append('%s 剩 %d, slot %d 后回来' % (t, -c, rt))
        if ret: lines.append('回来: %s 剩 %d → push 进 heap' % (ret[2], -ret[1]))
        row['calc'] = lines[:4]
        rows.append(row)
    print(time)
    y = trace_rows(s, y, rows)
    H = footer(s, y, ['总时间 = 7 slots (A B C A B idle A, 中间有 1 个 idle)'],
               [('new', '从 cooldown 回来的', 160), ('pop', '本 slot 执行的', 110), ('ring', 'heap top (剩余最多)', 150), ('norm', 'heap 里其他的', 120)])
    save(s, H, 'task_scheduler_trace.svg')

if __name__ == '__main__':
    kth_trace(); topk_trace(); closest_trace(); merge_trace(); hire_trace(); median_trace(); task_trace()
