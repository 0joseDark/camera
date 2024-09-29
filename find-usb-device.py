import usb.core
import usb.util

# Função para detectar os dispositivos USB conectados e identificar câmaras
def detectar_camara_usb():
    dispositivos = usb.core.find(find_all=True)
    camaras_usb = []

    # Iterar sobre todos os dispositivos USB conectados
    for dispositivo in dispositivos:
        try:
            # Obtém informações sobre o dispositivo
            id_vendor = dispositivo.idVendor
            id_product = dispositivo.idProduct
            fabricante = usb.util.get_string(dispositivo, dispositivo.iManufacturer)
            produto = usb.util.get_string(dispositivo, dispositivo.iProduct)
            classe = dispositivo.bDeviceClass

            # Exibe informações sobre o dispositivo
            print(f"Dispositivo USB encontrado: {fabricante} {produto} (ID {id_vendor:04x}:{id_product:04x}) - Classe {classe}")

            # Verifica se a classe do dispositivo é uma câmara (classe de vídeo = 239)
            if classe == 239:  # Classe 239 é para dispositivos de vídeo (ex: câmaras)
                camaras_usb.append(f"Câmara encontrada: {fabricante} {produto} (ID {id_vendor:04x}:{id_product:04x})")
        except usb.core.USBError as e:
            print(f"Erro ao acessar o dispositivo: {e}")
    
    # Verifica se alguma câmara foi encontrada
    if camaras_usb:
        print("\nCâmaras USB encontradas:")
        for camara in camaras_usb:
            print(camara)
    else:
        print("\nNenhuma câmara USB encontrada.")

# Chamar a função para detectar dispositivos USB e câmaras
detectar_camara_usb()
