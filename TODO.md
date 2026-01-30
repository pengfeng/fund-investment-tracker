# TODO

## In Progress

- [ ] No items currently in progress.*
- [ ] Add unit tests for Crunchbase connector and CLI
- [ ] Add unit tests for CLI
- [ ] Implement Crunchbase API client (replace stub)

## Pending

- [ ] Purpose
- [ ] Scope
- [ ] Input: fund name, fund identifier, or fund profile URL
- [ ] Output: a structured list of portfolio companies with metadata (company name, website, industry, HQ, funding rounds, date of investment, amount invested if available, investor role, company status, brief description, links to sources)
- [ ] Optional: export to CSV/JSON, deduplication of company names, fuzzy matching, and scheduled updates
- [ ] Users
- [ ] Investment analysts
- [ ] Market researchers
- [ ] Product managers
- [ ] Requirements
- [ ] 1 Functional
- [ ] F1: Accept fund input via CLI, API, or UI
- [ ] F2: Search public data sources (Crunchbase, PitchBook, LinkedIn, official fund pages, news) to find portfolio companies
- [ ] F3: Extract company details: name, website, industry, HQ, founding date, description, current status
- [ ] F4: Extract investment details: round type, date, amount, co-investors
- [ ] F5: Provide confidence score and source links for each data point
- [ ] F6: Export results (CSV/JSON) and provide a summary report
- [ ] 2 Non-functional
- [ ] N1: Respect rate limits and robots.txt; use caching
- [ ] N2: Modular connector architecture for data sources
- [ ] N3: Configurable concurrency and retry policies
- [ ] N4: Secure storage of any API keys; do not commit keys
- [ ] Architecture
- [ ] Input layer (CLI/API/UI)
- [ ] Orchestrator that coordinates source connectors
- [ ] Connectors for each data source (scraper or API client)
- [ ] Normalizer to unify company and investment schema
- [ ] Storage layer (in-memory, optional DB)
- [ ] Exporter module
- [ ] MCP Tools
- [ ] Use available MCP tools for web fetch, KB creation, and connectors where applicable. Prefer kb_add_url, kb_add_website, kb_query for document ingestion and semantic search. Use WebFetch for fetching web pages. Use TodoWrite to track tasks.
- [ ] Data Model
- [ ] Fund: id, name, source_links
- [ ] Company: id, name, website, industry, hq, status, description, founding_date
- [ ] Investment: fund_id, company_id, round_type, date, amount, co_investors, source_links, confidence
- [ ] Implementation Guide Compliance
- [ ] Implementation Plan
- [ ] Phase 1: MVP: CLI input, Crunchbase connector (using API or scraping with care), normalize output, export JSON/CSV
- [ ] Phase 2: Add more connectors (PitchBook, LinkedIn, news), UI, scheduling
- [ ] Phase 3: Improve entity resolution, fuzzy matching, and dashboards
- [ ] Risks
- [ ] Data availability behind paywalls (Crunchbase/PitchBook)
- [ ] Legal/scraping restrictions
- [ ] Inconsistent data across sources
- [ ] Success Metrics
- [ ] Coverage: % of funds for which >=50% of portfolio companies found
- [ ] Accuracy: % of company-investment pairs verified by at least one reliable source
- [ ] Performance: time to process a fund (MVP target < 2 minutes for medium-size funds)
- [ ] Next Steps
- [ ] Identify required data sources and obtain API access
- [ ] Run initial tests on sample funds

## Completed

- [x] No items completed yet.*
- [x] This file is automatically updated by the coding agent.*
- [x] This file is automatically updated by the coding agent.*
- [x] This file is automatically updated by the coding agent.*
- [x] Add CSV exporter and tests
- [x] This file is automatically updated by the coding agent.*
- [x] This file is automatically updated by the coding agent.*
- [x] Implement Crunchbase connector and CLI
- [x] This file is automatically updated by the coding agent.*
- [x] This file is automatically updated by the coding agent.*

---

*This file is automatically updated by the coding agent.*