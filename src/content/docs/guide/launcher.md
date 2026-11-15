---
title: Launcher
description: The xTux Launcher, a graphical library to sign in and play.
---

The **xTux Launcher** (`xtux-launcher`) is the graphical front end of xTux. It is at its first milestone: it shows
the games you already have and starts them. Installing, updates and the Game Pass catalog follow (see the
[launcher plan](/project/launcher-plan/#milestones)).

```bash
xtux-launcher
```

## Pages

- **Library:** every game in your library folders, marked as an xTux install or a Windows Xbox app install, with a
  **Play** button. **Refresh** scans the folders again.
- **Settings:** the Wine binary, the prefix and the library folders (one per line). **Save** writes them to
  `~/.config/xtux/settings.toml`, which `xtux-cli` uses too.
- **Sign in** (in the sidebar while you are signed out) opens Microsoft's sign-in window.

The status bar at the bottom shows what is happening: game started, game exited with its exit code, or an error.

## How it works

The launcher does not contain the game logic itself. It talks to `xtux-service`, the same background service
`xtux-cli` uses, and starts it when needed. That way the command line and the launcher always behave the same. See
[Architecture](/project/architecture/).
