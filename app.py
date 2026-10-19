import os
import pymysql
from flask import Flask, jsonify

# Muat environment variable dari file .env jika tersedia (untuk development lokal)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__)

def get_db_connection():
    """Membuat koneksi ke MySQL menggunakan environment variables dengan fallback default."""
    return pymysql.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", ""),
        database=os.environ.get("DB_NAME", "tugas_praktikum1"),
        port=int(os.environ.get("DB_PORT", 3306)),
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route("/")
def index():
    """Endpoint utama yang mengembalikan status aplikasi dalam format JSON."""
    return jsonify({
        "status": "success",
        "message": "Aplikasi Flask berjalan dengan baik!",
        "project": "tuprak_CC_1"
    })

@app.route("/db-check")
def db_check():
    """Endpoint untuk uji koneksi langsung ke database MySQL tugas_praktikum1."""
    host = os.environ.get("DB_HOST", "localhost")
    database = os.environ.get("DB_NAME", "tugas_praktikum1")
    port = int(os.environ.get("DB_PORT", 3306))

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT DATABASE() AS current_db, VERSION() AS mysql_version;")
            result = cursor.fetchone()
        connection.close()

        return jsonify({
            "status": "connected",
            "message": "Koneksi ke database berhasil!",
            "database": result["current_db"] if result else database,
            "version": result["mysql_version"] if result else "unknown",
            "host": host,
            "port": port
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Gagal terhubung ke database",
            "database": database,
            "host": host,
            "port": port,
            "error": str(e)
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
