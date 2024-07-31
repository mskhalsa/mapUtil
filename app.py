from flask import Flask, render_template, jsonify, request
import folium
import os

app = Flask(__name__)

# Create a folder to store the template
os.makedirs('templates', exist_ok=True)

@app.route('/')
def index():
    start_coords = (37.7749, -122.4194)
    folium_map = folium.Map(location=start_coords, zoom_start=13)
    folium_map.save('templates/map.html')
    return render_template('index.html')

@app.route('/export', methods=['POST'])
def export():
    data = request.json
    points = data.get('points', [])
    return jsonify(points), 200

if __name__ == '__main__':
    app.run(debug=True, port=1234)
