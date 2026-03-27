# FinOps Optimization Playbook

Reference para rate optimization, usage optimization, y priorizacion de iniciativas.

---

## Rate Optimization Techniques

### Reserved Instances (RI) vs. Savings Plans (SP)

| Dimension | Reserved Instances | Savings Plans |
|-----------|-------------------|---------------|
| Scope | Specific instance type + region | Any instance family (Compute SP) or any usage (EC2 SP) |
| Flexibility | Low — locked to config | High — applies to any matching usage |
| Discount depth | Deepest (up to 72%) | Moderate (up to 66%) |
| Best for | Stable, predictable workloads | Variable workloads, multi-service |
| Risk | Stranded capacity if needs change | Lower — broader applicability |
| Recommendation | Databases, core infra | Compute fleet, general purpose |

### Commitment Strategy Matrix

| Usage Stability | Confidence | Recommendation | Term |
|----------------|------------|----------------|------|
| >90% steady | High | All Upfront 3yr RI | Max savings |
| 70-90% steady | Medium | Partial Upfront 1yr SP | Balance savings/flexibility |
| 50-70% steady | Low | No Upfront 1yr SP | Minimize commitment risk |
| <50% steady | Variable | On-demand + spot | No commitment |

### Spot / Preemptible Instances

**Eligible:** Batch/ETL, CI/CD, ML training (with checkpointing), dev/test, stateless workers.
**Not eligible:** Databases, stateful services, real-time user-facing APIs.
**Best practices:** Diversify 4+ instance types, 3+ AZs, graceful shutdown on 2-min warning. Savings: 60-90%.

---

## Usage Optimization Patterns

### Right-Sizing Decision Framework

| Metric | Threshold | Action | Savings Estimate |
|--------|-----------|--------|-----------------|
| CPU avg <10% for 14d | Critical waste | Terminate or downsize 2+ sizes | 75-90% |
| CPU avg <40% for 14d | Over-provisioned | Downsize 1 size | 30-50% |
| CPU avg 40-70% for 14d | Well-sized | Monitor | — |
| CPU avg >80% for 14d | Under-provisioned | Upsize or scale out | Performance risk |
| Memory avg <20% for 14d | Over-provisioned | Switch to compute-optimized | 20-40% |
| GPU avg <30% for 14d | Critical waste | Evaluate CPU or smaller GPU | 60-80% |

### Scheduling Patterns

| Environment | Schedule | Hours/Week | Savings vs. 24/7 |
|-------------|----------|------------|-------------------|
| Development | Mon-Fri 8am-8pm | 60/168 | 64% |
| Staging | Mon-Fri 6am-10pm | 80/168 | 52% |
| QA/Test | Mon-Fri 8am-6pm | 50/168 | 70% |
| Demo | On-demand (manual start) | ~10/168 | 94% |
| Production | 24/7 (no scheduling) | 168/168 | 0% |

### Idle Resource Detection Checklist

| Resource Type | Idle Signal | Monthly Waste (typical) |
|--------------|-------------|------------------------|
| Unattached EBS volumes | No attachment for 7+ days | $50-500 per volume |
| Unused Elastic IPs | Not associated to running instance | $3.65/month each |
| Idle load balancers | Zero connections for 7+ days | $16-30/month each |
| Stopped EC2 with EBS | Stopped >7 days, EBS still billed | Varies by volume size |
| Unused NAT Gateways | Zero bytes processed 7+ days | $32+/month each |
| Orphaned snapshots | No associated volume, >90 days old | $0.05/GB/month |
| Idle RDS instances | Zero connections for 7+ days | $50-2000/month |
| Unused SageMaker endpoints | Zero invocations 7+ days | $100-5000/month |

---

## Storage Optimization

### S3 Lifecycle Policy Template

| Data Age | Access Pattern | Storage Class | Cost/GB/month |
|----------|---------------|---------------|---------------|
| 0-30 days | Frequent | S3 Standard | $0.023 |
| 30-90 days | Infrequent | S3 Standard-IA | $0.0125 |
| 90-180 days | Rare | S3 Glacier IR | $0.004 |
| 180-365 days | Archive | S3 Glacier Flexible | $0.0036 |
| >365 days | Compliance/legal | S3 Glacier Deep Archive | $0.00099 |

### EBS: Migrate gp2 to gp3 (20% savings, better perf). Evaluate io1/io2 → gp3 if <16K IOPS.

---

## AI/ML Cost Optimization

| Optimization | Technique | Savings |
|-------------|-----------|---------|
| Training compute | Spot + checkpointing | 60-70% |
| Inference compute | Graviton/Inferentia vs. GPU | 40-60% |
| Model serving | Batch vs. real-time (async) | 50-80% |
| Model selection | Smaller model tier | 80-95% per call |
| Prompt optimization | Shorter prompts, caching | 20-40% |

---

## Optimization Prioritization Matrix

| Priority | Category | Typical Savings | Effort | Risk | Timeline |
|----------|----------|----------------|--------|------|----------|
| P0 | Terminate waste (idle, orphaned) | 5-15% total | Low | None | Week 1 |
| P1 | Right-sizing (obvious cases) | 10-20% compute | Low | Low | Week 2-3 |
| P2 | Scheduling non-prod | 50-70% non-prod | Medium | Low | Week 3-4 |
| P3 | Storage tiering + EBS migration | 20-40% storage | Medium | Low | Month 2 |
| P4 | RI/SP purchase (1yr) | 20-40% committed | Medium | Medium | Month 2-3 |
| P5 | Spot adoption | 60-80% eligible | High | Medium | Month 3-4 |
| P6 | Architecture refactor | 30-60% workload | High | High | Quarter 2+ |

**Rule of thumb:** P0-P2 deliver 60% of total savings with 20% of effort. Start there.

---
**Source**: FinOps Foundation. *FinOps Framework* (2024). | AWS Cost Optimization Pillar (2024).
