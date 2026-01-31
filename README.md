# fund-investment-tracker

> This project is being developed by an autonomous coding agent.

## Overview

Product Requirements Document: Fund Investment Tracker

1. Purpose

Build a program that, given a fund name or identifier, finds all companies the fund has invested in and aggregates related informati...

## Features

- CLI entrypoint: accepts fund name, identifier, or profile URL and outputs normalized portfolio data (JSON/CSV).
- Orchestrator: runs connectors in parallel, merges and deduplicates results, and returns normalized data model.
- Crunchbase connector: stubbed dataset with a small API client fallback (uses CRUNCHBASE_API_KEY if provided via env).
- Normalizer: maps connector output to the project data model and computes per-field confidence scores.
- Exporter: JSON export (includes generated summary) and CSV export (companies + investments).
## Getting Started

### Prerequisites

*Prerequisites will be documented here.*

### Installation

```bash
# Installation instructions will be added
```

### Usage

```bash
# Usage examples will be added
```

## Development

See [TODO.md](TODO.md) for the current development status.

## Testing

```bash
# Test instructions will be added
```

## License

MIT
