from typing import Optional
from pydantic import BaseModel
from datetime import date, time
from db.models import degreeStatus 

class UserBase(BaseModel):
    email: str
    name: str
    role: str
    Username: str

class UserModel(UserBase):
    user_id: int

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str
   
class UserUpdate(BaseModel):
    username: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str] = None

class UserLogin(BaseModel):
    Username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_tyoe :str



class TokenData(BaseModel):
    email:str = None
    



class AdminBase(BaseModel):
    email: str
    name: str
    role: str
    Username: str

class AdminModel(UserBase):
    user_id: int

class AdminLogin(BaseModel):
    Username: str
    password: str
    class Config:
        from_attributes = True



class DoctorBase(BaseModel):
    email: str
    name: str
    Username: str
    specialization: str
    work_experience: int
    about_dr: str
    degree: degreeStatus
    
class DoctorCreate(DoctorBase):
    password: str
   

class DoctorLogin(BaseModel):
    Username: str
    password: str


class DoctorModel(DoctorBase):
     doctor_id: int
     class Config:
        from_attributes = True

class DrUpdate(BaseModel):
    username: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str] = None

class Appointmentmodel(BaseModel):
    id: int
    day: date
    time: time
    user_id: int
    doctor_id: int
    explanation: str
    status: str

    class Config:
          from_attributes = True

class AppointmentCreat(BaseModel):
    doctor_name: str  #کاربر نام دکتر را وارد می‌کند
    day: date
    time: time
    explanation: str
    status: str

    
class SeeAppointment(BaseModel):
    day: date
    time: time
    doctor_name: int
    specialization_dr:str
    status: str

class ResponseModel(BaseModel):
    appointments: list[SeeAppointment]

 
class SeeAppointmentforAdmin(BaseModel):
    day: str
    time: str
    patient_name: str
    doctor_name: str
    specialization_dr:str
    status: str

class ResponseModel1(BaseModel):
    appointments: list[SeeAppointmentforAdmin]



class SeeAppointmentforDr(BaseModel):
    day: str
    time: str
    patient_name: str
    status: str
    explanation:str

class ResponseModelDr(BaseModel):
    appointments: list[SeeAppointmentforDr]