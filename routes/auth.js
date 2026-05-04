const express = require('express');
const requireAuth = require('../middleware/requireAuth');

module.exports = function authRoutes(iam) {
  const router = express.Router();

  router.post('/login', async (req, res) => {
    const { username, password } = req.body || {};
    if (!username || !password) {
      return res.status(400).json({ error: 'username and password are required' });
    }
    try {
      const tokens = await iam.login(username, password);
      const user = await iam.getUser(tokens.accessToken);
      req.session.tokens = tokens;
      req.session.user = user;
      return res.json({ user });
    } catch (err) {
      return res.status(err.status || 500).json({ error: err.message });
    }
  });

  router.get('/me', requireAuth, async (req, res) => {
    try {
      const user = req.session.user || await iam.getUser(req.session.tokens.accessToken);
      return res.json({ user });
    } catch (err) {
      return res.status(err.status || 500).json({ error: err.message });
    }
  });

  router.post('/refresh', requireAuth, async (req, res) => {
    try {
      const tokens = await iam.refresh(req.session.tokens.refreshToken);
      req.session.tokens = { ...req.session.tokens, ...tokens };
      return res.json({ ok: true });
    } catch (err) {
      return res.status(err.status || 500).json({ error: err.message });
    }
  });

  router.post('/logout', async (req, res) => {
    const refreshToken = req.session?.tokens?.refreshToken;
    try { await iam.logout(refreshToken); } catch (_err) { /* ignore */ }
    req.session.destroy(() => {
      res.clearCookie('connect.sid');
      res.json({ ok: true });
    });
  });

  return router;
};
