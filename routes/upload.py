"""
MARGAM AI - Image Upload & AI Detection API
"""
import os
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename

from db import get_collection, TAMIL_NADU_DISTRICTS
from utils.ai_detector import detect_road_damage, count_by_class
from utils.risk_calculator import compute_crrs, crrs_risk_level
from models.schemas import detection_doc, maintenance_doc

upload_bp = Blueprint("upload", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
DEFAULT_DISTRICT = "Chennai"


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_bp.route("/", methods=["POST"])
def upload_image():
    """
    Upload road image, run AI detection, compute CRRS, store in MongoDB.
    Form fields: file, district, latitude, longitude, traffic_volume
    """
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Allowed: png, jpg, jpeg, webp"}), 400
    
    district = request.form.get("district", DEFAULT_DISTRICT)
    if district not in TAMIL_NADU_DISTRICTS:
        district = DEFAULT_DISTRICT
    
    lat = request.form.get("latitude", type=float)
    lon = request.form.get("longitude", type=float)
    traffic = request.form.get("traffic_volume", "medium")
    
    ext = file.filename.rsplit(".", 1)[1].lower()
    safe_name = f"{uuid.uuid4().hex}.{ext}"
    save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], safe_name)
    file.save(save_path)
    
    try:
        detections = detect_road_damage(save_path)
    except Exception as e:
        return jsonify({"error": f"Detection failed: {str(e)}"}), 500
    
    counts = count_by_class(detections)
    pothole_count = counts.get("pothole", 0)
    crack_count = counts.get("crack", 0) + counts.get("surface_damage", 0)
    
    crrs = compute_crrs(
        pothole_count=pothole_count,
        crack_count=crack_count,
        district=district,
        traffic_volume=traffic,
        maintenance_count=0,
        area_px=1920 * 1080,
    )
    risk_level = crrs_risk_level(crrs)
    
    rel_path = f"/static/uploads/{safe_name}"
    doc = detection_doc(
        image_path=rel_path,
        detections=detections,
        composite_risk_score=crrs,
        district=district,
        latitude=lat,
        longitude=lon,
        traffic_volume=traffic,
        risk_level=risk_level,
        pothole_count=pothole_count,
        crack_count=crack_count,
    )
    
    coll = get_collection("detections")
    result = coll.insert_one(doc)
    doc_id = str(result.inserted_id)
    
    maint_coll = get_collection("maintenance")
    maint_coll.insert_one(maintenance_doc(detection_id=doc_id, district=district, status="reported"))
    
    return jsonify({
        "id": doc_id,
        "image_path": rel_path,
        "detections": detections,
        "composite_risk_score": crrs,
        "risk_level": risk_level,
        "district": district,
        "pothole_count": pothole_count,
        "crack_count": crack_count,
    }), 201
