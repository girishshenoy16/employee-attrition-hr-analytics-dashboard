const chartColors = {
    cyan: '#00d2ff', purple: '#6c5ce7', rose: '#ff6b6b', gold: '#feca57',
    teal: '#1dd1a1', blue: '#54a0ff', pink: '#fd79a8', orange: '#ff9f43'
};
const deptColors = {
    Sales: '#ff6b6b', Support: '#54a0ff', IT: '#00d2ff', Operations: '#ff9f43',
    Marketing: '#fd79a8', 'R&D': '#6c5ce7', HR: '#1dd1a1', Finance: '#feca57',
    Legal: '#a29bfe', Admin: '#00b894'
};
const chartDefaults = {
    color: '#4a4a6a',
    font: { family: "'Inter','Segoe UI',sans-serif" },
    plugins: {
        legend: { labels: { color: '#4a4a6a', font: { size: 13 }, boxWidth: 14, padding: 14 } }
    },
    scales: {
        x: { ticks: { color: '#888', font: { size: 12 } }, grid: { color: 'rgba(0,0,0,0.05)' } },
        y: { ticks: { color: '#888', font: { size: 12 } }, grid: { color: 'rgba(0,0,0,0.05)' } }
    }
};
Chart.defaults.color = chartDefaults.color;
Chart.defaults.font.family = chartDefaults.font.family;

let charts = {};

function createAttritionCostBreakdown(data) {
    var ctx = document.getElementById('chart-attrition-donut');
    if (!ctx) return;
    if (charts.attritionCostBreakdown) charts.attritionCostBreakdown.destroy();
    var deptCost = {};
    data.forEach(function(e) {
        if (e.AttritionStatus === 'Yes' && e.AttritionCost) {
            if (!deptCost[e.Department]) deptCost[e.Department] = 0;
            deptCost[e.Department] += e.AttritionCost;
        }
    });
    var labels = Object.keys(deptCost).sort(function(a, b) { return deptCost[b] - deptCost[a]; });
    var values = labels.map(function(l) { return Math.round(deptCost[l]); });
    var totalCost = values.reduce(function(s, v) { return s + v; }, 0);
    var colors = labels.map(function(l) { return deptColors[l] || chartColors.purple; });
    var labelPlugin = {
        id: 'costLabels',
        afterDraw: function(chart) {
            var ctx = chart.ctx;
            chart.data.datasets.forEach(function(ds, i) {
                var meta = chart.getDatasetMeta(i);
                meta.data.forEach(function(bar, j) {
                    var v = ds.data[j];
                    var label = typeof formatCurrency !== 'undefined' ? formatCurrency(v) : '$' + v.toLocaleString();
                    ctx.fillStyle = j === 0 ? '#d63031' : '#1a1a2e';
                    ctx.font = j === 0 ? 'bold 15px Inter, sans-serif' : 'bold 14px Inter, sans-serif';
                    ctx.textAlign = 'right';
                    ctx.textBaseline = 'middle';
                    ctx.fillText(label, bar.x - 8, bar.y);
                });
            });
        }
    };
    charts.attritionCostBreakdown = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Attrition Cost', data: values,
                backgroundColor: colors, borderColor: 'rgba(255,255,255,0.2)',
                borderWidth: 1, borderRadius: 4, barThickness: 38
            }]
        },
        options: {
            indexAxis: 'y', responsive: true, maintainAspectRatio: true,
            layout: { padding: { left: 12 } },
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(ctx) {
                            var v = ctx.parsed.x, p = totalCost > 0 ? Math.round(v / totalCost * 1000) / 10 : 0;
                            return (typeof formatCurrency !== 'undefined' ? formatCurrency(v) : '$' + v.toLocaleString()) + ' (' + p + '%)';
                        }
                    }
                }
            },
            scales: {
                x: { ticks: { font: { size: 14 }, callback: function(v) { return ''; } }, grid: { color: 'rgba(0,0,0,0.03)' } },
                y: { ticks: { font: { size: 14 }, padding: 12 }, grid: { display: false } }
            }
        },
        plugins: [labelPlugin]
    });
}

function createDeptAttrition(data) {
    var ctx = document.getElementById('chart-dept-attrition');
    if (!ctx) return;
    if (charts.deptAttrition) charts.deptAttrition.destroy();
    var deptMap = {};
    data.forEach(function(e) {
        if (!deptMap[e.Department]) deptMap[e.Department] = { total: 0, attrition: 0 };
        deptMap[e.Department].total++;
        if (e.AttritionStatus === 'Yes') deptMap[e.Department].attrition++;
    });
    var labels = Object.keys(deptMap).sort(function(a,b) {
        return (deptMap[a].attrition/deptMap[a].total) - (deptMap[b].attrition/deptMap[b].total);
    });
    var rates = labels.map(function(l) { return Math.round(deptMap[l].attrition / deptMap[l].total * 100); });
    var colors = rates.map(function(r) {
        if (r >= 30) return '#ff6b6b'; if (r >= 20) return '#ff9f43'; if (r >= 10) return '#feca57'; return '#1dd1a1';
    });
    var deptLabelPlugin = {
        id: 'deptLabels',
        afterDraw: function(chart) {
            var ctx = chart.ctx;
            chart.data.datasets.forEach(function(ds, i) {
                var meta = chart.getDatasetMeta(i);
                meta.data.forEach(function(bar, j) {
                    var v = ds.data[j];
                    if (v === 0) return;
                    ctx.fillStyle = '#1a1a2e';
                    ctx.font = 'bold 14px Inter, sans-serif';
                    ctx.textAlign = 'left';
                    ctx.textBaseline = 'middle';
                    ctx.fillText(v + '%', bar.x + 8, bar.y);
                });
            });
        }
    };
    charts.deptAttrition = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Attrition Rate (%)', data: rates,
                backgroundColor: colors, borderColor: 'rgba(255,255,255,0.2)', borderWidth: 1, borderRadius: 4, barThickness: 32
            }]
        },
        options: {
            indexAxis: 'y', responsive: true, maintainAspectRatio: true,
            layout: { padding: { left: 16 } },
            plugins: { legend: { display: false } },
            scales: {
                x: { ticks: { font: { size: 14 }, callback: function(v) { return ''; } }, grid: { color: 'rgba(0,0,0,0.03)' } },
                y: { ticks: { font: { size: 15 }, padding: 16 }, grid: { display: false } }
            }
        },
        plugins: [deptLabelPlugin]
    });
}

function createOvertimeAttrition(data) {
    var ctx = document.getElementById('chart-overtime');
    if (!ctx) return;
    if (charts.overtime) charts.overtime.destroy();
    var otYes = data.filter(function(e) { return e.OvertimeStatus === 'Yes'; });
    var otNo = data.filter(function(e) { return e.OvertimeStatus === 'No'; });
    charts.overtime = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['No Overtime', 'Overtime'],
            datasets: [
                { label: 'Stayed', data: [otNo.filter(function(e) { return e.AttritionStatus === 'No'; }).length, otYes.filter(function(e) { return e.AttritionStatus === 'No'; }).length], backgroundColor: chartColors.teal },
                { label: 'Left', data: [otNo.filter(function(e) { return e.AttritionStatus === 'Yes'; }).length, otYes.filter(function(e) { return e.AttritionStatus === 'Yes'; }).length], backgroundColor: chartColors.rose }
            ]
        },
        options: {
            responsive: true, maintainAspectRatio: true,
            scales: {
                x: { stacked: true, ticks: { font: { size: 13 } } },
                y: { stacked: true, beginAtZero: true, ticks: { stepSize: 1, font: { size: 13 } } }
            },
            plugins: { legend: { position: 'bottom', labels: { font: { size: 13 } } } }
        }
    });
}

function createPromotionAttrition(data) {
    var ctx = document.getElementById('chart-promotion');
    if (!ctx) return;
    if (charts.promotion) charts.promotion.destroy();
    var promYes = data.filter(function(e) { return e.PromotionStatus === 'Yes'; });
    var promNo = data.filter(function(e) { return e.PromotionStatus === 'No'; });
    charts.promotion = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Not Promoted', 'Promoted'],
            datasets: [
                { label: 'Stayed', data: [promNo.filter(function(e) { return e.AttritionStatus === 'No'; }).length, promYes.filter(function(e) { return e.AttritionStatus === 'No'; }).length], backgroundColor: chartColors.teal },
                { label: 'Left', data: [promNo.filter(function(e) { return e.AttritionStatus === 'Yes'; }).length, promYes.filter(function(e) { return e.AttritionStatus === 'Yes'; }).length], backgroundColor: chartColors.rose }
            ]
        },
        options: {
            responsive: true, maintainAspectRatio: true,
            scales: { x: { stacked: true, ticks: { font: { size: 13 } } }, y: { stacked: true, beginAtZero: true, ticks: { stepSize: 1, font: { size: 13 } } } },
            plugins: { legend: { position: 'bottom', labels: { font: { size: 13 } } } }
        }
    });
}

function createMonthlyAttritionTrend(data) {
    var ctx = document.getElementById('chart-monthly-trend');
    if (!ctx) return;
    if (charts.monthlyTrend) charts.monthlyTrend.destroy();
    var monthly = {};
    for (var m = 1; m <= 12; m++) monthly[m] = 0;
    data.forEach(function(e) {
        if (e.AttritionStatus === 'Yes' && e.DepartureMonth > 0) monthly[e.DepartureMonth]++;
    });
    var actualCounts = [];
    for (var m = 1; m <= 12; m++) actualCounts.push(monthly[m]);
    var recentAvg = Math.round(actualCounts.slice(-6).reduce(function(s, v) { return s + v; }, 0) / 6);
    var forecastCounts = [recentAvg, recentAvg, recentAvg];
    var monthLabels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan (F)','Feb (F)','Mar (F)'];
    charts.monthlyTrend = new Chart(ctx, {
        type: 'line',
        data: {
            labels: monthLabels,
            datasets: [
                {
                    label: 'Actual Attrition', data: actualCounts.concat([null, null, null]),
                    borderColor: chartColors.cyan, backgroundColor: 'rgba(0,210,255,0.1)',
                    borderWidth: 3, pointBackgroundColor: chartColors.cyan, pointRadius: 4,
                    fill: true, tension: 0.3
                },
                {
                    label: 'Forecast', data: [null, null, null, null, null, null, null, null, null, null, null, null].concat(forecastCounts),
                    borderColor: chartColors.gold, backgroundColor: 'rgba(254,202,87,0.1)',
                    borderWidth: 3, borderDash: [6, 3], pointBackgroundColor: chartColors.gold, pointRadius: 5,
                    fill: true, tension: 0.3
                }
            ]
        },
        options: {
            responsive: true, maintainAspectRatio: true,
            plugins: { legend: { position: 'bottom', labels: { font: { size: 13 } } } },
            scales: { x: { ticks: { font: { size: 12 } } }, y: { beginAtZero: true, ticks: { stepSize: 1, font: { size: 12 } } } }
        }
    });
}

function createRetentionForecast(data) {
    var ctx = document.getElementById('chart-retention-forecast');
    if (!ctx) return;
    if (charts.retentionForecast) charts.retentionForecast.destroy();
    var total = data.length;
    var retention = data.filter(function(e) { return e.AttritionStatus === 'No'; }).length;
    var currentRate = total > 0 ? Math.round(retention / total * 1000) / 10 : 0;
    var monthly = {};
    for (var m = 1; m <= 12; m++) monthly[m] = 0;
    data.forEach(function(e) {
        if (e.AttritionStatus === 'Yes' && e.DepartureMonth > 0) monthly[e.DepartureMonth]++;
    });
    var counts = [];
    for (var m = 1; m <= 12; m++) counts.push(monthly[m]);
    var recentAvg = counts.slice(-6).reduce(function(s, v) { return s + v; }, 0) / 6;
    var projRetention = [currentRate];
    var projRetentionCount = retention;
    for (var i = 0; i < 3; i++) {
        projRetentionCount -= recentAvg;
        if (projRetentionCount < 0) projRetentionCount = 0;
        projRetention.push(total > 0 ? Math.round(projRetentionCount / total * 1000) / 10 : 0);
    }
    charts.retentionForecast = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Current', 'Q+1', 'Q+2', 'Q+3'],
            datasets: [{
                label: 'Retention Rate (%)',
                data: projRetention,
                borderColor: chartColors.teal, backgroundColor: 'rgba(29,209,161,0.15)',
                borderWidth: 3, pointBackgroundColor: [chartColors.teal, chartColors.gold, chartColors.orange, chartColors.rose],
                pointRadius: 6, pointHoverRadius: 8, fill: true, tension: 0.3
            }]
        },
        options: {
            responsive: true, maintainAspectRatio: true,
            plugins: {
                legend: { display: false },
                tooltip: { callbacks: { label: function(ctx) { return ctx.parsed.y + '%'; } } }
            },
            scales: {
                x: { ticks: { font: { size: 13 } } },
                y: { min: 0, max: 100, ticks: { font: { size: 13 }, callback: function(v) { return v + '%'; } } }
            }
        }
    });
}

function updateAllCharts(data) {
    createAttritionCostBreakdown(data);
    createDeptAttrition(data);
    createOvertimeAttrition(data);
    createPromotionAttrition(data);
    createMonthlyAttritionTrend(data);
    createRetentionForecast(data);
}
