from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

def pad(data):
    padding_length = 16 - len(data) % 16
    return data + bytes([padding_length] * padding_length)

def aes_encrypt_file(plaintext, key):
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    padded = pad(plaintext)
    encrypted = cipher.encrypt(padded)

    encrypted_bytes = iv + encrypted
    encrypted_b64 = base64.b64encode(encrypted_bytes).decode("utf-8")

    return encrypted_b64
