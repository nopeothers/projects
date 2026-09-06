-- Отчёт по безопасности

-- Найти все запросы с признаками атак
SELECT 
    id,
    url,
    classification,
    CASE 
        WHEN classification = 'SQLI' THEN 'КРИТИЧЕСКИЙ'
        WHEN classification = 'XSS' THEN 'ВЫСОКИЙ'
        WHEN classification = 'PHISHING' THEN 'ВЫСОКИЙ'
        ELSE 'НОРМАЛЬНЫЙ'
    END as risk_level
FROM requests
WHERE classification != 'NORMAL'
ORDER BY risk_level DESC;

-- Найти подозрительные URL с IP-адресами
SELECT id, url
FROM requests
WHERE url ~ '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+';

-- Найти запросы с кавычками (потенциальные SQLi)
SELECT id, url
FROM requests
WHERE text LIKE '%''%' 
   OR text LIKE '%"%"%';
