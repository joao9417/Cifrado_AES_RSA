from rsa_cipher import generate_rsa_keys, encrypt_rsa, decrypt_rsa

def simular_ataque_rsa():
    print("--- Simulacion ataque RSA (Tampering) ---")
    
    llave_privada, llave_publica = generate_rsa_keys()
    mensaje_original = "Clave secreta AES: 987654321"
    
    # 1. Cifrado
    texto_cifrado = encrypt_rsa(llave_publica, mensaje_original)
    
    # 2. El Atacante modifica el texto cifrado (Bit-flipping)
    cifrado_alterado = bytearray(texto_cifrado)
    cifrado_alterado[20] = cifrado_alterado[20] ^ 0xFF
    
    # 3. La clínica intenta descifrar
    print("[?] Intentando descifrar paquete RSA alterado...")
    try:
        texto_recuperado = decrypt_rsa(llave_privada, bytes(cifrado_alterado))
        print(f"Mensaje recuperado: {texto_recuperado}")
    except Exception as e:
        print("\n[+] ATAQUE BLOQUEADO POR RSA-OAEP:")
        print(f"El sistema detectó la manipulación y abortó de forma segura. Error: {e}")
        print("Conclusión: RSA con OAEP garantiza confidencialidad E integridad.")

if __name__ == "__main__":
    simular_ataque_rsa()
