# PvP HQ (PvPHQ / PVPHQ) - Feature Research for a Competing Paper 1.21.11 Practice Server

Research method note: in this session, direct page fetches were blocked for every relevant host (pvphq.com, pvphq.net, lunarclient.com, minecraft.how all failed DNS in the sandbox). All findings below come from web-search result summaries and snippets of the cited pages, not full page reads. Treat figures (player counts, prices, top ratings) as point-in-time snapshots. `pvphq.net` did not appear in any search result; the official domain is **pvphq.com** (site, leaderboards, store at store.pvphq.com). The older site domain was **flowpvp.gg**, which still serves PVPHQ-branded pages.

Identity summary: PvPHQ is a competitive Minecraft Java PvP network formed in mid-2026 by merging **FlowPvP** (the "Ranked PvP" server of YouTuber Flowtives, built as an mcpvp.club replacement) and **MCLeagues**, backed by **Lunar Client**. The merger announcement on X ("FlowPvP & MCLeagues are now PvPHQ, Powered by @LunarClient") is dated around 16 June 2026. Do not confuse it with an unrelated India-based "Flow PvP" server (flowpvp.net) or an old Factions server at play.PvPHQ.org.

Sources used throughout:
- Lunar Client announcement: https://www.lunarclient.com/news/lunar-client-x-pvphq (mirror https://www-new.lunarclient.com/news/lunar-client-x-pvphq)
- X announcement: https://x.com/playPvPHQ/status/2066970865758265373
- Flowtives post: https://x.com/flowtives/status/2066971121883222318
- Co-owner post (Sols): https://x.com/McSolsy/status/2067069231573737894
- Wiki summary: https://wikiindex.org/w/PvPHQ
- BoardMC listing: https://www.boardmc.com/server/pvphq
- Discord listing: https://discord.com/servers/pvphq-1462963503689371805 (also listed as "PvPHQ (Formerly FlowPvP)": https://discord.com/servers/pvphq-formerly-flowpvp-1462963503689371805)
- Leaderboards: https://pvphq.com/leaderboard and per-kit pages
- Store: https://store.pvphq.com/category/ranks, https://store.pvphq.com/category/coins
- EloTiers guide: https://elotiers.com/guides/minecraft-pvp-tier-lists-compared
- TierTagger addon: https://modrinth.com/project/PzNBY0IN, https://www.9minecraft.net/pvphq-tiertagger-addon-mod/
- Liquipedia: https://liquipedia.net/lab/Minecraft/PvPHQ/PVP_Championship

---

## Game modes, kits and combat versions

### Takeaway
PvPHQ is a ranked-first, 1.9+ (modern) combat practice network with roughly 11 ranked kits (Sword, Axe, Mace, Spear/Spear-Mace, UHC, Pot, NethPot, SMP, DiaSMP, Vanilla, Cart), plus FFA, party team fights and tournaments. Critics at launch noted no unranked modes and missing "standard" kits. No evidence of a 1.8 combat mode or bot fights was found.

### Cited Findings
1. **Ranked duels** are the core mode — [Discord listing](https://discord.com/servers/pvphq-1462963503689371805); [Lunar Client](https://www.lunarclient.com/news/lunar-client-x-pvphq)
2. **FFA** ("intense FFA matches") is offered — [Discord listing](https://discord.com/servers/pvphq-1462963503689371805)
3. **Party team fights** (party vs party) at launch — [Lunar Client](https://www.lunarclient.com/news/lunar-client-x-pvphq); BoardMC lists "Party Fights" — [BoardMC](https://www.boardmc.com/server/pvphq)
4. **Weekly events** advertised — [Discord listing](https://discord.com/servers/pvphq-1462963503689371805)
5. **Player guilds** listed as a feature (pre-merger FlowPvP-era description; treat as uncertain for current state) — [Discord listing, via search summary](https://discord.com/servers/flowpvp-1462963503689371805)
6. BoardMC categorizes it as "Practice, PvP, Arena, KitPvP, Ranks" — [BoardMC](https://www.boardmc.com/server/pvphq)
7. **Kit ladders that exist on the website**: Overall, Sword, Axe, Mace, Spear (URL slug `spear_mace`), UHC, Pot, NethPot (`netherite_pot`), SMP, DiaSMP (`diamond_smp`), Vanilla, Cart, plus an "HT Cart" ladder (`ht_cart`) — [Overall](https://pvphq.com/leaderboard/overall), [Sword](https://pvphq.com/leaderboard/sword), [Axe](https://pvphq.com/leaderboard/axe), [Spear](https://pvphq.com/leaderboard/spear_mace), [UHC](https://pvphq.com/leaderboard/uhc), [Pot](https://pvphq.com/leaderboard/pot), [NethPot](https://pvphq.com/leaderboard/netherite_pot), [DiaSMP](https://pvphq.com/leaderboard/diamond_smp), [Cart](https://pvphq.com/leaderboard/cart), [HT Cart](https://pvphq.com/leaderboard/ht_cart), [Mace](https://flowpvp.gg/leaderboard/mace), [Vanilla](https://flowpvp.gg/leaderboard/vanilla)
8. The PvPHQ TierTagger addon says tiers are shown "across 11 gamemodes, including Sword, Axe, Mace, UHC, Pot, and SMP" — [Modrinth addon](https://modrinth.com/project/PzNBY0IN); [9Minecraft](https://www.9minecraft.net/pvphq-tiertagger-addon-mod/)
9. **Cart** kit (minecart PvP, likely TNT-minecart; inferred from name) has its own ladder with ~11,320 ranked players — [Cart ladder](https://pvphq.com/leaderboard/cart)
10. **Spear** (1.21.11 "Mounts of Mayhem" spear weapon) ladder with ~18,448 ranked players — [Spear ladder](https://pvphq.com/leaderboard/spear_mace)
11. **Custom kits** and **advanced kit customization** (kit editor) at launch — [Lunar Client](https://www.lunarclient.com/news/lunar-client-x-pvphq)
12. **Custom shields and armor trims** (cosmetic kit customization) — [Lunar Client](https://www.lunarclient.com/news/lunar-client-x-pvphq); [BoardMC](https://www.boardmc.com/server/pvphq)
13. **Totem anti-ghost** (server-side fix for "ghost" totem pops / desync in totem-based kits) — [Lunar Client](https://www.lunarclient.com/news/lunar-client-x-pvphq)
14. Hit registration and anti-ghosting are part of its "fairness" focus — [Lunar Client, via search summary](https://www.lunarclient.com/news/lunar-client-x-pvphq)
15. Player criticism: "poor knockback, missing standard kits, and an absence of unranked modes"; praise for custom kits and maps — [Discord listing summary](https://discord.com/servers/pvphq-1462963503689371805)
16. Client versions: BoardMC recommends Minecraft **26.2** (the new year-based Java version numbering); the TierTagger addon targets **1.21.11**; a player report mentions being unable to connect on **26.3** — [BoardMC](https://www.boardmc.com/server/pvphq); [Modrinth addon](https://modrinth.com/project/PzNBY0IN); [Discord listing](https://discord.com/servers/pvphq-1462963503689371805)
17. Older FlowPvP claim: better hit registration and anticheat than mcpvp.club — [Unstable Universe fandom post](https://unstable-universe-mc.fandom.com/f/p/4400000000000151166)

### Inferences
- Combat is modern (1.9+ cooldown) "vanilla tierlist" style; the kit list mirrors MCTiers/PvPTiers categories (Sword, Axe, Mace, Pot, NethPot, SMP, UHC, Vanilla/Crystal) plus newer Spear and Cart. A "Vanilla" ladder is likely the crystal/end-crystal kit (that is MCTiers naming), but this is not confirmed.
- No 1.8/legacy combat, no bot fights and no minigames (Bridge, Sumo, BedFight etc.) were found. If these exist, they were not in any indexed page. This is a possible gap a competitor could fill (unranked queues, 1.8 kits, bots).
- "HT Cart" ladder suggests a separate high-tier-only bracket for Cart. This is a guess from the URL slug.

### Gaps
- Exact kit contents (items, enchants, potion counts) were not found.
- No confirmation of unranked queues being added after launch, bot/AI duels, Sumo/Boxing/Bridge-type minigames, or FFA rules (kit, arena, killstreaks).
- How "weekly events" work (format, rewards) was not found.

---

## Ranked system: rating, tiers, tier tests, seasons, leaderboards

### Takeaway
PvPHQ replaces human-run tier tests with a match-derived rating. Each kit has a rating called **TR** that maps to a 15-step tier ladder (LT5 to HT1, through MT). Each player also has an overall points total (PTS). Rankings come from ranked matches, not tester evaluations. A recent "Ranked Update" released Tier 2 and Tier 1, overhauled low-tier ranked, improved matchmaking and recalibrated ratings.

### Cited Findings
18. **Tier structure**: HT1-HT5, MT1-MT5, LT1-LT5 (high, mid, low tiers, five divisions each) — [9Minecraft TierTagger addon](https://www.9minecraft.net/pvphq-tiertagger-addon-mod/); [Modrinth](https://modrinth.com/project/PzNBY0IN). Note: "MT" (mid tier) is an addition beyond the MCTiers HT/LT scheme.
19. Tier 1 is the strongest band and Tier 5 is entry level — [EloTiers](https://elotiers.com/guides/minecraft-pvp-tier-lists-compared)
20. **Per-kit rating "TR"** shown on kit ladders (e.g., Cart ladder top "MT2 noouv 374 TR"; UHC top "ninorc15 276 TR") — [Cart](https://pvphq.com/leaderboard/cart); [UHC](https://pvphq.com/leaderboard/uhc)
21. **Overall ladder uses PTS** (e.g., 81,746 players ranked, "Swight" top at 265 PTS at time of indexing) — [Overall ladder](https://pvphq.com/leaderboard/overall)
22. Leaderboard rows show the tier label next to the name (e.g., "HT2 clesa 114 TR" on Sword) — [Sword ladder](https://pvphq.com/leaderboard/sword)
23. Ladder size snapshots: Sword 36,369 (pvphq.com) vs 84,649 (flowpvp.gg copy, different snapshot); UHC 15,685; Spear 18,448; Mace 13,020; Cart 11,320 — [Sword](https://pvphq.com/leaderboard/sword), [Sword (flowpvp.gg)](https://flowpvp.gg/leaderboard/sword), [UHC](https://pvphq.com/leaderboard/uhc), [Spear](https://pvphq.com/leaderboard/spear_mace), [Mace](https://flowpvp.gg/leaderboard/mace), [Cart](https://pvphq.com/leaderboard/cart). The two Sword snapshots conflict, which suggests a reset or recalibration between them (inference).
24. EloTiers: unlike MCTiers/PvPTiers/SubTiers/MCPvP (which publish tester-assigned tiers), **PVPHQ publishes ratings derived from recorded matches, so it behaves like Elo** — [EloTiers](https://elotiers.com/guides/minecraft-pvp-tier-lists-compared)
25. EloTiers weights PVPHQ data by sample size, from about 0.15 for one match up to 1.0 at about 20 matches. This shows PvPHQ ratings are public per-match data — [EloTiers](https://elotiers.com/guides/minecraft-pvp-tier-lists-compared); [EloTiers ratings guide](https://elotiers.com/guides/how-minecraft-pvp-ratings-work)
26. Design intent: ranked "designed to reflect actual skill, not just who can grind the most games" — [Lunar Client](https://www.lunarclient.com/news/lunar-client-x-pvphq)
27. FlowPvP-era pitch: a rank system better than tiers because it "removes bias, time wastes, and is more precise". This is Flowtives' "Ranked PvP", launched as an open beta — [TikTok (Ceyoh)](https://www.tiktok.com/@ceyohh/video/7627748558166314271)
28. FlowPvP described as "ranked ELO-based matchmaking system" — [fandom post](https://unstable-universe-mc.fandom.com/f/p/4400000000000151166); "custom ELO ranking system" — [Discord listing](https://discord.com/servers/pvphq-1462963503689371805)
29. **"The Ranked Update"** (recent YouTube video): "We've released Tier 2 and Tier 1, overhauling low-tier ranked, improving matchmaking, and recalibrating" — [YouTube](https://www.youtube.com/watch?v=sXbmOuCsPfI). This means T1/T2 were locked or unreleased at launch and opened later.
30. Community content about climbing ranked tiers ("How I Got Tier Two In Diamond SMP (PVPHQ)") — [YouTube](https://www.youtube.com/watch?v=0WMzVYkhgv8)
31. **Third-party tier display**: a Fabric "PvPHQ Tiertagger Addon" shows PvPHQ tiers in nametags, tab list and chat. You select "PVPHQ" in the Tier Tagger config — [Modrinth](https://modrinth.com/project/PzNBY0IN)
32. **Ranked map selection** (players get some choice or ban over ranked maps) — [Lunar Client](https://www.lunarclient.com/news/lunar-client-x-pvphq)
33. **Skill-based / enhanced matchmaking** — [BoardMC](https://www.boardmc.com/server/pvphq)
34. Homepage tagline: headquarters for competitive Minecraft PvP with "live tiers and TR" — [pvphq.com](https://pvphq.com/)

### Inferences
- TR is most likely "Tier Rating", a per-kit Elo-like number whose thresholds map to LT5..HT1. The overall PTS is probably a sum or derived score across kits, similar to MCTiers points. Both meanings are unconfirmed.
- Top TR values are small (114 to 621), so TR is probably not a standard 1000-base Elo. It may be a points-above-floor scale.
- No tester-run "tier tests" exist; promotion is purely by ranked results, with T1/T2 gated until the Ranked Update.

### Gaps
- TR thresholds per tier, K-factor, placement-match count, decay and win/loss gains were not found.
- No information on seasons or season resets (aside from the inferred recalibration).
- Whether ranked map selection is a ban/veto or a pick system is unknown.

---

## Queue, matchmaking, match start, arenas, rematch, spectating, post-match

### Takeaway
Confirmed: skill-based queues, ranked map selection, a **replay system**, **post-match analysis**, and the ability to **queue directly through Lunar Client** across 22 regional server locations. Match-start presentation (capsules, cages, countdowns), rematch, spectating and post-match inventory details were not found in any indexed source.

### Cited Findings
35. **Queue directly through Lunar Client** (client-integrated queue) — [Lunar Client](https://www.lunarclient.com/news/lunar-client-x-pvphq); [wikiindex](https://wikiindex.org/w/PvPHQ)
36. **22 server locations** at launch across North America, Europe, Asia, the Middle East, Oceania and more (regional servers for low ping) — [Lunar Client](https://www.lunarclient.com/news/lunar-client-x-pvphq)
37. **Replay system** (match replays) — [Lunar Client](https://www.lunarclient.com/news/lunar-client-x-pvphq); [BoardMC](https://www.boardmc.com/server/pvphq)
38. **Post-match analysis** ("detailed Post-Match Analysis") — [Lunar Client](https://www.lunarclient.com/news/lunar-client-x-pvphq); [BoardMC](https://www.boardmc.com/server/pvphq)
39. **Performance optimizations** / client-side optimizations via Lunar — [Lunar Client](https://www.lunarclient.com/news/lunar-client-x-pvphq); [BoardMC](https://www.boardmc.com/server/pvphq)
40. "Epic arenas" and custom maps (praised by players) — [Discord listing](https://discord.com/servers/pvphq-1462963503689371805)
41. **Web match history**: each player has a `/matches` page — [example](https://pvphq.com/player/a048f59e-3cd3-4e55-ad6a-052633b27ab7/matches)
42. Launch-era technical problems: disconnects right after entering a queue, HTTP 429 and auth-server failure errors, "queue black boxes" (a visual bug in the queue UI or world) — [Discord listing](https://discord.com/servers/pvphq-1462963503689371805)

### Inferences
- "Post-match analysis" probably shows per-match stats (hits, combos, potions or totems used, damage) on the web profile and/or in-game. The exact content is unconfirmed.
- Spectating, rematch and post-match inventory viewing are standard on practice servers and likely exist, but no source confirms them.

### Gaps
- No source describes a match-start animation (capsule split, cages, elevators) or a countdown style. Not found.
- No details on arena count, map rotation, per-kit maps, or how the 22 regions are picked (auto by ping or manual).
- Rematch, spectate command, and post-match inventory GUI: not found.

---

## Lobby, hub, profile, stats, web platform

### Takeaway
The web platform is the most visible part: pvphq.com has public profiles with per-kit live tiers, TR history, head-to-head rivals, career totals and match history, plus per-kit leaderboards. In-game lobby features (NPCs, holograms, parkour, settings GUI) are not documented anywhere indexed.

### Cited Findings
43. **Social profiles** at launch — [Lunar Client](https://www.lunarclient.com/news/lunar-client-x-pvphq)
44. Profile contents: kits ranked, matches played, ranked points, best tier, recent matches, most-played rivals, career totals — [pvphq.com player page](https://pvphq.com/player/f60270d3-5d95-4a0d-9c5e-e25dcbe0335b); [another](https://pvphq.com/player/7c860f9e-ed18-4321-8b9f-c1c83ecb8458)
45. **Per-kit rating history graph** (select a kit to see rating progression) — [pvphq.com player page](https://pvphq.com/player/cc8f8e29-2cb7-48d2-93fb-8c52679cd3c7)
46. **Head-to-head rivals** with W-L and win percentage, shown with "You lead" / "You trail" labels — [pvphq.com player page](https://pvphq.com/player/ef37325f-3471-470c-ab1f-3e3b9b6e0bbd)
47. Profiles can be reached by UUID or by username URL (e.g., /player/ohLama, /player/qwgt) — [ohLama](https://pvphq.com/player/ohLama); [qwgt](https://pvphq.com/player/qwgt)
48. Per-kit public leaderboards plus an overall ladder — [Leaderboard](https://pvphq.com/leaderboard)
49. Site describes itself as offering "Live tiers, TR, head-to-head records, and match history" — [pvphq.com/medal](https://pvphq.com/medal)

### Inferences
- With a ranked-first design, the in-game lobby likely carries queue NPCs or items, a kit editor and leaderboard holograms, but none is confirmed.

### Gaps
- Lobby layout, NPCs, holograms, parkour, settings menu options and in-game /stats: no indexed source.

---

## Cosmetics, ranks, store, parties, clans, tournaments, Discord, anti-cheat, staff

### Takeaway
Monetization is a two-rank store (HQ $10, HQ+ $20) plus a Coins currency used for timed ranks and cosmetics. Lunar supplies anti-cheat support and exclusive cosmetics. The Medal.tv partnership rewards clipping with HQ+ and a verified badge. PvPHQ co-hosted a $10,000 "PVP Championship" with Tubbo Events in July 2026. The Discord is very large (around 66k members).

### Cited Findings
50. **Store ranks: HQ Rank $10.00 and HQ+ Rank $20.00** — [store ranks](https://store.pvphq.com/category/ranks)
51. **Coins** currency: buys longer rank durations without subscribing, and cosmetics. This implies ranks are sold as subscriptions or timed purchases — [store coins](https://store.pvphq.com/category/coins)
52. **Lunar-exclusive cosmetics**, creator activations and partnerships — [Lunar Client](https://www.lunarclient.com/news/lunar-client-x-pvphq)
53. **Custom shields and trims** (in-kit cosmetic customization) — [Lunar Client](https://www.lunarclient.com/news/lunar-client-x-pvphq)
54. **Medal.tv partnership**: a "PVPHQ x Medal" quest rewards **HQ+ rank and a verified badge** for connecting your Java account and clipping PvPHQ gameplay — [Medal quest](https://medal.tv/quests/8HWT-MakzW/pvphq_x_medal); [pvphq.com/medal](https://pvphq.com/medal); server clip hub [Medal](https://medal.tv/games/minecraft/servers/4j8RSb-lojq8lz/pvphq)
55. **Verified badge** exists as a profile or status marker (via Medal quest) — [Medal quest](https://medal.tv/quests/8HWT-MakzW/pvphq_x_medal)
56. **Parties** with party team fights — [Lunar Client](https://www.lunarclient.com/news/lunar-client-x-pvphq)
57. **Guilds** (FlowPvP-era listing; current status uncertain) — [Discord listing](https://discord.com/servers/flowpvp-1462963503689371805)
58. **Tournaments** built in at launch, with "large-scale tournaments and live events with serious prize pools" planned — [Lunar Client](https://www.lunarclient.com/news/lunar-client-x-pvphq); [wikiindex](https://wikiindex.org/w/PvPHQ)
59. **PVP Championship**: organized by PVPHQ and Tubbo Events, A-Tier, 16 to 18 July 2026, **$10,000 USD prize pool**. Closed qualifier 14 July 2026; open qualifier where the top 12 qualified for PVP Champs — [Liquipedia](https://liquipedia.net/lab/Minecraft/PvPHQ/PVP_Championship); [Closed Qualifiers](https://liquipedia.net/lab/Minecraft/PvPHQ/PVP_Championship/Closed_Qualifiers); [Open Qualifiers](https://liquipedia.net/lab/Minecraft/PvPHQ/PVP_Championship/Open_Qualifiers). One search summary described it as a Spear & Mace event; unverified.
60. **Anti-cheat**: Lunar Client provides anti-cheat support ("advanced anti-cheat systems through the Lunar integration") — [Lunar Client](https://www.lunarclient.com/news/lunar-client-x-pvphq); [BoardMC](https://www.boardmc.com/server/pvphq)
61. **Discord**: discord.gg/pvphq, around 66,456 members and 13,223 online at indexing time; guild created 20 January 2026 (the FlowPvP Discord, renamed "PvPHQ (Formerly FlowPvP)") — [Discord listing](https://discord.com/servers/pvphq-1462963503689371805); [renamed listing](https://discord.com/servers/pvphq-formerly-flowpvp-1462963503689371805)
62. **Socials**: X @playPvPHQ — [X](https://x.com/playPvPHQ/status/2066970865758265373)
63. Ownership and vision: Flowtives ("this will be the future of minecraft pvp") and co-owner Sols ("help bring and create exactly what the PvP community needs... in the most ethical way possible") — [Flowtives X](https://x.com/flowtives/status/2066971121883222318); [Sols X](https://x.com/McSolsy/status/2067069231573737894)
64. Scale: one listing showed about 1,844 online of a 5,000 cap; the IP is pvphq.com:25565 — [craftane listing via search](https://craftane-main.onrender.com/servers/520506)

### Inferences
- The "ethical" monetization framing plus only two cheap ranks suggests a no pay-to-win stance. Perks are probably cosmetic or queue-priority only (unconfirmed).
- Lunar integration likely includes Lunar-rendered nametag tiers or Apollo API features (waypoints, team view, notifications), but no source confirms the specific Apollo modules used.

### Gaps
- Rank perks (queue priority, cosmetics, chat color) are not listed in any snippet.
- Cosmetic catalog (kill effects, trails, win effects, titles) not found.
- Staff structure, rules, appeals and punishment system: no PvPHQ-specific source found.
- Clan/guild feature details after the merger: not found.

---

## Unique features and recent changelog (2024-2026)

### Takeaway
Timeline: FlowPvP "Ranked PvP" open beta (early 2026) -> FlowPvP + MCLeagues merge into PvPHQ with Lunar backing (about 16 June 2026) -> $10k PVP Championship (July 2026) -> "The Ranked Update" (T1/T2 release, low-tier overhaul, matchmaking improvements, recalibration; recent, exact date not found). Its key differences from rivals: rating-based tiers instead of tier tests, Lunar-native queueing, 22 regions, replays, post-match analysis and a public match-history website.

### Cited Findings
65. FlowPvP Discord created 20 January 2026; FlowPvP Ranked released as an open beta — [Discord](https://discord.com/servers/pvphq-formerly-flowpvp-1462963503689371805); [TikTok](https://www.tiktok.com/@ceyohh/video/7627748558166314271)
66. FlowPvP was built by YouTuber Flowtives as a replacement for mcpvp.club — [fandom](https://unstable-universe-mc.fandom.com/f/p/4400000000000151166)
67. Merger announced around 16 June 2026 — [X](https://x.com/playPvPHQ/status/2066970865758265373); [wikiindex](https://wikiindex.org/w/PvPHQ)
68. Lunar's launch list (verbatim feature set): "Custom kits, ranked map selection, a replay system, party team fights, advanced kit customization, tournaments, social profiles, post-match analysis, custom shields and trims, totem anti-ghost, and performance optimizations" — [Lunar Client](https://www.lunarclient.com/news/lunar-client-x-pvphq)
69. Domain moved from flowpvp.gg to pvphq.com (both serve PVPHQ-branded leaderboards) — [flowpvp.gg](https://flowpvp.gg/leaderboard/sword); [pvphq.com](https://pvphq.com/leaderboard/sword)
70. The Ranked Update: Tier 2 and Tier 1 released, low-tier ranked overhauled, matchmaking improved, ratings recalibrated — [YouTube](https://www.youtube.com/watch?v=sXbmOuCsPfI)
71. BoardMC listing last updated 23 July 2026 — [BoardMC](https://www.boardmc.com/server/pvphq)

### Inferences
- Competitive takeaways for a Paper 1.21.11 server. The things PvPHQ has that are hardest to copy are Lunar queue integration, the 22-region footprint and a large creator network. Copyable: a rating-to-tier mapping (LT5..HT1 with MT), a public web profile with H2H and rating graphs, replays, post-match analysis, totem anti-ghost, ranked map vetoes, custom shields/trims in the kit editor, and Spear/Cart kits.
- Its reported gaps at launch (unranked queues, 1.8 kits, knockback complaints, missing standard kits) are openings for a competitor. These may have been fixed since.

### Gaps
- No full changelog was accessible (Discord announcements are not indexed, and the site could not be fetched). The exact date of "The Ranked Update" is unknown.
- The source dates are inconsistent. The Discord listing's review snippets were described as around 303 days old, which is hard to square with a guild created in January 2026 and a June merger. Treat the review sentiment as possibly FlowPvP-era.
- MCLeagues' pre-merger features and history were not found.
- 2024-2025 history: PvPHQ did not exist under this name before 2026, so there is nothing to report for that period.
