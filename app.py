from flask import Flask, render_template, jsonify, request, send_file
import os
import csv

app = Flask(__name__)

# Create folders to store the template and exports
os.makedirs('templates', exist_ok=True)
os.makedirs('exports', exist_ok=True)

# HTML content for the interactive map
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Map</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>
    <link rel="stylesheet" href="https://unpkg.com/leaflet-geosearch/dist/geosearch.css"/>
    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    <script src="https://unpkg.com/leaflet-geosearch/dist/bundle.min.js"></script>
    <style>
        #map { height: 80vh; cursor: crosshair; }
        .btn { padding: 10px; background-color: #007bff; color: white; border: none; cursor: pointer; margin: 5px; }
        .remove-btn { padding: 10px; background-color: #ff0000; color: white; border: none; cursor: pointer; margin: 5px; }
        .search-bar { padding: 10px; background-color: #f1f1f1; margin: 5px; }
        .coordinates { position: absolute; padding: 5px; background-color: rgba(255, 255, 255, 0.8); border: 1px solid #ccc; border-radius: 3px; pointer-events: none; z-index: 1000; }
        .map-layers { margin: 5px; }
        .layer-btn { padding: 8px; background-color: #4CAF50; color: white; border: none; cursor: pointer; margin-right: 5px; }
        .layer-btn.active { background-color: #2E7D32; }
    </style>
</head>
<body>
    <div id="map"></div>
    <div class="search-bar" id="search-bar"></div>
    <div class="map-layers">
        <button id="streets-btn" class="layer-btn active">Streets</button>
        <button id="satellite-btn" class="layer-btn">Satellite</button>
    </div>
    <button id="done-btn" class="btn">Done</button>
    <button id="remove-btn" class="remove-btn">Remove Last</button>
    <div class="coordinates" id="coordinates">Lat: , Lng: </div>
    <script>
        let map = L.map('map').setView([37.7749, -122.4194], 13);
        
        // Define tile layers
        const streetLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        });
        
        const satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
        });
        
        // Add street layer by default
        streetLayer.addTo(map);
        
        // Layer switch functionality
        document.getElementById('streets-btn').addEventListener('click', function() {
            map.removeLayer(satelliteLayer);
            map.addLayer(streetLayer);
            document.getElementById('streets-btn').classList.add('active');
            document.getElementById('satellite-btn').classList.remove('active');
        });
        
        document.getElementById('satellite-btn').addEventListener('click', function() {
            map.removeLayer(streetLayer);
            map.addLayer(satelliteLayer);
            document.getElementById('satellite-btn').classList.add('active');
            document.getElementById('streets-btn').classList.remove('active');
        });

        let points = [];
        let markers = [];

        map.on('mousemove', function(e) {
            let lat = e.latlng.lat.toFixed(5);
            let lng = e.latlng.lng.toFixed(5);
            let coordsDiv = document.getElementById('coordinates');
            coordsDiv.innerHTML = `Lat: ${lat}, Lng: ${lng}`;
            coordsDiv.style.left = e.originalEvent.pageX + 15 + 'px';
            coordsDiv.style.top = e.originalEvent.pageY + 15 + 'px';
            coordsDiv.style.display = 'block';
        });

        map.on('mouseleave', function() {
            let coordsDiv = document.getElementById('coordinates');
            coordsDiv.style.display = 'none';
        });

        map.on('click', function(e) {
            let lat = e.latlng.lat;
            let lng = e.latlng.lng;
            points.push([lat, lng]);
            let marker = L.marker([lat, lng]).addTo(map);
            markers.push(marker);
        });

        document.getElementById('done-btn').addEventListener('click', function() {
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

        document.getElementById('remove-btn').addEventListener('click', function() {
            if (markers.length > 0) {
                let lastMarker = markers.pop();
                map.removeLayer(lastMarker);
                points.pop();
            }
        });

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

        map.on('geosearch/showlocation', function(e) {
            let lat = e.location.y;
            let lng = e.location.x;
            points.push([lat, lng]);
            let marker = L.marker([lat, lng]).addTo(map);
            markers.push(marker);
        });
    </script>
</body>
</html>
"""

# Write the HTML content to a file in the templates directory
with open('templates/index.html', 'w') as f:
    f.write(html_content)

@app.route('/')
def index():
    # Use the custom HTML file for the map interface
    return render_template('index.html')

@app.route('/export', methods=['POST'])
def export():
    data = request.json
    points = data.get('points', [])
    
    if points:
        file_path = 'exports/points.csv'
        with open(file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Latitude', 'Longitude'])
            csvwriter.writerows(points)
        return jsonify({'message': 'File exported', 'file_path': file_path}), 200
    return jsonify({'message': 'No points to export'}), 400

@app.route('/download')
def download():
    file_path = request.args.get('file_path')
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({'message': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=1234)