# SaaS Revenue & Churn Analytics

Analyzing subscriber data (MRR, churn drivers, cohort retention, LTV) 
to identify where a subscription business is losing revenue and why.

## Data
Telco Customer Churn dataset (IBM), reframed as a SaaS subscriber base —
tenure = months as customer, MonthlyCharges = per-customer MRR, 
Contract = plan type.

## Status
🚧 In progress — Phase 5 of 6 complete

## Phases
- [x] Phase 1 — Data cleaning
- [x] Phase 2 — MRR
- [x] Phase 3 — Churn by segment
- [x] Phase 4 — Cohort retention
- [x] Phase 5 — LTV
- [ ] Phase 6 — Tableau dashboard

## Key Findings
- Total MRR: $316,985.75 | ARR: $3,803,829.00
- Month-to-month contracts are the largest revenue segment ($136,447 MRR), ahead of Two year ($98,840) and One year ($81,698)
- Churn is heavily concentrated in Month-to-month contracts (42.71%) and the first 6 months of tenure (52.94%) — both point to the same underlying risk: customers who haven't committed long-term or aren't yet "settled" are the most likely to leave
- Electronic check payers churn at 45.29%, ~3x the rate of automatic payment methods (15-17%) — a correlation worth flagging, though the dataset can't confirm why
- LTV by contract: Month-to-month ($155) vs Two year ($2,146) — a 14x difference, driven almost entirely by churn rate rather than price
- Electronic check payers have the lowest LTV ($168) despite the highest average monthly charge ($76/mo) — high churn cancels out the higher per-month revenue


## Note on Cohort Analysis
This dataset provides only a snapshot in time (tenure as of one moment), not real signup dates or ongoing history. Cohorts here are reconstructed by working backward from tenure, which means customers in the same cohort share nearly identical tenure values by construction. As a result, this chart is better read as a "survival curve by tenure length" (when do customers with a given tenure tend to churn) rather than true calendar-time retention tracking (which would require watching the same real cohort's behavior diverge over following months). This also means the oldest cohort label (e.g. 2020-01) isn't really "one signup month" — it's a pile-up of every customer at the dataset's maximum tenure value (72 months), since tenure appears to be capped in this dataset. In a production dataset with real signup timestamps, this analysis would show gradual divergence within each cohort instead of the flat-then-drop pattern seen here.