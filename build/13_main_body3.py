
# ===================================================================== SVG
import os
SVGDIR = os.path.join(ROOT_DIR, "docs", "svg", "13-backtracking")
os.makedirs(SVGDIR, exist_ok=True)


def save(s):
    with open(os.path.join(SVGDIR, s.name + ".svg"), "w", encoding="utf-8") as f:
        f.write(s.out())


# ---------- trace 右侧列 (每题一个) ----------
def res_line(s, x, y, e):
    if e["kind"] == "record":
        txt = "res += %s (共 %d)" % (e["val"], e["nres"])
        w = tw(txt, 12) + 12
        s.rect(x - 4, y - 10, w, 20, NEW)
        s.t(x + 2, y, txt, 12, NEW[2], "start", 500, maxw=176)
    else:
        s.t(x, y, "res 共 %d 个" % e["nres"], 12, SUB)


def ex_res(s, x, top, rh, e):
    res_line(s, x, top + rh / 2, e)


def mk_ex_perm(nums):
    def fn(s, x, top, rh, e):
        used = e["extra"]["used"]
        for j, u in enumerate(used):
            s.cell(x + j * 25, top + 6, 23, 20, str(nums[j]), NEW if u else OTH, size=12)
        s.t(x + 3 * 25 + 4, top + 16, "← used", 12, SUB)
        res_line(s, x, top + rh - 12, e)
    return fn


def mk_ex_remain(target):
    def fn(s, x, top, rh, e):
        if e["kind"] == "record":
            rem = 0
        else:
            rem = e["extra"]["remain"]
        p = e["path"]
        if e["kind"] == "prune":
            sm = "+".join(str(v) for v in p) or "0"
        else:
            sm = "+".join(str(v) for v in p) or "0"
        s.t(x, top + 13, "remain = %d - (%s) = %d" % (target, sm, target - sum(p)), 12, INK,
            "start", 400, maxw=176)
        res_line(s, x, top + rh - 12, e)
    return fn


def ex_parens(s, x, top, rh, e):
    o, c = e["extra"]["o"], e["extra"]["c"]
    s.t(x, top + 13, "open_ = %d, close = %d" % (o, c), 12, INK)
    res_line(s, x, top + rh - 12, e)


def mk_ex_letters(n):
    def fn(s, x, top, rh, e):
        s.t(x, top + 13, "idx = %d / %d" % (e["extra"]["idx"], n), 12, INK)
        res_line(s, x, top + rh - 12, e)
    return fn


def ex_ws(s, x, top, rh, e):
    g = e["extra"]["grid"]
    cs = 18
    gy = top + (rh - cs * len(g)) / 2
    for r, row in enumerate(g):
        for c, ch in enumerate(row):
            s.cell(x + c * (cs + 2), gy + r * (cs + 2) - (r * 0), cs, cs, ch,
                   NEW if ch == "#" else OTH, size=12)
    nh = sum(ch == "#" for row in g for ch in row)
    s.t(x + len(g[0]) * (cs + 2) + 8, top + rh / 2 - 7, "# 个数 = %d" % nh, 12, INK)
    s.t(x + len(g[0]) * (cs + 2) + 8, top + rh / 2 + 9, "len(path) = %d" % len(e["path"]), 12, INK)


def ex_nq(s, x, top, rh, e):
    ex = e["extra"]
    fmt = lambda a: "{" + ", ".join(str(v) for v in a) + "}"
    s.t(x, top + 9, "cols = " + fmt(ex["cols"]), 12, INK)
    s.t(x, top + 24, "diag = " + fmt(ex["diag"]), 12, INK)
    s.t(x, top + 39, "anti = " + fmt(ex["anti"]), 12, INK)
    if e["kind"] == "record":
        s.rect(x + 108, top + 14, 66, 20, NEW)
        s.t(x + 113, top + 24, "res 共 %d 个" % e["nres"], 12, NEW[2], "start", 500)


# ---------- core: decision tree ----------
def core_tree(name, title, desc, lines, R, bottom, legend_extra=None, level_h=66,
              label_size=13):
    y0 = 18 + 20 * len(lines) + 34
    # 先画到一个临时 Svg 拿到 bottom 高度
    tmp = Svg(name, 100, title, desc)
    b = draw_tree(tmp, R.root, y0, level_h=level_h, label_size=label_size)
    H = int(b + 14 + 22 * len(bottom) + 40)
    s = Svg(name, H, title, desc)
    for i, ln in enumerate(lines):
        s.t(40, 18 + i * 20, ln, 12, SUB)
    draw_tree(s, R.root, y0, level_h=level_h, label_size=label_size)
    y = b + 6
    for i, ln in enumerate(bottom):
        s.t(40, y + 10 + i * 22, ln, 14 if i == 0 else 12, INK if i == 0 else SUB,
            "start", 500 if i == 0 else 400)
    y += 22 * len(bottom) + 18
    items = [(NEW, False, "收集到的答案"), (OTH, False, "普通节点 (path)")]
    if R.nprune:
        items.append((REM, True, "被剪枝的分支 (写原因)"))
    if legend_extra:
        items += legend_extra
    s.legend(y, items)
    return s


# ---------- 第 0 节 core ----------
def svg_core0():
    R, _ = rec_subsets([1, 2])
    s = Svg("first_principles_core", 520, "Backtracking = decision tree 上的 DFS",
            "nums=[1,2] 的 decision tree, 以及 DFS 过程中 path 这个共用 list 的 push/pop 时间线。")
    s.t(40, 18, "nums = [1, 2] · 节点 = 一个 path 状态 · 边 = 一次选择 · DFS 往下走 = push, 往回走 = pop", 12, SUB)
    s.t(40, 38, "左: decision tree (绿箭头 push, 红虚线 pop) · 右: 同一个 path list 随时间 t 的变化", 12, SUB)
    nodes = {"": (150, 100), "1": (84, 176), "2": (216, 176), "12": (84, 252)}
    labels = {"": "[]", "1": "[1]", "2": "[2]", "12": "[1,2]"}
    for k, (cx, cy) in nodes.items():
        pass
    # 边 (down 绿实线 / up 红虚线), 偏移 5px 并排
    def edge(a, b, dx):
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        s.line(x1 - dx, y1 + 13, x2 - dx, y2 - 13, NEW[1], None, 1.5, "arrowG")
        s.line(x2 + dx, y2 - 13, x1 + dx, y1 + 13, ARROW_RED, "4 3", 1.5, "arrowR")
    edge("", "1", 5)
    edge("", "2", 5)
    edge("1", "12", 5)
    for k, (cx, cy) in nodes.items():
        role = NEW
        w = 54 if k == "12" else 44
        s.node(cx, cy, w, 26, labels[k], role)
    # 边上的 t 标签
    s.t(104, 128, "t1 push 1", 12, NEW[2], "end", 500)
    s.t(122, 150, "t4 pop 1", 12, REM[2], "start", 500)
    s.t(206, 128, "t5 push 2", 12, NEW[2], "start", 500)
    s.t(196, 150, "t6 pop 2", 12, REM[2], "start", 500)
    s.t(98, 202, "t2 push 2", 12, NEW[2], "start", 500)
    s.t(98, 224, "t3 pop 2", 12, REM[2], "start", 500)
    s.t(40, 296, "path 上每个节点都已是答案 (绿): 节点数 = 4 = 2^2", 12, SUB)
    # 右: 时间线
    tx = 340
    s.t(tx, 62, "t", 12, SUB)
    s.t(tx + 26, 62, "动作", 12, SUB)
    s.t(tx + 90, 62, "被撤销", 12, SUB)
    s.t(tx + 146, 62, "path (同一个 list)", 12, SUB)
    s.sep(72, tx, 640)
    ev = [e for e in R.ev if e["kind"] in ("push", "pop")]
    rows = [dict(kind="init", val="", path=[])] + ev
    y = 80
    cw = 30
    for t, e in enumerate(rows):
        s.t(tx, y + 17, "t%d" % t, 12, SUB)
        k = e["kind"]
        if k == "init":
            s.t(tx + 26, y + 17, "开始", 14, INK, "start", 500)
        else:
            s.t(tx + 26, y + 17, "%s %s" % (k, e["val"]), 14,
                NEW[2] if k == "push" else REM[2], "start", 500)
        p = e["path"]
        px = tx + 146
        for j, v in enumerate(p):
            s.cell(px + j * (cw + 2), y + 3, cw, 28, str(v), NEW if (k == "push" and j == len(p) - 1) else OTH)
        if p:
            s.ring(px + (len(p) - 1) * (cw + 2), y + 3, cw, 28)
        else:
            s.t(px, y + 17, "[ ] 空", 12, SUB)
        if k == "pop":
            s.cell(tx + 90, y + 3, cw, 28, str(e["val"]), REM, True)
            sx = px + len(p) * (cw + 2)
            s.path("M%g %g L%g %g L%g %g L%g %g" % (sx + cw / 2, y + 3, sx + cw / 2, y - 1,
                                                  tx + 90 + cw / 2, y - 1, tx + 90 + cw / 2, y + 2),
                   ARROW_RED, "4 3", 1.5, "arrowR")
        y += 36
        s.sep(y - 2, tx, 640)
    # 底部: 三件事 + 为什么要 pop
    yb = 352
    s.t(40, yb, "backtracking 的三件事", 14, INK, "start", 500)
    s.t(40, yb + 24, "path = 已做的选择 (从 root 走到当前节点的路), 一个共用的 list · 此刻 t2: path = [1, 2]", 12, SUB)
    s.t(40, yb + 44, "choices = 还能选什么 (nums[start:]), 每个选择是一条往下的边 · t2: start = 2, 没有可选 => 往回走", 12, SUB)
    s.t(40, yb + 64, "结束条件 = 什么时候收集答案 / 不能再往下 · 这里: 进入每个节点就收集 path[:]", 12, SUB)
    s.t(40, yb + 90, "为什么必须 pop", 14, INK, "start", 500)
    s.t(40, yb + 114, "path 只有一个 list。t3、t4 如果不 pop, t5 push 2 之后 path = [1, 2, 2], 而不是 [2]。", 12, SUB)
    s.t(40, yb + 134, "收集时也要 copy: res.append(path) 存的是同一个 list, 最后 res 里全是 [] (t6 之后 path 为空)。", 12, SUB)
    s.t(40, yb + 160, "complexity = decision tree 的节点数 × 每个节点的工作: 4 个节点 × copy path", 14, INK, "start", 500)
    s.legend(yb + 192, [(NEW, False, "push / 新选择 / 答案"), (REM, True, "pop 撤销")])
    s.rect(330, yb + 185, 16, 14, OTH, fill="none", stroke=RING, sw=2.5)
    s.t(352, yb + 192, "path 栈顶", 12, SUB)
    s.h = yb + 192 + 28
    return s


def svg_ws_core(board, word):
    R, ok = rec_wsearch(board, word)
    grids = [("进入 dfs 前", [r[:] for r in board], None),
             ("t2: 走了 A→B", R.ev[1]["extra"]["grid"], (1, 0)),
             ("t7: pop B 之后", R.ev[6]["extra"]["grid"], (1, 0)),
             ("t13: 找到 ABAD", R.ev[12]["extra"]["grid"], (1, 2))]
    caps = [["原始 board", "A B A / B B D"],
            ["(0,0) (1,0) 变成 #", "# 个数 = len(path) = 2"],
            ["(1,0) 变回 B", "(0,0) 仍是 # (A 还在 path)"],
            ["4 个 # = ABAD", "return True 之前"]]
    s = Svg("word_search_core", 360, "Word Search: 用 board 本身当 used[]",
            "同一个 board 在 DFS 不同时刻的四个快照: 标记 # 和恢复。")
    s.t(40, 18, "board = A B A / B B D · word = ABAD · 做选择 = 把格子改成 #, 撤销 = 改回原字母", 12, SUB)
    s.t(40, 38, "# 的位置 = path 走过的格子, 所以 \"同一格不能用两次\" 不需要额外的 used 或 set", 12, SUB)
    cs = 36
    for gi, (ttl, g, cur) in enumerate(grids):
        gx = 40 + gi * 150
        s.t(gx, 66, ttl, 14, INK, "start", 500)
        for r, row in enumerate(g):
            for c, ch in enumerate(row):
                s.cell(gx + c * (cs + 2), 82 + r * (cs + 2), cs, cs, ch,
                       NEW if ch == "#" else OTH)
        if cur and g[cur[0]][cur[1]] == "#":
            s.ring(gx + cur[1] * (cs + 2), 82 + cur[0] * (cs + 2), cs, cs)
        if gi == 2:
            s.cell(gx + 0 * (cs + 2), 82 + 1 * (cs + 2), cs, cs, "B", OTH)
            s.ring(gx + 0 * (cs + 2), 82 + 1 * (cs + 2), cs, cs)
        for j, ln in enumerate(caps[gi]):
            s.t(gx, 82 + 2 * (cs + 2) + 14 + j * 16, ln, 12, SUB, maxw=140)
    y = 82 + 2 * (cs + 2) + 66
    s.t(40, y, "三步写法 (一定成对出现)", 14, INK, "start", 500)
    s.t(40, y + 24, "1. board[r][c] = \"#\"        做选择: 当前格子标记为已用", 12, SUB)
    s.t(40, y + 44, "2. found = dfs(上) or dfs(下) or dfs(左) or dfs(右)        递归: 往 4 个方向走", 12, SUB)
    s.t(40, y + 64, "3. board[r][c] = word[k]    撤销: 改回原字母 (找到了也要改回, 否则调用者的 board 被破坏)", 12, SUB)
    s.t(40, y + 92, "忘了第 3 步: (1,0) 永远是 #, 之后从别的起点或别的路线都经过不了它, 会漏掉答案", 12, SUB)
    s.legend(y + 124, [(NEW, False, "# = 在 path 里 (已用)"), (OTH, False, "原字母")])
    s.rect(330, y + 117, 16, 14, OTH, fill="none", stroke=RING, sw=2.5)
    s.t(352, y + 124, "当前 / 刚恢复的格子", 12, SUB)
    s.h = y + 124 + 28
    return s


def svg_nq_core():
    s = Svg("n_queens_core", 470, "N-Queens: 三个 set 把 \"是否冲突\" 变成 O(1)",
            "n=4, 前两行已放皇后, 第 2 行每一列的检查过程。")
    s.t(40, 18, "n = 4 · 已放: (0,1) 和 (1,3) · 现在要放第 r = 2 行 · 每行恰好一个皇后, 所以 path[r] = 列", 12, SUB)
    s.t(40, 38, "同一列: c 相同 · 同一条 \\ 对角线: r - c 相同 · 同一条 / 对角线: r + c 相同", 12, SUB)
    cs, bx, by = 44, 40, 62
    queens = [(0, 1), (1, 3)]
    # 先画红色虚线: 皇后的攻击线 (列 + 两条对角线), 画在格子下面
    for r in range(4):
        for c in range(4):
            s.rect(bx + c * cs, by + r * cs, cs, cs, OTH, fill="#FFFFFF" if (r + c) % 2 == 0 else "#F1EFE8",
                   stroke="#B4B2A9", sw=1, rx=0)
    def center(r, c):
        return bx + c * cs + cs / 2, by + r * cs + cs / 2
    for (qr, qc) in queens:
        # 列
        x1, y1 = center(0, qc); x2, y2 = center(3, qc)
        s.line(x1, y1, x2, y2, ARROW_RED, "4 3", 1.2)
        # \ 对角线 r-c 相同
        pts = [(r, r - (qr - qc)) for r in range(4) if 0 <= r - (qr - qc) < 4]
        (ar, ac), (br, bc) = pts[0], pts[-1]
        x1, y1 = center(ar, ac); x2, y2 = center(br, bc)
        s.line(x1, y1, x2, y2, ARROW_RED, "4 3", 1.2)
        # / 对角线 r+c 相同
        pts = [(r, (qr + qc) - r) for r in range(4) if 0 <= (qr + qc) - r < 4]
        (ar, ac), (br, bc) = pts[0], pts[-1]
        x1, y1 = center(ar, ac); x2, y2 = center(br, bc)
        s.line(x1, y1, x2, y2, ARROW_RED, "4 3", 1.2)
    for (qr, qc) in queens:
        cx, cy = center(qr, qc)
        s.circ(cx, cy, 15, NEW, False, 1.5)
        s.t(cx, cy, "Q", 14, NEW[2], "middle", 500)
    # 第 2 行的四个候选: 标记
    marks = {0: ("ok", "OK"), 1: ("x", "x"), 2: ("x", "x"), 3: ("x", "x")}
    for c, (k, txt) in marks.items():
        cx, cy = center(2, c)
        if k == "ok":
            s.ring(bx + c * cs + 3, by + 2 * cs + 3, cs - 6, cs - 6)
            s.t(cx, cy, "OK", 14, NEW[2], "middle", 500)
        else:
            s.rect(bx + c * cs + 5, by + 2 * cs + 5, cs - 10, cs - 10, REM, True)
            s.t(cx, cy, "x", 14, REM[2], "middle", 500)
    for c in range(4):
        s.t(bx + c * cs + cs / 2, by - 8, "c=%d" % c, 12, SUB, "middle")
    for r in range(4):
        s.t(bx - 6, by + r * cs + cs / 2, "r=%d" % r, 12, SUB, "end")
    # 右: 三个 set + 第 2 行逐列检查
    rx = 262
    s.t(rx, 66, "三个 set (已放 (0,1) 和 (1,3))", 14, INK, "start", 500)
    s.t(rx, 90, "cols = {1, 3}", 14, INK, "start", 500)
    s.t(rx + 130, 90, "= 已占用的列", 12, SUB)
    s.t(rx, 112, "diag = {-1, -2}", 14, INK, "start", 500)
    s.t(rx + 130, 112, "= r - c: 0-1, 1-3", 12, SUB)
    s.t(rx, 134, "anti = {1, 4}", 14, INK, "start", 500)
    s.t(rx + 130, 134, "= r + c: 0+1, 1+3", 12, SUB)
    s.sep(148, rx, 640)
    s.t(rx, 164, "第 r = 2 行, 逐列检查 (只查 3 次 set, O(1))", 14, INK, "start", 500)
    rows = [
        (NEW, "c=0: 0 不在 cols, 2-0=2 不在 diag, 2+0=2 不在 anti", "放"),
        (REM, "c=1: 1 在 cols => 剪枝", ""),
        (REM, "c=2: 2+2=4 在 anti => 剪枝", ""),
        (REM, "c=3: 3 在 cols => 剪枝", ""),
    ]
    for i, (role, txt, _) in enumerate(rows):
        yy = 190 + i * 24
        s.rect(rx, yy - 9, 14, 14, role, role is REM)
        s.t(rx + 22, yy, txt, 12, role[2] if role is REM else INK, "start", 400, maxw=360)
    s.t(rx, 296, "做选择: 三个 set 各 add 一个值 + path.append(c)", 12, SUB)
    s.t(rx, 316, "撤销: 三个 set 各 remove 同一个值 + path.pop()", 12, SUB)
    s.t(rx, 336, "漏掉一个 remove => 后面的分支会被 \"幽灵皇后\" 误剪", 12, SUB)
    s.t(40, 270, "红色虚线 = 已有皇后的攻击线 (列 / 两条对角线)", 12, SUB)
    s.t(40, 290, "第 2 行只有 c=0 不被攻击 => 只剩一个选择", 12, SUB)
    s.t(40, 380, "没有 set 的话: 每放一个皇后要扫已有皇后 O(n) 次 => 总共 O(n) × 节点数", 14, INK, "start", 500)
    s.t(40, 404, "有了 set: 每次检查 O(1), 同一个 decision tree 少一个 n 的因子", 12, SUB)
    s.legend(436, [(NEW, False, "皇后 / 可以放"), (REM, True, "被攻击 => 剪枝")])
    return s


# ---------- 把所有图生成出来 ----------
def build_svgs():
    out = {}
    s = svg_core0(); save(s); out["core0"] = s

    # 1 Subsets
    R, res = rec_subsets([1, 2, 3])
    s = core_tree("subsets_core", "Subsets 的 decision tree",
                  "nums=[1,2,3], 每个节点都是答案, 共 8 个。",
                  ["nums = [1, 2, 3] · 节点 = path · 子节点 = path + [nums[i]], i 只能取 start 之后的",
                   "每个节点都收集 => 没有剪枝, 也没有 \"废节点\""],
                  R, ["节点数 = 2^3 = 8 => 8 个答案 (每个节点收集一次)",
                      "[2,1] 不会出现: 选了 2 之后 start = 2, 只能再选 3"])
    save(s)
    ex = ex_res
    s = trace_svg("subsets_trace", "Subsets 的 path 变化",
                  "nums=[1,2,3] 前 13 步 push/pop。",
                  ["nums = [1, 2, 3] · 每个节点: 先收集 path[:], 再逐个 push → 递归 → pop",
                   "'被撤销' 列 = 刚 pop 掉的元素 (虚线扔到左边); 原因写在左边动作下面"],
                  R.ev, 13, "res (收集到的答案)", ex,
                  ["最终 res = %s" % str(res).replace(" ", ""),
                   "共 %d 个 = 2^3; 前 13 步已经走完 [1] 整棵子树, 第 14 步 push 2 开始 [2] 子树" % len(res)])
    save(s)

    # 2 Permutations
    R, res = rec_permute([1, 2, 3])
    s = core_tree("permutations_core", "Permutations 的 decision tree",
                  "nums=[1,2,3], 6 个叶子。",
                  ["nums = [1, 2, 3] · 每层都从头看 3 个数, used[i] 为真的跳过 (没有画出)",
                   "每层的 choices = 还没用的数: 第 1 层 3 个, 第 2 层 2 个, 第 3 层 1 个"],
                  R, ["节点数 = 1 + 3 + 3×2 + 3×2×1 = 16 · 叶子 = 3! = 6 个答案",
                      "只有叶子是答案 (len(path) == 3); 中间节点只是 partial path"])
    save(s)
    s = trace_svg("permutations_trace", "Permutations 的 path / used 变化",
                  "nums=[1,2,3] 前 12 步。",
                  ["nums = [1, 2, 3] · push: used[i] = True 且 path.append · pop: 两个一起还原",
                   "'used' 列: 绿色 = 在 path 里的数, 灰色 = 还能选的数"],
                  R.ev, 12, "used / res", mk_ex_perm([1, 2, 3]),
                  ["最终 res = %s" % str(res).replace(" ", ""),
                   "共 %d 个 = 3!; 第 6、11、12 步 pop 之后 used 变回灰色, 兄弟分支才能选它" % len(res)])
    save(s)

    # 3 Combination Sum
    R, res = rec_comb([2, 3, 5], 6)
    s = core_tree("combination_sum_core", "Combination Sum 的 decision tree",
                  "candidates=[2,3,5], target=6。",
                  ["candidates = [2, 3, 5] · target = 6 · 子节点 = 从 candidates[start:] 里选一个, 可以和父节点同值",
                   "剪枝: c > remain => break (排序后后面更大, 都不行)"],
                  R, ["答案 %s · 节点数 %d (含 %d 个被剪掉的)" % (str(res).replace(" ", ""), count_nodes(R.root), R.nprune),
                      "dfs(i, ...) 传 i: [2,2] 的下一层仍可选 2; 如果传 i+1, 每个数只能用一次, [2,2,2] 和 [3,3] 都出不来"])
    save(s)
    s = trace_svg("combination_sum_trace", "Combination Sum 的 path / remain 变化",
                  "candidates=[2,3,5], target=6 前 14 步。",
                  ["candidates = [2, 3, 5] · target = 6 · remain = target - sum(path)",
                   "每次 push c: remain 减 c · c > remain 就剪枝 (红色虚线格子 = 想选但不能选)"],
                  R.ev, 14, "remain / res", mk_ex_remain(6),
                  ["最终 res = %s" % str(res).replace(" ", ""),
                   "[3,3] 里的第二个 3 来自 dfs(i, ...): 同一个下标可以重复选"])
    save(s)

    # 4 Combination Sum II
    R, res = rec_comb2([1, 2, 2, 3], 5)
    s = core_tree("combination_sum_ii_core", "Combination Sum II 的 decision tree",
                  "candidates=[1,2,2,3], target=5, 同层去重。",
                  ["candidates 排序后 = [1, 2, 2, 3] · target = 5 · 每个数最多用一次 => dfs(i+1, ...)",
                   "同一层第二个 2 (i > start 且 与前一个相等) 的子树和第一个 2 完全相同 => 剪掉"],
                  R, ["答案 %s · 节点数 %d (含 %d 个被剪掉的)" % (str(res).replace(" ", ""), count_nodes(R.root), R.nprune),
                      "[1,2,2] 里两个 2 都留着: 第二个 2 在下一层 (i == start), 不是同一层"])
    save(s)
    s = trace_svg("combination_sum_ii_trace", "Combination Sum II 的同层去重",
                  "candidates=[1,2,2,3], target=5 前 12 步。",
                  ["candidates = [1, 2, 2, 3] (下标 0..3) · target = 5 · 去重条件: i > start 且 c == candidates[i-1]",
                   "第 8 步: 在 path=[1] 这一层, i=2 的 2 和 i=1 的 2 相同, 子树重复 => 剪枝"],
                  R.ev, 12, "remain / res", mk_ex_remain(5),
                  ["最终 res = %s" % str(res).replace(" ", ""),
                   "第 3 步 [1,2,2] 允许: 那是下一层, i=2 == start=2, 不触发去重条件"])
    save(s)

    # 5 Generate Parentheses
    R, res = rec_parens(2)
    s = core_tree("generate_parentheses_core", "Generate Parentheses 的 decision tree",
                  "n=2, 两个剪枝条件。",
                  ["n = 2 · 每个节点最多两个选择: 加 \"(\" (需要 open_ < n) 或 加 \")\" (需要 close < open_)",
                   "红色虚线 = 被两个条件挡住的选择; 剩下的每个叶子都合法"],
                  R, ["答案 %s · 节点数 %d (含 %d 个被剪掉的)" % (str(res).replace(" ", ""), count_nodes(R.root), R.nprune),
                      "没有剪枝要枚举 2^4 = 16 个串再检查; 剪枝后只展开了 %d 个节点, 叶子全是答案" % (count_nodes(R.root) - R.nprune)])
    save(s)
    s = trace_svg("generate_parentheses_trace", "Generate Parentheses 的 path 变化",
                  "n=2 前 12 步。",
                  ["n = 2 · push \"(\" 要 open_ < n · push \")\" 要 close < open_ · path 的长度到 2n = 4 就收集",
                   "红色虚线格子 = 想加但被条件挡住 (原因写在左边)"],
                  R.ev, 12, "open_ / close / res", ex_parens,
                  ["最终 res = %s" % str(res).replace(" ", ""),
                   "n = 3 时共 5 个答案 (Catalan 数: 1, 2, 5, 14, ...)"])
    save(s)

    # 6 Letter Combinations
    R, res = rec_letters("23")
    s = core_tree("letter_combinations_core", "Letter Combinations 的 decision tree",
                  "digits=23, 3×3=9 个叶子。",
                  ["digits = \"23\" · 第 1 层从 \"abc\" 选一个, 第 2 层从 \"def\" 选一个",
                   "每层的 choices 由层数 idx 决定, 和 path 里选了什么无关 => 不需要 start / used"],
                  R, ["节点数 = 1 + 3 + 3×3 = 13 · 叶子 = 3 × 3 = 9 个答案",
                      "没有剪枝: 这是纯粹的笛卡尔积, backtracking 只是把 \"层数不固定的嵌套 for\" 写成递归"])
    save(s)
    s = trace_svg("letter_combinations_trace", "Letter Combinations 的 path 变化",
                  "digits=23 前 12 步。",
                  ["digits = \"23\" · idx = 正在决定第几个数字 · 到 idx == 2 收集",
                   "每个叶子 push 一次、收集一次、pop 一次; 第 11 步 pop a, 回到空 path 试 b"],
                  R.ev, 12, "idx / res", mk_ex_letters(2),
                  ["最终 res = %s" % str(res).replace(" ", ""),
                   "共 %d 个 = 3 × 3" % len(res)])
    save(s)

    # 7 Word Search
    board = [list("ABA"), list("BBD")]
    word = "ABAD"
    s = svg_ws_core(board, word); save(s)
    R, ok = rec_wsearch(board, word)
    s = trace_svg("word_search_trace", "Word Search 的 path / board 变化",
                  "board=ABA/BBD, word=ABAD 全部 18 步。",
                  ["board = A B A / B B D · word = ABAD · 方向顺序: 下 上 右 左 · 从 (0,0) 开始",
                   "push = 标记成 # · pop = 恢复原字母 · 红色虚线格子 = 这一步走不通 (越界 / 字母不对 / 已用)"],
                  R.ev, 18, "board (# = 已用) / 不变量", ex_ws,
                  ["结果 exist = %s · 路径 (0,0) A → (0,1) B → (0,2) A → (1,2) D" % ok,
                   "第 2-7 步: 先走下 (1,0) 的 B, 四个方向都不行, pop 恢复; 第 9 步改走右 (0,1)"],
                  row_h=42, cw=34)
    save(s)

    # 8 N-Queens
    s = svg_nq_core(); save(s)
    R, res = rec_nqueens(4)
    s = trace_svg("n_queens_trace", "N-Queens 的 path / 三个 set 变化",
                  "n=4 前 17 步。",
                  ["n = 4 · path[r] = 第 r 行的列 · 每步先查 3 个 set, 冲突就剪枝, 不冲突就 push 并同时 add 到 3 个 set",
                   "红色虚线格子 = 想放的列被挡住 (原因写在左边); pop 时三个 set 一起还原"],
                  R.ev, 17, "三个 set", ex_nq,
                  ["最终 n=4 共 %d 个解: %s" % (len(res), str(res).replace(" ", "")),
                   "[0,2] 在第 2 行无处可放, [0,3,1] 在第 3 行无处可放 (死路, 回溯); 全树共 %d 个事件, 解在第 31、48 步" % len(R.ev)],
                  row_h=48, path_title="path (path[r] = 列)")
    save(s)
    return out
