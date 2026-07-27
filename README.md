# SaaS Revenue & Churn Analytics

Analyzing subscriber data (MRR, churn drivers, cohort retention, LTV) 
to identify where a subscription business is losing revenue and why.

## Data
Telco Customer Churn dataset (IBM), reframed as a SaaS subscriber base —
tenure = months as customer, MonthlyCharges = per-customer MRR, 
Contract = plan type.

## Status
🚧 In progress — Phase 3 of 6 complete

## Phases
- [x] Phase 1 — Data cleaning
- [x] Phase 2 — MRR
- [x] Phase 3 — Churn by segment
- [ ] Phase 4 — Cohort retention
- [ ] Phase 5 — LTV
- [ ] Phase 6 — Tableau dashboard

## Key Findings
- Total MRR: $316,985.75 | ARR: $3,803,829.00
- Month-to-month contracts are the largest revenue segment ($136,447 MRR), ahead of Two year ($98,840) and One year ($81,698)
- Churn is heavily concentrated in Month-to-month contracts (42.71%) and the first 6 months of tenure (52.94%) — both point to the same underlying risk: customers who haven't committed long-term or aren't yet "settled" are the most likely to leave
- Electronic check payers churn at 45.29%, ~3x the rate of automatic payment methods (15-17%) — a correlation worth flagging, though the dataset can't confirm why