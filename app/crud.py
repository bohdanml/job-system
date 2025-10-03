from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from . import models, schemas, utils

# Users
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed = utils.get_password_hash(user.password)
    db_user = models.User(email=user.email, full_name=user.full_name, role=user.role, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_employers(db: Session):
    return db.query(models.User).filter(models.User.role == "employer").all()

# Vacancies
def create_vacancy(db: Session, vacancy: schemas.VacancyCreate):
    db_v = models.Vacancy(title=vacancy.title, description=vacancy.description, employer_id=vacancy.employer_id)
    db.add(db_v)
    db.commit()
    db.refresh(db_v)
    return db_v

def get_vacancies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vacancy).options(joinedload(models.Vacancy.employer)).offset(skip).limit(limit).all()

# Resumes
def create_resume(db: Session, resume: schemas.ResumeCreate):
    db_r = models.Resume(title=resume.title, content=resume.content, user_id=resume.user_id)
    db.add(db_r)
    db.commit()
    db.refresh(db_r)
    return db_r

def get_resumes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Resume).offset(skip).limit(limit).all()

# Applications
def create_application(db: Session, app_in: schemas.ApplicationCreate):
    db_app = models.Application(user_id=app_in.user_id, vacancy_id=app_in.vacancy_id, cover_letter=app_in.cover_letter)
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app

def get_applications(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Application).offset(skip).limit(limit).all()
