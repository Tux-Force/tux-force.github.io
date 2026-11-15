---
title: Launcher plan
description: "The plan for the xTux Launcher: goals, architecture, milestones and decisions."
---

Status: decided on 2026-11-14 (see [Decisions](#decisions-2026-11-14)). Milestone 0 is done, milestone 1 is in
progress.

:::note
This plan was written before milestone 0. Some details changed while building it: the service protocol v2 uses
length-prefixed JSON frames (`XTX2`) instead of protobuf, the crates are called `xtux-games`, `xtux-service` and
`xtux-cli`, and Windows installs are read in place instead of linked. [Architecture](/project/architecture/)
describes the current state.
:::

The launcher is Roadmap Phase 3: a graphical app that takes a user from "I have Game Pass or own a game" to
"I am playing" without a terminal. It sits on top of xTux (`xodus-src/xodus`) and the Tux-Force Wine tree.

## Goals of v1

1. **Sign-in** with a Microsoft account, show who is signed in, sign out.
2. **Library**: games installed locally (streamed by xTux or linked from a Windows Xbox app install), games the
   account owns, and Game Pass games the subscription includes. Filter and search.
3. **Install, update, verify, uninstall** with a visible download queue (progress, pause/cancel, resume after restart).
4. **Reuse Windows installs** (dual boot): detect `XboxGames/*` folders on mounted Windows partitions and run them in
   place, never copy and never delete Windows files. xTux uses the same install layout as the Windows Xbox app
   (`Content/` plus the package header named by its content id) for its own downloads too, so there is one format;
   `xtux-cli migrate` moves older Xodus installs into it.
5. **One-click play** with per-game settings (Wine build, prefix, DXVK/vkd3d-proton, env vars, arguments, exe).
6. **Prefix setup** through `xodus-cli prefix init` logic (DXVK/vkd3d-proton, Microsoft TLS roots, DLL overrides),
   run automatically before the first launch.
7. **Flatpak** as the first and only official package of v1.

## Non-goals of v1

- Store view (browse and buy), prices, wishlists. Game Pass titles appear in the library, there is no shop.
- Cloud saves, achievements, friends overlay (Phase 4).
- Compatibility reports beyond a "Report / view reports" link to the GitHub-based tracker.
- Gamepad-first "big picture" UI. The UI should work at Steam Deck resolution, but a dedicated controller mode waits.
- Running Windows Xbox app (MSIX/UWP-only) titles that xTux cannot run today.
- Multiple accounts at the same time.
- Distribution packages other than Flatpak (deb/rpm/AUR can follow the Wachposten scripts later).

## What xTux offers today, and the gaps

| Need | Exists | Where | Gap |
|---|---|---|---|
| Device identity | yes | `xodus::tokens::device::ensure_device_credentials` | none |
| Token storage | yes | `TokenManager` (Secret Service keychain + memory) | none |
| User sign-in | CLI only | `xodus-cli/src/commands/login.rs`, tao + wry webview | flow lives in the CLI crate; tao event loop clashes with Slint's winit loop in one process |
| User identity (xuid, gamertag) | yes | service `UserInfoRequest` | none |
| Product details | single product | `xodus::api::displaycatalog::find_products_by_id` | no batch lookup (`/v7.0/products?bigIds=...`), images/sizes/description not modelled in `models/displaycatalog.rs` |
| Product id to content id | CLI only | `xodus-cli/src/package.rs::get_content_id` | interactive (`inquire`) sub-product picker; must become a library function returning choices |
| Package files and version | CLI only | `package.rs::get_packages` (packagespc `GetBasePackage`) | `unwrap()`s, no error types; needed for install and update check |
| **Owned games list** | **no** | | needs an entitlement query (collections.mp.microsoft.com `collections/query`, or titlehub title history as a fallback) |
| **Game Pass catalog** | **no** | `models/xbox/subscriptions.rs` has the product ids (`GAMEPASS_SUBS`), unused | needs the public Game Pass lists (catalog.gamepass.com `sigls`) plus a check which subscription the user has (collections query for the `CFQ7TTC0*` ids) |
| Install (streaming) | CLI only | `commands/streaming.rs` + `msixvc` crate | progress is `indicatif`, no cancel/resume API, no events |
| Verify | partly | `msixvc` hash tree, `PackageFile::file_hash`, `hash_of_hashes` | no "verify installed game" function |
| Update check | no | `PackageDetails::version_id` | compare against a stored install manifest; delta downloads later |
| Windows installs | done | `xtux-games::layout` (read in place, unified layout), `settings::detect_windows_libraries` | whether the Windows Xbox app accepts installs made on Linux is untested |
| Run | CLI only | `commands/run.rs` (license, mem-fd mapping, env, Wine spawn) + `bridge.rs` | logic is in the CLI; the bridge lives as long as the `run` process |
| Prefix setup | planned | `xodus-cli prefix init` | design the library function first, CLI and launcher call it |
| Service protocol | minimal | `xodus-service`: ping, MSA token, token+signature, user info (XML) | protobuf path is `unimplemented!`; frame size is `u16` (64 KiB max), too small for library lists; no server-to-client events (progress); service panics without a device token and has no "signed out" start |

The main structural gap: almost everything a launcher needs is implemented, but inside `xodus-cli`, with
terminal UI calls mixed in. Milestone 0 fixes that.

## Architecture

**Recommendation: the launcher is a client of `xodus-service`; it does not link the `xodus` library for account,
license or game operations.**

```
 tux-force-launcher (Slint UI)  --unix socket, protobuf-->  xodus-service  --> Microsoft services
        |  spawns/monitors                                  |  holds tokens, sessions, downloads
        v                                                   |  spawns Wine + game, hosts bridge
   (nothing secret)                     game + xgameruntime --+  (same socket, Phase 2)
```

Reasons:

- **One token holder.** Tokens stay in one process, as the Vision promises. The launcher never sees an XSTS token.
- **Games outlive the UI.** Today the bridge dies with `xodus-cli run`. If the service spawns the game and hosts the
  bridge, closing the launcher does not break a running game, and downloads can continue in the background.
- **Roadmap fit.** Phase 2 already moves the runtime bridge onto the service socket; the launcher reuses the same
  channel instead of creating a second integration path.
- **Other clients for free.** CLI, a later controller UI, or a Steam shortcut (`tux-force run <id>`) use the same API.
- **Crash isolation.** A UI bug does not lose a 100 GB download or a license session.

Cost: the protocol must be designed first (Milestone 0). Linking the library directly would be faster for the
first demo, but would duplicate the token holder and the game lifetime problem, and need rework in Phase 2.

What the launcher links directly: only a small `xodus-client` crate (typed requests, generated protobuf types,
reconnect logic) and pure local code (settings files, artwork cache). It may read `msixvc` metadata locally for
display, never for licensing.

### Changes in xTux (Milestone 0)

1. New library crate (working name `xodus-games`) with the logic now in `xodus-cli`: content id lookup (choices
   returned, not prompted), package lookup, streaming install with progress callbacks and cancellation, link,
   run (spawn + bridge), prefix init, verify. Error types instead of `unwrap()`/`eprintln!`.
   `xodus-cli` becomes a thin terminal front end over it, so CLI and launcher behave the same.
2. Service protocol v2 on the protobuf magic: `u32` length, request ids, and server-pushed events
   (`DownloadProgress`, `GameStarted`, `GameExited`, `SignInStateChanged`). XML stays for the existing runtime messages.
3. Service starts without a user (signed-out state) and reports it instead of panicking.
4. Service lifecycle: the launcher starts the service if the socket is missing; the service can keep running while
   downloads or games are active, then exits after an idle timeout.
5. Sign-in: keep the wry webview, but in a separate small process (`xodus-cli login` or a `xodus-login` helper)
   started on the service's request. This avoids two GUI event loops in one process and keeps the MSA flow
   identical to the CLI.

### UI toolkit

**Recommendation: Rust + Slint** (same stack as Wachposten and OpenRAGE: Slint 1.18, winit backend, femtovg and
software renderer, `build.rs` + `ui/*.slint`, translations folder).

| Option | For | Against |
|---|---|---|
| **Slint** | Same language and patterns as the core and the user's other apps; small binary; software renderer fallback; good for a fixed, styled game-library look; works on Steam Deck | Grid/image-heavy views need care (lazy image loading); no web view, so sign-in stays a helper process |
| Tauri / web UI | Store-like layouts and artwork grids are easy; webview already needed for sign-in | Second language/toolchain (TS), WebKitGTK quirks on Linux, larger attack surface for a token-adjacent app |
| GTK4 / libadwaita | Native GNOME look, Flatpak GNOME runtime fits | Looks foreign on KDE/Deck, gtk-rs is verbose, less suited to a game-library design |

## Screens and flows (v1)

1. **First run**: welcome, then sign-in (helper window), choose a library folder (default
   `~/Games/Tux-Force`), scan for Windows Xbox app installs on mounted partitions and offer to link them.
2. **Library** (main window): grid of cover art with badges (Installed, Update, Game Pass, Owned, Linked from
   Windows). Filters: All / Installed / Owned / Game Pass; search box. Sidebar or header shows the account
   (gamertag, subscription name) and the download queue indicator.
3. **Game page**: hero art, title, publisher, install size, state. Primary button changes with state:
   Install, Resume, Update, Play, Running (Stop). Secondary: Verify, Uninstall (or Remove from library for Windows installs),
   Open folder, Settings, Report compatibility (opens GitHub). Short compat note if one exists.
4. **Install flow**: pick target folder (default library folder), show size and free space, start; the job
   joins the **Downloads** view (queue, speed, ETA, pause, cancel). Resumes after a restart.
5. **Play flow**: Play -> prefix check (create or upgrade via prefix init, with a progress dialog on first run)
   -> license check -> launch. Errors are shown in plain language with a "Show log" button.
6. **Per-game settings** (tab on the game page): see below. A "Reset to defaults" button.
7. **Settings**: Account (sign out, remove device), Storage (library folders, Windows partitions to scan),
   Compatibility defaults (Wine build, DXVK/vkd3d-proton versions, default env), Advanced (market, log level,
   open logs folder), About (versions of launcher, xTux, Wine, runtime).

## Per-game settings and prefixes

Stored per game as TOML in the launcher's config dir (Flatpak: `~/.var/app/<app-id>/config/tux-force/games/<product-id>.toml`),
keyed by product id, with a global `defaults.toml` that games inherit from. Settings:

- Wine build (bundled Tux-Force Wine by default; custom path allowed), executable override (`run --exe`), launch
  arguments, extra environment variables, market.
- DXVK / vkd3d-proton on/off and version, software video decoders (today's `GST_PLUGIN_FEATURE_RANK` default),
  fsync/ntsync toggles where the Wine build supports them.
- Optional wrappers: gamescope, MangoHud, GameMode (only shown when available, Flatpak extensions).

Prefix handling:

- **One prefix per game** by default (`<data>/prefixes/<product-id>`), so a broken game cannot break others and
  uninstall can remove the prefix. A shared prefix is an advanced option.
- The launcher never touches prefix internals; it calls prefix init through the service (same code as
  `xodus-cli prefix init`). Prefix init writes a stamp (prefix-init version, Wine version, DXVK/vkd3d versions);
  the launcher re-runs it when the stamp differs from the current settings.
- Save games live in the prefix today; uninstall asks whether to keep the prefix (default: keep).

## Data sources

| Data | Source | Cached |
|---|---|---|
| Account, gamertag, xuid | service `UserInfo` | in memory |
| Subscription | collections query for `GAMEPASS_SUBS` product ids (new) | per session |
| Owned games | collections/entitlements query (new) | 24 h, refresh button |
| Game Pass list | public catalog.gamepass.com lists for PC (new) | 24 h |
| Titles, art, sizes | displaycatalog batch lookup (new), images from `LocalizedProperties` | disk cache with ETag |
| Install state | install manifest per game written by the install code (new): product id, content id, version id, path, source (streamed / linked) | local |
| Update available | packagespc `GetBasePackage` version id vs manifest | on start and on demand |
| Runtime state | service events (`GameStarted`/`GameExited`, download progress) | live |

Endpoint details (exact API versions, required auth, whether PC-only games can be filtered server side) must be
verified in Milestone 2/3 before relying on them.

## Packaging (Flatpak first)

- App id e.g. `io.github.TuxForce.Launcher` (avoid Microsoft/Xbox trademarks in the id and name).
- Runtime: `org.freedesktop.Platform` (plus WebKitGTK built in the manifest for the sign-in helper), or the GNOME
  runtime if it ships the WebKitGTK ABI wry needs; check this in Milestone 1.
- One Flatpak contains launcher, `xodus-service`, the sign-in helper and the Tux-Force Wine build with
  xgameruntime. GDK games are 64-bit, so check whether a pure WoW64 Wine avoids the i386 compat extension.
- Permissions: Secret Service (`--talk-name=org.freedesktop.secrets`), network, GPU (`--device=dri`), audio,
  X11/Wayland, game folders (library folder via portal or `--filesystem=~/Games`), Windows partitions
  (`/run/media`, `/mnt`; read-only may be enough for linked installs, to verify).
- Service socket under `$XDG_RUNTIME_DIR/app/<app-id>/` inside the sandbox.
- Optional extensions: MangoHud and gamescope (Flatpak VulkanLayer / Utility extensions).
- Built in CI on GitHub Actions, published first as a Flatpak bundle and a Tux-Force Flatpak repo; Flathub later.

## Milestones

Each milestone ends with a release that someone can use.

| # | Scope | Shippable result |
|---|---|---|
| M0 | xTux: move CLI logic into `xodus-games`, service protocol v2 (protobuf, `u32` frames, events), signed-out start, sign-in helper | xTux release; CLI behaves as before, now on the library |
| M1 | Launcher skeleton: sign-in/out, local library (xTux installs + Windows installs read in place, with the drive scan), Play via the service, basic per-game settings (Wine, exe, args, env), logs view; Flatpak build in CI | "Local launcher" for games already installed; first Flatpak |
| M2 | Owned games (entitlement query), artwork and displaycatalog batch lookup, install via streaming with queue, progress, pause/resume | Install owned games from the GUI |
| M3 | Game Pass: subscription detection, Game Pass list in the library, update check, verify, uninstall/unlink | Feature-complete library for Phase 3 |
| M4 | Prefix init integration (auto on first play, stamps, upgrade), DXVK/vkd3d settings, gamescope/MangoHud/GameMode, compat report link, translations (en, de) | v1.0 |

## Decisions (2026-11-14)

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
