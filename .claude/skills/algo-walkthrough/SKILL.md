---
name: algo-walkthrough
description: 把算法题 / 一个算法 pattern 写成 NeetCode 式的讲解 (单文件 HTML + 静态 SVG): 先讲清题意和例子, 再从 brute force 的浪费推出 intuition, 再用文字步骤讲算法, 用逐步 trace 图手把手走一遍, 代码放最后折叠。用户说「讲一下这道题」「帮我理解 X 算法」「写算法 learning doc」「准备 coding interview」「画图解释这题」时使用。
---

# Algo Walkthrough: 讲算法题的方式

读者在准备 coding interview。目标不是背代码，而是：**理解题意 → 从 brute force 自己推出 pattern → 看到某个题目特征，能本能地想到该用哪个算法或数据结构，以及它把哪部分 complexity 降下来。** 代码是最不重要的。读者理解了 intuition,自己就能写出来。

## 讲解顺序(每道题固定，不能跳)

用 H3 小标题，按下面的顺序写:

1. **题目在问什么**:用白话复述题意。把容易误解的点讲清楚，比如 substring 和 subsequence 的区别、"顺序算不算不同"、闭区间还是半开区间。
2. **看例子**:配一张例子图，放 2–3 个例子。绿色是答案。红色虚线括号标出"看起来像、但不对"的部分，并写明原因，例如 `"pwke" 不连续`、`同一个位置不能用两次`。图下面用一两句话说出从例子里能看出什么。
3. **Brute force**:先用文字说明最直接的做法，写出它的 complexity,再指出**它浪费在哪里**:哪些工作被重复做了，或者哪些信息被丢掉了。基础题要配一张 brute force 图，把重复劳动标出来。
4. **Intuition**:从上面那份浪费出发，用编号步骤一步步推出优化方法。如果需要换一种问法，要讲出来，例如"问'等于 target 吗'没法二分，换成'≥ target 吗'就可以"。如果这道题用 greedy,还要用一句话说明为什么这样选不会吃亏。
5. **算法**:用文字写成编号步骤，再配一张 core 图。core 图只回答一个问题：这一步为什么是对的，或者 invariant 是什么。
6. **手动走一遍**:配 trace 图，用具体的小例子从头走到尾。图下面用一句话说明关键的那几步。
7. **复杂度**:写出 Time 和 Space,并说明它们分别从哪里来。
8. **参考代码**:放进 `<details>` 里，默认折叠。关键行加注释。
9. `记:` 一行，写读者可以直接抄进笔记的结论。

## 一篇文档的结构

```
H2 这篇讲什么      ← 用白话讲这一类题长什么样、pattern 名字的意思、它把什么 complexity 降到什么
                     放一张题目表: # / 题目 / 考过的公司数 / 相比上一题多了什么
H2 1. 第一道题     ← 最基础的模板题，完整地从零讲起
H2 把第 1 题抽象一下 ← 讲完第一题之后，再总结 pattern 什么时候能用，给出通用模板(折叠)
H2 2..N. 变体题    ← 每道都说明"和上一题相比改了什么"; brute force 可以写短，但题意和例子不能省
H2 识别信号        ← 表格: 题目特征 → 做法 → complexity 从 X 降到 Y
H2 以后再学        ← 一行带过偏门的特定技巧(KMP、Manacher、Morris……)
```

- 题目按 popularity 选，由浅到深排成一条链，每道比上一道只多一个变化。
- 只讲通用、可迁移的思路。最优解依赖偏门技巧的题，讲通用解法，偏门的部分只用一句话提到。

## SVG 规则(用户亲自迭代参考图得到的结论)

参考图:`reference_trace.svg`(heap 的 trace)。

- 只用静态 SVG,不要交互。
- **一行一步，列的顺序固定**:当前输入 → 操作 1 之后的状态 → 操作 2 之后的状态 → 计算。不要加任何会被误认为参与计算的列。
- **每次移除都要画出原因**:被 pop 的元素用虚线箭头扔到左边，离结构远一点，旁边用具体数字写原因，例如 `len = 4 > k = 3, pop 最大的 20`、`76 > 72, pop`。**触发移除的那个新元素也要画出来**:用绿色画在结构旁边，表示"等待进入",读者一眼就能看出为什么要 pop。
- 用读者熟悉的画法:heap 画成 tree,stack 画成竖直的桶，linked list 画成 node 加箭头(刚改过的 next 用绿色，刚断开的用红色虚线),interval 画成数轴上的横条，dp 画成表格(依赖的格子加橙色圈)。
- 画概念值，不画实现细节。比如 max-heap 里存的是 `-x`,图里仍然画 x。
- 不要做任何抽象：图、代码、正文里的变量名必须完全一致，计算要写出具体数字，例如 `total_q = 20 + 10 + 5 = 35`。
- 配色:新进来的 `#E1F5EE/#0F6E56`;被移除的 `#FAECE7/#993C1D`,虚线用 `#D85A30`;关键元素外面加一圈 `#EF9F27` ring;其他元素 `#F1EFE8/#5F5E5A`。底部放图例和最终答案。
- 图里每一个数字都必须来自代码的真实运行:写一个带记录的 sim 函数，用它的输出画图，再 assert 结果和题解函数一致。

## 工具(都在 `scripts/` 下)

- `doclib.py`:`Doc` 类，提供 h2 / h3 / p / code / svg / note / raw / write,输出单文件 HTML,CSS 内联，没有 JS。
- `nclib.py`:
  - `examples_svg(path, title, head, blocks)`:画数组或字符串的例子图。block 的字段有 `items`、`ans=[(l,r)]`、`hl`、`bad=[(l,r,reason)]`、`rows`(多行，比如 grid、两个数组)、`extra`。
  - `tree_examples_svg(...)`:画 tree 的例子，输入是 LeetCode level-order 列表。
  - `steps` / `bullets` / `table` / `solution(doc, *codes)`:分别生成编号步骤、列表、表格、折叠的代码块。代码块里太长的注释行会自动折行。
  - 长文字会按宽度自动换行。
- `render_check.js`:`node render_check.js doc.html [out.png]`,报告 code 块横向溢出，以及 SVG 文字超出 viewBox。

## 工作流程

1. 先写题解代码和 brute force,做随机对拍，确认代码是对的。
2. 写带记录的 sim 函数，生成 trace 图和 core 图。
3. 写例子图，例子里的输出先用 assert 验证。
4. 按上面的顺序写正文。
5. 检查:`render_check.js` 的结果要求 codeOverflow 为 0、textOutOfViewBox 为空。然后截图，亲眼看每一张新图：文字不重叠、箭头指对、每次 pop 都看得出原因。截图方法：用 playwright 的 `page.setContent` 把 svg 包进 680px 宽的 body 再截。直接打开 .svg 截 fullPage 会卡住。

## 写作风格

- 中文，短句。技术术语保留英文，不翻译，例如 pointer、heap、invariant、subarray。
- 不写练习题、自测题，也不要用多种颜色的提示框。全文只保留 `记:` 这一种底色。
