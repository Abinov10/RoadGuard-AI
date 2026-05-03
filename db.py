"""
RoadGuard AI - MongoDB Database Connection & Config
Tamil Nadu district-aware schema support
"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("MONGODB_DB", "roadguard_ai")

# Tamil Nadu districts (38 districts) - for scalable district-level handling
TAMIL_NADU_DISTRICTS = [
    "Ariyalur", "Chengalpattu", "Chennai", "Coimbatore", "Cuddalore",
    "Dharmapuri", "Dindigul", "Erode", "Kallakurichi", "Kanchipuram",
    "Kanyakumari", "Karur", "Krishnagiri", "Madurai", "Mayiladuthurai",
    "Nagapattinam", "Namakkal", "Nilgiris", "Perambalur", "Pudukkottai",
    "Ramanathapuram", "Ranipet", "Salem", "Sivaganga", "Tenkasi",
    "Thanjavur", "Theni", "Thoothukudi", "Tiruchirappalli", "Tirunelveli",
    "Tirupattur", "Tiruppur", "Tiruvallur", "Tiruvannamalai", "Tiruvarur",
    "Vellore", "Viluppuram", "Virudhunagar"
]

# Collection names
COLLECTIONS = {
    "detections": "road_detections",
    "maintenance": "maintenance_workflows",
    "users": "admin_users",
    "risk_scores": "composite_risk_scores",
}

_client = None
_db = None


def get_db():
    """Get MongoDB database instance."""
    global _db
    if _db is None:
        _db = get_client()[DB_NAME]
    return _db


def get_client():
    """Get MongoDB client."""
    global _client
    if _client is None:
        _client = MongoClient(MONGODB_URI)
        try:
            _client.admin.command("ping")
        except ConnectionFailure:
            raise ConnectionFailure("MongoDB server not available. Check MONGODB_URI.")
    return _client


def get_collection(name: str):
    """Get a collection by name."""
    return get_db()[COLLECTIONS.get(name, name)]


def ensure_indexes():
    """Create indexes for performance."""
    db = get_db()
    det = db[COLLECTIONS["detections"]]
    det.create_index([("district", 1), ("created_at", -1)])
    det.create_index([("latitude", 1), ("longitude", 1)])
    det.create_index("composite_risk_score")
    maint = db[COLLECTIONS["maintenance"]]
    maint.create_index([("detection_id", 1)])
    maint.create_index([("status", 1), ("district", 1)])
