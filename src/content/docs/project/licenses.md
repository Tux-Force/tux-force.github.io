---
title: Licenses
description: The licenses of Tux-Force, of the libraries it uses, and of what it downloads at run time.
---

Tux-Force is open source. This page lists the licenses of its own code, of the libraries built into it, and of what
it only uses at run time.

## Tux-Force code

| Part | License |
|---|---|
| [xTux](https://github.com/Tux-Force/xTux): crates taken over from Xodus (`xodus`, `msixvc`, …) | GPL-3.0-only, as in Xodus' license, which gives no "or later" |
| xTux: new crates (`xtux-games`, `xtux-protocol`, `xtux-service`, `xtux-cli`, `xtux-launcher`) | GPL-3.0-or-later |
| [Tux-Force Wine](https://github.com/Tux-Force/wine) | LGPL-2.1-or-later, like Wine |
| [xgameruntime](https://github.com/Tux-Force/xgameruntime) | LGPL-2.1-or-later, like upstream |
| Brand assets (logo, mascot) | © Tux-Force, see [Brand](/project/brand/) |

Together, xTux as a program is distributed under GPL-3.0. The full text is the `LICENSE` file in each repository and
in every release archive.

## Libraries in xTux

xTux is built from many Rust libraries (crates). All of their licenses, with the full texts, are listed in
[`licenses/THIRD-PARTY-LICENSES.md`](https://github.com/Tux-Force/xTux/blob/develop/licenses/THIRD-PARTY-LICENSES.md).
The file is generated with [cargo-about](https://github.com/EmbarkStudios/cargo-about) by
`scripts/third-party-licenses.sh` and is shipped in every release archive next to `LICENSE`.

The **xTux Launcher** shows the same in its **About** page: version, the GPL notice, a link to the source code, "Made
with Slint", and every third-party license with its full text.

### Checked on every pull request

The CI job **Licenses and advisories** runs [cargo-deny](https://github.com/EmbarkStudios/cargo-deny) with the
rules in `deny.toml`:

- **Licenses:** only licenses that can be combined with GPL-3.0 are allowed, for example MIT, Apache-2.0, BSD,
  ISC, Zlib, MPL-2.0, Unicode-3.0, LGPL-2.1-or-later and GPL-3.0. A dependency with any other license fails the
  check.
- **Sources:** crates come from crates.io or from a short list of known git repositories; anything else fails.
- **Security advisories:** known vulnerabilities from the [RustSec](https://rustsec.org) database are reported. They
  do not block a pull request yet.

## Used at run time, not distributed

Some things are downloaded or used on your PC but are not part of the Tux-Force releases:

| What | License | How it gets there |
|---|---|---|
| [DXVK](https://github.com/doitsujin/dxvk) | zlib | downloaded from its GitHub releases by `xtux-cli prefix init` |
| [vkd3d-proton](https://github.com/HansKristian-Work/vkd3d-proton) | LGPL-2.1-or-later | downloaded from its GitHub releases by `xtux-cli prefix init` |
| Game artwork | belongs to the publishers | loaded from the Microsoft Store catalog and only cached on your PC |
| Games | belong to their publishers | licensed to your Microsoft account; xTux only starts what your account is entitled to |

Microsoft, Xbox and the names of games are trademarks of their owners. Tux-Force is not affiliated with Microsoft or
Xbox.

## Questions

Found a license problem or a missing notice? Open an [issue in xTux](https://github.com/Tux-Force/xTux/issues).
