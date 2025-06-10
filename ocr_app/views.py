import os
import json
import google.generativeai as genai
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import ReceiptSerializer

# Configure Gemini
genai.configure(api_key=os.getenv('gemini_api_key'))

def clean_markdown_fences(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```json"):
        lines = stripped.splitlines()
        lines = [ln for ln in lines if ln.strip() not in ("```json", "```")]
        return "\n".join(lines).strip()
    if stripped.startswith("```"):
        stripped = stripped.lstrip("```").strip()
    if stripped.endswith("```"):
        stripped = stripped.rstrip("```").strip()
    return stripped

def parse_receipt_with_gemini(image_bytes: bytes, mime_type: str, prompt: str) -> dict:
    model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")
    multimodal_input = [prompt, {"mime_type": mime_type, "data": image_bytes}]
    response = model.generate_content(multimodal_input)
    cleaned = clean_markdown_fences(response.text)
    return json.loads(cleaned)

class ReceiptUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    PROMPT = """
You are a JSON-output-only receipt-parsing assistant. You will Output only the JSON object. You do not print any other text.
Given the receipt image below, output a JSON object with these keys:
{
    "merchant": "string"
    "date": "YYYY-MM-DD"
    "items": [{"name" : "string", "quantity" : "number", "unit_price" : "number", "total : "number"}]
    "total": "number"
    "category": "string"
    "accuracy" : "number"
}
"accuracy" is to be calculated using (total correctly identified)/ (total no. of fields)* 100. Derive accuracy based on given rules. 
Rules : 
(1)The identification of the values for the field(keys) should be done with confidence. (1)If any field is missing or can't be identified confidently, use `null` or an empty list. (3)Based on the receipt data, predict which one(1) of the allowed categories the bill falls under and put that in the 'category' key if confidently identified.
(4)Allowed Categories : ["Food", "Income", "Housing", "Groceries", "Electronics", "Transportation", "Dining", "Healthcare", "Shopping", "Entertainment", "Utilities", "Other"] (5) null / missing will affect accuracy.
(5)Do NOT output any text other than the final JSON object.
"""

    def post(self, request, *args, **kwargs):
        if 'image' not in request.data:
            return Response(
                {"error": "No image provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        image_file = request.data['image']
        try:
            data = image_file.read()
            mime = image_file.content_type
            parsed = parse_receipt_with_gemini(data, mime, self.PROMPT)
            
            # Create a serializer instance with the parsed data
            serializer = ReceiptSerializer(data=parsed)
            if serializer.is_valid():
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Invalid data format from OCR", "details": serializer.errors},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
                
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )