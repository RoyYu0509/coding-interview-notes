"""07 · Monotonic Stack / Queue
生成: cd build && python3 -I 07_monotonic-stack.py
SVG 在 docs/svg/07-monotonic-stack/ (每张都是跑过代码后按打印结果画的)。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import doclib as d  # noqa: E402

# ------------------------------------------------------------------ code
S_BRUTE = '''
def next_greater_brute(nums):             # O(n^2)
    n = len(nums)
    ans = [-1] * n
    for i in range(n):
        for j in range(i + 1, n):         # 每个 i 都从 i+1 重新往右扫
            if nums[j] > nums[i]:
                ans[i] = nums[j]
                break
    return ans
'''

S_TEMPLATE = '''
def next_greater(nums):                   # O(n)
    ans = [-1] * len(nums)
    stack = []                            # 存 index; 对应的值从底到顶递减
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:   # x 比栈顶大: x 就是栈顶的 next greater
            ans[stack.pop()] = x          # pop 的这一刻结算; 弹出的元素以后再也用不到
        stack.append(i)                   # 栈里全是 "还没等到更大数" 的元素
    return ans
'''

S_BOTH = '''
def nearest_smaller_both(nums):           # 递增栈: 一次循环同时得到左右两个边界
    n = len(nums)
    left, right = [-1] * n, [n] * n       # -1 / n 表示那一侧没有更小的
    stack = []
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] > x:
            right[stack.pop()] = i        # 被 x pop: x 是它右边第一个更小的
        left[i] = stack[-1] if stack else -1   # pop 完剩下的栈顶 = i 左边第一个 <= x 的
        stack.append(i)
    return left, right
'''

S_DT = '''
def daily_temperatures(T):
    ans = [0] * len(T)
    stack = []                            # 存 index (不存温度): 答案是 i - j, 需要位置
    for i, t in enumerate(T):
        while stack and T[stack[-1]] < t: # t 是栈顶那天等到的第一个更高温
            j = stack.pop()
            ans[j] = i - j                # 在 pop 时结算 j 的答案
        stack.append(i)
    return ans                            # 栈里剩下的天没等到更高温, ans 保持 0
'''

S_NGE2 = '''
def next_greater_elements(nums):
    n = len(nums)
    ans = [-1] * n
    stack = []
    for i in range(2 * n):                # 走 2 圈: 第 2 圈让右边没有的元素绕回去找
        x = nums[i % n]                   # 用 i % n 取值, 不拷贝数组
        while stack and nums[stack[-1]] < x:
            ans[stack.pop()] = x
        if i < n:                         # 只在第 1 圈 push: 第 2 圈只负责结算
            stack.append(i)
    return ans
'''

S_LRH = '''
def largest_rectangle_area(heights):
    heights = heights + [0]               # 哨兵 0: 最后一步把栈里剩下的柱子全部 pop 出来
    stack = []                            # 存 index; heights 从底到顶递增
    best = 0
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:   # h 比栈顶矮 -> 栈顶的右边界就是 i
            height = heights[stack.pop()]
            left = stack[-1] if stack else -1     # pop 后的新栈顶 = 左边界 (空: -1)
            width = i - left - 1          # 左右边界之间 (不含边界) 的柱子数
            best = max(best, height * width)
        stack.append(i)                   # 相等的柱子不 pop: 后面那根会把宽度补全
    return best
'''

S_MAXRECT = '''
def maximal_rectangle(matrix):            # 逐行套用 largest_rectangle_area
    if not matrix:
        return 0
    heights = [0] * len(matrix[0])
    best = 0
    for row in matrix:
        for j, c in enumerate(row):
            heights[j] = heights[j] + 1 if c == "1" else 0   # 这一列往上连续 1 的个数
        best = max(best, largest_rectangle_area(heights))    # 这一行就是一个直方图
    return best
'''

S_RKD = '''
def remove_k_digits(num, k):
    stack = []                            # 栈就是答案本身 (数字字符), 从底到顶非递减
    for dig in num:
        while k and stack and stack[-1] > dig:   # 前一位比当前大: 删前一位, 高位变小
            stack.pop()
            k -= 1                        # pop 一次 = 花掉 1 个删除名额
        stack.append(dig)
    if k:                                 # 整串都是递增: 名额没花完, 删最末尾的 k 位
        stack = stack[:-k]
    return "".join(stack).lstrip("0") or "0"   # 去前导零; 全删光时返回 "0"
'''

S_SWM = '''
from collections import deque

def max_sliding_window(nums, k):
    dq = deque()                          # 存 index; 值从头到尾递减, dq[0] = 窗口最大
    ans = []
    for i, x in enumerate(nums):
        if dq and dq[0] <= i - k:         # 队头已滑出窗口 [i-k+1, i]: 过期, 从头部出队
            dq.popleft()
        while dq and nums[dq[-1]] <= x:   # 队尾比 x 小: 比 x 早过期又更小, 永远当不了最大
            dq.pop()
        dq.append(i)
        if i >= k - 1:                    # 窗口满了才有答案
            ans.append(nums[dq[0]])       # 队头 = 窗口最大, O(1)
    return ans
'''

SNIPPETS = [S_BRUTE, S_TEMPLATE, S_BOTH, S_DT, S_NGE2, S_LRH, S_MAXRECT, S_RKD, S_SWM]

if __name__ == "__main__":
    SV = "07-monotonic-stack/"
    doc = d.Doc("07 · Monotonic Stack / Queue")
    doc.main("主线: 扫一遍数组, 同时维护一个 <b>单调</b> 的容器 (stack 或 deque)。"
             "新元素一到, 就把 \"从此没用\" 的元素弹掉 —— <b>弹出的那一刻, 就是它的答案 / 边界出现的那一刻</b>。"
             "每个元素最多进出一次, 把 O(n²) 的反复往右扫降成 O(n)。")
    doc.main("概念链: Next Greater (模板) → Daily Temperatures (存 index, pop 时结算) → "
             "Next Greater Element II (循环数组, 走 2n) → Largest Rectangle in Histogram (pop 时左右边界同时确定, 哨兵 0) → "
             "Remove K Digits (greedy: 栈就是答案) → Sliding Window Maximum (两头都能 pop 的 deque)")

    # ============================================================ 0
    doc.h2("0. 第一性原理: 暴力在反复扫什么, stack 怎么消掉")
    doc.p("<b>题目:</b> 数组里每个数, 找它右边第一个比它大的数, 没有就是 −1。例子: "
          "<code>[9, 8, 7, 6, 5, 10]</code> → <code>[10, 10, 10, 10, 10, −1]</code>。")
    doc.p("<b>Brute force:</b> 每个 i 都从 i+1 往右扫, 直到遇到更大的。最坏 O(n²)。")
    doc.code(S_BRUTE)
    doc.p("<b>浪费在哪:</b> 看图左边。8, 7, 6, 5 被 i = 0, 1, 2, 3 各扫了一遍, 但它们其实都在等同一个 10。"
          "暴力每个 i 都从头扫, <b>没有记住 \"谁还在等答案\"</b>。")
    doc.p("<b>怎么消掉:</b> 扫的时候只保留 \"还没等到更大数\" 的元素, 放进 stack。"
          "它们一定是 <b>从底到顶递减</b> 的 (如果某个元素比它下面的大, 下面的早就被它结算了)。"
          "所以新来的 x 只要和栈顶比: 栈顶更小就 pop 并结算, 直到栈顶 ≥ x 为止, 再往下全 ≥ 栈顶, 不用看。")
    doc.p("<b>为什么 pop 掉的元素以后再也用不到:</b> 它已经拿到答案; 栈里还在等的元素都 ≥ 它, 不会拿它当答案; "
          "它右边的新元素只往右找, 它在左边, 看不到。所以每个元素 push 1 次、最多 pop 1 次, 总共 ≤ 2n 次操作, "
          "是 amortized O(n) (一次 pop 好几个没关系, 总数还是 ≤ n)。")
    doc.svg(SV + "first_principles_core.svg", "左: 暴力每个 i 重新扫 (15 次比较)。右: 10 一来, 栈里 5 个等答案的数一次性结算, 每个数只进出一次。")
    doc.p("通用模板 (找右边第一个更大 → 递减栈):")
    doc.code(S_TEMPLATE)
    doc.h3("口诀: 递增栈还是递减栈")
    doc.raw('<table><tr><th>要找</th><th>栈 (底 → 顶)</th><th>while 条件 (pop)</th><th>答案什么时候出现</th></tr>'
            '<tr><td>右边第一个 <b>更大</b></td><td>递减</td><td><code>nums[stack[-1]] &lt; x</code></td><td>pop 时: 答案 = x</td></tr>'
            '<tr><td>右边第一个 <b>更小</b></td><td>递增</td><td><code>nums[stack[-1]] &gt; x</code></td><td>pop 时: 答案 = x</td></tr>'
            '<tr><td>左边第一个 更大</td><td>递减</td><td>同右边更大</td><td>pop 完, push 前: 看栈顶</td></tr>'
            '<tr><td>左边第一个 更小</td><td>递增</td><td>同右边更小</td><td>pop 完, push 前: 看栈顶</td></tr></table>')
    doc.p("口诀: <b>找更大 → 栈递减</b> (小的在栈里等大的来); <b>找更小 → 栈递增</b>。"
          "while 条件永远是 \"来了个比栈顶更 '强' 的, 栈顶出去\"。右边的答案在 pop 时拿到, 左边的答案在 pop 完后看栈顶。")
    doc.p("同一个循环可以同时拿到左右两个边界 (后面 Largest Rectangle 就靠这个):")
    doc.code(S_BOTH)
    doc.p("相等怎么办: 条件用 <code>&lt;</code> 还是 <code>&lt;=</code>, 取决于题目要 \"严格更大\" 还是 \"大于等于\"。"
          "面试里先问清楚, 再决定把哪边的等号放进 while。")
    doc.note("单调栈 = 记住 \"谁还在等答案\"。新元素和栈顶比, 能 pop 就结算; 每个元素最多进出一次, O(n)。找更大用递减栈, 找更小用递增栈。")

    # ============================================================ 1
    doc.h2("1. Daily Temperatures: 存 index, 在 pop 时结算答案")
    doc.p("<b>题目:</b> 给每日温度 T, 对每一天算出还要等几天才有更高的温度, 没有则 0。"
          "例子: <code>T = [73, 74, 75, 71, 69, 72, 76, 73]</code> → <code>[1, 1, 4, 2, 1, 1, 0, 0]</code>。")
    doc.p("<b>Brute force:</b> 每天往右扫到第一个更高温, O(n²)。浪费: 和第 0 节一样, 71 和 69 都在等 72, 却各自扫了一遍。")
    doc.p("<b>关键观察:</b> 这就是模板, 只改一点: 答案是 <b>距离</b> i − j, 不是值, 所以栈里存 <b>index</b>, 比较时回 T 里取温度。")
    doc.svg(SV + "daily_temperatures_core.svg", "i = 5 (T = 72) 到来: 栈里 69、71 都比 72 冷 → pop 并结算; 75 不比 72 冷 → 停。")
    doc.svg(SV + "daily_temperatures_trace.svg", "8 天的完整运行。注意 i = 5 一次 pop 两个、i = 6 一次 pop 两个; 每一次 pop 都对应一个 ans 的确定。")
    doc.code(S_DT)
    doc.p("<b>Time:</b> O(n)。每个 index push 1 次, 最多 pop 1 次, while 循环总共执行 ≤ n 次。"
          "<b>Space:</b> O(n), 最坏是温度严格递减 (<code>[5, 4, 3, 2, 1]</code>), 全部留在栈里。")
    doc.p("变体: Next Greater Element I (nums1 是 nums2 的子集) 就是模板 + 一个 dict 记 \"值 → 它的 next greater\"。"
          "Final Prices With a Special Discount 是 \"右边第一个 ≤ 自己\" → 换成递增栈。")
    doc.note("存 index; while 栈顶 < 当前: pop, 并在这一刻写 ans[j] = i − j。")

    # ============================================================ 2
    doc.h2("2. Next Greater Element II: 循环数组, 遍历 2n")
    doc.p("<b>题目:</b> 数组首尾相连 (循环), 对每个元素找它 \"往右走\" 遇到的第一个更大的数, 可以绕回开头。"
          "例子: <code>[2, 3, 1]</code> → <code>[3, −1, 2]</code> (最后的 1 绕回去遇到 2)。")
    doc.p("<b>相比上一题:</b> 多了 \"绕回\"。Brute force 是每个元素往右扫最多 n−1 个 (取模), O(n²)。")
    doc.p("<b>关键观察:</b> 把数组虚拟地拼成两份, 取值用 <code>i % n</code>, 就能看到每个元素 \"右边\" 的全部 n−1 个元素。"
          "改两行: <code>range(2 * n)</code> 和只在 <code>i &lt; n</code> 时 push。")
    doc.svg(SV + "next_greater_ii_core.svg", "拼成两份后, idx 2 (值 1) 在第 2 圈遇到 2; idx 1 (值 3) 绕一圈都没有更大的。")
    doc.svg(SV + "next_greater_ii_trace.svg", "6 步 (2n)。第 2 圈 (i = 3, 4, 5) 不 push, 只结算: i = 3 把 1 pop 掉并得到 ans[2] = 2。")
    doc.code(S_NGE2)
    doc.p("<b>Time:</b> O(n), 循环 2n 次, 每个元素仍然最多 push 1 次 / pop 1 次。<b>Space:</b> O(n)。")
    doc.note("循环数组 = 遍历 2n, 用 i % n 取值; 只在第 1 圈 push, 第 2 圈只结算。")

    # ============================================================ 3
    doc.h2("3. Largest Rectangle in Histogram: pop 时左右边界同时确定")
    doc.p("<b>题目:</b> 一排宽为 1 的柱子 heights, 求柱状图里最大的矩形面积。"
          "例子: <code>[2, 1, 5, 6, 2, 3]</code> → <code>10</code> (高 5, 宽 2)。")
    doc.p("<b>Brute force:</b> 对每根柱子, 向左右各扩展到第一根比它矮的, 面积 = 高 × 宽, O(n²)。"
          "浪费: 每根柱子都从自己出发重新向两边走, 不知道别人已经走过哪一段。")
    doc.p("<b>相比上一题:</b> 不再是 \"给每个元素找一个答案\", 而是 <b>每根柱子要左右两个边界</b>, 即 \"以它为最矮的柱子, 能延伸多远\"。"
          "这正是第 0 节那个 <code>nearest_smaller_both</code>: 用递增栈, 当柱子被 pop 的那一刻, "
          "右边界 = 当前 i (第一根比它矮的, 才触发 pop), 左边界 = pop 后的新栈顶 (栈递增, 它下面那根就是左边第一根更矮的)。"
          "两个边界同时确定, 当场算面积。")
    doc.svg(SV + "largest_rectangle_core.svg", "高 5 的柱子在 i = 4 被 pop: 右边界 = 4, 左边界 = 新栈顶 idx 1, 宽 = 4 − 1 − 1 = 2, 面积 10。")
    doc.svg(SV + "largest_rectangle_trace.svg", "heights + [0] 共 7 步。每个 pop 都写出 w 和面积, 最后一行哨兵 0 把栈清空。")
    doc.code(S_LRH)
    doc.p("<b>哨兵 0 的作用:</b> 末尾补一根高 0 的柱子, 它比所有柱子都矮, 所以一定把栈里剩下的柱子全部 pop 出来结算, "
          "不用在循环后面再写一段清栈代码。")
    doc.p("<b>Time:</b> O(n)。<b>Space:</b> O(n), 最坏是柱子严格递增, 全留在栈里。")
    doc.p("<b>Maximal Rectangle</b> 是逐行套用: 矩阵每一行, 把每一列 \"到这一行为止往上连续 1 的个数\" 当成柱子高度, "
          "这一行就是一个直方图, 直接调用上面的函数。")
    doc.code(S_MAXRECT)
    doc.p("Time O(rows × cols): 每行更新 heights 是 O(cols), 再 O(cols) 的单调栈。"
          "同一套 \"左右边界\" 换成数个数, 就是 Sum of Subarray Minimums (每个数作为最小值贡献 (i − left) × (right − i) 次)。")
    doc.note("以每个元素为最值能延伸多远 = 左右边界 = 单调栈。pop 时右边界是 i, 左边界是新栈顶。末尾补哨兵 0 清栈。")

    # ============================================================ 4
    doc.h2("4. Remove K Digits: greedy + 递增栈, 栈就是答案")
    doc.p("<b>题目:</b> 数字字符串 num, 删掉恰好 k 位, 使剩下的数最小。例子: <code>num = \"1432219\", k = 3</code> → <code>\"1219\"</code>。")
    doc.p("<b>Brute force:</b> 枚举删哪 k 位, C(n, k) 种, 指数级。稍好一点的 greedy: 每次从头扫找第一个 \"比后一位大\" 的数字删掉, 重复 k 次, O(nk)。")
    doc.p("<b>浪费在哪:</b> 每删一次, 又要从头扫一遍。其实删掉一位后, 只可能让 \"紧挨着它左边\" 的那一位变成新的 \"比后一位大\", 前面不会再有。"
          "这正是栈: 每次只看栈顶。")
    doc.p("<b>相比上一题:</b> 栈里存的不再是 \"等答案的元素\", 而是 <b>最终结果本身</b>; pop 也不是结算, 而是 <b>真的删掉</b>, "
          "且受 k 个名额限制 (<code>while k and ...</code>)。")
    doc.svg(SV + "remove_k_digits_core.svg", "位数相同, 先比高位。\"1432\" 删 4 得 132 最小: 从左往右第一个比后一位大的数字 (4 &gt; 3) 删掉最划算。")
    doc.svg(SV + "remove_k_digits_trace.svg", "7 个数字。d = 3, 2, 1 各 pop 一个比它大的前一位 (共 3 次, k: 3 → 0); 之后 d = 9 直接 push。")
    doc.code(S_RKD)
    doc.p("两个收尾: ① 名额没用完 (整串递增, 如 <code>\"12345\"</code>, k = 2) → 删末尾 k 位; "
          "② 前导零要去掉, 全删光返回 <code>\"0\"</code>。")
    doc.p("<b>Time:</b> O(n), 每个数字 push 1 次 / pop 1 次。<b>Space:</b> O(n)。"
          "同一思路: Remove Duplicate Letters (再加一个 \"这个字母后面还会不会出现\" 的判断), 不展开。")
    doc.note("要在保持顺序的前提下删/选若干元素使结果字典序最小: 栈顶比当前 \"差\" 就 pop (有预算限制), 栈就是答案。")

    # ============================================================ 5
    doc.h2("5. Sliding Window Maximum: 窗口会过期, 用 deque 两头 pop")
    doc.p("<b>题目:</b> 长度 k 的窗口从左滑到右, 输出每个窗口的最大值。"
          "例子: <code>nums = [1, 3, −1, −3, 5, 3, 6, 7], k = 3</code> → <code>[3, 3, 5, 5, 6, 7]</code>。")
    doc.p("<b>Brute force:</b> 每个窗口 <code>max(nums[i-k+1:i+1])</code>, O(nk)。"
          "浪费: 相邻两个窗口有 k − 1 个元素相同, 却每次重新找最大。(另一个做法: heap, O(n log n), 要惰性删除过期元素。)")
    doc.p("<b>相比上一题:</b> 单调栈只在一头 (栈顶) 进出。这里元素会 <b>过期</b> (滑出窗口), 过期的是最老的, 在另一头, "
          "所以改用 deque: <b>队尾</b> 和新元素比 (比 x 小的出队), <b>队头</b> 检查过期 (滑出窗口的出队)。"
          "队列里保持 index 递增、值递减, 所以队头永远是窗口最大。")
    doc.svg(SV + "sliding_window_max_core.svg", "i = 4, x = 5 到来: idx 1 滑出窗口 (队头过期); −1、−3 又小又早过期 (队尾被压住), 都不可能再是最大。")
    doc.svg(SV + "sliding_window_max_trace.svg", "8 步, k = 3。i = 4 一次出队 3 个 (队头过期 1 个 + 队尾 2 个); i = 2..7 每步输出 nums[队头]。")
    doc.code(S_SWM)
    doc.p("<b>Time:</b> O(n)。每个 index 进 deque 1 次、出 1 次 (头或尾)。<b>Space:</b> O(k), deque 里最多 k 个。")
    doc.note("窗口最大/最小 = 单调 deque。队头过期出队, 队尾比新元素差的出队, 队头 = 答案。")

    # ============================================================ 6
    doc.h2("6. 识别信号: 看到什么 → 试什么")
    doc.raw('<table><tr><th>题目特征</th><th>做法</th><th>complexity</th></tr>'
            '<tr><td>每个元素找右 / 左边 <b>第一个更大 / 更小</b> 的数或距离</td><td>单调栈, 存 index, pop 时结算</td><td>O(n²) → O(n)</td></tr>'
            '<tr><td>数组 <b>循环</b> (首尾相连)</td><td>遍历 2n, <code>i % n</code>, 只在第 1 圈 push</td><td>O(n²) → O(n)</td></tr>'
            '<tr><td>以每个元素为 <b>最大 / 最小值</b> 能延伸多远 (矩形面积、子数组最小值之和)</td><td>单调栈, pop 时右边界 = i, 左边界 = 新栈顶</td><td>O(n²) → O(n)</td></tr>'
            '<tr><td>二维 0/1 矩阵里找最大矩形</td><td>逐行压成直方图, 套 Largest Rectangle</td><td>O(rows²·cols²) 以上 → O(rows·cols)</td></tr>'
            '<tr><td>删 / 选 k 个元素, 使结果 <b>字典序或数值最小</b> (顺序不变)</td><td>greedy + 单调栈, 栈就是答案, pop 受预算 k 限制</td><td>O(nk) 或指数 → O(n)</td></tr>'
            '<tr><td>固定长度滑动窗口求 <b>max / min</b></td><td>单调 deque: 队头过期出队, 队尾 ≤ x 出队</td><td>O(nk) → O(n)</td></tr>'
            '<tr><td>\"后面有更大的才轮到我\" / \"被后来者盖住就没用\"</td><td>先想: 谁还在等? 谁被 pop 就永远没用?</td><td>反复往右扫 → 每个元素进出 1 次</td></tr></table>')
    doc.p("选栈的方向: <b>找更大 → 递减栈; 找更小 → 递增栈</b>。右边的答案在 pop 时拿, 左边的答案在 pop 完后看栈顶。"
          "窗口会过期 (两头都要出) → 换成 deque。")
    doc.p("<b>以后再学 (一行):</b> Car Fleet (按位置排序后从后往前, 栈里存 \"到达时间\")、132 Pattern、Max Chunks To Make Sorted "
          "都是同一套 pop 逻辑的变形, 先把上面六题吃透。")
    doc.write("docs/07-monotonic-stack.html")
