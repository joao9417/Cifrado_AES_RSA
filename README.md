# Cifrado AES, RSA y Sistema Híbrido

Este repositorio contiene diversos ejercicios y pruebas de concepto relacionados con algoritmos de criptografía, específicamente AES (Advanced Encryption Standard) y RSA (Rivest-Shamir-Adleman), así como la implementación de un sistema híbrido que combina ambos para alcanzar un mayor nivel de seguridad.

## Contenido del Repositorio

El proyecto se compone de los siguientes scripts principales:

- **Ejercicios de Cifrado:**
  - `aes_cipher.py`: Implementación de cifrado y descifrado utilizando el algoritmo simétrico AES.
  - `rsa_cipher.py`: Implementación de cifrado y descifrado utilizando el algoritmo asimétrico RSA.

- **Ataques a los Algoritmos:**
  - `ataque_aes.py`: Demostración o simulación de posibles vulnerabilidades o ataques sobre la implementación de AES.
  - `ataque_rsa.py`: Demostración o simulación de ataques sobre la implementación de RSA (por ejemplo, cuando se emplean claves débiles).

- **Evaluación de Rendimiento:**
  - `perfomance_test.py`: Script diseñado para medir y comparar el rendimiento (tiempos de ejecución, coste computacional) entre los algoritmos de cifrado AES y RSA bajo diferentes escenarios.

- **Sistema Híbrido:**
  - `sistema_hibrido.py`: Implementación de un sistema criptográfico híbrido que combina la velocidad del cifrado simétrico (AES) para los datos y la seguridad del cifrado asimétrico (RSA) para la transmisión segura de las claves. Además, implementa una firma HMAC para detectar modificaciones fraudulentas en la información antes de procesarla, evitando así desbordamientos o paradas abruptas en el sistema.

## Requisitos

Las dependencias necesarias para ejecutar estos scripts se encuentran en el archivo `requirements.txt`. Puedes instalarlas creando un entorno virtual y ejecutando el siguiente comando:

```bash
pip install -r requirements.txt
```
