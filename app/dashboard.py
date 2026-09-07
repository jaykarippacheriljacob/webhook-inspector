"""The live dashboard page, served at / by main.py."""

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>Webhook Inspector</title>
<style>
  :root{--bg:#0f1720;--card:#18222e;--line:#26333f;--ink:#e6edf3;--soft:#93a3b2;--accent:#37c4d6;--ok:#54cc8d;}
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace}
  header{padding:20px 24px;border-bottom:1px solid var(--line);display:flex;align-items:center;gap:14px;flex-wrap:wrap}
  h1{font-size:18px;margin:0}
  .dot{width:9px;height:9px;border-radius:50%;background:var(--ok);box-shadow:0 0 0 4px rgba(84,204,141,.15)}
  .hint{color:var(--soft);font-size:12.5px}
  .hint code{color:var(--accent);background:#0c1219;padding:1px 6px;border-radius:5px}
  main{max-width:900px;margin:0 auto;padding:20px 24px}
  .empty{color:var(--soft);text-align:center;padding:60px 0}
  .req{background:var(--card);border:1px solid var(--line);border-radius:10px;margin-bottom:12px;overflow:hidden}
  .req-top{display:flex;gap:10px;align-items:center;padding:10px 14px;border-bottom:1px solid var(--line);flex-wrap:wrap}
  .m{font-weight:700;padding:2px 8px;border-radius:5px;font-size:12px}
  .m.POST{background:#123324;color:var(--ok)} .m.GET{background:#122a3a;color:#6ea9e8}
  .m.DELETE{background:#341613;color:#f0776c} .m.PUT,.m.PATCH{background:#32270f;color:#e2a850}
  .path{color:var(--ink)} .id{color:var(--soft);margin-left:auto;font-size:12px}
  .time{color:var(--soft);font-size:12px}
  pre{margin:0;padding:12px 14px;white-space:pre-wrap;word-break:break-word;font-size:12.5px;color:var(--soft)}
  .k{color:var(--accent)}
</style>
</head>
<body>
<header>
  <span class="dot"></span>
  <h1>Webhook Inspector</h1>
  <span class="hint">Send a request to <code>POST /webhook</code> and it appears below · polling every 2s</span>
</header>
<main><div id="list"><div class="empty">Waiting for the first request…</div></div></main>
<script>
const esc = s => String(s).replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
async function tick(){
  try{
    const r = await fetch('/requests?limit=25');
    const {requests} = await r.json();
    const el = document.getElementById('list');
    if(!requests.length){ el.innerHTML = '<div class="empty">Waiting for the first request…</div>'; return; }
    el.innerHTML = requests.map(q => `
      <div class="req">
        <div class="req-top">
          <span class="m ${esc(q.method)}">${esc(q.method)}</span>
          <span class="path">${esc(q.path)}</span>
          <span class="time">${esc(q.received_at)}</span>
          <span class="id">${esc(q.id)}</span>
        </div>
        <pre><span class="k">headers</span> ${esc(JSON.stringify(q.headers))}
<span class="k">query</span>   ${esc(JSON.stringify(q.query))}
<span class="k">body</span>    ${esc(q.body || '(empty)')}</pre>
      </div>`).join('');
  }catch(e){ /* ignore transient errors */ }
}
tick(); setInterval(tick, 2000);
</script>
</body>
</html>
"""