/**
 * MARGAM AI – Tamil Nadu Leaflet map visualization
 */
(function () {
  const mapEl = document.getElementById('map');
  const districtFilter = document.getElementById('districtFilter');

  if (!mapEl) return;

  // Tamil Nadu center (approximate)
  const center = [11.1271, 78.6569];
  const map = L.map('map').setView(center, 7);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap'
  }).addTo(map);

  const markers = [];
  const colors = { critical: '#c62828', high: '#c41e3a', medium: '#ed6c02', low: '#2e7d32' };

  function addMarker(m) {
    const color = colors[m.risk_level] || colors.low;
    const marker = L.circleMarker([m.lat, m.lng], {
      radius: 8,
      fillColor: color,
      color: '#fff',
      weight: 2,
      opacity: 1,
      fillOpacity: 0.8
    });
    marker.bindPopup(
      `<b>CRRS: ${m.crrs}</b><br>District: ${m.district}<br>Risk: ${m.risk_level}`
    );
    marker.addTo(map);
    markers.push({ layer: marker, data: m });
  }

  function clearMarkers() {
    markers.forEach(({ layer }) => map.removeLayer(layer));
    markers.length = 0;
  }

  async function loadMarkers() {
    const district = districtFilter ? districtFilter.value : '';
    const url = `/detections/map/data${district ? '?district=' + encodeURIComponent(district) : ''}`;
    const res = await fetch(url);
    const data = await res.json();
    clearMarkers();
    (data.markers || []).forEach(addMarker);
  }

  if (districtFilter) {
    districtFilter.addEventListener('change', loadMarkers);
  }

  loadMarkers();
})();
