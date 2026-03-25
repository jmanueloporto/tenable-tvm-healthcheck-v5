""" VERSION: 5.5.0-STABLE | STATUS: DOMAIN 1 READY """

from datetime import datetime

class RemediationAuditor:
    def __init__(self, data):
        self.data = data
        self.config = data.get('config', {})
        self.vulnerabilities = data.get('vulnerabilities', {}).get('list', [])

    def parse_date(self, date_str):
        try:
            if not date_str:
                return None
            clean_str = date_str.replace('Z', '+00:00')
            return datetime.fromisoformat(clean_str)
        except Exception:
            return None

    def calculate_mttr(self):
        fixed_vuls = [v for v in self.vulnerabilities if v.get('state', '').upper() == 'FIXED']
        if not fixed_vuls:
            return None

        total_days = 0
        valid_count = 0

        for vuln in fixed_vuls:
            first_found = vuln.get('first_found') or vuln.get('first_seen')
            last_fixed = vuln.get('last_fixed') or vuln.get('last_seen')
            
            if first_found and last_fixed:
                d1 = self.parse_date(first_found)
                d2 = self.parse_date(last_fixed)
                if d1 and d2:
                    delta = (d2 - d1).days
                    total_days += max(0, delta)
                    valid_count += 1
        
        if valid_count == 0:
            return None
            
        return total_days / valid_count

    def run_audit(self):
        findings = []
        sla_limit = self.config.get('internal_sla_critical', 30) 
        
        # 1. Lógica Original: SLA Breach Detected
        breaches = 0
        for vuln in self.vulnerabilities:
            if vuln.get('state', '').upper() in ['OPEN', 'ACTIVE', 'REOPENED']:
                age = vuln.get('age', 0)
                if age > sla_limit:
                    breaches += 1
                    
        if breaches > 0:
            findings.append({
                "domain": 4,
                "title": "SLA Breach Detected",
                "override_score": 2.0,
                "observation": f"Se detectaron {breaches} vulnerabilidades activas superando el SLA interno de {sla_limit} dias."
            })
        else:
            findings.append({
                "domain": 4,
                "title": "SLA Breach Detected",
                "override_score": 5.0,
                "observation": "Todas las vulnerabilidades activas estan dentro de los tiempos aceptables del SLA."
            })

        # 2. Nueva Lógica: MTTR Engine
        mttr_days = self.calculate_mttr()
        
        if mttr_days is None:
            findings.append({
                "domain": 4,
                "title": "SLA Performance: Global MTTR",
                "override_score": 3.0,
                "observation": "No hay suficientes vulnerabilidades en estado FIXED con fechas validas para calcular un MTTR historico."
            })
        else:
            if mttr_days > sla_limit:
                findings.append({
                    "domain": 4,
                    "title": "SLA Performance: Global MTTR",
                    "override_score": 2.0,
                    "observation": f"El MTTR global es de {mttr_days:.1f} dias, superando el limite establecido del SLA ({sla_limit} dias)."
                })
            else:
                findings.append({
                    "domain": 4,
                    "title": "SLA Performance: Global MTTR",
                    "override_score": 5.0,
                    "observation": f"Excelente tiempo de respuesta. El MTTR global es de {mttr_days:.1f} dias, operando dentro del SLA."
                })
                
        return findings
