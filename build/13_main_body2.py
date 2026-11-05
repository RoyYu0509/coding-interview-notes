
# ===================================================================== 带记录的版本 (逻辑与上面完全一致, 只多了 rec.* 调用)
def F(p):
    return "[" + ",".join(str(x) for x in p) + "]"


def rec_subsets(nums):
    R = Rec("[]")
    res, path = [], []

    def dfs(start):
        res.append(path[:])
        R.record(path, F(path), "res 多一个答案")
        for i in range(start, len(nums)):
            path.append(nums[i])
            R.push(nums[i], path, F(path), why="start=%d, i=%d" % (start, i))
            dfs(i + 1)
            before = F(path)
            path.pop()
            R.pop(nums[i], path, "%s 的子树走完" % before)
    dfs(0)
    return R, res


def rec_permute(nums):
    R = Rec("[]")
    res, path = [], []
    used = [False] * len(nums)

    def dfs():
        if len(path) == len(nums):
            res.append(path[:])
            R.record(path, F(path), "len(path) == %d" % len(nums), dict(used=list(used)))
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            R.push(nums[i], path, F(path), dict(used=list(used)), "used[%d] = True" % i)
            dfs()
            path.pop()
            used[i] = False
            R.pop(nums[i], path, "used[%d] = False" % i, dict(used=list(used)))
    dfs()
    return R, res


def rec_comb(candidates, target):
    candidates = sorted(candidates)
    R = Rec("[]")
    res, path = [], []

    def dfs(start, remain):
        if remain == 0:
            res.append(path[:])
            R.record(path, F(path), "remain == 0", dict(remain=remain))
            return
        for i in range(start, len(candidates)):
            c = candidates[i]
            if c > remain:
                R.prune(c, path, F(path + [c]), "%d>%d" % (c, remain),
                        "%d > remain %d, break" % (c, remain), dict(remain=remain))
                break
            path.append(c)
            R.push(c, path, F(path), dict(remain=remain - c), "%d <= remain %d" % (c, remain))
            dfs(i, remain - c)
            path.pop()
            R.pop(c, path, "%d 的子树走完" % c, dict(remain=remain))
    dfs(0, target)
    return R, res


def rec_comb2(candidates, target):
    candidates = sorted(candidates)
    R = Rec("[]")
    res, path = [], []

    def dfs(start, remain):
        if remain == 0:
            res.append(path[:])
            R.record(path, F(path), "remain == 0", dict(remain=remain))
            return
        for i in range(start, len(candidates)):
            c = candidates[i]
            if i > start and c == candidates[i - 1]:
                R.prune(c, path, F(path + [c]), "同层重复",
                        "i=%d>start=%d, %d==%d" % (i, start, c, candidates[i - 1]),
                        dict(remain=remain))
                continue
            if c > remain:
                R.prune(c, path, F(path + [c]), "%d>%d" % (c, remain),
                        "%d > remain %d, break" % (c, remain), dict(remain=remain))
                break
            path.append(c)
            R.push(c, path, F(path), dict(remain=remain - c), "i=%d, start=%d" % (i, start))
            dfs(i + 1, remain - c)
            path.pop()
            R.pop(c, path, "%d 的子树走完" % c, dict(remain=remain))
    dfs(0, target)
    return R, res


def rec_parens(n):
    R = Rec('""')
    res, path = [], []

    def S():
        return "".join(path)

    def dfs(o, c):
        if len(path) == 2 * n:
            res.append("".join(path))
            R.record(path, S(), "len(path) == %d" % (2 * n), dict(o=o, c=c))
            return
        if o < n:
            path.append("(")
            R.push("(", path, S(), dict(o=o + 1, c=c), "open_ %d < n %d" % (o, n))
            dfs(o + 1, c)
            path.pop()
            R.pop("(", path, "子树走完", dict(o=o, c=c))
        else:
            R.prune("(", path, S() + "(", "open_=n", "open_ = n = %d" % n, dict(o=o, c=c))
        if c < o:
            path.append(")")
            R.push(")", path, S(), dict(o=o, c=c + 1), "close %d < open_ %d" % (c, o))
            dfs(o, c + 1)
            path.pop()
            R.pop(")", path, "子树走完", dict(o=o, c=c))
        else:
            R.prune(")", path, S() + ")", "close\n>= open_", "close %d >= open_ %d" % (c, o),
                    dict(o=o, c=c))
    dfs(0, 0)
    return R, res


PHONE = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
         "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}


def rec_letters(digits):
    R = Rec('""')
    res, path = [], []

    def dfs(idx):
        if idx == len(digits):
            res.append("".join(path))
            R.record(path, "".join(path), "idx == %d" % len(digits), dict(idx=idx))
            return
        for ch in PHONE[digits[idx]]:
            path.append(ch)
            R.push(ch, path, "".join(path), dict(idx=idx + 1), "digits[%d]=%s" % (idx, digits[idx]))
            dfs(idx + 1)
            path.pop()
            R.pop(ch, path, "子树走完", dict(idx=idx))
    dfs(0)
    return R, res


def rec_wsearch(board, word):
    board = [r[:] for r in board]
    R = Rec("")
    path = []
    Rn, Cn = len(board), len(board[0])
    ans = {}

    def snap():
        return dict(grid=[r[:] for r in board])

    def dfs(r, c, k):
        if k == len(word):
            R.record(path, "".join(path), "k == len(word)", snap())
            return True
        if not (0 <= r < Rn and 0 <= c < Cn):
            R.prune("x", path, "x", "越界", "(%d,%d) 越界" % (r, c), snap())
            return False
        if board[r][c] != word[k]:
            why = ("(%d,%d) 是 # 用过了" % (r, c)) if board[r][c] == "#" else \
                  ("%s != word[%d]=%s" % (board[r][c], k, word[k]))
            R.prune(board[r][c], path, "x", "", why, snap())
            return False
        board[r][c] = "#"
        path.append(word[k])
        R.push(word[k], path, "x", snap(), "mark (%d,%d) -> #" % (r, c))
        found = (dfs(r + 1, c, k + 1) or dfs(r - 1, c, k + 1) or
                 dfs(r, c + 1, k + 1) or dfs(r, c - 1, k + 1))
        board[r][c] = word[k]
        path.pop()
        R.pop(word[k], path, "恢复 (%d,%d) = %s" % (r, c, word[k]), snap())
        return found
    out = any(dfs(r, c, 0) for r in range(Rn) for c in range(Cn))
    return R, out


def rec_nqueens(n):
    R = Rec("[]")
    res, path = [], []
    cols, diag, anti = set(), set(), set()

    def sets():
        return dict(cols=sorted(cols), diag=sorted(diag), anti=sorted(anti))

    def dfs(r):
        if r == n:
            res.append(list(path))
            R.record(path, F(path), "r == n", sets())
            return
        for c in range(n):
            if c in cols or (r - c) in diag or (r + c) in anti:
                if c in cols:
                    why = "col %d 在 cols 里" % c
                elif (r - c) in diag:
                    why = "r-c=%d 在 diag 里" % (r - c)
                else:
                    why = "r+c=%d 在 anti 里" % (r + c)
                R.prune(c, path, F(path + [c]), "", why, sets())
                continue
            cols.add(c); diag.add(r - c); anti.add(r + c)
            path.append(c)
            R.push(c, path, F(path), sets(), "place (%d,%d)" % (r, c))
            dfs(r + 1)
            path.pop()
            cols.remove(c); diag.remove(r - c); anti.remove(r + c)
            R.pop(c, path, "撤销 (%d,%d)" % (r, c), sets())
    dfs(0)
    return R, res


# 一致性: 带记录版本的答案 == 展示的版本的答案
assert rec_subsets([1, 2, 3])[1] == NS["subsets_start"]([1, 2, 3])
assert rec_permute([1, 2, 3])[1] == NS["permute"]([1, 2, 3])
assert rec_comb([2, 3, 5], 8)[1] == NS["combination_sum"]([2, 3, 5], 8)
assert rec_comb2([1, 2, 2, 3], 5)[1] == NS["combination_sum2"]([1, 2, 2, 3], 5)
assert rec_parens(2)[1] == NS["generate_parenthesis"](2)
assert rec_parens(3)[1] == NS["generate_parenthesis"](3)
assert rec_letters("23")[1] == NS["letter_combinations"]("23")
assert [[r for r in range(4)] for _ in range(1)]
assert [["." * c + "Q" + "." * (3 - c) for c in sol] for sol in rec_nqueens(4)[1]] == NS["solve_n_queens"](4)
