---
title: Vision
description: What Tux-Force is, what makes it different, principles and non-goals.
---

**Every PC game you legitimately own or subscribe to should run on Linux as a first-class experience.**

Microsoft Store and Game Pass games for PC are built on the GDK and packaged in encrypted MSIXVC containers. They
need Xbox services that Wine does not provide, and there is no official way to run them on Linux. Tux-Force closes
that gap without cracks: you sign in with your account, Microsoft issues the licenses, and the games talk to the
real Xbox Live, PlayFab and store services.

## What makes Tux-Force different

### 1. A complete ecosystem

Tools exist for single pieces. Tux-Force wants the whole path from "I have Game Pass" to "I am playing":

| Layer | Piece | State |
|---|---|---|
| Account and licenses | xTux: device and user sign-in, license retrieval, store license tokens | works |
| Content | xTux: downloads, streaming, reuse of Windows Xbox app installs (dual boot) | works |
| Game services | xgameruntime: task queues, users, saves, store, networking; xTux bridge for tokens | works for tested games |
| Compatibility | Wine tree with the runtime and fixes; DXVK/vkd3d-proton and certificate setup with `xtux-cli prefix init` | works |
| Launcher | xTux Launcher: local library, play, per-game settings, logs, Store catalog and queued installs | implemented; updates and verify planned |
| Store view | Browse PC Game Pass and owned titles, inspect supported packages and queue installs | implemented; title entitlement checked at launch |
| Community | Compatibility reports per game (GitHub-based, no own server needed at first); [list](/compatibility/) started | started |
| Extras | Cloud saves, achievements and friends overlay | planned |

### 2. Built with AI, AI welcome

Tux-Force is developed with AI, and AI-assisted contributions are welcome. Many open source projects ban AI-written
code; we decided differently, because AI tools let a small community build and maintain a whole ecosystem. What counts
is a tested, reviewed result (see [Contributing](/project/contributing/)).

> **Our opinion:** used well, today's coding assistants are better than the average programmer, provided you know
> how to work with them.

### 3. Independent, on solid foundations

The core repositories are forks of the xodus-gaming projects and Wine. We pull in new upstream code when it is
useful and credit it everywhere, but Tux-Force sets its own direction and pace.

## Principles

- **Legal:** no license bypass, no DRM circumvention, only games your account is entitled to.
- **Private:** account tokens stay on your machine and only go to Microsoft; games get per-request results.
- **Honest:** we document what works and what does not, per game.
- **Open:** GPL-3.0 and LGPL-2.1 like the projects we build on.

## Non-goals

- Running games you do not own or subscribe to.
- Replacing Microsoft services with our own servers.
- Using Microsoft trademarks for the project.
