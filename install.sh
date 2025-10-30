#!/bin/bash

# Installation script for Multi-Country Camera Scanner
# Supports both Termux and Linux

echo "╔═══════════════════════════════════════╗"
echo "║ Multi-Country Camera Scanner Installer║"
echo "║        Credit: W8Team/W8SOJIB         ║"
echo "║          44 Countries Supported       ║"
echo "╚═══════════════════════════════════════╝"
echo ""
echo "[*] Developed by: W8Team/W8SOJIB"
echo "[*] Termux Compatible"
echo "[*] One-Click Operation"
echo ""

# Detect environment
if [ -d "$PREFIX" ] && [ -n "$ANDROID_ROOT" ]; then
    echo "[*] Termux environment detected"
    ENV="termux"
else
    echo "[*] Linux/Unix environment detected"
    ENV="linux"
fi

# Update package manager
if [ "$ENV" = "termux" ]; then
    echo "[*] Updating Termux packages..."
    pkg update -y
    pkg upgrade -y
    
    echo "[*] Installing Python..."
    pkg install python -y
else
    echo "[*] Checking Python installation..."
    if ! command -v python3 &> /dev/null; then
        echo "[!] Python3 not found. Please install Python3 first."
        exit 1
    fi
fi

# Install Python dependencies
echo "[*] Installing Python packages..."
pip install --upgrade pip

echo "[*] Installing required packages..."
pip install requests aiohttp pyfiglet

echo "[*] Installing optional packages..."
pip install colorama

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "╔═══════════════════════════════════════╗"
    echo "║   Installation Complete! ✓            ║"
    echo "╚═══════════════════════════════════════╝"
    echo ""
    echo "[✓] Ready to scan 44 countries!"
    echo ""
    echo "Run the scanner with:"
    echo "  python W8CameraHackV2.py"
    echo ""
    echo "Features:"
    echo "  • Select from 44 countries"
    echo "  • Automatic IP range download"
    echo "  • Automatic camera scanning"
    echo "  • One-click operation!"
    echo ""
else
    echo "[!] Some packages failed to install, but the script may still work."
    echo "[*] Try running: python W8CameraHackV2.py"
fi

