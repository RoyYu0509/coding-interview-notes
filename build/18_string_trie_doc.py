# 18 · String + Trie 正文 (NeetCode 式讲法)。由 18_string_trie.py 的 build() exec, 共用 figs / CODE_* / NS / SLUG。
import nclib as nc
from counts import cnt

EX = os.path.join(SVG_DIR, "%s_examples.svg")
EXS = SLUG + "/%s_examples.svg"

# ---------------------------------------------------------------- 例子图
assert NS["LCP"]["longestCommonPrefix"](["flower", "flow", "flight"]) == "fl"
assert NS["LCP"]["longestCommonPrefix"](["dog", "racecar", "car"]) == ""
nc.examples_svg(EX % "lcp", "Longest Common Prefix examples", ["一组字符串, 找它们共同的最长前缀 (从开头开始, 大家都一样的那一段)"], [
    dict(title="Example 1:  [\"flower\",\"flow\",\"flight\"]  →  \"fl\"", index=False, rows=[
        ("flower", list("flower"), ["new", "new", "rem", "keep", "keep", "keep"]),
        ("flow", list("flow"), ["new", "new", "rem", "keep"]),
        ("flight", list("flight"), ["new", "new", "rem", "keep", "keep", "keep"])],
         extra=["第 3 列: o, o, i 不一样, 停"]),
    dict(title="Example 2:  [\"dog\",\"racecar\",\"car\"]  →  \"\"", extra=["第一个字母就不一样"])],
    legend=[("new", "公共前缀"), ("rem", "第一个不同的列")])

A = NS["ATOI"]["myAtoi"]
assert A("42") == 42 and A("   -042") == -42 and A("1337c0d3") == 1337 and A("words 987") == 0 and A("-91283472332") == -2147483648
nc.examples_svg(EX % "atoi", "atoi examples", ["把字符串转成 32 位整数: 跳过开头的空格 → 读一个可选的 +/- → 读连续的数字, 遇到非数字就停 → 超出范围就截到边界"], [
    dict(title="Example 1:  \"   -042\"  →  -42", items=list("   -042"), hl=[3, 4, 5, 6], ans_text="空格跳过, - 是符号, 042 → 42"),
    dict(title="Example 2:  \"1337c0d3\"  →  1337", items=list("1337c0d3"), hl=[0, 1, 2, 3], bad=[(4, 7, "遇到 c 就停, 后面不管")]),
    dict(title="Example 3:  \"words 987\"  →  0", extra=["第一个非空格字符是 w, 不是数字, 什么都读不到 → 0"]),
    dict(title="Example 4:  \"-91283472332\"  →  -2147483648", extra=["超出 32 位范围 [-2³¹, 2³¹ - 1], 截到 -2³¹"])],
    legend=[("new", "读进来的字符"), ("rem", "停下后忽略的")])

assert NS["REV1"]["reverseWords"]("  hello world  ") == "world hello" and NS["REV1"]["reverseWords"]("a good   example") == "example good a"
nc.examples_svg(EX % "rev", "Reverse Words examples", ["把字符串里的单词倒过来排。单词之间可能有多个空格, 开头结尾也可能有空格; 结果里单词之间只留一个空格"], [
    dict(title="Example 1:  \"the sky is blue\"  →  \"blue is sky the\""),
    dict(title="Example 2:  \"  hello world  \"  →  \"world hello\"", extra=["开头和结尾的空格去掉"]),
    dict(title="Example 3:  \"a good   example\"  →  \"example good a\"", extra=["中间的多个空格变成一个"])],
    legend=[])

T = NS["TRIE"]["Trie"]()
T.insert("apple")
assert T.search("apple") and not T.search("app") and T.startsWith("app")
T.insert("app")
assert T.search("app")
nc.examples_svg(EX % "trie", "Implement Trie examples", ["实现 Trie (前缀树): insert(word)、search(word) (完整的 word 在不在)、startsWith(prefix) (有没有 word 以它开头)"], [
    dict(title="Example:  insert(\"apple\")",
         extra=["search(\"apple\") → True", "search(\"app\") → False: 存过的是 apple, app 只是它的前缀, 不是一个完整的 word",
                "startsWith(\"app\") → True", "insert(\"app\") 之后, search(\"app\") → True"])],
    legend=[])

P = ["mobile", "mouse", "moneypot", "monitor", "mousepad"]
assert NS["SUG"]["suggestedProducts"](P, "mouse") == [["mobile", "moneypot", "monitor"], ["mobile", "moneypot", "monitor"],
                                                     ["mouse", "mousepad"], ["mouse", "mousepad"], ["mouse", "mousepad"]]
nc.examples_svg(EX % "sug", "Search Suggestions examples", ["用户一个字母一个字母地输入 searchWord。每输入一个字母, 返回以当前输入为前缀的产品里, 字典序最小的 3 个"], [
    dict(title="Example:  products = [mobile,mouse,moneypot,monitor,mousepad], searchWord = \"mouse\"", index=False,
         extra=["输入 m   → [mobile, moneypot, monitor]", "输入 mo  → [mobile, moneypot, monitor]",
                "输入 mou → [mouse, mousepad]   (只有两个)", "输入 mous、mouse → [mouse, mousepad]"])],
    legend=[])

W = NS["ADD"]["WordDictionary"]()
for w in ("bad", "dad", "mad"):
    W.addWord(w)
assert not W.search("pad") and W.search("bad") and W.search(".ad") and W.search("b..")
nc.examples_svg(EX % "add", "Add and Search Words examples", ["addWord(word) 加一个词; search(word) 判断有没有匹配的词, word 里的 '.' 可以匹配任意一个字母"], [
    dict(title="Example:  addWord(bad) addWord(dad) addWord(mad)",
         extra=["search(\"pad\") → False", "search(\"bad\") → True", "search(\".ad\") → True (bad、dad、mad 都可以)", "search(\"b..\") → True"])],
    legend=[])

bd = [list("oaan"), list("etae"), list("ihkr"), list("iflv")]
assert sorted(NS["WS2"]["findWords"]([r[:] for r in bd], ["oath", "pea", "eat", "rain"])) == ["eat", "oath"]
nc.examples_svg(EX % "ws2", "Word Search II examples", ["和 13 的 Word Search 一样的规则 (上下左右走, 格子不能重复用), 但这次给一组 words, 返回所有能在 board 上找到的"], [
    dict(title="Example:  words = [oath, pea, eat, rain]  →  [eat, oath]", index=False, rows=[
        ("row 0", list("oaan"), ["new", "new", "keep", "keep"]), ("row 1", list("etae"), ["keep", "new", "keep", "keep"]),
        ("row 2", list("ihkr"), ["keep", "new", "keep", "keep"]), ("row 3", list("iflv"), None)],
         extra=["oath: o(0,0) → a(0,1) → t(1,1) → h(2,1) (绿色);  eat: e(1,3) → a(1,2) → t(1,1)",
                "pea 和 rain 找不到"])],
    legend=[("new", "oath 的路径")])

# ================================================================ HTML
doc = d.Doc("18 · String 基本功 + Trie")
doc.h2("这篇讲什么")
doc.p("这一篇分两部分。")
doc.p("前半部分是 <b>Python 处理字符串的基本功</b>。很多 string 题本身不难, 但写的时候容易在细节上出错 (空格、符号、越界), 或者不小心写出 <code>O(n²)</code>。这部分讲两个通用的写法: 用 list + join 拼字符串, 用一个指针 i 一段一段地 parse。")
doc.p("后半部分是 <b>Trie</b> (前缀树)。当有<b>很多个字符串</b>, 而且它们有<b>共同的前缀</b>时, 把它们存成一棵树, 共同的前缀只存一次。查一个前缀、或者同时找很多个词, 都会快很多。")
nc.table(doc, ["#", "题目", "考过的公司数", "相比上一题多了什么"], [
    ["0", "(基本功) str 不可变", "", "拼接用 list + join"],
    ["1", "Longest Common Prefix", cnt("Longest Common Prefix"), "多个字符串按列比较, 引出 Trie"],
    ["2", "String to Integer (atoi)", cnt("String to Integer (atoi)"), "一个指针 i 分阶段 parse"],
    ["3", "Reverse Words in a String", cnt("Reverse Words in a String"), "split 的坑 + 同一个 parse 写法"],
    ["4", "Implement Trie", cnt("Implement Trie (Prefix Tree)"), "Trie 模板"],
    ["5", "Search Suggestions System", cnt("Search Suggestions System"), "Trie 的每个 node 存答案"],
    ["6", "Design Add and Search Words", cnt("Design Add and Search Words Data Structure"), "通配符: 在 Trie 上分叉搜索"],
    ["7", "Word Search II", cnt("Word Search II"), "Trie + backtracking"]])
doc.p("每道题的顺序: <b>题目在问什么 → 看例子 → brute force → intuition → 算法 → 手动走一遍 → 复杂度</b>。代码放在最后, 默认折叠。")

# ================================================================ 0
doc.h2("0. 基本功: str 不可变, 拼接要用 list + join")
doc.p("Python 的 str 是<b>不可变</b>的 (immutable): 一旦创建就不能修改。<code>s += c</code> 看起来是在 s 后面加了一个字符, 实际上是新建了一个字符串, 把 s 的内容和 c 都复制进去。")
doc.p("所以在循环里写 <code>s += c</code>, 第 1 次复制 1 个字符, 第 2 次复制 2 个……第 n 次复制 n 个, 总共 <code>O(n²)</code>。(CPython 有时会偷偷优化成原地追加, 但这是实现细节, 面试里不能依赖。)")
doc.p("正确的写法: 把每一段放进一个 list (<code>append</code> 是 <code>O(1)</code>), 最后用 <code>''.join(parts)</code> 一次拼起来, 总共 <code>O(n)</code>。")
doc.svg(figs["s0_core"], "n = 8 时, += 一共复制 36 个字符, append + join 一共 16 个。n 越大差距越大。")
nc.solution(doc, CODE_S0, CODE_S0_TOOLS, summary="代码: += vs join, 以及常用的 string 工具")
doc.p("常用工具: <code>s.split()</code> (不带参数, 按任意空白切, 自动去掉空串)、<code>s.split(' ')</code> (只按单个空格切, 会留下空串)、<code>ord(c) - ord('a')</code> (字母转 0..25)、<code>c.isalnum()</code>、<code>c.isdigit()</code>、<code>s[::-1]</code> (反转)。")
doc.note("循环里拼字符串: list.append + ''.join, 不要 s += c。")

# ================================================================ 1
doc.h2("1. Longest Common Prefix")
doc.h3("题目在问什么")
doc.p("给一组字符串, 找它们<b>共同的最长前缀</b>。没有就返回空字符串。")
doc.h3("看例子")
doc.svg(EXS % "lcp", "两个例子。")
doc.h3("Brute force")
doc.p("先拿第一个字符串当候选前缀, 再和每个字符串比, 不断缩短。最坏 <code>O(S)</code>, S 是所有字符的总数。这题本身已经是线性的, 重点是写法清楚。")
doc.h3("Intuition: 把字符串上下对齐, 一列一列看")
doc.p("把所有字符串左对齐, 上下排好。从第 0 列开始, 看这一列所有字符串的字符是不是都一样。都一样就继续看下一列; 一旦有一个不一样, 或者某个字符串已经没有这一列了 (太短), 就停。前面的那些列就是答案。")
doc.p("这道题引出一个想法: 如果有<b>很多</b>字符串, 并且经常要问\"有没有以 xxx 开头的\", 每次都这样一列一列比就太慢了。把它们共同的前缀合并起来存, 就是后面要讲的 Trie。")
doc.h3("算法")
nc.steps(doc, "j 从 0 开始, 以 <code>strs[0][j]</code> 为标准。", "对其他每个字符串: 如果 j 越界, 或者字符不同, 返回 <code>strs[0][:j]</code>。", "全部看完, 返回 strs[0]。")
doc.svg(figs["lcp_core"], "把 4 个字符串上下对齐, 一列一列检查; 前 5 列都相同, 第 5 列出现不同就停。")
doc.h3("手动走一遍")
doc.svg(figs["lcp_trace"], "每一行 = 一列。strs[0][j] 是标准, 依次和其他字符串比。")
doc.h3("复杂度")
doc.p("Time <code>O(S)</code>, Space <code>O(1)</code>。")
nc.solution(doc, CODE_LCP)
doc.note("多个字符串比较前缀: 纵向对齐, 一列一列比。")

# ================================================================ 2
doc.h2("2. String to Integer (atoi)")
doc.h3("题目在问什么")
doc.p("把字符串转成一个 32 位有符号整数, 规则是:")
nc.steps(doc, "跳过开头的空格。", "读一个可选的 + 或 -。", "读连续的数字, 遇到不是数字的字符就停, 后面的全部忽略。", "结果超出 <code>[-2³¹, 2³¹ - 1]</code> 就截到边界。什么数字都没读到就返回 0。")
doc.h3("看例子")
doc.svg(EXS % "atoi", "四个例子。")
doc.h3("Brute force")
doc.p("这题没有算法上的难度, 难在规则多、容易漏边界。用一堆 if 判断各种情况很容易写乱。")
doc.h3("Intuition: 一个指针 i, 每个阶段一个循环")
doc.p("用一个下标 i 从左往右走, 把规则拆成几个<b>阶段</b>, 每个阶段只负责一件事, 做完了 i 停在下一阶段的开头:")
nc.bullets(doc, "阶段 1: <code>while s[i] == ' '</code>, i 往前走。", "阶段 2: 如果 s[i] 是 + 或 -, 记下符号, i 往前一格。",
           "阶段 3: <code>while s[i] 是数字</code>, <code>num = num * 10 + 这个数字</code>, i 往前走。", "最后乘上符号, 截到范围内。")
doc.p("每个 while 都要先检查 <code>i < n</code>, 防止越界。这个\"一个指针、分阶段\"的写法可以用在所有 parse 类的题上 (解析表达式、解析路径、解析版本号)。")
doc.h3("算法")
nc.steps(doc, "跳空格 → 读符号 → 读数字 → 乘符号 → 截断。")
doc.svg(figs["atoi_core"], "'  -42x' 被 i 切成 4 段: 空格 (i 从 0 到 2)、符号 (2 到 3)、数字 (3 到 5)、停在 'x'。")
doc.h3("手动走一遍")
doc.svg(figs["atoi_trace"], "每一行 = i 往右走一格。数字阶段 num = num × 10 + d 的每一步都写出了具体数字。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(1)</code>。")
nc.solution(doc, CODE_ATOI)
doc.note("parse 字符串: 一个指针 i, 每个阶段一个 while, 每个 while 先检查 i < n。")

# ================================================================ 3
doc.h2("3. Reverse Words in a String")
doc.h3("题目在问什么")
doc.p("把字符串里的单词顺序倒过来。单词之间可能有多个空格, 开头和结尾也可能有空格。结果里, 单词之间只留一个空格, 开头结尾没有空格。")
doc.h3("看例子")
doc.svg(EXS % "rev", "三个例子。")
doc.h3("最简单的做法")
doc.p("<code>' '.join(reversed(s.split()))</code>, 一行。<code>split()</code> 不带参数时, 会按任意多个空白切, 并且自动去掉空字符串, 正好满足要求。")
doc.p("常见的错误是写成 <code>split(' ')</code>: 它只按单个空格切, 连续的空格会切出空字符串, join 回去就会多出空格。")
doc.svg(figs["rev_core"], "上面是正确做法; 下面是 split(' ') 留下了 4 个空串, join 之后会多出空格。")
doc.h3("如果面试官不让用 split")
doc.p("用第 2 题的写法, 一个指针从右往左走: 先跳过空格, 然后一直走到下一个空格, 中间这一段就是一个单词, 放进结果 list。重复直到走完。")
doc.h3("手动走一遍")
doc.svg(figs["rev_trace"], "每一行读进一个单词 (绿色)。j 是单词的最后一格, i 读完之后停在单词前面一格。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(n)</code>。")
nc.solution(doc, CODE_REVERSE_ONE, CODE_REVERSE_SCAN)
doc.note("按空白切单词用 split() 不带参数。手写的话: 指针跳空格 → 读单词, 重复。")

# ================================================================ 4
doc.h2("4. Implement Trie (Prefix Tree)")
doc.h3("题目在问什么")
doc.p("实现一个 Trie, 支持三个操作: <code>insert(word)</code> 存一个词; <code>search(word)</code> 这个<b>完整的</b>词有没有存过; <code>startsWith(prefix)</code> 有没有存过的词以 prefix 开头。")
doc.h3("看例子")
doc.svg(EXS % "trie", "例子。")
doc.h3("Brute force")
doc.p("把所有词存在一个 list (或 set) 里。search 用 set 是 <code>O(L)</code>; 但 startsWith 要把所有词都检查一遍, <code>O(N · L)</code>。")
doc.p("浪费: \"apple\"、\"app\"、\"apply\" 都以 \"app\" 开头, 这个前缀被存了很多遍, 每次查询也要重复比较很多遍。")
doc.h3("Intuition: 共同的前缀只存一次")
doc.p("把所有词存成一棵树: 每个 node 代表一个字符, 从 root 往下走的一条路径就拼出一个前缀。共同前缀的词共用同一段路径。")
nc.bullets(doc, "每个 node 有一个 <code>children</code> dict: 下一个字符 → 下一个 node。",
           "每个 node 有一个 <code>is_end</code> 标记: 有没有某个词正好在这里结束。这就是 search(\"app\") 和 startsWith(\"app\") 的区别。")
doc.p("insert: 从 root 开始, 一个字符一个字符往下走, 没有对应的 child 就新建一个。走到最后一个字符, 标记 is_end = True。")
doc.p("search / startsWith: 同样往下走, 中途找不到 child 就返回 False。走完之后, search 还要检查 is_end, startsWith 不用。")
doc.h3("算法")
nc.steps(doc, "insert: <code>node = root</code>; 每个字符 c: 不在 children 里就新建; <code>node = node.children[c]</code>。最后 <code>node.is_end = True</code>。",
         "查找前缀 (共用的辅助函数): 往下走, 找不到返回 None, 找到返回最后的 node。",
         "search: 找到了并且 <code>is_end</code>。startsWith: 找到了就行。")
doc.svg(figs["trie_core"], "同样 4 个词: list 里 'ap' 存了 3 次 (红色), trie 里 a、p 只存 1 次 (绿色)。")
doc.h3("手动走一遍")
doc.svg(figs["trie_trace"], "依次 insert 4 个词, 每次新建的 node 是绿色; 复用的 node 是灰色。")
doc.h3("复杂度")
doc.p("每个操作 Time <code>O(L)</code>, L 是词的长度, 和存了多少个词无关。Space 是所有词的字符总数 (共同前缀只算一次)。")
nc.solution(doc, CODE_TRIE)
doc.note("很多字符串、要按前缀查: Trie。node 有 children (dict) 和 is_end。")

# ================================================================ 5
doc.h2("5. Search Suggestions System")
doc.h3("题目在问什么")
doc.p("一组产品名 products 和一个搜索词 searchWord。用户一个字母一个字母地输入 searchWord, 每输入一个字母, 返回以<b>当前已输入的部分</b>为前缀的产品里, 字典序最小的最多 3 个。")
doc.h3("看例子")
doc.svg(EXS % "sug", "例子。")
doc.h3("Brute force")
doc.p("每输入一个字母, 都把所有产品扫一遍, 找出以它开头的, 排序取前 3。<code>O(L · N · L)</code>。")
doc.h3("Intuition: 在 Trie 的每个 node 里直接存好答案")
doc.p("每输入一个字母, 就是在 Trie 上往下走一步。走到的那个 node 代表\"当前输入的前缀\", 它下面的所有词就是以这个前缀开头的产品。")
doc.p("与其每次都去遍历它下面所有的词, 不如在 insert 的时候, 就让每个经过的 node 记住\"以我为前缀的、字典序最小的 3 个词\"。")
doc.p("怎么保证是字典序最小的 3 个? <b>先把 products 排序</b>, 再按顺序 insert。每个 node 只在它的 list 还不满 3 个时才加进去, 这样留下的一定是最小的 3 个。")
doc.h3("算法")
nc.steps(doc, "products 排序。", "insert 每个产品: 往下走的路上, 每个 node 的 <code>top</code> list 如果少于 3 个, 就把这个产品加进去。",
         "查询: 沿着 searchWord 往下走, 每走一步输出那个 node 的 top; 走不下去之后都输出空 list。")
doc.svg(figs["sug_core"], "排序后 mobile、moneypot、monitor 先到, 把 m 和 o 的 top 3 填满了; 后面的 mouse、mousepad 到 m 时已经满了, 只填进更深的 node。")
doc.h3("手动走一遍")
doc.svg(figs["sug_trace"], "搜索 'mouse', 每一行多走一步 (绿色是当前 node), 右边是这个 node 里存的 top 3。")
doc.h3("复杂度")
doc.p("建树 <code>O(N · L)</code> (加上排序), 查询 <code>O(L)</code>。另一种做法: 排序后对每个前缀用二分 (bisect) 找第一个 ≥ 前缀的位置, 往后看 3 个。")
nc.solution(doc, CODE_SUGGEST)
doc.note("每个前缀都要一个答案: 在 Trie 的 node 里预先存好答案。")

# ================================================================ 6
doc.h2("6. Design Add and Search Words Data Structure")
doc.h3("题目在问什么")
doc.p("<code>addWord(word)</code> 加一个词。<code>search(word)</code>: 有没有加过的词能匹配 word, 其中 <code>.</code> 可以匹配任意一个字母。")
doc.h3("看例子")
doc.svg(EXS % "add", "例子。")
doc.h3("Brute force")
doc.p("把所有词存进 list, search 时逐个比较 (. 跳过)。<code>O(N · L)</code>。")
doc.h3("Intuition: 普通字母走一条路, . 就每条路都试")
doc.p("用 Trie 存。search 时, 普通字母和第 4 题一样, 只有一条路可走。遇到 <code>.</code> 时, 它可以是任何字母, 所以要<b>对当前 node 的每个 child 都试一次</b>, 有一个能匹配成功就行。")
doc.p("这就是在 Trie 上做 DFS。没有 . 的时候是一条直线; 每个 . 会让搜索分叉。")
doc.h3("算法")
nc.steps(doc, "<code>dfs(node, i)</code>: i == len(word), 返回 node.is_end。",
         "word[i] 是 .: 对每个 child, 有一个 <code>dfs(child, i + 1)</code> 为 True 就返回 True。",
         "否则: word[i] 在 children 里就继续 dfs, 不在就返回 False。")
doc.svg(figs["add_core"], "普通字母只有一条路; '.' 对每个 child 都要递归一次。")
doc.h3("手动走一遍")
doc.svg(figs["add_trace"], "search('.id'): 在 '.' 处分成 b、d、m 三条路; b 和 d 的 children 里没有 'i', 马上失败。")
doc.h3("复杂度")
doc.p("没有 . 时 <code>O(L)</code>; 最坏 (全是 .) 要遍历整棵 Trie。")
nc.solution(doc, CODE_ADDSEARCH)
doc.note("Trie + 通配符: DFS, 遇到通配符就对所有 child 分叉。")

# ================================================================ 7
doc.h2("7. Word Search II")
doc.h3("题目在问什么")
doc.p("和 13 的 Word Search 规则一样 (在字母 grid 上上下左右走, 同一个格子不能重复用), 但这次给的是<b>一组</b> words, 返回所有能在 board 上找到的词。")
doc.h3("看例子")
doc.svg(EXS % "ws2", "例子。")
doc.h3("Brute force")
doc.p("对每个 word 都跑一遍 13 里的 Word Search。k 个词就跑 k 遍, 每遍 <code>O(m·n · 3^L)</code>。")
doc.p("浪费: 很多词有共同的前缀 (比如 oath、oat、oak)。在 board 上找 \"oa\" 这段路径的工作, 被每个词重复做了一遍。")
doc.h3("Intuition: 把所有 words 放进 Trie, 一次搜索找所有的词")
doc.p("把所有 words 建成一棵 Trie。然后从 board 的每个格子出发做 backtracking, <b>一边在 board 上走, 一边在 Trie 上往下走</b>:")
nc.bullets(doc, "下一个格子的字母, 必须是当前 Trie node 的一个 child, 否则这条路上不可能有任何 word, 直接剪掉。",
           "走到一个 is_end 的 node (在代码里是 node.word 不为空), 就找到了一个词, 加进结果。")
doc.p("这样所有共同前缀的词在 board 上只搜一次。")
doc.p("两个额外的剪枝:")
nc.bullets(doc, "找到一个词之后, 把它从 Trie 里标记掉 (<code>node.word = None</code>), 防止重复加入结果。",
           "如果一个 node 已经没有 children 也没有 word 了, 说明它下面不会再有答案, 把它从 Trie 上摘掉。后面的搜索会越来越快。")
doc.p("board 上的访问标记和 13 一样: 进去时改成 #, 出来时恢复。")
doc.h3("算法")
nc.steps(doc, "所有 words 建 Trie, 每个词的结尾 node 存这个词。",
         "对每个格子: 如果它的字母在 root 的 children 里, 开始 dfs。",
         "dfs(r, c, parent): <code>node = parent.children[字母]</code>。有 word 就加进结果并清掉。标记格子, 对四个邻居 (字母在 node.children 里的) 继续 dfs, 恢复格子。node 变空了就从 parent 里删掉。")
doc.svg(figs["ws2_core"], "board 上的路径 o → a → t → h 和 Trie 里的 o → a → t → h 同步走; Trie 里没有的字母直接剪掉。")
doc.h3("手动走一遍")
doc.svg(figs["ws2_trace"], "6 步走完 4 × 4 board。摘掉的分支用虚线扔到左边; Trie 的 node 数 14 → 10 → 7。")
doc.h3("复杂度")
doc.p("最坏 Time <code>O(m·n · 3^L)</code>, 但因为共享前缀和剪枝, 实际比逐个 word 搜快得多。Space 是 Trie 的大小。")
nc.solution(doc, CODE_WS2)
doc.note("在同一个结构上找很多个词: 把词建成 Trie, 一次 backtracking 同时在 board 和 Trie 上走。")

# ================================================================ 识别信号
doc.h2("8. 识别信号: 看到什么, 就想到什么")
nc.table(doc, ["题目特征", "做法", "complexity"], [
    ["循环里拼字符串", "list.append + ''.join", "<code>O(n²)</code> → <code>O(n)</code>"],
    ["按空白切单词", "split() 不带参数", "<code>O(n)</code>"],
    ["解析数字 / 表达式 / 路径", "一个指针 i, 分阶段 while, 每次先检查 i < n", "<code>O(n)</code>"],
    ["多个字符串的公共前缀", "纵向逐列比较", "<code>O(S)</code>"],
    ["很多字符串 + 按前缀查询", "Trie", "<code>O(N·L)</code> → <code>O(L)</code>"],
    ["每个前缀都要一个答案 (自动补全)", "Trie 的 node 里存好答案", "每次 <code>O(N·L)</code> → <code>O(1)</code>"],
    ["带通配符的匹配", "Trie + DFS 分叉", "最坏遍历整棵树"],
    ["在 grid 上找很多个词", "Trie + backtracking, 找到就剪枝", "比逐个搜快很多"]])

doc.h2("以后再学")
doc.p("KMP / Z-function / Rabin-Karp (单个 pattern 的匹配)、Manacher (回文)、Aho-Corasick (多 pattern 匹配, 是 Trie + fail 指针)。这些只对特定题有用, 面试优先级低。")
doc.write("docs/18-string-trie.html")
