import requests

def generate_image_url(prompt):
    api_url = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
    headers = {"Authorization": f"Bearer YOUR_HUGGINGFACE_API_TOKEN"}
    response = requests.post(api_url, headers=headers, json={"inputs": prompt})
    if response.status_code == 200:
        return response.json()[0]["generated_image"]
    else:
        return "https://via.placeholder.com/512?text=Image+Not+Generated"