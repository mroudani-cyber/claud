# Scene: "failure is part of the successful path" → "midlife opportunity" (8.75 s, 1080×1920)

Editorial paper-desk explainer used at 21.3–30.05 s of the McConaughey edit.
- One continuous camera over a 4800×3800 paper world; the camera follows the pen tip, then pulls back, whips to the newspaper and zooms through "OPPORTUNITY".
- Every element has a height `z`: its shadow offset/softness and its depth-of-field blur come from `z` and the animated focus plane (real rack focus).
- Physical drops: notes, stamp and paper strip fall from height (ease-in, shadow tightening) and stop dead; no bounce.
- Render: `node render.js` (8 sub-frames, 180° shutter) → `ffmpeg -framerate 240 -i fr/%05d.jpg -vf "tmix=frames=8,framestep=8" -r 30 out.mp4`.
- Fonts load from Refract's `node_modules/@fontsource` (absolute paths in `scene.html`; fix them on another machine).
- Assets: `assets.py` makes the paper, B&W print, host sticker, stamp grunge, tape; `cut.py` cuts subjects out with Refract's u2netp model.
