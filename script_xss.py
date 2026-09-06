#!/usr/bin/env python3
"""
XSS-атак детектор (с проверкой контекста)
"""

import re

class XSSDetector:
    def __init__(self):
        # Критические признаки (достаточно одного)
        self.critical_patterns = [
            r'<script', r'javascript:', r'<iframe',
            r'onerror=', r'onload=', r'onclick=',
            r'onmouseover=', r'eval\(', r'prompt\(', r'confirm\(',
        ]
        
        # Опасные теги (требуют обработчик или функцию)
        self.dangerous_tags = [r'<img', r'<body', r'<svg', r'<div']
        
        # Опасные функции (требуют тег или контекст)
        self.dangerous_functions = [r'alert\(', r'console\.log\(']
    
    def detect(self, text):
        if not text:
            return False
        
        text_lower = text.lower()
        
        # 1. Проверка критических признаков
        for pattern in self.critical_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return True
        
        # 2. Проверка опасных тегов
        for tag in self.dangerous_tags:
            if re.search(tag, text_lower, re.IGNORECASE):
                if re.search(r'on\w+\s*=', text_lower):
                    return True
                for func in self.dangerous_functions:
                    if re.search(func, text_lower, re.IGNORECASE):
                        return True
        
        # 3. Проверка опасных функций
        for func in self.dangerous_functions:
            if re.search(func, text_lower, re.IGNORECASE):
                for tag in self.dangerous_tags + [r'<script', r'javascript:']:
                    if re.search(tag, text_lower, re.IGNORECASE):
                        return True
                if re.search(r'on\w+\s*=', text_lower):
                    return True
        
        return False
