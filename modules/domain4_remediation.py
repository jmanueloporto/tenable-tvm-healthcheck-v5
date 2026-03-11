"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.1.3
LAYER: Business / Modules
DESCRIPTION: SLA Compliance Engine. Analyzes first_found against strategic context.
AUTHOR: Senior Software Architect
"""

from core.models import Finding
from typing import List, Dict, Any
from datetime import datetime, timezone

def run_audit(master_data: Dict[str, Any]) -> List[Finding]:
    all_findings: List[Finding] = []
    domain_id = 4
    source_tag = "api"
    
    try:
        context = master_data.get('context', {})
        vulns = master_data.get('vulnerabilities', [])
        
        # 1. Extraer SLA Estratégico (v5.1.2)
        sla_critical = context.get('internal_sla_critical', 30)
        
        # 2. Filtrado y Análisis de Violaciones
        violations = []
        now = datetime.now(timezone.utc)
        
        # Filtro: Critical + Open/Active
        critical_open = [v for v in vulns if str(v.get('severity')).lower() == 'critical' 
                         and str(v.get('state')).lower() in ['open', 'reopened', 'active']]
        
        for v in critical_open:
            ff_str = v.get('first_found')
            if ff_str:
                try:
                    # Normalización ISO 8601 a UTC para cálculo de edad
                    ff_dt = datetime.fromisoformat(ff_str.replace('Z', '+00:00'))
                    age_days = (now - ff_dt).days
                    
                    if age_days > sla_critical:
                        violations.append(v)
                except (ValueError, TypeError):
                    continue

        # 3. Generación de Hallazgos Estratégicos
        if violations:
            all_findings.append(Finding(
                title="Critical Risk: SLA Breach Detected",
                domain=domain_id,
                score=5.0,
                observation=f"Se detectaron {len(violations)} vulnerabilidades Criticas abiertas que superan el SLA interno de {sla_critical} dias.",
                recommendations=[
                    f"Priorizar la remediacion de los {len(violations)} hallazgos fuera de SLA",
                    "Revisar cuellos de botella en el proceso de parcheo",
                    "Validar si los activos afectados requieren ventanas de mantenimiento urgentes"
                ]
            ))
        else:
            all_findings.append(Finding(
                title="SLA Compliance: Healthy Status",
                domain=domain_id,
                score=1.0,
                observation=f"No se detectaron vulnerabilidades Criticas que superen el SLA de {sla_critical} dias.",
                recommendations=["Mantener el ritmo actual de remediacion", "Monitorear proactivamente nuevos hallazgos"]
            ))

    except Exception as e:
        all_findings.append(Finding(
            title="Module Error: Domain 4",
            domain=domain_id,
            score=1.0,
            observation=f"Error en calculo de SLA: {str(e)}",
            recommendations=["Verificar estructura de first_found en la API"]
        ))

    return all_findings
