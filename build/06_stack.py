"""06 · Stack 生成脚本。
运行: cd build && python3 -I 06_stack.py
做三件事:
  1. 把文档里展示的每段代码 exec 一遍并 assert (代码和测试是同一份字符串)
  2. 用带记录的模拟器跑 trace 例子, 生成 docs/svg/06-stack/*.svg (数字全部来自实际运行)
  3. 生成 docs/06-stack.html
"""
import html
import os
import random
import re
import posixpath
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import doclib as d  # noqa: E402

SLUG = "06-stack"
SVG_DIR = os.path.join(d.ROOT, "docs", "svg", SLUG)
os.makedirs(SVG_DIR, exist_ok=True)

# ---------------------------------------------------------------- 代码 (展示 + 测试)

CODE = {}
CODE["match_brute"] = '''
def match_brute(s):                      # O(n^2): 每个 ')' 都往左扫, 找最近的、还没被用掉的 '('
    used, pairs = set(), []
    for j, ch in enumerate(s):
        if ch == ')':
            for i in range(j - 1, -1, -1):           # 往左扫 —— 每个 ')' 都重扫一遍
                if s[i] == '(' and i not in used:
                    used.add(i)
                    pairs.append((i, j))
                    break
    return pairs
'''
CODE["match_stack"] = '''
def match_stack(s):                      # O(n): 栈 = "往左扫会依次碰到的候选", 已经按"最近优先"排好
    stack, pairs = [], []
    for j, ch in enumerate(s):
        if ch == '(':
            stack.append(j)              # 还没被匹配的 '(' 入栈, 栈顶 = 最近的
        elif ch == ')' and stack:
            pairs.append((stack.pop(), j))   # pop = 最近的、没被用掉的 '(' , O(1), 不用扫
    return pairs
'''
CODE["valid"] = '''
def is_valid(s):
    pair = {')': '(', ']': '[', '}': '{'}
    stack = []                           # invariant: 从底到顶 = 还没闭合的开括号, 栈顶是最内层的
    for ch in s:
        if ch in pair:                   # 闭括号: 只能和"最近一个没闭合的开括号"配对
            if not stack or stack.pop() != pair[ch]:   # 栈空 = 多余的闭括号; pop 出来不对 = 交叉
                return False
        else:
            stack.append(ch)             # 开括号: 先存着, 等后面的闭括号来找它
    return not stack                     # 结尾栈非空 = 有开括号一直没被闭合
'''
CODE["minstack"] = '''
class MinStack:
    def __init__(self):
        self.stack = []                  # 每个元素 (val, min_so_far): min_so_far = 从栈底到它自己的最小值

    def push(self, val):
        cur_min = min(val, self.stack[-1][1]) if self.stack else val   # 只看下面的元素, 写入后永不改变
        self.stack.append((val, cur_min))

    def pop(self):
        self.stack.pop()                 # min_so_far 跟着元素一起走; 新栈顶的 min_so_far 本来就是对的

    def top(self):
        return self.stack[-1][0]

    def get_min(self):
        return self.stack[-1][1]         # O(1): 不用扫整个栈
'''
CODE["decode"] = '''
def decode_string(s):
    stack = []                           # 每层存 (prev_str, k): 进入 '[' 之前外层拼好的字符串, 和这个 '[' 的重复次数
    cur, num = "", 0                     # cur = 当前这层 [] 里已经拼出的字符串; num = 正在读的数字
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)     # 多位数 "12[a]"
        elif ch == '[':
            stack.append((cur, num))     # 保存外层现场
            cur, num = "", 0             # 进入内层: 从空字符串重新拼
        elif ch == ']':
            prev_str, k = stack.pop()    # 回到外层
            cur = prev_str + cur * k     # 内层拼好的 cur 重复 k 次, 接在外层字符串后面
        else:
            cur += ch
    return cur
'''
CODE["rpn"] = '''
def eval_rpn(tokens):
    stack = []                           # invariant: 栈里 = 已经算出来的操作数, 栈顶是最近算出的
    for t in tokens:
        if t in ("+", "-", "*", "/"):    # 运算符: 它的两个操作数一定是栈顶两个
            b = stack.pop()              # 先 pop 出来的是右操作数
            a = stack.pop()              # 再 pop 出来的是左操作数
            if t == "+": stack.append(a + b)
            elif t == "-": stack.append(a - b)          # 顺序: a - b, 不是 b - a
            elif t == "*": stack.append(a * b)
            else: stack.append(int(a / b))              # 向 0 取整; 不能用 // (负数会向下取整)
        else:
            stack.append(int(t))         # 数字: 先存着, 等运算符来取
    return stack[0]
'''
CODE["calc2"] = '''
def calculate(s):
    stack, num, op = [], 0, '+'          # op = num 前面的运算符; 要等 num 读完 (遇到下一个运算符) 才能处理它
    for i, ch in enumerate(s):
        if ch.isdigit():
            num = num * 10 + int(ch)
        if ch in '+-*/' or i == len(s) - 1:     # 读到下一个运算符 (或到结尾): 处理 "op num"
            if op == '+':   stack.append(num)             # + - 先记成带符号的项, 后面可能有 * / 抢先
            elif op == '-': stack.append(-num)
            elif op == '*': stack.append(stack.pop() * num)          # * / 立即和栈顶那一项合并
            else:           stack.append(int(stack.pop() / num))
            op, num = ch, 0
    return sum(stack)                    # 栈里全是 "项", 最后一次性相加
'''
CODE["calc"] = '''
def calculate(s):
    stack = []
    result, num, sign = 0, 0, 1          # result = 当前括号层已累加的值; sign = num 前面的符号 (+1 / -1)
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch in '+-':
            result += sign * num         # 把刚读完的 num 并进 result
            num, sign = 0, (1 if ch == '+' else -1)
        elif ch == '(':
            stack.append((result, sign)) # 保存外层: 外层累加到哪了, 以及 '(' 前面的符号
            result, sign = 0, 1          # 括号内部从 0 重新算
        elif ch == ')':
            result += sign * num         # 先把括号内最后一个 num 并进来
            num = 0
            prev_result, prev_sign = stack.pop()
            result = prev_result + prev_sign * result   # 整个括号当成一个数, 乘上 '(' 前面的符号
    return result + sign * num
'''
CODE["asteroid"] = '''
def asteroid_collision(asteroids):
    stack = []                           # invariant: 栈里没有会相撞的一对 (栈顶向右 + 下一个向左)
    for a in asteroids:
        alive = True
        while alive and a < 0 and stack and stack[-1] > 0:   # 只有 "栈顶向右 + 新来的向左" 才会撞
            if stack[-1] < -a:           # 栈顶更小: 栈顶炸掉, 新来的继续去撞下一个
                stack.pop()
            elif stack[-1] == -a:        # 一样大: 同归于尽
                stack.pop()
                alive = False
            else:                        # 栈顶更大: 新来的炸掉
                alive = False
        if alive:
            stack.append(a)
    return stack
'''
CODE["dup2"] = '''
def remove_duplicates(s, k):
    stack = []                           # 每个元素 [char, count]: 栈顶这一段 char 已经连续出现 count 次
    for ch in s:
        if stack and stack[-1][0] == ch:
            stack[-1][1] += 1            # 和栈顶同字符: 这一段变长 (不用回头数)
            if stack[-1][1] == k:        # 凑够 k 个: 整段删掉, 它下面的段自然变成相邻
                stack.pop()
        else:
            stack.append([ch, 1])
    return "".join(c * n for c, n in stack)
'''
CODE["path"] = '''
def simplify_path(path):
    stack = []                           # invariant: 栈 = 当前目录从根到现在的每一层名字
    for part in path.split('/'):         # "//" 会切出空串 ''
        if part == '..':
            if stack:
                stack.pop()              # 回上一层; 已经在根 '/' 就忽略
        elif part and part != '.':       # '' 和 '.' 什么都不做; 其余是目录名
            stack.append(part)
    return '/' + '/'.join(stack)
'''


def _cw(t):
    return sum(1.75 if ord(c) > 0x2E80 else 1 for c in t)


def display(code, limit=78):
    """行太宽的 "代码  # 注释" 把注释挪到代码上一行 (同缩进), 再按宽度折行。只影响展示。"""
    out = []
    for line in code.split("\n"):
        if _cw(line) <= limit or " # " not in line or line.lstrip().startswith("#"):
            out.append(line)
            continue
        i = line.index(" # ")
        codepart, cm = line[:i].rstrip(), line[i + 3:]
        indent = len(line) - len(line.lstrip())
        pad = " " * indent
        buf = ""
        for c in cm:
            if _cw(pad + "# " + buf + c) > limit:
                out.append(pad + "# " + buf)
                buf = ""
            buf += c
        out.append(pad + "# " + buf)
        out.append(codepart)
    return "\n".join(out)


def show(code):
    ns = {}
    exec(display(code), ns)      # 展示版本也必须能 exec
    return display(code)


def load(name):
    ns = {}
    exec(CODE[name], ns)
    return ns


def run_tests():
    # section 0
    mb, ms = load("match_brute")["match_brute"], load("match_stack")["match_stack"]
    rnd = random.Random(1)
    for _ in range(500):
        s = "".join(rnd.choice("()a") for _ in range(rnd.randint(0, 14)))
        assert sorted(mb(s)) == sorted(ms(s)), s
    assert sorted(ms("([{}])".replace("[", "(").replace("{", "(").replace("}", ")").replace("]", ")"))) == [(0, 5), (1, 4), (2, 3)]

    # valid parentheses vs replace-brute
    iv = load("valid")["is_valid"]

    def brute(s):
        while True:
            t = s.replace("()", "").replace("[]", "").replace("{}", "")
            if t == s:
                return s == ""
            s = t
    for _ in range(3000):
        s = "".join(rnd.choice("()[]{}") for _ in range(rnd.randint(0, 10)))
        assert iv(s) == brute(s), s
    assert iv("{[()]}") and not iv("([)]") and not iv("(") and not iv(")")

    # min stack
    MS = load("minstack")["MinStack"]
    for _ in range(300):
        m, ref = MS(), []
        for _ in range(30):
            if ref and rnd.random() < 0.4:
                m.pop(); ref.pop()
            else:
                v = rnd.randint(-5, 5); m.push(v); ref.append(v)
            if ref:
                assert m.get_min() == min(ref) and m.top() == ref[-1]

    # decode
    dec = load("decode")["decode_string"]
    assert dec("3[a2[c]]") == "accaccacc" and dec("3[a]2[bc]") == "aaabcbc" and dec("2[abc]3[cd]ef") == "abcabccdcdcdef"
    assert dec("10[a]") == "a" * 10

    # rpn
    ev = load("rpn")["eval_rpn"]
    assert ev(["2", "1", "+", "3", "*"]) == 9 and ev(["4", "13", "5", "/", "+"]) == 6
    assert ev(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]) == 22
    assert ev(["4", "13", "5", "/", "+", "2", "*"]) == 12
    assert ev(["-7", "2", "/"]) == -3

    # calc II vs eval with // (non-negative operands -> same semantics)
    c2 = load("calc2")["calculate"]
    for _ in range(3000):
        n = rnd.randint(1, 6)
        toks = [str(rnd.randint(1, 20))]
        for _ in range(n):
            toks += [rnd.choice("+-*/"), str(rnd.randint(1, 20))]
        e = "".join(toks)
        e2 = e.replace(" ", "")
        ref = eval(e2.replace("/", "//"))
        assert c2(e) == ref, (e, c2(e), ref)
        # with spaces
        assert c2(" ".join(toks)) == ref
    assert c2("3+2*2") == 7 and c2(" 3/2 ") == 1 and c2(" 3+5 / 2 ") == 5 and c2("3+5*2-6/3") == 11
    assert c2("42") == 42

    # calc
    c1 = load("calc")["calculate"]

    def gen(depth=0):
        r = rnd.random()
        if depth > 2 or r < 0.4:
            return str(rnd.randint(0, 20))
        if r < 0.7:
            return "(" + gen(depth + 1) + ")"
        return gen(depth + 1) + rnd.choice("+-") + gen(depth + 1)
    for _ in range(3000):
        e = gen()
        if rnd.random() < 0.3:
            e = "-" + "(" + e + ")"
        assert c1(e) == eval(e), (e, c1(e), eval(e))
        assert c1(e.replace("+", " + ").replace("-", " - ")) == eval(e)
    assert c1("1-(2+(3-1))") == -3 and c1("(1+(4+5+2)-3)+(6+8)") == 23 and c1("1 + 1") == 2

    # asteroid vs brute simulation
    ac = load("asteroid")["asteroid_collision"]

    def abrute(a):
        a = list(a)
        while True:
            for i in range(len(a) - 1):
                if a[i] > 0 > a[i + 1]:
                    if a[i] > -a[i + 1]:
                        del a[i + 1]
                    elif a[i] < -a[i + 1]:
                        del a[i]
                    else:
                        del a[i:i + 2]
                    break
            else:
                return a
    for _ in range(3000):
        a = [rnd.choice([-1, 1]) * rnd.randint(1, 6) for _ in range(rnd.randint(0, 9))]
        assert ac(a) == abrute(a), a
    assert ac([5, 10, -5]) == [5, 10] and ac([8, -8]) == [] and ac([10, 2, -5]) == [10]
    assert ac([5, 10, -8, -12, 3]) == [-12, 3]

    # dup II vs brute
    rd = load("dup2")["remove_duplicates"]

    def dbrute(s, k):
        while True:
            for i in range(len(s) - k + 1):
                if len(set(s[i:i + k])) == 1:
                    s = s[:i] + s[i + k:]
                    break
            else:
                return s
    for _ in range(3000):
        s = "".join(rnd.choice("abc") for _ in range(rnd.randint(0, 14)))
        k = rnd.randint(2, 4)
        assert rd(s, k) == dbrute(s, k), (s, k)
    assert rd("abbbaac", 3) == "c" and rd("deeedbbcccbbdddd", 3) == dbrute("deeedbbcccbbdddd", 3)

    # simplify path
    sp = load("path")["simplify_path"]
    assert sp("/home/") == "/home" and sp("/../") == "/" and sp("/home//foo/") == "/home/foo"
    assert sp("/a/./b/../../c/") == "/c"
    for _ in range(3000):
        parts = [rnd.choice(["a", "b", "c", ".", "..", "", "d"]) for _ in range(rnd.randint(1, 8))]
        p = "/" + "/".join(parts) + rnd.choice(["", "/"])
        if p.startswith("//"):
            continue
        assert sp(p) == posixpath.normpath(p), (p, sp(p), posixpath.normpath(p))
    print("all code tests passed")


run_tests()

# ---------------------------------------------------------------- SVG 工具

ROLE = {
    "new": ("#E1F5EE", "#0F6E56", "#085041"),
    "gone": ("#FAECE7", "#993C1D", "#712B13"),
    "old": ("#F1EFE8", "#5F5E5A", "#444441"),
}
SUB = "#52514E"
INK = "#0B0B0B"
RING = "#EF9F27"
FONT = 'ui-sans-serif, system-ui, -apple-system, "PingFang SC", sans-serif'
CELL_H = 30


def est_w(t, size):
    return sum(size if ord(c) > 0x2E80 else size * 0.58 for c in t)


class S:
    def __init__(self, name, w=680):
        self.name, self.w = name, w
        self.body = []
        self.boxes = []          # (x0, y0, x1, y1, text) 估算文字框, 用来查重叠
        self.h = 0

    def esc(self, t):
        return html.escape(t, quote=False)

    def text(self, x, y, t, size=12, fill=SUB, anchor="start", weight=400):
        self.body.append(
            '<text x="%s" y="%s" font-size="%d" fill="%s" font-weight="%d" text-anchor="%s" '
            'dominant-baseline="central">%s</text>' % (x, y, size, fill, weight, anchor, self.esc(t)))
        w = est_w(t, size)
        x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w)
        self.boxes.append((x0, y - size / 2, x0 + w, y + size / 2, t))

    def rect(self, x, y, w, h, role="old", rx=4, dashed=False, sw=1):
        f, s, _ = ROLE[role]
        self.body.append(
            '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>'
            % (x, y, w, h, rx, f, s, sw, ' stroke-dasharray="4 3"' if dashed else ""))

    def ring(self, x, y, w, h, rx=6):
        self.body.append(
            '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="none" stroke="%s" stroke-width="2.5"/>'
            % (x - 3, y - 3, w + 6, h + 6, rx, RING))

    def line(self, x1, y1, x2, y2, color="#B4B2A9", dashed=True, sw=1):
        self.body.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s/>'
                         % (x1, y1, x2, y2, color, sw, ' stroke-dasharray="4 4"' if dashed else ""))

    def path(self, dstr, color=SUB, dashed=False, arrow=True, sw=1.5, marker=None):
        m = ""
        if arrow:
            m = ' marker-end="url(#%s)"' % (marker or ("arrR" if color == "#D85A30" else "arr"))
        self.body.append('<path d="%s" fill="none" stroke="%s" stroke-width="%s"%s%s/>'
                         % (dstr, color, sw, ' stroke-dasharray="5 4"' if dashed else "", m))

    def arrow(self, x1, y1, x2, y2, color=SUB, dashed=False):
        self.path("M%s %s L%s %s" % (x1, y1, x2, y2), color, dashed)

    def cell(self, x, y, w, h, label, role="old", size=14, ring=False, dashed=False, weight=500):
        self.rect(x, y, w, h, role, dashed=dashed)
        if ring:
            self.ring(x, y, w, h)
        self.text(x + w / 2, y + h / 2, label, size, ROLE[role][2], "middle", weight)

    def bucket(self, x, bottom, w, cells, cap, top_ring=True, empty=True):
        """竖直的桶: cells 从底到顶 [(label, role)]; cap = 桶能画的格数 (统一高度)"""
        top = bottom - cap * CELL_H - 6
        self.body.append(
            '<path d="M%s %s L%s %s L%s %s L%s %s" fill="none" stroke="#5F5E5A" stroke-width="1.5" '
            'stroke-linejoin="round"/>' % (x, top, x, bottom, x + w, bottom, x + w, top))
        if not cells and empty:
            self.text(x + w / 2, bottom - 14, "空", 12, SUB, "middle")
        for i, (label, role) in enumerate(cells):
            cy = bottom - (i + 1) * CELL_H + 2
            self.cell(x + 8, cy, w - 16, CELL_H - 4, label, role, ring=(top_ring and i == len(cells) - 1))
        return top

    def defs(self):
        def mk(i, c):
            return ('<marker id="%s" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" '
                    'orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="%s" stroke-width="1.5" '
                    'stroke-linecap="round" stroke-linejoin="round"/></marker>' % (i, c))
        return "<defs>%s%s</defs>" % (mk("arr", SUB), mk("arrR", "#D85A30"))

    def legend(self, y, items):
        x = 40
        for kind, label in items:
            if kind == "ring":
                self.body.append('<rect x="%s" y="%s" width="14" height="14" rx="3" fill="#F1EFE8" stroke="#5F5E5A" '
                                 'stroke-width="1"/><rect x="%s" y="%s" width="20" height="20" rx="5" fill="none" '
                                 'stroke="%s" stroke-width="2.5"/>' % (x + 3, y - 7 + 3, x, y - 10 + 0, RING))
                x += 6
            else:
                self.rect(x, y - 7, 14, 14, kind, dashed=(kind == "gone"))
            self.text(x + 22, y, label, 12, SUB)
            x += 22 + est_w(label, 12) + 18

    def save(self, h):
        self.h = h
        out = ('<svg width="100%%" viewBox="0 0 %d %d" role="img" xmlns="http://www.w3.org/2000/svg" '
               'font-family=\'%s\'><title>%s</title>%s%s</svg>\n'
               % (self.w, h, FONT.replace('"', "&quot;"), html.escape(self.name), self.defs(), "\n".join(self.body)))
        with open(os.path.join(SVG_DIR, self.name + ".svg"), "w", encoding="utf-8") as f:
            f.write(out)
        # 粗查: 文字越界 / 文字框互相重叠
        for (x0, y0, x1, y1, t) in self.boxes:
            if x0 < 0 or x1 > self.w or y0 < 0 or y1 > h:
                print("WARN out-of-bounds", self.name, repr(t), round(x0), round(x1), round(y0), round(y1))
        bs = self.boxes
        for i in range(len(bs)):
            for j in range(i + 1, len(bs)):
                a, b = bs[i], bs[j]
                if a[0] < b[2] - 2 and b[0] < a[2] - 2 and a[1] < b[3] - 2 and b[1] < a[3] - 2:
                    print("WARN overlap", self.name, repr(a[4]), repr(b[4]))


LEGEND = [("new", "新 push / 刚被修改"), ("gone", "pop 掉 (虚线扔到左边)"), ("old", "栈里其他的"), ("ring", "栈顶")]


# ---------------------------------------------------------------- trace 通用版式

X_IN, X_POP, X_BKT, X_NOTE = 40, 108, 290, 414
BKT_W = 104


def trace_svg(name, head, rows, footer, title_extra=None, hdr=("输入", "pop 掉的", "操作后的 stack", "说明")):
    """rows: dict(inp=[(text,size,weight)], inp_role, stack=[(label,role)], popped=[(label,reason)], notes=[(text,kind)])
    一行 = 一步; 列顺序固定: 输入 → pop 掉的(虚线扔到左边) → 操作后的 stack(竖直桶) → 说明"""
    s = S(name)
    y = 18
    for line in head:
        s.text(40, y, line, 12, SUB)
        y += 20
    y += 6
    for x, t in zip((X_IN, X_POP, X_BKT, X_NOTE), hdr):
        s.text(x + 4, y, t, 12, SUB)
    y += 12
    s.line(40, y, 640, y)
    def slot0(r):
        pp = r.get("popped", [])
        reason = len(pp) == 1 and bool(pp[0][1])
        return max(len(r["stack"]), 1 if reason else 0)
    cap = max(slot0(r) + len(r.get("popped", [])) for r in rows)
    cap = max(cap, max(len(r["stack"]) for r in rows), 2)
    H = cap * CELL_H + 30
    top = y
    for r in rows:
        bottom = top + H - 10
        stack = r["stack"]
        popped = r.get("popped", [])
        # bucket
        s.bucket(X_BKT, bottom, BKT_W, stack, cap)
        # popped: 虚线扔到左边
        n = len(popped)
        for i, (lab, reason) in enumerate(popped):
            slot = slot0(r) + (n - 1 - i)
            cy = bottom - (slot + 1) * CELL_H + 2
            s.cell(X_POP, cy, 72, CELL_H - 4, lab, "gone", dashed=True)
            s.arrow(X_BKT + 8, cy + (CELL_H - 4) / 2, X_POP + 76, cy + (CELL_H - 4) / 2, "#D85A30", dashed=True)
            if reason:
                for k, ln in enumerate(reason.split("\n")):
                    s.text(X_POP, cy + CELL_H + 8 + 15 * k, ln, 12, "#712B13")
        # input
        has_push = stack and stack[-1][1] == "new" and not popped
        if has_push:
            cy_mid = bottom - len(stack) * CELL_H + 2 + (CELL_H - 4) / 2
        else:
            cy_mid = top + H / 2
        ih = 44
        iy = cy_mid - ih / 2
        role = r.get("inp_role", "new")
        s.rect(X_IN, iy, 56, ih, role)
        lines = r["inp"]
        n_l = len(lines)
        for k, (t, sz, wt) in enumerate(lines):
            yy = iy + ih / 2 + (k - (n_l - 1) / 2) * 17
            s.text(X_IN + 28, yy, t, sz, ROLE[role][2], "middle", wt)
        if has_push:
            s.arrow(X_IN + 58, cy_mid, X_BKT + 6, cy_mid)
        # notes
        notes = r["notes"]
        n_n = len(notes)
        for k, (t, kind) in enumerate(notes):
            yy = top + H / 2 + (k - (n_n - 1) / 2) * 19
            if kind == "b":
                s.text(X_NOTE, yy, t, 14, INK, weight=500)
            elif kind == "red":
                s.text(X_NOTE, yy, t, 12, "#712B13")
            else:
                s.text(X_NOTE, yy, t, 12, SUB)
        top += H
        s.line(40, top - 4, 640, top - 4)
    y = top + 14
    for ln in footer:
        s.text(40, y, ln, 16 if ln is footer[0] else 12, INK if ln is footer[0] else SUB, weight=500 if ln is footer[0] else 400)
        y += 24 if ln is footer[0] else 20
    y += 4
    s.legend(y, LEGEND)
    s.save(int(y + 20))


def st(*labels, new=None):
    """把 label 列表变成 [(label, role)], 位置 new 的那个是 'new'"""
    out = []
    for i, lab in enumerate(labels):
        out.append((lab, "new" if new is not None and i == new else "old"))
    return out


def stk(stack, new_top=False):
    out = [(str(x), "old") for x in stack]
    if new_top and out:
        out[-1] = (out[-1][0], "new")
    return out


# ---------------------------------------------------------------- trace 模拟器 (带记录)

def tr_valid():
    s = "{[()]}"
    pair = {')': '(', ']': '[', '}': '{'}
    stack, rows = [], []
    for ch in s:
        if ch in pair:
            top = stack.pop()
            assert top == pair[ch]
            rows.append(dict(inp=[(ch, 16, 500)], stack=stk(stack),
                             popped=[(top, "配对: %s 对 %s" % (ch, top))],
                             notes=[("闭括号 %s → 只能和栈顶配对" % ch, "n"),
                                    ("pop 出 %s == pair['%s'] = %s" % (top, ch, pair[ch]), "b"),
                                    ("栈里还剩 %d 个没闭合的" % len(stack), "n")]))
        else:
            stack.append(ch)
            rows.append(dict(inp=[(ch, 16, 500)], stack=stk(stack, True),
                             notes=[("开括号 %s → push" % ch, "b"),
                                    ("栈里现在 %d 个没闭合的, 栈顶是最内层的" % len(stack), "n")]))
    assert not stack and load("valid")["is_valid"](s)
    return rows


def tr_min():
    ops = [("push", 5), ("push", 3), ("push", 7), ("getMin",), ("pop",), ("pop",), ("getMin",)]
    ms = load("minstack")["MinStack"]()
    rows = []
    for op in ops:
        if op[0] == "push":
            v = op[1]
            below = ms.stack[-1][1] if ms.stack else None
            ms.push(v)
            cm = ms.stack[-1][1]
            n1 = "栈空 → cur_min = %d" % v if below is None else "cur_min = min(%d, 下面的 min %d) = %d" % (v, below, cm)
            rows.append(dict(inp=[("push", 12, 400), (str(v), 14, 500)], stack=[("(%d, %d)" % t, "old") for t in ms.stack][:-1] + [("(%d, %d)" % ms.stack[-1], "new")],
                             notes=[("push (%d, %d)" % (v, cm), "b"), (n1, "n")]))
        elif op[0] == "pop":
            t = ms.stack[-1]
            ms.pop()
            rows.append(dict(inp=[("pop", 14, 500)], inp_role="old", stack=[("(%d, %d)" % t2, "old") for t2 in ms.stack],
                             popped=[("(%d, %d)" % t, "连 min 一起丢")],
                             notes=[("pop 掉 (%d, %d)" % t, "b"),
                                    ("新栈顶 (%d, %d) 的 min = %d 本来就对" % (ms.stack[-1][0], ms.stack[-1][1], ms.stack[-1][1]), "n")]))
        else:
            m = ms.get_min()
            rows.append(dict(inp=[("getMin", 12, 500)], inp_role="old", stack=[("(%d, %d)" % t2, "old") for t2 in ms.stack],
                             notes=[("返回 栈顶[1] = %d" % m, "b"), ("O(1), 不用扫整个栈", "n")]))
    return rows, ms.get_min()


def tr_decode():
    s = "3[a2[c]]"
    stack, cur, num = [], "", 0
    rows = []

    def q(x):
        return "'%s'" % x
    for ch in s:
        popped = []
        if ch.isdigit():
            n0 = num
            num = num * 10 + int(ch)
            notes = [("读数字: num = %d×10 + %s = %d" % (n0, ch, num), "b")]
            new_top = False
        elif ch == '[':
            stack.append((cur, num))
            notes = [("push (cur, num) = (%s, %d)" % (q(cur), num), "b")]
            cur, num = "", 0
            new_top = True
        elif ch == ']':
            prev, k = stack.pop()
            old = cur
            cur = prev + cur * k
            popped = [("(%s, %d)" % (q(prev), k), "回到外层")]
            notes = [("pop → prev_str = %s, k = %d" % (q(prev), k), "n"),
                     ("cur = %s + %s × %d" % (q(prev), q(old), k), "n"),
                     ("= %s" % q(cur), "b")]
            new_top = False
        else:
            cur += ch
            notes = [("字母: cur += '%s'" % ch, "b")]
            new_top = False
        if ch != ']':
            notes.append(("num = %d · cur = %s" % (num, q(cur)), "n"))
        rows.append(dict(inp=[(ch, 16, 500)], stack=[("(%s, %d)" % (q(a), b), "old") for a, b in stack][:-1] + ([("(%s, %d)" % (q(stack[-1][0]), stack[-1][1]), "new" if new_top else "old")] if stack else []),
                         popped=popped, notes=notes))
    assert cur == load("decode")["decode_string"](s) == "accaccacc"
    return rows, cur


def tr_rpn():
    tokens = ["4", "13", "5", "/", "+", "2", "*"]
    stack, rows = [], []
    for t in tokens:
        if t in ("+", "-", "*", "/"):
            b = stack.pop()
            a = stack.pop()
            r = {"+": a + b, "-": a - b, "*": a * b, "/": int(a / b)}[t]
            stack.append(r)
            sym = {"*": "×", "/": "÷"}.get(t, t)
            rows.append(dict(inp=[(t, 16, 500)], stack=stk(stack, True),
                             popped=[("b = %d" % b, None), ("a = %d" % a, None)],
                             notes=[("先 pop 右操作数 b = %d" % b, "n"), ("再 pop 左操作数 a = %d" % a, "n"),
                                    ("a %s b = %d %s %d = %d" % (sym, a, sym, b, r), "b"),
                                    ("push %d" % r, "n")]))
            # 这一行里新 push 的 r 在栈顶 (has_push 为 False 因为有 popped, 不画 input 箭头)
        else:
            stack.append(int(t))
            rows.append(dict(inp=[(t, 16, 500)], stack=stk(stack, True), notes=[("数字 → push %s" % t, "b")]))
    assert stack == [12] == [load("rpn")["eval_rpn"](tokens)]
    return rows, stack[0]


def tr_calc2():
    s = "3+5*2-6/3"
    stack, num, op = [], 0, '+'
    rows = []
    for i, ch in enumerate(s):
        if ch.isdigit():
            num = num * 10 + int(ch)
        if ch in '+-*/' or i == len(s) - 1:
            popped = []
            if op == '+':
                stack.append(num)
                notes = [("op = '+' → 记成 +%d" % num, "n"), ("push %d" % num, "b")]
            elif op == '-':
                stack.append(-num)
                notes = [("op = '-' → 记成 -%d" % num, "n"), ("push %d" % (-num), "b")]
            elif op == '*':
                t = stack.pop()
                stack.append(t * num)
                notes = [("op = '*' → 立即和栈顶合并", "n"), ("pop %d, %d × %d = %d" % (t, t, num, t * num), "b"), ("push %d" % (t * num), "n")]
                popped = [(str(t), "%d × %d\n合并成 %d" % (t, num, t * num))]
            else:
                t = stack.pop()
                v = int(t / num)
                stack.append(v)
                notes = [("op = '/' → 立即和栈顶合并", "n"), ("pop %d, int(%d / %d) = %d" % (t, t, num, v), "b"), ("push %d" % v, "n")]
                popped = [(str(t), "int(%d / %d)\n= %d" % (t, num, v))]
            last = (i == len(s) - 1)
            inp = [(str(num), 14, 500), ("读到结尾" if last else "读到 %s" % ch, 12, 400)]
            rows.append(dict(inp=inp, stack=stk(stack, True), popped=popped, notes=notes))
            if not last:
                op = ch
            num = 0
    total = sum(stack)
    assert total == load("calc2")["calculate"](s) == 11
    return rows, stack, total


def tr_calc():
    s = "1-(2+(3-1))"
    stack, result, num, sign = [], 0, 0, 1
    rows = []
    pend = ""

    def pr(p):
        return "(%d, %d)" % p
    for ch in s:
        popped, notes = [], []
        if ch.isdigit():
            num = num * 10 + int(ch)
            pend += ch + " "
            continue
        if ch in '+-':
            old = result
            result += sign * num
            notes = [("result = %d + %d×%d = %d" % (old, sign, num, result), "n") if True else None]
            notes[0] = ("result = %d + (%d)×%d = %d" % (old, sign, num, result), "n")
            n0 = num
            num, sign = 0, (1 if ch == '+' else -1)
            notes.append(("sign = %+d" % sign, "b"))
            inp = [((pend + ch).replace(" ", ""), 14, 500)]
            pend = ""
            rows.append(dict(inp=inp, stack=[(pr(p), "old") for p in stack], notes=notes + [("stack 不动", "n")]))
        elif ch == '(':
            stack.append((result, sign))
            notes = [("push (result, sign) = %s" % pr((result, sign)), "b"), ("result = 0, sign = +1 (括号内重新算)", "n")]
            result, sign = 0, 1
            rows.append(dict(inp=[("(", 16, 500)], stack=[(pr(p), "old") for p in stack[:-1]] + [(pr(stack[-1]), "new")], notes=notes))
            pend = ""
        elif ch == ')':
            old = result
            result += sign * num
            n0 = num
            num = 0
            pr_, ps_ = stack.pop()
            r2 = pr_ + ps_ * result
            notes = []
            if n0 or True:
                notes.append(("括号内并入 num: result = %d + (%d)×%d = %d" % (old, sign, n0, result), "n"))
            notes.append(("pop (prev_result, prev_sign) = %s" % pr((pr_, ps_)), "n"))
            notes.append(("result = %d + (%d)×%d = %d" % (pr_, ps_, result, r2), "b"))
            popped = [(pr((pr_, ps_)), "回到外层")]
            result = r2
            inp = [((pend + ")").replace(" ", ""), 14, 500)]
            pend = ""
            rows.append(dict(inp=inp, stack=[(pr(p), "old") for p in stack], popped=popped, notes=notes))
    final = result + sign * num
    assert final == load("calc")["calculate"](s) == -3
    return rows, final, (result, sign, num)


def tr_ast():
    a = [5, 10, -8, -12, 3]
    stack, rows = [], []
    for x in a:
        alive = True
        steps = []   # 每个 pop 一行
        placed = False
        first = True
        while alive and x < 0 and stack and stack[-1] > 0:
            t = stack[-1]
            if t < -x:
                stack.pop()
                nxt_alive = bool(stack and stack[-1] > 0)
                steps.append(("pop", t, nxt_alive))
            elif t == -x:
                stack.pop()
                alive = False
                steps.append(("both", t, False))
            else:
                alive = False
                steps.append(("die", t, False))
        if alive:
            stack_before_push = list(stack)
            stack.append(x)
        # 生成行
        if not steps:
            rows.append(dict(inp=[(str(x), 16, 500)], stack=stk(stack, True),
                             notes=[("%d 和栈顶不会相撞" % x if len(stack) > 1 else "栈空 → push %d" % x, "n"),
                                    ("push %d" % x, "b")]))
        else:
            # 重放: 每个 pop 一行, 最后一行包含 push/消失
            sim = list(stack_before_push) if alive else None
            # 重建 pop 前的栈
            pre = list(stack) if not alive else list(stack[:-1])
            popped_vals = [v for k, v, _ in steps if k in ("pop", "both")]
            full = pre + list(reversed(popped_vals))   # pop 之前的栈 (底到顶)
            cur = list(full)
            for idx, (k, t, _) in enumerate(steps):
                is_last = idx == len(steps) - 1
                if k == "pop":
                    cur.pop()
                    if is_last:   # pop 之后栈顶不再相撞, 然后 push
                        st_ = list(cur) + [x]
                        rows.append(dict(inp=[(str(x), 16, 500)], stack=stk(st_, True),
                                         popped=[(str(t), "%d < |%d| = %d\n栈顶炸掉" % (t, x, -x))],
                                         notes=[("栈顶 %d > 0, %d < 0 → 相撞" % (t, x), "n"),
                                                ("%d < %d: pop %d" % (t, -x, t), "b"),
                                                ("%s → 不再相撞, push %d" % ("栈空" if not cur else "栈顶 %d" % cur[-1] + " 为负" if cur[-1] < 0 else "?", x), "n")]))
                    else:
                        rows.append(dict(inp=[(str(x), 16, 500)], inp_role="old", stack=stk(cur),
                                         popped=[(str(t), "%d < |%d| = %d\n栈顶炸掉" % (t, x, -x))],
                                         notes=[("栈顶 %d > 0, %d < 0 → 相撞" % (t, x), "n"),
                                                ("%d < %d: pop %d" % (t, -x, t), "b"),
                                                ("%d 还活着, 继续撞下一个" % x, "n")]))
                elif k == "both":
                    cur.pop()
                    rows.append(dict(inp=[(str(x), 16, 500)], inp_role="gone", stack=stk(cur),
                                     popped=[(str(t), "一样大\n同归于尽")],
                                     notes=[("%d == %d" % (t, -x), "b"), ("两个都消失, 不 push", "n")]))
                else:
                    rows.append(dict(inp=[(str(x), 16, 500)], inp_role="gone", stack=stk(cur),
                                     notes=[("栈顶 %d > 0, %d < 0 → 相撞" % (t, x), "n"),
                                            ("%d > %d: %d 被炸掉" % (t, -x, x), "b"), ("不 push, stack 不变", "n")]))
    assert stack == load("asteroid")["asteroid_collision"](a) == [-12, 3]
    return rows, stack


def tr_dup():
    s, k = "abbbaac", 3
    stack, rows = [], []
    for ch in s:
        popped = []
        if stack and stack[-1][0] == ch:
            stack[-1][1] += 1
            if stack[-1][1] == k:
                t = stack.pop()
                popped = [("(%s, %d)" % (t[0], t[1]), "count = %d = k\n整段删掉" % t[1])]
                notes = [("和栈顶同字符 → count += 1 = %d" % k, "n"), ("count == k = %d → pop 整段" % k, "b"),
                         ("下面的段变成栈顶" if stack else "栈空了", "n")]
                newtop = False
            else:
                notes = [("和栈顶同字符 → count += 1", "n"), ("(%s, %d), %d < k = %d" % (ch, stack[-1][1], stack[-1][1], k), "b")]
                newtop = True
        else:
            stack.append([ch, 1])
            notes = [("和栈顶不同 → push (%s, 1)" % ch, "b")] if len(stack) > 1 else [("栈空 → push (%s, 1)" % ch, "b")]
            newtop = True
        rows.append(dict(inp=[(ch, 16, 500)],
                         stack=[("(%s, %d)" % (c, n), "old") for c, n in stack[:-1]] + ([("(%s, %d)" % (stack[-1][0], stack[-1][1]), "new" if newtop else "old")] if stack else []),
                         popped=popped, notes=notes))
    res = "".join(c * n for c, n in stack)
    assert res == load("dup2")["remove_duplicates"](s, k) == "c"
    return rows, res


def tr_path():
    path = "/a/./b/../../c/"
    stack, rows = [], []
    for part in path.split('/'):
        if part == '':
            continue
        popped = []
        if part == '..':
            if stack:
                t = stack.pop()
                popped = [(t, "'..' 回上一层")]
                notes = [("'..' → 回到上一层", "n"), ("pop %s" % t, "b")]
            else:
                notes = [("'..' 但栈空 → 忽略", "b")]
            newtop = False
        elif part == '.':
            notes = [("'.' = 当前目录 → 什么都不做", "b")]
            newtop = False
        else:
            stack.append(part)
            notes = [("目录名 → push %s" % part, "b")]
            newtop = True
        rows.append(dict(inp=[(part, 16, 500)], inp_role="new" if newtop else "old",
                         stack=stk(stack, newtop), popped=popped, notes=notes))
    res = '/' + '/'.join(stack)
    assert res == load("path")["simplify_path"](path) == "/c"
    return rows, res


# ---------------------------------------------------------------- core 图 (手工布局)

HEAD_Y = (18, 38)


def core_stack_basic():
    s = S("stack_core")
    s.text(40, 18, "s = ( ( ( ) ) ) · 每个 ')' 要配的 = 左边最近的、还没被配对的 '('", 12, SUB)
    s.text(40, 38, "最近 = 栈顶 · 后开的先关 (LIFO) ⇔ 括号嵌套", 12, SUB)
    chars = "((()))"
    x0, y0 = 60, 130
    for i, c in enumerate(chars):
        s.cell(x0 + i * 46, y0, 38, 34, c, "old", 16)
    # 嵌套的弧: (2,3) (1,4) (0,5)
    for (i, j, h) in ((2, 3, 22), (1, 4, 44), (0, 5, 66)):
        xa, xb = x0 + i * 46 + 19, x0 + j * 46 + 19
        s.path("M%s %s L%s %s L%s %s L%s %s" % (xa, y0, xa, y0 - h, xb, y0 - h, xb, y0), "#0F6E56", arrow=False, sw=1.5)
    s.text(x0, y0 + 56, "下标 0 1 2 3 4 5", 12, SUB)
    s.text(x0, y0 + 76, "弧 = 配对: (2,3) 最内层先配, 最后才是 (0,5)", 12, SUB)
    # 读到下标 3 的 ')' 之前的栈
    bx = 500
    s.text(bx - 6, 62, "读到下标 3 之前的 stack", 12, SUB)
    s.bucket(bx, 210, 110, [("下标 0", "old"), ("下标 1", "old"), ("下标 2", "old")], 3)
    s.text(bx + 55, 226, "栈底", 12, SUB, "middle")
    s.text(40, 262, "brute force: 每个 ')' 往左扫, 找最近没用过的 '(' → 每个 O(n), 共 O(n²)", 12, SUB)
    s.text(40, 284, "stack: 栈本身就是 '往左扫会依次碰到的候选', 已按最近优先排好 → pop 一次 O(1), 共 O(n)", 12, SUB)
    s.text(40, 306, "栈顶 (橙色 ring) 永远是最近的、还没处理完的那个", 12, SUB)
    s.save(330)


def core_valid():
    s = S("valid_core")
    s.text(40, 18, "invariant: stack 从底到顶 = 还没闭合的开括号, 栈顶是最内层的", 12, SUB)
    s.text(40, 38, "读到闭括号时, 它只能和栈顶配对 · 四种情况:", 12, SUB)
    panels = [
        ("开括号", "push", ["(", "["], None, "(", "ok"),
        ("闭括号, 栈顶配对", "pop 栈顶", ["("], "[", "]", "ok"),
        ("闭括号, 栈顶不配", "return False", ["(", "["], None, ")", "bad"),
        ("闭括号, 栈空", "return False", [], None, "]", "bad"),
    ]
    xs = [40, 200, 360, 520]
    # panel 数据手写
    data = [
        dict(title="① 开括号", tok="{", cells=[("(", "old"), ("[", "old")], newc=("{", "new"), verdict="push {", ok=True, sub="等后面的来找它"),
        dict(title="② 闭括号, 栈顶配对", tok="]", cells=[("(", "old")], pop=("[", "gone"), verdict="pop [ == pair[']']", ok=True, sub="配对成功, 继续"),
        dict(title="③ 闭括号, 栈顶不配", tok=")", cells=[("(", "old"), ("[", "old")], verdict="pop [ ≠ pair[')'] = (", ok=False, sub="交叉 ([)] → False"),
        dict(title="④ 闭括号, 栈空", tok="]", cells=[], verdict="not stack", ok=False, sub="多余闭括号 → False"),
    ]
    for x, p in zip(xs, data):
        s.text(x, 70, p["title"], 14, INK, weight=500)
        s.cell(x, 88, 40, 34, p["tok"], "new", 16)
        s.text(x + 48, 105, "读到", 12, SUB)
        bottom = 220
        cells = list(p["cells"])
        if "newc" in p:
            cells = cells + [p["newc"]]
        s.bucket(x + 4, bottom, 100, cells, 3)
        if "pop" in p:
            py = bottom - (len(cells) + 1) * CELL_H + 2
            s.cell(x + 118, py, 36, CELL_H - 4, p["pop"][0], "gone", dashed=True)
            s.arrow(x + 108, py + 13, x + 116, py + 13, "#D85A30", dashed=True)
        col = "#0F6E56" if p["ok"] else "#993C1D"
        s.text(x, 246, p["verdict"], 12, col, weight=500)
        s.text(x, 266, p["sub"], 12, col)
    s.text(40, 304, "走完以后: stack 非空 → 有开括号一直没被闭合 → False · 空 → True", 14, INK, weight=500)
    s.save(330)


def core_minstack():
    s = S("minstack_core")
    s.text(40, 18, "要求: push / pop / top / get_min 全部 O(1)", 12, SUB)
    s.text(40, 38, "pop 掉当前最小值之后, 新的最小值是谁? —— 必须在 push 的时候就记下来", 12, SUB)
    # 左: 单变量
    s.text(40, 70, "只存一个 min 变量 (错)", 14, "#993C1D", weight=500)
    s.bucket(50, 200, 90, [("5", "old"), ("3", "old")], 3)
    s.text(95, 218, "min = 3", 14, INK, "middle", 500)
    s.arrow(150, 150, 200, 150)
    s.text(175, 134, "pop", 12, SUB, "middle")
    s.bucket(210, 200, 90, [("5", "old")], 3)
    s.text(255, 218, "min 还是 3 ✗", 14, "#993C1D", "middle", 500)
    s.text(40, 246, "实际最小值是 5, 变量不知道 → 只能重新扫整个栈 O(n)", 12, "#712B13")
    s.line(335, 62, 335, 262, "#B4B2A9", True)
    # 右: pair
    s.text(358, 70, "每个元素带 (val, min_so_far) (对)", 14, "#0F6E56", weight=500)
    s.bucket(368, 200, 110, [("(5, 5)", "old"), ("(3, 3)", "old")], 3)
    s.text(423, 218, "get_min = 3", 14, INK, "middle", 500)
    s.arrow(486, 150, 524, 150)
    s.text(505, 134, "pop", 12, SUB, "middle")
    s.bucket(530, 200, 110, [("(5, 5)", "old")], 3)
    s.text(585, 218, "get_min = 5 ✓", 14, "#0F6E56", "middle", 500)
    s.text(358, 246, "min_so_far 只取决于它下面的元素 → 写入后不再变", 12, SUB)
    s.text(40, 292, "栈的每个元素都是一个 '快照': 记着 '栈只有到它为止这么高时' 的答案", 14, INK, weight=500)
    s.text(40, 314, "pop 掉它, 快照一起走, 下面元素的快照原封不动 —— 这就是 '每个元素带额外状态'", 12, SUB)
    s.save(336)


def core_decode():
    s = S("decode_core")
    s.text(40, 18, "s = 3[a2[c]] · 每个 '[' 开一层新上下文, 每个 ']' 回到外层", 12, SUB)
    s.text(40, 38, "stack 存 '外层的现场' = (prev_str, k) · cur = 当前这层已拼出的字符串", 12, SUB)
    chars = ["3", "[", "a", "2", "[", "c", "]", "]"]
    x0, y0 = 40, 76
    for i, c in enumerate(chars):
        s.cell(x0 + i * 40, y0, 34, 32, c, "old", 16)
    # 外层括号范围 idx1..7, 内层 4..6
    def span(i, j, yy, col, label):
        xa, xb = x0 + i * 40, x0 + j * 40 + 34
        s.path("M%s %s L%s %s L%s %s L%s %s" % (xa, yy - 6, xa, yy, xb, yy, xb, yy - 6), col, arrow=False)
        s.text((xa + xb) / 2, yy + 14, label, 12, SUB, "middle")
    span(1, 7, y0 + 46, "#5F5E5A", "外层 [ ]: k = 3")
    span(4, 6, y0 + 74, "#0F6E56", "内层 [ ]: k = 2")
    s.text(40, 196, "读到下标 5 的 'c' 时:", 14, INK, weight=500)
    s.bucket(60, 320, 120, [("('', 3)", "old"), ("('a', 2)", "old")], 2)
    s.text(120, 338, "栈底", 12, SUB, "middle")
    s.text(210, 262, "cur = 'c'  (内层正在拼)", 14, INK, weight=500)
    s.text(210, 286, "('a', 2) = 进内层之前的 cur 是 'a', 这个 [ ] 重复 2 次", 12, SUB)
    s.text(210, 306, "('', 3) = 进外层之前的 cur 是 '', 这个 [ ] 重复 3 次", 12, SUB)
    s.text(210, 330, "读到 ']' → pop ('a', 2):", 14, INK, weight=500)
    s.text(210, 352, "cur = prev_str + cur × k = 'a' + 'c' × 2 = 'acc'", 14, "#0F6E56", weight=500)
    s.save(374)


def core_rpn():
    s = S("rpn_core")
    s.text(40, 18, "后缀表达式: 运算符出现时, 它的两个操作数 = 左边最近算好的两个 = 栈顶两个", 12, SUB)
    s.text(40, 38, "tokens = [2, 1, +, 3, *] · 先看 '+':", 12, SUB)
    s.text(60, 82, "读到 '+' 之前", 12, SUB)
    s.bucket(60, 240, 104, [("2", "old"), ("1", "old")], 3)
    s.cell(240, 240 - 3 * CELL_H - 6 + 2, 72, CELL_H - 4, "b = 1", "gone", dashed=True)
    s.cell(240, 240 - 2 * CELL_H - 6 + 2, 72, CELL_H - 4, "a = 2", "gone", dashed=True)
    s.arrow(172, 240 - 3 * CELL_H - 6 + 15, 236, 240 - 3 * CELL_H - 6 + 15, "#D85A30", dashed=True)
    s.arrow(172, 240 - 2 * CELL_H - 6 + 15, 236, 240 - 2 * CELL_H - 6 + 15, "#D85A30", dashed=True)
    s.text(204, 100, "先 pop 的是 b (右)", 12, "#712B13", "middle")
    s.text(204, 120, "再 pop 的是 a (左)", 12, "#712B13", "middle")
    s.path("M318 188 L418 214", SUB)
    s.text(240, 258, "a + b = 2 + 1 = 3", 14, INK, weight=500)
    s.bucket(430, 240, 104, [("3", "new")], 3)
    s.text(482, 258, "push 回去", 12, SUB, "middle")
    s.text(40, 292, "为什么是栈: 括号让表达式嵌套, 后缀式把嵌套摊平 —— 最近算好的结果马上被下一个运算符消耗", 12, SUB)
    s.text(40, 314, "顺序: b 先 pop, a 后 pop, 算 a - b / a ÷ b (减法除法不能交换)", 14, INK, weight=500)
    s.text(40, 338, "除法: int(a / b) 向 0 取整, 不能写 a // b (-7 // 2 = -4, 但要 -3)", 12, SUB)
    s.save(360)


def core_calc2():
    s = S("calc2_core")
    s.text(40, 18, "s = 2 - 3 * 2 · 乘除优先级更高 → '+ -' 不能边读边算, 要等后面有没有 '* /'", 12, SUB)
    s.text(40, 38, "做法: 每一项带符号 push 进 stack; '* /' 立刻和栈顶这一项合并; 最后 sum(stack)", 12, SUB)
    # 错
    s.text(40, 70, "边读边算 (错)", 14, "#993C1D", weight=500)
    for i, c in enumerate(["2", "-", "3", "*", "2"]):
        s.cell(40 + i * 44, 84, 38, 32, c, "old", 16)
    s.text(40, 138, "(2 - 3) × 2 = -1 × 2 = -2 ✗", 14, "#993C1D", weight=500)
    s.line(40, 158, 640, 158)
    # 对
    s.text(40, 182, "按 '项' 切开 (对)", 14, "#0F6E56", weight=500)
    for i, c in enumerate(["2", "-", "3", "*", "2"]):
        s.cell(40 + i * 44, 196, 38, 32, c, "old", 16)
    # 项1: 下标 0 ; 项2: 下标 1..4
    s.path("M40 238 L40 244 L78 244 L78 238", "#0F6E56", arrow=False)
    s.text(59, 258, "项1", 12, SUB, "middle")
    s.path("M84 238 L84 244 L254 244 L254 238", "#0F6E56", arrow=False)
    s.text(169, 258, "项2 = -(3 × 2)", 12, SUB, "middle")
    s.text(40, 292, "项1 = +2 → push 2", 12, SUB)
    s.text(40, 312, "项2: '-' 先 push -3 · 读到 '*' → pop -3, -3 × 2 = -6 → push -6", 12, SUB)
    s.text(40, 340, "最后 sum(stack) = 2 + (-6) = -4 ✓", 14, INK, weight=500)
    s.bucket(430, 330, 110, [("2", "old"), ("-6", "new")], 3)
    s.text(485, 348, "stack = 项", 12, SUB, "middle")
    s.text(40, 366, "延迟处理 '+ -' = 先把项存进栈, 等整项算完", 12, SUB)
    s.text(40, 386, "立即处理 '* /' = 栈顶那一项就是它的左操作数", 12, SUB)
    s.save(408)


def core_calc():
    s = S("calc_core")
    s.text(40, 18, "s = 1 - (2 + 3) · 括号 = 一个新的子问题: 进括号时 push 外层现场, 出括号时 pop 回来", 12, SUB)
    s.text(40, 38, "现场 = (result, sign): 外层累加到哪, 以及 '(' 前面的符号", 12, SUB)
    xs = [40, 250, 460]
    titles = ["① 读完 '1 -', 还没读 '('", "② 读到 '('", "③ 括号内算完, 读到 ')'"]
    for x, t in zip(xs, titles):
        s.text(x, 70, t, 14, INK, weight=500)
    s.text(40, 100, "result = 1 · sign = -1", 14, INK, weight=500)
    s.bucket(40, 205, 100, [], 2)
    s.text(40, 229, "stack 空 · 要减的是整个括号", 12, SUB)
    s.text(250, 100, "result = 0 · sign = +1", 14, INK, weight=500)
    s.bucket(250, 205, 100, [("(1, -1)", "new")], 2)
    s.text(250, 229, "push 现场, 括号内重新算", 12, SUB)
    s.text(460, 100, "result = 5 (括号内)", 14, INK, weight=500)
    s.bucket(460, 205, 100, [], 2)
    py = 205 - 2 * CELL_H - 6 + 2
    s.cell(578, py, 60, CELL_H - 4, "(1, -1)", "gone", size=12, dashed=True)
    s.arrow(568, py + 13, 576, py + 13, "#D85A30", dashed=True)
    s.text(460, 229, "pop 回外层现场", 12, SUB)
    s.text(40, 271, "pop (prev_result, prev_sign) = (1, -1)", 14, INK, weight=500)
    s.text(40, 297, "result = prev_result + prev_sign × result = 1 + (-1) × 5 = -4", 14, "#0F6E56", weight=500)
    s.text(40, 323, "整个括号 = 一个数, 带上 '(' 前面的符号 · 嵌套多深, 栈就有多深", 12, SUB)
    s.save(345)


def core_asteroid():
    s = S("asteroid_core")
    s.text(40, 18, "正数向右飞, 负数向左飞 · 只有 '栈顶向右 + 新来的向左' 才会相撞", 12, SUB)
    s.text(40, 38, "stack 里是 '目前活着、且互相不会再撞' 的 asteroid", 12, SUB)
    cases = [("栈顶 3, 新来 5", 3, 5, False, "都向右, 不撞"),
             ("栈顶 -3, 新来 -5", -3, -5, False, "都向左, 不撞"),
             ("栈顶 -3, 新来 5", -3, 5, False, "背离, 不撞"),
             ("栈顶 3, 新来 -5", 3, -5, True, "相向 → 撞")]
    xs = [40, 200, 360, 520]
    for x, (t, a, b, hit, v) in zip(xs, cases):
        s.text(x, 66, t, 12, SUB)
        for k, val in enumerate((a, b)):
            cx = x + 20 + k * 70
            s.body.append('<circle cx="%s" cy="112" r="18" fill="%s" stroke="%s" stroke-width="1"/>'
                          % (cx, "#F1EFE8" if k == 0 else "#E1F5EE", "#5F5E5A" if k == 0 else "#0F6E56"))
            s.text(cx, 112, str(val), 14, "#444441" if k == 0 else "#085041", "middle", 500)
            d_ = 1 if val > 0 else -1
            s.arrow(cx - 12 * d_, 80, cx + 12 * d_, 80)
        s.text(x, 150, v, 14, "#993C1D" if hit else "#0F6E56", weight=500)
    s.line(40, 176, 640, 176)
    s.text(40, 200, "相撞时 (栈顶 t > 0, 新来 x < 0), 比较 t 和 |x|:", 14, INK, weight=500)
    items = [("t < |x|", "栈顶炸掉 → pop", "x 继续撞下一个 (while)", "gone"),
             ("t == |x|", "同归于尽 → pop", "x 也消失, 不 push", "gone"),
             ("t > |x|", "x 被炸掉", "不 push, stack 不变", "new")]
    for i, (c, a, b, role) in enumerate(items):
        x = 40 + i * 210
        s.cell(x, 220, 78, 30, c, "old", 14)
        s.text(x, 272, a, 12, INK)
        s.text(x, 292, b, 12, SUB)
    s.text(40, 326, "while 的条件: alive and x < 0 and stack and stack[-1] > 0", 14, INK, weight=500)
    s.text(40, 350, "x 之所以能反复和新的栈顶比, 是因为栈顶炸掉后, 露出来的就是 '下一个最近的'", 12, SUB)
    s.save(372)


def core_dup2():
    s = S("dup2_core")
    s.text(40, 18, "s = abbbaac, k = 3 · 删掉 bbb 以后, 左边的 a 和右边的 aa 变成相邻 → 还要继续合并", 12, SUB)
    s.text(40, 38, "stack 每个元素存一整段 [char, count], 栈顶 = 当前最右边的连续段", 12, SUB)
    s.text(40, 70, "只存 char (需要回头数)", 14, "#993C1D", weight=500)
    s.bucket(50, 230, 90, [("a", "old"), ("b", "old"), ("b", "old"), ("b", "old")], 4)
    s.text(40, 252, "第 3 个 b 进来才知道凑够 3", 12, SUB)
    s.text(40, 272, "删完后又要回头数 a 有几个 → 重复劳动", 12, SUB)
    s.line(250, 62, 250, 290, "#B4B2A9", True)
    s.text(270, 70, "存 [char, count] (对): 栈顶的 count 就是答案", 14, "#0F6E56", weight=500)
    s.bucket(280, 230, 100, [("(a, 1)", "old"), ("(b, 3)", "old")], 4)
    s.text(330, 248, "count == k", 12, "#712B13", "middle")
    s.arrow(390, 150, 424, 150)
    s.text(407, 132, "pop", 12, SUB, "middle")
    s.bucket(430, 230, 100, [("(a, 1)", "old")], 4)
    s.text(480, 248, "新栈顶", 12, SUB, "middle")
    s.arrow(540, 150, 566, 150)
    s.bucket(570, 230, 100 - 30, [("(a,2)", "new")], 4)
    s.text(605, 248, "读到 a", 12, SUB, "middle")
    s.text(40, 306, "删掉一段 = pop 一个元素 · 左右两段自动相邻, 因为它们在栈里本来就上下挨着", 14, INK, weight=500)
    s.text(40, 330, "额外状态 (count) 跟着元素存进栈 —— 和 Min Stack 的 (val, min) 是同一个套路", 12, SUB)
    s.save(352)


def core_path():
    s = S("path_core")
    s.text(40, 18, "path = /a/./b/../../c/ · split('/') 之后每个 part 只有三种", 12, SUB)
    s.text(40, 38, "parts = ['', 'a', '.', 'b', '..', '..', 'c', ''] · stack = 当前目录的每一层", 12, SUB)
    xs = [40, 250, 460]
    cases = [("目录名 (a, b, c)", "push", [("a", "old")], [("a", "old"), ("b", "new")], "进入下一层"),
             ("'..'", "pop", [("a", "old"), ("b", "old")], [("a", "old")], "回上一层; 栈空则忽略"),
             ("'' 或 '.'", "不动", [("a", "old")], [("a", "old")], "'//' 切出空串; '.' = 当前目录")]
    for x, (t, act, before, after, why) in zip(xs, cases):
        s.text(x, 70, t, 14, INK, weight=500)
        s.bucket(x, 190, 70, before, 2)
        s.arrow(x + 78, 150, x + 104, 150)
        s.text(x + 91, 132, act, 12, SUB, "middle")
        s.bucket(x + 110, 190, 70, after, 2)
        if act == "pop":
            s.cell(x + 78, 190 - 2 * CELL_H - 6 + 2 - 2, 0, 0, "", "old") if False else None
        s.text(x, 214, why, 12, SUB)
    s.text(40, 258, "返回 '/' + '/'.join(stack) · stack 为空时就是 '/'", 14, INK, weight=500)
    s.text(40, 282, "Unix 路径 = 目录栈: 进目录 push, '..' pop · 和 '最近没处理的' 是同一个结构", 12, SUB)
    s.save(304)


# ---------------------------------------------------------------- 生成所有 SVG

core_stack_basic()
core_valid()
core_minstack()
core_decode()
core_rpn()
core_calc2()
core_calc()
core_asteroid()
core_dup2()
core_path()

# traces
rows = tr_valid()
trace_svg("valid_trace",
          ["s = \"{[()]}\" · 每一步: 开括号 push → 闭括号 pop 栈顶并检查配对",
           "invariant: stack = 还没闭合的开括号, 栈顶 (橙色 ring) = 最内层"],
          rows, ["结束: stack 为空 → return True", "反例 \"([)]\": 读到 ')' 时栈顶是 '[' , pop 出 '[' ≠ '(' → False"])

rows, final_min = tr_min()
trace_svg("minstack_trace",
          ["ops: push 5, push 3, push 7, getMin, pop, pop, getMin",
           "stack 每个元素 = (val, min_so_far) · min_so_far = 从栈底到它自己的最小值"],
          rows, ["最后 getMin = %d (pop 掉 3 之后, 5 自己带着的 min 就是答案)" % final_min],
          hdr=("操作", "pop 掉的", "操作后的 stack", "说明"))

rows, res = tr_decode()
trace_svg("decode_trace",
          ["s = \"3[a2[c]]\" · '[' 把 (cur, num) push 进 stack, 然后重新开始; ']' pop 回来",
           "cur = 当前这层拼出的字符串 · num = 正在读的数字 · stack 元素 = (prev_str, k)"],
          rows, ["结果: cur = '%s' (= 'a' + 'c'×2 = 'acc', 再 '' + 'acc'×3)" % res])

rows, res = tr_rpn()
trace_svg("rpn_trace",
          ["tokens = [4, 13, 5, /, +, 2, *] = (4 + 13 / 5) × 2",
           "数字 → push · 运算符 → pop b, pop a, push (a 运算 b)"],
          rows, ["结果: stack = [%d] → 返回 %d" % (res, res), "13 ÷ 5 = 2.6 → 向 0 取整成 2; 4 + 2 = 6; 6 × 2 = 12"])

rows, stack_, total = tr_calc2()
trace_svg("calc2_trace",
          ["s = \"3+5*2-6/3\" · op = 上一个运算符, num 属于它; 读到下一个运算符时才处理 \"op num\"",
           "+ - → 带符号 push · * / → pop 栈顶, 算完 push 回去"],
          rows, ["结束: sum(stack) = %s = %d" % (" + ".join(str(x) if x >= 0 else "(%d)" % x for x in stack_), total)],
          hdr=("读到", "pop 掉的", "操作后的 stack", "说明"))

rows, final, (r_, sg_, n_) = tr_calc()
trace_svg("calc_trace",
          ["s = \"1-(2+(3-1))\" · stack 元素 = (result, sign) = '(' 之前的现场",
           "'(' push 现场并清零 · ')' 先并入 num, 再 pop 现场: result = prev_result + prev_sign × result"],
          rows, ["结束: result + sign × num = %d + (%d)×%d = %d" % (r_, sg_, n_, final)],
          hdr=("读到", "pop 掉的", "操作后的 stack", "说明"))

rows, stack_ = tr_ast()
trace_svg("asteroid_trace",
          ["asteroids = [5, 10, -8, -12, 3] · 正数向右, 负数向左",
           "只有 '栈顶 > 0 且 新来的 < 0' 才撞 · 撞完谁小谁炸, 一样大都炸"],
          rows, ["结果: stack = %s" % stack_, "-8 撞不过 10 (被炸); -12 炸掉 10 和 5, 自己活下来; 3 在 -12 右边, 方向相背, 不撞"])

rows, res = tr_dup()
trace_svg("dup2_trace",
          ["s = \"abbbaac\", k = 3 · stack 元素 = (char, count)",
           "和栈顶同字符 → count += 1 · count == k → pop 整段 · 否则 push (ch, 1)"],
          rows, ["结果: stack 只剩 (c, 1) → \"%s\"" % res, "bbb 被删后, a 和 aa 在栈里本来就上下挨着 → 继续合并成 aaa 被删"])

rows, res = tr_path()
trace_svg("path_trace",
          ["path = \"/a/./b/../../c/\" · split('/') 之后跳过空串, 逐个 part 处理",
           "目录名 → push · '..' → pop (栈空则忽略) · '.' → 不动"],
          rows, ["结果: '/' + '/'.join(%s) = \"%s\"" % (["c"], res)])

print("svgs written to", SVG_DIR)

# ---------------------------------------------------------------- HTML

exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '06_stack_doc.py'), encoding='utf-8').read())
