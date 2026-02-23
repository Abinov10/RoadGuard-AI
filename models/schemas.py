"""
MARGAM AI - MongoDB document schemas (structure reference)
District-level compatible for Tamil Nadu
"""
from datetime import datetime
from typing import Optional, List


def detection_doc(
    image_path: str,
    detections: list,
    composite_risk_score: float,
    district: str,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    traffic_volume: str = "medium",
    **kwargs
) -> dict:
    """Schema for road detection document."""
    return {
        "image_path": image_path,
        "detections": detections,
        "composite_risk_score": composite_risk_score,
        "district": district,
        "latitude": latitude,
        "longitude": longitude,
        "traffic_volume": traffic_volume,
        "status": kwargs.get("status", "pending"),
        "created_at": kwargs.get("created_at", datetime.utcnow()),
        "updated_at": datetime.utcnow(),
        **{k: v for k, v in kwargs.items() if k not in ("status", "created_at", "updated_at")}
    }


def maintenance_doc(
    detection_id: str,
    district: str,
    status: str = "reported",
    **kwargs
) -> dict:
    """Schema for maintenance workflow."""
    return {
        "detection_id": detection_id,
        "district": district,
        "status": status,  # reported, assigned, in_progress, completed, deferred
        "created_at": kwargs.get("created_at", datetime.utcnow()),
        "updated_at": datetime.utcnow(),
        "notes": kwargs.get("notes", ""),
        **{k: v for k, v in kwargs.items() if k not in ("created_at", "updated_at", "notes")}
    }
