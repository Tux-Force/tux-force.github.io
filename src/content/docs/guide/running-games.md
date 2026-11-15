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
| `-e`, `--exe <exe>` | Start a different executable of the game than the one in `MicrosoftGame.config` |
| `-m`, `--market <market>` | Store market for the license, for example `DE` |

Before the game starts, xTux fetches its license from Microsoft, so only games your account is entitled to start.
**Ctrl+C** asks the game to quit, as closing it on Windows would.

If the same game is installed twice (for example once by Windows and once by xTux), `run` lists both folders and asks
you to pick one by path.

## Windows Xbox app installs (dual boot)

Games the Windows Xbox app installed, usually in `XboxGames` on a Windows partition, run straight from there. Mount
the partition (most desktops do this when you open it in the file manager) and add its `XboxGames` folder to
`library_dirs`; drives under `/mnt`, `/media` and `/run/media/$USER` are found automatically.

Nothing is copied and no Windows file is changed or deleted.

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
