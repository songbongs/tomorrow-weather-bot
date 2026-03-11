"""
환경변수 로딩 및 설정 관리
"""
import os
import json
from dotenv import load_dotenv

load_dotenv()

TIMEZONE = os.getenv("TIMEZONE", "Asia/Seoul")

KMA_SERVICE_KEY = os.getenv("KMA_SERVICE_KEY", "")
AIRKOREA_SERVICE_KEY = os.getenv("AIRKOREA_SERVICE_KEY", "")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

LOCATIONS = os.getenv("LOCATIONS", "")
LOCATIONS_JSON = os.getenv("LOCATIONS_JSON", "")
