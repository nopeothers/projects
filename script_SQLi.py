#!/usr/bin/env python3
"""
SQL-инъекции детектор (смешанный подход + белый список)
"""

import re

class SQLiDetector:
    def __init__(self):
        # Белый список нормальных доменов
        self.whitelist_domains = [
            r'example\.com', r'google\.com', r'facebook\.com',
            r'yandex\.ru', r'mail\.ru', r'github\.com', r'localhost',
        ]
        
        # Сильные признаки (достаточно одного)
        self.strong_patterns = [
            r'\bSELECT\b', r'\bUNION\b', r'\bDROP\b',
            r'\bINSERT\b', r'\bDELETE\b', r'\bUPDATE\b',
            r'\bALTER\b', r'\bCREATE\b', r'\bEXEC\b',
            r'SLEEP\(', r'BENCHMARK\(', r'WAITFOR',
            r'--', r'#', r'/\*', r'\*/',
        ]
        
        # Слабые признаки (нужно 2+)
        self.weak_patterns = [
            r"'", r'"',
            r'1\s*=\s*1',
            r'OR\s+1\s*=\s*1', r'AND\s+1\s*=\s*1',
            r"'\s+OR\s+'", r"'\s+AND\s+'",
        ]
    
    def detect(self, text):
        if not text:
            return False
        
        text_lower = text.lower()
        
        # Проверка белого списка
        for domain in self.whitelist_domains:
            if re.search(domain, text_lower):
                return False
        
        # Проверка сильных признаков
        for pattern in self.strong_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return True
        
        # Проверка слабых признаков (нужно 2+)
        weak_count = 0
        for pattern in self.weak_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                weak_count += 1
        
        return weak_count >= 2
