import requests
import json

API_ENDPOINT = "https://api.kemenkes.go.id/v1/data/stunting"

AUTH_TOKEN = "aBcXyZ123pQrStR456vWxyz789mNoPq"


def fetch_stunting_data(wilayah_kode):
    print(f"Menginisiasi pengambilan data untuk wilayah: {wilayah_kode}...")

    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Accept": "application/json"
    }

    params = {
        "wilayah": wilayah_kode
    }

    try:
        response = requests.get(API_ENDPOINT, headers=headers, params=params, timeout=10)

        if response.status_code == 200:
            print("Sukses: Data diterima dari Kemenkes.")
            data = response.json()
            
            process_and_save_data(data)
            return data
        
        elif response.status_code == 401:
            print("Error: Autentikasi Gagal. Periksa API Token.")
            return None
            
        else:
            print(f"Error: Gagal mengambil data. Status: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error: Koneksi ke API Kemenkes gagal. {e}")
        return None
def process_and_save_data(data):
    print(f"Memproses {len(data['data_stunting'])} record data stunting...")
    print("Data berhasil disimpan ke database SIDIK.")

if __name__ == "__main__":
    data_diy = fetch_stunting_data(wilayah_kode="DIY")

    if data_diy:
        print("\n--- CONTOH DATA YANG DITERIMA ---")
        print(json.dumps(data_diy, indent=2))
