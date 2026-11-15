---
title: Roadmap
description: Where Tux-Force is and what comes next.
---

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
- [ ] Launcher milestone 1: sign-in, local library, play and settings work; per-game settings, log view and Flatpak are next
- [ ] Library of owned and Game Pass games
- [x] Reuse Windows installs in place, one install format for all
- [ ] Install, update, verify, uninstall from the launcher
- [ ] One-click play with per-game settings

## Phase 4: Ecosystem

- [ ] Store view: catalog and subscription contents
- [ ] Compatibility reports per game (GitHub-based)
- [ ] Cloud saves, achievements, friends
- [ ] Packages for common distributions (Flatpak first)
