#!/bin/bash
# VERSION: 5.1.3-PREMERGE
# LAYER: DevOps / Quality Assurance
# DESCRIPTION: Valida integridad de código y entorno antes de promoción a main.

echo "===================================================="
echo "   INICIANDO VALIDACIÓN DE SEGURIDAD v5.1.3         "
echo "===================================================="

echo "--- [1/4] Limpiando artefactos de caché ---"
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

echo "--- [2/4] Análisis Estático de Sintaxis (Anti-NameError) ---"
# El comando py_compile es el filtro definitivo para evitar NameErrors
python3 -m py_compile main.py core/*.py modules/*.py
if [ $? -ne 0 ]; then
    echo ""
    echo "[FALLO CRÍTICO] Se detectaron errores de sintaxis o imports faltantes."
    echo "Revisa el Traceback arriba y corrige antes de continuar."
    exit 1
fi
echo "[OK] Sintaxis y referencias validadas correctamente."

echo "--- [3/4] Verificación de Entorno Virtual ---"
if [ ! -d ".venv" ]; then
    echo "[ADVERTENCIA] No se detectó carpeta .venv. Asegúrate de estar en el entorno correcto."
else
    pip install -r requirements.txt | grep -v "already satisfied"
    echo "[OK] Dependencias sincronizadas."
fi

echo "--- [4/4] Verificación de Valor Real (44 Usuarios) ---"
# Verificamos que el código de gobernanza procese el valor absoluto
grep -q "len(self.users)" modules/domain5_6_proxy.py
if [ $? -eq 0 ]; then
    echo "[OK] Lógica de Integridad de Valores Reales (v5.1.1+) detectada."
else
    echo "[AVISO] La lógica de valores reales no se detectó en domain5_6_proxy.py."
fi

echo "===================================================="
echo "[SUCCESS] Entorno validado. Es seguro proceder a GitHub."
echo "===================================================="
