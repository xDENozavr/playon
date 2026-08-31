/* ── Auth page elements ── */
const authTabs      = document.getElementById('auth-tabs');
const authSuccess   = document.getElementById('auth-success');
const passInput     = document.getElementById('r-password');
const strengthWrap  = document.getElementById('strength-wrap');
const strengthLabel = document.getElementById('strength-label');
const btnRegister   = document.getElementById('btn-register');
const btnLogin      = document.getElementById('btn-login');

const segs = [1, 2, 3, 4].map(i => document.getElementById('seg' + i));

/* ── Tab switching ── */
function switchTab(name) {
  document.querySelectorAll('.auth-tab').forEach(t =>
    t.classList.toggle('active', t.dataset.tab === name)
  );
  document.querySelectorAll('.auth-form-wrap').forEach(f =>
    f.classList.toggle('active', f.id === 'form-' + name)
  );
  if (authSuccess) authSuccess.classList.remove('show');
}

document.querySelectorAll('.auth-tab').forEach(tab => {
  tab.addEventListener('click', () => switchTab(tab.dataset.tab));
});

document.querySelectorAll('[data-goto]').forEach(btn => {
  btn.addEventListener('click', () => switchTab(btn.dataset.goto));
});

/* ── Show / hide password ── */
document.querySelectorAll('.toggle-pass').forEach(btn => {
  btn.addEventListener('click', () => {
    const input = document.getElementById(btn.dataset.target);
    if (!input) return;
    const isPass = input.type === 'password';
    input.type = isPass ? 'text' : 'password';
    btn.textContent = isPass ? '🙈' : '👁';
  });
});

/* ── Password strength indicator ── */
if (passInput && strengthWrap) {
  const levels = [
    { label: 'Very weak', cls: 'weak',   count: 1 },
    { label: 'Weak',      cls: 'weak',   count: 2 },
    { label: 'Medium',    cls: 'medium', count: 3 },
    { label: 'Strong',    cls: 'strong', count: 4 },
  ];

  passInput.addEventListener('input', () => {
    const v = passInput.value;
    strengthWrap.classList.toggle('show', v.length > 0);
    if (!v) return;

    let score = 0;
    if (v.length >= 8)                       score++;
    if (/[A-Z]/.test(v))                     score++;
    if (/[0-9]/.test(v))                     score++;
    if (/[!@#$%^&*()_+\-=\[\]{}]/.test(v))   score++;

    const lvl = levels[Math.max(0, score - 1)];
    segs.forEach((s, i) => {
      if (s) {
        s.className = 'strength-seg';
        if (i < lvl.count) s.classList.add(lvl.cls);
      }
    });
    if (strengthLabel) strengthLabel.textContent = lvl.label;
  });
}

/* ── Helper: field validation ── */
function validate(id, errId, condition) {
  const input = document.getElementById(id);
  if (!input) return true;
  const err = document.getElementById(errId);
  const ok = condition(input.value.trim());
  input.classList.toggle('error', !ok);
  if (err) err.classList.toggle('show', !ok);
  return ok;
}

/* ── Success screen ── */
function showSuccess(msg) {
  document.querySelectorAll('.auth-form-wrap').forEach(f => f.classList.remove('active'));
  if (authTabs) {
    authTabs.style.opacity = '0';
    authTabs.style.pointerEvents = 'none';
  }
  const successMsg = document.getElementById('success-msg');
  if (successMsg) successMsg.textContent = msg;
  if (authSuccess) authSuccess.classList.add('show');
}

/* ── Helper: read CSRF token from cookie ── */
function getCsrf() {
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  return match ? match[1] : '';
}

/* ══════════════════════════════════════
   REGISTRATION
══════════════════════════════════════ */
if (btnRegister) {
  btnRegister.addEventListener('click', () => {
    const p1 = document.getElementById('r-password')?.value || '';
    const p2 = document.getElementById('r-password2')?.value || '';

    const ok = [
      validate('r-firstname', 'err-firstname', v => v.length >= 2),
      validate('r-lastname',  'err-lastname',  v => v.length >= 2),
      validate('r-email',     'err-email',     v => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)),
      validate('r-password',  'err-password',  v => v.length >= 8),
      (() => {
        const match = p1 === p2;
        const input2 = document.getElementById('r-password2');
        const err2   = document.getElementById('err-password2');
        if (input2) input2.classList.toggle('error', !match);
        if (err2)   err2.classList.toggle('show', !match);
        return match;
      })(),
    ].every(Boolean);

    if (!ok) return;

    // Collect form data
    const form = document.getElementById('form-register');
    const data = new FormData(form);

    // Disable the button while the request is in progress
    btnRegister.disabled = true;
    btnRegister.textContent = 'Please wait...';

    fetch(form.action, {
      method: 'POST',
      headers: { 'X-CSRFToken': getCsrf() },
      body: data,
    })
      .then(r => r.json())
      .then(response => {
        if (response.status === 'success') {
          const name = document.getElementById('r-firstname')?.value.trim() || '';
          showSuccess(`${name}, your account has been created! Check your inbox - we've sent a confirmation email.`);

          // Redirect after 2 seconds
          setTimeout(() => {
            window.location.href = response.redirect || '/';
          }, 2000);
        } else {
          // Show error from the server
          alert(response.message || 'Something went wrong');
          btnRegister.disabled = false;
          btnRegister.textContent = 'Sign up →';
        }
      })
      .catch(() => {
        alert('Connection error');
        btnRegister.disabled = false;
        btnRegister.textContent = 'Sign up →';
      });
  });
}

/* ══════════════════════════════════════
   LOGIN
══════════════════════════════════════ */
if (btnLogin) {
  btnLogin.addEventListener('click', () => {
    const ok = [
      validate('l-email',    'err-l-email',    v => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)),
      validate('l-password', 'err-l-password', v => v.length >= 1),
    ].every(Boolean);

    if (!ok) return;

    const form = document.getElementById('form-login');
    const data = new FormData(form);

    btnLogin.disabled = true;
    btnLogin.textContent = 'Please wait...';

    fetch(form.action, {
      method: 'POST',
      headers: { 'X-CSRFToken': getCsrf() },
      body: data,
    })
      .then(r => r.json())
      .then(response => {
        if (response.status === 'success') {
          showSuccess('You have signed in successfully. Welcome!');

          setTimeout(() => {
            window.location.href = response.redirect || '/';
          }, 1500);
        } else {
          // Show error under the email field
          const errEl = document.getElementById('err-l-email');
          if (errEl) {
            errEl.textContent = response.message || 'Invalid email or password';
            errEl.classList.add('show');
          }
          document.getElementById('l-email')?.classList.add('error');
          btnLogin.disabled = false;
          btnLogin.textContent = 'Sign in →';
        }
      })
      .catch(() => {
        alert('Connection error');
        btnLogin.disabled = false;
        btnLogin.textContent = 'Sign in →';
      });
  });
}

/* ── Clear errors on focus ── */
document.querySelectorAll('.field input').forEach(input => {
  input.addEventListener('focus', () => {
    input.classList.remove('error');
    const errEl = input.closest('.field')?.querySelector('.field-error');
    if (errEl) errEl.classList.remove('show');
  });
});