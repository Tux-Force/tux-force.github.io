---
title: Roadmap
description: Where Tux-Force is and what comes next.
---

Source status checked on 2026-11-16. Implemented means present in the current source, not a guarantee for every game.

Where we are and what comes next. The detailed plan for the launcher is in the [launcher plan](/project/launcher-plan/).

## Phase 1: Foundation

- [x] Soft forks: xTux (Xodus), xgameruntime, wine
- [x] First fully playable game: Farming Simulator 25
- [x] Store license tokens and title-bound, signed Xbox Live tokens
- [x] Prefix setup: DXVK/vkd3d-proton, Microsoft TLS roots, DLL overrides (`xtux-cli prefix init`)
- [ ] Microsoft Flight Simulator 2024 past its backend checks

## Phase 2: Runtime

- [ ] Move xgameruntime to the C++ code base (upstream `main`), module by module
- [ ] Bridge on the xtux-service socket protocol
- [ ] Tests for every runtime module
- [ ] Regularly pull useful upstream changes into `develop`

## Phase 3: Launcher (now)

- [x] Background service with thin clients (CLI and launcher), protocol v2
- [x] Sign-in, local library, Play/Stop, per-game settings and logs
- [ ] Flatpak build and packaging
- [x] Store catalog of owned and PC Game Pass games with search, filters and artwork
- [x] Reuse Windows installs in place, one install format for all
- [x] Store installs with a persistent queue, progress, pause/resume and reordering
- [x] Delete installed games from the launcher after confirmation
- [ ] Update checks and verification of installed games
- [x] One-click play with per-game Wine, prefix, executable, arguments and environment
- [ ] Automatic prefix setup on first launch

## Phase 4: Ecosystem

- [x] Store view: PC Game Pass catalog and owned titles
- [ ] Compatibility reports per game (GitHub-based)
- [ ] Cloud saves, achievements, friends
- [ ] Packages for common distributions (Flatpak first)
