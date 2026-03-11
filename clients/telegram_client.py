"""
Telegram 메신저 클라이언트
"""
import requests
import time
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from utils.retry import retry_request
from utils.logger import get_logger

logger = get_logger("telegram_client")

class TelegramClient:
    def __init__(self):
        self.base_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
        
    @retry_request(max_retries=3, delay=3.0)
    def send_message(self, text: str):
        """텔레그램 메시지 발송"""
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            logger.warning("Telegram credentials not set. Skipping message.")
            return

        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text,
            "parse_mode": "HTML"
        }
        
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        
        # 순차 발송 지연 시간
        time.sleep(1.0)
