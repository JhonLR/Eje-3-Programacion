from tkinter import ttk
from tkinter import *
import sqlite3

class Product:

    db = r"bdatos.db"

    def __init__(self, window):
        self.wind = window
        self.wind.title("Gym Optimus")

        #Ventana
        frame = LabelFrame(self.wind, text = "Resgistrar nuevo usuario", fg="black", font=("Helvetica 18 bold"))
        frame.grid(row = 0, column = 0, pady = 20)

        # Nombre de input
        Label(frame, text = "Nombres: ", fg="gray", font=("Helvetica 10 bold")).grid(row = 1, column = 0)
        self.nombre = Entry(frame, justify="left", width=22, font=("Helvetica 12"))
        self.nombre.focus()  
        self.nombre.grid(row = 1, column = 1)

        #Apellido input
        Label(frame, text = "Apellidos: ", fg="gray", font=("Helvetica 10 bold")).grid(row = 2, column = 0)
        self.apellido = Entry(frame, justify="left", width=22, font=("Helvetica 12"))
        self.apellido.grid(row=2, column=1)

        #Cedula input
        Label(frame, text = "Cedula: ", fg="gray", font=("Helvetica 10 bold")).grid(row = 3, column = 0)
        self.cedula = Entry(frame, justify="left", width=22, font=("Helvetica 12"))
        self.cedula.grid(row=3, column=1)

        #Correo input
        Label(frame, text = "Correo: ", fg="gray", font=("Helvetica 10 bold")).grid(row = 4, column = 0)
        self.correo = Entry(frame, justify="left", width=22, font=("Helvetica 12"))
        self.correo.grid(row=4, column=1)

        #Boton 1
        ttk.Button(frame, text = "Registrar", command= self.add_user, cursor="hand2").grid(row=5, columnspan=2)

        #Mensaje de salida
        self.mensaje = Label(text="", font=("Helvetica 13 bold"))
        self.mensaje.grid(row=5, column=0, columnspan=2, sticky= W+E)

        # Tabla
        self.tree = ttk.Treeview(height = 8, columns = ("#1, #2, #3"))
        self.tree.grid(row = 6, column = 0)
        self.tree.heading('#0', text = 'Nombres', anchor = CENTER)
        self.tree.heading('#1', text = "Apellidos", anchor = CENTER)
        self.tree.heading('#2', text = "Cedula", anchor = CENTER)
        self.tree.heading('#3', text = "Correo", anchor = CENTER)
        
        #Botones de estado
        ttk.Button(text= "Borrar", command= self.borrar_usuario).grid(row=7, column=0, sticky=W+E)

        self.get_usuarios()

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    # Info de base de datos
    def get_usuarios(self):
        # Limpieza 
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        
        #datos
        query = "   SELECT * FROM usuarios ORDER BY nombre DESC"
        db_rows = self.run_query(query)

        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = row[2:5])

    def validacion(self):  
        return len(self.nombre.get()) !=0 and len(self.apellido.get()) !=0 and len(self.cedula.get()) !=0 and len(self.correo.get()) !=0

    def add_user(self):
        if self.validacion():
            query = "INSERT INTO usuarios VALUES(NULL, ?, ?, ?, ?)"
            parameters =  (self.nombre.get(), self.apellido.get(), self.cedula.get(), self.correo.get())
            self.run_query(query, parameters)
            self.mensaje["text"] = 'Usuario "{}" añadido correctamente'.format(self.nombre.get())
            self.nombre.delete(0, END)
            self.apellido.delete(0, END)
            self.cedula.delete(0, END)
            self.correo.delete(0, END)
     
        else:
            self.message['text'] = "Es necesario llenar todas las casillas"
        self.get_usuarios()

    def borrar_usuario(self):
        self.mensaje["text"] = ""
        try:
           self.tree.item(self.tree.selection())["text"][0]
        except IndexError as e:
            self.mensaje["text"] = "Selecciona un nombre"
            return
        self.mensaje["text"] = ""
        nombre = self.tree.item(self.tree.selection())["text"]
        query = "DELETE FROM usuarios WHERE nombre = ?"
        self.run_query(query, (nombre, ))
        self.mensaje["text"] = 'Usuario "{}" borrado correctamente'.format(nombre)
        self.get_usuarios()

    
if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.iconbitmap("imag.ico")
    window.resizable(height=0, width=0)
    window.mainloop()
