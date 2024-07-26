import os
import json
import random
import urllib.request
from PIL import Image
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
user_setup_path = os.path.join(BASE_DIR, 'user_setup.json')


class MethodClient:

    def __init__(self, hour=0, minute=0):
        self.hour = hour
        self.minute = minute

    def read_json(self):
        ret_data = {}
        with open(user_setup_path, 'r', encoding='utf-8') as f:
            ret_data = json.loads(f.read())
        return ret_data

    def write_json(self, data):
        save_data = self.read_json()
        save_data.update(data)
        with open(user_setup_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(save_data, indent=4))

    def save_img(self, data):
        numpy_data = np.array(data)
        img = Image.fromarray((numpy_data).astype(np.uint8))
        img.save('show_picture.png')

    def url_post(self, data):
        setup_data = self.read_json()
        ip = setup_data['ip']
        url = f'http://{ip}:9630/api'
        data_json = json.dumps(data).encode('utf-8')
        request = urllib.request.Request(url, data=data_json)
        request.add_header('Content-Type', 'application/json')
        response = urllib.request.urlopen(request)
        response_content = response.read()
        ret_data = json.loads(response_content)
        return ret_data

    def task_method(self):
        text = ''
        task_type = ''
        setup_data = self.read_json()
        always_display = setup_data['always_display']
        if always_display:
            run_interval = {1: 'image', 11: 'text', 14: 'get_data', 15: 'tkinter_show',
                            16: 'image', 26: 'text', 29: 'get_data', 30: 'tkinter_show',
                            31: 'image', 41: 'text', 44: 'get_data', 45: 'tkinter_show',
                            46: 'image', 56: 'text', 59: 'get_data', 0: 'tkinter_show'}
            if self.minute in run_interval:
                task_type = run_interval[self.minute]
        else:
            run_interval = setup_data['run_interval']
            for i in run_interval:
                if i['hour'] == self.hour and i['minute'] == self.minute:
                    task_type = i['task_type']
                    text = i.get('task_text', '')
        return task_type, text

    def task_text(self):
        task_type, text = self.task_method()
        setup_data = self.read_json()
        like = random.choice(setup_data['like'])
        if task_type == 'text':
            if not text:
                text_prompt = setup_data['text_prompt']
                text = f'{like}: {text_prompt}'
        elif task_type == 'image':
            if not text:
                image_prompt = setup_data['image_prompt']
                style = random.choice(setup_data['style'])
                text = f'{style},{like}:{image_prompt}'
        return task_type, text

    def run_method(self):
        task_type, text = self.task_text()
        data = {}
        if task_type == 'text':
            data = {'task_method': 'text', 'task_text': text}
        elif task_type == 'image':
            data = {'task_method': 'image', 'task_text': text}
        elif task_type == 'get_data':
            data = {'task_method': 'get_data', 'task_text': text}
        elif task_type == 'tkinter_show':
            setup_data = self.read_json()
            always_display = setup_data['always_display']
            if not always_display:
                os.popen('python tkinter_util.py')
        if task_type != 'tkinter_show' and data:
            response = self.url_post(data)
            if task_type == 'get_data':
                self.save_img(response['img_array'])
                self.write_json({'show_text': response['show_text']})
        print(data)


if __name__ == "__main__":
    MethodClient()