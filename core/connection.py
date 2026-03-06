"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.0.6
LAYER: Core / Connection
DESCRIPTION: Standardized Tenable.io SDK Connection (The missing link).
AUTHOR: Senior Software Architect
"""

import os
from tenable.io import TenableIO
from dotenv import load_dotenv

class TenableConnection:
    def __init__(self):
        load_dotenv()
        self.access_key = os.getenv("TENABLE_ACCESS_KEY")
        self.secret_key = os.getenv("TENABLE_SECRET_KEY")
        
        if not self.access_key or not self.secret_key:
            raise ValueError("CRITICAL: TENABLE_ACCESS_KEY or TENABLE_SECRET_KEY not found in .env")
        
        # Aquí es donde nace el atributo .tio que el colector necesita
        self.tio = TenableIO(self.access_key, self.secret_key)
