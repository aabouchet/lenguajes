from tkinter import StringVar
from tkinter import DoubleVar
from tkinter import Label
from tkinter import Entry
import os
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import *
from modelo import BaseDeDatos
from tkinter import PhotoImage
from tkinter import Button


class Ventana:
    def __init__(self, window):
        self.base = BaseDeDatos()
        self.root = window

        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        os.chdir(directorio_actual)

        self.a_val, self.b_val, self.c_val, self.d_val = (
            StringVar(),
            StringVar(),
            StringVar(),
            StringVar(),
        )
        self.w_ancho = 20

        self.style = ttk.Style()
        self.style.configure(
            "Treeview",
            background="#B22222",
            foreground="#000000",
            fieldbackground="#B22222",
            rowheight=25,
        )

        self.tree = ttk.Treeview(
            self.root, columns=("Nombre", "Apellido", "Correo", "Contraseña", "Fecha")
        )
        self.tree.heading("#0", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellido", text="Apellido")
        self.tree.heading("Correo", text="Correo")
        self.tree.heading("Contraseña", text="Contraseña")
        self.tree.heading("Fecha", text="Fecha de suscripcion")
        self.tree.column("#0", width=50, minwidth=50)
        self.tree.grid(row=0, column=0, columnspan=6, padx=10, pady=10)

        self.label_nombre = tk.Label(self.root, text="Nombre:", bg="#CD5C5C")
        self.label_nombre.grid(row=1, column=0, padx=5, pady=5)
        self.entry_nombre = tk.Entry(self.root)
        self.entry_nombre.grid(row=2, column=1, padx=5, pady=5)

        self.label_apellido = tk.Label(self.root, text="Apellido:", bg="#CD5C5C")
        self.label_apellido.grid(row=2, column=0, padx=5, pady=5)
        self.entry_apellido = tk.Entry(self.root)
        self.entry_apellido.grid(row=2, column=1, padx=5, pady=5)

        self.label_correo = tk.Label(self.root, text="Correo:", bg="#CD5C5C")
        self.label_correo.grid(row=3, column=0, padx=5, pady=5)
        self.entry_correo = tk.Entry(self.root)
        self.entry_correo.grid(row=3, column=1, padx=5, pady=5)

        self.label_contraseña = tk.Label(self.root, text="Contraseña:", bg="#CD5C5C")
        self.label_contraseña.grid(row=4, column=0, padx=5, pady=5)
        self.entry_contraseña = tk.Entry(self.root, show="*")
        self.entry_contraseña.grid(row=4, column=1, padx=5, pady=5)

        self.imagen_agregar = PhotoImage(file="scr/agregar.png").subsample(2, 2)
        self.imagen_modificar = PhotoImage(file="scr/modificar.png").subsample(2, 2)
        self.imagen_eliminar = PhotoImage(file="scr/borrar.png").subsample(2, 2)

        self.entrada1 = Entry(self.root, textvariable=self.a_val, width=self.w_ancho)
        self.entrada1.grid(row=1, column=1)
        self.entrada2 = Entry(self.root, textvariable=self.b_val, width=self.w_ancho)
        self.entrada2.grid(row=2, column=1)
        self.entrada3 = Entry(self.root, textvariable=self.c_val, width=self.w_ancho)
        self.entrada3.grid(row=3, column=1)
        self.entrada4 = Entry(self.root, textvariable=self.d_val, width=self.w_ancho)
        self.entrada4.grid(row=4, column=1)

        self.boton_agregar = Button(
            self.root,
            image=self.imagen_agregar,
            text="agregar",
            command=lambda: self.base.agregar_datos(
                self.a_val.get(),
                self.b_val.get(),
                self.c_val.get(),
                self.d_val.get(),
                self.tree,
            ),
        )
        self.boton_agregar.grid(row=5, column=0, padx=10, pady=5)

        self.boton_modificar = Button(
            self.root,
            image=self.imagen_modificar,
            text="modificar",
            command=lambda: self.base.modificar_datos(
                self.a_val.get(),
                self.b_val.get(),
                self.c_val.get(),
                self.d_val.get(),
                self.tree,
                self.tree.item(self.tree.focus(), "text"),
            ),
        )
        self.boton_modificar.grid(row=5, column=1, padx=10, pady=5)

        self.boton_borrar = Button(
            self.root,
            image=self.imagen_eliminar,
            text="Borrar",
            command=lambda: self.base.eliminar_datos(
                self.tree, self.tree.item(self.tree.focus(), "text")
            ),
        )
        self.boton_borrar.grid(row=5, column=2, padx=10, pady=5)

        self.base.cargar_datos(self.tree)

        tree2 = ttk.Treeview(self.root, columns=("Nombre", "Cantidad"), height=1)
        tree2.heading("Nombre", text="Nombre")
        tree2.heading("Cantidad", text="Cantidad")
        tree2.column("#0", width=0, stretch=tk.NO)
        tree2.grid(row=6, column=3, columnspan=6, padx=10, pady=10)

        label_consulta = tk.Label(self.root, text="Consultar Nombre:", bg="#7B68EE")
        label_consulta.grid(row=6, column=0, padx=10, pady=5)
        entry_consulta = tk.Entry(self.root)
        entry_consulta.grid(row=6, column=1, padx=10, pady=5)

        self.boton_consultar = Button(
            self.root,
            text="Consultar",
            command=lambda: self.base.consultar_repetidos(entry_consulta.get(), tree2),
        )
        self.boton_consultar.grid(row=6, column=2, padx=10, pady=5)
