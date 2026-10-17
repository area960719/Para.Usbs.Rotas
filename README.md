# 🛠️ Para_Usbs_Rotas

Herramienta de escritorio profesional diseñada para talleres de reparación de PC. Permite detectar, reparar y formatear memorias USB y tarjetas SD de manera rápida y segura, solucionando problemas de virus, errores de lectura o particiones corruptas.

## ✨ Características

*   **Interfaz Gráfica Moderna:** Diseño oscuro con botones redondeados y colores nítidos, construido con `customtkinter`.
*   **Consola en Tiempo Real:** Visualiza exactamente lo que el programa está haciendo paso a paso (creación de particiones, limpieza de disco, etc.).
*   **Doble Formato:** Permite formatear en **FAT32** (ideal para compatibilidad universal) o **NTFS** (para archivos de más de 4GB).
*   **Auto-Elevación:** El programa solicitará permisos de Administrador automáticamente al abrirse, ya que es necesario para manipular los discos.
*   **Compilado con GitHub Actions:** No requiere instalar Python en la PC de destino. Se distribuye como un único archivo ejecutable `.exe`.

## 🚀 ¿Cómo usarlo?

1. Descarga el archivo `Para.Usbs.Rotas.exe` desde la sección de **Releases** o **Actions** (Artifacts) de este repositorio.
2. Conecta la memoria USB o tarjeta SD dañada a tu PC.
3. Ejecuta el archivo `.exe`. Acepta la ventana de permisos de Administrador que aparecerá.
4. En la interfaz, haz clic en **"🔄 Buscar Unidades"** para actualizar la lista de dispositivos conectados.
5. Selecciona tu USB en el menú desplegable.
6. Haz clic en **"⚡ Formatear FAT32"** o **"🔥 Formatear NTFS"** según tus necesidades.
7. Confirma la advertencia y observa el progreso en la consola de la derecha.

## ⚠️ ADVERTENCIA CRÍTICA

> **Esta herramienta utiliza el comando `diskpart` de Windows para borrar y recrear las particiones.**
> Al formatear una unidad, **TODOS LOS DATOS SE PERDERÁN PERMANENTEMENTE**. Asegúrate de seleccionar la letra de unidad correcta antes de confirmar. El autor no se hace responsable de la pérdida de datos por mal uso.

## 🛠️ Detalles Técnicos (Para Desarrolladores)

Si deseas modificar o compilar este proyecto por tu cuenta:

*   **Lenguaje:** Python 3.11
*   **Librerías principales:** `customtkinter`, `subprocess`, `ctypes`.
*   **Sistema de compilación:** GitHub Actions (PyInstaller).
*   **Archivo principal:** `reparar_usb_pro.py`

Para compilar en GitHub Actions, el archivo `.github/workflows/build.yml` está configurado para generar el ejecutable de forma automática en cada *push* a la rama `main`.

## 📸 Vista Previa
*(Interfaz oscura con botones ovalados y consola de comandos en tiempo real).*

---
*Desarrollado para uso interno del taller.*
