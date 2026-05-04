const Auth0Provider = require('./Auth0Provider');
const MockProvider = require('./MockProvider');

function createIamProvider(env = process.env) {
  const provider = (env.IAM_PROVIDER || 'auth0').toLowerCase();

  switch (provider) {
    case 'auth0':
      return new Auth0Provider({
        domain: env.AUTH0_DOMAIN,
        clientId: env.AUTH0_CLIENT_ID,
        clientSecret: env.AUTH0_CLIENT_SECRET,
        audience: env.AUTH0_AUDIENCE,
        connection: env.AUTH0_CONNECTION || 'Username-Password-Authentication',
        scope: env.AUTH0_SCOPE || 'openid profile email offline_access',
      });
    case 'mock':
      return new MockProvider();
    default:
      throw new Error(`Unknown IAM_PROVIDER: ${provider}`);
  }
}

module.exports = { createIamProvider };
