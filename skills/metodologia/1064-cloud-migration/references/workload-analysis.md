# S2: Workload Analysis & Dependency Mapping -- Detailed Reference

## Automated Discovery Tools

| Tool | Provider | Method | Discovers |
|---|---|---|---|
| AWS Application Discovery Service | AWS | Agent or agentless | Server config, utilization, network connections, process data |
| AWS Migration Hub | AWS | Aggregator | Unified view across discovery + migration tools |
| Azure Migrate | Azure | Agent or appliance | Servers, databases, web apps, VDI; includes assessment + migration |
| Azure App Service Migration Assistant | Azure | Web app scan | .NET/Java web app readiness for Azure App Service |
| Google Cloud Migration Center | GCP | Agent or API import | Technical fit, TCO, migration complexity scoring |
| Cloudamize | Multi-cloud | Agent-based | Performance profiling, right-sizing, cost projection, dependency mapping |
| Flexera One | Multi-cloud | CMDB integration | License optimization, cloud cost modeling, portfolio rationalization |

- **Start with agentless discovery** for broad inventory (network flow analysis, DNS logs). Deploy agents on Tier 1/2 applications for detailed dependency and performance data. [EXPLICIT]
- Run discovery for minimum 30 days to capture full monthly patterns (batch jobs, month-end processing). [EXPLICIT]

## Application Inventory Fields

Name, owner, business unit, criticality tier (T1-T4), technology stack, infrastructure requirements (CPU, memory, storage, network), performance baseline (response time, throughput, utilization), compliance requirements. [EXPLICIT]

## Dependency Graph

- App-to-app: API calls, file transfers, shared databases
- App-to-infrastructure: specific hardware, network, licenses
- Data dependencies: shared databases, ETL feeds, replication chains
- External: third-party APIs, SaaS integrations, partner connections

[EXPLICIT]

## Data Gravity Analysis

- Data gravity score per workload: `(data_volume_TB * access_frequency * compliance_anchors)` -- higher score = harder to move [EXPLICIT]
- Transfer time estimate: `(data_size_GB / bandwidth_Gbps) * 8 / 3600 = hours` + 30-50% verification overhead [EXPLICIT]
- Connectivity: Direct Connect/ExpressRoute for >5TB; VPN for smaller transfers; Snowball/Data Box for >50TB
- **Anti-pattern:** Underestimating data volumes and WAN throttling. Start continuous replication weeks before cutover. [EXPLICIT]

## Application Difficulty Scoring

- Score 1-5 on: technical complexity, dependency count, data gravity, compliance constraints [EXPLICIT]
- Composite: `(technical * 0.3) + (dependencies * 0.25) + (data_gravity * 0.25) + (compliance * 0.2)` [EXPLICIT]
- Score >4.0: requires dedicated migration architect and extended parallel-run [EXPLICIT]
- Group tightly coupled applications into the same wave [EXPLICIT]

---

# S5: Migration Execution Patterns -- Detailed Reference

## Rehost Tools

AWS MGN (Application Migration Service), Azure Migrate/Site Recovery, GCP Migrate for Compute Engine. Process: install agent, replicate, test, cutover, decommission. [EXPLICIT]

## Database Migration

Homogeneous (native replication, DMS continuous) or heterogeneous (schema conversion + DMS). Zero-downtime via continuous replication. Validate: row counts, checksums, sample comparison. [EXPLICIT]

## TCO Calculator Methodology

| Cost Category | On-Premises | Cloud |
|---|---|---|
| Compute | Hardware amortization (3-5yr) | Reserved + on-demand instances |
| Storage | SAN/NAS, disk replacement | S3/EBS tiered pricing |
| Facilities | Power, cooling, DC lease ($8-15/kW/mo) | Included |
| Staff | FTE * fully loaded cost | Reduced (managed services) |
| Licenses | On-prem perpetual or subscription | BYOL, cloud-native, or included |
| Network | WAN circuits, load balancers | Egress fees, cross-AZ traffic |
| Migration (one-time) | N/A | Dual-run, tooling, consulting, training |

- Break-even: typically 18-36 months. Include hidden costs: egress fees, premium support, cross-AZ traffic. [EXPLICIT]
- Use AWS Pricing Calculator, Azure TCO Calculator, or Google Cloud Pricing Calculator for estimates. Validate with 3-month post-migration actuals. [EXPLICIT]

## Cutover Rehearsal Checklist

Perform a full dress rehearsal 1-2 weeks before each production cutover: [EXPLICIT]

1. [ ] Execute complete cutover runbook end-to-end in non-prod environment
2. [ ] Measure actual duration vs. planned window (target: <80% of window)
3. [ ] Test data sync: verify final replication lag <1 minute
4. [ ] Execute DNS switch and verify propagation
5. [ ] Run full smoke test suite against cloud endpoints
6. [ ] **Execute rollback procedure** -- restore source, revert DNS, verify source healthy
7. [ ] Validate monitoring/alerting fires correctly in cloud environment
8. [ ] Time the rollback procedure (target: <30 minutes)
9. [ ] Document gaps and update runbook before production cutover
10. [ ] Obtain sign-off from app owner and operations team

## Rollback Decision Criteria

Trigger rollback if ANY of the following occur during cutover: [EXPLICIT]

| Condition | Threshold | Action |
|---|---|---|
| Error rate spike | >5x baseline for 15+ minutes | Immediate rollback |
| Latency degradation | P99 >3x baseline for 15+ minutes | Immediate rollback |
| Data integrity failure | Any checksum mismatch on critical tables | Immediate rollback |
| Functionality gap | Any Tier 1 feature non-functional | Immediate rollback |
| Cutover window exceeded | >80% of planned window with steps remaining | Assess and likely rollback |
| Monitoring blind spot | Key dashboards/alerts not functioning | Pause and remediate; rollback if >30 min |

- Keep source running during validation period (1-2 weeks minimum). [EXPLICIT]
- Reverse replication from cloud to on-prem for data-heavy workloads. [EXPLICIT]
- Rollback window: define per application (typically 24-72 hours post-cutover). [EXPLICIT]

## Common Anti-Patterns

| Anti-Pattern | Consequence | Mitigation |
|---|---|---|
| Skip discovery; migrate by guesswork | Missed dependencies cause outages during cutover | Run automated discovery 30+ days |
| Migrate without application owner | No UAT, no sign-off, unclear accountability | Require named owner before wave assignment |
| No cutover rehearsal | Surprises on go-live night, panic rollbacks | Mandatory dress rehearsal for every wave |
| Big-bang migration of entire portfolio | Maximum blast radius, no learning curve | Wave-based with pilot first |
| Underestimate data transfer time | Cutover window exceeded, forced rollback | Calculate transfer time + 50% buffer; use continuous replication |
| Retire nothing | Cloud costs add to existing costs | Enforce retire/retain classification in 7R assessment |
| No rollback plan | Cannot revert when issues found | Define rollback triggers and test procedure |

[EXPLICIT]
