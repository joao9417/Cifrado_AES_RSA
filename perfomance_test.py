import time
import os
from aes_cipher import encrypt_aes, decrypt_aes
from rsa_cipher import generate_rsa_keys, encrypt_rsa, decrypt_rsa

def run_performance_test():
    print("--- Iniciando prueba de rendimiento ---")
    
    # Preparamos un dato médico simulado
    mensaje = "Paciente: Juan P. - Historial: Hipertensión controlada, alergia a penicilina. Tratamiento actual: Losartán 50mg."
    
    # --- Prueba AES ---
    print("\n[1] Evaluando rendimiento de AES-256 (Simétrico)...")
    clave_aes = os.urandom(32)
    
    inicio_aes_enc = time.perf_counter()
    iv, texto_cifrado_aes = encrypt_aes(mensaje, clave_aes)
    fin_aes_enc = time.perf_counter()
    
    inicio_aes_dec = time.perf_counter()
    _ = decrypt_aes(iv, texto_cifrado_aes, clave_aes)
    fin_aes_dec = time.perf_counter()
    
    tiempo_aes_enc = (fin_aes_enc - inicio_aes_enc) * 1000 # Convertir a milisegundos
    tiempo_aes_dec = (fin_aes_dec - inicio_aes_dec) * 1000
    
    print(f"Tiempo de Cifrado AES:   {tiempo_aes_enc:.4f} ms")
    print(f"Tiempo de Descifrado AES: {tiempo_aes_dec:.4f} ms")

    # --- Prueba RSA ---
    print("\n[2] Evaluando rendimiento de RSA-2048 (Asimétrico)...")
    # No medimos la generación de claves porque se hace una sola vez, medimos solo cifrado/descifrado
    llave_privada, llave_publica = generate_rsa_keys()
    
    inicio_rsa_enc = time.perf_counter()
    texto_cifrado_rsa = encrypt_rsa(llave_publica, mensaje)
    fin_rsa_enc = time.perf_counter()
    
    inicio_rsa_dec = time.perf_counter()
    _ = decrypt_rsa(llave_privada, texto_cifrado_rsa)
    fin_rsa_dec = time.perf_counter()
    
    tiempo_rsa_enc = (fin_rsa_enc - inicio_rsa_enc) * 1000
    tiempo_rsa_dec = (fin_rsa_dec - inicio_rsa_dec) * 1000
    
    print(f"Tiempo de Cifrado RSA:   {tiempo_rsa_enc:.4f} ms")
    print(f"Tiempo de Descifrado RSA: {tiempo_rsa_dec:.4f} ms")
    
    # --- Conclusion rapida ---
    print("\n--- RESUMEN ---")
    if tiempo_rsa_enc > tiempo_aes_enc:
        diferencia = tiempo_rsa_enc / tiempo_aes_enc if tiempo_aes_enc > 0 else 0
        print(f"AES fue aproximadamente {diferencia:.0f} veces más rápido que RSA al cifrar.")

if __name__ == "__main__":
    run_performance_test()