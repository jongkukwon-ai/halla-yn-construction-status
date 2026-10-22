-- 영남지사 Cloudflare D1 표 구조 (계정 자료는 넣지 않음 — _server/cloudflare_seed.sql 은 저장소 밖에서만 보관)
CREATE TABLE IF NOT EXISTS store (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS audit (ts TEXT NOT NULL, actor TEXT NOT NULL, action TEXT NOT NULL, detail TEXT);
CREATE TABLE IF NOT EXISTS reviews (key TEXT PRIMARY KEY, value TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'draft');
