#EJERICIO 3 

import tkinter as tk
from tkinter import messagebox, simpledialog

class Contacto:
    def __init__(self, nombres, apellidos, fecha_nacimiento, direccion, telefono, correo):
        self.nombres = nombres
        self.apellidos = apellidos
        self.fecha_nacimiento = fecha_nacimiento
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo

class ListaContactos:
    def __init__(self):
        self.lista = []

    def agregar_contacto(self, contacto):
        self.lista.append(contacto)

class VentanaContacto:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda de Contactos")
        self.lista_contactos = ListaContactos()

        # Etiquetas
        tk.Label(root, text="Nombres:").grid(row=0, column=0)
        tk.Label(root, text="Apellidos:").grid(row=1, column=0)
        tk.Label(root, text="Fecha de Nacimiento:").grid(row=2, column=0)
        tk.Label(root, text="Dirección:").grid(row=3, column=0)
        tk.Label(root, text="Teléfono:").grid(row=4, column=0)
        tk.Label(root, text="Correo:").grid(row=5, column=0)

        # Campos de texto
        self.campo_nombres = tk.Entry(root)
        self.campo_apellidos = tk.Entry(root)
        self.campo_fecha = tk.Entry(root)
        self.campo_direccion = tk.Entry(root)
        self.campo_telefono = tk.Entry(root)
        self.campo_correo = tk.Entry(root)

        self.campo_nombres.grid(row=0, column=1)
        self.campo_apellidos.grid(row=1, column=1)
        self.campo_fecha.grid(row=2, column=1)
        self.campo_direccion.grid(row=3, column=1)
        self.campo_telefono.grid(row=4, column=1)
        self.campo_correo.grid(row=5, column=1)

        # Lista de contactos
        self.lista = tk.Listbox(root, width=80)
        self.lista.grid(row=6, column=0, columnspan=2, pady=10)

        # Botón Agregar
        tk.Button(root, text="Agregar", command=self.agregar_contacto).grid(row=7, column=0, columnspan=2)

        # Botón para seleccionar fecha (sin tkcalendar)
        tk.Button(root, text="Seleccionar Fecha", command=self.seleccionar_fecha).grid(row=2, column=2)

    def seleccionar_fecha(self):
        fecha = simpledialog.askstring("Fecha de Nacimiento", "Ingrese la fecha (DD/MM/AAAA):")
        if fecha:
            self.campo_fecha.delete(0, tk.END)
            self.campo_fecha.insert(0, fecha)

    def agregar_contacto(self):
        nombres = self.campo_nombres.get()
        apellidos = self.campo_apellidos.get()
        fecha = self.campo_fecha.get()
        direccion = self.campo_direccion.get()
        telefono = self.campo_telefono.get()
        correo = self.campo_correo.get()

        if not nombres or not apellidos or not fecha or not direccion or not telefono or not correo:
            messagebox.showinfo("Error", "No se permiten campos vacíos")
            return

        contacto = Contacto(nombres, apellidos, fecha, direccion, telefono, correo)
        self.lista_contactos.agregar_contacto(contacto)
        self.lista.insert(tk.END, f"{nombres} - {apellidos} - {fecha} - {direccion} - {telefono} - {correo}")

        # Limpiar campos
        self.campo_nombres.delete(0, tk.END)
        self.campo_apellidos.delete(0, tk.END)
        self.campo_fecha.delete(0, tk.END)
        self.campo_direccion.delete(0, tk.END)
        self.campo_telefono.delete(0, tk.END)
        self.campo_correo.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaContacto(root)
    root.mainloop()
