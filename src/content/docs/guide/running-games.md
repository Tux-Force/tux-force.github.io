---
title: Running games
description: Find, start, download and move games with xtux-cli; Windows Xbox app installs run in place.
---

## Your library

xTux looks for games in the folders of `library_dirs` in `~/.config/xtux/settings.toml` (see
[Installation](/guide/installation/#settings)). Every folder in there that contains a game counts, whether xTux
downloaded it or the Windows Xbox app installed it.

```bash
xtux-cli list
```

```text
Atomfall                         Xbox app  701B45CA  /mnt/windows/XboxGames/Atomfall
Farming Simulator 25 (PC)        xTux      69445d50  /home/you/.local/share/xtux/games/LS25
```

`xtux-cli list --paths` prints only the folders, for scripts.

## Starting a game

Start a game by its name, its folder name or its path. With [shell completion](/guide/installation/#shell-completion)
set up, Tab completes the names:

```bash
xtux-cli run "Farming Simulator 25 (PC)"
xtux-cli run /mnt/windows/XboxGames/Atomfall
```

Wine, prefix and market come from the settings. You can pass them for a single run instead:

```bash
WINEPREFIX=~/Games/other-prefix xtux-cli run -m DE "Atomfall" ~/wine-tux-force-x86_64/bin/wine
```

| Option | Effect |
|---|---|
| `[WINE]` | Wine binary, defaults to `wine` from the settings |
| `-e`, `--exe <exe>` | Start a different executable of the game than the one xTux picks from `MicrosoftGame.config` |
| `-m`, `--market <market>` | Store market for the license, for example `DE` |
| `-- <args...>` | Replace the game arguments saved in the per-game settings for this run |

Before the game starts, xTux fetches its license from Microsoft, so only games your account is entitled to start.
**Ctrl+C** asks the game to quit, as closing it on Windows would.

If the same game is installed twice (for example once by Windows and once by xTux), `run` lists both folders and asks
you to pick one by path.

Some games need extra setup, which xTux does on its own: games such as Minecraft for Windows start an unencrypted
entry executable from the game folder, get a Windows package identity when they depend on the Windows App Runtime,
and get the GameInput redistributable from their own `Installers` folder installed into the prefix.

If a game crashes, xTux shows a message with the cause it found, and a hint when the graphics card has little video
memory.

## Controllers

PlayStation controllers (DualShock 4, DualSense, DualSense Edge) reach games as **Xbox gamepads** through SDL by
default, because most GDK games only know Xbox gamepads. For a game with its own PlayStation support, choose
**As PlayStation controller** in **Settings → Games** or in the game's settings in the launcher, or in
`settings.toml`:

```toml
controller = "native"   # default: "xbox"
```

The setting is per prefix: a change applies once all games of that prefix are closed.

## Windows Xbox app installs (dual boot)

Games the Windows Xbox app installed, usually in `XboxGames` on a Windows partition, run straight from there. Mount
the partition (most desktops do this when you open it in the file manager) and add its `XboxGames` folder to
`library_dirs`; drives under `/mnt`, `/media` and `/run/media/$USER` are found automatically.

xTux reuses these installs without copying them, and can update them: the launcher's **Updates** page and
`xtux-cli downloads check` also find updates the Xbox app left unfinished (see [Updates](#updates-and-verification)).
The launcher also offers **Delete game…**: after confirmation,
it removes the entire game folder, including Windows installs and any saves inside that folder. Windows then needs
to repair or reinstall that game.

## One install format

xTux uses the same folder layout as the Windows Xbox app for its own downloads too:

```text
<game>/Content/...          the game files
<game>/<CONTENT-ID>         package header (license, keys, file list), named by the content id
<game>/<CONTENT-ID>.xvi     bookkeeping of the Windows Xbox app (only in its installs)
```

So one folder format works everywhere. Whether the Windows Xbox app accepts an install made on Linux has not been
tested yet.

### Moving older installs

Installs made by Xodus or early xTux versions keep the game files directly in the folder with a
`.xodus-streaming.msixvc` file. They still run. To move one into the common layout:

```bash
xtux-cli migrate ~/.local/share/xtux/games/LS25
```

`migrate` only renames files inside the folder, so it is quick and needs no extra space.

## Downloading a game

```bash
xtux-cli streaming 9NXN8GF8N9ZQ ~/.local/share/xtux/games/LS25
```

The source is the game's store id (the code at the end of its Microsoft Store web address) or a content id. If a
product has several packages, xTux asks which one. `--parallel <n>` sets the number of parallel downloads. Ctrl+C
stops the download.


## Download queue

The launcher and CLI share the service's persistent download queue. Add a Store ID from the catalog, optionally
with a configured library folder as the destination:

```bash
xtux-cli downloads
xtux-cli downloads add 9NXN8GF8N9ZQ
xtux-cli downloads pause 1
xtux-cli downloads resume 1
xtux-cli downloads up 1
xtux-cli downloads down 1
xtux-cli downloads remove 1
xtux-cli downloads clear
```

Use the actual queue ID shown by `xtux-cli downloads` in place of `1`. Jobs run one at a time; the service
continues while the launcher is closed and restores the queue after restart. `remove` can delete a partial
installation created by that job; `clear` removes completed queue entries, not installed games.

## Updates and verification

```bash
xtux-cli downloads check
xtux-cli downloads update /mnt/windows/XboxGames/Atomfall
xtux-cli verify /mnt/windows/XboxGames/Atomfall
```

`downloads check` lists installed games with their installed and latest version, for xTux installs and Windows Xbox app
installs alike, including updates the Xbox app started but did not finish. `downloads update <folder>` adds the update
to the download queue. `verify <folder>` checks the files of an installed game against its package.

Per-game Wine, prefix, executable, arguments, environment and controller settings saved in the launcher also apply to
CLI launches. See [Launcher](/guide/launcher/#settings-and-launch-options).
