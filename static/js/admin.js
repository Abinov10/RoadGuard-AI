/**
 * MARGAM AI – Admin dashboard Chart.js analytics
 */
(function () {
  const totalEl = document.getElementById('totalDetections');
  const districtCanvas = document.getElementById('districtChart');
  const riskCanvas = document.getElementById('riskChart');
  const maintenanceCanvas = document.getElementById('maintenanceChart');
  const maintTableBody = document.getElementById('maintTableBody');
  const maintDistrict = document.getElementById('maintDistrict');

  let districtChart, riskChart, maintenanceChart;

  async function fetchStats() {
    const res = await fetch('/admin/stats');
    return res.json();
  }

  async function fetchMaintenance() {
    const district = maintDistrict ? maintDistrict.value : '';
    const url = `/admin/maintenance${district ? '?district=' + encodeURIComponent(district) : ''}`;
    const res = await fetch(url);
    return res.json();
  }

  function renderCharts(stats) {
    totalEl.textContent = stats.total_detections;

    if (districtCanvas && stats.by_district?.length) {
      if (districtChart) districtChart.destroy();
      districtChart = new Chart(districtCanvas, {
        type: 'bar',
        data: {
          labels: stats.by_district.map(d => d._id),
          datasets: [{
            label: 'Detections',
            data: stats.by_district.map(d => d.count),
            backgroundColor: 'rgba(13, 79, 139, 0.7)'
          }]
        },
        options: {
          responsive: true,
          scales: { y: { beginAtZero: true } }
        }
      });
    }

    if (riskCanvas && stats.by_risk_level?.length) {
      if (riskChart) riskChart.destroy();
      riskChart = new Chart(riskCanvas, {
        type: 'doughnut',
        data: {
          labels: stats.by_risk_level.map(d => d._id),
          datasets: [{
            data: stats.by_risk_level.map(d => d.count),
            backgroundColor: ['#c62828', '#c41e3a', '#ed6c02', '#2e7d32']
          }]
        },
        options: { responsive: true }
      });
    }

    if (maintenanceCanvas && stats.by_maintenance_status?.length) {
      if (maintenanceChart) maintenanceChart.destroy();
      maintenanceChart = new Chart(maintenanceCanvas, {
        type: 'pie',
        data: {
          labels: stats.by_maintenance_status.map(d => d._id),
          datasets: [{
            data: stats.by_maintenance_status.map(d => d.count),
            backgroundColor: ['#0d4f8b', '#ed6c02', '#2e7d32', '#5c6b73']
          }]
        },
        options: { responsive: true }
      });
    }
  }

  async function renderMaintenanceTable() {
    const data = await fetchMaintenance();
    if (!maintTableBody) return;
    maintTableBody.innerHTML = (data.workflows || [])
      .map(w => `
        <tr>
          <td><code>${(w.detection_id || w._id || '').slice(-8)}</code></td>
          <td>${w.district || '-'}</td>
          <td>
            <select data-id="${w._id}" onchange="updateMaintStatus(this)">
              <option ${w.status === 'reported' ? 'selected' : ''}>reported</option>
              <option ${w.status === 'assigned' ? 'selected' : ''}>assigned</option>
              <option ${w.status === 'in_progress' ? 'selected' : ''}>in_progress</option>
              <option ${w.status === 'completed' ? 'selected' : ''}>completed</option>
              <option ${w.status === 'deferred' ? 'selected' : ''}>deferred</option>
            </select>
          </td>
          <td>-</td>
        </tr>
      `).join('') || '<tr><td colspan="4">No workflows</td></tr>';
  }

  window.updateMaintStatus = async function (sel) {
    const id = sel.getAttribute('data-id');
    const status = sel.value;
    await fetch('/admin/maintenance', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id, status })
    });
    const stats = await fetchStats();
    renderCharts(stats);
    renderMaintenanceTable();
  };

  if (maintDistrict) {
    maintDistrict.addEventListener('change', renderMaintenanceTable);
  }

  async function init() {
    const stats = await fetchStats();
    renderCharts(stats);
    renderMaintenanceTable();
  }

  init();
})();
