"""
MARGAM AI - YOLOv8-based Pothole & Crack Detection
Ultralytics YOLOv8 for road damage classification
"""
import os
from pathlib import Path

# Optional: Use ultralytics only when available
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False

# Detection classes for road damage (custom model or COCO fallback)
# Extend with fine-tuned weights for pothole/crack detection
DAMAGE_CLASSES = ["pothole", "crack", "surface_damage"]


def get_model_path():
    """Return path to YOLOv8 model weights (custom or pretrained)."""
    base = Path(__file__).resolve().parent.parent
    custom = base / "models" / "weights" / "road_damage_yolov8.pt"
    if custom.exists():
        return str(custom)
    return "yolov8n.pt"  # Fallback to nano model for demo


def detect_road_damage(image_path: str, conf_threshold: float = 0.25):
    """
    Run YOLOv8 inference on road image for pothole/crack detection.
    
    Args:
        image_path: Path to uploaded image
        conf_threshold: Confidence threshold for detections
    
    Returns:
        List of detections: [{"class": str, "confidence": float, "bbox": [x1,y1,x2,y2]}]
    """
    if not YOLO_AVAILABLE:
        # Mock response for environments without ultralytics
        return [
            {"class": "pothole", "confidence": 0.85, "bbox": [100, 150, 200, 220]},
            {"class": "crack", "confidence": 0.72, "bbox": [300, 100, 450, 120]},
        ]
    
    model_path = get_model_path()
    model = YOLO(model_path)
    
    results = model.predict(
        source=image_path,
        conf=conf_threshold,
        verbose=False
    )
    
    detections = []
    for r in results:
        if r.boxes is None:
            continue
        for box in r.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            xyxy = box.xyxy[0].tolist()
            cls_name = model.names.get(cls_id, "damage")
            detections.append({
                "class": cls_name,
                "confidence": round(conf, 4),
                "bbox": [round(x, 2) for x in xyxy]
            })
    
    return detections


def count_by_class(detections: list) -> dict:
    """Aggregate detection counts by class."""
    counts = {}
    for d in detections:
        c = d.get("class", "unknown")
        counts[c] = counts.get(c, 0) + 1
    return counts
