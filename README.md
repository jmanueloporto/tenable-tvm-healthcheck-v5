# V5-Tenable Health Check API Automation
**Current Version: 5.0.6

## Descripción
Plataforma avanzada de asesoría de postura de seguridad para Tenable Vulnerability Management [cite: 10-11].
Actualmente en la **Fase 1 (API-Driven)**, extrayendo la verdad objetiva de la plataforma sin intervención humana [cite: 42-43, 256].

## Avances Actuales (v5.0.6)
- **Core Architecture:** Motor de recolección asíncrona de 7 pasos usando REST API directa (rendimiento de ejecución en ~15-20s) [cite: 39-40, 819-822]. Orquestador desacoplado y Motor de Puntuación dinámico[cite: 197].
- **Módulos de Auditoría Operativos:**
  - **Domain 1:** Asset Visibility & Inventory [cite: 22]
  - **Domain 2:** Scanning Operations & Data Quality [cite: 23]
  - **Domain 3:** Risk Prioritization & Analysis [cite: 24]
  - **Domain 4:** Remediation & Response [cite: 25]

## Arquitectura del Repositorio (GitOps)
El proyecto sigue un flujo de trabajo de ramas estructurado para proteger el código:
- `main`: Rama de producción / estable. Contiene únicamente versiones consolidadas y etiquetadas (tags).
- `develop`: Rama de desarrollo continuo. Aquí se integran los nuevos módulos y características (Feature integration) antes de cada release.

## Ejecución
1. Activar entorno virtual: `source .venv/bin/activate`
2. Ejecutar orquestador: `python3 main.py`
