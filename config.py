"""
RoadGuard AI - Application configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "roadguard-ai-secret-key-change-in-production")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    MONGODB_DB = os.getenv("MONGODB_DB", "roadguard_ai")
