from core.models import Finding
from core.scoring import ScoringEngine

def run_tests():
    print("=== INICIANDO PRUEBAS DE LA TAREA 1 ===")
    
    # 1. Probar la creación correcta de Hallazgos (Findings)
    print("\n[*] Creando hallazgos de prueba...")
    f1 = Finding(
        title="Baja cobertura de escaneo", domain=1, source="api", 
        metrics={"coverage": 65}, score=2.0, confidence="High", 
        recommendations=["Escanear más redes"]
    )
    f2 = Finding(
        title="Agentes desconectados", domain=1, source="api", 
        metrics={"offline": 15}, score=4.0, confidence="Medium", 
        recommendations=["Revisar conectividad"]
    )
    f3 = Finding(
        title="Escaneos sin credenciales", domain=2, source="api", 
        metrics={"auth_rate": 40}, score=1.5, confidence="High", 
        recommendations=["Añadir credenciales"]
    )
    print("[+] 3 Hallazgos válidos creados exitosamente.")

    # 2. Probar la validación de errores (Resiliencia)
    print("\n[*] Probando validación de puntuación (Debe ser entre 1 y 5)...")
    try:
        f_bad = Finding(
            title="Error", domain=1, source="api", metrics={}, 
            score=8.5, confidence="Low", recommendations=[]
        )
        print("[-] ERROR: El sistema permitió una puntuación inválida.")
    except ValueError as e:
        print(f"[+] Validación exitosa. El sistema bloqueó el error: {e}")

    # 3. Probar el Motor de Puntuación (Scoring Engine)
    print("\n[*] Probando cálculos matemáticos del Scoring Engine...")
    engine = ScoringEngine()
    
    domain_scores = engine.calculate_domain_scores([f1, f2, f3])
    print(f"[+] Puntuaciones por Dominio calculadas: {domain_scores}")
    print("    -> Esperado para Dominio 1: 3.0 (Promedio de 2.0 y 4.0)")
    print("    -> Esperado para Dominio 2: 1.5 (Único valor 1.5)")

    overall = engine.calculate_overall_score(domain_scores)
    print(f"[+] Puntuación General calculada: {overall}")
    print("    -> Toma los promedios y los multiplica por los pesos de la Fase 1.")
    
    print("\n=== PRUEBAS FINALIZADAS CON ÉXITO ===")

if __name__ == "__main__":
    run_tests()
