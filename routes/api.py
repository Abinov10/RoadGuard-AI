"""
MARGAM AI - General API endpoints
"""
from flask import Blueprint, jsonify, render_template
from db import get_collection, TAMIL_NADU_DISTRICTS

api_bp = Blueprint("api", __name__)


@api_bp.route("/districts")
def districts():
    """Return Tamil Nadu districts for dropdowns."""
    return jsonify({"districts": TAMIL_NADU_DISTRICTS})


@api_bp.route("/upload-page")
def upload_page():
    """Render upload page."""
    return render_template("upload.html", districts=TAMIL_NADU_DISTRICTS)
