# Currency Converter in Python

An experiential learning project developed under the **Python Programming Lab (N-PCCCM304P)** curriculum at **S. B. Jain Institute of Technology, Management and Research, Nagpur** (Session 2026-27 ODD).

---

## 📌 Project Overview
The **Currency Converter Application** converts values between global currencies accurately. It has evolved from a basic static rate script (Phase 1) into an interactive, menu-driven CLI application featuring live exchange rate API fetching, offline resilience, persistent file logging, and exception handling (Phase 2).

---

## 🚀 Features (Phase 1 & Phase 2)

* **Real-Time Exchange Rates:** Fetches live rates using standard Python networking (`urllib.request` and `json`).
* **Offline Resilience:** Automatically switches to an internal fallback dictionary if internet connectivity is unavailable.
* **Transaction Logging (File Handling):** Saves all conversions with timestamps to `conversion_history.txt`.
* **History Viewer:** Allows users to view previous transactions directly from the application menu.
* **Robust Input Validation:** Catches `ValueError` (invalid amounts, non-numeric input) and `KeyError` (unsupported currency codes).
* **Currency Alias Support:** Supports standard 3-letter ISO codes (e.g., `USD`, `INR`, `EUR`).

---

## 🛠️ Python Concepts Demonstrated

1. **Data Structures:** Dictionaries for fallback rates and alias mappings.
2. **Networking & APIs:** Consuming public REST APIs using `urllib.request` and parsing responses with `json`.
3. **File Handling:** Appending transaction records using mode `'a'` and reading log entries with mode `'r'`.
4. **Exception Handling:** Structured `try...except...finally` blocks for network calls, file operations, and type casting.
5. **Control Flow & Functions:** Modular design with clean function signatures and a persistent interactive loop.

---

## 💻 Installation & Usage

### Prerequisites
* Python 3.8 or higher installed on your machine.
* No external third-party dependencies required (uses built-in standard libraries).

### Running the Application

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/AnupamTrivedi-gh/Currency-Converter-Python.git](https://github.com/AnupamTrivedi-gh/Currency-Converter-Python.git)
   cd Currency-Converter-Python