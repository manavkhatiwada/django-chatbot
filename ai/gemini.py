import google.generativeai as genai 
from django.conf import settings


genai.configure(
    api_key=settings.GEMINI_API_KEY
)

# Get the actual available models from the API
def get_available_model():
    try:
        models = genai.list_models()
        # Find a model that supports generateContent
        for m in models:
            if "generateContent" in m.supported_generation_methods:
                print(f"Using model: {m.name}")
                return genai.GenerativeModel(m.name)
    except Exception as e:
        print(f"Error listing models: {e}")
    
    raise Exception("No compatible generative model found. Check your API key and permissions.")

model = get_available_model()

def generate_ai_response(prompt):
    response = model.generate_content(prompt)
    return response.text