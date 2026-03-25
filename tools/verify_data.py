""" VERSION: 5.5.0-STABLE | STATUS: DOMAIN 1 READY """
# VERSION: 5.3.4-FINAL
import os
import json
import requests
from dotenv import load_dotenv

def get_evidence():
    print("[*] Iniciando extracción de evidencia forense...")
    load_dotenv()
    
    # Configurar conexión usando las variables de tu .env
    access_key = os.getenv('TENABLE_ACCESS_KEY')
    secret_key = os.getenv('TENABLE_SECRET_KEY')
    url = os.getenv('TENABLE_URL', 'https://cloud.tenable.com')
    
    headers = {
        "accept": "application/json",
        "X-ApiKeys": f"accessKey={access_key};secretKey={secret_key}"
    }
    
    evidence = {}

    try:
        # 1. Validar Usuarios (Para Dominios 5 y 6)
        print(" -> Consultando usuarios...")
        user_resp = requests.get(f"{url}/users", headers=headers)
        if user_resp.status_code == 200:
            users = user_resp.json().get('users', [])
            evidence['users_total'] = len(users)
            evidence['users_active'] = [{"name": u.get('name'), "username": u.get('username')} 
                                        for u in users if u.get('enabled')]
        
        # 2. Validar Escáneres (Para Dominio 2)
        print(" -> Consultando escáneres...")
        scan_resp = requests.get(f"{url}/scanners", headers=headers)
        if scan_resp.status_code == 200:
            scanners = scan_resp.json().get('scanners', [])
            evidence['scanners'] = [{"name": s.get('name'), "status": s.get('status')} for s in scanners]

        # Guardar los datos en un archivo JSON
        with open("evidence.json", "w") as f:
            json.dump(evidence, f, indent=4)
            
        print("\n[SUCCESS] Datos reales extraídos y guardados en 'evidence.json'")
        
    except Exception as e:
        print(f"[ERROR] Falló la extracción: {str(e)}")

if __name__ == "__main__":
    get_evidence()
