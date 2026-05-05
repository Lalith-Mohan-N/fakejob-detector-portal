import re


def sanitize_text(text: str, max_length: int = 10000) -> str:
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_length]
