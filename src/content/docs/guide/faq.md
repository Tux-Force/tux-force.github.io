---
title: FAQ
description: Common questions about Tux-Force.
---

### Is this legal?

Tux-Force only runs games your Microsoft account owns or your subscription includes. You sign in with your own
account, the licenses come from Microsoft's licensing service, and there is no license bypass or DRM circumvention.
The code is written from public documentation and observed behaviour and contains no Microsoft code.

### Is Tux-Force made by Microsoft?

No. It is an unofficial community project, not affiliated with, endorsed by, or sponsored by Microsoft or Xbox.

### Which games work?

GDK games for PC, as sold in the Microsoft Store and included in PC Game Pass. Each game uses the GDK services
differently, so every game needs testing. The [compatibility list](/compatibility/) shows the current state.

### Do I need Windows?

No. xTux can download games itself. If you dual boot, games the Windows Xbox app installed run straight from the
Windows partition, without a second download.

### Do I need Game Pass?

Only for games you do not own. Games you bought in the Microsoft Store work with the account that bought them.

### Does Tux-Force see my account?

No. Your password goes into Microsoft's own sign-in page. The tokens stay in your system keychain on your PC and only
go to Microsoft. Games get single results (a license, a token for one service), never your account tokens. Tux-Force
runs no servers.

### Why does it ask for my password?

Either your keychain is locked, or the PC is registered with Microsoft for the first time. See
[Sign-in and password prompts](/guide/sign-in/#why-a-password-can-be-asked).

### Does it work on the Steam Deck?

Not tested yet. A controller-driven launcher mode for the Deck is still planned.

### Do controllers work?

Yes, in games. Xbox controllers work as usual. PlayStation controllers (DualShock 4, DualSense, DualSense Edge) reach
games as Xbox gamepads by default; see [Controllers](/guide/running-games/#controllers). The launcher itself is still
used with mouse and keyboard.

### How is this different from Xodus?

xTux, xgameruntime and the Wine tree are soft forks of the [xodus-gaming](https://github.com/xodus-gaming) projects,
and everything builds on their work. Tux-Force aims at the whole ecosystem (launcher, store view, prefix setup,
compatibility reports), sets its own pace and welcomes AI-assisted contributions. Useful upstream changes are pulled
in and credited.

### Can I use AI to contribute?

Yes. See [Contributing](/project/contributing/).
