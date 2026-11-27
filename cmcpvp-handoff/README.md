# CMCPVP 1.0.19 (Cracked Minecraft PvP)

A practice-only server plugin: ranked and unranked duels, LT5 to HT1 tiers, FFA, parties, bots, tournaments, cosmetics.
There is no SMP, no hub and no server selector, only the lobby.

**The jar:** `CMCPvP-1.0.19.jar`

## New in 1.0.19

The full change list of 1.0.11 to 1.0.19 is in `vortex-realm/README.md` of the plugin repo. 1.0.19 itself:

- **Three new arenas**, with all the detail where players fight and look: the **Imperial Amphitheatre**, the **Crown Citadel** (castle courtyard) and the **Sultan's Palace**.
- **FFA** arenas (except crystal) become the **Grand Colosseum**; existing ones on plain terrain are rebuilt once, one at a time.
- Nothing is built outside the view, so the maps are light.
- The old court and pro maps are retired (out of rotation, not deleted), and no floor has a logo any more.
- `cmcpvp-1.0.19.bundle` holds the two 1.0.19 commits on top of 1.0.18 (`02b4025`).

## New in 1.0.10

- **No more automatic NPC placement.** You place lobby NPCs by hand with `/npc` again.
- If 1.0.9 already built NPC booths in your lobby, they're taken away on the first start, along with their NPCs. The floor under each booth gets the surrounding floor block back. NPCs you placed or moved yourself are never touched.
- Leaderboards or welcome holograms that 1.0.9 placed stay where they are. Remove any you don't want in game.

## New in 1.0.9

| What | How it works |
| --- | --- |
| **1.8 kits removed** | 1.8 combat, the 1.8 kits, the Legacy Hall, the 1.8 tab and every 1.8 setting and command are gone. Saved 1.8 kits are deleted on the first start, and the console says how many. |
| **Arenas built when needed** | No duel map is built at start-up. When two players are matched, their map is built then. If every copy of a map is in use, one more copy is built. |
| **Waiting room** | While their map builds, both players stand in a small room styled like that arena, split by a glass wall. They see a progress bar, "Waiting for the arena" with the opponent's name, and particles. When the map is ready the bar turns green, "ARENA READY" shows, and they're moved in. |
| **FFA built once** | FFA arenas are built once, on the first start, and never rebuilt by themselves. |
| **Faster generation** | Maps are pasted chunk by chunk instead of block by block, and the designs are planned off the main thread. Building a map costs the server much less. |
| **New duel animations** | Match found types itself in. The countdown closes in with a flash. FIGHT and DEATHMATCH slam onto the screen. A round win splits open and a loss shatters. Victory slams in with a gold crown of particles, and defeat shatters. Your Elo counts up or down after the match. |

To build every map at start-up like before, turn **On-Demand Arenas** (`arena.on-demand`) off in /pvpadmin → Settings → Arena.

| Picture | What it shows |
| --- | --- |
| `previews/pro-signature-sheet.jpg` | New: the C MCPvP Arena, the only arena with the server's name |
| `previews/pro-imperial-sheet.jpg` | New: the Imperial Colosseum (big colosseum, duels and tournaments) |
| `previews/pro-highpeak-sheet.jpg` | New: the Highpeak Colosseum (mace) |
| `previews/pro-arenas-air-sheet.jpg` | New: 12 pro arenas from above, each with its own main building and gardens |
| `previews/pro-arenas-main-sheet.jpg` | New: the main building of each court, seen from the floor |
| `previews/pro-walled-sheet.jpg` | New: Sunken Atlantis and Starfall Citadel, the two walled courts |
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
2. Put `CMCPvP-1.0.19.jar` in `plugins/`.
3. **Do not install PracticePvP or VortexRealm on this server.** C MCPvP refuses to start next to them because they share commands and tables.
4. Optional plugins work as before: LuckPerms, PlaceholderAPI (placeholders are `%cmcpvp_...%`), Vault, GrimAC or Vulcan.
5. Start the server.
   - Everything is saved in `plugins/CMCPvP/`.
   - The database name is `cmcpvp`.
   - Permissions start with `cmcpvp.`, and the admin permission is `cmcpvp.admin`.

On the first start, one FFA arena is built for each FFA kit. Duel maps are built the first time two players are matched on them, while they wait in the waiting room (see New in 1.0.9).

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

### 17 pro arenas (new in 1.0.6, rebuilt in 1.0.8)

Every arena from before stays, and is still generated. These 17 are added next to them:

| Arena | What it is | Where it's played |
| --- | --- | --- |
| **C MCPvP Arena** | A court with a giant castle. It's the only arena with the server's name | Duels |
| Frostfang Bastion, Sunspire Palace, Stonewatch Keep, Blossom Court, Ember Citadel, Nightspire Abbey, Palmshore Court, Jade Temple, Obsidian Forge, Corsair's Wharf, Golden Dynasty | Courts, each with its own giant main building | Duels |
| Sunken Atlantis, Starfall Citadel | Walled courts: the ring design, in prismarine and in purpur and end stone | Duels |
| Gladiator Pit | A small colosseum: grey podium with a gold band, wooden stands | Duels |
| Imperial Colosseum | A big white-marble colosseum | Duels and tournaments |
| Highpeak Colosseum | A huge round colosseum on grass | Mace duels |

What's in them:

- **Colosseums.** From the floor up: pilasters with arched niches (a banner or a lantern in each), a terrace with urns and cypresses, stands in two-colour sectors with aisles and walkways, an arcade with a banner in every arch, upper stands, a two-storey colonnade, and a tiled awning with flagpoles. Two monumental gates with a red pediment, a portcullis and banner tapestries. The outside wall is three storeys of open arches.
- **Courts.** No ring of walls: every court is laid out like palace grounds, and each one is different.
  - One long side has a giant main building: a castle with a keep, great round towers and a gatehouse (C MCPvP Arena, Frostfang Bastion, Stonewatch Keep on a rock, Corsair's Wharf with a lighthouse); an onion-domed palace with minarets (Sunspire Palace, Ember Citadel); a cathedral with twin spires and a rose window (Nightspire Abbey, Obsidian Forge); a pagoda temple (Blossom Court, Palmshore Court); a ziggurat (Jade Temple); or a pyramid behind pylon gates (Golden Dynasty).
  - Facing it: covered stands, an arcade with palms on its terrace, or garden pavilions.
  - At each end: a freestanding gateway in the theme's style (castle gate, pointed portal, gothic arch, torii, pylon gate).
  - The corners are open gardens: trees, fountains, statues or obelisks, hedges with flowers and lamp posts.
- **Walled courts.** Sunken Atlantis and Starfall Citadel keep the ring design: stone walls with pilasters and light panels, a balcony with flower boxes, an arcade, tiled roofs, corner towers and a gatehouse at each end.
- **Floors.** Plain, with no decoration: natural floors (sand with sandstone blocks, red sand, snow) or same-colour textures (terracotta shades, white stones, mossy stone, wood planks...). Only the C MCPvP Arena has a small pixel-art sword in the middle of its floor. No ice or magma on any floor.
- **Landscapes.** Each arena has its own: snowy peaks, desert mesas, sakura hills, badlands, dark woods, tropical isles, jungle hills or volcanic peaks. They come with set pieces such as pagodas, torii gates, domed pavilions, pyramids, graveyards, stilt huts and ice spikes.
- **Landmarks.** A giant knight statue stands behind one end and a giant sword in a rock behind the other. Both are high enough to see over the walls from the floor.
- **The name.** Only the C MCPvP Arena shows it: on a big board over its stands, and on a giant sign behind its gate in place of the sword.
- **Only the floor is playable.** An invisible wall stands at its edge, and building or explosions only change the floor.

Each one is built the first time a match needs it. With **On-Demand Arenas** off, they're all built on the first start instead (a few minutes; admins get a message when they're switched on). The tournament final is still played in the Champions Colosseum.

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
- Every 30 minutes (**Update Check**, `updates.check-minutes`) it checks for a new version. A new jar is downloaded in the background, checked against its SHA-256 and put in `plugins/update/`.
- It goes in by itself. The server restarts as soon as nobody is online. Otherwise it restarts at 5:00 (**Update Restart Hour**), after running matches finish (it waits up to 30 minutes) and a 5-minute countdown in chat. A full backup is taken first. For this, spigot.yml needs a restart script (`settings.restart-script`, `./start.sh` by default) so the server comes back. Without one, the update goes in at your next restart.
- **Update Restart** (`updates.restart`): `EMPTY_OR_NIGHT` (default), `NOW` (a 60-second countdown as soon as it's downloaded) or `MANUAL`.
- To install it right away, run `/pvpadmin update now`.

---

**Source code:** `cmcpvp-1.0.19.bundle` is a git bundle of the source.

- It holds only the C MCPvP commit, so apply `vortex-handoff/vortexrealm-3.14.10.bundle` first.
- C MCPvP is generated from the same code as the Vortex plugin, with `tools/make_cmcpvp.py`.
