async function load() {
  try {
    const res = await fetch('/api/auth/me', { credentials: 'same-origin' });
    if (!res.ok) {
      window.location.href = '/';
      return;
    }
    const { user } = await res.json();
    document.getElementById('profile').innerHTML = `
      <div><strong>Name:</strong> ${user.name || '-'}</div>
      <div><strong>Email:</strong> ${user.email || '-'}</div>
      <div><strong>Subject:</strong> ${user.sub || '-'}</div>
      <div><strong>Email verified:</strong> ${user.emailVerified ? 'Yes' : 'No'}</div>
    `;
  } catch (_e) {
    window.location.href = '/';
  }
}

document.getElementById('logout').addEventListener('click', async () => {
  await fetch('/api/auth/logout', { method: 'POST', credentials: 'same-origin' });
  window.location.href = '/';
});

load();
