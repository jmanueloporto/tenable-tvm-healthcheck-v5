""" VERSION: 5.4.0 | STATUS: Stable """
# VERSION: 5.3.4-FINAL
from core.models import Finding

class GovernanceValidator:
    def __init__(self, master_data):
        self.users = master_data.get('users', [])

    def validate_user_governance(self):
        # Captura real de los 44 usuarios detectados
        actual_user_count = len(self.users)
        penalty = 0.0 if actual_user_count > 5 else 1.5
        
        return Finding(
            title="User Inventory Integrity",
            domain=5,
            score=penalty,
            observation=f"Detected {actual_user_count} real users in Tenable platform.",
            recommendations=["Maintain periodic review of active users"]
        )

def run_audit(master_data):
    validator = GovernanceValidator(master_data)
    return [validator.validate_user_governance()]
