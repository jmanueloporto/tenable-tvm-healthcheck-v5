"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.1.1
LAYER: Core / Connection
DESCRIPTION: Robust REST Client with GET/POST support.
AUTHOR: Senior Software Architect
"""

import os
import requests
from dotenv import load_dotenv

class TenableConnection:
    def __init__(self):
        load_dotenv()
        self.access_key = os.getenv("TENABLE_ACCESS_KEY")
        self.secret_key = os.getenv("TENABLE_SECRET_KEY")
        self.base_url = "https://cloud.tenable.com"
        
        if not self.access_key or not self.secret_key:
            raise ValueError("CRITICAL: API Keys missing in .env")
            
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-ApiKeys": f"accessKey={self.access_key}; secretKey={self.secret_key}"
        }

    def get(self, endpoint: str):
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, json: dict = None):
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, headers=self.headers, json=json or {})
        response.raise_for_status()
        return response.json()
