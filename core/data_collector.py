import time
from typing import Dict, Any

class TenableDataCollector:
    def __init__(self, connection):
        self.tio = connection.tio

    def collect_all(self) -> Dict[str, Any]:
        print("[*] Starting 7-Step Asynchronous Collection Sequence...")
        data = {}
        
        print(" [Step 1/7] Fetching Infrastructure...")
        data['scanners'] = self.tio.scanners.list()
        
        print(" [Step 2/7] Exporting Assets...")
        # Obtenemos el objeto de exportación
        asset_exp = self.tio.exports.assets()
        # El UUID real se extrae así:
        asset_uuid = asset_exp.uuid
        while True:
            status = self.tio.exports.status('assets', asset_uuid)
            if status.get('status') == 'FINISHED': break
            time.sleep(5)
        data['assets_raw'] = self.tio.exports.download_chunk('assets', asset_uuid, 1)

        print(" [Step 3/7] Fetching Scans & Policies...")
        data['scans'] = self.tio.scans.list()
        data['policies'] = self.tio.policies.list()

        print(" [Step 4/7] Fetching Tags...")
        data['tags'] = self.tio.tags.list()

        print(" [Step 5/7] Exporting Vulnerabilities...")
        vuln_exp = self.tio.exports.vulns()
        vuln_uuid = vuln_exp.uuid
        while True:
            status = self.tio.exports.status('vulns', vuln_uuid)
            if status.get('status') == 'FINISHED': break
            time.sleep(5)
        data['vulns_raw'] = self.tio.exports.download_chunk('vulns', vuln_uuid, 1)

        print(" [Step 6/7] Fetching Users...")
        data['users'] = self.tio.users.list()
        
        print(" [Step 7/7] Finalizing Master Data Map...")
        data['connectors'] = [] 

        print("[SUCCESS] Master Data Collection complete.")
        return data
