# 02 · Two Pointers 正文 (NeetCode 式讲法)。由 02_two_pointers.py 末尾 exec, 共用 doc / CODE / NS / SLUG。
import nclib as nc
from counts import cnt

EX = os.path.join(d.ROOT, "docs", "svg", SLUG, "%s_examples.svg")
steps = lambda *a: nc.steps(doc, *a)

# ---------------------------------------------------------------- 例子图
assert NS["two_sum_sorted"]([2, 7, 11, 15], 9) == [0, 1]
assert NS["two_sum_sorted"]([1, 3, 4, 6, 9, 12, 14], 16) == [2, 5]
nc.examples_svg(EX % "two_sum_ii", "Two Sum II examples", ["数组已经从小到大排好。找两个不同位置的数, 和等于 target"], [
    dict(title="Example 1:  nums = [2,7,11,15], target = 9  →  [0, 1]", items=[2, 7, 11, 15], hl=[0, 1],
         ans_text="2 + 7 = 9"),
    dict(title="Example 2:  nums = [1,3,4,6,9,12,14], target = 16  →  [2, 5]", items=[1, 3, 4, 6, 9, 12, 14],
         hl=[2, 5], ans_text="4 + 12 = 16",
         extra=["LeetCode 原题要求返回 1-indexed 的下标 [3, 6], 这里为了统一写成 0-indexed"])],
    legend=[("new", "答案的两个数")])

assert sorted(NS["three_sum"]([-1, 0, 1, 2, -1, -4])) == [[-1, -1, 2], [-1, 0, 1]]
assert NS["three_sum"]([0, 1, 1]) == []
nc.examples_svg(EX % "three_sum", "3Sum examples", ["找出所有三个数加起来等于 0 的组合, 同样的组合只能出现一次"], [
    dict(title="Example 1:  nums = [-1,0,1,2,-1,-4]  →  [[-1,-1,2], [-1,0,1]]", items=[-1, 0, 1, 2, -1, -4], cw=40,
         extra=["(-1) + (-1) + 2 = 0;  (-1) + 0 + 1 = 0",
                "index 0 的 -1 和 index 4 的 -1 都能和 0, 1 组成 [-1,0,1], 但这是同一个组合, 只算一次"]),
    dict(title="Example 2:  nums = [0,1,1]  →  []", items=[0, 1, 1], extra=["只有一种选法 0 + 1 + 1 = 2 ≠ 0"]),
    dict(title="Example 3:  nums = [0,0,0]  →  [[0,0,0]]", items=[0, 0, 0], hl=[0, 1, 2])],
    legend=[("new", "答案")])

assert NS["max_area"]([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
assert NS["max_area"]([1, 1]) == 1
nc.examples_svg(EX % "container", "Container With Most Water examples",
                ["选两根竖线, 和 x 轴围成一个容器。水的高度 = 两根里较矮的那根, 宽度 = 下标之差。求最大面积"], [
    dict(title="Example 1:  height = [1,8,6,2,5,4,8,3,7]  →  49", items=[1, 8, 6, 2, 5, 4, 8, 3, 7], hl=[1, 8],
         ans_text="min(8, 7) × (8 - 1) = 7 × 7 = 49",
         bad=[(1, 6, "8 和 8 更高, 但宽度只有 5: 8 × 5 = 40")]),
    dict(title="Example 2:  height = [1,1]  →  1", items=[1, 1], hl=[0, 1], ans_text="min(1, 1) × 1 = 1")],
    legend=[("new", "选中的两根线"), ("rem", "看起来像, 但不对")])

assert NS["trap"]([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
assert NS["trap"]([2, 0, 1, 3, 0, 1, 2]) == 6
nc.examples_svg(EX % "trap", "Trapping Rain Water examples",
                ["height[i] 是第 i 根柱子的高度, 宽度都是 1。下雨后, 柱子之间一共能存多少水"], [
    dict(title="Example:  height = [2,0,1,3,0,1,2]  →  6", items=[2, 0, 1, 3, 0, 1, 2], hl=[1, 2, 4, 5],
         ans_text="每格的水: 0, 2, 1, 0, 2, 1, 0",
         extra=["index 1: 左边最高 2, 右边最高 3, 水能涨到 min(2, 3) = 2, 柱子高 0 → 存 2 - 0 = 2",
                "index 4: 左边最高 3, 右边最高 2, 水涨到 2, 柱子高 0 → 存 2",
                "两端 (index 0 和 6) 存不了水: 一边没有墙, 水会流走。合计 2 + 1 + 2 + 1 = 6"])],
    legend=[("new", "能存水的格子")])

nc.examples_svg(EX % "move_zeroes", "Move Zeroes examples", ["把所有 0 移到最后, 非零的数保持原来的先后顺序, 必须在原数组上改"], [
    dict(title="Example:  [0,1,0,3,12]  →  [1,3,12,0,0]",
         rows=[("改之前", [0, 1, 0, 3, 12], ["rem", "new", "rem", "new", "new"]),
               ("改之后", [1, 3, 12, 0, 0], ["new", "new", "new", "rem", "rem"])],
         extra=["非零的数 1, 3, 12 先后顺序没变。不能写成 [12, 3, 1, 0, 0]"])],
    legend=[("new", "非零 (保持顺序)"), ("rem", "0")])

nc.examples_svg(EX % "remove_dup", "Remove Duplicates examples",
                ["数组已排好序。原地删掉重复的数, 每个值只留一个, 返回留下了几个 (前 k 格就是结果, 后面是什么不重要)"], [
    dict(title="Example:  [0,0,1,1,1,2,2,3]  →  4", rows=[
        ("改之前", [0, 0, 1, 1, 1, 2, 2, 3], ["new", "rem", "new", "rem", "rem", "new", "rem", "new"]),
        ("改之后", [0, 1, 2, 3, "_", "_", "_", "_"], ["new"] * 4 + ["keep"] * 4)],
         extra=["前 4 格是 [0, 1, 2, 3], 返回 4。后面的 _ 是什么都可以"])],
    legend=[("new", "留下"), ("rem", "重复的"), ("keep", "不关心")])

nc.examples_svg(EX % "sort_colors", "Sort Colors examples", ["数组里只有 0, 1, 2 三种数 (三种颜色)。原地排成 0...0 1...1 2...2, 不能用 sort"], [
    dict(title="Example:  [2,0,2,1,1,0]  →  [0,0,1,1,2,2]", rows=[
        ("改之前", [2, 0, 2, 1, 1, 0], None),
        ("改之后", [0, 0, 1, 1, 2, 2], ["new", "new", "keep", "keep", "rem", "rem"])],
         extra=["相当于把数组切成三块: 左边全是 0, 中间全是 1, 右边全是 2"])],
    legend=[("new", "0"), ("keep", "1"), ("rem", "2")])

nc.examples_svg(EX % "merge", "Merge Sorted Array examples",
                ["nums1 前 m 个是有效的数, 后面 n 格是空位; nums2 有 n 个数。两个都已排序, 合并进 nums1, 结果也要有序"], [
    dict(title="Example:  nums1 = [1,2,3,_,_,_], m = 3, nums2 = [2,5,6], n = 3", rows=[
        ("nums1", [1, 2, 3, "_", "_", "_"], ["keep"] * 3 + ["rem"] * 3),
        ("nums2", [2, 5, 6], ["new"] * 3),
        ("结果", [1, 2, 2, 3, 5, 6], ["keep", "keep", "new", "keep", "new", "new"])],
         extra=["结果直接写在 nums1 里, 不能另开数组返回"])],
    legend=[("keep", "来自 nums1"), ("new", "来自 nums2"), ("rem", "空位")])

assert NS["is_palindrome"]("A man, a plan, a canal: Panama") is True
assert NS["is_palindrome"]("race a car") is False
assert NS["valid_palindrome_ii"]("abca") is True
assert NS["valid_palindrome_ii"]("abc") is False
nc.examples_svg(EX % "valid_palindrome", "Valid Palindrome examples",
                ["只看字母和数字, 不分大小写, 正着读和反着读一样就是 palindrome (回文)"], [
    dict(title="Example 1:  \"A man, a plan, a canal: Panama\"  →  True",
         extra=["去掉空格和标点, 全变小写: \"amanaplanacanalpanama\", 反过来也一样"]),
    dict(title="Example 2:  \"race a car\"  →  False", extra=["变成 \"raceacar\", 反过来是 \"racaecar\", 不一样"]),
    dict(title="II, Example:  \"abca\"  →  True (最多删一个字符)", items=list("abca"), bad=[(2, 2, "删掉 c")],
         extra=["删掉 index 2 的 c 得到 \"aba\", 是回文。\"abc\" 删哪个都不行 → False"])],
    legend=[("rem", "要删掉的字符")])

# ================================================================ HTML
doc.h2("这篇讲什么")
doc.p("很多数组题的 brute force 是两层循环: 把所有的 pair (i, j) 都试一遍, <code>O(n²)</code>。"
      "<b>Two Pointers</b> 是用两个下标同时在数组上走, 每走一步都能说明\"有一大批 pair 不用再看了\", 于是只走 <code>O(n)</code> 步。")
doc.p("两个下标怎么放, 有三种常见的形状:")
nc.bullets(doc,
           "<b>相向</b>: 一个从最左边、一个从最右边, 往中间走。用于排好序的数组找 pair、左右对称的问题 (第 1–4、9 题)。",
           "<b>同向</b>: 两个都从左边出发, 一个快一个慢。一个负责读, 一个负责写, 用于原地删除、过滤 (第 5、6 题)。",
           "<b>各管一块</b>: 几个下标当作分界线, 把数组切成几个区, 或者两个数组各放一个下标 (第 7、8 题)。")
nc.table(doc, ["#", "题目", "考过的公司数", "相比上一题多了什么"], [
    ["1", "Two Sum II (sorted)", cnt("Two Sum II - Input Array Is Sorted"), "模板题: 相向, 比一次丢一个"],
    ["2", "3Sum", cnt("3Sum"), "三个数: 外面固定一个, 里面套第 1 题; 还要去重"],
    ["3", "Container With Most Water", cnt("Container With Most Water"), "数组没排序, 要自己证明该丢哪边"],
    ["4", "Trapping Rain Water", cnt("Trapping Rain Water"), "先写出每格的公式, 再用双指针算"],
    ["5", "Move Zeroes", cnt("Move Zeroes"), "换成同向: 一个读、一个写"],
    ["6", "Remove Duplicates from Sorted Array", cnt("Remove Duplicates from Sorted Array"), "同向, 只换\"留不留\"的条件"],
    ["7", "Sort Colors", cnt("Sort Colors"), "三个下标切出几个区"],
    ["8", "Merge Sorted Array", cnt("Merge Sorted Array"), "两个数组各一个下标, 从后往前"],
    ["9", "Valid Palindrome I / II", "%d / %d" % (cnt("Valid Palindrome"), cnt("Valid Palindrome II")), "左右对称; II 允许失配一次"]])
doc.p("每道题的顺序: <b>题目在问什么 → 看例子 → brute force → intuition → 算法 → 手动走一遍 → 复杂度</b>。代码放在最后, 默认折叠。")
doc.p("前置知识: 无。第 1 题如果数组没排序, 用 Hash Table 做 (见 01)。")

# ================================================================ 1
doc.h2("1. Two Sum II (Input Array Is Sorted)")
doc.h3("题目在问什么")
doc.p("和 Two Sum 一样: 找两个不同位置的数, 和等于 target。区别是这次数组<b>已经从小到大排好了</b>, 而且要求只用 <code>O(1)</code> 额外空间, 所以不能用 dict。")
doc.h3("看例子")
doc.svg(SLUG + "/two_sum_ii_examples.svg", "两个例子。")
doc.h3("Brute force: 所有 pair 都试")
doc.p("两层循环, 每个 pair (i, j) 都加一下, <code>O(n²)</code>。")
doc.p("把所有 pair 画成一张表格: 第 l 行第 r 列表示 <code>nums[l] + nums[r]</code>。brute force 就是把整张表的格子一个一个看过去。"
      "问题在于, 它完全没用上\"数组排好序\"这个信息。")
doc.h3("Intuition: 比一次, 能排除一整行")
doc.p("排好序意味着: 同一行从左往右, 和越来越大; 同一列从上往下, 和也越来越大。")
steps("从表格的右上角开始, 也就是 <code>l = 0</code> (最小的数) 和 <code>r = n - 1</code> (最大的数)。",
      "如果 <code>nums[l] + nums[r] < target</code>: nums[l] 和<b>最大</b>的数配都不够, 和其他任何数配只会更小。所以 nums[l] 不可能在答案里, 整行都可以划掉, <code>l += 1</code>。",
      "如果 <code>nums[l] + nums[r] > target</code>: 同理, nums[r] 和<b>最小</b>的数配都太大, 整列划掉, <code>r -= 1</code>。",
      "等于 target, 就找到了。")
doc.p("每比较一次, 就划掉一整行或一整列, 所以最多 n - 1 步。下面这张图就是这个过程:")
doc.svg(SLUG + "/template_core.svg", "每个格子是一个 pair。每一步比较划掉一整行或一整列, 总共只走 n - 1 步。")
doc.h3("算法")
steps("<code>l = 0</code>, <code>r = n - 1</code>。",
      "当 <code>l < r</code>: 算 <code>s = nums[l] + nums[r]</code>。",
      "<code>s == target</code> 返回; <code>s < target</code> 则 <code>l += 1</code>; <code>s > target</code> 则 <code>r -= 1</code>。")
doc.svg(SLUG + "/two_sum_ii_core.svg", "丢掉的那个数, 和它所有剩下的搭档加起来都不可能等于 target, 所以丢它不会错过答案。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/two_sum_ii_trace.svg", "nums = [1,3,4,6,9,12,14], target = 16: 4 步找到答案。依次丢掉 1、14、3, 然后 4 + 12 命中。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>: 每一步 l 加 1 或 r 减 1, 最多 n - 1 步。Space <code>O(1)</code>。")
nc.solution(doc, CODE["two_sum"])
doc.note("排好序 + 找 pair: 两个下标站两头。太小就移左边, 太大就移右边。每一步都排除一整批候选。")

# ================================================================ 抽象
doc.h2("把第 1 题抽象一下: 什么时候能用相向双指针")
doc.p("第 1 题能用双指针, 是因为每次比较之后, 都能<b>证明</b>其中一个下标再也不会出现在答案里, 可以放心丢掉。")
doc.p("所以判断能不能用相向双指针, 就问: <b>比较完 (l, r) 之后, 我能不能确定丢掉 l 或者丢掉 r 不会错过答案?</b> 能, 就可以 <code>O(n)</code>。")
doc.p("第 2–4 题都是这个思路, 区别只在于\"丢谁\"的理由不同。")
doc.note("相向双指针的核心: 每一步都要能证明\"丢掉这一边不会错过答案\"。")

# ================================================================ 2
doc.h2("2. 3Sum")
doc.h3("题目在问什么")
doc.p("给一个整数数组 (没排序)。找出<b>所有</b>满足 <code>a + b + c = 0</code> 的三元组。每个三元组只能出现一次, 比如 <code>[-1, 0, 1]</code> 和 <code>[0, -1, 1]</code> 算同一个。")
doc.h3("看例子")
doc.svg(SLUG + "/three_sum_examples.svg", "三个例子。")
doc.p("Example 1 里有两个 -1, 但 <code>[-1, 0, 1]</code> 只能输出一次。去重是这道题最容易错的地方。")
doc.h3("Brute force")
doc.p("三层循环试所有三元组, 再用 set 去重。<code>O(n³)</code>。")
doc.p("浪费在哪: 固定了前两个数 a 和 b 之后, 第三个数必须是 <code>-(a + b)</code>, 它是被确定的。但第三层循环还是一个一个去找它。")
doc.h3("Intuition: 固定一个, 剩下的就是第 1 题")
doc.p("先把数组排序。外层循环固定第一个数 <code>nums[i]</code>, 剩下的问题是: 在 i 右边找两个数, 和等于 <code>-nums[i]</code>。这正是第 1 题, 用相向双指针 <code>O(n)</code> 解决。")
doc.p("去重也因为排序变简单了: 相同的值挨在一起。<b>同一层里, 如果这个值和前一个一样, 就跳过</b>。需要跳的地方有两处:")
nc.bullets(doc, "外层: <code>nums[i] == nums[i-1]</code> 时跳过。否则同一个第一个数会算两遍。",
           "找到一组答案后, l 和 r 各自要跳过和刚才相同的值, 再继续找。")
doc.h3("算法")
steps("排序。",
      "i 从 0 走到 n - 3。如果 <code>i > 0</code> 且 <code>nums[i] == nums[i-1]</code>, 跳过。",
      "<code>l = i + 1</code>, <code>r = n - 1</code>, 按第 1 题找和为 <code>-nums[i]</code> 的 pair。",
      "找到一组: 记录, 然后 l 往右跳过所有相同的值, r 往左跳过所有相同的值。")
doc.svg(SLUG + "/three_sum_core.svg", "去重 = 在 i、l、r 三个位置, 都跳过\"和前一个值相同\"的位置。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/three_sum_trace.svg", "[-2,-2,0,0,2,2]: i = 0 找到唯一答案 [-2,0,2]; i = 1、3 和前一个值相同, 被跳过; i = 2 里层找不到。")
doc.h3("复杂度")
doc.p("Time <code>O(n²)</code>: 排序 <code>O(n log n)</code>, 外层 n 次, 每次里层 <code>O(n)</code>。Space <code>O(1)</code> (不算排序和输出)。")
doc.p("4Sum 是再套一层: 固定两个, 里层双指针, <code>O(n³)</code>。")
nc.solution(doc, CODE["three_sum"])
doc.note("k 个数的和: 排序, 固定 k - 2 个, 最里层用相向双指针。去重: 同一层不连续用同一个值。")

# ================================================================ 3
doc.h2("3. Container With Most Water")
doc.h3("题目在问什么")
doc.p("<code>height[i]</code> 是第 i 根竖线的高度。选两根线, 和 x 轴围成一个容器。能装的水 = 宽度 × 高度, 宽度是两根线的下标差, 高度是<b>两根里较矮的那根</b> (水会从矮的那边溢出)。求最大能装多少。")
doc.h3("看例子")
doc.svg(SLUG + "/container_examples.svg", "两个例子。")
doc.p("Example 1 说明: 两根最高的线不一定最好, 宽度也很重要。")
doc.h3("Brute force")
doc.p("所有 pair 都算一遍面积, 取最大。<code>O(n²)</code>。")
doc.h3("Intuition: 丢掉矮的那根")
doc.p("这题数组没排序, 也没有 target, 但还是可以\"比一次丢一个\"。")
steps("从最宽的开始: <code>l = 0</code>, <code>r = n - 1</code>。",
      "假设 <code>height[l] < height[r]</code>。考虑所有\"保留 l, 换掉 r\"的选择: 宽度只会更小 (r 往里走); 高度不会超过 height[l], 因为 l 是矮的那根, 它把高度封顶了。",
      "所以保留 l 的所有其他选择, 面积都不会比现在大。l 可以丢掉, <code>l += 1</code>。",
      "反过来 height[r] 更矮就丢 r。")
doc.p("一句话: <b>矮的那根限制了结果, 留着它只会越来越差</b>。")
doc.h3("算法")
steps("<code>l = 0</code>, <code>r = n - 1</code>, <code>best = 0</code>。",
      "算面积 <code>min(height[l], height[r]) × (r - l)</code>, 更新 best。",
      "矮的那边往里移一格。重复直到 l 和 r 相遇。")
doc.svg(SLUG + "/container_core.svg", "保留矮墙、换掉另一根: 面积上界只会变小, 所以矮墙可以丢。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/container_trace.svg", "49 在第 2 步就出现了, 后面 6 步都是在确认没有更大的。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(1)</code>。")
nc.solution(doc, CODE["container"])
doc.note("求 f(l, r) 的最大值, 往里收的时候宽度变小: 从最宽开始, 每次丢掉\"限制了结果\"的那一边。")

# ================================================================ 4
doc.h2("4. Trapping Rain Water")
doc.h3("题目在问什么")
doc.p("<code>height[i]</code> 是第 i 根柱子的高度, 每根宽度为 1。下雨之后, 柱子之间的凹槽会存水。问一共能存多少水。")
doc.h3("看例子")
doc.svg(SLUG + "/trap_examples.svg", "一个例子, 每一格的水都算出来了。")
doc.p("从例子里能看出一个规律: <b>每一格能存多少水, 只取决于它左边最高的柱子和右边最高的柱子</b>。水面高度是这两个里较矮的那个, 减去这一格自己的高度。")
doc.h3("Brute force")
doc.p("每一格 i: 往左扫一遍找最高, 往右扫一遍找最高, 算 <code>min(左最高, 右最高) - height[i]</code>。每格 <code>O(n)</code>, 共 <code>O(n²)</code>。")
doc.p("浪费: 相邻两格的\"左边最高\"几乎一样, 却每次重新扫。")
doc.h3("Intuition 1: 先把左最高、右最高都算好")
doc.p("用两个数组: <code>lmax[i]</code> = 0..i 里最高的, 从左往右一遍就能算; <code>rmax[i]</code> = i..n-1 里最高的, 从右往左一遍。然后每格直接套公式。<code>O(n)</code> 时间, <code>O(n)</code> 空间。")
doc.h3("Intuition 2: 其实只需要知道哪边更矮")
doc.p("公式里用的是 <code>min(lmax, rmax)</code>。我们其实不需要两个值都精确知道, 只需要知道<b>哪个更小</b>。")
steps("用两个下标: l 从左走, r 从右走。<code>lmax</code> = l 左边 (含 l) 最高的, <code>rmax</code> = r 右边 (含 r) 最高的。",
      "如果 <code>lmax < rmax</code>: 对 l 这一格来说, 它右边至少有一根 rmax 那么高的柱子, 比 lmax 高。所以 l 的\"右边最高\" ≥ rmax > lmax, min 一定是 lmax。l 的水位已经确定了: <code>lmax - height[l]</code>。算完 l 往右走。",
      "反过来 <code>rmax ≤ lmax</code>, 就确定了 r 的水位, r 往左走。")
doc.p("这样只用两个变量, 空间降到 <code>O(1)</code>。")
doc.h3("算法")
steps("<code>l = 0</code>, <code>r = n - 1</code>, <code>lmax = rmax = 0</code>, <code>water = 0</code>。",
      "每一步先更新 <code>lmax = max(lmax, height[l])</code>, <code>rmax = max(rmax, height[r])</code>。",
      "<code>lmax < rmax</code>: <code>water += lmax - height[l]</code>, <code>l += 1</code>; 否则 <code>water += rmax - height[r]</code>, <code>r -= 1</code>。")
doc.svg(SLUG + "/trap_core.svg", "左边的表格是 O(n) 空间的版本; 双指针只保留 lmax 和 rmax 两个数。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/trap_trace.svg", "height = [2,0,1,3,0,1,2]: 先推进 r 三次, 再推进 l 三次, 每一步只确定一格的水。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(1)</code>。另有 monotonic stack 的做法 (见 07)。")
nc.solution(doc, CODE["trap"])
doc.note("每个位置的值由\"左边的某个最值\"和\"右边的某个最值\"决定: 先写出公式; 如果只需要比较两边的大小, 就用双指针代替两个数组。")

# ================================================================ 5
doc.h2("5. Move Zeroes")
doc.h3("题目在问什么")
doc.p("给一个数组, 把所有的 0 移到最后。非零的数要<b>保持原来的先后顺序</b>。必须在原数组上改, 不能新开数组。")
doc.h3("看例子")
doc.svg(SLUG + "/move_zeroes_examples.svg", "例子。")
doc.h3("Brute force")
doc.p("开一个新数组, 先放所有非零的数, 再补 0。<code>O(n)</code> 时间, 但用了 <code>O(n)</code> 空间, 题目不允许。")
doc.p("另一种: 每遇到一个 0, 就把后面的数全往前挪一格, 再把 0 放到最后。每次挪 <code>O(n)</code>, 共 <code>O(n²)</code>。浪费: 同一个数被挪了很多次。")
doc.h3("Intuition: 换一种双指针, 一个读一个写")
doc.p("这题的两个下标不再相向, 而是<b>同向</b>, 都从左边出发:")
nc.bullets(doc, "<code>r</code> 负责<b>读</b>: 每一步都往右走, 看每一个数。",
           "<code>w</code> 负责<b>写</b>: 指向下一个非零数应该放的位置。只有读到非零数时才往右走。")
doc.p("读到非零数, 就和 w 位置交换, 然后 w 加 1。因为 w 永远 ≤ r, 写的位置总是在已经读过的区域里, 不会盖掉还没读的数。")
doc.p("任何时候数组都分成三段: <code>[0, w)</code> 是已经排好的非零数, <code>[w, r)</code> 全是 0, <code>[r, n)</code> 还没读。")
doc.h3("算法")
steps("<code>w = 0</code>。",
      "r 从 0 走到 n - 1。如果 <code>nums[r] != 0</code>: 交换 <code>nums[w]</code> 和 <code>nums[r]</code>, <code>w += 1</code>。")
doc.svg(SLUG + "/move_zeroes_core.svg", "三段: [0, w) 是非零数, [w, r) 全是 0, [r, n) 还没读。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/move_zeroes_trace.svg", "[0,1,0,3,12]: 5 步, 遇到 1、3、12 时各交换一次。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(1)</code>。")
nc.solution(doc, CODE["move_zeroes"])
doc.note("原地删除 / 过滤, 还要保持顺序: r 读, w 写。nums[:w] 永远是已读部分的答案。")

# ================================================================ 6
doc.h2("6. Remove Duplicates from Sorted Array")
doc.h3("题目在问什么")
doc.p("给一个<b>排好序</b>的数组, 原地删除重复的数, 每个值只留一个。返回留下了几个 (记为 k)。数组的前 k 格必须是结果, 后面是什么都可以。")
doc.h3("看例子")
doc.svg(SLUG + "/remove_dup_examples.svg", "例子。")
doc.h3("Brute force")
doc.p("用 set 去重再写回去, 但要 <code>O(n)</code> 空间。或者每遇到重复就 <code>list.pop</code> 删掉, 每次删 <code>O(n)</code>, 共 <code>O(n²)</code>。")
doc.h3("Intuition: 和第 5 题一样, 只换\"留不留\"的条件")
doc.p("还是 r 读 w 写。第 5 题\"留下\"的条件是 <code>!= 0</code>, 这题是<b>和上一个留下的数不同</b>。")
doc.p("因为数组排好序, 相同的数一定挨在一起。所以只需要和最后一个留下的数 <code>nums[w-1]</code> 比较: 不同就写, 相同就跳过。被跳过的数不需要保留, 所以直接覆盖, 不用交换。")
doc.h3("算法")
steps("<code>w = 1</code> (第一个数一定留下)。",
      "r 从 1 走到 n - 1。如果 <code>nums[r] != nums[w-1]</code>: <code>nums[w] = nums[r]</code>, <code>w += 1</code>。",
      "返回 w。")
doc.svg(SLUG + "/remove_dup_core.svg", "r 读到的数和 nums[w-1] 比: 不同才写。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/remove_dup_trace.svg", "[0,0,1,1,2,2,3]: 6 步, 写入 1、2、3 三次, 其余三次跳过。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, Space <code>O(1)</code>。")
doc.p("变体 Remove Duplicates II (每个值最多留 2 个): 只改一处, 和 <code>nums[w-2]</code> 比。")
nc.solution(doc, CODE["remove_dup"], CODE["remove_dup_k"])
doc.note("同向双指针的题, 区别只在\"留下\"的条件: != 0、和 nums[w-1] 不同、和 nums[w-k] 不同。")

# ================================================================ 7
doc.h2("7. Sort Colors")
doc.h3("题目在问什么")
doc.p("数组里只有 0、1、2 三种数。原地把它排成所有 0 在前、1 在中间、2 在最后。不能用内置的 sort, 最好只扫一遍。")
doc.h3("看例子")
doc.svg(SLUG + "/sort_colors_examples.svg", "例子。")
doc.h3("Brute force")
doc.p("直接排序是 <code>O(n log n)</code>。或者数一下 0、1、2 各有几个, 再按个数写回去, <code>O(n)</code> 但要扫两遍。")
doc.h3("Intuition: 三个下标, 切出四个区")
doc.p("第 5 题是把数组分成两类 (非零 / 零)。这题是三类, 那就用三个下标当分界线:")
nc.bullets(doc, "<code>[0, lo)</code>: 已经确定是 0",
           "<code>[lo, i)</code>: 已经确定是 1",
           "<code>[i, hi]</code>: 还没看过",
           "<code>(hi, n)</code>: 已经确定是 2")
doc.p("i 是当前在看的数。看到 0, 就把它换到 lo 的位置, lo 和 i 都前进; 看到 1, 它本来就该在中间, i 前进; 看到 2, 把它换到 hi 的位置, hi 后退。")
doc.p("一个细节: 看到 2 换完之后, <b>i 不前进</b>。因为从 hi 换过来的数还没看过, 下一步要检查它。看到 0 换完 i 可以前进, 因为从 lo 换过来的一定是 1 (已经看过)。")
doc.h3("算法")
steps("<code>lo = 0</code>, <code>i = 0</code>, <code>hi = n - 1</code>。",
      "当 <code>i ≤ hi</code>: 是 0, 交换 nums[lo] 和 nums[i], lo 和 i 都加 1; 是 1, i 加 1; 是 2, 交换 nums[i] 和 nums[hi], hi 减 1 (i 不动)。")
doc.svg(SLUG + "/sort_colors_core.svg", "四个区的含义, 以及三种情况下 i 为什么前进、为什么不前进。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/sort_colors_trace.svg", "[2,0,2,1,1,0]: 第 1 步把 2 换到右边, i 不动; 之后两个 0 换到左边, 又一个 2 换到右边, 两个 1 直接跳过。")
doc.h3("复杂度")
doc.p("Time <code>O(n)</code>, 一遍。Space <code>O(1)</code>。这个分区的思路也是 quick sort 里 partition 的基础。")
nc.solution(doc, CODE["sort_colors"])
doc.note("值只有 2~3 种, 要原地分类: 用几个下标当分界线。交换之后 i 要不要前进, 看换过来的数有没有看过。")

# ================================================================ 8
doc.h2("8. Merge Sorted Array")
doc.h3("题目在问什么")
doc.p("两个排好序的数组。<code>nums1</code> 长度是 m + n, 前 m 个是有效的数, 后 n 格是空位; <code>nums2</code> 有 n 个数。把 nums2 合并进 nums1, 结果要有序, 直接写在 nums1 里。")
doc.h3("看例子")
doc.svg(SLUG + "/merge_examples.svg", "例子。")
doc.h3("Brute force")
doc.p("把 nums2 复制到 nums1 后面的空位, 再整个排序。<code>O((m+n) log(m+n))</code>。浪费: 两个数组本来就各自有序, 却当成乱序来排。")
doc.h3("Intuition: 从后往前合并")
doc.p("合并两个有序数组的标准做法是: 两个数组各放一个下标, 每次取小的那个放进结果, 取走的那边下标前进。<code>O(m+n)</code>。")
doc.p("但这里结果要写在 nums1 里。如果从前往后写, 会把 nums1 里还没读的数盖掉。")
doc.p("解决办法是<b>从后往前</b>: 每次取两个数组末尾<b>较大</b>的那个, 写到 nums1 的最后。nums1 的最后是空位, 写在那里永远不会盖掉没读的数。")
doc.h3("算法")
steps("<code>i = m - 1</code> (nums1 有效部分的末尾), <code>j = n - 1</code> (nums2 的末尾), <code>k = m + n - 1</code> (写的位置)。",
      "当 <code>j ≥ 0</code>: 如果 <code>i ≥ 0</code> 且 <code>nums1[i] > nums2[j]</code>, 写 nums1[i], i 减 1; 否则写 nums2[j], j 减 1。每写一次 k 减 1。",
      "nums2 用完就结束。nums1 剩下的数本来就在正确的位置。")
doc.svg(SLUG + "/merge_core.svg", "写的位置 k 永远 ≥ i, 从后往前写不会盖掉还没读的数。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/merge_trace.svg", "4 步: 6 和 5 来自 nums2, 3 来自 nums1, 最后 2 来自 nums2。")
doc.h3("复杂度")
doc.p("Time <code>O(m + n)</code>, Space <code>O(1)</code>。")
nc.solution(doc, CODE["merge"])
doc.note("两个有序数组合并, 其中一个后面有空位: 从后往前, 每次取大的。写的方向要保证不会盖掉没读的数。")

# ================================================================ 9
doc.h2("9. Valid Palindrome I / II")
doc.h3("题目在问什么")
doc.p("<b>I</b>: 给一个字符串, 只看字母和数字, 忽略大小写, 判断它正着读和反着读是不是一样 (palindrome, 回文)。")
doc.p("<b>II</b>: 给一个只有小写字母的字符串, <b>最多删掉一个字符</b>, 能不能变成回文。")
doc.h3("看例子")
doc.svg(SLUG + "/valid_palindrome_examples.svg", "例子。")
doc.h3("Brute force")
doc.p("I: 先把字符串过滤成只有小写字母和数字的新串 t, 再比较 <code>t == t[::-1]</code>。<code>O(n)</code> 时间, 但开了新字符串, <code>O(n)</code> 空间。")
doc.p("II: 每个位置都试着删一次, 再检查是不是回文。n 个位置, 每次检查 <code>O(n)</code>, 共 <code>O(n²)</code>。")
doc.h3("Intuition")
doc.p("I: 回文就是左右对称。用两个下标从两头往中间走, 遇到不是字母数字的就跳过, 比较 <code>s[l]</code> 和 <code>s[r]</code> (转小写)。不用开新字符串。")
doc.p("II: 还是从两头往中间比。前面都相等时照常走。<b>第一次不相等时</b>, 只有两种可能的删法: 删 <code>s[l]</code>, 或者删 <code>s[r]</code>。"
      "删别的位置没用, 因为这一对还是不相等。所以分别检查 <code>s[l+1..r]</code> 和 <code>s[l..r-1]</code> 是不是回文, 有一个是就行。")
doc.p("只会分叉一次 (只能删一个), 所以不会指数爆炸。")
doc.h3("算法")
steps("I: <code>l = 0</code>, <code>r = n - 1</code>。l 跳过非字母数字, r 也跳过。比较小写后的 s[l] 和 s[r], 不同就返回 False, 相同就 l 加 1、r 减 1。",
      "II: 同样两头往中间比。第一次失配时, 返回 <code>是回文(l+1, r) or 是回文(l, r-1)</code>。")
doc.svg(SLUG + "/valid_palindrome_core.svg", "I: 两头往中间一对一对比; II: 第一次失配只有两种删法。")
doc.h3("手动走一遍")
doc.svg(SLUG + "/valid_palindrome_trace.svg", "I, \"A,bxB;a\": 5 步, 2 次配对, 2 次跳过标点, l 追上 r。")
doc.svg(SLUG + "/valid_palindrome_ii_trace.svg", "II, \"cbbcc\": 在 (1, 3) 失配; 删 s[l] 不行, 删 s[r] 可以。")
doc.h3("复杂度")
doc.p("都是 Time <code>O(n)</code>, Space <code>O(1)</code>。")
nc.solution(doc, CODE["palin"], CODE["palin2"])
doc.note("回文 / 对称: 两头往中间走。允许失配一次: 失配时两种删法都试一下。")

# ================================================================ 识别信号
doc.h2("10. 识别信号: 看到什么, 就想到 Two Pointers")
nc.table(doc, ["题目特征", "做法", "complexity"], [
    ["排好序的数组, 找 pair / 和满足条件", "相向: 太小移左边, 太大移右边", "<code>O(n²)</code> → <code>O(n)</code>"],
    ["k 个数的和 (3Sum, 4Sum)", "排序, 固定 k - 2 个, 最里层相向; 同一层跳过同值", "<code>O(n^k)</code> → <code>O(n^(k-1))</code>"],
    ["最大化 f(l, r), 往里收时宽度变小", "从最宽开始, 丢掉限制结果的那一边", "<code>O(n²)</code> → <code>O(n)</code>"],
    ["每个位置由左边最值和右边最值决定", "先写公式, 两个数组 → 双指针两个变量", "空间 <code>O(n)</code> → <code>O(1)</code>"],
    ["原地删除 / 过滤 / 去重, 保持顺序", "同向: r 读, w 写", "<code>O(n²)</code> 或 <code>O(n)</code> 空间 → <code>O(n)</code> 时间 <code>O(1)</code> 空间"],
    ["值只有 2~3 种, 原地分类", "几个下标切分区 (lo, i, hi)", "<code>O(n log n)</code> → <code>O(n)</code>"],
    ["两个有序数组合并, 一个有空位", "各一个下标, 从后往前", "<code>O((m+n) log(m+n))</code> → <code>O(m+n)</code>"],
    ["回文 / 对称", "两头往中间", "空间 <code>O(n)</code> → <code>O(1)</code>"]])
doc.p("先问两件事: 数组排好序了吗 (或者能不能先排序)? 要不要原地改、保持顺序? 这两个答案基本决定了用哪一种双指针。")

doc.h2("以后再学")
doc.p("Sliding Window (同向双指针的一种, 见 03); linked list 的 fast / slow 指针 (见 08); Next Permutation (单题技巧)。")
doc.write("docs/02-two-pointers.html")
