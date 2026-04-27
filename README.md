# 🍽️ Food Recipe Manager API

![CI](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/ci.yml/badge.svg)

REST API untuk manajemen resep makanan. Dibangun dengan Python + Flask sebagai Final Project Mata Kuliah Software Testing.

---

## Fitur Utama

- **Manajemen Resep** — CRUD resep makanan lengkap dengan bahan dan instruksi
- **Kategori Makanan** — Kelompokkan resep berdasarkan kategori
- **Rating & Ulasan** — Beri rating 1–5 pada setiap resep

---

## Cara Menjalankan Aplikasi

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Jalankan server
```bash
python -m src.server
```

Server berjalan di `http://localhost:5000`

---

## Endpoint API

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | /api/categories | Daftar semua kategori |
| POST | /api/categories | Tambah kategori |
| DELETE | /api/categories/:id | Hapus kategori |
| GET | /api/recipes | Daftar semua resep |
| GET | /api/recipes/search?q= | Cari resep |
| GET | /api/recipes/:id | Detail resep |
| POST | /api/recipes | Tambah resep |
| PUT | /api/recipes/:id | Update resep |
| DELETE | /api/recipes/:id | Hapus resep |
| POST | /api/recipes/:id/ratings | Tambah rating |
| GET | /api/recipes/:id/ratings | Lihat rating |

---

## Cara Menjalankan Test

### Jalankan semua test
```bash
pytest tests/ -v
```

### Jalankan dengan laporan coverage
```bash
pytest tests/ --cov=src --cov-report=term-missing -v
```

---

## Strategi Pengujian

### Unit Testing (15+ test cases)
Menguji komponen secara terisolasi:
- `test_validators.py` — Validasi input untuk resep, kategori, dan rating
- `test_services.py` — Business logic: CRUD, search, average rating

### Integration Testing (5+ test cases)
Menguji alur end-to-end melalui HTTP:
- `test_integration.py` — Endpoint API, interaksi database, cascade delete

### Coverage Target
Minimal **60%** code coverage. Diukur menggunakan `pytest-cov`.

---

## Struktur Repository

```
├── src/
│   ├── app.py          # Flask app factory
│   ├── models.py       # Database models (SQLAlchemy)
│   ├── routes.py       # API endpoints
│   ├── services.py     # Business logic
│   └── validators.py   # Input validation
├── tests/
│   ├── conftest.py         # Pytest fixtures
│   ├── test_validators.py  # Unit tests - validasi
│   ├── test_services.py    # Unit tests - service layer
│   └── test_integration.py # Integration tests - API
├── .github/workflows/ci.yml  # GitHub Actions CI
├── requirements.txt
└── README.md
```

---

## CI/CD Pipeline

GitHub Actions otomatis berjalan saat **push** dan **pull request**:

1. Checkout kode
2. Setup Python 3.11
3. Install dependencies
4. Jalankan semua test + generate coverage report
5. Upload coverage artifact

---

## Teknologi

- **Python 3.11**
- **Flask** — Web framework
- **Flask-SQLAlchemy** — ORM + SQLite
- **pytest** — Testing framework
- **pytest-cov** — Coverage reporting
- **GitHub Actions** — CI/CD
