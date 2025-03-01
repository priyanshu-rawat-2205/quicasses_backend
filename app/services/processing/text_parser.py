from google import genai
from google.genai import types
from app.config import API_KEY
from app.services.processing.assessment_schema import Assessment

client = genai.Client(api_key=API_KEY)

def parse_assessment_text(text):
    """Sends extracted text to Gemini API for processing into structured JSON."""

    # prompt = """
    # Extract structured assessment data from the given text-content.

    # text-content = 
    # """

    prompt = """Extract structured assessment data from the given text-content"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",

            contents=[types.Part.from_bytes(data=text.read_bytes(), mime_type='application/pdf'), prompt],



            # contents=prompt + text,
            # config={
            #     'response_mime_type': 'application/json',
            #     'response_schema': Assessment,
            # }


            config=types.GenerateContentConfig(
                max_output_tokens=7000,
                temperature=0.1,
                response_schema=Assessment,
                response_mime_type='application/json',
            )
        )
        print(f"model: gemini-2.0-flash-lite, token limit: input: [1,048,576], output: [8,192] usage: {response.usage_metadata}")
        return response.text  # Assuming Gemini returns a JSON-formatted string
    except Exception as e:
        print("Error processing text with Gemini:", e)
        return None
