// ── Scroll-reveal on scroll ──
const revealEls = document.querySelectorAll('.reveal');
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      setTimeout(() => entry.target.classList.add('visible'), i * 80);
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

revealEls.forEach(el => observer.observe(el));


// ── News slider ──
const track   = document.getElementById('news-track');
const dotsEl  = document.getElementById('news-dots');
const btnPrev = document.getElementById('news-prev');
const btnNext = document.getElementById('news-next');

if (track && dotsEl && btnPrev && btnNext) {
  const cards   = track.querySelectorAll('.news-card');
  const total   = cards.length;
  if (total > 0) {
    const perView    = window.innerWidth < 700 ? 1 : 3;
    const maxSlide   = total - perView;
    let   current    = 0;

    const dots = [];
    for (let i = 0; i <= maxSlide; i++) {
      const d = document.createElement('button');
      d.className = 'news-dot' + (i === 0 ? ' active' : '');
      d.setAttribute('aria-label', `Slide ${i + 1}`);
      d.addEventListener('click', () => goTo(i));
      dotsEl.appendChild(d);
      dots.push(d);
    }

    function goTo(idx) {
      current = Math.max(0, Math.min(idx, maxSlide));
      const cardW = cards[0].offsetWidth + 24; 
      track.style.transform = `translateX(-${current * cardW}px)`;
      dots.forEach((d, i) => d.classList.toggle('active', i === current));
      btnPrev.disabled = current === 0;
      btnNext.disabled = current === maxSlide;
    }

    btnPrev.addEventListener('click', () => goTo(current - 1));
    btnNext.addEventListener('click', () => goTo(current + 1));
    btnPrev.disabled = true;
    goTo(0);

    window.addEventListener('resize', () => goTo(current));
  }
}