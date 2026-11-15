---
title: Tux-Force starts
date: 2026-11-15
authors: tuxforce
excerpt: Tux-Force lets you play the Xbox PC games you own or subscribe to on Linux, with real licenses. Here is where it stands and where it is going.
tags:
  - announcement
---

Tux-Force is a new community project with one goal: every PC game you legitimately own or subscribe to should run on
Linux as a first-class experience. That includes the Microsoft Store and PC Game Pass games built on the GDK, which so
far have no official way onto Linux.

## Real licenses, no cracks

You sign in with your own Microsoft account. Microsoft issues the licenses, and the games talk to the real Xbox Live,
PlayFab and store services. Only what your account is entitled to will start. Account tokens stay on your PC.

## What works today

- **Farming Simulator 25 plays** completely: menus, saves, ModHub, achievements, presence and a clean exit.
- **Windows installs run in place.** If you dual boot, games the Windows Xbox app installed start straight from the
  Windows partition. xTux uses the same install layout for its own downloads.
- **A first launcher.** The xTux Launcher shows your games, signs you in and starts them. The command line
  (`xtux-cli list`, `xtux-cli run "<game>"`) does the same and completes game names.
- **Prefix setup in one command:** DXVK, vkd3d-proton and the Microsoft root certificates with
  `xtux-cli prefix init`.

Microsoft Flight Simulator 2024 signs in and reaches its services but does not get past its own backend yet.

## Built on Xodus, built with AI

The core repositories are soft forks of the [xodus-gaming](https://github.com/xodus-gaming) projects, and everything
builds on their work. Tux-Force sets its own direction: a whole ecosystem with launcher, store view, automatic setup
and community compatibility reports. It is developed with AI tools in the open, and AI-assisted contributions are
welcome.

## What comes next

Owned and Game Pass games in the launcher, installs and updates from the GUI, a Flatpak, and more tested games. The
[roadmap](/project/roadmap/) has the details, and the [compatibility list](/compatibility/) shows what runs.

Want to help? Test a game and [report it](/compatibility/#report-a-game), or read
[Contributing](/project/contributing/).
