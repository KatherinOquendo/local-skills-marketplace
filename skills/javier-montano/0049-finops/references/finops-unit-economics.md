# FinOps Unit Economics & Cost Allocation

Reference para unit cost methodology, margin analysis, cloud P&L, y showback/chargeback.


## Unit Cost Calculation Methodology

### Core Unit Metrics

| Metric | Formula | Good Benchmark | Data Sources |
|--------|---------|---------------|--------------|
| Cost per Transaction (CPT) | Total infra cost / total transactions | Declining MoM | Billing + APM |
| Cost per Active User (CPAU) | Total infra cost / monthly active users | <5% of ARPU | Billing + analytics |
| Cost per API Call | API-tier infra cost / total API calls | <$0.001 for high-volume | Billing + API gateway |
| Cost per GB Processed | Processing infra cost / GB processed | Declining with scale | Billing + pipeline metrics |
| Cost per GB Stored | Storage cost / total GB stored | Tiered by data age | Billing + storage metrics |
| Infra Cost as % Revenue | Total cloud cost / total revenue | 10-25% SaaS, 5-15% enterprise | Billing + finance |

### Calculation Principles

1. **Denominator consistency**: Use same time window for cost and usage (monthly recommended)
2. **Include all layers**: Compute + storage + network + support + tax
3. **Amortized commitments**: Spread RI/SP cost across term, not payment date
4. **Exclude one-time**: Migration, initial setup, POC costs tracked separately
5. **Marginal vs. average**: Report both — marginal cost drives scaling decisions

### Unit Cost Trend Analysis Template

| Month | Revenue | Cloud Cost | Cost/Revenue | MAU | CPAU | Transactions | CPT |
|-------|---------|-----------|:------------:|-----|------|-------------|-----|
| Jan | $XXX,XXX | $XX,XXX | XX.X% | XX,XXX | $X.XX | X,XXX,XXX | $0.XXX |
| Feb | — | — | — | — | — | — | — |
| Mar | — | — | — | — | — | — | — |
| Trend | — | — | Target: declining | — | Target: declining | — | Target: declining |

---

## Margin Analysis Framework

### Cloud Cost Impact on Gross Margin

| Component | Calculation | Target |
|-----------|------------|--------|
| Revenue | Top-line revenue per product/service | From finance |
| COGS — Cloud | Direct cloud cost for delivering product | Tracked via tagging |
| COGS — Other | Support, third-party APIs, licensing | From finance |
| Gross Profit | Revenue - COGS (cloud + other) | — |
| Gross Margin | Gross Profit / Revenue | >65% SaaS benchmark |
| Cloud Margin Impact | Cloud COGS / Revenue | <20% is healthy |

### Per-Customer Profitability

| Customer Tier | Revenue/mo | Cloud Cost/mo | Margin | Action |
|--------------|-----------|--------------|--------|--------|
| Enterprise | >$10K | Measure via tags | >70% target | Optimize shared infra |
| Mid-market | $1K-10K | Measure via tags | >60% target | Right-size per tenant |
| SMB | <$1K | Estimate proportional | >50% target | Multi-tenant efficiency |
| Free tier | $0 | Estimate proportional | Negative (planned) | Cap resource limits |

---

## Cloud P&L Template

### Cloud P&L Structure

| Category | Line Items | Allocation Method |
|----------|-----------|-------------------|
| Revenue | Product revenue by line | Finance attribution |
| Direct Cloud (COGS) | Compute, DB, AI/ML, Storage, Network | Tagged to product |
| Shared Cloud | Platform, Security, Networking, Support | Proportional or even-split |
| **Total Cloud Cost** | Direct + Shared | Sum |
| **Cloud Gross Margin** | Revenue - Total Cloud Cost | Calculated |

Target: Cloud cost <20% of revenue for healthy SaaS margin.

---

## Showback / Chargeback Models

### Model Comparison

| Dimension | Showback | Chargeback |
|-----------|----------|------------|
| Financial impact | Visibility only | Cost transfer to BU budget |
| Complexity | Low | High (billing integration, disputes) |
| Maturity | Crawl/Walk | Run |
| Behavior change | Moderate | Strong (budget accountability) |
| Recommended | New to FinOps | >$1M/mo cloud spend |

### Allocation Methods

| Cost Type | Method |
|-----------|--------|
| Tagged resources | Direct attribution |
| Shared compute | Proportional by CPU/memory |
| Shared storage/network | Proportional by usage |
| Security/compliance | Even split |
| Discounts (RI/SP) | Proportional to eligible usage |

### Chargeback timeline: Report T+5 → Review T+10 → Dispute T+10 → Investigate T+15 → Final T+15 → P&L T+20.

---

## Tagging Strategy Template

### Mandatory Tags (Enforce via SCP/Policy)

| Tag Key | Purpose | Example Values |
|---------|---------|---------------|
| `Environment` | Env classification | prod, staging, dev, test |
| `Team` | Owning team | platform, data, ml, frontend |
| `Project` | Project/initiative | project-alpha, ml-pipeline |
| `CostCenter` | Finance cost center | CC-1001, CC-2050 |
| `Application` | Application name | api-gateway, ml-inference |
| `Owner` | Technical owner | jane@company.com |

**Enforcement:** Preventive (SCP deny untagged) + Detective (Config Rules) + Corrective (auto-tag Lambda) + Reporting (weekly compliance dashboard).

---
**Source**: FinOps Foundation. *FinOps Framework — Capabilities* (2024). | Storment & Fuller. *Cloud FinOps* (2nd ed.).
