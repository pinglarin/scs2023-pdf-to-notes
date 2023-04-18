from fastapi import UploadFile
from fastapi.responses import FileResponse
import PyPDF2
import aspose.words as aw
from docx import Document
from io import BytesIO

def generate_summary(file: UploadFile):
    inputText = ""
    print("generating summary of ", file.filename)
    f = file.file
    f.seek(0)
    reader = PyPDF2.PdfReader(f)
    for page in reader.pages:
        inputText += page.extract_text()
    # idea: maybe we can seperate each page so the output will be seperate into pages?
    print("\nDone with generate_summary function in crud\n")
    outputText  = "this is the output text"
    print(outputText)
    doc = Document()
    print("doc = Document()")
    doc.add_paragraph(outputText)
    print("doc.add_paragraph(outputText)")
    docx_bytes = BytesIO()
    print("before doc.save")
    doc.save(docx_bytes)
    print("after doc.save")
    headers = { "Content-Disposition": "inline; filename=Summary.txt" } # vs attachment
    print("before return")
    return FileResponse(docx_bytes.getvalue(), headers=headers)


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