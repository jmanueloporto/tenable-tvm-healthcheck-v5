# V5-Tenable Health Check API Automation

**Current Version:** 5.4.2  
**Status:** STABLE - PURE API ARCHITECTURE & MTTR ENGINE

## Description
Advanced technical and executive auditing platform for Tenable Vulnerability Management. Version 5.4.2 marks a milestone in the project's maturity, consolidating a purist data collection engine (Pure API) that guarantees total fidelity with the real infrastructure (without GUI distortions), and incorporates the new mathematical engine for MTTR calculation.

## New Features and Key Characteristics (v5.4.2)
* **Pure API Sensor Discovery:** Exact and auditable classification of sensors by querying native endpoints[cite: 3, 23].
* **MTTR Engine (Domain 4):** Deep analysis of vulnerabilities in FIXED state to calculate Mean Time to Remediate[cite: 30].
* **Triple-Engine Reporting:** Infallible export in JSON, TXT, and PDF (via FPDF)[cite: 30].

## Repository Architecture (Git Flow)
* **main (Production):** Stable, untouchable branch for functional and sealed code.
* **develop (Development):** Engineering laboratory for building and testing new domains.

## Project Structure
```text
tenable-tvm-healthcheck-v5/
├── core/                   # Core Orchestrator Engine (Layer 1)
├── web/                    # Web User Interface (Flask)
├── modules/                # Audit Engines (Layer 2)
├── main.py                 # CLI Main Orchestrator
└── README.md               # Official Documentation
