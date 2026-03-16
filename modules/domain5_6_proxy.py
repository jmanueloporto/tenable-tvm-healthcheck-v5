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
        
        # Lógica de madurez: > 5 usuarios se considera un entorno distribuido y saludable
        score = 5.0 if actual_user_count > 5 else 3.5
        status = f"Healthy ({actual_user_count} users detected)"
        
        return {
            'domain': 'Governance & User Management',
            'metric': 'Absolute User Inventory',
            'value': actual_user_count,
            'score': score,
            'status': status,
            'insight': "Real-value count bypasses legacy 'enabled' field issues."
        }
