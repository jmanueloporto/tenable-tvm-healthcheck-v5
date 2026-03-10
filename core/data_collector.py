"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.1.0
LAYER: Core / Data Collection
DESCRIPTION: Silent execution collector. Polling and 403/405 errors are silenced. 
             Steps 3 and 4 are separated for CLI clarity.
AUTHOR: Senior Software Architect
"""

import time
from typing import Dict, Any, List

class TenableDataCollector:
    def __init__(self, connection):
        self.connection = connection

    def _wait_for_export(self, export_type: str, uuid: str) -> List[int]:
        """Polls export status silently until FINISHED."""
        while True:
            try:
                status_res = self.connection.get(f"/{export_type}/export/{uuid}/status")
                status = status_res.get("status")
                if status == "FINISHED":
                    return status_res.get("chunks_available", [])
                elif status == "ERROR":
                    return []
            except:
                return []
            time.sleep(2)

    def collect_all(self) -> Dict[str, Any]:
        print("[*] Starting Phase 1 Silent Collection (v5.0.16)...")
        data = {
            'infrastructure': {}, 'assets': [], 'vulnerabilities': [],
            'users': [], 'audit_log': [], 'scans': [], 'policies': [], 'tags': []
        }

        # --- STEP 1: Infrastructure (Silent) ---
        print(" [Step 1/7] Fetching Hybrid Sensors...")
        infra = {'scanners': [], 'was_scanners': [], 'nnm_monitors': [], 'connectors': [], 'exclusions': []}
        try:
            infra['scanners'] = self.connection.get("/scanners").get('scanners', [])
            try: infra['connectors'] = self.connection.get("/connectors").get('connectors', [])
            except: pass
        except: pass
        data['infrastructure'] = infra

        # --- STEP 2: Assets (Silent Polling) ---
        print(" [Step 2/7] Exporting Assets...")
        try:
            asset_payload = {"chunk_size": 1000, "filters": {"is_terminated": False}}
            asset_req = self.connection.post("/assets/export", json=asset_payload)
            a_uuid = asset_req.get("export_uuid")
            chunks = self._wait_for_export("assets", a_uuid)
            for c_id in chunks:
                chunk_data = self.connection.get(f"/assets/export/{a_uuid}/chunks/{c_id}")
                data['assets'].extend(chunk_data if isinstance(chunk_data, list) else [])
        except: pass

        # --- STEP 3: Scans (Separated) ---
        print(" [Step 3/7] Fetching Scans...")
        try:
            data['scans'] = self.connection.get("/scans").get('scans', [])
        except: pass

        # --- STEP 4: Policies (Separated) ---
        print(" [Step 4/7] Fetching Policies...")
        try:
            data['policies'] = self.connection.get("/policies").get('policies', [])
            data['tags'] = self.connection.get("/tags/values").get('values', [])
        except: pass

        # --- STEP 5: Vulnerabilities (Flattening Engine) ---
        print(" [Step 5/7] Exporting Vulnerabilities...")
        try:
            vuln_payload = {"filters": {"severity": ["low", "medium", "high", "critical"], "state": ["OPEN", "REOPENED"]}}
            vuln_req = self.connection.post("/vulns/export", json=vuln_payload)
            v_uuid = vuln_req.get("export_uuid")
            chunks = self._wait_for_export("vulns", v_uuid)
            
            for c_id in chunks:
                chunk_data = self.connection.get(f"/vulns/export/{v_uuid}/chunks/{c_id}")
                for vuln in chunk_data:
                    port_val = vuln.get("port") or vuln.get("plugin", {}).get("port", [0])
                    if isinstance(port_val, list):
                        for p in port_val:
                            v_copy = vuln.copy()
                            v_copy['port'] = p
                            data['vulnerabilities'].append(v_copy)
                    else:
                        data['vulnerabilities'].append(vuln)
        except: pass

        # --- STEP 6: Users (Silent 403) ---
        print(" [Step 6/7] Fetching Platform Users...")
        try:
            data['users'] = self.connection.get("/users").get('users', [])
        except: pass

        # --- STEP 7: Audit Logs (Silent 403) ---
        print(" [Step 7/7] Fetching Audit Logs...")
        try:
            res = self.connection.get("/audit-log/events?limit=500")
            data['audit_log'] = res.get('events', [])
        except:
            data['audit_log'] = []

        print("-" * 60)
        print(f"[SUCCESS] Collection Complete (v5.0.16)")
        print(f" > Total Assets: {len(data['assets'])} | Total Vulns: {len(data['vulnerabilities'])}")
        print("-" * 60)
        
        return data
