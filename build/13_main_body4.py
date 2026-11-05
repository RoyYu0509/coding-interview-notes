
# ===================================================================== HTML
def build_doc():
    nq8 = rec_nqueens(8)[0]
    nq8_nodes = nq8.npush + 1
    nq4 = rec_nqueens(4)[0]
    nq4_nodes = nq4.npush + 1
    doc = d.Doc("13 · Backtracking")
    doc.main("主线: backtracking = 在 decision tree 上做 DFS。节点 = 一个 partial path, 边 = 一次选择。"
             "做选择 → 递归 → 撤销选择; 一定走不通的分支, 进去之前就剪掉。")
    doc.main("概念链: Subsets (模板) → Permutations (+ used) → Combination Sum (+ 重复选, + remain 剪枝) → "
             "Combination Sum II (+ 同层去重) → Generate Parentheses (约束剪枝) → "
             "Letter Combinations (每层候选不同) → Word Search (grid, 原地标记) → N-Queens (多个约束 set)")

    # ---------------------------------------------------------------- 0
    doc.h2("0. 第一性原理: 暴力在浪费什么, backtracking 怎么消掉")
    doc.p("题目要的是 <b>所有</b> 组合 / 排列 / 路径。答案个数本身就是指数级, 所以输出大小就是 time complexity 的下限。"
          "能优化的只有一件事: <b>不要展开一定没有答案的分支</b>。")
    doc.p("最直接的暴力是 n 层嵌套 <code>for</code>, 每层选一个, 最后检查合法。它有两个问题。")
    doc.p("① n 是 input, 嵌套层数写不出来。解法: 一层递归 = 一层 <code>for</code>, 递归深度 = 层数。")
    doc.p("② 先生成完整候选, 再检查。以 3 对括号为例: 一共 2^6 = 64 个串, 合法的只有 5 个。"
          "前缀是 <code>)</code> 的串一开始就注定不合法, 却还要把后面 5 位全展开 (2^5 = 32 个)。"
          "backtracking 在每一步选择之前就检查约束, 一旦违反就不进这个分支。")
    doc.p("把所有选择画成树就是 <b>decision tree</b>: 根 = 什么都没选; 每个节点 = 已做的选择 (path); "
          "每条边 = 一个选择。backtracking 就是在这棵树上做 DFS: 往下走 = 做选择, 往回走 = 撤销选择。")
    doc.svg("13-backtracking/first_principles_core.svg",
            "图 0: nums=[1,2] 的 decision tree (左) 和 path 这个共用 list 在 DFS 过程中随时间的 push/pop (右)。"
            "t3、t4 的 pop 保证了 t5 从 [] 开始, 而不是从 [1,2] 开始。")
    doc.h3("三件事")
    doc.p("<b>path</b>: 已经做过的选择, 一个共用的 list。<b>choices</b>: 此刻还能选什么 "
          "(每个选择是一条往下的边)。<b>结束条件</b>: path 什么时候是一个完整答案。")
    doc.h3("为什么必须撤销")
    doc.p("path 只有一个 list, 递归的每一层都在改同一个对象。回到上一层之后, 兄弟分支要看到的是 "
          "<b>做选择之前</b> 的 path。不 pop, 兄弟分支就带着上一个分支的选择 (图 0: path 会变成 [1,2,2])。"
          "收集答案要 <code>path[:]</code> 复制一份, 否则 <code>res</code> 里存的全是同一个 list 的引用, 最后都变成空 list。")
    doc.p("另一种写法是每次传新 list (<code>path + [c]</code>), 不用撤销, 代价是每个节点多 O(n) 的复制。面试默认写 mutate + undo。")
    doc.h3("通用模板")
    doc.code(SRC["template"])
    doc.h3("Complexity 怎么算")
    doc.p("time = decision tree 的节点数 × 每个节点的工作 (通常是 <code>path[:]</code> 的 O(n))。"
          "space = 树的深度 (递归栈 + path), 不算输出。"
          "剪枝的价值就是让节点数从 \"所有候选\" 降到 \"接近答案数\"。")
    doc.note("backtracking = 树上 DFS。path 是共用 list: 做选择 push, 回来 pop; 收集要 copy。complexity 数节点。")

    # ---------------------------------------------------------------- 1 Subsets
    doc.h2("1. Subsets: 每个节点都是答案, start index 防重复")
    doc.p("题: <code>nums = [1,2,3]</code> (无重复), 返回所有子集, 共 8 个: "
          "<code>[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]</code>。")
    doc.p("Brute force: 枚举 bitmask 0 … 2^n−1, 每个 mask 扫 n 位, O(n·2^n)。这其实已经和输出大小一样大, 没有浪费; "
          "但 bitmask 一遇到 \"和等于 target\" \"去重\" 这类约束就没法剪枝。所以先用这题把 backtracking 的骨架学会。")
    doc.p("关键观察: 子集 = 每个元素选 / 不选。为了不生成 <code>[1,2]</code> 和 <code>[2,1]</code> 两个相同的子集, "
          "规定只能往后选: 选了 <code>nums[i]</code> 之后, 下一层从 <code>i+1</code> 开始。这个 <code>start</code> 就是 choices。")
    doc.svg("13-backtracking/subsets_core.svg",
            "图 1a: decision tree。每个节点都是一个答案 (绿); 子节点只能加 start 之后的元素。8 个节点 = 8 个子集。")
    doc.svg("13-backtracking/subsets_trace.svg",
            "图 1b: 前 13 步。进入节点先收集; push 往下, pop 往回, pop 掉的元素虚线扔到左边。")
    doc.code(SRC["subsets"])
    doc.p("等价的 \"选 / 不选\" 写法 (二叉树, 只有叶子是答案), 适合元素有额外状态的题:")
    doc.code(SRC["subsets2"])
    doc.p("Time O(n·2^n): 2^n 个节点, 每个节点 <code>path[:]</code> 复制 O(n)。Space O(n): 递归深度 + path (不算输出)。")
    doc.note("子集 / 组合: 每层只往后选 (<code>range(start, n)</code>, 递归传 <code>i+1</code>); 每个节点都可能是答案。")

    # ---------------------------------------------------------------- 2 Permutations
    doc.h2("2. Permutations: 每层从头看, 用 used[] 跳过已选")
    doc.p("题: <code>nums = [1,2,3]</code>, 返回所有排列, 共 3! = 6 个。")
    doc.p("Brute force: 每个位置从 n 个数里选, 共 n^n = 27 个序列, 再过滤出没有重复数字的, O(n^n · n)。"
          "浪费: 第 2 层又选了 path 里已有的数, 整棵子树都是废的。")
    doc.p("关键观察: 相比 Subsets, 顺序有意义 (<code>[1,2]</code> 和 <code>[2,1]</code> 是两个答案), "
          "所以不能再 \"只往后选\", 每层都要从头看。改两处: <code>range(start, n)</code> → <code>range(n)</code>; "
          "加 <code>used[i]</code> 跳过 path 里已有的数。只有叶子 (<code>len(path) == n</code>) 是答案。")
    doc.svg("13-backtracking/permutations_core.svg",
            "图 2a: decision tree。第 1 层 3 个选择, 第 2 层 2 个, 第 3 层 1 个; 叶子 3! = 6 个。")
    doc.svg("13-backtracking/permutations_trace.svg",
            "图 2b: path 和 used[] 同步变化。push 时 used 变绿, pop 时 used 变回灰色。")
    doc.code(SRC["permute"])
    doc.p("Time O(n·n!): 叶子 n! 个, 节点总数约 e·n!, 每个叶子复制 O(n)。Space O(n): path + used + 递归栈。")
    doc.note("排列: 每层 <code>range(n)</code> + <code>used[]</code>; 做选择改两个状态 (path, used), 撤销也要改两个。")

    # ---------------------------------------------------------------- 3 Combination Sum
    doc.h2("3. Combination Sum: 可重复选 => 递归传 i, 不是 i+1")
    doc.p("题: <code>candidates = [2,3,5]</code>, <code>target = 6</code>, 每个数可以用任意多次, 返回和为 target 的所有组合 "
          "(顺序不同算同一个)。答案: <code>[[2,2,2],[3,3]]</code>。")
    doc.p("Brute force: 每个数枚举用 0 … target/c 次, 共 (6/2+1)·(6/3+1)·(6/5+1) = 4·3·2 = 24 种, 每种求和检查。"
          "浪费: 2 已经用了 4 次 (和 8 &gt; 6), 却还要继续枚举 3 和 5 的次数。")
    doc.p("关键观察: 这是 Subsets 加两处改动。① 同一个数能再选: 递归传 <code>i</code> "
          "(下一层仍可选 <code>candidates[i]</code>), 而不是 <code>i+1</code>; "
          "<code>start</code> 仍然保证不会出现 <code>[3,2]</code>。② 剪枝: 维护 <code>remain = target − sum(path)</code>, "
          "排序后一旦 <code>c &gt; remain</code>, 后面更大的数也不行, 直接 <code>break</code>。")
    doc.svg("13-backtracking/combination_sum_core.svg",
            "图 3a: decision tree。红色虚线 = 选了就超过 target, break。[2,2,2] 和 [3,3] 是绿色答案。")
    doc.svg("13-backtracking/combination_sum_trace.svg",
            "图 3b: 每步写出 remain = target − sum(path) 的具体数字。")
    doc.code(SRC["comb"])
    doc.p("Time: 树深最多 target/min(c) 层, 每层最多 n 个分支, 上界 O(n^(target/min)), 实际因为剪枝和 start 小得多。"
          "Space O(target/min): 递归深度。")
    doc.note("元素可重复用: 递归传 <code>i</code>; 每个数只能用一次: 传 <code>i+1</code>。有和的约束: sort + <code>c &gt; remain</code> 就 break。")

    # ---------------------------------------------------------------- 4 Combination Sum II
    doc.h2("4. Combination Sum II: 排序 + 同层去重")
    doc.p("题: <code>candidates = [1,2,2,3]</code>, <code>target = 5</code>, 每个数最多用一次, 候选里有重复值, "
          "答案不能有重复组合。答案: <code>[[1,2,2],[2,3]]</code>。")
    doc.p("Brute force: 枚举 2^4 = 16 个子集, 筛出和为 5 的, 再用 set 去重, O(n·2^n)。"
          "浪费: 选第一个 2 和选第二个 2 生成的是完全相同的子树, 白白展开了两遍, 最后还要靠 set 去重。")
    doc.p("关键观察: 先排序, 相同的值就挨在一起。在 <b>同一层</b> (同一个 <code>for</code> 循环里), "
          "如果 <code>candidates[i] == candidates[i-1]</code>, 说明这个值在这一层已经试过, 子树会一模一样, 跳过。"
          "但 <code>i == start</code> 时是 \"下一层的第一个\", 不是同一层, 必须允许 — 否则 <code>[1,2,2]</code> 出不来。"
          "所以条件是 <code>i &gt; start and candidates[i] == candidates[i-1]</code>。")
    doc.p("相比上一题改两行: 递归传 <code>i+1</code> (每个数只用一次); 加这一行去重。")
    doc.svg("13-backtracking/combination_sum_ii_core.svg",
            "图 4a: decision tree。\"同层重复\" 的红色分支是第二个 2 (i=2, start=1 或 0), 子树和第一个 2 一样, 剪掉。")
    doc.svg("13-backtracking/combination_sum_ii_trace.svg",
            "图 4b: 第 8 步 path=[1], i=2 > start=1 且 2 == 2, 剪枝; 第 3 步 path=[1,2,2] 允许, 因为 i=2 == start=2。")
    doc.code(SRC["comb2"])
    doc.p("Time O(2^n) 上界 (每个元素选 / 不选), 去重后实际更少, 不再需要 set。Space O(n)。")
    doc.note("有重复元素又要去重: 先 sort, 循环里加 <code>if i &gt; start and nums[i] == nums[i-1]: continue</code>。"
             "Subsets II 同样一行。")

    # ---------------------------------------------------------------- 5 Parentheses
    doc.h2("5. Generate Parentheses: 约束剪枝, 只生成合法前缀")
    doc.p("题: 给 <code>n</code>, 生成所有 n 对合法括号。<code>n = 2</code>: <code>[\"(())\", \"()()\"]</code>。")
    doc.p("Brute force: 2^(2n) 个由 <code>(</code> <code>)</code> 组成的串, 逐个检查合法, O(n·4^n)。"
          "n = 3 时 64 个串里只有 5 个合法。")
    doc.p("关键观察: 一个串合法 ⟺ 每个前缀里 <code>)</code> 的个数 ≤ <code>(</code> 的个数, 且最后各 n 个。"
          "所以不用事后检查, 每一步只加 \"不会破坏前缀\" 的字符: "
          "<code>(</code> 要 <code>open_ &lt; n</code>; <code>)</code> 要 <code>close &lt; open_</code>。"
          "两个 <code>if</code> 就是约束剪枝, 树上每个叶子都是答案, 没有一个废叶子。")
    doc.svg("13-backtracking/generate_parentheses_core.svg",
            "图 5a: n=2 的 decision tree。红色虚线 = 被两个条件挡住的选择, 写明哪个条件。")
    doc.svg("13-backtracking/generate_parentheses_trace.svg",
            "图 5b: 前 12 步。第 3、5 步 open_ = n 挡住 \"(\"; 根节点的 \")\" 要到第 21 步才被挡 (close=0 ≥ open_=0)。")
    doc.code(SRC["parens"])
    doc.p("Time O(4^n / √n) 量级 (Catalan 数个答案 × 每个 O(n) 的 join); Space O(n)。")
    doc.note("构造的串有 \"前缀合法性\": 把条件写成 <code>if</code> 挡在 push 之前, 不要先生成再检查。")

    # ---------------------------------------------------------------- 6 Letters
    doc.h2("6. Letter Combinations of a Phone Number: 每层候选不同")
    doc.p("题: <code>digits = \"23\"</code>, 每个数字对应几个字母, 返回所有字母组合。<code>\"2\"→abc</code>, <code>\"3\"→def</code>, 共 3×3 = 9 个。")
    doc.p("Brute force: 嵌套 for / <code>itertools.product</code>。问题是 <code>digits</code> 的长度是 input, 嵌套层数写不出来。"
          "这里没有任何东西可以剪枝 — 它是纯粹的笛卡尔积。")
    doc.p("关键观察: 相比前面几题, choices 不再是 \"从 start 往后\" 或 \"没用过的\", 而是由 <b>层数 idx</b> 决定: "
          "第 idx 层的候选 = <code>PHONE[digits[idx]]</code>, 和 path 里选了什么无关。"
          "所以不需要 start 也不需要 used, 只要一个 <code>idx</code>。backtracking 在这里只是把 \"层数不固定的嵌套 for\" 写成递归。")
    doc.svg("13-backtracking/letter_combinations_core.svg",
            "图 6a: decision tree。每层的分支数固定 (3 和 3), 没有被剪的分支; 9 个叶子 = 9 个答案。")
    doc.svg("13-backtracking/letter_combinations_trace.svg",
            "图 6b: 前 12 步。每个叶子: push → 收集 → pop。pop 到空 path 之后换第一个字母。")
    doc.code(SRC["letters"])
    doc.p("Time O(4^n · n): n = <code>len(digits)</code>, 每位最多 4 个字母, 叶子 ≤ 4^n 个, 每个 join 花 O(n)。Space O(n)。")
    doc.note("每一位有各自的候选集: 递归的参数是层数 <code>idx</code>, choices = 第 idx 层的候选; 层数固定 = 笛卡尔积。")

    # ---------------------------------------------------------------- 7 Word Search
    doc.h2("7. Word Search: grid 上的 backtracking, 原地标记再恢复")
    doc.p("题: 在字符 grid 里找 <code>word</code>, 路径是相邻格子 (上下左右), 同一个格子不能用两次。"
          "例: board = <code>ABA / BBD</code>, word = <code>ABAD</code> → True。")
    doc.p("Brute force: 从每个格子出发枚举所有长度为 L 的路径, 每步 4 个方向, O(R·C·4^L), 最后才比较字母。"
          "浪费有两处: 字母不对了还继续走; 每一步都允许走回头路。")
    doc.p("关键观察: 这是 Permutations 的 grid 版本。path = 走过的格子序列, \"同一格不能用两次\" 就是 <code>used[]</code>。"
          "grid 里可以直接把 board 当 used: 做选择时把 <code>board[r][c]</code> 改成 <code>\"#\"</code>, "
          "撤销时改回原字母。没有额外的 visited set。剪枝: 越界 / 字母不对 / 已经是 <code>#</code> 都在同一个 <code>if</code> 里返回 False。")
    doc.svg("13-backtracking/word_search_core.svg",
            "图 7a: 同一个 board 在 DFS 不同时刻的四个快照。# 的个数始终等于 len(path)。")
    doc.svg("13-backtracking/word_search_trace.svg",
            "图 7b: 全部 18 步。第 2-7 步走进 (1,0) 的死路再恢复; 第 9 步换方向, 第 14 步找到。右列是 board 的实时状态。")
    doc.code(SRC["wsearch"])
    doc.p("Time O(R·C·3^L): R·C 个起点, 每个起点最多 L 层, 除第一步外每步最多 3 个方向 (第 4 个是来的方向, 已经是 #)。"
          "Space O(L): 只有递归栈, 原地标记不需要 O(R·C) 的 visited。")
    doc.note("grid + 路径不能重复用: 原地改成 <code>#</code> 当 used, 递归之后改回。找到答案也要先恢复再 return。")

    # ---------------------------------------------------------------- 8 N-Queens
    doc.h2("8. N-Queens: 多个约束 => 多个 set")
    doc.p("题: n×n 棋盘放 n 个皇后, 互相不能同行、同列、同一条对角线。返回所有摆法。<code>n = 4</code> 有 2 个解。")
    doc.p("Brute force: 从 16 格里选 4 个, C(16,4) = 1820 种, 逐一检查。每行恰好放一个后是 4^4 = 256 种; "
          "再要求列不重复就是 4! = 24 种 (和 Permutations 一样); 对角线冲突则要靠剪枝在中途发现。")
    doc.p("关键观察: 一行放一个皇后, 所以 path[r] = 第 r 行的列, 层数 = 行数, 这就是 Permutations (列不能重复) 再加两个约束。"
          "同一条 <code>\\</code> 对角线上所有格子 <code>r − c</code> 相同; 同一条 <code>/</code> 对角线上 <code>r + c</code> 相同。"
          "所以用三个 set (<code>cols</code> / <code>diag</code> / <code>anti</code>) 记录已占用的值, 检查一个格子只要 3 次 O(1) 查询。"
          "做选择要往三个 set 各 add, 撤销要各 remove。")
    doc.svg("13-backtracking/n_queens_core.svg",
            "图 8a: 前两行已放 (0,1) 和 (1,3); 第 2 行四列里只有 c=0 通过三个 set 的检查。")
    doc.svg("13-backtracking/n_queens_trace.svg",
            "图 8b: 前 17 步。右列是三个 set 的实时内容; 红色虚线格子 = 被某个 set 挡住的列。")
    doc.code(SRC["nqueens"])
    doc.p("Time O(n!) 上界 (第 r 行至多还有 n−r 列可选)。实际远小: n = 4 只访问 %d 个节点 (4! = 24 个叶子位置); "
          "n = 8 访问 %d 个节点, 而 8! = 40320。Space O(n): path + 三个 set + 递归栈。" % (nq4_nodes, nq8_nodes))
    doc.note("放置类约束题: 把每条约束写成一个 set (key = 它禁止的东西), 检查 O(1); 撤销时所有 set 同步还原。")

    # ---------------------------------------------------------------- 识别信号
    doc.h2("9. 识别信号: 看到什么 → 试什么")
    rows = [
        ("要 <b>所有</b> 组合 / 排列 / 子集 / 路径 (输出是指数级)", "backtracking 模板: path + 做选择 / 递归 / 撤销",
         "下限是输出大小; 剪枝把节点数从 \"所有候选\" 降到 \"接近答案数\""),
        ("无序, 每个元素选或不选 (Subsets, Combinations)", "<code>range(start, n)</code>, 递归传 <code>i+1</code>",
         "n^n 或带重复 → 2^n, 没有 [1,2] / [2,1] 重复"),
        ("有序, 元素不可重复用 (Permutations)", "每层 <code>range(n)</code> + <code>used[]</code>",
         "n^n → n!"),
        ("元素可重复用, 要凑 target (Combination Sum)", "sort + 递归传 <code>i</code> + <code>remain</code>, <code>c &gt; remain</code> 就 break",
         "每个数的次数全枚举 → 超过 target 的分支全部不展开"),
        ("候选有重复值, 答案要去重 (Combination Sum II, Subsets II)", "sort + 同层 <code>i &gt; start and a[i] == a[i-1]</code> 跳过",
         "生成再用 set 去重 → 重复子树根本不展开"),
        ("构造的串 / 序列有前缀合法性 (括号)", "把条件写成 push 之前的 <code>if</code>",
         "2^(2n) 个串逐个检查 → Catalan(n) 个叶子, 无废叶子"),
        ("每一位有各自的候选集 (电话号码)", "递归参数 = 层数 <code>idx</code>, 无剪枝",
         "嵌套 for 层数不固定 → 递归; 复杂度 = 候选数的乘积"),
        ("grid 上找路径, 格子不能重复用 (Word Search)", "原地改成 <code>#</code>, 递归后改回; 不匹配立刻 return",
         "visited set O(R·C) → 原地 O(1) 额外空间; 4^L → 3^L"),
        ("放置问题, 约束可写成 \"某个值不能重复\" (N-Queens, Sudoku)", "每条约束一个 set, 做选择 add / 撤销 remove",
         "检查冲突 O(n) → O(1)"),
        ("只问 <b>能不能</b> / <b>有几个</b> / 最优值, 且子问题会重复", "不是 backtracking: 加 memo 变 DP",
         "指数 → 多项式 (状态数)"),
    ]
    tbl = ["<table><tr><th>特征</th><th>做法</th><th>complexity 从 X 降到 Y</th></tr>"]
    for a, b, c in rows:
        tbl.append("<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (a, b, c))
    tbl.append("</table>")
    doc.raw("".join(tbl))
    doc.note("题目要 \"列出所有\" → 画 decision tree, 问自己三件事: path 是什么, choices 是什么, 什么时候收集; "
             "再问: 哪些分支可以在 push 之前就判死刑?")

    doc.h2("以后再学")
    doc.p("Sudoku Solver (N-Queens 的 rows / cols / boxes 三个 set)、Palindrome Partitioning 和 Restore IP Addresses "
          "(choices = 下一段切多长)、bitmask 版 N-Queens、给 backtracking 加 memo 变成 DP。思路都已经在上面的模板里。")
    doc.write("docs/13-backtracking.html")


build_svgs()
for w in WARN:
    print("WARN", w)
build_doc()
