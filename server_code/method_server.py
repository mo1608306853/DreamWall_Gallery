import os
import json
import subprocess
import numpy as np
from PIL import Image


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'model')
index_model_path = os.path.join(model_path, 'Index_1_9B')
sd_model_path = os.path.join(model_path, 'chilloutmix-fp16')
text_path = os.path.join(BASE_DIR, 'text.json')


def run_method(arg_data):
    task_method = arg_data['task_method']
    task_text = arg_data['task_text']
    ret_data = {'message': 'run code', 'code': 200}
    if task_method in ['text', 'image']:
        subprocess.Popen(f'python text_image.py {task_method} {task_text}', shell=True, cwd=BASE_DIR)
    elif task_method == 'get_data':
        img = Image.open('./sd_picture.png')
        img_data = np.array(img)
        show_text = []
        with open(text_path, 'r', encoding='utf-8') as f:
            show_text = json.loads(f.read())
        ret_data = {'code': 200, 'show_text': show_text, 'img_array': img_data.tolist()}
    return ret_data


if __name__ == "__main__":
    arg_data = {'task_method': 'image', 'task_text': 'The composition of the foreground with the soft focus of the budding flowers'}
    arg_data = {'task_method': 'get_data', 'task_text': ''}
    ret_data = run_method(arg_data)
    print(ret_data)