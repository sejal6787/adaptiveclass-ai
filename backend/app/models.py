from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text
)
from sqlalchemy.orm import relationship
from app.database import Base

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    department = Column(String(100), default="Computer Science & Engineering")
    hashed_password = Column(String(255), nullable=False)

    classes = relationship("Class", back_populates="teacher", cascade="all, delete-orphan")


class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    subject = Column(String(100), nullable=False)
    semester = Column(String(50), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)

    teacher = relationship("Teacher", back_populates="classes")
    students = relationship("Student", back_populates="class_group", cascade="all, delete-orphan")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    roll_number = Column(String(50), unique=True, index=True, nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    hashed_password = Column(String(255), nullable=False)

    class_group = relationship("Class", back_populates="students")
    performances = relationship("ConceptPerformance", back_populates="student", cascade="all, delete-orphan")
    quiz_attempts = relationship("QuizAttempt", back_populates="student", cascade="all, delete-orphan")


class Concept(Base):
    __tablename__ = "concepts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    subject = Column(String(100), default="Data Structures")
    description = Column(Text, nullable=True)
    order_index = Column(Integer, default=0)

    questions = relationship("Question", back_populates="concept", cascade="all, delete-orphan")
    performances = relationship("ConceptPerformance", back_populates="concept", cascade="all, delete-orphan")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=False)
    difficulty = Column(String(20), nullable=False)  # "beginner", "intermediate", "advanced"
    question_text = Column(Text, nullable=False)
    option_a = Column(String(255), nullable=False)
    option_b = Column(String(255), nullable=False)
    option_c = Column(String(255), nullable=False)
    option_d = Column(String(255), nullable=False)
    correct_answer = Column(String(5), nullable=False)  # "A", "B", "C", "D"
    explanation = Column(Text, nullable=True)

    concept = relationship("Concept", back_populates="questions")


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=True)
    quiz_title = Column(String(150), nullable=False)
    score = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)
    accuracy = Column(Float, nullable=False)  # percentage, e.g. 80.0
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    student = relationship("Student", back_populates="quiz_attempts")
    answers = relationship("QuizAttemptAnswer", back_populates="attempt", cascade="all, delete-orphan")


class QuizAttemptAnswer(Base):
    __tablename__ = "quiz_attempt_answers"

    id = Column(Integer, primary_key=True, index=True)
    quiz_attempt_id = Column(Integer, ForeignKey("quiz_attempts.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    selected_answer = Column(String(5), nullable=False)
    is_correct = Column(Boolean, nullable=False)

    attempt = relationship("QuizAttempt", back_populates="answers")
    question = relationship("Question")


class ConceptPerformance(Base):
    __tablename__ = "concept_performance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=False)
    mastery_score = Column(Float, nullable=False)  # 0.0 - 100.0
    attempt_count = Column(Integer, default=1)
    correct_count = Column(Integer, default=0)
    last_updated = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    student = relationship("Student", back_populates="performances")
    concept = relationship("Concept", back_populates="performances")
