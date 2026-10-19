# tuprak_CC_1

Project Python Flask untuk Tugas Integrasi Jenkins, Docker, dan MySQL (`tugas_praktikum1`).

## Struktur File Proyek

```text
tuprak_CC_1/
├── app.py                # Aplikasi Flask (endpoint / dan /db-check)
├── requirements.txt      # Dependensi (Flask, PyMySQL, cryptography)
├── Dockerfile            # Spesifikasi container image python:3.10-slim
├── .dockerignore         # Pengecualian file untuk build Docker
├── Jenkinsfile           # Declarative pipeline CI/CD untuk Windows Agent
├── .env                  # Konfigurasi environment lokal (opsional)
├── .env.example          # Contoh template environment variables
├── .gitignore            # File pengecualian git
└── README.md             # Dokumentasi proyek
```

## Konfigurasi Environment Variables

Aplikasi membaca konfigurasi basis data melalui environment variables dengan fallback default:

| Variabel | Default | Keterangan |
| :--- | :--- | :--- |
| `DB_HOST` | `localhost` | Host MySQL Server |
| `DB_PORT` | `3306` | Port MySQL Server |
| `DB_USER` | `root` | Username MySQL |
| `DB_PASSWORD` | *(kosong)* | Password MySQL |
| `DB_NAME` | `tugas_praktikum1` | Nama Database |
| `PORT` | `5000` | Port aplikasi Flask |

## Endpoint API

1. **Endpoint Root (`/`)**
   - **Method**: `GET`
   - **Format**: JSON
   - **Contoh Respons**:
     ```json
     {
       "status": "success",
       "message": "Aplikasi Flask berjalan dengan baik!",
       "project": "tuprak_CC_1"
     }
     ```

2. **Endpoint Cek Database (`/db-check`)**
   - **Method**: `GET`
   - **Format**: JSON
   - **Contoh Respons (Berhasil - 200)**:
     ```json
     {
       "status": "connected",
       "message": "Koneksi ke database berhasil!",
       "database": "tugas_praktikum1",
       "version": "8.0.30",
       "host": "localhost",
       "port": 3306
     }
     ```
   - **Contoh Respons (Gagal - 500)**:
     ```json
     {
       "status": "error",
       "message": "Gagal terhubung ke database",
       "database": "tugas_praktikum1",
       "host": "localhost",
       "port": 3306,
       "error": "..."
     }
     ```

## Menjalankan dengan Docker

### 1. Build Image Docker
```powershell
docker build -t abdullohalwahab/tuprak-cc-1:latest .
```

### 2. Jalankan Container
Jika MySQL berjalan di host machine (Windows):
```powershell
docker run -d -p 5000:5000 -e DB_HOST=host.docker.internal -e DB_USER=root -e DB_NAME=tugas_praktikum1 --name tuprak-app abdullohalwahab/tuprak-cc-1:latest
```

## Integrasi CI/CD Jenkins

`Jenkinsfile` menggunakan **Declarative Pipeline** yang kompatibel dengan **Windows Agent**:
- **Environment**:
  - `IMAGE_NAME = 'abdullohalwahab/tuprak-cc-1'`
  - `REGISTRY_CREDENTIALS = 'dockerhub-credentials'`
- **Stages**:
  1. **Checkout**: Mengambil kode sumber dari repository (`checkout scm`).
  2. **Build**: Verifikasi file proyek dan dependensi (`bat 'echo ...'`).
  3. **Build Docker Image**: Menjalankan `bat "docker build -t %IMAGE_NAME%:%BUILD_NUMBER% ."`.
  4. **Push Docker Image**: Mengautentikasi ke Docker Hub menggunakan `withCredentials`, melakukan tagging `latest`, dan mem-push kedua tag (`%BUILD_NUMBER%` dan `latest`).
