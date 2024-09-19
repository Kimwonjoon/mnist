from typing import Annotated
from fastapi import FastAPI, File, UploadFile
import os

app = FastAPI()

@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile): # async 비동기 ??? -> 이거 좀 알아보자
    # 이미지 파일 서버에 저장
    img = await file.read()
    file_name = file.filename
    upload_dir = "./photo"
    file_full_path = os.path.join(upload_dir, file_name)
    os.makedirs(os.path.dirname(file_full_path), exist_ok = True)
    with open(file_full_path, 'wb') as f:
        f.write(img)

    # 이미지 파일 저장 경로를 DB에 insert
    # 컬럼정보 : 파일이름, 파일경로, 요청시간(초기 insert), 요청 사용자(n??)
    # 컬럼정보 : 예측모델, 예측결과, 요청시간, 예측시간(추후 업뎃)
    return {
            "filename": file_name,
            "content_type" : file.content_type,
            "file_full_path" : file_full_path
            }
