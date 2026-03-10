# V5-Tenable Health Check API Automation
**Version:** 5.0.19 (Phase 1 Final)
**Status:** Stable / Production Ready

## 1. Project Structure
- `main.py`: Orchestrator of the audit process.
- `core/`:
  - `connection.py`: API authentication and request handling.
  - `data_collector.py`: Fault-tolerant asynchronous data extraction.
  - `models.py`: Golden data model for findings and evidence.
  - `scoring.py`: Mathematical maturity calculation engine.
- `modules/`:
  - `domain1_assets.py`: Inventory visibility and agent health audit.
  - `domain2_scans.py`: Scan quality and authentication rate audit.
  - `domain3_risks.py`: VPR-based risk and density analysis.
  - `domain4_remediation.py`: Velocity (TTR) and coverage efficiency audit.
  - `domain5_6_proxy.py`: Identity hygiene and ecosystem proxy audit.
- `reports/`:
  - `export_engine.py`: Forensic PDF/TXT report generator.
  - `reports/`: Target directory for generated audit evidence.

## 2. Phase 1 Engineering Milestones
- **Asynchronous Data Parity:** Implemented POST-based export flows to ensure 1:1 parity with Tenable GUI.
- **Vulnerability Flattening:** Engine that splits multi-port vulnerabilities into individual findings for accurate risk density.
- **Fault Tolerance:** Robust try/except isolation for Step 1-7 collection, surviving 403 (Forbidden) and 405 (Method Not Allowed) errors.
- **Evidence Injection:** Automatic hostname/IP extraction into findings to eliminate "N/A" in forensic reports.
- **Golden Model:** Unified `Finding` class supporting `observation`, `source`, `confidence`, and `override_score`.

## 3. Quick Start
```bash
# Install dependencies
pip install requests fpdf

# Run full audit
python3 main.py
