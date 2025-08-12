from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse

import json
from pathlib import Path

router = APIRouter()

from src.get_user_dir import get_user_dir
from src.html2img import html_to_png
from src.processing import (
    read_html_file,
    img_to_base64
)


def preprocess_data(user_id):
    user_base_dir = get_user_dir(user_id)

    user_raw_html_dir = user_base_dir / "raw"
    user_saved_html_dir = user_base_dir / "saved"
    user_raw_png_dir = user_base_dir / "raw"

    user_html_to_png_dir = user_base_dir / "html_to_png"

    html_files = {file.stem: file for file in user_raw_html_dir.rglob("*.html")}
    for file in user_saved_html_dir.rglob("*.html"):
        html_files[file.stem] = file

    png_files = {file.stem: file for file in user_raw_png_dir.rglob("*.png")}

    for key in png_files.keys():
        html_file = html_files[key]
        png_file = png_files[key]
        html_to_png(html_file, png_file, user_html_to_png_dir / f"{key}.png")

    return True


@router.get("/inspect/{index}", response_class=HTMLResponse)
async def main(request: Request, index: str):
    user_id = request.client.host

    user_base_dir = get_user_dir(user_id)

    with open(user_base_dir / "file_index.json", "r", encoding="utf-8") as f:
        file_index = json.load(f)

    file_index_keys = sorted(list(file_index.keys()))

    file_index_min = int(file_index_keys[0])
    file_index_max = int(file_index_keys[-1])

    if file_index_min > int(index) or int(index) > file_index_max:
        return JSONResponse({"error": "Invalid ID"}, status_code=404)
    
    target_index = file_index[str(index)]
    # print({
    #         "mainImage": img_to_base64(target_index['png']),
    #         "hoverImage": img_to_base64(target_index['html_to_png']),
    #         "html": read_html_file(target_index['html']),
    #         "hiddenTextInfo": target_index['hidden_text_info']
    #     })
    return JSONResponse(
        {
            "mainImage": img_to_base64(target_index['png']),
            "hoverImage": img_to_base64(target_index['html_to_png']),
            "html": read_html_file(target_index['html']),
            "hiddenTextInfo": target_index['hidden_text_info']
        }
    )

