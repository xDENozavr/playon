document.addEventListener('DOMContentLoaded', function() {

  // Finds every map container on the page (works whether there's one,
  // like on club_detail, or many, like on the clubs list page) and
  // initializes a small Leaflet map with a single marker for each.
  document.querySelectorAll('[id^="map-"]').forEach(function(mapEl) {
    const lat = parseFloat(mapEl.dataset.lat);
    const lng = parseFloat(mapEl.dataset.lng);
    const name = mapEl.dataset.name || '';

    if (isNaN(lat) || isNaN(lng)) return;

    const map = L.map(mapEl.id, {
      zoomControl: false,
      dragging: false,
      scrollWheelZoom: false,
    }).setView([lat, lng], 15);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
    }).addTo(map);

    L.marker([lat, lng]).addTo(map).bindPopup(name);
  });

});