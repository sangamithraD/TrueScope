import re
import hashlib
from langdetect import detect, DetectorFactory
from googletrans import Translator

DetectorFactory.seed = 0
translator = Translator()

def detect_language(text):
    try:
        return detect(text)
    except Exception:
        return "en"

def translate_text(text, dest):
    try:
        if not text:
            return ""
        res = translator.translate(text, dest=dest)
        return res.text
    except Exception:
        # fallback: return original english if translation fails
        return text

def normalize_text_for_hash(text):
    # lowercase, remove punctuation, collapse whitespace
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()

def content_hash(title_en, content_en):
    canonical = (normalize_text_for_hash(title_en) + " " + normalize_text_for_hash(content_en)).strip()
    return hashlib.sha256(canonical.encode('utf-8')).hexdigest()
