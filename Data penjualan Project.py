import json
import os
import matplotlib.pyplot as plt

# Nama file untuk menyimpan data secara permanen
NAMA_FILE = 'aditya_motor_sales.json'

# CRUD & File Handling

def muat_data():
    """Memuat data dari file JSON. Jika file tidak ada, kembalikan dictionary kosong."""
    if os.path.exists(NAMA_FILE):
        with open(NAMA_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

def simpan_data(data):
    """Menyimpan data (dictionary) ke dalam file JSON."""
    with open(NAMA_FILE, 'w') as file:
        json.dump(data, file, indent=4)
    print("\n[INFO] Data berhasil disimpan ke file.")

def lihat_data(data):
    """(Read) Menampilkan semua data penjualan yang tersimpan."""
    print("\n===== Data Penjualan PT. Aditya Motor =====")
    if not data:
        print("Belum ada data penjualan.")
        return
    
    # Mengurutkan tahun dari yang terkecil ke terbesar
    for tahun in sorted(data.keys()):
        print(f"\n--- Tahun: {tahun} ---")
        if not data[tahun]:
            print("  (Tidak ada data untuk tahun ini)")
        else:
            for model, unit in data[tahun].items():
                print(f"  - Model: {model:<15} | Unit Terjual: {unit}")
    print("=" * 41)


def tambah_data(data):
    """(Create) Menambahkan data penjualan baru."""
    print("\n--- Tambah Data Penjualan Baru ---")
    tahun = input("Masukkan Tahun Penjualan: ")
    model = input("Masukkan Model Mobil: ").title()
    
    while True:
        try:
            unit = int(input("Masukkan Jumlah Unit Terjual: "))
            break
        except ValueError:
            print("[ERROR] Masukkan harus berupa angka.")

    if tahun not in data:
        data[tahun] = {}
    
    data[tahun][model] = unit
    simpan_data(data)
    print(f"Berhasil menambahkan data: Tahun {tahun}, Model {model}, Unit {unit}.")


def update_data(data):
    """(Update) Mengubah data unit penjualan yang sudah ada."""
    print("\n--- Update Data Penjualan ---")
    tahun = input("Masukkan Tahun dari data yang ingin di-update: ")
    if tahun not in data:
        print(f"[ERROR] Data untuk tahun {tahun} tidak ditemukan.")
        return

    model = input("Masukkan Model Mobil yang ingin di-update: ").title()
    if model not in data[tahun]:
        print(f"[ERROR] Model '{model}' tidak ditemukan di tahun {tahun}.")
        return

    while True:
        try:
            unit_baru = int(input(f"Masukkan Jumlah Unit BARU untuk model {model}: "))
            break
        except ValueError:
            print("[ERROR] Masukkan harus berupa angka.")
    
    data[tahun][model] = unit_baru
    simpan_data(data)
    print(f"Berhasil mengupdate data: Tahun {tahun}, Model {model}, Unit {unit_baru}.")


def hapus_data(data):
    """(Delete) Menghapus data penjualan model mobil tertentu."""
    print("\n--- Hapus Data Penjualan ---")
    tahun = input("Masukkan Tahun dari data yang ingin dihapus: ")
    if tahun not in data:
        print(f"[ERROR] Data untuk tahun {tahun} tidak ditemukan.")
        return

    model = input("Masukkan Model Mobil yang ingin dihapus: ").title()
    if model not in data[tahun]:
        print(f"[ERROR] Model '{model}' tidak ditemukan di tahun {tahun}.")
        return
    
    # Konfirmasi sebelum menghapus
    konfirmasi = input(f"Anda yakin ingin menghapus data {model} tahun {tahun}? (y/n): ").lower()
    if konfirmasi == 'y':
        del data[tahun][model]
        simpan_data(data)
        print("Data berhasil dihapus.")
    else:
        print("Penghapusan dibatalkan.")

def hapus_tahun(data):
    """Menghapus seluruh data penjualan untuk satu tahun tertentu."""
    print("\n--- Hapus Seluruh Data Penjualan Tahun Tertentu ---")
    if not data:
        print("[INFO] Belum ada data penjualan.")
        return

    print("Tahun yang tersedia:", ', '.join(sorted(data.keys())))
    tahun = input("Masukkan tahun yang ingin dihapus: ")
    if tahun not in data:
        print(f"[ERROR] Data untuk tahun {tahun} tidak ditemukan.")
        return

    konfirmasi = input(f"Yakin ingin menghapus SEMUA data tahun {tahun}? (y/n): ").lower()
    if konfirmasi == 'y':
        del data[tahun]
        simpan_data(data)
        print(f"[INFO] Seluruh data tahun {tahun} berhasil dihapus.")
    else:
        print("Penghapusan dibatalkan.")

# FUNGSI-FUNGSI VISUALISASI DATA
def menu_visualisasi(data):
    if not data:
        print("\n[INFO] Belum ada data untuk divisualisasikan.")
        return

    while True:
        print("\n--- Menu Visualisasi Data ---")
        print("1. Grafik Pertumbuhan (Line Chart)")
        print("2. Grafik Batang (Bar Chart)")
        print("3. Diagram Lingkaran (Pie Chart)")
        print("4. Kembali ke Menu Utama")
        pilihan = input("Pilih jenis visualisasi (1-4): ")

        if pilihan == '1':
            plt.figure(figsize=(10, 6))
            semua_model = sorted(list(set(model for tahun in data for model in data[tahun])))
            for model in semua_model:
                penjualan = [data.get(tahun, {}).get(model, 0) for tahun in sorted(data.keys())]
                plt.plot(sorted(data.keys()), penjualan, marker='o', linestyle='-', label=model)
            plt.title('Grafik Pertumbuhan Penjualan per Model')
            plt.xlabel('Tahun')
            plt.ylabel('Unit Terjual')
            plt.legend()
            plt.grid(True)
            plt.show()

        elif pilihan == '2':
            # Logika untuk grafik batang (total semua tahun)
            plt.figure(figsize=(10, 6))
            total_per_model = {}
            for tahun in data:
                for model, unit in data[tahun].items():
                    total_per_model[model] = total_per_model.get(model, 0) + unit
            if total_per_model:
                plt.bar(total_per_model.keys(), total_per_model.values(), color='skyblue')
                plt.title('Total Penjualan per Model (Semua Tahun)')
                plt.ylabel('Total Unit Terjual')
                plt.show()

        elif pilihan == '3':
            # Logika untuk pie chart (total semua tahun)
            plt.figure(figsize=(8, 8))
            total_per_model = {}
            for tahun in data:
                for model, unit in data[tahun].items():
                    total_per_model[model] = total_per_model.get(model, 0) + unit
            if total_per_model:
                plt.pie(total_per_model.values(), labels=total_per_model.keys(), autopct='%1.1f%%', startangle=90)
                plt.title('Proporsi Total Penjualan per Model')
                plt.axis('equal')
                plt.show()

        elif pilihan == '4':
            break
        else:
            print("[ERROR] Pilihan tidak valid.")

# FUNGSI UTAMA (MAIN LOOP PROGRAM)
def main():
    data_penjualan = muat_data()
    
    while True:
        print("\n===== SISTEM MANAJEMEN PENJUALAN - PT. ADITYA MOTOR =====")
        print("1. Lihat Semua Data Penjualan")
        print("2. Tambah Data Penjualan Baru")
        print("3. Update Data Penjualan")
        print("4. Hapus Data Penjualan")
        print("5. Hapus Seluruh Data Tahun Tertentu")  # Tambahan menu
        print("6. Tampilkan Menu Visualisasi Data")
        print("7. Keluar")
        
        pilihan = input("Masukkan pilihan Anda (1-7): ")

        if pilihan == '1':
            lihat_data(data_penjualan)
        elif pilihan == '2':
            tambah_data(data_penjualan)
        elif pilihan == '3':
            update_data(data_penjualan)
        elif pilihan == '4':
            hapus_data(data_penjualan)
        elif pilihan == '5':
            hapus_tahun(data_penjualan)  # Panggil fungsi baru
        elif pilihan == '6':
            menu_visualisasi(data_penjualan)
        elif pilihan == '7':
            print("\nTerima kasih. Program ditutup.")
            break
        else:
            print("\n[ERROR] Pilihan tidak valid. Silakan masukkan angka dari 1 hingga 7.")


# Menjalankan fungsi utama saat script dieksekusi
if __name__ == "__main__":
    main()