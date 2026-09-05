# ITM Partners — two site concepts

Two complete, distinct, scroll-driven websites for **ITM Partners**
(Mohammedia, Maroc) — *société d'ingénierie et des réalisations techniques*.

| | Concept | Direction |
|---|---|---|
| **A** | `site-a-forge/` — **Forge** | Dark, cinematic, industrial. Anton display, ember/arc palette, pinned horizontal métiers, word-scrub manifesto, velocity-skewed marquees. |
| **B** | `site-b-blueprint/` — **Dossier technique** | Light editorial drafting table. Instrument Serif, sticky sheet stack, exploded axonometric substation, horizontal ledger, crosshair cursor. |

Both are static: open `index.html`, or serve the folder.

```bash
node tools/serve.js site-a-forge     4600
node tools/serve.js site-b-blueprint 4700
```

## Source of the content

Copy and data come from ITM Partners' own published material
(itmp.ma — présentation, services, moyens, contact) plus its public
company listings. Verified facts used throughout:

- Signature — *Ingénierie | Travaux | Maintenance*
- Objet — société d'ingénierie et des réalisations techniques
- Création — 2012
- Métiers — construction métallique, électricité industrielle, maintenance industrielle
- Moyens humains — 2 ingénieurs, 2 techniciens électriciens,
  1 technicien construction métallique, ouvriers qualifiés
- Moyens techniques — the 17-item inventory as published
- Siège — N°2 Wahda, 2ᵉ étage, Appt. N°3, Bd de la Résistance, 28830 Mohammedia
- Tél +212 5 23 32 06 73 · Fax +212 5 23 32 06 72 · contact@itmp.ma

No client names, project references or certifications are claimed —
none are published, so none were invented.

## Build notes

- **No runtime CDN.** GSAP + ScrollTrigger + Lenis and all fonts
  (Anton, Archivo, Instrument Serif/Sans, JetBrains Mono) are vendored
  locally, with both `latin` and `latin-ext` subsets so French
  diacritics render in every weight.
- **Imagery is generated, not stock** — `tools/gen_assets.py` and
  `tools/gen_lattice.py` render the steel corridor, HV network,
  thermogram, weld field and the drafting plates procedurally.
- **Verification** — `tools/shoot.js` scrolls each site at four
  viewports, screenshots every step, and fails on console errors,
  document overflow or text clipped by its own box.

```bash
STEPS=16 node tools/shoot.js site-a-forge 4600 a desktop
node tools/find-overflow.js 4600 390 844
```

## Verification status

| Site | Viewport | Height | Console errors | Overflow | Clipped text |
|---|---|---|---|---|---|
| A Forge | 1600×950 | 11331px | 0 | none | none |
| A Forge | 1440×900 | 10985px | 0 | none | none |
| A Forge | 834×1112 | 12042px | 0 | none | none |
| A Forge | 390×844 | 10250px | 0 | none | none |
| B Dossier | 1600×950 | 9669px | 0 | none | none |
| B Dossier | 1440×900 | 9180px | 0 | none | none |
| B Dossier | 834×1112 | 8823px | 0 | none | none |
| B Dossier | 390×844 | 7980px | 0 | none | none |

Also checked on both: single `<h1>`, no skipped heading levels, every
`<img>` has `alt`, no empty links, `lang="fr"`, sensible tab order, and
nothing left stuck at `opacity: 0` in the viewport.
