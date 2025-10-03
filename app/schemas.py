from pydantic import BaseModel, EmailStr
from typing import Optional

# User
class UserCreate(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    password: str
    role: Optional[str] = "job_seeker"

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str]
    role: str

    class Config:
        orm_mode = True

# Vacancy
class VacancyCreate(BaseModel):
    title: str
    description: str
    employer_id: int

class VacancyOut(BaseModel):
    id: int
    title: str
    description: str
    employer_id: int

    class Config:
        orm_mode = True

# Resume
class ResumeCreate(BaseModel):
    title: str
    content: str
    user_id: int

class ResumeOut(BaseModel):
    id: int
    title: str
    content: str
    user_id: int

    class Config:
        orm_mode = True

# Application
class ApplicationCreate(BaseModel):
    user_id: int
    vacancy_id: int
    cover_letter: Optional[str] = None

class ApplicationOut(BaseModel):
    id: int
    user_id: int
    vacancy_id: int
    cover_letter: Optional[str]

    class Config:
        orm_mode = True
