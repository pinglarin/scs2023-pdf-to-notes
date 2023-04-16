from sqlalchemy.orm import Session

import models, schemas
from fastapi import FastAPI, File, UploadFile

def generate_summary(file: UploadFile):
    print("generating summary of ", file.filename)
    return "TEMPORARY SUMMARY"

# used for reference
# def get_video_by_ID(db: Session, uuid: str):
#     print("in get_video_by_ID")
#     print("uuid in get_video: ", uuid)
#     return db.query(models.Video).filter(models.Video.uuid == uuid).first()

# def get_all_videos(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Video).offset(skip).limit(limit).all()

# def create_video(db: Session, video: schemas.VideoBase, file: UploadFile, uuid: str, path:str):
#     print("in create_video")
#     vdo = models.Video(uuid=uuid, VideoName=file.filename, VideoPath = path, LectureName=video.LectureName, CourseName = video.CourseName, LecturerID=video.LecturerID, Details=video.Details)
#     db.add(vdo)
#     db.commit()
#     db.refresh(vdo)
#     print("file is inside database ", file.filename)
#     print("Video is successfully uploaded")
#     return vdo

# def create_student(db: Session, student: schemas.StudentBase):
#     print("in create_student")
#     stu = models.Student(StudentID=student.StudentID, Firstname=student.Firstname, Lastname=student.Lastname)
#     db.add(stu)
#     db.commit()
#     db.refresh(stu)
#     print("student is successfully created")
#     return stu