// 用法: node build/render_check.js docs/02-two-pointers.html out.png
// 截全页图, 并报告 .code 横向溢出和 svg 内 text 超出 viewBox 的情况。
const { chromium } = require('playwright');
(async () => {
  const [file, png] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 900, height: 1000 } });
  await p.goto('file://' + require('path').resolve(file));
  const r = await p.evaluate(() => {
    const over = [...document.querySelectorAll('.code')]
      .filter(e => e.scrollWidth > e.clientWidth + 1).length;
    const bad = [];
    document.querySelectorAll('figure svg').forEach((s, i) => {
      const vb = s.viewBox.baseVal;
      s.querySelectorAll('text').forEach(t => {
        const bb = t.getBBox();
        if (bb.x < vb.x - 1 || bb.y < vb.y - 1 || bb.x + bb.width > vb.x + vb.width + 1 ||
            bb.y + bb.height > vb.y + vb.height + 1) bad.push(`svg#${i}: "${t.textContent.slice(0, 30)}"`);
      });
    });
    return { codeOverflow: over, textOutOfViewBox: bad, svgs: document.querySelectorAll('figure svg').length };
  });
  console.log(JSON.stringify(r, null, 1));
  if (png) await p.screenshot({ path: png, fullPage: true });
  await b.close();
})();
