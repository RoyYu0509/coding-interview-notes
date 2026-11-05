"""
所有 learning doc 共用的 HTML 生成工具。

每个 category 写一个 build/NN_name.py:
    import doclib as d
    doc = d.Doc("02 · Two Pointers")
    doc.main("主线: ...")
    doc.h2("1. 一句结论")
    doc.p("正文")
    doc.code('''python 代码''')
    doc.svg("02-two-pointers/3sum_trace.svg", "图说: 这张图说明的结论")
    doc.note("笔记里该写的那句话")
    doc.write("docs/02-two-pointers.html")

运行: cd build && python3 -I NN_name.py
SVG 是独立文件 (docs/svg/<slug>/*.svg), 生成 HTML 时内联进去,
所以 HTML 单文件就能看, GitHub 上也能单独打开 SVG。
"""
import html
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

KEYWORDS = {
    "def", "class", "if", "elif", "else", "for", "while", "in", "not",
    "and", "or", "is", "None", "True", "False", "import", "from", "as",
    "with", "try", "except", "finally", "lambda", "yield", "pass",
    "break", "continue", "global", "nonlocal", "del", "assert", "raise",
}
RETURN_WORDS = {"return"}
BUILTINS = {
    "len", "range", "min", "max", "sum", "sorted", "enumerate", "zip",
    "list", "dict", "set", "tuple", "int", "str", "float", "bool",
    "abs", "any", "all", "map", "filter", "reversed", "print", "ord",
    "chr", "self", "heapq", "deque", "defaultdict", "Counter",
    "collections", "bisect", "inf", "math", "functools", "cache",
    "lru_cache", "ListNode", "TreeNode", "Optional", "List",
}

TOKEN = re.compile(
    r'(#.*$)|("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')|([A-Za-z_]\w*)'
    r'|(\s+)|(.)')


def _hl(line):
    parts = []
    for m in TOKEN.finditer(line):
        comment, string, ident, space, other = m.groups()
        if comment:
            parts.append('<span class="c">%s</span>' % html.escape(comment))
        elif string:
            parts.append('<span class="s">%s</span>' % html.escape(string))
        elif ident:
            rest = line[m.end():].lstrip()
            if ident in KEYWORDS:
                cls = "k"
            elif ident in RETURN_WORDS:
                cls = "r"
            elif ident in BUILTINS:
                cls = "t"
            elif rest.startswith("("):
                cls = "f"
            else:
                cls = ""
            t = html.escape(ident)
            parts.append('<span class="%s">%s</span>' % (cls, t) if cls else t)
        elif space:
            parts.append(space)
        else:
            parts.append(html.escape(other))
    return "".join(parts)


CSS = '''
:root{--bg:#fff;--fg:#1d1d1f;--sub:#6b6b70;--code:#f3f1ea;--note:#e8f0fe;--line:#4a7de0;
--row:#f3f3f3;--gutter:#b9b9bd;--gnum:#8a8a90;--kw:#1b3de0;--ty:#2e8bc0;--fn:#7a5a2e;--cm:#2b7a2b;--st:#d12f2f;--rt:#7a1fb8;--box:#e2e2e5}
@media(prefers-color-scheme:dark){:root{--bg:#16181d;--fg:#e8e8ea;--sub:#9a9aa2;--code:#262932;--note:#1c2a45;
--row:#23262e;--gutter:#4a4d57;--gnum:#7c7f89;--kw:#6ea1ff;--ty:#4ec9c0;--fn:#d7ba7d;--cm:#6a9955;--st:#ff7b72;--rt:#c792ea;--box:#363a45}}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.8 -apple-system,"PingFang SC",sans-serif}
article{max-width:820px;margin:0 auto;padding:24px 16px 64px}
h1{font-size:26px;margin:8px 0 12px}
h2{font-size:21px;margin:40px 0 8px;border-bottom:1px solid var(--box);padding-bottom:4px}
h3{font-size:17px;margin:24px 0 6px}
code{background:var(--code);padding:1px 5px;border-radius:4px;font:0.9em ui-monospace,Menlo,Consolas,monospace}
.code{counter-reset:ln;border:1px solid var(--box);border-radius:6px;overflow-x:auto;margin:12px 0;padding:4px 0;
font:14px/1.7 ui-monospace,Menlo,Consolas,monospace;background:var(--bg)}
.code .l{display:block;position:relative;white-space:pre;min-height:1.7em;padding:0 14px 0 62px;counter-increment:ln;
background-image:linear-gradient(to right,transparent 48px,var(--gutter) 48px,var(--gutter) 50px,transparent 50px)}
.code .l:nth-child(odd){background-color:var(--row)}
.code .l::before{content:counter(ln);position:absolute;left:0;width:38px;text-align:right;color:var(--gnum)}
.k{color:var(--kw)}.t{color:var(--ty)}.f{color:var(--fn)}.c{color:var(--cm)}.s{color:var(--st)}.r{color:var(--rt)}
.note{background:var(--note);border-left:4px solid var(--line);padding:6px 12px;border-radius:4px}
.main{color:var(--sub)}
figure{margin:14px 0;background:#fff;border:1px solid var(--box);border-radius:8px;padding:8px}
figure svg{width:100%;height:auto;display:block}
figcaption{color:#52514e;font-size:14px;padding:4px 6px 0}
table{border-collapse:collapse;margin:10px 0;font-size:15px}
td,th{border:1px solid var(--box);padding:4px 10px;text-align:left}
details{margin:12px 0;border:1px dashed var(--box);border-radius:6px;padding:4px 12px}
summary{cursor:pointer;color:var(--sub);font-size:15px}
ol,ul{padding-left:24px}li{margin:4px 0}
'''


class Doc:
    def __init__(self, title):
        self.title = title
        self.items = ["<h1>%s</h1>" % html.escape(title)]

    def main(self, text):
        self.items.append('<p class="main">%s</p>' % text)

    def h2(self, text):
        self.items.append("<h2>%s</h2>" % text)

    def h3(self, text):
        self.items.append("<h3>%s</h3>" % text)

    def p(self, text):
        self.items.append("<p>%s</p>" % text)

    def raw(self, text):
        self.items.append(text)

    def note(self, text):
        self.items.append('<p class="note"><b>记:</b>%s</p>' % text)

    def code(self, text):
        lines = text.strip("\n").split("\n")
        rows = "".join('<span class="l">%s</span>' % _hl(l) for l in lines)
        self.items.append('<div class="code">%s</div>' % rows)

    def svg(self, rel_path, caption):
        path = os.path.join(ROOT, "docs", "svg", rel_path)
        with open(path, encoding="utf-8") as f:
            s = f.read()
        s = re.sub(r"<\?xml.*?\?>", "", s)
        self.items.append("<figure>%s<figcaption>%s</figcaption></figure>"
                          % (s, caption))

    def write(self, rel_out):
        out = os.path.join(ROOT, rel_out)
        doc = ('<!doctype html>\n<html lang="zh-CN"><head><meta charset="utf-8">'
               '<meta name="viewport" content="width=device-width,initial-scale=1">'
               '<title>%s</title><style>%s</style></head><body>'
               '<article contenteditable="true">\n%s\n</article></body></html>\n'
               % (html.escape(self.title), CSS, "\n".join(self.items)))
        assert "<script" not in doc.lower()
        with open(out, "w", encoding="utf-8") as f:
            f.write(doc)
        print("wrote", out, len(doc))
