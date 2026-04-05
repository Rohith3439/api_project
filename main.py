from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from datetime import date
from passlib.context import CryptContext
from pydantic import BaseModel

DATABASE_URL = "postgresql://postgres:343936@localhost/leave_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# =============================
# ORM MODELS
# =============================
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    employee_id = Column(String, unique=True)
    password = Column(String)
    role = Column(String)

    leaves = relationship("LeaveRequest", back_populates="user")


class LeaveRequest(Base):
    __tablename__ = "leave_requests"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    leave_type = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    reason = Column(String)
    status = Column(String, default="Pending")

    user = relationship("User", back_populates="leaves")


Base.metadata.create_all(bind=engine)

# =============================
# PYDANTIC SCHEMAS
# =============================
class LoginSchema(BaseModel):
    employee_id: str
    password: str


class LeaveCreate(BaseModel):
    user_id: int
    leave_type: str
    start_date: date
    end_date: date
    reason: str


class LeaveUpdate(BaseModel):
    reason: str


# =============================
# DB SESSION
# =============================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =============================
# LOGIN
# =============================
@app.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.employee_id == data.employee_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not pwd_context.verify(data.password, user.password):
        raise HTTPException(status_code=400, detail="Wrong password")

    return {"user_id": user.id, "role": user.role}


# =============================
# APPLY LEAVE
# =============================
@app.post("/leave")
def apply_leave(data: LeaveCreate, db: Session = Depends(get_db)):
    if data.start_date < date.today():
        raise HTTPException(status_code=400, detail="Past date not allowed")

    if data.end_date < data.start_date:
        raise HTTPException(status_code=400, detail="End date must be after start date")

    leave = LeaveRequest(**data.dict())

    db.add(leave)
    db.commit()
    return leave


# =============================
# VIEW LEAVES (EMPLOYEE)
# =============================
@app.get("/leave/{user_id}")
def view_leave(user_id: int, db: Session = Depends(get_db)):
    return db.query(LeaveRequest).filter(LeaveRequest.user_id == user_id).all()


# =============================
# UPDATE LEAVE
# =============================
@app.put("/leave/{leave_id}")
def update_leave(leave_id: int, data: LeaveUpdate, db: Session = Depends(get_db)):
    leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    if leave.status != "Pending":
        raise HTTPException(status_code=400, detail="Only pending can update")

    leave.reason = data.reason
    db.commit()
    return leave


# =============================
# DELETE LEAVE
# =============================
@app.delete("/leave/{leave_id}")
def delete_leave(leave_id: int, db: Session = Depends(get_db)):
    leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    if leave.status != "Pending":
        raise HTTPException(status_code=400, detail="Only pending can delete")

    db.delete(leave)
    db.commit()
    return {"msg": "Deleted"}


# =============================
# ADMIN APPROVE / REJECT
# =============================
@app.put("/approve/{leave_id}")
def approve_leave(leave_id: int, db: Session = Depends(get_db)):
    leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()

    if leave.status != "Pending":
        raise HTTPException(status_code=400, detail="Already processed")

    leave.status = "Approved"
    db.commit()
    return leave


@app.put("/reject/{leave_id}")
def reject_leave(leave_id: int, db: Session = Depends(get_db)):
    leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()

    if leave.status != "Pending":
        raise HTTPException(status_code=400, detail="Already processed")

    leave.status = "Rejected"
    db.commit()
    return leave


# =============================
# ALL LEAVES (ADMIN)
# =============================
@app.get("/all-leaves")
def get_all_leaves(db: Session = Depends(get_db)):
    leaves = db.query(LeaveRequest).join(User).all()
    today = date.today()

    result = []

    for leave in leaves:

        # 🔥 AUTO UPDATE EXPIRED
        if leave.end_date < today and leave.status == "Pending":
            leave.status = "Expired"
            db.commit()

        result.append({
            "leave_id": leave.id,
            "employee_name": leave.user.name,
            "employee_id": leave.user.employee_id,
            "leave_type": leave.leave_type,
            "start_date": str(leave.start_date),
            "end_date": str(leave.end_date),
            "reason": leave.reason,
            "status": leave.status
        })

    return result


# =============================
# ACTIVE LEAVES (ONLY FOR ACTION)
# =============================
@app.get("/active-leaves")
def get_active_leaves(db: Session = Depends(get_db)):
    leaves = db.query(LeaveRequest).join(User).all()
    today = date.today()

    result = []

    for leave in leaves:
        if leave.end_date < today:
            continue

        if leave.status != "Pending":
            continue

        result.append({
            "leave_id": leave.id,
            "employee_name": leave.user.name,
            "employee_id": leave.user.employee_id,
            "leave_type": leave.leave_type,
            "start_date": str(leave.start_date),
            "end_date": str(leave.end_date),
            "reason": leave.reason,
            "status": leave.status
        })

    return result