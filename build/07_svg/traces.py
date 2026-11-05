import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svglib import *

OUT = "/home/user/coding-interview-notes/docs/svg/07-monotonic-stack/"
LEG = [("new", "当前输入 / 待 push"), ("old", "pop (虚线扔到左边)"), ("oth", "栈里其他"), ("ring", "栈顶")]


def write(fn, s):
    open(OUT + fn, "w", encoding="utf-8").write(s)


# ------------------------------------------------------------ Daily Temperatures
def dt_rows(T):
    ans = [0] * len(T)
    stack = []
    rows = []
    for i, t in enumerate(T):
        pre = ["%d·%d" % (j, T[j]) for j in stack]
        pops = []
        while stack and T[stack[-1]] < t:
            slot = len(stack) - 1
            j = stack.pop()
            ans[j] = i - j
            pops.append((slot, "%d·%d" % (j, T[j]), "%d > %d, pop" % (t, T[j]),
                         ["ans[%d] = %d − %d = %d" % (j, i, j, i - j)]))
        keep = [(s, "%d·%d" % (j, T[j])) for s, j in enumerate(stack)]
        stack.append(i)
        post = ["%d·%d" % (j, T[j]) for j in stack]
        nopop = None
        if not pops:
            if len(stack) > 1:
                nopop = "%d > %d, 不 pop" % (T[stack[-2]], t)
            else:
                nopop = "栈空, 不 pop"
        rows.append(dict(wait="%d·%d" % (i, t), inp=["i = %d" % i, "T = %d" % t], pre=pre, pops=pops, keep=keep,
                         push="%d·%d" % (i, t), post=post, nopop=nopop, calc=[]))
        print("DT i=%d t=%d pre=%s pops=%s post=%s ans=%s" % (i, t, pre, [p[1] for p in pops], post, ans))
    return rows, ans, stack


def dt_svg():
    T = [73, 74, 75, 71, 69, 72, 76, 73]
    rows, ans, stack = dt_rows(T)
    assert ans == [1, 1, 4, 2, 1, 1, 0, 0]
    for r in rows:
        if not r["pops"] and not r["calc"]:
            r["calc"] = [("(还没有答案)", False)]
    footer = [("栈里剩 6·76, 7·73: 右边没有更高温 → ans[6] = 0, ans[7] = 0", False),
              ("ans = [1, 1, 4, 2, 1, 1, 0, 0]", True)]
    s = trace_svg("dttrace", "Daily Temperatures trace",
                  "T = [73,74,75,71,69,72,76,73]: for each day pop colder days off a decreasing stack and settle ans.",
                  ["T = [73, 74, 75, 71, 69, 72, 76, 73] · 栈里存 i·T (index·温度), 从底到顶温度递减",
                   "每一步: 当前 T 和栈顶比 → 栈顶更冷就 pop 并结算 ans = i − j → 最后把 i push 进去"],
                  ["当前输入", "pop (扔到左边)", "pop 后", "push 后", "计算"],
                  rows, footer, LEG)
    write("daily_temperatures_trace.svg", s)


# ------------------------------------------------------------ NGE II
def nge_rows(nums):
    n = len(nums)
    ans = [-1] * n
    stack = []
    rows = []
    for i in range(2 * n):
        x = nums[i % n]
        pre = ["%d·%d" % (j, nums[j]) for j in stack]
        pops = []
        while stack and nums[stack[-1]] < x:
            slot = len(stack) - 1
            j = stack.pop()
            ans[j] = x
            pops.append((slot, "%d·%d" % (j, nums[j]), "%d > %d, pop" % (x, nums[j]),
                         ["ans[%d] = %d" % (j, x)]))
        keep = [(s, "%d·%d" % (j, nums[j])) for s, j in enumerate(stack)]
        pushed = None
        if i < n:
            stack.append(i)
            pushed = "%d·%d" % (i, x)
        post = ["%d·%d" % (j, nums[j]) for j in stack]
        nopop = None
        if not pops:
            if not keep:
                nopop = "栈空, 不 pop"
            else:
                top = keep[-1][1]
                nopop = "栈顶 %s ≥ %d, 不 pop" % (top.split("·")[1], x)
        calc = []
        if i >= n and not pops:
            calc.append(("第 2 圈, 不 push", False))
        if i >= n and pops:
            for k_ in range(len(pops)):
                p_ = pops[k_]
                pops[k_] = (p_[0], p_[1], p_[2], ["第 2 圈, 不 push", p_[3][0]])
        rows.append(dict(wait="%d·%d" % (i % n, x), inp=["i = %d" % i, "x = %d" % x] if i < n else
                         ["i = %d → %d" % (i, i % n), "x = %d" % x],
                         pre=pre, pops=pops, keep=keep, push=pushed, post=post, nopop=nopop, calc=calc))
        print("NGE i=%d x=%d pre=%s pops=%s post=%s ans=%s" % (i, x, pre, [p[1] for p in pops], post, ans))
    return rows, ans, stack


def nge_svg():
    nums = [2, 3, 1]
    rows, ans, stack = nge_rows(nums)
    assert ans == [3, -1, 2]
    s = trace_svg("ngetrace", "Next Greater Element II trace",
                  "nums=[2,3,1] circular: 2n iterations, only push in the first pass.",
                  ["nums = [2, 3, 1] (循环) · 走 i = 0..5 (共 2n = 6 步), x = nums[i % n]",
                   "栈里存 idx·值, 从底到顶递减 · 只在第 1 圈 (i < n) push, 第 2 圈只负责结算"],
                  ["当前输入", "pop (扔到左边)", "pop 后", "push 后", "计算"],
                  rows, [("栈里剩 1·3 (值 3): 绕一圈也没有更大的 → ans[1] = −1", False),
                         ("ans = [3, −1, 2]  (ans[2] = 2: 1 绕回第 2 圈才遇到 2)", True)], LEG, inp_w=72)
    write("next_greater_ii_trace.svg", s)


# ------------------------------------------------------------ Largest Rectangle
def lrh_rows(heights):
    H = heights + [0]
    stack = []
    best = 0
    rows = []
    for i, h in enumerate(H):
        pre = ["%d·%d" % (j, H[j]) for j in stack]
        pops = []
        while stack and H[stack[-1]] > h:
            slot = len(stack) - 1
            j = stack.pop()
            hh = H[j]
            left = stack[-1] if stack else -1
            w = i - left - 1
            area = hh * w
            best = max(best, area)
            pops.append((slot, "%d·%d" % (j, hh), "%d > %d, pop" % (hh, h),
                         ["w = %d − %s − 1 = %d" % (i, ("(−1)" if left < 0 else left), w), "%d × %d = %d" % (hh, w, area)]))
        keep = [(s, "%d·%d" % (j, H[j])) for s, j in enumerate(stack)]
        stack.append(i)
        post = ["%d·%d" % (j, H[j]) for j in stack]
        nopop = None
        calc = []
        if not pops:
            nopop = ("栈空, 不 pop" if not keep else "栈顶 %s ≤ %d, 不 pop" % (keep[-1][1].split("·")[1], h))
        rows.append(dict(wait="%d·%d" % (i, h), inp=["i = %d" % i, "h = %d%s" % (h, " 哨兵" if i == len(H) - 1 else "")],
                         pre=pre, pops=pops, keep=keep, push="%d·%d" % (i, h), post=post, nopop=nopop, calc=calc))
        print("LRH i=%d h=%d pre=%s pops=%s post=%s best=%d" % (i, h, pre, [(p[1], p[3]) for p in pops], post, best))
    return rows, best


def lrh_svg():
    heights = [2, 1, 5, 6, 2, 3]
    rows, best = lrh_rows(heights)
    assert best == 10
    s = trace_svg("lrhtrace", "Largest Rectangle in Histogram trace",
                  "heights=[2,1,5,6,2,3]+[0]: increasing stack, popped bar's width is fixed at pop time.",
                  ["heights = [2, 1, 5, 6, 2, 3] + [0 哨兵] · 栈里存 i·h, 从底到顶 h 递增",
                   "pop 的那一刻: 高 = 被 pop 的 h · 右边界 = i · 左边界 = pop 后的新栈顶 (空则 −1) · w = i − 左 − 1"],
                  ["当前输入", "pop (扔到左边)", "pop 后", "push 后", "面积"],
                  rows, [("pop 过的面积: 2, 6, 10, 3, 8, 6 → best = max = 10 (高 5 × 宽 2, i = 2..3)", True)],
                  LEG, slot=40)
    write("largest_rectangle_trace.svg", s)


# ------------------------------------------------------------ Remove K Digits
def rkd_rows(num, k):
    stack = []
    rows = []
    k0 = k
    for i, d in enumerate(num):
        pre = list(stack)
        pops = []
        kin = k
        while k and stack and stack[-1] > d:
            slot = len(stack) - 1
            c = stack.pop()
            k -= 1
            pops.append((slot, c, "%s > %s 且 k = %d > 0" % (c, d, k + 1), ["删掉 %s, k: %d → %d" % (c, k + 1, k)]))
        keep = [(s, c) for s, c in enumerate(stack)]
        stack.append(d)
        post = list(stack)
        nopop = None
        if not pops:
            if not keep:
                nopop = "栈空, 不 pop"
            elif k == 0:
                nopop = "k = 0, 不能再删"
            else:
                nopop = "%s ≤ %s, 不 pop" % (keep[-1][1], d)
        rows.append(dict(wait=d, inp=["d = %s" % d, "k = %d" % kin], pre=pre, pops=pops, keep=keep, push=d,
                         post=post, nopop=nopop, calc=[]))
        print("RKD d=%s kin=%d pre=%s pops=%s post=%s k=%d" % (d, kin, pre, [p[1] for p in pops], post, k))
    return rows, "".join(stack), k


def rkd_svg():
    rows, res, k = rkd_rows("1432219", 3)
    assert res == "1219" and k == 0
    for r in rows:
        if not r["pops"]:
            r["calc"] = []
    s = trace_svg("rkdtrace", "Remove K Digits trace",
                  "num='1432219', k=3: increasing stack of digits, pop a bigger previous digit while k>0.",
                  ["num = \"1432219\", k = 3 · 栈里存数字, 从底到顶非递减 (高位尽量小)",
                   "每一步: 前一位 (栈顶) > 当前位 d 且 k > 0 → pop 栈顶 (删掉它, k 减 1) → 把 d push 进去"],
                  ["当前输入", "pop (扔到左边)", "pop 后", "push 后", "计算"],
                  rows, [("k 用完 (k = 0), 栈 = [1, 2, 1, 9] → 结果 \"1219\"", True)], LEG)
    write("remove_k_digits_trace.svg", s)


# ------------------------------------------------------------ Sliding Window Max
def swm_rows(nums, k):
    from collections import deque
    dq = deque()
    ans = []
    rows = []
    for i, x in enumerate(nums):
        pre = ["%d·%d" % (j, nums[j]) for j in dq]
        slots_alive = list(range(len(dq)))
        pops = []
        removed = set()
        if dq and dq[0] <= i - k:
            j = dq.popleft()
            removed.add(0)
            pops.append((0, "%d·%d" % (j, nums[j]), "%d ≤ %d − %d = %d, 过期" % (j, i, k, i - k), []))
        orig = list(pre)
        # tail pops: slot is original index in pre
        while dq and nums[dq[-1]] <= x:
            j = dq.pop()
            slot = len(dq) + (1 if 0 in removed else 0)
            pops.append((slot, "%d·%d" % (j, nums[j]), "%d ≤ %d, pop 队尾" % (nums[j], x), []))
        keep = [(s + (1 if 0 in removed else 0), "%d·%d" % (j, nums[j])) for s, j in enumerate(dq)]
        dq.append(i)
        post = ["%d·%d" % (j, nums[j]) for j in dq]
        calc = []
        if i >= k - 1:
            ans.append(nums[dq[0]])
            window = nums[i - k + 1:i + 1]
            calc = [("窗口 [%d..%d] = %s" % (i - k + 1, i, ", ".join(map(str, window))), False),
                    ("max = nums[队头] = %d" % nums[dq[0]], True)]
        else:
            calc = [("窗口还没满 (i < k − 1)", False)]
        nopop = None if pops else "队头没过期, 队尾更大"
        if not pops:
            nopop = "队头未过期, 队尾 > %d" % x if keep else "队列空"
        rows.append(dict(wait="%d·%d" % (i, x), inp=["i = %d" % i, "x = %d" % x], pre=pre, pops=pops, keep=keep,
                         push="%d·%d" % (i, x), post=post, nopop=nopop, calc=calc))
        print("SWM i=%d x=%d pre=%s pops=%s post=%s ans=%s" % (i, x, pre, [p[1] for p in pops], post, ans))
    return rows, ans


def swm_svg():
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    rows, ans = swm_rows(nums, 3)
    assert ans == [3, 3, 5, 5, 6, 7]
    # pops with no calc column: calc is per-row here (window), pops have empty calc
    s = trace_svg("swmtrace", "Sliding Window Maximum trace",
                  "nums=[1,3,-1,-3,5,3,6,7], k=3: monotonic deque, head expires, tail smaller than x dropped.",
                  ["nums = [1, 3, −1, −3, 5, 3, 6, 7], k = 3 · deque 存 idx·值, 底 = 队头 (最大), 顶 = 队尾",
                   "每一步: ① 队头过期就出队 ② 队尾 ≤ x 就出队 ③ push x ④ 窗口满了就输出 nums[队头]"],
                  ["当前输入", "出队 (扔到左边)", "出队后", "push 后", "窗口 / 答案"],
                  rows, [("ans = [3, 3, 5, 5, 6, 7]  (i = 2..7 各输出一个, 共 n − k + 1 = 6 个)", True)],
                  [("new", "当前输入 / 待 push"), ("old", "出队 (扔到左边)"), ("oth", "deque 里其他"), ("ring", "队头 = 窗口最大")],
                  ring_head=True)
    write("sliding_window_max_trace.svg", s)


if __name__ == "__main__":
    dt_svg(); nge_svg(); lrh_svg(); rkd_svg(); swm_svg()
