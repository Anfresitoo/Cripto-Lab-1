import sys
from scapy.all import rdpcap, ICMP

def descifrar_cesar(texto, desplazamiento):
    resultado = ""
    for char in texto:
        if char.isalpha():
            ascii_base = ord('a') if char.islower() else ord('A')
            # Restamos el desplazamiento para descifrar
            nuevo_char = chr((ord(char) - ascii_base - desplazamiento) % 26 + ascii_base)
            resultado += nuevo_char
        else:
            resultado += char
    return resultado

def es_texto_probable(texto):
    # Criterio heurístico: Busca conectores y palabras comunes en español
    palabras_comunes = [" y ", " de ", " en ", " la ", " el ", " que ", " a "]
    for palabra in palabras_comunes:
        if palabra in texto.lower():
            return True
    return False

def leer_pcap_y_bruteforce(archivo_pcap):
    try:
        paquetes = rdpcap(archivo_pcap)
    except Exception as e:
        print(f"Error al leer el archivo pcap: {e}")
        return

    mensaje_interceptado = ""
    
    # Extraemos el primer byte del payload de cada ICMP Request (tipo 8)
    for pkt in paquetes:
        if ICMP in pkt and pkt[ICMP].type == 8: 
            payload = bytes(pkt[ICMP].payload)
            if len(payload) > 0:
                mensaje_interceptado += chr(payload[0])
    
    print(f"Mensaje interceptado en el pcap: {mensaje_interceptado}\n")
    
    # Códigos ANSI para colores en la terminal
    VERDE = '\033[92m'
    RESET = '\033[0m'
    
    for i in range(1, 26):
        texto_prueba = descifrar_cesar(mensaje_interceptado, i)
        
        # Si cumple con nuestra heurística de texto probable, lo pintamos verde
        if es_texto_probable(texto_prueba):
            print(f"{VERDE}{i:02d} {texto_prueba}{RESET}")
        else:
            print(f"{i:02d} {texto_prueba}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 readv2.py archivo.pcapng")
        sys.exit(1)
    
    archivo = sys.argv[1]
    leer_pcap_y_bruteforce(archivo)
