import requests
from core.connection import TenableConnection

def test():
    print("--- [DIAGNÓSTICO DE CONEXIÓN V5] ---")
    try:
        # Instanciar la lógica que ya creamos en core/
        conn = TenableConnection()
        headers = conn.get_headers()
        url = f"{conn.base_url}/scanners"
        
        print(f"[*] Intentando conectar a: {conn.base_url}")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("[SUCCESS] Conexión establecida exitosamente.")
            print(f"[INFO] Código de estado: {response.status_code}")
            # Mostrar cuántos scanners ve la cuenta para confirmar permisos
            scanners_count = len(response.json().get('scanners', []))
            print(f"[INFO] Scanners detectados: {scanners_count}")
        else:
            print(f"[FAILURE] Tenable respondió con error.")
            print(f"[DEBUG] Código: {response.status_code}")
            print(f"[DEBUG] Respuesta: {response.text}")

    except Exception as e:
        print(f"[ERROR] No se pudo iniciar la conexión: {e}")

if __name__ == "__main__":
    test()
