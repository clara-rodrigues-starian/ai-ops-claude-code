# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a personal reference workspace for AI tooling at Starian. It currently contains standalone HTML reference documents — not a software project with a build system or test suite.

## Contents

- `time_tracking_claude_code_figma_make.html` — A bilingual (Portuguese) reference guide documenting time-tracking methods for Claude Code (CLI) and Figma Make. Intended to be embedded in a web interface that provides CSS variables (`--color-*`, `--border-radius-*`, `--font-mono`) and the Tabler Icons font (`ti ti-*`). Renders correctly only inside that host environment.

## Working with the HTML files

These files use CSS custom properties from a host design system — they will look unstyled if opened directly in a browser. Edit the markup and embedded scripts directly; there is no build step.

The embedded Python/bash code snippets are documentation examples, not executable files in this repo.
