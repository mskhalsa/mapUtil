# Map Utility

---

## Overview of the Application

This is a lightweight Flask web application that allows users to:
- Visualize geographical points on a map
- Export point coordinates to CSV
- Download exported data files
- Simple browser-based interface
- Lightweight server with minimal dependencies

---

## Instructions on Setting Up the Development Environment

### Prerequisites

1. **Python** (3.6 or newer)
2. **Flask** web framework
3. **Web browser** with JavaScript enabled

---
### Deploy
This application can be deployed using Python directly.

1. **Clone the Repository**
   ```bash
   git clone https://github.com/mskhalsa/maputil
   ```

2. **Install Dependencies**
   ```bash
   pip install flask
   ```

3. **Run the Application**
   ```bash
   python app.py
   ```
   
   **Note:** The application will be available at http://localhost:1234

4. **Stop the Server**
   Press `CTRL+C` in the terminal where the server is running

---
### Environment Configuration
1. **Configure Environment** 
   - No environment variables are required for basic functionality
   - Edit the port in `app.py` if needed (default: 1234)
   
   ***Note:*** The application will create an `exports` directory automatically to store CSV files

---

## Project Structure

```
.
├── app.py
├── exports
│   └── points.csv
├── static
│   ├── css
│   └── js
└── templates
    ├── index.html
    └── map.html
```

---

## Development

```bash
# Start development server
python app.py

# Run with different port
python -c "import app; app.app.run(debug=True, port=5000)"

# Create production-ready WSGI server (using gunicorn)
# First install: pip install gunicorn
gunicorn app:app -b 0.0.0.0:1234
```

---

## API Endpoints

The application provides the following API endpoints:

- `GET /` - Main application interface
- `POST /export` - Export points data to CSV
  - Accepts JSON body with `points` array of [lat, lng] coordinates
  - Returns path to the generated file
- `GET /download` - Download generated CSV file
  - Requires `file_path` query parameter

---

## File Exports

Exported files are stored in the `exports` directory and contain:
- CSV format with headers (Latitude, Longitude)
- One coordinate pair per line
- Files are named `points.csv` by default

---

## Browser Support

The application has been tested on:
- Chrome (latest)
- Firefox (latest)
- Edge (latest)
- Safari (latest)

---

## License

MIT License
