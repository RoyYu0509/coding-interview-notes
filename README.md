# Coding Interview Notes (Python)

按公司出题热度排序的算法面试 learning docs。

## 第 1 步:题目热度统计 (已完成)

- 数据源:[liquidslr/leetcode-company-wise-problems](https://github.com/liquidslr/leetcode-company-wise-problems),470 家公司,数据截至 2025-06-01。
- 脚本:`scripts/count_problems.py`。统计每道题出现在多少家公司的 `All` 列表里,把每道题归到一个面试 pattern category。
- 结果:
  - `data/RANKING.md`:category 热度排行、总 Top 100、每个 category 的 Top 25
  - `data/problems_ranked.csv`:全部 3396 道题的排行
  - `data/category_summary.csv`:每个 category 的汇总

重新生成:

```bash
git clone --depth 1 https://github.com/liquidslr/leetcode-company-wise-problems.git /tmp/lc
python3 scripts/count_problems.py /tmp/lc data/
```

## 第 2 步: learning docs (已完成)

直接打开 `docs/NN-*.html` 就能读 (单文件, 没有 JS)。建议顺序:

| # | 文档 | 内容 |
|---|---|---|
| 01 | `docs/01-hash-table.html` | Two Sum, Group Anagrams, Longest Consecutive ... |
| 02 | `docs/02-two-pointers.html` | 3Sum, Container With Most Water, Trapping Rain Water ... |
| 03 | `docs/03-sliding-window.html` | Longest Substring, Minimum Window Substring ... |
| 04 | `docs/04-prefix-sum.html` | Subarray Sum Equals K, Product Except Self ... |
| 05 | `docs/05-binary-search.html` | Rotated Array, Koko, Split Array Largest Sum ... |
| 06 | `docs/06-stack.html` | Valid Parentheses, Decode String, Basic Calculator ... |
| 07 | `docs/07-monotonic-stack.html` | Daily Temperatures, Largest Rectangle, Sliding Window Max |
| 08 | `docs/08-linked-list.html` | Reverse, Merge, Fast/Slow, Reverse k-Group ... |
| 09 | `docs/09-heap.html` | Kth Largest, Top K, Merge k Lists, Median, Hire K Workers |
| 10 | `docs/10-intervals.html` | Merge Intervals, Meeting Rooms II ... |
| 11 | `docs/11-tree.html` | Max Path Sum, Validate BST, LCA, Serialize ... |
| 12 | `docs/12-graph.html` | Islands, Rotting Oranges, Course Schedule, Union-Find, Dijkstra |
| 13 | `docs/13-backtracking.html` | Subsets, Permutations, Combination Sum, N-Queens ... |
| 14 | `docs/14-dp-1d.html` | House Robber, Kadane, Coin Change, Knapsack, LIS ... |
| 15 | `docs/15-dp-2d.html` | LCS, Edit Distance, Palindromes, Regex ... |
| 16 | `docs/16-greedy.html` | Jump Game, Gas Station, Candy ... |
| 17 | `docs/17-design.html` | LRU Cache, GetRandom O(1), Snapshot Array ... |
| 18 | `docs/18-string-trie.html` | atoi, Trie, Word Search II ... |
| 19 | `docs/19-matrix-math-bit.html` | Spiral, Rotate, Pow, XOR, bit tricks ... |

每份文档的生成脚本是 `build/NN_*.py`, 运行 `cd build && python3 -I NN_*.py` 会先对拍代码, 再生成 SVG 和 HTML。

- 讲解规则: `STYLE_GUIDE.md`
- 讲题 skill: `.claude/skills/algo-walkthrough/SKILL.md`
- 复盘: `RETRO.md`
