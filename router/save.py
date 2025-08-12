from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi import Form

from pathlib import Path

from src.get_user_dir import get_user_dir
from src.html2img import html_to_png

router = APIRouter()


@router.post("/save", response_class=JSONResponse)
async def save_html(
    request: Request,
    html: str = Form(...),
    hiddenTextInfo: str = Form(...)
):
    """
    프론트엔드에서 수정된 html을 받아서 해당 유저의 user_dir/saved/에 저장(덮어쓰기)합니다.
    """
    try:
        user_id = request.client.host
        user_base_dir = Path(get_user_dir(user_id))

        user_saved_dir = Path(user_base_dir) / "saved"
        user_raw_dir = Path(user_base_dir) / "raw"
        user_html_to_png_dir = Path(user_base_dir) / "html_to_png"

        file_path = user_saved_dir / f"{hiddenTextInfo}.html"
        with open(file_path, "w", encoding="utf-8") as f:
            if html.endswith("<p><br></p>"):
                html = html[:-len("<p><br></p>")]
                
            f.write(html)

        html_to_png(file_path, 
                    user_raw_dir / f"{hiddenTextInfo}.png",
                    user_html_to_png_dir / f"{hiddenTextInfo}.png")

        return JSONResponse({"message": "HTML 저장 성공", "filename": hiddenTextInfo}, status_code=200)
    
    except Exception as e:
        return JSONResponse({"message": f"HTML 저장 실패: {str(e)}"}, status_code=400)

