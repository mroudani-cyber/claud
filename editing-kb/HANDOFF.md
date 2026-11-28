# Handoff: professional video editing & motion graphics for Refract

Written for the next AI that edits videos for this user. Read the whole file before touching a project. Everything here was learned from this user's reference videos, the installed motion skills, frame-by-frame study, and the mistakes made along the way.

---

## 0. Who the user is and what they want

- The user builds **Refract**, an AI video editor for Windows (Electron, React). Another Claude session develops the app; **your job is editing**: make videos that impress on TikTok/Reels/Shorts.
- They judge by one bar: **"does it look like a professional After Effects editor made it?"** Their references (r01–r11, see §2) are that bar. Anything that looks like a template, a slideshow, or "AI slop" gets rejected immediately.
- **Explicitly hated:** glowing blobs, gradient backgrounds, everything bouncing, generic slide-in captions, clips cut on a fixed grid without looking at the content, "1% of pro motion", weird AI voices, captions covering faces, captions running off the frame, clips that start or end mid-word.
- **Explicitly wanted:** real camera moves (push, pull, orbit, whip, rack focus), real depth (layers at different distances, depth of field, text behind the subject), physical motion (things fall and land, stamps slam, paper drops), varied fonts/colours/placements per beat, text stacks that push down line by line, a different style for every video, real PNG/cut-out elements, motion graphics explainer scenes, velocity (speed-curve) edits on music, and the best moments only (for gaming: the actual hits and combos).
- **Working style:** they want you to **act, not ask**. They interrupt long runs; keep each step short and report results. They get frustrated by permission prompts. Show progress with frames, not promises. Be honest when something is not done.
- They sometimes use a secondary (dad's/verification) account that **cannot approve network changes**: the phone app only shows "Deny" for environment changes ("This request can't be approved here. Review it on your computer"). Plan around that (see §9).

---

## 1. The 10 golden rules of a pro edit

1. **Change the visual on the word onset (±1 frame)**, never on the sentence. Get word-level timestamps (Whisper; here Groq `whisper-large-v3` with `timestamp_granularities[]=word` worked through the proxy).
2. **Transform instead of cutting.** One object becomes the next (letters → light → UI → code → website; a video frame flies back and becomes a photo print). Save hard cuts for beat hits. At most ⅓ of seams are hard cuts; worlds never crossfade.
3. **1–3 words per beat.** Giant (25–100% of frame height) or tiny. No mid-size captions.
4. **2–3 fonts per video**: heavy condensed (Anton / Bebas / Oswald) + italic serif (Playfair Display Italic / Instrument Serif / DM Serif) + a clean grotesk or mono (Montserrat / Inter / Space Grotesk / JetBrains Mono). Optional one handwritten accent (Caveat / Permanent Marker). Gaming: pixel font (Press Start 2P) + condensed.
5. **One accent colour that means something** (gold = value/success, red = danger/failure, teal/blue = calm/tech) on a neutral or monochrome base. Max 3 colours per scene besides black and white. Pull the accent from the footage.
6. **Depth everywhere**: text behind the subject (person matte), collage over text, depth of field, 3D tilt, parallax layers, a camera that never fully stops.
7. **Physics, not tweens**: long ease-out arrivals, short ease-in exits, motion blur only on fast moves, overshoot only where something physically lands, landed titles stay dead still.
8. **Pacing contrast**: 2-frame strobe bursts next to 1.5 s holds. Hold 0.3–0.75 s before a payoff.
9. **Sound mirrors meaning**: sub hit on "hit"/"fired", whoosh on every big move, riser into reveals, paper/stamp foley for paper scenes. Mix voice to −14 LUFS, music ducked 8–10 dB under speech.
10. **Bookends**: a strong hook in the first second, a rich middle, a clean end card or a cut to black on the last word.

---

## 2. What the reference videos teach (batch 01, 11 videos)

Full breakdowns: `editing-kb/breakdowns/*.md`. Summary:

| Ref | Style | Steal this |
|---|---|---|
| r07 | Kinetic-type masterclass (talking head, 61 cuts in 29 s) | Every spoken word = a visual change; giant red word behind head; circular text orbiting the head; face-crop collages; 2-frame strobe montage under one fixed word; red/white/black only |
| r08 | Before/After talking-head upgrade | Two-tier captions (small serif lead-in + giant bold italic key word at ~60% grey, partly off the bottom edge); B-roll on every concrete noun; key-word colour pulled from the B-roll; repetition device ("you work Hard / More / longer"); focus pulls; cut to black on the last word |
| r06 | "17 video effects" | Orbit, UI world, frame break, digital zoom, phone mockup, headline wall, zoom-through cut, chart grow, pull-back reveal, green screen, doodle boil, vertigo (dolly zoom), cover story, glass type: recipes in the breakdown |
| r03 | RDR2 wanted-file documentary | Cold open with no voice (4.6 s of SFX + macro shots); red/off-white/black; typewriter on paper; giant stencil name behind a halftone B&W portrait; ember particles over B&W footage |
| r04 | Billionaire bio | Banknote slide, circular iris reveal, name type-on + small bio, glowing green money counter rolling up behind the subject |
| r01, r09, r11 | AI brand promos (Claude, Gemini) | No cuts at all: continuous transformation; rebuilt vector UI in 3D tilt; DOF; one hero colour on black; typing with a trailing colour highlight; prompt "explodes" into code into result |
| r05 | SaaS ad | Gradient-blob text that morphs into a pill; photo cloud; list carousel with active-item highlight synced to VO; toggle "Autopilot" reveal |
| r10 | Portfolio | Word-at-a-time cards; fisheye/barrel grid of tiles; glowing card stacks with rim light and overshoot pop |
| r02 | Brand animation POV | Motion inside a monitor in a real scene; white 3D world + one brand colour; words riding 3D arrows |
| Minecraft refs (4) | Gaming edits | Glitch/RGB transitions, giant text with character behind ("I AM GAZIN'"), starfield/zoom tunnels, pie-slice image collages, fast beat cuts, fireworks/particle accents |

---

## 3. Motion physics (exact values)

Easing (cubic-bezier):
- Arrive: expoOut `.16,1,.3,1` (premium), quartOut `.25,1,.5,1`, cubicOut `.33,1,.68,1`
- Leave: cubicIn `.32,0,.67,0`, expoIn `.7,0,.84,0`
- Move on screen / camera: inOutCubic `.65,0,.35,1`, inOutQuart `.76,0,.24,1`, inOutSine
- Overshoot (only physical landings / playful): backOut `.34,1.56,.64,1`; anticipation `.36,0,.66,-.56`

Rules:
- Exits are 40–50% shorter than entrances. Arrive slow, leave clean (one motion, never slide-stop-leave).
- Springs by damping ratio: 1.0 no bounce; **0.7–0.85 premium**; 0.4–0.6 playful; <0.3 cartoon. Position/scale may bounce; **opacity and colour never bounce**.
- Overlap: next element starts when the previous is 30–50% done. Children lag the parent by 2–4 frames.
- Stagger: letters 1 frame, words 60–120 ms, list items 40–80 ms.
- Motion blur: 6–12 px on text-sized elements, 15–20 px full frame, along the travel direction only, peaking at the fastest frame. In code renders: 8 sub-frames per frame on a 180° shutter (16 for spins), averaged with ffmpeg `tmix`.
- Durations: hero headline 0.5–0.8 s; card reveal 0.4–0.5 s; count-up 0.6–1.2 s expoOut; camera push 0.8–2 s; exit 0.2–0.3 s.
- Hold a read line 0.5 s + 0.3 s/word; 1–2-word lines 0.4 s; last line ≥ 2 s.
- Banned (looks AI-generated): breathing/floating/pulsing titles; titles that keep moving after landing; slow creeping push late in a scene; same fade+slide-up on every title; light leaks on every cut; one transition type everywhere; glow on all text; flat static background; screenshots zoomed instead of rebuilt UI; ALL CAPS 800 centred for every line.

---

## 4. Camera, depth and focus (the "After Effects 3D" look)

- **Every scene has a virtual camera** (a wrapper transform: centre x/y, scale, roll; or AE-style x/y/z/pan/tilt). It pushes 5–10% per beat, changes shot size (wide → close on the element that is "talking", scale 1.4–2.2 in 0.6–0.9 s inOut), orbits a stage at 3–5°/s, whips between areas (0.13–0.3 s directional smear), and zooms *through* an object to exit.
- **Z-layers with parallax**: background 0.3×, mid 1×, foreground 1.6×. Foreground debris/bokeh passes close to the lens, blurred.
- **Depth of field from real depth**: give every element a height `z`. Blur = `min(14, |z − focusZ| × 0.16) / cameraScale` px; animate `focusZ` for rack focus. Elements enter out of focus and sharpen as they land.
- **Shadows from height**: offset `(z·0.18, z·0.36)` px, softness `5 + z·0.5` px, opacity `0.30 − z·0.0006`. A falling object's shadow tightens as it lands. That's what sells "physical".
- **3D tilt**: cards/text at rotateX/Y 5–18°, perspective 1200–2000 px, flattening as they land.
- **Light**: one source behind the subject (rim/horizon); bloom only on objects, never body text; radial vignette; subtle animated film grain.
- **Never show the world's edge** (no black gaps when panning).
- **Text behind subject** only if ≥ 60% of the word stays visible. In tight 9:16 talking-head crops the face fills the middle, so behind-head giant words fail; use the r08 front-of-frame style there, or shrink the subject.

---

## 5. Text systems to rotate (change per video and every 2–3 beats)

1. **Two-tier caption** (r08): small serif lead-in (≈3% height) + giant bold/italic key word (12–15% height), low in frame, accent colour from footage.
2. **Push-down stack**: each new line enters word by word (blur 8→0, 0.16 s) and lifts the stack with a small spring overshoot; old lines dim to 55% and shrink to 0.92×; a slam word (condensed, accent colour) squashes 1.6 → 0.96/1.05 → 1 with a decaying camera shake; the stack clears with a blur-out; the payoff rises from a mask with a 5° skew. Component: `editing-kb/components/push_stack.py`.
3. **Behind-the-subject giant word** (r07/r03): needs a clean person matte; only when the subject leaves room.
4. **Black & white blend**: grayscale footage, text in `mix-blend-mode: difference` or a white plate with `multiply`, one red word.
5. **Typewriter / document**: mono type on paper, line by line, with a caret.
6. **Per-word ink-in** (opacity + blur, no translate), **grey→ink fill**, **slot-machine roll** of one word, **mask rise with skew**, **per-letter name reveal** (0.1 s apart).
7. **Gaming**: pixel font with stacked-shadow extrusion (`1px 1px … 14px 14px` in a darker colour), letters falling from z with rotateX, glint sweep across a title, combo/HUD counters punching on each hit.
Fonts available in Refract (fontsource): Anton, Bebas Neue, Oswald, Montserrat, Playfair Display, DM Serif Display, Space Grotesk, Caveat, Permanent Marker, Press Start 2P, Black Ops One, Bungee, Unbounded, Syne, Cinzel, Teko, Rajdhani, plus Arabic families (Cairo, Tajawal, Amiri, Reem Kufi, Lalezar…).

---

## 6. Explainer motion-graphics scenes (what impressed the user most)

Style used: **editorial paper desk** (documentary, like r03/r04/r08). No glow, no gradients.
- One continuous camera over a large paper world (procedural paper texture: low-frequency mottling + grain + fibres).
- Real elements: B&W photo prints of the speaker cut from the footage (white border, tape strips with torn edges), torn notes, rubber stamps (Anton in red, rounded border, grunge mask, multiply blend), newspaper clippings (masthead in Playfair italic, rules, grey text lines), dictionary entries, signed agreements (blue-ink Caveat signature revealed left→right), red marker strikes/circles (SVG stroke-dashoffset), handwritten notes with arrows.
- Physical drops: notes/stamps/paper strips fall from height (quadIn, 0.11–0.36 s), shadow tightening, **stop dead** (no bounce); a stamp gives a 10 px decaying camera jolt.
- Transitions with a cause: the live video frame freezes and **flies back into a photo print** on the desk; whip across the desk; **zoom through** a stamp/letter back to the footage; classic **spinning newspaper** (rotate −1080°→0, scale 0.06→1, quartOut 0.8 s) landing on the key word.
- Scenes built so far (source in `editing-kb/scenes/`): `failure-path` (ink path with FAIL notes → "successful path." → NECESSARY stamp → newspaper MIDLIFE CRISIS → OPPORTUNITY strip), `dictionary-agreement`, `newspaper-spin`. Shared engine: `scenes/engine/lib.js` (camera keyframes, DOF from z, `drop()`, `shake()`, `inkWords()`, typewriter).
- **Pipeline**: HTML page with a pure `seek(t)` → Playwright screenshots at 30 fps × 8 sub-frames (180° shutter) → `ffmpeg -framerate 240 -i %05d.jpg -vf "tmix=frames=8,framestep=8" -r 30` → MP4 → import into Refract on the overlay track at the exact word time → delete captions/SFX under it → add matching SFX.
- Always render **stills first** at the key moments and inspect them; fix framing, layer order, contrast between paper sheets (raise cards to z≈14 with a lighter paper so they separate from the desk), and text cut off at edges before the full render.
- Other explainer styles to rotate: dark UI/SaaS (rebuilt UI in 3D tilt, typing with trailing highlight, code waterfall), kinetic collage (r07), documentary iris + counters (r04), gaming HUD (pixel type, hearts, XP bar, combo counter).

---

## 7. Editing playbooks

### Talking head / podcast clip (9:16, 35–60 s)
1. Transcribe word-level. Pick the strongest 30–50 s that stands alone (a clear question → answer → payoff). Open with the strongest line as a **hook** (repeat it from later), then the main take.
2. Cut on natural pauses (silences), never mid-word; remove dead air >0.4 s.
3. Reframe each camera angle separately (split at scene cuts first; auto-detection misses some: measure with ffmpeg `select='gt(scene,0.25)'`). Check every angle; host/reaction shots need their own framing.
4. Grade (film look ~0.6, slight contrast, grain + vignette).
5. Captions on every phrase using the text systems in §5; vary every 2–3 beats; keep away from the face and the TikTok UI zone (bottom ~15%, right edge).
6. Insert 1–3 **explainer cutaways** (§6) on the most visual ideas; return to the face for emotional lines.
7. SFX: whoosh on transitions, impact/stamp on slams, riser into reveals. End card or cut to black.

### Car / gaming edit (beat-driven)
1. Get the **song first**. Analyse: BPM, kicks, sections (intro / build / drop / break / drop 2 / outro). Example: "AINSI BAS LA VIDA (Hardtekk slowed)": intro 0–15 s, build with bass hits ~every 0.95 s 15–29 s, gap 29.5 s, **drop 30.6 s** (kicks every ~0.48 s) to ~60.5 s.
2. **Find the real action first**, never cut on a grid blindly. For gaming: mace smashes, combos, totem pops, explosions, clutch moments. Scan the footage densely (1–2 s steps, larger thumbnails), then zoom to 0.25 s around each candidate to find the **exact impact frame**. Use game-audio onsets (hit sounds) when available.
3. Place each hit **on** a kick/drop; start the shot 0.3–0.6 s before the impact.
4. **Velocity edit**: per-clip speed curves following the music: ~1.8× between kicks, ~0.3× on the impact, smooth ramps (Refract `set_speed` with `ramp` + `keep_duration:true`).
5. Intro: slow-mo cinematic shots + title; drop: shake-hit, zoom-punch on alternate cuts, chromatic, flash/glitch at section changes, handheld 3D camera; outro title ("GG.").
6. Mute game audio under music (or keep hit sounds very low as texture).

### Biography / documentary intro
Cold open with SFX only → iris reveal of the subject → name type-on + short bio → glowing counter/stat behind the subject → stencil/halftone collage → ember/dust particles.

---

## 8. Refract specifics (the user's app)

- Tools (75 in v0.3.8+): timeline (`add_media`, `split`, `trim`, `move`, `delete_clips` (pass `ripple:false` or other text clips shift!), `delete_range`), `set_speed` (ramps, keep_duration), `apply_effect` (shake-hit, zoom-punch, push-in, whip-zoom, glitch-hit, chromatic, grain, vignette…), `apply_look`, `color_grade`, `add_text` (presets, fonts, `behind_subject`), `add_motion_html` (HTML+CSS animated with CSS keyframes only; seeked frame-accurately; Google Fonts allowed; `layer:"behind"`), `add_motion_template`, **`set_camera`** (AE 3D camera presets or custom keyframes, DOF), **`set_depth`** (z per layer), `remove_background`, `auto_reframe`, `add_audio` (sfx: whoosh, riser, impact, bass-drop, click, shutter, pop, ding, glitch), `voice_fx`, `look_at_frame` (render a frame + layout report; use it constantly to check), `critique`, `export_video`, `run_steps` (batch; keep batches ≤12 steps: longer batches silently stop).
- **CSS keyframes in `add_motion_html` must end with a 100% hold**, or animated properties snap back to their initial values.
- `auto_reframe` with subject tracking can pan past the frame edge (black bar): use `track_subject:false` and reframe per camera angle.
- `add_media` of a freshly imported video may place it as 0.2 s; follow with `trim` to the right end.
- Export: frame-accurate MP4 export is very slow without a GPU (≈4 fps in the cloud sandbox). WebM "browser" export is real-time capture. In the sandbox, screen-recording the preview (x11grab of the Xvfb display) is faster but drifts; retime against known cut points, then splice pristine renders over the scene ranges.

### Running Refract in the cloud sandbox
`refract-sandbox/setup.sh`: unzip the Windows build, `npx @electron/asar extract resources/app.asar app`, install the matching Linux Electron version, run under `xvfb-run` with `--no-sandbox`. The app writes `~/.config/Refract/agent.json` (port + token); call `POST http://127.0.0.1:<port>/call {name,args}` with `Authorization: Bearer <token>` (set `NO_PROXY=127.0.0.1`). Use `setsid nohup` so it survives interrupted commands.

### Remote control of the user's PC
Refract → Settings → Remote creates a Cloudflare tunnel MCP link (`https://<random>.trycloudflare.com/mcp/<code>`). It changes every time Refract restarts. Options:
1. Best: add it as a **custom connector** on the Claude account (claude.ai → Settings → Connectors → Add custom connector, name "Refract"), then start a new chat with Refract enabled.
2. From a cloud session: the host must be on the environment's allowed hosts; that approval only works from a computer, not the phone app. Calling it: MCP streamable HTTP (`initialize` → `Mcp-Session-Id` header → `tools/call`). Cloudflare times out calls after 100 s: keep each call short.

---

## 9. Getting media in and out (what works / what doesn't)

- Works: files attached in chat; **gofile** links (download through a headless browser, which reads the API response for the direct link; only some gofile storage servers are allowed: `cold-eu-agl-1`, `store-eu-par-3`; re-upload if it lands elsewhere).
- Does not work from the sandbox: YouTube, Spotify, Wikimedia, Pexels, archive.org (blocked unless approved). Data-URI imports into Refract are not supported. Uploading to random file hosts may be blocked by the safety classifier.
- Music: the user supplies tracks (they want real songs like phonk/hardtekk, not synthesized beats). Never download from Spotify.
- **Rights**: only edit/post content the user owns or has permission to use, licensed speeches (e.g. Mindset DRM), Creative Commons with matching terms (TED is CC BY-NC-ND: no edits), or public domain (US federal works like JFK/NASA speeches). Reposting others' podcasts gets channels struck.

---

## 10. Mistakes made (don't repeat)

1. Spawning many parallel agents to read video frames burned the user's tokens: **don't use subagents** for this user; read compact contact sheets yourself (one tiled image per video, frames only at cuts; text data such as cuts, onsets and transcripts first).
2. Cutting gaming footage on a fixed beat grid from 15–30 s-apart thumbnails produced clips "that don't make any sense." **Find the actual hits first.**
3. Giant behind-subject words in a tight 9:16 face crop were hidden by the head.
4. Deleting clips with ripple shifted every later caption out of sync.
5. Long tool runs got interrupted: work in small, verified steps and send results early.
6. Promising things the environment can't do (remote links that need approval). Check reachability first and say clearly what is blocked.

---

## 11. Installed skills worth using (cloud session)

`/watch`, `/ffmpeg-analyse-video`, `/video-perception` (watching references); `/hyperframes` + `/hyperframes-registry` (≈450 motion blocks: transitions, kinetic type, captions, 3D, camera moves), `/remotion-*`, `/bang-motion` (GSAP, anti-PPT rules), `/explainer-high-energy`, `/motion-broll`, `/sound-effects`, `/animation-principles`, `/motion-art-direction`, `/shot-composition`, `/color-motion`, `/after-effects`, `/beat-sync-editing`, `/video-talkcraft` (108 motion recipe cards), `/anything2explainer`, `/lemo-opuscar` (film styles), `/threejs-*`, `/blender`. Skills live in `~/.claude/skills` and vanish when the container resets; reinstall with `npx skills add <repo> -y -g -a claude-code --all` (repo list in `installed-skills.md`).

---

## 12. How to be better than the previous editor

- Study each new reference **before** editing: cut rhythm (ffmpeg scene detection), a contact sheet at every cut, frame strips at 12 fps through transitions, spectrogram for sound design. Write a breakdown to `editing-kb/breakdowns/`.
- Plan a **beat sheet** first: time, spoken word / music event, visual, transition, sound. Then build.
- Make every video's style different on purpose (pick a style family per video: editorial paper, dark UI, kinetic collage, B&W blend, documentary, gaming HUD) and log which one you used.
- Verify with frames at every step (`look_at_frame`, stills) and fix before rendering.
- Deliver early, then improve; tell the user exactly what's done, what's approximate, and what's blocked.
