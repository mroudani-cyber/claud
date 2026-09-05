/* ═══════════════════════ ITM PARTNERS · DOSSIER TECHNIQUE — motion */
(() => {
  'use strict';
  const { gsap } = window;
  gsap.registerPlugin(ScrollTrigger, CustomEase);
  const REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const q = (s, c = document) => c.querySelector(s);
  const qa = (s, c = document) => Array.from(c.querySelectorAll(s));
  CustomEase.create('draft', '0.19,1,0.22,1');
  CustomEase.create('snap',  '0.76,0,0.24,1');

  /* ── smooth scroll ─────────────────────────────────────────────── */
  let lenis = null;
  if (!REDUCED && window.Lenis) {
    lenis = new Lenis({ duration: 1.1, lerp: .085, smoothWheel: true });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(t => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
  }
  const goTo = y => lenis ? lenis.scrollTo(y, { duration: 1.3 }) : window.scrollTo({ top: y, behavior: 'smooth' });
  qa('[data-nav]').forEach(a => a.addEventListener('click', e => {
    const t = q(a.getAttribute('href')); if (!t) return;
    e.preventDefault(); goTo(t.getBoundingClientRect().top + scrollY - 60);
  }));

  /* ── split helpers ─────────────────────────────────────────────── */
  function splitChars(el) {
    const walk = node => {
      if (node.nodeType === 3) {
        const frag = document.createDocumentFragment();
        node.textContent.split('').forEach(ch => {
          const s = document.createElement('span');
          s.className = 'ch'; s.textContent = ch === ' ' ? ' ' : ch;
          frag.appendChild(s);
        });
        node.replaceWith(frag);
      } else if (node.nodeType === 1 && node.tagName !== 'BR') {
        Array.from(node.childNodes).forEach(walk);
      }
    };
    Array.from(el.childNodes).forEach(walk);
    return el.querySelectorAll('.ch');
  }
  function splitWords(el) {
    const html = el.innerHTML;
    el.innerHTML = html.split(' ')
      .map(w => `<span class="wd"><i>${w}</i></span>`).join(' ');
    return el.querySelectorAll('.wd i');
  }

  /* ── intro ─────────────────────────────────────────────────────── */
  function intro() {
    const g = q('#introLines');
    if (g) {
      let s = '';
      for (let i = 1; i < 12; i++) s += `<line x1="${i * 100 / 12}" y1="0" x2="${i * 100 / 12}" y2="100"/>`;
      for (let i = 1; i < 8; i++)  s += `<line x1="0" y1="${i * 100 / 8}" x2="100" y2="${i * 100 / 8}"/>`;
      g.innerHTML = s;
    }
    const el = q('#intro');
    const finish = () => { el.remove(); hero(); };
    if (REDUCED) { finish(); return; }
    const lines = qa('#introLines line');
    gsap.set(lines, { scaleY: 0, scaleX: 0, transformOrigin: '50% 50%' });
    const tl = gsap.timeline({ defaults: { ease: 'draft' } });
    tl.to(lines, { scaleY: 1, scaleX: 1, duration: .85, stagger: { each: .018, from: 'center' } })
      .from('.intro__t', { yPercent: 108, duration: 1, ease: 'draft' }, '-=.55')
      .from(['.intro__k', '.intro__s'], { yPercent: 120, opacity: 0, duration: .7, stagger: .07 }, '-=.7')
      .to({}, { duration: .34 })
      .to('.intro__c', { yPercent: -12, opacity: 0, duration: .55, ease: 'snap' })
      .to(lines, { scaleY: 0, scaleX: 0, duration: .5, stagger: { each: .012, from: 'edges' } }, '-=.42')
      .to(el, { opacity: 0, duration: .45, ease: 'power2.inOut' }, '-=.3')
      .add(finish);
  }

  /* ── hero ──────────────────────────────────────────────────────── */
  function hero() {
    const t = q('[data-chars]');
    const chars = splitChars(t);
    const tl = gsap.timeline({ defaults: { ease: 'draft' } });
    tl.from(chars, { yPercent: 118, opacity: 0, duration: .95, stagger: .014 })
      .from('.kicker', { opacity: 0, y: 14, duration: .7 }, .1)
      .from('.hero__lede', { opacity: 0, y: 22, duration: .85 }, .34)
      .from('.hero__meta > div', { opacity: 0, y: 18, duration: .7, stagger: .08 }, .44)
      .from('.hero__btns .pill', { opacity: 0, y: 16, duration: .7, stagger: .08 }, .52)
      .from('.plate', { opacity: 0, y: 40, scale: .97, duration: 1.1 }, .18)
      .from('.hero__stack i', { opacity: 0, x: 16, y: -16, duration: .9, stagger: .07 }, .5)
      .from('.head', { yPercent: -110, duration: .7, clearProps: 'transform' }, .28)
      .add(drawLeaders, .55);

    // plate parallax: image drifts against its frame
    gsap.to('.plate__img img', {
      yPercent: -7, ease: 'none',
      scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true }
    });
    gsap.to('.plate', {
      yPercent: -6, ease: 'none',
      scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true }
    });
    gsap.to('.hero__stack i', {
      yPercent: i => -2 - i * 3, ease: 'none',
      scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true }
    });
    counters();
  }

  function drawLeaders() {
    qa('.plate__lead .ld').forEach(p => {
      const len = p.getTotalLength();
      gsap.set(p, { strokeDasharray: len, strokeDashoffset: len });
      gsap.to(p, { strokeDashoffset: 0, duration: .9, ease: 'draft' });
    });
    gsap.to('.plate__lead .ld-d', { opacity: 1, duration: .3, delay: .75, stagger: .08 });
    gsap.to('.lbl', { opacity: 1, duration: .5, delay: .85, stagger: .1 });
  }

  /* ── word reveals on every section heading ─────────────────────── */
  function headings() {
    qa('[data-words]').forEach(h => {
      const words = splitWords(h);
      gsap.from(words, {
        yPercent: 112, duration: .9, ease: 'draft', stagger: .05,
        scrollTrigger: { trigger: h, start: 'top 88%', once: true }
      });
    });
    qa('.sec-h .num, .sec-h__x').forEach(el => gsap.from(el, {
      opacity: 0, y: 16, duration: .8, ease: 'draft',
      scrollTrigger: { trigger: el, start: 'top 92%', once: true }
    }));
  }

  /* ── fiche rows: clip-path wipe (distinct from Forge's line masks) */
  function fiche() {
    qa('.fr').forEach((r, i) => gsap.from(r, {
      clipPath: 'inset(0 100% 0 0)', opacity: 0, duration: .85, ease: 'snap', delay: i * .045,
      scrollTrigger: { trigger: r, start: 'top 92%', once: true }
    }));
  }

  /* ── sheet stack: each sheet shrinks as the next climbs over it ─── */
  function sheets() {
    const list = qa('.sheet');
    list.forEach((s, i) => {
      const next = list[i + 1];
      gsap.from(s, {
        y: 70, opacity: 0, duration: 1, ease: 'draft',
        scrollTrigger: { trigger: s, start: 'top 92%', once: true }
      });
      gsap.fromTo(s.querySelector('.sheet__r img'), { yPercent: -6 }, {
        yPercent: 6, ease: 'none',
        scrollTrigger: { trigger: s, start: 'top bottom', end: 'bottom top', scrub: true }
      });
      if (!next) return;
      // NOTE: animate filter from an explicit brightness(1) — GSAP treats a
      // starting value of `none` as zero, which would flash the sheet black.
      gsap.fromTo(s.querySelector('.sheet__in'),
        { scale: 1, y: 0, filter: 'brightness(1)' },
        {
          scale: .935, y: -18, filter: 'brightness(.94)', ease: 'none',
          scrollTrigger: { trigger: next, start: 'top bottom', end: 'top top', scrub: .5 }
        });
    });
  }

  /* ── exploded axonometric ──────────────────────────────────────── */
  function schema() {
    const layers = qa('.axo .lay');
    const legend = qa('#axoLegend b');
    if (!layers.length) return;
    const desktop = () => !matchMedia('(max-width:1080px)').matches;

    layers.forEach(l => {
      const y = parseFloat(l.dataset.y);
      gsap.fromTo(l, { y: 0, opacity: l.dataset.l === '0' ? 1 : .25 }, {
        y: () => desktop() ? y : y * .5, opacity: 1, ease: 'none',
        scrollTrigger: {
          trigger: '.schema', start: 'top top', end: 'bottom bottom',
          scrub: .6, invalidateOnRefresh: true
        }
      });
    });
    ScrollTrigger.create({
      trigger: '.schema', start: 'top top', end: 'bottom bottom',
      onUpdate(self) {
        const i = Math.min(legend.length - 1, Math.floor(self.progress * legend.length));
        legend.forEach((b, k) => b.classList.toggle('on', k <= i));
      }
    });
    // draw the leader arrows once in view
    qa('.axo .ldr').forEach(p => {
      const len = p.getTotalLength();
      gsap.set(p, { strokeDasharray: len, strokeDashoffset: len });
      gsap.to(p, {
        strokeDashoffset: 0, duration: .8, ease: 'draft',
        scrollTrigger: { trigger: '.schema', start: 'top 60%', once: true }
      });
    });
  }

  /* ── ledger: horizontal drift tied to vertical scroll ──────────── */
  function ledger() {
    const track = q('#ledgerTrack'); if (!track) return;
    const dist = () => Math.max(0, track.scrollWidth - q('#ledger').clientWidth + 40);
    gsap.fromTo(track, { x: 0 }, {
      x: () => -dist(), ease: 'none',
      scrollTrigger: {
        trigger: '.moyens', start: 'top 30%', end: 'bottom bottom',
        scrub: .7, invalidateOnRefresh: true
      }
    });
    gsap.from('.tCell', {
      opacity: 0, y: 26, duration: .85, ease: 'draft', stagger: .08,
      scrollTrigger: { trigger: '.teamRow', start: 'top 88%', once: true }
    });
  }

  function counters() {
    qa('[data-count]').forEach(el => {
      const end = parseFloat(el.dataset.count);
      ScrollTrigger.create({
        trigger: el, start: 'top 92%', once: true,
        onEnter: () => gsap.to({ v: 0 }, {
          v: end, duration: 1.2, ease: 'power2.out',
          onUpdate() { el.textContent = String(Math.round(this.targets()[0].v)).padStart(2, '0'); }
        })
      });
    });
  }

  /* ── méthode + contact + footer ────────────────────────────────── */
  function tail() {
    qa('.mth li').forEach(li => gsap.from(li.children, {
      opacity: 0, y: 26, duration: .85, ease: 'draft', stagger: .06,
      scrollTrigger: { trigger: li, start: 'top 88%', once: true }
    }));
    gsap.from('.cLede, .cBtn', {
      opacity: 0, y: 28, duration: .95, ease: 'draft', stagger: .1,
      scrollTrigger: { trigger: '.cGrid', start: 'top 86%', once: true }
    });
    gsap.from('.cRow', {
      opacity: 0, x: 26, duration: .85, ease: 'draft', stagger: .08,
      scrollTrigger: { trigger: '.cSide', start: 'top 88%', once: true }
    });
    gsap.from('.foot__in > *', {
      opacity: 0, y: 22, duration: .85, ease: 'draft', stagger: .1,
      scrollTrigger: { trigger: '.foot', start: 'top 94%', once: true }
    });
  }

  /* ── marquees ──────────────────────────────────────────────────── */
  function marquees() {
    qa('[data-marq]').forEach(el => {
      el.innerHTML += el.innerHTML;
      const half = () => el.scrollWidth / 2;
      gsap.to(el, {
        x: () => -half(), ease: 'none', duration: 30, repeat: -1,
        modifiers: { x: gsap.utils.unitize(x => gsap.utils.wrap(-half(), 0, parseFloat(x))) }
      });
    });
  }

  /* ── header, rail, crosshair ───────────────────────────────────── */
  function chrome() {
    const head = q('#head');
    ScrollTrigger.create({
      start: 0, end: 'max',
      onUpdate: self => head.classList.toggle('is-solid', self.scroll() > 80)
    });
    qa('#rail b').forEach(b => {
      const t = q(b.dataset.r); if (!t) return;
      ScrollTrigger.create({
        trigger: t, start: 'top 55%', end: 'bottom 45%',
        onToggle: s => b.classList.toggle('on', s.isActive)
      });
      b.style.cursor = 'pointer';
      b.addEventListener('click', () => goTo(t.getBoundingClientRect().top + scrollY - 60));
    });
    q('#rail').setAttribute('aria-hidden', 'false');

    const cr = q('#cross'), pos = q('#crossPos');
    if (cr && !matchMedia('(hover:none)').matches) {
      const xT = gsap.quickTo(cr, 'x', { duration: .35, ease: 'power3' });
      const yT = gsap.quickTo(cr, 'y', { duration: .35, ease: 'power3' });
      let shown = false;
      addEventListener('mousemove', e => {
        if (!shown) { shown = true; gsap.set(cr, { x: e.clientX, y: e.clientY }); gsap.to(cr, { opacity: 1, duration: .3 }); }
        xT(e.clientX); yT(e.clientY);
        pos.textContent = String(Math.round(e.clientX)).padStart(3, '0') + ' · ' +
                          String(Math.round(e.clientY + scrollY)).padStart(3, '0');
      }, { passive: true });

    }
    // subtle tilt on the hero plate
    const plate = q('[data-tilt]');
    if (plate && !REDUCED && !matchMedia('(hover:none)').matches) {
      const rx = gsap.quickTo(plate, 'rotationX', { duration: .8, ease: 'power3' });
      const ry = gsap.quickTo(plate, 'rotationY', { duration: .8, ease: 'power3' });
      gsap.set(plate, { transformPerspective: 1100 });
      plate.addEventListener('mousemove', e => {
        const r = plate.getBoundingClientRect();
        ry(((e.clientX - (r.left + r.width / 2)) / r.width) * 7);
        rx(-((e.clientY - (r.top + r.height / 2)) / r.height) * 7);
      });
      plate.addEventListener('mouseleave', () => { rx(0); ry(0); });
    }
  }

  function init() {
    headings(); fiche(); sheets(); schema(); ledger(); tail(); marquees(); chrome();
    ScrollTrigger.refresh();
  }

  document.fonts.ready.then(() => {
    intro(); init();
    addEventListener('load', () => ScrollTrigger.refresh());
    setTimeout(() => ScrollTrigger.refresh(), 900);
  });
  let rt; addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(() => ScrollTrigger.refresh(), 220); });
  window.__itm = { goTo, get lenis() { return lenis; } };
})();
