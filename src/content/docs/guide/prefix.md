---
title: Wine prefix
description: Prepare a Wine prefix for GDK games with DXVK, vkd3d-proton and the Microsoft root certificates.
---

GDK games need a few things in their Wine prefix that a fresh prefix does not have. `xtux-cli prefix init` sets them
up in one go and can be run again at any time to update them.

```bash
xtux-cli prefix init ~/wine-tux-force-x86_64/bin/wine --prefix ~/Games/xtux-prefix
```

It does this:

1. Creates the prefix with `wineboot` if it does not exist yet.
2. Downloads **DXVK** (Direct3D 8 to 11) and **vkd3d-proton** (Direct3D 12) from their GitHub releases and installs
   them into the prefix. Wine's own DLLs are kept in `xtux-builtin-backup/` inside the prefix.
3. Adds the **Microsoft TLS root certificates** that games and Xbox services expect to the prefix's certificate store.
4. Records the setup in `xtux-prefix.json` in the prefix. `xtux-cli run` and the launcher read the DLL overrides from
   there, so you do not need to set `WINEDLLOVERRIDES` yourself.

Some things are set up automatically when a game starts, not by `prefix init`:

- **GameInput:** if a game ships the GameInput redistributable (`Installers/GameInputRedist.msi` in its folder, as
  Minecraft for Windows does), xTux installs it into the prefix.
- **Controller mode:** the [controller setting](/guide/running-games/#controllers) is written into the prefix. A
  change applies once all games of that prefix are closed.

## Options

| Option | Effect |
|---|---|
| `--prefix <path>` | Prefix to set up. Without it: `WINEPREFIX`, else `~/Games/xtux-prefix` |
| `--from-proton <dir>` | Take DXVK and vkd3d-proton from a local Proton build instead of downloading them |
| `--skip-graphics` | Leave Wine's own Direct3D DLLs in place (for testing) |

## One prefix or one per game

By default all games share one prefix. That saves space and time, and works for the tested games. A game can use its
own prefix: set `WINEPREFIX` when you start it, or choose it in the launcher's per-game settings.

```bash
WINEPREFIX=~/Games/msfs-prefix xtux-cli run "Microsoft Flight Simulator 2024"
```

Run `prefix init` for every prefix you use. The launcher does not initialize a new prefix automatically yet.
