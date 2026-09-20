from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Teacher, Student
from app.schemas import LoginRequest, LoginResponse
from app.security import verify_password, create_access_token

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/login", response_model=LoginResponse)
def login(creds: LoginRequest, db: Session = Depends(get_db)):
    # 1. Check Teacher
    teacher = db.query(Teacher).filter(Teacher.email == creds.email).first()
    if teacher and verify_password(creds.password, teacher.hashed_password):
        class_obj = teacher.classes[0] if teacher.classes else None
        class_id = class_obj.id if class_obj else 1
        token = create_access_token({"sub": teacher.email, "role": "teacher", "id": teacher.id})
        return LoginResponse(
            user_id=teacher.id,
            name=teacher.name,
            email=teacher.email,
            role="teacher",
            class_id=class_id,
            token=token
        )

    # 2. Check Student
    student = db.query(Student).filter(Student.email == creds.email).first()
    if student and verify_password(creds.password, student.hashed_password):
        token = create_access_token({"sub": student.email, "role": "student", "id": student.id})
        return LoginResponse(
            user_id=student.id,
            name=student.name,
            email=student.email,
            role="student",
            class_id=student.class_id,
            token=token
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials. For demo: teacher@demo.com or student@demo.com with password 'password'"
    )

@router.get("/demo-users")
def get_demo_users():
    """Returns quick switcher accounts for live evaluator demonstration."""
    return [
        {
            "role": "teacher",
            "name": "Prof. Vikram Sen",
            "email": "teacher@demo.com",
            "password": "password",
            "description": "Instructor view: Classroom analytics, critical gap alerts, and teaching interventions"
        },
        {
            "role": "student",
            "name": "Aarav Sharma",
            "email": "student@demo.com",
            "password": "password",
            "description": "Student view: Needs practice on Recursion (28%), personalized recommendations"
        },
        {
            "role": "student",
            "name": "Priya Patel",
            "email": "advanced@demo.com",
            "password": "password",
            "description": "Advanced learner: High mastery across all concepts (92%), enrichment challenges"
        }
    ]
