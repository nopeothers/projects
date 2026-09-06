#!/usr/bin/env python3
"""
Главный классификатор
"""

import json
import sys
from sqli_detector import SQLiDetector
from xss_detector import XSSDetector
from phishing_detector import PhishingDetector

class Classifier:
    def __init__(self):
        self.sqli = SQLiDetector()
        self.xss = XSSDetector()
        self.phish = PhishingDetector()
    
    def classify(self, text):
        if self.phish.detect(text):
            return "PHISHING"
        elif self.sqli.detect(text):
            return "SQLI"
        elif self.xss.detect(text):
            return "XSS"
        else:
            return "NORMAL"

def main():
    if len(sys.argv) < 2:
        print("Использование: python3 classifier.py <input.json> [output.json]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    with open(input_file, 'r') as f:
        requests = json.load(f)
    
    classifier = Classifier()
    results = []
    stats = {"NORMAL": 0, "SQLI": 0, "XSS": 0, "PHISHING": 0}
    
    for req in requests:
        text = req.get('text', '')
        attack_type = classifier.classify(text)
        stats[attack_type] += 1
        results.append({
            'id': req.get('id'),
            'url': req.get('url'),
            'classification': attack_type
        })
    
    print("=" * 50)
    print("РЕЗУЛЬТАТЫ АНАЛИЗА")
    print("=" * 50)
    for r in results:
        print(f"ID {r['id']}: {r['classification']}")
        print(f"    {r['url'][:65]}")
    
    print("\n" + "-" * 50)
    print("СТАТИСТИКА:")
    print(f"  НОРМАЛЬНЫХ:     {stats['NORMAL']}")
    print(f"  SQL-ИНЪЕКЦИЙ:   {stats['SQLI']}")
    print(f"  XSS-АТАК:       {stats['XSS']}")
    print(f"  ФИШИНГ:         {stats['PHISHING']}")
    print("=" * 50)
    
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\nСохранено в: {output_file}")

if __name__ == "__main__":
    main()
