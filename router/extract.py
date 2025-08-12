'''
html_to_extract
zipping_html
'''

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, FileResponse


import zipfile
import io
from pathlib import Path

from src.get_user_dir import get_user_dir




router = APIRouter()



@router.get("/extract", response_class=FileResponse)
async def download_html_zip(request: Request):
    '''
    user_dir 내의 모든 html 파일을 zip으로 묶어 클라이언트가 다운로드할 수 있게 함
    '''
    try:
        user_id = request.client.host
        user_saved_dir = get_user_dir(user_id) / "saved"

        html_files = list(user_saved_dir.rglob("*.html"))
        if not html_files:
            return JSONResponse({"message": "html 파일이 존재하지 않습니다."}, status_code=404)

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for html_file in html_files:
                zip_file.write(html_file, arcname=html_file.name)
        zip_buffer.seek(0)

        return FileResponse(
            zip_buffer,
            media_type="application/x-zip-compressed",
            filename="html_files.zip"
        )
    except Exception as e:
        return JSONResponse({"message": f"압축 및 다운로드 실패: {str(e)}"}, status_code=400)
