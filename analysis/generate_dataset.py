import csv
import random
import math

random.seed(42)

# Configuration
NUM_EMPLOYEES = 148

# Names
first_names = ['James','Mary','John','Patricia','Robert','Jennifer','Michael','Linda','David','Elizabeth','William','Barbara','Richard','Susan','Joseph','Jessica','Thomas','Sarah','Christopher','Karen','Charles','Lisa','Daniel','Nancy','Matthew','Betty','Anthony','Margaret','Mark','Sandra','Donald','Ashley','Steven','Kimberly','Paul','Emily','Andrew','Donna','Joshua','Michelle','Kenneth','Carol','Kevin','Amanda','Brian','Dorothy','George','Melissa','Timothy','Deborah','Ronald','Stephanie','Edward','Rebecca','Jason','Sharon','Jeffrey','Laura','Ryan','Cynthia','Jacob','Kathleen','Gary','Amy','Nicholas','Angela','Eric','Shirley','Jonathan','Anna','Stephen','Brenda','Larry','Pamela','Justin','Emma','Scott','Nicole','Brandon','Helen','Benjamin','Samantha','Samuel','Katherine','Raymond','Christine','Gregory','Debra','Frank','Rachel','Alexander','Carolyn','Patrick','Janet','Jack','Catherine','Dennis','Maria','Jerry','Heather','Tyler','Diane']
last_names = ['Smith','Johnson','Williams','Brown','Jones','Garcia','Miller','Davis','Rodriguez','Martinez','Hernandez','Lopez','Gonzalez','Wilson','Anderson','Thomas','Taylor','Moore','Jackson','Martin','Lee','Perez','Thompson','White','Harris','Sanchez','Clark','Ramirez','Lewis','Robinson','Walker','Young','Allen','King','Wright','Scott','Torres','Nguyen','Hill','Flores','Green','Adams','Nelson','Baker','Hall','Rivera','Campbell','Mitchell','Carter','Roberts']

departments = ['Sales','Operations','IT','Marketing','Support','R&D','Finance','HR','Legal','Admin']
dept_weights = [20,15,13,12,11,10,8,6,3,2]

job_roles = {
    'Sales': ['Sales Executive','Sales Manager','Account Executive','Sales Representative'],
    'Operations': ['Operations Manager','Logistics Coordinator','Process Analyst','Operations Associate'],
    'IT': ['Software Engineer','IT Support Specialist','System Administrator','Data Analyst'],
    'Marketing': ['Marketing Manager','Digital Marketing Specialist','Content Writer','Brand Strategist'],
    'Support': ['Customer Support Rep','Support Manager','Technical Support','Client Success Manager'],
    'R&D': ['Research Scientist','Product Developer','R&D Engineer','Innovation Analyst'],
    'Finance': ['Financial Analyst','Accountant','Finance Manager','Auditor'],
    'HR': ['HR Coordinator','HR Manager','Recruiter','Training Specialist'],
    'Legal': ['Legal Counsel','Compliance Officer','Contract Specialist','Paralegal'],
    'Admin': ['Admin Assistant','Office Manager','Executive Assistant','Facilities Coordinator']
}

education_levels = ['Diploma', 'Bachelor\'s Degree', 'Master\'s Degree', 'PhD']
edu_weights = [15, 45, 30, 10]

marital_statuses = ['Single', 'Married', 'Divorced']
marital_weights = [40, 45, 15]

attrition_reasons = ['Career Growth', 'Compensation', 'Work-Life Balance', 'Management', 'Relocation', 'Health', 'Retirement', 'Other']
reason_weights = [30, 20, 18, 12, 8, 6, 4, 2]

employees = []
for i in range(1, NUM_EMPLOYEES + 1):
    emp_id = f'EMP{i:03d}'
    name = f'{random.choice(first_names)} {random.choice(last_names)}'
    age = random.randint(22, 65)
    gender = random.choices(['Male','Female','Other'], weights=[55,43,2])[0]
    department = random.choices(departments, weights=dept_weights)[0]
    role = random.choice(job_roles[department])
    edu = random.choices(education_levels, weights=edu_weights)[0]
    marital = random.choices(marital_statuses, weights=marital_weights)[0]
    years = max(0, min(25, round(random.expovariate(1/4))))
    base_income = random.randint(2500, 8000)
    role_mult = {'Sales Executive':1.0,'Sales Manager':1.8,'Account Executive':1.2,'Sales Representative':0.8,
                 'Operations Manager':1.5,'Logistics Coordinator':0.9,'Process Analyst':1.1,'Operations Associate':0.7,
                 'Software Engineer':1.6,'IT Support Specialist':0.9,'System Administrator':1.2,'Data Analyst':1.3,
                 'Marketing Manager':1.5,'Digital Marketing Specialist':1.0,'Content Writer':0.8,'Brand Strategist':1.2,
                 'Customer Support Rep':0.7,'Support Manager':1.3,'Technical Support':0.9,'Client Success Manager':1.1,
                 'Research Scientist':1.7,'Product Developer':1.5,'R&D Engineer':1.4,'Innovation Analyst':1.2,
                 'Financial Analyst':1.3,'Accountant':1.0,'Finance Manager':1.8,'Auditor':1.2,
                 'HR Coordinator':0.8,'HR Manager':1.5,'Recruiter':1.0,'Training Specialist':0.9,
                 'Legal Counsel':2.0,'Compliance Officer':1.3,'Contract Specialist':1.1,'Paralegal':0.9,
                 'Admin Assistant':0.7,'Office Manager':1.0,'Executive Assistant':0.9,'Facilities Coordinator':0.8}
    income = int(base_income * role_mult.get(role, 1.0) * (1 + years * 0.03))
    income = max(2500, min(20000, income))

    perf_weights = [5,15,40,30,10]
    perf = random.choices([1,2,3,4,5], weights=perf_weights)[0]

    # Correlated: higher performance -> slightly higher satisfaction
    sat_base = random.choices([1,2,3,4,5], weights=[10,15,30,30,15])[0]
    wlb_base = random.choices([1,2,3,4,5], weights=[15,20,30,25,10])[0]

    training = random.randint(0, 80)
    promotion = 'Yes' if random.random() < 0.15 else 'No'
    overtime = random.choices(['Yes','No'], weights=[35,65])[0]

    # Calculate attrition probability based on factors
    attrition_prob = 0.05  # base
    if overtime == 'Yes':
        attrition_prob += 0.20
    if sat_base <= 2:
        attrition_prob += 0.25
    elif sat_base == 3:
        attrition_prob += 0.10
    if wlb_base <= 2:
        attrition_prob += 0.10
    if promotion == 'No' and years > 3:
        attrition_prob += 0.15
    if age < 30:
        attrition_prob += 0.08
    if department == 'Sales':
        attrition_prob += 0.08
    elif department == 'Support':
        attrition_prob += 0.05
    if perf >= 4 and promotion == 'No' and years > 2:
        attrition_prob += 0.10  # high performer not promoted -> likely to leave

    attrition_prob = min(attrition_prob, 0.85)
    attrition = 'Yes' if random.random() < attrition_prob else 'No'

    reason = 'N/A' if attrition == 'No' else random.choices(attrition_reasons, weights=reason_weights)[0]

    mgr_rating = max(1, min(5, round(random.gauss(3.5, 0.8))))
    engagement = max(1, min(5, round(random.gauss(3.3, 0.9))))

    employees.append([emp_id, name, age, gender, department, role, edu, marital,
                      years, income, perf, sat_base, wlb_base, training,
                      promotion, overtime, attrition, reason, mgr_rating, engagement])

# Write CSV
with open('data/raw/employee_attrition_dataset.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['EmployeeID','EmployeeName','Age','Gender','Department','JobRole',
                     'EducationLevel','MaritalStatus','YearsAtCompany','MonthlyIncome',
                     'PerformanceRating','JobSatisfaction','WorkLifeBalance','TrainingHours',
                     'PromotionStatus','OvertimeStatus','AttritionStatus','AttritionReason',
                     'ManagerRating','EmployeeEngagementScore'])
    writer.writerows(employees)

print(f'Generated {NUM_EMPLOYEES} employee records')
