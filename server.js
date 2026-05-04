require('dotenv').config();
const path = require('path');
const express = require('express');
const session = require('express-session');
const cookieParser = require('cookie-parser');
const { createIamProvider } = require('./iam');
const authRoutes = require('./routes/auth');
const requireAuth = require('./middleware/requireAuth');

const app = express();
const PORT = process.env.PORT || 3000;

const iam = createIamProvider();

app.use(express.json());
app.use(cookieParser());
app.use(session({
  secret: process.env.SESSION_SECRET || 'dev-secret-change-me',
  resave: false,
  saveUninitialized: false,
  cookie: {
    httpOnly: true,
    sameSite: 'lax',
    secure: process.env.NODE_ENV === 'production',
    maxAge: 1000 * 60 * 60 * 8,
  },
}));

app.use(express.static(path.join(__dirname, 'public')));
app.use('/api/auth', authRoutes(iam));

app.get('/dashboard', requireAuth, (_req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'dashboard.html'));
});

app.get('/healthz', (_req, res) => res.json({ ok: true, provider: process.env.IAM_PROVIDER || 'auth0' }));

app.listen(PORT, () => {
  console.log(`SSO server listening on http://localhost:${PORT}`);
  console.log(`IAM provider: ${process.env.IAM_PROVIDER || 'auth0'}`);
});
