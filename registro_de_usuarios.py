import tkinter as tk
from tkinter import messagebox, ttk
from collections import deque
from tkcalendar import DateEntry

class EstructuraDatosAfiliado:
    def __init__(self, tipoIdentificacion, numeroIdentificacion, nombreCompleto,
                 ingresosActuales, servicioDeseado, modalidadEmpleo,
                 tarifaAfiliacion, fechaAfiliacion):
        self.tipoIdentificacion   = tipoIdentificacion
        self.numeroIdentificacion = numeroIdentificacion
        self.nombreCompleto       = nombreCompleto
        self.ingresosActuales     = ingresosActuales
        self.servicioDeseado      = servicioDeseado
        self.modalidadEmpleo      = modalidadEmpleo
        self.tarifaAfiliacion     = tarifaAfiliacion
        self.fechaAfiliacion      = fechaAfiliacion

    def calcularTarifa(self):
        ingresos  = self.ingresosActuales
        modalidad = self.modalidadEmpleo
        servicio  = self.servicioDeseado

        if modalidad == "Empleado":
            if   1000000 <= ingresos <= 2000000: tarifa = 45000
            elif 2000000 <  ingresos <= 3000000: tarifa = 60000
            elif 3000000 <  ingresos <= 4000000: tarifa = 75000
            elif 4000000 <  ingresos <= 5000000: tarifa = 90000
            else:                                tarifa = 150000
        else:
            if   1000000 <= ingresos <= 2000000: tarifa = 10000
            elif 2000000 <  ingresos <= 3000000: tarifa = 20000
            elif 3000000 <  ingresos <= 4000000: tarifa = 30000
            elif 4000000 <  ingresos <= 5000000: tarifa = 40000
            else:                                tarifa = 80000

        if   servicio == "Ingreso a parque":    tarifa += 2500
        elif servicio == "Curso de formación":  tarifa += 7500
        elif servicio == "Paquete de viaje":    tarifa += 10000
        elif servicio == "Medicina preventiva": tarifa += ingresos * 0.10

        self.tarifaAfiliacion = tarifa
        return tarifa

class Login:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Login - Compensándote")
        self.ventana.geometry("400x250")
        self.ventana.resizable(False, False)

        menuBar    = tk.Menu(self.ventana)
        menuAcerca = tk.Menu(menuBar, tearoff=0)
        menuAcerca.add_command(label="Acerca de", command=self.mostrarAcercaDe)
        menuBar.add_cascade(label="Menú", menu=menuAcerca)
        self.ventana.config(menu=menuBar)

        tk.Label(self.ventana, text="FORMULARIO DE INICIO DE SESIÓN",
                 font=("Arial", 12, "bold")).pack(pady=20)
        tk.Label(self.ventana, text="* Clave:").pack()
        self.campoClave = tk.Entry(self.ventana, show="*", width=30)
        self.campoClave.pack(pady=5)

        frameBotones = tk.Frame(self.ventana)
        frameBotones.pack(pady=20)
        tk.Button(frameBotones, text="Ingresar", width=10,
                  command=self.validarClave).grid(row=0, column=0, padx=5)
        tk.Button(frameBotones, text="Salir", width=10,
                  command=self.ventana.destroy).grid(row=0, column=1, padx=5)

        self.ventana.mainloop()

    def validarClave(self):
        if self.campoClave.get() == "Caja":
            self.ventana.destroy()
            FormularioAfiliados()
        else:
            messagebox.showerror("Error", "Contraseña incorrecta. Intente de nuevo.")
            self.campoClave.delete(0, tk.END)

    def mostrarAcercaDe(self):
        messagebox.showinfo("Información",
            "Caja Compensándote\n"
            "Desarrollo de Aplicación - Python Tkinter\n"
            "Estudiante: Tu Nombre Completo\n"   # <-- Cambia esto
            "Grupo: XX"                           # <-- Cambia esto
        )


class FormularioAfiliados:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Caja Compensándote – Control de Afiliados")
        self.ventana.geometry("900x700")
        self.ventana.resizable(False, False)

        # Estructuras de datos en memoria
        self.pila  = []
        self.cola  = deque()
        self.lista = []

        frameSuperior = tk.LabelFrame(self.ventana,
                                      text="─── REGISTRO DE AFILIADOS ───",
                                      padx=10, pady=10)
        frameSuperior.pack(fill="x", padx=10, pady=5)

        tk.Label(frameSuperior, text="* Tipo de estructura:").grid(
            row=0, column=0, sticky="w", pady=3)
        self.varEstructura = tk.StringVar()
        ttk.Combobox(frameSuperior, textvariable=self.varEstructura,
                     values=["Pila", "Cola", "Lista"],
                     state="readonly", width=25).grid(row=0, column=1, sticky="w", pady=3)

        tk.Label(frameSuperior, text="* Tipo de identificación:").grid(
            row=1, column=0, sticky="w", pady=3)
        self.varTipoId = tk.StringVar()
        ttk.Combobox(frameSuperior, textvariable=self.varTipoId,
                     values=["CC", "CE", "NUIP", "PAS"],
                     state="readonly", width=25).grid(row=1, column=1, sticky="w", pady=3)

        tk.Label(frameSuperior, text="* Nro. de identificación:").grid(
            row=2, column=0, sticky="w", pady=3)
        self.varNumId = tk.StringVar()
        tk.Entry(frameSuperior, textvariable=self.varNumId,
                 width=27).grid(row=2, column=1, sticky="w", pady=3)

        tk.Label(frameSuperior, text="* Nombre completo:").grid(
            row=3, column=0, sticky="w", pady=3)
        self.varNombre = tk.StringVar()
        tk.Entry(frameSuperior, textvariable=self.varNombre,
                 width=27).grid(row=3, column=1, sticky="w", pady=3)

        tk.Label(frameSuperior, text="* Ingresos actuales:").grid(
            row=4, column=0, sticky="w", pady=3)
        self.varIngresos = tk.StringVar()
        campoIngresos = tk.Entry(frameSuperior, textvariable=self.varIngresos, width=27)
        campoIngresos.grid(row=4, column=1, sticky="w", pady=3)
        campoIngresos.bind("<FocusOut>", lambda e: self.calcularTarifa())

        tk.Label(frameSuperior, text="* Servicio deseado:").grid(
            row=5, column=0, sticky="w", pady=3)
        self.varServicio = tk.StringVar()
        cboServicio = ttk.Combobox(frameSuperior, textvariable=self.varServicio,
                                   values=["Subsidio de desempleo", "Ingreso a parque",
                                           "Curso de formación", "Paquete de viaje",
                                           "Medicina preventiva"],
                                   state="readonly", width=25)
        cboServicio.grid(row=5, column=1, sticky="w", pady=3)
        cboServicio.bind("<<ComboboxSelected>>", lambda e: self.calcularTarifa())

        tk.Label(frameSuperior, text="* Modalidad de empleo:").grid(
            row=6, column=0, sticky="w", pady=3)
        self.varModalidad = tk.StringVar(value="Empleado")
        frameRadio = tk.Frame(frameSuperior)
        frameRadio.grid(row=6, column=1, sticky="w")
        tk.Radiobutton(frameRadio, text="Empleado", variable=self.varModalidad,
                       value="Empleado", command=self.calcularTarifa).pack(side="left")
        tk.Radiobutton(frameRadio, text="Independiente", variable=self.varModalidad,
                       value="Independiente", command=self.calcularTarifa).pack(side="left")

        tk.Label(frameSuperior, text="Tarifa de afiliación ($):").grid(
            row=7, column=0, sticky="w", pady=3)
        self.varTarifa = tk.StringVar()
        tk.Entry(frameSuperior, textvariable=self.varTarifa,
                 state="readonly", width=27).grid(row=7, column=1, sticky="w", pady=3)

        tk.Label(frameSuperior, text="* Fecha de afiliación:").grid(
            row=8, column=0, sticky="w", pady=3)
        self.campoFecha = DateEntry(frameSuperior, width=24, date_pattern="dd/mm/yyyy")
        self.campoFecha.grid(row=8, column=1, sticky="w", pady=3)

        frameBotReg = tk.Frame(frameSuperior)
        frameBotReg.grid(row=9, column=0, columnspan=2, pady=10)
        tk.Button(frameBotReg, text="Registrar", width=12,
                  command=self.registrarAfiliado).pack(side="left", padx=5)
        tk.Button(frameBotReg, text="Limpiar", width=12,
                  command=self.limpiarFormulario).pack(side="left", padx=5)

        frameInferior = tk.LabelFrame(self.ventana,
                                      text="─── DATOS DE AFILIADOS ───",
                                      padx=10, pady=10)
        frameInferior.pack(fill="both", expand=True, padx=10, pady=5)

        frameVer = tk.Frame(frameInferior)
        frameVer.pack(fill="x")

        tk.Label(frameVer, text="* Ver estructura:").pack(side="left")
        self.varVerEstructura = tk.StringVar(value="Pila")
        cboVer = ttk.Combobox(frameVer, textvariable=self.varVerEstructura,
                               values=["Pila", "Cola", "Lista"],
                               state="readonly", width=10)
        cboVer.pack(side="left", padx=5)
        cboVer.bind("<<ComboboxSelected>>", lambda e: self.actualizarTreeview())

        tk.Label(frameVer, text="Reporte:").pack(side="left", padx=(20, 0))
        self.varReporte = tk.StringVar()
        tk.Entry(frameVer, textvariable=self.varReporte,
                 state="readonly", width=20).pack(side="left", padx=5)

        tk.Button(frameVer, text="Reporte",  width=10,
                  command=self.generarReporte).pack(side="left", padx=5)
        tk.Button(frameVer, text="Eliminar", width=10,
                  command=self.eliminarAfiliado).pack(side="left", padx=5)
        tk.Button(frameVer, text="Salir",    width=10,
                  command=self.ventana.destroy).pack(side="left", padx=5)

        columnas = ("tipoId","numId","nombre","ingresos","servicio","modalidad","tarifa","fecha")
        self.treeview = ttk.Treeview(frameInferior, columns=columnas,
                                      show="headings", height=8)
        encabezados = ["Tipo Id","Número Id","Nombre","Ingresos",
                       "Servicio","Modalidad","Tarifa","Fecha"]
        anchos = [70, 100, 150, 100, 160, 100, 90, 90]
        for col, enc, ancho in zip(columnas, encabezados, anchos):
            self.treeview.heading(col, text=enc)
            self.treeview.column(col, width=ancho, anchor="center")

        sb = ttk.Scrollbar(frameInferior, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=sb.set)
        self.treeview.pack(side="left", fill="both", expand=True, pady=5)
        sb.pack(side="right", fill="y", pady=5)

        self.ventana.mainloop()

    def calcularTarifa(self):
        try:
            ingresos = float(self.varIngresos.get())
        except ValueError:
            return
        servicio  = self.varServicio.get()
        modalidad = self.varModalidad.get()
        if not servicio:
            return
        obj = EstructuraDatosAfiliado("","",""  ,ingresos, servicio, modalidad, 0, "")
        tarifa = obj.calcularTarifa()
        self.varTarifa.set(f"${tarifa:,.0f}")

    def registrarAfiliado(self):
        estructura = self.varEstructura.get()
        tipoId     = self.varTipoId.get()
        numId      = self.varNumId.get().strip()
        nombre     = self.varNombre.get().strip()
        ingresos   = self.varIngresos.get().strip()
        servicio   = self.varServicio.get()
        modalidad  = self.varModalidad.get()
        tarifa     = self.varTarifa.get()
        fecha      = self.campoFecha.get()

        if not estructura:
            messagebox.showwarning("Atención", "Seleccione el tipo de estructura."); return
        if not tipoId:
            messagebox.showwarning("Atención", "Seleccione el tipo de identificación."); return
        if not numId.isdigit():
            messagebox.showwarning("Atención", "El número de identificación solo debe contener números."); return
        if not nombre.replace(" ","").isalpha():
            messagebox.showwarning("Atención", "El nombre solo debe contener letras."); return
        if not ingresos.isdigit():
            messagebox.showwarning("Atención", "Los ingresos solo deben contener números."); return
        if not servicio:
            messagebox.showwarning("Atención", "Seleccione el servicio deseado."); return
        if not tarifa:
            messagebox.showwarning("Atención", "Calcule primero la tarifa."); return

        nuevo = EstructuraDatosAfiliado(tipoId, numId, nombre, float(ingresos),
                                        servicio, modalidad, 0, fecha)
        nuevo.calcularTarifa()

        if   estructura == "Pila":  self.pila.append(nuevo)
        elif estructura == "Cola":  self.cola.append(nuevo)
        elif estructura == "Lista": self.lista.append(nuevo)

        messagebox.showinfo("Éxito", f"Afiliado registrado en la {estructura}.")
        self.limpiarFormulario()
        self.actualizarTreeview()

    def limpiarFormulario(self):
        self.varEstructura.set("")
        self.varTipoId.set("")
        self.varNumId.set("")
        self.varNombre.set("")
        self.varIngresos.set("")
        self.varServicio.set("")
        self.varModalidad.set("Empleado")
        self.varTarifa.set("")

    def actualizarTreeview(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        estructura = self.varVerEstructura.get()
        if   estructura == "Pila":  datos = list(reversed(self.pila))
        elif estructura == "Cola":  datos = list(self.cola)
        else:                       datos = self.lista
        for a in datos:
            self.treeview.insert("", "end", values=(
                a.tipoIdentificacion, a.numeroIdentificacion, a.nombreCompleto,
                f"${a.ingresosActuales:,.0f}", a.servicioDeseado, a.modalidadEmpleo,
                f"${a.tarifaAfiliacion:,.0f}", a.fechaAfiliacion
            ))

    def generarReporte(self):
        estructura = self.varVerEstructura.get()
        if estructura == "Pila":
            if not self.pila:
                self.varReporte.set("Sin datos"); return
            total = sum(a.tarifaAfiliacion for a in self.pila)
            self.varReporte.set(f"${total:,.0f}")
            messagebox.showinfo("Reporte - Pila", f"Suma de tarifas:\n${total:,.0f}")
        elif estructura == "Cola":
            cantidad = len(self.cola)
            self.varReporte.set(str(cantidad))
            messagebox.showinfo("Reporte - Cola", f"Cantidad de afiliados:\n{cantidad}")
        elif estructura == "Lista":
            if not self.lista:
                self.varReporte.set("Sin datos"); return
            promedio = sum(a.ingresosActuales for a in self.lista) / len(self.lista)
            self.varReporte.set(f"${promedio:,.0f}")
            messagebox.showinfo("Reporte - Lista", f"Promedio de ingresos:\n${promedio:,.0f}")

    def eliminarAfiliado(self):
        estructura = self.varVerEstructura.get()
        if estructura == "Pila":
            if not self.pila:
                messagebox.showwarning("Atención", "La pila está vacía."); return
            if messagebox.askyesno("Confirmar",
                    f"¿Desapilar a '{self.pila[-1].nombreCompleto}'?"):
                self.pila.pop()
                self.actualizarTreeview()
                messagebox.showinfo("Éxito", "Registro desapilado.")

        elif estructura == "Cola":
            if not self.cola:
                messagebox.showwarning("Atención", "La cola está vacía."); return
            if messagebox.askyesno("Confirmar",
                    f"¿Desencolar a '{self.cola[0].nombreCompleto}'?"):
                self.cola.popleft()
                self.actualizarTreeview()
                messagebox.showinfo("Éxito", "Registro desencolado.")

        elif estructura == "Lista":
            if not self.lista:
                messagebox.showwarning("Atención", "La lista está vacía."); return
            ventanaBuscar = tk.Toplevel(self.ventana)
            ventanaBuscar.title("Eliminar de Lista")
            ventanaBuscar.geometry("300x150")
            tk.Label(ventanaBuscar, text="Ingrese el Nro. de identificación:").pack(pady=10)
            varBuscar = tk.StringVar()
            tk.Entry(ventanaBuscar, textvariable=varBuscar, width=25).pack()

            def confirmarEliminacion():
                encontrado = next((a for a in self.lista
                                   if a.numeroIdentificacion == varBuscar.get().strip()), None)
                if not encontrado:
                    messagebox.showwarning("No encontrado",
                        "No existe afiliado con ese ID.", parent=ventanaBuscar); return
                if messagebox.askyesno("Confirmar",
                        f"¿Eliminar a '{encontrado.nombreCompleto}'?", parent=ventanaBuscar):
                    self.lista.remove(encontrado)
                    self.actualizarTreeview()
                    ventanaBuscar.destroy()
                    messagebox.showinfo("Éxito", "Afiliado eliminado.")

            tk.Button(ventanaBuscar, text="Buscar y Eliminar",
                      command=confirmarEliminacion).pack(pady=10)

if __name__ == "__main__":
    Login()