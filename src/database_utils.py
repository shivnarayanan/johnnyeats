https://docs.bigdata.com/llms.txt
https://docs.bigdata.com/api-rest/openapi/openapi_search_service.json
https://docs.bigdata.com/api-reference/search/search-documents.md



# RavenPack Filter Modal Update

## Overview

This change updates two existing flows and renames one of them. The relevant changes are as follows:

- **"RavenPack Company Sources"** is renamed to **"RavenPack Financial Documents"** and its filter modal is updated.
- **"RavenPack Financial News"** retains its name but its filter modal is fully replaced with a new implementation.

Both flows share the same overall layout and field structure, and differ only in how the **"Include Sources"** field works. This is described in detail below.

Review `<PLACEHOLDER>` to understand how filters flow for vector databases. The relevant frontend files are `<PLACEHOLDER>`, `<PLACEHOLDER>`, `<PLACEHOLDER>`, and `<PLACEHOLDER>`. The relevant backend files are `<PLACEHOLDER>`, `<PLACEHOLDER>`, `<PLACEHOLDER>`, and `<PLACEHOLDER>`. Then review `<PLACEHOLDER>` for the full list of changes that need to be made.

---

## General Guidelines

- Field ordering, input field types, and descriptions should be driven by backend configuration as much as possible.
- All input fields are referred to by their **display name (alias)** throughout this document. It is your responsibility to convert them into the appropriate variable names for backend, frontend, and API processing.
- Any fields currently defined in the backend that are not listed in this document should be **removed**.

---

## Search Mode

At the top of the modal, display a **"Search Mode"** radio button with two options. The default value is **"Fast"**.

| Option | Description |
|--------|-------------|
| Fast | Manually select and apply filters with a single query execution for quicker results. |
| Smart | Automatically detects relevant filters and performs multiple query executions to generate more comprehensive results. |

When the user switches between modes, any previously set Fast-mode filters should be **preserved in state but hidden** — they should not be reset. No confirmation dialog is required when switching modes.

---

## Fast Mode

When "Search Mode" is set to **"Fast"**, display the following three sections and their respective fields.

### 1. Content Filters

| Display name | Field type | Notes |
|---|---|---|
| Search Mode | Radio button | As described above — rendered at the top of this section |
| Date Range | Date range picker | Maps to `timestamp.start` and `timestamp.end` in UTC |
| Document Category | Multi-select pills | Maps to `category` with mode always set to `INCLUDE`. Options are the unique list of available categories |
| Include Sources | See per-flow notes below | Behaviour differs between the two flows — see "Include Sources" section |
| Document Type | Panel-driven text area | See "Document Type" section below |

### 2. Reporting Details

| Display name | Field type | Notes |
|---|---|---|
| Company Name(s) | Search-as-you-type multi-select | Searches the KG lookup endpoint. Stores and sends the resolved **entity ID** to `entity.any_of`. Displays the company name in the UI |
| Reporting Entities | Search-as-you-type multi-select | Searches the same KG lookup endpoint as Company Name(s). Stores and sends the resolved **entity ID** to `reporting_entities`. Displays the company name in the UI. Note: unlike Company Name(s), this filters documents *reported by* the company, not merely mentioning it |
| Fiscal Year | Multi-select | Fixed range from **2010 to the current year**. Fiscal Year and Fiscal Quarter selections are paired **explicitly** — there is no cross-product. Each year-quarter pair is added individually and sent as a separate `{fiscal_year, fiscal_quarter}` object in `reporting_periods` |
| Fiscal Quarter | Multi-select | Options: Q1, Q2, Q3, Q4. See Fiscal Year notes above |

### 3. Ranking Parameters

| Display name | Field type | Notes |
|---|---|---|
| Source Boost | Slider | Range: 0–10, step: 0.1, default: 1.0. Controls how much source rank influences relevance |
| Freshness Boost | Slider | Range: 0–10, step: 0.1, default: 1.0. Controls how much document recency influences relevance |
| Diversification | Checkbox | Default: checked. Maps to `ranking_params.content_diversification.enabled` |
| Reranker | Checkbox | Default: checked. Maps to `ranking_params.reranker.enabled` |
| Reranker Threshold | Slider | Only visible when "Reranker" is checked. Range: 0–1, step: 0.01, default: 0.20. Maps to `ranking_params.reranker.threshold` |

---

## Smart Mode

When "Search Mode" is set to **"Smart"**, display only the following section. All other sections and fields should be hidden but their state preserved.

### 1. Content Filters

| Display name | Field type | Notes |
|---|---|---|
| Search Mode | Radio button | As described above |
| Include Sources | See per-flow notes below | Behaviour differs between the two flows — see "Include Sources" section |

---

## Include Sources — Per-Flow Behaviour

Both flows use `source` with `mode: "INCLUDE"` in the API. There is no exclude mode. They differ only in how the user selects sources.

### RavenPack Financial Documents

"Include Sources" uses a **panel-driven text area**. It is not directly editable and works as follows:

- The field displays the user's current selections as read-only text.
- When the user clicks into the field, a **right panel** appears within the filter modal showing a list of checkboxes.
- The checkbox options are hardcoded in the backend using the known `document_type` values from the API spec. Each document type is rendered as a **group header**, with its subtypes rendered as **individual checkboxes** beneath it.
- Note: `NEWS` is intentionally excluded from this panel — news granularity is handled via the Document Category pills. `NEWS` and `SOCIAL-MEDIA-POST` have no subtypes and should not appear as expandable groups.

### RavenPack Financial News

"Include Sources" uses a **search-as-you-type multi-select field**, consistent with the Company Name(s) and Reporting Entities fields. It works as follows:

- The user types a source name (e.g. "Business Insider", "Factset Transcripts").
- The field queries the Knowledge Graph Find Sources endpoint (`/v1/knowledge-graph/sources`) and returns matching results.
- The user selects a source from the dropdown, which is added as a chip displaying the source name.
- The resolved **source ID** is stored and sent to the API — not the source name.

---

## Document Type Panel — Hardcoded Values

The document type right panel is used by **RavenPack Financial Documents** only. The options are hardcoded in the backend as follows. `NEWS` and `SOCIAL-MEDIA-POST` are excluded as they have no subtypes and news filtering is handled via Document Category pills.

| Type | Subtypes |
|------|----------|
| `TRANSCRIPT` | `ANALYST_INVESTOR_SHAREHOLDER_MEETING`, `CONFERENCE_CALL`, `GENERAL_PRESENTATION`, `EARNINGS_CALL`, `EARNINGS_RELEASE`, `GUIDANCE_CALL`, `SALES_REVENUE_CALL`, `SALES_REVENUE_RELEASE`, `SPECIAL_SITUATION_MA`, `SHAREHOLDERS_MEETING`, `MANAGEMENT_PLAN_ANNOUNCEMENT`, `INVESTOR_CONFERENCE_CALL` |
| `TRANSCRIPT-PRESENTATION` | `GENERAL_PRESENTATION` |
| `FILING` | `SEC_10_K`, `SEC_10_Q`, `SEC_8_K`, `SEC_20_F`, `SEC_S_1`, `SEC_S_3`, `SEC_6_K`, `SEC_DEF_14A` |
| `INVESTMENT-RESEARCH` | `COMPANY_REPORT`, `COVERAGE_ANALYSIS`, `ECONOMIC_REPORT`, `FIXED_INCOME_REPORT`, `FUND_REPORT`, `FX_AND_DERIVATIVES_REPORT`, `GENERIC_REPORT`, `INDEX_REPORT`, `INDUSTRY_REPORT`, `MARKET_UPDATE`, `PORTFOLIO_STRATEGY`, `PORTFOLIO_SUMMARY`, `RATING_REPORT`, `RESEARCH_NOTE`, `THEMATIC_ANALYSIS` |

---

## Additional Reference Documentation

The following documentation may be referenced to better understand the available RavenPack API filters and behaviour: `<PLACEHOLDER>`, `<PLACEHOLDER>`, `<PLACEHOLDER>`.
