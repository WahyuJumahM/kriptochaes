from flask import Flask, render_template, request
from encoder import encode_for_web
from decoder import decode_for_web
from encrypt import aes_encrypt_file
from decrypt import aes_decrypt_bytes
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/encrypt", methods=["GET", "POST"])
def encrypt():
    key = b'1234567890abcdef'
    steps = []
    aes_output = ""
    if request.method == "POST":
        file = request.files["file"]
        if file:
            file_content = file.read()
            encrypted_b64 = aes_encrypt_file(file_content, key)
            aes_output = encrypted_b64
            encrypted_bytes = base64.b64decode(encrypted_b64)
            steps, pgn_output = encode_for_web(encrypted_bytes)
            with open("output/encrypted.pgn", "w") as f:
                f.write("\n\n".join(pgn_output))
    return render_template("encrypt.html", steps=steps, aes_output=aes_output)

@app.route("/decrypt", methods=["GET", "POST"])
def decrypt():
    key = b"1234567890abcdef"
    steps = []
    decrypted_text = ""
    if request.method == "POST":
        file = request.files["file"]
        if file:
            input_byte = file.read()
            input_pgn = input_byte.decode("utf-8")
            encrypted_bytes, steps = decode_for_web(input_pgn)
            
            # Ambil IV dari 16 byte pertama
            iv = encrypted_bytes[:16]
            ciphertext = encrypted_bytes[16:]

            # Decrypt
            plaintext = aes_decrypt_bytes(ciphertext, key, iv)

            decrypted_text = plaintext.decode(errors="ignore")

    return render_template("decrypt.html", result=decrypted_text, steps=steps)

if __name__ == "__main__":
    app.run(debug=True)
