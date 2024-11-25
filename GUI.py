import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import client as c

vector =[]
class guiClass :
    
    def _init_(self):
        
        self.gui = TkinterDnD.Tk()
        self.gui.geometry("1500x760")
        self.gui.title("gg")

        #frame del titulo
        self.titleFrame= tk.Frame(self.gui,bg="#9ed1c8")
        self.titleFrame.pack(side=tk.LEFT)
        self.titleFrame.pack_propagate(False)
        self.titleFrame.configure(width=300, height=770)

        self.titulo = tk.Label(self.titleFrame,text="Ordenador \n de \nvectores",bg="#9ed1c8",font = ("Bold", 30))
        self.titulo.place(x=25,y=250,height=200,width=250)

        #frame con las opciones 
        self.opcionesFrame = tk.Frame(self.gui, bg="#FFFAF0", highlightbackground="black", highlightthickness=2)
        self.opcionesFrame.pack(fill=tk.BOTH, expand=True)

        self.mergeButton = tk.Button(self.opcionesFrame,text="Mergesort",font=("Arial", 16), command= lambda: c.start_client(vector,self.tiempoBarra.get(),1))
        self.mergeButton.place(x=150,y=600,height=70,width=220)

        self.heapButton = tk.Button(self.opcionesFrame,text="Heapsort",font=("Arial", 16), command= lambda: c.start_client(vector,self.tiempoBarra.get(),3))
        self.heapButton.place(x=470,y=600,height=70,width=220)

        self.quickButton = tk.Button(self.opcionesFrame,text="Quicksort",font=("Arial", 16), command= lambda: c.start_client(vector,    self.tiempoBarra.get(),2))
        self.quickButton.place(x=790,y=600,height=70,width=220)

        self.drop_area = tk.Label(self.opcionesFrame,text="Arrastra aquí un archivo .txt",bg="#d9d9d9",relief="ridge",font=("Arial", 14))
        self.drop_area.place(x=300,y=45, width=600,height=300)
        
        self.tiempoLabel = tk.Label(self.opcionesFrame,text="Tiempo \n(en segundos)",bg="#dee0e1",relief="ridge",font=("Arial", 11))
        self.tiempoLabel.place(x=300,y=395, width=100, height=50)

        self.tiempoBarra = tk.Entry(self.opcionesFrame,text="",font=("Arial", 11))
        self.tiempoBarra.place(x=450,y=395,width=200,height=50)

        #esta funcion habilita para que se pueda soltar archivos en la interfaz
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind("<<Drop>>", self.handle_drop)

        self.gui.mainloop()


    def handle_drop(self, event):
        # Obtiene la ruta del archivo que va a ser soltado
        file_path = event.data.strip().strip('{}')
        print(f"Ruta del archivo: {file_path}")

        if file_path.endswith(".txt"):  #Verifica que sea un archivo .txt, es decir que termine en un .txt
            print("SI ENTRO")
            try:
                # Lee el archivo de texto
                with open(file_path, "r", encoding="utf-8") as file:
                    #lee las lineas de texto
                    for line in file:    
                        # Muestra el contenido del archivo
                        #print(f"Contenido del archivo:"+line)

                        #limpia la linea y elimina espacios 
                        clean_line = line.strip()

                        #Hace un filtro para solo extraer los numeros
                        if(line!=""):
                            vector.append(int(clean_line))
                #for i in vector:
                    #print("\nNumero del vector: " +str(i))

            except Exception as e:
                print("No fue posible leer el archivo"+e)

        else:
            print("El archivo no es de tipo txt, intenta de nuevo")



guiClass()