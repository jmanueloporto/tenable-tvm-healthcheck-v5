""" VERSION: 5.5.0-STABLE | STATUS: DOMAIN 1 READY """
# VERSION: 5.3.4-FINAL
"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.3.4
LAYER: Presentation / Reporter
DESCRIPTION: Decoupled logic for generating human-readable TXT reports.
AUTHOR: Senior Software Architect
"""

from datetime import datetime
from typing import Dict, Any

class TXTReporter:
    """Handles visual formatting and file generation."""

    def generate(self, data: Dict[str, Any]) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"reports/health_report_{timestamp}.txt"
        
        try:
            with open(filepath, "w") as f:
                f.write("="*60 + "\n")
                f.write(f"{'TENABLE HEALTH CHECK REPORT V5.0.0':^60}\n")
                f.write(f"{f'Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}':^60}\n")
                f.write("="*60 + "\n\n")

                f.write("[1] METRICS OVERVIEW\n")
                f.write("-" * 20 + "\n")
                for key, val in data["metrics"].items():
                    f.write(f" > {key.replace('_', ' ').title()}: {val}\n")

                f.write("\n[2] AUDIT FINDINGS\n")
                f.write("-" * 20 + "\n")
                if not data["findings"]:
                    f.write("Status: No issues detected.\n")
                else:
                    for issue in data["findings"]:
                        f.write(f"[{issue['severity']}] {issue['module']}: {issue['description']}\n")
            
            return filepath
        except Exception as e:
            return f"Error: {str(e)}"
