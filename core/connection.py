"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.0.0
LAYER: Core / Connection
DESCRIPTION: Singleton-like class for Tenable API authentication and session management.
AUTHOR: Senior Software Architect
"""

import os
from typing import Dict
from dotenv import load_dotenv

class TenableConnection:
    """Handles authentication and session setup for Tenable API."""
    
    def __init__(self):
        load_dotenv()
        self.access_key = os.getenv("TENABLE_ACCESS_KEY")
        self.secret_key = os.getenv("TENABLE_SECRET_KEY")
        self.base_url = os.getenv("TENABLE_BASE_URL", "https://cloud.tenable.com")
        
        if not self.access_key or not self.secret_key:
            raise EnvironmentError("CRITICAL: Missing Tenable credentials in .env file.")

    def get_headers(self) -> Dict[str, str]:
        """Returns standard headers for Tenable API calls."""
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-ApiKeys": f"accessKey={self.access_key}; secretKey={self.secret_key}"
        }
