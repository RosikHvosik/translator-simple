# expressions.py - ПОЛНОСТЬЮ ИСПРАВЛЕННАЯ ВЕРСИЯ
import re

def handle_struct_pointer_access(code: str) -> str:
    code = re.sub(r'(\w+)->(\w+)', r'\1.\2', code)
    return code

def handle_operators(code: str) -> str:
    
    # Инкремент и декремент
    # i++ -> i += 1
    code = re.sub(r'(\w+)\+\+', r'\1 += 1', code)
    # ++i -> i += 1
    code = re.sub(r'\+\+(\w+)', r'\1 += 1', code)
    # i-- -> i -= 1
    code = re.sub(r'(\w+)--', r'\1 -= 1', code)
    # --i -> i -= 1
    code = re.sub(r'--(\w+)', r'\1 -= 1', code)
    
    # Логические операторы
    code = re.sub(r'\|\|', ' or ', code)
    code = re.sub(r'&&', ' and ', code)
    
    # Логическое отрицание: ! -> not
    # Но нужно быть осторожным с != 
    code = re.sub(r'!(\w+)', r'not \1', code)
    code = re.sub(r'!\(([^)]+)\)', r'not (\1)', code)
    
    return code

def handle_pointers(code: str) -> str:
    # Взятие адреса: &var -> var
    code = re.sub(r'&(\w+)', r'\1', code)
    
    # Разыменование в присваивании: *ptr = value -> ptr = value
    code = re.sub(r'\*(\w+)\s*=', r'\1 =', code)
    
    # НЕ трогаем * в других контекстах (умножение, объявления типов)
    
    return code

def handle_null(code: str) -> str:
    code = re.sub(r'\bNULL\b', 'None', code)
    return code

def normalize_spacing(code: str) -> str:
    # Пробелы вокруг = (но не ==, !=, <=, >=)
    code = re.sub(r'([^=!<>])=([^=])', r'\1 = \2', code)
    
    # Пробелы вокруг операторов сравнения
    code = re.sub(r'([^=!<>])(<|>)([^=])', r'\1 \2 \3', code)
    
    # Убираем лишние пробелы
    code = re.sub(r'\s+', ' ', code)
    
    return code

def process_expressions(code: str) -> str:
    # 1. СНАЧАЛА struct pointer access (до обработки указателей)
    code = handle_struct_pointer_access(code)
    
    # 2. Потом NULL
    code = handle_null(code)
    
    # 3. Потом указатели
    code = handle_pointers(code)
    
    # 4. Потом операторы
    code = handle_operators(code)
    
    # 5. Нормализация в конце
    # code = normalize_spacing(code)  # Осторожно - может сломать строки
    
    return code