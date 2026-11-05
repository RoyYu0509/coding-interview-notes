"""16 · Greedy 文档生成。 运行: cd build && python3 -I 16_greedy.py"""
import os
import sys
import random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import doclib as d
import importlib.util

spec = importlib.util.spec_from_file_location("g16svg", os.path.join(HERE, "16_greedy_svg.py"))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

# ------------------------------------------------------------------ 展示的代码 (同时 exec 做对拍)
CODE_COIN = '''
def coin_change_dp(coins, amount):
    INF = float("inf")
    dp = [0] + [INF] * amount            # dp[a] = 凑出 a 的最少枚数
    for a in range(1, amount + 1):
        for c in coins:                  # 试每一种最后一枚, 而不是只赌最大的
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] < INF else -1
'''

CODE_JUMP = '''
def can_jump(nums):
    max_reach = 0                        # invariant: 0..max_reach 全部可达
    for i, step in enumerate(nums):
        if i > max_reach:                # 连 i 都够不到 -> 后面全都够不到
            return False
        max_reach = max(max_reach, i + step)   # 从 i 起跳最远到 i + step
    return True
'''

CODE_JUMP2 = '''
def jump(nums):
    jumps = 0
    cur_end = 0                          # 当前层 (跳 jumps 步能到的区间) 的右边界
    farthest = 0                         # 扫完当前层后, 下一层的右边界
    for i in range(len(nums) - 1):       # 最后一格不用再跳, 所以到 n-2
        farthest = max(farthest, i + nums[i])
        if i == cur_end:                 # 当前层扫完 -> 必须再跳一次
            jumps += 1
            cur_end = farthest           # 下一层边界 = 这一层能到的最远处
    return jumps                         # 题目保证一定能到终点
'''

CODE_GAS = '''
def can_complete_circuit(gas, cost):
    total = 0                            # 全局 sum(gas - cost), 决定有没有解
    tank = 0                             # 从 start 出发到现在的油量
    start = 0
    for i in range(len(gas)):
        net = gas[i] - cost[i]
        total += net
        tank += net
        if tank < 0:                     # start..i 任何起点都到不了 i+1
            start = i + 1                # 下一个候选: 失败点的下一站
            tank = 0
    return start if total >= 0 else -1   # total >= 0 保证最后留下的 start 可行
'''

CODE_STOCK = '''
def max_profit(prices):
    profit = 0
    for i in range(1, len(prices)):
        diff = prices[i] - prices[i - 1]
        if diff > 0:                     # 每一段上涨都吃掉; 下跌段 = 空仓
            profit += diff
    return profit
'''

CODE_CANDY = '''
def candy(ratings):
    n = len(ratings)
    left = [1] * n                       # left[i]: 只管左约束的最少糖
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            left[i] = left[i - 1] + 1
    right = [1] * n                      # right[i]: 只管右约束的最少糖
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            right[i] = right[i + 1] + 1
    return sum(max(l, r) for l, r in zip(left, right))   # 两条约束同时满足
'''

CODE_LARGEST = '''
from functools import cmp_to_key

def largest_number(nums):
    strs = [str(x) for x in nums]
    # a 排在 b 前面 <=> a+b > b+a (字符串拼接, 不是字典序)
    strs.sort(key=cmp_to_key(lambda a, b: -1 if a + b > b + a else 1))
    res = "".join(strs)
    return "0" if res[0] == "0" else res   # [0, 0] 这类全零要返回 "0"
'''

CODE_PART = '''
def partition_labels(s):
    last = {c: i for i, c in enumerate(s)}   # 每个字母最后一次出现的位置
    res = []
    start = end = 0
    for i, c in enumerate(s):
        end = max(end, last[c])          # 这段至少要延伸到 c 的最后一次出现
        if i == end:                     # 段内所有字母都已最后一次出现 -> 可以切
            res.append(i - start + 1)
            start = i + 1
    return res
'''

CODE_TEMPLATE = '''
def greedy(items):
    items.sort(key=...)                  # 1) 有些题需要先排序 (Largest Number / interval 按 end)
    state = 初始值                        # 2) 一个(或两个)汇总量: max_reach / tank / end ...
    for x in items:                      # 3) 一遍扫描, 每步只看 x 和 state, 不回头
        做局部最优的选择, 更新 state
    return 答案
'''

def tight(code):
    out, w = [], 0
    ls = code.split("\n")
    for l in ls:
        if "#" in l and not l.strip().startswith("#") and '"' not in l.split("#")[0]:
            w = max(w, len(l.split("#")[0].rstrip()))
    for l in ls:
        if "#" in l and not l.strip().startswith("#") and '"' not in l.split("#")[0]:
            a, b = l.split("#", 1)
            l = a.rstrip().ljust(w + 2) + "#" + b
        out.append(l)
    return "\n".join(out)


CODE_COIN, CODE_JUMP, CODE_JUMP2, CODE_GAS, CODE_STOCK, CODE_CANDY, CODE_LARGEST, CODE_PART, CODE_TEMPLATE = map(
    tight, (CODE_COIN, CODE_JUMP, CODE_JUMP2, CODE_GAS, CODE_STOCK, CODE_CANDY, CODE_LARGEST, CODE_PART, CODE_TEMPLATE))

ns = {}
for c in (CODE_COIN, CODE_JUMP, CODE_JUMP2, CODE_GAS, CODE_STOCK, CODE_CANDY, CODE_LARGEST, CODE_PART):
    exec(c, ns)


# ------------------------------------------------------------------ 对拍
def brute_can_jump(nums):
    n = len(nums)
    ok = [False] * n
    ok[-1] = True
    for i in range(n - 2, -1, -1):
        ok[i] = any(ok[j] for j in range(i + 1, min(n, i + nums[i] + 1)))
    return ok[0]


def brute_jump(nums):
    n = len(nums)
    INF = 10 ** 9
    dp = [INF] * n
    dp[-1] = 0
    for i in range(n - 2, -1, -1):
        for j in range(i + 1, min(n, i + nums[i] + 1)):
            dp[i] = min(dp[i], dp[j] + 1)
    return dp[0]


def brute_gas(gas, cost):
    n = len(gas)
    for s in range(n):
        t = 0
        ok = True
        for k in range(n):
            j = (s + k) % n
            t += gas[j] - cost[j]
            if t < 0:
                ok = False
                break
        if ok:
            return s
    return -1


def brute_stock(p):
    hold, free = -10 ** 9, 0
    for x in p:
        hold, free = max(hold, free - x), max(free, hold + x)
    return free


def brute_candy(r):
    n = len(r)
    c = [1] * n
    ch = True
    while ch:
        ch = False
        for i in range(n):
            if i > 0 and r[i] > r[i - 1] and c[i] <= c[i - 1]:
                c[i] = c[i - 1] + 1
                ch = True
            if i < n - 1 and r[i] > r[i + 1] and c[i] <= c[i + 1]:
                c[i] = c[i + 1] + 1
                ch = True
    return sum(c)


def brute_largest(nums):
    from itertools import permutations
    best = max("".join(map(str, p)) for p in permutations(nums))
    return "0" if best[0] == "0" else best


def brute_part(s):
    iv = {}
    for i, c in enumerate(s):
        a, b = iv.get(c, (i, i))
        iv[c] = (a, i)
    iv = sorted(iv.values())
    out, cs, ce = [], iv[0][0], iv[0][1]
    for a, b in iv[1:]:
        if a > ce:
            out.append(ce - cs + 1)
            cs, ce = a, b
        else:
            ce = max(ce, b)
    out.append(ce - cs + 1)
    return out


def coin_greedy(coins, amount):
    cnt = 0
    for c in sorted(coins, reverse=True):
        cnt += amount // c
        amount %= c
    return cnt if amount == 0 else -1


random.seed(7)
for _ in range(3000):
    n = random.randint(1, 8)
    nums = [random.randint(0, 4) for _ in range(n)]
    assert ns["can_jump"](nums) == brute_can_jump(nums), nums
    if brute_can_jump(nums):
        assert ns["jump"](nums) == brute_jump(nums), nums
    gas = [random.randint(0, 5) for _ in range(n)]
    cost = [random.randint(0, 5) for _ in range(n)]
    b = brute_gas(gas, cost)
    r = ns["can_complete_circuit"](gas, cost)
    assert (b == -1) == (r == -1), (gas, cost)
    if r != -1:
        t = 0
        for k in range(n):
            j = (r + k) % n
            t += gas[j] - cost[j]
            assert t >= 0, (gas, cost, r)
    p = [random.randint(0, 9) for _ in range(n)]
    assert ns["max_profit"](p) == brute_stock(p)
    rt = [random.randint(0, 4) for _ in range(n)]
    assert ns["candy"](rt) == brute_candy(rt), rt
    nn = [random.choice([0, 1, 3, 30, 34, 5, 9, 10, 2, 20]) for _ in range(random.randint(1, 5))]
    assert ns["largest_number"](nn) == brute_largest(nn), nn
    s = "".join(random.choice("abcde") for _ in range(random.randint(1, 10)))
    assert ns["partition_labels"](s) == brute_part(s), s
    assert sum(ns["partition_labels"](s)) == len(s)
assert ns["coin_change_dp"]([1, 3, 4], 6) == 2 and coin_greedy([1, 3, 4], 6) == 3
assert ns["coin_change_dp"]([1, 5, 10, 25], 30) == coin_greedy([1, 5, 10, 25], 30) == 2
assert ns["can_jump"]([2, 3, 1, 1, 4]) is True and ns["can_jump"]([3, 2, 1, 0, 4]) is False
assert ns["jump"]([2, 3, 1, 1, 4]) == 2 and ns["jump"]([2, 3, 1, 1, 2, 4, 1]) == 3
assert ns["can_complete_circuit"]([2, 1, 1, 5, 1, 2], [1, 3, 2, 2, 2, 2]) == 3
assert ns["can_complete_circuit"]([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]) == 3
assert ns["max_profit"]([7, 1, 5, 3, 6, 4]) == 7
assert ns["candy"]([1, 0, 2, 3, 1]) == 9
assert ns["largest_number"]([3, 30, 34, 5, 9]) == "9534330" and ns["largest_number"]([0, 0]) == "0"
assert ns["partition_labels"]("abacbdefe") == [5, 1, 3]
assert ns["partition_labels"]("ababcbacadefegdehijhklij") == [9, 7, 8]
print("all code checks passed")

# ------------------------------------------------------------------ SVG
g.build_all()
_, ok = g.jump_trace_data([2, 3, 1, 1, 4])
assert ok
_, jumps = g.jump2_trace_data([2, 3, 1, 1, 2, 4, 1])
assert jumps == ns["jump"]([2, 3, 1, 1, 2, 4, 1])
_, ans = g.gas_trace_data([2, 1, 1, 5, 1, 2], [1, 3, 2, 2, 2, 2])
assert ans == ns["can_complete_circuit"]([2, 1, 1, 5, 1, 2], [1, 3, 2, 2, 2, 2])
assert g.stock_rows([7, 1, 5, 3, 6, 4])[1] == 7
_, _, L, R, fin = g.candy_data([1, 0, 2, 3, 1])
assert sum(fin) == ns["candy"]([1, 0, 2, 3, 1]) and (L, R, fin) == ([1, 1, 2, 3, 1], [2, 1, 1, 2, 1], [2, 1, 2, 3, 1])
assert g.largest_rows([3, 30, 34, 5, 9])[1] == ns["largest_number"]([3, 30, 34, 5, 9])
assert g.partition_rows("abacbdefe")[1] == ns["partition_labels"]("abacbdefe")

# ------------------------------------------------------------------ HTML
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '16_greedy_doc.py'), encoding='utf-8').read())
