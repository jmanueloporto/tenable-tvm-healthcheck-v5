# VERSION: 5.1.1-FINAL
"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.1.1
LAYER: Core / Context
DESCRIPTION: Loads manual business context from JSON.
"""
import json
import os

def load_context():
    path = "data/context_input.json"
    if not os.path.exists(path):
        return {}
    try:
        with open(path, 'r') as f:
            data = json.load(f)
            return data.get('context', {})
    except Exception:
        return {}

def display_context_info(context):
    print("="*60)
    print("         STRATEGIC CONTEXT LOADED (v5.1.0)")
    print("="*60)
    print(f" > Expected Assets     : {context.get('expected_assets', 'N/A')}")
    print(f" > Critical SLA (Days) : {context.get('internal_sla_critical', 'N/A')}")
    print(f" > Maint. Windows      : {'Enabled' if context.get('maintenance_windows') else 'Disabled'}")
    print("-"*60)
    print("[TIP] To adjust these values, edit: data/context_input.json")
    print("="*60)
