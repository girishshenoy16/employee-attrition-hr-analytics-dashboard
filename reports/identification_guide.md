# Identification Guide

## How to Identify High Attrition Departments

1. Calculate attrition rate per department (attrition count / total employees in dept)
2. Sort departments by attrition rate descending
3. Flag departments exceeding company average by 50% or more
4. Investigate common factors among high-attrition departments

## How to Identify High-Risk Employees

Use the Risk Score algorithm:
- Low satisfaction (< 3) : +2 points per level below 5
- Low work-life balance (< 3) : +1.5 points per level below 5
- Low engagement (< 3) : +2 points per level below 5
- Low manager rating (< 3) : +1 point per level below 5
- Working overtime : +2 points
- No promotion after 3+ years : +1.5 points
- High performer (rating >= 4) : -1 point (bonus)
- New joiner (< 1 year) : +1 point

**Risk Tiers (Employee-Level Dashboard)**: ≤ 9 Low | ≤ 11 Medium | ≤ 18 High | > 18 Critical
**Risk Tiers (Department-Level Table)**: ≤ 9 Low | ≤ 11 Medium | ≤ 13 High | > 13 Critical

> Note: The dashboard uses a wider High/Critical boundary for employee-level scoring (18) to ensure only the most at-risk individuals (top 5.4%) are flagged Critical. The department-level table uses a lower threshold (13) so executive viewers can see meaningful differentiation between departments. The risk score itself weights satisfaction, engagement, overtime, promotions, performance, and tenure — not attrition rate alone. A department with high attrition may show moderate risk if departing employees had average multi-factor scores.

## How to Identify Low Satisfaction Employee Groups

- Pivot table: average satisfaction by department
- Cross-reference: satisfaction by role within department
- Identify departments/roles where avg satisfaction < 3.0
- Check if low satisfaction correlates with high overtime

## How to Identify High-Performing Employee Groups

- Filter employees with Performance Rating >= 4
- Cross-reference by department, role, tenure
- Check which high performers are NOT being promoted
- Flag high performers with low satisfaction or engagement

## How to Identify Retention Opportunities

- Find high performers (rating >= 4) with low satisfaction (< 3)
- Find high performers not promoted in 2+ years
- Find employees with high engagement but low satisfaction
- These are at-risk valuable employees worth targeted retention efforts

## How to Identify Overtime-Related Attrition

- Compare attrition rate of overtime vs non-overtime employees
- Calculate the attrition rate ratio (overtime / non-overtime)
- Identify departments with both high overtime and high attrition
- This confirms overtime as an attrition driver

## How to Identify Promotion-Related Attrition

- Compare attrition rate of promoted vs non-promoted employees
- Analyze employees with >3 years tenure and no promotion
- Cross-reference with performance rating
- This highlights career growth as a retention factor

## How to Identify Employee Engagement Issues

- Calculate average engagement score by department
- Flag departments with engagement < 3.0
- Compare engagement between attrition Yes vs No groups
- Low engagement often precedes attrition by 3-6 months
