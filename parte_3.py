# SOLUCION DEL EJERCICIO 8.4 página 517


from tkinter import *
from tkinter import ttk, messagebox, filedialog
from enum import Enum
import os
import io

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False


class TipoCargo(Enum):
    DIRECTIVO = 'Directivo'
    ESTRATEGICO = 'Estratégico'
    OPERATIVO = 'Operativo'

class TipoGenero(Enum):
    MASCULINO = 'Masculino'
    FEMENINO = 'Femenino'

class Empleado:
    def __init__(self, nombre: str, apellidos: str, cargo: TipoCargo,
                 genero: TipoGenero, salario_dia: float, dias_trabajados: int,
                 otros_ingresos: float, pagos_salud: float, aporte_pensiones: float):
        self.nombre = nombre
        self.apellidos = apellidos
        self.cargo = cargo
        self.genero = genero
        self.salario_dia = salario_dia
        self.dias_trabajados = dias_trabajados
        self.otros_ingresos = otros_ingresos
        self.pagos_salud = pagos_salud
        self.aporte_pensiones = aporte_pensiones

    def calcular_nomina(self) -> float:
        return (self.salario_dia * self.dias_trabajados) + self.otros_ingresos - self.pagos_salud - self.aporte_pensiones


class ListaEmpleados:
    def __init__(self):
        self.lista = []

    def agregar(self, e: Empleado):
        self.lista.append(e)

    def convertir_matriz(self):
        datos = []
        for e in self.lista:
            datos.append((e.nombre, e.apellidos, f"{e.calcular_nomina():.2f}"))
        return datos

    def total_nomina(self) -> float:
        return sum(e.calcular_nomina() for e in self.lista)

    def convertir_texto(self) -> str:
        partes = []
        for e in self.lista:
            partes.append(
                f"Nombre = {e.nombre}\n"
                f"Apellidos = {e.apellidos}\n"
                f"Cargo = {e.cargo.value}\n"
                f"Genero = {e.genero.value}\n"
                f"Salario por dia = ${e.salario_dia:.2f}\n"
                f"Días trabajados = {e.dias_trabajados}\n"
                f"Otros ingresos = ${e.otros_ingresos:.2f}\n"
                f"Pagos por salud = ${e.pagos_salud:.2f}\n"
                f"Aporte pensiones = ${e.aporte_pensiones:.2f}\n"
                f"Sueldo mensual = ${e.calcular_nomina():.2f}\n---------\n"
            )
        partes.append(f"Total nómina = ${self.total_nomina():.2f}\n")
        return '\n'.join(partes)


class VentanaPrincipal(Tk):
    def __init__(self):
        super().__init__()
        self.title('Nómina')
        self.geometry('350x150')
        self.resizable(False, False)

        self.empleados = ListaEmpleados()
        self._crear_menu()

        lbl = Label(self, text='Programa de Nómina', font=('Arial', 14))
        lbl.pack(pady=20)

        info = Label(self, text='Use el menú "Menú" para agregar empleados, ver nómina o guardar archivo')
        info.pack()

    def _crear_menu(self):
        menubar = Menu(self)
        menu = Menu(menubar, tearoff=0)
        menu.add_command(label='Agregar empleado', command=self.abrir_agregar)
        menu.add_command(label='Calcular nómina', command=self.abrir_nomina)
        menu.add_separator()
        menu.add_command(label='Guardar archivo', command=self.guardar_archivo)
        menu.add_separator()
        menu.add_command(label='Generar diagramas (PNG)', command=self.generar_diagramas)
        menubar.add_cascade(label='Menú', menu=menu)
        self.config(menu=menubar)

    def abrir_agregar(self):
        VentanaAgregarEmpleado(self, self.empleados)

    def abrir_nomina(self):
        VentanaNomina(self, self.empleados)

    def guardar_archivo(self):
        if not self.empleados.lista:
            messagebox.showwarning('Aviso', 'No hay empleados para guardar.')
            return
        carpeta = filedialog.askdirectory(title='Seleccione carpeta para guardar Nómina.txt')
        if not carpeta:
            return
        ruta = os.path.join(carpeta, 'Nómina.txt')
        try:
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write(self.empleados.convertir_texto())
            messagebox.showinfo('Éxito', f'Archivo generado: {ruta}')
        except Exception as ex:
            messagebox.showerror('Error', f'No se pudo guardar el archivo:\n{ex}')

    def generar_diagramas(self):
        carpeta = filedialog.askdirectory(title='Seleccione carpeta para guardar diagramas (PNG)')
        if not carpeta:
            return
        if not PIL_AVAILABLE:
            messagebox.showwarning('Pillow no disponible', 'La generación de PNG requiere Pillow.\nInstale con: pip install pillow')
            return
        ruta1 = os.path.join(carpeta, 'diagrama_clases.png')
        ruta2 = os.path.join(carpeta, 'diagrama_casos_uso.png')

        try:
            generar_diagrama_clases_png(ruta1)
            generar_diagrama_casos_uso_png(ruta2)
            messagebox.showinfo('Éxito', f'Diagramas guardados:\n{ruta1}\n{ruta2}')
        except Exception as ex:
            messagebox.showerror('Error', f'No se pudieron generar diagramas:\n{ex}')


class VentanaAgregarEmpleado(Toplevel):
    def __init__(self, parent: Tk, lista: ListaEmpleados):
        super().__init__(parent)
        self.lista = lista
        self.title('Agregar Empleado')
        self.geometry('380x420')
        self.resizable(False, False)
        self._crear_componentes()

    def _crear_componentes(self):
        pady = 6
        padx = 8
        Label(self, text='Nombre:').place(x=20, y=20)
        self.c_nombre = Entry(self)
        self.c_nombre.place(x=160, y=20, width=180)

        Label(self, text='Apellidos:').place(x=20, y=50)
        self.c_apellidos = Entry(self)
        self.c_apellidos.place(x=160, y=50, width=180)

        Label(self, text='Cargo:').place(x=20, y=85)
        self.c_cargo = ttk.Combobox(self, values=[c.value for c in TipoCargo], state='readonly')
        self.c_cargo.current(2)
        self.c_cargo.place(x=160, y=85)

        Label(self, text='Género:').place(x=20, y=120)
        self.genero_var = StringVar(value=TipoGenero.MASCULINO.value)
        Radiobutton(self, text='Masculino', variable=self.genero_var, value=TipoGenero.MASCULINO.value).place(x=160, y=120)
        Radiobutton(self, text='Femenino', variable=self.genero_var, value=TipoGenero.FEMENINO.value).place(x=260, y=120)

        Label(self, text='Salario por día:').place(x=20, y=155)
        self.c_salario = Entry(self)
        self.c_salario.place(x=160, y=155)

        Label(self, text='Días trabajados (1-31):').place(x=20, y=190)
        self.spin_dias = Spinbox(self, from_=1, to=31)
        self.spin_dias.place(x=220, y=190, width=50)

        Label(self, text='Otros ingresos:').place(x=20, y=225)
        self.c_otros = Entry(self)
        self.c_otros.place(x=160, y=225)

        Label(self, text='Pagos por salud:').place(x=20, y=260)
        self.c_salud = Entry(self)
        self.c_salud.place(x=160, y=260)

        Label(self, text='Aporte pensiones:').place(x=20, y=295)
        self.c_pensiones = Entry(self)
        self.c_pensiones.place(x=160, y=295)

        Button(self, text='Agregar', command=self._agregar_empleado).place(x=80, y=340, width=80)
        Button(self, text='Limpiar', command=self._limpiar).place(x=200, y=340, width=80)

    def _limpiar(self):
        self.c_nombre.delete(0, 'end')
        self.c_apellidos.delete(0, 'end')
        self.c_salario.delete(0, 'end')
        self.spin_dias.delete(0, 'end')
        self.spin_dias.insert(0, '1')
        self.c_otros.delete(0, 'end')
        self.c_salud.delete(0, 'end')
        self.c_pensiones.delete(0, 'end')

    def _agregar_empleado(self):
        try:
            nombre = self.c_nombre.get().strip()
            apellidos = self.c_apellidos.get().strip()
            if not nombre or not apellidos:
                raise ValueError('Nombre y apellidos son obligatorios')
            cargo = TipoCargo(self.c_cargo.get())
            genero = TipoGenero(self.genero_var.get())
            salario = float(self.c_salario.get())
            dias = int(self.spin_dias.get())
            otros = float(self.c_otros.get() or 0)
            salud = float(self.c_salud.get() or 0)
            pensiones = float(self.c_pensiones.get() or 0)
            e = Empleado(nombre, apellidos, cargo, genero, salario, dias, otros, salud, pensiones)
            self.lista.agregar(e)
            messagebox.showinfo('Éxito', 'El empleado ha sido agregado')
            self._limpiar()
        except Exception as ex:
            messagebox.showerror('Error', f'Verifique los datos:\n{ex}')


class VentanaNomina(Toplevel):
    def __init__(self, parent: Tk, lista: ListaEmpleados):
        super().__init__(parent)
        self.lista = lista
        self.title('Nómina de Empleados')
        self.geometry('600x350')
        self.resizable(False, False)
        self._crear_componentes()

    def _crear_componentes(self):
        cols = ('Nombre', 'Apellidos', 'Cargo', 'Género', 'Salario mensual')
        self.tree = ttk.Treeview(self, columns=cols, show='headings')
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=110 if c != 'Salario mensual' else 140, anchor='center')
        self.tree.place(x=10, y=10, width=580, height=260)

        for e in self.lista.lista:
            self.tree.insert('', 'end', values=(e.nombre, e.apellidos, e.cargo.value, e.genero.value, f"${e.calcular_nomina():.2f}"))

        total = self.lista.total_nomina()
        Label(self, text=f'Total nómina mensual = ${total:.2f}', font=('Arial', 12)).place(x=10, y=280)

        Button(self, text='Guardar tabla como CSV', command=self._guardar_csv).place(x=420, y=280, width=170)

    def _guardar_csv(self):
        carpeta = filedialog.askdirectory(title='Seleccione carpeta para guardar nómina (CSV)')
        if not carpeta:
            return
        ruta = os.path.join(carpeta, 'Nomina.csv')
        try:
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write('Nombre,Apellidos,Cargo,Genero,Salario mensual\n')
                for e in self.lista.lista:
                    f.write(f'{e.nombre},{e.apellidos},{e.cargo.value},{e.genero.value},{e.calcular_nomina():.2f}\n')
            messagebox.showinfo('Éxito', f'CSV guardado: {ruta}')
        except Exception as ex:
            messagebox.showerror('Error', f'No se pudo guardar CSV:\n{ex}')


# -------------------------------
# 🔧 GENERACIÓN DE DIAGRAMA DE CLASES (NO CAMBIÓ)
# -------------------------------

def generar_diagrama_clases_png(ruta: str, ancho=900, alto=500):
    if not PIL_AVAILABLE:
        raise RuntimeError('Pillow no está disponible')

    img = Image.new('RGB', (ancho, alto), 'white')
    d = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype('DejaVuSans.ttf', 14)
    except Exception:
        font = ImageFont.load_default()

    cajas = [
        ('Empleado', 50, 50,
         ['- nombre: String', '- apellidos: String', '- cargo: TipoCargo', '- genero: TipoGenero',
          '- salario_dia: double', '- dias_trabajados: int', '- otros_ingresos: double',
          '- pagos_salud: double', '- aporte_pensiones: double', '+ calcular_nomina()']),
        ('ListaEmpleados', 450, 50,
         ['- lista: List[Empleado]', '+ agregar(e)', '+ convertir_matriz()', '+ convertir_texto()', '+ total_nomina()']),
    ]

    for titulo, x, y, atributos in cajas:
        w = 380
        h = 30 + 20 * len(atributos)

        d.rectangle([x, y, x + w, y + h], outline='black')
        d.rectangle([x, y, x + w, y + 30], outline='black', fill='#dddddd')
        d.text((x + 8, y + 6), titulo, font=font, fill='black')

        yy = y + 36
        for a in atributos:
            d.text((x + 8, yy), a, font=font, fill='black')
            yy += 18

    d.line([(430, 100), (450, 100)], fill='black', width=2)
    d.polygon([(445, 95), (450, 100), (445, 105)], fill='black')

    img.save(ruta)


# -------------------------------
# 🔧 GENERACIÓN DE DIAGRAMA DE CASOS DE USO (CORREGIDO)
# -------------------------------

def generar_diagrama_casos_uso_png(ruta: str, ancho=900, alto=500):
    if not PIL_AVAILABLE:
        raise RuntimeError('Pillow no está disponible')

    img = Image.new('RGB', (ancho, alto), 'white')
    d = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype('DejaVuSans.ttf', 14)
    except Exception:
        font = ImageFont.load_default()

    # Actor
    d.text((40, 80), 'Usuario', font=font)
    d.ellipse([20, 120, 60, 160], outline='black')
    d.line([(40, 160), (40, 220)], fill='black')

    # Casos de uso
    casos = ['Agregar empleado', 'Calcular nómina', 'Guardar archivo']
    x0 = 200
    y0 = 80

    for i, c in enumerate(casos):
        x = x0 + i * 220

        # Dibujo del óvalo
        d.ellipse([x, y0, x + 180, y0 + 80], outline='black')

        # Obtención del tamaño del texto usando textbbox()
        bbox = d.textbbox((0, 0), c, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]

        # Centrando el texto dentro del óvalo
        d.text((x + (180 - w) / 2, y0 + (80 - h) / 2), c, font=font, fill='black')

        # Línea actor → caso de uso
        d.line([(80, 140), (x, 140)], fill='black')

    img.save(ruta)


if __name__ == '__main__':
    app = VentanaPrincipal()
    app.mainloop()