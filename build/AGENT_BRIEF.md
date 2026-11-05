# Subagent brief: 写一个 category 的 learning doc

你负责一个 category。repo 根目录: /home/user/coding-interview-notes

## 必读(动手前完整读一遍)
1. `STYLE_GUIDE.md` —— 讲题模式 + SVG 规则 + 文档骨架。最重要。
2. `docs/svg/REFERENCE_min_cost_hire_workers.svg` —— 用户亲自迭代多轮得到的参考图。你的 trace 图要做到同样清晰: 一行一步、固定列顺序、颜色区分角色、移除的元素用虚线扔到左边并写原因、具体数字、底部最终答案 + 图例。
3. `build/doclib.py` —— HTML 生成工具 (文件头有用法)。
4. `data/RANKING.md` —— 你的 category 的 Top 25 (按公司数排序)。选题优先用高频题。

## 你要产出的文件 (只碰这些, 不要改别的文件, 不要 git commit)
- `build/<NN>_<slug>.py`        生成脚本
- `docs/svg/<NN>-<slug>/*.svg`  每道题 ≥ 2 张: `<problem>_core.svg` (算法核心/invariant/为什么对) 和 `<problem>_trace.svg` (具体例子 4–6+ 步运行流程)。第 0 节第一性原理也要 1 张 core 图。
- `docs/<NN>-<slug>.html`

## 内容要求
- Python 代码。读者明天面试, 要的是 **通用 pattern 的本质 + 使用时机 + 识别信号**, 覆盖这个 category 里 ~90% 面试会遇到的子 pattern (下面给了清单), 不要在单题特有技巧上花时间。
- 5–9 道题, 由浅到深的变体链。每道题按 STYLE_GUIDE A.8 的固定顺序。
- 第 0 节: brute force 在浪费什么 → pattern 怎么消掉 → 通用 Python 模板。
- 最后一节 "识别信号": 特征 → 做法 → complexity 从 X 降到 Y。
- **正确性**: 每段代码和每张 trace 图里的数字都必须实际跑过。在 scratch 里写测试 (python3 -I), 用 trace 的例子输入跑一遍, 打印每一步的中间状态, 照着打印结果画图。图里每一步数据结构里的元素数量、数值都要和打印对上。
- SVG 手写 (或用 Python 生成 SVG 字符串都行), 配色/字号/版式严格按 STYLE_GUIDE B。

## 检查 (交付前必须做)
1. `cd build && python3 -I <NN>_<slug>.py`
2. `node build/render_check.js docs/<NN>-<slug>.html <scratchpad>/<slug>.png` → codeOverflow 必须 0, textOutOfViewBox 必须空。
3. 用 Read 工具打开截图 (或单独把每张 svg 用 playwright 截图) 亲眼看: 元素不重叠、箭头指对、颜色角色对、文字没被截。有问题就改到没问题。

## 最后回复 (简短)
题目列表 (概念链)、文件路径、检查结果、任何你不确定的地方。
