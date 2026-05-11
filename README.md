# AI-Powered Launch Readiness Command Center

> End-to-end Technical Program Management case study simulating the deployment of an AI-based visual inspection system in a manufacturing environment.

**[Live Dashboard →](YOUR_STREAMLIT_URL)**

---

## Project Summary

A 19-week program simulation managing the cross-functional deployment of an AI-powered defect detection system across 6 teams and 7 phases. Built using Hybrid Agile-Waterfall methodology with real PM tools — Smartsheet for program scheduling, Notion for Agile sprint tracking, and Python/Streamlit for live KPI monitoring.

**Final launch status: AT RISK** — driven by supply chain delays, integration failures, and UAT pass rate of 85% (below 95% threshold).

---

## Key Metrics

| Metric | Value |
|--------|-------|
| Program Duration | 19 weeks (May – Sep 2026) |
| Total Phases | 7 |
| Total Tasks | 39 |
| Milestones | 7 |
| Overall Completion | ~74% |
| UAT Pass Rate | 85% (target: 95%) |
| High-Risk Tasks | 12 |
| Change Requests | 7 (6 approved, 1 rejected) |
| RAID Items | 9 |
| Launch Status | **AT RISK** |

---

## Program Architecture

```
Phase 1: Initiation & Requirements     [100% Complete]
Phase 2: Planning & Design             [90%  In Progress]
Phase 3: Hardware & Data Readiness     [70%  At Risk]
Phase 4: Installation & Integration    [60%  At Risk]
Phase 5: UAT & Quality Validation      [50%  At Risk]
Phase 6: Launch Preparation            [60%  At Risk]
Phase 7: Go-Live & Monitoring          [45%  Delayed]
```

---

## PM Deliverables

| Deliverable | Tool | Status |
|-------------|------|--------|
| Program Schedule (Gantt) | Smartsheet | Complete |
| Agile Sprint Board | Notion | Active |
| RAID Log | Structured log | 9 items tracked |
| Risk Register | Probability × Impact matrix | 8 risks scored |
| Change Request Log | Formal CR process | 7 CRs (6 approved) |
| Stakeholder Matrix | Interest/Influence grid | 6 stakeholders |
| UAT Test Plan | Structured test cycles | 2 cycles planned |
| KPI Dashboard | Streamlit (live) | Deployed |
| Executive Status Report | Formal memo | AT RISK issued |
| Lessons Learned | End-of-phase retrospective | Documented |

---

## Why Launch is AT RISK

Three compounding issues:

1. **Supply chain delay** — Camera hardware delivery slipped, creating a cascade into Phase 4 installation (dependent on hardware arrival)
2. **Integration failure** — Data pipeline refresh failing intermittently; false negatives in AI model above acceptable threshold
3. **UAT below threshold** — 17/20 tests passed in Cycle 1 (85%) against a 95% acceptance criteria; Cycle 2 not yet executable pending defect resolution

---

## Methodology

**Hybrid Agile-Waterfall** — Waterfall for program-level governance (phases, milestones, gates) with Agile sprints inside each phase for development and testing tasks.

Key frameworks used:
- RAID Log (Risks, Assumptions, Issues, Dependencies)
- Risk Register with Probability × Impact scoring
- Formal Change Control with CR log
- Stakeholder mapping (Interest vs Influence matrix)
- Go/No-Go decision framework with quantified KPIs
- UAT acceptance criteria with measurable pass/fail thresholds

---

## Tech Stack

| Layer | Tool |
|-------|------|
| Program Scheduling | Smartsheet (Gantt, task tracking, milestones) |
| Agile Sprint Management | Notion (sprint board, backlog) |
| KPI Dashboard | Python · Streamlit · Plotly |
| Documentation | Notion (case study) |

---

## Author

**Akshada Karade**  
MS Engineering Management, UMass Amherst  
[LinkedIn](https://www.linkedin.com/in/akshadakarade2412/) | [GitHub](https://github.com/Akshada2412)
