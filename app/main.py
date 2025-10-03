from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pathlib import Path
from . import models, schemas, crud, database

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Job Automation - FastAPI + Jinja2")

# шаблони і статичні файли
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# стартап: створюємо таблиці (безпечніше робити при стартапі)
@app.on_event("startup")
def on_startup():
    database.init_db()

# Dependency
def get_db():
    yield from database.get_db()

@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    # одразу joinedload employer (щоб не потребувати сесії в шаблоні)
    vacancies = crud.get_vacancies(db)
    return templates.TemplateResponse("jobs.html", {"request": request, "vacancies": vacancies})

# --- Форма для створення користувача (GET/POST) ---
@app.get("/users/new", response_class=HTMLResponse)
def new_user_form(request: Request):
    return templates.TemplateResponse("jobs.html", {"request": request, "show_user_form": True})

@app.post("/users/create")
def create_user(
    email: str = Form(...),
    full_name: str = Form(None),
    password: str = Form(...),
    role: str = Form("job_seeker"),
    db: Session = Depends(get_db),
):
    from .schemas import UserCreate
    uc = UserCreate(email=email, full_name=full_name, password=password, role=role)
    existing = crud.get_user_by_email(db, uc.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    crud.create_user(db, uc)
    return RedirectResponse("/", status_code=303)

# --- Форма для створення вакансії (GET/POST) ---
@app.get("/vacancies/new", response_class=HTMLResponse)
def new_vacancy_form(request: Request, db: Session = Depends(get_db)):
    employers = crud.get_employers(db)
    return templates.TemplateResponse("jobs.html", {"request": request, "show_vacancy_form": True, "employers": employers})

@app.post("/vacancies/create")
def create_vacancy(
    title: str = Form(...),
    description: str = Form(...),
    employer_id: int = Form(...),
    db: Session = Depends(get_db),
):
    from .schemas import VacancyCreate
    # перевірка employer
    employers = crud.get_employers(db)
    if not any(e.id == int(employer_id) for e in employers):
        raise HTTPException(status_code=404, detail="Employer not found")
    vc = VacancyCreate(title=title, description=description, employer_id=int(employer_id))
    crud.create_vacancy(db, vc)
    return RedirectResponse("/", status_code=303)

# --- Прості API endpoints (для тестів / Postman / Swagger) ---
@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.post("/api/users/", response_model=schemas.UserOut)
def api_create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user_in)

@app.get("/api/vacancies/", response_model=list[schemas.VacancyOut])
def api_list_vacancies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_vacancies(db, skip, limit)
