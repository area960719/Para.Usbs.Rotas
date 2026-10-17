import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import subprocess
import ctypes
import sys
import os
import threading

# --- ELEVACIÓN A ADMINISTRADOR ---
def es_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not es_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

# Configuración de la apariencia moderna
ctk.set_appearance_mode("dark")  # Modo oscuro para colores nítidos
ctk.set_default_color_theme("blue")

class ReparadorUSBApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Panel de Control - Reparador USB Pro")
        self.geometry("850x500")
        self.resizable(False, False)

        # --- LAYOUT PRINCIPAL (2 Columnas) ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ==========================================
        # COLUMNA IZQUIERDA: Botones
        # ==========================================
        self.frame_botones = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.frame_botones.grid(row=0, column=0, sticky="nsew")
        
        self.lbl_titulo = ctk.CTkLabel(self.frame_botones, text="💾 USB REPAIR", font=ctk.CTkFont(size=22, weight="bold"), text_color="#00e5ff")
        self.lbl_titulo.pack(pady=(30, 20))

        # Combo para seleccionar unidad
        self.combo_unidades = ctk.CTkComboBox(self.frame_botones, values=["Buscando..."], width=220, font=ctk.CTkFont(size=13))
        self.combo_unidades.pack(pady=10)

        # Botón: Actualizar
        self.btn_actualizar = ctk.CTkButton(self.frame_botones, text="🔄 Buscar Unidades", width=220, height=40, corner_radius=20,
                                            font=ctk.CTkFont(size=14, weight="bold"), fg_color="#3498db", hover_color="#2980b9",
                                            command=self.cargar_unidades_hilo)
        self.btn_actualizar.pack(pady=15)

        # Botón: Formatear FAT32
        self.btn_formatear_fat = ctk.CTkButton(self.frame_botones, text="⚡ Formatear FAT32", width=220, height=40, corner_radius=20,
                                               font=ctk.CTkFont(size=14, weight="bold"), fg_color="#2ecc71", hover_color="#27ae60",
                                               command=lambda: self.confirmar_formateo("fat32"))
        self.btn_formatear_fat.pack(pady=10)

        # Botón: Formatear NTFS
        self.btn_formatear_ntfs = ctk.CTkButton(self.frame_botones, text="🔥 Formatear NTFS", width=220, height=40, corner_radius=20,
                                                font=ctk.CTkFont(size=14, weight="bold"), fg_color="#f39c12", hover_color="#d68910",
                                                command=lambda: self.confirmar_formateo("ntfs"))
        self.btn_formatear_ntfs.pack(pady=10)

        # Botón: Salir
        self.btn_salir = ctk.CTkButton(self.frame_botones, text="❌ Salir", width=220, height=40, corner_radius=20,
                                       font=ctk.CTkFont(size=14, weight="bold"), fg_color="#e74c3c", hover_color="#c0392b",
                                       command=self.destroy)
        self.btn_salir.pack(pady=(40, 10))

        # ==========================================
        # COLUMNA DERECHA: Consola en tiempo real
        # ==========================================
        self.frame_consola = ctk.CTkFrame(self, corner_radius=0, fg_color="#1e1e1e")
        self.frame_consola.grid(row=0, column=1, sticky="nsew")
        
        self.lbl_consola = ctk.CTkLabel(self.frame_consola, text="📟 Registro de Actividad en Tiempo Real", font=ctk.CTkFont(size=16, weight="bold"), text_color="#a6a6a6")
        self.lbl_consola.pack(anchor="w", padx=20, pady=(20, 5))

        self.txt_consola = ctk.CTkTextbox(self.frame_consola, width=500, height=400, corner_radius=10, 
                                          font=ctk.CTkFont(family="Consolas", size=13), fg_color="#121212", text_color="#00ffcc")
        self.txt_consola.pack(padx=20, pady=10, fill="both", expand=True)
        self.txt_consola.configure(state="disabled") # Solo lectura

        # Iniciar carga de unidades
        self.after(500, self.cargar_unidades_hilo)

    # --- FUNCIÓN PARA IMPRIMIR EN LA CONSOLA ---
    def log(self, mensaje):
        self.txt_consola.configure(state="normal")
        self.txt_consola.insert("end", mensaje + "\n")
        self.txt_consola.see("end") # Auto-scroll
        self.txt_consola.configure(state="disabled")

    # --- CARGAR UNIDADES EN UN HILO APARTE ---
    def cargar_unidades_hilo(self):
        self.log("🔄 Buscando unidades conectadas...")
        threading.Thread(target=self.cargar_unidades, daemon=True).start()

    def cargar_unidades(self):
        try:
            resultado = subprocess.check_output(['wmic', 'logicaldisk', 'get', 'deviceid,volumename,drivetype'], shell=True).decode('utf-8', errors='ignore')
            lineas = resultado.split('\n')
            unidades = []
            
            for linea in lineas:
                partes = linea.split()
                if len(partes) >= 2:
                    letra = partes[0]
                    tipo = partes[-1]
                    if len(letra) == 2 and letra.endswith(':'):
                        nombre = " ".join(partes[1:-1]) if len(partes) > 2 else "Extraíble"
                        # Mostramos solo tipo 2 (extraíbles) o todas por seguridad
                        if tipo == '2' or tipo == '3': 
                            unidades.append(f"{letra} - {nombre}")
            
            if not unidades:
                self.combo_unidades.configure(values=["No hay USBs detectados"])
                self.combo_unidades.set("No hay USBs detectados")
                self.log("⚠️ No se encontraron USBs o discos conectados.")
            else:
                self.combo_unidades.configure(values=unidades)
                self.combo_unidades.set(unidades[0])
                self.log(f"✅ Se encontraron {len(unidades)} unidades.")
        except Exception as e:
            self.log(f"❌ Error al buscar unidades: {e}")

    # --- CONFIRMAR Y FORMATEAR ---
    def confirmar_formateo(self, formato):
        seleccion = self.combo_unidades.get()
        if not seleccion or "No hay" in seleccion:
            messagebox.showwarning("Atención", "Selecciona una unidad válida primero.")
            return

        letra = seleccion.split(" - ")[0].replace(":", "")

        respuesta = messagebox.askyesno("🚨 ¡ADVERTENCIA CRÍTICA!", 
            f"¿Estás seguro de formatear la unidad {letra}: en {formato.upper()}?\n\n"
            "SE BORRARÁN TODOS LOS DATOS.")
        
        if respuesta:
            # Deshabilitar botones mientras formatea
            self.btn_formatear_fat.configure(state="disabled")
            self.btn_formatear_ntfs.configure(state="disabled")
            self.btn_actualizar.configure(state="disabled")
            
            threading.Thread(target=self.ejecutar_formateo, args=(letra, formato), daemon=True).start()

    def ejecutar_formateo(self, letra, formato):
        self.log(f"\n--- INICIANDO FORMATEO EN {letra}: ({formato.upper()}) ---")
        
        script = f"select volume {letra}\nclean\ncreate partition primary\nformat fs={formato} quick\nassign\nexit\n"
        with open("script_diskpart.txt", "w") as f:
            f.write(script)

        try:
            # Ejecutamos diskpart y leemos su salida en tiempo real
            proceso = subprocess.Popen(['diskpart', '/s', 'script_diskpart.txt'], 
                                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                       text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
            for linea in proceso.stdout:
                if linea.strip():
                    self.log(f"> {linea.strip()}")
            
            proceso.wait()
            
            if proceso.returncode == 0:
                self.log(f"✅ ¡Unidad {letra}: formateada con éxito!")
                messagebox.showinfo("Éxito", f"El USB {letra}: está listo para usarse.")
            else:
                self.log(f"❌ Error al formatear. Código: {proceso.returncode}")
                
        except Exception as e:
            self.log(f"❌ Error inesperado: {e}")
        finally:
            if os.path.exists("script_diskpart.txt"):
                os.remove("script_diskpart.txt")
            
            # Reactivar botones
            self.btn_formatear_fat.configure(state="normal")
            self.btn_formatear_ntfs.configure(state="normal")
            self.btn_actualizar.configure(state="normal")
            self.log("--- FIN DEL PROCESO ---\n")
            self.cargar_unidades_hilo()

if __name__ == "__main__":
    app = ReparadorUSBApp()
    app.mainloop()
