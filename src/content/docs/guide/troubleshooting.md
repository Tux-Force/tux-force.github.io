---
title: Troubleshooting
description: Logs, debug switches and fixes for common problems.
---

## Where the logs are

- **Service log:** `~/.local/state/xtux/service.log`. Game starts, the game bridge (tokens, licenses) and errors of
  `xtux-service` end up here, also when you start games from the launcher.
- **Terminal:** `xtux-cli` prints progress and errors directly.
- **More detail:** `XODUS_LOG` sets the log filter, for example `XODUS_LOG=debug xtux-cli run "..."`. Wine's own
  output can be widened with `WINEDEBUG`.

When you [report a problem](https://github.com/Tux-Force/xTux/issues), add the game, your distribution, GPU and
driver, and the relevant part of the log. **Remove tokens and personal data first.**

## Debug switches

| Variable | Effect |
|---|---|
| `XTUX_DIRECT=1` | Run the command inside `xtux-cli` instead of through `xtux-service`; output goes to the terminal |
| `XTUX_IDLE_TIMEOUT=<seconds>` | How long `xtux-service` waits idle before it exits (default 300, `0` keeps it running) |
| `XTUX_SERVICE=<path>` | Use this `xtux-service` binary instead of the one next to `xtux-cli` |
| `XTUX_SKIP_SMBIOS=1` | Register the PC without the firmware information, see [password prompts](/guide/sign-in/#2-polkit-once-per-pc) |

## Common problems

### A password dialog appears

See [Sign-in and password prompts](/guide/sign-in/#why-a-password-can-be-asked): it is either your keychain or the
one-time registration of the PC.

### "cannot read the device license from the keychain"

The keychain is locked or not running. Unlock KWallet or GNOME Keyring and try again. Make sure a Secret Service
provider runs in your session (`gnome-keyring-daemon` or `kwalletd`).

### "... is neither a game folder nor an installed game"

`run` did not find the name in your library. Check `xtux-cli list`, the `library_dirs` in the settings, and that the
Windows partition is mounted.

### "... is installed more than once"

The same game is in two library folders. Start it by path, as the message shows.

### No Wine binary

`run` needs the Wine binary, either as the second argument or as `wine` in the settings (launcher: **Settings**).

### The game shows a black screen or no intro video

Make sure the prefix was set up with `xtux-cli prefix init` and that you start the game with the
[Tux-Force Wine release](/downloads/); it contains the video decoder setup and runtime the games need. Check the
[compatibility list](/compatibility/) for known problems with the game.

### The game cannot reach its online services

Run `xtux-cli prefix init` again: it adds the Microsoft root certificates games expect. Check the service log for
errors of the game bridge.

### The game crashed

xTux shows a message with the cause it found, for example a license problem, a missing DLL or running out of
memory. When the graphics card has little video memory, the message says so; lower the graphics settings or the
resolution. The game log (see the launcher's game page) has the details.

### A game no longer starts after an update on Windows

The Windows Xbox app may have left an update unfinished. Check and update the game, then verify it:

```bash
xtux-cli downloads check
xtux-cli downloads update <game folder>
xtux-cli verify <game folder>
```

In the launcher, the **Updates** page does the same.

### A PlayStation controller does not work in a game

By default DualShock 4, DualSense and DualSense Edge reach games as Xbox gamepads. If a game expects a PlayStation
controller, switch the [controller setting](/guide/running-games/#controllers) to *As PlayStation controller*.
Close all games of the prefix before you try again: the change applies only then.

### xtux-cli crashes with "illegal instruction"

xTux uses the AES instructions of the CPU to decrypt game packages. CPUs older than about 2011 do not have them.
