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
    document.getElementById('btn-save').addEventListener('click', () => {
      const toast = document.getElementById('toast');
      toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 2800);
    });

    // Cancel — reset fields
    const originals = {};
    document.querySelectorAll('.pc-tab-content input:not([disabled])').forEach(inp => {
      originals[inp.id] = inp.value;
    });
    document.getElementById('btn-cancel').addEventListener('click', () => {
      Object.entries(originals).forEach(([id, val]) => {
        const el = document.getElementById(id);
        if (el) el.value = val;
      });
    });