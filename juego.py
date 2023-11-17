import tkinter as tk
import time
from tkinter import *
from tkinter import messagebox
from tkinter import PhotoImage
import sqlite3
import random
import numpy as np


def conexionBD(consulta, parametros=()):
    with sqlite3.connect("papiMemoria.db") as conexion:
        posicion = conexion.cursor()
        resultadoCon = posicion.execute(consulta, parametros)
        conexion.commit()
        return resultadoCon

class login:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Login")
                
        self.label_instruccion = tk.Label(self.ventana, text="Papi Memoria")
        self.label_instruccion.pack()

        self.user = tk.Entry(self.ventana)
        self.user.pack()

        self.password = tk.Entry(self.ventana)
        self.password.pack()

        self.login_button = tk.Button(self.ventana, text="Login", command=self.verifyUser)
        self.login_button.pack()

        self.error_label = tk.Label(self.ventana, text="")
        self.error_label.pack()
    
    def conexionBD(consulta, parametros=()):
        with sqlite3.connect("papiMemoria.db") as conexion:
            posicion = conexion.cursor()
            resultadoCon = posicion.execute(consulta, parametros)
            # No necesitas hacer commit para consultas de selección
            return resultadoCon

    def verifyUser(self):
        user = self.user.get()
        password = self.password.get()

        if (len(password) > 0 and len(user) > 0):
            query = "SELECT * FROM user WHERE nickname = ? AND password = ?"
            parameters = (user, password)
            resultQuery = conexionBD(query, parameters)

            if resultQuery:
                result = 'Acceso concedido.'
            else:
                result = 'Credenciales incorrectas.'
        else:
            result = 'No se han obtenido los datos necesarios.'

        self.error_label.config(text=result)





class Menu:
        

    def __init__(self):
        self.ventana_menu = tk.Tk()
        self.ventana_menu.title("Menú")
        self.ventana_matriz = None  # Inicializa la variable para la matriz
        self.botones_matriz = []   # Lista para mantener referencias a los botones

        # Etiqueta de instrucción
        self.label_instruccion = tk.Label(self.ventana_menu, text="Elige una opción:")
        self.label_instruccion.pack(pady=2)

        # Botones de opciones
        self.opcion1_button = tk.Button(self.ventana_menu, text="Opción 1", command=self.opcion1)
        self.opcion1_button.pack(pady=5)

        self.opcion2_button = tk.Button(self.ventana_menu, text="Opción 2", command=self.opcion2)
        self.opcion2_button.pack(pady=5)

        self.opcion3_button = tk.Button(self.ventana_menu, text="Opción 3", command=self.opcion3)
        self.opcion3_button.pack(pady=5)

        # Cargar las imágenes
        self.imagenes = [PhotoImage(file=f"nariz.png").subsample(5) for i in range(1, 10)]

    def crear_ventana_matriz(self, filas, columnas, minute, second):
        self.ventana_matriz = tk.Toplevel(self.ventana_menu)
        self.ventana_matriz.title(f"Matriz {filas}x{columnas}")
        
        


        # Use of Entry class to take input from the user

        self.minuteEntry= tk.Label(self.ventana_matriz, textvariable=minute)
        self.minuteEntry.place(x=130,y=20)

        self.secondEntry= tk.Label(self.ventana_matriz, textvariable=second)
        self.secondEntry.place(x=180,y=20)


        self.botones_matriz = []  # Reinicia la lista de botones

        for i in range(filas):
            fila_botones = []
            for j in range(columnas):
                # Seleccionar una imagen aleatoria
                imagen = random.choice(self.imagenes)
                # Crear botón con la función correspondiente
                boton = tk.Button(self.ventana_matriz, image=imagen, padx=2, pady=2, borderwidth=2, relief="solid", command=lambda i=i, j=j: self.clic_matriz(i, j))
                boton.grid(row=i, column=j)
                fila_botones.append(boton)
            self.botones_matriz.append(fila_botones)
    
    
    def submit(self, hour, minute, second):
        try:
            # the input provided by the user is
            # stored in here :temp
            temp = int(hour.get())*3600 + int(minute.get())*60 + int(second.get())
        except:
            print("Please input the right value")
        while temp >-1:
            
            # divmod(firstvalue = temp//60, secondvalue = temp%60)
            mins,secs = divmod(temp,60) 

            # Converting the input entered in mins or secs to hours,
            # mins ,secs(input = 110 min --> 120*60 = 6600 => 1hr :
            # 50min: 0sec)
            hours=0
            if mins >60:
                
                # divmod(firstvalue = temp//60, secondvalue 
                # = temp%60)
                hours, mins = divmod(mins, 60)
            
            # using format () method to store the value up to 
            # two decimal places
            hour.set("{0:2d}".format(hours))
            minute.set("{0:2d}".format(mins))
            second.set("{0:2d}".format(secs))

            # updating the GUI window after decrementing the
            # temp value every time
            self.ventana_matriz.update()
            time.sleep(1)

            # when temp value = 0; then a messagebox pop's up
            # with a message:"Time's up"
            if (temp == 0):
                messagebox.showinfo("Time Countdown", "Time's up ")
            
            # after every one sec the value of temp will be decremented
            # by one
            temp -= 1

    def __generar_matriz(self, filas, columnas):
        self.ventana_matriz = tk.Toplevel(self.ventana_menu)
        self.ventana_matriz.title(f"Matriz {filas}x{columnas}")

        # Asegúrate de que el total de elementos sea filas * columnas
        total_elementos = filas * columnas

        # Crea una matriz con duplicados
        matriz = np.arange(total_elementos)
        matriz_duplicada = np.tile(matriz, 2)

        # Mezcla los elementos en la matriz
        np.random.shuffle(matriz_duplicada)

        # Da forma a la matriz con las dimensiones correctas
        return matriz_duplicada.reshape(filas, -1)


    def crear_ventana_matriz(self, filas, columnas):
        self.botones_matriz = []  # Reinicia la lista de botones
        matriz_resultante = self.__generar_matriz(filas, columnas)
        
        for i, fila in enumerate(matriz_resultante):
            fila_botones = []
            for j, numero in enumerate(fila):
                # Seleccionar una imagen aleatoria
                imagen = random.choice(self.imagenes)
                # Crear botón con la función correspondiente
                boton = tk.Button(self.ventana_matriz, image=imagen, padx=2, pady=2, borderwidth=2, relief="solid", command=lambda i=i, j=j, numero=numero: self.clic_matriz(i, j, numero))
                boton.grid(row=i, column=j)
                fila_botones.append(boton)

                print(numero) # este es el numero que se encontraria dentro del boton

            self.botones_matriz.append(fila_botones)

        print(matriz_resultante)

    def clic_matriz(self, i, j, numero):
        print(f"Has clic en la posición ({i}, {j}), con elemento: {numero}")
        # Seleccionar una imagen aleatoria
        imagen = random.choice(self.imagenes)
        # Configurar la imagen del botón en la posición seleccionada
        self.botones_matriz[i][j].config(image=imagen)

    def opcion1(self):
        print("Has elegido la Opción 1")
        filas, columnas = 3, 4
        self.crear_ventana_matriz(filas, columnas)

    def opcion2(self):
        print("Has elegido la Opción 2")
        filas, columnas = 4, 4
        self.crear_ventana_matriz(filas, columnas)

    def opcion3(self):
        print("Has elegido la Opción 3")
        filas, columnas = 4, 5
        self.crear_ventana_matriz(filas, columnas)

    def run(self):
        self.ventana_menu.mainloop()

# Ejemplo de uso
if __name__ == "__main__":
    menu = Menu()
    menu.run()


# # Especifica un rango de números más pequeño para que la cantidad total sea par
# inicio = 1
# fin = 32

# # Crea una matriz con duplicados
# matriz = np.arange(inicio, fin + 1)
# matriz_duplicada = np.tile(matriz, 2)

# # Mezcla los elementos en la matriz
# np.random.shuffle(matriz_duplicada)

# # Da forma a la matriz con cinco filas y dos columnas
# matriz_5x2 = matriz_duplicada.reshape(8, -1)

# print(matriz_5x2)