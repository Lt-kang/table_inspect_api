from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse

import numpy as np
import json
from pathlib import Path

router = APIRouter()

from src.get_user_dir import get_user_dir
from src.html2img import html_to_png
from src.processing import (
    read_html_file,
    img_to_base64
)



@router.get("/inspect/{index}", response_class=HTMLResponse)
async def main(request: Request, index: str):
    user_id = request.client.host

    if int(index) == -1:
        return JSONResponse(
            {
                "mainImage": "",
                "hoverImage": "",
                "html": "",
                "hiddenTextInfo": ""
            }
        )

    user_base_dir = get_user_dir(user_id)
    user_html_to_png_dir = user_base_dir / "html_to_png"

    with open(user_base_dir / "file_index.json", "r", encoding="utf-8") as f:
        file_index = json.load(f)

    file_index_keys = sorted(list(file_index.keys()), key=lambda x: int(x))

    file_index_min = int(file_index_keys[0])
    file_index_max = int(file_index_keys[-1])

    if file_index_min > int(index) or int(index) > file_index_max:
        return JSONResponse({"error": "Invalid ID"}, status_code=404)
    
    target_index = file_index[str(index)]

    '''
    html to png randering
    '''

    if not (Path(user_html_to_png_dir) / f"{target_index['hidden_text_info']}.png").exists() and \
        Path(target_index['html']).exists() and \
        Path(target_index['html']).read_text(encoding="utf-8").strip() != "":
        
        html_to_png(Path(target_index['html']), 
                    Path(target_index['png']), 
                    Path(user_html_to_png_dir) / f"{target_index['hidden_text_info']}.png")



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

