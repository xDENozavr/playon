/* ── Team data ── */
    const TEAMS = {
      'bears': {
        name: 'Bears',
        wins: 5, losses: 7, pts: 10, diff: '−55',
        players: [
          { num: 14, name: 'Serhii Popkov', cap: true,  pts: 16.3 },
          { num:  5, name: 'Oleksii Turov', cap: false, pts: 11.5 },
          { num: 27, name: 'Borys Sharov', cap: false, pts:  9.8 },
          { num: 36, name: 'Taras Hrytsenko', cap: false, pts:  8.4 },
          { num: 49, name: 'Kyrylo Medvediev', cap: false, pts:  7.1 },
          { num: 19, name: 'Leonid Ivashchenko', cap: false, pts:  5.5 },
        ]
      }
    };

    /* ── Elements ── */
    const overlay    = document.getElementById('drawer-overlay');
    const drawer     = document.getElementById('drawer');
    const drawerName = document.getElementById('drawer-name');
    const drawerStats= document.getElementById('drawer-stats');
    const drawerPl   = document.getElementById('drawer-players');
    const closeBtn   = document.getElementById('drawer-close');
    const grid       = document.getElementById('teams-grid');

    /* ── Open the drawer ── */
    function openDrawer(teamId) {
      const t = TEAMS[teamId];
      if (!t) return;

      drawerName.textContent = t.name;

      drawerStats.innerHTML = `
        <div class="dts-item">
          <span class="dts-val red">${t.wins}</span>
          <span class="dts-key">Wins</span>
        </div>
        <div class="dts-item">
          <span class="dts-val">${t.losses}</span>
          <span class="dts-key">Losses</span>
        </div>
        <div class="dts-item">
          <span class="dts-val red">${t.pts}</span>
          <span class="dts-key">Points (AVG)</span>
        </div>
      `;

      drawerPl.innerHTML = t.players.map(p => `
        <div class="player-row">
          <span class="pr-num">${p.num}</span>
          <div class="pr-info">
            <span class="pr-name">
              ${p.name}
              ${p.cap ? '<span class="pr-cap">C</span>' : ''}
            </span>
          </div>
          <div class="pr-stats">
            <div>
              <span class="pr-stat-val">${p.pts}</span>
              <span class="pr-stat-key">Pts</span>
            </div>
          </div>
        </div>
      `).join('');

      overlay.classList.add('open');
      drawer.classList.add('open');
      document.body.style.overflow = 'hidden';
      drawer.scrollTop = 0;
    }

    /* ── Close the drawer ── */
    function closeDrawer() {
      overlay.classList.remove('open');
      drawer.classList.remove('open');
      document.body.style.overflow = '';
    }

    /* ── Card clicks ── */
    grid.addEventListener('click', e => {
      const card = e.target.closest('.team-card');
      if (card) openDrawer(card.dataset.team);
    });

    closeBtn.addEventListener('click', closeDrawer);
    overlay.addEventListener('click', closeDrawer);

    /* Close on Escape */
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') closeDrawer();
    });

    /* ── Spotlight effect on cards ── */
    grid.addEventListener('mousemove', e => {
      const card = e.target.closest('.team-card');
      if (!card) return;
      const rect = card.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width * 100).toFixed(1) + '%';
      const y = ((e.clientY - rect.top)  / rect.height * 100).toFixed(1) + '%';
      card.style.setProperty('--mx', x);
      card.style.setProperty('--my', y);
    });

    /* ── Age filter ── */
    const ageFilter = document.getElementById('age-filter');
    ageFilter.addEventListener('change', () => {
      const val = ageFilter.value;
      ageFilter.classList.toggle('filtered', val !== 'all');
      grid.querySelectorAll('.team-card').forEach(card => {
        const teamCategories = card.dataset.age.split(',');
        const show = val === 'all' || teamCategories.includes(val);
        card.style.display = show ? '' : 'none';
      });
    });

    /* ── Sort filters ── */
    const filterBtns = document.querySelectorAll('.filter-btn');
    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        const cards = [...grid.querySelectorAll('.team-card')];
        const sort  = btn.dataset.sort;

        cards.sort((a, b) => {
          if (sort === 'rank') {
            return parseInt(a.querySelector('.tc-bg-num').textContent)
                 - parseInt(b.querySelector('.tc-bg-num').textContent);
          }
          if (sort === 'wins') {
            return parseInt(b.querySelector('.tc-stat-val').textContent)
                 - parseInt(a.querySelector('.tc-stat-val').textContent);
          }
          if (sort === 'name') {
            return a.querySelector('.tc-name').textContent
              .localeCompare(b.querySelector('.tc-name').textContent, 'en');
          }
          return 0;
        });

        cards.forEach(c => grid.appendChild(c));
      });
    });

    /* Kick off the grid animation */
    requestAnimationFrame(() => grid.classList.add('loaded'));