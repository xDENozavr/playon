const sections = document.querySelectorAll('.rule-section');
    const tocItems = document.querySelectorAll('.toc-item');

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const id = entry.target.id;
          tocItems.forEach(item => {
            item.classList.toggle('active', item.getAttribute('href') === '#' + id);
          });
        }
      });
    }, { rootMargin: '-20% 0px -70% 0px', threshold: 0 });

    sections.forEach(sec => observer.observe(sec));

    document.querySelectorAll('.reveal').forEach(el => {
      new IntersectionObserver(entries => {
        entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
      }, { threshold: 0.06 }).observe(el);
    });