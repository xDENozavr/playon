/* ── Modal window elements ── */
const overlay    = document.getElementById('modal-overlay');
const modal      = document.getElementById('modal');
const modalClose = document.getElementById('modal-close');
const formWrap   = document.getElementById('modal-form-wrap');
const loginWrap  = document.getElementById('modal-login-wrap');
const successEl  = document.getElementById('modal-success');
const submitBtn  = document.getElementById('form-submit');
const loginBtn   = document.getElementById('login-submit');
const tabs       = document.getElementById('modal-tabs');

/* ── Reset modal fields ── */
function resetModal() {
  if (formWrap)  formWrap.style.display  = 'block';
  if (loginWrap) loginWrap.style.display = 'none';
  if (successEl) successEl.classList.remove('show');

  document.querySelectorAll('.modal-tab').forEach((t, i) => t.classList.toggle('active', i === 0));

  ['f-team','f-captain','f-email','f-phone','f-comment','l-email','l-pass'].forEach(id => {
    const el = document.getElementById(id);
    if (el) { el.value = ''; el.style.borderColor = ''; }
  });
}

/* ── Open the modal ── */
function openModal(btn) {
  const mType  = document.getElementById('modal-type');
  const mTitle = document.getElementById('modal-title');
  const mMeta  = document.getElementById('modal-meta');

  if (mType)  mType.textContent  = btn.dataset.type  || '';
  if (mTitle) mTitle.textContent = btn.dataset.title || '';
  if (mMeta) {
    mMeta.textContent = (btn.dataset.date || '') + '  ·  ' + (btn.dataset.place || '');
  }

  resetModal();
  if (overlay) overlay.classList.add('open');
  document.body.style.overflow = 'hidden';
  if (modal) modal.scrollTop = 0;
}

/* ── Close the modal ── */
function closeModal() {
  if (overlay) overlay.classList.remove('open');
  document.body.style.overflow = '';
}

/* ── Modal event listeners ── */
document.addEventListener('click', e => {
  const btn = e.target.closest('.ec-reg-btn, .eli-btn');
  if (btn && !btn.disabled) openModal(btn);
});

if (modalClose) modalClose.addEventListener('click', closeModal);

if (overlay) {
  overlay.addEventListener('click', e => {
    if (e.target === overlay) closeModal();
  });

  /* Restore the tabs after closing */
  overlay.addEventListener('transitionend', () => {
    if (!overlay.classList.contains('open') && tabs) tabs.style.display = '';
  });
}

document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeModal();
});

/* ── Tab switching (New application / Sign in) ── */
if (tabs) {
  tabs.addEventListener('click', e => {
    const tab = e.target.closest('.modal-tab');
    if (!tab) return;
    document.querySelectorAll('.modal-tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    const isLogin = tab.dataset.tab === 'login';
    if (formWrap)  formWrap.style.display  = isLogin ? 'none'  : 'block';
    if (loginWrap) loginWrap.style.display = isLogin ? 'block' : 'none';
  });
}

/* ── Submit new application ── */
if (submitBtn) {
  submitBtn.addEventListener('click', () => {
    const team    = document.getElementById('f-team')?.value.trim();
    const captain = document.getElementById('f-captain')?.value.trim();
    const email   = document.getElementById('f-email')?.value.trim();

    [['f-team', team], ['f-captain', captain], ['f-email', email]].forEach(([id, val]) => {
      const el = document.getElementById(id);
      if (el) el.style.borderColor = val ? '' : 'var(--red)';
    });

    if (!team || !captain || !email) return;

    if (formWrap)  formWrap.style.display = 'none';
    if (tabs)      tabs.style.display = 'none';
    if (successEl) successEl.classList.add('show');

    const successText = document.getElementById('success-text');
    if (successText) {
      successText.innerHTML = `Team <strong>${team}</strong> has been registered.<br>A confirmation will be sent to ${email}.`;
    }
  });
}

/* ── Sign in for already registered teams ── */
if (loginBtn) {
  loginBtn.addEventListener('click', () => {
    const email = document.getElementById('l-email')?.value.trim();
    const pass  = document.getElementById('l-pass')?.value.trim();

    [['l-email', email], ['l-pass', pass]].forEach(([id, val]) => {
      const el = document.getElementById(id);
      if (el) el.style.borderColor = val ? '' : 'var(--red)';
    });

    if (!email || !pass) return;

    if (loginWrap) loginWrap.style.display = 'none';
    if (tabs)      tabs.style.display = 'none';
    if (successEl) successEl.classList.add('show');

    const successText = document.getElementById('success-text');
    if (successText) {
      successText.innerHTML = `Application submitted.<br>A confirmation will be sent to ${email}.`;
    }
  });
}

/* ── View switch: Grid / List ── */
const viewBtns = document.querySelectorAll('.view-btn');
if (viewBtns.length > 0) {
  viewBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      viewBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      document.body.className = document.body.className
        .replace(/view-\w+/, '').trim() + ' view-' + btn.dataset.view;
    });
  });
}

/* ── Filter by event type ── */
const typeBtns = document.querySelectorAll('.type-btn');
if (typeBtns.length > 0) {
  typeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      typeBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const type = btn.dataset.type;

      document.querySelectorAll('.event-card, .event-list-item').forEach(card => {
        card.style.display = (type === 'all' || card.dataset.type === type) ? '' : 'none';
      });

      document.querySelectorAll('.month-group').forEach(group => {
        const hasVisible = [...group.querySelectorAll('.event-card, .event-list-item')]
          .some(c => c.style.display !== 'none');
        group.style.display = hasVisible ? '' : 'none';
      });
    });
  });
}