# cs122-budget-app
# MyPocketbook

**Group Members**  
- Lisa Yu  
- Jessica Fung  

---

## 📌 Project Description

*MyPocketbook* is a personal budgeting desktop application built in Python. It allows users to track income and expenses, set monthly budgeting goals, and visualize spending behavior using pie charts. Through a user-friendly interface, individuals can monitor their finances and make informed decisions about saving and spending.

---

## 📦 Dependencies

The following Python libraries are required:

- `customtkinter==5.2.0`
- `sqlalchemy==2.0.25`
- `pandas==2.2.1`
- `matplotlib==3.8.3`

> Install all dependencies using:
```bash
pip3 install -r requirements.txt
```

---

## 🛠 Setup & Execution Instructions

1. **Clone or extract** the project directory.

2. **Install dependencies** (if not already installed):
```bash
pip3 install -r requirements.txt
```

3. **Run the application**:
```bash
python3 main.py
```

4. The application will launch in a window. Use the sign-up page to create a new account, or log in if you already have one.

---

## 📁 File Structure Overview

| File/Folder         | Purpose                                                                 |
|---------------------|-------------------------------------------------------------------------|
| `main.py`           | Entry point of the application. Loads the main menu window.             |
| `login_page.py`     | Handles user registration and login authentication.                     |
| `budgeting.py`      | GUI and logic for budget creation, progress tracking, and reports.      |
| `transactions.py`   | GUI and logic for adding/viewing income/expense entries.                |
| `models.py`         | SQLAlchemy models for users, transactions, and budget goals.            |
| `budget.db`         | SQLite database file used for storing data.                             |
| `README.md`         | Project overview, setup instructions, and file documentation.           |
| `requirements.txt`  | Lists required Python packages and versions.                            |

---

## ⚠️ Known Bugs or Limitations

- Passwords are stored as plaintext (no hashing or encryption).
- Input fields allow some invalid entries (e.g., category text field has no restrictions).
- Visual layout may not fully scale across different screen sizes or OSes.
- Reporting features do not support export (e.g., CSV, PDF).
- No handling for recurring income/expenses.

---

## If you get this error: 
ModuleNotFoundError: No module named 'distutils'

`python3 -m pip install setuptools`