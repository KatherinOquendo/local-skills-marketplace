# FinOps Operating Model

Reference para estructura de equipo, gobernanza, cadencia, madurez, y tooling.


## FinOps Team Structure

### Core Roles

| Role | Responsibility | FTE |
|------|---------------|-----|
| FinOps Lead | Strategy, cross-functional coordination, maturity roadmap | 1.0 |
| Cloud Economist | Cost analysis, forecasting, rate optimization | 0.5-1.0 |
| Finance Partner | Budget alignment, P&L integration, variance analysis | 0.25-0.5 |
| Engineering Champion | Team-level optimization, tagging compliance | 0.1 per team |
| Executive Sponsor | Budget approval, cultural alignment, escalation | As needed |

### RACI Matrix

| Activity | FinOps Lead | Cloud Economist | Finance Partner | Eng Champion | Exec Sponsor |
|----------|:-----------:|:---------------:|:---------------:|:------------:|:------------:|
| Tagging strategy | A | R | C | R | I |
| Cost dashboards | A | R | C | I | I |
| RI/SP purchases | R | R | A | C | I |
| Right-sizing | C | R | I | A | I |
| Budget setting | C | R | A | C | A |
| Anomaly response | A | R | I | R | I |
| Forecasting | A | R | R | C | I |
| Showback reports | A | R | R | I | I |
| Chargeback model | A | C | R | I | A |
| Maturity assessment | R | C | C | C | A |
| Quarterly business review | R | R | R | C | A |

*R=Responsible, A=Accountable, C=Consulted, I=Informed*

---

## Cadence Framework

| Cadence | Activity | Owner | Duration |
|---------|----------|-------|----------|
| Daily | Anomaly alert review | Cloud Economist | 15 min |
| Daily | Cost dashboard check | FinOps Lead | 10 min |
| Weekly | Team cost standup | Eng Champion + team | 15 min |
| Weekly | FinOps sync + waste review | FinOps Lead + Economist | 30 min |
| Monthly | Cost review (budget vs. actual) | FinOps Lead + Finance | 60 min |
| Monthly | RI/SP coverage + tag compliance | Cloud Economist | 30 min |
| Quarterly | Business review (P&L, unit economics) | All + Exec Sponsor | 90 min |
| Quarterly | Maturity assessment + commitment planning | FinOps Lead + Finance | 60 min |

---

## Maturity Model: Crawl / Walk / Run

### Crawl — Foundation (Months 0-6)

| Dimension | Capabilities | KPIs |
|-----------|-------------|------|
| Visibility | Basic tagging (4+ mandatory tags), monthly cost reports | Tag compliance >60% |
| Allocation | Top-level cost by account/service | Cost attributed >50% |
| Optimization | Ad-hoc right-sizing, terminate obvious waste | Waste reduction 10-15% |
| Rate | No commitments or basic 1yr SP | RI/SP coverage 0-30% |
| Forecasting | Spreadsheet-based, quarterly forecast | Accuracy ±20% |
| Governance | Reactive budgets, manual alerts | Budget breach <3/quarter |
| Culture | Centralized FinOps team drives all actions | FinOps team hired |

### Walk — Operationalize (Months 6-18)

| Dimension | Capabilities | KPIs |
|-----------|-------------|------|
| Visibility | Full tagging, daily dashboards, anomaly detection | Tag compliance >85% |
| Allocation | Showback reports per team, shared cost allocation | Cost attributed >80% |
| Optimization | Systematic right-sizing, scheduling, storage tiering | Waste <10% of spend |
| Rate | RI/SP portfolio managed, spot for eligible workloads | Coverage 50-70% |
| Forecasting | Driver-based forecasting, monthly updates | Accuracy ±10% |
| Governance | Proactive budgets, automated alerts, escalation paths | Budget breach <1/quarter |
| Culture | Engineering champions per team, cost in sprint reviews | Champions in 80% of teams |

### Run — Optimize (Months 18+)

| Dimension | Capabilities | KPIs |
|-----------|-------------|------|
| Visibility | Real-time dashboards, automated anomaly response | Tag compliance >95% |
| Allocation | Chargeback to P&L, unit economics per product | Cost attributed >95% |
| Optimization | ML-driven recommendations, autonomous right-sizing | Waste <5% of spend |
| Rate | Optimized portfolio, automated RI/SP management | Coverage 70-85% |
| Forecasting | ML-assisted forecasting, weekly updates | Accuracy ±5% |
| Governance | Predictive budgets, policy-as-code guardrails | Zero unplanned breaches |
| Culture | Engineering-owned, cost as architecture decision | Cost in every design review |

---

## KPIs by Category

| Category | KPI | Crawl Target | Walk Target | Run Target |
|----------|-----|:------------:|:-----------:|:----------:|
| Efficiency | Effective savings rate | 10-15% | 25-35% | 40-50% |
| Efficiency | Waste as % of spend | <20% | <10% | <5% |
| Coverage | RI/SP coverage | 0-30% | 50-70% | 70-85% |
| Coverage | Tag compliance | >60% | >85% | >95% |
| Accuracy | Forecast accuracy | ±20% | ±10% | ±5% |
| Speed | Anomaly response time | 48h | 8h | 1h (automated) |
| Business | Unit cost trend | Measured | Declining | Optimized per unit |
| Culture | Teams with FinOps champion | 1 central | 80% of teams | 100% of teams |

---

## Tooling Landscape

| Category | AWS Native | Third-Party |
|----------|-----------|-------------|
| Visibility | Cost Explorer, CUR | CloudHealth, Apptio, OpenCost |
| Optimization | Compute Optimizer, Trusted Advisor | Spot.io, ProsperOps, Karpenter |
| Anomaly detection | Cost Anomaly Detection | Anodot, Datadog |
| Governance | AWS Budgets, SCPs | Flexera, Infracost, Cloud Custodian |
| RI/SP management | Cost Explorer RI/SP | ProsperOps, Zesty |
| Kubernetes | — | Kubecost, Cast.ai, OpenCost |

---
**Source**: FinOps Foundation. *FinOps Framework — Capabilities* (2024). | Storment & Fuller. *Cloud FinOps* (2nd ed.).
