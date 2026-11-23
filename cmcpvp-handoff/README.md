# C MCPvP 1.0.1 (Cracked Minecraft PvP)

A practice-only server plugin: ranked and unranked duels, LT5 to HT1 tiers, FFA, parties, bots, tournaments, cosmetics.
There is no SMP, no hub and no server selector, only the lobby.

**The jar:** `CMCPvP-1.0.1.jar`

| Picture | What it shows |
| --- | --- |
| `previews/fracturespawndesign-air.png` | The new spawn, The Fracture |
| `previews/fracturespawndesign-spawn.png` | What a player sees on joining |
| `previews/arenas-air-sheet.png` | The 13 designed arenas with their new landscapes |
| `previews/arenas-floor-sheet.png` | The view from each arena's fighting floor |
| `previews/colosseum_grand-air.png` | The mace arena (Grand Colosseum) in its alpine valley |
| `previews/colosseum_champions-air.png` | The tournament arena (Champions Colosseum) in its valley |

---

## 1. Install

1. Use **Paper 1.21.11** and **Java 21**, the same as the Vortex server.
2. Put `CMCPvP-1.0.1.jar` in `plugins/`.
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

- The fighting floor of every designed arena is **exactly as before**.
- Behind each build there is now a whole landscape:
  - a valley ringed by mountains, mesas, volcanic peaks or jungle hills, depending on the theme
  - forests of the theme's trees
  - set pieces such as villages, watchtowers, a windmill, camps, temples, pyramids, obelisks, graveyards, stilt huts and spires
  - small islands floating in the sky
- The mace arena (Grand Colosseum) stands in an alpine valley: snowy peaks, spruce forests, a village, watchtowers and a windmill.
- The tournament arena (Champions Colosseum) stands in a valley with white-stone mountains, cypress forests, quartz temples, gold-tipped obelisks and camps.
- From the floor, you see the mountains and trees over the stands and walls.
- The landscape is only scenery. An invisible wall stands where each arena used to end, so fights (mace flights and pearls too) stay in the same area as before.
- New arenas get this automatically.
- To rebuild arenas that already exist with the new look, use the **Regenerate Designed Arenas** button in /pvpadmin, or run `/pvpadmin regenerate confirm`. The vanilla terrain maps are not touched.

## 4. Set it up as yours

All of these are in **/pvpadmin → Settings**:

| Setting | Default | What to do |
| --- | --- | --- |
| Server IP (`general.server-ip`) | `play.cmcpvp.net` | Set your real address. It shows on the scoreboard |
| Discord link (`extras.links.discord`) | Empty | Paste your new Discord invite. It shows in `/links` and in the "Join our Discord!" message |
| Website | Branded C MCPvP, with a placeholder crimson-and-gold logo | The logo is built into the jar. Send me your logo and I'll put it in the next version |

## 5. Updates

- C MCPvP checks its own update feed: `cmcpvp-handoff/update.json` on this branch. It never downloads the Vortex jar.
- A new version is downloaded in the background but installs only on a restart. To install it now:
  1. Run `/pvpadmin update now`.
  2. Restart the server.

---

**Source code:** `cmcpvp-1.0.1.bundle` is a git bundle of the source.

- It holds only the C MCPvP commit, so apply `vortex-handoff/vortexrealm-3.14.10.bundle` first.
- C MCPvP is generated from the same code as the Vortex plugin, with `tools/make_cmcpvp.py`.
