# fund-investment-tracker

> This project is being developed by an autonomous coding agent.

## Overview

Product Requirements Document: Fund Investment Tracker

1. Purpose

Build a program that, given a fund name or identifier, finds all companies the fund has invested in and aggregates related informati...

## Features

- CLI entrypoint (src/leet_apps/cli.py): accepts --fund, --output, --format
- Crunchbase connector (stub) at src/leet_apps/connectors/crunchbase.py: returns sample data for MVP and provides a clear extension point for a real API/scraper
- Normalizer (src/leet_apps/normalizer.py): maps raw connector output to unified Fund/Company/Investment schema
- Exporter (src/leet_apps/exporter.py): exports results to JSON and CSV (companies + investments)
- Unit tests for connector, normalizer, and exporter under src/leet_apps/tests

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
