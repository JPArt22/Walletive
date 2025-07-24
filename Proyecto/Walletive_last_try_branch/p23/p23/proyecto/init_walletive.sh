#!/bin/bash

# Walletive - Inicializador para Linux/macOS
# =========================================

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}"
echo "================================================================"
echo "                    WALLETIVE - INIT DESARROLLO"
echo "================================================================"
echo -e "${NC}"
echo "Este script configurará automáticamente todo el entorno de"
echo "desarrollo para Walletive."
echo ""

# Función para imprimir mensajes de estado
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Verificar si Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 no está instalado"
    echo ""
    echo "Por favor instala Python 3:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  macOS: brew install python3"
    echo "  CentOS/RHEL: sudo dnf install python3 python3-pip"
    exit 1
fi

print_status "Python 3 encontrado"

# Verificar si pip está disponible
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 no está disponible"
    echo ""
    echo "Instala pip3:"
    echo "  Ubuntu/Debian: sudo apt install python3-pip"
    echo "  macOS: generalmente viene con Python 3"
    exit 1
fi

print_status "pip3 encontrado"

# Detectar el sistema operativo y dar instrucciones para dependencias del sistema
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    print_info "Sistema Linux detectado"
    echo ""
    print_warning "Asegúrate de tener las dependencias del sistema instaladas:"
    echo "  Ubuntu/Debian:"
    echo "    sudo apt update"
    echo "    sudo apt install python3-pyqt5 python3-pyqt5-dev qtbase5-dev"
    echo ""
    echo "  CentOS/RHEL/Fedora:"
    echo "    sudo dnf install python3-qt5 python3-qt5-devel qt5-qtbase-devel"
    echo ""
elif [[ "$OSTYPE" == "darwin"* ]]; then
    print_info "Sistema macOS detectado"
    echo ""
    print_warning "Para macOS, asegúrate de tener Xcode Command Line Tools:"
    echo "    xcode-select --install"
    echo ""
fi

echo "Presiona Enter para continuar con la instalación automática..."
read

# Hacer ejecutable el script de Python limpio y ejecutarlo
chmod +x dev_init_clean.py
python3 dev_init_clean.py

if [ $? -eq 0 ]; then
    echo ""
    print_status "Configuración completa!"
    echo ""
    echo "Para ejecutar Walletive:"
    echo "  ./run_walletive.sh"
    echo "  o directamente: python3 main.py"
else
    print_error "Error durante la configuración"
    exit 1
fi
