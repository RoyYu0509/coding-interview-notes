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

## 第 2 步:每个 category 一份 learning doc (待做)
