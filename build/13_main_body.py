
# ===================================================================== 被讲解的代码 (单一来源: 展示 = 测试)
SRC = {}

SRC["template"] = '''
def backtrack(path, choices):
    if is_done(path):                 # 1. 结束条件: path 已经是一个完整答案
        res.append(path[:])           #    必须 copy: path 还会继续被改
        return
    for c in choices:                 # 2. choices: 此刻还能选什么
        if not valid(path, c):        #    约束剪枝: 这个选择一定走不通, 不进去
            continue
        path.append(c)                # 3. 做选择
        backtrack(path, next_choices(path, c))   # 4. 递归: 树往下一层
        path.pop()                    # 5. 撤销选择: path 回到 "做选择之前"
'''

SRC["subsets"] = '''
def subsets(nums):
    res, path = [], []
    def dfs(start):
        res.append(path[:])                  # 每个节点本身就是一个答案; copy, 因为 path 之后还会变
        for i in range(start, len(nums)):    # 只能选 start 之后的: [1,2] 会出现, [2,1] 不会
            path.append(nums[i])             # 做选择
            dfs(i + 1)                       # 递归: 下一层只能选 i 之后的
            path.pop()                       # 撤销: 回到做选择之前, 兄弟分支才看到干净的 path
    dfs(0)
    return res
'''

SRC["subsets2"] = '''
def subsets(nums):                   # 另一种写法: 每个元素 "选 / 不选" (二叉树)
    res, path = [], []
    def dfs(i):
        if i == len(nums):           # 每个元素都决定完了, 才是叶子
            res.append(path[:])
            return
        dfs(i + 1)                   # 不选 nums[i]: path 不变
        path.append(nums[i])         # 选 nums[i]
        dfs(i + 1)
        path.pop()                   # 撤销
    dfs(0)
    return res
'''

SRC["permute"] = '''
def permute(nums):
    res, path = [], []
    used = [False] * len(nums)               # used[i]: nums[i] 已经在 path 里 (比 "x in path" 的 O(n) 快)
    def dfs():
        if len(path) == len(nums):           # 每个位置都填好了
            res.append(path[:])
            return
        for i in range(len(nums)):           # 每一层都从头看: 排列允许先选后面的元素
            if used[i]:                      # 剪枝: 已经用过的不能再用
                continue
            used[i] = True                   # 做选择: 两个状态一起改 (path 和 used)
            path.append(nums[i])
            dfs()
            path.pop()                       # 撤销: 两个状态一起还原
            used[i] = False
    dfs()
    return res
'''

SRC["comb"] = '''
def combination_sum(candidates, target):
    candidates.sort()                        # 排序: 一旦 c > remain, 后面更大的也不行, 可以 break
    res, path = [], []
    def dfs(start, remain):                  # remain = target - sum(path), 不用每次重算 sum
        if remain == 0:                      # 结束条件: 刚好凑够
            res.append(path[:])
            return
        for i in range(start, len(candidates)):
            c = candidates[i]
            if c > remain:                   # 剪枝: 超了; 排过序, 后面的更大, 直接 break
                break
            path.append(c)
            dfs(i, remain - c)               # 关键: 传 i (不是 i+1) => 同一个数可以重复选
            path.pop()
    dfs(0, target)
    return res
'''

SRC["comb2"] = '''
def combination_sum2(candidates, target):
    candidates.sort()                        # 排序: 相同的数挨在一起, 才能 "和前一个比" 去重
    res, path = [], []
    def dfs(start, remain):
        if remain == 0:
            res.append(path[:])
            return
        for i in range(start, len(candidates)):
            if i > start and candidates[i] == candidates[i - 1]:
                continue                     # 同一层 (同一个 for 里) 已经试过这个值了, 子树会完全一样
            c = candidates[i]
            if c > remain:
                break
            path.append(c)
            dfs(i + 1, remain - c)           # 每个数只能用一次 => 传 i + 1
            path.pop()
    dfs(0, target)
    return res
'''

SRC["parens"] = '''
def generate_parenthesis(n):
    res, path = [], []
    def dfs(open_, close):                   # open_ / close: path 里已有的 ( 和 ) 的个数
        if len(path) == 2 * n:
            res.append("".join(path))
            return
        if open_ < n:                        # 剪枝 1: ( 最多 n 个
            path.append("(")
            dfs(open_ + 1, close)
            path.pop()
        if close < open_:                    # 剪枝 2: ) 不能比 ( 多, 否则前缀已经不合法
            path.append(")")
            dfs(open_, close + 1)
            path.pop()
    dfs(0, 0)
    return res
'''

SRC["letters"] = '''
def letter_combinations(digits):
    if not digits:
        return []
    PHONE = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
             "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
    res, path = [], []
    def dfs(idx):                            # idx: 正在决定第几个数字; 层数 = len(digits), 固定
        if idx == len(digits):
            res.append("".join(path))
            return
        for ch in PHONE[digits[idx]]:        # choices 取决于层数, 不是 start index: 每层是独立的 "槽"
            path.append(ch)
            dfs(idx + 1)
            path.pop()
    dfs(0)
    return res
'''

SRC["wsearch"] = '''
def exist(board, word):
    R, C = len(board), len(board[0])
    def dfs(r, c, k):                        # k: 已经匹配了 word[:k]; 现在要让 (r, c) 匹配 word[k]
        if k == len(word):                   # 结束条件: word 全部匹配
            return True
        if not (0 <= r < R and 0 <= c < C) or board[r][c] != word[k]:
            return False                     # 剪枝: 越界 / 字母不对 / 已经被标记成 "#"
        board[r][c] = "#"                    # 做选择: 原地标记, 当作 used[] (字母里不会有 "#")
        found = (dfs(r + 1, c, k + 1) or dfs(r - 1, c, k + 1) or
                 dfs(r, c + 1, k + 1) or dfs(r, c - 1, k + 1))
        board[r][c] = word[k]                # 撤销: 恢复原字母; 找到了也要恢复, 不能留着改过的 board
        return found
    return any(dfs(r, c, 0) for r in range(R) for c in range(C))
'''

SRC["nqueens"] = '''
def solve_n_queens(n):
    res, path = [], []                       # path[r] = 第 r 行的皇后放在第几列
    cols, diag, anti = set(), set(), set()   # 已占用的 列 / 主对角线 (r - c) / 副对角线 (r + c)
    def dfs(r):
        if r == n:                           # n 行都放好了
            res.append(["." * c + "Q" + "." * (n - c - 1) for c in path])
            return
        for c in range(n):
            if c in cols or (r - c) in diag or (r + c) in anti:
                continue                     # 剪枝: 同列 / 同一条 \\ 对角线 / 同一条 / 对角线
            cols.add(c); diag.add(r - c); anti.add(r + c)      # 做选择: 三个 set + path
            path.append(c)
            dfs(r + 1)
            path.pop()                                         # 撤销: 三个 set + path 全部还原
            cols.remove(c); diag.remove(r - c); anti.remove(r + c)
    dfs(0)
    return res
'''

import re as _re


def _tidy(code):
    """把每行的注释对齐到该代码块里最长的代码行之后 (缩短横向宽度)。"""
    lines = code.strip("\n").split("\n")
    parts = []
    for l in lines:
        m = _re.search(r"\s{2,}# ", l)
        if m:
            parts.append((l[:m.start()].rstrip(), l[m.start():].strip()))
        else:
            parts.append((l, None))
    width = max(len(c) for c, cm in parts if cm) + 2
    out = []
    for c, cm in parts:
        out.append(c.ljust(width) + cm if cm else c)
    return "\n" + "\n".join(out) + "\n"


for _k in list(SRC):
    if _k != "template":
        SRC[_k] = _tidy(SRC[_k])

NS = {}
for _k, _v in SRC.items():
    if _k == "template":
        continue
    exec(_v, NS)
    if _k == "subsets2":
        NS["subsets_bin"] = NS["subsets"]
    if _k == "subsets":
        NS["subsets_start"] = NS["subsets"]
# subsets2 覆盖了 subsets: 分别取回
exec(SRC["subsets"], NS)
NS["subsets_start"] = NS["subsets"]
exec(SRC["subsets2"], NS)
NS["subsets_bin"] = NS["subsets"]

# ===================================================================== 正确性测试 (对照 itertools / 暴力)
import itertools


def _test():
    for nums in ([], [1], [1, 2, 3], [4, 5, 6, 7]):
        want = sorted(sorted(c) for r in range(len(nums) + 1)
                      for c in itertools.combinations(nums, r))
        assert sorted(sorted(x) for x in NS["subsets_start"](nums)) == want
        assert sorted(sorted(x) for x in NS["subsets_bin"](nums)) == want
        assert len(NS["subsets_start"](nums)) == 2 ** len(nums)
    for nums in ([1], [1, 2], [1, 2, 3], [1, 2, 3, 4]):
        got = NS["permute"](nums)
        assert sorted(got) == sorted(list(p) for p in itertools.permutations(nums))
    def brute_cs(c, t):
        out = set()
        for counts in itertools.product(*[range(t // x + 1) for x in c]):
            if sum(a * b for a, b in zip(counts, c)) == t:
                out.add(tuple(sorted(x for x, k in zip(c, counts) for _ in range(k))))
        return out
    for c, t in (([2, 3, 5], 8), ([2, 3, 6, 7], 7), ([2], 1), ([3, 5, 8], 11)):
        got = NS["combination_sum"](list(c), t)
        assert {tuple(x) for x in got} == brute_cs(c, t) and len(got) == len({tuple(x) for x in got})
    def brute_cs2(c, t):
        out = set()
        for r in range(len(c) + 1):
            for comb in itertools.combinations(c, r):
                if sum(comb) == t:
                    out.add(tuple(sorted(comb)))
        return out
    for c, t in (([10, 1, 2, 7, 6, 1, 5], 8), ([2, 5, 2, 1, 2], 5), ([1, 2, 2, 3], 5), ([1, 1, 1], 2)):
        got = NS["combination_sum2"](list(c), t)
        assert {tuple(x) for x in got} == brute_cs2(c, t) and len(got) == len({tuple(x) for x in got})
    def valid(s):
        b = 0
        for ch in s:
            b += 1 if ch == "(" else -1
            if b < 0:
                return False
        return b == 0
    for n in range(1, 8):
        got = NS["generate_parenthesis"](n)
        want = [s for s in ("".join(p) for p in itertools.product("()", repeat=2 * n)) if valid(s)]
        assert sorted(got) == sorted(want)
    assert len(NS["generate_parenthesis"](3)) == 5
    PH = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl", "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
    for d in ("", "2", "23", "79"):
        got = NS["letter_combinations"](d)
        want = ["".join(p) for p in itertools.product(*[PH[x] for x in d])] if d else []
        assert got == want
    def brute_ws(board, word):
        R, C = len(board), len(board[0])
        def go(r, c, k, seen):
            if board[r][c] != word[k]:
                return False
            if k == len(word) - 1:
                return True
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and (nr, nc) not in seen:
                    if go(nr, nc, k + 1, seen | {(nr, nc)}):
                        return True
            return False
        return any(go(r, c, 0, {(r, c)}) for r in range(R) for c in range(C))
    import random
    random.seed(7)
    for _ in range(400):
        R, C = random.randint(1, 3), random.randint(1, 3)
        b = [[random.choice("ABC") for _ in range(C)] for _ in range(R)]
        w = "".join(random.choice("ABC") for _ in range(random.randint(1, 5)))
        b0 = [r[:] for r in b]
        assert NS["exist"](b, w) == brute_ws(b0, w)
        assert b == b0                       # 撤销做对了: board 原样
    for n, cnt in ((1, 1), (2, 0), (3, 0), (4, 2), (5, 10), (6, 4), (8, 92)):
        assert len(NS["solve_n_queens"](n)) == cnt
    assert NS["solve_n_queens"](4) == [[".Q..", "...Q", "Q...", "..Q."], ["..Q.", "Q...", "...Q", ".Q.."]]
    # 模板: 用最简单的 "n 位二进制串" 实例化, 确认骨架能跑
    res = []
    def is_done(p): return len(p) == 3
    def valid_(p, c): return True
    def next_choices(p, c): return [0, 1]
    def backtrack(path, choices):
        if is_done(path):
            res.append(path[:]); return
        for c in choices:
            if not valid_(path, c): continue
            path.append(c)
            backtrack(path, next_choices(path, c))
            path.pop()
    backtrack([], [0, 1])
    assert len(res) == 8 and res[0] == [0, 0, 0] and res[-1] == [1, 1, 1]
    print("all tests passed")


_test()
