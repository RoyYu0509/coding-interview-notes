import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svglib import *
from traces import write

WHITE = ("#FFFFFF", "#B4B2A9", "#52514E")


def mk(name, title, desc, H, body):
    return svg_doc(name, title, desc, H, body)


def mk_arrow_defs():
    pass


def bucket_with(x, bottom, w, cells, slot=28, n_slots=None, ring_top=True, roles=None):
    n = n_slots or len(cells)
    top = bottom - n * slot - 4
    out = [bucket(x, top, bottom, w)]
    for s, lab in enumerate(cells):
        role = (roles[s] if roles else OTH)
        out.append(cell(x + 6, bottom - slot * s - slot / 2 - 2 - 12, w - 12, 24, role, lab,
                        ringed=(ring_top and s == len(cells) - 1)))
    return "".join(out), top


# ---------------------------------------------------------------- core 0
def core0():
    nm = "c0"
    b = []
    b.append(text(40, 18, "nums = [9, 8, 7, 6, 5, 10] · 每个数找 \"右边第一个更大的数\"", 12))
    b.append(text(40, 38, "同一个例子: 左边暴力每个 i 重新往右扫, 右边 stack 每个数只进出一次", 12))
    # left panel
    b.append(text(40, 70, "暴力: 每个 i 从 i+1 重新往右扫", 14, INK, 500))
    xs = [40 + 40 * k for k in range(6)]
    vals = [9, 8, 7, 6, 5, 10]
    for k, v in enumerate(vals):
        b.append(text(xs[k] + 17, 92, "i=%d" % k, 12, SUB, 400, "middle"))
        b.append(cell(xs[k], 102, 34, 30, NEW if k == 5 else OTH, str(v)))
    total = 0
    for k in range(5):
        y = 156 + 26 * k
        cnt = 5 - k
        total += cnt
        b.append('<circle cx="%s" cy="%s" r="3" fill="%s"/>' % (xs[k] + 17, y, SUB))
        b.append(arrow(xs[k] + 17, y, xs[5] + 15, y, SUB, None, 1.5, nm))
        b.append(text(xs[5] + 24, y, "i=%d 比较 %d 次" % (k, cnt), 12, SUB))
    assert total == 15
    b.append(text(40, 296, "比较次数 = 5 + 4 + 3 + 2 + 1 = 15 ≈ n²/2", 14, INK, 500))
    b.append(text(40, 318, "8, 7, 6, 5 被反复扫: 它们其实都在等同一个 10", 12, SUB))
    # divider
    b.append(line(352, 60, 352, 330, SEP, "4 4"))
    # right panel
    b.append(text(372, 70, "stack: 每个数只进出一次", 14, INK, 500))
    bx, bottom, w = 470, 316, 70
    n = 5
    top = bottom - n * 28 - 4
    b.append(bucket(bx, top, bottom, w))
    b.append(cell(bx + 6, bottom - 14 - 2 - 12, w - 12, 24, NEW, "10", ringed=True))
    b.append(text(bx + w / 2, top - 22, "10 到来 (i = 5)", 12, SUB, 400, "middle"))
    for s in range(1, 5):
        val = [9, 8, 7, 6, 5][s]  # slot s holds vals[s] (slot 0 is 9)
    popped = [9, 8, 7, 6, 5]
    for s in range(5):
        yy = bottom - 28 * s - 14 - 2
        v = popped[s]
        if s == 0:
            # slot 0 is occupied by the new 10 after push, the popped 9 sits beside
            pass
        b.append(cell(374, yy - 12, 48, 24, OLD, str(v)))
        b.append(arrow(bx + 2, yy, 428, yy, ARROW, "5 3", 1.5, nm))
        b.append(text(bx + w + 10, yy, "10 > %d, pop" % v, 12, OLD[2]))
    b.append(text(372, 332, "push 6 次 + pop 5 次 = 11 次 ≈ 2n", 14, INK, 500))
    # bottom explanation
    y0 = 364
    b.append(line(40, y0 - 14, 640, y0 - 14))
    b.append(text(40, y0, "为什么 pop 掉的数以后再也用不到:", 14, INK, 500))
    b.append(text(40, y0 + 24, "① 栈从底到顶递减: 还在栈里等答案的数都 ≥ 被 pop 的数, 它们不会拿它当答案", 12, SUB))
    b.append(text(40, y0 + 44, "② 它右边的新数只往右找答案, 被 pop 的数在它们左边, 根本看不到", 12, SUB))
    b.append(text(40, y0 + 68, "→ 每个数 push 1 次、最多 pop 1 次 → 总共 ≤ 2n 次操作 = O(n)", 14, INK, 500))
    b.append(legend(y0 + 100, [("new", "新 push / 当前输入"), ("old", "pop (虚线扔到左边)"), ("oth", "数组 / 栈里其他"), ("ring", "栈顶")]))
    write("first_principles_core.svg", mk(nm, "Brute force vs monotonic stack",
          "Left: brute force rescans to the right O(n^2); right: stack pops every element at most once.", y0 + 126, b))


# ---------------------------------------------------------------- core DT
def core_dt():
    nm = "c1"
    T = [73, 74, 75, 71, 69, 72, 76, 73]
    b = []
    b.append(text(40, 18, "T = [73, 74, 75, 71, 69, 72, 76, 73] · 走到 i = 5 (T = 72) 这一刻", 12))
    b.append(text(40, 38, "invariant: 栈里 = 还没等到更高温的那些天 · 从底到顶温度递减", 12))
    xs = [40 + 52 * k for k in range(8)]
    for k, v in enumerate(T):
        role = WHITE
        sub = None
        if k in (0, 1):
            role = WHITE
        if k in (2, 3, 4):
            role = OTH
        if k == 5:
            role = NEW
        b.append(text(xs[k] + 22, 66, "i=%d" % k, 12, SUB, 400, "middle"))
        b.append(cell(xs[k], 78, 44, 30, role, str(v), dash="3 2" if k in (6, 7) else None, ringed=(k == 5)))
    b.append(text(xs[0], 128, "已结算", 12, SUB))
    b.append(text(xs[2], 128, "在栈里 (还在等)", 12, SUB))
    b.append(text(xs[5] - 4, 128, "当前", 12, SUB))
    b.append(text(xs[6], 128, "还没看到", 12, SUB))
    b.append(line(40, 146, 640, 146))
    # bucket
    cells = ["2·75", "3·71", "4·69"]
    bx, bottom, w = 70, 330, 84
    top = bottom - 3 * 28 - 4
    bk, top = bucket_with(bx, bottom, w, cells, 28, 4)
    b.append(bk)
    b.append(text(bx + w / 2, bottom + 14, "底", 12, SUB, 400, "middle"))
    b.append(text(bx + w / 2, 164, "栈 (T 递减: 75 ≥ 71 ≥ 69)", 12, SUB, 400, "middle"))
    b.append(cell(bx + 6, top - 30, w - 12, 24, NEW, "5·72"))   # incoming element waiting above the stack
    # right: while loop
    x = 230
    b.append(text(x, 176, "T = 72 来了: while T[栈顶] < 72", 14, INK, 500))
    lines = [("69 < 72 → pop 4·69, 它等到了: ans[4] = 5 − 4 = 1", OLD[2]),
             ("71 < 72 → pop 3·71, 它等到了: ans[3] = 5 − 3 = 2", OLD[2]),
             ("75 ≥ 72 → 停. 75 还在等更高温", SUB)]
    for k, (s, col) in enumerate(lines):
        b.append(text(x, 206 + 24 * k, s, 12, col))
    b.append(text(x, 288, "然后 push 5·72 → 栈 = [2·75, 5·72], 仍然递减", 12, SUB))
    b.append(text(x, 312, "为什么停在 75: 栈递减, 75 往下全是 ≥ 75 > 72, 不用再看", 12, SUB))
    b.append(text(x, 336, "pop 的那一刻就是答案出现的那一刻 → 在 pop 里结算 ans", 14, INK, 500))
    b.append(legend(372, [("new", "当前输入"), ("oth", "栈里其他"), ("ring", "栈顶 / 当前")]))
    write("daily_temperatures_core.svg", mk(nm, "Daily Temperatures invariant",
          "Stack holds days still waiting for a warmer day, temperatures decreasing; pop settles the answer.", 396, b))


# ---------------------------------------------------------------- core NGE II
def core_nge():
    nm = "c2"
    b = []
    b.append(text(40, 18, "nums = [2, 3, 1] · 循环数组: 最后一个元素的 \"右边\" 要绕回开头", 12))
    b.append(text(40, 38, "把数组虚拟地拼成两份, 取值用 nums[i % n], 不真的拷贝", 12))
    vals = [2, 3, 1, 2, 3, 1]
    xs = [60 + 90 * k for k in range(6)]
    for k, v in enumerate(vals):
        real = k < 3
        b.append(text(xs[k] + 28, 70, "i=%d" % k, 12, SUB, 400, "middle"))
        b.append(cell(xs[k], 84, 56, 34, OTH if real else WHITE, str(v), dash=None if real else "3 2"))
        b.append(text(xs[k] + 28, 134, "idx %d" % (k % 3), 12, SUB, 400, "middle"))
    b.append(text(xs[0], 160, "第 1 圈: 真实数组, 要 push", 12, SUB))
    b.append(text(xs[3], 160, "第 2 圈: 虚拟拷贝, 不 push", 12, SUB))
    b.append(line(xs[3] - 17, 62, xs[3] - 17, 170, SEP, "4 4"))
    # arcs below
    # ans[2]: from i=2 (value 1) to i=3 (value 2)
    cx2, cx3 = xs[2] + 28, xs[3] + 28
    b.append(path("M%s 176 C%s 216 %s 216 %s 178" % (cx2, cx2, cx3, cx3), NEW[1], None, 2, True, nm).replace("arrR", "arrG"))
    b.append(text((cx2 + cx3) / 2, 222, "idx 2 (值 1): 第 1 圈右边没有更大的, 绕回去遇到 2", 12, NEW[2], 500, "middle"))
    b.append(text((cx2 + cx3) / 2, 240, "ans[2] = 2", 14, NEW[2], 500, "middle"))
    # idx1: 3 never finds bigger
    b.append(text(40, 282, "idx 1 (值 3): 第 2 圈遇到 3 (不 > 3), 绕一圈也没有更大的 → ans[1] = −1", 12, OLD[2]))
    b.append(line(40, 302, 640, 302))
    b.append(text(40, 326, "做法: 还是同一个递减栈, i 从 0 走到 2n − 1, x = nums[i % n]", 12, SUB))
    b.append(text(40, 346, "只在 i < n 时 push: 第 2 圈只是给栈里还没答案的元素 \"再找一次\"", 12, SUB))
    b.append(text(40, 370, "2n 次循环, 每个元素最多 push 1 次 / pop 1 次 → 仍是 O(n)", 14, INK, 500))
    b.append(legend(404, [("oth", "第 1 圈 (真实)"), ("new", "答案")]))
    write("next_greater_ii_core.svg", mk(nm, "Circular array doubled",
          "Walk 2n indices with i % n; wrap-around gives elements at the end a second chance.", 430, b))


# ---------------------------------------------------------------- core LRH
def core_lrh():
    nm = "c3"
    h = [2, 1, 5, 6, 2, 3]
    u = 20
    base = 250
    px = 62
    bw = 56
    b = []
    b.append(text(40, 18, "heights = [2, 1, 5, 6, 2, 3] · 以每根柱子为 \"最矮的那根\" 能向左右延伸多远?", 12))
    b.append(text(40, 38, "看高 = 5 的柱子 (idx 2): 它是 i = 4 时被 pop 的", 12))
    xs = [40 + px * k for k in range(6)]
    # extended rectangle (idx2..3, height 5)
    rx = xs[2]
    rw = xs[3] + bw - xs[2]
    for k, v in enumerate(h):
        role = OTH
        b.append(rect(xs[k], base - v * u, bw, v * u, role, 2))
        b.append(text(xs[k] + bw / 2, base - v * u - 12, str(v), 14, INK, 500, "middle"))
        b.append(text(xs[k] + bw / 2, base + 16, "i=%d" % k, 12, SUB, 400, "middle"))
    b.append(rect(xs[2], base - 5 * u, bw, 5 * u, NEW, 2))
    b.append('<rect x="%s" y="%s" width="%s" height="%s" rx="2" fill="none" stroke="%s" stroke-width="1.5" stroke-dasharray="5 3"/>' % (rx, base - 5 * u, rw, 5 * u, NEW[1]))
    b.append(ring(xs[1], base - 1 * u, bw, 1 * u, 4))
    b.append(ring(xs[4], base - 2 * u, bw, 2 * u, 4))
    b.append(text(xs[1] + bw / 2, base + 36, "左边界", 12, SUB, 400, "middle"))
    b.append(text(xs[4] + bw / 2, base + 36, "右边界", 12, SUB, 400, "middle"))
    b.append(text(xs[2] + 4, base - 5 * u + 18, "5 × 2", 14, NEW[2], 500))
    # right text
    x = 450
    b.append(text(x, 80, "以高 5 为最矮:", 14, INK, 500))
    b.append(text(x, 108, "往左: 第一根比 5 矮的", 12, SUB))
    b.append(text(x, 126, "  = idx 1 (h = 1) → 左边界", 12, SUB))
    b.append(text(x, 154, "往右: 第一根比 5 矮的", 12, SUB))
    b.append(text(x, 172, "  = idx 4 (h = 2) → 右边界", 12, SUB))
    b.append(text(x, 200, "宽 = 右 − 左 − 1", 12, SUB))
    b.append(text(x, 218, "   = 4 − 1 − 1 = 2", 14, INK, 500))
    b.append(text(x, 244, "面积 = 5 × 2 = 10", 14, INK, 500))
    y0 = 322
    b.append(line(40, y0 - 14, 640, y0 - 14))
    b.append(text(40, y0, "栈里从底到顶 h 递增 → 栈里每根柱子下面那根, 就是它左边第一根更矮的", 12, SUB))
    b.append(text(40, y0 + 20, "pop 时: 右边界 = 当前 i (它是第一个更矮的, 才触发 pop) · 左边界 = pop 之后的新栈顶", 12, SUB))
    b.append(text(40, y0 + 40, "两个边界在同一时刻确定 → 一次 pop 算出一根柱子的最大面积", 14, INK, 500))
    b.append(text(40, y0 + 64, "哨兵: 在 heights 末尾补一根 0, 最后一步把栈里剩下的柱子全部 pop 出来结算", 12, SUB))
    b.append(legend(y0 + 96, [("new", "被结算的柱子及其矩形"), ("oth", "其他柱子"), ("ring", "左 / 右边界")]))
    write("largest_rectangle_core.svg", mk(nm, "Largest rectangle boundaries",
          "Bar 5 extends from the first smaller bar on the left to the first smaller bar on the right; both known at pop time.", y0 + 122, b))


# ---------------------------------------------------------------- core RKD
def core_rkd():
    nm = "c4"
    b = []
    b.append(text(40, 18, "num = \"1432\", 删 1 位 · 4 种删法, 哪个最小?", 12))
    b.append(text(40, 38, "位数相同 → 先比最高位, 高位越小越好", 12))
    digs = "1432"
    cand = []
    for r in range(4):
        y = 66 + 44 * r
        res = digs[:r] + digs[r + 1:]
        cand.append(res)
        b.append(text(40, y + 15, "删 idx %d" % r, 14, INK, 500))
        for k, d in enumerate(digs):
            role = OLD if k == r else OTH
            b.append(cell(140 + 40 * k, y, 34, 30, role, d, dash="3 2" if k == r else None))
        b.append(arrow(310, y + 15, 350, y + 15, SUB, None, 1.5, nm))
        b.append(cell(360, y, 64, 30, NEW if res == min(["432", "132", "142", "143"]) else OTH, res,
                      ringed=(res == "132")))
    assert cand == ["432", "132", "142", "143"] and min(cand) == "132"
    b.append(text(440, 66 + 44 + 15, "← 最小: 删掉 4", 14, NEW[2], 500))
    y0 = 262
    b.append(line(40, y0 - 14, 640, y0 - 14))
    b.append(text(40, y0, "删 4: 第 2 位从 4 变成 3, 变小了; 删 3: 第 2 位还是 4, 没变小", 12, SUB))
    b.append(text(40, y0 + 22, "从左往右第一个 \"比后一位大\" 的数字 (4 > 3) 删掉最划算", 12, SUB))
    b.append(text(40, y0 + 44, "= 栈顶 > 当前数字时 pop 栈顶 (k 次这样的操作, 一次扫描完成)", 14, INK, 500))
    b.append(text(40, y0 + 68, "栈从底到顶非递减 = 高位尽量小 · 如果整个数字都是递增的, 就删最末尾的 k 位", 12, SUB))
    b.append(legend(y0 + 100, [("oth", "保留的数字"), ("old", "删掉的数字"), ("new", "结果最小"), ("ring", "答案")]))
    write("remove_k_digits_core.svg", mk(nm, "Why delete the first bigger digit",
          "Deleting the first digit that is larger than its successor gives the smallest number.", y0 + 126, b))


# ---------------------------------------------------------------- core SWM
def core_swm():
    nm = "c5"
    b = []
    b.append(text(40, 18, "nums = [1, 3, −1, −3, 5, 3, 6, 7], k = 3 · 看 i = 4 (x = 5) 到来的这一刻", 12))
    b.append(text(40, 38, "idx j 在窗口里的时间 = i ∈ [j, j + 2] (窗口 [i − 2, i] 里有 j)", 12))
    col0, pitch = 150, 70
    def cx(i):
        return col0 + pitch * (i - 1)
    for i in range(1, 8):
        b.append(text(cx(i) + 30, 66, "i = %d" % i, 12, SUB, 400, "middle"))
    rows = [(1, 3), (2, -1), (3, -3), (4, 5)]
    for r, (j, v) in enumerate(rows):
        y = 84 + 38 * r
        b.append(text(40, y + 12, "idx %d · 值 %s" % (j, str(v).replace("-", "−")), 14, INK, 500))
        for i in range(j, j + 3):
            if j == 4:
                role = NEW
            elif i >= 4 and j in (2, 3):
                role = OLD
            else:
                role = OTH
            b.append(rect(cx(i), y, 60, 24, role, 3))
        # annotations right of the bar
    # vertical line at i = 4
    b.append(line(cx(4) - 5, 76, cx(4) - 5, 240, ARROW, "5 3", 1.5))
    b.append(text(cx(4) - 5, 252, "i = 4: 5 进来", 12, OLD[2], 500, "middle"))
    b.append(text(cx(4) + 2, 96, "idx 1 已滑出窗口 [2, 4] → 队头过期", 12, SUB))
    b.append(text(cx(6) + 4, 134, "← −1 < 5", 12, OLD[2]))
    b.append(text(cx(6) + 4, 172, "← −3 < 5", 12, OLD[2]))
    y0 = 284
    b.append(line(40, y0 - 14, 640, y0 - 14))
    b.append(text(40, y0, "红色段: −1、−3 比 5 小, 又比 5 先过期 → 它们还活着的每一刻 5 都在窗口里且更大", 12, SUB))
    b.append(text(40, y0 + 20, "→ 永远当不了最大 → 队尾比 x 小的直接丢 (从尾部 pop)", 14, INK, 500))
    b.append(text(40, y0 + 46, "留下的 deque 从头到尾递减 → 队头 = 窗口最大 → 取最大 O(1)", 12, SUB))
    b.append(text(40, y0 + 66, "队头最老, 最先过期 → 过期的从头部 popleft · 每个元素最多进出一次 → O(n)", 12, SUB))
    b.append(legend(y0 + 100, [("oth", "还在窗口里"), ("old", "被 5 压住 (永远不是最大)"), ("new", "新来的最大")]))
    write("sliding_window_max_core.svg", mk(nm, "Why drop smaller tail elements",
          "Elements smaller than a newcomer and older than it can never be the window maximum again.", y0 + 126, b))


if __name__ == "__main__":
    core0(); core_dt(); core_nge(); core_lrh(); core_rkd(); core_swm()
