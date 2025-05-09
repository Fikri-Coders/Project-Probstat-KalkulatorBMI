from flask import Flask, render_template, request

app = Flask(__name__)

def hitung_bmi(berat, tinggi):
    return berat / (tinggi * tinggi)

def hitung_rata_rata(data):
    if len(data) == 0:
        return 0
    total = 0
    for nilai in data:
        total += nilai
    return total / len(data)

def hitung_median(data):
    if len(data) == 0:
        return 0
    data_urut = sorted(data)
    panjang = len(data_urut)
    tengah = panjang // 2
    if panjang % 2 == 1:
        return data_urut[tengah]
    return (data_urut[tengah - 1] + data_urut[tengah]) / 2

def cari_modus(data):
    if len(data) == 0:
        return "Tidak ada modus"
    frekuensi = {}
    for nilai in data:
        if nilai in frekuensi:
            frekuensi[nilai] += 1
        else:
            frekuensi[nilai] = 1

    modus = 0
    max_kemunculan = 0
    for nilai, jumlah in frekuensi.items():
        if jumlah > max_kemunculan:
            max_kemunculan = jumlah
            modus = nilai
    if max_kemunculan == 1:
        return "Tidak ada modus"
    return modus

@app.route('/', methods=['GET', 'POST'])
def beranda():
    if request.method == 'POST':
        try:
            jumlah_orang = int(request.form.get('jumlah_orang', 1))
            return render_template('bmi_form.html', jumlah_orang=jumlah_orang)
        except ValueError:
            return render_template('index.html', pesan_error="Masukkan angka yang benar.")
    return render_template('index.html')

@app.route('/hitung', methods=['POST'])
def hitung():
    jumlah_orang = int(request.form.get('jumlah_orang', 1))
    berat_badan = []
    tinggi_badan = []
    bmi = []
    

    for i in range(jumlah_orang):
        try:
            berat = float(request.form.get(f'berat_{i}', 0))
            tinggi_cm = float(request.form.get(f'tinggi_{i}', 0))
            tinggi_m = tinggi_cm / 100

            if berat > 0 and tinggi_m > 0:
                nilai_bmi = hitung_bmi(berat, tinggi_m)
            else:
                nilai_bmi = 0

            berat_badan.append(berat)
            tinggi_badan.append(tinggi_cm)
            bmi.append(nilai_bmi)
        except ValueError:
            berat_badan.append(0)
            tinggi_badan.append(0)
            bmi.append(0)


    stat = {
        'rata_rata_berat': hitung_rata_rata(berat_badan),
        'median_berat': hitung_median(berat_badan),
        'modus_berat': cari_modus(berat_badan),
        'rata_rata_tinggi': hitung_rata_rata(tinggi_badan),
        'median_tinggi': hitung_median(tinggi_badan),
        'modus_tinggi': cari_modus(tinggi_badan),
        'rata_rata_bmi': hitung_rata_rata(bmi),
        'median_bmi': hitung_median(bmi),
        'modus_bmi': cari_modus(bmi),
    }

    return render_template('bmi_form.html', jumlah_orang=jumlah_orang, berat=berat_badan, tinggi=tinggi_badan, bmi=bmi, stat=stat)

if __name__ == '__main__':
    app.run(debug=True)