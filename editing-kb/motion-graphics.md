# Motion graphics rulebook (pro level, not "moving elements")

Sources: the HyperFrames motion reference (measured frame by frame from launch films), animation-principles easing library, bang-motion "anti-PPT" rules, explainer-high-energy rules, and the user's references r01/r05/r09/r10/r11 (SaaS/pro) and r07/r08 (talking-head kinetic type).

## 1. Physics, not tweens
- **Arrive slow, leave clean.** Arrivals use a long-tailed ease-out (`expo.out` = cubic-bezier(.16,1,.3,1), `quart.out` = (.25,1,.5,1)). Exits accelerate (`power3.in` = (.32,0,.67,0)) and are **40–50% shorter** than entrances. Moves on screen ease both ways (`inOutCubic` = (.65,0,.35,1)).
- **Springs by damping ratio:** 1.0 = never bounces; **0.7–0.85 = premium**; 0.4–0.6 = playful; <0.3 = cartoon. Position and scale may bounce; **opacity and colour never bounce**.
- **Mass:** big things move slower and overshoot less; small things are snappy. Scale duration with distance (≈ duration ∝ √distance).
- **Overlap and follow-through:** the next element starts when the previous one is 30–50% done. Children lag the parent by 2–4 frames (a card lands, its text settles 3 frames later, its shadow 2 frames after that).
- **Stagger:** letters 1 frame apart, words 60–120 ms, list items 40–80 ms.
- **Squash/stretch on impact:** a slammed word scales 1.08 → 0.97 → 1.0 (on the y-axis a little more than x); the frame shakes 6–12 px for 4–6 frames, decaying.
- **Motion blur on every fast move**: 6–12 px on text-sized elements, 15–20 px full-frame, along the direction of travel only, peaking at the fastest frame.

## 2. Camera, depth and blur (what makes it "3D" instead of flat)
- **A virtual camera exists in every scene.** Everything sits in a wrapper (`camera`) that pushes, drifts and tilts: a slow orbit of 3–5°/s, a push-in of 5–10% per beat, **shot-size changes** (wide → medium close-up on the element that is "talking", scale 1.4–2.2 in 0.6–0.9 s inOut), then back out.
- **Z-layers with parallax:** background (moves 0.3×), mid (1×), foreground (1.6×). Foreground particles and bokeh pass close to the lens, blurred.
- **Depth of field:** elements enter out of focus (blur 12–20 px) and **rack into focus** as they land; far layers stay blurred 4–8 px; a focus pull moves attention from one element to the next.
- **3D tilt:** UI cards and text blocks at rotateX/Y 5–18°, perspective 1200–2000 px; they flatten as they land.
- **Light:** one light source behind the subject (rim/horizon glow); bloom only on objects, never on body text; a radial vignette on every flat background; subtle film grain.
- **The world never shows its edge.** Never pan a layer so far that its edge or black gap appears.

## 3. Text on talking-head video (depth-aware, varied)
- **Find the empty space first.** Use the person matte (background remover) to measure where the head and body are, then place text in the free zones: beside the head, above the shoulders, behind the head with only the edges tucked in. Text behind the subject only works if ≥ 60% of the word stays visible; otherwise put it in front.
- **Vary every 2–3 beats:** position (left stack, right stack, behind-head giant, lower band), font pairing, colour and entrance. Never one caption template for the whole video.
- **Font system (pick 3 per video):** heavy condensed (Anton / Bebas Neue / Oswald 700) for slams; italic serif (Playfair Display Italic / Instrument Serif / DM Serif) for the human or emotional word; clean grotesk (Montserrat 600 / Inter / Space Grotesk) for lead-ins; optional script/marker (Caveat / Permanent Marker) for one handwritten accent.
- **Colour:** white/cream for most words; one accent colour carries meaning (gold = value or success, red = danger or failure, teal/blue = calm or tech); a second accent at most. Pull the accent from the footage (r08 technique).
- **Push-down stacks:** in a 2–4 line stack, each new line enters at the top (or bottom) and **pushes the previous lines** down (or up) by one line height with a spring (ζ≈0.8, ~0.35 s). The old lines dim to 60% and shrink to 0.9×; the new line is the biggest and brightest. Mix sizes: small grotesk, then giant condensed, then italic serif.
- **Entrances to rotate between:** per-word blur-in (blur 6→0 px + opacity, 0.13 s, 0.067 s apart, no translate); mask reveal rising from a hidden baseline with a 4–6° skew; per-letter for names (opacity 0.3→1, 0.1 s apart); grey→white ink fill; slot-machine roll of one word; slam with squash and shake.
- **Landed titles are dead still.** The motion moves to the next element or the camera, never a floating or pulsing title.
- **Hold time:** 0.5 s + 0.3 s per word; 1–2 word lines may hold 0.4 s; the last line at least 2 s.

## 4. Transitions with a cause (pick 3–5 per film)
| Transition | Build |
|---|---|
| Zoom through an object | Track to it with blur 0.6 s, then scale it ~8% → 250% of the frame in 0.35 s (strong ease-in); its fill becomes the next scene |
| Object becomes the world | A card or pill grows past the frame in 0.65 s inOut, radius shrinking; surroundings blur ~15 px and fade in 0.3 s |
| Morph | A container widens into the next (110 → 880 px in 0.2 s, power3.out) with horizontal blur 12 → 0 |
| Carry across | The result shrinks 1 → 0.6, blur peaking at 6 px mid-move, and lands inside the next layout |
| Colour flood | The hero object stays while the ground changes colour in ~0.4 s inOut |
| Whip | 0.13–0.3 s directional smear; the arriving element lands blurred and sharpens in 0.13 s |
| Iris | `clip-path: circle()` opens from a point of interest in 0.15–0.5 s |
| Dip cut | Darken the outgoing frame ~40% for 3 frames, then hard cut |
| Blur swap | Out: opacity → 0 with 8 px blur in 0.13–0.2 s; in: blur → 0 in 0.13 s; the background never cuts |
Cut at the **fastest frame** of a move with matching direction and speed on both sides. At most one third of seams are hard cuts. Worlds never crossfade.

## 5. Structure (from the SaaS/pro references)
- **One shot = one statement**, ≤ 5 words. More than 6 words means split it or turn it into a visual.
- **Order of attention:** sentence → main object → supporting detail. Never the reverse.
- Hero object present for > 60% of the duration (something the viewer carries between scenes).
- Rhythm: montage cuts every 0.13–0.8 s; demo holds 7–10 s with the UI acting; average shot 1.8–3 s with motion inside it. Hold 0.3–0.75 s before a payoff.
- Beat grid: frames per beat = fps × 60 / BPM; compute each beat from its index (no accumulated rounding). Cut on the beat, change layout on the bar.

## 6. Banned (looks AI-generated or template)
Breathing/floating/pulsing loops on titles; titles that keep scaling after landing; a slow creeping push late in a scene; the same fade + slide-up on every title; light leaks on every cut; one transition type everywhere; glow on all text; more than 3 colours per scene (besides black and white); a flat static background; static screenshots zoomed instead of rebuilt UI; ALL-CAPS 800-weight centred text for every line; full stops on every 2-word phrase.

## 7. Easing quick sheet (cubic-bezier)
expoOut .16,1,.3,1 · quartOut .25,1,.5,1 · cubicOut .33,1,.68,1 · cubicIn .32,0,.67,0 · expoIn .7,0,.84,0 · inOutCubic .65,0,.35,1 · inOutQuart .76,0,.24,1 · backOut .34,1.56,.64,1 · anticipate .36,0,.66,-.56
Durations: hero headline 0.5–0.8 s · card reveal 0.4–0.5 s · count-up 0.6–1.2 s expoOut · camera push 0.8–2 s inOutQuad · exit 0.2–0.3 s.
