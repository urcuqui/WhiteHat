from PIL import Image

def ocultar_mensaje(imagen_path, mensaje, salida_path):
    img = Image.open(imagen_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    pixeles = list(img.getdata())

    # Añadir delimitador para saber dónde termina el mensaje
    mensaje += "|||"

    # Convertir el mensaje a binario
    binario_mensaje = ''.join(format(ord(c), '08b') for c in mensaje)

    if len(binario_mensaje) > len(pixeles) * 3:
        raise ValueError("El mensaje es demasiado largo para esta imagen.")

    nuevos_pixeles = []
    idx = 0
    for pixel in pixeles:
        r, g, b = pixel
        if idx < len(binario_mensaje):
            r = (r & ~1) | int(binario_mensaje[idx])
            idx += 1
        if idx < len(binario_mensaje):
            g = (g & ~1) | int(binario_mensaje[idx])
            idx += 1
        if idx < len(binario_mensaje):
            b = (b & ~1) | int(binario_mensaje[idx])
            idx += 1
        nuevos_pixeles.append((r, g, b))

    img.putdata(nuevos_pixeles)
    img.save(salida_path)
    print("Mensaje oculto guardado en", salida_path)

def extraer_mensaje(imagen_path):
    img = Image.open(imagen_path)
    pixeles = list(img.getdata())

    bits = ''
    for pixel in pixeles:
        for valor in pixel:
            bits += str(valor & 1)

    caracteres = [bits[i:i+8] for i in range(0, len(bits), 8)]
    mensaje = ''
    for byte in caracteres:
        char = chr(int(byte, 2))
        mensaje += char
        if mensaje.endswith("|||"):
            break

    return mensaje[:-3]  # Eliminar delimitador

# --- USO ---

# Ocultar un mensaje
import os
file_to_stego = os.path.join(os.path.dirname(__file__), 'ic.png')
file_stego = os.path.join(os.path.dirname(__file__), 'imagen_con_mensaje.png')
ocultar_mensaje(file_to_stego, 'hack the planet', file_stego)

# Extraer un mensaje
mensaje = extraer_mensaje('imagen_con_mensaje.png')
print("Mensaje oculto:", mensaje)