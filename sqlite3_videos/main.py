from fastapi import FastAPI, File, UploadFile
import crud
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi import FastAPI

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    print("at the root")
    return {"message": "Hello World"}


@app.post("/gen_summary")
async def Generate_Summary(file: UploadFile = File(...)):
    summary = crud.generate_summary(file);
    print("summary generated")
    print(summary)
    return summary