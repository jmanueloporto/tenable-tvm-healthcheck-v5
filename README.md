# V5-Tenable Health Check API Automation
**Current Version:** 5.3.3  
**Status:** FASE 3 FINALIZED - INTERACTIVE & ROBUST REPORTING

## Descripción
Plataforma avanzada de auditoría para Tenable VM. La versión 5.3.3 marca el cierre de la Fase 3, integrando una interfaz web basada en Flask, un disparador de auditoría en tiempo real (Web Trigger) y un motor de exportación de alta fidelidad que genera simultáneamente reportes en JSON (para dashboards), TXT (forense) y PDF (ejecutivo).

## Novedades de la v5.3.3
* **Web Orchestration:** Capacidad de ejecutar auditorías desde el navegador[cite: 115].
* **Triple-Engine Reporting:** Generación garantizada de archivos JSON, TXT y PDF[cite: 7, 107].
* **Failsafe PDF:** Corrección de truncamiento de texto y errores de codificación Latin-1/UTF-8[cite: 14].
* **Shadow IT Detection:** Reporte detallado de brecha de visibilidad (Gap Analysis)[cite: 61].

## Project Structure
\`\`\`plaintext
.
├── core/                       # Núcleo del Orquestador
│   ├── connection.py           # Conectividad API
│   ├── context_loader.py       # Carga de contexto estratégico
│   ├── data_collector.py       # Recolección de datos masiva
│   ├── models.py               # Golden Model de hallazgos
│   └── scoring.py              # Scoring con Contextual Override
├── web/                        # Interfaz de Usuario (v5.3.x)
│   ├── app.py                  # Servidor Flask & API Trigger
│   └── templates/
│       └── index.html          # Dashboard Radar Chart (Chart.js)
├── modules/                    # Motores de Auditoría
│   ├── domain1_assets.py       # Shadow IT & Inventory
│   ├── domain2_scans.py        # Scan Coverage
│   ├── domain3_risk.py         # Risk & VPR
│   ├── domain4_remediation.py  # SLA Tracking
│   └── domain5_6_proxy.py      # Governance Proxy
├── reports/                    # Salida de Datos
│   ├── export_engine.py        # Motor Triple (PDF/TXT/JSON)
│   └── latest_results.json     # Buffer para Dashboard
├── main.py                     # Orquestador Principal
└── README.md                   # Documentación v5.3.3
\`\`\`
