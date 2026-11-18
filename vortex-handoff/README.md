# VortexRealm handoff files

- `VortexRealm-3.11.0.jar` — the newest plugin: put it in `plugins/` (replace the old VortexRealm jar) and restart.
- `court-arenas.png` — the 8 new arenas, seen from the fighting floor.
- `HANDOFF.md` — everything the next AI agent needs.
- `vortexrealm-3.11.0.bundle` — the commits (handoff, 3.10.0, 3.11.0) that could not be pushed to
  `Rayanboonty/3Dmodel` (no push access in that session). With push access, from a clone of that repo:

```bash
git fetch origin claude/vortex-realm-pvp-plugin-2x1tq1
git checkout claude/vortex-realm-pvp-plugin-2x1tq1
git pull /path/to/vortexrealm-3.11.0.bundle HEAD
git push origin claude/vortex-realm-pvp-plugin-2x1tq1
```

Once pushed, servers pick up 3.10.0 by themselves (auto-update reads `dist/update.json` on that branch).
