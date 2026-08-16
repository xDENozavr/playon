/* ── Card animation on page load ── */
const sectionsGrid = document.querySelectorAll('.sections-grid');

if (sectionsGrid.length > 0) {
  requestAnimationFrame(() => {
    sectionsGrid.forEach(grid => grid.classList.add('loaded'));
  });
}