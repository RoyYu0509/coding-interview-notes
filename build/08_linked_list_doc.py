# 08 · Linked List 正文 (NeetCode 式讲法)。由 08_linked_list.py 末尾 exec。
EX = os.path.join(SVG_DIR, "%s_examples.svg")
EXS = SLUG + "/%s_examples.svg"
SV = lambda n: SLUG + "/" + n

# ---------------------------------------------------------------- 例子图
nc.examples_svg(EX % "reverse", "Reverse Linked List examples", ["把一条 singly linked list 反过来, 返回新的 head"], [
    dict(title="Example:  1 → 2 → 3 → 4 → 5  →  5 → 4 → 3 → 2 → 1", index=False, rows=[
        ("之前", ["1", "→", "2", "→", "3", "→", "4", "→", "5"], None), ("之后", ["5", "→", "4", "→", "3", "→", "2", "→", "1"], None)], cw=30,
         extra=["不是把值换位置, 而是把每个箭头掉头。空 list 返回 None"])],
    legend=[])
nc.examples_svg(EX % "merge", "Merge Two Sorted Lists examples", ["两条排好序的 linked list, 合并成一条排好序的 (直接把 node 接起来, 不新建)"], [
    dict(title="Example:  l1 = 1 → 2 → 4, l2 = 1 → 3 → 4  →  1 → 1 → 2 → 3 → 4 → 4", index=False, rows=[
        ("l1", [1, 2, 4], None), ("l2", [1, 3, 4], ["new"] * 3), ("结果", [1, 1, 2, 3, 4, 4], ["keep", "new", "keep", "new", "keep", "new"])])],
    legend=[("keep", "来自 l1"), ("new", "来自 l2")])
nc.examples_svg(EX % "cycle", "Linked List Cycle examples", ["判断 linked list 里有没有环: 顺着 next 一直走, 会不会走回之前走过的 node"], [
    dict(title="Example 1:  3 → 2 → 0 → -4 → (回到 2)  →  True", items=["3", "2", "0", "-4"], hl=[1, 2, 3], extra=["-4 的 next 指回了 2, 2 0 -4 构成一个环"]),
    dict(title="Example 2:  1 → 2 → None  →  False")],
    legend=[("new", "环上的 node")])
nc.examples_svg(EX % "middle", "Middle of the Linked List examples", ["返回中间的 node。有两个中间的 (偶数个) 时, 返回第二个"], [
    dict(title="Example 1:  1 → 2 → 3 → 4 → 5  →  3", items=[1, 2, 3, 4, 5], hl=[2]),
    dict(title="Example 2:  1 → 2 → 3 → 4 → 5 → 6  →  4", items=[1, 2, 3, 4, 5, 6], hl=[3], extra=["中间有 3 和 4 两个, 返回第二个 4"])],
    legend=[("new", "中间的 node")])
nc.examples_svg(EX % "remove", "Remove Nth Node From End examples", ["删掉倒数第 n 个 node, 返回 head。要求只遍历一遍"], [
    dict(title="Example 1:  1 → 2 → 3 → 4 → 5, n = 2  →  1 → 2 → 3 → 5", items=[1, 2, 3, 4, 5], bad=[(3, 3, "倒数第 2 个")]),
    dict(title="Example 2:  [1], n = 1  →  []", extra=["删掉的正好是 head, 结果是空 list"])],
    legend=[("rem", "要删的")])
nc.examples_svg(EX % "add", "Add Two Numbers examples", ["两个非负整数, 每一位存在一个 node 里, 倒着存 (个位在最前面)。把两数之和也用同样的方式返回"], [
    dict(title="Example:  l1 = 2 → 4 → 3, l2 = 5 → 6 → 4  →  7 → 0 → 8", index=False, rows=[
        ("l1 (342)", [2, 4, 3], None), ("l2 (465)", [5, 6, 4], None), ("和 (807)", [7, 0, 8], ["new"] * 3)],
         extra=["342 + 465 = 807。十位 4 + 6 = 10, 写 0 进 1"])],
    legend=[])
nc.examples_svg(EX % "revk", "Reverse Nodes in k-Group examples", ["每 k 个 node 一组, 组内反转。最后不够 k 个的保持原样"], [
    dict(title="Example 1:  1 → 2 → 3 → 4 → 5, k = 2  →  2 → 1 → 4 → 3 → 5", items=[2, 1, 4, 3, 5], hl=[0, 1, 2, 3], index=False),
    dict(title="Example 2:  1 → 2 → 3 → 4 → 5, k = 3  →  3 → 2 → 1 → 4 → 5", items=[3, 2, 1, 4, 5], hl=[0, 1, 2], index=False,
         extra=["4 → 5 只有 2 个, 不够 3, 不动"])],
    legend=[("new", "反转过的组")])
nc.examples_svg(EX % "copy", "Copy List with Random Pointer examples", ["每个 node 除了 next, 还有一个 random 指针, 可以指向任何 node 或 None。返回整条 list 的深拷贝"], [
    dict(title="Example:  [[7,null],[13,0],[11,4],[10,2],[1,0]]", items=["7", "13", "11", "10", "1"], cw=44,
         extra=["每对是 [值, random 指向的下标]。比如 13 的 random 指向下标 0 的 7",
                "新 list 里的 next 和 random 都必须指向新建的 node, 不能指回原来的"])],
    legend=[])
nc.examples_svg(EX % "pal", "Palindrome Linked List examples", ["判断 linked list 的值正着读和反着读是不是一样。最好 O(1) 额外空间"], [
    dict(title="Example 1:  1 → 2 → 2 → 1  →  True", items=[1, 2, 2, 1]),
    dict(title="Example 2:  1 → 2  →  False", items=[1, 2])],
    legend=[])

# ================================================================ HTML
doc = d.Doc("08 · Linked List")
doc.h2("这篇讲什么")
doc.p("linked list (链表) 是一串 node, 每个 node 有一个值 <code>val</code> 和一个指向下一个 node 的 <code>next</code>。最后一个 node 的 next 是 None。手里通常只有第一个 node, 叫 head。")
doc.p("和数组比, 它有一个根本的限制: <b>不能按下标直接访问, 只能从 head 开始顺着 next 一个一个往后走</b>。好处是只要手里有某个 node, 在它后面插入或删除都是 <code>O(1)</code>, 改一下 next 就行。")
doc.p("所以 linked list 的题, 本质上都是在<b>改 next 指针</b>。容易出错的地方也都在这里: 改了某个 node 的 next 之后, 原来它后面的那些 node 就找不到了。所有技巧都是为了避免这个问题:")
doc.svg(SV("core.svg"), "上: 直接改 next 会丢掉后面的 node。中: 先用一个变量存下来再改。下: dummy node 让\"改 head\"不用特判。")
nc.bullets(doc, "<b>改 next 之前, 先把以后要用的 node 存进变量</b>。", "<b>dummy node</b>: 在 head 前面放一个假的 node, 这样 head 也有\"前一个\", 删除或替换 head 时不用特判。最后返回 <code>dummy.next</code>。",
           "<b>快慢指针</b>: 两个指针用不同的速度走, 用来找中点、找倒数第 n 个、判断有没有环。")
nc.solution(doc, CODE["node"], summary="ListNode 的定义")
nc.table(doc, ["#", "题目", "考过的公司数", "相比上一题多了什么"], [
    ["1", "Reverse Linked List", cnt("Reverse Linked List"), "模板题: 改 next 前先存"],
    ["2", "Merge Two Sorted Lists", cnt("Merge Two Sorted Lists"), "dummy node + tail 指针"],
    ["3", "Middle of the Linked List / Linked List Cycle", "%d / %d" % (cnt("Middle of the Linked List"), cnt("Linked List Cycle")), "快慢指针"],
    ["4", "Remove Nth Node From End of List", cnt("Remove Nth Node From End of List"), "两个指针拉开固定距离"],
    ["5", "Add Two Numbers", cnt("Add Two Numbers"), "边走边建新 list, 处理进位"],
    ["6", "Reverse Nodes in k-Group", cnt("Reverse Nodes in k-Group"), "第 1 题的局部版本, 反转后接回去"],
    ["7", "Copy List with Random Pointer", cnt("Copy List with Random Pointer"), "dict 记 old → new"],
    ["8", "Palindrome Linked List", cnt("Palindrome Linked List"), "第 3 题 + 第 1 题组合"]])
doc.p("每道题的顺序: <b>题目在问什么 → 看例子 → brute force → intuition → 算法 → 手动走一遍 → 复杂度</b>。代码放在最后, 默认折叠。")
doc.p("LRU Cache (dict + 双向链表) 在 17 · Design; Merge k Sorted Lists 在 09 · Heap。")

# ================================================================ 1
doc.h2("1. Reverse Linked List")
doc.h3("题目在问什么")
doc.p("给一条 linked list 的 head, 把它反转, 返回新的 head。")
doc.h3("看例子")
doc.svg(EXS % "reverse", "例子。")
doc.h3("Brute force")
doc.p("把所有值读进一个数组, 反过来再建一条新 list。<code>O(n)</code> 时间, 但用了 <code>O(n)</code> 额外空间, 而且没有真正\"反转\"原来的 list。")
doc.h3("Intuition: 每个箭头掉头")
doc.p("反转就是让每个 node 的 next 指向它<b>前面</b>的那个 node。从左往右走, 每到一个 node (叫 curr), 把它的 next 改成指向前一个 (叫 prev)。")
doc.p("问题是: 改完 <code>curr.next = prev</code> 之后, curr 原来后面的 node 就找不到了 (上面那张图的情况)。所以改之前, 先用 <code>nxt</code> 把它存下来。")
doc.p("每一步四个动作, 顺序不能乱: 存下一个 → 掉头 → prev 前进 → curr 前进。")
doc.h3("算法")
nc.steps(doc, "<code>prev = None</code>, <code>curr = head</code>。",
         "当 curr 不是 None: <code>nxt = curr.next</code>; <code>curr.next = prev</code>; <code>prev = curr</code>; <code>curr = nxt</code>。",
         "返回 prev (curr 走出末尾时, prev 是原来的最后一个, 也就是新的 head)。")
doc.h3("手动走一遍")
doc.svg(SV("reverse_trace.svg"), "每一步: 绿色箭头是刚掉头的 next, 红色虚线是刚被断开的旧 next (它指向的 node 已经先存进了 nxt)。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(1)</code>。")
nc.solution(doc, CODE["reverse"])
doc.note("改 next 之前, 先存下以后还要用的 node。反转: nxt = curr.next → curr.next = prev → prev = curr → curr = nxt。")

# ================================================================ 2
doc.h2("2. Merge Two Sorted Lists")
doc.h3("题目在问什么")
doc.p("两条排好序的 linked list, 合并成一条排好序的 linked list。直接把原来的 node 接起来, 不新建 node。")
doc.h3("看例子")
doc.svg(EXS % "merge", "例子。")
doc.h3("Brute force")
doc.p("把所有值读出来排序, 再建新 list。<code>O((m+n) log(m+n))</code>, 没用上\"已经排好序\"。")
doc.h3("Intuition: 每次取两个头里小的那个")
doc.p("和 02 里合并两个有序数组一样: 两条 list 当前的头里, 小的那个一定是剩下所有 node 里最小的, 把它接到结果后面, 那条 list 往后走一步。")
doc.p("两个技巧:")
nc.bullets(doc, "<b>dummy</b>: 结果 list 一开始是空的, 第一次接的时候要特判 \"结果的 head 是谁\"。放一个假的 dummy 当头, 永远往它后面接, 最后返回 dummy.next。",
           "<b>tail</b>: 一直指向结果的最后一个 node, 接的时候直接 <code>tail.next = ...</code>, 不用每次从头走。")
doc.p("一条走完之后, 另一条剩下的部分本来就是排好序的, 直接接上。")
doc.h3("算法")
nc.steps(doc, "<code>dummy = tail = ListNode()</code>。",
         "当两条都没走完: 小的那个接到 tail 后面, 它那条 list 往后走; <code>tail = tail.next</code>。",
         "<code>tail.next = l1 or l2</code>。返回 dummy.next。")
doc.h3("手动走一遍")
doc.svg(SV("merge_trace.svg"), "每一步比较两个头, 小的 (相等时取 l1) 接到结果后面。")
doc.h3("复杂度")
doc.p("Time <code>O(m + n)</code>, Space <code>O(1)</code>。")
nc.solution(doc, CODE["merge"])
doc.note("要建一条新的结果 list: dummy 当头 + tail 指向末尾, 最后返回 dummy.next。")

# ================================================================ 3
doc.h2("3. Middle of the Linked List / Linked List Cycle")
doc.h3("题目在问什么")
doc.p("<b>Middle</b>: 返回中间的 node, 偶数个时返回第二个中间的。<b>Cycle</b>: 判断 list 里有没有环 (顺着 next 走会不会走回来)。")
doc.h3("看例子")
doc.svg(EXS % "middle", "Middle 的例子。")
doc.svg(EXS % "cycle", "Cycle 的例子。")
doc.h3("Brute force")
doc.p("Middle: 先走一遍数出长度 n, 再走 n/2 步。要走两遍。")
doc.p("Cycle: 用一个 set 记下走过的 node, 走到已经在 set 里的就是有环。<code>O(n)</code> 空间。")
doc.h3("Intuition: 两个指针, 一个快一个慢")
doc.p("让 slow 每次走 1 步, fast 每次走 2 步, 同时从 head 出发。")
nc.bullets(doc, "<b>找中点</b>: fast 走的距离永远是 slow 的两倍。所以 fast 走到末尾时, slow 正好走了一半, 就在中间。只要一遍。",
           "<b>判断环</b>: 如果没有环, fast 会先走到 None。如果有环, 两个指针最后都会进入环里一直转圈; 在环里, fast 每一轮比 slow 多走 1 步, 两者之间的距离每轮缩小 1, 所以一定会在某一轮正好相遇。相遇就说明有环, 不需要 set。")
doc.h3("算法")
nc.steps(doc, "<code>slow = fast = head</code>。", "当 <code>fast and fast.next</code>: slow 走 1 步, fast 走 2 步。Cycle 版本里, 每走一次检查 <code>slow is fast</code>。",
         "Middle 返回 slow; Cycle 循环正常结束就返回 False。")
doc.h3("手动走一遍")
doc.svg(SV("fastslow_trace.svg"), "Middle: fast 走到最后时, slow 正好在 3。")
doc.svg(SV("cycle_trace.svg"), "Cycle: 进入环之后 fast 一点点追上 slow, 最后相遇。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(1)</code>。进阶 (Linked List Cycle II, 找环的入口): 相遇后让一个指针回到 head, 两个都每次走 1 步, 再次相遇的地方就是入口。")
nc.solution(doc, CODE["middle"], CODE["cycle"])
doc.note("快慢指针: slow 1 步, fast 2 步。fast 到末尾时 slow 在中间; 有环则一定相遇。")

# ================================================================ 4
doc.h2("4. Remove Nth Node From End of List")
doc.h3("题目在问什么")
doc.p("删掉 linked list 的<b>倒数第 n 个</b> node, 返回 head。要求只遍历一遍。")
doc.h3("看例子")
doc.svg(EXS % "remove", "两个例子。")
doc.p("Example 2 里删掉的是 head 本身, 用 dummy 可以避免特判。")
doc.h3("Brute force")
doc.p("先走一遍数出长度 L, 倒数第 n 个就是正数第 L - n + 1 个, 再走一遍找到它前面那个, 删掉。两遍。")
doc.h3("Intuition: 让两个指针隔开固定的距离")
doc.p("要删一个 node, 得停在它<b>前面</b>那个 node 上, 才能改 next 跳过它。")
doc.p("让 fast 先走 n + 1 步, 然后 fast 和 slow 一起走。两者之间的距离一直是 n + 1。当 fast 走出末尾 (变成 None) 时, slow 离末尾正好 n + 1 步, 也就是停在倒数第 n 个的前一个。")
doc.p("从 dummy 出发 (不是 head), 这样要删 head 时, slow 正好停在 dummy 上, 不用特判。")
doc.h3("算法")
nc.steps(doc, "<code>dummy = ListNode(0, head)</code>, <code>fast = slow = dummy</code>。",
         "fast 先走 n + 1 步。", "当 fast 不是 None: 两个一起走一步。",
         "<code>slow.next = slow.next.next</code>。返回 dummy.next。")
doc.h3("手动走一遍")
doc.svg(SV("remove_trace.svg"), "n = 2: fast 先走 3 步; 一起走到 fast = None 时, slow 停在 3; 让 3 直接指向 5。")
doc.h3("复杂度")
doc.p("Time <code>O(L)</code>, 一遍。Space <code>O(1)</code>。")
nc.solution(doc, CODE["remove_nth"])
doc.note("倒数第 n 个: fast 先走 n (+1) 步, 再一起走; 从 dummy 出发, 删 head 不用特判。")

# ================================================================ 5
doc.h2("5. Add Two Numbers")
doc.h3("题目在问什么")
doc.p("两个非负整数, 每一位存在一个 node 里, 而且是<b>倒着</b>存的 (个位在第一个 node)。把两数之和用同样的格式返回。")
doc.h3("看例子")
doc.svg(EXS % "add", "例子。")
doc.h3("Brute force")
doc.p("把两条 list 转成整数, 相加, 再转回 list。在 Python 里能做 (整数没有上限), 但在其他语言里会溢出, 面试官想看的是逐位相加。")
doc.h3("Intuition: 就是竖式加法")
doc.p("倒着存的好处是: 从 head 开始走, 正好是从个位开始, 和手算竖式加法的顺序一样。")
doc.p("每一位: <code>s = carry + l1 这一位 + l2 这一位</code> (哪条走完了就当 0)。新的这一位是 <code>s % 10</code>, 进位 <code>carry = s // 10</code>。建一个新 node 接到结果后面 (用第 2 题的 dummy + tail)。")
doc.p("循环条件是 <code>l1 or l2 or carry</code>: 两条都走完了但还有进位时, 还要再加一个 node, 比如 5 + 5 = 10。")
doc.h3("算法")
nc.steps(doc, "<code>dummy = tail = ListNode()</code>, <code>carry = 0</code>。",
         "当 l1 或 l2 或 carry: 加起来, <code>carry, digit = divmod(s, 10)</code>, 新建 node(digit) 接到 tail 后面。",
         "返回 dummy.next。")
doc.h3("手动走一遍")
doc.svg(SV("add_trace.svg"), "342 + 465: 每一步写出 s = carry + 两个数字, 以及新的 digit 和 carry。")
doc.h3("复杂度")
doc.p("Time <code>O(max(m, n))</code>, Space <code>O(max(m, n))</code> (结果)。")
nc.solution(doc, CODE["add"])
doc.note("逐位相加: 边走边建新 node, 处理进位; 循环条件里别忘了 carry。")

# ================================================================ 6
doc.h2("6. Reverse Nodes in k-Group")
doc.h3("题目在问什么")
doc.p("每 k 个 node 一组, 每组内部反转。最后剩下的不够 k 个, 保持原样。只能改 next, 不能改 val。")
doc.h3("看例子")
doc.svg(EXS % "revk", "两个例子。")
doc.h3("Brute force")
doc.p("把值读进数组, 每 k 个反转一次, 再写回去。但题目不允许改 val, 而且要 <code>O(1)</code> 空间。")
doc.h3("Intuition: 第 1 题的局部版本, 反转完再接回去")
doc.p("对每一组, 做三件事:")
nc.steps(doc, "<b>确认够 k 个</b>: 从上一组的最后一个 (group_prev) 往后数 k 个, 找到这一组的第 k 个 (kth)。不够就结束。",
         "<b>组内反转</b>: 和第 1 题完全一样, 只是 prev 一开始不是 None, 而是这一组<b>后面</b>的那个 node (group_next)。这样反转完, 这一组原来的第一个 node 自然就指向了后面。",
         "<b>接回前面</b>: 上一组的最后一个 (group_prev) 原来指向这一组的第一个, 现在要改成指向 kth (这一组新的头)。原来的第一个变成了这一组的最后一个, 它就是下一组的 group_prev。")
doc.p("用 dummy 当第一个 group_prev, 这样第一组也不用特判。")
doc.h3("算法")
nc.steps(doc, "<code>dummy = ListNode(0, head)</code>, <code>group_prev = dummy</code>。",
         "循环: 找 kth, 找不到就返回 dummy.next。",
         "<code>group_next = kth.next</code>; 用 prev = group_next 反转这一组。",
         "<code>first = group_prev.next</code>; <code>group_prev.next = kth</code>; <code>group_prev = first</code>。")
doc.h3("手动走一遍")
doc.svg(SV("revk_trace.svg"), "k = 2: 每组反转后接回前后, 最后的 5 不够一组。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(1)</code>。Reverse Linked List II (反转第 left 到 right 个) 是同样的\"局部反转 + 接回\"。")
nc.solution(doc, CODE["reverse_k"])
doc.note("反转一段: 记住这一段前面的 node 和后面的 node, 段内照第 1 题反转, 再把前后接上。")

# ================================================================ 7
doc.h2("7. Copy List with Random Pointer")
doc.h3("题目在问什么")
doc.p("每个 node 除了 next, 还有一个 <code>random</code> 指针, 可以指向 list 里任意一个 node 或者 None。返回这条 list 的<b>深拷贝</b>: 每个 node 都新建, 新 list 的 next 和 random 都要指向新的 node。")
doc.h3("看例子")
doc.svg(EXS % "copy", "例子。")
doc.h3("Brute force")
doc.p("先按 next 复制出新 list。然后对每个新 node, 要找它的 random 应该指向哪个新 node: 从原 list 的 head 开始数, 原 node 的 random 是第几个, 再在新 list 里数到第几个。每个都要 <code>O(n)</code>, 共 <code>O(n²)</code>。")
doc.h3("Intuition: 用 dict 从\"原 node\"直接找到\"对应的新 node\"")
doc.p("难点就是: 知道原 node 的 random 是 X, 怎么快速找到 X 对应的新 node? 用一个 dict <code>old2new</code> 记下每个原 node 对应的新 node。")
doc.p("分两遍: 第一遍只新建 node, 填好 old2new; 第二遍再连 next 和 random: <code>new.next = old2new[old.next]</code>, <code>new.random = old2new[old.random]</code>。必须分两遍, 因为 random 可能指向后面还没建的 node。")
doc.p("这和 12 里的 Clone Graph 是同一个思路。")
doc.h3("算法")
nc.steps(doc, "<code>old2new = {None: None}</code>。第一遍: 每个 node 新建一个, 放进 old2new。",
         "第二遍: 按 old2new 连每个新 node 的 next 和 random。", "返回 old2new[head]。")
doc.h3("手动走一遍")
doc.svg(SV("copy_trace.svg"), "第 1 遍只建 node; 第 2 遍查表连箭头。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(n)</code>。另有 <code>O(1)</code> 空间的做法: 把每个新 node 插在原 node 后面, 利用相对位置找 random, 最后再拆开。面试里 dict 写法就够了。")
nc.solution(doc, CODE["copy"])
doc.note("复制带额外指针的结构: dict old → new, 第一遍建 node, 第二遍连指针。")

# ================================================================ 8
doc.h2("8. Palindrome Linked List")
doc.h3("题目在问什么")
doc.p("判断 linked list 的值正着读和反着读是不是一样。最好 <code>O(n)</code> 时间、<code>O(1)</code> 额外空间。")
doc.h3("看例子")
doc.svg(EXS % "pal", "两个例子。")
doc.h3("Brute force")
doc.p("把值读进数组, 判断数组是不是回文。<code>O(n)</code> 空间。")
doc.h3("Intuition: 把前面学过的两招组合起来")
doc.p("回文要\"从两头往中间比\", 但 singly linked list 不能从后往前走。办法是把<b>后半段反转</b>, 这样就可以从两头同时往中间走了。")
nc.steps(doc, "用第 3 题的快慢指针找到中点。", "用第 1 题把后半段反转。", "一个指针从 head、一个从反转后的后半段开头, 一起往中间走, 逐个比较。")
doc.h3("算法")
nc.steps(doc, "快慢指针: 结束时 slow 在中间。", "从 slow 开始反转, 得到后半段的新头 prev。", "left = head, right = prev, 当 right 不是 None: 值不同就返回 False, 否则都往后走。", "返回 True。")
doc.h3("手动走一遍")
doc.svg(SV("pal_trace.svg"), "1 → 2 → 3 → 2 → 1: 找中点, 反转后半段, 再从两头比。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(1)</code>。面试时可以提一句: 这样会修改原 list, 如果需要, 最后再把后半段反转回去。")
nc.solution(doc, CODE["palindrome"])
doc.note("linked list 上要\"从后往前\": 反转后半段。很多难题就是 快慢指针 + 反转 + 合并 的组合 (比如 Reorder List)。")

# ================================================================ 识别信号
doc.h2("9. 识别信号: 看到什么, 就想到什么")
nc.table(doc, ["题目特征", "做法", "complexity"], [
    ["反转整条 / 一段 list", "prev / curr / nxt 三个指针, 改 next 前先存", "空间 <code>O(n)</code> → <code>O(1)</code>"],
    ["要建一条新的结果 list, 或者可能删 head", "dummy node (+ tail)", "省掉特判"],
    ["合并两条有序 list", "每次取小的头接到 tail", "<code>O(m + n)</code>"],
    ["找中点 / 判断有没有环", "快慢指针 (1 步 / 2 步)", "空间 <code>O(n)</code> → <code>O(1)</code>"],
    ["倒数第 n 个", "fast 先走 n 步, 再一起走", "两遍 → 一遍"],
    ["逐位运算 (加法)", "边走边建, 处理 carry", "<code>O(n)</code>"],
    ["每 k 个一组处理", "找 kth, 段内反转, 接回前后", "<code>O(n)</code>, <code>O(1)</code> 空间"],
    ["复制带 random / 图的结构", "dict old → new, 两遍", "<code>O(n²)</code> → <code>O(n)</code>"],
    ["回文 / 需要从后往前", "找中点 + 反转后半段", "空间 <code>O(n)</code> → <code>O(1)</code>"]])
doc.p("linked list 的题几乎都是这几招的组合: dummy、改 next 前先存、快慢指针、反转。画图是最好的调试方法: 每改一个 next, 都在纸上画出来。")

doc.h2("以后再学")
doc.p("Linked List Cycle II (找环的入口)、Reorder List (中点 + 反转 + 交替合并)、Intersection of Two Linked Lists (两个指针走完自己的再走对方的)、Sort List (merge sort)。")
doc.write("docs/08-linked-list.html")
