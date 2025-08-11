from pathlib import Path
import json
import shutil
import os



user_mapping_dir = Path(__file__).parent.parent / "user_mapping.json"
if not user_mapping_dir.exists():
    with open(user_mapping_dir, "w", encoding="utf-8") as f:
        json.dump({}, f)

with open(user_mapping_dir, "r", encoding="utf-8") as f:
    user_mapping = json.load(f)

    if user_mapping == "":
        user_mapping = {}

    user_list = list(user_mapping.keys())



def create_user_dir(user_dir:str):
    user_dir = Path(user_dir)

    user_raw_dir = user_dir / "raw"
    user_saved_dir = user_dir / "saved"
    user_html_to_png_dir = user_dir / "html_to_png"
    
    user_raw_dir.mkdir(parents=True, exist_ok=True)
    user_saved_dir.mkdir(parents=True, exist_ok=True)
    user_html_to_png_dir.mkdir(parents=True, exist_ok=True)

    with open(user_dir / "file_index.json", "w", encoding="utf-8") as f:
        json.dump({}, f)




def get_user_dir(user_id, init=False):
    if user_id in user_list:
        if init:
            shutil.rmtree(user_mapping[user_id])
            os.makedirs(user_mapping[user_id], exist_ok=True)

    else:
        '''
        user_id가 user_list에 없을 경우
        '''
        user_mapping[user_id] = str(Path(__file__).parent.parent / "user_dir" / str(user_id).split(".")[-1])
        with open(user_mapping_dir, "w", encoding="utf-8") as f:
            json.dump(user_mapping, f)

    user_dir = user_mapping[user_id]
    create_user_dir(user_dir)
    return user_dir
