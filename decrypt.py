from Crypto.Cipher import AES

def unpad(data):
    padding_length = data[-1]
    return data[:-padding_length]

def aes_decrypt_bytes(encrypted_bytes, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_padded = cipher.decrypt(encrypted_bytes)
    return unpad(decrypted_padded)
