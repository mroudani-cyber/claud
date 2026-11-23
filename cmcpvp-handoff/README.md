# C MCPvP 1.0.6 (Cracked Minecraft PvP)

A practice-only server plugin: ranked and unranked duels, LT5 to HT1 tiers, FFA, parties, bots, tournaments, cosmetics.
There is no SMP, no hub and no server selector, only the lobby.

**The jar:** `CMCPvP-1.0.6.jar`

| Picture | What it shows |
| --- | --- |
| `previews/pro-signature-sheet.jpg` | New: the C MCPvP Arena, the only arena with the server's name |
| `previews/pro-imperial-sheet.jpg` | New: the Imperial Colosseum (big colosseum, duels and tournaments) |
| `previews/pro-highpeak-sheet.jpg` | New: the Highpeak Colosseum (mace) |
| `previews/pro-arenas-air-sheet.jpg` | New: the other 12 pro arenas from above |
| `previews/pro-arenas-floor-sheet.jpg` | New: the same 12 from their fighting floors |
| `previews/fracturespawndesign-air.png` | The new spawn, The Fracture |
| `previews/fracturespawndesign-spawn.png` | What a player sees on joining |
| `previews/arenas-air-sheet.png` | The 13 designed arenas with their new landscapes |
| `previews/arenas-floor-sheet.png` | The view from each arena's fighting floor |
| `previews/colosseum_grand-air.png` | The mace arena (Grand Colosseum) in its alpine valley |
| `previews/colosseum_champions-air.png` | The tournament arena (Champions Colosseum) in its valley |
| `previews/colosseum_champions-close.png`, `previews/colosseum_grand-close.png` | The new colosseum walls up close |

---

## 1. Install

1. Use **Paper 1.21.11** and **Java 21**, the same as the Vortex server.
2. Put `CMCPvP-1.0.6.jar` in `plugins/`.
3. **Do not install PracticePvP or VortexRealm on this server.** C MCPvP refuses to start next to them because they share commands and tables.
4. Optional plugins work as before: LuckPerms, PlaceholderAPI (placeholders are `%cmcpvp_...%`), Vault, GrimAC or Vulcan.
5. Start the server.
   - Everything is saved in `plugins/CMCPvP/`.
   - The database name is `cmcpvp`.
   - Permissions start with `cmcpvp.`, and the admin permission is `cmcpvp.admin`.

On the first start, the arenas build themselves: every duel map, plus one FFA arena for each FFA kit. This takes a few minutes. Admins get a chat message when the arenas are switched on.

## 2. Build the lobby (The Fracture)

1. Stand where the middle of the spawn should be, in open air (y=100 in a void or flat world is good).
2. Run **`/pvpadmin hub build FRACTURE`**. You can also use **/pvpadmin → Builds → ★ The Fracture**, which lets you preview it in 3D first.
3. Wait for the build to finish. When it's done, the lobby spawn is set, every NPC is placed, and you are teleported to the spawn point.

**The old MCPVP.club map is still there:** use `/pvpadmin hub build CLUB_SPAWN`, or pick **Club Spawn** in Builds.

### What's in The Fracture

The Fracture is a floating island about 350 blocks across. A glowing chasm splits it in two, with three bridges across.

| Place | NPC | What's there |
| --- | --- | --- |
| Arrival (spawn) | | A crowned gate that frames the plaza, a fountain, flower beds, and a lookout balcony over the south edge |
| Crown Plaza | | White marble with crimson rays and a glowing crystal heart in the middle. The middle is open, with no tower |
| 8 domed pavilions | Duels, Ranked, Parties, Settings, Tournaments, Stats, New Here?, Academy | One pavilion per menu, round the plaza |
| FFA Colosseum (east) | Free For All | Sand pit, tiered seats, arches, braziers, a grand gate |
| Hall of Champions (north, over the bridge) | Leaderboards | Colonnade, a cupola with a gold crown, podiums inside |
| Kit Forge | Kit Editor | Smithy with a giant anvil |
| Cosmetic Spire | Cosmetics | Rainbow glass tower with turrets and a garden |
| Tournament Stage | Spectate | A round stage with seats and a trophy |
| Training Yard | Bot Practice | Archery lanes, dummies, sparring rings, a watchtower |
| Parkour Spire | Parkour | About 50 jumps up a spire |
| Elsewhere | | Ponds with a dock, waterfalls into the chasm, snowy mountains, forests, crystal shards, floating rocks |

**Launch pads:** gold plates on the four roads out of the plaza. They throw you over the chasm to the Hall, or to the FFA Colosseum, the Training Yard or the Arrival. There is no fall damage after a launch.

**Parkour Spire:**

- Step on the **lime block** to start the timer.
- Gold blocks are checkpoints. If you fall, you go back to your last checkpoint.
- The **diamond ring** round the flag at the top is the finish.
- `/parkour top` shows the top 10, `/parkour checkpoint` takes you to your checkpoint, and `/parkour quit` stops your run.

**Ambience:** glowing motes rise out of the chasm, and sparks circle the crystal heart.

## 3. The arenas

### New in 1.0.6: 15 pro arenas

Every arena from before stays, and is still generated. These 15 are added next to them:

| Arena | What it is | Where it's played |
| --- | --- | --- |
| **C MCPvP Arena** | A castle court. It's the only arena with the server's name | Duels |
| Frostfang Bastion, Sunspire Palace, Stonewatch Keep, Blossom Court, Ember Citadel, Nightspire Abbey, Palmshore Court, Jade Temple, Obsidian Forge, Corsair's Wharf, Golden Dynasty | Courts, each with its own theme | Duels |
| Gladiator Pit | A small colosseum: grey podium with a gold band, wooden stands | Duels |
| Imperial Colosseum | A big white-marble colosseum | Duels and tournaments |
| Highpeak Colosseum | A huge round colosseum on grass | Mace duels |

What's in them:

- **Colosseums.** From the floor up: pilasters with arched niches (a banner or a lantern in each), a terrace with urns and cypresses, stands in two-colour sectors with aisles and walkways, an arcade with a banner in every arch, upper stands, a two-storey colonnade, and a tiled awning with flagpoles. Two monumental gates with a red pediment, a portcullis and banner tapestries. The outside wall is three storeys of open arches.
- **Courts.** Stone walls with wooden pilasters and light arched panels, a balcony with flower boxes and lantern posts, an arcade, tiled roofs with chimneys, round towers on the corners (cones, onion domes, pyramids or spires by theme), and a fortified gatehouse at each end.
- **Floors.** Flat, with an inlaid crest in the middle: crossed swords on a shield, or a mace in the Highpeak Colosseum. The Imperial Colosseum's floor has a red sunburst; the Highpeak's has paths like the spokes of a wheel.
- **Landscapes.** Each arena has its own: snowy peaks, desert mesas, sakura hills, badlands, dark woods, tropical isles, jungle hills or volcanic peaks. They come with set pieces such as pagodas, torii gates, domed pavilions, pyramids, graveyards, stilt huts and ice spikes.
- **Landmarks.** A giant knight statue stands behind one end and a giant sword in a rock behind the other. Both are high enough to see over the walls from the floor.
- **The name.** Only the C MCPvP Arena shows it: giant cloths over both long sides, and a giant sign behind its gate in place of the sword.
- **Only the floor is playable.** An invisible wall stands at its edge, and building or explosions only change the floor.

They're built by themselves on the first start after the update (a few minutes; admins get a message when they're switched on). This needs **First-Run Arenas** (`general.auto-generate-arenas`) on, which is the default. The tournament final is still played in the Champions Colosseum.

### The arenas from before (unchanged)

- The fighting floor of every designed arena is **exactly as before**.
- Behind each build there is now a whole landscape:
  - a valley ringed by mountains, mesas, volcanic peaks or jungle hills, depending on the theme
  - forests of the theme's trees
  - set pieces such as villages, watchtowers, a windmill, camps, temples, pyramids, obelisks, graveyards, stilt huts and spires
  - small islands floating in the sky
- The mace arena (Grand Colosseum) stands in an alpine valley: snowy peaks, spruce forests, a village, watchtowers and a windmill.
- The tournament arena (Champions Colosseum) stands in a valley with white-stone mountains, cypress forests, quartz temples, gold-tipped obelisks and camps.
- From the floor, you see the mountains and trees over the stands and walls.
- The colosseum walls are fully detailed:
  - the arena wall has pilasters with carved capitals and framed panels with an emblem in each bay
  - the stands are split into two-colour seating sectors, with lanterns where the walkways meet the aisles
  - arched tunnel entrances are cut into the stands, each with a keystone
  - the gallery above has keystones, a two-colour frieze, cloth hangings, balconies, corbels, battlements and flagpoles
  - the tournament arena has a golden trophy on each main gate, between the towers
  - the Titan Colosseum's wall got the same framed design
- The landscape is only scenery. An invisible wall stands where each arena used to end, so fights (mace flights and pearls too) stay in the same area as before.
- New arenas get this automatically.
- To rebuild arenas that already exist with the new look, use the **Regenerate Designed Arenas** button in /pvpadmin, or run `/pvpadmin regenerate confirm`. The vanilla terrain maps are not touched.

## 4. Tournaments: where matches are played

When you host a tournament (`/event host`), pick **Arenas**. Nobody votes:

| Mode | How it works |
| --- | --- |
| **Road to the Colosseum** (default) | Every round is played in its own arena. The whole road is shown when the bracket starts, and each stop is revealed to everyone with a big title when its round begins. |
| **Champion's Choice** | The higher-ranked player of each match earns the pick. They choose the arena from five, and their opponent watches the pick live. They have 10 seconds, then a random arena is picked for them. |
| **Arena Roulette** | Both players watch a slot machine spin through the arenas, slow down and stop on one. |
| **Colosseum only** | Every match is in the Champions Colosseum, like before. |

With **Final in the Champions Colosseum** on (the default once it's built), the final is always fought there, with its own reveal.

## 5. Set it up as yours

All of these are in **/pvpadmin → Settings**:

| Setting | Default | What to do |
| --- | --- | --- |
| Server IP (`general.server-ip`) | `play.cmcpvp.net` | Set your real address. It shows on the scoreboard |
| Discord link (`extras.links.discord`) | Empty | Paste your new Discord invite. It shows in `/links` and in the "Join our Discord!" message |
| Website | Branded C MCPvP, with a placeholder crimson-and-gold logo | The logo is built into the jar. Send me your logo and I'll put it in the next version |

## 6. Updates

- C MCPvP checks its own update feed: `cmcpvp-handoff/update.json` on this branch. It never downloads the Vortex jar.
- A new version is downloaded in the background but installs only on a restart. To install it now:
  1. Run `/pvpadmin update now`.
  2. Restart the server.

---

**Source code:** `cmcpvp-1.0.6.bundle` is a git bundle of the source.

- It holds only the C MCPvP commit, so apply `vortex-handoff/vortexrealm-3.14.10.bundle` first.
- C MCPvP is generated from the same code as the Vortex plugin, with `tools/make_cmcpvp.py`.
