# 19 · Matrix / Math / Bit / Sorting 正文 (NeetCode 式讲法)。由 19_matrix-math-bit.py 末尾 exec。
import nclib as nc
from counts import cnt

EX = os.path.join(d.ROOT, "docs", "svg", SLUG, "%s_examples.svg")
EXS = SLUG + "/%s_examples.svg"
SVG = lambda name, cap: doc.svg(SLUG + "/" + name + ".svg", cap)

# ---------------------------------------------------------------- 例子图
assert load(SPIRAL)["spiralOrder"]([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]) == [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
nc.examples_svg(EX % "spiral", "Spiral Matrix examples", ["按顺时针螺旋的顺序, 返回矩阵的所有元素"], [
    dict(title="Example:  [[1,2,3,4],[5,6,7,8],[9,10,11,12]]  →  [1,2,3,4,8,12,11,10,9,5,6,7]", index=False, rows=[
        ("row 0", [1, 2, 3, 4], ["new"] * 4), ("row 1", [5, 6, 7, 8], ["new", "rem", "rem", "new"]), ("row 2", [9, 10, 11, 12], ["new"] * 4)],
         extra=["先走最外面一圈 (绿色): 右 1→4, 下 8→12, 左 11→9, 上 5; 再走里面剩下的 6, 7 (红色)"])],
    legend=[("new", "第一圈"), ("rem", "第二圈")])

m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
load(ROTATE)["rotate"](m)
assert m == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
nc.examples_svg(EX % "rotate", "Rotate Image examples", ["把 n × n 的矩阵顺时针旋转 90 度, 必须原地修改 (不能开新矩阵)"], [
    dict(title="Example:  [[1,2,3],[4,5,6],[7,8,9]]  →  [[7,4,1],[8,5,2],[9,6,3]]", index=False, rows=[
        ("之前 r0", [1, 2, 3], ["new", "keep", "keep"]), ("之前 r1", [4, 5, 6], None), ("之前 r2", [7, 8, 9], None),
        ("之后 r0", [7, 4, 1], ["keep", "keep", "new"]), ("之后 r1", [8, 5, 2], None), ("之后 r2", [9, 6, 3], None)],
         extra=["原来的第一行 1, 2, 3 变成了最后一列 (从上往下)。例如 1 从左上角转到了右上角"])],
    legend=[("new", "1 的位置")])

z = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
load(ZEROES)["setZeroes"](z)
assert z == [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
nc.examples_svg(EX % "zeroes", "Set Matrix Zeroes examples", ["只要某个格子是 0, 就把它所在的整行、整列都变成 0。原地修改"], [
    dict(title="Example:  [[1,1,1],[1,0,1],[1,1,1]]  →  [[1,0,1],[0,0,0],[1,0,1]]", index=False, rows=[
        ("之前 r0", [1, 1, 1], None), ("之前 r1", [1, 0, 1], ["keep", "rem", "keep"]), ("之前 r2", [1, 1, 1], None),
        ("之后 r0", [1, 0, 1], ["keep", "rem", "keep"]), ("之后 r1", [0, 0, 0], ["rem"] * 3), ("之后 r2", [1, 0, 1], ["keep", "rem", "keep"])],
         extra=["中间那个 0, 让第 1 行和第 1 列都变成了 0。注意: 新变成的 0 不能再去影响别的行列"])],
    legend=[("rem", "0")])

P_ = load(POW)["myPow"]
assert abs(P_(2.0, 10) - 1024) < 1e-9 and abs(P_(2.0, -2) - 0.25) < 1e-9
nc.examples_svg(EX % "pow", "Pow examples", ["实现 x 的 n 次方。n 可以是负数, 可以非常大 (到 2³¹)"], [
    dict(title="Example 1:  x = 2, n = 10  →  1024"),
    dict(title="Example 2:  x = 2, n = -2  →  0.25", extra=["负数次方 = 1 / 正数次方: 1 / 2² = 0.25"]),
    dict(title="难点", extra=["n = 2³¹ 时, 乘 n 次要 20 亿次乘法, 太慢"])],
    legend=[])

I = load(PALIN)["isPalindrome"]
assert I(121) and not I(-121) and not I(10)
nc.examples_svg(EX % "palin", "Palindrome Number examples", ["判断一个整数正着读和反着读是不是一样。不能转成字符串"], [
    dict(title="Example 1:  121  →  True"), dict(title="Example 2:  -121  →  False", extra=["反过来读是 121-, 不一样。负数一定不是"]),
    dict(title="Example 3:  10  →  False", extra=["反过来是 01, 不一样。末尾是 0 的 (除了 0 本身) 一定不是"])],
    legend=[])

X = load(XOR)
assert X["singleNumber"]([4, 1, 2, 1, 2]) == 4 and X["missingNumber"]([3, 0, 1]) == 2
nc.examples_svg(EX % "xor", "Single / Missing Number examples", ["Single Number: 每个数都出现两次, 只有一个出现一次, 找它。Missing Number: 0..n 里少了一个, 找它。都要 O(1) 空间"], [
    dict(title="Single Number:  [4,1,2,1,2]  →  4", items=[4, 1, 2, 1, 2], hl=[0], extra=["1 和 2 各出现两次, 4 只出现一次"]),
    dict(title="Missing Number:  [3,0,1]  →  2", items=[3, 0, 1], extra=["n = 3, 应该有 0, 1, 2, 3, 少了 2"])],
    legend=[("new", "答案")])

H = load(BITS)["hammingWeight"]
assert H(11) == 3 and H(128) == 1
nc.examples_svg(EX % "bits", "Number of 1 Bits examples", ["一个正整数的二进制表示里有几个 1"], [
    dict(title="Example 1:  n = 11  →  3", items=list("1011"), hl=[0, 2, 3], index=False, ans_text="11 = 1011 (二进制)"),
    dict(title="Example 2:  n = 128  →  1", items=list("10000000"), hl=[0], index=False, ans_text="128 = 10000000")],
    legend=[("new", "1")])

assert load(MINDIFF)["minimumAbsDifference"]([4, 2, 1, 3]) == [[1, 2], [2, 3], [3, 4]]
nc.examples_svg(EX % "mindiff", "Minimum Absolute Difference examples", ["数组里的数互不相同。找所有差的绝对值最小的 pair, 按从小到大输出"], [
    dict(title="Example:  [4,2,1,3]  →  [[1,2],[2,3],[3,4]]", index=False, rows=[("排序后", [1, 2, 3, 4], ["new"] * 4)],
         extra=["最小的差是 1。排好序之后, 差最小的 pair 一定是相邻的两个"])],
    legend=[])

R = load(ROMAN)["romanToInt"]
assert R("III") == 3 and R("LVIII") == 58 and R("MCMXCIV") == 1994
nc.examples_svg(EX % "roman", "Roman to Integer examples", ["罗马数字转整数。I=1, V=5, X=10, L=50, C=100, D=500, M=1000; 小的写在大的左边表示相减, 比如 IV = 4"], [
    dict(title="Example 1:  \"LVIII\"  →  58", items=list("LVIII"), index=False, extra=["50 + 5 + 1 + 1 + 1"]),
    dict(title="Example 2:  \"MCMXCIV\"  →  1994", index=False, rows=[("", list("MCMXCIV"), ["keep", "rem", "keep", "rem", "keep", "rem", "keep"])],
         extra=["M=1000, CM=900, XC=90, IV=4 → 1994。C、X、I 都比右边的小, 所以是减"])],
    legend=[("rem", "要减的")])

# ================================================================ HTML
doc = d.Doc("19 · Matrix / Simulation / Math / Bit / Sorting")
doc.h2("这篇讲什么")
doc.p("这一篇是\"杂项\": 矩阵模拟、数学、位运算、排序。这些题没有一个统一的数据结构, 但思路有共同点: <b>brute force 要么多存了一份输入里本来就有的信息, 要么重复做了可以复用的计算</b>。每道题的关键都是找到输入里现成的结构, 把浪费消掉。")
SVG("intro_core", "四类题: brute force 浪费在哪 (灰色) → 用什么结构消掉 (绿色)。")
doc.p("读完要建立的反射: 看到\"原地 / O(1) 空间\", 想能不能借输入自己存信息; 看到\"n 很大\", 想二进制拆分; 看到\"成对 / 配对\", 想 XOR; 看到\"最近 / 最小差\", 想排序之后只看相邻。")
nc.solution(doc, TEMPLATE, summary="本篇用到的 Python 写法")
nc.table(doc, ["#", "题目", "考过的公司数", "用到的结构"], [
    ["1", "Spiral Matrix", cnt("Spiral Matrix"), "四个边界"], ["2", "Rotate Image", cnt("Rotate Image"), "坐标变换"],
    ["3", "Set Matrix Zeroes", cnt("Set Matrix Zeroes"), "用矩阵自己当标记"], ["4", "Pow(x, n)", cnt("Pow(x, n)"), "n 的二进制"],
    ["5", "Palindrome Number", cnt("Palindrome Number"), "% 10 和 // 10"],
    ["6", "Single Number / Missing Number", "%d / %d" % (cnt("Single Number"), cnt("Missing Number")), "XOR 抵消"],
    ["7", "Number of 1 Bits", cnt("Number of 1 Bits"), "n & (n - 1)"],
    ["8", "Minimum Absolute Difference", cnt("Minimum Absolute Difference"), "排序后只看相邻"],
    ["9", "Roman to Integer", cnt("Roman to Integer"), "查表 + 看右边"]])
doc.p("每道题的顺序: <b>题目在问什么 → 看例子 → brute force → intuition → 算法 → 手动走一遍 → 复杂度</b>。代码放在最后, 默认折叠。")

# ================================================================ 1
doc.h2("1. Spiral Matrix")
doc.h3("题目在问什么")
doc.p("给一个 m × n 的矩阵, 按<b>顺时针螺旋</b>的顺序返回所有元素: 先往右走第一行, 再往下走最后一列, 再往左走最后一行, 再往上走第一列, 然后进入里面一圈, 重复。")
doc.h3("看例子")
doc.svg(EXS % "spiral", "例子。")
doc.h3("Brute force")
doc.p("模拟一个人在走: 用一个 <code>visited</code> 矩阵记录走过的格子, 加一个方向 (右、下、左、上)。撞到边界或者走过的格子就右转。")
doc.p("Time <code>O(m·n)</code>, 但多用了 <code>O(m·n)</code> 的 visited。浪费: 用一整张表去记一个其实很规则的集合。")
doc.h3("Intuition: 还没走的部分永远是一个矩形")
doc.p("每走完一条边, 走过的都是最外面的一圈, 剩下没走的永远是一个<b>矩形</b>。一个矩形只要 4 个数就能描述: <code>top</code>、<code>bottom</code>、<code>left</code>、<code>right</code>。")
doc.p("所以不需要 visited: 走完上面一行, top 加 1; 走完右边一列, right 减 1; 走完下面一行, bottom 减 1; 走完左边一列, left 加 1。")
doc.p("一个细节: 走\"下面一行\"和\"左边一列\"之前, 要先检查矩形是否还存在 (<code>top ≤ bottom</code>、<code>left ≤ right</code>)。比如只剩一行时, 走完上面那一行就没有了, 不能再往回走一遍。")
doc.h3("算法")
nc.steps(doc, "<code>top, bottom, left, right = 0, m-1, 0, n-1</code>。",
         "当 <code>top ≤ bottom and left ≤ right</code>: 往右走 top 行, top += 1; 往下走 right 列, right -= 1;",
         "如果 top ≤ bottom: 往左走 bottom 行, bottom -= 1; 如果 left ≤ right: 往上走 left 列, left += 1。")
SVG("spiral_core", "四个边界圈出还没走过的矩形, 走完一条边就收缩对应的边界。")
doc.h3("手动走一遍")
SVG("spiral_trace", "3 × 4 矩阵, 6 行走完, 每一行能看到边界怎么收缩。")
doc.h3("复杂度")
doc.p("Time <code>O(m·n)</code>, 额外 Space <code>O(1)</code>。")
nc.solution(doc, SPIRAL)
doc.note("矩阵按圈走: 4 个边界变量代替 visited, 走完一条边收缩一个边界。")

# ================================================================ 2
doc.h2("2. Rotate Image")
doc.h3("题目在问什么")
doc.p("把一个 n × n 的矩阵顺时针旋转 90 度, 必须<b>原地</b>修改。")
doc.h3("看例子")
doc.svg(EXS % "rotate", "例子。")
doc.h3("Brute force")
doc.p("开一个新矩阵, 把每个元素放到旋转后的位置, 再复制回来。<code>O(n²)</code> 额外空间。")
doc.h3("Intuition: 先写出坐标怎么变, 再拆成两个简单的操作")
doc.p("看例子: 原来在 (i, j) 的元素, 旋转后到了 <code>(j, n-1-i)</code>。比如 1 在 (0, 0), 转到了 (0, 2)。")
doc.p("直接按这个公式原地挪很难写 (要四个一组地转圈)。但这个变换可以拆成两步, 每一步都很容易原地做:")
nc.steps(doc, "<b>transpose</b> (沿主对角线翻转): (i, j) → (j, i)。交换 <code>m[i][j]</code> 和 <code>m[j][i]</code> (只对 j > i 做)。",
         "<b>每一行左右反转</b>: (j, i) → (j, n-1-i)。")
doc.p("两步合起来就是 (i, j) → (j, n-1-i), 正好是顺时针旋转。逆时针的话, 先 transpose 再上下反转 (或者先反转每一行再 transpose)。")
doc.h3("算法")
nc.steps(doc, "i 从 0 到 n-1, j 从 i+1 到 n-1: 交换 m[i][j] 和 m[j][i]。", "每一行 <code>row.reverse()</code>。")
SVG("rotate_core", "坐标变换 (i, j) → (j, n-1-i) 拆成 transpose + 每行反转。")
doc.h3("手动走一遍")
SVG("rotate_trace", "3 × 3 矩阵: transpose 之后再逐行反转。")
doc.h3("复杂度")
doc.p("Time <code>O(n²)</code>, Space <code>O(1)</code>。")
nc.solution(doc, ROTATE)
doc.note("矩阵旋转: 先写出坐标变换, 再拆成 transpose + 反转。")

# ================================================================ 3
doc.h2("3. Set Matrix Zeroes")
doc.h3("题目在问什么")
doc.p("如果矩阵里某个格子是 0, 就把它所在的整行和整列都变成 0。原地修改, 最好只用 <code>O(1)</code> 额外空间。")
doc.h3("看例子")
doc.svg(EXS % "zeroes", "例子。")
doc.p("难点: 一边扫一边改, 新变成的 0 会被误以为是原来的 0, 又去清别的行列。")
doc.h3("Brute force")
doc.p("先扫一遍, 用两个 set 记下哪些行、哪些列有 0; 再扫一遍, 把这些行列清零。Time <code>O(m·n)</code>, Space <code>O(m + n)</code>。")
doc.h3("Intuition: 用矩阵自己的第一行、第一列当标记")
doc.p("brute force 里的两个 set, 其实就是\"每一行一个标记\"和\"每一列一个标记\"。矩阵的第一列正好每行有一个格子, 第一行正好每列有一个格子。所以可以把标记直接写在第一行和第一列上: 如果 (i, j) 是 0, 就把 <code>m[i][0]</code> 和 <code>m[0][j]</code> 设为 0。")
doc.p("但第一行和第一列自己也可能原本有 0。所以先用两个变量 <code>row0</code>、<code>col0</code> 记下第一行、第一列原本有没有 0。")
doc.p("处理顺序: 先根据标记清掉内部 (第 1 行以后、第 1 列以后) 的格子, <b>最后</b>再根据 row0 和 col0 处理第一行和第一列。如果先改第一行, 标记就被破坏了。")
doc.h3("算法")
nc.steps(doc, "记下 row0 = 第一行有没有 0, col0 = 第一列有没有 0。",
         "扫内部的格子: (i, j) 是 0 就 <code>m[i][0] = m[0][j] = 0</code>。",
         "再扫内部: <code>m[i][0] == 0 or m[0][j] == 0</code> 就把 (i, j) 设为 0。",
         "最后按 row0、col0 清第一行、第一列。")
SVG("zeroes_core", "第一行 / 第一列当标记, row0 / col0 单独记, 最后处理。")
doc.h3("手动走一遍")
SVG("zeroes_trace", "标记 → 清内部 → 清第一行和第一列。")
doc.h3("复杂度")
doc.p("Time <code>O(m·n)</code>, Space <code>O(1)</code>。")
nc.solution(doc, ZEROES)
doc.note("要 O(1) 空间的标记: 借输入的一部分 (第一行 / 第一列) 来存, 注意处理顺序, 别提前破坏标记。")

# ================================================================ 4
doc.h2("4. Pow(x, n)")
doc.h3("题目在问什么")
doc.p("实现 x 的 n 次方。n 可以是负数, 也可以非常大 (到 2³¹)。")
doc.h3("看例子")
doc.svg(EXS % "pow", "例子。")
doc.h3("Brute force")
doc.p("把 x 乘 n 次, <code>O(n)</code>。n = 2³¹ 时要 20 亿次乘法, 太慢。")
doc.h3("Intuition: 把 n 拆成二进制")
doc.p("观察: <code>x¹⁰ = x⁸ · x²</code>, 因为 10 的二进制是 1010 (= 8 + 2)。而 x², x⁴, x⁸ 可以不断平方得到: x → x² → x⁴ → x⁸, 每次只要一次乘法。")
doc.p("所以: 从 n 的最低位开始看, 同时维护当前的 <code>x^(2^k)</code>。这一位是 1, 就把它乘进结果; 然后 x 平方, n 右移一位。n 有 <code>log n</code> 位, 所以只要 <code>O(log n)</code> 次乘法。")
doc.p("负数次方: 先算 <code>x^|n|</code>, 再取倒数。")
doc.h3("算法")
nc.steps(doc, "n < 0 时: x = 1/x, n = -n。", "<code>res = 1</code>。当 n > 0: 如果 <code>n & 1</code>, <code>res *= x</code>。然后 <code>x *= x</code>, <code>n >>= 1</code>。", "返回 res。")
SVG("pow_core", "n 的二进制决定乘哪几个 x^(2^k)。")
doc.h3("手动走一遍")
SVG("pow_trace", "每一行看 n 的一位, x 不断平方。")
doc.h3("复杂度")
doc.p("Time <code>O(log n)</code>, Space <code>O(1)</code>。")
nc.solution(doc, POW)
doc.note("n 很大的重复操作 (幂、矩阵幂): 按 n 的二进制拆, 不断平方, O(log n)。")

# ================================================================ 5
doc.h2("5. Palindrome Number")
doc.h3("题目在问什么")
doc.p("判断一个整数是不是回文 (正着读和反着读一样)。不转成字符串。")
doc.h3("看例子")
doc.svg(EXS % "palin", "三个例子。")
doc.h3("Brute force")
doc.p("<code>str(x) == str(x)[::-1]</code>。可以, 但题目要求不转字符串。")
doc.h3("Intuition: 用 % 10 和 // 10 拆数字, 只反转一半")
doc.p("处理整数的每一位, 只需要两个操作: <code>x % 10</code> 拿到最后一位, <code>x // 10</code> 去掉最后一位。")
doc.p("把 x 的后半部分反转出来: 每次从 x 末尾拿一位, 接到 rev 后面 (<code>rev = rev * 10 + x % 10</code>), x 去掉这一位。当 <code>rev ≥ x</code> 时, 说明已经处理了一半。")
doc.p("然后比较: 偶数位时 <code>x == rev</code>; 奇数位时中间那一位跑到了 rev 末尾, 比较 <code>x == rev // 10</code>。")
doc.p("只反转一半还有一个好处: 不会溢出。特殊情况先排除: 负数不是回文; 末尾是 0 的 (除了 0 本身) 也不是。")
doc.h3("算法")
nc.steps(doc, "x < 0 或者 (x % 10 == 0 且 x != 0), 返回 False。",
         "<code>rev = 0</code>。当 <code>x > rev</code>: <code>rev = rev * 10 + x % 10</code>, <code>x //= 10</code>。",
         "返回 <code>x == rev or x == rev // 10</code>。")
SVG("palin_core", "从末尾拆一半, 和前一半比较; 奇数位时去掉中间那一位。")
doc.h3("手动走一遍")
SVG("palin_trace", "奇数位和偶数位各一个例子。")
doc.h3("复杂度")
doc.p("Time <code>O(位数)</code>, Space <code>O(1)</code>。Reverse Integer 用同样的 % 10 / // 10, 只是要注意溢出。")
nc.solution(doc, PALIN)
doc.note("处理整数的每一位: % 10 取末位, // 10 去末位。")

# ================================================================ 6
doc.h2("6. Single Number → Missing Number")
doc.h3("题目在问什么")
doc.p("<b>Single Number</b>: 数组里每个数都出现两次, 只有一个数出现一次, 找出它。<b>Missing Number</b>: 数组里有 n 个不同的数, 取自 0..n, 少了一个, 找出它。都要求 <code>O(n)</code> 时间、<code>O(1)</code> 空间。")
doc.h3("看例子")
doc.svg(EXS % "xor", "两道题的例子。")
doc.h3("Brute force")
doc.p("用 Counter 或 set (01), <code>O(n)</code> 时间但 <code>O(n)</code> 空间。")
doc.h3("Intuition: XOR 让成对的数互相抵消")
doc.p("XOR (异或, Python 里是 <code>^</code>) 有三个性质: <code>a ^ a = 0</code> (自己和自己抵消); <code>a ^ 0 = a</code>; 而且顺序无所谓 (满足交换律和结合律)。")
doc.p("所以把所有数 XOR 起来, 出现两次的都抵消成 0, 只剩下出现一次的那个。")
doc.p("Missing Number 也能这样做: 把\"应该有的\" 0..n 和\"实际有的\"数组里的数全部 XOR 在一起。每个出现了的数都出现两次 (一次在 0..n 里, 一次在数组里), 抵消掉; 缺的那个只出现一次, 留了下来。代码里用下标 i 代替 0..n-1, 再补上 n。")
doc.h3("算法")
nc.steps(doc, "Single Number: <code>res = 0</code>, 对每个 x: <code>res ^= x</code>。",
         "Missing Number: <code>res = n</code>, 对每个 i: <code>res ^= i ^ nums[i]</code>。")
SVG("xor_core", "XOR 把成对的数抵消掉, 只剩下没有配对的那个。")
doc.h3("手动走一遍")
SVG("xor_trace", "逐个 XOR 的二进制过程。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(1)</code>。Missing Number 也可以用求和公式: <code>n(n+1)/2 - sum(nums)</code>。")
nc.solution(doc, XOR)
doc.note("成对出现、找落单的: XOR 全部, 成对的抵消。")

# ================================================================ 7
doc.h2("7. Number of 1 Bits")
doc.h3("题目在问什么")
doc.p("给一个正整数, 返回它的二进制表示里有几个 1。")
doc.h3("看例子")
doc.svg(EXS % "bits", "两个例子。")
doc.h3("Brute force")
doc.p("一位一位看: <code>n & 1</code> 是最低位, 然后 <code>n >>= 1</code>。要看所有 32 位。")
doc.h3("Intuition: n & (n - 1) 每次正好消掉最低位的 1")
doc.p("看 n - 1 的二进制: 它是把 n 最低位的那个 1 变成 0, 并把它右边的 0 全变成 1。比如 n = 1100, n - 1 = 1011。")
doc.p("所以 <code>n & (n - 1)</code> = 1000: 最低位的 1 被消掉了, 其他位不变。")
doc.p("每做一次消掉一个 1, 做到 n 变成 0 为止, 做了几次就有几个 1。只需要循环\"1 的个数\"次, 不用看所有 32 位。")
doc.p("相关的技巧: <code>n & -n</code> 取出最低位的那个 1; <code>n > 0 and n & (n - 1) == 0</code> 判断 n 是不是 2 的幂 (只有一个 1)。")
doc.h3("算法")
nc.steps(doc, "<code>count = 0</code>。当 n: <code>n &= n - 1</code>, count += 1。", "返回 count。")
SVG("bits_core", "n & (n - 1) 消掉最低位的 1。")
doc.h3("手动走一遍")
SVG("bits_trace", "每一步消掉一个 1, 直到 n = 0。")
doc.h3("复杂度")
doc.p("Time <code>O(1 的个数)</code>, Space <code>O(1)</code>。")
nc.solution(doc, BITS)
doc.note("n & (n - 1) 消掉最低位的 1; n & -n 取出最低位的 1。")

# ================================================================ 8
doc.h2("8. Minimum Absolute Difference (以及排序的用法)")
doc.h3("题目在问什么")
doc.p("数组里的数互不相同。找出所有差的绝对值最小的 pair, 按从小到大的顺序输出。")
doc.h3("看例子")
doc.svg(EXS % "mindiff", "例子。")
doc.h3("Brute force")
doc.p("两两比较算差, <code>O(n²)</code>。")
doc.h3("Intuition: 排好序之后, 差最小的一定是相邻的")
doc.p("排序后, 对任意 i < j < k, 有 <code>a[k] - a[i] ≥ a[j] - a[i]</code>。也就是说, 隔着别的数的 pair, 差一定不会比相邻的更小。所以只需要看相邻的 n - 1 对。")
doc.p("这是一个很通用的思路: <b>排序当预处理</b>。排完序之后很多问题都只需要看相邻的元素, 比如区间合并 (10)、Meeting Rooms (10)、去重、找最接近的两个数。排序本身 <code>O(n log n)</code>, 往往比 brute force 的 <code>O(n²)</code> 快很多。")
doc.p("自定义排序: 用 <code>key=</code> (比如 <code>sort(key=lambda x: (x[1], -x[0]))</code> 按第二个元素升序、第一个降序); 需要\"两两比较\"的规则时用 <code>functools.cmp_to_key</code> (比如 16 里的 Largest Number)。")
doc.p("什么时候不用通用排序: 只要第 k 个用 quickselect 或 heap (09); 值的范围很小用 counting sort; 值分布均匀用 bucket sort。")
doc.h3("算法")
nc.steps(doc, "排序。", "算所有相邻的差, 找最小值。", "再扫一遍, 收集差等于最小值的相邻 pair。")
SVG("mindiff_core", "排序之后只看相邻: 隔着的 pair 差一定更大。")
doc.h3("手动走一遍")
SVG("mindiff_trace", "排序后逐对计算相邻的差。")
doc.h3("复杂度")
doc.p("Time <code>O(n log n)</code>, Space <code>O(n)</code> (排序)。")
nc.solution(doc, MINDIFF, LARGEST)
doc.note("\"最近 / 最小差 / 重叠 / 去重\": 先排序, 之后只看相邻的。")

# ================================================================ 9
doc.h2("9. Roman to Integer")
doc.h3("题目在问什么")
doc.p("把罗马数字转成整数。I=1, V=5, X=10, L=50, C=100, D=500, M=1000。一般大的在左、小的在右, 加起来; 但如果小的写在大的<b>左边</b>, 表示相减, 比如 IV = 4, IX = 9, CM = 900。")
doc.h3("看例子")
doc.svg(EXS % "roman", "两个例子。")
doc.h3("Brute force")
doc.p("列出所有的减法组合 (IV、IX、XL、XC、CD、CM), 先匹配两个字符, 匹配不上再按一个字符算。可以做, 但规则写起来比较多。")
doc.h3("Intuition: 只看右边那个字符")
doc.p("规则可以简化成一句: <b>一个字符如果比它右边的字符小, 就减去它; 否则加上它</b>。最后一个字符没有右边, 一定是加。")
doc.h3("算法")
nc.steps(doc, "建一个 dict 存 7 个字符的值。",
         "从左往右: 如果当前值 < 右边的值, <code>total -= 当前值</code>; 否则 <code>total += 当前值</code>。")
SVG("roman_core", "比右边小就减, 否则加。")
doc.h3("手动走一遍")
SVG("roman_trace", "MCMXCIV 逐个字符的加减。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(1)</code>。")
nc.solution(doc, ROMAN)
doc.note("查表 + 看相邻: 规则如果只取决于相邻两个元素, 扫一遍时看一眼右边。")

# ================================================================ 识别信号
doc.h2("10. 识别信号: 看到什么, 就想到什么")
nc.table(doc, ["题目特征", "做法", "complexity"], [
    ["矩阵按圈 / 螺旋遍历", "4 个边界变量, 走完一条边收缩", "空间 <code>O(m·n)</code> → <code>O(1)</code>"],
    ["矩阵旋转 / 翻转", "写出坐标变换, 拆成 transpose + 反转", "空间 <code>O(n²)</code> → <code>O(1)</code>"],
    ["原地 + O(1) 空间的标记", "借输入的一部分存标记 (第一行 / 第一列 / 正负号)", "空间 <code>O(m + n)</code> → <code>O(1)</code>"],
    ["n 很大的重复操作 (幂)", "按 n 的二进制拆, 不断平方", "<code>O(n)</code> → <code>O(log n)</code>"],
    ["处理整数的每一位", "% 10 取末位, // 10 去末位", "不需要转字符串"],
    ["成对出现, 找落单的 / 缺的", "XOR 全部", "空间 <code>O(n)</code> → <code>O(1)</code>"],
    ["数二进制的 1 / 判断 2 的幂", "n & (n - 1)", "<code>O(位数)</code> → <code>O(1 的个数)</code>"],
    ["最近 / 最小差 / 重叠 / 去重", "排序后只看相邻", "<code>O(n²)</code> → <code>O(n log n)</code>"],
    ["规则只和相邻元素有关", "扫一遍, 看右边一个", "<code>O(n)</code>"]])

doc.h2("以后再学")
doc.p("Game of Life (原地用多个状态值标记)、Sqrt(x) (二分或 Newton 法)、Reverse Bits、Counting Bits (dp[i] = dp[i >> 1] + (i & 1))、Multiply Strings (竖式乘法)。")
doc.write("docs/19-matrix-math-bit.html")
