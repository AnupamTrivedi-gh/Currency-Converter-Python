# Currency Converter — Phase 3 Web Application

A Python Flask web application for currency conversion, built on the Phase 2 project logic.

## Features
- Browser-based responsive interface
- Live exchange rates from open.er-api.com, with offline fallback rates
- Currency selection and swap controls
- Input validation and helpful errors
- Timestamped conversion history in `conversion_history.txt`
- JSON API endpoints for currencies, conversion and history

## Requirements
- Python 3.8+
- Flask

## Run locally (Windows)
1. Open a terminal in this project folder.
2. Create and activate a virtual environment (recommended):
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Install dependency:
   ```powershell
   python -m pip install -r requirements.txt
   ```
4. Start the app:
   ```powershell
   python app.py
   ```
5. Open http://127.0.0.1:5000 in your browser.

## Project structure
```text
Currency-Converter-Python/
├── app.py
├── main.py
├── requirements.txt
├── README.md
├── conversion_history.txt   # created after a successful conversion
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── app.js
```

## API endpoints
- `GET /api/currencies` — list supported currencies and rate source status
- `POST /api/convert` — convert an amount (`amount`, `source`, `target`)
- `GET /api/history` — recent saved conversions

## Notes
- The offline fallback rates are hardcoded example values and can become outdated. The interface reports whether live or fallback rates are being used.
- The development server is intended for local testing. Use a production WSGI server when deploying publicly.
