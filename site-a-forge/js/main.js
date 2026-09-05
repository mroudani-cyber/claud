/* ════════════════════════════════ ITM PARTNERS · FORGE — motion engine */
(() => {
  'use strict';
  const { gsap } = window;
  gsap.registerPlugin(ScrollTrigger, CustomEase, ScrollToPlugin);

  const REDUCED = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const q  = (s, c = document) => c.querySelector(s);
  const qa = (s, c = document) => Array.from(c.querySelectorAll(s));

  CustomEase.create('forge', '0.16,1,0.30,1');
  CustomEase.create('steel', '0.65,0,0.35,1');

  /* ── smooth scroll ─────────────────────────────────────────────── */
  let lenis = null;
  if (!REDUCED && window.Lenis) {
    lenis = new Lenis({ duration: 1.05, lerp: 0.09, wheelMultiplier: 1, smoothWheel: true });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(t => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
  }
  const scrollTo = y => lenis ? lenis.scrollTo(y, { duration: 1.25 })
                             : window.scrollTo({ top: y, behavior: 'smooth' });

  qa('[data-nav]').forEach(a => a.addEventListener('click', e => {
    const t = q(a.getAttribute('href'));
    if (!t) return;
    e.preventDefault();
    scrollTo(t.getBoundingClientRect().top + window.scrollY);
  }));

  /* ── preloader ─────────────────────────────────────────────────── */
  function bootLoader() {
    const loader = q('#loader'), num = q('#loaderNum'), fill = q('#loaderFill');
    const bars = qa('.loader__bars span');
    const done = () => { loader.remove(); document.body.classList.add('is-ready'); heroIntro(); };
    if (REDUCED) { done(); return; }

    const counter = { v: 0 };
    const tl = gsap.timeline({ defaults: { ease: 'steel' } });
    tl.from('.loader__mark', { yPercent: 115, duration: .8, ease: 'forge' })
      .from('.loader__meta', { opacity: 0, y: 14, duration: .6 }, '-=.55')
      .to(counter, {
        v: 100, duration: 1.15, ease: 'power1.inOut',
        onUpdate: () => {
          const n = Math.round(counter.v);
          num.textContent = String(n).padStart(3, '0');
          fill.style.width = n + '%';
        }
      }, '-=.5')
      .to('.loader__inner', { yPercent: -18, opacity: 0, duration: .6, ease: 'forge' })
      .to(bars, { yPercent: -101, duration: .82, ease: 'forge', stagger: { each: .06, from: 'start' } }, '-=.32')
      .add(done);
  }

  /* ── hero intro ────────────────────────────────────────────────── */
  function heroIntro() {
    const tl = gsap.timeline({ defaults: { ease: 'forge' } });
    tl.from('.hero__title .line__i', { yPercent: 112, duration: 1.15, stagger: .085 })
      .from('.hero__eyebrow', { opacity: 0, y: 16, duration: .7 }, .18)
      .from('.hero__sub p',   { opacity: 0, y: 22, duration: .85 }, .42)
      .from('.hero__actions .btn', { opacity: 0, y: 18, duration: .7, stagger: .08 }, .55)
      .from('.hero__foot',    { opacity: 0, y: 24, duration: .9 }, .62)
      .from('.hero__ghost',   { opacity: 0, scale: 1.14, duration: 1.6, ease: 'power2.out' }, 0)
      .from('.hero__lattice', { opacity: 0, duration: 1.5 }, 0)
      .from('.hero__grid i',  { scaleY: 0, transformOrigin: '50% 0%', duration: 1.1, stagger: .05 }, .2)
      .from('.nav',           { yPercent: -110, duration: .8, clearProps: 'transform' }, .3);
    countUp();
  }

  /* ── numeric counters ──────────────────────────────────────────── */
  function countUp() {
    qa('[data-count]').forEach(el => {
      if (el.hasAttribute('data-plain')) return;
      const end = parseFloat(el.dataset.count);
      ScrollTrigger.create({
        trigger: el, start: 'top 92%', once: true,
        onEnter: () => gsap.to({ v: 0 }, {
          v: end, duration: 1.4, ease: 'power2.out',
          onUpdate() { el.textContent = String(Math.round(this.targets()[0].v)).padStart(2, '0'); }
        })
      });
    });
  }

  /* ── HERO: differential parallax + recession ───────────────────── */
  function heroScroll() {
    const stage = q('#heroStage');
    qa('[data-depth]', q('#hero')).forEach(el => {
      const d = parseFloat(el.dataset.depth);
      gsap.to(el, {
        yPercent: -26 * (1.05 - d), ease: 'none',
        scrollTrigger: { trigger: '#hero', start: 'top top', end: 'bottom top', scrub: true }
      });
    });
    // outgoing section recedes: scale down, blur, dim — the "card slides over" feel
    gsap.to(stage, {
      scale: .90, filter: 'blur(7px) brightness(.44)', ease: 'none',
      scrollTrigger: { trigger: '#hero', start: 'top top', end: 'bottom top', scrub: .5 }
    });
    gsap.to('.hero__content', {
      yPercent: -14, opacity: 0, ease: 'none',
      scrollTrigger: { trigger: '#hero', start: 'top top', end: '58% top', scrub: .4 }
    });
    gsap.to('.hero__foot', {
      opacity: 0, y: 30, ease: 'none',
      scrollTrigger: { trigger: '#hero', start: 'top top', end: '32% top', scrub: .4 }
    });
  }

  /* ── generic: masked line reveals ──────────────────────────────── */
  function lineReveals() {
    qa('.h2, .contact__title').forEach(h => {
      gsap.from(h.querySelectorAll('.line__i'), {
        yPercent: 112, duration: 1.05, ease: 'forge', stagger: .08,
        scrollTrigger: { trigger: h, start: 'top 86%', once: true }
      });
    });
    qa('.tag').forEach(t => gsap.from(t, {
      opacity: 0, x: -18, duration: .8, ease: 'forge',
      scrollTrigger: { trigger: t, start: 'top 92%', once: true }
    }));
  }

  /* ── MANIFESTE: word-by-word opacity scrub ─────────────────────── */
  function manifeste() {
    const el = q('#scrubText');
    const words = el.textContent.trim().split(/\s+/);
    el.innerHTML = words.map(w => `<span class="w">${w}</span>`).join(' ');
    gsap.to(el.querySelectorAll('.w'), {
      opacity: 1, ease: 'none', stagger: .5,
      scrollTrigger: { trigger: '.manifeste', start: 'top top', end: '72% top', scrub: .55 }
    });
    gsap.to('.manifeste__bg img', {
      yPercent: -16, ease: 'none',
      scrollTrigger: { trigger: '.manifeste', start: 'top bottom', end: 'bottom top', scrub: true }
    });
    gsap.from('.manifeste__sign', {
      opacity: 0, y: 22, duration: .9, ease: 'forge',
      scrollTrigger: { trigger: '.manifeste', start: 'top 42%', once: true }
    });
    // the whole panel recedes as the next section climbs over it
    gsap.to('.manifeste__inner', {
      scale: .95, opacity: 0, ease: 'none',
      scrollTrigger: { trigger: '.manifeste', start: '76% top', end: 'bottom top', scrub: .5 }
    });
  }

  /* ── MÉTIERS: pinned horizontal with inner parallax ────────────── */
  function metiers() {
    const track = q('#metiersTrack');
    const pin   = q('#metiersPin');
    const rail  = q('#metiersRail');
    const numEl = q('#panelNum');
    const panels = qa('.panel', track);

    const distance = () => Math.max(0, track.scrollWidth - window.innerWidth);

    const st = ScrollTrigger.create({
      trigger: '.metiers',
      start: 'top top',
      end: () => '+=' + (distance() + window.innerHeight * 0.4),
      pin: pin, pinSpacing: true, scrub: .7, invalidateOnRefresh: true,
      onUpdate(self) {
        const p = self.progress;
        gsap.set(track, { x: -distance() * p });
        rail.style.width = (8 + p * 92) + '%';
        const idx = Math.min(panels.length, Math.floor(p * panels.length) + (p >= 1 ? 0 : 1)) || 1;
        numEl.textContent = String(idx).padStart(2, '0');
      }
    });

    // counter-parallax inside each panel image
    panels.forEach(pnl => {
      gsap.fromTo(pnl.querySelector('[data-pfx]'),
        { xPercent: -6, scale: 1.12 },
        {
          xPercent: 6, scale: 1.02, ease: 'none',
          scrollTrigger: {
            trigger: '.metiers', start: 'top top',
            end: () => '+=' + (distance() + window.innerHeight * 0.4),
            scrub: .8, invalidateOnRefresh: true
          }
        });
    });

    gsap.from('.panel', {
      yPercent: 8, opacity: 0, duration: 1, ease: 'forge', stagger: .07,
      scrollTrigger: { trigger: '.metiers', start: 'top 62%', once: true }
    });
    // reveal each panel's content as it comes into the pinned viewport
    const panelIntros = panels.map(pnl => {
      const bits = pnl.querySelectorAll('.panel__spec, .panel__title, .panel__lede, .panel__list li');
      return gsap.from(bits, {
        y: 26, opacity: 0, duration: .8, ease: 'forge', stagger: .05, paused: true
      });
    });
    ScrollTrigger.create({
      trigger: '.metiers', start: 'top top',
      end: () => '+=' + (distance() + window.innerHeight * 0.4),
      invalidateOnRefresh: true,
      onUpdate(self) {
        const seg = 1 / panels.length;
        panelIntros.forEach((tw, i) => {
          if (!tw.__fired && self.progress >= Math.max(0, i * seg - .12)) { tw.__fired = true; tw.play(); }
        });
      }
    });

    return st;
  }

  /* ── CAPACITÉS: row reveal + cursor preview ────────────────────── */
  function capacites() {
    const rows = qa('.caps__row');
    rows.forEach((r, i) => gsap.from(r, {
      opacity: 0, y: 34, duration: .9, ease: 'forge', delay: i * .04,
      scrollTrigger: { trigger: r, start: 'top 90%', once: true }
    }));

    const prev = q('#capsPreview');
    if (!prev || window.matchMedia('(max-width:860px)').matches) return;
    const img = prev.querySelector('img');
    const pos = { x: 0, y: 0 };
    const setX = gsap.quickTo(prev, 'x', { duration: .55, ease: 'power3' });
    const setY = gsap.quickTo(prev, 'y', { duration: .55, ease: 'power3' });

    rows.forEach(r => {
      r.addEventListener('mouseenter', () => {
        img.src = r.dataset.img;
        gsap.to(prev, { opacity: 1, scale: 1, duration: .55, ease: 'forge' });
      });
      r.addEventListener('mouseleave', () => {
        gsap.to(prev, { opacity: 0, scale: .86, duration: .4, ease: 'forge' });
      });
    });
    window.addEventListener('mousemove', e => { setX(e.clientX); setY(e.clientY); }, { passive: true });
    gsap.set(prev, { xPercent: -50, yPercent: -50, left: 0, top: 0 });

    gsap.to('.caps__glow', {
      yPercent: 22, ease: 'none',
      scrollTrigger: { trigger: '.caps', start: 'top bottom', end: 'bottom top', scrub: true }
    });
  }

  /* ── MOYENS: staggered inventory + bg drift ────────────────────── */
  function moyens() {
    gsap.from('.crew__list li', {
      opacity: 0, x: -24, duration: .8, ease: 'forge', stagger: .09,
      scrollTrigger: { trigger: '.crew__list', start: 'top 86%', once: true }
    });
    gsap.from('#kitList li', {
      opacity: 0, y: 18, duration: .6, ease: 'forge', stagger: .035,
      scrollTrigger: { trigger: '#kitList', start: 'top 88%', once: true }
    });
    gsap.to('.moyens__bg img', {
      yPercent: 14, ease: 'none',
      scrollTrigger: { trigger: '.moyens', start: 'top bottom', end: 'bottom top', scrub: true }
    });
    gsap.from('.moyens__lede', {
      opacity: 0, y: 22, duration: .9, ease: 'forge',
      scrollTrigger: { trigger: '.moyens__lede', start: 'top 90%', once: true }
    });
  }

  /* ── PROCESSUS: SVG line draw + step reveals ───────────────────── */
  function processus() {
    const fill = q('#procFill');
    const dots = qa('#procDots b');
    if (fill) {
      gsap.to(fill, {
        height: '100%', ease: 'none',
        scrollTrigger: { trigger: '.proc__steps', start: 'top 76%', end: 'bottom 86%', scrub: .5 }
      });
      qa('.step').forEach((s, i) => ScrollTrigger.create({
        trigger: s, start: 'top 62%', end: 'bottom 42%',
        onToggle: self => dots[i] && dots[i].classList.toggle('on', self.isActive)
      }));
    }
    qa('.step').forEach(s => {
      gsap.from(s.children, {
        opacity: 0, y: 30, duration: .9, ease: 'forge', stagger: .07,
        scrollTrigger: { trigger: s, start: 'top 86%', once: true }
      });
    });
  }

  /* ── SECTEURS: infinite marquee with scroll-velocity skew ──────── */
  function secteurs() {
    qa('[data-marq]').forEach(inner => {
      inner.innerHTML += inner.innerHTML;               // duplicate for seamless loop
      const dir = parseFloat(inner.closest('.sect__row').dataset.dir);
      const half = () => inner.scrollWidth / 2;
      const tween = gsap.to(inner, {
        x: () => dir > 0 ? -half() : 0,
        ease: 'none', duration: 26, repeat: -1,
        modifiers: { x: gsap.utils.unitize(x => gsap.utils.wrap(-half(), 0, parseFloat(x))) }
      });
      if (dir < 0) gsap.set(inner, { x: -half() / 2 });

      ScrollTrigger.create({
        trigger: '.sect', start: 'top bottom', end: 'bottom top',
        onUpdate(self) {
          const v = gsap.utils.clamp(-2.2, 2.2, self.getVelocity() / -900);
          gsap.to(inner, { skewX: v * dir, duration: .5, ease: 'power3', overwrite: 'auto' });
          tween.timeScale(gsap.utils.clamp(.4, 4.5, 1 + Math.abs(self.getVelocity()) / 2200));
        }
      });
    });
  }

  /* ── CONTACT + FOOTER ──────────────────────────────────────────── */
  function outro() {
    gsap.to('.contact__plate img', {
      yPercent: -12, ease: 'none',
      scrollTrigger: { trigger: '.contact', start: 'top bottom', end: 'bottom top', scrub: true }
    });
    gsap.from('.card', {
      opacity: 0, y: 40, duration: .95, ease: 'forge', stagger: .09,
      scrollTrigger: { trigger: '.contact__grid', start: 'top 88%', once: true }
    });
    gsap.from('.bigcta', {
      opacity: 0, scale: .9, duration: .9, ease: 'forge',
      scrollTrigger: { trigger: '.bigcta', start: 'top 92%', once: true }
    });
    gsap.from('.foot__col', {
      opacity: 0, y: 28, duration: .9, ease: 'forge', stagger: .08,
      scrollTrigger: { trigger: '.foot__top', start: 'top 92%', once: true }
    });
    // wordmark rises out of the fold
    gsap.from('.foot__mark span', {
      yPercent: 42, duration: 1.3, ease: 'forge',
      scrollTrigger: { trigger: '.foot__mark', start: 'top 98%', end: 'bottom bottom', scrub: .8 }
    });
  }

  /* ── nav auto-hide / solidify ──────────────────────────────────── */
  function navBehaviour() {
    const nav = q('#nav');
    let last = 0;
    ScrollTrigger.create({
      start: 0, end: 'max',
      onUpdate(self) {
        const y = self.scroll();
        nav.classList.toggle('is-solid', y > window.innerHeight * .55);
        nav.classList.toggle('is-hidden', y > last + 4 && y > window.innerHeight * .9);
        last = y;
      }
    });
  }

  /* ── magnetic buttons ──────────────────────────────────────────── */
  function magnets() {
    if (REDUCED || window.matchMedia('(hover:none)').matches) return;
    qa('[data-magnet]').forEach(el => {
      const strength = 0.26;
      const xTo = gsap.quickTo(el, 'x', { duration: .6, ease: 'power3' });
      const yTo = gsap.quickTo(el, 'y', { duration: .6, ease: 'power3' });
      el.addEventListener('mousemove', e => {
        const r = el.getBoundingClientRect();
        xTo((e.clientX - (r.left + r.width / 2)) * strength);
        yTo((e.clientY - (r.top + r.height / 2)) * strength);
      });
      el.addEventListener('mouseleave', () => { xTo(0); yTo(0); });
    });
  }

  /* ── boot ──────────────────────────────────────────────────────── */
  function init() {
    heroScroll(); lineReveals(); manifeste(); metiers();
    capacites(); moyens(); processus(); secteurs(); outro();
    navBehaviour(); magnets();
    ScrollTrigger.refresh();
  }

  document.fonts.ready.then(() => {
    bootLoader();
    init();
    // re-measure once layout has fully settled (fonts, images)
    window.addEventListener('load', () => ScrollTrigger.refresh());
    setTimeout(() => ScrollTrigger.refresh(), 900);
  });

  let rt;
  window.addEventListener('resize', () => {
    clearTimeout(rt);
    rt = setTimeout(() => ScrollTrigger.refresh(), 220);
  });

  window.__itm = { scrollTo, lenis };
})();
