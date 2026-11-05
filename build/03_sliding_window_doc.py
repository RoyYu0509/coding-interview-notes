# 03 · Sliding Window 的正文 (NeetCode 式讲法)。
# 由 03_sliding_window.py 在末尾 exec, 共用它的 Svg / NS / CODE 等。
# 每道题的顺序: 题目在问什么 → 看例子 → brute force → intuition → 算法 → 手动走一遍 → 复杂度 → 参考代码 (折叠)

# ---------------------------------------------------------------- 新增: 例子图 & brute force 图
EX_CW = 34


def examples_svg(name, title, head, blocks):
    """每个 block = 一个 example:
    title: 第一行 (输入 → 输出)
    items: 数组 / 字符串
    ans: [(l, r)] 答案区间 (绿色 + 下方括号)
    ans_text: 答案括号旁的说明
    bad: [(l, r, text)] 看起来像但不对的区间 (上方红色虚线括号)
    extra: 额外的说明行
    """
    S = Svg(title)
    y = 18
    for h in head:
        S.t(40, y, h, 12, SUB)
        y += 20
    y += 4
    for bi, b in enumerate(blocks):
        S.line(40, y, 640, y)
        items = b["items"]
        n = len(items)
        cw = b.get("cw", EX_CW)
        S.t(40, y + 20, b["title"], 14, INK, "start", 500)
        top = y + 40                      # 红色括号行
        cy = top + 22                     # 格子
        roles = ["keep"] * n
        for (l, r) in b.get("ans", []):
            for k in range(l, r + 1):
                roles[k] = "new"
        # 下标
        for k in range(n):
            S.t(40 + k * cw + cw / 2, cy + 44, str(k), 11, SUB, "middle")
        S.array(40, cy, items, roles, cw, 30, 15)
        tx = 40 + n * cw + 24
        for (l, r, text) in b.get("bad", []):
            x1, x2 = 40 + l * cw + 3, 40 + (r + 1) * cw - 3
            S.p.append('<path d="M%s %s L%s %s L%s %s L%s %s" fill="none" stroke="%s" '
                       'stroke-width="1.5" stroke-dasharray="4 3"/>'
                       % (x1, top + 14, x1, top + 6, x2, top + 6, x2, top + 14, ARR))
            S.t(tx, top + 8, text, 12, REM[2])
        for (l, r) in b.get("ans", []):
            S.ring(40 + l * cw, cy, (r - l + 1) * cw, 30)
        if b.get("ans_text"):
            S.t(tx, cy + 15, b["ans_text"], 14, NEW[2], "start", 500)
        yy = cy + 66
        for line in b.get("extra", []):
            S.t(40, yy, line, 12, SUB)
            yy += 18
        y = yy + 6
    S.line(40, y, 640, y)
    S.legend(y + 22, [("new", "答案 substring / subarray"), ("ring", "答案的范围"),
                      ("rem", "看起来像, 但不对 (原因写在右边)")])
    S.save(name, y + 42)


def brute_longest_svg():
    """Brute force: 每个 left 都从头往右试, 直到遇到重复。标出 '其实已经知道不重复, 又检查了一遍' 的格子。"""
    s = "pwwkew"
    n = len(s)
    cw = 34
    S = Svg("Brute force on pwwkew")
    S.t(40, 18, "s = \"pwwkew\" · brute force: 每个起点 left 都从 left 开始往右一个一个加, 遇到重复就停", 12, SUB)
    S.t(40, 38, "每一行 = 一个起点 left。格子里的字符都被\"检查了一次有没有重复\"", 12, SUB)
    S.t(40, 66, "起点", 12, SUB)
    S.t(112, 66, "从 left 往右检查", 12, SUB)
    S.t(112 + n * cw + 28, 66, "这一行的结果", 12, SUB)
    y = 76
    S.line(40, y, 640, y)
    prev_stop = 0
    total = redundant = 0
    best = 0
    for left in range(n):
        seen = set()
        stop = left
        while stop < n and s[stop] not in seen:
            seen.add(s[stop])
            stop += 1
        # [left, stop) 不重复; stop < n 时 s[stop] 是撞上的重复字符
        roles, rings = [], []
        for k in range(n):
            if k < left:
                roles.append("out")
            elif k < stop:
                roles.append("keep" if k < prev_stop else "new")
            elif k == stop:
                roles.append("rem")
            else:
                roles.append("out")
        rings = [k for k in range(left, min(stop, prev_stop))]
        S.t(40, y + 26, "left = %d" % left, 14, INK, "start", 500)
        S.array(112, y + 12, list(s), roles, cw, 30, 15, ring_idx=rings)
        checks = (stop - left) + (1 if stop < n else 0)
        red = len(rings)
        total += checks
        redundant += red
        best = max(best, stop - left)
        msg = "\"%s\" 不重复, 长度 %d" % (s[left:stop], stop - left)
        msg2 = ("s[%d] = '%s' 撞上重复, 停" % (stop, s[stop])) if stop < n else "走到结尾, 停"
        tx = 112 + n * cw + 28
        S.t(tx, y + 20, msg, 12, INK)
        S.t(tx, y + 38, msg2, 12, SUB)
        if red:
            S.t(tx, y + 56, "%d 个格子是重复劳动" % red, 12, "#B5700F")
        y += 72
        S.line(40, y, 640, y)
        prev_stop = stop
    S.t(40, y + 22, "一共检查了 %d 次, 其中 %d 次 (橙色圈) 是\"上一行已经确认不重复, 这一行又从头确认一遍\"。最长 = %d" % (total, redundant, best),
        14, INK, "start", 500)
    S.legend(y + 52, [("new", "这一行新检查的字符"), ("ring", "上一行已确认过, 又检查一遍"), ("rem", "撞上的重复字符")])
    S.save("longest_substring_brute.svg", y + 74)
    return total, redundant


BF_TOTAL, BF_RED = brute_longest_svg()

# 例子图里用到的数字, 先用代码算出来再画
assert NS["length_of_longest_substring"]("abcabcbb") == 3
assert NS["length_of_longest_substring"]("bbbbb") == 1
assert NS["length_of_longest_substring"]("pwwkew") == 3
examples_svg("longest_substring_examples.svg", "Longest Substring examples",
             ["找最长的一段连续字符, 段里没有任何字符出现两次"],
             [dict(title="Example 1:  s = \"abcabcbb\"  →  3", items=list("abcabcbb"),
                   ans=[(0, 2)], ans_text="\"abc\": a, b, c 各一次, 长度 3",
                   bad=[(0, 3, "\"abca\": a 出现两次 ✗")]),
              dict(title="Example 2:  s = \"bbbbb\"  →  1", items=list("bbbbb"),
                   ans=[(0, 0)], ans_text="\"b\": 再长就是 \"bb\", 重复了",
                   bad=[(0, 1, "\"bb\": b 出现两次 ✗")]),
              dict(title="Example 3:  s = \"pwwkew\"  →  3", items=list("pwwkew"),
                   ans=[(2, 4)], ans_text="\"wke\", 长度 3",
                   bad=[(1, 2, "\"ww\": 相邻两个 w ✗")],
                   extra=["注意: \"pwke\" 不算 —— 它跳过了 index 2 的 w, 不是连续的一段 (那叫 subsequence, 不是 substring)"])])

assert NS["longest_ones"]([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2) == 6
assert NS["longest_ones"]([0, 0, 1, 1], 0) == 2
examples_svg("max_consecutive_ones_iii_examples.svg", "Max Consecutive Ones III examples",
             ["最多把 k 个 0 改成 1, 问最长能得到多长的一段连续 1"],
             [dict(title="Example 1:  nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2  →  6",
                   items=[1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], cw=30,
                   ans=[(5, 10)], ans_text="index 5 和 10 的 0 改成 1 → 6 个 1",
                   bad=[(0, 5, "这一段有 3 个 0, 只能改 2 个 ✗")]),
              dict(title="Example 2:  nums = [0,0,1,1], k = 0  →  2", items=[0, 0, 1, 1],
                   ans=[(2, 3)], ans_text="一个 0 都不能改, 只能用原本的 1,1")])

assert NS["character_replacement"]("ABAB", 2) == 4
assert NS["character_replacement"]("AABABBA", 1) == 4
examples_svg("char_replacement_examples.svg", "Longest Repeating Character Replacement examples",
             ["最多把 k 个字符改成别的字母, 问最长能得到多长的一段\"全是同一个字母\""],
             [dict(title="Example 1:  s = \"ABAB\", k = 2  →  4", items=list("ABAB"),
                   ans=[(0, 3)], ans_text="把两个 B 改成 A → \"AAAA\""),
              dict(title="Example 2:  s = \"AABABBA\", k = 1  →  4", items=list("AABABBA"),
                   ans=[(0, 3)], ans_text="\"AABA\": 把 1 个 B 改成 A → \"AAAA\"",
                   bad=[(0, 4, "\"AABAB\": 要改 2 个 B, 超过 k = 1 ✗")])])

assert NS["check_inclusion"]("ab", "eidbaoo") is True
assert NS["check_inclusion"]("ab", "eidboaoo") is False
examples_svg("permutation_in_string_examples.svg", "Permutation in String examples",
             ["s2 里有没有一段连续的、长度和 s1 一样的 substring, 字母和 s1 完全一样 (顺序可以不同)"],
             [dict(title="Example 1:  s1 = \"ab\", s2 = \"eidbaoo\"  →  True", items=list("eidbaoo"),
                   ans=[(3, 4)], ans_text="\"ba\" 是 \"ab\" 换了顺序 ✓"),
              dict(title="Example 2:  s1 = \"ab\", s2 = \"eidboaoo\"  →  False", items=list("eidboaoo"),
                   bad=[(3, 5, "b 和 a 被 o 隔开, 长度 3 ≠ 2 ✗")],
                   extra=["长度为 2 的段: ei, id, db, bo, oa, ao, oo —— 没有一段恰好是一个 a 加一个 b"])])

assert NS["min_subarray_len"](7, [2, 3, 1, 2, 4, 3]) == 2
assert NS["min_subarray_len"](11, [1, 1, 1, 1, 1, 1, 1, 1]) == 0
examples_svg("min_subarray_len_examples.svg", "Minimum Size Subarray Sum examples",
             ["全是正整数。找一段连续的数, 加起来 ≥ target, 而且越短越好"],
             [dict(title="Example 1:  target = 7, nums = [2,3,1,2,4,3]  →  2", items=[2, 3, 1, 2, 4, 3],
                   ans=[(4, 5)], ans_text="4 + 3 = 7 ≥ 7, 长度 2",
                   bad=[(0, 3, "2+3+1+2 = 8 ≥ 7 也行, 但长度 4 不是最短")]),
              dict(title="Example 2:  target = 11, nums = [1,1,1,1,1,1,1,1]  →  0", items=[1] * 8,
                   extra=["全部加起来才 8 < 11, 没有任何一段够大 → 返回 0"])])

assert NS["min_window"]("ADOBECODEBANC", "ABC") == "BANC"
assert NS["min_window"]("a", "aa") == ""
examples_svg("min_window_examples.svg", "Minimum Window Substring examples",
             ["在 s 里找最短的一段连续 substring, 它包含 t 的每一个字符 (t 里重复的字符要重复包含)"],
             [dict(title="Example 1:  s = \"ADOBECODEBANC\", t = \"ABC\"  →  \"BANC\"", items=list("ADOBECODEBANC"),
                   cw=30, ans=[(9, 12)], ans_text="",
                   bad=[(0, 5, "\"ADOBEC\" 也包含 A, B, C, 但长度 6")],
                   extra=["答案 \"BANC\" (index 9..12): 含 B, A, C, 长度 4, 是所有\"包含 A,B,C 的段\"里最短的"]),
              dict(title="Example 2:  s = \"a\", t = \"aa\"  →  \"\"", items=["a"],
                   extra=["t 要两个 a, s 只有一个 a → 不存在, 返回空字符串"])])

assert NS["num_subarray_product_less_than_k"]([10, 5, 2, 6], 100) == 8
examples_svg("product_less_than_k_examples.svg", "Subarray Product Less Than K examples",
             ["全是正整数。数一数: 有多少段连续的数, 乘起来 < k"],
             [dict(title="Example:  nums = [10,5,2,6], k = 100  →  8", items=[10, 5, 2, 6],
                   bad=[(0, 2, "10 × 5 × 2 = 100, 不 < 100 ✗")],
                   extra=["合法的 8 段: [10]  [5]  [2]  [6]  [10,5]=50  [5,2]=10  [2,6]=12  [5,2,6]=60",
                          "答案是\"个数\", 不是长度: 同一个数可以出现在很多段里"])])

assert NS["subarrays_with_k_distinct"]([1, 2, 1, 2, 3], 2) == 7
assert NS["subarrays_with_k_distinct"]([1, 2, 1, 3, 4], 3) == 3
examples_svg("k_distinct_examples.svg", "Subarrays with K Different Integers examples",
             ["数一数: 有多少段连续的数, 里面恰好有 k 种不同的数字"],
             [dict(title="Example 1:  nums = [1,2,1,2,3], k = 2  →  7", items=[1, 2, 1, 2, 3],
                   bad=[(2, 4, "[1,2,3] 有 3 种 ✗")],
                   extra=["恰好 2 种的 7 段: [1,2]  [2,1]  [1,2]  [2,3]  [1,2,1]  [2,1,2]  [1,2,1,2]"]),
              dict(title="Example 2:  nums = [1,2,1,3,4], k = 3  →  3", items=[1, 2, 1, 3, 4],
                   extra=["恰好 3 种的 3 段: [1,2,1,3]  [2,1,3]  [1,3,4]"])])


# ---------------------------------------------------------------- HTML 工具
def solution_code(*keys):
    doc.raw('<details><summary>参考代码 (先自己按上面的算法步骤写, 写不出来再展开)</summary>')
    for k in keys:
        doc.code(CODE[k])
    doc.raw('</details>')


def steps(*lines):
    doc.raw("<ol>%s</ol>" % "".join("<li>%s</li>" % x for x in lines))


# ================================================================ HTML
doc = d.Doc("03 · Sliding Window")

doc.h2("这篇讲什么")
doc.p("面试里有一大类题是这样问的: 给你一个数组或字符串, 在里面找<b>一段连续的</b>部分, 满足某个条件, "
      "然后问\"最长是多少\"\"最短是多少\"或者\"一共有多少段\"。")
doc.p("这里\"连续的一段\"有专门的叫法。在数组里叫 <b>subarray</b>, 在字符串里叫 <b>substring</b>。"
      "比如 <code>\"abcde\"</code> 里, <code>\"bcd\"</code> 是 substring, <code>\"ace\"</code> 不是, 因为它跳过了字符。"
      "跳着取的那种叫 subsequence, 不在这篇的范围里。")
doc.p("这类题最直接的做法是把所有\"连续的一段\"都列出来, 一段一段检查。长度为 n 的数组有大约 <code>n²/2</code> 段, "
      "所以至少 <code>O(n²)</code>。<b>Sliding Window</b> 就是专门把这类题从 <code>O(n²)</code> 降到 <code>O(n)</code> 的方法。")
doc.p("名字的意思很形象: 想象数组上放了一个可以伸缩的框 (window), 框住的那一段就是当前在看的 subarray。"
      "框的右边 (right) 一格一格往右推, 框的左边 (left) 在需要的时候也往右收。两条边都只往右走, 不回头。"
      "整篇就是在讲: <b>为什么可以不回头, 以及什么时候不能用</b>。")
doc.p("这篇的题都来自公司高频题统计。第 1 题 Longest Substring Without Repeating Characters 在 470 家公司的总榜排第 4, "
      "有 95 家公司考过。后面 7 道题每一道都是在第 1 题上改一个条件:")
doc.raw('''<table>
<tr><th>#</th><th>题目</th><th>考过的公司数</th><th>相比上一题多了什么</th></tr>
<tr><td>1</td><td>Longest Substring Without Repeating Characters</td><td>95</td><td>模板题: 求最长, 条件是\"没有重复\"</td></tr>
<tr><td>2</td><td>Max Consecutive Ones III</td><td>21</td><td>条件换成\"0 的个数 ≤ k\"</td></tr>
<tr><td>3</td><td>Longest Repeating Character Replacement</td><td>18</td><td>条件要多想一步才能写出来</td></tr>
<tr><td>4</td><td>Permutation in String</td><td>16</td><td>框的长度是固定的</td></tr>
<tr><td>5</td><td>Minimum Size Subarray Sum</td><td>15</td><td>求最短, 方向反过来</td></tr>
<tr><td>6</td><td>Minimum Window Substring</td><td>32</td><td>求最短 + 判断条件变复杂</td></tr>
<tr><td>7</td><td>Subarray Product Less Than K</td><td>21</td><td>不求长度, 求个数</td></tr>
<tr><td>8</td><td>Subarrays with K Different Integers</td><td>15</td><td>\"恰好 k\" 不能直接做, 要拆开</td></tr>
</table>''')
doc.p("每道题都按同一个顺序讲: <b>题目在问什么 → 看例子 → brute force → 从 brute force 里找 intuition → 算法 → 手动走一遍 → 复杂度</b>。"
      "代码放在最后, 默认折叠。理解了算法以后, 代码你自己就能写出来。")
doc.p("前置知识: 只需要会用 dict 计数 (见 01 · Hash Table)。")

# ================================================================ 1
doc.h2("1. Longest Substring Without Repeating Characters")
doc.h3("题目在问什么")
doc.p("给一个字符串 <code>s</code>。在里面找一段<b>连续的</b> substring, 要求这一段里<b>每个字符最多出现一次</b>。"
      "问: 满足要求的 substring 最长有多长。")
doc.h3("看例子")
doc.svg("03-sliding-window/longest_substring_examples.svg",
        "三个例子。绿色是答案。红色虚线是\"看起来可以, 但其实不满足要求\"的段, 原因写在右边。")
doc.p("从例子里能看出两件事。第一, \"连续\"很重要: Example 3 里 <code>\"pwke\"</code> 虽然没有重复字符, 但它不连续, 不算。"
      "第二, 答案只要长度, 不要具体是哪一段。")
doc.h3("Brute force: 每个起点都试一遍")
doc.p("最直接的想法: 对每一个起点 <code>left</code>, 从它开始一个字符一个字符往右加, 用一个 set 记住已经见过的字符。"
      "一旦遇到 set 里已经有的字符, 说明重复了, 这个起点就到头了, 记下长度, 换下一个起点。")
doc.svg("03-sliding-window/longest_substring_brute.svg",
        "Brute force 在 \"pwwkew\" 上的全过程。每一行是一个起点。橙色圈出来的格子是重复劳动。")
doc.p("一共有 n 个起点, 每个起点最多往右走 n 步, 所以是 <code>O(n²)</code>。")
doc.p("看橙色圈的格子。比如 <code>left = 3</code> 那一行: 它检查 k, e, w 有没有重复。"
      "但上一行 <code>left = 2</code> 已经确认过 <code>\"wkew\"</code> 前面的 <code>\"wke\"</code> 不重复了。"
      "一段不重复的字符串, 去掉开头一个字符, 剩下的当然也不重复。所以 k 和 e 根本不用再查一遍。")
doc.h3("Intuition: 换起点的时候, 不要从头再来")
doc.p("把上面的观察说完整:")
steps("假设当前这一段 <code>s[left..right]</code> 没有重复。",
      "现在想把 right 往右扩一格, 加进来一个新字符 <code>ch</code>。",
      "如果 ch 在这一段里没出现过, 那新的一段也没有重复, 继续扩就行。",
      "如果 ch 在这一段里已经出现过, 那么<b>只要这一段还包含着旧的那个 ch, 它就一定有重复</b>。"
      "这时候再往右扩是没用的, 只会继续重复。唯一的办法是把左边收进来, 直到把旧的 ch 扔出去。",
      "收完之后, 这一段又没有重复了。接着扩 right。")
doc.p("关键在第 4 步: left 只会往右收, 从来不需要回到左边去。因为左边那些起点, 在它们自己那一轮已经\"试过并且失败了\"。"
      "这就是 brute force 里橙色那部分重复劳动被省掉的原因。")
doc.p("这个\"右边扩、左边收、两边都不回头\"的框, 就是 <b>sliding window</b>。")
doc.h3("算法")
doc.p("用一个 dict <code>cnt</code> 记录 window 里每个字符出现了几次。")
steps("<code>left = 0</code>, <code>best = 0</code>。",
      "right 从 0 走到 n-1。每一步把 <code>ch = s[right]</code> 放进 window: <code>cnt[ch] += 1</code>。",
      "如果 <code>cnt[ch] > 1</code>, 说明 ch 重复了。不断把最左边的字符 <code>s[left]</code> 移出 window "
      "(<code>cnt[s[left]] -= 1</code>, <code>left += 1</code>), 直到 <code>cnt[ch]</code> 回到 1。",
      "这时 window 一定没有重复。用它的长度 <code>right - left + 1</code> 更新 best。")
doc.p("为什么第 3 步只需要检查 ch: 在 ch 进来之前, window 是没有重复的。所以如果现在有重复, 一定是刚进来的 ch 造成的。")
doc.svg("03-sliding-window/longest_substring_core.svg", "核心: 只有新进来的 ch 可能造成重复, 把左边收到 cnt[ch] 回到 1, window 就又合法了。")
doc.h3("手动走一遍")
doc.p("还是用 <code>\"pwwkew\"</code>。每一行是 right 走的一步。第 2 列是 ch 刚放进来的样子, 第 3 列是收完 left 之后的样子, 最右边是算长度。")
doc.svg("03-sliding-window/longest_substring_trace.svg",
        "right = 2 时第二个 w 进来, 和旧的 w 重复, 左边一次收掉 p 和 w 两个字符。right = 5 时又遇到 w, 再收掉一个 w。")
doc.p("对比 brute force 的图: 这里 right 走了 6 步, left 一共只往右移了 3 次, 每个字符最多进一次、出一次。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>。right 走 n 步, left 加起来最多也只走 n 步。虽然代码里 while 写在 for 里面, 但 while 一共最多执行 n 次, 不是每一轮 n 次。"
      "Space <code>O(Σ)</code>, Σ 是字符集大小, 因为 cnt 里最多存这么多种字符。")
solution_code("longest")
doc.note("求最长 + 不能重复: 右边一格一格加进来。一旦重复, 就收左边, 直到不重复。left 永远不回头, 所以是 O(n)。")

# ================================================================ 模板
doc.h2("把第 1 题抽象一下: Sliding Window 什么时候能用")
doc.p("第 1 题里, left 能\"永远不回头\", 是因为一条性质: <b>一段如果已经不合法 (有重复), 那把它再往右扩, 还是不合法</b>。"
      "反过来, 一段如果合法, 把它从左边缩短一点, 还是合法。")
doc.p("下面这张图把所有可能的 (left, right) 画成一个表格。每个格子是一段 substring。绿色是合法的段, 红色是不合法的。"
      "因为上面那条性质, 合法区和不合法区之间是一条阶梯状的边界。brute force 把每个格子都看一遍; sliding window 只沿着边界走。")
doc.svg("03-sliding-window/template_core.svg",
        "每个格子是一个 (left, right)。sliding window 的两个指针沿着合法区的边界走, 一共 9 步, 另外 12 个格子不用看。")
doc.p("所以判断一道题能不能用 sliding window, 就问一个问题: <b>把 window 往右扩一格, \"合法\"只会往一个方向变吗?</b>")
doc.raw("<ul>"
        "<li>求<b>最长</b>的题: window 越大越容易不合法 (重复、0 太多、乘积太大)。做法是: 不合法了才收左边, 收完再记答案。</li>"
        "<li>求<b>最短</b>的题: window 越大越容易合法 (和够大、覆盖了所有字符)。做法是: 一合法就记答案, 然后收左边看看还能不能更短。第 5 题会讲。</li>"
        "<li>如果扩一格可能变好也可能变坏 (比如数组里有负数), 这条性质就没了, 不能用 sliding window。要改用 04 · Prefix Sum。</li>"
        "</ul>")
doc.p("后面每道题都是同一个骨架, 只换两样东西: <b>window 里要记什么 (state)</b>, 和<b>什么叫合法</b>。")
doc.raw('<details><summary>通用模板 (最长 / 最短 两个版本)</summary>')
doc.code(CODE["template"])
doc.code(CODE["template_short"])
doc.raw('</details>')
doc.note("sliding window 能用的前提: 合法性随 window 变大只往一个方向变。两个指针都只往右走, 所以 O(n)。")

# ================================================================ 2
doc.h2("2. Max Consecutive Ones III")
doc.h3("题目在问什么")
doc.p("给一个只有 0 和 1 的数组 <code>nums</code>, 和一个整数 <code>k</code>。你最多可以把 k 个 0 改成 1。问: 改完之后, 最长能得到多长的一段连续的 1。")
doc.h3("看例子")
doc.svg("03-sliding-window/max_consecutive_ones_iii_examples.svg", "两个例子。绿色是答案那一段。")
doc.p("换个角度看例子 1: 答案那一段 <code>[0,1,1,1,1,0]</code> 本来不全是 1, 但里面只有 2 个 0, 正好够 k = 2 次修改。"
      "所以题目其实在问: <b>找最长的一段, 里面 0 的个数不超过 k</b>。真的去改数组是不需要的。")
doc.h3("Brute force")
doc.p("和第 1 题一样: 每个起点往右扩, 数 0 的个数, 超过 k 就停。<code>O(n²)</code>。浪费也一样: 换起点时把中间那段的 0 又数了一遍。")
doc.h3("Intuition")
doc.p("和第 1 题是同一个结构。一段里 0 已经超过 k 个了, 再往右扩, 0 只会更多, 不会变少。所以合法性是单调的, 可以用 sliding window。")
doc.p("和第 1 题的区别只有两处: window 里要记的东西从\"每个字符几次\"变成了\"有几个 0\" (一个整数 <code>zeros</code>); "
      "不合法的条件从\"有字符重复\"变成了 <code>zeros > k</code>。")
doc.h3("算法")
steps("right 往右走, 遇到 0 就 <code>zeros += 1</code>。",
      "当 <code>zeros > k</code> 时, 收左边: 如果 <code>nums[left]</code> 是 0 就 <code>zeros -= 1</code>, 然后 <code>left += 1</code>。一直收到 <code>zeros ≤ k</code>。",
      "用 <code>right - left + 1</code> 更新 best。")
doc.svg("03-sliding-window/max_consecutive_ones_iii_core.svg", "核心: \"能翻 k 个\" 等价于 \"window 里 0 的个数 ≤ k\", 所以只需要数 0。")
doc.h3("手动走一遍")
doc.svg("03-sliding-window/max_consecutive_ones_iii_trace.svg", "right = 6 时 zeros = 3 > k = 2, 收左边直到扔掉一个 0。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(1)</code>。")
solution_code("ones")
doc.note("\"最多改 / 删 / 翻 k 个\" → 找最长的一段, 里面\"需要改的\"不超过 k 个。")

# ================================================================ 3
doc.h2("3. Longest Repeating Character Replacement")
doc.h3("题目在问什么")
doc.p("给一个只有大写字母的字符串 <code>s</code>, 和整数 <code>k</code>。你最多可以把 k 个字符改成任意字母。问: 改完之后, 最长能得到多长的一段<b>全是同一个字母</b>的 substring。")
doc.h3("看例子")
doc.svg("03-sliding-window/char_replacement_examples.svg", "两个例子。")
doc.p("例子 2 里 <code>\"AABA\"</code> 可以, 因为只要改 1 个 B。<code>\"AABAB\"</code> 不行, 因为要改 2 个 B, 超过了 k = 1。")
doc.h3("Brute force")
doc.p("每个起点往右扩, 每扩一格就重新算一遍\"这一段要改几个字符\"。<code>O(n²)</code> 段。")
doc.h3("Intuition")
doc.p("先回答一个更小的问题: <b>给定一段, 最少要改几个字符才能变成全是同一个字母?</b>")
doc.p("答案是: 保留出现次数最多的那个字母, 其他的全改掉。比如 <code>\"AABA\"</code> 里 A 出现 3 次, 最多, 那就把剩下的 1 个改成 A。"
      "所以要改的个数 = <code>这一段的长度 - 出现最多的字母的次数</code>。")
doc.p("于是\"合法\"就是 <code>长度 - 最多的次数 ≤ k</code>。和第 2 题比, 这里的\"违规数\"不是直接数出来的, 而是从 cnt 算出来的。")
doc.p("它也是单调的: window 往右扩一格, 长度加 1, 最多的次数最多也只加 1, 所以\"要改的个数\"只会不变或变大。")
doc.h3("算法")
steps("用 dict <code>cnt</code> 记 window 里每个字母的次数。right 往右走, <code>cnt[ch] += 1</code>。",
      "当 <code>(right - left + 1) - max(cnt.values()) > k</code> 时, 收左边。",
      "用当前长度更新 best。")
doc.svg("03-sliding-window/char_replacement_core.svg", "核心: 合法 ⇔ 长度 - 最多的次数 ≤ k。")
doc.h3("手动走一遍")
doc.svg("03-sliding-window/char_replacement_trace.svg", "right = 4 和 right = 6 时要改 2 个 > k = 1, 收掉最左边一个字符就重新合法。")
doc.h3("复杂度")
doc.p("Time <code>O(26n) = O(n)</code>, 每次 <code>max(cnt.values())</code> 最多看 26 个字母。Space <code>O(26)</code>。")
solution_code("replace")
doc.note("合法条件可以是从 state 算出来的量 (长度 - 最多的次数), 只要它随 window 变大只会变坏, 就能用同一个骨架。")

# ================================================================ 4
doc.h2("4. Permutation in String")
doc.h3("题目在问什么")
doc.p("给两个字符串 <code>s1</code> 和 <code>s2</code>。问: s2 里有没有一段连续的 substring, 它是 s1 的某种重新排列 (permutation)。"
      "也就是: 长度和 s1 一样, 每个字母出现的次数也和 s1 一样, 只是顺序可以不同。")
doc.h3("看例子")
doc.svg("03-sliding-window/permutation_in_string_examples.svg", "两个例子。")
doc.p("这题和前面三题有一个明显的不同: 要找的那一段<b>长度是固定的</b>, 必须正好等于 <code>len(s1)</code>。")
doc.h3("Brute force")
doc.p("s2 里每个长度为 m (m = len(s1)) 的段都拿出来, 排个序, 和排好序的 s1 比。一共 n 段, 每段排序 <code>O(m log m)</code>。")
doc.p("浪费在哪: 相邻两段只差两个字符, 左边出去一个、右边进来一个, 中间 m-2 个字符都一样, 却每次都重新排序。")
doc.h3("Intuition")
doc.p("两个字符串互为 permutation, 等价于<b>每个字母的出现次数都一样</b>。所以不用排序, 比两个计数表就行。")
doc.p("框的长度固定为 m, 所以 left 不用\"收到合法为止\", 而是每次 right 进来一个, left 就跟着出去一个, 框一直保持 m 长。"
      "每滑一格只改两个计数, 是 <code>O(1)</code> 的。")
doc.h3("算法")
steps("<code>need</code> = s1 里每个字母的次数。<code>win</code> = 当前框里每个字母的次数。",
      "right 往右走, 把 <code>s2[right]</code> 加进 win。",
      "如果框的长度超过了 m (也就是 <code>right ≥ m</code>), 把 <code>s2[right - m]</code> 从 win 里减掉。",
      "如果 <code>win == need</code>, 返回 True。")
doc.svg("03-sliding-window/permutation_in_string_core.svg", "核心: 框的长度恒为 m, 每滑一格 = 右边进一个 + 左边出一个。")
doc.h3("手动走一遍")
doc.svg("03-sliding-window/permutation_in_string_trace.svg", "right = 2 起框满了, 之后每步先进后出。right = 4 时框是 \"ba\", 计数和 need 一样。")
doc.p("Find All Anagrams in a String 是同一题, 区别只是不在第一次找到时返回, 而是把所有起点都记下来。")
doc.h3("复杂度")
doc.p("Time <code>O(26n)</code>, 每步比较两个长度 26 的表。Space <code>O(26)</code>。")
solution_code("perm", "anagrams")
doc.note("长度固定为 m 的连续段: 右边进一个, 左边出一个, 用计数表代替排序。")

# ================================================================ 5
doc.h2("5. Minimum Size Subarray Sum")
doc.h3("题目在问什么")
doc.p("给一个<b>全是正整数</b>的数组 <code>nums</code> 和一个 <code>target</code>。找一段连续的 subarray, 它的和 ≥ target, 而且越短越好。问最短长度。找不到就返回 0。")
doc.h3("看例子")
doc.svg("03-sliding-window/min_subarray_len_examples.svg", "两个例子。")
doc.p("这次要的是<b>最短</b>。例子 1 里 <code>[2,3,1,2]</code> 的和也够大, 但它有 4 个数, 而 <code>[4,3]</code> 只要 2 个。")
doc.h3("Brute force")
doc.p("每个起点往右加, 加到和 ≥ target 就停, 记下长度。<code>O(n²)</code>。")
doc.h3("Intuition: 方向反过来了")
doc.p("前四题都是\"window 越大越容易<b>不合法</b>\"。这题因为全是正数, window 越大和越大, 所以是\"window 越大越容易<b>合法</b>\"。方向反过来了。")
doc.p("于是做法也反过来:")
steps("right 往右扩, 直到和刚好 ≥ target。这时找到了一个候选答案, 记下长度。",
      "既然已经合法了, 就试着从左边收: 收掉一个, 和变小了, 如果还 ≥ target, 说明更短的也行, 再记一次。",
      "一直收到和 < target 为止, 然后继续扩 right。")
doc.p("和\"求最长\"的模板相比, 区别有两个: while 的条件反过来 (合法才收), 以及<b>记答案的位置挪到了 while 里面</b> (每收一次之前都记一次)。")
doc.h3("算法")
steps("<code>total</code> = 框里的数加起来。right 往右走, <code>total += nums[right]</code>。",
      "当 <code>total ≥ target</code> 时: 先用 <code>right - left + 1</code> 更新 best (取 min), 再 <code>total -= nums[left]</code>, <code>left += 1</code>。",
      "最后 best 还是无穷大就返回 0。")
doc.svg("03-sliding-window/min_subarray_len_core.svg", "核心: 最长和最短的模板只差两处: while 的条件, 以及\"记答案\"放在哪里。")
doc.h3("手动走一遍")
doc.svg("03-sliding-window/min_subarray_len_trace.svg", "right = 4 和 right = 5 时, 合法后连续收了两次, 每收一次之前都记一次 best。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(1)</code>。")
solution_code("minlen")
doc.note("求最短: 合法了就记答案, 然后收左边看看还能不能更短。记答案要写在 while 里面。")

# ================================================================ 6
doc.h2("6. Minimum Window Substring")
doc.h3("题目在问什么")
doc.p("给字符串 <code>s</code> 和 <code>t</code>。在 s 里找最短的一段 substring, 它要包含 t 里的每一个字符。"
      "t 里重复的字符要重复包含, 比如 t = \"AAB\", 那这一段里至少要有 2 个 A 和 1 个 B。找不到就返回空字符串。")
doc.h3("看例子")
doc.svg("03-sliding-window/min_window_examples.svg", "两个例子。")
doc.h3("Brute force")
doc.p("枚举每一段, 用两个 Counter 比较这一段是否覆盖了 t。<code>O(n²)</code> 段, 每段比较还要时间。")
doc.h3("Intuition")
doc.p("和第 5 题同一个结构: 框越大越容易覆盖 t (越容易合法), 要求最短。所以还是\"扩到合法, 然后收到不合法\"。")
doc.p("难点只有一个: <b>怎么快速知道当前框是否覆盖了 t</b>。每次都把两个计数表完整比一遍太慢。")
doc.p("办法是记一个总数: <code>missing</code> = 框里还缺几个 t 需要的字符。一开始 <code>missing = len(t)</code>。"
      "再用 <code>need[c]</code> 记字符 c 还缺几个。")
steps("一个字符进框时, 如果它正好是缺的 (<code>need[c] > 0</code>), missing 减 1。不管缺不缺, need[c] 都减 1。need[c] 变成负数表示框里这个字符多了。",
      "一个字符出框时, need[c] 加 1。如果加完变成正数, 说明它从\"够了\"变成了\"缺了\", missing 加 1。",
      "<code>missing == 0</code> 就是合法。这样判断合不合法只要看一个数。")
doc.h3("算法")
steps("right 往右走, 按上面第 1 条更新 need 和 missing。",
      "当 <code>missing == 0</code>: 用当前框更新答案 (记下起点和长度), 然后按第 2 条把 <code>s[left]</code> 移出去, <code>left += 1</code>。",
      "最后返回记下的那一段。")
doc.svg("03-sliding-window/min_window_core.svg", "核心: need[c] > 0 表示缺, = 0 表示刚好, < 0 表示多了。missing 只统计缺的。")
doc.h3("手动走一遍")
doc.svg("03-sliding-window/min_window_trace.svg", "right = 4 时框覆盖了 t, 连续收两次 (第二次把 B 收走后变成缺 B, 停)。right = 6 时又收两次, 得到 \"CBA\"。")
doc.h3("复杂度")
doc.p("Time <code>O(|s| + |t|)</code>, Space <code>O(Σ)</code>。")
solution_code("minwin")
doc.note("\"包含 t 的所有字符\": 用 need 记每种字符还缺几个, 用 missing 记一共还缺几个。missing == 0 就是合法。")

# ================================================================ 7
doc.h2("7. Subarray Product Less Than K")
doc.h3("题目在问什么")
doc.p("给一个<b>全是正整数</b>的数组 <code>nums</code> 和整数 <code>k</code>。数一数: 有多少段连续的 subarray, 乘积 < k。")
doc.h3("看例子")
doc.svg("03-sliding-window/product_less_than_k_examples.svg", "例子。")
doc.p("这题第一次问的是<b>个数</b>, 不是长度。同一个元素可以出现在很多段里, 每一段都要算一次。")
doc.h3("Brute force")
doc.p("每个起点往右乘, 乘到 ≥ k 就停, 停之前每一段都计一次数。<code>O(n²)</code>。")
doc.h3("Intuition: 每一段按它的右端点来数")
doc.p("全是正数, 所以框越大乘积越大, 和前四题一样是\"越大越容易不合法\", 可以按\"最长\"的方式维护框。")
doc.p("问题是怎么数个数。关键想法: <b>每一段都有唯一的右端点。按右端点分组来数, 就不会重复也不会漏。</b>")
doc.p("固定 right。sliding window 收完之后, <code>[left..right]</code> 是以 right 结尾的最长合法段。"
      "那么从它里面任取一个起点 (left, left+1, ..., right), 得到的段都更短, 乘积更小, 所以也都合法。"
      "这样的起点有 <code>right - left + 1</code> 个。")
doc.p("所以和前面的唯一区别: 把 <code>best = max(best, 长度)</code> 换成 <code>ans += right - left + 1</code>。")
doc.h3("算法")
steps("<code>prod</code> = 框里的数乘起来。right 往右走, <code>prod *= nums[right]</code>。",
      "当 <code>prod ≥ k</code> 时, 收左边: <code>prod //= nums[left]</code>, <code>left += 1</code>。",
      "<code>ans += right - left + 1</code>。")
doc.svg("03-sliding-window/product_less_than_k_core.svg", "核心: 以 right 结尾的段, 起点可以是 left..right 中的任何一个, 一共 right - left + 1 段。")
doc.h3("手动走一遍")
doc.svg("03-sliding-window/product_less_than_k_trace.svg", "nums = [10,5,2,6,1,3]: 每一步新增的段都列出来了, 总数 1+2+2+3+4+4 = 16。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(1)</code>。")
solution_code("prod")
doc.note("求个数: 按右端点分组, 每个 right 贡献 right - left + 1 段。前提还是合法性单调 (这里靠\"全是正数\")。")

# ================================================================ 8
doc.h2("8. Subarrays with K Different Integers")
doc.h3("题目在问什么")
doc.p("给一个整数数组 <code>nums</code> 和整数 <code>k</code>。数一数: 有多少段连续的 subarray, 里面<b>恰好</b>有 k 种不同的数字。")
doc.h3("看例子")
doc.svg("03-sliding-window/k_distinct_examples.svg", "两个例子。")
doc.h3("Brute force")
doc.p("每个起点往右扩, 用 set 数种类, 种类恰好 k 就计数, 超过 k 就停。<code>O(n²)</code>。")
doc.h3("Intuition: \"恰好\" 不单调, 但 \"最多\" 单调")
doc.p("先试试直接套第 7 题。问题出在\"恰好 k 种\"不是单调的: 一段只有 1 种 (少了), 往右扩可能变成 2 种 (刚好), 再扩可能变成 3 种 (多了)。"
      "扩大既可能让它变合法, 也可能让它变不合法, left 不知道该怎么动。")
doc.p("但是 \"<b>最多</b> k 种\" 是单调的: 一段已经超过 k 种了, 再扩只会更多。所以\"最多 k 种的段有几个\"可以直接用第 7 题的方法数。")
doc.p("然后用一个减法: <code>恰好 k 种 = 最多 k 种 - 最多 (k-1) 种</code>。最多 k 种的段, 去掉最多 k-1 种的段, 剩下的就是恰好 k 种的。")
doc.h3("算法")
steps("写一个函数 <code>at_most(k)</code>: 用第 7 题的方法数\"种类 ≤ k 的段有几个\"。window 里用 dict 计数, <code>len(cnt)</code> 就是种类数, "
      "某个数的次数减到 0 时要把它从 dict 里删掉。",
      "答案 = <code>at_most(k) - at_most(k - 1)</code>。")
doc.svg("03-sliding-window/k_distinct_core.svg", "核心: 种类 ≤ 2 的 12 段 = 种类 ≤ 1 的 5 段 + 种类恰好 2 的 7 段。")
doc.h3("手动走一遍")
doc.svg("03-sliding-window/k_distinct_trace.svg", "同一个 right 上有两个框 (最多 2 种 / 最多 1 种), 各自收左边。每一步两者的差, 就是以 right 结尾、恰好 2 种的段数。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code> (扫两遍), Space <code>O(k)</code>。")
solution_code("kdistinct")
doc.note("\"恰好 k\" 不单调, 拆成 atMost(k) - atMost(k-1), 两个都能用 sliding window 数。")

# ================================================================ 识别信号
doc.h2("9. 识别信号: 看到什么, 就想到 sliding window")
doc.p("读完上面 8 题以后, 这张表用来做最后的整理。面试时看到左边的特征, 先试右边的做法。")
doc.raw('''<table>
<tr><th>题目特征</th><th>做法</th><th>complexity</th></tr>
<tr><td>连续 subarray / substring + 求<b>最长</b>, 而且 window 越大越容易不合法</td><td>right 进 → 不合法就收 left → 记答案</td><td>$O(n^2)$ → $O(n)$</td></tr>
<tr><td>连续 + 求<b>最短</b>, 而且 window 越大越容易合法 (正数和 ≥ target, 覆盖 t)</td><td>合法就先记答案, 再收 left</td><td>$O(n^2)$ → $O(n)$</td></tr>
<tr><td>\"最多修改 / 翻转 / 替换 k 个\"</td><td>window 里需要改的个数 ≤ k</td><td>$O(n^2)$ → $O(n)$</td></tr>
<tr><td>长度<b>固定</b>为 m</td><td>右边进一个, 左边出一个</td><td>$O(n \\cdot m)$ → $O(n)$</td></tr>
<tr><td>包含 / 覆盖 t 的所有字符</td><td>need 记每种缺几个 + missing 记一共缺几个</td><td>$O(n^2 \\cdot |t|)$ → $O(|s| + |t|)$</td></tr>
<tr><td>求<b>个数</b>, 合法性单调</td><td>每个 right 贡献 right - left + 1 段</td><td>$O(n^2)$ → $O(n)$</td></tr>
<tr><td>\"恰好 k 个\"</td><td>atMost(k) - atMost(k-1)</td><td>$O(n^2)$ → $O(n)$</td></tr>
<tr><td>数组有<b>负数</b>, 或者求\"和恰好等于 k\"</td><td>合法性不单调, 不能用 sliding window → 04 · Prefix Sum</td><td>$O(n^2)$ → $O(n)$</td></tr>
<tr><td>求每个 window 里的<b>最大 / 最小值</b></td><td>需要 monotonic deque → 07 · Monotonic Stack / Queue</td><td>$O(nk)$ → $O(n)$</td></tr>
</table>''')
doc.p("一句话判断: <b>把 right 往右推一格, \"合法\"只会往一个方向变吗?</b> 是, 就用 sliding window。不是 (有负数、要\"恰好\"), 就换方法或者拆成 atMost。")

doc.h2("以后再学")
doc.p("Longest Substring with At Least K Repeating Characters (合法性不单调, 要枚举种类数或分治)、"
      "Substring with Concatenation of All Words (按 word 长度分几个起点各滑一遍)。")

import re as _re


def _clean(x):
    x = x.replace("\\cdot", "×").replace("\\log", "log").replace("\\Sigma", "Σ")
    return _re.sub(r"\$([^$<]+)\$", r"<code>\1</code>", x)


doc.items = [_clean(i) if not i.startswith('<div class="code">') else i for i in doc.items]
doc.write("docs/%s.html" % SLUG)
