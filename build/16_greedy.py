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
doc = d.Doc("16 · Greedy")
doc.main("主线: greedy = 每一步只做当前看起来最好的选择, 永不回头; 前提是你能证明'最优解里一定可以含这个选择' (exchange argument)。"
         "题型上基本只有三种手法: 维护一个汇总量一遍扫 (max_reach / tank / end), 两遍扫描满足左右约束, 自定义排序。")
doc.main("概念链: Jump Game (max_reach) → Jump Game II (BFS 分层: cur_end / farthest) → Gas Station (tank &lt; 0 就重置起点) → "
         "Stock II (所有上涨都吃) → Candy (两遍扫描) → Largest Number (自定义比较 a+b vs b+a) → Partition Labels (last occurrence 当边界)。")

doc.h2("0. 第一性原理: greedy 在省什么, 什么时候不能用")
doc.p("Brute force 是'每一步试所有选择, 再看哪条路最好'。以 Jump Game 为例: 从 i 可以跳 1..nums[i] 步, DFS 把每个选择都走一遍, O(2^n); 加 memo 后 O(n^2)。"
      "它在浪费的是: <b>明明有些选择一定不会比另一个选择差, 却还要把它们都走完</b>。")
doc.p("Greedy 的做法: 每一步只留下那个'一定不会更差'的选择, 其余直接丢掉, 于是不用分叉, 也不用记 dp 表, 往往 O(n) 或 O(n log n) (多出来的 log 来自排序)。"
      "关键不在于'选最大/最小', 而在于<b>能说清楚为什么这一步选择不会错过全局最优</b>。证明套路叫 exchange argument:")
doc.p("假设有一个最优解没用我这步选择。把它里面的某一部分换成我的选择, 如果换完<b>不比原来差</b>, 就说明'含我这步选择'的最优解一定存在, greedy 这一步安全。"
      "下图左边 (硬币 1/5/10/25) 换得动, 右边 (coins=[1,3,4]) 换不动, 这就是 greedy 和 DP 的分界线。")
doc.svg("16-greedy/greedy_core.svg", "同样是 Coin Change 先拿最大面额: [1,5,10,25] 能换所以 greedy 对; [1,3,4] 换不了所以必须 DP。")
doc.p("反例要用 DP 解 (试每一种最后一枚硬币, 不赌最大的):")
doc.code(CODE_COIN)
doc.p("所以遇到'求最少/最多'的题: 先试着说一句 '最优解里一定可以含我这步选择, 因为换掉别的东西不会变差'。说得出来 → greedy; 举得出反例 → DP。"
      "面试里最稳的做法是: 先写 2-3 个小例子手算, 看 greedy 有没有被打脸。")
doc.p("通用模板 (本文每道题都是它的变体):")
doc.code(CODE_TEMPLATE)
doc.p("顺带: 区间题 (最多不重叠区间 / 射气球 / 合并) 的 greedy 是'按 end 排序再扫', 见 10 doc; 需要反复取当前最大/最小再做决定的 greedy "
      "(Task Scheduler, Reorganize String) 要配 heap, 见 09 doc。本文只讲不需要这两样的 greedy。")

doc.h2("1. Jump Game: 只维护一个数 max_reach")
doc.p("题目: <code>nums[i]</code> 是在 i 最多能往前跳几步, 从 0 出发, 能否到最后一格? 例: <code>[2,3,1,1,4]</code> 可以, <code>[3,2,1,0,4]</code> 不行 (卡在下标 3 的 0)。")
doc.p("Brute force: DFS 或 DP, 对每个 i 试 1..nums[i] 种跳法, O(n^2)。浪费在: 能到 i 之后, 从 i 起跳的所有落点都要单独记一遍, 但其实<b>只有'最远能到哪'才重要</b>。")
doc.p("关键观察: 若 i 可达, 那么从 i 起跳能落到 i+1 ... i+nums[i] 任意一格, 没有洞。所以可达集合永远是前缀 [0, max_reach], 一个数就描述了全部状态。")
doc.svg("16-greedy/jump_game_core.svg", "invariant: 0..max_reach 全部可达。失败 = 扫到的 i 超过 max_reach。")
doc.svg("16-greedy/jump_game_trace.svg", "[2,3,1,1,4]: i=0 时 max_reach=2, i=1 时推到 4, 之后一直 ≤ 4, 没卡住。")
doc.code(CODE_JUMP)
doc.p("Time O(n) (一遍扫); Space O(1) (只有 max_reach)。")
doc.note("Jump Game = 扫描 + max_reach = max(max_reach, i + nums[i]);i &gt; max_reach 就失败。")

doc.h2("2. Jump Game II: 同一个 max_reach, 加上 BFS 分层")
doc.p("题目: 保证能到终点, 问<b>最少</b>跳几次。例: <code>[2,3,1,1,4]</code> → 2。相比上一题: 多出来的条件是'要数层数', 所以把 max_reach 拆成两个量: 当前层的边界 <code>cur_end</code> 和下一层的边界 <code>farthest</code>。")
doc.p("Brute force: BFS (每个下标是节点, i → i+1..i+nums[i] 是边), O(n^2) 条边。浪费在: 同一层里的下标跳出去的区间是连续、互相重叠的, 不需要逐个节点入队, 只要知道这一层最右能到哪。")
doc.p("关键观察: BFS 第 j 层 = 跳 j 步能到的下标区间 (连续)。扫当前层时用 farthest 收集'下一层最右到哪'; 扫到当前层末尾 (i == cur_end) 就是 BFS 换层, jumps += 1。")
doc.svg("16-greedy/jump_game_ii_core.svg", "每一层是一个连续区间; cur_end 是它的右端, farthest 是扫这一层时算出的下一层右端。")
doc.svg("16-greedy/jump_game_ii_trace.svg", "[2,3,1,1,2,4,1]: i=0,2,4 三次走到层尾, jumps = 3; farthest 在 i=4 时已 ≥ 终点 6。")
doc.code(CODE_JUMP2)
doc.p("Time O(n); Space O(1)。和上一题相比只多了 <code>cur_end</code> 和 <code>jumps</code> 两个变量, 循环范围到 n-2 (最后一格不用再跳)。")
doc.note("Jump Game II = max_reach 拆成 cur_end (本层边界) + farthest (下一层边界);i == cur_end 时 jumps += 1。")

doc.h2("3. Gas Station: 累计量变负, 就把起点重置到下一站")
doc.p("题目: 环形路, 站 i 加油 <code>gas[i]</code>, 开到下一站耗 <code>cost[i]</code>, 找出发点让你能绕一圈, 无解返回 -1。例: <code>gas=[2,1,1,5,1,2]</code>, <code>cost=[1,3,2,2,2,2]</code> → 3。")
doc.p("Brute force: 每个起点模拟一圈, O(n^2)。浪费在: 起点 s 在 j 失败, 但我们对 s+1, s+2, ... 又重新模拟了一遍同样的路段。")
doc.p("关键观察 (两句话): (1) 从 s 出发在 j 失败, 则 s+1..j 作起点全部也失败: 从 s 走到那些站时 tank 都 ≥ 0 (否则早就在那之前失败了), 那笔'剩余油'相当于补贴, 换成从中途出发就没有这笔补贴, 只会更差。"
      "所以下一个候选直接跳到 j+1。(2) 如果 sum(gas) ≥ sum(cost), 一定有解, 且就是最后留下的 start。")
doc.svg("16-greedy/gas_station_core.svg", "net=[2,1,-5,3,1]: 起点 0,1,2 都失败, 只有起点 3 走得完。")
doc.svg("16-greedy/gas_station_trace.svg", "i=1,2 时 tank 变负, start 依次被推到 2, 3; 之后 tank 不再变负, total=0 ≥ 0, 答案 3。")
doc.code(CODE_GAS)
doc.p("Time O(n) (每个站只看一次); Space O(1)。注意 tank 会清零而 total 不会: tank 回答'从 start 出发能不能走到 i', total 回答'整圈够不够'。")
doc.note("Gas Station = 两个累计量:tank &lt; 0 就 start = i+1 并清零;total ≥ 0 才有解。")

doc.h2("4. Best Time to Buy and Sell Stock II: 所有上涨段都吃掉")
doc.p("题目: 可以买卖任意多次 (同一时刻最多持有一股), 求最大利润。例: <code>[7,1,5,3,6,4]</code> → 7 (买 1 卖 5, 买 3 卖 6)。")
doc.p("Brute force: 枚举所有买卖组合, 指数级 (DP 记录'持有/不持有'是 O(n), 但 greedy 更短)。浪费在: 想去找'真正的买点和卖点', 其实不用找。")
doc.p("关键观察: 任何一段上涨 a → b 都可以拆成逐日上涨的和 (b - a = (p1 - a) + (p2 - p1) + ...), 逐日上涨的收益和一次性买卖相同; 下跌的日子不碰就好。所以答案 = 所有正的 diff 之和。")
doc.svg("16-greedy/stock_ii_core.svg", "绿色是上涨段 (+4, +3), 虚线橙色是下跌段 (-6, -2, -2)。长持有 1→6 只有 5。")
doc.svg("16-greedy/stock_ii_trace.svg", "每天只看和昨天的差: -6, +4, -2, +3, -2。profit 只在 +4 和 +3 时增加。")
doc.code(CODE_STOCK)
doc.p("Time O(n); Space O(1)。对比 Stock I (只能买卖一次): 那题要维护 min_price, 不能把每段上涨都加起来。")
doc.note("Stock II = 相邻差为正就加进 profit,不需要找买卖点。")

doc.h2("5. Candy: 两个方向的约束, 拆成两遍扫描")
doc.p("题目: 孩子排成一行, 每人至少 1 颗糖, rating 比邻居高的孩子要比该邻居多糖, 求最少总糖数。例: <code>ratings=[1,0,2,3,1]</code> → 9。")
doc.p("Brute force: 反复修补直到没有违反 (像 brute_candy 那样循环), 最坏 O(n^2)。一遍扫不行: 扫到 rating=0 的孩子, 它比左邻居低, 可是它要几颗糖取决于<b>右边</b>还没看到的孩子。")
doc.p("关键观察: 约束分成两种, 各自只依赖一边。'比左邻居高'只需要从左往右看一遍; '比右邻居高'只需要从右往左看一遍。每遍各自给出满足这类约束的最少糖数, 最后每个人取两者的 max, 两个约束就同时满足, 而且 max 已经是最小值。")
doc.svg("16-greedy/candy_core.svg", "left 管左约束, right 管右约束, 逐格取 max 就是答案: 2+1+2+3+1 = 9。")
doc.svg("16-greedy/candy_trace.svg", "A 段从左到右填 left, B 段从右到左填 right, C 段取 max 求和。")
doc.code(CODE_CANDY)
doc.p("Time O(n) (三次线性扫描); Space O(n) (left 和 right)。另有 O(1) 空间的'上坡/下坡'写法, 面试用这个两遍版本即可。")
doc.note("Candy = 约束有左右两个方向:从左扫一遍、从右扫一遍,每格取 max。")

doc.h2("6. Largest Number: 自定义排序, 比较 a+b 和 b+a")
doc.p("题目: 把非负整数列表拼成最大的数, 返回字符串。例: <code>[3,30,34,5,9]</code> → <code>\"9534330\"</code>。")
doc.p("Brute force: 枚举所有排列取最大, O(n! · n)。浪费在: 排列的好坏其实只由<b>相邻两个</b>谁在前决定, 不需要看整体。")
doc.p("关键观察: 对任意两个数 a, b, 只有两种拼法 a+b 和 b+a (字符串拼接), 谁大谁在前。这个比较关系可以传递, 所以直接用它当 comparator 排序即可。普通字典序会错: \"3\" 和 \"30\" 里 \"30\" 更大, 但 330 &gt; 303。")
doc.svg("16-greedy/largest_number_core.svg", "字典序给出 303, a+b vs b+a 给出 330。最优解里每个相邻对都必须满足 x+y ≥ y+x。")
doc.svg("16-greedy/largest_number_trace.svg", "逐个插入: 30 排在 3 后面 (303 < 330), 34 插到 3 前面 (343 > 334), 5 和 9 一路插到最前。结果 9534330。")
doc.code(CODE_LARGEST)
doc.p("Time O(n log n · L) (L 是数字位数, 每次比较拼接要 O(L)); Space O(n)。")
doc.note("Largest Number = 自定义 comparator:a 在前 ⇔ a+b &gt; b+a;全零要返回 \"0\"。")

doc.h2("7. Partition Labels: 用 last occurrence 当边界")
doc.p("题目: 把字符串切成尽量多的段, 使每个字母只出现在一段里, 返回每段长度。例: <code>\"abacbdefe\"</code> → <code>[5,1,3]</code>。")
doc.p("Brute force: 对每个切点检查'左右两边有没有共同字母', O(n^2) 或更差。浪费在: 每次都重新查集合, 其实一个字母'必须延伸到哪'是固定的, 就是它的最后一次出现。")
doc.p("关键观察: 当前这段里出现过的每个字母 c, 这段至少要延伸到 last[c]。所以 end = 段内所有字母 last 的最大值 (随扫描只增不减)。当 i == end 时, 段内所有字母都已出现完, 此刻切最早, 段数最多。这和 Jump Game II 是同一个形状: 一个只增不减的边界, 扫到边界就切。")
doc.svg("16-greedy/partition_labels_core.svg", "a 的 last=2, b 的 last=4: 第一段至少到 4。每一段的右边界由段内字母的 last 最大值决定。")
doc.svg("16-greedy/partition_labels_trace.svg", "i=0..4 时 end 从 2 推到 4, 在 i=4 切 (长度 5); i=5 单独成段; i=6,7 把 end 推到 8, i=8 切 (长度 3)。")
doc.code(CODE_PART)
doc.p("Time O(n) (建 last 一遍, 扫描一遍); Space O(1) (字母表大小固定)。")
doc.note("Partition Labels = 先记每个字母的 last,再扫描 end = max(end, last[c]),i == end 就切。")

doc.h2("8. 识别信号: 看到什么 → 试什么")
doc.raw("""<table>
<tr><th>题目特征</th><th>做法</th><th>complexity</th></tr>
<tr><td>问'能不能到 / 最少几步到', 每格有跳跃上限</td><td>扫描维护 max_reach; 数最少步时加 cur_end / farthest 分层</td><td>O(n^2) DP/BFS → O(n)</td></tr>
<tr><td>环形路 / 累计量, 一旦变负当前起点就作废</td><td>tank &lt; 0 就重置起点到 i+1; 另用 total 判断有无解</td><td>O(n^2) → O(n)</td></tr>
<tr><td>可以无限次交易 / 每个正的增量都能拿</td><td>把序列拆成相邻差, 正的全加</td><td>指数 / DP → O(n)</td></tr>
<tr><td>每个元素受左邻居和右邻居两个方向的约束</td><td>从左一遍 + 从右一遍, 最后取 max (或 min)</td><td>反复修补 O(n^2) → O(n)</td></tr>
<tr><td>拼接 / 排队, 只看相邻两项就能比谁先谁后</td><td>自定义 comparator 排序 (交换相邻对不会更差)</td><td>O(n!) → O(n log n)</td></tr>
<tr><td>切段 / 分组, 每个元素有"最晚必须到哪"</td><td>先记 last occurrence, 扫描时维护 end, i == end 就切</td><td>O(n^2) → O(n)</td></tr>
<tr><td>区间选最多 / 合并 / 射气球</td><td>按 end (或 start) 排序再扫, 见 10 doc</td><td>指数 → O(n log n)</td></tr>
<tr><td>每步要取当前最大/最小再决定 (Task Scheduler)</td><td>greedy + heap, 见 09 doc</td><td>O(n^2) → O(n log n)</td></tr>
<tr><td>举得出反例 (如 coins=[1,3,4]) / 选择之间互相影响</td><td>不是 greedy, 用 DP</td><td>-</td></tr>
</table>""")
doc.note("看到'求最少/最多'先想 exchange argument:能说清最优解里一定可以含我这步选择就 greedy,举得出反例就 DP。")
doc.p("以后再学 (一行): Huffman 编码、Dijkstra (greedy + heap 的图版本)、matroid 理论; 面试里基本不会展开。")

doc.write("docs/16-greedy.html")
