import base64


def read_html_file(html_path: str) -> str:
    """
    HTML 파일을 텍스트로 읽습니다.
    
    :param html_path: HTML 파일 경로
    :return: HTML 내용 문자열
    """
    with open(html_path, "r", encoding="utf-8") as html_file:
        return html_file.read() + "<p><br></p>"

def img_to_base64(image_path: str) -> str:
    """
    이미지 파일을 base64 문자열로 변환합니다.

    :param image_path: 변환할 이미지 파일의 경로
    :return: base64 인코딩된 문자열
    """
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
    return "data:image/png;base64," + encoded_string
