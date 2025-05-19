from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    hasil_enkripsi = ""
    pesan_asli = ""

    if request.method == 'POST':
        # Ambil dari textarea
        pesan_asli = request.form.get('plaintext')

        # Cek kalau ada file di-upload
        file = request.files.get('file')
        if file and file.filename != '':
            pesan_asli = file.read().decode('utf-8')

        # Contoh proses enkripsi dummy (asli-nya nanti diganti dengan AES kamu)
        hasil_enkripsi = pesan_asli[::-1]  # Balik string doang buat contoh

    return render_template('encrypt.html', request=request, hasil=hasil_enkripsi, pesan=pesan_asli)


@app.route('/decrypt')
def decrypt():
    return render_template('decrypt.html')

if __name__ == '__main__':
    app.run(debug=True)
