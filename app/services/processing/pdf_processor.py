# import pdfplumber
# from app.services.processing.text_parser import parse_assessment_text

# def process_pdf(pdf_path):
#     """Extracts text from a PDF and returns structured JSON."""
#     extracted_text = []

#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             extracted_text.append(page.extract_text())

#     text = "\n".join(extracted_text)
#     return parse_assessment_text(text)

# import fitz  # PyMuPDF (faster alternative to pdfplumber)
# from concurrent.futures import ProcessPoolExecutor
# from app.services.processing.text_parser import parse_assessment_text

# def extract_page_text(args):
#     """Extracts text from a single page by reopening the PDF inside the worker process."""
#     pdf_path, page_number = args
#     with fitz.open(pdf_path) as pdf:
#         return pdf[page_number].get_text("text")

# def process_pdf(pdf_path):
#     """Extracts text from a PDF using multiprocessing and returns structured JSON."""
#     with fitz.open(pdf_path) as pdf:
#         num_pages = len(pdf)

#     with ProcessPoolExecutor() as executor:
#         extracted_text = list(executor.map(extract_page_text, [(pdf_path, i) for i in range(num_pages)]))

#     text = "\n".join(extracted_text)
#     print(text)
#     return parse_assessment_text(text)

import pathlib
from google import genai
from google.genai import types
from app.config import API_KEY
from app.services.processing.assessment_schema import Assessment

client = genai.Client(api_key=API_KEY)


def process_pdf(pdf_path):
    """Extracts text from a PDF and returns structured JSON."""

    filepath = pathlib.Path(pdf_path)

    prompt = """Extract structured assessment data from the given file"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",

            contents=[types.Part.from_bytes(data=filepath.read_bytes(), mime_type='application/pdf'), prompt],

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
