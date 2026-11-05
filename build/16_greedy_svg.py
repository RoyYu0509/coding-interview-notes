"""16 · Greedy 的 SVG 生成器 (被 16_greedy.py import)。
所有 trace 的数字都来自下面真的跑过的 traced 函数, 并且和 16_greedy.py 里展示的代码做过对拍。"""
import html
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "docs", "svg", "16-greedy")
FONT = 'ui-sans-serif, system-ui, -apple-system, "PingFang SC", sans-serif'
ROLE = {
    "new":   ("#E1F5EE", "#0F6E56", "#085041"),
    "rm":    ("#FAECE7", "#993C1D", "#712B13"),
    "other": ("#F1EFE8", "#5F5E5A", "#444441"),
    "empty": ("#FFFFFF", "#B4B2A9", "#52514E"),
}
INK, SUB, ORANGE, GRAY = "#0B0B0B", "#52514E", "#D85A30", "#898781"


class S:
    def __init__(self, title, desc=""):
        self.title, self.desc, self.e = title, desc, []

    def text(self, x, y, s, size=14, fill=INK, anchor="start", weight=400):
        self.e.append('<text x="%s" y="%s" font-size="%d" fill="%s" text-anchor="%s" font-weight="%d">%s</text>'
                      % (x, y, size, fill, anchor, weight, html.escape(str(s))))

    def line(self, x1, y1, x2, y2, stroke="#B4B2A9", dash="4 4", w=1, arrow=None):
        m = ' marker-end="url(#%s)"' % arrow if arrow else ""
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        self.e.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s%s/>'
                      % (x1, y1, x2, y2, stroke, w, d, m))

    def path(self, d, stroke=GRAY, w=1.5, dash=None, arrow=None, fill="none"):
        m = ' marker-end="url(#%s)"' % arrow if arrow else ""
        da = ' stroke-dasharray="%s"' % dash if dash else ""
        self.e.append('<path d="%s" fill="%s" stroke="%s" stroke-width="%s"%s%s/>' % (d, fill, stroke, w, da, m))

    def cell(self, x, y, w, h, label, role="other", ring=False, size=16, dash=False):
        f, st, tx = ROLE[role]
        da = ' stroke-dasharray="4 3"' if dash else ""
        self.e.append('<rect x="%s" y="%s" width="%s" height="%s" rx="4" fill="%s" stroke="%s" stroke-width="1"%s/>'
                      % (x, y, w, h, f, st, da))
        if ring:
            self.e.append('<rect x="%s" y="%s" width="%s" height="%s" rx="6" fill="none" stroke="#EF9F27" stroke-width="2.5"/>'
                          % (x - 3, y - 3, w + 6, h + 6))
        if label != "":
            self.text(x + w / 2, y + h / 2 + 5.5, label, size, tx, "middle")

    def circle(self, cx, cy, r, label, role="other", ring=False):
        f, st, tx = ROLE[role]
        self.e.append('<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s"/>' % (cx, cy, r, f, st))
        if ring:
            self.e.append('<circle cx="%s" cy="%s" r="%s" fill="none" stroke="#EF9F27" stroke-width="2.5"/>' % (cx, cy, r + 3))
        self.text(cx, cy + 5.5, label, 16, tx, "middle")

    def sep(self, y):
        self.line(20, y, 660, y)

    def legend(self, y, items):
        x = 20
        for role, name in items:
            self.cell(x, y - 11, 16, 16, "", role)
            self.text(x + 22, y + 2, name, 12, SUB)
            x += 22 + 12 * len(name) * 0.62 + 30 + (12 * len([c for c in name if ord(c) > 255]) * 0.4)
        return y

    def save(self, name, h):
        body = "\n".join(self.e)
        svg = ('<svg width="100%%" viewBox="0 0 680 %d" role="img" xmlns="http://www.w3.org/2000/svg" '
               'font-family=\'%s\'>\n<title>%s</title><desc>%s</desc>\n'
               '<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
               '<path d="M2 1L8 5L2 9" fill="none" stroke="%s" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>'
               '<marker id="arrowo" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
               '<path d="M2 1L8 5L2 9" fill="none" stroke="%s" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>\n'
               '%s\n</svg>\n' % (h, FONT, html.escape(self.title), html.escape(self.desc), GRAY, ORANGE, body))
        os.makedirs(OUT, exist_ok=True)
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(svg)


def header(s, l1, l2=None):
    s.text(20, 26, l1, 14, INK)
    if l2:
        s.text(20, 46, l2, 12, SUB)


def row_cells(s, x, y, vals, roles=None, rings=(), w=34, h=32, size=16):
    for k, v in enumerate(vals):
        s.cell(x + k * w, y, w, h, v, (roles or {}).get(k, "other"), k in rings, size)


# ---------------------------------------------------------------- 0 core
def greedy_core():
    s = S("Greedy 的 exchange argument 与反例",
          "coins [1,5,10,25] 可以把最优解换成含 25 的解; coins [1,3,4] 换不了, greedy 失败。")
    header(s, "greedy = 每步取局部最优; 要证明 (exchange argument):",
           "任何最优解都能换成'含这步选择'的解, 且不变差")
    # panel A
    s.text(20, 78, "A. coins = [1, 5, 10, 25], amount = 30。greedy 第一步拿最大的 25", 14, INK, weight=600)
    s.text(20, 106, "随便一个不含 25 的最优解:", 14)
    row_cells(s, 260, 88, [10, 10, 5, 5], {0: "other", 1: "other", 2: "other", 3: "other"})
    s.text(410, 109, "10+10+5+5 = 30, 共 4 枚", 12, SUB)
    s.text(20, 156, "取出 10+10+5 = 25, 换成一枚 25:", 14)
    row_cells(s, 260, 138, [10, 10, 5, 5], {0: "rm", 1: "rm", 2: "rm", 3: "other"})
    s.text(410, 150, "10+10+5 = 25 被换掉", 12, ORANGE)
    s.path("M 291 172 L 291 190", ORANGE, 1.5, "4 3", "arrowo")
    s.path("M 360 172 L 330 190", ORANGE, 1.5, "4 3", "arrowo")
    row_cells(s, 260, 192, [25, 5], {0: "new", 1: "other"})
    s.text(340, 213, "25+5 = 30, 共 2 枚 (4 → 2)", 12, "#085041")
    s.text(20, 252, "换完没有变差 → '含 25' 的最优解一定存在 → greedy 拿 25 不会错过最优。往后对剩下的 5 重复同样论证。", 12, SUB)
    s.sep(268)
    # panel B
    s.text(20, 296, "B. coins = [1, 3, 4], amount = 6。greedy 第一步拿 4", 14, INK, weight=600)
    s.text(20, 330, "greedy:", 14)
    row_cells(s, 260, 312, [4, 1, 1], {0: "new", 1: "other", 2: "other"})
    s.text(380, 333, "4+1+1 = 6, 共 3 枚", 12, SUB)
    s.text(20, 380, "真正的最优:", 14)
    row_cells(s, 260, 362, [3, 3], {0: "other", 1: "other"})
    s.text(340, 383, "3+3 = 6, 共 2 枚", 12, SUB)
    s.text(20, 424, "最优解 3+3 里找不到'加起来 = 4'的子集 (3 ≠ 4, 3+3 = 6 ≠ 4) → 换不进 4 → exchange 失败。", 12, ORANGE)
    s.text(20, 444, "greedy 的局部最优选择会丢掉全局最优 → 这种题要 DP: dp[6] = min(dp[5], dp[3], dp[2]) + 1 = 2。", 12, ORANGE)
    s.sep(462)
    s.text(20, 486, "判断口诀: 能说清'最优解里一定可以含我这步选择'才用 greedy; 说不清、或者举得出反例 → DP。", 14, INK)
    s.save("greedy_core.svg", 504)


# ---------------------------------------------------------------- Jump Game
def jump_trace_data(nums):
    mr, rows = 0, []
    for i, step in enumerate(nums):
        if i > mr:
            rows.append((i, step, mr, None, False))
            return rows, False
        old = mr
        mr = max(mr, i + step)
        rows.append((i, step, old, mr, True))
    return rows, True


def jump_game_core():
    s = S("Jump Game 的 invariant", "可达集合永远是前缀 [0, max_reach], 所以只需要维护 max_reach 一个数")
    header(s, "invariant: 扫到 i 时, 下标 0..max_reach 全部可达 (中间没有'洞'),  max_reach = max(i + nums[i])",
           "因为从某个可达的格子起跳, 能落到它后面任意一格 (跳 1..nums[i] 步), 所以可达集合是连续的前缀")
    # ex 1 fail
    nums = [3, 2, 1, 0, 4]
    s.text(20, 82, "例 1: nums = [3, 2, 1, 0, 4]", 14, INK, weight=600)
    for k in range(5):
        s.text(300 + k * 40 + 18, 104, "i=%d" % k, 12, SUB, "middle")
        s.cell(300 + k * 40, 110, 36, 32, nums[k], "other" if k <= 3 else "rm", k == 4)
    s.text(20, 132, "i=0: 0+3 = 3 · i=1: 1+2 = 3", 12, SUB)
    s.text(20, 150, "i=2: 2+1 = 3 · i=3: 3+0 = 3", 12, SUB)
    s.path("M 300 154 L 456 154", "#0F6E56", 2)
    s.text(300, 172, "可达 = [0, 3]  (max_reach = 3)", 12, "#085041")
    s.text(500, 172, "i=4 > max_reach=3 → 卡住", 12, "#712B13")
    s.text(20, 194, "→ return False", 14, "#712B13")
    s.sep(214)
    nums = [2, 3, 1, 1, 4]
    s.text(20, 242, "例 2: nums = [2, 3, 1, 1, 4]", 14, INK, weight=600)
    for k in range(5):
        s.text(300 + k * 40 + 18, 264, "i=%d" % k, 12, SUB, "middle")
        s.cell(300 + k * 40, 270, 36, 32, nums[k], "other")
    s.text(20, 292, "i=0: 0+2 = 2 · i=1: 1+3 = 4", 12, SUB)
    s.path("M 300 314 L 494 314", "#0F6E56", 2)
    s.text(300, 332, "max_reach = 4 ≥ 最后一格 4 → 可达", 12, "#085041")
    s.text(20, 332, "→ return True", 14, "#085041")
    s.sep(352)
    s.text(20, 376, "greedy 选择 = '每个格子都尽量往远处记': 只留最远的一个数, 比 DFS 记录每个可达位置省掉所有重复探索。", 12, SUB)
    s.save("jump_game_core.svg", 394)


def jump_game_trace():
    nums = [2, 3, 1, 1, 4]
    rows, ok = jump_trace_data(nums)
    assert ok
    s = S("Jump Game trace", "nums=[2,3,1,1,4] 每一步的 max_reach")
    header(s, "nums = [2, 3, 1, 1, 4] · 每一步: 检查 i ≤ max_reach → max_reach = max(max_reach, i + nums[i])",
           "max_reach = 当前能到的最远下标; 初始 max_reach = 0")
    s.text(20, 76, "当前 i", 14, SUB)
    s.text(130, 76, "检查 i ≤ max_reach", 14, SUB)
    s.text(300, 76, "更新 max_reach", 14, SUB)
    s.text(500, 76, "可达范围 (数组)", 14, SUB)
    s.sep(86)
    y = 96
    for (i, step, old, new, _) in rows:
        s.text(20, y + 24, "i=%d, nums=%d" % (i, step), 14)
        s.text(130, y + 24, "%d ≤ %d  通过" % (i, old), 14)
        s.text(300, y + 24, "max(%d, %d+%d) = %d" % (old, i, step, new), 16)
        for k in range(5):
            role = "empty"
            if k <= old:
                role = "other"
            elif k <= new:
                role = "new"
            s.cell(500 + k * 32, y + 6, 30, 30, nums[k], role, k == i, 14)
        y += 52
        s.sep(y - 6)
    s.text(20, y + 14, "答案: 每个 i 都 ≤ max_reach, 没有被卡住 → True", 16, "#085041", weight=600)
    s.legend(y + 44, [("other", "之前就可达"), ("new", "这一步新增可达"), ("empty", "目前不可达")])
    s.text(500, y + 44, "金色圈 = 当前 i", 12, SUB)
    s.save("jump_game_trace.svg", y + 64)
    return rows


# ---------------------------------------------------------------- Jump Game II
def jump2_trace_data(nums):
    jumps = cur_end = far = 0
    rows = []
    for i in range(len(nums) - 1):
        oldfar = far
        far = max(far, i + nums[i])
        cut = i == cur_end
        oldend = cur_end
        if cut:
            jumps += 1
            cur_end = far
        rows.append(dict(i=i, step=nums[i], oldfar=oldfar, far=far, cut=cut, oldend=oldend, end=cur_end, jumps=jumps))
    return rows, jumps


def jump2_core():
    s = S("Jump Game II BFS 分层", "每一层 = 跳 j 步能到的下标区间")
    header(s, "把 Jump Game 看成 BFS: 第 j 层 = 跳 j 步能到的下标区间。不用 queue, 只用两个数标出层的边界",
           "cur_end = 当前层最右边的下标;  farthest = 扫过当前层所有格子后, 下一层最右能到哪")
    nums = [2, 3, 1, 1, 4]
    x0, cw = 40, 56
    s.text(20, 78, "nums = [2, 3, 1, 1, 4], 目标 = 下标 4", 14, INK, weight=600)
    for k in range(5):
        s.text(x0 + k * cw + 26, 104, "i=%d" % k, 12, SUB, "middle")
        s.cell(x0 + k * cw, 110, 52, 32, nums[k], "other")
    # brackets
    def br(a, b, y, label, col="#5F5E5A"):
        xa, xb = x0 + a * cw, x0 + b * cw + 52
        s.path("M %d %d L %d %d L %d %d L %d %d" % (xa, y - 8, xa, y, xb, y, xb, y - 8), col, 1.5)
        s.text((xa + xb) / 2, y + 18, label, 12, col, "middle")
    br(0, 0, 166, "层 0: {0}")
    br(1, 2, 166, "层 1: {1, 2}")
    br(3, 4, 166, "层 2: {3, 4}")
    s.text(340, 200, "", 12)
    s.text(20, 218, "从层 0 (只有 i=0) 出发: farthest = 0+2 = 2 → 层 1 的右边界 cur_end = 2", 12, SUB)
    s.text(20, 238, "扫层 1 (i=1,2): farthest = max(1+3, 2+1) = 4 → 层 2 的右边界 cur_end = 4", 12, SUB)
    s.text(20, 258, "4 ≥ 最后一格 4, 到达终点; 一共走了 2 层 = 跳 2 次", 12, SUB)
    s.sep(274)
    s.text(20, 300, "为什么每层只要记 farthest 一个数就够:", 14, INK, weight=600)
    s.text(20, 324, "下一层 = 当前层所有格子能跳到的区间之并, 而每个区间的左端都紧贴当前层, 并起来仍是连续区间。", 12, SUB)
    s.text(20, 344, "所以下一层只由右端点 farthest 决定, 且层 j 的下标一定比层 j+1 靠前 → 第一次覆盖到终点的层数就是最少步数。", 12, SUB)
    s.text(20, 364, "i == cur_end 表示当前层扫完了, 必须再跳一次 (jumps += 1), 并把边界推到 farthest。", 12, SUB)
    s.save("jump_game_ii_core.svg", 382)


def jump_game_ii_trace():
    nums = [2, 3, 1, 1, 2, 4, 1]
    rows, jumps = jump2_trace_data(nums)
    n = len(nums)
    s = S("Jump Game II trace", "nums=[2,3,1,1,2,4,1]")
    header(s, "nums = [2, 3, 1, 1, 2, 4, 1] · 每一步: farthest = max(farthest, i + nums[i])",
           "若 i == cur_end: jumps += 1, cur_end = farthest · 初始全 0 · 循环到 i = n-2 = 5 (最后一格不用再跳)")
    s.text(20, 76, "当前 i", 14, SUB)
    s.text(110, 76, "farthest / 是否到层尾", 14, SUB)
    s.text(470, 76, "数组 (金色圈 = i)", 14, SUB)
    s.sep(86)
    y = 96
    cw = 28
    for r in rows:
        s.text(20, y + 22, "i=%d" % r["i"], 14)
        s.text(20, y + 40, "nums=%d" % r["step"], 12, SUB)
        s.text(110, y + 20, "farthest = max(%d, %d+%d) = %d" % (r["oldfar"], r["i"], r["step"], r["far"]), 14)
        if r["cut"]:
            s.text(110, y + 42, "i=%d == cur_end=%d → 层尾, jumps = %d, cur_end = %d" % (r["i"], r["oldend"], r["jumps"], r["end"]), 12, "#085041", weight=600)
        else:
            s.text(110, y + 42, "i=%d ≠ cur_end=%d → 还在这一层, 不跳 (jumps = %d)" % (r["i"], r["oldend"], r["jumps"]), 12, SUB)
        for k in range(n):
            role = "empty"
            if k <= r["end"]:
                role = "other"
            elif k <= r["far"]:
                role = "new"
            s.cell(470 + k * cw, y + 8, cw - 2, 30, nums[k], role, k == r["i"], 14)
        # cur_end marker: triangle under cell
        ex = 470 + r["end"] * cw + (cw - 2) / 2
        if r["end"] < n:
            s.path("M %s %s l -5 8 l 10 0 z" % (ex, y + 42), "#0F6E56", 1, fill="#0F6E56")
        y += 58
        s.sep(y - 6)
    s.text(20, y + 14, "答案: jumps = %d  (层 0 → 层 1 → 层 2 → 层 3)" % jumps, 16, "#085041", weight=600)
    s.legend(y + 44, [("other", "已在 cur_end 以内"), ("new", "cur_end 之外、farthest 以内 (下一层候选)"), ("empty", "还够不到")])
    s.text(20, y + 66, "绿色小三角 = cur_end (当前层右边界)", 12, SUB)
    s.save("jump_game_ii_trace.svg", y + 84)
    return rows, jumps


# ---------------------------------------------------------------- Gas Station
def gas_trace_data(gas, cost):
    tank = total = start = 0
    rows = []
    for i in range(len(gas)):
        d = gas[i] - cost[i]
        total += d
        oldtank = tank
        tank += d
        reset = tank < 0
        rows.append(dict(i=i, g=gas[i], c=cost[i], d=d, oldtank=oldtank, tank=tank, reset=reset, total=total, start=start))
        if reset:
            start = i + 1
            tank = 0
    return rows, (start if total >= 0 else -1)


def gas_core():
    net = [2, 1, -5, 3, 1]
    s = S("Gas Station 为什么从失败点的下一个开始", "起点 s 在 j 失败, 则 s..j 之间任何起点都失败")
    header(s, "net[i] = gas[i] - cost[i] = [2, 1, -5, 3, 1] · 从 start 出发, 每站 tank += net[i], tank < 0 就失败",
           "每个起点一行: 方框里是走到该站后的 tank")
    s.text(20, 80, "起点", 14, SUB)
    for k in range(5):
        s.text(150 + k * 70 + 28, 70, "站 %d" % k, 12, SUB, "middle")
        s.text(150 + k * 70 + 28, 86, "net=%+d" % net[k], 12, SUB, "middle")
    s.sep(94)
    y = 104
    notes = []
    for st in range(4):
        tank, ok = 0, True
        s.text(20, y + 22, "start = %d" % st, 14)
        k = st
        for step in range(5):
            idx = (st + step) % 5
            tank += net[idx]
            bad = tank < 0
            s.cell(150 + idx * 70, y + 4, 56, 30, tank, "rm" if bad else "other", False, 16, dash=idx < st)
            if bad:
                ok = False
                break
        if st < 3:
            nt = {0: "走到站 1: tank = 2+1 = 3, 站 2: 3-5 = -2 ✗", 1: "只有站 1 的 +1 当底: 1-5 = -4 ✗", 2: "一上来 0-5 = -5 ✗"}[st]
            s.text(150, y + 54, nt, 12, "#712B13")
        else:
            s.text(150, y + 54, "站 3: 3, 站 4: 4, 回到站 0 (虚线): 6, 站 1: 7, 站 2: 7-5 = 2 ≥ 0 ✓", 12, "#085041")
        y += 66
        s.sep(y - 6)
    s.text(20, y + 14, "start=0 在站 2 失败。到站 1 时 tank = 2 ≥ 0 (起点 0 给的'补贴'); start=1 没有这笔补贴, 到同一位置只会更差:", 12, SUB)
    s.text(20, y + 34, "tank(start=1, 站2) = tank(start=0, 站2) - tank(start=0, 站0) = -2 - 2 = -4 < -2", 14, INK)
    s.text(20, y + 54, "所以 start 到失败点之间的起点全部作废, 下一个候选 = 失败点 + 1。", 14, INK)
    s.text(20, y + 80, "全局: total = sum(net) = 2+1-5+3+1 = 2 ≥ 0 → 一定有解, 且就是最后留下的 start。", 12, SUB)
    s.save("gas_station_core.svg", y + 100)


def gas_trace():
    gas = [2, 1, 1, 5, 1, 2]
    cost = [1, 3, 2, 2, 2, 2]
    rows, ans = gas_trace_data(gas, cost)
    s = S("Gas Station trace", "gas=[2,1,1,5,1,2] cost=[1,3,2,2,2,2]")
    header(s, "gas = [2, 1, 1, 5, 1, 2] · cost = [1, 3, 2, 2, 2, 2] · net = gas - cost",
           "每一步: tank += net → 若 tank < 0: 起点 start = i + 1, tank 清 0 · total 一直累加不清零")
    for x, t in ((20, "站 i"), (80, "net = gas - cost"), (230, "tank (本段起点)"), (430, "start / 动作"), (610, "total")):
        s.text(x, 76, t, 14, SUB)
    s.sep(86)
    y = 96
    for r in rows:
        s.text(20, y + 26, "i=%d" % r["i"], 14)
        s.text(80, y + 26, "%d - %d = %+d" % (r["g"], r["c"], r["d"]), 14)
        s.text(230, y + 26, "%d %s %d = " % (r["oldtank"], "+" if r["d"] >= 0 else "-", abs(r["d"])), 14)
        s.cell(310, y + 6, 46, 30, r["tank"], "rm" if r["reset"] else "new", False, 16)
        if r["reset"]:
            s.text(430, y + 20, "tank = %d < 0 → 起点作废" % r["tank"], 12, "#712B13")
            s.text(430, y + 38, "start = %d + 1 = %d, tank = 0" % (r["i"], r["i"] + 1), 12, "#712B13", weight=600)
        else:
            s.text(430, y + 20, "tank = %d ≥ 0" % r["tank"], 12, "#085041")
            s.text(430, y + 38, "继续, start 仍是 %d" % r["start"], 12, SUB)
        s.text(610, y + 26, "%d" % r["total"], 14)
        y += 50
        s.sep(y - 6)
    tot = rows[-1]["total"]
    s.text(20, y + 14, "total = 1 - 2 - 1 + 3 - 1 + 0 = %d ≥ 0 → 有解, 答案 start = %d" % (tot, ans), 16, "#085041", weight=600)
    s.legend(y + 44, [("new", "tank ≥ 0, 继续"), ("rm", "tank < 0, 重置起点")])
    s.save("gas_station_trace.svg", y + 62)
    return rows, ans


# ---------------------------------------------------------------- Stock II
def stock_rows(p):
    profit, rows = 0, []
    for i in range(1, len(p)):
        d = p[i] - p[i - 1]
        old = profit
        if d > 0:
            profit += d
        rows.append(dict(i=i, a=p[i - 1], b=p[i], d=d, old=old, profit=profit))
    return rows, profit


def stock_core():
    p = [7, 1, 5, 3, 6, 4]
    s = S("Stock II core", "总利润 = 所有上涨段之和")
    header(s, "能买卖无限次 (但同一时间只能持有一股) → 每一段上涨都吃掉, 下跌段不碰",
           "prices = [7, 1, 5, 3, 6, 4]")
    x0, dx = 60, 100
    ys = {pp: 250 - pp * 22 for pp in set(p)}
    pts = [(x0 + k * dx, ys[v]) for k, v in enumerate(p)]
    s.line(40, 260, 640, 260, "#B4B2A9", None)
    for k in range(5):
        a, b = pts[k], pts[k + 1]
        up = p[k + 1] > p[k]
        s.path("M %d %d L %d %d" % (a[0], a[1], b[0], b[1]), "#0F6E56" if up else ORANGE, 3 if up else 2, None if up else "5 4")
    for k, (x, y) in enumerate(pts):
        s.circle(x, y, 15, p[k], "other")
        s.text(x, 280, "i=%d" % k, 12, SUB, "middle")
    s.text(186, 188, "+4", 14, "#085041", "middle", 600)
    s.text(392, 150, "+3", 14, "#085041", "middle", 600)
    s.text(132, 164, "-6", 14, "#712B13", "middle")
    s.text(296, 178, "-2", 14, "#712B13", "middle")
    s.text(498, 160, "-2", 14, "#712B13", "middle")
    s.sep(300)
    s.text(20, 324, "上涨段: 1→5 (+4), 3→6 (+3)。profit = 4 + 3 = 7 = (买1卖5) + (买3卖6)", 14, INK)
    s.text(20, 346, "对比一次长持有 1 → 6: 6 - 1 = 5 < 7, 因为它把中间 5→3 的下跌也吃进去了。", 12, SUB)
    s.text(20, 366, "每个相邻差 p[i] - p[i-1] 只有两种: 正的拿 (相当于当天买第二天卖), 负的跳过 (相当于空仓)。", 12, SUB)
    s.text(20, 386, "多个上涨段首尾相连时: (5-1) + (6-5) = 6-1, 逐天拿和一次拿到的总利润一样, 所以不用找'真正的买卖点'。", 12, SUB)
    s.save("stock_ii_core.svg", 404)


def stock_trace():
    p = [7, 1, 5, 3, 6, 4]
    rows, profit = stock_rows(p)
    s = S("Stock II trace", "prices=[7,1,5,3,6,4]")
    header(s, "prices = [7, 1, 5, 3, 6, 4] · 每一步: d = prices[i] - prices[i-1] → d > 0 就 profit += d",
           "初始 profit = 0")
    for x, t in ((20, "i"), (70, "今天 - 昨天"), (240, "d > 0 ?"), (360, "profit"), (520, "价格数组 (金圈 = 今天)")):
        s.text(x, 76, t, 14, SUB)
    s.sep(86)
    y = 96
    for r in rows:
        s.text(20, y + 26, "i=%d" % r["i"], 14)
        s.text(70, y + 26, "%d - %d = %+d" % (r["b"], r["a"], r["d"]), 16)
        if r["d"] > 0:
            s.text(240, y + 26, "%+d > 0  吃" % r["d"], 14, "#085041", weight=600)
            s.text(360, y + 26, "%d + %d = " % (r["old"], r["d"]), 14)
            s.cell(430, y + 6, 40, 30, r["profit"], "new")
        else:
            s.text(240, y + 26, "%+d ≤ 0  跳过" % r["d"], 14, "#712B13")
            s.text(360, y + 26, "不变 = ", 14, SUB)
            s.cell(430, y + 6, 40, 30, r["profit"], "other")
        for k, v in enumerate(p):
            role = "other" if k < r["i"] - 1 else "empty"
            if k == r["i"]:
                role = "new" if r["d"] > 0 else "rm"
            if k == r["i"] - 1:
                role = "other"
            s.cell(520 + k * 24, y + 7, 22, 28, v, role, k == r["i"], 12)
        y += 50
        s.sep(y - 6)
    s.text(20, y + 14, "答案: profit = 0 + 4 + 3 = %d" % profit, 16, "#085041", weight=600)
    s.legend(y + 44, [("new", "上涨, 加进 profit"), ("rm", "下跌, 跳过"), ("empty", "还没走到")])
    s.save("stock_ii_trace.svg", y + 62)
    return rows, profit


# ---------------------------------------------------------------- Candy
def candy_data(r):
    n = len(r)
    L = [1] * n
    steps_l = []
    for i in range(1, n):
        up = r[i] > r[i - 1]
        L[i] = L[i - 1] + 1 if up else 1
        steps_l.append((i, up, L[:]))
    R = [1] * n
    steps_r = []
    for i in range(n - 2, -1, -1):
        up = r[i] > r[i + 1]
        R[i] = R[i + 1] + 1 if up else 1
        steps_r.append((i, up, R[:]))
    fin = [max(a, b) for a, b in zip(L, R)]
    return steps_l, steps_r, L, R, fin


def candy_core():
    r = [1, 0, 2, 3, 1]
    steps_l, steps_r, L, R, fin = candy_data(r)
    s = S("Candy 两遍扫描", "左约束和右约束分开处理, 最后取 max")
    header(s, "ratings 比左邻居高 → 糖比左邻居多; 比右邻居高 → 糖比右邻居多。两条约束一遍扫不完, 就拆成两遍",
           "ratings = [1, 0, 2, 3, 1],  每个孩子至少 1 颗")
    cw = 52
    x0 = 150

    def line(y, name, vals, role="other"):
        s.text(20, y + 21, name, 14)
        for k, v in enumerate(vals):
            s.cell(x0 + k * cw, y, cw - 4, 30, v, role)
    for k in range(5):
        s.text(x0 + k * cw + 24, 74, "i=%d" % k, 12, SUB, "middle")
    line(82, "ratings", r)
    line(132, "left (只管左约束)", L, "other")
    s.text(x0 + 5 * cw + 6, 153, "只看左邻居: 比左高 +1", 12, SUB)
    line(182, "right (只管右约束)", R, "other")
    s.text(x0 + 5 * cw + 6, 203, "只看右邻居: 比右高 +1", 12, SUB)
    for k in range(5):
        s.path("M %d %d L %d %d" % (x0 + k * cw + 24, 216, x0 + k * cw + 24, 236), GRAY, 1.2, "3 3", "arrow")
    line(240, "max(left, right)", fin, "new")
    s.text(x0 + 5 * cw + 6, 261, "= 糖数", 12, SUB)
    s.sep(284)
    s.text(20, 308, "为什么取 max 两条约束同时成立: fin[i] ≥ left[i] 保证比左邻居高的更多; fin[i] ≥ right[i] 保证比右邻居高的更多。", 12, SUB)
    s.text(20, 328, "为什么 max 不浪费: 每条约束单独要求的最小值就是 left[i] / right[i], 同时满足的最小值就是两者较大者。", 12, SUB)
    s.text(20, 348, "一遍扫不行: 扫到 i=1 (rating 0) 时, 它比左邻居低, 但它比谁多要看后面 i=2 才知道 → 所以倒着再扫一次。", 12, SUB)
    s.save("candy_core.svg", 366)


def candy_trace():
    r = [1, 0, 2, 3, 1]
    steps_l, steps_r, L, R, fin = candy_data(r)
    s = S("Candy trace", "ratings=[1,0,2,3,1]")
    header(s, "ratings = [1, 0, 2, 3, 1] · 先从左往右填 left, 再从右往左填 right, 最后逐格取 max 求和",
           "left[i] = left[i-1] + 1 (若 ratings[i] > ratings[i-1]) 否则 1;  right[i] 同理看右邻居")
    cw = 34
    ax = 440
    y = 76
    s.text(20, y + 14, "A. 从左往右 → left", 14, INK, weight=600)
    for k, v in enumerate(r):
        s.cell(ax + k * cw, y - 4, cw - 2, 26, v, "empty", False, 14)
    s.text(ax - 6, y + 14, "ratings", 12, SUB, "end")
    y += 38
    s.sep(y - 6)
    cur = [1] * 5
    s.text(20, y + 22, "i=0: left[0] = 1 (起点)", 14)
    for k in range(5):
        s.cell(ax + k * cw, y + 4, cw - 2, 30, 1 if k == 0 else "", "new" if k == 0 else "empty", k == 0)
    y += 44
    s.sep(y - 6)
    for (i, up, arr) in steps_l:
        if up:
            f = "ratings[%d]=%d > ratings[%d]=%d → left[%d] = %d + 1 = %d" % (i, r[i], i - 1, r[i - 1], i, arr[i - 1], arr[i])
        else:
            f = "ratings[%d]=%d ≤ ratings[%d]=%d → left[%d] = 1" % (i, r[i], i - 1, r[i - 1], i)
        s.text(20, y + 22, "i=%d: " % i + f, 14)
        for k in range(5):
            role = "empty" if k > i else "other"
            if k == i:
                role = "new"
            s.cell(ax + k * cw, y + 4, cw - 2, 30, arr[k] if k <= i else "", role, k == i)
        y += 44
        s.sep(y - 6)
    y += 12
    s.text(20, y + 16, "B. 从右往左 → right", 14, INK, weight=600)
    for k, v in enumerate(r):
        s.cell(ax + k * cw, y - 2, cw - 2, 26, v, "empty", False, 14)
    s.text(ax - 6, y + 16, "ratings", 12, SUB, "end")
    y += 38
    s.sep(y - 6)
    s.text(20, y + 22, "i=4: right[4] = 1 (起点)", 14)
    for k in range(5):
        s.cell(ax + k * cw, y + 4, cw - 2, 30, 1 if k == 4 else "", "new" if k == 4 else "empty", k == 4)
    y += 44
    s.sep(y - 6)
    for (i, up, arr) in steps_r:
        if up:
            f = "ratings[%d]=%d > ratings[%d]=%d → right[%d] = %d + 1 = %d" % (i, r[i], i + 1, r[i + 1], i, arr[i + 1], arr[i])
        else:
            f = "ratings[%d]=%d ≤ ratings[%d]=%d → right[%d] = 1" % (i, r[i], i + 1, r[i + 1], i)
        s.text(20, y + 22, "i=%d: " % i + f, 14)
        for k in range(5):
            role = "empty" if k < i else "other"
            if k == i:
                role = "new"
            s.cell(ax + k * cw, y + 4, cw - 2, 30, arr[k] if k >= i else "", role, k == i)
        y += 44
        s.sep(y - 6)
    y += 12
    s.text(20, y + 16, "C. 逐格取 max(left, right)", 14, INK, weight=600)
    y += 30
    s.sep(y - 6)
    s.text(20, y + 22, "left  = %s" % L, 14)
    s.text(20, y + 44, "right = %s" % R, 14)
    for k in range(5):
        s.cell(ax + k * cw, y + 4, cw - 2, 30, fin[k], "new")
    s.text(ax + 5 * cw + 2, y + 24, "", 12)
    y += 74
    s.text(20, y + 8, "答案: " + " + ".join(map(str, fin)) + " = %d" % sum(fin), 16, "#085041", weight=600)
    s.text(20, y + 30, "i=0: max(%d,%d)=%d,  i=1: max(%d,%d)=%d,  i=2: max(%d,%d)=%d,  i=3: max(%d,%d)=%d,  i=4: max(%d,%d)=%d" % tuple(
        v for k in range(5) for v in (L[k], R[k], fin[k])), 12, SUB)
    s.legend(y + 58, [("new", "这一步写入"), ("other", "已填好"), ("empty", "还没填")])
    s.save("candy_trace.svg", y + 76)
    return L, R, fin


# ---------------------------------------------------------------- Largest Number
def largest_rows(nums):
    strs = [str(x) for x in nums]
    lst, rows = [], []
    for x in strs:
        if not lst:
            rows.append((x, None, None, None, "empty", [x]))
            lst = [x]
            continue
        pos = len(lst)
        cmp_rows = []
        for j, e in enumerate(lst):
            ok = x + e > e + x
            cmp_rows.append((e, x + e, e + x, ok))
            if ok:
                pos = j
                break
        lst = lst[:pos] + [x] + lst[pos:]
        rows.append((x, cmp_rows, pos, lst[:], None, lst[:]))
    return rows, "".join(lst)


def largest_core():
    s = S("Largest Number 比较器", "a+b vs b+a")
    header(s, "最大拼接数 = 把数字当字符串排序, 比较规则不是字典序, 而是: a 排前面 ⇔ a+b > b+a (字符串拼接)",
           "为什么不能用普通字典序: 3 和 30")
    s.text(20, 80, "例: a = \"3\", b = \"30\"", 14, INK, weight=600)
    s.text(20, 110, "字典序: \"30\" > \"3\" (多一位更大)  → 30 排前面", 14)
    s.cell(380, 92, 40, 30, "30", "rm", False, 16)
    s.cell(424, 92, 40, 30, "3", "rm", False, 16)
    s.text(476, 112, "拼成 303", 16, "#712B13", weight=600)
    s.text(20, 156, "a+b vs b+a: \"3\"+\"30\" = 330 > \"30\"+\"3\" = 303", 14)
    s.cell(380, 138, 40, 30, "3", "new", False, 16)
    s.cell(424, 138, 40, 30, "30", "new", False, 16)
    s.text(476, 158, "拼成 330, 3 在前", 16, "#085041", weight=600)
    s.sep(184)
    s.text(20, 210, "为什么对 (exchange argument):", 14, INK, weight=600)
    s.text(20, 234, "取最优答案里任意相邻的两段 x y。如果 y+x > x+y, 把它们互换, 整个数里只有这两段的位置变了,", 12, SUB)
    s.text(20, 254, "前面和后面的部分完全不动, 数字变大 → 说明原来的不是最优。所以最优解里每对相邻的 x y 都满足 x+y ≥ y+x。", 12, SUB)
    s.text(20, 274, "这个关系是全序 (可传递), 所以按它排序出来的就是满足'所有相邻对都对'的唯一(并列)排列 → greedy 成立。", 12, SUB)
    s.sep(294)
    s.text(20, 318, "代码里: sorted(strs, key=cmp_to_key(lambda a, b: -1 if a + b > b + a else 1))", 14, INK)
    s.save("largest_number_core.svg", 336)


def largest_trace():
    nums = [3, 30, 34, 5, 9]
    rows, res = largest_rows(nums)
    s = S("Largest Number trace", "nums=[3,30,34,5,9] 逐个插入")
    header(s, "nums = [3, 30, 34, 5, 9] · 逐个插入已排好的 list: 放到第一个满足 x+e > e+x 的 e 前面",
           "x = 新数字, e = list 里的数字, 比较的是字符串拼接 (sorted 的结果和这个一样)")
    for x, t in ((20, "新数字 x"), (110, "比较 (x+e vs e+x)"), (430, "插入后的 list")):
        s.text(x, 76, t, 14, SUB)
    s.sep(86)
    y = 96
    for (x, cmps, pos, lst, _, final) in rows:
        s.text(20, y + 26, "x = %s" % x, 16)
        if cmps is None:
            s.text(110, y + 26, "list 为空, 直接放入", 14, SUB)
        else:
            for ci, (e, xe, ex, ok) in enumerate(cmps):
                yy = y + 18 + ci * 18
                if ok:
                    s.text(110, yy, "%s+%s = %s  >  %s+%s = %s → %s 排在 %s 前面" % (x, e, xe, e, x, ex, x, e), 12, "#085041")
                else:
                    s.text(110, yy, "%s+%s = %s  <  %s+%s = %s → %s 排在 %s 后面, 看下一个" % (x, e, xe, e, x, ex, x, e), 12, "#712B13")
            if pos == len(final) - 1 and not cmps[-1][3]:
                pass
        for k, v in enumerate(final):
            isnew = (cmps is None and k == 0) or (cmps is not None and k == pos)
            s.cell(430 + k * 44, y + 8, 40, 30, v, "new" if isnew else "other", isnew)
        y += max(52, 30 + 18 * (len(cmps) if cmps else 1))
        s.sep(y - 6)
    s.text(20, y + 14, "答案: \"\".join(list) = " + " + ".join('"%s"' % v for v in rows[-1][5]) + " = \"%s\"" % res, 16, "#085041", weight=600)
    s.legend(y + 44, [("new", "刚插入的"), ("other", "list 里已有的")])
    s.save("largest_number_trace.svg", y + 62)
    return rows, res


# ---------------------------------------------------------------- Partition Labels
def partition_rows(s_):
    last = {c: i for i, c in enumerate(s_)}
    start = end = 0
    rows, out = [], []
    for i, c in enumerate(s_):
        olde = end
        end = max(end, last[c])
        cut = i == end
        rows.append(dict(i=i, c=c, last=last[c], olde=olde, end=end, cut=cut, start=start))
        if cut:
            out.append(i - start + 1)
            start = i + 1
    return rows, out, last


def partition_core():
    s_ = "abacbdefe"
    rows, out, last = partition_rows(s_)
    s = S("Partition Labels invariant", "每段的右边界 = 段内字母 last occurrence 的最大值")
    header(s, "每个字母只能出现在一段里 → 一段里出现了字母 c, 这段至少要延伸到 c 的最后一次出现 (last[c])",
           "s = \"abacbdefe\"")
    x0 = 100
    for k, ch in enumerate(s_):
        s.text(x0 + k * 40 + 18, 76, "i=%d" % k, 12, SUB, "middle")
        s.cell(x0 + k * 40, 82, 36, 32, ch, "other")
    s.text(20, 104, "s", 14)
    for a_, b_ in [(0, 4), (5, 5), (6, 8)]:
        xa, xb = x0 + a_ * 40, x0 + b_ * 40 + 36
        s.path("M %d 124 L %d 132 L %d 132 L %d 124" % (xa, xa, xb, xb), "#0F6E56", 1.5)
        s.text((xa + xb) / 2, 152, "一段, 长度 %d" % (b_ - a_ + 1), 12, "#085041", "middle")
    s.text(20, 184, "last = " + str(last).replace("'", ""), 14)
    s.sep(200)
    s.text(20, 224, "a 最后出现在 2 → 包含 a 的段至少延伸到 i=2; 这段里的 b (last=4) 又把右边界推到 4; c (last=3) 没推远。", 12, SUB)
    s.text(20, 244, "end = max(扫过的字母的 last) 只会变大; 当 i == end 时, 段内所有字母都已经最后一次出现 → 可以安全切。", 12, SUB)
    s.text(20, 264, "切得越早越好 (greedy): 第一次满足 i == end 就切, 再往后拖只会把后面的字母拉进来、段更长, 段数不会更多。", 12, SUB)
    s.text(20, 300, "答案 = [5, 1, 3]", 16, "#085041", weight=600)
    s.save("partition_labels_core.svg", 318)


def partition_trace():
    s_ = "abacbdefe"
    rows, out, last = partition_rows(s_)
    s = S("Partition Labels trace", "s=abacbdefe")
    header(s, "s = \"abacbdefe\" · last = {a: 2, b: 4, c: 3, d: 5, e: 8, f: 7}",
           "每一步: end = max(end, last[s[i]]) → 若 i == end 就切一刀, 长度 = i - start + 1, start = i + 1。初始 start = 0, end = 0")
    for x, t in ((20, "i, s[i]"), (100, "end 更新"), (340, "i == end ?"), (550, "字符串 (金圈 = i)")):
        s.text(x, 76, t, 14, SUB)
    s.sep(86)
    y = 96
    cw = 12
    for r in rows:
        s.text(20, y + 24, "i=%d  %s" % (r["i"], r["c"]), 14)
        s.text(100, y + 24, "max(%d, last[%s]=%d) = %d" % (r["olde"], r["c"], r["last"], r["end"]), 14)
        if r["cut"]:
            s.text(340, y + 17, "%d == %d → 切" % (r["i"], r["end"]), 12, "#085041", weight=600)
            s.text(340, y + 34, "长度 %d - %d + 1 = %d" % (r["i"], r["start"], r["i"] - r["start"] + 1), 12, "#085041")
        else:
            s.text(340, y + 24, "%d ≠ %d → 不切" % (r["i"], r["end"]), 12, SUB)
        for k, ch in enumerate(s_):
            role = "empty"
            if r["start"] <= k <= r["i"]:
                role = "new" if r["cut"] else "other"
        # use 9 small cells
        for k, ch in enumerate(s_):
            role = "empty"
            if r["start"] <= k <= r["i"]:
                role = "new" if r["cut"] else "other"
            elif k < r["start"]:
                role = "other"
            s.cell(550 + k * 12, y + 8, 12, 26, "", role, False)
        s.e.append('<rect x="%s" y="%s" width="%s" height="%s" rx="4" fill="none" stroke="#EF9F27" stroke-width="2.5"/>'
                   % (550 + r["i"] * 12 - 2, y + 5, 16, 32))
        y += 46
        s.sep(y - 6)
    s.text(20, y + 14, "答案: 切在 i = 4, 5, 8 → 长度 5, 1, 3 = %s" % out, 16, "#085041", weight=600)
    s.legend(y + 44, [("new", "这一步切出的一段"), ("other", "已扫过 (段内 / 已切)"), ("empty", "没扫到")])
    s.save("partition_labels_trace.svg", y + 62)
    return rows, out


def build_all():
    greedy_core()
    jump_game_core()
    jump_game_trace()
    jump2_core()
    jump_game_ii_trace()
    gas_core()
    gas_trace()
    stock_core()
    stock_trace()
    candy_core()
    candy_trace()
    largest_core()
    largest_trace()
    partition_core()
    partition_trace()


if __name__ == "__main__":
    build_all()
