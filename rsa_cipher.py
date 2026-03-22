from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def generate_rsa_keys():
    # Generar una llave privada de 2048 bits (tamaño recomendado para seguridad)
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    # Extraemos la llave publica a partir de la privada
    public_key = private_key.public_key()
    return private_key, public_key

def encrypt_rsa(public_key, message):
    # Ciframos usando la llave publica y padding OAEP con SHA256
    ciphertext = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

def decrypt_rsa(private_key, ciphertext):
    # Desciframos usando la llave privada y el mismo padding OAEP con SHA256
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label= None
        )
    )
    return plaintext.decode()


# --- Prueba del script simulando el caso de la clinica ---
if __name__ == "__main__":
    print("--- Iniciando prueba RSA ---")

    # Generamos el par de llaves para la clinica
    print("Generando par de llaves RSA (esto puede tardar unos segundos)...")
    llave_privada, llave_publica = generate_rsa_keys()

    # Simulamos datos personales de un paciente
    datos_paciente = "Nombre: Ana M. -Tel: 555-0192 - Seguro: Vidaplus 9928"
    print(f"Datos originales del paciente: {datos_paciente}")

    # Ciframos los datos del paciente usando la llave publica
    texto_cifrado = encrypt_rsa(llave_publica, datos_paciente)
    print(f"Datos cifrados (Hexadecimal): {texto_cifrado.hex()[:60]}... (Truncado)")

    # Desciframos los datos usando la llave privada
    texto_recuperado = decrypt_rsa(llave_privada, texto_cifrado)
    print(f"Datos recuperados: {texto_recuperado}")