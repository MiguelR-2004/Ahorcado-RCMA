import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Asegúrate de tener Pillow instalado
import random
import os  # Para verificar la existencia de las imágenes

# Palabras para el juego
PALABRAS = [
    "Python", "Diccionarios", "Listas", "Interfaz", "Programacion", "GitHub", 
    "Pseudocodigo", "Variables", "Constantes", "Ejecutar", "Estructuras", 
    "Cadenas", "Repositorio", "Sistemas", "Codigos", "Atributos", "Entorno", 
    "Pillow", "Botones", "Etiquetas", "Funciones", "Ventana", "Raton", 
    "Tkinter", "Componentes", "Texto", "Version", "Sintaxis", "Imagen", 
    "Contenedor"
]

class Ahorcado:
    def __init__(self, root):
        self.root = root
        self.root.title("Miguel Angel Renteria Contreras / 2-D")
        self.root.geometry("800x575")  # Ajustar tamaño de la ventana
        self.root.configure(bg="skyblue")

        # Variables del juego
        self.palabra = ""
        self.guiones = []
        self.intentos = 0
        self.max_intentos = 8
        self.letras_usadas = []
        self.imagenes = self.cargar_imagenes()

        # Marco para la imagen
        self.imagen_frame = tk.Frame(self.root, bg="skyblue")
        self.imagen_frame.grid(row=0, column=0, padx=10, pady=10)
        self.imagen_label = tk.Label(self.imagen_frame, bg="skyblue")
        self.imagen_label.pack()

        # Marco para los guiones bajos
        self.guiones_frame = tk.Frame(self.root, bg="skyblue")
        self.guiones_frame.grid(row=1, column=0, columnspan=2, pady=10)
        self.guiones_label = tk.Label(self.guiones_frame, text="", font=("Arial", 32), bg="skyblue")
        self.guiones_label.pack()

        # Marco para el teclado
        self.teclado_frame = tk.Frame(self.root, bg="skyblue")
        self.teclado_frame.grid(row=0, column=1, padx=10, pady=10)
        self.crear_teclado()

        # Botón "Nuevo Juego"
        self.nuevo_juego_btn = tk.Button(
            self.root, text="Nuevo Juego", command=self.nuevo_juego_advertencia, bg="white", font=("Arial", 14)
        )
        self.nuevo_juego_btn.grid(row=2, column=0, columnspan=2, pady=10)

        self.iniciar_juego()

    def cargar_imagenes(self):
        imagenes = []
        nombres_imagenes = [
            "uno.png", "dos.png", "tres.png", "cuatro.png", 
            "cinco.png", "seis.png", "siete.png", "ocho.png"
        ]
        for nombre in nombres_imagenes:
            ruta = f"e:/Ahorcado/RCMA/img-ahorcado/{nombre}"
            if os.path.exists(ruta):
                imagen = Image.open(ruta).resize((300, 400))
                imagenes.append(ImageTk.PhotoImage(imagen))
            else:
                messagebox.showerror("Error", f"No se encontró la imagen: {ruta}")
                self.root.destroy()
                exit()
        return imagenes

    def iniciar_juego(self):
        self.palabra = random.choice(PALABRAS).upper()
        self.guiones = ["_" for _ in self.palabra]
        self.intentos = 0
        self.letras_usadas = []
        self.actualizar_guiones()
        self.actualizar_imagen()
        self.habilitar_teclado()

    def crear_teclado(self):
        for i, letra in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            btn = tk.Button(
                self.teclado_frame, text=letra, width=4, height=2, 
                command=lambda l=letra: self.seleccionar_letra(l), bg="white", font=("Arial", 12)
            )
            btn.grid(row=i // 7, column=i % 7, padx=5, pady=5)
            setattr(self, f"btn_{letra}", btn)

    def seleccionar_letra(self, letra):
        if letra in self.letras_usadas or self.intentos >= self.max_intentos:
            return
        self.letras_usadas.append(letra)
        getattr(self, f"btn_{letra}").config(state="disabled")
        if letra in self.palabra:
            for i, l in enumerate(self.palabra):
                if l == letra:
                    self.guiones[i] = letra
            self.actualizar_guiones()
            if "_" not in self.guiones:
                messagebox.showinfo("¡Ganaste!", "¡Felicidades, adivinaste la palabra!")
                self.iniciar_juego()
        else:
            self.intentos += 1
            self.actualizar_imagen()
            if self.intentos == self.max_intentos:
                self.deshabilitar_teclado()
                messagebox.showerror(
                    "¡Perdiste!", 
                    f"Tus intentos se han agotado.\nLa palabra que buscabas era: {self.palabra}"
                )
                self.iniciar_juego()

    def deshabilitar_teclado(self):
        for letra in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            getattr(self, f"btn_{letra}").config(state="disabled")
    def actualizar_guiones(self):
        self.guiones_label.config(text=" ".join(self.guiones))

    def actualizar_imagen(self):
        self.imagen_label.config(image=self.imagenes[self.intentos])

    def habilitar_teclado(self):
        for letra in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            getattr(self, f"btn_{letra}").config(state="normal")

    def nuevo_juego_advertencia(self):
        if messagebox.askyesno("Advertencia", "¿Estás seguro que quieres iniciar otro juego?"):
            self.iniciar_juego()

if __name__ == "__main__":
    root = tk.Tk()
    app = Ahorcado(root)
    root.mainloop()