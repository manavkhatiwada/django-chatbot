from langchain_google_genai import GoogleGenerativeAI
from django.conf import settings


embeddings = GoogleGenerativeAI(
    model = 'models/embedding-001',
    google_api_key = settings.GEMINI_API_KEY
)