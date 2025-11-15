# 🚀 How to Run BossBoard Application

This is a full-stack application with a FastAPI backend and frontend. Here's how to run it:

## Quick Start (Simplest Method)

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

**Note for Windows users:** Use `py -m pip` instead of `pip`, and `py` instead of `python`

### Step 1: Setup Backend

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install backend dependencies:**
   ```bash
   # On Windows (PowerShell):
   py -m pip install -r requirements.txt
   
   # On Mac/Linux:
   pip install -r requirements.txt
   ```

3. **Create `.env` file** (if it doesn't exist):
   ```bash
   # On Windows (PowerShell):
   @"
   DATABASE_URL=sqlite:///./bossboard.db
   JWT_SECRET_KEY=my-secret-key-change-in-production
   CIRCLE_API_KEY=test-key
   CIRCLE_BASE_URL=https://api.circle.com/v1
   "@ | Out-File -FilePath .env -Encoding utf8
   
   # On Mac/Linux:
   cat > .env << 'EOF'
   DATABASE_URL=sqlite:///./bossboard.db
   JWT_SECRET_KEY=my-secret-key-change-in-production
   CIRCLE_API_KEY=test-key
   CIRCLE_BASE_URL=https://api.circle.com/v1
   EOF
   ```

4. **Start the backend server:**
   ```bash
   # On Windows:
   py main.py
   
   # On Mac/Linux:
   python main.py
   ```
   
   You should see:
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```
   
   **Keep this terminal window open!**

### Step 2: Setup Frontend

1. **Open a NEW terminal window** (keep backend running)

2. **Navigate to src directory:**
   ```bash
   cd src
   ```

3. **Install frontend dependencies:**
   ```bash
   # On Windows:
   py -m pip install fastapi uvicorn jinja2 python-multipart requests
   
   # On Mac/Linux:
   pip install fastapi uvicorn jinja2 python-multipart requests
   ```

4. **Start the frontend server:**
   ```bash
   # On Windows:
   py frontend.py
   
   # On Mac/Linux:
   python frontend.py
   ```
   
   You should see:
   ```
   🚀 Starting frontend on http://localhost:8001
   ```

### Step 3: Access the Application

Open your web browser and go to:
- **Login page:** http://localhost:8001/login
- **Sign up page:** http://localhost:8001/signup
- **Backend API docs:** http://localhost:8000/docs

## Alternative: Using Shell Scripts (Mac/Linux)

If you're on Mac or Linux, you can use the provided scripts:

**Terminal 1 (Backend):**
```bash
bash start_backend.sh
```

**Terminal 2 (Frontend):**
```bash
bash start_frontend.sh
```

## What's Running?

- **Backend API** (Port 8000): Handles all data operations, authentication, and Circle API integration
- **Frontend** (Port 8001): Web interface for the application
- **Database**: SQLite database file (`bossboard.db` in the `backend/` folder) - created automatically

## First Time Setup

1. Go to http://localhost:8001/signup
2. Create an account (username and password)
3. Log in at http://localhost:8001/login
4. You'll be redirected to the dashboard

## Troubleshooting

### Port Already in Use
If you get "Address already in use" error:
- **Backend (8000):** Change port in `backend/main.py` line 46
- **Frontend (8001):** Change port in `src/frontend.py` (last line)

### Module Not Found
Install missing dependencies:
```bash
# On Windows:
py -m pip install fastapi uvicorn sqlalchemy python-jose passlib python-multipart pydantic python-dotenv requests jinja2

# On Mac/Linux:
pip install fastapi uvicorn sqlalchemy python-jose passlib python-multipart pydantic python-dotenv requests jinja2
```

### "pip is not recognized" (Windows)
On Windows, use `py -m pip` instead of `pip`:
```powershell
py -m pip install -r requirements.txt
```

### Database Errors
The SQLite database is created automatically. If you see database errors:
- Make sure you're in the `backend/` directory when running `main.py`
- Check that the `.env` file exists with `DATABASE_URL=sqlite:///./bossboard.db`

## Optional: React Frontend

There's also a React frontend in the `frontend/` folder. To use it:

```bash
cd frontend
npm install
npm run dev
```

This will run on http://localhost:3000 (or another port if 3000 is taken).

## Need Help?

- Check `backend/README.md` for backend-specific details
- Check `frontend/README.md` for React frontend details
- Check `SETUP_COMPLETE.md` for more setup information

