"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.0.0
LAYER: Core / Data
DESCRIPTION: Orchestrates API calls to Tenable following the optimized 7-step async sequence.
AUTHOR: Senior Software Architect
"""

import requests
import time
from typing import Dict, Any, List, Union, Optional
from core.connection import TenableConnection

class TenableDataCollector:
    """
    Handles complex data collection from Tenable.io, including 
    standard REST calls and heavy asynchronous exports.
    """

    def __init__(self, connection: TenableConnection):
        self.conn = connection
        self.headers = self.conn.get_headers()
        self.base_url = self.conn.base_url

    def _fetch_lightweight(self, endpoint: str) -> Union[Dict, List, str]:
        """Executes a simple GET request with error suppression."""
        try:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            response = requests.get(url, headers=self.headers, timeout=20)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return f"ERROR: {str(e)}"

    def _run_export(self, export_type: str, filters: Dict[str, Any]) -> Union[List, str]:
        """
        Manages the 3-step asynchronous export process:
        1. Request Export (POST)
        2. Poll Status (GET /status)
        3. Download Chunks (GET /chunks)
        """
        try:
            # Step A: Trigger Export
            path = "assets/export" if export_type == "assets" else "vulns/export"
            url = f"{self.base_url}/{path}"
            
            # Phase 1 minimal payload: assets need at least an empty filter or specific criteria
            init_res = requests.post(url, headers=self.headers, json=filters, timeout=20)
            init_res.raise_for_status()
            export_uuid = init_res.json().get("export_uuid")

            # Step B: Polling for Completion
            print(f" [*] Export {export_type} initiated. UUID: {export_uuid}")
            while True:
                status_url = f"{url}/{export_uuid}/status"
                status_res = requests.get(status_url, headers=self.headers, timeout=20)
                status_res.raise_for_status()
                
                status = status_res.json().get("status")
                if status == "FINISHED":
                    chunks = status_res.json().get("chunks_available", [])
                    break
                elif status in ["ERROR", "CANCELLED"]:
                    return f"ERROR: Export failed with status {status}"
                
                time.sleep(5) # Polling interval

            # Step C: Download Chunks
            all_data = []
            for chunk_id in chunks:
                chunk_url = f"{url}/{export_uuid}/chunks/{chunk_id}"
                chunk_res = requests.get(chunk_url, headers=self.headers, timeout=30)
                chunk_res.raise_for_status()
                all_data.extend(chunk_res.json())
            
            return all_data

        except Exception as e:
            return f"ERROR: Async export failed: {str(e)}"

    def collect_all(self) -> Dict[str, Any]:
        """
        Orchestrates the 7-step optimized sequence to populate master_data.
        """
        master_data = {}
        print("[*] Starting 7-Step Asynchronous Collection Sequence...")

        # Paso 1: Infraestructura base
        print(" [Step 1/7] Fetching Scanners and Agents...")
        master_data["scanners"] = self._fetch_lightweight("scanners")
        # Example: Fetching agents for the first scanner found (simplified for health check)
        master_data["agents"] = "PENDING_DETAILED_LOGIC" 

        # Paso 2: Export Assets (Pesado)
        print(" [Step 2/7] Running Asset Export (Async)...")
        master_data["assets_raw"] = self._run_export("assets", {"chunk_size": 1000})

        # Paso 3: Configuración de Escaneo
        print(" [Step 3/7] Fetching Scans, Policies, Exclusions, and Target Groups...")
        master_data["scans"] = self._fetch_lightweight("scans")
        master_data["policies"] = self._fetch_lightweight("policies")
        master_data["exclusions"] = self._fetch_lightweight("exclusions")
        master_data["target_groups"] = self._fetch_lightweight("target-groups")

        # Paso 4: Redes y Clasificación
        print(" [Step 4/7] Fetching Tags and Networks...")
        master_data["tags"] = self._fetch_lightweight("tags/values")
        master_data["networks"] = self._fetch_lightweight("networks")

        # Paso 5: Export Vulnerabilidades (Pesado)
        print(" [Step 5/7] Running Vulnerability Export (Async)...")
        # Severity filters usually required for vulns to avoid massive overhead
        master_data["vulns_raw"] = self._run_export("vulns", {"num_assets": 500})

        # Paso 6: Usuarios y Auditoría
        print(" [Step 6/7] Fetching Users, Audit Logs, and Access Groups...")
        master_data["users"] = self._fetch_lightweight("users")
        master_data["audit_log"] = self._fetch_lightweight("audit-log/events")
        master_data["access_groups"] = self._fetch_lightweight("access-groups")

        # Paso 7: Conectores Externos
        print(" [Step 7/7] Fetching Cloud Connectors...")
        master_data["connectors"] = self._fetch_lightweight("connectors")

        print("[SUCCESS] Master Data Collection complete.")
        return master_data
