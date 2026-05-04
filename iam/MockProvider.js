const crypto = require('crypto');
const IamProvider = require('./IamProvider');

/**
 * In-memory provider used for local demos and tests when an Auth0
 * tenant is not configured. Demonstrates the abstraction: the rest of
 * the app does not know or care that this is not Auth0.
 */
class MockProvider extends IamProvider {
  constructor() {
    super();
    this.users = new Map([
      ['demo@example.com', { password: 'demo1234', name: 'Demo User', sub: 'mock|1' }],
    ]);
    this.tokens = new Map();
  }

  _issue(user) {
    const accessToken = crypto.randomBytes(24).toString('hex');
    const refreshToken = crypto.randomBytes(24).toString('hex');
    this.tokens.set(accessToken, user);
    this.tokens.set(refreshToken, user);
    return { accessToken, refreshToken, idToken: accessToken, expiresIn: 3600, tokenType: 'Bearer' };
  }

  async login(username, password) {
    const user = this.users.get(username);
    if (!user || user.password !== password) {
      const e = new Error('Invalid email or password');
      e.status = 401;
      throw e;
    }
    return this._issue(user);
  }

  async getUser(accessToken) {
    const user = this.tokens.get(accessToken);
    if (!user) {
      const e = new Error('Invalid token');
      e.status = 401;
      throw e;
    }
    return { sub: user.sub, email: [...this.users.entries()].find(([, u]) => u === user)[0], name: user.name, emailVerified: true };
  }

  async refresh(refreshToken) {
    const user = this.tokens.get(refreshToken);
    if (!user) {
      const e = new Error('Invalid refresh token');
      e.status = 401;
      throw e;
    }
    return this._issue(user);
  }

  async logout(refreshToken) {
    this.tokens.delete(refreshToken);
  }
}

module.exports = MockProvider;
