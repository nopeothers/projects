#!/usr/bin/env python3
"""
Фишинг детектор
"""

import re

class PhishingDetector:
    def __init__(self):
        # Белый список нормальных доменов
        self.whitelist = [
            r'example\.com', r'google\.com', r'facebook\.com',
            r'yandex\.ru', r'mail\.ru', r'github\.com', r'localhost',
        ]
        
        # Высокодоверительные (достаточно одного)
        self.high_confidence = [
            r'g00gle', r'go0gle', r'faceb00k', r'facebok',
            r'sber-secure', r'\d+\.\d+\.\d+\.\d+',
        ]
        
        # Низкодоверительные (нужно 2)
        self.low_confidence = [
            r'\.tk', r'\.ml', r'\.cf', r'\.ga', r'\.xyz', r'\.top',
            r'login', r'verify', r'secure', r'confirm',
            r'update', r'password', r'signin', r'auth',
        ]
    
    def detect(self, text):
        if not text:
            return False
        text_lower = text.lower()
        
        # Проверка белого списка
        for domain in self.whitelist:
            if re.search(domain, text_lower):
                return False
        
        # Проверка высокодоверительных признаков
        for pattern in self.high_confidence:
            if re.search(pattern, text_lower):
                return True
        
        # Проверка комбинации низкодоверительных признаков
        low_count = 0
        for pattern in self.low_confidence:
            if re.search(pattern, text_lower):
                low_count += 1
        
        return low_count >= 2
