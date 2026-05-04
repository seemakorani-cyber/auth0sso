const axios = require('axios');
const IamProvider = require('./IamProvider');

class Auth0Provider extends IamProvider {
  constructor(config) {
    super();
    this.domain = config.domain;
    this.clientId = config.clientId;
    this.clientSecret = config.clientSecret;
    this.audience = config.audience;
    this.connection = config.connection;
    this.scope = config.scope;
    this.baseUrl = `https://${this.domain}`;
  }

  async login(username, password) {
    try {
      const { data } = await axios.post(`${this.baseUrl}/oauth/token`, {
        grant_type: 'http://auth0.com/oauth/grant-type/password-realm',
        realm: this.connection,
        username,
        password,
        audience: this.audience,
        scope: this.scope,
        client_id: this.clientId,
        client_secret: this.clientSecret,
      }, { headers: { 'Content-Type': 'application/json' } });

      return {
        accessToken: data.access_token,
        idToken: data.id_token,
        refreshToken: data.refresh_token,
        expiresIn: data.expires_in,
        tokenType: data.token_type,
      };
    } catch (err) {
      const status = err.response?.status || 500;
      const description = err.response?.data?.error_description
        || err.response?.data?.error
        || 'Authentication failed';
      const e = new Error(description);
      e.status = status === 403 ? 401 : status;
      throw e;
    }
  }

  async getUser(accessToken) {
    try {
      const { data } = await axios.get(`${this.baseUrl}/userinfo`, {
        headers: { Authorization: `Bearer ${accessToken}` },
      });
      return {
        sub: data.sub,
        email: data.email,
        emailVerified: data.email_verified,
        name: data.name,
        nickname: data.nickname,
        picture: data.picture,
        updatedAt: data.updated_at,
      };
    } catch (err) {
      const e = new Error('Failed to fetch user profile');
      e.status = err.response?.status || 500;
      throw e;
    }
  }

  async refresh(refreshToken) {
    try {
      const { data } = await axios.post(`${this.baseUrl}/oauth/token`, {
        grant_type: 'refresh_token',
        client_id: this.clientId,
        client_secret: this.clientSecret,
        refresh_token: refreshToken,
      }, { headers: { 'Content-Type': 'application/json' } });
      return {
        accessToken: data.access_token,
        idToken: data.id_token,
        refreshToken: data.refresh_token || refreshToken,
        expiresIn: data.expires_in,
      };
    } catch (err) {
      const e = new Error('Failed to refresh token');
      e.status = err.response?.status || 500;
      throw e;
    }
  }

  async logout(refreshToken) {
    if (!refreshToken) return;
    try {
      await axios.post(`${this.baseUrl}/oauth/revoke`, {
        client_id: this.clientId,
        client_secret: this.clientSecret,
        token: refreshToken,
      }, { headers: { 'Content-Type': 'application/json' } });
    } catch (_err) {
      // Revocation failures should not block local session destruction.
    }
  }
}

module.exports = Auth0Provider;
