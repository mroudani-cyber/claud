# r06 + r08: talking-head edits (9:16)

## r08: Before/After of a pro captioned talking-head edit (~21 s)
Quote: "Leonardo da Vinci famously said, God will sell you anything at the price of labor… luck does not exist… you work hard, you work more, you work longer… increase your odds of success."

### What the pro edit does (After panel)
| t (s) | Speech | Visual treatment |
|---|---|---|
| 0–1.6 | "Leonardo da Vinci" | **B-roll of the person named**: engraved portrait, B&W, slow push; name in grey serif + script ("Leonardo / Davinci"); torn-paper strip transition |
| 2.3 | (starts talking) | Speaker shot with a **focus-pull from blur to sharp** |
| 3.4 | "God will sell you" | Small serif lead-in ("god will") + **huge bold italic key word** ("Sell you") in grey at ~50% opacity, *behind/under* his chin, bleeding off the bottom |
| 4.5 | "at the price of labor" | Same system: small serif "at the price of" + giant "labor" |
| 5.7–6.8 | "If you want something / you have to work" | **B-roll with colour**: a sign reading "GOOD FEELING", then a sunset hand reach; the key word in a big colour (teal "want", orange "work") picks up colours from the shot |
| 7.9–10.2 | "most people… think that… luck" | Three quick B-rolls (paraglider, man on a cliff, kitchen), white bold caption centred, one word per shot on "luck" |
| 11.3 | "have never truly worked" | Back to the speaker, small serif |
| 12.4–14.6 | "luck does not exist / it's merely / probabilities" | **Dark abstract B-roll** (night light streaks, bokeh), white bold sans centred, 2–3 words per card |
| 15.8–18.0 | "you work Hard / More / longer" | **Repetition device**: the same layout three times, the lead-in "you work" stays and only the giant italic word swaps: "Hard" → "More" → "longer" |
| 19.1–20.2 | "eventually you… odds of" | Speaker, white bold caption |
| 21.3 | "success." | **Cut to black** on the final word |

### The pro upgrade checklist (Before → After)
1. **Grade:** moody, crushed blacks, warm skin, deep green background (the Before is flat).
2. **Caption system = 2 tiers:** a small *serif* lead-in (Playfair/EB Garamond, ~3% height, white) + a giant *bold italic sans* key word (Inter/Helvetica Black Italic, ~12–15% height, grey ~60% opacity or a colour), sitting low in the frame, partly cut off by the frame edge.
3. **B-roll on every concrete noun or emotion** (Leonardo, want, work, people, luck), cut on the word, about 1–1.5 s each.
4. **Key-word colour pulled from the B-roll** (teal sign → teal "want", sunset → orange "work").
5. **Abstract dark B-roll for abstract ideas** ("luck does not exist", "probabilities").
6. **Repetition with a swap** ("you work ___") to build rhythm.
7. **Focus-pull and slow push-ins** on the speaker, never a static frame.
8. **End on a black cut** on the last word.

## r06: "17 video effects Claude can create" (9:16, ~28 s)
Structure: 0–18 s is a fast list of 17 effects, ~1 s each, with a fixed header "17 video effects / claude can create" (yellow-white bold, top) and a counter "NN/17" + effect name (yellow bold, lower third). Then 18–28 s is a talking CTA with one-line white captions mid-lower.

Effects seen (each with a rebuild recipe):
| Effect | What it is | Recipe |
|---|---|---|
| orbit | Phone/photo cards orbiting around the subject | 3–5 cards on an ellipse path in 3D, z-sorted so they pass behind the person matte |
| ui world | A chat-UI box ("How can I help you today?") floating in the scene | Rebuilt UI card, perspective-tilted, with soft shadow and a slight float |
| frame break | Subject breaks out of an inner frame | Inner rectangle with border; person matte drawn over the border |
| digital zoom | Hard punch-in, 1.0 → 1.4 in 4 frames | Scale with ease-out expo + motion blur |
| phone mockup | Footage plays inside a phone held in frame | Composited phone frame with screen corner-pinned |
| headline wall | Stacked newspaper/headline cards behind the subject | Paper cards with text, behind the matte, slight rotation |
| zoom-through cut | Camera zooms into a dark area/object and comes out in the next shot | Scale 1→3 on the outgoing shot into a dark pixel region, cut, incoming shot from 0.6→1 |
| chart grow | Line chart draws over the footage with a glowing dot | SVG path stroke-dashoffset animation + glow dot following the end point |
| pull-back reveal | Camera pulls back to show the shot is a screen/window inside a UI | Shot scales down 1→0.45 into a UI frame |
| green screen | Subject keyed over a phone/glow scene | Person matte over a new background |
| doodle boil | Hand-drawn white outline around the subject that "boils" | Matte edge → stroke, redraw with jitter every 2–3 frames (wiggle 2 px) |
| vertigo | Dolly zoom: background stretches, subject size holds | Background scale up while the subject layer scales down to compensate |
| cover story | Magazine cover layout ("STUDIO" masthead, serif) over the subject | Big serif masthead behind the head + small cover lines |
| couch wall, checklist, paper cut, glass type | Text/graphic layouts (checklist card ticking items, cut-paper texture, frosted-glass type) | Tick items in sync with words; glass = backdrop blur + white 20% fill + 1 px border |

Pacing: one effect per spoken word in the list (the transcript lists names at 0.5–1.1 s intervals). The label changes on the word onset.
