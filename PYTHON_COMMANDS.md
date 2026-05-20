# Python Environment & Command Guide

A comprehensive quick-reference guide for setting up and managing your Python development environment, specifically configured for this **FastAPI** application.

---

## 1. Virtual Environment Management

Using a virtual environment (`venv`) ensures that project dependencies are isolated from your system-wide Python installation.

### 📁 Creating the Virtual Environment
To create a new virtual environment in a folder named `venv`:

```bash
# On macOS and Linux
python3 -m venv venv

# On Windows
python -m venv venv
```

---

### 🚀 Activating the Virtual Environment
Before installing packages or running the application, you must activate the virtual environment.

```bash
# macOS / Linux (zsh, bash)
source venv/bin/activate

# Windows (Command Prompt - cmd)
venv\Scripts\activate.bat

# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

> [!TIP]
> You'll know the activation succeeded when you see `(venv)` prepended to your terminal prompt!

---

### 🛑 Deactivating the Virtual Environment
To exit the virtual environment and return to your global system Python:

```bash
deactivate
```

---

## 2. Dependency Management (`pip`)

Use these commands to install, update, and manage your project dependencies.

### 📥 Installing Dependencies
Install all package requirements listed in `requirements.txt`:

```bash
# Always upgrade pip first to avoid installation issues
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt
```

### 💾 Saving Dependencies
If you install a new package (e.g., `pip install requests`) and want to save it to your project requirements:

```bash
pip freeze > requirements.txt
```

### 🔍 Listing Installed Packages
To view all installed packages in the current environment:

```bash
pip list
```

---

## 3. Running the FastAPI Application

Once the virtual environment is active and dependencies are installed, you can start the development server.

### 💻 Starting the Local Dev Server
We use `uvicorn` (an ASGI server) to run the FastAPI application with auto-reload enabled:

```bash
uvicorn main:app --reload
```

* **`main:app`**: Points to the `app` instance inside the `main.py` file.
* **`--reload`**: Automatically restarts the server whenever code changes are saved (perfect for development).

### 🌐 Accessing the API & Documentation
Once the server is running, open your browser and navigate to:

* 🏠 **Base URL**: [http://localhost:8000/](http://localhost:8000/)
* 📖 **Interactive Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs) (Interactive API testing)
* 📘 **Alternative ReDoc UI**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 4. Quick Cheat Sheet

| Action | macOS / Linux | Windows |
| :--- | :--- | :--- |
| **Create Venv** | `python3 -m venv venv` | `python -m venv venv` |
| **Activate Venv** | `source venv/bin/activate` | `venv\Scripts\activate` |
| **Upgrade Pip** | `pip install --upgrade pip` | `python -m pip install --upgrade pip` |
| **Install Requirements** | `pip install -r requirements.txt` | `pip install -r requirements.txt` |
| **Run Dev Server** | `uvicorn main:app --reload` | `uvicorn main:app --reload` |
| **Deactivate** | `deactivate` | `deactivate` |
