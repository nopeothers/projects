#!/usr/bin/env python3
import json
import sys
import re
from urllib.parse import unquote

# СПИСОК СТАТИЧЕСКИХ РАСШИРЕНИЙ
STATIC_PATTERNS = [
    r'\.css(\?|$)', r'\.js(\?|$)', r'\.png(\?|$)',
    r'\.jpg(\?|$)', r'\.jpeg(\?|$)', r'\.gif(\?|$)',
    r'\.ico(\?|$)', r'\.svg(\?|$)', r'\.woff(\?|$)',
    r'favicon\.ico',
]

def is_static(url):
    if not url:
        return False
    url_lower = url.lower()
    for pattern in STATIC_PATTERNS:
        if re.search(pattern, url_lower):
            return True
    return False

def normalize_text(text):
    if not text:
        return ""
    text = unquote(text)
    text = text.lower()
    return text.strip()

input_file = sys.argv[1]
output_file = sys.argv[2] if len(sys.argv) > 2 else None

results = []
static_count = 0
dynamic_count = 0

with open(input_file, 'r') as f:
    for line in f:
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except:
            continue
        
        if event.get('event_type') != 'http':
            continue
        
        http_data = event.get('http', {})
        url = http_data.get('url', '')
        
        # ФИЛЬТРАЦИЯ СТАТИКИ
        if is_static(url):
            static_count += 1
            print(f"[УДАЛЕН] {url}")
        else:
            dynamic_count += 1
            text = normalize_text(url)
            results.append({
                'id': len(results) + 1,
                'url': url,
                'text': text
            })
            print(f"[ОСТАВЛЕН] {url}")

print(f"\nСтатических: {static_count}")
print(f"Динамических: {dynamic_count}")

if output_file:
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nСохранено в {output_file}")
