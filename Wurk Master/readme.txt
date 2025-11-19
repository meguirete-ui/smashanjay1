# 🚀 WURK ULTIMATE BOT (v3.8)
**All-in-One Twitter/X Automation & Analytics Tool**

Script Python canggih untuk mengelola "ternak" akun Twitter, melakukan raid otomatis (RT/Like/Follow), mengintip data follower kompetitor, dan mengecek kesehatan akun secara massal.

---

## 🔥 FITUR UTAMA

1.  **⚡ Wurk Assistant (Raid Mode)**
    * Auto Retweet, Like, & Follow target.
    * **On-Demand Speed:** Atur kecepatan (Safe/Normal/Turbo) langsung saat beraksi.
    * **Smart Fallback:** Tetap jalan meskipun link tweet tidak terbaca sempurna.
2.  **🕵️‍♂️ Scraper Pro**
    * Ambil data **Follower** atau **Following** dari target.
    * Menampilkan **Umur Akun** (misal: 3 Bulan, 5 Tahun) untuk analisa kualitas audience.
    * **Pagination Otomatis:** Bisa mengambil ribuan data tanpa putus.
3.  **🏥 Health Checker**
    * Cek massal apakah list akunmu masih **Hidup**, **Suspend**, atau **Hilang**.
    * **Smart Filter:** Cukup masukkan file teks berantakan, script otomatis mendeteksi username (dengan atau tanpa `@`).
4.  **💾 Session Manager**
    * Login via Cookies (Anti Error 404 & Login Challenge).
    * **Export/Import:** Backup semua akun ke file ZIP (mudah dipindah antar device).
5.  **🛡️ Anti-Detect**
    * Menggunakan User-Agent Chrome Windows asli untuk menghindari deteksi bot.

---

## 📱 CARA INSTALASI: TERMUX (ANDROID)

1.  **Buka Termux**, lalu jalankan perintah berikut satu per satu (Copy-Paste):

    ```bash
    termux-setup-storage
    ```
    *(Klik "Allow" jika muncul popup izin)*

    ```bash
    pkg update && pkg upgrade -y
    ```

2.  **Install Paket Pendukung** (Wajib agar tidak error saat install library):
    ```bash
    pkg install python rust binutils libjpeg-turbo git -y
    ```

3.  **Install Library Python**:
    ```bash
    pip install --upgrade pip
    pip install twikit rich
    ```

4.  **Jalankan Script**:
    Pastikan file `wurk_ultimate.py` sudah ada di folder Termux (bisa dipindah dari folder Download HP).
    ```bash
    python wurk_ultimate.py
    ```

---

## 💻 CARA INSTALASI: VS CODE (WINDOWS/PC)

1.  **Install Python**:
    * Download dari [python.org](https://www.python.org/downloads/).
    * **⚠️ PENTING:** Saat instalasi, centang kotak **"Add Python.exe to PATH"** di bagian bawah.

2.  **Siapkan Folder**:
    * Buat folder baru (misal: `WurkBot`).
    * Masukkan file `wurk_ultimate.py` ke dalamnya.
    * Klik kanan folder tersebut > **Open with Code** (atau buka terminal di folder itu).

3.  **Install Library**:
    Buka Terminal di VS Code (`Ctrl` + `` ` ``), lalu ketik:
    ```powershell
    pip install twikit rich
    ```

4.  **Jalankan Script**:
    ```powershell
    python wurk_ultimate.py
    ```

---

## 🔑 CARA LOGIN (AMBIL COOKIES)

Script ini tidak menggunakan password (karena rawan checkpoint), melainkan menggunakan **Cookies**.

1.  Buka browser (Chrome di PC atau Kiwi Browser di Android).
2.  Login ke akun Twitter/X kamu.
3.  Buka **Developer Tools** (Tekan `F12` di PC, atau Menu > Developer Tools di Kiwi).
4.  Pilih tab **Application** (atau Storage).
5.  Di menu kiri, klik **Cookies** > `https://twitter.com` (atau x.com).
6.  Cari dan Copy isi (Value) dari dua nama ini:
    * `auth_token`
    * `ct0`



7.  Di Script, pilih menu **[4] Tambah Akun Baru**, lalu paste kode tersebut.

---

## 📖 PANDUAN FITUR

### 1. Melakukan Raid (Wurk Assistant)
* Pilih menu `[1]`.
* Masukkan **Link Tweet Lengkap** (Contoh: `https://x.com/user/status/123...`).
* Pilih Template Aksi (RT Only / Like / Follow).
* Pilih Kecepatan:
    * 🐢 **Safe:** Jeda 30-60 detik (Untuk akun utama).
    * 🚗 **Normal:** Jeda 10-20 detik (Standar).
    * 🚀 **Turbo:** Jeda 1-3 detik (Resiko tinggi, untuk akun bodong).

### 2. Cek Kesehatan Akun
* Siapkan file `.txt` (misal: `list_akun.txt`) berisi daftar username.
* Isinya boleh campur aduk, contoh:
    ```text
    @akun1
    akun2
    Data akun: @akun3
    ```
* Script akan otomatis menyaring username dan mengecek statusnya.

### 3. Backup & Pindah Device
* Pilih menu `[6] Export Sessions`.
* File `sessions_backup.zip` akan muncul.
* Kirim file itu ke HP/Laptop baru.
* Di device baru, pilih menu `[7] Import Sessions`.

---

## ⚠️ DISCLAIMER

Script ini dibuat untuk tujuan edukasi dan manajemen akun pribadi.
* **Gunakan dengan bijak.** Terlalu agresif (spamming/turbo mode terus-menerus) dapat menyebabkan akun terkunci (Locked) atau ditangguhkan (Suspended) oleh Twitter.
* Penulis tidak bertanggung jawab atas risiko yang terjadi pada akun Anda.

---
*Created with ❤️ by Wurk Master*


# 🚀 WURK ULTIMATE WEB (v4.2)
**All-in-One Twitter Automation Dashboard (Localhost)**

Versi terbaru Wurk Ultimate kini hadir dengan tampilan **Web Dashboard** yang modern! Tidak perlu lagi mengetik perintah rumit di layar hitam. Cukup klik-klik tombol di browser, semua jalan otomatis.

---

## 🔥 FITUR BARU (WEB EDITION)
* **🖥️ GUI Dashboard:** Tampilan visual yang mudah digunakan (seperti admin panel).
* **🛡️ Anti-Rate Limit:** Sistem delay pintar untuk mencegah error 429 (Too Many Requests).
* **🔒 Private Account Check:** Otomatis mendeteksi akun digembok saat scraping agar tidak error.
* **💾 Auto-Save:** Jika scraping terhenti di tengah jalan, data yang sudah didapat tidak akan hilang.
* **📊 Progress Bar:** Visualisasi loading saat Raid atau Scraping.

---

## 📱 CARA INSTALASI: TERMUX (ANDROID)

1.  **Update & Install Paket Dasar:**
    Buka Termux, jalankan perintah ini satu per satu:
    ```bash
    termux-setup-storage
    pkg update && pkg upgrade -y
    pkg install python rust binutils libjpeg-turbo git -y
    ```

2.  **Install Library (Wajib):**
    Kita butuh `streamlit` untuk menjalankan web server.
    ```bash
    pip install --upgrade pip
    pip install twikit streamlit
    ```

3.  **Menjalankan Script:**
    Pastikan file script bernama `app.py`.
    ```bash
    streamlit run app.py
    ```

4.  **Membuka Dashboard:**
    * Termux akan memunculkan tulisan: `Local URL: http://localhost:8501`.
    * Klik link tersebut (atau copy-paste ke Chrome/Kiwi Browser).
    * **TADAA!** Dashboard Wurk Ultimate akan muncul di browsermu.
    * *(Untuk mematikan script, tekan `CTRL + C` di Termux).*

---

## 💻 CARA INSTALASI: VS CODE (WINDOWS/PC)

1.  **Install Python:**
    * Download [Python 3.12](https://www.python.org/downloads/).
    * **⚠️ PENTING:** Centang **"Add Python to PATH"** saat install.

2.  **Siapkan Folder:**
    * Buat folder `WurkBot`.
    * Masukkan file script dengan nama `app.py`.
    * Klik kanan folder -> **Open with Code**.

3.  **Install Library:**
    Buka Terminal VS Code (`Ctrl` + `` ` ``), ketik:
    ```powershell
    pip install twikit streamlit
    ```

4.  **Menjalankan Script:**
    Ketik perintah ini di terminal:
    ```powershell
    streamlit run app.py
    ```
    * Browser (Chrome/Edge) akan otomatis terbuka dan menampilkan dashboard.

---

## 🔑 CARA LOGIN (COOKIES)

Karena ini tool otomatisasi, kita login menggunakan **Cookies** (lebih aman dari password).

1.  Buka browser (Chrome Desktop / Kiwi Browser Android).
2.  Login ke **Twitter/X**.
3.  Buka **Developer Tools** (Tekan `F12` -> Tab **Application** -> **Cookies**).
4.  Cari `auth_token` dan `ct0`. Copy isinya.
5.  Buka Dashboard Wurk Ultimate -> Menu **Akun Manager**.
6.  Paste Username, auth_token, dan ct0 -> Klik **Simpan Akun**.

---

## 📖 PANDUAN MENU DASHBOARD

### 1. 🚀 Raid Assistant
Gunakan ini untuk "menyerang" tweet target.
* Paste Link Tweet.
* Centang aksi (RT / Like / Follow).
* Atur kecepatan (Min/Max Delay) agar aman.
* Klik **GAS RAID**.

### 2. 🕵️‍♂️ Scraper Pro
Gunakan ini untuk mengambil data follower kompetitor.
* Masukkan Username target.
* Pilih mode (Followers/Following).
* Tentukan jumlah ambil.
* Klik **Ambil Data**.
* Jika selesai, tombol **Download TXT** akan muncul.

### 3. 🏥 Health Checker
Gunakan ini untuk mengecek kondisi akun ternakmu.
* Paste daftar username (bisa banyak sekaligus).
* Klik **Cek**.
* Hasil akan menunjukkan mana yang **ACTIVE**, **SUSPENDED**, atau **LOCKED**.

---

## ❓ SOLUSI MASALAH (TROUBLESHOOTING)

**Q: Muncul Error `429: Rate limit exceeded`?**
A: Anda terlalu cepat! Twitter memblokir IP sementara.
* Solusi: Stop dulu 15-30 menit. Ganti koneksi (Wifi ke Data) untuk refresh IP.

**Q: Error `404` atau `401` saat Scraping?**
A: Target akun kemungkinan di-private (digembok) atau username salah.

**Q: Gagal Install `streamlit` di Windows?**
A: Pastikan Python sudah terinstall dengan benar (Add to PATH). Jika error `C++ Build Tools`, coba gunakan Python versi 3.11 atau 3.12 yang lebih stabil.

---
*Created with ❤️ by Wurk Master*