from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Class, Student, Concept, ConceptPerformance
from app.schemas import ClassAnalyticsResponse, StudentNeedingAttentionItem
from app.analytics_engine import get_class_analytics, get_students_needing_attention, get_student_status_label

router = APIRouter(prefix="/api/classes", tags=["Classes"])

@router.get("")
def list_classes(db: Session = Depends(get_db)):
    classes = db.query(Class).all()
    results = []
    for c in classes:
        student_count = db.query(Student).filter(Student.class_id == c.id).count()
        results.append({
            "id": c.id,
            "name": c.name,
            "subject": c.subject,
            "semester": c.semester,
            "teacher_name": c.teacher.name if c.teacher else "Instructor",
            "student_count": student_count
        })
    return results

@router.get("/{class_id}/analytics", response_model=ClassAnalyticsResponse)
def get_analytics(class_id: int, db: Session = Depends(get_db)):
    try:
        return get_class_analytics(class_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{class_id}/students-needing-attention", response_model=List[StudentNeedingAttentionItem])
def get_attention_students(class_id: int, db: Session = Depends(get_db)):
    return get_students_needing_attention(class_id, db)

@router.get("/{class_id}/students")
def list_class_students(class_id: int, db: Session = Depends(get_db)):
    students = db.query(Student).filter(Student.class_id == class_id).all()
    results = []
    for s in students:
        overall = db.query(func.avg(ConceptPerformance.mastery_score))\
            .filter(ConceptPerformance.student_id == s.id)\
            .scalar() or 0.0
        overall_val = round(float(overall), 1)
        tier = get_student_status_label(overall_val)

        # find weak concept
        lowest = db.query(ConceptPerformance)\
            .join(Concept)\
            .filter(ConceptPerformance.student_id == s.id)\
            .order_by(ConceptPerformance.mastery_score.asc())\
            .first()

        results.append({
            "id": s.id,
            "name": s.name,
            "roll_number": s.roll_number,
            "email": s.email,
            "overall_mastery": overall_val,
            "status_label": tier,
            "weak_concept": lowest.concept.name if lowest else "None",
            "weak_mastery": round(lowest.mastery_score, 1) if lowest else 0.0
        })

    # Put demo accounts first
    results.sort(key=lambda x: (
        0 if x["email"] == "student@demo.com" else
        (1 if x["email"] == "advanced@demo.com" else 2),
        x["id"]
    ))
    return results
