import sys
import winreg
import ctypes
import tkinter as tk
from tkinter import ttk, messagebox

# Daftar Tombol Preset (Format Little Endian Hex)
PRESET_SCAN_CODES = {
    "Power Key (255 / E0 5E)": "5EE0",
    "Sleep Key (E0 5F)": "5FE0",
    "Wake Key (E0 63)": "63E0",
    "Caps Lock (00 3A)": "3A00",
    "Windows Key Kiri (E0 5B)": "5BE0",
    "Windows Key Kanan (E0 5C)": "5CE0"
}

# Referensi Scan Code Lengkap untuk Dialog Help
HELP_SCAN_CODES = [
    # System & Power Management
    ("Power Key", "E0 5E", "Tombol Power Management / VK 255"),
    ("Sleep Key", "E0 5F", "Tombol Mode Sleep Hardware"),
    ("Wake Key", "E0 63", "Tombol Wake / Membangunkan Sistem"),
    
    # Modifier Keys
    ("Caps Lock", "00 3A", "Tombol Caps Lock"),
    ("Left Windows", "E0 5B", "Tombol Windows Kiri"),
    ("Right Windows", "E0 5C", "Tombol Windows Kanan"),
    ("Left Ctrl", "00 1D", "Tombol Control Kiri"),
    ("Right Ctrl", "E0 1D", "Tombol Control Kanan"),
    ("Left Alt", "00 38", "Tombol Alt Kiri"),
    ("Right Alt (AltGr)", "E0 38", "Tombol Alt Kanan"),
    ("Left Shift", "00 2A", "Tombol Shift Kiri"),
    ("Right Shift", "00 36", "Tombol Shift Kanan"),
    ("Application / Menu", "E0 5D", "Tombol Menu Klik Kanan Keyboard"),

    # Navigation & Editing Keys
    ("Escape (Esc)", "00 01", "Tombol Esc"),
    ("Spacebar", "00 39", "Tombol Spasi"),
    ("Enter Utama", "00 1C", "Tombol Enter"),
    ("Backspace", "00 0E", "Tombol Hapus Kiri"),
    ("Tab", "00 0F", "Tombol Tab"),
    ("Insert", "E0 52", "Tombol Insert"),
    ("Delete", "E0 53", "Tombol Delete"),
    ("Home", "E0 47", "Tombol Home"),
    ("End", "E0 4F", "Tombol End"),
    ("Page Up", "E0 49", "Tombol Page Up"),
    ("Page Down", "E0 51", "Tombol Page Down"),
    ("Panah Atas", "E0 48", "Tombol Navigasi Atas"),
    ("Panah Bawah", "E0 50", "Tombol Navigasi Bawah"),
    ("Panah Kiri", "E0 4B", "Tombol Navigasi Kiri"),
    ("Panah Kanan", "E0 4D", "Tombol Navigasi Kanan"),

    # Function Keys (F1 - F12)
    ("F1", "00 3B", "Tombol Function F1"),
    ("F2", "00 3C", "Tombol Function F2"),
    ("F3", "00 3D", "Tombol Function F3"),
    ("F4", "00 3E", "Tombol Function F4"),
    ("F5", "00 3F", "Tombol Function F5"),
    ("F6", "00 40", "Tombol Function F6"),
    ("F7", "00 41", "Tombol Function F7"),
    ("F8", "00 42", "Tombol Function F8"),
    ("F9", "00 43", "Tombol Function F9"),
    ("F10", "00 44", "Tombol Function F10"),
    ("F11", "00 57", "Tombol Function F11"),
    ("F12", "00 58", "Tombol Function F12"),

    # Numpad Keys
    ("Num Lock", "00 45", "Tombol Num Lock"),
    ("Numpad Enter", "E0 1C", "Tombol Enter pada Numpad"),
    ("Numpad Slash (/)", "E0 35", "Tombol Pembagi Numpad"),
    ("Numpad Star (*)", "00 37", "Tombol Pengali Numpad"),
    ("Numpad Minus (-)", "00 4A", "Tombol Pengurang Numpad"),
    ("Numpad Plus (+)", "00 4E", "Tombol Penambah Numpad"),
    ("Numpad Period (.)", "00 53", "Tombol Titik/Desimal Numpad"),
    ("Numpad 0", "00 52", "Tombol Angka 0 Numpad"),
    ("Numpad 1", "00 4F", "Tombol Angka 1 Numpad"),
    ("Numpad 2", "00 50", "Tombol Angka 2 Numpad"),
    ("Numpad 3", "00 51", "Tombol Angka 3 Numpad"),
    ("Numpad 4", "00 4B", "Tombol Angka 4 Numpad"),
    ("Numpad 5", "00 4C", "Tombol Angka 5 Numpad"),
    ("Numpad 6", "00 4D", "Tombol Angka 6 Numpad"),
    ("Numpad 7", "00 47", "Tombol Angka 7 Numpad"),
    ("Numpad 8", "00 48", "Tombol Angka 8 Numpad"),
    ("Numpad 9", "00 49", "Tombol Angka 9 Numpad"),

    # Media & Volume Controls
    ("Mute Audio", "E0 20", "Matikan Suara System"),
    ("Volume Down", "E0 2E", "Kecilkan Volume System"),
    ("Volume Up", "E0 30", "Besarkan Volume System"),
    ("Media Play/Pause", "E0 22", "Play/Pause Media Player"),
    ("Media Stop", "E0 24", "Stop Media Player"),
    ("Media Previous", "E0 10", "Lagu / Track Sebelumnya"),
    ("Media Next", "E0 19", "Lagu / Track Selanjutnya"),
    ("Web Home", "E0 32", "Buka Browser Home"),
    ("Calculator", "E0 21", "Buka Aplikasi Kalkulator")
]

REG_PATH = r"SYSTEM\CurrentControlSet\Control\Keyboard Layout"
REG_KEY_NAME = "Scancode Map"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def format_hex_scancode(hex_str):
    clean_hex = hex_str.strip().upper().replace("0X", "").replace(" ", "")
    if len(clean_hex) == 2:
        clean_hex = "00" + clean_hex
    elif len(clean_hex) == 3:
        clean_hex = "0" + clean_hex
    
    if len(clean_hex) != 4:
        raise ValueError(f"Scan code '{hex_str}' tidak valid (harus 2 atau 4 karakter hex).")
    
    # Swap byte order ke Little Endian (2 byte)
    byte1 = clean_hex[0:2]
    byte2 = clean_hex[2:4]
    return byte2 + byte1

class MultiKeyRegistryRemapper:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Key Registry Blocker")
        self.root.geometry("500x520")
        self.root.resizable(False, False)

        # Header Title
        title_frame = ttk.Frame(root)
        title_frame.pack(fill="x", padx=15, pady=10)
        
        ttk.Label(title_frame, text="Multi-Key Registry Blocker", font=("Helvetica", 14, "bold")).pack(side="left")
        ttk.Button(title_frame, text="❓ Help / Daftar Kode", command=self.show_help_dialog).pack(side="right")

        # Frame Preset Checkbox
        frame_preset = ttk.LabelFrame(root, text=" Pilih Tombol Preset ", padding=10)
        frame_preset.pack(fill="x", padx=15, pady=5)

        self.check_vars = {}
        for key_name in PRESET_SCAN_CODES.keys():
            var = tk.IntVar()
            chk = ttk.Checkbutton(frame_preset, text=key_name, variable=var)
            chk.pack(anchor="w", pady=1)
            self.check_vars[key_name] = var

        # Frame Manual Input
        frame_manual = ttk.LabelFrame(root, text=" Input Manual Scan Code ", padding=10)
        frame_manual.pack(fill="x", padx=15, pady=5)

        ttk.Label(frame_manual, text="Masukkan Scan Code Hex (pisahkan dengan koma):").pack(anchor="w")
        self.entry_manual = ttk.Entry(frame_manual, width=50)
        self.entry_manual.pack(fill="x", pady=5)
        
        ttk.Label(
            frame_manual, 
            text="Contoh: E05E, E05F, 3A  atau  E0 5E, E0 5F", 
            font=("Helvetica", 8, "italic"),
            foreground="gray"
        ).pack(anchor="w")

        # Status Label
        self.lbl_status = ttk.Label(root, text="Status: Periksa registry...", font=("Helvetica", 9, "italic"))
        self.lbl_status.pack(pady=5)

        # Action Buttons
        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Terapkan Blokir", command=self.apply_multi_block).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Reset ke Default", command=self.reset_registry).pack(side="left", padx=5)

        self.check_status()

    def show_help_dialog(self):
        """Menampilkan jendela dialog berisi tabel referensi Scan Code."""
        help_win = tk.Toplevel(self.root)
        help_win.title("Daftar Kode & Tombol Keyboard")
        help_win.geometry("520x400")
        help_win.resizable(False, False)
        
        # Biarkan dialog muncul di atas jendela utama
        help_win.transient(self.root)
        help_win.grab_set()

        ttk.Label(
            help_win, 
            text="Referensi Scan Code Hex Standar Windows", 
            font=("Helvetica", 11, "bold")
        ).pack(pady=10)

        # Container Frame untuk Treeview + Scrollbar
        container = ttk.Frame(help_win)
        container.pack(fill="both", expand=True, padx=15, pady=5)

        # Membuat Tabel (Treeview)
        columns = ("tombol", "code", "keterangan")
        tree = ttk.Treeview(container, columns=columns, show="headings", height=12)

        tree.heading("tombol", text="Nama Tombol")
        tree.heading("code", text="Scan Code (Hex)")
        tree.heading("keterangan", text="Keterangan / Fungsi")

        tree.column("tombol", width=140, anchor="w")
        tree.column("code", width=110, anchor="center")
        tree.column("keterangan", width=220, anchor="w")

        # Masukkan Data Scan Code
        for item in HELP_SCAN_CODES:
            tree.insert("", tk.END, values=item)

        # Scrollbar Vertikal
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        ttk.Button(help_win, text="Tutup", command=help_win.destroy).pack(pady=10)

    def check_status(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REG_PATH, 0, winreg.KEY_READ)
            value, _ = winreg.QueryValueEx(key, REG_KEY_NAME)
            winreg.CloseKey(key)
            if value:
                self.lbl_status.config(text="Status Registry: Custom Scancode Map Aktif", foreground="green")
        except FileNotFoundError:
            self.lbl_status.config(text="Status Registry: Default (Belum Ada Blokir)", foreground="gray")
        except Exception as e:
            self.lbl_status.config(text=f"Status: Error - {str(e)}", foreground="red")

    def apply_multi_block(self):
        selected_codes = []

        # 1. Ambil dari Checkbox Preset
        for key_name, var in self.check_vars.items():
            if var.get() == 1:
                selected_codes.append(PRESET_SCAN_CODES[key_name])

        # 2. Ambil dari Entry Manual
        manual_text = self.entry_manual.get().strip()
        if manual_text:
            items = manual_text.split(",")
            for item in items:
                item = item.strip()
                if item:
                    try:
                        formatted_code = format_hex_scancode(item)
                        if formatted_code not in selected_codes:
                            selected_codes.append(formatted_code)
                    except ValueError as ve:
                        messagebox.showerror("Format Error", str(ve))
                        return

        if not selected_codes:
            messagebox.showwarning("Peringatan", "Pilih preset atau masukkan scan code manual terlebih dahulu!")
            return

        header = bytes([0x00] * 8)
        total_entries = len(selected_codes) + 1
        count = total_entries.to_bytes(4, byteorder='little')

        mappings = bytearray()
        for code_hex in selected_codes:
            mappings.extend(bytes([0x00, 0x00]))
            mappings.extend(bytes.fromhex(code_hex))

        footer = bytes([0x00] * 4)
        binary_data = header + count + bytes(mappings) + footer

        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REG_PATH, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, REG_KEY_NAME, 0, winreg.REG_BINARY, binary_data)
            winreg.CloseKey(key)
            
            messagebox.showinfo(
                "Berhasil", 
                f"Registry berhasil memblokir {len(selected_codes)} tombol.\n\nSilakan RESTART laptop Anda agar perubahan aktif!"
            )
            self.check_status()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menulis ke Registry:\n{str(e)}")

    def reset_registry(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REG_PATH, 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, REG_KEY_NAME)
            winreg.CloseKey(key)
            
            for var in self.check_vars.values():
                var.set(0)
            self.entry_manual.delete(0, tk.END)

            messagebox.showinfo("Berhasil", "Registry Scancode Map dihapus.\n\nSilakan RESTART laptop Anda!")
            self.check_status()
        except FileNotFoundError:
            messagebox.showinfo("Informasi", "Registry sudah dalam kondisi default.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menghapus Registry:\n{str(e)}")

if __name__ == "__main__":
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        root = tk.Tk()
        app = MultiKeyRegistryRemapper(root)
        root.mainloop()