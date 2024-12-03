
import base64
import json
import requests
import time

def convert_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string.decode('utf-8')

human_image_b64 = convert_image_to_base64("./human.webp")
garment_image_b64 = convert_image_to_base64("./garment.webp")

catvton_path = "path/to/catvton"
cloth_type = "Tshirt"
steps = 30
cfg = 2.0
seed = 42
mixed_precision = "fp16"
sd15_inpaint_path = "path/to/sd15_inpaint"

payload = json.dumps({
    "input": {
        "human_image_b64": human_image_b64,
        "garment_image_b64": garment_image_b64,
        "catvton_path": catvton_path,
        "cloth_type": cloth_type,
        "steps": steps,
        "cfg": cfg,
        "seed": seed,
        "mixed_precision": mixed_precision,
        "sd15_inpaint_path": sd15_inpaint_path,
    }
})

start = time.time()

endpoint_url = "http://127.0.0.1:8188"
headers = {
    'content-type': 'application/json',
}

response = requests.request(
    "POST", f"{endpoint_url}/run", headers=headers, data=payload)

data = response.json()

job_id = data["id"]
job_finished = False
result = None

while not job_finished:
    time.sleep(1)
    response = requests.request(
        "GET", f"{endpoint_url}/status/{job_id}", headers=headers)
    result = response.json()

    job_finished = result["status"] == "COMPLETED"

base64_image = result['output']['payload']['result']
image_data = base64.b64decode(base64_image)

end = time.time()

with open("result.png", "wb") as f:
    f.write(image_data)

print("Total time taken (sec):", end-start)