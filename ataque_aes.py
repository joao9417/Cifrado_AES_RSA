import os
from aes_cipher import encrypt_aes, decrypt_aes

def simular_ataque():
    print("--- Simulacion de ataque (Tampering) ---")
    
    # Configuración inicial (El sistema de la clínica)
    clave_aes = os.urandom(32)
    mensaje_original = "Diagnostico: Paciente estable, dar de alta inmediatamente."
    iv, texto_cifrado = encrypt_aes(mensaje_original, clave_aes)
    
    print(f"[*] Mensaje original de la clínica: {mensaje_original}")
    print(f"[*] Texto cifrado interceptado (Hex): {texto_cifrado.hex()[:40]}...\n")
    
    # Intervención del atacante
    print("[!] Atacante intercepta el paquete en la red y modifica 1 byte...")
    cifrado_alterado = bytearray(texto_cifrado)
    # El atacante invierte los bits del byte número 15
    cifrado_alterado[15] = cifrado_alterado[15] ^ 0xFF 
    
    # El sistema de la clínica recibe el paquete alterado
    print("\n[?] La clínica recibe el paquete e intenta descifrarlo...")
    try:
        texto_recuperado = decrypt_aes(iv, bytes(cifrado_alterado), clave_aes)
        print(f"\n[X] VULNERABILIDAD DETECTADA:")
        print("El sistema NO detectó la alteración y descifró esto:")
        print(f"-> {texto_recuperado}")
        print("\nConclusión: AES-CBC cifra, pero NO garantiza la integridad del mensaje.")
    except Exception as e:
        print(f"\n[X] VULNERABILIDAD DETECTADA:")
        print(f"El sistema falló abruptamente (Error de Padding): {e}")
        print("El atacante logró corromper el sistema al alterar el texto cifrado.")

if __name__ == "__main__":
    simular_ataque()
