"""
RoadGuard AI - Admin Dashboard
"""
from flask import Blueprint, render_template, jsonify, request
from db import get_collection, TAMIL_NADU_DISTRICTS
from bson import ObjectId
from datetime import datetime, timedelta

admin_bp = Blueprint("admin", __name__)


def serialize_doc(doc):
    if doc is None:
        return None
    d = dict(doc)
    d["_id"] = str(d["_id"])
    for k in ("created_at", "updated_at"):
        if k in d and hasattr(d[k], "isoformat"):
            d[k] = d[k].isoformat()
    return d


@admin_bp.route("/")
def dashboard():
    """Admin dashboard page."""
    return render_template("admin.html", districts=TAMIL_NADU_DISTRICTS)


@admin_bp.route("/stats")
def stats():
    """Aggregate stats for charts."""
    coll = get_collection("detections")
    maint = get_collection("maintenance")
    
    total = coll.count_documents({})
    
    by_district = list(coll.aggregate([
        {"$group": {"_id": "$district", "count": {"$sum": 1}, "avg_crrs": {"$avg": "$composite_risk_score"}}},
        {"$sort": {"count": -1}}
    ]))
    
    by_risk = list(coll.aggregate([
        {"$group": {"_id": "$risk_level", "count": {"$sum": 1}}}
    ]))
    
    by_status = list(maint.aggregate([
        {"$group": {"_id": "$status", "count": {"$sum": 1}}}
    ]))
    
    return jsonify({
        "total_detections": total,
        "by_district": by_district,
        "by_risk_level": by_risk,
        "by_maintenance_status": by_status,
    })


@admin_bp.route("/maintenance", methods=["GET", "PATCH"])
def maintenance():
    """List or update maintenance workflows."""
    if request.method == "PATCH":
        data = request.get_json() or {}
        mid = data.get("id")
        status = data.get("status")
        if not mid or not status:
            return jsonify({"error": "id and status required"}), 400
        maint = get_collection("maintenance")
        maint.update_one(
            {"_id": ObjectId(mid)},
            {"$set": {"status": status, "updated_at": datetime.utcnow()}}
        )
        return jsonify({"ok": True})
    
    coll = get_collection("maintenance")
    district = request.args.get("district")
    q = {}
    if district and district in TAMIL_NADU_DISTRICTS:
        q["district"] = district
    items = list(coll.find(q).sort("created_at", -1).limit(100))
    return jsonify({"workflows": [serialize_doc(d) for d in items]})
