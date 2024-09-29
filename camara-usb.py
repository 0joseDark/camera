import tkinter as tk  # Para a interface gráfica
from tkinter import messagebox  # Para exibir mensagens
import cv2  # Para manipular a câmara
import usb.core  # Para interagir com dispositivos USB
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

# Função para mostrar o vídeo da câmara
def mostrar_video():
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            cv2.imshow('Feed da Câmara', frame)
        root.after(10, mostrar_video)  # Atualiza o feed a cada 10ms

# Função para desligar a câmara
def desligar_camara():
    global cap
    if cap.isOpened():
        cap.release()
        cv2.destroyAllWindows()
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
root.geometry("400x300")

# Lista de portas USB (simulação para o exemplo)
portas_usb = detectar_camara_usb()

# Dropdown para escolher a porta USB
porta_usb = tk.StringVar()
porta_menu = tk.OptionMenu(root, porta_usb, *portas_usb)
porta_menu.pack(pady=10)

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
