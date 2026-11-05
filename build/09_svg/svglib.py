import html
FONT = 'ui-sans-serif, system-ui, -apple-system, "PingFang SC", sans-serif'
ROLE = {
    'norm': ('#F1EFE8', '#5F5E5A', '#444441'),
    'new':  ('#E1F5EE', '#0F6E56', '#085041'),
    'pop':  ('#FAECE7', '#993C1D', '#712B13'),
    'out':  ('#FFFFFF', '#B4B2A9', '#52514E'),
}
INK = '#0B0B0B'; SUB = '#52514E'; RING = '#EF9F27'; DASH = '#D85A30'; EDGE = '#898781'; SEP = '#B4B2A9'

def esc(s): return html.escape(str(s), quote=False)

class S:
    def __init__(self, pid, title, desc):
        self.pid, self.title, self.desc = pid, title, desc
        self.el = []
    # ---- primitives
    def text(self, x, y, s, size=14, anchor='start', fill=INK, bold=False):
        w = ' font-weight="600"' if bold else ''
        self.el.append('<text x="%s" y="%s" font-size="%d" text-anchor="%s" fill="%s"%s dominant-baseline="central">%s</text>'
                       % (x, y, size, anchor, fill, w, esc(s)))
    def line(self, x1, y1, x2, y2, stroke=EDGE, sw=1.5, dash=None):
        d = ' stroke-dasharray="%s"' % dash if dash else ''
        self.el.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s/>' % (x1, y1, x2, y2, stroke, sw, d))
    def sep(self, y, x1=40, x2=640):
        self.line(x1, y, x2, y, SEP, 1, '4 4')
    def path(self, d, stroke=EDGE, sw=1.5, dash=None, marker='g'):
        da = ' stroke-dasharray="%s"' % dash if dash else ''
        m = ' marker-end="url(#%s-a%s)"' % (self.pid, marker) if marker else ''
        self.el.append('<path d="%s" fill="none" stroke="%s" stroke-width="%s"%s%s/>' % (d, stroke, sw, da, m))
    def rect(self, x, y, w, h, role='norm', rx=4, sw=1, dash=None, fill=None):
        f, s, _ = ROLE[role]
        if fill: f = fill
        da = ' stroke-dasharray="%s"' % dash if dash else ''
        self.el.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x, y, w, h, rx, f, s, sw, da))
    def node(self, x, y, role, l1, l2=None, ring=False, r=19):
        f, s, t = ROLE[role]
        da = ' stroke-dasharray="3 3"' if role == 'out' else ''
        self.el.append('<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" stroke-width="1"%s/>' % (x, y, r, f, s, da))
        if l2 is None:
            self.text(x, y, l1, 16, 'middle', t)
        else:
            self.text(x, y - 6, l1, 14, 'middle', t)
            self.text(x, y + 8, l2, 12, 'middle', t)
        if ring:
            self.el.append('<circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-width="2.5"/>' % (x, y, r + 4, RING))
    # ---- tree
    def positions(self, n, cx, cy, dxs=(0, 32, 22, 14), ystep=34):
        pos = []
        for i in range(n):
            if i == 0:
                pos.append((cx, cy)); continue
            p = (i - 1) // 2
            d = (i + 1).bit_length() - 1  # depth of i
            dx = dxs[d]
            sign = -1 if i % 2 == 1 else 1
            pos.append((pos[p][0] + sign * dx, cy + ystep * d))
        return pos
    def tree(self, items, cx, cy, new=(), role_of=None, ring=True, dxs=(0, 32, 22, 14), ystep=34, r=19):
        """items: list of (l1,l2) in heap-array order. new: indices drawn green."""
        pos = self.positions(len(items), cx, cy, dxs, ystep)
        for i in range(1, len(items)):
            p = (i - 1) // 2
            self.line(pos[p][0], pos[p][1], pos[i][0], pos[i][1], EDGE, 1.2)
        for i, it in enumerate(items):
            role = 'new' if i in new else 'norm'
            if role_of and i in role_of: role = role_of[i]
            self.node(pos[i][0], pos[i][1], role, it[0], it[1] if len(it) > 1 else None, ring=(ring and i == 0), r=r)
        return pos
    # ---- output
    def render(self, H):
        pid = self.pid
        defs = ('<defs>'
                '<marker id="%s-ag" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#898781" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>'
                '<marker id="%s-ao" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#D85A30" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>'
                '</defs>' % (pid, pid))
        return ('<svg width="100%%" viewBox="0 0 680 %d" role="img" xmlns="http://www.w3.org/2000/svg" font-family=\'%s\'>'
                '<title>%s</title><desc>%s</desc>%s<rect x="0" y="0" width="680" height="%d" fill="#FFFFFF"/>\n%s\n</svg>\n'
                % (H, FONT, esc(self.title), esc(self.desc), defs, H, "\n".join(self.el)))

def legend(s, y, items, x0=40):
    """items: list of (kind, label, width) kind in new/pop/norm/ring/out"""
    x = x0
    for kind, label, w in items:
        if kind == 'ring':
            s.el.append('<circle cx="%d" cy="%d" r="7" fill="none" stroke="%s" stroke-width="2.5"/>' % (x + 8, y, RING))
        else:
            f, st, _ = ROLE[kind]
            da = ' stroke-dasharray="3 3"' if kind == 'out' else ''
            s.el.append('<circle cx="%d" cy="%d" r="7" fill="%s" stroke="%s" stroke-width="1"%s/>' % (x + 8, y, f, st, da))
        s.text(x + 22, y, label, 12, 'start', SUB)
        x += w

def trace_rows(s, y, rows, c1=220, c2=350, calc_x=440, in_arrow=True, k_note=None, pop_label='pop'):
    """rows: dicts with keys
       box: list of text lines; items1,new1; popped: None|dict(node=(l1,l2), lines=[...]);
       items2,new2; noop: [lines]; calc: [(text,bold)]
       Returns y after all rows."""
    for ri, r in enumerate(rows):
        y0 = y
        n = max(len(r.get('items1', [])), len(r.get('items2', [])), 1)
        L = 1
        while (1 << L) - 1 < n: L += 1
        cy = y0 + 72
        h_tree = 72 + 34 * (L - 1) + 22 + 14
        h = max(h_tree, 100)
        if r.get('popped'): h = max(h, 176)
        # box
        bl = r['box']
        s.rect(40, y0 + 8, 64, 50, 'norm', 4, 1, fill='#FFFFFF')
        ys = {1: [33], 2: [25, 42], 3: [19, 34, 49]}[len(bl)]
        for t, yy in zip(bl, ys):
            s.text(72, y0 + yy, t, 14, 'middle', INK)
        # tree1
        it1 = r.get('items1', [])
        if it1:
            s.tree(it1, c1, cy, new=r.get('new1', ()), ring=True)
            if in_arrow:
                s.path('M104 %d L%d %d L%d %d' % (y0 + 33, c1, y0 + 33, c1, cy - 24), EDGE, 1.5)
        elif r.get('empty1'):
            s.text(c1, cy, r['empty1'], 14, 'middle', SUB)
        # popped
        p = r.get('popped')
        if p:
            s.path('M%d %d L66 %d L66 %d' % (c1 - 24, cy, cy, y0 + 92), DASH, 1.5, '5 4', 'o')
            s.text((c1 - 24 + 66) / 2 + 6, cy - 10, pop_label, 12, 'middle', '#712B13')
            s.node(66, y0 + 112, 'pop', p['node'][0], p['node'][1] if len(p['node']) > 1 else None)
            for j, t in enumerate(p['lines']):
                s.text(40, y0 + 142 + 16 * j, t, 12, 'start', '#712B13')
        # tree2 / noop
        it2 = r.get('items2')
        if it2:
            s.tree(it2, c2, cy, new=r.get('new2', ()), ring=True)
        elif it2 is not None:
            s.text(c2, cy, r.get('empty2', '空'), 14, 'middle', SUB)
        if r.get('noop'):
            for j, t in enumerate(r['noop']):
                s.text(300, cy - 6 + 16 * j, t, 14, 'start', INK)
        # calc
        cy0 = y0 + 40
        for j, c in enumerate(r['calc']):
            t, b = (c if isinstance(c, tuple) else (c, False))
            s.text(calc_x, cy0 + 20 * j, t, 14, 'start', INK, bold=b)
        y = y0 + h
        s.sep(y)
        y += 0
    return y
