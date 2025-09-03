#!/usr/bin/env python3
"""
Script para ejecutar la API de Xafiro en modo headless (sin navegador)
"""
import uvicorn
from app_headless import app

if __name__ == "__main__":
    print("🚀 Iniciando Xafiro Data Extraction API (Modo Headless)...")
    print("🔒 Modo discreto: SIN navegador visible")
    print("📋 Documentación disponible en: http://localhost:8002/docs")
    print("🔧 API disponible en: http://localhost:8002")
    print("⚡ Ventajas: Más rápido, discreto y eficiente")

    uvicorn.run(
        "app_headless:app",
        host="0.0.0.0",
        port=8002,
        reload=True,
        log_level="info"
    )