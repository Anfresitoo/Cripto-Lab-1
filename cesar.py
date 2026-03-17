import sys

def cifrado_cesar(texto, desplazamiento):
    resultado = ""
    for char in texto:
        if char.isalpha():
            ascii_base = ord('a') if char.islower() else ord('A')
            # Aplicamos la fórmula del cifrado César
            nuevo_char = chr((ord(char) - ascii_base + desplazamiento) % 26 + ascii_base)
            resultado += nuevo_char
        else:
            # Mantenemos espacios y otros caracteres especiales
            resultado += char
    return resultado

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 cesar.py \"texto a cifrar\" desplazamiento")
        sys.exit(1)

    texto_original = sys.argv[1]
    desplazamiento = int(sys.argv[2])
    
    texto_cifrado = cifrado_cesar(texto_original, desplazamiento)
    print(texto_cifrado)
