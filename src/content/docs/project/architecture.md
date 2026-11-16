---
title: Architecture
description: How the pieces of Tux-Force fit together, from sign-in to a running game.
---

## Overview

```text
 xtux-cli ─┐                                  ┌─> Microsoft: sign-in, licenses, Xbox Live, packages
           ├─ unix socket (XTX2) ─> xtux-service ─┤
 xtux-launcher ─┘                                  └─> Wine + game ─ xgameruntime.dll
                                       ▲                                  │
                                       └──── game bridge (loopback) ◄─────┘
```

- **xtux-service** is the one background service. It holds the account and device tokens, talks to Microsoft,
  downloads games, sets up prefixes, starts Wine with the game and hosts the game bridge.
- **xtux-cli** and **xtux-launcher** use the service for shared game operations and progress. The launcher also
  reads local settings and artwork. Lower-level CLI research commands still use the core libraries directly.
  Shared game operations use the same `xtux-games` implementation.
- **xgameruntime** inside the Tux-Force Wine build implements the GDK runtime the game loads, and asks the service
  through the game bridge for what only Microsoft can answer.

## The service

`xtux-service` listens on `$XDG_RUNTIME_DIR/xtux.sock`. A client starts it when the socket is missing (from the
same folder as the client, or `XTUX_SERVICE`), and it exits after five idle minutes while no game or download runs
(`XTUX_IDLE_TIMEOUT`). It also starts while nobody is signed in and reports that state instead of failing. Its log
is `~/.local/state/xtux/service.log`.

The logic lives in the library crate `xtux-games` (library scan, layouts, install, prefix setup, launch, bridge),
which the service uses. `XTUX_DIRECT=1` runs a CLI command with the same library in-process, without the service,
for debugging.

## Protocol v2

Clients and service talk in frames: the magic `XTX2` once per connection, then frames of a 32-bit length (up to
16 MiB) and a JSON body. Every request has an id; the service answers with a response for that id and can send
events in between:

| Requests | Events | Responses |
|---|---|---|
| `Ping`, `Status`, `Library`, `SignIn`, `PrefixInit`, `Install`, `Launch`, `Catalog`, `Downloads`, `Uninstall`, `Cancel` | `Message`, `Bytes`, `File`, `FileFinished`, `GameStarted` | `Pong`, `Status`, `Library`, `PrefixReady`, `Installed`, `GameExited`, `Catalog`, `Downloads`, `Uninstalled`, `Cancelled`, errors with a kind |

`Cancel` stops a running request by its id (for example a download on Ctrl+C). The older XML messages of the
runtime are still answered on the same socket.

Sign-in uses Microsoft's web page, so the service starts a small helper (`xtux-cli login`) that shows it in its own
window; that keeps web view and launcher UI apart.

## Catalog, downloads and settings

`xtux-games::catalog` fetches PC Game Pass and owned-title metadata. Catalog responses are cached per account
and market for a day; clients can request a refresh. Catalog presence does not replace a launch-time license check.

The service owns a persistent download queue (`$XDG_STATE_HOME/xtux/downloads.json`), processes one install at a time
and continues without a connected client. Clients use `Downloads` commands to add, pause, resume, reorder, remove
or clear completed jobs. Queue status includes recent network and disk-rate samples.

Clients share `$XDG_CONFIG_HOME/xtux/settings.toml`, including appearance settings and per-game overrides keyed by
canonical game folder. The launcher uses `xtux-games` directly for local settings and artwork; service requests
handle the game, account and download operations. Per-game logs are in `$XDG_STATE_HOME/xtux/logs/`.

The `Uninstall` request removes the checked game folder inside a configured library. This includes Windows installs
when explicitly confirmed in the launcher; it is a disk deletion, not a library-only unlink.

## Starting a game

1. The service reads the game folder: `Content/` plus the package header named by the content id (the layout of the
   Windows Xbox app), or the older Xodus layout. See [Running games](/guide/running-games/#one-install-format).
2. It fetches the game's license for the signed-in account. Without an entitlement the game does not start.
3. It starts Wine with the game, the DLL overrides recorded by `prefix init`, and the address and a per-run secret of
   the game bridge.
4. It reports `GameStarted` with the process id and `GameExited` with the exit code to the client.

## The game bridge

GDK games ask the runtime for things only Microsoft can answer: store license tokens, Xbox Live tokens bound to the
title and signed like on Windows, user identity. `xgameruntime` sends these requests to a loopback service on
`127.0.0.1` that only accepts the per-run secret. The service answers each request with that one result, so account
tokens never enter the game process.

For Xbox Live, the service gets title-bound tokens (device, title and user token, as on Windows) and picks the
relying party for each service from the title's own endpoint table.

## Repositories

| Repository | Contents | Upstream |
|---|---|---|
| [xTux](https://github.com/Tux-Force/xTux) | `xodus` (core: auth, APIs, tokens), `msixvc` (packages), `xtux-games`, `xtux-protocol`, `xtux-service`, `xtux-cli`, `xtux-launcher` | [xodus-gaming/xodus](https://github.com/xodus-gaming/xodus) |
| [xgameruntime](https://github.com/Tux-Force/xgameruntime) | `xgameruntime.dll`: task queues, async, users, store, saves, networking, package identity | [xodus-gaming/xgameruntime](https://github.com/xodus-gaming/xgameruntime) |
| [wine](https://github.com/Tux-Force/wine) | Wine with xgameruntime as a submodule and WinHTTP fixes for GDK games | [xodus-gaming/wine](https://github.com/xodus-gaming/wine) |
| [tux-force.github.io](https://github.com/Tux-Force/tux-force.github.io) | This website: guide, compatibility list, project documents, brand | |

Upstream changes are pulled in when useful; nothing is pushed upstream.
