from sqlalchemy import create_engine, Column, Integer, String, Text, exc # To handle exceptions while querying
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker
from fastapi import FastAPI, Response, status
from pydantic import BaseModel, parse_obj_as
from typing import Optional, List
import json, os
from dotenv import load_dotenv

# To run use the below command from the same directory which has courseservice.py
# uvicorn courseservice:app --port 8081 --reload 
# The Swagger API documentation is hosted at http://localhost:8081/docs 

Base = declarative_base()
class Course(Base):
    __tablename__ = 'course'

    id = Column(Integer(), primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    duration_in_weeks = Column(Integer, nullable=False)
    category = Column(String(15), nullable=False)
    description = Column(String(100), nullable=False)

class CourseSchema(BaseModel):

    id: Optional[int] = None
    name: str   
    duration_in_weeks: int
    category:str
    description:str

    class Config:
        orm_mode = True

#Read the environment variables
load_dotenv('.env')
app = FastAPI()

#Construct the DB Connection URL using environment variable
url = URL.create( drivername=os.environ['DB_Driver'], username=os.environ['DB_Username'], password=os.environ['DB_Password'], host=os.environ['DB_Host'], database=os.environ['Database'])
engine = create_engine(url)
print("Connecting to database")
connection = engine.connect()
print("Connection successful ")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


@app.get('/courses')
def getAllCourses(response: Response):
    courses = session.query(Course).all()
    
    if len(courses) == 0: #No courses exists return appropraite HTTPS response
        response.status_code = status.HTTP_200_OK
        retString = "No courses exists in the course database"
        json_string = '{"message": "' + retString + '"}'
        return json.loads(json_string)
    else:
        course_list = parse_obj_as(List[CourseSchema], courses)
        response.status_code = status.HTTP_200_OK
        return course_list

@app.get('/courses/{u_id}')
def get_course(u_id: int, response: Response):
    courses = session.query(Course).filter(Course.id == u_id).all()
    if len(courses) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND 
        retString = "Course with id " + str(u_id) + " does not exists in course database"
        json_string = '{"message": "' + retString + '"}'
        return json.loads(json_string)
    else:
        course_list = parse_obj_as(List[CourseSchema], courses)
        response.status_code = status.HTTP_200_OK
        return course_list

@app.delete('/courses/{u_id}', status_code=202)
def delete_course(u_id: int):
    try:
        retValue = session.query(Course).filter(Course.id==u_id).delete()

        if retValue == 0:
            retString = "course with course id " + str(u_id) + " does not exists"
            json_string = '{"message": "' + retString + '"}'
            return json.loads(json_string)
        else:
            session.commit()
            retString = "course with course id " + str(u_id) + " deleted successfully"
            json_string = '{"message": "' + retString + '"}'
            return json.loads(json_string)
    except:
        session.rollback()
        print('Exception occurred while deleting the course')

@app.put('/courses/{u_id}', status_code=202)
def update_course(u_id: int, courseObj: CourseSchema, response: Response):
    courses = session.query(Course).filter(Course.id == u_id).all()
    if len(courses) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        retString = "Course with id " + str(u_id) + " does not exists in course database"
        json_string = '{"message": "' + retString + '"}'
        return json.loads(json_string)
    else:
        new_course = Course(
        id=courseObj.id,
        name=courseObj.name,
        duration_in_weeks=courseObj.duration_in_weeks,
        category=courseObj.category,
        description=courseObj.description
        )
        try:
            session.query(Course).filter(Course.id == u_id).update({Course.name:new_course.name, 
            Course.duration_in_weeks:new_course.duration_in_weeks, Course.category:new_course.category, Course.description:new_course.description})
            session.commit()
            return CourseSchema.from_orm(new_course)
        except Exception:
            session.rollback()
            print("Exception Occured")
            return "Unable to add duplicate values"

@app.post('/courses', status_code=201)
def new_course(courseObj: CourseSchema):
    courses = session.query(Course).all()
    if len(courses) == 0:
        u_id = 1
    else:
        max_id = 1
        for u in courses:
            if u.id > max_id:
                max_id = u.id
        u_id = max_id + 1

    new_course = Course(
        id=u_id,
        name=courseObj.name,
        duration_in_weeks=courseObj.duration_in_weeks,
        category=courseObj.category,
        description=courseObj.description
    )

    try:
        session.add(new_course)
        session.commit()
        return CourseSchema.from_orm(new_course)
    
    except exc.IntegrityError:
        session.rollback()
        print("Exception Occured")
        return "Unable to add duplicate values"

    