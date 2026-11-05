# 06 · Stack 正文 (NeetCode 式讲法)。由 06_stack.py 末尾 exec, 共用 CODE / show / load / SLUG。
import nclib as nc
from counts import cnt

EX = os.path.join(d.ROOT, "docs", "svg", SLUG, "%s_examples.svg")

# ---------------------------------------------------------------- 例子图
f = load("valid")["is_valid"]
assert f("()[]{}") and not f("(]") and not f("([)]") and f("{[()]}")
nc.examples_svg(EX % "valid", "Valid Parentheses examples",
                ["字符串只有 ( ) [ ] { }。每个开括号都要被同类型的闭括号关上, 而且要按正确的顺序 (里面的先关)"], [
    dict(title="Example 1:  \"()[]{}\"  →  True", items=list("()[]{}"), hl=[0, 1, 2, 3, 4, 5], ans_text="三对, 各自配好"),
    dict(title="Example 2:  \"{[()]}\"  →  True", items=list("{[()]}"), hl=[0, 1, 2, 3, 4, 5], ans_text="一层套一层, 最里面的先关"),
    dict(title="Example 3:  \"([)]\"  →  False", items=list("([)]"), bad=[(1, 2, "[ 还没关, 就来了 ) ✗")],
         extra=["数量是够的 (一个 ( 一个 ) 一个 [ 一个 ]), 但顺序不对: 后开的 [ 必须先关"])],
    legend=[("new", "配好的"), ("rem", "顺序错了")])

nc.examples_svg(EX % "minstack", "Min Stack examples",
                ["设计一个 stack, 支持 push / pop / top, 外加 getMin (返回当前栈里最小的数)。每个操作都要 O(1)"], [
    dict(title="Example:  依次 push 5, 3, 7, 3, 然后 pop 三次",
         index=False, rows=[
             ("push 完", [5, 3, 7, 3], ["keep", "new", "keep", "new"]),
             ("pop 两次", [5, 3], ["keep", "new"]),
             ("再 pop", [5], ["new"])],
         extra=["getMin: push 完是 3; pop 两次后还是 3; 再 pop 一次变成 5", "难点在 pop: 最小值 3 被 pop 掉以后, 怎么 O(1) 知道下一个最小值是谁?"])],
    legend=[("new", "当前最小值")])

f = load("decode")["decode_string"]
assert f("3[a]2[bc]") == "aaabcbc" and f("3[a2[c]]") == "accaccacc" and f("2[abc]3[cd]ef") == "abcabccdcdcdef"
nc.examples_svg(EX % "decode", "Decode String examples",
                ["k[s] 表示把 s 重复 k 次。可以嵌套。把字符串展开"], [
    dict(title="Example 1:  \"3[a]2[bc]\"  →  \"aaabcbc\"", extra=["3[a] → aaa,  2[bc] → bcbc,  接起来"]),
    dict(title="Example 2:  \"3[a2[c]]\"  →  \"accaccacc\"",
         extra=["先展开里面: 2[c] → cc, 于是变成 3[acc] → accaccacc", "嵌套时必须先算里面, 再算外面"]),
    dict(title="Example 3:  \"2[abc]3[cd]ef\"  →  \"abcabccdcdcdef\"", extra=["括号外面的普通字母 ef 直接接上"])],
    legend=[])

f = load("rpn")["eval_rpn"]
assert f(["2", "1", "+", "3", "*"]) == 9 and f(["4", "13", "5", "/", "+"]) == 6
nc.examples_svg(EX % "rpn", "Evaluate RPN examples",
                ["Reverse Polish Notation: 运算符写在两个操作数后面。例如 \"2 1 +\" 表示 2 + 1。算出结果 (除法向 0 取整)"], [
    dict(title="Example 1:  [\"2\",\"1\",\"+\",\"3\",\"*\"]  →  9", items=["2", "1", "+", "3", "*"],
         extra=["2 1 + → 3;  再 3 3 * → 9。也就是 (2 + 1) × 3"]),
    dict(title="Example 2:  [\"4\",\"13\",\"5\",\"/\",\"+\"]  →  6", items=["4", "13", "5", "/", "+"],
         extra=["13 5 / → 2 (13 / 5 = 2.6, 向 0 取整);  再 4 2 + → 6。也就是 4 + 13 / 5"])],
    legend=[("keep", "token")])

f = load("calc2")["calculate"]
assert f("3+2*2") == 7 and f(" 3/2 ") == 1 and f("3+5*2-6/3") == 11
nc.examples_svg(EX % "calc2", "Basic Calculator II examples",
                ["字符串里有非负整数和 + - * / 和空格, 没有括号。按正常的运算优先级 (先乘除后加减) 算出结果, 除法向 0 取整"], [
    dict(title="Example 1:  \"3+2*2\"  →  7", extra=["先算 2*2 = 4, 再 3 + 4 = 7。如果从左往右直接算, 会得到 (3+2)*2 = 10, 错"]),
    dict(title="Example 2:  \"3+5*2-6/3\"  →  11", extra=["3 + 10 - 2 = 11"])],
    legend=[])

f = load("calc")["calculate"]
assert f("1 + 1") == 2 and f("(1+(4+5+2)-3)+(6+8)") == 23 and f("1-(2+3)") == -4
nc.examples_svg(EX % "calc", "Basic Calculator examples",
                ["字符串里有非负整数、+ -、括号和空格 (没有 * /)。算出结果。负号也可以出现在括号前面"], [
    dict(title="Example 1:  \"1-(2+3)\"  →  -4", extra=["括号里先算出 5, 外面是 1 - 5 = -4。注意括号前的减号会把括号里每一项都变号"]),
    dict(title="Example 2:  \"(1+(4+5+2)-3)+(6+8)\"  →  23", extra=["(1 + 11 - 3) + 14 = 9 + 14 = 23, 括号可以嵌套"])],
    legend=[])

f = load("asteroid")["asteroid_collision"]
assert f([5, 10, -5]) == [5, 10] and f([8, -8]) == [] and f([10, 2, -5]) == [10]
nc.examples_svg(EX % "asteroid", "Asteroid Collision examples",
                ["每个数是一颗小行星: 绝对值是大小, 正号向右飞, 负号向左飞。迎面相撞时小的爆炸, 一样大就都爆炸。求最后剩下的"], [
    dict(title="Example 1:  [5,10,-5]  →  [5,10]", items=[5, 10, -5], hl=[0, 1], bad=[(2, 2, "-5 撞上 10, 5 < 10, -5 爆炸")]),
    dict(title="Example 2:  [8,-8]  →  []", items=[8, -8], bad=[(0, 1, "一样大, 一起爆炸")]),
    dict(title="Example 3:  [10,2,-5]  →  [10]", items=[10, 2, -5], hl=[0],
         bad=[(1, 2, "-5 先撞掉 2, 再撞 10 时自己爆炸")],
         extra=["一颗向左飞的可以连续撞掉好几颗。而 [-2, 3] 这种 (左边的向左、右边的向右) 永远不会相撞"])],
    legend=[("new", "最后剩下的"), ("rem", "相撞")])

f = load("dup2")["remove_duplicates"]
assert f("abcd", 2) == "abcd" and f("deeedbbcccbdaa", 3) == "aa"
nc.examples_svg(EX % "dup2", "Remove All Adjacent Duplicates II examples",
                ["只要有 k 个相同的字符连在一起, 就把它们删掉。删完以后左右两边接起来, 可能又凑成 k 个, 继续删, 直到删不动"], [
    dict(title="Example:  s = \"deeedbbcccbdaa\", k = 3  →  \"aa\"", items=list("deeedbbcccbdaa"), cw=30,
         extra=["删 eee → \"ddbbcccbdaa\";  删 ccc → \"ddbbbdaa\";  删 bbb → \"dddaa\";  删 ddd → \"aa\"",
                "每删一次, 两边接上可能又凑出新的 k 个"])],
    legend=[])

f = load("path")["simplify_path"]
assert f("/home/") == "/home" and f("/a/./b/../../c/") == "/c" and f("/home//foo/") == "/home/foo"
nc.examples_svg(EX % "path", "Simplify Path examples",
                ["Unix 路径化简: '.' 表示当前目录, '..' 表示上一级, 多个 '/' 当一个。返回最简的绝对路径"], [
    dict(title="Example 1:  \"/home//foo/\"  →  \"/home/foo\"", extra=["连续的 // 当成一个 /, 末尾的 / 去掉"]),
    dict(title="Example 2:  \"/a/./b/../../c/\"  →  \"/c\"", extra=["进 a → 原地 (.) → 进 b → 退回 a (..) → 退回根 (..) → 进 c"]),
    dict(title="Example 3:  \"/../\"  →  \"/\"", extra=["已经在根目录了, 再 .. 还是根目录"])],
    legend=[])

# ================================================================ HTML
doc = d.Doc("06 · Stack")
doc.h2("这篇讲什么")
doc.p("<b>Stack</b> (栈) 是一种只能从顶上放、从顶上拿的容器: 最后放进去的, 最先拿出来 (LIFO, last in first out)。Python 里用 list 就行: <code>append</code> 是放, <code>pop()</code> 是拿, <code>stack[-1]</code> 是看栈顶。都是 <code>O(1)</code>。")
doc.p("什么时候想到 stack? 当你从左往右扫的时候, 需要记住\"<b>最近的、还没处理完的</b>东西\", 而且后来的要先处理。最典型的就是<b>嵌套结构</b>: 括号、嵌套的字符串、表达式里的括号、目录的进入和退出。它们都是\"最里面的先结束\"。")
doc.p("不用 stack 的 brute force, 通常是每遇到一个\"结束\"的东西, 就往回扫去找它对应的\"开始\", <code>O(n²)</code>。stack 让\"往回找\"变成看一眼栈顶, <code>O(1)</code>。")
nc.table(doc, ["#", "题目", "考过的公司数", "相比上一题多了什么"], [
    ["1", "Valid Parentheses", cnt("Valid Parentheses"), "模板题: 栈顶就是最内层还没关的括号"],
    ["2", "Min Stack", cnt("Min Stack"), "每个元素带上额外的信息"],
    ["3", "Decode String", cnt("Decode String"), "遇到 [ 把当前状态存起来, 遇到 ] 拿回来"],
    ["4", "Evaluate Reverse Polish Notation", cnt("Evaluate Reverse Polish Notation"), "栈里存算好的数"],
    ["5", "Basic Calculator II", cnt("Basic Calculator II"), "运算优先级: 乘除立刻算, 加减先存着"],
    ["6", "Basic Calculator", cnt("Basic Calculator"), "加上括号: 和第 3 题一样存状态"],
    ["7", "Asteroid Collision", cnt("Asteroid Collision"), "新来的和栈顶反复\"抵消\""],
    ["8", "Remove All Adjacent Duplicates II", cnt("Remove All Adjacent Duplicates in String II"), "栈里存 (字符, 个数)"],
    ["9", "Simplify Path", cnt("Simplify Path"), "目录的进入和退出"]])
doc.p("每道题的顺序: <b>题目在问什么 → 看例子 → brute force → intuition → 算法 → 手动走一遍 → 复杂度</b>。代码放在最后, 默认折叠。")
doc.p("另一类用 stack 的题是 monotonic stack (找下一个更大的数), 单独放在 07。")

# ================================================================ 1
doc.h2("1. Valid Parentheses")
doc.h3("题目在问什么")
doc.p("字符串里只有 <code>( ) [ ] { }</code> 六种字符。判断它是不是合法的: 每个开括号都要被<b>同类型</b>的闭括号关上, 而且<b>后开的必须先关</b>。")
doc.h3("看例子")
doc.svg(SLUG + "/valid_examples.svg", "三个例子。")
doc.p("Example 3 说明, 只数个数是不够的, 顺序也要对。")
doc.h3("Brute force")
doc.p("每遇到一个闭括号, 就往左扫, 找离它最近的、还没配对的开括号, 检查类型是否一致。每次往左扫 <code>O(n)</code>, 共 <code>O(n²)</code>。")
doc.p("浪费在哪: 每次都从头往左扫, 但其实我们每次要找的都是\"<b>最近的</b>还没配对的开括号\"。")
doc.h3("Intuition: 把还没配对的开括号放进 stack")
doc.p("从左往右扫, 把还没配对的开括号按顺序放进 stack。那么 stack 顶上的, 就是最近的、还没配对的开括号, 正是我们要找的。")
doc.p("遇到闭括号, 看一眼栈顶: 类型对上, 就 pop 掉 (这一对配好了); 对不上或者栈是空的, 就不合法。")
doc.p("为什么是 stack? 因为括号的规则是\"后开的先关\", 和 stack \"后放的先拿\" 完全一样。")
doc.h3("算法")
nc.steps(doc, "<code>stack = []</code>, 准备一个 dict: 闭括号 → 对应的开括号。",
         "遇到开括号: push。",
         "遇到闭括号: 栈空, 或者栈顶不是对应的开括号, 返回 False; 否则 pop。",
         "扫完后, 栈必须是空的 (没有多出来的开括号)。")
doc.svg(SLUG + "/stack_core.svg", "stack 里存的是\"往左扫会碰到的候选\", 最近的在栈顶。嵌套的括号永远是最内层先配, 正好是 LIFO。")
doc.svg(SLUG + "/valid_core.svg", "stack = 还没关的开括号。闭括号只和栈顶比。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/valid_trace.svg", "\"{[()]}\": 三层嵌套, 栈深到 3, 再一层一层 pop 回空。pop 掉的开括号在左边标出了和谁配对。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>: 每个字符最多 push 一次、pop 一次。Space <code>O(n)</code>。")
nc.solution(doc, show(CODE["valid"]))
doc.note("嵌套结构 / 括号配对: 还没处理完的放进 stack, 栈顶就是最近的那个。")

doc.h2("把第 1 题抽象一下: 什么时候用 stack")
doc.p("第 1 题的结构是: 从左往右扫, 每个\"开始\"先存起来, 等到对应的\"结束\"出现时再处理, 而且最近开始的最先结束。")
doc.p("后面的题都是这个结构, 区别在于 stack 里存什么:")
nc.bullets(doc, "存元素本身 (第 1、4、7、9 题)",
           "存元素 + 额外信息, 比如当时的最小值、连续个数 (第 2、8 题)",
           "存\"进入括号之前的状态\", 出括号时恢复 (第 3、6 题)")
nc.solution(doc, show(CODE["match_brute"] + CODE["match_stack"]), summary="对比: 往左扫找配对 (brute force) 和 用 stack")
doc.note("看到\"最近的、还没处理完的\"或者嵌套结构, 就想 stack。关键是想清楚 stack 里存什么。")

# ================================================================ 2
doc.h2("2. Min Stack")
doc.h3("题目在问什么")
doc.p("设计一个 stack, 支持 <code>push</code>、<code>pop</code>、<code>top</code>, 再加一个 <code>getMin</code>: 返回当前栈里最小的数。<b>每个操作都要 <code>O(1)</code></b>。")
doc.h3("看例子")
doc.svg(SLUG + "/minstack_examples.svg", "例子。")
doc.h3("Brute force")
doc.p("getMin 时把栈扫一遍, <code>O(n)</code>。不满足要求。")
doc.p("另一个想法: 用一个变量 <code>cur_min</code> 记最小值, push 时更新。但 pop 掉的恰好是最小值时, 不知道新的最小值是谁, 还是要扫一遍。")
doc.h3("Intuition: 每个元素记住\"它放进来的时候, 栈里的最小值\"")
doc.p("关键观察: stack 只能从顶上拿。所以当某个元素在栈顶时, 它下面的元素和它被放进来那一刻<b>完全一样</b>。")
doc.p("那么在 push 的时候, 就把\"包括我在内, 当前栈里的最小值\"和元素一起存进去: <code>(val, min_so_far)</code>。"
      "之后任何时候, 栈顶的 min_so_far 就是整个栈的最小值。pop 掉以后, 新的栈顶自带它那一刻的最小值, 也是对的。")
doc.h3("算法")
nc.steps(doc, "push(x): 新的最小值 = <code>min(x, 栈顶的 min)</code> (栈空时就是 x)。push <code>(x, 新的最小值)</code>。",
         "pop(): 直接 pop。", "top(): 返回栈顶的 val。", "getMin(): 返回栈顶的 min。")
doc.svg(SLUG + "/minstack_core.svg", "只用一个变量记 min, pop 之后就失效了; 每个元素自带 min_so_far, pop 之后下面的元素的 min 本来就是对的。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/minstack_trace.svg", "每次 push 的 min 只看栈顶的 min; pop 时 (7,3)、(3,3) 带着自己的 min 一起走。")
doc.h3("复杂度")
doc.p("每个操作 Time <code>O(1)</code>。Space <code>O(n)</code>。")
nc.solution(doc, show(CODE["minstack"]))
doc.note("stack 的每个元素可以带额外信息。因为栈顶下面的部分不会变, \"放进来那一刻的信息\"一直有效。")

# ================================================================ 3
doc.h2("3. Decode String")
doc.h3("题目在问什么")
doc.p("编码规则是 <code>k[s]</code>: 把 s 重复 k 次。可以嵌套, 比如 <code>3[a2[c]]</code>。把字符串完全展开。")
doc.h3("看例子")
doc.svg(SLUG + "/decode_examples.svg", "三个例子。")
doc.p("Example 2 说明, 嵌套时必须先展开里面的, 再展开外面的。")
doc.h3("Brute force")
doc.p("反复找最里面的一对 <code>[ ]</code> (里面没有别的括号), 展开它, 拼回字符串, 再找下一个。每次查找和拼接都是 <code>O(长度)</code>, 嵌套多时很慢。")
doc.h3("Intuition: 进括号前把\"外面的状态\"存起来")
doc.p("从左往右读。用 <code>cur</code> 记当前这一层已经拼出来的字符串, <code>k</code> 记刚读到的数字。")
doc.p("遇到 <code>[</code>: 要进入新的一层了。但外面这一层还没完, 它的 cur 和 k 要先存起来, 进去以后才能回来接着拼。"
      "于是 push <code>(cur, k)</code>, 然后 cur 清空, 开始拼里面这一层。")
doc.p("遇到 <code>]</code>: 里面这一层拼完了。pop 出外面的 <code>(prev, k)</code>, 把里面的 cur 重复 k 次接到 prev 后面, 这就是外面这一层新的 cur。")
doc.p("和第 1 题一样: 最后进入的一层最先结束, 所以用 stack。")
doc.h3("算法")
nc.steps(doc, "<code>cur = \"\"</code>, <code>k = 0</code>, <code>stack = []</code>。",
         "数字: <code>k = k * 10 + 数字</code> (数字可能有好几位)。",
         "<code>[</code>: push <code>(cur, k)</code>, 然后 <code>cur = \"\"</code>, <code>k = 0</code>。",
         "<code>]</code>: <code>prev, times = stack.pop()</code>, <code>cur = prev + cur * times</code>。",
         "字母: <code>cur += 字母</code>。最后返回 cur。")
doc.svg(SLUG + "/decode_core.svg", "每个 [ 开一层: stack 存 (prev_str, k); 读到 ] 时 pop 最近的一层, 把里面的 cur 重复 k 次接到 prev_str 后面。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/decode_trace.svg", "3[a2[c]]: stack 最深 2 层, 每个 ] pop 回一层, cur 从 'c' 变成 'acc' 再变成 'accaccacc'。")
doc.h3("复杂度")
doc.p("Time <code>O(n + 输出长度)</code>。Space <code>O(n + 输出长度)</code>。")
nc.solution(doc, show(CODE["decode"]))
doc.note("嵌套结构: 进入新的一层前, 把当前层的状态 push; 离开时 pop 回来, 合并结果。")

# ================================================================ 4
doc.h2("4. Evaluate Reverse Polish Notation")
doc.h3("题目在问什么")
doc.p("RPN (逆波兰表达式) 把运算符写在两个操作数<b>后面</b>: <code>2 1 +</code> 就是 2 + 1。给一个 token 列表, 算出结果。除法向 0 取整。")
doc.h3("看例子")
doc.svg(SLUG + "/rpn_examples.svg", "两个例子。")
doc.h3("Brute force")
doc.p("反复找第一个运算符, 用它前面两个数算出结果, 替换回列表。每次替换 <code>O(n)</code>, 共 <code>O(n²)</code>。")
doc.h3("Intuition")
doc.p("读到运算符时, 它要用的两个操作数, 恰好是<b>最近</b>算出来的两个数。所以把数都放进 stack: 读到数就 push; 读到运算符就 pop 两个, 算完 push 回去。")
doc.p("注意顺序: 先 pop 出来的是<b>右边</b>的操作数 b, 后 pop 的是左边的 a。减法和除法要算 <code>a - b</code>、<code>a / b</code>。")
doc.h3("算法")
nc.steps(doc, "数字: push。",
         "运算符: <code>b = pop()</code>, <code>a = pop()</code>, push <code>a op b</code>。除法用 <code>int(a / b)</code> 向 0 取整。",
         "最后栈里只剩一个数, 就是结果。")
doc.svg(SLUG + "/rpn_core.svg", "读到 +: pop 两个 (先 b 后 a), 算出 a + b, push 回去。栈里永远是\"已经算好的值\"。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/rpn_trace.svg", "每个运算符 pop 两个、push 一个, 栈高度减 1; 最后栈里剩 [12]。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(n)</code>。")
nc.solution(doc, show(CODE["rpn"]))
doc.note("后缀表达式: 数 push, 运算符 pop 两个算完 push 回去。先 pop 的是右操作数。")

# ================================================================ 5
doc.h2("5. Basic Calculator II")
doc.h3("题目在问什么")
doc.p("字符串里有非负整数、<code>+ - * /</code> 和空格, <b>没有括号</b>。按正常优先级 (先乘除、后加减) 算出结果。除法向 0 取整。")
doc.h3("看例子")
doc.svg(SLUG + "/calc2_examples.svg", "两个例子。")
doc.h3("Brute force")
doc.p("先扫一遍把所有 * / 算掉, 再扫一遍算 + -。或者反复找优先级最高的运算符替换。")
doc.h3("Intuition: 加减先存着, 乘除马上算")
doc.p("难点是优先级: 读到 <code>3 + 2</code> 时不能马上加, 因为后面可能是 <code>* 2</code>。")
doc.p("换个角度看: 整个表达式其实是若干\"项\"相加, 每一项是由 * / 连起来的。比如 <code>3 + 5*2 - 6/3</code> = <code>3</code> + <code>(5*2)</code> + <code>(-6/3)</code>。")
doc.p("所以用一个 stack 存每一项:")
nc.bullets(doc, "一个数前面是 <code>+</code>: push 这个数 (新的一项)。",
           "前面是 <code>-</code>: push 它的相反数 (把减法当成加一个负数)。",
           "前面是 <code>*</code> 或 <code>/</code>: 它属于上一项, pop 出栈顶, 乘或除完再 push 回去。")
doc.p("最后把 stack 里所有项加起来。")
doc.h3("算法")
nc.steps(doc, "<code>num = 0</code>, <code>op = '+'</code> (第一个数前面假装有个 +)。",
         "读到数字就拼进 num。读到运算符 (或者到了字符串末尾) 时, 按<b>上一个</b>运算符 op 处理 num: + push, - push 负数, * / 和栈顶合并。然后 op 换成当前的运算符, num 清零。",
         "返回 <code>sum(stack)</code>。")
doc.svg(SLUG + "/calc2_core.svg", "从左往右直接算会把 2-3*2 算成 -2; 按项切开, 加减项 push, 乘除和栈顶合并, 最后求和得到 -4。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/calc2_trace.svg", "3+5*2-6/3: 遇到 * 时 pop 出 5 算成 10 再 push; 遇到 / 时 pop 出 -6 算成 -2 再 push; 最后 sum = 11。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(n)</code> (可以只用一个变量记最后一项, 降到 <code>O(1)</code>)。")
nc.solution(doc, show(CODE["calc2"]))
doc.note("有优先级的表达式: 加减的项先 push, 乘除马上和栈顶合并, 最后求和。")

# ================================================================ 6
doc.h2("6. Basic Calculator")
doc.h3("题目在问什么")
doc.p("字符串里有非负整数、<code>+ -</code>、<b>括号</b>和空格 (没有 * /)。算出结果。括号可以嵌套, 括号前面可以是负号。")
doc.h3("看例子")
doc.svg(SLUG + "/calc_examples.svg", "两个例子。")
doc.h3("Brute force")
doc.p("反复找最里面的一对括号, 算出里面的值, 替换回去。<code>O(n²)</code>。")
doc.h3("Intuition: 和第 3 题一样, 进括号前存状态")
doc.p("没有括号时很简单: 用 <code>result</code> 记到目前为止的结果, <code>sign</code> 记下一个数前面是 + 还是 -, 读到数就 <code>result += sign * num</code>。")
doc.p("加上括号: 遇到 <code>(</code> 时, 括号里是一个独立的小表达式, 要先算。外面的 result 和括号前的 sign 要存起来。于是 push <code>(result, sign)</code>, 然后 result 清零, 开始算括号里面。")
doc.p("遇到 <code>)</code>: 括号里算完了, 值是 result。pop 出外面的 <code>(prev_result, prev_sign)</code>, 合并: <code>result = prev_result + prev_sign * result</code>。")
doc.p("这和第 3 题 Decode String 是同一个结构: 进入一层前存状态, 出来时取回状态并合并。")
doc.h3("算法")
nc.steps(doc, "<code>result = 0</code>, <code>sign = 1</code>, <code>num = 0</code>。",
         "数字: 拼进 num。<code>+</code> / <code>-</code>: 先 <code>result += sign * num</code>, num 清零, 再设 sign = 1 或 -1。",
         "<code>(</code>: push <code>(result, sign)</code>, 然后 result = 0, sign = 1。",
         "<code>)</code>: 先把 num 加进 result, 然后 pop 出 (prev, s), <code>result = prev + s * result</code>。",
         "最后 <code>result += sign * num</code>。")
doc.svg(SLUG + "/calc_core.svg", "1-(2+3): 读 ( 时 push (1, -1) 并清零; 括号里算出 5; 读 ) 时 pop, 1 + (-1) × 5 = -4。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/calc_trace.svg", "1-(2+(3-1)): 嵌套两层, 栈深到 2。每个 ) 先把 num 加进去, 再 pop 合并。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(括号深度)</code>。")
nc.solution(doc, show(CODE["calc"]))
doc.note("表达式里的括号: ( 时 push (result, sign) 并清零, ) 时 pop 合并。和 Decode String 是同一个套路。")

# ================================================================ 7
doc.h2("7. Asteroid Collision")
doc.h3("题目在问什么")
doc.p("一排小行星, 每个用一个整数表示: 绝对值是大小, 正数向右飞, 负数向左飞。两颗<b>迎面</b>相撞时, 小的爆炸; 一样大就一起爆炸。同方向的永远不会撞。求最后剩下的小行星。")
doc.h3("看例子")
doc.svg(SLUG + "/asteroid_examples.svg", "三个例子。")
doc.p("只有\"左边的向右飞、右边的向左飞\"才会相撞。Example 3 里一颗向左飞的可以连续撞掉好几颗。")
doc.h3("Brute force")
doc.p("反复扫整个数组, 找相邻的一对 (正, 负), 让它们相撞, 直到没有可以撞的。每轮 <code>O(n)</code>, 最多 n 轮, <code>O(n²)</code>。")
doc.h3("Intuition: 新来的只会和\"最近的幸存者\"相撞")
doc.p("从左往右处理。已经处理过的、目前还活着的小行星放在 stack 里。一颗新的小行星来了:")
nc.bullets(doc, "如果它向右飞, 或者栈顶向左飞, 不会撞, 直接 push。",
           "如果它向左飞, 而栈顶向右飞, 会撞。比较大小: 栈顶小, 栈顶爆炸 (pop), 新的继续和下一个栈顶撞; 一样大, 都爆炸; 新的小, 新的爆炸。")
doc.p("为什么只看栈顶? 因为新来的向左飞, 第一个碰到的一定是它左边最近的那个幸存者, 也就是栈顶。")
doc.h3("算法")
nc.steps(doc, "对每颗 a: 当 <code>a < 0</code> 且栈顶 <code>> 0</code>: 比较 <code>-a</code> 和栈顶。",
         "栈顶小: pop, 继续比较 (while 循环)。一样大: pop, a 也没了, 停。栈顶大: a 没了, 停。",
         "a 还活着, push。")
doc.svg(SLUG + "/asteroid_core.svg", "只有\"栈顶向右 + 新来的向左\"会撞; 撞的时候三种结果, 分别是 pop / 一起爆炸 / 新的消失。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/asteroid_trace.svg", "-8 撞不过 10 被炸掉; -12 连续撞掉 10 和 5 (一个 while 里 pop 两次) 后 push; 3 和 -12 方向相背, 直接 push。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>: 每颗最多 push 一次、pop 一次。Space <code>O(n)</code>。")
nc.solution(doc, show(CODE["asteroid"]))
doc.note("新元素和\"最近的幸存者\"反复抵消: 用 stack, while 循环和栈顶比, 能消就 pop。")

# ================================================================ 8
doc.h2("8. Remove All Adjacent Duplicates in String II")
doc.h3("题目在问什么")
doc.p("给一个字符串 s 和整数 k。只要有 k 个<b>相同的字符连在一起</b>, 就把它们删掉, 左右两边接上。接上之后可能又凑出 k 个, 继续删, 直到删不动为止。")
doc.h3("看例子")
doc.svg(SLUG + "/dup2_examples.svg", "例子: 每删一次, 两边接上可能又凑出新的 k 个。")
doc.h3("Brute force")
doc.p("反复扫字符串, 找连续 k 个相同的, 删掉, 重新扫。每次 <code>O(n)</code>, 最多删 n/k 次, <code>O(n²/k)</code>。")
doc.h3("Intuition: stack 里存 (字符, 连续个数)")
doc.p("从左往右, 用 stack 记录\"目前还留着的字符串\"。但如果 stack 只存字符, 每次都要往回数有几个相同的。")
doc.p("所以存 <code>[字符, 连续个数]</code>: 新来的字符和栈顶字符一样, 就把栈顶的个数加 1; 不一样, push <code>[字符, 1]</code>。个数到了 k, 就把这一项整个 pop 掉。")
doc.p("pop 之后, 下面那一项自动成了栈顶。如果后面来的字符和它一样, 就会继续累加, 这正好对应\"删完两边接上\"。")
doc.h3("算法")
nc.steps(doc, "对每个字符 c: 栈顶字符是 c, 个数加 1; 否则 push <code>[c, 1]</code>。",
         "栈顶个数 == k: pop。",
         "最后把每项的 <code>字符 × 个数</code> 拼起来。")
doc.svg(SLUG + "/dup2_core.svg", "只存字符的话要回头数; 存 (字符, 个数), 个数到 k 就整段 pop, 下面的段自动接上。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/dup2_trace.svg", "abbbaac, k = 3: (b,3) 凑够被 pop, 露出 (a,1); 后面的 a 把它加到 (a,2), 再到 (a,3), 又被 pop。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(n)</code>。")
nc.solution(doc, show(CODE["dup2"]))
doc.note("连续相同的元素要整段处理: stack 里存 (值, 连续个数)。")

# ================================================================ 9
doc.h2("9. Simplify Path")
doc.h3("题目在问什么")
doc.p("给一个 Unix 风格的绝对路径, 化简它: <code>.</code> 表示当前目录 (不动), <code>..</code> 表示回到上一级, 连续的 <code>/</code> 当成一个。结果以 <code>/</code> 开头, 末尾没有 <code>/</code>。")
doc.h3("看例子")
doc.svg(SLUG + "/path_examples.svg", "三个例子。")
doc.h3("Brute force")
doc.p("反复用字符串替换去掉 <code>/./</code>、<code>//</code>、<code>/xxx/../</code>。规则多, 容易漏, 而且每次替换 <code>O(n)</code>。")
doc.h3("Intuition: stack 就是\"当前所在的目录链\"")
doc.p("先用 <code>split('/')</code> 把路径切成一段一段。然后想象自己在走目录: 进入一个目录就 push 它的名字; <code>..</code> 就是退回上一级, pop; <code>.</code> 和空字符串 (连续 / 切出来的) 不动。")
doc.p("走完之后, stack 从底到顶就是最终所在的目录。用 <code>'/' + '/'.join(stack)</code> 拼起来。")
doc.h3("算法")
nc.steps(doc, "<code>for part in path.split('/')</code>:",
         "<code>part == '..'</code>: 栈不空就 pop。<code>part</code> 是空串或 <code>'.'</code>: 跳过。其他: push。",
         "返回 <code>'/' + '/'.join(stack)</code>。")
doc.svg(SLUG + "/path_core.svg", "split 之后有三类: 目录名 push, '..' pop, 空串和 '.' 不动。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/path_trace.svg", "/a/./b/../../c/: 进 a, 进 b, 两次 .. 回到根, 再进 c。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(n)</code>。")
nc.solution(doc, show(CODE["path"]))
doc.note("进入 / 退出、前进 / 撤销 (目录、浏览器历史、undo): 用 stack。")

# ================================================================ 识别信号
doc.h2("10. 识别信号: 看到什么, 就想到 stack")
nc.table(doc, ["题目特征", "做法", "complexity"], [
    ["括号配对 / 合法性", "开括号 push, 闭括号和栈顶比", "<code>O(n²)</code> → <code>O(n)</code>"],
    ["要 O(1) 拿到栈里的最小 / 最大值", "每个元素存 (val, min_so_far)", "getMin <code>O(n)</code> → <code>O(1)</code>"],
    ["嵌套结构展开: k[...]、括号表达式", "进一层 push 当前状态, 出来 pop 合并", "<code>O(n²)</code> → <code>O(n)</code>"],
    ["后缀表达式", "数 push, 运算符 pop 两个", "<code>O(n)</code>"],
    ["有优先级的表达式, 没有括号", "加减项 push, 乘除和栈顶合并, 最后求和", "<code>O(n)</code>"],
    ["新元素和最近的元素反复抵消 / 碰撞", "while 和栈顶比, 能消就 pop", "<code>O(n²)</code> → <code>O(n)</code>"],
    ["连续 k 个相同就消掉", "stack 存 (值, 个数)", "<code>O(n²/k)</code> → <code>O(n)</code>"],
    ["进入 / 退出、前进 / 撤销", "stack 就是当前的路径", "<code>O(n)</code>"],
    ["找每个元素\"下一个更大 / 更小\"的", "monotonic stack → 07", "<code>O(n²)</code> → <code>O(n)</code>"]])

doc.h2("以后再学")
doc.p("Basic Calculator III (同时有括号和 * /, 把第 5、6 题合起来); Number of Atoms (嵌套的化学式); 用 stack 模拟 recursion (iterative DFS)。")
doc.write("docs/06-stack.html")
