"""13 · Backtracking: 生成 docs/13-backtracking.html 和 docs/svg/13-backtracking/*.svg
运行: cd build && python3 -I 13_backtracking.py
所有展示的代码都在本文件里被 exec 并对照暴力解测试; trace 图的数字来自带记录的同逻辑版本。
"""
import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT_DIR = os.path.dirname(HERE)
import doclib as d

