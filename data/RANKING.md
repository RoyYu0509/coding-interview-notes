# LeetCode 公司高频题统计

数据源: [liquidslr/leetcode-company-wise-problems](https://github.com/liquidslr/leetcode-company-wise-problems) (数据截至 2025-06-01)。

- 公司数: 470
- 不同题目数: 3396
- popularity = 在多少家公司的 `All` 列表里出现; 并列时比 Frequency 总和。
- category 先按 LeetCode tag 规则归类,再对少数经典题手动修正 (见 `scripts/count_problems.py`)。

## Category 热度排行

| # | Category | 题量 | Top 30 题公司数之和 | 最热的题 |
|---:|---|---:|---:|---|
| 1 | Dynamic Programming | 439 | 761 | Best Time to Buy and Sell Stock |
| 2 | Two Pointers | 119 | 692 | Trapping Rain Water |
| 3 | Hash Table / Counting | 283 | 640 | Two Sum |
| 4 | Graph (BFS / DFS / Topological Sort / Shortest Path) | 211 | 597 | Number of Islands |
| 5 | Design | 82 | 522 | LRU Cache |
| 6 | Binary Search | 190 | 499 | Search in Rotated Sorted Array |
| 7 | Heap / Top-K | 125 | 478 | Top K Frequent Elements |
| 8 | Stack | 56 | 453 | Valid Parentheses |
| 9 | Sliding Window | 123 | 434 | Longest Substring Without Repeating Characters |
| 10 | Linked List | 65 | 428 | Reverse Linked List |
| 11 | Tree | 217 | 403 | Binary Tree Maximum Path Sum |
| 12 | Backtracking | 96 | 389 | Generate Parentheses |
| 13 | Monotonic Stack / Queue | 61 | 347 | Sliding Window Maximum |
| 14 | Matrix / Simulation | 132 | 324 | Spiral Matrix |
| 15 | Intervals | 42 | 319 | Merge Intervals |
| 16 | Greedy | 215 | 314 | Jump Game |
| 17 | Array / String Basics | 209 | 301 | Longest Common Prefix |
| 18 | Math | 177 | 287 | Palindrome Number |
| 19 | Prefix Sum | 116 | 269 | Subarray Sum Equals K |
| 20 | SQL / Database | 178 | 242 | Second Highest Salary |
| 21 | Union-Find | 66 | 228 | Evaluate Division |
| 22 | Bit Manipulation | 92 | 216 | Single Number |
| 23 | Trie | 51 | 208 | Implement Trie (Prefix Tree) |
| 24 | Sorting | 44 | 158 | Minimum Absolute Difference |
| 25 | Concurrency | 7 | 24 | Web Crawler Multithreaded |

## 总 Top 100

| 总排名 | 题目 | 难度 | 考过的公司数 | 近 3 个月公司数 |
|---:|---|---|---:|---:|
| 1 | [Two Sum](https://leetcode.com/problems/two-sum) | Easy | 113 | 12 |
| 2 | [LRU Cache](https://leetcode.com/problems/lru-cache) | Medium | 103 | 12 |
| 3 | [Merge Intervals](https://leetcode.com/problems/merge-intervals) | Medium | 100 | 14 |
| 4 | [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters) | Medium | 95 | 13 |
| 5 | [Valid Parentheses](https://leetcode.com/problems/valid-parentheses) | Easy | 90 | 11 |
| 6 | [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock) | Easy | 81 | 14 |
| 7 | [Number of Islands](https://leetcode.com/problems/number-of-islands) | Medium | 81 | 11 |
| 8 | [Group Anagrams](https://leetcode.com/problems/group-anagrams) | Medium | 75 | 10 |
| 9 | [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water) | Hard | 70 | 9 |
| 10 | [Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring) | Medium | 65 | 9 |
| 11 | [Maximum Subarray](https://leetcode.com/problems/maximum-subarray) | Medium | 56 | 9 |
| 12 | [Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix) | Easy | 52 | 8 |
| 13 | [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements) | Medium | 49 | 8 |
| 14 | [3Sum](https://leetcode.com/problems/3sum) | Medium | 48 | 7 |
| 15 | [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum) | Hard | 48 | 9 |
| 16 | [Container With Most Water](https://leetcode.com/problems/container-with-most-water) | Medium | 47 | 8 |
| 17 | [Rotting Oranges](https://leetcode.com/problems/rotting-oranges) | Medium | 47 | 8 |
| 18 | [Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists) | Hard | 46 | 6 |
| 19 | [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array) | Medium | 45 | 6 |
| 20 | [Course Schedule](https://leetcode.com/problems/course-schedule) | Medium | 43 | 5 |
| 21 | [Spiral Matrix](https://leetcode.com/problems/spiral-matrix) | Medium | 42 | 7 |
| 22 | [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream) | Hard | 41 | 7 |
| 23 | [Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays) | Hard | 41 | 8 |
| 24 | [Decode String](https://leetcode.com/problems/decode-string) | Medium | 40 | 7 |
| 25 | [Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii) | Medium | 40 | 5 |
| 26 | [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k) | Medium | 40 | 6 |
| 27 | [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas) | Medium | 40 | 4 |
| 28 | [Valid Palindrome](https://leetcode.com/problems/valid-palindrome) | Easy | 39 | 5 |
| 29 | [String Compression](https://leetcode.com/problems/string-compression) | Medium | 38 | 6 |
| 30 | [Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence) | Medium | 38 | 6 |
| 31 | [Move Zeroes](https://leetcode.com/problems/move-zeroes) | Easy | 37 | 8 |
| 32 | [Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array) | Medium | 37 | 8 |
| 33 | [Sort Colors](https://leetcode.com/problems/sort-colors) | Medium | 37 | 6 |
| 34 | [Course Schedule II](https://leetcode.com/problems/course-schedule-ii) | Medium | 36 | 9 |
| 35 | [Min Stack](https://leetcode.com/problems/min-stack) | Medium | 36 | 3 |
| 36 | [House Robber](https://leetcode.com/problems/house-robber) | Medium | 35 | 6 |
| 37 | [Generate Parentheses](https://leetcode.com/problems/generate-parentheses) | Medium | 35 | 6 |
| 38 | [Coin Change](https://leetcode.com/problems/coin-change) | Medium | 35 | 4 |
| 39 | [Asteroid Collision](https://leetcode.com/problems/asteroid-collision) | Medium | 35 | 6 |
| 40 | [Insert Delete GetRandom O(1)](https://leetcode.com/problems/insert-delete-getrandom-o1) | Medium | 34 | 6 |
| 41 | [Text Justification](https://leetcode.com/problems/text-justification) | Hard | 34 | 2 |
| 42 | [Valid Anagram](https://leetcode.com/problems/valid-anagram) | Easy | 34 | 7 |
| 43 | [Word Ladder](https://leetcode.com/problems/word-ladder) | Hard | 34 | 3 |
| 44 | [Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array) | Easy | 34 | 6 |
| 45 | [Roman to Integer](https://leetcode.com/problems/roman-to-integer) | Easy | 34 | 6 |
| 46 | [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list) | Easy | 33 | 6 |
| 47 | [Climbing Stairs](https://leetcode.com/problems/climbing-stairs) | Easy | 33 | 7 |
| 48 | [Add Two Numbers](https://leetcode.com/problems/add-two-numbers) | Medium | 33 | 5 |
| 49 | [Time Based Key-Value Store](https://leetcode.com/problems/time-based-key-value-store) | Medium | 32 | 7 |
| 50 | [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring) | Hard | 32 | 5 |
| 51 | [Word Search](https://leetcode.com/problems/word-search) | Medium | 32 | 3 |
| 52 | [Rotate Image](https://leetcode.com/problems/rotate-image) | Medium | 32 | 4 |
| 53 | [Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists) | Easy | 32 | 6 |
| 54 | [Letter Combinations of a Phone Number](https://leetcode.com/problems/letter-combinations-of-a-phone-number) | Medium | 32 | 6 |
| 55 | [Jump Game](https://leetcode.com/problems/jump-game) | Medium | 31 | 6 |
| 56 | [Palindrome Number](https://leetcode.com/problems/palindrome-number) | Easy | 30 | 6 |
| 57 | [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self) | Medium | 30 | 5 |
| 58 | [Next Permutation](https://leetcode.com/problems/next-permutation) | Medium | 30 | 5 |
| 59 | [Find First and Last Position of Element in Sorted Array](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array) | Medium | 30 | 6 |
| 60 | [First Missing Positive](https://leetcode.com/problems/first-missing-positive) | Hard | 30 | 3 |
| 61 | [Integer to Roman](https://leetcode.com/problems/integer-to-roman) | Medium | 29 | 5 |
| 62 | [Find Peak Element](https://leetcode.com/problems/find-peak-element) | Medium | 29 | 6 |
| 63 | [LFU Cache](https://leetcode.com/problems/lfu-cache) | Hard | 29 | 6 |
| 64 | [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram) | Hard | 28 | 4 |
| 65 | [Jump Game II](https://leetcode.com/problems/jump-game-ii) | Medium | 28 | 3 |
| 66 | [Gas Station](https://leetcode.com/problems/gas-station) | Medium | 27 | 4 |
| 67 | [Word Break](https://leetcode.com/problems/word-break) | Medium | 26 | 4 |
| 68 | [Basic Calculator II](https://leetcode.com/problems/basic-calculator-ii) | Medium | 26 | 5 |
| 69 | [Best Time to Buy and Sell Stock II](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii) | Medium | 26 | 5 |
| 70 | [Combination Sum](https://leetcode.com/problems/combination-sum) | Medium | 26 | 4 |
| 71 | [Happy Number](https://leetcode.com/problems/happy-number) | Easy | 25 | 4 |
| 72 | [Rotate Array](https://leetcode.com/problems/rotate-array) | Medium | 25 | 7 |
| 73 | [Daily Temperatures](https://leetcode.com/problems/daily-temperatures) | Medium | 25 | 4 |
| 74 | [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence) | Medium | 25 | 5 |
| 75 | [Longest Valid Parentheses](https://leetcode.com/problems/longest-valid-parentheses) | Hard | 25 | 5 |
| 76 | [Reverse Words in a String](https://leetcode.com/problems/reverse-words-in-a-string) | Medium | 25 | 4 |
| 77 | [Maximal Square](https://leetcode.com/problems/maximal-square) | Medium | 25 | 1 |
| 78 | [Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching) | Hard | 24 | 2 |
| 79 | [Palindromic Substrings](https://leetcode.com/problems/palindromic-substrings) | Medium | 24 | 3 |
| 80 | [Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group) | Hard | 24 | 4 |
| 81 | [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum) | Hard | 24 | 4 |
| 82 | [Permutations](https://leetcode.com/problems/permutations) | Medium | 24 | 4 |
| 83 | [Valid Sudoku](https://leetcode.com/problems/valid-sudoku) | Medium | 23 | 3 |
| 84 | [Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array) | Easy | 23 | 6 |
| 85 | [Maximum Profit in Job Scheduling](https://leetcode.com/problems/maximum-profit-in-job-scheduling) | Hard | 23 | 3 |
| 86 | [Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree) | Hard | 23 | 3 |
| 87 | [Linked List Cycle](https://leetcode.com/problems/linked-list-cycle) | Easy | 23 | 5 |
| 88 | [Task Scheduler](https://leetcode.com/problems/task-scheduler) | Medium | 23 | 3 |
| 89 | [Random Pick with Weight](https://leetcode.com/problems/random-pick-with-weight) | Medium | 22 | 3 |
| 90 | [Design Hit Counter](https://leetcode.com/problems/design-hit-counter) | Medium | 22 | 2 |
| 91 | [Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum) | Hard | 22 | 6 |
| 92 | [Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray) | Medium | 22 | 4 |
| 93 | [Basic Calculator](https://leetcode.com/problems/basic-calculator) | Hard | 22 | 3 |
| 94 | [First Unique Character in a String](https://leetcode.com/problems/first-unique-character-in-a-string) | Easy | 22 | 4 |
| 95 | [Edit Distance](https://leetcode.com/problems/edit-distance) | Medium | 22 | 3 |
| 96 | [Reconstruct Itinerary](https://leetcode.com/problems/reconstruct-itinerary) | Hard | 22 | 1 |
| 97 | [Logger Rate Limiter](https://leetcode.com/problems/logger-rate-limiter) | Easy | 21 | 2 |
| 98 | [Lowest Common Ancestor of a Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree) | Medium | 21 | 4 |
| 99 | [Simplify Path](https://leetcode.com/problems/simplify-path) | Medium | 21 | 3 |
| 100 | [Top K Frequent Words](https://leetcode.com/problems/top-k-frequent-words) | Medium | 21 | 2 |

## 每个 Category 的 Top 25

### Dynamic Programming

| 总排名 | 题目 | 难度 | 考过的公司数 | 近 3 个月公司数 |
|---:|---|---|---:|---:|
| 6 | [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock) | Easy | 81 | 14 |
| 10 | [Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring) | Medium | 65 | 9 |
| 11 | [Maximum Subarray](https://leetcode.com/problems/maximum-subarray) | Medium | 56 | 9 |
| 36 | [House Robber](https://leetcode.com/problems/house-robber) | Medium | 35 | 6 |
| 38 | [Coin Change](https://leetcode.com/problems/coin-change) | Medium | 35 | 4 |
| 47 | [Climbing Stairs](https://leetcode.com/problems/climbing-stairs) | Easy | 33 | 7 |
| 67 | [Word Break](https://leetcode.com/problems/word-break) | Medium | 26 | 4 |
| 74 | [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence) | Medium | 25 | 5 |
| 75 | [Longest Valid Parentheses](https://leetcode.com/problems/longest-valid-parentheses) | Hard | 25 | 5 |
| 77 | [Maximal Square](https://leetcode.com/problems/maximal-square) | Medium | 25 | 1 |
| 78 | [Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching) | Hard | 24 | 2 |
| 79 | [Palindromic Substrings](https://leetcode.com/problems/palindromic-substrings) | Medium | 24 | 3 |
| 85 | [Maximum Profit in Job Scheduling](https://leetcode.com/problems/maximum-profit-in-job-scheduling) | Hard | 23 | 3 |
| 92 | [Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray) | Medium | 22 | 4 |
| 95 | [Edit Distance](https://leetcode.com/problems/edit-distance) | Medium | 22 | 3 |
| 110 | [Decode Ways](https://leetcode.com/problems/decode-ways) | Medium | 20 | 3 |
| 126 | [Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence) | Medium | 19 | 2 |
| 132 | [Unique Paths](https://leetcode.com/problems/unique-paths) | Medium | 18 | 4 |
| 137 | [Wildcard Matching](https://leetcode.com/problems/wildcard-matching) | Hard | 17 | 2 |
| 162 | [Valid Parenthesis String](https://leetcode.com/problems/valid-parenthesis-string) | Medium | 16 | 4 |
| 167 | [House Robber II](https://leetcode.com/problems/house-robber-ii) | Medium | 16 | 4 |
| 168 | [Russian Doll Envelopes](https://leetcode.com/problems/russian-doll-envelopes) | Hard | 16 | 4 |
| 169 | [Burst Balloons](https://leetcode.com/problems/burst-balloons) | Hard | 16 | 3 |
| 174 | [Pascal's Triangle](https://leetcode.com/problems/pascals-triangle) | Easy | 15 | 5 |
| 175 | [Word Break II](https://leetcode.com/problems/word-break-ii) | Hard | 15 | 2 |

### Two Pointers

| 总排名 | 题目 | 难度 | 考过的公司数 | 近 3 个月公司数 |
|---:|---|---|---:|---:|
| 9 | [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water) | Hard | 70 | 9 |
| 14 | [3Sum](https://leetcode.com/problems/3sum) | Medium | 48 | 7 |
| 16 | [Container With Most Water](https://leetcode.com/problems/container-with-most-water) | Medium | 47 | 8 |
| 28 | [Valid Palindrome](https://leetcode.com/problems/valid-palindrome) | Easy | 39 | 5 |
| 29 | [String Compression](https://leetcode.com/problems/string-compression) | Medium | 38 | 6 |
| 31 | [Move Zeroes](https://leetcode.com/problems/move-zeroes) | Easy | 37 | 8 |
| 33 | [Sort Colors](https://leetcode.com/problems/sort-colors) | Medium | 37 | 6 |
| 44 | [Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array) | Easy | 34 | 6 |
| 58 | [Next Permutation](https://leetcode.com/problems/next-permutation) | Medium | 30 | 5 |
| 71 | [Happy Number](https://leetcode.com/problems/happy-number) | Easy | 25 | 4 |
| 72 | [Rotate Array](https://leetcode.com/problems/rotate-array) | Medium | 25 | 7 |
| 76 | [Reverse Words in a String](https://leetcode.com/problems/reverse-words-in-a-string) | Medium | 25 | 4 |
| 84 | [Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array) | Easy | 23 | 6 |
| 122 | [4Sum](https://leetcode.com/problems/4sum) | Medium | 19 | 5 |
| 154 | [Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array) | Easy | 16 | 4 |
| 157 | [Find the Index of the First Occurrence in a String](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string) | Easy | 16 | 5 |
| 158 | [Valid Palindrome II](https://leetcode.com/problems/valid-palindrome-ii) | Easy | 16 | 3 |
| 180 | [Reverse String](https://leetcode.com/problems/reverse-string) | Easy | 15 | 5 |
| 195 | [Count Binary Substrings](https://leetcode.com/problems/count-binary-substrings) | Easy | 15 | 2 |
| 235 | [Reverse Vowels of a String](https://leetcode.com/problems/reverse-vowels-of-a-string) | Easy | 13 | 4 |
| 245 | [3Sum Closest](https://leetcode.com/problems/3sum-closest) | Medium | 12 | 4 |
| 271 | [Boats to Save People](https://leetcode.com/problems/boats-to-save-people) | Medium | 12 | 3 |
| 282 | [Candy Crush](https://leetcode.com/problems/candy-crush) | Medium | 11 | 1 |
| 301 | [Next Greater Element III](https://leetcode.com/problems/next-greater-element-iii) | Medium | 11 | 0 |
| 314 | [Compare Version Numbers](https://leetcode.com/problems/compare-version-numbers) | Medium | 10 | 0 |

### Hash Table / Counting

| 总排名 | 题目 | 难度 | 考过的公司数 | 近 3 个月公司数 |
|---:|---|---|---:|---:|
| 1 | [Two Sum](https://leetcode.com/problems/two-sum) | Easy | 113 | 12 |
| 8 | [Group Anagrams](https://leetcode.com/problems/group-anagrams) | Medium | 75 | 10 |
| 30 | [Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence) | Medium | 38 | 6 |
| 42 | [Valid Anagram](https://leetcode.com/problems/valid-anagram) | Easy | 34 | 7 |
| 45 | [Roman to Integer](https://leetcode.com/problems/roman-to-integer) | Easy | 34 | 6 |
| 60 | [First Missing Positive](https://leetcode.com/problems/first-missing-positive) | Hard | 30 | 3 |
| 61 | [Integer to Roman](https://leetcode.com/problems/integer-to-roman) | Medium | 29 | 5 |
| 83 | [Valid Sudoku](https://leetcode.com/problems/valid-sudoku) | Medium | 23 | 3 |
| 94 | [First Unique Character in a String](https://leetcode.com/problems/first-unique-character-in-a-string) | Easy | 22 | 4 |
| 105 | [Majority Element](https://leetcode.com/problems/majority-element) | Easy | 20 | 7 |
| 114 | [Contains Duplicate](https://leetcode.com/problems/contains-duplicate) | Easy | 19 | 5 |
| 116 | [Set Matrix Zeroes](https://leetcode.com/problems/set-matrix-zeroes) | Medium | 19 | 1 |
| 176 | [Isomorphic Strings](https://leetcode.com/problems/isomorphic-strings) | Easy | 15 | 4 |
| 184 | [Max Points on a Line](https://leetcode.com/problems/max-points-on-a-line) | Hard | 15 | 2 |
| 199 | [Intersection of Two Arrays](https://leetcode.com/problems/intersection-of-two-arrays) | Easy | 14 | 3 |
| 219 | [Ransom Note](https://leetcode.com/problems/ransom-note) | Easy | 13 | 5 |
| 230 | [Degree of an Array](https://leetcode.com/problems/degree-of-an-array) | Easy | 13 | 1 |
| 284 | [Majority Element II](https://leetcode.com/problems/majority-element-ii) | Medium | 11 | 2 |
| 322 | [Count Vowel Substrings of a String](https://leetcode.com/problems/count-vowel-substrings-of-a-string) | Easy | 10 | 1 |
| 330 | [Minimum Number of Steps to Make Two Strings Anagram](https://leetcode.com/problems/minimum-number-of-steps-to-make-two-strings-anagram) | Medium | 10 | 0 |
| 362 | [Sparse Matrix Multiplication](https://leetcode.com/problems/sparse-matrix-multiplication) | Medium | 10 | 0 |
| 372 | [Restore the Array From Adjacent Pairs](https://leetcode.com/problems/restore-the-array-from-adjacent-pairs) | Medium | 9 | 0 |
| 412 | [Fraction to Recurring Decimal](https://leetcode.com/problems/fraction-to-recurring-decimal) | Medium | 9 | 0 |
| 430 | [Number of Black Blocks](https://leetcode.com/problems/number-of-black-blocks) | Medium | 8 | 0 |
| 431 | [Rank Teams by Votes](https://leetcode.com/problems/rank-teams-by-votes) | Medium | 8 | 1 |

### Graph (BFS / DFS / Topological Sort / Shortest Path)

| 总排名 | 题目 | 难度 | 考过的公司数 | 近 3 个月公司数 |
|---:|---|---|---:|---:|
| 7 | [Number of Islands](https://leetcode.com/problems/number-of-islands) | Medium | 81 | 11 |
| 17 | [Rotting Oranges](https://leetcode.com/problems/rotting-oranges) | Medium | 47 | 8 |
| 20 | [Course Schedule](https://leetcode.com/problems/course-schedule) | Medium | 43 | 5 |
| 34 | [Course Schedule II](https://leetcode.com/problems/course-schedule-ii) | Medium | 36 | 9 |
| 43 | [Word Ladder](https://leetcode.com/problems/word-ladder) | Hard | 34 | 3 |
| 96 | [Reconstruct Itinerary](https://leetcode.com/problems/reconstruct-itinerary) | Hard | 22 | 1 |
| 112 | [Alien Dictionary](https://leetcode.com/problems/alien-dictionary) | Hard | 19 | 5 |
| 124 | [Longest Increasing Path in a Matrix](https://leetcode.com/problems/longest-increasing-path-in-a-matrix) | Hard | 19 | 3 |
| 130 | [Clone Graph](https://leetcode.com/problems/clone-graph) | Medium | 18 | 2 |
| 133 | [Max Area of Island](https://leetcode.com/problems/max-area-of-island) | Medium | 18 | 1 |
| 149 | [Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops) | Medium | 17 | 4 |
| 156 | [Bus Routes](https://leetcode.com/problems/bus-routes) | Hard | 16 | 4 |
| 159 | [Making A Large Island](https://leetcode.com/problems/making-a-large-island) | Hard | 16 | 3 |
| 165 | [Shortest Bridge](https://leetcode.com/problems/shortest-bridge) | Medium | 16 | 0 |
| 192 | [Word Ladder II](https://leetcode.com/problems/word-ladder-ii) | Hard | 15 | 0 |
| 198 | [Open the Lock](https://leetcode.com/problems/open-the-lock) | Medium | 15 | 0 |
| 208 | [Shortest Path in a Grid with Obstacles Elimination](https://leetcode.com/problems/shortest-path-in-a-grid-with-obstacles-elimination) | Hard | 14 | 0 |
| 236 | [Shortest Path in Binary Matrix](https://leetcode.com/problems/shortest-path-in-binary-matrix) | Medium | 13 | 2 |
| 243 | [Trapping Rain Water II](https://leetcode.com/problems/trapping-rain-water-ii) | Hard | 12 | 1 |
| 248 | [Collect Coins in a Tree](https://leetcode.com/problems/collect-coins-in-a-tree) | Hard | 12 | 0 |
| 249 | [Shortest Distance from All Buildings](https://leetcode.com/problems/shortest-distance-from-all-buildings) | Hard | 12 | 0 |
| 252 | [Number of Distinct Islands](https://leetcode.com/problems/number-of-distinct-islands) | Medium | 12 | 3 |
| 262 | [Pacific Atlantic Water Flow](https://leetcode.com/problems/pacific-atlantic-water-flow) | Medium | 12 | 2 |
| 263 | [Flood Fill](https://leetcode.com/problems/flood-fill) | Easy | 12 | 2 |
| 266 | [Surrounded Regions](https://leetcode.com/problems/surrounded-regions) | Medium | 12 | 1 |

### Design

| 总排名 | 题目 | 难度 | 考过的公司数 | 近 3 个月公司数 |
|---:|---|---|---:|---:|
| 2 | [LRU Cache](https://leetcode.com/problems/lru-cache) | Medium | 103 | 12 |
| 35 | [Min Stack](https://leetcode.com/problems/min-stack) | Medium | 36 | 3 |
| 40 | [Insert Delete GetRandom O(1)](https://leetcode.com/problems/insert-delete-getrandom-o1) | Medium | 34 | 6 |
| 49 | [Time Based Key-Value Store](https://leetcode.com/problems/time-based-key-value-store) | Medium | 32 | 7 |
| 63 | [LFU Cache](https://leetcode.com/problems/lfu-cache) | Hard | 29 | 6 |
| 90 | [Design Hit Counter](https://leetcode.com/problems/design-hit-counter) | Medium | 22 | 2 |
| 97 | [Logger Rate Limiter](https://leetcode.com/problems/logger-rate-limiter) | Easy | 21 | 2 |
| 107 | [Design Circular Queue](https://leetcode.com/problems/design-circular-queue) | Medium | 20 | 0 |
| 136 | [Design Memory Allocator](https://leetcode.com/problems/design-memory-allocator) | Medium | 18 | 3 |
| 139 | [Snapshot Array](https://leetcode.com/problems/snapshot-array) | Medium | 17 | 2 |
| 152 | [Simple Bank System](https://leetcode.com/problems/simple-bank-system) | Medium | 16 | 1 |
| 250 | [Design Tic-Tac-Toe](https://leetcode.com/problems/design-tic-tac-toe) | Medium | 12 | 0 |
| 256 | [Insert Delete GetRandom O(1) - Duplicates allowed](https://leetcode.com/problems/insert-delete-getrandom-o1-duplicates-allowed) | Hard | 12 | 1 |
| 265 | [Implement Queue using Stacks](https://leetcode.com/problems/implement-queue-using-stacks) | Easy | 12 | 1 |
| 307 | [Dot Product of Two Sparse Vectors](https://leetcode.com/problems/dot-product-of-two-sparse-vectors) | Medium | 11 | 0 |
| 308 | [Maximum Frequency Stack](https://leetcode.com/problems/maximum-frequency-stack) | Hard | 11 | 0 |
| 350 | [Range Sum Query 2D - Immutable](https://leetcode.com/problems/range-sum-query-2d-immutable) | Medium | 10 | 1 |
| 380 | [Moving Average from Data Stream](https://leetcode.com/problems/moving-average-from-data-stream) | Easy | 9 | 0 |
| 398 | [Encode and Decode Strings](https://leetcode.com/problems/encode-and-decode-strings) | Medium | 9 | 0 |
| 399 | [Implement Stack using Queues](https://leetcode.com/problems/implement-stack-using-queues) | Easy | 9 | 0 |
| 417 | [Product of the Last K Numbers](https://leetcode.com/problems/product-of-the-last-k-numbers) | Medium | 9 | 0 |
| 419 | [Design Snake Game](https://leetcode.com/problems/design-snake-game) | Medium | 9 | 0 |
| 428 | [Encode and Decode TinyURL](https://leetcode.com/problems/encode-and-decode-tinyurl) | Medium | 9 | 0 |
| 449 | [Number of Recent Calls](https://leetcode.com/problems/number-of-recent-calls) | Easy | 8 | 3 |
| 451 | [Design A Leaderboard](https://leetcode.com/problems/design-a-leaderboard) | Medium | 8 | 0 |

### Binary Search

| 总排名 | 题目 | 难度 | 考过的公司数 | 近 3 个月公司数 |
|---:|---|---|---:|---:|
| 19 | [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array) | Medium | 45 | 6 |
| 23 | [Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays) | Hard | 41 | 8 |
| 27 | [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas) | Medium | 40 | 4 |
| 59 | [Find First and Last Position of Element in Sorted Array](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array) | Medium | 30 | 6 |
| 62 | [Find Peak Element](https://leetcode.com/problems/find-peak-element) | Medium | 29 | 6 |
| 89 | [Random Pick with Weight](https://leetcode.com/problems/random-pick-with-weight) | Medium | 22 | 3 |
| 91 | [Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum) | Hard | 22 | 6 |
| 108 | [Capacity To Ship Packages Within D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days) | Medium | 20 | 2 |
| 134 | [Find the Duplicate Number](https://leetcode.com/problems/find-the-duplicate-number) | Medium | 18 | 2 |
| 143 | [Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix) | Medium | 17 | 4 |
| 161 | [Sqrt(x)](https://leetcode.com/problems/sqrtx) | Easy | 16 | 4 |
| 178 | [Single Element in a Sorted Array](https://leetcode.com/problems/single-element-in-a-sorted-array) | Medium | 15 | 4 |
| 214 | [Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array) | Medium | 14 | 4 |
| 217 | [Block Placement Queries](https://leetcode.com/problems/block-placement-queries) | Hard | 13 | 4 |
| 233 | [Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted) | Medium | 13 | 4 |
| 234 | [Search a 2D Matrix II](https://leetcode.com/problems/search-a-2d-matrix-ii) | Medium | 13 | 3 |
| 272 | [Heaters](https://leetcode.com/problems/heaters) | Medium | 12 | 1 |
| 280 | [Search Insert Position](https://leetcode.com/problems/search-insert-position) | Easy | 11 | 5 |
| 291 | [Binary Search](https://leetcode.com/problems/binary-search) | Easy | 11 | 5 |
| 295 | [Find the Smallest Divisor Given a Threshold](https://leetcode.com/problems/find-the-smallest-divisor-given-a-threshold) | Medium | 11 | 1 |
| 347 | [Search in Rotated Sorted Array II](https://leetcode.com/problems/search-in-rotated-sorted-array-ii) | Medium | 10 | 1 |
| 371 | [Peak Index in a Mountain Array](https://leetcode.com/problems/peak-index-in-a-mountain-array) | Medium | 9 | 2 |
| 376 | [Minimum Number of Days to Make m Bouquets](https://leetcode.com/problems/minimum-number-of-days-to-make-m-bouquets) | Medium | 9 | 1 |
| 393 | [Kth Missing Positive Number](https://leetcode.com/problems/kth-missing-positive-number) | Easy | 9 | 1 |
| 422 | [Intersection of Two Arrays II](https://leetcode.com/problems/intersection-of-two-arrays-ii) | Easy | 9 | 0 |

### Heap / Top-K

| 总排名 | 题目 | 难度 | 考过的公司数 | 近 3 个月公司数 |
|---:|---|---|---:|---:|
| 13 | [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements) | Medium | 49 | 8 |
| 18 | [Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists) | Hard | 46 | 6 |
| 22 | [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream) | Hard | 41 | 7 |
| 32 | [Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array) | Medium | 37 | 8 |
| 88 | [Task Scheduler](https://leetcode.com/problems/task-scheduler) | Medium | 23 | 3 |
| 100 | [Top K Frequent Words](https://leetcode.com/problems/top-k-frequent-words) | Medium | 21 | 2 |
| 144 | [Reorganize String](https://leetcode.com/problems/reorganize-string) | Medium | 17 | 1 |
| 148 | [Find K Closest Elements](https://leetcode.com/problems/find-k-closest-elements) | Medium | 17 | 3 |
| 171 | [K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin) | Medium | 16 | 1 |
| 173 | [Maximum Number of Events That Can Be Attended](https://leetcode.com/problems/maximum-number-of-events-that-can-be-attended) | Medium | 16 | 0 |
| 205 | [Sort Characters By Frequency](https://leetcode.com/problems/sort-characters-by-frequency) | Medium | 14 | 3 |
| 254 | [Car Pooling](https://leetcode.com/problems/car-pooling) | Medium | 12 | 3 |
| 255 | [The Skyline Problem](https://leetcode.com/problems/the-skyline-problem) | Hard | 12 | 1 |
| 257 | [Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit](https://leetcode.com/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit) | Medium | 12 | 3 |
| 260 | [Furthest Building You Can Reach](https://leetcode.com/problems/furthest-building-you-can-reach) | Medium | 12 | 2 |
| 276 | [Last Stone Weight](https://leetcode.com/problems/last-stone-weight) | Easy | 12 | 1 |
| 302 | [Kth Smallest Element in a Sorted Matrix](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix) | Medium | 11 | 0 |
| 343 | [Sort an Array](https://leetcode.com/problems/sort-an-array) | Medium | 10 | 3 |
| 355 | [Smallest Range Covering Elements from K Lists](https://leetcode.com/problems/smallest-range-covering-elements-from-k-lists) | Hard | 10 | 2 |
| 365 | [Put Marbles in Bags](https://leetcode.com/problems/put-marbles-in-bags) | Hard | 10 | 2 |
| 390 | [Sliding Window Median](https://leetcode.com/problems/sliding-window-median) | Hard | 9 | 1 |
| 408 | [Shortest Subarray with Sum at Least K](https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k) | Hard | 9 | 4 |
| 410 | [Find K Pairs with Smallest Sums](https://leetcode.com/problems/find-k-pairs-with-smallest-sums) | Medium | 9 | 2 |
| 457 | [Minimum Number of Refueling Stops](https://leetcode.com/problems/minimum-number-of-refueling-stops) | Hard | 8 | 4 |
| 467 | [IPO](https://leetcode.com/problems/ipo) | Hard | 8 | 0 |

### Stack

| 总排名 | 题目 | 难度 | 考过的公司数 | 近 3 个月公司数 |
|---:|---|---|---:|---:|
| 5 | [Valid Parentheses](https://leetcode.com/problems/valid-parentheses) | Easy | 90 | 11 |
| 24 | [Decode String](https://leetcode.com/problems/decode-string) | Medium | 40 | 7 |
| 39 | [Asteroid Collision](https://leetcode.com/problems/asteroid-collision) | Medium | 35 | 6 |
| 68 | [Basic Calculator II](https://leetcode.com/problems/basic-calculator-ii) | Medium | 26 | 5 |
| 93 | [Basic Calculator](https://leetcode.com/problems/basic-calculator) | Hard | 22 | 3 |
| 99 | [Simplify Path](https://leetcode.com/problems/simplify-path) | Medium | 21 | 3 |
| 119 | [Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation) | Medium | 19 | 5 |
| 129 | [Remove All Adjacent Duplicates in String II](https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string-ii) | Medium | 18 | 2 |
| 179 | [Basic Calculator III](https://leetcode.com/problems/basic-calculator-iii) | Hard | 15 | 0 |
| 201 | [Remove All Adjacent Duplicates In String](https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string) | Easy | 14 | 2 |
| 238 | [Remove All Occurrences of a Substring](https://leetcode.com/problems/remove-all-occurrences-of-a-substring) | Medium | 13 | 1 |
| 289 | [Exclusive Time of Functions](https://leetcode.com/problems/exclusive-time-of-functions) | Medium | 11 | 1 |
| 290 | [Backspace String Compare](https://leetcode.com/problems/backspace-string-compare) | Easy | 11 | 2 |
| 297 | [Using a Robot to Print the Lexicographically Smallest String](https://leetcode.com/problems/using-a-robot-to-print-the-lexicographically-smallest-string) | Medium | 11 | 4 |
| 334 | [Minimum Remove to Make Valid Parentheses](https://leetcode.com/problems/minimum-remove-to-make-valid-parentheses) | Medium | 10 | 1 |
| 360 | [Minimum Number of Swaps to Make the String Balanced](https://leetcode.com/problems/minimum-number-of-swaps-to-make-the-string-balanced) | Medium | 10 | 1 |
| 458 | [Maximum Nesting Depth of the Parentheses](https://leetcode.com/problems/maximum-nesting-depth-of-the-parentheses) | Easy | 8 | 2 |
| 487 | [Reverse Substrings Between Each Pair of Parentheses](https://leetcode.com/problems/reverse-substrings-between-each-pair-of-parentheses) | Medium | 8 | 1 |
| 554 | [Minimum Add to Make Parentheses Valid](https://leetcode.com/problems/minimum-add-to-make-parentheses-valid) | Medium | 7 | 4 |
| 594 | [Remove Outermost Parentheses](https://leetcode.com/problems/remove-outermost-parentheses) | Easy | 7 | 3 |
| 605 | [Check if a Parentheses String Can Be Valid](https://leetcode.com/problems/check-if-a-parentheses-string-can-be-valid) | Medium | 7 | 0 |
| 668 | [Maximum Score From Removing Substrings](https://leetcode.com/problems/maximum-score-from-removing-substrings) | Medium | 7 | 0 |
| 708 | [Number of Atoms](https://leetcode.com/problems/number-of-atoms) | Hard | 6 | 2 |
| 807 | [Robot Collisions](https://leetcode.com/problems/robot-collisions) | Hard | 6 | 0 |
| 891 | [Parsing A Boolean Expression](https://leetcode.com/problems/parsing-a-boolean-expression) | Hard | 6 | 0 |

### Sliding Window

| 总排名 | 题目 | 难度 | 考过的公司数 | 近 3 个月公司数 |
|---:|---|---|---:|---:|
| 4 | [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters) | Medium | 95 | 13 |
| 50 | [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring) | Hard | 32 | 5 |
| 102 | [Max Consecutive Ones III](https://leetcode.com/problems/max-consecutive-ones-iii) | Medium | 21 | 7 |
| 104 | [Subarray Product Less Than K](https://leetcode.com/problems/subarray-product-less-than-k) | Medium | 21 | 5 |
| 128 | [Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement) | Medium | 18 | 5 |
| 172 | [Permutation in String](https://leetcode.com/problems/permutation-in-string) | Medium | 16 | 5 |
| 193 | [Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum) | Medium | 15 | 5 |
| 196 | [Subarrays with K Different Integers](https://leetcode.com/problems/subarrays-with-k-different-integers) | Hard | 15 | 0 |
| 203 | [Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string) | Medium | 14 | 3 |
| 224 | [Maximum Points You Can Obtain from Cards](https://leetcode.com/problems/maximum-points-you-can-obtain-from-cards) | Medium | 13 | 4 |
| 226 | [Fruit Into Baskets](https://leetcode.com/problems/fruit-into-baskets) | Medium | 13 | 5 |
| 240 | [Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters) | Medium | 13 | 1 |
| 242 | [Contains Duplicate II](https://leetcode.com/problems/contains-duplicate-ii) | Easy | 12 | 5 |
| 317 | [Frequency of the Most Frequent Element](https://leetcode.com/problems/frequency-of-the-most-frequent-element) | Medium | 10 | 5 |
| 329 | [Substring with Concatenation of All Words](https://leetcode.com/problems/substring-with-concatenation-of-all-words) | Hard | 10 | 3 |
| 348 | [Maximum Average Subarray I](https://leetcode.com/problems/maximum-average-subarray-i) | Easy | 10 | 4 |
| 389 | [Longest Substring with At Least K Repeating Characters](https://leetcode.com/problems/longest-substring-with-at-least-k-repeating-characters) | Medium | 9 | 1 |
| 395 | [Count Number of Nice Subarrays](https://leetcode.com/problems/count-number-of-nice-subarrays) | Medium | 9 | 2 |
| 415 | [Maximum Number of Occurrences of a Substring](https://leetcode.com/problems/maximum-number-of-occurrences-of-a-substring) | Medium | 9 | 1 |
| 446 | [Longest Subarray of 1's After Deleting One Element](https://leetcode.com/problems/longest-subarray-of-1s-after-deleting-one-element) | Medium | 8 | 3 |
| 502 | [Grumpy Bookstore Owner](https://leetcode.com/problems/grumpy-bookstore-owner) | Medium | 8 | 1 |
| 545 | [Binary Subarrays With Sum](https://leetcode.com/problems/binary-subarrays-with-sum) | Medium | 7 | 3 |
| 547 | [Repeated DNA Sequences](https://leetcode.com/problems/repeated-dna-sequences) | Medium | 7 | 2 |
| 583 | [Alternating Groups II](https://leetcode.com/problems/alternating-groups-ii) | Medium | 7 | 1 |
| 590 | [Number of Substrings Containing All Three Characters](https://leetcode.com/problems/number-of-substrings-containing-all-three-characters) | Medium | 7 | 0 |

### Linked List

| 总排名 | 题目 | 难度 | 考过的公司数 | 近 3 个月公司数 |
|---:|---|---|---:|---:|
| 46 | [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list) | Easy | 33 | 6 |
| 48 | [Add Two Numbers](https://leetcode.com/problems/add-two-numbers) | Medium | 33 | 5 |
| 53 | [Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists) | Easy | 32 | 6 |
| 80 | [Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group) | Hard | 24 | 4 |
| 87 | [Linked List Cycle](https://leetcode.com/problems/linked-list-cycle) | Easy | 23 | 5 |
| 111 | [Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer) | Medium | 19 | 2 |
| 164 | [Remove Nth Node From End of List](https://leetcode.com/problems/remove-nth-node-from-end-of-list) | Medium | 16 | 3 |
| 181 | [Palindrome Linked List](https://leetcode.com/problems/palindrome-linked-list) | Easy | 15 | 4 |
| 187 | [Reverse Linked List II](https://leetcode.com/problems/reverse-linked-list-ii) | Medium | 15 | 4 |
| 213 | [Swap Nodes in Pairs](https://leetcode.com/problems/swap-nodes-in-pairs) | Medium | 14 | 2 |
| 228 | [Reorder List](https://leetcode.com/problems/reorder-list) | Medium | 13 | 5 |
| 241 | [Design Authentication Manager](https://leetcode.com/problems/design-authentication-manager) | Medium | 12 | 2 |
| 247 | [Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list) | Easy | 12 | 2 |
| 253 | [All O`one Data Structure](https://leetcode.com/problems/all-oone-data-structure) | Hard | 12 | 0 |
| 259 | [Intersection of Two Linked Lists](https://leetcode.com/problems/intersection-of-two-linked-lists) | Easy | 12 | 2 |
| 261 | [Design Twitter](https://leetcode.com/problems/design-twitter) | Medium | 12 | 0 |
| 270 | [Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii) | Medium | 12 | 2 |
| 296 | [Odd Even Linked List](https://leetcode.com/problems/odd-even-linked-list) | Medium | 11 | 2 |
| 298 | [Design HashMap](https://leetcode.com/problems/design-hashmap) | Easy | 11 | 0 |
| 316 | [Rotate List](https://leetcode.com/problems/rotate-list) | Medium | 10 | 3 |
| 328 | [Design a Text Editor](https://leetcode.com/problems/design-a-text-editor) | Hard | 10 | 1 |
| 349 | [Design Browser History](https://leetcode.com/problems/design-browser-history) | Medium | 10 | 3 |
| 367 | [Max Stack](https://leetcode.com/problems/max-stack) | Hard | 9 | 1 |
| 391 | [Sort List](https://leetcode.com/problems/sort-list) | Medium | 9 | 3 |
| 423 | [Remove Duplicates from Sorted List II](https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii) | Medium | 9 | 0 |

### Tree

| 总排名 | 题目 | 难度 | 考过的公司数 | 近 3 个月公司数 |
|---:|---|---|---:|---:|
| 81 | [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum) | Hard | 24 | 4 |
| 86 | [Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree) | Hard | 23 | 3 |
| 98 | [Lowest Common Ancestor of a Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree) | Medium | 21 | 4 |
| 121 | [Diameter of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree) | Easy | 19 | 4 |
| 123 | [Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree) | Medium | 19 | 6 |
| 131 | [Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree) | Easy | 18 | 5 |
| 135 | [Binary Tree Zigzag Level Order Traversal](https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal) | Medium | 18 | 3 |
| 140 | [Flatten Nested List Iterator](https://leetcode.com/problems/flatten-nested-list-iterator) | Medium | 17 | 1 |
| 145 | [All Nodes Distance K in Binary Tree](https://leetcode.com/problems/all-nodes-distance-k-in-binary-tree) | Medium | 17 | 3 |
| 182 | [Binary Tree Cameras](https://leetcode.com/problems/binary-tree-cameras) | Hard | 15 | 1 |
| 190 | [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal) | Medium | 15 | 3 |
| 202 | [Binary Tree Right Side View](https://leetcode.com/problems/binary-tree-right-side-view) | Medium | 14 | 3 |
| 231 | [Amount of Time for Binary Tree to Be Infected](https://leetcode.com/problems/amount-of-time-for-binary-tree-to-be-infected) | Medium | 13 | 0 |
| 251 | [Vertical Order Traversal of a Binary Tree](https://leetcode.com/problems/vertical-order-traversal-of-a-binary-tree) | Hard | 12 | 3 |
| 269 | [House Robber III](https://leetcode.com/problems/house-robber-iii) | Medium | 12 | 1 |
| 293 | [Lowest Common Ancestor of a Binary Tree III](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree-iii) | Medium | 11 | 1 |
| 304 | [Delete Node in a BST](https://leetcode.com/problems/delete-node-in-a-bst) | Medium | 11 | 1 |
| 318 | [Symmetric Tree](https://leetcode.com/problems/symmetric-tree) | Easy | 10 | 3 |
| 321 | [Lowest Common Ancestor of a Binary Search Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree) | Medium | 10 | 3 |
| 326 | [Kth Smallest Element in a BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst) | Medium | 10 | 2 |
| 337 | [Construct Binary Tree from Preorder and Inorder Traversal](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal) | Medium | 10 | 0 |
| 344 | [Boundary of Binary Tree](https://leetcode.com/problems/boundary-of-binary-tree) | Medium | 10 | 0 |
| 346 | [Unique Binary Search Trees](https://leetcode.com/problems/unique-binary-search-trees) | Medium | 10 | 1 |
| 356 | [Convert Sorted List to Binary Search Tree](https://leetcode.com/problems/convert-sorted-list-to-binary-search-tree) | Medium | 10 | 1 |
| 378 | [Kth Largest Element in a Stream](https://leetcode.com/problems/kth-largest-element-in-a-stream) | Easy | 9 | 1 |

### Backtracking

| 总排名 | 题目 | 难度 | 考过的公司数 | 近 3 个月公司数 |
|---:|---|---|---:|---:|
| 37 | [Generate Parentheses](https://leetcode.com/problems/generate-parentheses) | Medium | 35 | 6 |
| 51 | [Word Search](https://leetcode.com/problems/word-search) | Medium | 32 | 3 |
| 54 | [Letter Combinations of a Phone Number](https://leetcode.com/problems/letter-combinations-of-a-phone-number) | Medium | 32 | 6 |
| 70 | [Combination Sum](https://leetcode.com/problems/combination-sum) | Medium | 26 | 4 |
| 82 | [Permutations](https://leetcode.com/problems/permutations) | Medium | 24 | 4 |
| 118 | [Subsets](https://leetcode.com/problems/subsets) | Medium | 19 | 5 |
| 120 | [Restore IP Addresses](https://leetcode.com/problems/restore-ip-addresses) | Medium | 19 | 2 |
| 160 | [N-Queens](https://leetcode.com/problems/n-queens) | Hard | 16 | 5 |
| 183 | [Sudoku Solver](https://leetcode.com/problems/sudoku-solver) | Hard | 15 | 1 |
| 191 | [Combination Sum II](https://leetcode.com/problems/combination-sum-ii) | Medium | 15 | 2 |
| 223 | [Optimal Account Balancing](https://leetcode.com/problems/optimal-account-balancing) | Hard | 13 | 4 |
| 324 | [Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning) | Medium | 10 | 4 |
| 359 | [Path Sum II](https://leetcode.com/problems/path-sum-ii) | Medium | 10 | 3 |
| 369 | [Target Sum](https://leetcode.com/problems/target-sum) | Medium | 9 | 2 |
| 377 | [N-Queens II](https://leetcode.com/problems/n-queens-ii) | Hard | 9 | 0 |
| 439 | [Subsets II](https://leetcode.com/problems/subsets-ii) | Medium | 8 | 1 |
| 456 | [Binary Tree Paths](https://leetcode.com/problems/binary-tree-paths) | Easy | 8 | 1 |
| 489 | [Permutations II](https://leetcode.com/problems/permutations-ii) | Medium | 8 | 0 |
| 497 | [Partition to K Equal Sum Subsets](https://leetcode.com/problems/partition-to-k-equal-sum-subsets) | Medium | 8 | 1 |
| 559 | [Robot Room Cleaner](https://leetcode.com/problems/robot-room-cleaner) | Hard | 7 | 0 |
| 596 | [Combinations](https://leetcode.com/problems/combinations) | Medium | 7 | 3 |
| 598 | [24 Game](https://leetcode.com/problems/24-game) | Hard | 7 | 0 |
| 603 | [Beautiful Arrangement](https://leetcode.com/problems/beautiful-arrangement) | Medium | 7 | 0 |
| 645 | [Letter Case Permutation](https://leetcode.com/problems/letter-case-permutation) | Medium | 7 | 1 |
| 661 | [Sliding Puzzle](https://leetcode.com/problems/sliding-puzzle) | Hard | 7 | 0 |

### Monotonic Stack / Queue

| 总排名 | 题目 | 难度 | 考过的公司数 | 近 3 个月公司数 |
|---:|---|---|---:|---:|
| 15 | [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum) | Hard | 48 | 9 |
| 64 | [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram) | Hard | 28 | 4 |
| 73 | [Daily Temperatures](https://leetcode.com/problems/daily-temperatures) | Medium | 25 | 4 |
| 103 | [Remove K Digits](https://leetcode.com/problems/remove-k-digits) | Medium | 21 | 4 |
| 147 | [Next Greater Element II](https://leetcode.com/problems/next-greater-element-ii) | Medium | 17 | 4 |
| 188 | [Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle) | Hard | 15 | 1 |
| 204 | [Sum of Subarray Minimums](https://leetcode.com/problems/sum-of-subarray-minimums) | Medium | 14 | 2 |
| 206 | [Number of Visible People in a Queue](https://leetcode.com/problems/number-of-visible-people-in-a-queue) | Hard | 14 | 1 |
| 207 | [Next Greater Element I](https://leetcode.com/problems/next-greater-element-i) | Easy | 14 | 6 |
| 218 | [Remove Duplicate Letters](https://leetcode.com/problems/remove-duplicate-letters) | Medium | 13 | 3 |
| 274 | [Maximum Sum Circular Subarray](https://leetcode.com/problems/maximum-sum-circular-subarray) | Medium | 12 | 4 |
| 285 | [Car Fleet](https://leetcode.com/problems/car-fleet) | Medium | 11 | 1 |
| 333 | [Count Subarrays With Fixed Bounds](https://leetcode.com/problems/count-subarrays-with-fixed-bounds) | Hard | 10 | 2 |
| 385 | [Smallest Subsequence of Distinct Characters](https://leetcode.com/problems/smallest-subsequence-of-distinct-characters) | Medium | 9 | 0 |
| 402 | [Shortest Unsorted Continuous Subarray](https://leetcode.com/problems/shortest-unsorted-continuous-subarray) | Medium | 9 | 0 |
| 459 | [Minimum Number of Increments on Subarrays to Form a Target Array](https://leetcode.com/problems/minimum-number-of-increments-on-subarrays-to-form-a-target-array) | Hard | 8 | 2 |
| 493 | [Create Maximum Number](https://leetcode.com/problems/create-maximum-number) | Hard | 8 | 0 |
| 552 | [Final Prices With a Special Discount in a Shop](https://leetcode.com/problems/final-prices-with-a-special-discount-in-a-shop) | Easy | 7 | 0 |
| 563 | [Shortest Subarray to be Removed to Make Array Sorted](https://leetcode.com/problems/shortest-subarray-to-be-removed-to-make-array-sorted) | Medium | 7 | 0 |
| 569 | [Maximum Width Ramp](https://leetcode.com/problems/maximum-width-ramp) | Medium | 7 | 0 |
| 589 | [132 Pattern](https://leetcode.com/problems/132-pattern) | Medium | 7 | 2 |
| 650 | [Max Chunks To Make Sorted](https://leetcode.com/problems/max-chunks-to-make-sorted) | Medium | 7 | 0 |
| 830 | [Sum of Subarray Ranges](https://leetcode.com/problems/sum-of-subarray-ranges) | Medium | 6 | 0 |
| 1043 | [Maximum Number of Tasks You Can Assign](https://leetcode.com/problems/maximum-number-of-tasks-you-can-assign) | Hard | 5 | 0 |
| 1123 | [Max Chunks To Make Sorted II](https://leetcode.com/problems/max-chunks-to-make-sorted-ii) | Hard | 5 | 0 |

### Matrix / Simulation

| 总排名 | 题目 | 难度 | 考过的公司数 | 近 3 个月公司数 |
|---:|---|---|---:|---:|
| 21 | [Spiral Matrix](https://leetcode.com/problems/spiral-matrix) | Medium | 42 | 7 |
| 41 | [Text Justification](https://leetcode.com/problems/text-justification) | Hard | 34 | 2 |
| 52 | [Rotate Image](https://leetcode.com/problems/rotate-image) | Medium | 32 | 4 |
| 115 | [Multiply Strings](https://leetcode.com/problems/multiply-strings) | Medium | 19 | 3 |
| 163 | [Fizz Buzz](https://leetcode.com/problems/fizz-buzz) | Easy | 16 | 2 |
| 189 | [Add Strings](https://leetcode.com/problems/add-strings) | Easy | 15 | 0 |
| 225 | [Game of Life](https://leetcode.com/problems/game-of-life) | Medium | 13 | 1 |
| 306 | [Find the Winner of the Circular Game](https://leetcode.com/problems/find-the-winner-of-the-circular-game) | Medium | 11 | 0 |
| 313 | [Diagonal Traverse](https://leetcode.com/problems/diagonal-traverse) | Medium | 10 | 0 |
| 363 | [Spiral Matrix II](https://leetcode.com/problems/spiral-matrix-ii) | Medium | 10 | 0 |
| 392 | [Add Digits](https://leetcode.com/problems/add-digits) | Easy | 9 | 0 |
| 406 | [Best Meeting Point](https://leetcode.com/problems/best-meeting-point) | Hard | 9 | 0 |
| 504 | [Robot Bounded In Circle](https://leetcode.com/problems/robot-bounded-in-circle) | Medium | 8 | 0 |
| 516 | [Concatenation of Array](https://leetcode.com/problems/concatenation-of-array) | Easy | 7 | 4 |
| 597 | [Count Unguarded Cells in the Grid](https://leetcode.com/problems/count-unguarded-cells-in-the-grid) | Medium | 7 | 0 |
| 655 | [Water Bottles](https://leetcode.com/problems/water-bottles) | Easy | 7 | 1 |
| 717 | [Read N Characters Given read4 II - Call Multiple Times](https://leetcode.com/problems/read-n-characters-given-read4-ii-call-multiple-times) | Hard | 6 | 1 |
| 754 | [Transpose Matrix](https://leetcode.com/problems/transpose-matrix) | Easy | 6 | 2 |
| 798 | [Time Needed to Buy Tickets](https://leetcode.com/problems/time-needed-to-buy-tickets) | Easy | 6 | 2 |
| 832 | [Image Smoother](https://leetcode.com/problems/image-smoother) | Easy | 6 | 0 |
| 876 | [Matrix Diagonal Sum](https://leetcode.com/problems/matrix-diagonal-sum) | Easy | 6 | 1 |
| 905 | [Calculate Amount Paid in Taxes](https://leetcode.com/problems/calculate-amount-paid-in-taxes) | Easy | 5 | 1 |
| 911 | [Teemo Attacking](https://leetcode.com/problems/teemo-attacking) | Easy | 5 | 0 |
| 921 | [Toeplitz Matrix](https://leetcode.com/problems/toeplitz-matrix) | Easy | 5 | 0 |
| 950 | [Reshape the Matrix](https://leetcode.com/problems/reshape-the-matrix) | Easy | 5 | 0 |

### Intervals

| 总排名 | 题目 | 难度 | 考过的公司数 | 近 3 个月公司数 |
|---:|---|---|---:|---:|
| 3 | [Merge Intervals](https://leetcode.com/problems/merge-intervals) | Medium | 100 | 14 |
| 25 | [Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii) | Medium | 40 | 5 |
| 151 | [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals) | Medium | 17 | 4 |
| 197 | [Insert Interval](https://leetcode.com/problems/insert-interval) | Medium | 15 | 2 |
| 215 | [Meeting Rooms III](https://leetcode.com/problems/meeting-rooms-iii) | Hard | 14 | 2 |
| 279 | [Interval List Intersections](https://leetcode.com/problems/interval-list-intersections) | Medium | 11 | 2 |
| 309 | [Employee Free Time](https://leetcode.com/problems/employee-free-time) | Hard | 11 | 2 |
| 416 | [Minimum Number of Arrows to Burst Balloons](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons) | Medium | 9 | 1 |
| 420 | [Meeting Rooms](https://leetcode.com/problems/meeting-rooms) | Easy | 9 | 1 |
| 490 | [My Calendar I](https://leetcode.com/problems/my-calendar-i) | Medium | 8 | 0 |
| 567 | [Maximum Number of Non-overlapping Palindrome Substrings](https://leetcode.com/problems/maximum-number-of-non-overlapping-palindrome-substrings) | Hard | 7 | 2 |
| 646 | [Maximum Sum of 3 Non-Overlapping Subarrays](https://leetcode.com/problems/maximum-sum-of-3-non-overlapping-subarrays) | Hard | 7 | 0 |
| 705 | [Two Best Non-Overlapping Events](https://leetcode.com/problems/two-best-non-overlapping-events) | Medium | 6 | 1 |
| 813 | [Rectangle Overlap](https://leetcode.com/problems/rectangle-overlap) | Easy | 6 | 4 |
| 885 | [Count Odd Numbers in an Interval Range](https://leetcode.com/problems/count-odd-numbers-in-an-interval-range) | Easy | 6 | 0 |
| 991 | [Maximum Score of Non-overlapping Intervals](https://leetcode.com/problems/maximum-score-of-non-overlapping-intervals) | Hard | 5 | 3 |
| 1131 | [Remove Covered Intervals](https://leetcode.com/problems/remove-covered-intervals) | Medium | 5 | 0 |
| 1143 | [Image Overlap](https://leetcode.com/problems/image-overlap) | Medium | 5 | 5 |
| 1267 | [Count Integers in Intervals](https://leetcode.com/problems/count-integers-in-intervals) | Hard | 4 | 0 |
| 1482 | [Find Right Interval](https://leetcode.com/problems/find-right-interval) | Medium | 4 | 1 |
| 1483 | [Find Two Non-overlapping Sub-arrays Each With Target Sum](https://leetcode.com/problems/find-two-non-overlapping-sub-arrays-each-with-target-sum) | Medium | 4 | 2 |
| 1549 | [Divide Intervals Into Minimum Number of Groups](https://leetcode.com/problems/divide-intervals-into-minimum-number-of-groups) | Medium | 3 | 0 |
| 1576 | [Longest Well-Performing Interval](https://leetcode.com/problems/longest-well-performing-interval) | Medium | 3 | 0 |
| 1637 | [Maximum Sum of Two Non-Overlapping Subarrays](https://leetcode.com/problems/maximum-sum-of-two-non-overlapping-subarrays) | Medium | 3 | 1 |
| 1724 | [My Calendar II](https://leetcode.com/problems/my-calendar-ii) | Medium | 3 | 0 |

### Greedy

| 总排名 | 题目 | 难度 | 考过的公司数 | 近 3 个月公司数 |
|---:|---|---|---:|---:|
| 55 | [Jump Game](https://leetcode.com/problems/jump-game) | Medium | 31 | 6 |
| 65 | [Jump Game II](https://leetcode.com/problems/jump-game-ii) | Medium | 28 | 3 |
| 66 | [Gas Station](https://leetcode.com/problems/gas-station) | Medium | 27 | 4 |
| 69 | [Best Time to Buy and Sell Stock II](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii) | Medium | 26 | 5 |
| 138 | [Largest Number](https://leetcode.com/problems/largest-number) | Medium | 17 | 6 |
| 146 | [Candy](https://leetcode.com/problems/candy) | Hard | 17 | 4 |
| 209 | [Can Place Flowers](https://leetcode.com/problems/can-place-flowers) | Easy | 14 | 4 |
| 382 | [Maximum Swap](https://leetcode.com/problems/maximum-swap) | Medium | 9 | 1 |
| 440 | [Rabbits in Forest](https://leetcode.com/problems/rabbits-in-forest) | Medium | 8 | 0 |
| 473 | [Lemonade Change](https://leetcode.com/problems/lemonade-change) | Easy | 8 | 1 |
| 510 | [Maximum Units on a Truck](https://leetcode.com/problems/maximum-units-on-a-truck) | Easy | 8 | 1 |
| 513 | [Rearranging Fruits](https://leetcode.com/problems/rearranging-fruits) | Hard | 8 | 0 |
| 518 | [Maximum Palindromes After Operations](https://leetcode.com/problems/maximum-palindromes-after-operations) | Medium | 7 | 0 |
| 562 | [Longest Palindrome](https://leetcode.com/problems/longest-palindrome) | Easy | 7 | 1 |
| 570 | [Maximum 69 Number](https://leetcode.com/problems/maximum-69-number) | Easy | 7 | 0 |
| 620 | [Two City Scheduling](https://leetcode.com/problems/two-city-scheduling) | Medium | 7 | 2 |
| 629 | [Cinema Seat Allocation](https://leetcode.com/problems/cinema-seat-allocation) | Medium | 7 | 3 |
| 696 | [Minimum Replacements to Sort the Array](https://leetcode.com/problems/minimum-replacements-to-sort-the-array) | Hard | 6 | 0 |
| 706 | [Increasing Triplet Subsequence](https://leetcode.com/problems/increasing-triplet-subsequence) | Medium | 6 | 0 |
| 718 | [Max Difference You Can Get From Changing an Integer](https://leetcode.com/problems/max-difference-you-can-get-from-changing-an-integer) | Medium | 6 | 0 |
| 729 | [Broken Calculator](https://leetcode.com/problems/broken-calculator) | Medium | 6 | 0 |
| 738 | [Minimum Initial Energy to Finish Tasks](https://leetcode.com/problems/minimum-initial-energy-to-finish-tasks) | Hard | 6 | 0 |
| 771 | [Least Number of Unique Integers after K Removals](https://leetcode.com/problems/least-number-of-unique-integers-after-k-removals) | Medium | 6 | 0 |
| 786 | [Minimum Cost to Move Chips to The Same Position](https://leetcode.com/problems/minimum-cost-to-move-chips-to-the-same-position) | Easy | 6 | 1 |
| 791 | [Minimum Operations to Make the Array Increasing](https://leetcode.com/problems/minimum-operations-to-make-the-array-increasing) | Easy | 6 | 1 |

### Array / String Basics

| 总排名 | 题目 | 难度 | 考过的公司数 | 近 3 个月公司数 |
|---:|---|---|---:|---:|
| 12 | [Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix) | Easy | 52 | 8 |
| 113 | [String to Integer (atoi)](https://leetcode.com/problems/string-to-integer-atoi) | Medium | 19 | 2 |
| 153 | [Zigzag Conversion](https://leetcode.com/problems/zigzag-conversion) | Medium | 16 | 5 |
| 220 | [Max Consecutive Ones](https://leetcode.com/problems/max-consecutive-ones) | Easy | 13 | 5 |
| 281 | [Validate IP Address](https://leetcode.com/problems/validate-ip-address) | Medium | 11 | 2 |
| 288 | [Rotate String](https://leetcode.com/problems/rotate-string) | Easy | 11 | 5 |
| 320 | [Maximize Distance to Closest Person](https://leetcode.com/problems/maximize-distance-to-closest-person) | Medium | 10 | 2 |
| 327 | [Count and Say](https://leetcode.com/problems/count-and-say) | Medium | 10 | 2 |
| 366 | [Shortest Word Distance](https://leetcode.com/problems/shortest-word-distance) | Easy | 9 | 0 |
| 370 | [Check if Array Is Sorted and Rotated](https://leetcode.com/problems/check-if-array-is-sorted-and-rotated) | Easy | 9 | 2 |
| 374 | [Summary Ranges](https://leetcode.com/problems/summary-ranges) | Easy | 9 | 1 |
| 386 | [Shortest Palindrome](https://leetcode.com/problems/shortest-palindrome) | Hard | 9 | 2 |
| 436 | [Valid Number](https://leetcode.com/problems/valid-number) | Hard | 8 | 1 |
| 475 | [Repeated Substring Pattern](https://leetcode.com/problems/repeated-substring-pattern) | Easy | 8 | 0 |
| 477 | [Valid Word](https://leetcode.com/problems/valid-word) | Easy | 8 | 0 |
| 483 | [Cache With Time Limit](https://leetcode.com/problems/cache-with-time-limit) | Medium | 8 | 0 |
| 522 | [Create Hello World Function](https://leetcode.com/problems/create-hello-world-function) | Easy | 7 | 2 |
| 549 | [Number of Adjacent Elements With the Same Color](https://leetcode.com/problems/number-of-adjacent-elements-with-the-same-color) | Medium | 7 | 0 |
| 553 | [Flatten Deeply Nested Array](https://leetcode.com/problems/flatten-deeply-nested-array) | Medium | 7 | 0 |
| 601 | [Longest Strictly Increasing or Strictly Decreasing Subarray](https://leetcode.com/problems/longest-strictly-increasing-or-strictly-decreasing-subarray) | Easy | 7 | 1 |
| 621 | [Defanging an IP Address](https://leetcode.com/problems/defanging-an-ip-address) | Easy | 7 | 1 |
| 654 | [Find the Original Typed String I](https://leetcode.com/problems/find-the-original-typed-string-i) | Easy | 7 | 0 |
| 675 | [Valid Mountain Array](https://leetcode.com/problems/valid-mountain-array) | Easy | 7 | 0 |
| 703 | [Length of Last Word](https://leetcode.com/problems/length-of-last-word) | Easy | 6 | 3 |
| 726 | [Monotonic Array](https://leetcode.com/problems/monotonic-array) | Easy | 6 | 0 |

### Math

| 总排名 | 题目 | 难度 | 考过的公司数 | 近 3 个月公司数 |
|---:|---|---|---:|---:|
| 56 | [Palindrome Number](https://leetcode.com/problems/palindrome-number) | Easy | 30 | 6 |
| 101 | [Pow(x, n)](https://leetcode.com/problems/powx-n) | Medium | 21 | 2 |
| 125 | [Integer to English Words](https://leetcode.com/problems/integer-to-english-words) | Hard | 19 | 1 |
| 200 | [Reverse Integer](https://leetcode.com/problems/reverse-integer) | Medium | 14 | 6 |
| 211 | [Count Primes](https://leetcode.com/problems/count-primes) | Medium | 14 | 2 |
| 292 | [Angle Between Hands of a Clock](https://leetcode.com/problems/angle-between-hands-of-a-clock) | Medium | 11 | 0 |
| 311 | [Reaching Points](https://leetcode.com/problems/reaching-points) | Hard | 10 | 0 |
| 312 | [Plus One](https://leetcode.com/problems/plus-one) | Easy | 10 | 4 |
| 336 | [Excel Sheet Column Title](https://leetcode.com/problems/excel-sheet-column-title) | Easy | 10 | 1 |
| 407 | [Minimum Moves to Equal Array Elements](https://leetcode.com/problems/minimum-moves-to-equal-array-elements) | Medium | 9 | 1 |
| 418 | [Guess the Word](https://leetcode.com/problems/guess-the-word) | Hard | 9 | 1 |
| 429 | [Rectangle Area](https://leetcode.com/problems/rectangle-area) | Medium | 9 | 0 |
| 435 | [Permutation Sequence](https://leetcode.com/problems/permutation-sequence) | Hard | 8 | 2 |
| 437 | [Add Two Integers](https://leetcode.com/problems/add-two-integers) | Easy | 8 | 2 |
| 499 | [Bulb Switcher](https://leetcode.com/problems/bulb-switcher) | Medium | 8 | 2 |
| 579 | [Consecutive Numbers Sum](https://leetcode.com/problems/consecutive-numbers-sum) | Hard | 7 | 2 |
| 591 | [Count Good Numbers](https://leetcode.com/problems/count-good-numbers) | Medium | 7 | 1 |
| 595 | [Find Numbers with Even Number of Digits](https://leetcode.com/problems/find-numbers-with-even-number-of-digits) | Easy | 7 | 0 |
| 622 | [Ugly Number](https://leetcode.com/problems/ugly-number) | Easy | 7 | 2 |
| 630 | [Nim Game](https://leetcode.com/problems/nim-game) | Easy | 7 | 1 |
| 631 | [Power of Three](https://leetcode.com/problems/power-of-three) | Easy | 7 | 2 |
| 660 | [Subtract the Product and Sum of Digits of an Integer](https://leetcode.com/problems/subtract-the-product-and-sum-of-digits-of-an-integer) | Easy | 7 | 0 |
| 690 | [Count the Number of Infection Sequences](https://leetcode.com/problems/count-the-number-of-infection-sequences) | Hard | 6 | 0 |
| 740 | [Excel Sheet Column Number](https://leetcode.com/problems/excel-sheet-column-number) | Easy | 6 | 2 |
| 758 | [Greatest Common Divisor of Strings](https://leetcode.com/problems/greatest-common-divisor-of-strings) | Easy | 6 | 2 |

### Prefix Sum

| 总排名 | 题目 | 难度 | 考过的公司数 | 近 3 个月公司数 |
|---:|---|---|---:|---:|
| 26 | [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k) | Medium | 40 | 6 |
| 57 | [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self) | Medium | 30 | 5 |
| 185 | [Find Pivot Index](https://leetcode.com/problems/find-pivot-index) | Easy | 15 | 2 |
| 212 | [Contiguous Array](https://leetcode.com/problems/contiguous-array) | Medium | 14 | 4 |
| 305 | [Minimum Value to Get Positive Step by Step Sum](https://leetcode.com/problems/minimum-value-to-get-positive-step-by-step-sum) | Easy | 11 | 0 |
| 358 | [Continuous Subarray Sum](https://leetcode.com/problems/continuous-subarray-sum) | Medium | 10 | 3 |
| 394 | [Count Vowel Strings in Ranges](https://leetcode.com/problems/count-vowel-strings-in-ranges) | Medium | 9 | 0 |
| 397 | [Subarray Sums Divisible by K](https://leetcode.com/problems/subarray-sums-divisible-by-k) | Medium | 9 | 3 |
| 500 | [Find the Highest Altitude](https://leetcode.com/problems/find-the-highest-altitude) | Easy | 8 | 0 |
| 521 | [Ways to Make a Fair Array](https://leetcode.com/problems/ways-to-make-a-fair-array) | Medium | 7 | 1 |
| 523 | [Brightest Position on Street](https://leetcode.com/problems/brightest-position-on-street) | Medium | 7 | 1 |
| 682 | [Maximum Size Subarray Sum Equals k](https://leetcode.com/problems/maximum-size-subarray-sum-equals-k) | Medium | 7 | 0 |
| 715 | [Running Sum of 1d Array](https://leetcode.com/problems/running-sum-of-1d-array) | Easy | 6 | 4 |
| 723 | [Count the Hidden Sequences](https://leetcode.com/problems/count-the-hidden-sequences) | Medium | 6 | 0 |
| 743 | [Shifting Letters II](https://leetcode.com/problems/shifting-letters-ii) | Medium | 6 | 0 |
| 799 | [Range Product Queries of Powers](https://leetcode.com/problems/range-product-queries-of-powers) | Medium | 6 | 0 |
| 815 | [Minimum Moves to Make Array Complementary](https://leetcode.com/problems/minimum-moves-to-make-array-complementary) | Medium | 6 | 0 |
| 823 | [Minimum Penalty for a Shop](https://leetcode.com/problems/minimum-penalty-for-a-shop) | Medium | 6 | 0 |
| 836 | [Unique Length-3 Palindromic Subsequences](https://leetcode.com/problems/unique-length-3-palindromic-subsequences) | Medium | 6 | 0 |
| 843 | [Sum of Distances](https://leetcode.com/problems/sum-of-distances) | Medium | 6 | 1 |
| 854 | [Make Sum Divisible by P](https://leetcode.com/problems/make-sum-divisible-by-p) | Medium | 6 | 1 |
| 865 | [Maximum Population Year](https://leetcode.com/problems/maximum-population-year) | Easy | 6 | 0 |
| 873 | [Find the Minimum Amount of Time to Brew Potions](https://leetcode.com/problems/find-the-minimum-amount-of-time-to-brew-potions) | Medium | 6 | 0 |
| 893 | [Longest Balanced Substring II](https://leetcode.com/problems/longest-balanced-substring-ii) | Medium | 6 | 0 |
| 904 | [Maximum Good Subarray Sum](https://leetcode.com/problems/maximum-good-subarray-sum) | Medium | 5 | 1 |

### SQL / Database

| 总排名 | 题目 | 难度 | 考过的公司数 | 近 3 个月公司数 |
|---:|---|---|---:|---:|
| 127 | [Second Highest Salary](https://leetcode.com/problems/second-highest-salary) | Medium | 18 | 9 |
| 239 | [Department Top Three Salaries](https://leetcode.com/problems/department-top-three-salaries) | Hard | 13 | 0 |
| 258 | [Employees Earning More Than Their Managers](https://leetcode.com/problems/employees-earning-more-than-their-managers) | Easy | 12 | 2 |
| 287 | [Rising Temperature](https://leetcode.com/problems/rising-temperature) | Easy | 11 | 4 |
| 383 | [Article Views I](https://leetcode.com/problems/article-views-i) | Easy | 9 | 4 |
| 411 | [Delete Duplicate Emails](https://leetcode.com/problems/delete-duplicate-emails) | Easy | 9 | 1 |
| 438 | [Combine Two Tables](https://leetcode.com/problems/combine-two-tables) | Easy | 8 | 4 |
| 447 | [Replace Employee ID With The Unique Identifier](https://leetcode.com/problems/replace-employee-id-with-the-unique-identifier) | Easy | 8 | 0 |
| 450 | [Exchange Seats](https://leetcode.com/problems/exchange-seats) | Medium | 8 | 0 |
| 460 | [Consecutive Numbers](https://leetcode.com/problems/consecutive-numbers) | Medium | 8 | 3 |
| 479 | [Nth Highest Salary](https://leetcode.com/problems/nth-highest-salary) | Medium | 8 | 1 |
| 530 | [Average Time of Process per Machine](https://leetcode.com/problems/average-time-of-process-per-machine) | Easy | 7 | 3 |
| 538 | [Invalid Tweets](https://leetcode.com/problems/invalid-tweets) | Easy | 7 | 2 |
| 539 | [Employee Bonus](https://leetcode.com/problems/employee-bonus) | Easy | 7 | 2 |
| 542 | [Students and Examinations](https://leetcode.com/problems/students-and-examinations) | Easy | 7 | 2 |
| 551 | [Managers with at Least 5 Direct Reports](https://leetcode.com/problems/managers-with-at-least-5-direct-reports) | Medium | 7 | 1 |
| 566 | [Restaurant Growth](https://leetcode.com/problems/restaurant-growth) | Medium | 7 | 2 |
| 568 | [Game Play Analysis IV](https://leetcode.com/problems/game-play-analysis-iv) | Medium | 7 | 3 |
| 572 | [Customers Who Never Order](https://leetcode.com/problems/customers-who-never-order) | Easy | 7 | 3 |
| 575 | [Immediate Food Delivery II](https://leetcode.com/problems/immediate-food-delivery-ii) | Medium | 7 | 1 |
| 578 | [Find Customer Referee](https://leetcode.com/problems/find-customer-referee) | Easy | 7 | 3 |
| 580 | [Duplicate Emails](https://leetcode.com/problems/duplicate-emails) | Easy | 7 | 2 |
| 593 | [Rank Scores](https://leetcode.com/problems/rank-scores) | Medium | 7 | 1 |
| 606 | [Movie Rating](https://leetcode.com/problems/movie-rating) | Medium | 7 | 0 |
| 611 | [Product Price at a Given Date](https://leetcode.com/problems/product-price-at-a-given-date) | Medium | 7 | 1 |

### Union-Find

| 总排名 | 题目 | 难度 | 考过的公司数 | 近 3 个月公司数 |
|---:|---|---|---:|---:|
| 106 | [Evaluate Division](https://leetcode.com/problems/evaluate-division) | Medium | 20 | 2 |
| 150 | [Accounts Merge](https://leetcode.com/problems/accounts-merge) | Medium | 17 | 2 |
| 222 | [Minimize Malware Spread](https://leetcode.com/problems/minimize-malware-spread) | Hard | 13 | 4 |
| 303 | [Possible Bipartition](https://leetcode.com/problems/possible-bipartition) | Medium | 11 | 0 |
| 340 | [Min Cost to Connect All Points](https://leetcode.com/problems/min-cost-to-connect-all-points) | Medium | 10 | 1 |
| 354 | [Number of Operations to Make Network Connected](https://leetcode.com/problems/number-of-operations-to-make-network-connected) | Medium | 10 | 0 |
| 361 | [Is Graph Bipartite?](https://leetcode.com/problems/is-graph-bipartite) | Medium | 10 | 1 |
| 364 | [Make Lexicographically Smallest Array by Swapping Elements](https://leetcode.com/problems/make-lexicographically-smallest-array-by-swapping-elements) | Medium | 10 | 5 |
| 375 | [Number of Provinces](https://leetcode.com/problems/number-of-provinces) | Medium | 9 | 3 |
| 400 | [Most Stones Removed with Same Row or Column](https://leetcode.com/problems/most-stones-removed-with-same-row-or-column) | Medium | 9 | 2 |
| 469 | [Smallest String With Swaps](https://leetcode.com/problems/smallest-string-with-swaps) | Medium | 8 | 1 |
| 471 | [Couples Holding Hands](https://leetcode.com/problems/couples-holding-hands) | Hard | 8 | 1 |
| 528 | [Number of Connected Components in an Undirected Graph](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph) | Medium | 7 | 0 |
| 555 | [Graph Valid Tree](https://leetcode.com/problems/graph-valid-tree) | Medium | 7 | 0 |
| 588 | [Power Grid Maintenance](https://leetcode.com/problems/power-grid-maintenance) | Medium | 7 | 0 |
| 600 | [Redundant Connection](https://leetcode.com/problems/redundant-connection) | Medium | 7 | 1 |
| 697 | [Number of Islands II](https://leetcode.com/problems/number-of-islands-ii) | Hard | 6 | 1 |
| 783 | [Minimum Cost Walk in Weighted Graph](https://leetcode.com/problems/minimum-cost-walk-in-weighted-graph) | Hard | 6 | 0 |
| 864 | [Divide Nodes Into the Maximum Number of Groups](https://leetcode.com/problems/divide-nodes-into-the-maximum-number-of-groups) | Hard | 6 | 0 |
| 916 | [Satisfiability of Equality Equations](https://leetcode.com/problems/satisfiability-of-equality-equations) | Medium | 5 | 2 |
| 973 | [Find if Path Exists in Graph](https://leetcode.com/problems/find-if-path-exists-in-graph) | Easy | 5 | 1 |
| 1135 | [Path Existence Queries in a Graph I](https://leetcode.com/problems/path-existence-queries-in-a-graph-i) | Medium | 5 | 1 |
| 1326 | [Count Unreachable Pairs of Nodes in an Undirected Graph](https://leetcode.com/problems/count-unreachable-pairs-of-nodes-in-an-undirected-graph) | Medium | 4 | 0 |
| 1330 | [Remove Max Number of Edges to Keep Graph Fully Traversable](https://leetcode.com/problems/remove-max-number-of-edges-to-keep-graph-fully-traversable) | Hard | 4 | 0 |
| 1345 | [Minimize Maximum Component Cost](https://leetcode.com/problems/minimize-maximum-component-cost) | Medium | 4 | 0 |

### Bit Manipulation

| 总排名 | 题目 | 难度 | 考过的公司数 | 近 3 个月公司数 |
|---:|---|---|---:|---:|
| 141 | [Single Number](https://leetcode.com/problems/single-number) | Easy | 17 | 5 |
| 166 | [Missing Number](https://leetcode.com/problems/missing-number) | Easy | 16 | 2 |
| 170 | [Add Binary](https://leetcode.com/problems/add-binary) | Easy | 16 | 4 |
| 294 | [Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits) | Easy | 11 | 2 |
| 331 | [Power of Two](https://leetcode.com/problems/power-of-two) | Easy | 10 | 4 |
| 338 | [Reverse Bits](https://leetcode.com/problems/reverse-bits) | Easy | 10 | 1 |
| 442 | [Number of Steps to Reduce a Number in Binary Representation to One](https://leetcode.com/problems/number-of-steps-to-reduce-a-number-in-binary-representation-to-one) | Medium | 8 | 0 |
| 452 | [Sum of Two Integers](https://leetcode.com/problems/sum-of-two-integers) | Medium | 8 | 1 |
| 531 | [Divide Two Integers](https://leetcode.com/problems/divide-two-integers) | Medium | 7 | 3 |
| 557 | [Set Mismatch](https://leetcode.com/problems/set-mismatch) | Easy | 7 | 3 |
| 565 | [Power of Four](https://leetcode.com/problems/power-of-four) | Easy | 7 | 0 |
| 599 | [Single Number III](https://leetcode.com/problems/single-number-iii) | Medium | 7 | 0 |
| 664 | [K-th Symbol in Grammar](https://leetcode.com/problems/k-th-symbol-in-grammar) | Medium | 7 | 0 |
| 730 | [Binary Gap](https://leetcode.com/problems/binary-gap) | Easy | 6 | 0 |
| 769 | [Find the Difference](https://leetcode.com/problems/find-the-difference) | Easy | 6 | 2 |
| 788 | [Number of Steps to Reduce a Number to Zero](https://leetcode.com/problems/number-of-steps-to-reduce-a-number-to-zero) | Easy | 6 | 1 |
| 828 | [Find the Prefix Common Array of Two Arrays](https://leetcode.com/problems/find-the-prefix-common-array-of-two-arrays) | Medium | 6 | 0 |
| 903 | [IP to CIDR](https://leetcode.com/problems/ip-to-cidr) | Medium | 5 | 0 |
| 929 | [Single Number II](https://leetcode.com/problems/single-number-ii) | Medium | 5 | 2 |
| 941 | [Complement of Base 10 Integer](https://leetcode.com/problems/complement-of-base-10-integer) | Easy | 5 | 0 |
| 1006 | [Construct the Minimum Bitwise Array I](https://leetcode.com/problems/construct-the-minimum-bitwise-array-i) | Easy | 5 | 0 |
| 1013 | [Longest Subarray With Maximum Bitwise AND](https://leetcode.com/problems/longest-subarray-with-maximum-bitwise-and) | Medium | 5 | 0 |
| 1037 | [Check If a String Contains All Binary Codes of Size K](https://leetcode.com/problems/check-if-a-string-contains-all-binary-codes-of-size-k) | Medium | 5 | 0 |
| 1080 | [Find the K-th Character in String Game I](https://leetcode.com/problems/find-the-k-th-character-in-string-game-i) | Easy | 5 | 0 |
| 1124 | [Convert a Number to Hexadecimal](https://leetcode.com/problems/convert-a-number-to-hexadecimal) | Easy | 5 | 0 |

### Trie

| 总排名 | 题目 | 难度 | 考过的公司数 | 近 3 个月公司数 |
|---:|---|---|---:|---:|
| 109 | [Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree) | Medium | 20 | 4 |
| 117 | [Word Search II](https://leetcode.com/problems/word-search-ii) | Hard | 19 | 1 |
| 142 | [Search Suggestions System](https://leetcode.com/problems/search-suggestions-system) | Medium | 17 | 1 |
| 216 | [Design In-Memory File System](https://leetcode.com/problems/design-in-memory-file-system) | Hard | 13 | 1 |
| 244 | [Find the Length of the Longest Common Prefix](https://leetcode.com/problems/find-the-length-of-the-longest-common-prefix) | Medium | 12 | 0 |
| 267 | [Design Search Autocomplete System](https://leetcode.com/problems/design-search-autocomplete-system) | Hard | 12 | 0 |
| 273 | [Design Add and Search Words Data Structure](https://leetcode.com/problems/design-add-and-search-words-data-structure) | Medium | 12 | 1 |
| 352 | [Design File System](https://leetcode.com/problems/design-file-system) | Medium | 10 | 0 |
| 466 | [Remove Sub-Folders from the Filesystem](https://leetcode.com/problems/remove-sub-folders-from-the-filesystem) | Medium | 8 | 0 |
| 604 | [Palindrome Pairs](https://leetcode.com/problems/palindrome-pairs) | Hard | 7 | 0 |
| 663 | [Number of Matching Subsequences](https://leetcode.com/problems/number-of-matching-subsequences) | Medium | 7 | 0 |
| 727 | [K-th Smallest in Lexicographical Order](https://leetcode.com/problems/k-th-smallest-in-lexicographical-order) | Hard | 6 | 0 |
| 842 | [Delete Duplicate Folders in System](https://leetcode.com/problems/delete-duplicate-folders-in-system) | Hard | 6 | 0 |
| 1048 | [Lexicographical Numbers](https://leetcode.com/problems/lexicographical-numbers) | Medium | 5 | 0 |
| 1065 | [Maximum XOR of Two Numbers in an Array](https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array) | Medium | 5 | 2 |
| 1200 | [Number of Distinct Substrings in a String](https://leetcode.com/problems/number-of-distinct-substrings-in-a-string) | Medium | 4 | 0 |
| 1222 | [Word Abbreviation](https://leetcode.com/problems/word-abbreviation) | Hard | 4 | 0 |
| 1233 | [Count Prefix and Suffix Pairs I](https://leetcode.com/problems/count-prefix-and-suffix-pairs-i) | Easy | 4 | 0 |
| 1239 | [Add Bold Tag in String](https://leetcode.com/problems/add-bold-tag-in-string) | Medium | 4 | 0 |
| 1258 | [Replace Words](https://leetcode.com/problems/replace-words) | Medium | 4 | 0 |
| 1341 | [Stream of Characters](https://leetcode.com/problems/stream-of-characters) | Hard | 4 | 0 |
| 1380 | [Minimum Cost to Convert String II](https://leetcode.com/problems/minimum-cost-to-convert-string-ii) | Hard | 4 | 0 |
| 1410 | [Words Within Two Edits of Dictionary](https://leetcode.com/problems/words-within-two-edits-of-dictionary) | Medium | 4 | 0 |
| 1532 | [Shortest Uncommon Substring in an Array](https://leetcode.com/problems/shortest-uncommon-substring-in-an-array) | Medium | 3 | 0 |
| 1546 | [Count Prefix and Suffix Pairs II](https://leetcode.com/problems/count-prefix-and-suffix-pairs-ii) | Hard | 3 | 0 |

### Sorting

| 总排名 | 题目 | 难度 | 考过的公司数 | 近 3 个月公司数 |
|---:|---|---|---:|---:|
| 155 | [Minimum Absolute Difference](https://leetcode.com/problems/minimum-absolute-difference) | Easy | 16 | 2 |
| 278 | [Special Binary String](https://leetcode.com/problems/special-binary-string) | Hard | 11 | 0 |
| 384 | [Maximum Product of Three Numbers](https://leetcode.com/problems/maximum-product-of-three-numbers) | Easy | 9 | 2 |
| 426 | [Third Maximum Number](https://leetcode.com/problems/third-maximum-number) | Easy | 9 | 0 |
| 624 | [H-Index](https://leetcode.com/problems/h-index) | Medium | 7 | 1 |
| 669 | [Height Checker](https://leetcode.com/problems/height-checker) | Easy | 7 | 0 |
| 778 | [Minimum Time Difference](https://leetcode.com/problems/minimum-time-difference) | Medium | 6 | 0 |
| 781 | [Can Make Arithmetic Progression From Sequence](https://leetcode.com/problems/can-make-arithmetic-progression-from-sequence) | Easy | 6 | 2 |
| 789 | [Divide an Array Into Subarrays With Minimum Cost I](https://leetcode.com/problems/divide-an-array-into-subarrays-with-minimum-cost-i) | Easy | 6 | 0 |
| 802 | [Queue Reconstruction by Height](https://leetcode.com/problems/queue-reconstruction-by-height) | Medium | 6 | 0 |
| 833 | [Maximum Building Height](https://leetcode.com/problems/maximum-building-height) | Hard | 6 | 0 |
| 989 | [Maximum Gap](https://leetcode.com/problems/maximum-gap) | Medium | 5 | 1 |
| 1004 | [Minimum Moves to Equal Array Elements II](https://leetcode.com/problems/minimum-moves-to-equal-array-elements-ii) | Medium | 5 | 0 |
| 1021 | [Type of Triangle](https://leetcode.com/problems/type-of-triangle) | Easy | 5 | 0 |
| 1027 | [Count Days Without Meetings](https://leetcode.com/problems/count-days-without-meetings) | Medium | 5 | 1 |
| 1121 | [Sort Vowels in a String](https://leetcode.com/problems/sort-vowels-in-a-string) | Medium | 5 | 0 |
| 1156 | [Smallest Palindromic Rearrangement I](https://leetcode.com/problems/smallest-palindromic-rearrangement-i) | Medium | 5 | 1 |
| 1279 | [Maximize Area of Square Hole in Grid](https://leetcode.com/problems/maximize-area-of-square-hole-in-grid) | Medium | 4 | 0 |
| 1371 | [Largest Number At Least Twice of Others](https://leetcode.com/problems/largest-number-at-least-twice-of-others) | Easy | 4 | 0 |
| 1465 | [Find the Number of Ways to Place People I](https://leetcode.com/problems/find-the-number-of-ways-to-place-people-i) | Medium | 4 | 0 |
| 1492 | [Maximum Product of Two Digits](https://leetcode.com/problems/maximum-product-of-two-digits) | Easy | 4 | 1 |
| 1656 | [Sort Even and Odd Indices Independently](https://leetcode.com/problems/sort-even-and-odd-indices-independently) | Easy | 3 | 0 |
| 1745 | [Check if Grid can be Cut into Sections](https://leetcode.com/problems/check-if-grid-can-be-cut-into-sections) | Medium | 3 | 0 |
| 1765 | [Widest Vertical Area Between Two Points Containing No Points](https://leetcode.com/problems/widest-vertical-area-between-two-points-containing-no-points) | Easy | 3 | 0 |
| 1778 | [Reorder Data in Log Files](https://leetcode.com/problems/reorder-data-in-log-files) | Medium | 3 | 0 |

### Concurrency

| 总排名 | 题目 | 难度 | 考过的公司数 | 近 3 个月公司数 |
|---:|---|---|---:|---:|
| 689 | [Web Crawler Multithreaded](https://leetcode.com/problems/web-crawler-multithreaded) | Medium | 6 | 0 |
| 947 | [Building H2O](https://leetcode.com/problems/building-h2o) | Medium | 5 | 0 |
| 1692 | [Design Bounded Blocking Queue](https://leetcode.com/problems/design-bounded-blocking-queue) | Medium | 3 | 0 |
| 1722 | [Fizz Buzz Multithreaded](https://leetcode.com/problems/fizz-buzz-multithreaded) | Medium | 3 | 0 |
| 1842 | [The Dining Philosophers](https://leetcode.com/problems/the-dining-philosophers) | Medium | 3 | 0 |
| 2106 | [Print in Order](https://leetcode.com/problems/print-in-order) | Easy | 2 | 0 |
| 2128 | [Print Zero Even Odd](https://leetcode.com/problems/print-zero-even-odd) | Medium | 2 | 0 |
