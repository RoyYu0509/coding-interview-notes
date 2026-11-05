# 01 · Hash Table 正文 (NeetCode 式讲法)。由 01_hash_table.py 末尾 exec, 共用 CODE / ns / SLUG。
import nclib as nc
from counts import cnt

EX = os.path.join(SVG_DIR, "%s_examples.svg")

# ---------------------------------------------------------------- 例子图 (数字先用代码算出来)
assert ns["two_sum"]([2, 7, 11, 15], 9) == [0, 1]
assert ns["two_sum"]([3, 2, 4], 6) == [1, 2]
assert ns["two_sum"]([3, 8, 5, 2, 7], 9) == [3, 4]
nc.examples_svg(EX % "two_sum", "Two Sum examples", ["找两个不同位置的数, 加起来正好等于 target, 返回它们的下标"], [
    dict(title="Example 1:  nums = [2,7,11,15], target = 9  →  [0, 1]", items=[2, 7, 11, 15],
         hl=[0, 1], ans_text="2 + 7 = 9"),
    dict(title="Example 2:  nums = [3,2,4], target = 6  →  [1, 2]", items=[3, 2, 4],
         hl=[1, 2], bad=[(0, 0, "3 + 3 = 6, 但同一个位置不能用两次 ✗")], ans_text="2 + 4 = 6"),
    dict(title="Example 3:  nums = [3,8,5,2,7], target = 9  →  [3, 4]", items=[3, 8, 5, 2, 7],
         hl=[3, 4], ans_text="2 + 7 = 9 (后面会用这个例子走一遍)")])

assert ns["contains_nearby_duplicate"]([1, 2, 3, 1], 3) is True
assert ns["contains_nearby_duplicate"]([1, 2, 3, 1, 2, 3], 2) is False
assert ns["contains_nearby_duplicate"]([1, 2, 3, 1, 3], 2) is True
nc.examples_svg(EX % "cd2", "Contains Duplicate II examples",
                ["有没有两个位置 i ≠ j, 值相同, 而且下标差 |i - j| ≤ k"], [
    dict(title="Example 1:  nums = [1,2,3,1], k = 3  →  True", items=[1, 2, 3, 1],
         hl=[0, 3], ans_text="两个 1: 下标 0 和 3, 差 3 ≤ 3"),
    dict(title="Example 2:  nums = [1,2,3,1,2,3], k = 2  →  False", items=[1, 2, 3, 1, 2, 3],
         bad=[(0, 3, "两个 1 差 3 > 2 ✗ (两个 2、两个 3 也都差 3)")]),
    dict(title="Example 3:  nums = [1,2,3,1,3], k = 2  →  True", items=[1, 2, 3, 1, 3],
         hl=[2, 4], bad=[(0, 3, "两个 1 差 3 > 2, 不算")], ans_text="两个 3: 差 2 ≤ 2")])

assert ns["is_anagram"]("anagram", "nagaram") is True
assert ns["is_anagram"]("rat", "car") is False
nc.examples_svg(EX % "anagram", "Valid Anagram examples",
                ["t 是不是 s 把字母换了顺序得到的: 每个字母出现的次数必须完全一样"], [
    dict(title="Example 1:  s = \"anagram\", t = \"nagaram\"  →  True",
         rows=[("s", list("anagram"), None), ("t", list("nagaram"), None)], index=False,
         extra=["两边都是: a × 3, n × 1, g × 1, r × 1, m × 1 → 次数完全一样"]),
    dict(title="Example 2:  s = \"rat\", t = \"car\"  →  False",
         rows=[("s", list("rat"), ["keep", "keep", "rem"]), ("t", list("car"), ["rem", "keep", "keep"])], index=False,
         extra=["s 有 t, t 没有; t 有 c, s 没有 → 次数对不上"])],
    legend=[("keep", "两边都有, 次数一样"), ("rem", "对不上的字母")])

assert ns["first_uniq_char"]("leetcode") == 0
assert ns["first_uniq_char"]("loveleetcode") == 2
assert ns["first_uniq_char"]("aabb") == -1
nc.examples_svg(EX % "first_uniq", "First Unique Character examples",
                ["找第一个在整个字符串里只出现一次的字符, 返回它的下标; 没有就返回 -1"], [
    dict(title="Example 1:  s = \"leetcode\"  →  0", items=list("leetcode"), hl=[0],
         ans_text="l 只出现一次, 而且最靠前"),
    dict(title="Example 2:  s = \"loveleetcode\"  →  2", items=list("loveleetcode"), cw=30, hl=[2],
         bad=[(0, 1, "l 和 o 后面还会再出现 ✗")], ans_text="v"),
    dict(title="Example 3:  s = \"aabb\"  →  -1", items=list("aabb"),
         extra=["每个字符都出现了两次 → -1"])],
    legend=[("new", "答案"), ("rem", "看起来像, 但不对")])

g = ns["group_anagrams"](["eat", "tea", "tan", "ate", "nat", "bat"])
assert sorted(map(sorted, g)) == [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]
nc.examples_svg(EX % "group", "Group Anagrams examples",
                ["把互为 anagram (字母相同、顺序不同) 的词放进同一组"], [
    dict(title="Example 1:  [\"eat\",\"tea\",\"tan\",\"ate\",\"nat\",\"bat\"]",
         rows=[("组 1", ["eat", "tea", "ate"], ["new"] * 3), ("组 2", ["tan", "nat"], ["new"] * 2),
               ("组 3", ["bat"], ["new"])], cw=60, index=False,
         extra=["eat / tea / ate 都是 a, e, t 各一个; tan / nat 都是 a, n, t; bat 自己一组"]),
    dict(title="Example 2:  [\"\"]  →  [[\"\"]]      Example 3:  [\"a\"]  →  [[\"a\"]]",
         extra=["空字符串也是一个词, 自己一组"])],
    legend=[("new", "同一组的词")])

assert ns["longest_consecutive"]([100, 4, 200, 1, 3, 2]) == 4
assert ns["longest_consecutive"]([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
nc.examples_svg(EX % "lcs", "Longest Consecutive Sequence examples",
                ["数组里挑出一些数, 它们是连续的整数 (x, x+1, x+2, ...), 问最多能挑几个。位置不需要相邻"], [
    dict(title="Example 1:  nums = [100,4,200,1,3,2]  →  4", items=[100, 4, 200, 1, 3, 2], cw=44,
         hl=[1, 3, 4, 5], ans_text="1, 2, 3, 4",
         extra=["1, 2, 3, 4 在数组里的位置是乱的 —— 这题只看值, 不看位置。100 和 200 各自只有长度 1"]),
    dict(title="Example 2:  nums = [0,3,7,2,5,8,4,6,0,1]  →  9", items=[0, 3, 7, 2, 5, 8, 4, 6, 0, 1],
         hl=list(range(10)), ans_text="0 到 8",
         extra=["0 出现了两次, 只算一次"])],
    legend=[("new", "答案里的数")])

# ================================================================ HTML
doc = d.Doc("01 · Hash Table / Counting")

doc.h2("这篇讲什么")
doc.p("很多题的 brute force 都长一个样: 外层循环看每个元素, 内层循环再去<b>找</b>某个东西。"
      "比如\"前面有没有一个数和我加起来等于 target\", \"这个字符后面还会不会出现\"。内层每次都要从头找, 所以是 <code>O(n²)</code>。")
doc.p("<b>Hash Table</b> (Python 里就是 <code>dict</code> 和 <code>set</code>) 能在平均 <code>O(1)</code> 时间里回答\"某个 key 在不在, 对应的 value 是什么\"。"
      "所以思路很简单: <b>把以后要找的东西提前存进 dict, 内层循环就变成一次查表</b>。时间从 <code>O(n²)</code> 降到 <code>O(n)</code>, 代价是 <code>O(n)</code> 的额外空间。")
doc.p("这篇的 6 道题覆盖了 Hash Table 的 4 种用法。区别只在于 key 存什么、value 存什么:")
nc.table(doc, ["#", "题目", "考过的公司数", "用法 / 相比上一题多了什么"], [
    ["1", "Two Sum", cnt("Two Sum"), "查\"另一半\": key 是值, value 是下标。总榜第 1"],
    ["2", "Contains Duplicate II", cnt("Contains Duplicate II"), "还是查值, 但多了距离条件, value 要随时更新"],
    ["3", "Valid Anagram", cnt("Valid Anagram"), "不查在不在, 改成<b>数次数</b>"],
    ["4", "First Unique Character in a String", cnt("First Unique Character in a String"), "数完次数, 还要按原来的顺序找"],
    ["5", "Group Anagrams", cnt("Group Anagrams"), "把\"本质相同\"的东西算成同一个 key, 用来分组"],
    ["6", "Longest Consecutive Sequence", cnt("Longest Consecutive Sequence"), "只问在不在, 用 set 代替排序"],
])
doc.p("每道题的顺序: <b>题目在问什么 → 看例子 → brute force → intuition → 算法 → 手动走一遍 → 复杂度</b>。代码放在最后, 默认折叠。")
doc.p("前置知识: 知道 Python 的 <code>dict</code> 和 <code>set</code> 怎么用就够了。")

# ================================================================ 1
doc.h2("1. Two Sum")
doc.h3("题目在问什么")
doc.p("给一个整数数组 <code>nums</code> 和一个整数 <code>target</code>。在数组里找<b>两个不同位置</b>的数, 它们加起来等于 target, 返回这两个位置的下标。题目保证恰好有一个答案。")
doc.h3("看例子")
doc.svg(SLUG + "/two_sum_examples.svg", "三个例子。绿色是答案的两个位置。")
doc.p("Example 2 是一个容易错的点: <code>3 + 3 = 6</code>, 但数组里只有一个 3, 同一个位置不能用两次。")
doc.h3("Brute force: 两两都试")
doc.p("最直接的做法: 每一对 (j, i) 都试一遍, 看 <code>nums[j] + nums[i]</code> 是不是 target。一共大约 <code>n²/2</code> 对, 所以是 <code>O(n²)</code>。")
doc.p("换个角度看这个双层循环: 外层轮到 <code>x = nums[i]</code> 的时候, 内层其实是在前面的数里<b>找一个特定的值</b>, 也就是 <code>target - x</code>。"
      "下面左边就是这个\"一个一个比\"的过程。")
doc.svg(SLUG + "/principle_core.svg", "同一个 x = 7: 左边是 brute force, 把前面的数一个一个比过去 (O(n)); 右边是查表, 一次就知道 (O(1))。")
doc.p("浪费在哪: 轮到第 5 个数时, 内层把前 4 个数扫了一遍。轮到第 6 个数时, 又把同样的这 4 个数 (加上第 5 个) 扫了一遍。<b>前面看过的数, 每一轮都重新看</b>。")
doc.h3("Intuition: 看过的数存起来")
steps = lambda *a: nc.steps(doc, *a)
steps("内层循环要回答的问题是: \"前面有没有 <code>target - x</code>?\"。",
      "如果把前面看过的数都存进一个 dict, 这个问题就是一次 <code>need in seen</code>, 平均 <code>O(1)</code>。",
      "题目要返回下标, 所以 dict 的 key 存值, value 存它的下标。",
      "每个数先<b>查</b>, 再把自己<b>存</b>进去。顺序不能反: 如果先存再查, x 可能会找到它自己 (Example 2 里 3 就会和自己配对)。")
doc.p("这样每一对 (j, i) 都会在轮到后面那个 i 时被发现。因为那时 j 已经在 dict 里了。")
doc.h3("算法")
steps("<code>seen = {}</code>。",
      "从左到右看每个 <code>x = nums[i]</code>。算出 <code>need = target - x</code>。",
      "如果 <code>need</code> 在 seen 里, 返回 <code>[seen[need], i]</code>。",
      "否则把 <code>seen[x] = i</code> 存进去, 继续。")
doc.svg(SLUG + "/two_sum_core.svg", "invariant: 轮到 i 时, seen 里只装着 i 前面的数。先查后存, x 才不会匹配到自己。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/two_sum_trace.svg", "nums = [3,8,5,2,7], target = 9。前 4 步都没找到, 只是把 x → i 存进 seen; 第 5 步 need = 2, 在 seen 里, 返回 [3, 4]。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>: 只扫一遍, 每一步查一次、存一次 dict, 都是平均 <code>O(1)</code>。Space <code>O(n)</code>: seen 最多存 n - 1 个数。")
nc.solution(doc, CODE["two_sum"])
doc.note("找\"另一半\": 先算出我需要什么, 查 dict; 没有, 再把自己存进去。先查后存。")

# ================================================================ 抽象
doc.h2("把第 1 题抽象一下: 什么时候用 Hash Table")
doc.p("Two Sum 的做法可以总结成一句话: <b>如果你发现自己在循环里反复\"找\"某个东西, 就把它提前存进 dict 或 set</b>。")
doc.p("剩下要想的只有两件事: <b>key 存什么, value 存什么</b>。后面 5 道题就是这两件事的不同答案:")
nc.bullets(doc,
           "key = 值, value = 下标: 找另一半 (第 1、2 题)",
           "key = 字符, value = 出现次数: 数频率 (第 3、4 题)",
           "key = 某种\"规范形式\", value = 一组元素: 分组 (第 5 题)",
           "只有 key, 没有 value (set): 只问在不在 (第 6 题)")
nc.solution(doc, CODE["template"], summary="四种用法的通用写法")
doc.note("Hash Table = 用空间换掉一层循环。看到\"在内层循环里找某个东西\", 就问: 能不能把它提前存进 dict / set?")

# ================================================================ 2
doc.h2("2. Contains Duplicate II")
doc.h3("题目在问什么")
doc.p("给一个数组 <code>nums</code> 和一个整数 <code>k</code>。问: 有没有两个不同的位置 i 和 j, 满足 <code>nums[i] == nums[j]</code>, 而且 <code>|i - j| ≤ k</code>。"
      "也就是: 有没有<b>离得足够近</b>的两个相同的数。")
doc.h3("看例子")
doc.svg(SLUG + "/cd2_examples.svg", "三个例子。")
doc.p("Example 3 说明了一件事: 两个 1 离得太远不算, 但这不影响后面两个 3 离得够近。")
doc.h3("Brute force")
doc.p("每个位置 i, 往后看 k 个位置, 有没有和它相等的。<code>O(n·k)</code>。浪费和 Two Sum 一样: 内层在找\"有没有一个和我相同的值\"。")
doc.h3("Intuition")
doc.p("和 Two Sum 一样, 把看过的数存进 dict, key 是值。区别是这次还要判断距离, 所以 value 存下标。")
doc.p("关键问题是: 同一个值出现了好几次, value 存哪一次的下标? 答案是<b>最近的那一次</b>。"
      "因为我们是从左往右扫, 对当前的 i 来说, 越靠后的旧位置离 i 越近。最近的一次都不满足 ≤ k, 更早的那些只会更远。")
doc.p("所以每看到一个数, 不管有没有命中, 都把它的下标<b>覆盖</b>成当前位置。")
doc.h3("算法")
steps("<code>last = {}</code>, 记每个值最近一次出现的下标。",
      "从左到右看 <code>x = nums[i]</code>。如果 x 在 last 里, 并且 <code>i - last[x] ≤ k</code>, 返回 True。",
      "<code>last[x] = i</code> (覆盖成最新的)。",
      "扫完都没有, 返回 False。")
doc.svg(SLUG + "/cd2_core.svg", "两个 3 距离 2, 命中。两个 1 距离 3, 不算, 但 last[1] 仍然要更新成 3。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/cd2_trace.svg", "nums = [1,2,3,1,3], k = 2。i = 3 时没命中, 但把 1 的旧下标覆盖掉 (旧值用虚线扔到左边); i = 4 命中。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>。Space <code>O(n)</code>, last 存所有不同的值。"
      "如果只保留最近 k 个位置的值 (用一个 set, 超出 k 的从 set 里删掉), 空间可以降到 <code>O(k)</code>, 这其实就是 sliding window。")
nc.solution(doc, CODE["cd2"])
doc.note("相同值 + 距离条件: dict 的 value 存\"上次出现的下标\", 每一步都覆盖成最新的。")

# ================================================================ 3
doc.h2("3. Valid Anagram")
doc.h3("题目在问什么")
doc.p("给两个字符串 <code>s</code> 和 <code>t</code> (小写字母)。问: t 是不是 s 的 <b>anagram</b>。anagram 的意思是: 把 s 的字母换个顺序, 能得到 t。"
      "等价的说法: <b>两个字符串里, 每个字母出现的次数都一样</b>。")
doc.h3("看例子")
doc.svg(SLUG + "/anagram_examples.svg", "两个例子。")
doc.h3("Brute force")
doc.p("把两个字符串都排序, 比较是否相同: <code>sorted(s) == sorted(t)</code>。<code>O(n log n)</code>。")
doc.p("这已经不慢了, 但它做了多余的事: 排序是为了把字母排成同样的顺序再一个一个比。可我们只关心<b>每个字母有几个</b>, 顺序是白排的。")
doc.h3("Intuition")
doc.p("直接数次数。给 s 数一张表, 给 t 数一张表, 比较两张表。")
doc.p("可以再省一点: 只用一张表。s 里每个字母 +1, t 里每个字母 -1。如果两个字符串的次数完全一样, 最后每一格都正好抵消成 0。")
doc.p("还有一个常数上的优化: key 只可能是 26 个小写字母, 所以不用 dict, 用一个长度 26 的数组 <code>cnt = [0] * 26</code>, 下标 <code>ord(ch) - 97</code> 就是字母的编号。"
      "这其实就是一个\"key 是 0..25\" 的 Hash Table, 但不用算 hash, 更快。")
doc.h3("算法")
steps("长度不同, 直接返回 False。",
      "<code>cnt = [0] * 26</code>。s 的每个字母 +1, t 的每个字母 -1。",
      "所有格子都是 0, 返回 True; 否则 False。")
doc.svg(SLUG + "/anagram_core.svg", "两个字符串映射到同一张频率表。26 格的数组就是\"下标 = 字母\"的 dict。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/anagram_trace.svg", "s = \"rat\", t = \"car\": 6 步, 最后 t 的格子是 1, c 的格子是 -1, 没抵消, 返回 False。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>。Space <code>O(1)</code>: 数组固定 26 格, 和 n 无关。字符集不固定 (比如 Unicode) 时用 <code>Counter</code>, 空间是 <code>O(字符种类数)</code>。")
nc.solution(doc, CODE["anagram"])
doc.note("和顺序无关的比较 (anagram、两个 multiset 是否相等), 用数次数代替排序。key 范围小而固定, 用数组; 否则用 Counter。")

# ================================================================ 4
doc.h2("4. First Unique Character in a String")
doc.h3("题目在问什么")
doc.p("给一个字符串 <code>s</code>。找到<b>第一个</b>在整个字符串里只出现一次的字符, 返回它的下标。没有就返回 -1。")
doc.h3("看例子")
doc.svg(SLUG + "/first_uniq_examples.svg", "三个例子。")
doc.p("Example 2 里 l 是第一个字符, 但它后面还会出现, 所以不算。要知道\"后面还会不会出现\", 必须看过整个字符串。")
doc.h3("Brute force")
doc.p("对每个位置 i, 扫一遍整个字符串, 数 <code>s[i]</code> 出现了几次, 第一个次数为 1 的就是答案。<code>O(n²)</code>。浪费: 同一个字母被重复数了很多次。")
doc.h3("Intuition")
doc.p("和第 3 题一样, 先把每个字母的次数数出来。但这里有一个新问题: 要的是<b>按原来顺序的第一个</b>。频率表本身没有顺序信息。")
doc.p("所以分两遍: 第一遍扫完整个字符串, 得到每个字母的次数 (这时才知道谁\"后面还会出现\"); 第二遍按原来的顺序从左往右扫, 第一个次数为 1 的就是答案。")
doc.h3("算法")
steps("第一遍: <code>cnt = Counter(s)</code>。",
      "第二遍: 从左往右看 <code>s[i]</code>, 第一个 <code>cnt[s[i]] == 1</code> 的, 返回 i。",
      "都没有, 返回 -1。")
doc.svg(SLUG + "/first_uniq_core.svg", "第一遍得到全局的次数, 第二遍用原来的顺序保证是\"第一个\"。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/first_uniq_trace.svg", "s = \"aabc\": 第一遍 4 步建表; 第二遍在 s[2] = 'b' 命中, 返回 2。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, 两遍线性扫描。Space <code>O(1)</code>, 小写字母最多 26 种。")
nc.solution(doc, CODE["first_uniq"])
doc.note("要\"第一个满足某个次数条件的\": 第一遍数次数, 第二遍按原顺序查。")

# ================================================================ 5
doc.h2("5. Group Anagrams")
doc.h3("题目在问什么")
doc.p("给一组字符串 <code>strs</code>。把互为 anagram 的字符串放进同一组, 返回所有的组 (组的顺序、组内的顺序都随意)。")
doc.h3("看例子")
doc.svg(SLUG + "/group_examples.svg", "例子。")
doc.h3("Brute force")
doc.p("两两比较, 用第 3 题的方法判断是不是 anagram, 是的话合并到一组。n 个词有大约 <code>n²/2</code> 对, 每对比较 <code>O(k)</code> (k 是词长), 一共 <code>O(n²·k)</code>。"
      "浪费: 同一组里的词被反复互相比较。")
doc.h3("Intuition: 给每个词算一个\"身份证\"")
doc.p("与其问\"这两个词是不是同一组\", 不如给每个词算一个 <b>key</b>, 让同一组的词算出来的 key 完全一样, 不同组的 key 不一样。这个 key 叫 canonical key (规范形式)。")
doc.p("有了 key, 分组就是 Hash Table: <code>groups[key].append(word)</code>。每个词只处理一次, 不用两两比较。")
doc.p("anagram 的 key 怎么选? 两种常用的:")
nc.bullets(doc, "把词排序: <code>\"eat\"</code>、<code>\"tea\"</code>、<code>\"ate\"</code> 排序后都是 <code>\"aet\"</code>。每个词 <code>O(k log k)</code>。",
           "数 26 个字母的次数, 转成 tuple: 每个词 <code>O(k)</code>。注意 list 不能当 dict 的 key, 要转成 tuple。")
doc.h3("算法")
steps("<code>groups = defaultdict(list)</code>。",
      "对每个词 w: <code>key = \"\".join(sorted(w))</code>, <code>groups[key].append(w)</code>。",
      "返回 <code>groups.values()</code>。")
doc.svg(SLUG + "/group_core.svg", "左: 两两比较要 15 对; 右: 每个词算一次 key, 直接放进对应的桶。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/group_trace.svg", "6 个词 6 步: 'tea' 和 'ate' 的 key 都是 'aet', 放进已有的桶; 一共 3 个 key, 对应 3 组。")
doc.h3("复杂度")
doc.p("Time <code>O(n·k log k)</code> (用排序当 key), 换成计数 tuple 是 <code>O(n·k)</code>。Space <code>O(n·k)</code>, 要存下所有的词。")
nc.solution(doc, CODE["group"])
doc.note("要把\"本质相同\"的东西分组: 设计一个 canonical key, 用 defaultdict(list) 分桶。key 必须是 str 或 tuple, 不能是 list。")

# ================================================================ 6
doc.h2("6. Longest Consecutive Sequence")
doc.h3("题目在问什么")
doc.p("给一个没有排序的整数数组 <code>nums</code>。从里面挑一些数, 它们是<b>连续的整数</b> (比如 1, 2, 3, 4), 问最多能挑几个。"
      "注意这里的\"连续\"指的是值连续, 不是位置连续。题目要求 <code>O(n)</code> 时间。")
doc.h3("看例子")
doc.svg(SLUG + "/lcs_examples.svg", "两个例子。绿色是答案里的数。")
doc.h3("Brute force")
doc.p("最自然的做法是先排序, 再从左往右数最长的一段连续值。这是 <code>O(n log n)</code>, 不满足题目要求。")
doc.p("另一种想法: 把所有数放进 set, 然后对每个数 x, 一直往右数 x+1, x+2, ... 在不在 set 里。"
      "问题是, 如果数组是 <code>[1, 2, 3, ..., n]</code>, 从 1 开始数 n 个, 从 2 开始数 n-1 个, ... 一共 <code>O(n²)</code>。"
      "浪费: 序列中间的数被重复数了好几遍。从 2 开始数出来的那一段, 其实是从 1 开始那一段的一部分。")
doc.h3("Intuition: 只从起点开始数")
doc.p("一段连续的数只需要数一次, 从它的<b>起点</b>开始数。")
doc.p("怎么判断 x 是不是起点? 看 <code>x - 1</code> 在不在 set 里。在, 说明 x 前面还有数, x 不是起点, 跳过, 让起点去数。不在, x 就是起点, 从它往右数。")
doc.p("这样每个数最多被\"往右数\"的过程走到一次, 总共 <code>O(n)</code>。")
doc.h3("算法")
steps("<code>s = set(nums)</code>。",
      "对 s 里的每个 x: 如果 <code>x - 1 in s</code>, 跳过。",
      "否则 x 是起点。<code>y = x</code>, 只要 <code>y + 1 in s</code> 就 <code>y += 1</code>。这一段长度是 <code>y - x + 1</code>, 更新 best。")
doc.svg(SLUG + "/lcs_core.svg", "上: 每个数都出发, 2、3、4 被重复走; 下: 只有起点 1 出发, 其他数判断一次就跳过。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/lcs_trace.svg", "按 Python 遍历 set 的真实顺序: 1 是起点, 数到 4; 2、3、4 跳过; 100 和 200 各自是长度 1 的起点。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>: for 循环 n 次, 每次判断 <code>O(1)</code>; 所有 while 加起来, 每个数只被它所在那一段的起点走一次, 总共最多 n 步。Space <code>O(n)</code>, set。")
nc.solution(doc, CODE["lcs"])
doc.note("set 能在 O(1) 里回答\"在不在\", 可以用来代替\"排序 + 看相邻\"。再加上\"只从起点出发\", 嵌套循环就变成线性。")

# ================================================================ 7
doc.h2("7. 补充: dict 还是数组, 以及什么时候别用 Hash Table")
doc.p("Hash Table 是用空间换时间。前面每道题, 不用 hash 和用 hash 的对比:")
nc.table(doc, ["题", "不用 hash", "用 hash"], [
    ["Two Sum", "双层循环 <code>O(n²)</code> 时间, <code>O(1)</code> 空间", "<code>O(n)</code> 时间, <code>O(n)</code> 空间"],
    ["Valid Anagram", "排序 <code>O(n log n)</code>", "数次数 <code>O(n)</code>, 26 格数组 <code>O(1)</code> 空间"],
    ["Group Anagrams", "两两比较 <code>O(n²·k)</code>", "算 key + 分桶 <code>O(n·k log k)</code>"],
    ["Longest Consecutive", "排序 <code>O(n log n)</code>", "set + 只从起点数 <code>O(n)</code>"]])
doc.p("什么时候用数组代替 dict: key 是小写字母、数字 0-9、ASCII 这种<b>范围小而且固定</b>的, 用 <code>[0] * 26</code> 这样的数组, 常数更小。key 是任意整数或字符串, 用 dict。")
doc.p("什么时候别用 Hash Table: 输入已经排好序, 找 pair 用 two pointers (见 02), 空间是 <code>O(1)</code>; 需要\"最大、最小、有序\", 用 heap 或排序, dict 不管大小顺序; 面试官限制额外空间时, 退回排序。")
doc.p("Python 的一个坑: <code>defaultdict</code> 只要<b>读</b>一个不存在的 key, 就会把它插进去。只想查的时候, 用 <code>in</code> 或 <code>.get()</code>。")
nc.solution(doc, CODE["defaultdict_pitfall"], summary="defaultdict 的坑 (例子)")

# ================================================================ 识别信号
doc.h2("8. 识别信号: 看到什么, 就想到 Hash Table")
nc.table(doc, ["题目特征", "做法", "complexity"], [
    ["数组里找两个数满足某种关系 (和、差、配对), 不要求有序", "边扫边查\"另一半\" (Two Sum)", "<code>O(n²)</code> → <code>O(n)</code>"],
    ["\"相同的值\" + \"距离 ≤ k\"", "dict 记最近一次的下标, 每步覆盖", "<code>O(n·k)</code> → <code>O(n)</code>"],
    ["\"有没有重复\"", "<code>set</code> 一次遍历", "<code>O(n²)</code> → <code>O(n)</code>"],
    ["和顺序无关: anagram、字母够不够用 (Ransom Note)", "数次数, 比较频率表", "<code>O(n log n)</code> → <code>O(n)</code>"],
    ["\"第一个只出现一次的\" / \"出现次数最多的\"", "第一遍数次数, 第二遍按原顺序查", "<code>O(n²)</code> → <code>O(n)</code>"],
    ["把\"本质相同\"的东西分组", "canonical key + <code>defaultdict(list)</code>", "<code>O(n²)</code> → <code>O(n·k)</code>"],
    ["只问\"某个数在不在\", 要求 <code>O(n)</code>, 排序太慢", "<code>set</code> + 只从起点出发", "<code>O(n log n)</code> → <code>O(n)</code>"],
    ["key 是小写字母等固定小范围", "<code>[0] * 26</code> 代替 dict", "常数更小, 空间 <code>O(1)</code>"]])
doc.p("一句话: <b>在循环里反复\"找\"什么东西, 就把它存进 dict / set。</b> key 存什么、value 存什么, 决定了它是哪一种题。")

doc.h2("以后再学")
doc.p("Insert Delete GetRandom O(1) (dict + list 组合, 在 17 · Design); Rolling Hash / Rabin-Karp 字符串匹配; 把原数组当 hash 用的 First Missing Positive。")

doc.write("docs/01-hash-table.html")
