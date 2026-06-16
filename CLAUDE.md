# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a personal reference workspace for AI tooling at Starian. It currently contains standalone HTML reference documents — not a software project with a build system or test suite.

## Contents

- `tetris.html` — Fully self-contained Tetris game. No external dependencies, no build step — open directly in any modern browser. All game logic (board, pieces, rotation, scoring, levels, ghost piece) is in a single `<script>` block. Do not add external libraries or split into multiple files; keep it standalone.

- `time_tracking_claude_code_figma_make.html` — A bilingual (Portuguese) reference guide documenting time-tracking methods for Claude Code (CLI) and Figma Make. Intended to be embedded in a web interface that provides CSS variables (`--color-*`, `--border-radius-*`, `--font-mono`) and the Tabler Icons font (`ti ti-*`). Renders correctly only inside that host environment.

- `README.md` — Project overview in Brazilian Portuguese.

## Working with the HTML files

`tetris.html` is fully standalone and renders correctly when opened directly in a browser.

`time_tracking_claude_code_figma_make.html` uses CSS custom properties from a host design system — it will look unstyled if opened directly in a browser. Edit the markup and embedded scripts directly; there is no build step.

The embedded Python/bash code snippets in the time-tracking file are documentation examples, not executable files in this repo.

## GitHub Repository

This project is mirrored at: https://github.com/clara-rodrigues-starian/ai-ops-claude-code

**Sincronização automática:** Após cada alteração de arquivo (Edit ou Write), o hook PostToolUse em `.claude/settings.json` executa `.claude/git-sync.ps1`, que faz commit e push automaticamente para o branch `main`.

- O script só commita se houver mudanças reais (`git status --porcelain`)
- Mensagem de commit automática: `auto: sync YYYY-MM-DD HH:mm`
- O token de autenticação está embutido na URL do remote (`.git/config`) — não compartilhe esse arquivo
