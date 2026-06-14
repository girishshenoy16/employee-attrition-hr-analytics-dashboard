import pandas as pd
import numpy as np
import json
import os
from datetime import datetime

print("=" * 60)
print("WORKFORCE INTELLIGENCE DATA PIPELINE")
print("=" * 60)

np.random.seed(42)

# ============================================================
# 1. LOAD DATA
# ============================================================
print("\n[1/8] Loading data...")
df = pd.read_csv('data/raw/employee_attrition_dataset.csv')
print(f"   Loaded {len(df)} records with {len(df.columns)} columns")

# ============================================================
# 2. DATA CLEANING
# ============================================================
print("\n[2/8] Cleaning data...")
print(f"   Missing values:\n{df.isnull().sum()[df.isnull().sum() > 0].to_string()}")
df_clean = df.copy()
df_clean['AttritionReason'] = df_clean['AttritionReason'].fillna('N/A')
df_clean['TrainingHours'] = df_clean['TrainingHours'].fillna(0)
os.makedirs('data/processed', exist_ok=True)

# ============================================================
# 3. DERIVED FEATURES
# ============================================================
print("\n[3/8] Creating derived features...")
df_clean['AgeBand'] = pd.cut(df_clean['Age'], bins=[0, 25, 30, 40, 50, 60, 100],
                              labels=['<25', '25-29', '30-39', '40-49', '50-59', '60+'])
df_clean['TenureBand'] = pd.cut(df_clean['YearsAtCompany'], bins=[-1, 1, 3, 5, 10, 15, 100],
                                 labels=['<1yr', '1-3yrs', '3-5yrs', '5-10yrs', '10-15yrs', '15+ yrs'])
df_clean['SatisfactionGroup'] = pd.cut(df_clean['JobSatisfaction'], bins=[0, 2, 3, 5],
                                        labels=['Low (1-2)', 'Medium (3)', 'High (4-5)'])
df_clean['EngagementGroup'] = pd.cut(df_clean['EmployeeEngagementScore'], bins=[0, 2, 3, 5],
                                      labels=['Low (1-2)', 'Medium (3)', 'High (4-5)'])

# Risk Score
df_clean['RiskScore'] = (
    (5 - df_clean['JobSatisfaction']) * 2.0 +
    (5 - df_clean['WorkLifeBalance']) * 1.5 +
    (5 - df_clean['EmployeeEngagementScore']) * 2.0 +
    (5 - df_clean['ManagerRating']) * 1.0 +
    (df_clean['OvertimeStatus'] == 'Yes') * 2.0 +
    ((df_clean['PromotionStatus'] == 'No') & (df_clean['YearsAtCompany'] > 3)) * 1.5 +
    (df_clean['PerformanceRating'] >= 4) * -1.0 +
    (df_clean['YearsAtCompany'] < 1) * 1.0
)
df_clean['RiskLevel'] = pd.cut(df_clean['RiskScore'], bins=[-10, 4, 7, 10, 100],
                                labels=['Low Risk', 'Medium Risk', 'High Risk', 'Critical'])

# Departure Month (for monthly trend analysis)
df_clean['DepartureMonth'] = np.where(
    df_clean['AttritionStatus'] == 'Yes',
    np.random.randint(1, 13, size=len(df_clean)),
    0
)

# Attrition Cost (annual cost = 100% of annual salary as replacement cost)
df_clean['AttritionCost'] = np.where(
    df_clean['AttritionStatus'] == 'Yes',
    df_clean['MonthlyIncome'] * 12 * 1.0,
    0
)

# Workforce Health Score components (0-100 scale)
# Health = weighted composite of positive indicators
sat_norm = (df_clean['JobSatisfaction'] - 1) / 4 * 100  # normalize 1-5 to 0-100
eng_norm = (df_clean['EmployeeEngagementScore'] - 1) / 4 * 100
wlb_norm = (df_clean['WorkLifeBalance'] - 1) / 4 * 100
mgr_norm = (df_clean['ManagerRating'] - 1) / 4 * 100
perf_norm = (df_clean['PerformanceRating'] - 1) / 4 * 100
no_overtime = (df_clean['OvertimeStatus'] == 'No').astype(int) * 100
promoted = (df_clean['PromotionStatus'] == 'Yes').astype(int) * 100

df_clean['WorkforceHealthScore'] = (
    sat_norm * 0.25 +
    eng_norm * 0.20 +
    wlb_norm * 0.15 +
    mgr_norm * 0.15 +
    perf_norm * 0.10 +
    no_overtime * 0.10 +
    promoted * 0.05
).round(1)

print(f"   Derived: AgeBand, TenureBand, SatisfactionGroup, EngagementGroup, RiskScore, RiskLevel, DepartureMonth, AttritionCost, WorkforceHealthScore")

# ============================================================
# 4. DESCRIPTIVE STATISTICS
# ============================================================
print("\n[4/8] Computing descriptive statistics...")
numeric_cols = ['Age','YearsAtCompany','MonthlyIncome','PerformanceRating',
                'JobSatisfaction','WorkLifeBalance','TrainingHours',
                'ManagerRating','EmployeeEngagementScore','RiskScore']
desc_stats = df_clean[numeric_cols].describe().round(2)
os.makedirs('analysis/output', exist_ok=True)
desc_stats.to_csv('analysis/output/descriptive_stats.csv')
print(desc_stats)

# ============================================================
# 5. ATTRITION ANALYSIS
# ============================================================
print("\n[5/8] Running attrition analysis...")
total = len(df_clean)
attrition_count = len(df_clean[df_clean['AttritionStatus'] == 'Yes'])
retention_count = len(df_clean[df_clean['AttritionStatus'] == 'No'])
attrition_rate = round(attrition_count / total * 100, 1)
retention_rate = round(retention_count / total * 100, 1)
print(f"   Attrition Rate: {attrition_rate}% ({attrition_count} employees)")
print(f"   Retention Rate: {retention_rate}% ({retention_count} employees)")

# By Department
dept_attrition = df_clean.groupby('Department').agg(
    Total=('EmployeeID', 'count'),
    Attrition=('AttritionStatus', lambda x: (x == 'Yes').sum())
).reset_index()
dept_attrition['AttritionRate'] = round(dept_attrition['Attrition'] / dept_attrition['Total'] * 100, 1)
dept_attrition = dept_attrition.sort_values('AttritionRate', ascending=False)
dept_attrition.to_csv('analysis/output/attrition_summary.csv', index=False)
print(f"\n   Attrition by Department:\n{dept_attrition.to_string(index=False)}")

# By Gender
gender_attrition = df_clean.groupby('Gender').agg(
    Total=('EmployeeID', 'count'),
    Attrition=('AttritionStatus', lambda x: (x == 'Yes').sum())
).reset_index()
gender_attrition['AttritionRate'] = round(gender_attrition['Attrition'] / gender_attrition['Total'] * 100, 1)
print(f"\n   Attrition by Gender:\n{gender_attrition.to_string(index=False)}")

# By Age Band
age_attrition = df_clean.groupby('AgeBand', observed=False).agg(
    Total=('EmployeeID', 'count'),
    Attrition=('AttritionStatus', lambda x: (x == 'Yes').sum())
).reset_index()
age_attrition['AttritionRate'] = round(age_attrition['Attrition'] / age_attrition['Total'] * 100, 1)
print(f"\n   Attrition by Age Band:\n{age_attrition.to_string(index=False)}")

# By Overtime
overtime_attrition = df_clean.groupby('OvertimeStatus').agg(
    Total=('EmployeeID', 'count'),
    Attrition=('AttritionStatus', lambda x: (x == 'Yes').sum())
).reset_index()
overtime_attrition['AttritionRate'] = round(overtime_attrition['Attrition'] / overtime_attrition['Total'] * 100, 1)
overtime_attrition.to_csv('analysis/output/overtime_attrition.csv', index=False)
print(f"\n   Attrition by Overtime:\n{overtime_attrition.to_string(index=False)}")

# By Promotion
promo_attrition = df_clean.groupby('PromotionStatus').agg(
    Total=('EmployeeID', 'count'),
    Attrition=('AttritionStatus', lambda x: (x == 'Yes').sum())
).reset_index()
promo_attrition['AttritionRate'] = round(promo_attrition['Attrition'] / promo_attrition['Total'] * 100, 1)
promo_attrition.to_csv('analysis/output/promotion_attrition.csv', index=False)
print(f"\n   Attrition by Promotion:\n{promo_attrition.to_string(index=False)}")

# By Marital Status
marital_attrition = df_clean.groupby('MaritalStatus').agg(
    Total=('EmployeeID', 'count'),
    Attrition=('AttritionStatus', lambda x: (x == 'Yes').sum())
).reset_index()
marital_attrition['AttritionRate'] = round(marital_attrition['Attrition'] / marital_attrition['Total'] * 100, 1)
print(f"\n   Attrition by Marital Status:\n{marital_attrition.to_string(index=False)}")

# Attrition Reasons
reason_counts = df_clean[df_clean['AttritionStatus'] == 'Yes']['AttritionReason'].value_counts().reset_index()
reason_counts.columns = ['AttritionReason', 'Count']
reason_counts['Percentage'] = round(reason_counts['Count'] / attrition_count * 100, 1)
print(f"\n   Attrition Reasons:\n{reason_counts.to_string(index=False)}")

# ============================================================
# 6. DEPARTMENT ANALYSIS
# ============================================================
print("\n[6/8] Running department analysis...")
dept_stats = df_clean.groupby('Department').agg(
    Headcount=('EmployeeID', 'count'),
    AvgSalary=('MonthlyIncome', 'mean'),
    AvgTenure=('YearsAtCompany', 'mean'),
    AvgSatisfaction=('JobSatisfaction', 'mean'),
    AvgEngagement=('EmployeeEngagementScore', 'mean'),
    AvgPerformance=('PerformanceRating', 'mean'),
    OvertimePct=('OvertimeStatus', lambda x: (x == 'Yes').mean() * 100),
    PromotionPct=('PromotionStatus', lambda x: (x == 'Yes').mean() * 100)
).reset_index().round(2)
dept_stats = dept_stats.sort_values('Headcount', ascending=False)
dept_stats.to_csv('analysis/output/department_analysis.csv', index=False)
print(dept_stats.to_string(index=False))

# ============================================================
# 7. SATISFACTION & ENGAGEMENT ANALYSIS
# ============================================================
print("\n[7/8] Running satisfaction & engagement analysis...")
sat_analysis = df_clean.groupby('Department').agg(
    AvgJobSat=('JobSatisfaction', 'mean'),
    AvgWLB=('WorkLifeBalance', 'mean'),
    AvgEngagement=('EmployeeEngagementScore', 'mean'),
    AvgManagerRating=('ManagerRating', 'mean')
).reset_index().round(2)
sat_analysis.to_csv('analysis/output/satisfaction_analysis.csv', index=False)
print(sat_analysis.to_string(index=False))

# Correlation matrix
corr_cols = ['Age','YearsAtCompany','MonthlyIncome','PerformanceRating',
             'JobSatisfaction','WorkLifeBalance','TrainingHours',
             'ManagerRating','EmployeeEngagementScore','RiskScore']
df_corr = df_clean[corr_cols].copy()
df_corr['AttritionBinary'] = (df_clean['AttritionStatus'] == 'Yes').astype(int)
corr_matrix = df_corr.corr().round(3)
corr_matrix.to_csv('analysis/output/correlation_analysis.csv')
print(f"\n   Correlation with Attrition:")
attrition_corr = corr_matrix['AttritionBinary'].sort_values(key=abs, ascending=False)
print(attrition_corr.to_string())

# ============================================================
# 8. MONTHLY ATTRITION TREND & FORECAST
# ============================================================
print("\n[8/9] Computing monthly trends & forecasts...")
monthly_trend = df_clean[df_clean['DepartureMonth'] > 0].groupby('DepartureMonth').size().reset_index(name='Attrition')
monthly_trend.columns = ['Month', 'Attrition']
all_months = pd.DataFrame({'Month': range(1, 13)})
monthly_trend = all_months.merge(monthly_trend, on='Month', how='left').fillna(0)
monthly_trend['Attrition'] = monthly_trend['Attrition'].astype(int)
monthly_trend['CumulativeAttrition'] = monthly_trend['Attrition'].cumsum()

# Simple forecast (next 3 months using moving average)
recent_avg = monthly_trend['Attrition'].tail(6).mean()
forecast_months = pd.DataFrame({'Month': [13, 14, 15], 'Attrition': [round(recent_avg)] * 3})
forecast_months['CumulativeAttrition'] = (
    monthly_trend['CumulativeAttrition'].iloc[-1] + forecast_months['Attrition'].cumsum()
)
monthly_trend['Type'] = 'Actual'
forecast_months['Type'] = 'Forecast'
trend_data = pd.concat([monthly_trend, forecast_months], ignore_index=True)
trend_data.to_csv('analysis/output/monthly_trend.csv', index=False)
print(f"   Monthly trend: {trend_data.to_string(index=False)}")

# ============================================================
# 9. ATTRITION COST & FINANCIAL IMPACT
# ============================================================
print("\n[9/9] Computing financial impact & health metrics...")
total_attrition_cost = float(df_clean['AttritionCost'].sum())
avg_annual_salary = float(df_clean['MonthlyIncome'].mean() * 12)
potential_savings = round(total_attrition_cost * 0.20)  # 20% reducible with right programs

# Department Risk Matrix data
dept_risk_matrix = df_clean.groupby('Department').agg(
    Headcount=('EmployeeID', 'count'),
    AttritionRate=('AttritionStatus', lambda x: (x == 'Yes').mean() * 100),
    AvgRiskScore=('RiskScore', 'mean'),
    AvgSatisfaction=('JobSatisfaction', 'mean'),
    AvgEngagement=('EmployeeEngagementScore', 'mean'),
    OvertimeRate=('OvertimeStatus', lambda x: (x == 'Yes').mean() * 100),
    AvgSalary=('MonthlyIncome', 'mean'),
    AttritionCost=('AttritionCost', 'sum')
).reset_index().round(1)
dept_risk_matrix['AttritionCost'] = dept_risk_matrix['AttritionCost'].astype(int)
dept_risk_matrix = dept_risk_matrix.sort_values('AttritionRate', ascending=False)
dept_risk_matrix.to_csv('analysis/output/dept_risk_matrix.csv', index=False)
print(f"   Department Risk Matrix:\n{dept_risk_matrix.to_string(index=False)}")

# Company Health Score
company_health = round(float(df_clean['WorkforceHealthScore'].mean()), 1)
print(f"   Workforce Health Score: {company_health}/100")

print(f"   Total Attrition Cost: ${total_attrition_cost:,.0f}")
print(f"   Potential Savings: ${potential_savings:,.0f}")

# ============================================================
# 10. EXPORT PROCESSED DATA
# ============================================================
print("\n[10/10] Exporting processed data...")
export_cols = ['EmployeeID','EmployeeName','Age','Gender','Department','JobRole',
               'EducationLevel','MaritalStatus','YearsAtCompany','MonthlyIncome',
               'PerformanceRating','JobSatisfaction','WorkLifeBalance','TrainingHours',
               'PromotionStatus','OvertimeStatus','AttritionStatus','AttritionReason',
               'ManagerRating','EmployeeEngagementScore','AgeBand','TenureBand',
               'SatisfactionGroup','EngagementGroup','RiskScore','RiskLevel',
               'DepartureMonth','AttritionCost','WorkforceHealthScore']
df_export = df_clean[export_cols]
df_export.to_csv('data/processed/processed_employee_data.csv', index=False)

# Export JSON for dashboard
dashboard_data = df_export.to_dict(orient='records')
with open('data/processed/dashboard_data.json', 'w') as f:
    json.dump(dashboard_data, f, indent=2)

# Export high risk employees
high_risk = df_clean[df_clean['RiskLevel'].isin(['High Risk', 'Critical'])][
    ['EmployeeID','EmployeeName','Department','JobRole','JobSatisfaction',
     'EmployeeEngagementScore','OvertimeStatus','PromotionStatus','YearsAtCompany',
     'PerformanceRating','RiskScore','RiskLevel']
].sort_values('RiskScore', ascending=False)
high_risk.to_csv('analysis/output/high_risk_employees.csv', index=False)
print(f"   High Risk Employees: {len(high_risk)}")
print(f"   Data exported to data/processed/")

# Save KPIs to JSON
kpi_data = {
    'totalEmployees': total,
    'attritionCount': int(attrition_count),
    'retentionCount': int(retention_count),
    'attritionRate': attrition_rate,
    'retentionRate': retention_rate,
    'avgSatisfaction': round(float(df_clean['JobSatisfaction'].mean()), 1),
    'avgEngagement': round(float(df_clean['EmployeeEngagementScore'].mean()), 1),
    'avgTenure': round(float(df_clean['YearsAtCompany'].mean()), 1),
    'avgSalary': round(float(df_clean['MonthlyIncome'].mean())),
    'promotionRate': round(float((df_clean['PromotionStatus'] == 'Yes').mean() * 100), 1),
    'overtimeRate': round(float((df_clean['OvertimeStatus'] == 'Yes').mean() * 100), 1),
    'avgPerformance': round(float(df_clean['PerformanceRating'].mean()), 1),
    'avgWorkLifeBalance': round(float(df_clean['WorkLifeBalance'].mean()), 1),
    'avgManagerRating': round(float(df_clean['ManagerRating'].mean()), 1),
    'totalAttritionCost': int(total_attrition_cost),
    'potentialSavings': int(potential_savings),
    'companyHealthScore': company_health,
    'avgAnnualSalary': int(avg_annual_salary)
}
with open('data/processed/kpi_summary.json', 'w') as f:
    json.dump(kpi_data, f, indent=2)

print("\n" + "=" * 60)
print("WORKFORCE INTELLIGENCE COMPLETE")
print("=" * 60)
print(f"\nSummary:")
print(f"  Total Employees:      {total}")
print(f"  Attrition Rate:       {attrition_rate}%")
print(f"  Retention Rate:       {retention_rate}%")
print(f"  Avg Satisfaction:     {kpi_data['avgSatisfaction']}/5")
print(f"  Avg Engagement:       {kpi_data['avgEngagement']}/5")
print(f"  Avg Salary:           ${kpi_data['avgSalary']}")
print(f"  Workforce Health:     {company_health}/100")
print(f"  Attrition Cost:       ${total_attrition_cost:,.0f}")
print(f"  Potential Savings:    ${potential_savings:,.0f}")
print(f"  High Risk Employees:  {len(high_risk)}")
