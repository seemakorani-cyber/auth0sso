module.exports = function requireAuth(req, res, next) {
  if (req.session && req.session.tokens && req.session.tokens.accessToken) {
    return next();
  }
  return res.status(401).json({ error: 'Not authenticated' });
};
