#!/bin/bash

# Walletive - Ejecutor para Linux/macOS
# =====================================

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}"
echo "================================================================"
echo "                         WALLETIVE"
echo "                   Finanzas Personales"
echo "================================================================"
echo -e "${NC}"

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

echo "🚀 Iniciando aplicación..."
echo ""

# Verificar si Python 3 está disponible
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 no encontrado"
    echo ""
    echo "Ejecuta primero './init_walletive.sh' para configurar el entorno"
    exit 1
fi

# Verificar si el proyecto está inicializado
if [ ! -f "walletive.db" ]; then
    print_warning "Base de datos no encontrada"
    echo ""
    echo "Ejecutando inicialización automática..."
    echo ""
    python3 dev_init.py
    echo ""
fi

print_status "Ejecutando Walletive..."
echo ""
print_info "Para detener la aplicación, cierra la ventana de Walletive"
print_info "o presiona Ctrl+C en esta terminal"
echo ""

# Ejecutar la aplicación
python3 main.py

if [ $? -eq 0 ]; then
    echo ""
    print_status "Walletive cerrado correctamente"
else
    echo ""
    print_error "Error ejecutando la aplicación"
    echo ""
    echo "Si es la primera vez, ejecuta './init_walletive.sh' primero"
    exit 1
fi
