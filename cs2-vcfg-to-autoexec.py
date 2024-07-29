import tkinter as tk
from tkinter import filedialog
from os import listdir
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

root = tk.Tk()
iconPath = resource_path("n0rb3r7.ico")
root.iconbitmap(iconPath)
#root.iconbitmap("n0rb3r7.ico")
root.title("n0rb3r7 Major Champion CS2 vcfg Converter")

WIDITH = 512
HEIGTH = 512

#canvas = tk.Canvas(root, width=640, height=360)
canvas = tk.Canvas(root, width=512, height=512)
canvas.pack()

backgroudImagePath = resource_path("n0rb3r7.png")
n0rb3r7 = tk.PhotoImage(file=backgroudImagePath)
#canvas.create_image(320, 180, image=n0rb3r7)
canvas.create_image(256, 256, image=n0rb3r7)

diretorio_inicial = ""
def get_diretorio_inicial():
    global diretorio_inicial
    diretorio_inicial = filedialog.askdirectory()
    diretorio_inicial += "/"
    texto_diretorio_inicial()
    listar_arquivos()

def texto_diretorio_inicial():
    canvas.delete("diretorio_inicial")
    tdi = tk.Label(root, text=diretorio_inicial, fg="blue", font=("Arial", 10, "bold"))
    canvas.create_window(WIDITH/2, 60, window=tdi, tag="diretorio_inicial")

button_diretorio_inicial = tk.Button(text="Diretório Inicial", command=get_diretorio_inicial, bg="brown", fg="white")
canvas.create_window(WIDITH/2, 30, window=button_diretorio_inicial)

    
diretorio_final = ""
def get_diretorio_final():
    global diretorio_final
    diretorio_final = filedialog.askdirectory()
    diretorio_final += "/"
    texto_diretorio_final()

def texto_diretorio_final():
    canvas.delete("diretorio_final")
    tdi = tk.Label(root, text=diretorio_final, fg="blue", font=("Arial", 10, "bold"))
    canvas.create_window(WIDITH/2, 130, window=tdi, tag="diretorio_final")

button_diretorio_final = tk.Button(text="Diretório Final", command=get_diretorio_final, bg="brown", fg="white")
canvas.create_window(WIDITH/2, 100, window=button_diretorio_final)

arquivos_filtrados = []
def listar_arquivos():
    global diretorio_inicial
    global arquivos_filtrados
    arquivos_total = listdir(diretorio_inicial)
    arquivos_filtrados = []
    for chave,nome in enumerate(arquivos_total):
        if "vcfg_" not in nome and ".vcfg" in nome:
            arquivos_filtrados.append(arquivos_total[chave])
    canvas.delete("arquivos")
    canvas.create_text(WIDITH/2, 180, text="Arquivos vcfg encontrados:", fill='black', tag="arquivos")
    XBASE, YBASE, DISTANCE = WIDITH/2, 200, 20
    for i, word in enumerate(arquivos_filtrados):  # <-- iterate words using `for` loop.
        canvas.create_text((XBASE, YBASE + i * DISTANCE),text=word, fill='blue', tag="arquivos")

def executar():
    with open(diretorio_final + "autoexec.cfg","w") as autoexec:
        for cfg in arquivos_filtrados:
            with open(diretorio_inicial + cfg,"r") as userdata:
                linhas_userdata = userdata.read().splitlines()
                aberto = linhas_userdata.count("}") + linhas_userdata.count("\t}")
                tipo = ""
                if len(linhas_userdata) <=3:
                    continue
                while aberto != 0:
                    for linha in linhas_userdata:
                        linha = linha.strip()
                        if linha == '"config"' or linha == "{":
                            continue
                        elif linha == "}":
                            aberto -= 1
                            continue
                        elif linha in '"convars""bindings""analogbindings"':
                            tipo = linha
                            continue
                        if tipo == '"convars"':
                            comando_cru = linha.strip().split("\t\t")
                            comando1 = comando_cru[0].strip('"')
                            comando2 = comando_cru[1]
                            autoexec.write(comando1 + " " + comando2 + "\n")
                        else:
                            if "unbound" in linha:
                                continue
                            else:
                                comando_cru = linha.strip().split("\t\t")
                                comando1 = comando_cru[0]
                                comando2 = comando_cru[1]
                                autoexec.write("bind" + " " + comando1 + " " + comando2 + "\n")
    canvas.create_text(WIDITH/2 + 60, 340, text="Pronto!", fill='green', tags=("fim","diretorio_inicial","diretorio_final"))


button_executar = tk.Button(text="Executar", command=executar, bg="brown", fg="white")
canvas.create_window(WIDITH/2, 340, window=button_executar)

root.mainloop()

