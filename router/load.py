'''
upload_file
'''
'''
register_user
create_user_dir
'''

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from collections import defaultdict
from pathlib import Path
import json

from src.get_user_dir import get_user_dir
from src.html2img import html_to_png




def preprocess_data(user_id):
    user_dir = get_user_dir(user_id)

    user_raw_html_dir = Path(user_dir) / "raw"
    user_saved_html_dir = Path(user_dir) / "saved"
    user_raw_png_dir = Path(user_dir) / "raw"

    user_html_to_png_dir = Path(user_dir) / "html_to_png"

    html_files = {file.stem: file for file in user_raw_html_dir.rglob("*.html")}
    for file in user_saved_html_dir.rglob("*.html"):
        html_files[file.stem] = file

    png_files = {file.stem: file for file in user_raw_png_dir.rglob("*.png")}

    for key in png_files.keys():
        html_file = html_files[key]
        png_file = png_files[key]
        html_to_png(html_file, 
                    png_file, 
                    user_html_to_png_dir / f"{key}.png")

    file_index = defaultdict(dict)
    for idx, key in enumerate(html_files.keys()):
        file_index[idx] = {
            "html": html_files[key],
            "png": png_files[key],
            "html_to_png": user_html_to_png_dir / f"{key}.png"
        }

    with open(Path(user_dir) / "file_index.json", "w", encoding="utf-8") as f:
        json.dump(file_index, f, ensure_ascii=False, indent=4)

    return True




router = APIRouter()



from fastapi import UploadFile, File, Form
from typing import List

@router.post("/load", response_class=JSONResponse)
async def load_files(
    request: Request,
    user_folder: str = Form(...),
    files: List[UploadFile] = File(...)
):
    try:
        user_id = request.client.host

        user_dir = get_user_dir(user_id, init=True)

        user_raw_dir = Path(user_dir) / "raw"

        # png와 html 파일 저장
        saved_files = []
        for upload_file in files:
            filename = upload_file.filename
            if filename.endswith(".png") or filename.endswith(".html"):
                file_path = user_raw_dir / filename
                with open(file_path, "wb") as f:
                    content = await upload_file.read()
                    f.write(content)
                saved_files.append(filename)

        if not saved_files:
            return JSONResponse({"message": "저장된 파일이 없습니다. png 또는 html 파일만 허용됩니다."}, status_code=400)
        

        '''
        파일을 전부 server에 저장하였다면
        전처리를 시작함.
        이는 이후 작업시 load를 빨리 하기 위함에 있음.
        '''
        preprocess_data(user_id)

        return JSONResponse({"message": "upload success", "saved_files": saved_files}, status_code=200)
    
    except Exception as e:
        return JSONResponse({"message": f"upload failed: {str(e)}"}, status_code=400)


