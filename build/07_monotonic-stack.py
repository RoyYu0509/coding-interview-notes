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
    exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '07_monotonic_stack_doc.py'), encoding='utf-8').read())
