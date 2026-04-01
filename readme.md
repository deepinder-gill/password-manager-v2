# 🔐 Secure Password Manager (Python)

A **CLI-based password manager** written in Python that securely stores and retrieves passwords using modern cryptographic practices.

This project focuses on **security-first design**, proper key derivation, and encrypted storage while keeping sensitive data out of version control.

---

## ✨ Features

- 🔑 Master password–protected vault
- 🧂 Secure key derivation using **PBKDF2 + Salt**
- 🔐 Password encryption using **Fernet (AES)**
- ➕ Add new credentials
- 👀 View stored credentials
- 🔍 Search credentials by service
- ❌ Delete stored credentials
- 🛡️ Sensitive files excluded via `.gitignore`

---

## 🛠️ Technologies Used

- Python 3
- `cryptography` library
- PBKDF2 (SHA-256)
- Fernet symmetric encryption
- JSON-based encrypted storage

---

## 📂 Project Structure

```text
.
├── main.py
├── requirements.txt
├── README.md
├── .gitignore