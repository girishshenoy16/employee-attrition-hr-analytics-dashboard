import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

print("Generating EDA Visualizations...")
df = pd.read_csv('data/processed/processed_employee_data.csv')
os.makedirs('analysis/output/charts', exist_ok=True)

sns.set_style('darkgrid')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12
COLORS = ['#ff6b6b', '#00d2ff', '#6c5ce7', '#feca57', '#1dd1a1', '#54a0ff']

# 1. Attrition by Department
fig, ax = plt.subplots()
dept_order = df.groupby('Department')['AttritionStatus'].apply(lambda x: (x == "Yes").mean()).sort_values()
sns.barplot(x=dept_order.values*100, y=dept_order.index, palette='Reds_r', ax=ax)
ax.set_title('Attrition Rate by Department', fontsize=14, fontweight='bold')
ax.set_xlabel('Attrition Rate (%)')
ax.set_ylabel('Department')
for i, v in enumerate(dept_order.values*100):
    ax.text(v+0.5, i, f'{v:.1f}%', va='center', fontweight='bold')
plt.tight_layout()
plt.savefig('analysis/output/charts/attrition_by_dept.png', dpi=150, bbox_inches='tight')
plt.close()
print("   [1/10] Attrition by Department")

# 2. Attrition by Age Band
fig, ax = plt.subplots()
age_order = ['<25', '25-29', '30-39', '40-49', '50-59', '60+']
age_data = df.groupby('AgeBand', observed=False)['AttritionStatus'].apply(lambda x: (x == "Yes").mean()*100).reindex(age_order)
bars = ax.bar(age_order, age_data.values, color=COLORS[0], alpha=0.8, edgecolor='white', linewidth=1.5)
ax.set_title('Attrition Rate by Age Group', fontsize=14, fontweight='bold')
ax.set_xlabel('Age Group')
ax.set_ylabel('Attrition Rate (%)')
for bar, v in zip(bars, age_data.values):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5, f'{v:.1f}%', ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig('analysis/output/charts/attrition_by_age.png', dpi=150, bbox_inches='tight')
plt.close()
print("   [2/10] Attrition by Age Band")

# 3. Attrition by Overtime
fig, ax = plt.subplots()
ot_data = df.groupby('OvertimeStatus')['AttritionStatus'].apply(lambda x: (x == "Yes").mean()*100)
bars = ax.bar(ot_data.index, ot_data.values, color=[COLORS[2], COLORS[1]], alpha=0.85, edgecolor='white', linewidth=1.5)
ax.set_title('Attrition Rate by Overtime Status', fontsize=14, fontweight='bold')
ax.set_xlabel('Overtime Status')
ax.set_ylabel('Attrition Rate (%)')
for bar, v in zip(bars, ot_data.values):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5, f'{v:.1f}%', ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig('analysis/output/charts/attrition_by_overtime.png', dpi=150, bbox_inches='tight')
plt.close()
print("   [3/10] Attrition by Overtime")

# 4. Satisfaction Distribution
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.histplot(df['JobSatisfaction'], bins=5, discrete=True, kde=True, color=COLORS[1], ax=axes[0])
axes[0].set_title('Job Satisfaction Distribution', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Satisfaction Score')
axes[0].set_ylabel('Count')
sns.histplot(df['WorkLifeBalance'], bins=5, discrete=True, kde=True, color=COLORS[2], ax=axes[1])
axes[1].set_title('Work-Life Balance Distribution', fontsize=14, fontweight='bold')
axes[1].set_xlabel('WLB Score')
axes[1].set_ylabel('Count')
plt.tight_layout()
plt.savefig('analysis/output/charts/satisfaction_dist.png', dpi=150, bbox_inches='tight')
plt.close()
print("   [4/10] Satisfaction Distribution")

# 5. Correlation Heatmap
fig, ax = plt.subplots(figsize=(10, 8))
corr_cols = ['Age','YearsAtCompany','MonthlyIncome','PerformanceRating','JobSatisfaction',
             'WorkLifeBalance','TrainingHours','ManagerRating','EmployeeEngagementScore']
df['AttritionBinary'] = (df['AttritionStatus'] == 'Yes').astype(int)
corr_matrix = df[corr_cols + ['AttritionBinary']].corr()
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
            square=True, linewidths=0.5, ax=ax, cbar_kws={'shrink': 0.8})
ax.set_title('Correlation Heatmap', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('analysis/output/charts/correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print("   [5/10] Correlation Heatmap")

# 6. Salary Distribution by Dept
fig, ax = plt.subplots()
dept_order_sal = df.groupby('Department')['MonthlyIncome'].median().sort_values().index
sns.boxplot(x='Department', y='MonthlyIncome', data=df, order=dept_order_sal, palette='viridis', ax=ax)
ax.set_title('Salary Distribution by Department', fontsize=14, fontweight='bold')
ax.set_xlabel('Department')
ax.set_ylabel('Monthly Income ($)')
ax.tick_params(axis='x', rotation=45)
plt.tight_layout()
plt.savefig('analysis/output/charts/salary_by_dept.png', dpi=150, bbox_inches='tight')
plt.close()
print("   [6/10] Salary by Department")

# 7. Engagement vs Attrition
fig, ax = plt.subplots()
sns.violinplot(x='AttritionStatus', y='EmployeeEngagementScore', data=df, palette=['#1dd1a1', '#ff6b6b'], ax=ax)
ax.set_title('Engagement Score by Attrition Status', fontsize=14, fontweight='bold')
ax.set_xlabel('Attrition Status')
ax.set_ylabel('Engagement Score')
plt.tight_layout()
plt.savefig('analysis/output/charts/engagement_vs_attrition.png', dpi=150, bbox_inches='tight')
plt.close()
print("   [7/10] Engagement vs Attrition")

# 8. Promotion vs Attrition
fig, ax = plt.subplots()
promo_data = df.groupby('PromotionStatus')['AttritionStatus'].apply(lambda x: (x == "Yes").mean()*100)
bars = ax.bar(promo_data.index, promo_data.values, color=[COLORS[1], COLORS[4]], alpha=0.85, edgecolor='white', linewidth=1.5)
ax.set_title('Attrition Rate by Promotion Status', fontsize=14, fontweight='bold')
ax.set_xlabel('Promotion Status')
ax.set_ylabel('Attrition Rate (%)')
for bar, v in zip(bars, promo_data.values):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5, f'{v:.1f}%', ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig('analysis/output/charts/promotion_vs_attrition.png', dpi=150, bbox_inches='tight')
plt.close()
print("   [8/10] Promotion vs Attrition")

# 9. Tenure Distribution
fig, ax = plt.subplots()
sns.histplot(df['YearsAtCompany'], bins=15, kde=True, color=COLORS[3], edgecolor='white', ax=ax)
ax.set_title('Employee Tenure Distribution', fontsize=14, fontweight='bold')
ax.set_xlabel('Years at Company')
ax.set_ylabel('Count')
plt.tight_layout()
plt.savefig('analysis/output/charts/tenure_distribution.png', dpi=150, bbox_inches='tight')
plt.close()
print("   [9/10] Tenure Distribution")

# 10. Age Distribution
fig, ax = plt.subplots()
sns.histplot(df['Age'], bins=15, kde=True, color=COLORS[5], edgecolor='white', ax=ax)
ax.set_title('Employee Age Distribution', fontsize=14, fontweight='bold')
ax.set_xlabel('Age')
ax.set_ylabel('Count')
plt.tight_layout()
plt.savefig('analysis/output/charts/age_distribution.png', dpi=150, bbox_inches='tight')
plt.close()
print("   [10/10] Age Distribution")

print("\nAll 10 charts saved to analysis/output/charts/")
