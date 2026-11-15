---
title: Contributing
description: How to help, including the rules for AI-assisted work, branches and documentation.
---

Thanks for helping! This guide applies to all Tux-Force repositories unless a repository says otherwise. The
canonical copy is [CONTRIBUTING.md](https://github.com/Tux-Force/.github/blob/main/CONTRIBUTING.md) in the
organization repository.

## AI welcome

AI-assisted contributions are welcome here. Tux-Force itself is built with AI tools, and chat assistants, coding
agents or autocomplete are all fine to use. Writing everything by hand is just as welcome.

> **Our opinion:** used well, today's coding assistants write, review and debug code better than the average
> programmer, provided you know how to work with them.

What we care about is the result:

- **Test what you submit.** Run it and check that it does what the pull request says.
- **Same review for everyone.** Human, AI or both: every pull request gets the same review and tests.
- **Say when AI helped.** Add a `Co-Authored-By` trailer for the assistant or a short note in the pull request.
- **Say when you vibe-coded it.** If you have no solid background in software engineering or computer science and the
  change was written by AI without you really understanding the code, please say so in the pull request. That is
  welcome too. The reason: experienced developers steer AI differently, step in when it goes wrong and can answer its
  questions properly. Without that background a feature often just about works, and reviewers need to know where to
  look more closely.
- **Run an AI security review before the pull request.** Required when AI wrote any part of the change, recommended
  for changes written by hand. Let an AI assistant review the change for security problems (for example injection,
  unsafe file or network handling, leaked tokens, missing input checks), fix what it finds, and mention in the pull
  request that the review was done.

## Ground rules

- **Legal only.** Tux-Force runs games your account is entitled to. Contributions that bypass licenses, DRM or
  entitlement checks are not accepted.
- **No Microsoft code.** Do not contribute code copied from Microsoft products, leaked sources or decompiled
  binaries. Public documentation, observed behaviour and testing are the way.
- **Keep licenses and credits.** xTux, xgameruntime and wine are forks. Keep license headers and attributions intact.
- **Keep secrets out.** Remove tokens, account data and personal information from logs, issues and prompts.

## Branches

- `main` is protected and holds released code. It only changes through pull requests from `develop`, with green CI;
  every merge into `main` runs the release workflow.
- `develop` is the default branch and where development comes together.
- Work happens on short-lived branches off `develop`: `feature/<name>` for new things, `fix/<name>` for bug fixes,
  `chore/<name>` for tooling and docs. Open the pull request against `develop`; it is merged when CI is green.
- `upstream/...` branches (`upstream/main`, `upstream/legacy-c`, `upstream/bleeding-edge`) mirror the projects we
  forked from. We pull new upstream code into `develop` when it is useful; we do not push to upstream.
- Code, comments and documentation are written in English.

## Documentation

The user documentation lives on this website, in its own repository
([tux-force.github.io](https://github.com/Tux-Force/tux-force.github.io)), not next to the code. So when your change
alters something users notice, such as a new command or option, a changed setting, a new message or prompt, or a
game that now works, please also open a small pull request on the website that updates the page about it. Changes
users do not notice, like refactoring or internal fixes, need no website change. Developer notes that belong to the
code (formats, protocols, crate docs) stay in the code repository.

## Reporting problems

Open an issue in the repository of the affected part (for games: [xTux](https://github.com/Tux-Force/xTux/issues)) with the game, your distribution, GPU and driver, and the relevant part of the log (without tokens or
personal data).
