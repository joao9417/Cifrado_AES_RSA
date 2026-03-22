import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def encrypt_aes(plaintext_message, key):
    # Generar un vector de inicializacion (IV) aleatorio de 16 bytes
    iv = os.urandom(16)

    # Configurar el cifrado AES en modo CBC
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # AES requiere que el mensaje sea un multiplo de 128 bits (16 bytes) aplicamos padding
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext_message.encode()) + padder.finalize()

    # Cifrar los datos o mensaje
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv, ciphertext

def decrypt_aes(iv, ciphertext, key):
    # Configurar el descifrador con la misma clave y el mismo IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Descifrar los datos
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Quitar el padding para recuperar el mensaje original
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_data) + unpadder.finalize()
    return plaintext.decode()


# --- Prueba normal ---
if __name__ == "__main__":
    # AES requiere claves de 16, 24 o 32 bytes (para esta prueba usaremos 32bytes para AES-256)
    clave_secreta = os.urandom(32)
    registro_medico = "Paciente: Carlos G. - Diagnóstico: Requiere cirugía menor."

    print("-- Iniciando prueba AES normal --")
    print(f"Mensaje original: {registro_medico}")

    # Proceso de cifrado
    iv_usado, texto_cifrado = encrypt_aes(registro_medico, clave_secreta)
    print(f"Texto cifrado (Hexadecimal): {texto_cifrado.hex()}")

    # Proceso de descifrado
    texto_recuperado = decrypt_aes(iv_usado, texto_cifrado, clave_secreta)
    print(f"Texto descifrado: {texto_recuperado}")

"""
# --- Prueba de estres ---
if __name__ == "__main__":
    clave_secreta = os.urandom(32)
    registro_medico = "Paciente: Carlos G. - Diagnóstico: Requiere cirugía menor."

    print("-- Iniciando prueba AES normal --")
    print(f"Mensaje original: {registro_medico}")

    iv_usado, texto_cifrado = encrypt_aes(registro_medico, clave_secreta)
    
    # --- Inicio prueba de estres ---
    print("\n-- Simulando la alteración de un solo byte --")
    
    # Convertimos los bytes a un arreglo modificable
    texto_alterado = bytearray(texto_cifrado)

    # Modificamos un solo byte. Elegimos el byte en la posición 5 (que está en el primer bloque).
    # Al sumarle 1 (y usar % 256 para mantenerlo como byte válido), lo cambiamos.
    texto_alterado[5] = (texto_alterado[5] + 1) % 256

    # Intentamos descifrar el mensaje alterado
    try:
        texto_recuperado = decrypt_aes(iv_usado, bytes(texto_alterado), clave_secreta)
        print(f"Texto descifrado (¡Mira el resultado!):\n{texto_recuperado}")
    except Exception as e:
        print(f"¡El descifrado falló por completo y el programa colapsó!\nError: {e}")
"""