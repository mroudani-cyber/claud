# r01, r09, r11: AI-product brand promos (Claude ×2, Gemini 3)

All three use **one continuous shot with no hard cuts**: every change is a transformation of something already on screen. Each is 12–13 s, music only (no VO), dark background with one saturated light colour.

## Transition mechanics (measured at 12 fps)
| Ref / t | Transition | Frame-level mechanics |
|---|---|---|
| r01 1.8–2.8 s | **Word dissolves into light streaks** ("Claude" → embers) | Letters vanish *left to right*, one every ~2 frames ("laude"→"ude"→"de"→"e"), while orange light streaks (comet trails) spin out from where the letters were. The red ring background keeps rotating. About 0.5 s |
| r01 2.3–2.8 s | **Streaks become the UI** | The comet trails converge downward and a dark rounded input box fades up under them (opacity 0→100 over ~8 frames); a red glow "horizon" rises from the bottom |
| r01 2.8–3.7 s | **Prompt typing + greeting serif write-on** | Text types into the box (~25 chars/s) while the ember trails die out; "✳ Good evening, stepanvfx" writes on word by word above the box in a serif (Tiempos/Source Serif lookalike), each word fading in with a slight blur |
| r01 7.2–8.1 s | **Highlighted line → paragraph pull-back** | Starts on one glowing, blurred orange line (DOF macro); the camera pulls back over ~10 frames and blur resolves to show a full paragraph of small text; the orange glow behind stays |
| r01 8.6–11.4 s | **Word swap with a fixed anchor** | "Claude" stays; the second word swaps Code → Build → Learn with a blur cross-fade (~6 frames), warm serif gradient text |
| r09 3.4–4.3 s | **Typing with a colour-graded cursor tail** | "I want a website for my motion design work": the newest 3–4 letters are orange and fade to white as typing moves on (a trailing highlight); the camera slowly tilts and zooms in (3D rotateX ~10°) |
| r09 4.4–5.3 s | **Prompt "explodes" into code, code assembles the site** | The UI tilts and pushes forward; the text smears with a directional motion blur into **multicoloured code lines** (syntax colours) that scroll vertically like a waterfall in perspective; a glowing card ("Premium Motion Design") fades in from the right through the code, out of focus first |
| r09 8.1–9.0 s | **Colour change with a morph** | The orange website card slides up and out (motion blur) and the new **blue card** rises into place, already rotating from a 3D tilt to flat; the prompt "I want a blue background." stays under it as the cause |
| r09 9.9–11.3 s | Logo + curved text | ✳ sparkle pulses; "Built with Claude" sets along a curve that unrolls |
| r11 0–3.3 s | Logo resolve + particle numeral | A blue starburst blooms on white, then "Gemini 3" types in; the **"3" is built from thousands of glowing particles** (point cloud) on dark navy |
| r11 3.9–9.9 s | Glass UI + "Analyzing…" | "Hi Maxmill / Where should we start?" writes on large, then the camera pulls back so the text becomes a UI header; the input pill glows blue; a click turns it into an "Analyzing…" pill with a spinning loader and **bloom pulses** |

## Shared rules
1. **Nothing cuts. Things become other things** (letters → light → UI → code → website). The eye always has a continuous object to follow.
2. **Camera always moving:** slow 3D tilt (rotateX/Y 5–15°), push-ins of 5–10% per beat, pull-backs to reveal context.
3. **Depth of field** is the main "premium" cue: elements enter out of focus and rack into focus, and backgrounds stay soft.
4. **One hero colour on black:** red (r01), orange→blue (r09), electric blue (r11). Glow/bloom with a large radius; the light source sits *behind* the UI (a rim/horizon glow).
5. **Real UI rebuilt in vector** (input box, model dropdown, buttons, cursor), never screenshots: crisp at every zoom level.
6. **Typography:** an elegant serif for brand words (Claude), a clean grotesk for UI (Inter/SF), sizes jumping from tiny UI text to huge hero words.
7. **Motion blur on every fast move** (the code smear, the card swaps). Without it the moves look like slides.
8. **Hold the final logo ~1 s** with a subtle pulse.

## Rebuild recipe: "prompt explodes into code into result" (r09)
1. t0: UI card (dark glass, 16 px radius, 1 px #ffffff22 border) with typing text; the newest 4 chars are orange (#FF7A1A), fading to white over 8 frames.
2. t0+0.8 s: card rotateX 0→18°, translateZ +200, scale 1→1.15 over 10 frames, ease-in.
3. Same moment: duplicate the text layer, apply horizontal directional blur 0→60 px and a hue shift, fade it out; at the same time spawn 40 code lines (monospace, syntax colours) in a 3D column scrolling up at 1200 px/s with DOF blur by depth.
4. t0+1.3 s: result card fades in at z=-300, blur 20→0 px, while moving to z=0 over 14 frames, ease-out expo; orange radial glow behind it at 80% opacity.
5. SFX: a whoosh on 2, a digital glitch texture under 3, a soft "thump" when the card lands.
