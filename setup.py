#!/usr/bin/env python3
"""
Script de configuración inicial para BizFlow
"""
import os
import sys
import subprocess


def run_command(command, description):
    """Ejecuta un comando y maneja errores"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True,
                                capture_output=True, text=True)
        print(f"✅ {description} completado: {result}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e.stderr}")
        return False


def main():
    print("🚀 Configurando BizFlow - Sistema de Gestión de Ventas")
    print("=" * 50)

    # Verificar si estamos en el directorio correcto
    if not os.path.exists('manage.py'):
        print(
            "❌ Error: Ejecuta este script desde el directorio raíz "
            "del proyecto"
        )
        sys.exit(1)

    # Instalar dependencias restantes
    print("\n📦 Instalando dependencias...")
    dependencies = [
        "python-decouple==3.8",
        "Pillow==10.1.0"
    ]

    for dep in dependencies:
        if not run_command(f"pip install {dep}", f"Instalando {dep}"):
            print(f"⚠️  No se pudo instalar {dep}, continúa manualmente")

    # Crear migraciones
    if run_command("python manage.py makemigrations", "Creando migraciones"):
        run_command("python manage.py migrate", "Aplicando migraciones")

    # Crear superusuario
    print("\n👤 Para crear un superusuario, ejecuta:")
    print("python manage.py createsuperuser")

    print("\n🎉 ¡Configuración completada!")
    print("\n📋 Próximos pasos:")
    print("1. Configura tu base de datos MySQL en el archivo .env")
    print("2. Ejecuta: python manage.py createsuperuser")
    print("3. Ejecuta: python manage.py runserver")
    print("4. Visita http://127.0.0.1:8000 para ver tu aplicación")
    print(
        "5. Visita http://127.0.0.1:8000/admin para el panel de administración"
    )


if __name__ == "__main__":
    main()
