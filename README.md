# MARGAM AI – Tamil Nadu Climate-Aware Road Risk Monitoring System

A modular full-stack web system for AI-based road damage detection and district-level risk monitoring across Tamil Nadu. (Hackathon Project)

## Tech Stack

- **Backend:** Python Flask
- **AI:** YOLOv8 (Ultralytics)
- **Database:** MongoDB
- **Frontend:** HTML, CSS, JavaScript
- **Map:** Leaflet.js
- **Charts:** Chart.js

## Features

1. Image upload API for road damage
2. AI-based pothole and crack detection (YOLOv8)
3. Tamil Nadu Composite Road Risk Score (CRRS)
4. MongoDB storage with district-level indexing
5. Admin dashboard with analytics
6. Leaflet Tamil Nadu map visualization
7. Chart.js analytics
8. Tamil language toggle
9. Maintenance workflow tracking

## Project Structure

```
margam ai/
├── app.py              # Main Flask app
├── db.py               # MongoDB connection & district config
├── config.py           # App configuration
├── requirements.txt
├── .env.example
├── utils/
│   ├── ai_detector.py      # YOLOv8 detection
│   └── risk_calculator.py  # CRRS calculation
├── routes/
│   ├── upload.py           # Image upload & detection
│   ├── detections.py       # List & map data
│   ├── admin.py            # Admin dashboard
│   └── api.py              # General API
├── models/
│   ├── schemas.py          # Document schemas
│   └── weights/            # Custom YOLOv8 model (optional)
├── templates/
├── static/
│   ├── uploads/
│   ├── css/
│   └── js/
```

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your MongoDB URI
   ```

3. **Run MongoDB** (local or cloud)

4. **Start the app:**
   ```bash
   python app.py
   ```

5. Open `http://localhost:5000`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload/` | Upload image, run detection, compute CRRS |
| GET | `/detections/` | List detections (filter by district) |
| GET | `/detections/map` | Tamil Nadu map view |
| GET | `/detections/map/data` | GeoJSON markers for map |
| GET | `/admin/` | Admin dashboard |
| GET | `/admin/stats` | Aggregate stats for charts |
| GET/PATCH | `/admin/maintenance` | Maintenance workflows |
| GET | `/api/districts` | Tamil Nadu districts list |

## District-Level Handling

The system supports all 38 Tamil Nadu districts. District names are validated against `TAMIL_NADU_DISTRICTS` in `db.py`. Add custom climate factors in `utils/risk_calculator.py` for monsoon/cyclone zones.

## Custom YOLOv8 Model

Place fine-tuned road damage weights at `models/weights/road_damage_yolov8.pt` for pothole/crack detection. Without it, the app falls back to a mock or YOLOv8n.
