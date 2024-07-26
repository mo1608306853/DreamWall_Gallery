# Copyright 2022 Dirk Moerenhout. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program. If not,
# see <https://www.gnu.org/licenses/>.

import os
import sys
import json
import numpy
from diffusers import OnnxStableDiffusionPipeline, OnnxRuntimeModel
from transformers import AutoTokenizer, pipeline

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'model')
index_model_path = os.path.join(model_path, 'Index_1_9B')
sd_model_path = os.path.join(model_path, 'chilloutmix-fp16')
text_path = os.path.join(BASE_DIR, 'text.json')

def run_stable_diffusion(model_path, imgname, prompt):
    VAECPU = TECPU = False
    try:
        height=512
        width=512
        num_inference_steps=30
        guidance_scale=7.5
        negative_prompt = 'low quality'
        generator=numpy.random
        if TECPU:
            cputextenc=OnnxRuntimeModel.from_pretrained(model_path+"/text_encoder")
            if VAECPU:
                cpuvae=OnnxRuntimeModel.from_pretrained(model_path+"/vae_decoder")
                pipe = OnnxStableDiffusionPipeline.from_pretrained(model_path,
                    provider="VitisAIExecutionProvider", text_encoder=cputextenc, vae_decoder=cpuvae,
                    vae_encoder=None)
            else:
                pipe = OnnxStableDiffusionPipeline.from_pretrained(model_path,
                    provider="VitisAIExecutionProvider", text_encoder=cputextenc)
        else:
            pipe = OnnxStableDiffusionPipeline.from_pretrained(model_path,
                    provider="VitisAIExecutionProvider")
        image = pipe(prompt, width, height, num_inference_steps, guidance_scale,
                            negative_prompt,generator=generator).images[0]
        image.save(imgname)
    except Exception as e:
        print(e)


# be careful! The directory cannot contain "." and can be replaced with "_"
# https://hf-mirror.com/IndexTeam/Index-1.9B/tree/main

def run_index(model_path, prompt_str, save_output=False):
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    generator = pipeline("text-generation", model=model_path,
                        tokenizer=tokenizer, trust_remote_code=True, 
                        device='cpu')
    model_output = generator(prompt_str, max_new_tokens=300, top_k=5, top_p=0.8,
                             temperature=0.3, repetition_penalty=1.1, do_sample=True)

    if save_output:
        data = model_output[0]['generated_text'].split(' ')
        new_list = [' '.join(data[i:i+3]) for i in range(0, len(data), 3)]  
        with open(text_path, 'w') as f:
            f.write(json.dumps(new_list))
    return model_output

def run_method(task_method, task_text):
    if task_method == 'text':
        run_index(index_model_path, task_text, True)
    elif task_method == 'image':
        imgname='sd_picture.png'
        draw_prompt = run_index(index_model_path, task_text)
        prompt = draw_prompt[0]['generated_text'].replace(task_text, '').replace('\n\n', '')
        print(prompt)
        run_stable_diffusion(sd_model_path, imgname, prompt)


if __name__ == "__main__":
    task_method = sys.argv[1]
    task_text = sys.argv[2:]
    run_method(task_method, ' '.join(task_text))
    # model_path = 'model\\chilloutmix-fp16'
    # imgname="testpicture"+".png"
    # prompt = 'The composition of the foreground with the soft focus of the budding flowers, a single flower, and the foreground in focus'
    # run_stable_diffusion(model_path, imgname, prompt)
    # model_path = 'model\\Index_1_9B'
    # run_index(model_path, 'what is transformer', True)