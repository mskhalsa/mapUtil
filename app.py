from flask import Flask, render_template, jsonify, request, send_file
import os
import csv

app = Flask(__name__)

# Create folders to store exports
os.makedirs('exports', exist_ok=True)

@app.route('/')
def index():
    # Use the HTML template from templates directory
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