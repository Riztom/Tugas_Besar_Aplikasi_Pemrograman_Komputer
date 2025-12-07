<img width="744" height="276" alt="image" src="https://github.com/user-attachments/assets/e63e0c0c-0e70-4e1b-b645-8b0f4da806ab" />

# 📦Fitur Pada Program️

| Fitur                                | Deskripsi                                                       |
| ------------------------------------ | --------------------------------------------------------------- |
| 💸 Split Bill Otomatis               | Membagi tagihan secara adil berdasarkan kontribusi              |
| 🧮 Presisi Decimal                   | Perhitungan uang akurat tanpa error pembulatan                  |
| 📝 CLI Mode                          | Input langsung via command line (`--names`, `--pay`, `--total`) |
| 👤 Interactive Mode                  | Input data lewat terminal jika argumen kurang                   |
| 🇮🇩 Format Rupiah                   | Output tampil rapih: `Rp 100.000,00`                            |
| 📊 Ringkasan Pembayaran              | Menampilkan siapa **bayar** atau **terima** berapa              |
| ⚠️ Validasi Input                    | Deteksi nilai negatif, jumlah nama tidak cocok, dsb             |
| 🧾 Residual Info                     | Menampilkan sisa pembulatan dan opsi penyesuaian                |
| 💾 Bisa Dipakai untuk Kos / Keluarga | Fleksibel untuk berbagai kebutuhan patungan                     |

# 🖥️Output Program Split Bill Kost/Keluarga (Decimal,CLI)
<img width="767" height="370" alt="image" src="https://github.com/user-attachments/assets/918720a6-aa66-4518-8a04-e10f347e1a52" />

# Command Line Pada Hasil Output✏️
python "Tubes.py" --names Arul Rizqi Rome --pay 500000 400000 300000 --total 1300000

# 🧑‍🏫Penjelasan Singkat Program Split Bill Kost/Keluarga (Decimal,CLI)
Script ini adalah program pembagi tagihan (split bill) untuk kos/keluarga yang memiliki dua mode input:

1️⃣ Interactive Mode (Mode Interaktif)

📌 Aktif jika:

- Argumen CLI tidak lengkap
- User menjalankan script tanpa --names dan --pay
  
➡️ Program akan meminta input lewat input() satu per satu:

- Jumlah orang
- Nama dan kontribusi masing-masing
- Total tagihan

Fungsinya:

interactive_mode()

2️⃣ CLI Mode

📌 Aktif jika --names dan --pay diberikan lewat Command Line

➡️ Tidak perlu input manual

Fungsinya:

cli_mode(args)

3️⃣ Decimal Handling

Program memakai modul:

from decimal import Decimal, InvalidOperation, getcontext, ROUND_HALF_UP

Digunakan agar uang selalu akurat dan tidak salah pembulatan seperti float biasa.

➡️ Decimal digunakan ketika:

- Mengubah input uang → to_decimal()
- Menghitung porsi rata
- Pembulatan 2 desimal (uang)

4️⃣ Fungsi format Rupiah

Digunakan untuk menampilkan angka seperti:

Rp 150.000,00

Fungsinya:

format_rupiah(d: Decimal) -> str

5️⃣ Pengecekan Validasi

- Nama tidak boleh kosong
- Kontribusi harus angka
- Total tidak boleh negatif
- Jumlah nama dan kontribusi harus sama

6️⃣ Perhitungan Split Bill

- Hitung porsi rata-rata, selisih kontribusi, dan status bayar/terima
- Cek apakah total kontribusi kurang/lebih
- Ada residual pembulatan bila rata-rata berbasis uang tidak presisi
