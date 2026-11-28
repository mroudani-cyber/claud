# Editorial motion-graphics scenes (paper-desk system)

Shared engine: `engine/lib.js` + `engine/lib.css`. Each scene is a self-contained HTML page exposing `seek(t)` (a pure function of time).
- Camera: world wrapper transform (centre, scale, roll) driven by keyframes (`kf`).
- Depth: every `.el` has `data-z`. Its shadow and depth-of-field blur come from z and the animated focus plane.
- Physics: `drop()` (gravity fall, no bounce), `shake()` (decaying impact), `inkWords()` (per-word blur-in), typewriter by character.
- Render: `SCENE=x.html OD=frames SUB=8 node render.js` (180° shutter, SUB sub-frames per frame), then
  `ffmpeg -framerate $((30*SUB)) -i frames/%05d.jpg -vf "tmix=frames=SUB,framestep=SUB" -r 30 out.mp4`. Use SUB=16 for spins.
- Assets live in `failure-path/a/` (copy or symlink `a/` next to a scene before rendering). Font paths in lib.css point at Refract's `@fontsource` folder.

| Scene | Edit time | Beat |
|---|---|---|
| dictionary-agreement | 8.8–15.2 s | Video frame flies back into a print; dictionary "fail·ure: an embarrassing thing to do", marker circle; AGREEMENT card signed, AGREED stamp, zoom-through |
| failure-path | 21.3–30.05 s | Ink path with FAIL notes → "successful path." → NECESSARY stamp → newspaper "MIDLIFE CRISIS" → OPPORTUNITY strip |
| newspaper-spin | 32.6–35.84 s | Classic spinning newspaper lands on "revolutionary", "for the mind." inks in |
