"""
MARGAM AI - Tamil Nadu Composite Road Risk Score (CRRS)
Climate-aware risk scoring for district-level prioritization
"""
from db import TAMIL_NADU_DISTRICTS

# Weight factors for CRRS (0–1 scale)
WEIGHTS = {
    "damage_severity": 0.35,      # Pothole/crack density & severity
    "traffic_volume": 0.20,       # Road usage impact
    "climate_factor": 0.20,       # Rainfall, humidity (Tamil Nadu monsoon)
    "maintenance_history": 0.15,  # Past repair frequency
    "connectivity": 0.10,         # Hospital/school/highway proximity
}

# District-level climate factors (Tamil Nadu monsoon/cyclone zones)
# Higher = more rainfall / humidity impact
CLIMATE_FACTORS = {
    "Kanyakumari": 1.2, "Nilgiris": 1.15, "Coimbatore": 1.0,
    "Chennai": 1.1, "Cuddalore": 1.15, "Nagapattinam": 1.15,
    "Tiruvarur": 1.1, "Thanjavur": 1.0, "Mayiladuthurai": 1.1,
    "Ramanathapuram": 0.95, "Thoothukudi": 0.95, "Tirunelveli": 1.0,
    "Madurai": 0.9, "Dindigul": 0.9, "Salem": 0.95, "Erode": 0.95,
    "Viluppuram": 1.05, "Dharmapuri": 0.9, "Krishnagiri": 0.85,
}
# Default for districts not listed
DEFAULT_CLIMATE = 0.9


def get_climate_factor(district: str) -> float:
    """Get climate risk factor for Tamil Nadu district."""
    if not district or district not in TAMIL_NADU_DISTRICTS:
        return DEFAULT_CLIMATE
    return CLIMATE_FACTORS.get(district, DEFAULT_CLIMATE)


def compute_damage_severity(pothole_count: int, crack_count: int, area_px: int = 1) -> float:
    """Compute damage severity sub-score (0–1)."""
    if area_px <= 0:
        area_px = 1
    density = (pothole_count * 2 + crack_count) / (area_px / 1e6) if area_px else 0
    return min(1.0, density / 50)


def compute_crrs(
    pothole_count: int = 0,
    crack_count: int = 0,
    district: str = "",
    traffic_volume: str = "medium",
    maintenance_count: int = 0,
    area_px: int = 1,
) -> float:
    """
    Compute Tamil Nadu Composite Road Risk Score (CRRS).
    Returns value 0–100 (higher = higher risk).
    """
    damage = compute_damage_severity(pothole_count, crack_count, area_px)
    climate = get_climate_factor(district)
    climate_norm = min(1.0, (climate - 0.7) / 0.6)  # Normalize to 0–1
    
    traffic_map = {"low": 0.3, "medium": 0.6, "high": 1.0}
    traffic = traffic_map.get(traffic_volume, 0.6)
    
    maint = min(1.0, maintenance_count / 5)  # More repairs = slightly lower risk
    maint_score = 1.0 - (maint * 0.3)
    
    connectivity = 0.5  # Placeholder; can use GIS data
    
    score = (
        WEIGHTS["damage_severity"] * damage
        + WEIGHTS["traffic_volume"] * traffic
        + WEIGHTS["climate_factor"] * climate_norm
        + WEIGHTS["maintenance_history"] * maint_score
        + WEIGHTS["connectivity"] * connectivity
    )
    
    return round(min(100, score * 100), 2)


def crrs_risk_level(score: float) -> str:
    """Map CRRS score to risk level."""
    if score >= 70:
        return "critical"
    if score >= 50:
        return "high"
    if score >= 30:
        return "medium"
    return "low"
