let currentStep = 1;
    const totalSteps = 3;
    let selectedDiscipline = 'basketball';

/* ── Basketball / Streetball switch ── */
const teamTypeCheckbox = document.getElementById('w-team-type');
document.querySelectorAll('.discipline-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.discipline-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    selectedDiscipline = btn.dataset.discipline;
    teamTypeCheckbox.checked = (selectedDiscipline === 'basketball');
  });
});

/* ── Custom category dropdown ── */
const realSelect    = document.getElementById('w-category');
const customSelect  = document.getElementById('category-custom-select');
const trigger       = document.getElementById('category-trigger');
const optionsBox    = document.getElementById('category-options');

trigger.addEventListener('click', () => {
  customSelect.classList.toggle('open');
});

optionsBox.querySelectorAll('.custom-select-option').forEach(opt => {
  opt.addEventListener('click', () => {
    realSelect.value = opt.dataset.value;

    trigger.textContent = opt.textContent;
    trigger.classList.remove('placeholder', 'error');
    trigger.appendChild(Object.assign(document.createElement('span'), {
      className: 'custom-select-arrow',
      textContent: '▾'
    }));

    optionsBox.querySelectorAll('.custom-select-option').forEach(o => o.classList.remove('selected'));
    opt.classList.add('selected');

    customSelect.classList.remove('open');
  });
});

document.addEventListener('click', (e) => {
  if (!customSelect.contains(e.target)) {
    customSelect.classList.remove('open');
  }
});

/* ── Step navigation ── */
function goToStep(n) {
  if (n < 1 || n > totalSteps) return;
  currentStep = n;

  document.querySelectorAll('.wizard-step-content').forEach(c =>
    c.classList.toggle('active', +c.dataset.content === n)
  );
  document.querySelectorAll('.step').forEach(s => {
    const num = +s.dataset.step;
    s.classList.toggle('active', num === n);
    s.classList.toggle('done', num < n);
  });
  document.querySelectorAll('.step-line').forEach(l => {
    l.classList.toggle('filled', +l.dataset.line < n);
  });

  if (n === totalSteps) updateSummary();
}

document.querySelectorAll('[data-next]').forEach(btn => {
  btn.addEventListener('click', () => {
    if (currentStep === 1) {
      const name = document.getElementById('w-name').value.trim();
      const category = realSelect.value;

      if (!name) { document.getElementById('w-name').focus(); return; }
      if (!category) {
        trigger.classList.add('error');
        return;
      }
    }
    goToStep(currentStep + 1);
  });
});
document.querySelectorAll('[data-back]').forEach(btn => {
  btn.addEventListener('click', () => goToStep(currentStep - 1));
});

/* ── Summary on the last step ── */
function updateSummary() {
  document.getElementById('summary-name').textContent =
    document.getElementById('w-name').value.trim() || '—';
  document.getElementById('summary-discipline').textContent =
    selectedDiscipline === 'streetball' ? 'Streetball 3×3' : 'Basketball 5×5';
  document.getElementById('summary-category').textContent =
    trigger.textContent.trim() || '—';
}