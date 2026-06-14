# Employee Attrition & HR Analytics Dashboard
## Complete Project Report

---

## 1. Executive Summary

This project presents a comprehensive Employee Attrition & HR Analytics Dashboard built to analyze workforce dynamics, identify attrition drivers, and recommend data-driven retention strategies. Using a synthetic dataset of 148 employees across 10 departments, the project demonstrates end-to-end business analytics — from data collection and statistical analysis to interactive dashboard development and strategic recommendation generation.

**Key Findings**: The organization has a 26.4% attrition rate, with Sales (39.3%), Operations (33.3%), and IT (31.8%) being the most affected departments. Work-life balance concerns and career growth limitations are the primary drivers of voluntary turnover.

## 2. Business Problem

Employee attrition costs organizations 50-200% of annual salary per departing employee. Beyond direct costs, attrition leads to:
- Loss of institutional knowledge
- Decreased team morale
- Reduced productivity during replacement cycles
- Increased workload on remaining staff
- Potential customer relationship damage

The business problem is to understand WHY employees are leaving, WHO is most at risk, and WHAT can be done to improve retention.

## 3. Data Overview

- **Source**: Synthetic HR dataset (generated with realistic distributions)
- **Records**: 148 employees
- **Features**: 20 base columns + 9 derived fields (AgeBand, TenureBand, SatisfactionGroup, EngagementGroup, RiskScore, RiskLevel, DepartureMonth, AttritionCost, WorkforceHealthScore)
- **Attrition Rate**: 26.4% (39 left, 109 stayed)
- **Annual Attrition Cost**: $3.5M
- **Workforce Health Score**: 56/100 (At Risk)

## 4. Methodology

1. **Data Generation**: Created realistic employee records with correlated attributes
2. **Data Processing**: Cleaned, standardized, and derived features (risk scores, health scores, attrition costs, departure months)
3. **Statistical Analysis**: Descriptive statistics, groupby aggregations, correlation analysis
4. **Risk Modeling**: Multi-factor risk score (satisfaction, engagement, overtime, promotions, performance, tenure) with 4-tier classification
5. **Dashboard Development**: Interactive HTML/CSS/JS dashboard with Chart.js v4 — 6 KPIs, 7 charts, cascading filters, executive summaries
6. **Insight Generation**: Pattern identification and root cause analysis
7. **Recommendation Formulation**: Strategic, prioritized action plans with cost-benefit analysis

## 5. Exploratory Analysis

### Workforce Demographics
- Average age: 42.6 years
- Average tenure: 4 years
- Average salary: $6,462/month
- Gender distribution: 57% Male, 42% Female, 1% Other
- Workforce Health Score: 56/100 (At Risk — below 60 threshold)

### Attrition Patterns
- Highest attrition: Sales (39.3%), Operations (33.3%), IT (31.8%)
- Lowest attrition: Finance (0%), R&D (14.3%), Marketing (14.3%)
- Overtime employees: 37.5% attrition vs 21.0% for non-overtime (1.8× more likely to leave)
- Employees without promotion: 28.1% attrition vs 18.5% with promotion
- Annual attrition cost: $3.5M total; Sales accounts for $1.3M (37%)

### Risk Score Distribution
- **Critical** (> 18): 8 employees (5.4%) — highest intervention priority
- **High** (11–18): 74 employees (50.0%)
- **Medium** (9–11): 41 employees (27.7%)
- **Low** (≤ 9): 25 employees (16.9%)
- Highest-risk department: Operations (avg 14.4)

## 6. Root Cause Analysis

### Correlation Findings
| Factor | Correlation with Attrition | Interpretation |
|--------|---------------------------|----------------|
| Risk Score | +0.241 | Strongest composite predictor |
| Monthly Income | +0.218 | Higher earners more likely to leave |
| Job Satisfaction | -0.209 | Lower satisfaction = higher attrition |
| Work-Life Balance | -0.188 | Poor WLB = higher attrition |

### Key Root Causes
1. **Work-Life Balance** (28.2% of attrition reasons)
2. **Career Growth Limitations** (20.5%)
3. **Management Issues** (17.9%)
4. **Health Concerns** (10.3%)
5. **Relocation** (10.3%)

## 7. Dashboard Design

The dashboard follows a clean, executive-friendly layout with:

- **Left Sidebar**: 4 cascading filters (Department → cascading Job Role, Gender, Education) with Reset
- **KPI Row**: 6 metrics — Attrition Rate (primary), Attrition Cost (primary), Workforce Health Score (primary), Retention Rate, Critical Risk Employees, Estimated Annual Savings
- **Executive Summary**: 2 merged cards — Workforce Overview (retention, health, critical count, risk status) and Financial Impact (annual cost, largest cost center, potential savings, highest risk department)
- **Executive Alert Banner**: Bullet-format summary of annual cost, highest-cost department, and savings opportunity
- **At-Risk Employee Table**: Top 5 risk-ranked employees sorted by multi-factor risk score, showing satisfaction, overtime, tenure, risk level badge, and suggested actions
- **Attrition Drivers (2 full-width charts)**:
  - Attrition Cost by Department (ranked horizontal bar, Sales highlighted)
  - Attrition by Department (ranked horizontal bar with percentage labels, zero-values hidden)
- **Workforce Drivers & Forecast (2×2 grid)**:
  - Overtime vs Attrition (stacked bar)
  - Promotion vs Attrition (stacked bar)
  - Monthly Attrition Trend (line chart)
  - Retention Forecast (line chart with projection)
- **Executive Risk Ranking**: Department-level table sorted by average Risk Score with color-coded badges (Critical/High/Medium/Low); includes info note explaining multi-factor scoring
- **Strategic Recommendations**: 5 priority cards with Target / Savings / Timeline metadata

## 8. Key Insights

1. Sales department attrition (39.3%) is 2.5x higher than company average
2. Overtime employees are 1.8x more likely to leave
3. Work-life balance is the #1 reason employees leave
4. Average satisfaction is 3.4/5 — below the 4.0 threshold for healthy retention
5. 17.4% of high performers have not been promoted in 2+ years
6. Operations has the lowest engagement score (2.78) and highest overtime (50%)
7. Finance department has 0% attrition — best practices can be learned
8. Married employees have higher attrition (31.9%) than single employees (25%)
9. Career growth concerns account for 20.5% of voluntary departures
10. Management quality issues drive 17.9% of attrition

## 9. Strategic Recommendations

| Priority | Action | Target | Savings | Timeline |
|----------|--------|--------|---------|----------|
| P1 | **Attrition Cost Reduction** — Retention programs in Sales and Operations | 21% Attrition | $694K | 12 Months |
| P1 | **Sales & Operations Review** — Manager effectiveness and career paths | 25% Attrition | $450K | 6 Months |
| P2 | **Workforce Health Program** — Pulse surveys, flexible work, manager training | 70% Health Score | $200K | 9 Months |
| P2 | **High-Performer Retention** — Accelerated tracks, executive sponsors | 95% Retention | $180K | 6 Months |
| P3 | **Early Warning System** — Real-time alerts for high-risk departments | <15% Quarterly | $100K | 3 Months |

## 10. Conclusion

This project demonstrates how HR analytics can transform workforce data into strategic business insights. The interactive dashboard enables HR leaders to monitor attrition patterns, identify at-risk employees, and implement targeted retention programs. By addressing the root causes identified in this analysis, the organization can reduce voluntary turnover by an estimated 15-20% annually, saving significant costs in recruitment, training, and lost productivity.
