---
title: Launcher plan
description: Implemented launcher features, remaining work and original design decisions.
---

Source status checked on **2026-11-16** against `xtux-launcher`, `xtux-games`, `xtux-protocol` and `xtux-service`.
This page distinguishes implemented features from design targets. It does not certify individual games or claim
that unreleased source changes are already in a downloadable binary.

## Current implementation

| Area | Implemented | Remaining |
| --- | --- | --- |
| Service and clients | Slint launcher, CLI, shared `xtux-games` logic and `xtux-protocol`; on-demand service with idle timeout | Further runtime bridge integration |
| Protocol | `XTX2` magic, 32-bit length-prefixed JSON frames, request IDs, responses and progress events; legacy runtime XML still supported | No protobuf client protocol is used |
| Account | Sign-in through a separate `xtux-cli login` helper and account status in the launcher | Richer account and subscription management |
| Local library | Grid/list, search, refresh, Windows installs in place, Play/Stop, license and anti-cheat indicators | Community compatibility reports |
| Game page | Artwork, per-game Wine/prefix/exe/args/env, last launch log, confirmed deletion | Installed-game update checks and verify |
| Store | PC Game Pass and owned-title catalog, filters, details, artwork and screenshot gallery | Purchasing, pricing and wishlists are outside the current scope |
| Installs | Store install flow, library selection, persistent service queue, pause/resume, ordering, progress and activity graphs | Broader package support and update management |
| Settings | Shared TOML settings, themes, accents, background, icons, online artwork toggle | More compatibility wrappers and translations |
| Prefixes | Shared prefix by default, per-game override, CLI `prefix init` | Automatic setup/upgrade before first play |
| Packaging | Release binaries | Flatpak bundle and CI packaging |

A Store entry or Game Pass badge does not confirm the current account's entitlement. Microsoft checks the license
at launch. Optional Store anti-cheat estimates use title names and are unverified; installed games are checked by files.

## Architecture

```text
xtux-cli / xtux-launcher
           │ XTX2: length-prefixed JSON
           ▼
      xtux-service ── Microsoft services
           │
      xtux-games ── Wine + game ── xgameruntime
           ▲                         │
           └── loopback game bridge ──┘
```

The service holds tokens, owns downloads and game launches, and hosts the loopback bridge. Local settings and
artwork helpers can be used directly by the launcher. See [Architecture](/project/architecture/) for protocol details.

## Settings, prefixes and storage

- Global and per-game settings: `$XDG_CONFIG_HOME/xtux/settings.toml`; game overrides are keyed by game folder.
- Default install folder: `$XDG_DATA_HOME/xtux/games`. Windows libraries on mounted drives can be detected or added.
- One shared prefix by default (`WINEPREFIX` or `~/Games/xtux-prefix`); each game may select another initialized prefix.
- Queue: `$XDG_STATE_HOME/xtux/downloads.json`; service log and per-game logs share the same state directory.
- Artwork: `$XDG_CACHE_HOME/xtux/art`; catalog caches are account- and market-specific.

Windows games are reused without a copy. **Delete game…** removes the entire game folder after confirmation,
including a Windows installation and saves inside that folder. It is not merely an unlink operation.

## Packaging (Flatpak first)

Flatpak remains the planned first integrated package, with app ID `io.github.TuxForce.xTux` from the original design.
A bundled Wine/runtime build, permissions, sign-in helper and CI packaging still need implementation and validation.
For the available separate binaries, see [Downloads](/downloads/) and [Installation](/guide/installation/).

## Milestones

The original milestone groups overlap with features already implemented. They are not release announcements.

| Milestone | Current status | Remaining work |
| --- | --- | --- |
| M0: shared logic and service | Implemented with `xtux-games`, `xtux-protocol` and JSON protocol v2 | Continue runtime integration |
| M1: local launcher | Library, sign-in, Play/Stop, settings and logs implemented | Flatpak packaging |
| M2: catalog and installs | Owned-title catalog, artwork and queued installs implemented | Broader real-world package validation |
| M3: Game Pass and management | PC catalog, filters and confirmed game deletion implemented | Update checks and verify |
| M4: v1 polish | Prefix init available through CLI; per-game prefix selection implemented | Automatic prefix setup, compatibility wrappers, reports and translations |

See [Launcher](/guide/launcher/) for usage and [Roadmap](/project/roadmap/) for the remaining project work.

## Decisions (2026-11-14)

Historical design decisions, retained for context. Statements below about bundling, updates, compatibility statuses
and centralized saves are targets, not claims that these features are implemented. The implementation status above
takes precedence. The launcher now lives in the `Tux-Force/xTux` repository.

1. **Name:** product name **xTux Launcher**, Flatpak app id `io.github.TuxForce.xTux`. Repository name still to
   pick (proposal: `Tux-Force/xtux-launcher`).
2. **Naming:** the daemon becomes **xTux-service** (command and crate `xtux-service`), the CLI **xTux-cli** (command
   and crate `xtux-cli`); the renaming is part of M0.
3. **One daemon, thin clients:** xTux-service is the single daemon. CLI and GUI are both thin clients on its
   socket; the game bridge moves into the daemon too. No business logic is duplicated.
4. **Daemon lifecycle:** started on demand by CLI or GUI, exits after an idle timeout while no game or download runs.
5. **Library split:** the logic in `xodus-cli` moves into a library crate used by the daemon (M0), accepting harder
   upstream merges in the CLI.
6. **Wine:** one tested Tux-Force Wine build from CI is bundled; no version manager in v1.
7. **Prefixes:** one shared prefix by default; a game can opt into its own prefix.
8. **Game Pass:** v1 shows the full PC Game Pass catalog the user's subscription includes, with install.
9. **Compatibility:** every game is shown with a status (works, issues, does not work, untested); nothing is hidden.
10. **Windows installs:** the launcher may also update Windows installs (writes to the Windows partition).
   It refuses when the NTFS volume is mounted read-only or left hibernated by Windows Fast Startup (writing then
   risks data loss), and verifies the package after updating.
11. **Market and language:** from the system locale, changeable in settings.
12. **Steam Deck:** not required for v1; gamepad UI and Deck polish come later.
13. **License:** GPL-3.0-or-later.
14. **Save games:** stored centrally in `~/.local/share/xtux/saves/<game>`, outside prefixes, and mapped into each
    prefix; this is also the base for cloud saves later.
