// Live course games: shared database layer + helpers.
// Uses Firebase Realtime Database when window.LIVE_CONFIG.firebase is set,
// otherwise a local demo store (same browser only, for rehearsal/testing).
(function () {
  const CFG = window.LIVE_CONFIG || {};
  const ROOT = 'kse/' + (CFG.room || 'course1') + '/';
  const FB = 'https://www.gstatic.com/firebasejs/10.12.2/';
  const TS_LOCAL = { '.sv': 'timestamp' };

  function localApi() {
    const KEY = 'live-db-' + ROOT;
    const bc = 'BroadcastChannel' in window ? new BroadcastChannel(KEY) : null;
    const subs = [];
    const load = () => { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; } };
    const split = p => (ROOT + p).split('/').filter(Boolean);
    const getAt = (tree, parts) => parts.reduce((n, k) => (n == null ? undefined : n[k]), tree);
    const fix = v => (v && typeof v === 'object' && v['.sv'] === 'timestamp') ? Date.now()
      : (v && typeof v === 'object' ? Object.fromEntries(Object.entries(v).map(([k, x]) => [k, fix(x)])) : v);
    const write = (p, v, merge) => {
      const tree = load(), parts = split(p);
      let n = tree;
      for (let i = 0; i < parts.length - 1; i++) { if (typeof n[parts[i]] !== 'object' || n[parts[i]] === null) n[parts[i]] = {}; n = n[parts[i]]; }
      const last = parts[parts.length - 1];
      if (merge) {
        if (typeof n[last] !== 'object' || n[last] === null) n[last] = {};
        for (const [k, x] of Object.entries(v)) {
          const sub = k.split('/'); let m = n[last];
          for (let i = 0; i < sub.length - 1; i++) { if (typeof m[sub[i]] !== 'object' || m[sub[i]] === null) m[sub[i]] = {}; m = m[sub[i]]; }
          if (x === null) delete m[sub[sub.length - 1]]; else m[sub[sub.length - 1]] = fix(x);
        }
      } else if (v === null) delete n[last]; else n[last] = fix(v);
      localStorage.setItem(KEY, JSON.stringify(tree));
      notify(); if (bc) bc.postMessage(1);
    };
    const notify = () => { const tree = load(); subs.forEach(s => s.cb(clone(getAt(tree, split(s.p))))); };
    const clone = v => v === undefined ? null : JSON.parse(JSON.stringify(v));
    window.addEventListener('storage', e => { if (e.key === KEY) notify(); });
    if (bc) bc.onmessage = notify;
    return {
      mode: 'local',
      on(p, cb) { const s = { p, cb }; subs.push(s); setTimeout(() => cb(clone(getAt(load(), split(p)))), 0); return () => subs.splice(subs.indexOf(s), 1); },
      async get(p) { return clone(getAt(load(), split(p))); },
      async set(p, v) { write(p, v, false); },
      async update(p, v) { write(p, v, true); },
      push(p, v) { const k = Date.now().toString(36) + Math.random().toString(36).slice(2, 7); write(p + '/' + k, v, false); return k; },
      async remove(p) { write(p, null, false); },
      TS: TS_LOCAL,
      offset(cb) { cb(0); },
      conn(cb) { cb(true); },
    };
  }

  async function firebaseApi() {
    const { initializeApp } = await import(FB + 'firebase-app.js');
    const d = await import(FB + 'firebase-database.js');
    const app = initializeApp(CFG.firebase);
    const rdb = d.getDatabase(app);
    const R = p => d.ref(rdb, ROOT + p);
    return {
      mode: 'firebase',
      on(p, cb) { return d.onValue(R(p), s => cb(s.val())); },
      async get(p) { return (await d.get(R(p))).val(); },
      set(p, v) { return d.set(R(p), v); },
      update(p, v) { return d.update(R(p), v); },
      push(p, v) { return d.push(R(p), v).key; },
      remove(p) { return d.remove(R(p)); },
      TS: d.serverTimestamp(),
      offset(cb) { d.onValue(d.ref(rdb, '.info/serverTimeOffset'), s => cb(s.val() || 0)); },
      conn(cb) { d.onValue(d.ref(rdb, '.info/connected'), s => cb(!!s.val())); },
    };
  }

  let apiP = null;
  const LIVE = {
    db() { return apiP || (apiP = CFG.firebase ? firebaseApi() : Promise.resolve(localApi())); },
    T: 20, // seconds per question
    points(dt, ok) { if (!ok) return 0; const x = Math.min(Math.max(dt / 1000 / LIVE.T, 0), 1); return Math.round(1000 * (1 - x / 2)); },
    esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])); },
    COLORS: ['#E8505B', '#2F7DE1', '#F2A900', '#2FA36B'],
    LETTERS: ['A', 'B', 'C', 'D'],
    // Score a quiz set from its answers. returns {players:{pid:pts}, teams:[{tid,name,avg,total,n}]}
    score(set, ans, starts, players, teams) {
      const S = window.LIVE_SETS[set]; const P = {};
      if (!S) return { players: P, teams: [] };
      S.qs.forEach((q, i) => {
        const a = (ans && ans[i]) || {}, st = starts && starts[i];
        for (const [pid, r] of Object.entries(a)) {
          P[pid] = (P[pid] || 0) + (st ? LIVE.points(r.t - st, r.a === q.c) : 0);
        }
      });
      const T = {};
      for (const [pid, p] of Object.entries(players || {})) {
        if (!p.team || !(teams || {})[p.team]) continue;
        const t = T[p.team] || (T[p.team] = { tid: p.team, name: teams[p.team].name, total: 0, n: 0 });
        t.total += P[pid] || 0; t.n++;
      }
      const list = Object.values(T).map(t => Object.assign(t, { avg: Math.round(t.total / Math.max(t.n, 1)) })).sort((a, b) => b.avg - a.avg);
      return { players: P, teams: list };
    },
    cupTotals(cup, teams) {
      return Object.entries(teams || {}).map(([tid, t]) => {
        const ev = (cup && cup[tid]) || {};
        return { tid, name: t.name, pts: Object.values(ev).reduce((a, b) => a + (+b || 0), 0), ev };
      }).sort((a, b) => b.pts - a.pts);
    },
    // shrink a photo to a small JPEG data URL
    shrink(file, max = 900, q = 0.72) {
      return new Promise((res, rej) => {
        const img = new Image(), url = URL.createObjectURL(file);
        img.onload = () => {
          const k = Math.min(1, max / Math.max(img.width, img.height));
          const c = document.createElement('canvas'); c.width = Math.round(img.width * k); c.height = Math.round(img.height * k);
          c.getContext('2d').drawImage(img, 0, 0, c.width, c.height); URL.revokeObjectURL(url);
          res(c.toDataURL('image/jpeg', q));
        };
        img.onerror = rej; img.src = url;
      });
    },
  };
  window.LIVE = LIVE;
})();
