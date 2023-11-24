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
        posicion.execute(consulta, parametros)
        resultado = posicion.fetchall()
        conexion.commit()
        return resultado

class login:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Login")
                
        self.label_instruccion = tk.Label(self.ventana, text="Papi Memoria")
        self.label_instruccion.pack()

        self.user = tk.Entry(self.ventana)
        self.user.pack()

        self.password = tk.Entry(self.ventana, show="*")
        self.password.pack()

        self.login_button = tk.Button(self.ventana, text="Login", command=self.verifyUser)
        self.login_button.pack()

        self.register_button = tk.Button(self.ventana, text="Registrarse", command=self.abrirRegistro)
        self.register_button.pack()

        self.error_label = tk.Label(self.ventana, text="")
        self.error_label.pack()

        self.ventana.mainloop()
    
    def verifyUser(self):
        user = self.user.get()
        password = self.password.get()

        if (len(password) > 0 and len(user) > 0):
            query = "SELECT * FROM user WHERE nickname = ? AND password = ?"
            parameters = (user, password)
            resultQuery = conexionBD(query, parameters)

            if resultQuery:
                result = 'Acceso concedido.'

                self.ventana.destroy()

                menu = Menu(user)
                menu.run()
                
            else:
                result = 'Credenciales incorrectas.'
        else:
            result = 'No se han obtenido los datos necesarios.'

        self.error_label.config(text=result)
    
    def abrirRegistro(self):
        self.ventana.withdraw()
        registro(self.ventana)


class registro:
    def __init__(self, ventanaLogin):
        self.ventanaLogin = ventanaLogin

        self.ventana = tk.Tk()
        self.ventana.title("Registro")
                
        self.label_instruccion = tk.Label(self.ventana, text="Papi Memoria")
        self.label_instruccion.pack()

        self.user = tk.Entry(self.ventana)
        self.user.pack()

        self.password1 = tk.Entry(self.ventana, show="*")
        self.password1.pack()

        self.password2 = tk.Entry(self.ventana, show="*")
        self.password2.pack()

        self.login_button = tk.Button(self.ventana, text="Crear", command=self.createUser)
        self.login_button.pack()

        self.error_label = tk.Label(self.ventana, text="")
        self.error_label.pack()

        self.ventana.mainloop()
    
    def createUser(self):
        user = self.user.get()
        password1 = self.password1.get()
        password2 = self.password2.get()

        if (len(password1) > 0 and len(password2) > 0 and len(user) > 0):
            query = "SELECT * FROM user WHERE nickname = ?"
            parameters = (user,)
            resultQuery = conexionBD(query, parameters)

            if resultQuery:
                result = 'El usuario ingresado ya existe.'
            else:
                if (password1 == password2):
                    query = "INSERT INTO user(nickname, password) VALUES(?, ?)"
                    parameters = (user, password1)
                    conexionBD(query, parameters)

                    query = "SELECT * FROM user WHERE nickname = ? AND password = ?"
                    parameters = (user, password1)
                    resultQueryConfirmation = conexionBD(query, parameters)

                    if resultQueryConfirmation:
                        result = 'Usuario creado correctamente.'
                        self.ventanaLogin.deiconify()
                        self.ventana.destroy()
                    else:
                        result = 'No se pudo crear su usuario.'

                else:
                    result = 'Las contraseñas no coinciden.'
        else:
            result = 'No se han obtenido los datos necesarios.'
        
        self.error_label.config(text=result)


class Menu:
        

    def __init__(self, nickname):
        self.nickname = nickname

        self.numerosClickeados = []

        self.paresAcertados = []
        self.paresTotales = 0


        self.ventana_menu = tk.Tk()
        self.ventana_menu.title("Menú")
        self.ventana_matriz = None  # Inicializa la variable para la matriz
        self.botones_matriz = []   # Lista para mantener referencias a los botones

        # Etiqueta de instrucción
        self.label_instruccion = tk.Label(self.ventana_menu, text="Elige una opción:")
        self.label_instruccion.pack(pady=2)

        # Botones de opciones
        self.opcion1_button = tk.Button(self.ventana_menu, text="Chico", command=self.opcion1)
        self.opcion1_button.pack(pady=5)

        self.opcion2_button = tk.Button(self.ventana_menu, text="Mediano", command=self.opcion2)
        self.opcion2_button.pack(pady=5)

        self.opcion3_button = tk.Button(self.ventana_menu, text="Pinocho (grande)", command=self.opcion3)
        self.opcion3_button.pack(pady=5)
        
        self.score_button = tk.Button(self.ventana_menu, text="Score", command=score)
        self.score_button.pack(pady=15)

        # Cargar las imágenes
        self.imagen = PhotoImage(file=f"nariz.png").subsample(10)

        self.imagenesNumeros = []
        for i in range(0, 25):
            self.imagenesNumeros.append(PhotoImage(file=f"img/{i}.png").subsample(10))
        

    def crear_ventana_matriz(self, filas, columnas):
        self.ventana_matriz = tk.Toplevel(self.ventana_menu)
        self.ventana_matriz.title(f"Matriz {filas}x{columnas}")

        self.botones_matriz = []  # Reinicia la lista de botones

        for i in range(filas):
            fila_botones = []
            for j in range(columnas):
                # Crear botón con la función correspondiente
                boton = tk.Button(self.ventana_matriz, image=self.imagen, padx=2, pady=2, borderwidth=2, relief="solid", command=lambda i=i, j=j: self.clic_matriz(i, j))
                boton.grid(row=i, column=j)
                fila_botones.append(boton)
            self.botones_matriz.append(fila_botones)
    
    
    def submit(self, minute, second, temp):
        try:
            while temp > -1:
                mins, secs = divmod(temp, 60)
                minute.set("{:02d}".format(mins))
                second.set("{:02d}".format(secs))
                self.ventana_matriz.update()
                time.sleep(1)

                if temp == 0:
                    messagebox.showinfo("Temporizador", "El tiempo se ha acabado")
                    self.ventana_matriz.destroy()
                    self.ventana_menu.deiconify()

                temp -= 1
        except Exception as e:
            print("Error in submit:", e)



    def generar_matriz(self, filas, columnas):
        # Se determina la cantidad de elementos y reinicia los pares acertados.
        self.paresTotales = filas * columnas
        self.paresAcertados.clear()

        # Crea una matriz con duplicados
        matriz = np.arange(self.paresTotales)
        matriz_duplicada = np.tile(matriz, 2)

        # Mezcla los elementos en la matriz
        np.random.shuffle(matriz_duplicada)

        # Da forma a la matriz con las dimensiones correctas
        return matriz_duplicada.reshape(filas, -1)

    def crear_ventana_matriz(self, filas, columnas, minute, second):
        self.ventana_menu.withdraw()
        self.ventana_matriz = tk.Toplevel(self.ventana_menu)
        self.ventana_matriz.title(f"Matriz {filas}x{columnas*2}")

        marco_temporizador = tk.Frame(self.ventana_matriz)
        marco_temporizador.grid(row=filas, column=0, columnspan=columnas*2)

        self.minuteEntry = tk.Label(marco_temporizador, textvariable=minute)
        self.minuteEntry.grid(row=0, column=0, padx=10)

        self.secondEntry = tk.Label(marco_temporizador, textvariable=second)
        self.secondEntry.grid(row=0, column=1, padx=10)


        self.botones_matriz = []  # Reinicia la lista de botones
        matriz_resultante = self.generar_matriz(filas, columnas)
        
        # MOSTRAR NUMEROS
        for i, fila in enumerate(matriz_resultante):
            fila_botones = []
            for j, numero in enumerate(fila):
                # Crear botón con la función correspondiente
                boton = tk.Button(self.ventana_matriz, image=self.imagenesNumeros[numero], padx=2, pady=2, borderwidth=2, relief="solid")
                boton.grid(row=i, column=j)
                fila_botones.append(boton)

            self.botones_matriz.append(fila_botones)

        self.ventana_menu.after(2000, self.ocultarTodasLasFichas, fila_botones, matriz_resultante)        

        print(matriz_resultante)
        
    
    def ocultarTodasLasFichas(self, fila_botones, matriz_resultante):
        # Destruir los botones existentes en la matriz
        for fila_botones in self.botones_matriz:
            for boton in fila_botones:
                boton.destroy()

        # Limpiar la lista de botones
        self.botones_matriz.clear()

        for i, fila in enumerate(matriz_resultante):
            fila_botones = []
            for j, numero in enumerate(fila):
                # Crear botón con la función correspondiente
                boton = tk.Button(self.ventana_matriz, image=self.imagen, padx=2, pady=2, borderwidth=2, relief="solid", command=lambda i=i, j=j, numero=numero: self.clic_matriz(i, j, numero))
                boton.grid(row=i, column=j)
                fila_botones.append(boton)

            self.botones_matriz.append(fila_botones)


    def mostrarFicha(self, fila, columna, numero):
        # Obtener el botón correspondiente en la matriz
        boton = self.botones_matriz[fila][columna]

        # Configurar la imagen como None y establecer el texto
        boton.config(image=self.imagenesNumeros[numero])
    
    def ocultarFicha(self, fila, columna):
        # Obtener el botón correspondiente en la matriz
        boton = self.botones_matriz[fila][columna]

        # Configurar la imagen como None y establecer el texto
        boton.config(image=self.imagen)

    def clic_matriz(self, fila, columna, numero):
        if numero not in self.paresAcertados:
            if (len(self.numerosClickeados) < 2):
                boxPosicion = {'fila': fila, 'columna': columna, 'valor': numero}
                self.numerosClickeados.append(boxPosicion)

                self.mostrarFicha(fila, columna, numero)
                
                # TEMPORAL
                print(f"Has clic en la posición ({fila}, {columna}), con elemento: {numero}")

                if (len(self.numerosClickeados) == 2):
                    seleccionUno = self.numerosClickeados[0]
                    seleccionDos = self.numerosClickeados[1]

                    if (seleccionUno['valor'] == seleccionDos['valor'] and (seleccionUno['fila'] != seleccionDos['fila'] or seleccionUno['columna'] != seleccionDos['columna'])):
                        # TEMPORAL
                        print(f"Bien")
                        
                        self.paresAcertados.append(seleccionUno['valor'])

                        if (len(self.paresAcertados) >= (self.paresTotales)):
                            # TEMPORAL
                            print("Ganaste")
                            self.agrearTiempoDelUsuario()

                            self.ventana_matriz.destroy()
                            self.ventana_menu.deiconify()

                        self.numerosClickeados.clear()

                    else:
                        # TEMPORAL
                        print(f"mal")

                        self.ocultarFicha(seleccionUno['fila'], seleccionUno['columna'])

                        self.numerosClickeados.clear()
                        self.numerosClickeados.append(boxPosicion)
                        print(self.numerosClickeados)

    def agrearTiempoDelUsuario(self):
        tiempoRestante = (int(self.minuteEntry.cget("text")) * 60) + int(self.secondEntry.cget("text"))
        tiempoDisponible = 5 * 60
        tiempoTardado = tiempoDisponible - tiempoRestante

        query = "INSERT INTO ranking(nickname, time) VALUES(?, ?)"
        parameters = (self.nickname, tiempoTardado)

        conexionBD(query, parameters)

    def opcion1(self):
        print("Has elegido la Opción 1")
        minute = tk.StringVar()
        second = tk.StringVar()
        filas, columnas = 3, 3
        self.crear_ventana_matriz(filas, columnas, minute, second)

    def opcion2(self):
        print("Has elegido la Opción 2")
        minute = tk.StringVar()
        second = tk.StringVar()
        filas, columnas = 4, 4
        self.crear_ventana_matriz(filas, columnas, minute, second)

    def opcion3(self):
        print("Has elegido la Opción 3")
        filas, columnas = 5, 5
        minute = tk.StringVar()
        second = tk.StringVar()
        minute.set("05")
        second.set("00")

        self.crear_ventana_matriz(filas, columnas, minute, second)

        # Crear un temporizador y comenzar la cuenta regresiva
        temp = int(minute.get()) * 60 + int(second.get())
        self.ventana_menu.after(2000, lambda: self.submit(minute, second, temp))

    def run(self):
        self.ventana_menu.mainloop()


class score:
    def __init__(self):
        self.labels_top = []   # Lista labels

        self.ventana = tk.Tk()
        self.ventana.title("Score")
                
        self.label_instruccion = tk.Label(self.ventana, text="TOP 10")
        self.label_instruccion.pack()

        query = "SELECT nickname, MIN(time) AS time FROM ranking GROUP BY nickname ORDER BY time ASC LIMIT 10"
        resultado = conexionBD(query)
        
        for top in resultado:
            texto = top[0], top[1]

            label = tk.Label(self.ventana, text=texto)
            label.pack()


        self.error_label = tk.Label(self.ventana, text="")
        self.error_label.pack()

        self.ventana.mainloop()

login()