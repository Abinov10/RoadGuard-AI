"""
RoadGuard AI - Detections & Map Data API
"""
from flask import Blueprint, jsonify, request, render_template
from bson import ObjectId
from db import get_collection, TAMIL_NADU_DISTRICTS

detections_bp = Blueprint("detections", __name__)


def serialize_doc(doc):
    """Convert MongoDB doc for JSON (ObjectId -> str)."""
    if doc is None:
        return None
    d = dict(doc)
    d["_id"] = str(d["_id"])
    if "created_at" in d and hasattr(d["created_at"], "isoformat"):
        d["created_at"] = d["created_at"].isoformat()
    return d


@detections_bp.route("/", methods=["GET"])
def list_detections():
    """List detections with optional district filter."""
    district = request.args.get("district")
    limit = min(int(request.args.get("limit", 100)), 500)
    
    coll = get_collection("detections")
    q = {}
    if district and district in TAMIL_NADU_DISTRICTS:
        q["district"] = district
    
    cursor = coll.find(q).sort("created_at", -1).limit(limit)
    items = [serialize_doc(d) for d in cursor]
    return jsonify({"detections": items})


@detections_bp.route("/map", methods=["GET"])
def map_view():
    """Render Tamil Nadu map with Leaflet."""
    return render_template("map.html", districts=TAMIL_NADU_DISTRICTS)


@detections_bp.route("/map/data", methods=["GET"])
def map_data():
    """GeoJSON-like data for map markers."""
    district = request.args.get("district")
    coll = get_collection("detections")
    q = {"latitude": {"$exists": True, "$ne": None}, "longitude": {"$exists": True, "$ne": None}}
    if district and district in TAMIL_NADU_DISTRICTS:
        q["district"] = district
    
    cursor = coll.find(q).sort("created_at", -1).limit(500)
    markers = []
    for d in cursor:
        markers.append({
            "id": str(d["_id"]),
            "lat": d["latitude"],
            "lng": d["longitude"],
            "crrs": d.get("composite_risk_score", 0),
            "risk_level": d.get("risk_level", "low"),
            "district": d.get("district", ""),
        })
    return jsonify({"markers": markers})
