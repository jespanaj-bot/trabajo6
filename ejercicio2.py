#EJERCIO 8.5 página 546
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Diccionario de habitaciones: estado y tarifa
habitaciones = {
    "101": {"estado": "Disponible", "tarifa": 100},
    "102": {"estado": "Disponible", "tarifa": 120},
    "103": {"estado": "Disponible", "tarifa": 150},
}

# Registro de huéspedes
huespedes = {}

# Función para registrar huésped
def registrar_huesped():
    ventana_registro = tk.Toplevel()
    ventana_registro.title("Registrar Huésped")
    ventana_registro.geometry("300x250")

    tk.Label(ventana_registro, text="Nombre del Huésped:").pack(pady=5)
    nombre_entry = tk.Entry(ventana_registro)
    nombre_entry.pack(pady=5)

    tk.Label(ventana_registro, text="Selecciona la habitación:").pack(pady=5)
    combo = ttk.Combobox(
        ventana_registro, 
        values=[h for h, info in habitaciones.items() if info["estado"] == "Disponible"]
    )
    combo.pack(pady=5)

    tk.Label(ventana_registro, text="Fecha de ingreso (DD/MM/AAAA):").pack(pady=5)
    fecha_entry = tk.Entry(ventana_registro)
    fecha_entry.pack(pady=5)

    def guardar():
        nombre = nombre_entry.get()
        habitacion = combo.get()
        fecha_ingreso = fecha_entry.get()

        if not nombre or not habitacion or not fecha_ingreso:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        try:
            fecha_ingreso_dt = datetime.strptime(fecha_ingreso, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido")
            return

        habitaciones[habitacion]["estado"] = "No disponible"
        huespedes[habitacion] = {"nombre": nombre, "fecha_ingreso": fecha_ingreso_dt}
        messagebox.showinfo("Éxito", f"Huésped {nombre} registrado en habitación {habitacion}")
        ventana_registro.destroy()

    tk.Button(ventana_registro, text="Registrar", command=guardar).pack(pady=10)

# Función para salida de huésped
def salida_huesped():
    ventana_salida = tk.Toplevel()
    ventana_salida.title("Salida de Huésped")
    ventana_salida.geometry("300x250")

    tk.Label(ventana_salida, text="Número de habitación:").pack(pady=5)
    habitacion_entry = tk.Entry(ventana_salida)
    habitacion_entry.pack(pady=5)

    tk.Label(ventana_salida, text="Fecha de salida (DD/MM/AAAA):").pack(pady=5)
    fecha_entry = tk.Entry(ventana_salida)
    fecha_entry.pack(pady=5)

    def calcular_total():
        habitacion = habitacion_entry.get()
        fecha_salida = fecha_entry.get()

        if habitacion not in huespedes:
            messagebox.showerror("Error", "Habitación no está ocupada")
            return
        
        try:
            fecha_salida_dt = datetime.strptime(fecha_salida, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido")
            return
        
        fecha_ingreso_dt = huespedes[habitacion]["fecha_ingreso"]
        dias = (fecha_salida_dt - fecha_ingreso_dt).days
        dias = max(dias, 1)  # mínimo 1 día
        total = dias * habitaciones[habitacion]["tarifa"]

        messagebox.showinfo(
            "Total a Pagar", 
            f"Huésped: {huespedes[habitacion]['nombre']}\nHabitación: {habitacion}\nDías: {dias}\nTotal: ${total}"
        )

        # Liberar habitación
        habitaciones[habitacion]["estado"] = "Disponible"
        del huespedes[habitacion]
        ventana_salida.destroy()

    tk.Button(ventana_salida, text="Calcular Total y Registrar Salida", command=calcular_total).pack(pady=10)

# Menú principal
root = tk.Tk()
root.title("Sistema Hotelero")
root.geometry("300x200")

tk.Label(root, text="Menú Principal", font=("Arial", 16)).pack(pady=10)
tk.Button(root, text="Registrar Huésped", width=25, command=registrar_huesped).pack(pady=5)
tk.Button(root, text="Salida de Huésped", width=25, command=salida_huesped).pack(pady=5)
tk.Button(root, text="Salir", width=25, command=root.quit).pack(pady=5)

root.mainloop()
