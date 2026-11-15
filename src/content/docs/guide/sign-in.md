---
title: Sign-in and password prompts
description: How xTux signs in with your Microsoft account, where the tokens live, and why a password can be asked.
---

## Signing in

Sign in once with the Microsoft account that owns your games or has your Game Pass subscription:

```bash
xtux-cli login
```

A window with Microsoft's own sign-in page opens. In the launcher, the **Sign in** button does the same. xTux never
sees your password: you type it into Microsoft's page, and Microsoft hands xTux tokens for your account.

`xtux-cli logout` signs you out again; `xtux-cli logout --device` also removes the registration of this PC.

## Where the tokens are kept

xTux keeps the tokens of your account and of this PC in the system **keychain** (Secret Service: GNOME Keyring or
KWallet), not in a file. They only go to Microsoft. Games never get your account tokens: when a game needs a token or
a license, xTux asks Microsoft for that one result and hands it over (see [Architecture](/project/architecture/)).

## Why a password can be asked

Two password prompts can appear. Neither comes from xTux itself, and neither sends anything to Tux-Force.

### 1. The keychain

If your keychain is locked, KWallet or GNOME Keyring asks for **its** password when xTux reads the tokens. This
happens for example when the keychain does not unlock automatically at login, or closes itself after some idle time.

If you cancel and the keychain stays locked, xTux stops with a message instead of carrying on. It does **not**
register the PC again, which would replace its stored identity.

:::tip
To avoid this prompt, let the keychain unlock at login: use the same password for the wallet or keyring as for your
user account, and turn off the automatic closing in the wallet settings.
:::

### 2. polkit, once per PC

On the very first start xTux registers your PC with Microsoft, as Windows does when it first signs in. Windows sends
the system information of the firmware along (manufacturer, model, serial number, UUID). On Linux this information
is in `/sys/firmware/dmi`, which only root may read, so xTux uses `pkexec` and the system asks for your password.

Because the polkit dialog only shows a command, xTux first explains this in a dialog of its own (kdialog on KDE,
zenity elsewhere) with two buttons:

- **Continue**: the polkit prompt follows; xTux reads the firmware information once.
- **Skip**: no password; the PC is registered without these values. That works too.

The same text appears in the terminal or in the service log. To never be asked, set `XTUX_SKIP_SMBIOS=1`.

This happens only while the PC has no registration yet, so normally exactly once.
