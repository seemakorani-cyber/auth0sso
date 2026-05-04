/**
 * Abstract IAM provider contract. Any concrete provider (Auth0, Okta,
 * Cognito, Keycloak, ...) implements these methods. The rest of the
 * application talks only to this interface, so swapping the IAM only
 * requires writing a new adapter and updating the factory.
 */
class IamProvider {
  async login(_username, _password) {
    throw new Error('login() not implemented');
  }

  async getUser(_accessToken) {
    throw new Error('getUser() not implemented');
  }

  async refresh(_refreshToken) {
    throw new Error('refresh() not implemented');
  }

  async logout(_refreshToken) {
    throw new Error('logout() not implemented');
  }
}

module.exports = IamProvider;
