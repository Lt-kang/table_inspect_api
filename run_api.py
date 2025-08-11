from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi.responses import HTMLResponse
from pathlib import Path
from io import BytesIO
import base64

from router import (
    inspect,
    load,
    register
    )



app = FastAPI()

app.include_router(inspect.router, prefix="/api/v1")
app.include_router(register.router, prefix="/api/v1")
app.include_router(load.router, prefix="/api/v1")
# app.include_router(ip_check.router, prefix="/api/v1")
# app.include_router(summary_objects.router, prefix="/api/v1")
# app.include_router(json_schema_extract.router, prefix="/api/v1")
# app.include_router(json_validate.router, prefix="/api/v1")







app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React 앱의 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# def init_data():
#     data = []
#     target_path = Path(__file__).parent / "test_input"

#     html_png_list = sorted(list((target_path / "html_to_png").rglob("*.png")))
#     html_list = sorted(list((target_path / "html").rglob("*.html")))
#     raw_png_list = sorted(list((target_path / "png").rglob("*.png")))

#     for html_png, html, raw_png in zip(html_png_list, html_list, raw_png_list):
#         text_info = html_png.stem
#         html_png_base64 = img_to_base64(html_png)
#         raw_png_base64 = img_to_base64(raw_png)
#         html_base64 = read_html_file(html)

#         data.append({
#             "mainImage": "data:image/png;base64," +raw_png_base64,
#             "hoverImage": "data:image/png;base64," + html_png_base64,
#             "html": html_base64,
#             "hiddenTextInfo": text_info
#         })
#     return data
        
        

# data = init_data()




@app.get("/api/health")
async def health_check():
    """API 상태 확인 엔드포인트"""
    return {"status": "healthy", "message": "FastAPI 서버가 정상 작동 중입니다"}


if __name__ == "__main__":
    # uvicorn.run('run_api:app', host="172.127.0.201", port=8000, reload=True)
    uvicorn.run('run_api:app', host="0.0.0.0", port=8000, reload=True)



