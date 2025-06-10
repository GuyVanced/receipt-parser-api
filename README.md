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
git clone https://github.com/yourusername/receipt-parser-api.git
cd receipt-parser-api


