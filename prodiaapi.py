import requests

import os 
import dotenv
import concurrent.futures
import time

dotenv.load_dotenv()

apikey=str(os.getenv('apikey'))


def get_models():
    url = "https://api.prodia.com/v1/models/list"

    headers = {
        "accept": "application/json",
        "X-Prodia-Key": f"{apikey}"
    }

    response = requests.get(url, headers=headers)

    return response.text


def gen(positive_prompt,aspect_ratio,sampler,scale,steps,negativeprompt,model):

    url = "https://api.prodia.com/v1/sd/generate"

    headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "X-Prodia-Key": f"{apikey}"
    }
    
    payload = {
        "prompt": positive_prompt,
        "model": model,
        "negative_prompt": negativeprompt,
        "steps": steps,
        "cfg_scale": scale,
        "seed": -1,
        "upscale": False,
        "sampler": sampler,
        "aspect_ratio": aspect_ratio
}
    
    response = requests.post(url,json=payload, headers=headers)
    if response.status_code == 200:

        resp=response.json()
        return response.status_code,resp['job'],resp['status']
    else:
        return response.status_code,response.text
    

def checkjobstatus(jobid):
    Generated =False
    iterationno=0
    while Generated ==False :
    

        url = f"https://api.prodia.com/v1/job/{jobid}"

        headers = {
        "accept": "application/json",
        "X-Prodia-Key": apikey
        }

        response = requests.get(url, headers=headers)

        resp=response.json()
        if 'imageUrl' in response.text:
            Generated=True
            return response.status_code,resp['imageUrl']
            
            
        elif response.status_code != 200 :
            print(response.text)
            Generated = False
            return "Internal Issue : Job status code isnt 200 "
        else :
            Generated = False
            time.sleep(0.5)
            iterationno+=1
            
    
    


    
    
if __name__ == "__main__":
    print()
    # models = get_models()
    genner=gen("a cute dog ","portrait","DPM++ 2M Karras",7,20,"bad quality","v1-5-pruned-emaonly.ckpt [81761151]")
    if genner[0] == 200:
        print(f'Generation successfull JOB ID: {genner[1]} \nStatus : {genner[2]}')
    else:
        print(genner[1])
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(checkjobstatus, genner[1])
        return_value = future.result()
        print(return_value)