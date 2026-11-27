# Reference batch 01: 11 TikTok motion edits (studied 2026-11-27)

Method: ffprobe + scene-cut detection (`select=gt(scene,0.3)`) + 24-frame contact sheets per clip.
Every clip ends with a ~4–6 s TikTok outro (not part of the edit; ignore its duration).

| # | Format | Length (edit only) | Hard cuts | Style |
|---|---|---|---|---|
| r01 | 16:9 | ~12 s | 0 | Claude brand promo: red glow rings → logo → UI typing → model dropdown → serif word swap "Claude Code/Build/Learn" |
| r02 | 9:16 POV | ~18 s | 1 | "POV: you animate brands": monitor mockup, white 3D product world, Amazon logo end |
| r03 | 16:9 | ~12 s | 11 | RDR2 wanted-poster edit: grunge collage, typewriter text on paper, giant red stencil type behind subject, ember particles, B&W |
| r04 | 16:9 | ~6.5 s | 1 | Billionaire intro: banknote, circular iris reveal of subject, name + bio type-on, glowing green money counter behind subject |
| r05 | 16:9 | ~44 s | 6 | SaaS ad (Holo): pixel-dissolve gradient type, floating photo cloud, 3D sphere, list carousel with bullet highlight, "Autopilot" toggle |
| r06 | 9:16 | ~28 s | 8 | "17 video effects": talking head + numbered effect labels, captions bottom-third, phone mockup, doodle boil outline |
| r07 | 16:9 | ~29 s | 35 | Kinetic-type masterclass: text behind subject, circular text orbit, cutout collage, word-by-word sticker type, color wheel, giant split type |
| r08 | 9:16 | ~22 s | 1 | Before/After of a captioned talking-head edit: one stylised word per beat over B-roll, serif/italic mix, dark grade |
| r09 | 16:9 | ~12 s | 0 | Claude prompt-to-website: glowing orange liquid bg, pill buttons, cursor click, typing, 3D tilted website card, colour swap, curved "Built with Claude" text |
| r10 | 16:9 | ~20 s | 11 | Portfolio: word-at-a-time white cards, fisheye/barrel 3D grid of app tiles, stacked glowing cards with orange rim light |
| r11 | 9:16 (16:9 inside) | ~13 s | 1 | Gemini 3: particle-built "3" numeral, glassy UI, "Analyzing…" glowing pill, logo resolve |

## Patterns that repeat (the "pro" bar)
1. **Few hard cuts, continuous motion.** 6 of 11 have ≤1 cut: transitions happen *inside* one moving composition (camera push, morph, object carries across). Cuts are reserved for beat hits (r03, r07, r10 ≈ 0.9–2.3 s average shot).
2. **One word / one idea per beat.** Kinetic type shows 1–3 words at a time, huge, centred or anchored to the subject, never full sentences (r01, r07, r08, r10).
3. **Type mixing.** A heavy grotesk/condensed (Anton-like) + a serif or italic contrast word + small UI sans for context lines (r04, r07, r08).
4. **Text behind subject** (depth layering) is a signature move: r03, r04, r07. It needs a clean matte, and the text must be large enough that only *part* is occluded.
5. **Real UI rebuilt, not screenshots.** Prompt box typing, model dropdown, cursor click, buttons (r01, r09, r11): tilted in 3D with glow and depth of field.
6. **Dark base + one saturated light source.** Black + red glow (r01), black + orange fire (r09), black + orange rim (r10), black + blue (r11). Glow/bloom on everything that matters.
7. **Motion blur on every fast move**; nothing moves linearly: strong ease-out, overshoot on pops, whip blur between states.
8. **Counters and data roll.** Numbers roll up with blur and glow (r04 "$3,000,000,000").
9. **Reveal devices:** iris/circle mask (r04), pixel dissolve (r05), word-swap with fade + blur (r01), barrel fisheye (r10), particles assembling (r11).
10. **Sound** (not yet analysed; next pass: whoosh on every move, riser into reveals).

## To apply to the Mark Cuban edit
- Replace slide-in scenes with continuous camera moves through a single canvas (r09/r10 approach).
- Captions: 1–3 words per beat, mixed weights, some anchored behind his head (r07/r08).
- $1,500 / $5.7B: r04-style glowing counter behind him with blur roll.
- Intro: dark + single warm glow, logo-style name reveal (r01/r09).
