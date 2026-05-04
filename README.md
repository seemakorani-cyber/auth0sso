# auth0sso — Backend-driven SSO with a swappable IAM

A small Node.js / Express app that authenticates users against Auth0 **without
showing the Auth0 hosted UI**. The login form is served by this app and the
backend talks to Auth0's REST API directly. The IAM is hidden behind an
abstract `IamProvider` so a future swap (Okta, Cognito, Keycloak, ...) only
requires writing a new adapter.

```
+-----------+     POST /api/auth/login      +---------+   /oauth/token        +-------+
|  Browser  |  ───────────────────────────▶ | Express | ────────────────────▶ | Auth0 |
| (custom   |  ◀───────────────────────────  | server  | ◀────────────────────  | (API) |
|  HTML)    |     httpOnly session cookie   +---------+   tokens + userinfo   +-------+
+-----------+
```

## Why this layout

- **No Auth0 UI**: `/oauth/token` with the password-realm grant is called from
  the backend; the user never leaves the app.
- **Tokens stay server-side**: access / refresh tokens live in the session
  store, never in the browser.
- **Swappable IAM**: every provider implements `iam/IamProvider.js`. The
  factory in `iam/index.js` selects a provider via the `IAM_PROVIDER`
  environment variable (`auth0` or `mock`).

## Run

```bash
npm install
cp .env.example .env          # fill in AUTH0_* values
npm start
# open http://localhost:3000
```

To try it without an Auth0 tenant, use the mock provider:

```bash
IAM_PROVIDER=mock SESSION_SECRET=dev npm start
# login: demo@example.com / demo1234
```

## Auth0 setup

1. Create an Auth0 **Regular Web Application**.
2. In *Settings → Advanced → Grant Types*, enable **Password**.
3. In *Tenant Settings → API Authorization Settings*, set a default audience or
   pass `AUTH0_AUDIENCE`.
4. Confirm `AUTH0_CONNECTION` matches your DB connection name
   (default: `Username-Password-Authentication`).

## Endpoints

| Method | Path                | Purpose                              |
|--------|---------------------|--------------------------------------|
| POST   | `/api/auth/login`   | Exchange username/password for a session |
| GET    | `/api/auth/me`      | Current user profile (session-protected) |
| POST   | `/api/auth/refresh` | Rotate access token via refresh token |
| POST   | `/api/auth/logout`  | Revoke refresh token, destroy session |

## Test

```bash
npm test     # runs an in-process smoke test against the mock provider
```
