import sqlite3
from datetime import datetime
import re
import tkinter as tk
import os
from obs import Sujeto
import socket


def log(func):
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        with open("decorador.txt", "a") as file:
            file.write(f"Función: {func.__name__}\n")
            file.write(f"Argumentos: {args}\n")
            file.write(f"Fecha y Hora: {datetime.now()}\n")
            file.write("\n")
        return result

    return wrapper


class BaseDeDatos(Sujeto):
    def __init__(self):
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        os.chdir(directorio_actual)

        self.con = sqlite3.connect("mibase.db")
        self.cursor = self.con.cursor()
        self.crear_tabla()

    def crear_tabla(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS datos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            apellido TEXT,
            correo TEXT,
            contraseña TEXT,
            fecha TEXT
            )
            """
        )
        self.con.commit()

    def obtener_ultimo_id(self):
        self.cursor.execute("SELECT MAX(id) FROM datos")
        resultado = self.cursor.fetchone()
        if resultado and resultado[0] is not None:
            return resultado[0]
        else:
            return 0

    @log
    def agregar_datos(self, nombre, apellido, correo, contraseña, tree):
        try:
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if not nombre or not apellido or not correo or not contraseña:
                raise ValueError("Todos los campos son obligatorios")

            if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", nombre):
                raise ValueError("El nombre solo puede contener letras")

            if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", apellido):
                raise ValueError("El apellido solo puede contener letras")

            ultimo_id = self.obtener_ultimo_id()
            nuevo_id = ultimo_id + 1

            self.cursor.execute(
                "INSERT INTO datos (id, nombre, apellido, correo, contraseña, fecha) VALUES (?, ?, ?, ?, ?, ?)",
                (nuevo_id, nombre, apellido, correo, contraseña, fecha),
            )
            self.con.commit()
            self.cargar_datos(tree)
            tk.messagebox.showinfo("Éxito", "Los datos se guardaron exitosamente")
            self.notificar(nombre, apellido, correo, contraseña, "agregar")
        except ValueError as e:
            tk.messagebox.showerror("Error", str(e))
        except sqlite3.Error as e:
            self.con.rollback()
            tk.messagebox.showerror("Error de la base de datos", str(e))

    def modificar_datos(self, nombre, apellido, correo, contraseña, tree, id):
        self.cursor.execute(
            "UPDATE datos SET nombre = ?, apellido = ?, correo = ?, contraseña = ? WHERE id = ?",
            (nombre, apellido, correo, contraseña, id),
        )
        self.con.commit()
        self.notificar(nombre, apellido, correo, contraseña, "modificar")
        self.cargar_datos(tree)

    def eliminar_datos(self, tree, id):
        self.cursor.execute("DELETE FROM datos WHERE id = ?", (id,))
        self.con.commit()
        self.notificar(id, "eliminar")
        self.cargar_datos(tree)

    def cargar_datos(self, tree):
        self.crear_tabla()
        tree.delete(*tree.get_children())
        self.cursor.execute("SELECT * FROM datos")
        datos = self.cursor.fetchall()
        for dato in datos:
            id = dato[0]
            nombre = dato[1]
            apellido = dato[2]
            correo = dato[3]
            contraseña = dato[4]
            fecha = dato[5]
            tree.insert(
                "", "end", text=id, values=(nombre, apellido, correo, contraseña, fecha)
            )

    def consultar_repetidos(self, nombre, tree):
        self.cursor.execute(
            "SELECT nombre, COUNT(nombre) FROM datos WHERE nombre = ? GROUP BY nombre",
            (nombre,),
        )
        resultado = self.cursor.fetchone()
        if resultado:
            nombre_repetido, cantidad = resultado
            tree.delete(*tree.get_children())
            tree.insert("", "end", values=(nombre_repetido, cantidad))
        else:
            tree.delete(*tree.get_children())
            tree.insert("", "end", values=("No encontrado", 0))
