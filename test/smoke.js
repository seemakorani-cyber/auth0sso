// Smoke test: spins up the server with the mock IAM provider and exercises
// login -> /me -> logout. No external network required.
process.env.IAM_PROVIDER = 'mock';
process.env.SESSION_SECRET = 'test-secret';
process.env.PORT = '0';

const http = require('http');
const path = require('path');
const express = require('express');
const session = require('express-session');
const cookieParser = require('cookie-parser');
const { createIamProvider } = require('../iam');
const authRoutes = require('../routes/auth');

const app = express();
app.use(express.json());
app.use(cookieParser());
app.use(session({ secret: 'test', resave: false, saveUninitialized: false }));
app.use('/api/auth', authRoutes(createIamProvider()));
app.use(express.static(path.join(__dirname, '..', 'public')));

const server = http.createServer(app).listen(0, async () => {
  const port = server.address().port;
  const base = `http://127.0.0.1:${port}`;
  const jar = [];

  const fetchWithCookies = async (url, opts = {}) => {
    const headers = { ...(opts.headers || {}) };
    if (jar.length) headers.Cookie = jar.join('; ');
    const res = await fetch(url, { ...opts, headers });
    const setCookie = res.headers.getSetCookie ? res.headers.getSetCookie() : (res.headers.raw?.()['set-cookie'] || []);
    setCookie.forEach((c) => jar.push(c.split(';')[0]));
    return res;
  };

  let failed = 0;
  const assert = (cond, msg) => { if (!cond) { failed++; console.error('  FAIL:', msg); } else { console.log('  ok  ', msg); } };

  console.log('SMOKE: login with bad creds');
  let res = await fetchWithCookies(`${base}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: 'demo@example.com', password: 'wrong' }),
  });
  assert(res.status === 401, 'rejects bad password with 401');

  console.log('SMOKE: login with good creds');
  res = await fetchWithCookies(`${base}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: 'demo@example.com', password: 'demo1234' }),
  });
  assert(res.status === 200, 'accepts good password with 200');
  const body = await res.json();
  assert(body.user && body.user.email === 'demo@example.com', 'returns user profile');

  console.log('SMOKE: GET /me with session');
  res = await fetchWithCookies(`${base}/api/auth/me`);
  assert(res.status === 200, '/me returns 200 when logged in');

  console.log('SMOKE: logout');
  res = await fetchWithCookies(`${base}/api/auth/logout`, { method: 'POST' });
  assert(res.status === 200, 'logout returns 200');

  console.log('SMOKE: /me after logout');
  jar.length = 0;
  res = await fetchWithCookies(`${base}/api/auth/me`);
  assert(res.status === 401, '/me returns 401 after logout');

  server.close();
  if (failed) {
    console.error(`\n${failed} assertion(s) failed`);
    process.exit(1);
  } else {
    console.log('\nAll smoke tests passed.');
  }
});
