<<<<<<< HEAD
# models of db
from sqlalchemy import Column, Integer, TEXT, ForeignKey, DATE,String ,TIME ,Enum as SQLAlchemyEnum
from db.engine import Base
from enum import Enum



class USERROLES(str,Enum):
    USER = 'user'
    ADMIN = 'admin'


class USERS(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(TEXT, nullable=False, unique=True,index=True)
    password = Column(TEXT, nullable=False)
    name = Column(TEXT, nullable=False)
    role=Column(String,nullable=False,default=USERROLES.USER)
    Username = Column(TEXT, nullable=False)


####status FOR enum_DR
class degreeStatus(str ,Enum):
     GENERAL = 'general'
     SPECIALIZATION = 'specialization'
     SUBSPECIALTY = 'subspecialty'
    
class DOCTORS(Base):
    __tablename__ = 'doctors'
    doctor_id = Column(Integer, primary_key=True, index=True)
    email = Column(TEXT, nullable=False, unique=True,index=True)
    password = Column(TEXT, nullable=False)
    name = Column(TEXT, nullable=False)
    specialization = Column(TEXT, nullable=False)
    work_experience=Column(Integer,nullable=False)
    about_dr =Column(TEXT, nullable=False)
    degree=Column(SQLAlchemyEnum(degreeStatus),nullable=False)
    Username = Column(TEXT, nullable=False)
   



####status FOR enum_APPOINTMENT
class AppointmentStatus(str , Enum):
    CANCEL = "Cancel"
    COMPLETE = "Complete"
    NOT_COMPLETE = "Nocomplete"

class APPOINMENT(Base):
    __tablename__ ='appointments'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    day = Column(DATE, nullable=False) 
    time = Column(TIME, nullable=False)
    status = Column(SQLAlchemyEnum(AppointmentStatus), nullable=False , default=AppointmentStatus.NOT_COMPLETE) 
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False) 
    doctor_id = Column(Integer, ForeignKey('doctors.doctor_id'), nullable=False)  
    explanation =Column(TEXT,nullable=False)
=======
# models of db
from sqlalchemy.orm import Mapped, mapped_column
from .engine import Base


class User(Base):
    __tablename__ = "users"

    password: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column(unique=True)
    id: Mapped[int] = mapped_column(primary_key=True)
>>>>>>> c654aed5cb4e471277e496815c6912edc203b038
