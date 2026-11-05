"""
统计 liquidslr/leetcode-company-wise-problems 中每道题被多少家公司考过,
并把每道题归到一个面试 pattern category,输出排行榜。

用法:
    git clone --depth 1 https://github.com/liquidslr/leetcode-company-wise-problems.git
    python3 scripts/count_problems.py leetcode-company-wise-problems data/

输出:
    data/problems_ranked.csv     所有题目的总排行
    data/category_summary.csv    每个 category 的题量和热度
    data/RANKING.md              人能读的报告: 总 Top 100 + 每个 category 的 Top 题
"""
import csv
import os
import sys
from collections import defaultdict

ALL_FILE = "5. All.csv"
RECENT_FILE = "2. Three Months.csv"

# ---------------------------------------------------------------------
# 1. 按 LeetCode tag 归类。从上往下匹配,第一条命中的规则决定 category。
#    越具体的 pattern 越靠前,Array / String 这种泛 tag 放最后。
# ---------------------------------------------------------------------
CATEGORY_RULES = [
    ("SQL / Database", lambda t, n: "Database" in t),
    ("Concurrency", lambda t, n: "Concurrency" in t),
    ("Intervals", lambda t, n: any(w in n.lower() for w in (
        "interval", "meeting room", "overlap", "my calendar",
        "minimum number of arrows", "employee free time"))),
    ("Trie", lambda t, n: "Trie" in t),
    ("Union-Find", lambda t, n: "Union-Find" in t and not (
        "Matrix" in t and ("Depth-First Search" in t or
                           "Breadth-First Search" in t))),
    ("Graph (BFS / DFS / Topological Sort / Shortest Path)",
     lambda t, n: bool(t & {"Graph Theory", "Topological Sort",
                            "Shortest Path", "Dijkstra's Algorithm"})
     or ("Matrix" in t and ("Depth-First Search" in t or
                            "Breadth-First Search" in t)
         and "Backtracking" not in t)
     # 非 tree / 非 DP 的 BFS 题 (Word Ladder, Open the Lock) 本质是图上 BFS
     or ("Breadth-First Search" in t and not (
         t & {"Tree", "Binary Tree", "Binary Search Tree",
              "Dynamic Programming"}))),
    ("Backtracking", lambda t, n: "Backtracking" in t),
    ("Tree", lambda t, n: bool(t & {"Tree", "Binary Tree",
                                    "Binary Search Tree"})),
    ("Linked List", lambda t, n: "Linked List" in t),
    ("Design", lambda t, n: "Design" in t),
    ("Heap / Top-K", lambda t, n: bool(t & {"Heap (Priority Queue)",
                                            "Quickselect"})),
    ("Monotonic Stack / Queue", lambda t, n: bool(
        t & {"Monotonic Stack", "Monotonic Queue"})),
    ("Sliding Window", lambda t, n: "Sliding Window" in t),
    ("Dynamic Programming", lambda t, n: bool(
        t & {"Dynamic Programming", "Memoization"})),
    ("Binary Search", lambda t, n: "Binary Search" in t),
    ("Stack", lambda t, n: "Stack" in t),
    ("Prefix Sum", lambda t, n: "Prefix Sum" in t),
    ("Two Pointers", lambda t, n: "Two Pointers" in t),
    ("Greedy", lambda t, n: "Greedy" in t),
    ("Bit Manipulation", lambda t, n: "Bit Manipulation" in t),
    ("Hash Table / Counting", lambda t, n: bool(
        t & {"Hash Table", "Counting"})),
    ("Matrix / Simulation", lambda t, n: bool(t & {"Matrix",
                                                   "Simulation"})),
    ("Sorting", lambda t, n: "Sorting" in t),
    ("Math", lambda t, n: bool(t & {"Math", "Number Theory",
                                    "Geometry"})),
    ("Array / String Basics", lambda t, n: True),
]

# ---------------------------------------------------------------------
# 2. tag 规则会把少数经典题分错 (例如 LIS 带 Binary Search tag,
#    但面试里主要考 DP)。这里手动修正。
# ---------------------------------------------------------------------
OVERRIDES = {
    "Longest Increasing Subsequence": "Dynamic Programming",
    "Serialize and Deserialize Binary Tree": "Tree",
    "Binary Search Tree Iterator": "Tree",
    "Trapping Rain Water": "Two Pointers",
    "Container With Most Water": "Two Pointers",
    "Split Array Largest Sum": "Binary Search",
    "Koko Eating Bananas": "Binary Search",
    "Capacity To Ship Packages Within D Days": "Binary Search",
    "Merge k Sorted Lists": "Heap / Top-K",
    "Kth Largest Element in an Array": "Heap / Top-K",
    "Find Median from Data Stream": "Heap / Top-K",
    "Sliding Window Maximum": "Monotonic Stack / Queue",
    "Number of Islands": "Graph (BFS / DFS / Topological Sort / Shortest Path)",
    "Word Ladder": "Graph (BFS / DFS / Topological Sort / Shortest Path)",
    "Word Search": "Backtracking",
    "Median of Two Sorted Arrays": "Binary Search",
    "Copy List with Random Pointer": "Linked List",
    "Maximum Subarray": "Dynamic Programming",
    "Subarray Sum Equals K": "Prefix Sum",
    "Longest Consecutive Sequence": "Hash Table / Counting",
    "LRU Cache": "Design",
    "LFU Cache": "Design",
    "Design Circular Queue": "Design",
    "Word Break": "Dynamic Programming",
    "Word Break II": "Dynamic Programming",
    "Top K Frequent Words": "Heap / Top-K",
    "Longest Common Prefix": "Array / String Basics",
    "Jump Game": "Greedy",
    "Jump Game II": "Greedy",
    "Best Time to Buy and Sell Stock II": "Greedy",
    "Intersection of Two Arrays": "Hash Table / Counting",
    "Missing Number": "Bit Manipulation",
}


def classify(topics, title):
    if title in OVERRIDES:
        return OVERRIDES[title]
    for name, rule in CATEGORY_RULES:
        if rule(topics, title):
            return name
    raise AssertionError("unreachable")


def read_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main(src, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    problems = {}
    recent = defaultdict(set)
    companies = sorted(d for d in os.listdir(src)
                       if os.path.isdir(os.path.join(src, d))
                       and not d.startswith("."))

    for company in companies:
        for row in read_csv(os.path.join(src, company, ALL_FILE)):
            title = row["Title"].strip()
            p = problems.setdefault(title, {
                "title": title,
                "difficulty": row["Difficulty"].strip().title(),
                "link": row["Link"].strip(),
                "topics": [t.strip() for t in row["Topics"].split(",")
                           if t.strip()],
                "companies": set(),
                "freq_sum": 0.0,
            })
            p["companies"].add(company)
            p["freq_sum"] += float(row["Frequency"] or 0)
        for row in read_csv(os.path.join(src, company, RECENT_FILE)):
            recent[row["Title"].strip()].add(company)

    for p in problems.values():
        p["category"] = classify(set(p["topics"]), p["title"])
        p["n_companies"] = len(p["companies"])
        p["n_recent"] = len(recent[p["title"]])

    # popularity: 先比考过的公司数, 再比 frequency 总和
    ranked = sorted(problems.values(),
                    key=lambda p: (-p["n_companies"], -p["freq_sum"]))
    for i, p in enumerate(ranked, 1):
        p["rank"] = i

    with open(os.path.join(out_dir, "problems_ranked.csv"), "w",
              newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["rank", "title", "difficulty", "category",
                    "n_companies", "n_companies_last_3_months",
                    "frequency_sum", "topics", "link"])
        for p in ranked:
            w.writerow([p["rank"], p["title"], p["difficulty"],
                        p["category"], p["n_companies"], p["n_recent"],
                        round(p["freq_sum"], 1), "; ".join(p["topics"]),
                        p["link"]])

    by_cat = defaultdict(list)
    for p in ranked:
        by_cat[p["category"]].append(p)
    # category 热度 = 该 category 里 Top 30 题的公司数之和
    cat_order = sorted(by_cat, key=lambda c: -sum(
        p["n_companies"] for p in by_cat[c][:30]))

    with open(os.path.join(out_dir, "category_summary.csv"), "w",
              newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["category", "n_problems", "top30_company_hits",
                    "top_problem"])
        for c in cat_order:
            w.writerow([c, len(by_cat[c]),
                        sum(p["n_companies"] for p in by_cat[c][:30]),
                        by_cat[c][0]["title"]])

    def row(p):
        return "| %d | [%s](%s) | %s | %d | %d |" % (
            p["rank"], p["title"], p["link"], p["difficulty"],
            p["n_companies"], p["n_recent"])

    head = ("| 总排名 | 题目 | 难度 | 考过的公司数 | 近 3 个月公司数 |\n"
            "|---:|---|---|---:|---:|")
    md = ["# LeetCode 公司高频题统计", "",
          "数据源: [liquidslr/leetcode-company-wise-problems]"
          "(https://github.com/liquidslr/leetcode-company-wise-problems)"
          " (数据截至 2025-06-01)。",
          "",
          "- 公司数: %d" % len(companies),
          "- 不同题目数: %d" % len(problems),
          "- popularity = 在多少家公司的 `All` 列表里出现;"
          " 并列时比 Frequency 总和。",
          "- category 先按 LeetCode tag 规则归类,"
          "再对少数经典题手动修正 (见 `scripts/count_problems.py`)。",
          "", "## Category 热度排行", "",
          "| # | Category | 题量 | Top 30 题公司数之和 | 最热的题 |",
          "|---:|---|---:|---:|---|"]
    for i, c in enumerate(cat_order, 1):
        md.append("| %d | %s | %d | %d | %s |" % (
            i, c, len(by_cat[c]),
            sum(p["n_companies"] for p in by_cat[c][:30]),
            by_cat[c][0]["title"]))
    md += ["", "## 总 Top 100", "", head]
    md += [row(p) for p in ranked[:100]]
    md += ["", "## 每个 Category 的 Top 25", ""]
    for c in cat_order:
        md += ["### %s" % c, "", head]
        md += [row(p) for p in by_cat[c][:25]]
        md.append("")
    with open(os.path.join(out_dir, "RANKING.md"), "w",
              encoding="utf-8") as f:
        f.write("\n".join(md))
    print("companies=%d problems=%d" % (len(companies), len(problems)))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
