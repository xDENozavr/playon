document.addEventListener('DOMContentLoaded', function() {

  // Tabs
  document.querySelectorAll('.pc-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.pc-tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.pc-tab-content').forEach(c => c.classList.remove('active'));
      tab.classList.add('active');
      document.getElementById('tab-' + tab.dataset.tab).classList.add('active');
    });
  });

  // Save
  const btnSave = document.getElementById('btn-save');
  if (btnSave) {
    btnSave.addEventListener('click', () => {
      const toast = document.getElementById('toast');
      toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 2800);
    });
  }

  // Cancel - reset fields
  const originals = {};
  document.querySelectorAll('.pc-tab-content input:not([disabled])').forEach(inp => {
    originals[inp.id] = inp.value;
  });
  const btnCancel = document.getElementById('btn-cancel');
  if (btnCancel) {
    btnCancel.addEventListener('click', () => {
      Object.entries(originals).forEach(([id, val]) => {
        const el = document.getElementById(id);
        if (el) el.value = val;
      });
    });
  }

  // Avatar - open file picker via the pencil button, auto-submit on selection
  const avatarInput = document.getElementById('avatar-input');
  if (avatarInput) {
    avatarInput.addEventListener('change', function() {
      if (this.files.length > 0) {
        const form = document.getElementById('avatar-form');
        if (form) form.submit();
      }
    });
  }

});