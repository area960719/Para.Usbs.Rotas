import os
import subprocess
import ctypes
import sys
import time

# --- ELEVACIÓN A ADMINISTRADOR ---
def es_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not es_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

def listar_discos():
    print("\n💽 Unidades detectadas en el sistema:")
    print("="*60)
    # Usamos WMIC para listar las unidades de forma limpia
    subprocess.run(['wmic', 'logicaldisk', 'get', 'deviceid,volumename,size,drivetype'], shell=True)
    print("="*60)
    print("Nota: El 'DriveType 2' suele ser un USB o disco extraíble.")

def formatear_unidad():
    listar_discos()
    
    letra = input("\n👉 Introduce la LETRA de la unidad a formatear (ej. E): ").strip().upper()
    
    if len(letra) != 1:
        print("❌ Error: Debes introducir solo una letra.")
        return
        
    # Doble confirmación para evitar accidentes
    confirmar = input(f"\n🚨 ¡ADVERTENCIA! Se borrarán TODOS los datos de la unidad {letra}:\n¿Estás completamente seguro? (escribe 'BORRAR' para confirmar): ")
    if confirmar != "BORRAR":
        print("Operación cancelada. No se borró nada.")
        return

    # Preguntar formato
    print("\nElige el formato de archivo:")
    print("1. FAT32 (Recomendado para USBs, compatible con radios, TVs, etc.)")
    print("2. NTFS (Para archivos de más de 4GB)")
    opcion_formato = input("Opción (1 o 2): ")
    
    fs = "fat32" if opcion_formato == '1' else "ntfs"
    
    print(f"\n⏳ Formateando unidad {letra}: a {fs.upper()}... Por favor espera.")
    
    # Crear el script para diskpart
    script = f"""select volume {letra}
clean
create partition primary
format fs={fs} quick
assign
exit
"""
    with open("script_diskpart.txt", "w") as f:
        f.write(script)
        
    try:
        # Ejecutar diskpart
        subprocess.run(['diskpart', '/s', 'script_diskpart.txt'], shell=True)
        print("\n✅ ¡Proceso finalizado! El USB/SD debería estar como nuevo.")
    except Exception as e:
        print(f"❌ Error al formatear: {e}")
    finally:
        # Limpiar el archivo temporal
        if os.path.exists("script_diskpart.txt"):
            os.remove("script_diskpart.txt")

# --- MENÚ PRINCIPAL ---
def menu_principal():
    while True:
        print("\n" + "="*50)
        print("💾 HERRAMIENTA DE REPARACIÓN DE USB / SD 💾")
        print("="*50)
        print("1. Listar Unidades Conectadas")
        print("2. Formatear y Reparar USB/SD (Borra todo)")
        print("3. Salir")
        print("="*50)
        
        opcion = input("Elige una opción (1-3): ")
        
        if opcion == '1':
            listar_discos()
        elif opcion == '2':
            formatear_unidad()
        elif opcion == '3':
            print("Saliendo del programa...")
            break
        else:
            print("❌ Opción no válida.")
        
        input("\nPresiona Enter para volver al menú...")

if __name__ == "__main__":
    menu_principal()
