import os
import hmac
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from rsa_cipher import generate_rsa_keys, encrypt_rsa, decrypt_rsa

def cifrar_hibrido(mensaje_masivo, llave_publica_destino):
    # Generar clave AES y clave HMAC dinámicas para esta sesión
    clave_aes = os.urandom(32)
    clave_hmac = os.urandom(32) # Uso de HMAC para integridad 
    
    # Cifrar el mensaje masivo con AES
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(clave_aes), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(mensaje_masivo.encode()) + padder.finalize()
    texto_cifrado_aes = encryptor.update(padded_data) + encryptor.finalize()
    
    # Generar la firma HMAC del texto cifrado
    firma_hmac = hmac.new(clave_hmac, iv + texto_cifrado_aes, hashlib.sha256).digest()
    
    # Empaquetar y cifrar las claves simétricas usando RSA 
    claves_empaquetadas = clave_aes + clave_hmac
    claves_cifradas_rsa = encrypt_rsa(llave_publica_destino, claves_empaquetadas.hex())
    
    return claves_cifradas_rsa, iv, texto_cifrado_aes, firma_hmac

def descifrar_hibrido(claves_cifradas_rsa, iv, texto_cifrado_aes, firma_hmac, llave_privada_destino):
    # Descifrar las claves simétricas con RSA
    claves_desempaquetadas_hex = decrypt_rsa(llave_privada_destino, claves_cifradas_rsa)
    claves_desempaquetadas = bytes.fromhex(claves_desempaquetadas_hex)
    clave_aes = claves_desempaquetadas[:32]
    clave_hmac = claves_desempaquetadas[32:]
    
    # Verificar la integridad con HMAC ANTES de descifrar AES
    firma_calculada = hmac.new(clave_hmac, iv + texto_cifrado_aes, hashlib.sha256).digest()
    if not hmac.compare_digest(firma_hmac, firma_calculada):
        raise ValueError("¡ALERTA DE SEGURIDAD! El mensaje fue alterado en tránsito.")
        
    # Descifrar los datos médicos con AES
    cipher = Cipher(algorithms.AES(clave_aes), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(texto_cifrado_aes) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    return (unpadder.update(padded_data) + unpadder.finalize()).decode()

if __name__ == "__main__":
    print("--- SISTEMA HÍBRIDO SEGURO: CLÍNICA SALUD Y VIDA ---")
    llave_privada_lab, llave_publica_lab = generate_rsa_keys()
    
    datos_medicos = "Radiografía Torax: Normal. Resultados Laboratorio: Glucosa 90 mg/dL."
    print(f"Datos originales a enviar: {datos_medicos}")
    
    # La clínica cifra y envía
    claves_rsa, iv_aes, datos_aes, firma = cifrar_hibrido(datos_medicos, llave_publica_lab)
    print("\n[+] Datos cifrados exitosamente (AES + RSA + HMAC). Transmitiendo...")
    
    # El laboratorio recibe y descifra
    datos_recuperados = descifrar_hibrido(claves_rsa, iv_aes, datos_aes, firma, llave_privada_lab)
    print(f"\n[+] Datos recuperados con integridad verificada: {datos_recuperados}")