# Beat PvP Club and PvPHQ on fairness

The practice servers VortexRealm is up against are **PvP Club (mcpvp.club)**, its ranked sister platform **MCPVP.com** (Dream and DrDonut bought MCTiers and relaunched it there in April 2026), **PvPHQ (pvphq.com)** (a June 2026 merger of FlowPvP and MCLeagues, backed by Lunar Client), and the older leaders **Minemen Club**, **PvP Land** and **Hypixel Duels**. They do not win on feature count. VortexRealm already has more modes than any of them: 1.8 combat, bots, arcade, battle pass and SMP. They win on four things. First, a **per-kit tier ladder (LT5..HT1, now with MT mid tiers) that the community recognises**, fed by ratings. Second, **public web profiles** with match history, rating graphs and head-to-head records. Third, **many low-ping regions** (22 for PvPHQ, 38 for MCPVP.com). Fourth, **small, cosmetic-and-convenience stores**: VIP $19.99 permanent plus VIP+ $9.99/month at PvP Club, HQ $10 and HQ+ $20 per 30 days plus coins at PvPHQ. VortexRealm's own README shows it already covers more of their systems than the brief lists: Tier Defense, Tier Challenges, friends, spectating, map vote, first-to-N rounds, tier nametags, regions and alt checks. What is left is mostly visibility, trust and scale. The top priorities are a public profile and leaderboard site with an API, regions that actually run (two or more nodes), an anti-cheat that is tuned and visibly enforced, kit names that match the community ladders, acceptance of the new 26.x clients, and a store that does not sell gameplay advantage. That last point matters because VortexRealm's SMP currently gives VIP and MVP rank kits, which breaks Mojang's rules if those ranks are sold. **Caveat:** every competitor fact here comes from search-engine snippets. The researchers could not fetch mcpvp.club, store.mcpvp.club, pvphq.com, lunarclient.com, modrinth.com or builtbybit.com directly. Treat all figures as point-in-time, and **check every price on the live Tebex stores** before relying on it.

## Snippet-level evidence frames every claim below

Three disambiguations matter before reading any numbers. **PvP Club** (mcpvp.club, eu.mcpvp.club) is the duel/party/FFA practice server, with a Tebex store at store.mcpvp.club and staff-run tier tests that feed MCTiers. **MCPVP.com** is the ranked platform Dream and DrDonut launched after buying MCTiers, announced 2026-04-28 ([Sportskeeda](https://www.sportskeeda.com/minecraft/news-dream-drdonut-acquire-mctiers-launch-competitive-mcpvp-platform)). The PvP Club EU listing now sends players to mcpvp.com/tiers for leaderboards ([mclist.io](https://mclist.io/server/60213)), but **no source confirms whether the two are one network, partners or merged**. The look-alike store at mcpvp-club.com lists perks such as homes and /fly that do not fit a practice server, so this report ignores it as likely unofficial ([mcpvp-club.com](https://mcpvp-club.com/)). **PvPHQ** formed around 16 June 2026 when FlowPvP (Flowtives' "Ranked PvP") and MCLeagues merged, "Powered by @LunarClient" ([X](https://x.com/playPvPHQ/status/2066970865758265373); [Lunar Client](https://www.lunarclient.com/news/lunar-client-x-pvphq)). Its old domain, flowpvp.gg, still serves PvPHQ pages.

The researchers saw none of these sites directly. Snippets give a feature's name and a sentence about it. They do not give kit item lists, rating formulas or full perk lists. Where this report fills a gap by inference, it says so. For the gap analysis, the stated VortexRealm feature list was checked against the plugin's own documentation in `/home/user/claud/vortex-handoff/README.md`. That README shows several "missing" competitor features already exist. Those are marked as covered, not recommended.

## 148 competitor features across twelve areas

Abbreviations in the "Who" column: **PC** PvP Club (mcpvp.club), **MC** MCPVP.com, **HQ** PvPHQ, **MM** Minemen Club, **PL** PvP Land, **HY** Hypixel Duels, **MT** MCTiers, **Comm.** community mods and tools (not server features, but they show what players want).

### Modes and kits: eleven to thirteen modern ladders are the standard

| # | Feature | Who | One-line description | Source |
|---|---|---|---|---|
| 1 | Ranked 1v1 queue | PC, HQ | Rated duels across every kit; the core loop on both servers | [mclist.io](https://mclist.io/server/60213); [Lunar](https://www.lunarclient.com/news/lunar-client-x-pvphq) |
| 2 | Unranked 1v1 queue | PC | Casual duels with no rating change. PvPHQ was criticised for not having one at launch | [mclist.io](https://mclist.io/server/60213); [Discord HQ](https://discord.com/servers/pvphq-1462963503689371805) |
| 3 | Sword kit | PC, MC, HQ | Modern-combat sword duel ladder | [AutoQueue mod](https://modrinth.com/mod/autoqueue-mcpvpclub); [HQ Sword](https://pvphq.com/leaderboard/sword) |
| 4 | Axe kit | PC, HQ | Axe and shield-break duels | [AutoQueue](https://modrinth.com/mod/autoqueue-mcpvpclub); [HQ Axe](https://pvphq.com/leaderboard/axe) |
| 5 | Mace kit | PC, MC, HQ | Wind-charge and mace smash duels | [AutoQueue](https://modrinth.com/mod/autoqueue-mcpvpclub); [HQ Mace](https://flowpvp.gg/leaderboard/mace) |
| 6 | UHC kit | PC, MC, HQ | Rod, lava, water and gapple UHC-style duels | [mclist.io](https://mclist.io/server/60213); [HQ UHC](https://pvphq.com/leaderboard/uhc) |
| 7 | Pot kit | PC, MC, HQ | Splash-potion healing duels | [AutoQueue](https://modrinth.com/mod/autoqueue-mcpvpclub); [HQ Pot](https://pvphq.com/leaderboard/pot) |
| 8 | NethPot / NethOP | PC, MC, HQ | Netherite armour plus potions | [AutoQueue](https://modrinth.com/mod/autoqueue-mcpvpclub); [HQ NethPot](https://pvphq.com/leaderboard/netherite_pot) |
| 9 | SMP kit | PC, MC, HQ | Survival-style gear duel | [AutoQueue](https://modrinth.com/mod/autoqueue-mcpvpclub); [BoardMC guide](https://www.boardmc.com/post/mcpvp-guide-kits-tiers-rankings) |
| 10 | Diamond SMP | MC, HQ | Diamond-gear SMP variant with its own ladder | [BoardMC guide](https://www.boardmc.com/post/mcpvp-guide-kits-tiers-rankings); [HQ DiaSMP](https://pvphq.com/leaderboard/diamond_smp) |
| 11 | Vanilla kit | PC, HQ | Probably crystal/cart "vanilla" PvP, using MCTiers naming (inferred) | [AutoQueue](https://modrinth.com/mod/autoqueue-mcpvpclub); [HQ Vanilla](https://flowpvp.gg/leaderboard/vanilla) |
| 12 | Crystal ladder | MC | End-crystal ladder | [mcpvp.com/tiers](https://www.mcpvp.com/tiers) |
| 13 | Spear kit (1.21.11) | MC, HQ | New spear weapon. HQ's spear_mace ladder had about 18,448 ranked players | [MC Spear](https://www.mcpvp.com/tiers/spear); [HQ Spear](https://pvphq.com/leaderboard/spear_mace) |
| 14 | Shield kit | MC | Shield-centred skill kit | [MC Shield](https://www.mcpvp.com/tiers/shield) |
| 15 | Creeper kit | MC | Creeper-egg explosive kit | [MC Creeper](https://www.mcpvp.com/tiers/creeper) |
| 16 | Cart (TNT minecart) kit | MC, HQ | Minecart-TNT PvP. HQ ladder about 11,320 players | [horizon #11175](https://github.com/horizon-rust/horizon/issues/11175); [HQ Cart](https://pvphq.com/leaderboard/cart) |
| 17 | HT Cart bracket | HQ | Separate ladder that appears to be high-tier-only (inferred from the URL) | [HQ HT Cart](https://pvphq.com/leaderboard/ht_cart) |
| 18 | Bow kit | MC | Archery community kit | [BoardMC guide](https://www.boardmc.com/post/mcpvp-guide-kits-tiers-rankings) |
| 19 | Kit categories | MC | Kits grouped as Skill (Sword, Shield, Pot, Spear, Mace), Vanilla and Community | [BoardMC guide](https://www.boardmc.com/post/mcpvp-guide-kits-tiers-rankings) |
| 20 | FFA arenas | PC, HQ | Drop-in free-for-all arenas | [mclist.io](https://mclist.io/server/60213); [Discord HQ](https://discord.com/servers/pvphq-1462963503689371805) |
| 21 | 2v2 and 4v4 teams | PC | Team duel formats | [mclist.io](https://mclist.io/server/60213) |
| 22 | 1.8 legacy modes | PL | NoDebuff, BuildUHC, Boxing, Bridge, Sumo, Gapple | [VoxelRank PL](https://voxelrank.com/server/204-pvp-land) |
| 23 | AI practice bots | PL | Bots with difficulty settings from easy to impossible | [pvp.land](https://pvp.land/); [mcserverpost](https://mcserverpost.com/2023/09/10/pvp-land/) |
| 24 | Cross-version support | PL | Several client versions accepted | [pvp.land](https://pvp.land/) |
| 25 | 1.21.11 target | PC | Join on 1.21.2+, 1.21.11 recommended | [Modrinth PC](https://modrinth.com/server/pvp-club); [Discord PC](https://discord.com/servers/mcpvp-club-1477487779498692722) |
| 26 | 26.x client support | PC, HQ | Listings claim "1.21 – 26.3"; HQ recommends 26.2, and one player could not join on 26.3 | [anyserver.pro](https://anyserver.pro/server/224/pvp-club); [BoardMC HQ](https://www.boardmc.com/server/pvphq) |
| 27 | Free kits, no gear grind | PC | Every kit is handed out; nothing to farm | [mcserverip](https://mcserverip.com/ip/mcpvp-club) |

### Ranked and tiers: from tester judgement to rating-driven tiers

| # | Feature | Who | One-line description | Source |
|---|---|---|---|---|
| 28 | Staff tier tests | PC | A tester duels you and places you from LT5 to HT1 for that gamemode | [mcpvp.club/tiertest](https://mcpvp.club/tiertest) |
| 29 | 30-day retest cooldown | PC | One test per gamemode every 30 days | [tiertest](https://mcpvp.club/tiertest) |
| 30 | Per-gamemode test Discords | PC | Tests are requested in #request-test in each gamemode's own Discord | [tiertest](https://mcpvp.club/tiertest) |
| 31 | Premium-only testing | PC | A paid Java account is needed to be tested | [tiertest](https://mcpvp.club/tiertest) |
| 32 | Current and peak tier | PC | The latest result is shown publicly, and the best result is also tracked | [tiertest](https://mcpvp.club/tiertest) |
| 33 | MCTiers sync | PC | Tiers appear on MCTiers and PvP Club | [tiertest](https://mcpvp.club/tiertest) |
| 34 | /tiertest region queue | MT | Pick a gamemode and region, then wait to be pulled into a private arena with the official kit | [MCTiers guide](https://mctiers.gg/guides/how-to-get-tier-tested) |
| 35 | Peak-tier points | MT | HT1 60, LT1 45, HT2 30, LT2 20, HT3 10, LT3 6, HT4 4, LT4 3, HT5 2, LT5 1 | [mctier.us](https://mctier.us/tr/guides/minecraft-pvp-tiers-explained) |
| 36 | Player Rating | MC | Regular matchmaking feeds a per-kit rating | [BoardMC guide](https://www.boardmc.com/post/mcpvp-guide-kits-tiers-rankings) |
| 37 | Rating-unlocked tier test | MC | A high enough rating qualifies you for a test | [BoardMC guide](https://www.boardmc.com/post/mcpvp-guide-kits-tiers-rankings); [EloTiers](https://elotiers.com/guides/how-minecraft-pvp-ratings-work) |
| 38 | Tier Defense match | MC | If your rating falls below what your tier expects, you must beat someone from that tier | [BoardMC guide](https://www.boardmc.com/post/mcpvp-guide-kits-tiers-rankings) |
| 39 | MT mid tier | MC, HQ | HT, MT and LT bands with five divisions each, so 15 steps in total | [9minecraft addon](https://www.9minecraft.net/pvphq-tiertagger-addon-mod/); [mcpvp.com/tiers](https://www.mcpvp.com/tiers) |
| 40 | Points thresholds | MC | HT1 400+, HT2 250+, LT2 150+ points | [mcpvp.com/tiers](https://www.mcpvp.com/tiers) |
| 41 | Beta tiers and Season Zero | MC | Tiers are labelled beta and will be reset at the end of beta | [MC Mace](https://www.mcpvp.com/tiers/mace); [YouTube](https://www.youtube.com/watch?v=bwwp3dg3xRs) |
| 42 | Legacy tier tab | MC | Old MCTiers-era tiers kept as an archive view (inferred) | [legacy view](https://www.mcpvp.com/tiers?version=legacy) |
| 43 | Game-stage ladders | MC | Grouped early-game, late-game and end-game leaderboards | [early-game](https://www.mcpvp.com/tiers/early-game); [end-game](https://www.mcpvp.com/tiers/end-game) |
| 44 | Overall titles | MC | Account titles from "Combat Rookie" up to "Grandmaster" | [BoardMC MC](https://www.boardmc.com/server/mcpvp) |
| 45 | Per-kit TR | HQ | Tier Rating per kit, for example "MT2 noouv 374 TR" on Cart | [HQ Cart](https://pvphq.com/leaderboard/cart) |
| 46 | Overall PTS ladder | HQ | Cross-kit points; 81,746 players ranked at the time of indexing | [HQ Overall](https://pvphq.com/leaderboard/overall) |
| 47 | Tier badge on ladder rows | HQ | Tier label shown next to the name, for example "HT2 clesa 114 TR" | [HQ Sword](https://pvphq.com/leaderboard/sword) |
| 48 | Gated top tiers | HQ | Tier 1 and Tier 2 only opened in "The Ranked Update", which also recalibrated ratings | [YouTube](https://www.youtube.com/watch?v=sXbmOuCsPfI) |
| 49 | Low-tier overhaul | HQ | The same update reworked low-tier ranked and improved matchmaking | [YouTube](https://www.youtube.com/watch?v=sXbmOuCsPfI) |
| 50 | Match-derived public ratings | HQ | Ratings come from recorded matches, so they behave like Elo; EloTiers imports them | [EloTiers](https://elotiers.com/guides/minecraft-pvp-tier-lists-compared) |
| 51 | Numbered seasons | MM | Long-running ranked seasons (Season 14) with a "Top ELO" board | [minemen.shop](https://minemen.shop/) |
| 52 | Anti-boost rules | MM | Elo boosting and alting are banned in ranked; alts are allowed only outside the top 20 | [Minemen rules](http://minemen.club/rules) |
| 53 | Training tiers | McTrainer | "From one run to HT1" practice-tier marketing | [mctrainer.club](https://mctrainer.club/announcements/from-one-run-to-ht1-how-training-tiers-work) |
| 54 | Placement games | Comm. | Fan Elo mod: 10 placement games per kit, with no Elo change during placements | [MCPvP Ranked](https://modrinth.com/mod/mcpvp-ranked) |
| 55 | Ore-ladder divisions | Comm. | Coal → Netherite ranks with divisions I–III, plus bonus Elo for beating tiered players | [9minecraft](https://www.9minecraft.net/mcpvp-ranked-mod/) |

### Queues and matchmaking: regions are the moat

| # | Feature | Who | One-line description | Source |
|---|---|---|---|---|
| 56 | Hotbar queue sword | PC, MC | A sword in the hotbar opens a translucent queue GUI | [horizon #11175](https://github.com/horizon-rust/horizon/issues/11175) |
| 57 | In-game region switch | PC | NA (Ashburn), EU (Frankfurt), AS (Singapore), AU (Sydney) | [Modrinth PC](https://modrinth.com/server/pvp-club) |
| 58 | EU node | PC | Separate eu.mcpvp.club address | [mclist.io](https://mclist.io/server/60213) |
| 59 | 38 locations | MC | NA 14, EU 8, LATAM 5, Asia 5, ME 2, Africa 1, Oceania 3 | [BoardMC guide](https://www.boardmc.com/post/mcpvp-guide-kits-tiers-rankings) |
| 60 | 22 locations | HQ | Launch footprint across NA, EU, Asia, Middle East, Oceania | [Lunar](https://www.lunarclient.com/news/lunar-client-x-pvphq) |
| 61 | Queue from Lunar Client | HQ | Join queues from the client UI | [Lunar](https://www.lunarclient.com/news/lunar-client-x-pvphq) |
| 62 | Skill-based matchmaking | HQ | Opponents are paired by rating | [BoardMC HQ](https://www.boardmc.com/server/pvphq) |
| 63 | Queue priority when full | PC | VIP+ perk | [VIP+](https://store.mcpvp.club/package/6877860) |
| 64 | Queue bypass | HQ | HQ+ perk | [HQ+](https://store.mcpvp.club/package/6877860) |
| 65 | Ranked queue-priority ladder | MM | PRO gets #2 queue priority | [Minemen ranks](https://store.minemen.club/category/ranks) |
| 66 | Auto-queue mods | Comm. | Client mods re-queue players automatically | [AutoQueue](https://modrinth.com/mod/autoqueue-mcpvpclub) |
| 67 | Queue snipers | Comm. | Bots grab tier-test waitlist spots, which shows test capacity is the bottleneck | [queuesniper](https://queuesniper.com/) |

### Matches and arenas: map choice, replays, analysis, fair hits

| # | Feature | Who | One-line description | Source |
|---|---|---|---|---|
| 68 | Ranked map selection | HQ | Players get some say in ranked maps (pick or ban is not specified) | [Lunar](https://www.lunarclient.com/news/lunar-client-x-pvphq) |
| 69 | Duel map selector | MM | Choose from 100+ maps (PRO perk) | [Minemen ranks](https://store.minemen.club/category/ranks) |
| 70 | Custom "epic" arenas | HQ | Players praise the custom maps | [Discord HQ](https://discord.com/servers/pvphq-1462963503689371805) |
| 71 | Named maps per kit | MC | Match records name the map | [@CPVPVOID](https://www.mcpvp.com/@CPVPVOID) |
| 72 | Scored matches | MC | Records carry a score, which suggests first-to-N rounds (inferred) | [@pzmp](https://www.mcpvp.com/@pzmp) |
| 73 | Replay system | HQ, PL | Watch matches back | [Lunar](https://www.lunarclient.com/news/lunar-client-x-pvphq); [VoxelRank PL](https://voxelrank.com/server/204-pvp-land) |
| 74 | Post-match analysis | HQ | "Detailed post-match analysis" after each fight | [Lunar](https://www.lunarclient.com/news/lunar-client-x-pvphq) |
| 75 | Totem anti-ghost | HQ | Server-side fix for desynced "ghost" totem pops | [Lunar](https://www.lunarclient.com/news/lunar-client-x-pvphq) |
| 76 | Hit-registration focus | HQ | Marketed as better hit-reg than mcpvp.club | [fandom post](https://unstable-universe-mc.fandom.com/f/p/4400000000000151166) |
| 77 | Automated anti-cheat duels | MC | Anti-cheat checks built into ranked play | [Sportskeeda](https://www.sportskeeda.com/minecraft/news-dream-drdonut-acquire-mctiers-launch-competitive-mcpvp-platform) |
| 78 | Private test arena | MT | Official kit in an isolated arena for tests | [MCTiers guide](https://mctiers.gg/guides/how-to-get-tier-tested) |
| 79 | Long-range spectating | HQ | Spectating range of 300x300 in UHC (HQ+ perk) | [HQ+](https://store.pvphq.com/package/7548108) |
| 80 | /tpv | MM | Teleport-to-player spectate tool (PRO) | [Minemen ranks](https://store.minemen.club/category/ranks) |
| 81 | Late join | HQ | Join UHC games up to 20 minutes late | [HQ+](https://store.pvphq.com/package/7548108) |

### Lobby: thin public detail, mostly hotbar items and movement toys

| # | Feature | Who | One-line description | Source |
|---|---|---|---|---|
| 82 | "Create Party" nether star | PC | Hotbar item that makes a party | [AutoQueue](https://modrinth.com/mod/autoqueue-mcpvpclub) |
| 83 | Head-icon GUIs and custom nametags | PC | Seen in client rendering bug reports | [horizon #4116](https://github.com/horizon-rust/horizon/issues/4116) |
| 84 | Kit editor | PC, MC, HQ | Rearrange the inventory and hotbar layout per kit | [BoardMC guide](https://www.boardmc.com/post/mcpvp-guide-kits-tiers-rankings); [Lunar](https://www.lunarclient.com/news/lunar-client-x-pvphq) |
| 85 | Custom kit slots | PC | 3 base (inferred), 6 with VIP, 12 with VIP+ | [VIP](https://store.mcpvp.club/package/6877832) |
| 86 | Elytra and wind charges at spawn | PC | Lobby movement toys (VIP) | [VIP](https://store.mcpvp.club/package/6877832) |
| 87 | /elytra, /spear, /fly in lobby | HQ | Lobby movement perks (HQ+) | [HQ+](https://store.pvphq.com/package/7548108) |
| 88 | Lobby fly | MM | PRO perk | [Minemen ranks](https://store.minemen.club/category/ranks) |
| 89 | Sidebar customisation | MM | MVP perk | [Minemen ranks](https://store.minemen.club/category/ranks) |
| 90 | Tab priority | PC, HQ | Paid ranks sort to the top of the tab list | [VIP](https://store.mcpvp.club/package/6877832); [HQ+](https://store.pvphq.com/package/7548108) |

### Cosmetics: vanilla item customisers instead of particles

| # | Feature | Who | One-line description | Source |
|---|---|---|---|---|
| 91 | Armor trim customiser | PC, HQ | Apply trims to kit armour | [VIP](https://store.mcpvp.club/package/6877832); [Lunar](https://www.lunarclient.com/news/lunar-client-x-pvphq) |
| 92 | Shield pattern customiser | PC, HQ | Banner designs on kit shields | [VIP](https://store.mcpvp.club/package/6877832); [Lunar](https://www.lunarclient.com/news/lunar-client-x-pvphq) |
| 93 | Shulker colour customiser | PC | Recolour kit shulkers | [VIP](https://store.mcpvp.club/package/6877832) |
| 94 | Item renaming | PC | Custom names on kit items | [VIP](https://store.mcpvp.club/package/6877832) |
| 95 | Name colour | PC | Purple name (VIP) | [VIP](https://store.mcpvp.club/package/6877832) |
| 96 | Display name customiser | PC | VIP+ perk | [VIP+](https://store.mcpvp.club/package/6877860) |
| 97 | Custom rank tag | HQ | /custom tag (HQ+) | [HQ+](https://store.pvphq.com/package/7548108) |
| 98 | Lunar-exclusive cosmetics | HQ | Client cosmetics through the partnership | [Lunar](https://www.lunarclient.com/news/lunar-client-x-pvphq) |
| 99 | Cosmetic armour colours | MM | 9 colours on MVP, basic set on PRO | [Minemen ranks](https://store.minemen.club/category/ranks) |
| 100 | Earned cosmetic path | HY | "Duelist's Odyssey": titles, prefix icons, kill effects, victory dances unlocked by wins, in rarity tiers | [Hypixel Wiki](https://hypixel.fandom.com/wiki/Duels/Duelist%27s_Odyssey) |
| 101 | Verified badge | HQ | Profile badge granted by the Medal quest | [Medal quest](https://medal.tv/quests/8HWT-MakzW/pvphq_x_medal) |

### Social: parties are the second product

| # | Feature | Who | One-line description | Source |
|---|---|---|---|---|
| 102 | Party team duels | PC, HQ | Party vs party | [Modrinth PC](https://modrinth.com/server/pvp-club); [Lunar](https://www.lunarclient.com/news/lunar-client-x-pvphq) |
| 103 | Party FFA | PC | Free-for-all inside a party | [Modrinth PC](https://modrinth.com/server/pvp-club) |
| 104 | Host Battle | PC | One host fights the whole party (VIP+) | [VIP+](https://store.mcpvp.club/package/6877860) |
| 105 | Custom party fights | PC | Ad-hoc custom fights with friends | [Discord PC](https://discord.com/servers/mcpvp-club-1477487779498692722) |
| 106 | Party size caps | PC | 8 by default, 16 on VIP, 32 on VIP+ | [VIP](https://store.mcpvp.club/package/6877832); [VIP+](https://store.mcpvp.club/package/6877860) |
| 107 | Public parties | PC | Open parties anyone can join (VIP+) | [VIP+](https://store.mcpvp.club/package/6877860) |
| 108 | /party announce | HQ | Broadcast a party every 2 minutes (HQ+) | [HQ+](https://store.pvphq.com/package/7548108) |
| 109 | Larger party size | HQ | HQ+ perk | [HQ+](https://store.pvphq.com/package/7548108) |
| 110 | Guilds | HQ | Listed in the FlowPvP era; current status uncertain | [Discord FlowPvP](https://discord.com/servers/flowpvp-1462963503689371805) |
| 111 | Clubs | MM | Create a club of up to 50 members (PRO) | [Minemen ranks](https://store.minemen.club/category/ranks) |
| 112 | Friends list | MM | Up to 200 friends (PRO) | [Minemen ranks](https://store.minemen.club/category/ranks) |
| 113 | Head-to-head rivals | HQ | W-L and win % per rival, with "You lead / You trail" | [HQ profile](https://pvphq.com/player/ef37325f-3471-470c-ab1f-3e3b9b6e0bbd) |
| 114 | /disguise in unranked | HQ | Hide your identity in casual queues (HQ+) | [HQ+](https://store.pvphq.com/package/7548108) |
| 115 | Party-recruit chat culture | Comm. | "222 for axe" posts turned into clickable invites by mods | [Party Inviter](https://modrinth.com/project/ZHWdM4YU) |

### Events: always-on brackets plus occasional big-money championships

| # | Feature | Who | One-line description | Source |
|---|---|---|---|---|
| 116 | 24/7 automated tournaments | PC | Claims $15,000+ paid out (self-reported) | [mclist.io](https://mclist.io/server/60213) |
| 117 | Player-hosted tournaments | HQ | HQ+ can host a tournament every 20 minutes | [HQ+](https://store.pvphq.com/package/7548108) |
| 118 | Event and tournament hosting | MM | PRO hosts events; ACE hosts and force-starts tournaments | [Minemen ranks](https://store.minemen.club/category/ranks) |
| 119 | Weekly events | HQ | Advertised in the Discord listing; format unknown | [Discord HQ](https://discord.com/servers/pvphq-1462963503689371805) |
| 120 | $10k PVP Championship | HQ | With Tubbo Events, 16–18 July 2026, A-Tier on Liquipedia | [Liquipedia](https://liquipedia.net/lab/Minecraft/PvPHQ/PVP_Championship) |
| 121 | Qualifier pipeline | HQ | Closed qualifier plus an open qualifier whose top 12 advanced | [Open Qualifiers](https://liquipedia.net/lab/Minecraft/PvPHQ/PVP_Championship/Open_Qualifiers) |
| 122 | "Big events" programme | MC | Events to organise the competitive scene | [Sportskeeda](https://www.sportskeeda.com/minecraft/news-dream-drdonut-acquire-mctiers-launch-competitive-mcpvp-platform) |
| 123 | Prize tournaments | MM | Tournaments with real prizes | [minemen.shop](https://minemen.shop/) |
| 124 | Automated tournaments | PL | Scheduled brackets | [pvp.land](https://pvp.land/) |

### Store and ranks: two or three packages, cosmetics plus convenience

| # | Feature | Who | One-line description | Source |
|---|---|---|---|---|
| 125 | Permanent base rank | PC | VIP $19.99 one-time | [VIP](https://store.mcpvp.club/package/6877832) |
| 126 | Gated subscription | PC | VIP+ $9.99 per 30 days; VIP is required to buy it | [VIP+](https://store.mcpvp.club/package/6877860) |
| 127 | Timed ranks | HQ | HQ $10 and HQ+ $20, each 30 days | [HQ ranks](https://store.pvphq.com/category/ranks) |
| 128 | Coin currency | HQ | $10 = 1,000 coins, with bulk bonuses | [HQ coins](https://store.pvphq.com/category/coins) |
| 129 | Rank gifting | HQ | Coins can gift ranks (one package page contradicts this) | [HQ coins](https://store.pvphq.com/category/coins) |
| 130 | Upgrade pricing | MM | Upgrades priced near the price difference, for example PRO→ACE $30.99 | [Minemen pkg](https://store.minemen.club/package/4539727) |
| 131 | Free rank via clipping | HQ | Medal.tv quest gives HQ+ for linking an account and clipping | [Medal quest](https://medal.tv/quests/8HWT-MakzW/pvphq_x_medal) |
| 132 | Gift-card promo | HQ | Free $4 Tebex gift card promo (expired) | [HQ+](https://store.pvphq.com/package/7548108) |
| 133 | Cosmetics-only store | PL | Rated "cosmetics only" by a listing site | [VoxelRank PL](https://voxelrank.com/server/204-pvp-land) |

### Website and Discord: the profile site is the scoreboard

| # | Feature | Who | One-line description | Source |
|---|---|---|---|---|
| 134 | Public stat profiles | MC | Kills, deaths, K/D, wins, W/L, current and best streak, kit rankings | [BoardMC guide](https://www.boardmc.com/post/mcpvp-guide-kits-tiers-rankings) |
| 135 | Vanity profile URLs | MC, HQ | /@name, /profile/name, /player/name | [@DrDonutt](https://www.mcpvp.com/@DrDonutt); [HQ ohLama](https://pvphq.com/player/ohLama) |
| 136 | Web match history | MC, HQ | Kit, map, opponent and score per match | [@CPVPVOID](https://www.mcpvp.com/@CPVPVOID); [HQ matches](https://pvphq.com/player/a048f59e-3cd3-4e55-ad6a-052633b27ab7/matches) |
| 137 | Rating history graph | HQ | Per-kit rating chart | [HQ profile](https://pvphq.com/player/cc8f8e29-2cb7-48d2-93fb-8c52679cd3c7) |
| 138 | Career totals and best tier | HQ | Kits ranked, matches, points, best tier, most-played rivals | [HQ profile](https://pvphq.com/player/f60270d3-5d95-4a0d-9c5e-e25dcbe0335b) |
| 139 | Region-filtered ladders | MC | Region column and filters on leaderboards | [mcpvp.com/tiers](https://www.mcpvp.com/tiers) |
| 140 | Server directory | MC | mcpvp.com lists servers, for example /server/mcpvp.club | [MC directory](https://www.mcpvp.com/server/mcpvp.club) |
| 141 | Lunar Wrapped presence | PC | Server leaderboard in Lunar's 2025 Wrapped | [Lunar Wrapped](https://wrapped.lunarclient.com/leaderboards/2025/servers/mcpvp) |
| 142 | Very large Discords | HQ, MC | HQ about 66,456 members; MCPVP reportedly passed 42,000 | [Discord HQ](https://discord.com/servers/pvphq-1462963503689371805); [YouTube](https://www.youtube.com/watch?v=dyWv1kpUyqI) |
| 143 | Clip hub | HQ | Medal server page that collects clips | [Medal HQ](https://medal.tv/games/minecraft/servers/4j8RSb-lojq8lz/pvphq) |
| 144 | Tier Tagger mods | Comm. | Show MCPVP or PvPHQ tiers on nametags, tab and chat | [HQ addon](https://modrinth.com/project/PzNBY0IN); [MC tagger](https://modrinth.com/project/DCdFdNnR) |

### Anti-cheat, staff and quality of life

| # | Feature | Who | One-line description | Source |
|---|---|---|---|---|
| 145 | Lunar anti-cheat support | HQ | Anti-cheat help through the Lunar integration | [BoardMC HQ](https://www.boardmc.com/server/pvphq) |
| 146 | In-house anti-cheat | MM | "AntiGamingChair"; v3.2 claims 40% fewer false positives | [minemen.shop](https://minemen.shop/); [fandom](https://minecraftservers.fandom.com/wiki/Minemen_Club) |
| 147 | Slow chat and link controls | HQ | HQ+ bypasses slow chat and gets clickable links, which implies both are moderated by default | [HQ+](https://store.pvphq.com/package/7548108) |
| 148 | Duel toggle, join-full, performance | various | Duel-request toggle (a BuiltByBit MCPVP clone setup), joining full servers (HQ+), Lunar performance tuning | [BuiltByBit](https://builtbybit.com/resources/mcpvp-setup-modern-practice.103968/); [HQ+](https://store.pvphq.com/package/7548108); [Lunar](https://www.lunarclient.com/news/lunar-client-x-pvphq) |

The anti-cheat options a Paper server would actually use are also well mapped. **Grim** is the most recommended free option (it predicts movement and flags little falsely, but needs config per gamemode). **Polar** is paid and rated strongest for large PvP networks. **Vulcan** is cheaper and often paired with Grim ([mcvoting](https://mcvoting.com/blog/best-minecraft-server-anti-cheat-plugins); [SpigotMC](https://www.spigotmc.org/threads/best-ac-2025.687332/)).

## Ratings now decide tiers, and testers only confirm them

### LT5..HT1 tiers and tests

PvP Club still runs the classic MCTiers model. A human tester duels you in one gamemode and gives you a tier from **LT5 (entry) to HT1 (top)**. You can retest **once every 30 days per gamemode**. You request a test in **#request-test on that gamemode's own Discord**, and you need a **premium Java account**. Your current tier is always your latest result, and your **peak tier is tracked separately** ([mcpvp.club/tiertest](https://mcpvp.club/tiertest)). MCTiers adds the mechanics: run /tiertest, pick gamemode and region, and wait until a tester in your region pulls you into a private arena with the official kit. Testers judge more than round wins ([MCTiers guide](https://mctiers.gg/guides/how-to-get-tier-tested)). The weakness is capacity. Queue-sniper bots exist to grab tier-test waitlist spots ([queuesniper](https://queuesniper.com/)), which shows demand is far above what the testers can handle.

MCPVP.com automates the funnel. Ordinary matches feed a **Player Rating**, which can qualify you for a **Tier Test**. If your rating falls below what your tier expects, you face a **Tier Defense** match against someone from that tier ([BoardMC guide](https://www.boardmc.com/post/mcpvp-guide-kits-tiers-rankings)). No source mentions time-based decay, so Tier Defense appears to take its place. Tiers also gained a **mid band (MT)** and carry point values: **HT1 at 400+, HT2 at 250+, LT2 at 150+**. All current tiers are marked **beta and will be reset**, with a "Season Zero" label ([mcpvp.com/tiers](https://www.mcpvp.com/tiers); [MC Mace](https://www.mcpvp.com/tiers/mace)). Compare MCTiers, which scores peak tiers on a steep curve from HT1 = 60 down to LT5 = 1 ([mctier.us](https://mctier.us/tr/guides/minecraft-pvp-tiers-explained)).

### TR and PTS at PvPHQ

PvPHQ drops human tests altogether. Each kit has a **TR (likely "Tier Rating")** that maps onto **15 steps from LT5 to HT1 through MT** ([9minecraft](https://www.9minecraft.net/pvphq-tiertagger-addon-mod/)). An overall **PTS** total ranks players across kits, with 81,746 players on the overall ladder when indexed ([HQ Overall](https://pvphq.com/leaderboard/overall)). Top TR values are small, from 114 on Sword to 374 on Cart ([HQ Sword](https://pvphq.com/leaderboard/sword); [HQ Cart](https://pvphq.com/leaderboard/cart)). That suggests a points-above-floor scale rather than a 1000-base Elo, though this is an inference. EloTiers treats PvPHQ as the one major list that publishes **match-derived** ratings rather than tester-assigned tiers ([EloTiers](https://elotiers.com/guides/minecraft-pvp-tier-lists-compared)). PvPHQ also held back the top bands: **"The Ranked Update" released Tier 2 and Tier 1**, overhauled low-tier ranked and recalibrated everyone ([YouTube](https://www.youtube.com/watch?v=sXbmOuCsPfI)). The K-factor, placement count and TR thresholds are not public anywhere.

### Matchmaking and regions

Region count is the clearest dividing line. PvP Club lets players switch between **NA (Ashburn), EU (Frankfurt), AS (Singapore) and AU (Sydney)** in game ([Modrinth PC](https://modrinth.com/server/pvp-club)). PvPHQ launched on **22 locations** and lets players queue from inside Lunar Client ([Lunar](https://www.lunarclient.com/news/lunar-client-x-pvphq)). MCPVP.com claims **38 locations in 7 regions**, 14 of them in North America ([BoardMC guide](https://www.boardmc.com/post/mcpvp-guide-kits-tiers-rankings)). Within a region, PvPHQ advertises skill-based pairing and **ranked map selection** ([BoardMC HQ](https://www.boardmc.com/server/pvphq)). Nothing public describes their search-widening rules, rematch buttons or match-start presentation. No source mentions cages, capsules or elevators at either server, so VortexRealm's capsule/elevator start is a differentiator as far as the evidence goes.

### Kit editor

Every competitor has a per-kit layout editor ([BoardMC guide](https://www.boardmc.com/post/mcpvp-guide-kits-tiers-rankings); [Lunar](https://www.lunarclient.com/news/lunar-client-x-pvphq)). PvP Club monetises the editor itself. Saved **"Vanilla/Custom" kit slots** go from an inferred 3, to 6 with VIP, to 12 with VIP+, and the cosmetic customisers (trim, shield pattern, shulker colour, item names) sit inside the same flow ([VIP](https://store.mcpvp.club/package/6877832); [VIP+](https://store.mcpvp.club/package/6877860)). PvPHQ markets "custom kits" and "advanced kit customization" together with custom shields and trims ([Lunar](https://www.lunarclient.com/news/lunar-client-x-pvphq)).

### Events

PvP Club advertises **24/7 automated tournaments** and claims more than $15,000 paid out ([mclist.io](https://mclist.io/server/60213)). PvPHQ sells hosting as a perk (a tournament every 20 minutes on HQ+). It also co-ran a **$10,000 championship** with Tubbo Events, with closed and open qualifiers, and it is listed on Liquipedia ([Liquipedia](https://liquipedia.net/lab/Minecraft/PvPHQ/PVP_Championship)). Minemen ties hosting to its rank ladder: PRO hosts events, and ACE hosts and force-starts tournaments ([Minemen ranks](https://store.minemen.club/category/ranks)). The pattern has three layers: always-on automated brackets for retention, player hosting as a paid convenience, and a few big-prize events for press coverage.

## Stores stay small: one permanent rank, one subscription

| Server | Package | Price (as indexed) | Term | Key perks | Source |
|---|---|---|---|---|---|
| PvP Club | VIP | **$19.99** | Permanent | Armor trim, shield pattern and shulker colour customisers; item renaming; +3 kit slots (6); party 8→16; purple name; tab priority; elytra and wind charges at spawn | [VIP](https://store.mcpvp.club/package/6877832) |
| PvP Club | VIP+ | **$9.99** | 30 days, needs VIP | Display name customiser; queue priority when full; +9 kit slots (12); party 32; public parties; Host Battle | [VIP+](https://store.mcpvp.club/package/6877860) |
| PvPHQ | HQ | **$10.00** | 30 days | Featured package; late-join UHC and spectating range mentioned; full list not indexed | [HQ](https://store.pvphq.com/package/7544926) |
| PvPHQ | HQ+ | **$20.00** | 30 days | /custom tag; slow-chat and queue bypass; clickable links; tab priority; /elytra, /spear, lobby /fly; tournament hosting every 20 min; larger parties; /party announce; /disguise in unranked; UHC late-join, join full, 300x300 spectating | [HQ+](https://store.pvphq.com/package/7548108) |
| PvPHQ | Coins | **$10 / 1,000; $25 / 2,500; $50 / 5,250 (+5%)**; 11,500 (+15%) pack price unclear, probably about $100 | One-time | Longer rank durations, gifting, cosmetics (one package page says /gift and /shop are unavailable with coins) | [HQ coins](https://store.pvphq.com/category/coins) |
| Minemen | VIP / PRO / MVP / ACE / ACE Bundle | **$7.49 / $14.99 / $29.99 / $44.99 / $59.99** | One-time | PRO: #2 queue priority, 200 friends, 50-member club, lobby fly, 100+ map selector, /tpv, event hosting; MVP: sidebar, 9 armour colours; ACE: tournament hosting and force-start | [Minemen ranks](https://store.minemen.club/category/ranks) |

These stores make money in different ways. A PvP Club supporter who keeps VIP+ for a year pays about **$139.87** ($19.99 plus 12 × $9.99). The same year on PvPHQ's HQ+ costs **$240**. Minemen's top one-time bundle is **$59.99**. Upgrades are priced near the difference between ranks, though not exactly: PRO→ACE is $30.99 against a $30.00 gap, and VIP→MVP was $20.39, discounted from $23.99 ([Minemen pkg](https://store.minemen.club/package/4539727); [pkg 3450691](https://store.minemen.club/package/3450691)). Newer servers are moving to subscriptions: PvPHQ sells only 30-day ranks, and PvP Club stacks a monthly tier on a permanent one. **No crates or battle passes were found on any of these stores.** Hypixel instead gives its showiest cosmetics as rewards for wins ([Hypixel Wiki](https://hypixel.fandom.com/wiki/Duels/Duelist%27s_Odyssey)).

The perks they sell fall into the same few groups: queue priority or bypass, bigger parties and party modes, the right to host events, more kit slots, name, tag and display-name customisation, cosmetic armour (trims, shield patterns), lobby movement toys, and tab priority. None of these changes a fight's outcome. That fits Mojang's rules: the **Minecraft Usage Guidelines allow selling cosmetics but not capes or cape look-alikes** ([Minecraft Usage Guidelines](https://www.minecraft.net/en-us/usage-guidelines)), and hosting guides sum the rule up as **no gameplay advantage for paying players**. The same guides call crates, currencies and battle passes grey areas, and warn that the guidelines can change ([GameServerKings](https://www.gameserverkings.com/knowledge-base/minecraft/monetising-your-server/); [space-node](https://space-node.net/blog/minecraft-eula-monetization-rules-2026)). Queue priority is a mild access advantage that all three competitors sell anyway. **All prices above come from search-index snapshots of unknown date; check them on the live stores before using them as anchors.**

## VortexRealm already leads on breadth, so the gaps are trust, reach and visibility

### Covered or ahead of the field

Checked against the plugin's README, VortexRealm already matches or beats the competitors on most systems. Its **1.8 combat and eight 1.8 kits** (NoDebuff, Debuff, Gapple, Soup, Archer, Combo, BuildUHC with golden heads, Classic), its **arcade tab** (Bridge, Sumo, Boxing, Spleef, OITC, KOTH) and its **practice bots** cover PvP Land's niche. Neither PvP Club nor PvPHQ was found offering any of these ([README](/home/user/claud/vortex-handoff/README.md); [VoxelRank PL](https://voxelrank.com/server/204-pvp-land)). It already has the modern kits players compare tiers on (Cart, Creeper, Mace, Spear Mace, Crystal, NethPot, Shield, UHC, Pot, Bow, SMP), plus **Tier Defense Challenges, ranked Tier Challenges (first-to-3), placements**, a Coal→Netherite division ladder with promotion series and a demotion shield, repeat-win damping, an alt check, a ping equaliser, ranked seasons with a Hall of Fame, head-to-head records, **friends with spectate, nametags showing tier and overall rank**, a settings hub with request privacy, map vote, regions with transfer and GeoDNS support, replays, post-match analysis, staff /alts, and Grim/Vulcan soft-dependencies ([README](/home/user/claud/vortex-handoff/README.md)). Replays and post-match analysis put it level with PvPHQ, the only competitor known to advertise them. The battle pass, missions, ~300 achievements and cosmetic range (per-piece trims, shields, wings, pets, kill effects, trails, sword skins) go well beyond any store catalogue found. The capsule/elevator start has no documented equivalent. VortexRealm also has unranked queues, which PvPHQ was criticised for lacking ([Discord HQ](https://discord.com/servers/pvphq-1462963503689371805)).

So the remaining gaps are not modes. They are **making ratings public and trusted, being low-ping for more of the world, proving fairness, and monetising without breaking the EULA.**

### Missing pieces and upgrades, ranked

| Priority | Upgrade | What competitors do | Why it matters for VortexRealm |
|---|---|---|---|
| **High** | **Public profile and ladder website plus a read API** | MC and HQ show per-kit tiers, match history (kit, map, opponent, score), rating graphs, H2H rivals, career totals, vanity URLs and region filters ([HQ profile](https://pvphq.com/player/cc8f8e29-2cb7-48d2-93fb-8c52679cd3c7); [BoardMC guide](https://www.boardmc.com/post/mcpvp-guide-kits-tiers-rankings)) | The brief lists only a web *admin* panel; the server plan calls a public site a goal. Profiles are how tiers spread on social media, and a public JSON API lets Tier Tagger-style mods and EloTiers pick up VortexRealm tiers, as they already do for PvPHQ ([HQ addon](https://modrinth.com/project/PzNBY0IN); [EloTiers](https://elotiers.com/guides/minecraft-pvp-tier-lists-compared)) |
| **High** | **Run at least NA + EU nodes for real** | PC 4 regions, HQ 22, MC 38 ([Modrinth PC](https://modrinth.com/server/pvp-club); [Lunar](https://www.lunarclient.com/news/lunar-client-x-pvphq); [BoardMC guide](https://www.boardmc.com/post/mcpvp-guide-kits-tiers-rankings)) | The plugin supports regions, but ping-based matchmaking on one host cannot fix a 150 ms player. Regions are the one moat money buys; one shared MySQL keeps ratings global |
| **High** | **Tuned anti-cheat with visible enforcement**, plus totem anti-ghost and hit-reg tuning | HQ markets totem anti-ghost and hit-reg; MC runs automated anti-cheat duels; MM is known for its in-house anti-cheat ([Lunar](https://www.lunarclient.com/news/lunar-client-x-pvphq); [Sportskeeda](https://www.sportskeeda.com/minecraft/news-dream-drdonut-acquire-mctiers-launch-competitive-mcpvp-platform); [minemen.shop](https://minemen.shop/)) | Grim/Vulcan are only soft dependencies. Ranked tiers are worthless if top ladders hold cheaters. Ship tuned per-kit Grim configs, wire flags into the existing Fair+ and evidence replays, and fix totem desync in Crystal, Cart and NethPot. Knockback complaints hurt PvPHQ at launch ([Discord HQ](https://discord.com/servers/pvphq-1462963503689371805)) |
| **High** | **Remove or decouple paid-rank SMP kits** | Competitors sell only cosmetics and convenience ([VIP](https://store.mcpvp.club/package/6877832); [HQ+](https://store.pvphq.com/package/7548108)) | The README lists SMP `/kit` VIP and MVP/Legend kits. If those ranks are sold, the gear is a paid gameplay advantage that breaks the guidelines ([Usage Guidelines](https://www.minecraft.net/en-us/usage-guidelines)). Make SMP kits playtime- or achievement-based, or identical for everyone |
| **High** | **Accept 26.x clients** (for example ViaVersion on the 1.21.11 backend) | PC listings claim 1.21–26.3; HQ recommends 26.2, and one player failed on 26.3 ([anyserver.pro](https://anyserver.pro/server/224/pvp-club); [BoardMC HQ](https://www.boardmc.com/server/pvphq)) | New players arrive on the newest launcher version. Rejecting 26.x clients loses them at the door. This is inferred from listings; test 26.x handshakes before launch |
| **High** | **Rating-gated tests, peak tier, retest cooldown, premium-only ranked** | PC: 30-day cooldown, peak tier, premium-only; MC: rating unlocks tests ([tiertest](https://mcpvp.club/tiertest); [BoardMC guide](https://www.boardmc.com/post/mcpvp-guide-kits-tiers-rankings)) | Tier Defense already exists. Gating tests on rating and enforcing a cooldown protects tester time (the queue-sniper problem). Showing current *and* peak tier keeps decay from feeling punishing. Verify which of these the plugin already enforces |
| **Medium** | **Consider MT mid tiers (15 steps) and gated HT1/HT2** | MC and HQ both added MT; HQ held back T1 and T2 until ratings settled ([9minecraft](https://www.9minecraft.net/pvphq-tiertagger-addon-mod/); [YouTube](https://www.youtube.com/watch?v=sXbmOuCsPfI)) | Fifteen steps give more frequent promotions. Holding back the top tiers stops the first season's HT1s being placement flukes. Keep LT5–HT1 labels so they stay compatible with MCTiers |
| **Medium** | **Rename and group kits to match community ladders** | MC groups Skill/Vanilla/Community and early/late/end-game; HQ slugs such as `netherite_pot`, `diamond_smp`, `spear_mace` ([BoardMC guide](https://www.boardmc.com/post/mcpvp-guide-kits-tiers-rankings); [MC end-game](https://www.mcpvp.com/tiers/end-game)) | Players compare their VortexRealm tier with their MCPVP and PvPHQ tier. Matching names (and adding a Diamond SMP ladder if it is missing) makes those comparisons easy |
| **Medium** | **Ranked map ban or pick** | HQ ranked map selection; MM 100+ map selector ([Lunar](https://www.lunarclient.com/news/lunar-client-x-pvphq); [Minemen ranks](https://store.minemen.club/category/ranks)) | The map vote exists. A per-player ban in ranked (rather than a vote) is the competitive version. Keep the selector free in ranked so it is not pay-to-win |
| **Medium** | **Party upgrades: Host Battle, public parties, /party announce, size tiers** | PC party caps 8/16/32 and Host Battle; HQ party announce ([VIP+](https://store.mcpvp.club/package/6877860); [HQ+](https://store.pvphq.com/package/7548108)) | Parties are PC's second product. Host Battle (one vs party) is a creator-friendly mode and an easy, EULA-safe paid perk |
| **Medium** | **Store restructure: permanent base + monthly sub + coins for cosmetics** | PC $19.99 + $9.99/mo; HQ $10/$20 per 30 days; MM $7.49–$59.99 ([VIP](https://store.mcpvp.club/package/6877832); [HQ ranks](https://store.pvphq.com/category/ranks); [Minemen ranks](https://store.minemen.club/category/ranks)) | Turn existing cosmetics into packages: kit slots, party size, hosting rights, name and tag customisers, trims and shields. Coins allow gifting. Keep the battle pass premium track cosmetic-only (a grey area) and avoid crates |
| **Medium** | **Player-hosted tournaments with a cooldown** | HQ+ every 20 min; MM ACE force-start ([HQ+](https://store.pvphq.com/package/7548108); [Minemen ranks](https://store.minemen.club/category/ranks)) | Tournaments and the Weekly Cup exist. Letting supporters host them with a cooldown adds activity at no staff cost |
| **Medium** | **Prize events with qualifiers and a Liquipedia page** | HQ $10k championship; PC $15k+ claim ([Liquipedia](https://liquipedia.net/lab/Minecraft/PvPHQ/PVP_Championship); [mclist.io](https://mclist.io/server/60213)) | One small-prize season final with open qualifiers gets press coverage the Weekly Cup alone does not |
| **Medium** | **Creator and clip funnel** (Medal quest-style) | HQ gives HQ+ for linking Medal and clipping ([Medal quest](https://medal.tv/quests/8HWT-MakzW/pvphq_x_medal)) | Creator codes and LIVE badges exist. Paying for clips with a rank is cheap marketing |
| **Low** | **Extra customisers**: shulker colour, item rename, display name | PC VIP/VIP+ ([VIP](https://store.mcpvp.club/package/6877832)) | Cheap to add next to the existing trim and shield editors |
| **Low** | **Lobby movement toys** (elytra, wind charges, spear) | PC VIP, HQ+ ([VIP](https://store.mcpvp.club/package/6877832); [HQ+](https://store.pvphq.com/package/7548108)) | Fun, EULA-safe perk; keep them out of fights |
| **Low** | **/disguise in unranked, sidebar customisation, verified badge** | HQ+, MM MVP, HQ Medal ([HQ+](https://store.pvphq.com/package/7548108); [Minemen ranks](https://store.minemen.club/category/ranks)) | Nice to have; streamer mode partly covers disguise already |
| **Low** | **Lunar Client integration** | HQ queues from Lunar, gets exclusive cosmetics and anti-cheat help ([Lunar](https://www.lunarclient.com/news/lunar-client-x-pvphq)) | Requires a partnership; not something a plugin can build alone. Revisit once player counts justify it |
| **Low** | **Overall title ladder** (Rookie→Grandmaster) | MC ([BoardMC MC](https://www.boardmc.com/server/mcpvp)) | The titles and division ladder mostly cover it already |

Two cautions apply to cosmetics VortexRealm already sells or plans to sell. **Wings** sit on the player's back, and the guidelines ban capes and anything that looks like one ([Usage Guidelines](https://www.minecraft.net/en-us/usage-guidelines)). Wings are not capes, but a cautious owner would keep cape-shaped items free or reward-only. **Queue priority** is sold by every competitor, but it is an access advantage, so the server plan's "allowed by most" stance should be rechecked against the current guidelines before launch. Finally, warn players about look-alike store domains. The mcpvp-club.com case shows copycat stores appear around popular servers ([mcpvp-club.com](https://mcpvp-club.com/)).

## Conclusion

The 2026 practice market is being decided by **who owns the scoreboard, not who has the most modes**. Dream's MCPVP.com bought the ladder everyone already cited. PvPHQ got Lunar to put its queue inside the client. Both turned the tier into a public, shareable, rating-backed identity. VortexRealm's rating system is arguably already richer than either: it has Tier Defense, Tier Challenges, placements, damping and alt checks. But a strong ranked system that only shows in game counts for little next to one that is public and readable by players' mods. The best next investment is therefore not another mode. It is a public profile and ladder site with an API, two real regions and a tuned anti-cheat. Together these let VortexRealm's 1.8, bot and arcade breadth, which neither main rival offers, become a reason to stay instead of a feature list.

Two risks deserve attention before any marketing push. The paid SMP kits are a clear EULA exposure in an otherwise cosmetic store. And competitors are still changing fast: beta resets at MCPVP.com, recalibration at PvPHQ, and unconfirmed merger ties between mcpvp.club and mcpvp.com. Re-check their live pages and stores, ideally by joining the servers, before fixing prices or tier thresholds. Everything here was read from search snippets, not the sites themselves.
