"""
Simple Python frontend with FastAPI
Starting with Login and Sign Up pages
"""
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

# Create application
app = FastAPI(title="BossBoard Frontend")

# Setup for static files (CSS, JS, images)
static_dir = os.path.join(os.path.dirname(__file__), "static")
templates_dir = os.path.join(os.path.dirname(__file__), "templates")

# Create folders if they don't exist
os.makedirs(static_dir, exist_ok=True)
os.makedirs(templates_dir, exist_ok=True)

# Mount static files
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Setup templates
templates = Jinja2Templates(directory=templates_dir)

# Simple user storage (in real project use database)
# Format: {email: {"password": password, "company_name": company_name}}
users_db = {}

# Organization data storage (in real project use database)
# For simplicity, using in-memory storage per user session
# In production, this should be stored in database with user_id
organization_data = {
    "ceo": None,  # {master_wallet: str, payroll_frequency: str}
    "departments": {},  # {id: {name: str, workers: [], spendings: []}}
    "workers": {},  # {id: {name: str, surname: str, salary: float, wallet: str, department_id: int}}
    "spendings": [],  # [{name: str, amount: float, wallet: str, target_type: str, target_id: int}]
    "revenues": []  # [{month: str, amount: float}]
}
next_dept_id = 1
next_worker_id = 1
next_spending_id = 1


# Root page - redirect to login
@app.get("/")
async def root():
    return RedirectResponse(url="/login")


# Login page
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# Handle login
@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    # Basic email validation
    if "@" not in email or "." not in email.split("@")[1]:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid email format"}
        )
    
    # Check user (in real project check in database)
    email_lower = email.lower().strip()
    if email_lower in users_db and users_db[email_lower]["password"] == password:
        # In real project use sessions or JWT tokens
        return RedirectResponse(url="/constructor", status_code=303)
    else:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid email or password"}
        )


# Sign Up page
@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


# Handle sign up (register)
@app.post("/signup")
async def signup(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    company_name: str = Form(...)
):
    # Basic email validation
    if "@" not in email or "." not in email.split("@")[1]:
        return templates.TemplateResponse(
            "signup.html",
            {"request": request, "error": "Invalid email format"}
        )
    
    # Check if user already exists
    email_lower = email.lower().strip()
    if email_lower in users_db:
        return templates.TemplateResponse(
            "signup.html",
            {"request": request, "error": "Email already registered"}
        )
    
    # Validate password length
    if len(password) < 6:
        return templates.TemplateResponse(
            "signup.html",
            {"request": request, "error": "Password must be at least 6 characters"}
        )
    
    # Validate company name
    if not company_name.strip():
        return templates.TemplateResponse(
            "signup.html",
            {"request": request, "error": "Company name is required"}
        )
    
    # Save user (in real project save to database with password hashing!)
    users_db[email_lower] = {
        "password": password,
        "company_name": company_name.strip()
    }
    
    # Redirect to login after successful registration
    return RedirectResponse(url="/login?registered=true", status_code=303)


# Constructor page
@app.get("/constructor", response_class=HTMLResponse)
async def constructor_page(request: Request):
    try:
        # Calculate department stats
        departments_list = []
        for dept_id, dept in organization_data["departments"].items():
            workers_in_dept = [w for w in organization_data["workers"].values() if w.get("department_id") == dept_id]
            dept_spendings = [s for s in organization_data["spendings"] if s.get("target_type") == f"dept_{dept_id}"]
            total_spendings = sum(w.get("salary", 0) for w in workers_in_dept) + sum(s.get("amount", 0) for s in dept_spendings)
            
            departments_list.append({
                "id": dept_id,
                "name": dept.get("name", ""),
                "worker_count": len(workers_in_dept),
                "total_spendings": total_spendings,
                "workers": workers_in_dept,
                "spendings": dept_spendings
            })
        
        ceo_spendings = [s for s in organization_data["spendings"] if s.get("target_type") == "ceo"]
        
        return templates.TemplateResponse("constructor.html", {
            "request": request,
            "ceo_data": organization_data["ceo"],
            "ceo_spendings": ceo_spendings,
            "departments": departments_list,
            "revenues": organization_data["revenues"]
        })
    except Exception as e:
        # Return error page or redirect
        return templates.TemplateResponse("constructor.html", {
            "request": request,
            "ceo_data": None,
            "ceo_spendings": [],
            "departments": [],
            "revenues": [],
            "error": f"Error loading page: {str(e)}"
        })


# Handle CEO/Master Wallet
@app.post("/constructor/ceo")
async def save_ceo(request: Request, master_wallet: str = Form(...), payroll_frequency: str = Form(...)):
    # Basic wallet validation
    if not master_wallet.startswith("0x") or len(master_wallet) != 42:
        return templates.TemplateResponse("constructor.html", {
            "request": request,
            "error": "Invalid wallet address format"
        })
    
    organization_data["ceo"] = {
        "master_wallet": master_wallet,
        "payroll_frequency": payroll_frequency
    }
    return RedirectResponse(url="/constructor", status_code=303)


# Handle Department creation
@app.post("/constructor/department")
async def create_department(request: Request, name: str = Form(...)):
    global next_dept_id
    if not name.strip():
        return RedirectResponse(url="/constructor?error=Department name required", status_code=303)
    
    organization_data["departments"][next_dept_id] = {
        "name": name.strip(),
        "workers": [],
        "spendings": []
    }
    next_dept_id += 1
    return RedirectResponse(url="/constructor", status_code=303)


# Handle Worker creation
@app.post("/constructor/worker")
async def create_worker(
    request: Request,
    name: str = Form(...),
    surname: str = Form(...),
    salary: str = Form(...),
    wallet: str = Form(...),
    department_id: str = Form(...)
):
    global next_worker_id
    try:
        salary_float = float(salary)
        dept_id = int(department_id)
    except ValueError:
        return RedirectResponse(url="/constructor?error=Invalid input", status_code=303)
    
    if dept_id not in organization_data["departments"]:
        return RedirectResponse(url="/constructor?error=Department not found", status_code=303)
    
    if not wallet.startswith("0x") or len(wallet) != 42:
        return RedirectResponse(url="/constructor?error=Invalid wallet address", status_code=303)
    
    organization_data["workers"][next_worker_id] = {
        "name": name.strip(),
        "surname": surname.strip(),
        "salary": salary_float,
        "wallet": wallet.strip(),
        "department_id": dept_id
    }
    next_worker_id += 1
    return RedirectResponse(url="/constructor", status_code=303)


# Handle Additional Spending
@app.post("/constructor/spending")
async def create_spending(
    request: Request,
    name: str = Form(...),
    amount: str = Form(...),
    wallet: str = Form(...),
    target_type: str = Form(...)
):
    global next_spending_id
    try:
        amount_float = float(amount)
    except ValueError:
        return RedirectResponse(url="/constructor?error=Invalid amount", status_code=303)
    
    if not wallet.startswith("0x") or len(wallet) != 42:
        return RedirectResponse(url="/constructor?error=Invalid wallet address", status_code=303)
    
    spending = {
        "id": next_spending_id,
        "name": name.strip(),
        "amount": amount_float,
        "wallet": wallet.strip(),
        "target_type": target_type
    }
    organization_data["spendings"].append(spending)
    next_spending_id += 1
    return RedirectResponse(url="/constructor", status_code=303)


# Handle Revenue
@app.post("/constructor/revenue")
async def add_revenue(request: Request, month: str = Form(...), amount: str = Form(...)):
    try:
        amount_float = float(amount)
    except ValueError:
        return RedirectResponse(url="/constructor?error=Invalid amount", status_code=303)
    
    organization_data["revenues"].append({
        "month": month,
        "amount": amount_float
    })
    return RedirectResponse(url="/constructor", status_code=303)


# Dashboard page with statistics
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    # Calculate statistics
    total_workers = len(organization_data["workers"])
    total_departments = len(organization_data["departments"])
    
    # Calculate total payroll
    total_payroll = sum(w["salary"] for w in organization_data["workers"].values())
    
    # Calculate total additional spendings
    total_spendings = sum(s["amount"] for s in organization_data["spendings"])
    
    # Calculate total expenses
    total_expenses = total_payroll + total_spendings
    
    # Calculate total revenue
    total_revenue = sum(r["amount"] for r in organization_data["revenues"])
    
    # Calculate profit
    profit = total_revenue - total_expenses
    
    # Department statistics
    dept_stats = []
    for dept_id, dept in organization_data["departments"].items():
        workers_in_dept = [w for w in organization_data["workers"].values() if w["department_id"] == dept_id]
        dept_payroll = sum(w["salary"] for w in workers_in_dept)
        dept_spendings = sum(s["amount"] for s in organization_data["spendings"] if s["target_type"] == f"dept_{dept_id}")
        dept_stats.append({
            "name": dept["name"],
            "worker_count": len(workers_in_dept),
            "payroll": dept_payroll,
            "spendings": dept_spendings,
            "total": dept_payroll + dept_spendings,
            "workers": workers_in_dept
        })
    
    # Prepare revenues and expenses lists
    revenues_list = organization_data["revenues"]
    expenses_list = []
    
    # Add payroll expenses
    for worker_id, worker in organization_data["workers"].items():
        dept_name = "Unknown"
        for dept_id, dept in organization_data["departments"].items():
            if dept_id == worker.get("department_id"):
                dept_name = dept.get("name", "Unknown")
                break
        expenses_list.append({
            "type": "Payroll",
            "name": f"{worker.get('name', '')} {worker.get('surname', '')} ({dept_name})",
            "amount": worker.get("salary", 0)
        })
    
    # Add additional spendings
    for spending in organization_data["spendings"]:
        expenses_list.append({
            "type": "Spending",
            "name": spending.get("name", ""),
            "amount": spending.get("amount", 0)
        })
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "total_workers": total_workers,
        "total_departments": total_departments,
        "total_payroll": total_payroll,
        "total_spendings": total_spendings,
        "total_expenses": total_expenses,
        "total_revenue": total_revenue,
        "profit": profit,
        "dept_stats": dept_stats,
        "ceo_data": organization_data["ceo"],
        "revenues_list": revenues_list,
        "expenses_list": expenses_list
    })


if __name__ == "__main__":
    import uvicorn
    import socket
    
    # Try to find an available port
    def find_free_port(start_port=8001):
        for port in range(start_port, start_port + 10):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('', port))
                    return port
            except OSError:
                continue
        return start_port
    
    port = find_free_port(8001)
    print(f"🚀 Starting frontend on http://localhost:{port}")
    print(f"📝 Open in browser: http://localhost:{port}/login")
    uvicorn.run(app, host="0.0.0.0", port=port)

