from flask import Flask, request, render_template
from dotenv import load_dotenv
import os
from PIL import Image
import google.generativeai as genai

load_dotenv()  # Take environment variables from .env.

app = Flask(__name__)

# Ensure API key is set correctly
api_key = os.getenv("GOOGLE_API_KEY")
if api_key is None:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")
else:
    genai.configure(api_key=api_key)

## Function to load Google model and get responses
def get_gemini_response(input_text, image_path):
    model = genai.GenerativeModel('gemini-1.5-flash')
    with Image.open(image_path) as img:
        if input_text:
            response = model.generate_content([input_text, img])
        else:
            response = model.generate_content(img)
    return response.text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_text = request.form.get('input_text')
        image = request.files.get('image')
        if image:
            image_path = os.path.join('static', image.filename)
            image.save(image_path)
        else:
            image_path = ""
        
        if not input_text and not image_path:
            return render_template('index.html', error="Please provide a text prompt and/or upload an image.")
        
        response = get_gemini_response(input_text, image_path)
        return render_template('index.html', response=response, image_path=image_path)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)