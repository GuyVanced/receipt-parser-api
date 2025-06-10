# Receipt Parser API with Django & Gemini AI

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Django](https://img.shields.io/badge/django-4.2+-green.svg)
![Gemini](https://img.shields.io/badge/google__generativeai-0.1.0+-orange.svg)

A REST API that extracts structured data from receipt images using Google's Gemini AI for OCR processing.

## Features

- 🖼️ Image processing for receipts in JPG/PNG formats
- 🔍 Extracts merchant, date, line items, totals, and categories
- 📊 Calculates OCR confidence score (accuracy)
- 🔄 Returns clean JSON responses
- 🔒 Secure API endpoint with CSRF protection

## Prerequisites

- Python 3.9+
- Google Gemini API key
- Django 4.2+

## Setup

### 1. Clone Repository
```bash
git clone https://github.com/GuyVanced/receipt-parser-api.git
cd receipt-parser-api
```

### 2. Configure Environment

* Create a **.env** file
        
    **or**

* Copy from existing example file
```bash
cp .env.example .env
```
* Edit `.env`
```env
gemini_api_key = your_gemini_key
```

### 3. Install Dependencies

* Create a virtual environment
```bash
python -m venv venv
```

* Activate the virtual environment
```bash
venv\Scripts\activate #Windows
source venv/bin/activate # mac or Linux
```

* Install the requirements
```shell
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Start Development Server

```bash
python manage.py runserver
```

API will be available at `http://127.0.0.1/receipt/api`

# API Documentation

## Endpoint

`POST /receipt/api/`

## Request

```bash
curl -X POST -F "image=@receipt.jpg" http://127.0.0.1:8000/receipt/api/
```

* 'curl.exe ' instead of 'curl' in Windows Powershell

## Sample Response

```json
{
  "merchant": "Walmart",
  "date": "2023-11-15",
  "items": [
    {
      "name": "Organic Milk",
      "quantity": 1,
      "unit_price": 3.99,
      "total": 3.99
    }
  ],
  "total": 42.36,
  "category": "Groceries",
  "accuracy": 95.7
}
```

## Testing with Postman

1. Set request type to `POST`
    
2. URL: `http://127.0.0.1:8000/receipt/api/`
    
3. Body → form-data → Add key `image` (File type)
    
4. Select receipt image
    
5. Send request

## Troubleshooting

|Error|Solution|
|---|---|
|400 Bad Request|Verify image is attached with key `image`|
|500 Server Error|Check Gemini API key in `.env`|
|Invalid JSON|Review receipt image quality|
