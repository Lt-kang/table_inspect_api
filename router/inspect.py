from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse

import json
from pathlib import Path

router = APIRouter()

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
        html_to_png(html_file, png_file, user_html_to_png_dir / f"{key}.png")

    return True


@router.get("/data/{index}", response_class=HTMLResponse)
async def main(request: Request, index: str):
    user_id = request.client.host

    user_dir = get_user_dir(user_id)

    user_html_to_png_dir = Path(user_dir) / "html_to_png"

    





    if index >= len(data) or index < 0:
        return JSONResponse({"error": "Invalid ID"}, status_code=404)
    
    target_data = data[id]
    
    return JSONResponse(
        {
            "mainImage": target_data['mainImage'],
            "hoverImage": target_data['hoverImage'],
            "html": target_data['html'],
            "hiddenTextInfo": target_data['hiddenTextInfo']
        }
    )

