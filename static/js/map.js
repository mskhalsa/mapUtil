// Initialize map
let map = L.map('map').setView([37.7749, -122.4194], 13);
const pointCounter = document.getElementById('point-counter');

// Define tile layers
const streetLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
});

const satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
});

// Add street layer by default
streetLayer.addTo(map);

// Layer toggle functionality
document.getElementById('layer-toggle').addEventListener('change', function(e) {
    if (e.target.checked) {
        map.removeLayer(streetLayer);
        map.addLayer(satelliteLayer);
    } else {
        map.removeLayer(satelliteLayer);
        map.addLayer(streetLayer);
    }
});

// Arrays to store points and markers
let points = [];
let markers = [];

// Update point counter
function updatePointCounter() {
    pointCounter.textContent = `Points: ${points.length}`;
}

// Display coordinates on mouse move
map.on('mousemove', function(e) {
    let lat = e.latlng.lat.toFixed(5);
    let lng = e.latlng.lng.toFixed(5);
    let coordsDiv = document.getElementById('coordinates');
    coordsDiv.innerHTML = `Lat: ${lat}, Lng: ${lng}`;
    coordsDiv.style.left = e.originalEvent.pageX + 15 + 'px';
    coordsDiv.style.top = e.originalEvent.pageY + 15 + 'px';
    coordsDiv.style.display = 'block';
});

// Hide coordinates when mouse leaves map
map.on('mouseleave', function() {
    let coordsDiv = document.getElementById('coordinates');
    coordsDiv.style.display = 'none';
});

// Add marker on click
map.on('click', function(e) {
    let lat = e.latlng.lat;
    let lng = e.latlng.lng;
    points.push([lat, lng]);
    let marker = L.marker([lat, lng]).addTo(map);
    markers.push(marker);
    updatePointCounter();
});

// Export points to CSV
document.getElementById('done-btn').addEventListener('click', function() {
    if (points.length === 0) {
        alert('Please add at least one point before exporting.');
        return;
    }
    
    $.ajax({
        type: 'POST',
        url: '/export',
        contentType: 'application/json',
        data: JSON.stringify({ points: points }),
        success: function(response) {
            if (response.file_path) {
                window.location.href = '/download?file_path=' + response.file_path;
            }
        }
    });
});

// Remove last point
document.getElementById('remove-btn').addEventListener('click', function() {
    if (markers.length > 0) {
        let lastMarker = markers.pop();
        map.removeLayer(lastMarker);
        points.pop();
        updatePointCounter();
    }
});

// Set up search functionality
const provider = new window.GeoSearch.OpenStreetMapProvider();

const searchControl = new window.GeoSearch.GeoSearchControl({
    provider: provider,
    style: 'bar',
    autoComplete: true,
    autoCompleteDelay: 250,
    showMarker: true,
    showPopup: false,
    marker: {
        icon: new L.Icon.Default(),
        draggable: false,
    },
    updateMap: true,
});

map.addControl(searchControl);

// Add marker when location is found through search
map.on('geosearch/showlocation', function(e) {
    let lat = e.location.y;
    let lng = e.location.x;
    points.push([lat, lng]);
    let marker = L.marker([lat, lng]).addTo(map);
    markers.push(marker);
    updatePointCounter();
});