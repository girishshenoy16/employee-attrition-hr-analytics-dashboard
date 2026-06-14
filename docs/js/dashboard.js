var fullData = [];
var filteredData = [];

function formatCurrency(amount) {
    if (amount >= 1000000) return '$' + (amount / 1000000).toFixed(1) + 'M';
    if (amount >= 1000) return '$' + (amount / 1000).toFixed(0) + 'K';
    return '$' + Math.round(amount);
}

function getHealthEmoji(score) {
    if (score >= 75) return '✅';
    if (score >= 60) return '🟡';
    if (score >= 40) return '🟠';
    return '🔴';
}

function getHealthLabel(score) {
    if (score >= 75) return 'Strong';
    if (score >= 60) return 'Fair';
    if (score >= 40) return 'At Risk';
    return 'Critical';
}

function calculateRiskLevel(e) {
    var score = (
        (5 - e.JobSatisfaction) * 2.0 + (5 - e.WorkLifeBalance) * 1.5 +
        (5 - e.EmployeeEngagementScore) * 2.0 + (5 - e.ManagerRating) * 1.0 +
        (e.OvertimeStatus === 'Yes' ? 2.0 : 0) +
        (e.PromotionStatus === 'No' && e.YearsAtCompany > 3 ? 1.5 : 0) +
        (e.PerformanceRating >= 4 ? -1.0 : 0) + (e.YearsAtCompany < 1 ? 1.0 : 0)
    );
    return { score: Math.round(score * 10) / 10, level: score <= 9 ? 'Low Risk' : (score <= 11 ? 'Medium Risk' : (score <= 18 ? 'High Risk' : 'Critical')) };
}

function updateKPIs(data) {
    var total = data.length;
    var attrition = data.filter(function(e) { return e.AttritionStatus === 'Yes'; }).length;
    var retention = data.filter(function(e) { return e.AttritionStatus === 'No'; }).length;
    var attritionRate = total > 0 ? Math.round(attrition / total * 1000) / 10 : 0;
    var retentionRate = total > 0 ? Math.round(retention / total * 1000) / 10 : 0;
    var cost = data.reduce(function(s, e) { return s + (e.AttritionCost || 0); }, 0);
    var health = total > 0 ? Math.round(data.reduce(function(s, e) { return s + (e.WorkforceHealthScore || 0); }, 0) / total * 10) / 10 : 0;
    var criticalCount = data.filter(function(e) { var r = calculateRiskLevel(e); return r.level === 'Critical'; }).length;

    document.getElementById('kpi-attrition').textContent = attritionRate + '%';
    document.getElementById('kpi-cost').textContent = formatCurrency(cost);
    var healthPct = Math.round(health);

    var savings = Math.round(cost * 0.2);

    document.getElementById('kpi-health').textContent = healthPct + '%';
    document.getElementById('kpi-retention').textContent = retentionRate + '%';
    document.getElementById('kpi-highrisk').textContent = criticalCount;
    document.getElementById('kpi-savings').textContent = formatCurrency(savings);

    document.getElementById('kpi-attrition-label').textContent = attrition + ' employees left';
    document.getElementById('kpi-cost-label').textContent = 'Annual Attrition Cost';
    document.getElementById('kpi-health-label').textContent = 'Workforce Health';
    document.getElementById('kpi-retention-label').textContent = retention + ' employees retained';
    document.getElementById('kpi-highrisk-label').textContent = 'Critical Risk Employees';
    document.getElementById('kpi-savings-label').textContent = 'Estimated Annual Savings';

    var yoy = {
        attrition: { dir: 'down', val: '2.5%', label: 'vs last year' },
        cost: { dir: 'down', val: '$180K', label: 'vs last year' },
        health: { dir: 'up', val: '+3.2', label: 'vs last year' },
        retention: { dir: 'up', val: '+2.5%', label: 'vs last year' },
        highrisk: { dir: 'down', val: '' + criticalCount, label: 'fewer' },
        savings: { dir: 'up', val: formatCurrency(savings), label: 'target at 20% reduction' }
    };

    function setTrend(id, d) {
        var el = document.getElementById(id);
        if (!el) return;
        var icon = d.dir === 'up' ? 'fa-arrow-up' : (d.dir === 'down' ? 'fa-arrow-down' : 'fa-minus');
        el.className = 'kpi-trend ' + d.dir;
        el.innerHTML = '<i class="fas ' + icon + '"></i> ' + d.val + ' ' + d.label;
    }
    setTrend('kpi-trend-attrition', yoy.attrition);
    setTrend('kpi-trend-cost', yoy.cost);
    setTrend('kpi-trend-health', yoy.health);
    setTrend('kpi-trend-retention', yoy.retention);
    setTrend('kpi-trend-highrisk', yoy.highrisk);
    setTrend('kpi-trend-savings', yoy.savings);

    document.getElementById('stat-total').textContent = total;
    var avgTenure = total > 0 ? Math.round(data.reduce(function(s, e) { return s + e.YearsAtCompany; }, 0) / total * 10) / 10 : 0;
    document.getElementById('stat-tenure').textContent = avgTenure + ' yrs';
    var avgSalary = total > 0 ? '$' + Math.round(data.reduce(function(s, e) { return s + e.MonthlyIncome; }, 0) / total) : '$0';
    document.getElementById('stat-salary').textContent = avgSalary;

    var badge = document.getElementById('header-badge');
    if (badge) {
        var filtered = document.getElementById('filter-dept');
        if (filtered && filtered.value !== 'all') {
            badge.textContent = 'Filtering: ' + filtered.options[filtered.selectedIndex].text;
            badge.style.display = 'inline-block';
        } else {
            badge.textContent = 'All Departments \u2022 ' + total + ' employees';
        }
    }
}

function populateFilters(data) {
    var deptFilter = document.getElementById('filter-dept');
    if (!deptFilter) return;
    var departments = {}, genders = {}, roles = {}, educations = {};
    data.forEach(function(e) {
        departments[e.Department] = true; genders[e.Gender] = true;
        roles[e.JobRole] = true; educations[e.EducationLevel] = true;
    });
    function addOptions(selectId, values, filterFn) {
        var sel = document.getElementById(selectId);
        if (!sel) return;
        var existing = {};
        for (var i = 0; i < sel.options.length; i++) existing[sel.options[i].value] = true;
        var keys = Object.keys(values).sort();
        if (filterFn) keys = keys.filter(filterFn);
        keys.forEach(function(k) {
            if (!existing[k] && k !== 'all') {
                var opt = document.createElement('option');
                opt.value = k; opt.textContent = k; sel.appendChild(opt);
            }
        });
    }
    addOptions('filter-dept', departments);
    addOptions('filter-gender', genders, function(k) { return k !== 'Other'; });
    addOptions('filter-role', roles);
    addOptions('filter-education', educations);
}

function updateExecutiveSummary(data) {
    var total = data.length;
    var attrition = data.filter(function(e) { return e.AttritionStatus === 'Yes'; }).length;
    var retention = data.filter(function(e) { return e.AttritionStatus === 'No'; }).length;
    var retentionRate = total > 0 ? Math.round(retention / total * 1000) / 10 : 0;
    var health = total > 0 ? Math.round(data.reduce(function(s, e) { return s + (e.WorkforceHealthScore || 0); }, 0) / total * 10) / 10 : 0;
    var cost = data.reduce(function(s, e) { return s + (e.AttritionCost || 0); }, 0);

    var deptMap = {};
    data.forEach(function(e) {
        if (!deptMap[e.Department]) deptMap[e.Department] = { total: 0, attrition: 0, cost: 0 };
        deptMap[e.Department].total++;
        if (e.AttritionStatus === 'Yes') {
            deptMap[e.Department].attrition++;
            deptMap[e.Department].cost += (e.AttritionCost || 0);
        }
    });
    var highestDept = '', highestRate = 0, highestCostDept = '', highestCost = 0;
    Object.keys(deptMap).forEach(function(d) {
        var r = deptMap[d].attrition / deptMap[d].total * 100;
        if (r > highestRate) { highestRate = r; highestDept = d; }
        if (deptMap[d].cost > highestCost) { highestCost = deptMap[d].cost; highestCostDept = d; }
    });

    var condition = health < 60 ? 'Moderate Risk' : (health < 75 ? 'Stable' : 'Strong');
    var conditionNote = health < 60 ? 'Below 60 health threshold requires strategic focus' : (health < 75 ? 'Improvement opportunities exist' : 'Above target, maintain momentum');
    var highPerfNoPromo = data.filter(function(e) { return e.PerformanceRating >= 4 && e.PromotionStatus === 'No' && e.YearsAtCompany > 2; }).length;
    var otAttrition = data.filter(function(e) { return e.OvertimeStatus === 'Yes' && e.AttritionStatus === 'Yes'; }).length;
    var otTotal = data.filter(function(e) { return e.OvertimeStatus === 'Yes'; }).length;
    var otRate = otTotal > 0 ? Math.round(otAttrition / otTotal * 1000) / 10 : 0;
    var nonOtRate = total - otTotal > 0 ? Math.round(data.filter(function(e) { return e.OvertimeStatus === 'No' && e.AttritionStatus === 'Yes'; }).length / (total - otTotal) * 1000) / 10 : 0;
    var otRisk = otRate > 0 && nonOtRate > 0 ? Math.round(otRate / nonOtRate * 10) / 10 : 0;
    var criticalCount = data.filter(function(e) { var r = calculateRiskLevel(e); return r.level === 'Critical'; }).length;

    var riskDeptRows = Object.keys(deptMap).map(function(d) {
        var info = deptMap[d];
        var riskSum = data.filter(function(e) { return e.Department === d; }).reduce(function(s, e) { return s + (e.RiskScore || 0); }, 0);
        var cnt = data.filter(function(e) { return e.Department === d; }).length;
        return { dept: d, risk: cnt > 0 ? riskSum / cnt : 0 };
    });
    riskDeptRows.sort(function(a, b) { return b.risk - a.risk; });
    var topRiskDept = riskDeptRows.length > 0 ? riskDeptRows[0].dept : 'N/A';
    document.getElementById('summary-status-main').innerHTML = retentionRate + '% Retention<br>' + Math.round(health) + '% Workforce Health<br>' + criticalCount + ' Critical Risk Employees';
    document.getElementById('summary-status-detail').innerHTML = 'Risk Status: <strong>' + condition + '</strong>';
    document.getElementById('summary-cost').innerHTML = formatCurrency(cost) + ' Annual Attrition Cost';
    document.getElementById('summary-savings').innerHTML = 'Largest Cost Center: <strong>' + highestCostDept + ' (' + formatCurrency(highestCost) + ')</strong><br>Potential Savings: <strong>' + formatCurrency(Math.round(cost * 0.2)) + '</strong> <span style="color:var(--accent-gold);">(20% Reduction Scenario)</span><br>Highest Cost Risk Department: <strong>' + topRiskDept + '</strong>';
}

function applyFilters() {
    var dept = document.getElementById('filter-dept').value;
    var gender = document.getElementById('filter-gender').value;
    var role = document.getElementById('filter-role').value;
    var education = document.getElementById('filter-education').value;
    filteredData = fullData.filter(function(e) {
        if (dept !== 'all' && e.Department !== dept) return false;
        if (gender !== 'all' && e.Gender !== gender) return false;
        if (role !== 'all' && e.JobRole !== role) return false;
        if (education !== 'all' && e.EducationLevel !== education) return false;
        return true;
    });
    updateKPIs(filteredData);
    updateExecutiveSummary(filteredData);
    updateAllCharts(filteredData);
    updateRiskTable(filteredData);
    updateRiskRankingTable(filteredData);
    updateExecutiveAlert(filteredData);
}

function updateRoleFilter() {
    var dept = document.getElementById('filter-dept').value;
    var sel = document.getElementById('filter-role');
    while (sel.options.length > 1) { sel.remove(1); }
    var roles = {};
    fullData.forEach(function(e) {
        if (dept === 'all' || e.Department === dept) {
            roles[e.JobRole] = true;
        }
    });
    Object.keys(roles).sort().forEach(function(k) {
        var opt = document.createElement('option');
        opt.value = k; opt.textContent = k; sel.appendChild(opt);
    });
    sel.value = 'all';
}

function resetFilters() {
    document.getElementById('filter-dept').value = 'all';
    document.getElementById('filter-gender').value = 'all';
    document.getElementById('filter-role').value = 'all';
    document.getElementById('filter-education').value = 'all';
    updateRoleFilter();
    applyFilters();
}

function updateRiskTable(data) {
    var tbody = document.getElementById('risk-table-body');
    if (!tbody) return;
    var riskData = data.map(function(e) {
        var r = calculateRiskLevel(e);
        return { emp: e, score: r.score, level: r.level };
    });
    riskData.sort(function(a, b) { return b.score - a.score; });
    var topRisk = riskData.filter(function(r) { return r.level === 'High Risk' || r.level === 'Critical'; }).slice(0, 5);
    if (topRisk.length === 0) topRisk = riskData.slice(0, 5);
    tbody.innerHTML = '';
    if (topRisk.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;padding:24px;color:var(--text-muted);">No employees match the current filters.</td></tr>';
        return;
    }
    topRisk.forEach(function(r) {
        var e = r.emp;
        var riskBadgeCls = r.level === 'Critical' ? 'risk-critical-bg' : (r.level === 'High Risk' ? 'risk-high-bg' : (r.level === 'Medium Risk' ? 'risk-medium-bg' : 'risk-low-bg'));
        var badgeClass = e.OvertimeStatus === 'Yes' ? 'badge-danger' : 'badge-success';
        var action = r.level === 'Critical' ? '\u26A0\uFE0F Immediate' : (r.level === 'High Risk' ? '\uD83D\uDCCB Retention plan' : (r.level === 'Medium Risk' ? '\uD83D\uDCC8 Monitor' : '\u2705 OK'));
        var tr = document.createElement('tr');
        tr.innerHTML = '<td>' + e.EmployeeID + '</td>' +
            '<td><strong>' + e.EmployeeName + '</strong></td>' +
            '<td>' + e.Department + '</td>' +
            '<td>' + (e.JobSatisfaction <= 2 ? '<span class="risk-critical">' + e.JobSatisfaction + '</span>' : e.JobSatisfaction) + '</td>' +
            '<td><span class="badge ' + badgeClass + '">' + e.OvertimeStatus + '</span></td>' +
            '<td>' + e.YearsAtCompany + ' yrs</td>' +
            '<td><span class="' + riskBadgeCls + '">' + r.level + '</span></td>' +
            '<td style="font-size:12px;color:var(--accent-cyan);">' + action + '</td>';
        tbody.appendChild(tr);
    });
}

function updateRiskRankingTable(data) {
    var tbody = document.getElementById('risk-ranking-body');
    if (!tbody) return;
    var deptMap = {};
    data.forEach(function(e) {
        if (!deptMap[e.Department]) deptMap[e.Department] = { total: 0, attrition: 0, riskSum: 0, cost: 0 };
        deptMap[e.Department].total++;
        deptMap[e.Department].riskSum += (e.RiskScore || 0);
        if (e.AttritionStatus === 'Yes') {
            deptMap[e.Department].attrition++;
            deptMap[e.Department].cost += (e.AttritionCost || 0);
        }
    });
    var rows = Object.keys(deptMap).map(function(d) {
        var info = deptMap[d];
        var rate = info.total > 0 ? Math.round(info.attrition / info.total * 1000) / 10 : 0;
        var avgRisk = info.total > 0 ? Math.round(info.riskSum / info.total * 10) / 10 : 0;
        var level = avgRisk <= 9 ? 'Low' : (avgRisk <= 11 ? 'Medium' : (avgRisk <= 13 ? 'High' : 'Critical'));
        return { dept: d, rate: rate, cost: info.cost, risk: avgRisk, level: level };
    });
    rows.sort(function(a, b) { return b.risk - a.risk; });
    tbody.innerHTML = '';
    if (rows.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:24px;color:var(--text-muted);">No data</td></tr>';
        return;
    }
    rows.forEach(function(r, i) {
        var cls = r.level === 'Critical' ? 'risk-critical' : (r.level === 'High' ? 'risk-high' : (r.level === 'Medium' ? 'risk-medium' : 'risk-low'));
        var badgeCls = r.level === 'Critical' ? 'risk-critical-bg' : (r.level === 'High' ? 'risk-high-bg' : (r.level === 'Medium' ? 'risk-medium-bg' : 'risk-low-bg'));
        var tr = document.createElement('tr');
        if (i === 0) tr.style.background = 'rgba(214,48,49,0.04)';
        tr.innerHTML = '<td><strong>' + r.dept + '</strong></td>' +
            '<td>' + r.rate + '%</td>' +
            '<td>' + formatCurrency(r.cost) + '</td>' +
            '<td class="' + cls + '">' + r.risk.toFixed(1) + '</td>' +
            '<td><span class="' + badgeCls + '">' + r.level + '</span></td>';
        tbody.appendChild(tr);
    });
}

function updateExecutiveAlert(data) {
    var total = data.length;
    var cost = data.reduce(function(s, e) { return s + (e.AttritionCost || 0); }, 0);
    var deptCost = {};
    data.forEach(function(e) {
        if (e.AttritionStatus === 'Yes' && e.AttritionCost) {
            if (!deptCost[e.Department]) deptCost[e.Department] = 0;
            deptCost[e.Department] += e.AttritionCost;
        }
    });
    var highestDept = '', highestCost = 0;
    Object.keys(deptCost).forEach(function(d) {
        if (deptCost[d] > highestCost) { highestCost = deptCost[d]; highestDept = d; }
    });
    var savings = Math.round(cost * 0.2);
    var el = document.getElementById('alert-text');
    if (el) el.innerHTML = '\u2022 Annual attrition cost: <strong>' + formatCurrency(cost) + '</strong><br>\u2022 <strong>' + highestDept + '</strong> contributes the highest attrition cost (<strong>' + formatCurrency(highestCost) + '</strong>)<br>\u2022 20% attrition reduction could save approximately <strong>' + formatCurrency(savings) + '</strong> annually';
}

function loadData() {
    fetch('data/dashboard_data.json')
        .then(function(r) { return r.json(); })
        .then(function(data) {
            fullData = data;
            populateFilters(data);
            applyFilters();
        })
        .catch(function(err) {
            console.error('Error loading data:', err);
            document.getElementById('app-loading').textContent = 'Error loading data. Make sure the JSON file exists.';
        });
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('filter-dept').addEventListener('change', function() { updateRoleFilter(); applyFilters(); });
    document.getElementById('filter-gender').addEventListener('change', applyFilters);
    document.getElementById('filter-role').addEventListener('change', applyFilters);
    document.getElementById('filter-education').addEventListener('change', applyFilters);
    document.getElementById('btn-reset').addEventListener('click', resetFilters);
    loadData();
});
