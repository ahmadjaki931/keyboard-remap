# ⌨️ Multi-Key Registry Blocker

Aplikasi GUI berbasis Python (Tkinter) untuk memblokir sinyal tombol keyboard yang mengalami *short circuit*, *ghosting*, atau rusak (seperti tombol Power `255`, Caps Lock, Sleep) secara permanen di tingkat sistem operasi menggunakan Windows Registry (`Scancode Map`).

Sangat cocok untuk pengguna laptop yang sering mengalami masalah tombol *power* tertekan sendiri atau laptop yang mendadak gagal *sleep*.

---

## ✨ Fitur Utama

- **Atasi Ghosting/Short Circuit:** Memblokir input sinyal mentah (*scancode*) dari keyboard sebelum diproses oleh sistem.
- **Dukungan Banyak Tombol (Multi-Key):** Memblokir beberapa tombol sekaligus dalam satu kali eksekusi.
- **Preset & Input Manual:** Disediakan tombol preset umum (Power, Sleep, Caps Lock, Win Key) serta kolom input manual Scan Code Hex (dipisahkan koma).
- **Dialog Bantuan Interaktif:** Dilengkapi tabel referensi lengkap *Scan Code* keyboard (F1-F12, Numpad, Media Keys, Modifiers, dll).
- **Ringan & Tanpa Modul Luar:** Menggunakan pustaka standar Python (`winreg`, `tkinter`, `ctypes`), tidak perlu melakukan `pip install`.
- **Eksekusi Permanen:** Berjalan di level registry Windows tanpa perlu menjalankan aplikasi secara terus-menerus di *background*.
- **Otomatis Minta Akses Admin:** Memicu *UAC Prompt* otomatis untuk mendapatkan akses penulisan ke `HKEY_LOCAL_MACHINE`.
- **Fitur Reset:** Dilengkapi tombol untuk menghapus konfigurasi registry dan mengembalikan keyboard ke kondisi default.

---

## 🛠️ Prasyarat

- **Sistem Operasi:** Windows 10 / Windows 11
- **Bahasa Pemrograman:** Python 3.x

---

## 🚀 Cara Penggunaan

1. **Unduh / Clone Repositori:**
   ```bash
   git clone [https://github.com/username/multi-key-registry-blocker.git](https://github.com/username/multi-key-registry-blocker.git)
   cd multi-key-registry-blocker
   
2. **Jalankan Aplikasi:**
Klik ganda pada file .py atau jalankan via Terminal/Command Prompt:

```bash
  python keyboard-remap.py
  (Aplikasi akan otomatis meminta izin Run as Administrator).
```

3. **Langkah Memblokir Tombol:**
- Centang opsi tombol preset yang ingin diblokir, ATAU
- Ketik kode Scan Code manual pada kolom yang tersedia (pisahkan dengan koma jika lebih dari satu, contoh: E05E, E05F, 3A).
- Tekan tombol ❓ Help / Daftar Kode untuk melihat tabel referensi kode hex tombol.
- Klik Terapkan Blokir.
- Restart laptop/PC Anda agar Windows memperbarui pemetaan keyboard.

## ⚠️ Catatan Penting
Perubahan registry ini membutuhkan Restart/Reboot sistem operasi agar Scancode Map baru dibaca oleh driver input Windows.

Jika Anda telah mengganti keyboard fisik yang rusak dengan modul keyboard baru, cukup buka aplikasi ini lalu klik Reset ke Default dan restart PC Anda.

## 📄 Lisensi
Proyek ini dirilis di bawah lisensi MIT License.
