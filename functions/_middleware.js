/* ═══════════════════════════════════════════════════════════════
   Cloudflare Pages 로그인·계정관리 (로컬 _server/serve.py 와 같은 API)

   - 로그인 자체는 Cloudflare Access(회사 메일 인증코드)가 처리하고,
     여기서는 Access가 넘겨준 서명(JWT)을 확인해 메일 주소로 구성원 계정을 찾습니다.
   - 계정·권한등급은 D1 데이터베이스(바인딩 이름 DB)의 store 표에 JSON 하나로 저장합니다.
     구조는 로컬 _server/accounts.json 과 같습니다(공개 저장소에는 올리지 않음).
   - 필요한 환경변수: ACCESS_TEAM_DOMAIN (예: halla-yn.cloudflareaccess.com), ACCESS_AUD (Access 앱의 AUD 태그)
═══════════════════════════════════════════════════════════════ */

// 권한 목록 — serve.py 의 PERMISSIONS 와 같게 유지
const PERMISSIONS = [
  { key: 'view',                   label: '정보 조회',          desc: '착공현황·뉴스·통계 등 기본 화면' },
  { key: 'weekly_review_write',    label: '주간리뷰 작성',      desc: '자기 영업소 주간리뷰 작성·수정' },
  { key: 'weekly_review_read_all', label: '주간리뷰 전체 열람', desc: '모든 영업소 주간리뷰 열람' },
  { key: 'monthly_review_attend',  label: '월간 대면리뷰 참석', desc: '월간 대면리뷰 자료 제출·열람' },
  { key: 'monthly_review_host',    label: '월간 대면리뷰 주관', desc: '대면리뷰 일정·안건 관리, 전체 자료 열람' },
];
const PERM_KEYS = new Set(PERMISSIONS.map(p => p.key));

// 배포 폴더에 같이 올라가지만 내보내지 않는 파일
const DENY_PREFIX = ['/functions', '/_server', '/.github', '/scratchpad', '/cloudflare'];
const DENY_EXT = ['.py', '.md', '.xlsx', '.xls', '.sql', '.toml', '.log', '.pyc'];

class UserError extends Error {}

/* ── Access 서명 확인 ─────────────────────────────────────────── */
let certCache = { at: 0, keys: [] };

const b64url = s => Uint8Array.from(atob(s.replace(/-/g, '+').replace(/_/g, '/') + '==='.slice((s.length + 3) % 4)), c => c.charCodeAt(0));
const b64json = s => JSON.parse(new TextDecoder().decode(b64url(s)));

async function accessEmail(request, env) {
  const token = request.headers.get('Cf-Access-Jwt-Assertion');
  if (!token) {
    // 내 PC에서 wrangler 로 시험할 때만: DEV_EMAIL 로 로그인한 것으로 간주
    const host = new URL(request.url).hostname;
    return env.DEV_EMAIL && (host === 'localhost' || host === '127.0.0.1') ? env.DEV_EMAIL.toLowerCase() : null;
  }
  const [h, p, sig] = token.split('.');
  if (!h || !p || !sig) return null;
  const header = b64json(h), payload = b64json(p);
  const team = 'https://' + env.ACCESS_TEAM_DOMAIN;
  if (Date.now() - certCache.at > 3600_000 || !certCache.keys.some(k => k.kid === header.kid)) {
    const r = await fetch(team + '/cdn-cgi/access/certs');
    certCache = { at: Date.now(), keys: (await r.json()).keys || [] };
  }
  const jwk = certCache.keys.find(k => k.kid === header.kid);
  if (!jwk) return null;
  const key = await crypto.subtle.importKey('jwk', jwk, { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' }, false, ['verify']);
  const ok = await crypto.subtle.verify('RSASSA-PKCS1-v1_5', key, b64url(sig), new TextEncoder().encode(h + '.' + p));
  const aud = [].concat(payload.aud || []);
  if (!ok || payload.iss !== team || !aud.includes(env.ACCESS_AUD) || payload.exp * 1000 < Date.now()) return null;
  return String(payload.email || '').toLowerCase() || null;
}

/* ── 저장소(D1) ───────────────────────────────────────────────── */
async function loadDoc(env) {
  const row = await env.DB.prepare('SELECT value FROM store WHERE key = ?').bind('accounts').first();
  return row ? JSON.parse(row.value) : { version: 1, roles: [], accounts: [] };
}

async function saveDoc(env, doc) {
  await env.DB.prepare('INSERT INTO store (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value')
    .bind('accounts', JSON.stringify(doc)).run();
}

async function audit(env, actor, action, detail) {
  const ts = new Date(Date.now() + 9 * 3600_000).toISOString().replace('T', ' ').slice(0, 19); // 한국시간
  await env.DB.prepare('INSERT INTO audit (ts, actor, action, detail) VALUES (?, ?, ?, ?)')
    .bind(ts, actor, action, JSON.stringify(detail)).run();
}

/* ── 계정관리 검증 (serve.py 와 같은 규칙) ─────────────────────── */
const normEmp = v => String(v ?? '').replace(/\s+/g, '').toUpperCase();

function publicAccount(a, roles) {
  const role = roles.find(r => r.id === a.role);
  return {
    id: a.id, name: a.name, title: a.title, email: a.email,
    role: a.role, role_name: role ? role.name : '', level: role ? role.level : 0,
    perms: role ? role.perms : [], admin: !!a.admin,
  };
}

function cleanAccount(body, roles) {
  const a = {
    title: String(body.title ?? '').trim(),
    name: String(body.name ?? '').trim(),
    emp_no: normEmp(body.emp_no),
    email: String(body.email ?? '').trim().toLowerCase(),
    phone: String(body.phone ?? '').trim(),
    role: String(body.role ?? '').trim(),
    admin: !!body.admin,
    active: body.active === undefined ? true : !!body.active,
  };
  if (!a.title || !a.name || !a.emp_no) throw new UserError('직책·이름·사번은 꼭 입력해야 합니다.');
  if (!/^[A-Z0-9-]{3,20}$/.test(a.emp_no)) throw new UserError('사번은 영문·숫자로 3~20자입니다. (예: P13187)');
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(a.email)) throw new UserError('이메일을 확인해 주세요. (회사 메일로 로그인합니다)');
  if (!roles.some(r => r.id === a.role)) throw new UserError('권한등급을 골라 주세요.');
  return a;
}

function checkRules(accounts) {
  const act = accounts.filter(a => a.active);
  for (const [field, label] of [['emp_no', '사번'], ['email', '이메일'], ['title', '직책']]) {
    const seen = {};
    for (const a of act) {
      if (seen[a[field]]) throw new UserError(`${label} ${a[field]}이(가) ${seen[a[field]]}, ${a.title}에 겹칩니다.`);
      seen[a[field]] = a.title;
    }
  }
  if (!act.some(a => a.admin)) throw new UserError('관리자는 최소 1명 있어야 합니다.');
}

function cleanRole(body) {
  const r = {
    name: String(body.name ?? '').trim(),
    level: parseInt(body.level, 10) || 0,
    perms: (body.perms || []).filter(p => PERM_KEYS.has(p)),
  };
  if (!r.name) throw new UserError('권한등급 이름을 입력해 주세요.');
  return r;
}

/* ── 응답 도우미 ──────────────────────────────────────────────── */
const json = (code, obj) => new Response(JSON.stringify(obj), {
  status: code, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' },
});

const page = (code, title, msg) => new Response(`<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>영남지사</title>
<style>body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;background:#0a0d0c;color:#eee;
font-family:"Pretendard","Apple SD Gothic Neo",system-ui,sans-serif;text-align:center;padding:16px}
h1{font-size:20px;font-weight:500}p{color:#999;line-height:1.7}a{color:#4ED690}</style></head>
<body><div><h1>${title}</h1><p>${msg}</p><p><a href="/cdn-cgi/access/logout">다른 메일로 로그인</a></p></div></body></html>`,
  { status: code, headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' } });

/* ── API ──────────────────────────────────────────────────────── */
async function api(request, env, path, acc, doc) {
  const method = request.method;
  if (method === 'GET') {
    if (path === '/api/me') return json(200, publicAccount(acc, doc.roles));
    if (path === '/api/admin/data') {
      if (!acc.admin) return json(403, { error: '관리자만 볼 수 있습니다.' });
      return json(200, { roles: doc.roles, accounts: doc.accounts, permissions: PERMISSIONS, me: acc.id });
    }
    return json(404, { error: '없는 주소입니다.' });
  }
  // 다른 사이트에서 몰래 보내는 요청 차단
  if (request.headers.get('X-Requested-With') !== 'yn') return json(403, { error: '잘못된 요청입니다.' });
  if (path === '/api/logout' && method === 'POST') return json(200, { ok: true, redirect: '/cdn-cgi/access/logout' });
  if (!acc.admin) return json(403, { error: '관리자만 바꿀 수 있습니다.' });

  const m = path.match(/^\/api\/admin\/(accounts|roles)(?:\/([\w-]+))?$/);
  if (!m) return json(404, { error: '없는 주소입니다.' });
  const [, kind, oid] = m;
  const body = method === 'DELETE' ? {} : await request.json().catch(() => ({}));
  const { roles, accounts } = doc;
  const actor = `${acc.name}(${acc.emp_no})`;
  let log;

  if (kind === 'accounts') {
    if (method === 'POST' && !oid) {
      const a = cleanAccount(body, roles);
      a.id = 'a' + (Math.max(0, ...accounts.map(x => parseInt(x.id.slice(1), 10) || 0)) + 1);
      a.order = Math.max(0, ...accounts.map(x => x.order || 0)) + 1;
      accounts.push(a);
      checkRules(accounts);
      log = ['계정 추가', { title: a.title, name: a.name, emp_no: a.emp_no, email: a.email, role: a.role, admin: a.admin }];
    } else {
      const cur = accounts.find(x => x.id === oid);
      if (!cur) return json(404, { error: '계정을 찾을 수 없습니다.' });
      if (method === 'DELETE') {
        accounts.splice(accounts.indexOf(cur), 1);
        checkRules(accounts);
        log = ['계정 삭제', { title: cur.title, name: cur.name, emp_no: cur.emp_no }];
      } else if (method === 'PUT') {
        const next = cleanAccount(body, roles);
        const changed = {};
        for (const k in next) if (cur[k] !== next[k]) changed[k] = [cur[k], next[k]];
        Object.assign(cur, next);
        checkRules(accounts);
        // 이메일을 바꾸면 이전 담당자는 다음 요청부터 바로 '등록되지 않은 메일'이 됨(매 요청마다 계정표 확인)
        log = ['계정 수정', { title: cur.title, changed }];
      } else return json(405, { error: '허용되지 않는 요청입니다.' });
    }
  } else {
    if (method === 'POST' && !oid) {
      const r = cleanRole(body);
      const base = String(body.id || '').toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_|_$/g, '') || 'role';
      let rid = base, n = 2;
      while (roles.some(x => x.id === rid)) rid = `${base}_${n++}`;
      r.id = rid;
      roles.push(r);
      log = ['권한등급 추가', r];
    } else {
      const cur = roles.find(x => x.id === oid);
      if (!cur) return json(404, { error: '권한등급을 찾을 수 없습니다.' });
      if (method === 'DELETE') {
        const users = accounts.filter(a => a.role === oid).map(a => a.title);
        if (users.length) throw new UserError('이 등급을 쓰는 계정이 있어 지울 수 없습니다: ' + users.join(', '));
        roles.splice(roles.indexOf(cur), 1);
        log = ['권한등급 삭제', { id: oid, name: cur.name }];
      } else if (method === 'PUT') {
        const next = cleanRole(body);
        log = ['권한등급 수정', { id: oid, before: { name: cur.name, level: cur.level, perms: cur.perms }, after: next }];
        Object.assign(cur, next);
      } else return json(405, { error: '허용되지 않는 요청입니다.' });
    }
  }
  await saveDoc(env, doc);
  await audit(env, actor, ...log);
  return json(200, { ok: true });
}

/* ── 모든 요청의 입구 ─────────────────────────────────────────── */
export async function onRequest(context) {
  const { request, env, next } = context;
  const url = new URL(request.url);
  const path = decodeURIComponent(url.pathname);
  const low = path.toLowerCase();

  if (DENY_PREFIX.some(p => low.startsWith(p)) || DENY_EXT.some(e => low.endsWith(e)) || path.includes('/~$')) {
    return new Response('Not Found', { status: 404 });
  }

  const email = await accessEmail(request, env);
  if (!email) return page(403, '로그인이 필요합니다', '회사 메일 인증을 거쳐 들어와 주세요.');

  const doc = await loadDoc(env);
  const acc = doc.accounts.find(a => a.active && String(a.email || '').toLowerCase() === email);
  if (!acc) return page(403, '등록되지 않은 메일입니다', `${email} 은(는) 영남지사 구성원 계정에 없습니다.<br>관리자에게 계정 등록을 요청해 주세요.`);

  if (path.startsWith('/api/')) {
    try {
      return await api(request, env, path, acc, doc);
    } catch (e) {
      if (e instanceof UserError) return json(400, { error: e.message });
      throw e;
    }
  }
  if (path === '/login.html') return Response.redirect(url.origin + '/', 302);
  if (path === '/admin.html' && !acc.admin) return Response.redirect(url.origin + '/', 302);

  const res = await next();
  if ((res.headers.get('Content-Type') || '').includes('text/html')) {
    const out = new Response(res.body, res);
    out.headers.set('Cache-Control', 'no-store'); // 로그아웃 뒤 뒤로가기로 화면이 보이지 않게
    return out;
  }
  return res;
}
