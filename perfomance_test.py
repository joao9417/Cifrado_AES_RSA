import time
import os
from aes_cipher import encrypt_aes, decrypt_aes
from rsa_cipher import generate_rsa_keys, encrypt_rsa, decrypt_rsa

def run_accurate_performance_test():
    print("--- Prueba de rendimiento real (promedio de 100 interaciones) ---")
    mensaje = "Datos del paciente para prueba de carga masiva."
    iteraciones = 100
    
    # Ejecutamos una vez al vacío para que el motor OpenSSL cargue y no afecte los tiempos
    clave_aes_dummy = os.urandom(32)
    encrypt_aes(mensaje, clave_aes_dummy)

    # --- Prueba AES ---
    clave_aes = os.urandom(32)
    inicio_aes = time.perf_counter()
    for _ in range(iteraciones):
        iv, cifrado = encrypt_aes(mensaje, clave_aes)
        _ = decrypt_aes(iv, cifrado, clave_aes)
    fin_aes = time.perf_counter()
    tiempo_promedio_aes = ((fin_aes - inicio_aes) / iteraciones) * 1000

    # --- Prueba RSA ---
    llave_privada, llave_publica = generate_rsa_keys()
    inicio_rsa = time.perf_counter()
    for _ in range(iteraciones):
        cifrado = encrypt_rsa(llave_publica, mensaje)
        _ = decrypt_rsa(llave_privada, cifrado)
    fin_rsa = time.perf_counter()
    tiempo_promedio_rsa = ((fin_rsa - inicio_rsa) / iteraciones) * 1000

    print(f"\n[1] AES-256 (Simétrico) - Tiempo promedio por operación: {tiempo_promedio_aes:.4f} ms")
    print(f"[2] RSA-2048 (Asimétrico) - Tiempo promedio por operación: {tiempo_promedio_rsa:.4f} ms")
    print(f"\n[!] CONCLUSIÓN: AES es aproximadamente {tiempo_promedio_rsa/tiempo_promedio_aes:.0f} veces más rápido que RSA.")

if __name__ == "__main__":
    run_accurate_performance_test()
