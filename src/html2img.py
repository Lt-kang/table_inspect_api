import imgkit
from tqdm import tqdm
from pathlib import Path
import cv2
import numpy as np
import os
import tempfile


config = imgkit.config(wkhtmltoimage=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe")


def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8) -> None:
    n = np.fromfile(filename, dtype)
    img = cv2.imdecode(n, flags)
    return img

def imwrite(filename, img, params=None):
    ext = os.path.splitext(filename)[1]
    result, n = cv2.imencode(ext, img, params)

    if result:
        with open(filename, mode='w+b') as f:
            n.tofile(f)


code_path = Path(__file__).parent
def html_to_png(html_file:Path, png_file:Path, save_path:Path):
    img = imread(png_file)
    html_data = html_file.read_text(encoding="utf-8")

    with tempfile.TemporaryDirectory() as tmpdir:
        imgkit.from_string(
            html_data, 
            Path(tmpdir) / '_temp.png', 
            config = config,
            css = code_path / "style.css",
            options = {'enable-local-file-access': None,
                        'quality': '100',
                        'zoom': '1.0'}
        )

        img = imread(Path(tmpdir) / '_temp.png')
        img = cv2.resize(img, (img.shape[1], img.shape[0]))
        imwrite(str(save_path), img)

    
