# V5-Tenable Health Check API Automation
**Current Version:** 5.3.3
**Status:** FASE 3 FINALIZED - INTERACTIVE & ROBUST REPORTING

## Descripción
Plataforma avanzada de auditoría para Tenable VM. La versión 5.3.3 marca el cierre de la Fase 3, integrando una interfaz web basada en Flask, un disparador de auditoría en tiempo real (Web Trigger) y un motor de exportación de alta fidelidad que genera simultáneamente reportes en JSON (para dashboards), TXT (forense) y PDF (ejecutivo). [cite: 7, 114]

## Novedades de la v5.3.3
* **Web Orchestration:** Capacidad de ejecutar auditorías desde el navegador. 
* **Triple-Engine Reporting:** Generación garantizada de archivos JSON, TXT y PDF. [cite: 107, 108]
* **Failsafe PDF:** Corrección de truncamiento de texto y errores de codificación Latin-1/UTF-8. [cite: 14, 15]
* **Shadow IT Detection:** Reporte detallado de brecha de visibilidad (Gap Analysis). [cite: 61, 63]

## Project Structure
\`\`\`plaintext
.
├── core/                       # Núcleo del Orquestador
│   ├── connection.py           # Conectividad API [cite: 83]
│   ├── context_loader.py       # Carga de contexto estratégico [cite: 87]
│   ├── data_collector.py       # Recolección de datos masiva [cite: 92]
│   ├── models.py               # Golden Model de hallazgos [cite: 91]
│   └── scoring.py              # Scoring con Contextual Override [cite: 89]
├── web/                        # Interfaz de Usuario (v5.3.x)
│   ├── app.py                  # Servidor Flask & API Trigger [cite: 114]
│   └── templates/
│       └── index.html          # Dashboard Radar Chart (Chart.js)
├── modules/                    # Motores de Auditoría
│   ├── domain1_assets.py       # Shadow IT & Inventory [cite: 61]
│   ├── domain2_scans.py        # Scan Coverage [cite: 69]
│   ├── domain3_risk.py         # Risk & VPR [cite: 21, 22]
│   ├── domain4_remediation.py  # SLA Tracking [cite: 44]
│   └── domain5_6_proxy.py      # Governance Proxy [cite: 77]
├── reports/                    # Salida de Datos
│   ├── export_engine.py        # Motor Triple (PDF/TXT/JSON) [cite: 107]
│   └── latest_results.json     # Buffer para Dashboard [cite: 10]
├── main.py                     # Orquestador Principal [cite: 116]
└── README.md                   # Documentación v5.3.3
\`\`\`
