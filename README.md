# TarifParkirBanyumas - Streamlit Dashboard

Dashboard analisis potensi tarif parkir menggunakan Random Forest & analisis spasial.

## Run locally
1. Aktifkan virtualenv Anda (PowerShell):
```powershell
& D:/TarifParkirBanyumas/.venv/Scripts/Activate.ps1
```
2. Install dependencies:
```powershell
python -m pip install -r requirements.txt
```
3. Jalankan Streamlit:
```powershell
streamlit run app.py
```
4. Buka browser pada `http://localhost:8501`.

## Deploy to Streamlit Community Cloud (recommended)
1. Push repo ke GitHub (pastikan `app.py` dan `requirements.txt` sudah ada):
```powershell
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/<username>/<repo>.git
git push -u origin main
```
2. Buka https://streamlit.io/cloud dan login.
3. Add new app → pilih repository & branch → pilih `app.py` → Deploy.
4. (Optional) Jika dataset besar, host data di S3/Google Drive dan gunakan environment variable `DATA_URL`.

## Deploy with Docker
1. Build image:
```powershell
docker build -t tarif-parkir:latest .
```
2. Run container:
```powershell
docker run -p 8501:8501 tarif-parkir:latest
```

## Heroku / Render
- Gunakan `Procfile` dan `requirements.txt`.
- Pastikan `Procfile` berisi: `web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.enableCORS=false`.

## Notes
- Jika Anda mengandalkan `DataParkir_Fix.xlsx`, keep it small, or host externally. For sensitive data, do not commit dataset to a public repo.
- Streamlit Cloud picks repo's `requirements.txt` and `app.py`, and deploys automatically per-commit.

---

If you want, I can also:
- Add `.gitignore` entries (e.g., `.venv`, `__pycache__`, `data/`),
- Create a GitHub Action for automated deploy,
- Prepare a `deploy` branch and push files for you.
