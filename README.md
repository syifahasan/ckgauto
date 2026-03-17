# PKGUMUM Refactor Starter

Refactor awal untuk memisahkan proses menjadi beberapa layer:

- `runners/` → entry point per mode
- `workflows/` → orkestrasi per proses bisnis
- `services/` → logika aksi per domain
- `pages/` → interaksi UI/Playwright
- `readers/` → baca + mapping Excel
- `models/` → DTO/result object
- `selectors/` → selector terpusat
- `utils/` → helper umum

## Mode jalan

Atur env lalu jalankan:

```bash
set CKG_MODE=registration
python app.py
```

atau:

```bash
set CKG_MODE=service
python app.py
```

## Catatan

Refactor ini sudah memindahkan fondasi utama `daftarumum`, `konfirmasiumum`, dan sebagian `pelayananumum` ke struktur baru.

Bagian yang masih perlu dipindahkan bertahap dari script lama:

1. seluruh rule skrining mandiri di `screening_service.py`
2. seluruh error handling khusus modal per kasus
3. mapping kolom Excel jika format final berubah
4. unit test untuk validator, mapper, dan service
