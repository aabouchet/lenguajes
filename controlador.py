from tkinter import *
from vista import Ventana
from modelo import BaseDeDatos
import threading
from obs import ConcreteObserverA
import obs
from cliente import enviar_informacion_al_servidor


class Controller:
    def __init__(self, root):
        self.root = root
        self.objeto_vista = Ventana(self.root)
        self.base_de_datos = BaseDeDatos()
        self.observer_a = ConcreteObserverA(self.base_de_datos)
        threading.Thread(target=self.run_client, daemon=True).start()

        self.root.mainloop()

    def run_client(self):
        enviar_informacion_al_servidor()


if __name__ == "__main__":
    root = Tk()
    mi_app = Controller(root)
