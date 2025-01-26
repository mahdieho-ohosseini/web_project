<<<<<<< HEAD
from datetime import datetime, timedelta, date
from typing import Annotated, List
from fastapi import FastAPI, Depends, HTTPException,status, Header , status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
import auth
from db import models, schemas
from db.engine import SessionLocal, engine, get_db
from db.models import  Base ,USERS , DOCTORS ,APPOINMENT
from contextlib import asynccontextmanager
from typing import AsyncIterator 


Base.metadata.create_all(bind=engine)
app = FastAPI()
origins = [ ]



@app.post('/users/signup', response_model=schemas.UserBase)
def create_user(user: schemas.UserCreate, db: Annotated[Session, Depends(get_db)]):
    isTaken = db.query(models.USERS).filter(models.USERS.email == user.email).first()
    if isTaken:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This user already exists")
    hash_password = auth.hash_password(user.password)
    db_user = USERS(name=user.name,Username=user.Username, email=user.email, password=hash_password, role='user')  
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



@app.post('/users/login')
async def login_user(db: Annotated[Session, Depends(get_db)], form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(models.USERS).filter(models.USERS.Username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )  
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
       user.Username,user.user_id,"user", expires_delta=access_token_expires
    )  
    return {
        "message": "Login Successful",
        "access_token": access_token, "token_type": "bearer"
    }



@app.get("/logged-user")
async def get_current_user(db: Annotated[Session, Depends(get_db)], token: str = Header(...)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = token.split()
    token = token[1]
    try:
        payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        user_id :int  = payload.get("id")
        role :str = payload.get("role")
        if username is None or user_id is None or role!='user':
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.USERS).filter(models.USERS.user_id == user_id).first()
    if user is None:
        return {
            'user not found'
        }
    return user



@app.post('/admin/login')
def login_admin(form_data: schemas.AdminLogin, db: Annotated[Session, Depends(get_db)]):
    admin = db.query(models.USERS).filter(models.USERS.Username == form_data.Username, models.USERS.role == 'admin' ).first()
    if not admin or not auth.verify_password(form_data.password, admin.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
            ) 
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
       admin.Username,admin.user_id, 'admin', expires_delta=access_token_expires
    )   
    return {
        "message": "Login Successful",
        "user_detail": admin,
        "access_token": access_token, "token_type": "bearer"
        }



@app.get('/logged-admin')
def current_admin(db: Annotated[Session, Depends(get_db)], token: str = Header(...)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = token.split()
    token = token[1]
    try:
        payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        admin_id :int  = payload.get("id")
        role :str = payload.get("role")
        if admin_id is None or role!='admin':
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    admin = db.query(models.USERS).filter(models.USERS.user_id == admin_id, models.USERS.role == 'admin').first()
    if admin is None:
        return None
    return admin


  
@app.post('/doctor/login')
async def login_doctor(db: Annotated[Session, Depends(get_db)], form_data: OAuth2PasswordRequestForm = Depends()):
    doctor = db.query(models.DOCTORS).filter(models.DOCTORS.Username == form_data.username ).first()
    if not doctor or not auth.verify_password(form_data.password, doctor.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )  
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
         doctor.Username ,doctor.doctor_id,"doctor", expires_delta=access_token_expires
    )
    return {
        "message": "Login Successful",
        "access_token": access_token, "token_type": "bearer"
    }




@app.get("/logged-doctor")
async def get_current_doctor(db: Annotated[Session, Depends(get_db)], token: str = Header(...)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = token.split()
    token = token[1]
    try:
        payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        user_id :int  = payload.get("id")
        role :str = payload.get("role")
        if username is None or user_id is None or role!="doctor":
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.DOCTORS).filter(models.DOCTORS.doctor_id ==user_id).first()
    if user is None:
        raise credentials_exception
    return user



@app.post('/add/doctor')
async def add_doctor(
    data: schemas.DoctorCreate, 
    db: Annotated[Session, Depends(get_db)]
):
    doctor = db.query(models.DOCTORS).filter(
        (models.DOCTORS.email == data.email) |
        (models.DOCTORS.name == data.name) |
        (models.DOCTORS.specialization == data.specialization)
    ).first()
    if doctor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Doctor with this email, name, or specialization already exists"
        )
    hash_password = auth.hash_password(data.password)
    
    try:
        db_doctor = models.DOCTORS(
            email=data.email,
            password=hash_password,
            name=data.name,
            Username=data.Username,
            specialization=data.specialization,
            work_experience=data.work_experience,
            about_dr=data.about_dr,
            degree=data.degree.value  
        )
        db.add(db_doctor)
        db.commit()
        db.refresh(db_doctor)
        return db_doctor
    except Exception as e:

        print(f"An error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to add doctor"
        )
    

    
@app.post("/appointments/", response_model=schemas.Appointmentmodel)
async def create_appointment(
    db: Annotated[Session, Depends(get_db)],
    appointment: schemas.AppointmentCreat,
    token:str = Header(...)
):    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = token.split()
    token = token[1]
    try:
        payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        role: str = payload.get("role")
        id: int = payload.get('id')
        if role is None or id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    doctor = db.query(DOCTORS).filter(DOCTORS.name ==appointment.doctor_name ).first()

    if role == 'user':
        
        data = db.query(models.USERS).filter(models.USERS.user_id == id).first()
        db_appointment = models.APPOINMENT(
            day=appointment.day,
            time=appointment.time,
            user_id=data.user_id,
            doctor_id=doctor, 
            explanation=appointment.explanation,
            status=appointment.status
        )
        db.add(db_appointment)
        db.commit()
        db.refresh(db_appointment)
        return db_appointment
    return None


@app.get("/user/my-appointments/",response_model=schemas.SeeAppointment)
async def get_my_appointments(   
    db: Annotated[Session, Depends(get_db)],
    token:str = Header(...)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = token.split()
    token = token[1]
    try:
        payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        role: str = payload.get("role")
        id: int = payload.get('id')
        if role is None or id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    appointments = db.query(models.APPOINMENT).filter(models.APPOINMENT.user_id == id).all()
    appointment_list = []
    for appointment in appointments:
        dr_name= db.query(DOCTORS).filter(DOCTORS.doctor_id == appointment.doctor_id,).first()
        specialization_dr= db.query(DOCTORS).filter(DOCTORS.doctor_id == appointment.doctor_id).first()
        appointment_list.append({
            "day": appointment.day,
            "time": appointment.time,
            "status": appointment.status,
            "doctor_name":dr_name,
            "specialization_dr":specialization_dr
        })
    return {"appointments": appointment_list}

    


@app.get("/admin/allappointments/", response_model=schemas.ResponseModel1)
async def get_all_appointments(
    db: Session = Depends(get_db),
    token: str = Header(...)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = token.split()
    token = token[1]
    try:
        payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        role: str = payload.get("role")
        id: int = payload.get('id')
        if role is None or id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    appointments = db.query(models.APPOINMENT).all()
    appointment_list = []
    for appointment in appointments:
        user = db.query(USERS).filter(USERS.user_id == appointment.user_id).first()
        doctor = db.query(DOCTORS).filter(DOCTORS.doctor_id == appointment.doctor_id).first()
        specialization_dr = db.query(DOCTORS).filter(DOCTORS.doctor_id == appointment.doctor_id).first()
        
        appointment_list.append(schemas.SeeAppointmentforAdmin(
            day=str(appointment.day),  
            time=str(appointment.time),  
            status=appointment.status,
            patient_name=user.name,
            doctor_name=doctor.name,
            specialization_dr=specialization_dr.specialization
        ))
    return schemas.ResponseModel1(appointments=appointment_list)



@app.get("/doctor/my-appointments/", response_model=schemas.ResponseModelDr)
async def get_doctor_appointments(
    db: Session = Depends(get_db),
    token: str = Header(...)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = token.split()
    token = token[1]
    try:
        payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        role: str = payload.get("role")
        id: int = payload.get('id')
        if role is None or id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    appointments = db.query(APPOINMENT).filter(
        APPOINMENT.doctor_id == id,
        APPOINMENT.status == models.AppointmentStatus.NOT_COMPLETE
    ).all()
    
    appointment_list = []
    for appointment in appointments:
        user = db.query(USERS).filter(USERS.user_id == appointment.user_id).first()
        appointment_list.append(schemas.SeeAppointmentforDr(
            day=str(appointment.day),  
            time=str(appointment.time), 
            patient_name=user.name if user else "Unknown",
            status=appointment.status,
            explanation=appointment.explanation
        ))
    return schemas.ResponseModelDr(appointments=appointment_list)



@app.put("/user/update-profile/{user_id}")
def update_user_profile(  
    user_update:schemas.UserUpdate,
    db: Session = Depends(get_db),
    token: str = Header(...)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = token.split()
    token = token[1]
    try:
        payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        role: str = payload.get("role")
        id: int = payload.get('id')
        if role is None or id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(USERS).filter(USERS.user_id == id).first()
    if user_update.username is not None:
        user.Username = user_update.username
    if user_update.name is not None:
        user.name = user_update.name
    if user_update.password is not None:
        user.password = auth.hash_password(user_update.password)
    
    db.commit()
    db.refresh(user)
    return {"message": "Profile updated successfully"}



@app.put("/doctor/update-profile/{doctor_id}")
def update_doctor_profile(  
    user_update:schemas.DrUpdate,
    db: Session = Depends(get_db),
    token: str = Header(...)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = token.split()
    token = token[1]
    try:
        payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        role: str = payload.get("role")
        id: int = payload.get('id')
        if role is None or id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    doctor = db.query(DOCTORS).filter(DOCTORS.doctor_id == id).first()
    if user_update.username is not None:
        doctor.Username = user_update.username
    if user_update.name is not None:
        doctor.name = user_update.name
    if user_update.password is not None:
        doctor.password = auth.hash_password(user_update.password)
    
    db.commit()
    db.refresh(doctor)
    return {"message": "Profile updated successfully"}
=======
from fastapi import FastAPI
from router.user import user_router 
from db.engine import engine, Base



app = FastAPI()

@app.lifespan
async def lifespan(app: FastAPI):
    # رویداد startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(user_router,prefix="/user")
>>>>>>> c654aed5cb4e471277e496815c6912edc203b038
