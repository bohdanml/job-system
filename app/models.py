from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(String, default="job_seeker")  # job_seeker | employer | admin
    hashed_password = Column(String, nullable=False)

    resumes = relationship("Resume", back_populates="owner", cascade="all, delete-orphan")
    vacancies = relationship("Vacancy", back_populates="employer", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="applicant", cascade="all, delete-orphan")


class Vacancy(Base):
    __tablename__ = "vacancies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text)
    employer_id = Column(Integer, ForeignKey("users.id"))

    employer = relationship("User", back_populates="vacancies")
    applications = relationship("Application", back_populates="vacancy", cascade="all, delete-orphan")


class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="resumes")


class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    vacancy_id = Column(Integer, ForeignKey("vacancies.id"))
    cover_letter = Column(Text, nullable=True)

    applicant = relationship("User", back_populates="applications")
    vacancy = relationship("Vacancy", back_populates="applications")
