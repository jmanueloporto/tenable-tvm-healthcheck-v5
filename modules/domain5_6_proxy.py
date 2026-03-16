# VERSION: 5.1.1
"""
LAYER: Module / Governance
DESCRIPTION: Audit of user management using absolute detected values (44 users).
"""

class GovernanceValidator:
    def __init__(self, master_data):
        self.users = master_data.get('users', [])

    def validate_user_governance(self):
        # Captura del valor real absoluto detectado por la API
        actual_user_count = len(self.users)
        
        # Lógica de madurez: > 5 usuarios se considera un entorno saludable
        score = 5.0 if actual_user_count > 5 else 3.5
        status = f"Healthy ({actual_user_count} users detected)"
        
        return {
            'domain': 5,
            'title': 'Governance & User Management',
            'score': score,
            'observation': status
        }

def run_audit(master_data):
    """ Función puente para compatibilidad con el Orquestador V5.1.1 """
    validator = GovernanceValidator(master_data)
    result = validator.validate_user_governance()
    
    # Importación local para evitar dependencias circulares
    from core.models import Finding
    return [Finding(
        domain=result['domain'],
        title=result['title'],
        score=result['score'],
        observation=result['observation']
    )]
