import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Para mostrar o feed na GUI
import cv2
import usb.core
import usb.util
import os

# Função para detectar as câmaras USB ligadas
def detectar_camara_usb():
    dispositivos = usb.core.find(find_all=True)
    camaras_usb = []
    
    for dispositivo in dispositivos:
        if dispositivo.bDeviceClass == 239:  # Classe de vídeo (239 é a classe de dispositivos de vídeo USB)
            camaras_usb.append(f"Dispositivo USB: ID {dispositivo.idVendor}:{dispositivo.idProduct}")
    
    if not camaras_usb:
        camaras_usb.append("Nenhuma câmara USB encontrada.")
    
    return camaras_usb

# Função para ligar a câmara
def ligar_camara():
    global cap
    porta = porta_usb.get()
    
    if porta:
        cap = cv2.VideoCapture(0)  # Normalmente, 0 é a primeira câmara
        if cap.isOpened():
            messagebox.showinfo("Info", "Câmara ligada!")
            mostrar_video()
        else:
            messagebox.showerror("Erro", "Falha ao ligar a câmara.")
    else:
        messagebox.showwarning("Aviso", "Escolha uma porta USB primeiro.")

# Função para mostrar o feed de vídeo da câmara na GUI
def mostrar_video():
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # Converte a imagem para o formato compatível com o tkinter
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img_tk = ImageTk.PhotoImage(image=img)
            
            # Atualiza o widget de imagem com o novo frame
            lbl_video.img_tk = img_tk  # Guarda a referência para evitar o garbage collector
            lbl_video.config(image=img_tk)
        
        # Chama a função novamente após 10ms
        root.after(10, mostrar_video)

# Função para desligar a câmara
def desligar_camara():
    global cap
    if cap.isOpened():
        cap.release()
        lbl_video.config(image='')  # Limpa a imagem do vídeo
        messagebox.showinfo("Info", "Câmara desligada.")
    else:
        messagebox.showwarning("Aviso", "Nenhuma câmara ligada.")

# Função para sair do programa
def sair():
    if cap.isOpened():
        cap.release()
    root.quit()

# Criação da janela principal
root = tk.Tk()
root.title("Controlo de Câmara USB")
root.geometry("640x480")

# Lista de portas USB (simulação para o exemplo)
portas_usb = detectar_camara_usb()

# Dropdown para escolher a porta USB
porta_usb = tk.StringVar()
porta_menu = tk.OptionMenu(root, porta_usb, *portas_usb)
porta_menu.pack(pady=10)

# Label onde o vídeo será exibido
lbl_video = tk.Label(root)
lbl_video.pack(pady=10)

# Botão para ligar a câmara
botao_ligar = tk.Button(root, text="Ligar Câmara", command=ligar_camara)
botao_ligar.pack(pady=10)

# Botão para desligar a câmara
botao_desligar = tk.Button(root, text="Desligar Câmara", command=desligar_camara)
botao_desligar.pack(pady=10)

# Botão para sair
botao_sair = tk.Button(root, text="Sair", command=sair)
botao_sair.pack(pady=10)

# Loop principal da interface gráfica
cap = None  # Variável global para a câmara
root.mainloop()
