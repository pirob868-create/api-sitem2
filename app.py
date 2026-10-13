from flask import Flask, render_template, jsonify
import requests
import sqlite3

app = Flask(__name__)
@app.route("/veritabani")
def veritabani_listele():
    db = sqlite3.connect("kullanicilar.db")
    db.row_factory = sqlite3.Row

    kisiler = db.execute(
        "SELECT * FROM kullanicilar"
    ).fetchall()

    db.close()

    return jsonify([dict(kisi) for kisi in kisiler])
def veritabani_olustur():
    db = sqlite3.connect("kullanicilar.db")
    db.execute("""
        CREATE TABLE IF NOT EXISTS kullanicilar (
            id INTEGER PRIMARY KEY,
            isim TEXT,
            email TEXT,
            telefon TEXT
        )
    """)
    db.commit()
    db.close()

@app.route("/")
def ana_sayfa():
    return render_template("index.html")

@app.route("/api")
def api_verisi():
    try:
        cevap = requests.get(
            "https://jsonplaceholder.typicode.com/users",
            timeout=10
        )
        cevap.raise_for_status()
        kisiler = cevap.json()
        return jsonify(kisiler)
    except requests.RequestException:
        return jsonify({"hata": "API baglantisi basarisiz"}), 502


@app.route("/api")
def api_verisi():
    try:
        api_url = "https://jsonplaceholder.typicode.com/users"

        cevap = requests.get(api_url, timeout=15)
        cevap.raise_for_status()

        veriler = cevap.json()

        return jsonify(veriler)

    except requests.RequestException:
        return jsonify({"hata": "API baglanti hatasi"}), 502


("/kaydet")
def kaydet():
    try:
        cevap = requests.get(
            "https://jsonplaceholder.typicode.com/users",
            timeout=10
        )
        cevap.raise_for_status()
        kisiler = cevap.json()

        db = sqlite3.connect("kullanicilar.db")

        for kisi in kisiler:
            db.execute("""
                INSERT OR REPLACE INTO kullanicilar
                VALUES (?, ?, ?, ?)
            """, (
                kisi["id"],
                kisi["name"],
                kisi["email"],
                kisi["phone"]
            ))

        db.commit()
        db.close()

        return jsonify({
            "mesaj": "Kullanicilar kaydedildi!",
            "toplam": len(kisiler)
        })
    except requests.RequestException:
        return jsonify({"hata": "API baglantisi basarisiz"}), 502

veritabani_olustur()

if __name__ == "__main__":
    app.run(debug=False)