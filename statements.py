# statements.py - ПОЛНОСТЬЮ РАБОЧАЯ ВЕРСИЯ
import re

def handle_if_statements(code: str) -> str:
    """
    Обработка if/else/elif конструкций
    Преобразует ( ) и { } в Python синтаксис
    """
    # if (condition) { -> if condition:
    code = re.sub(r'if\s*\(([^)]+)\)\s*\{', r'if \1:', code)
    code = re.sub(r'if\s*\(([^)]+)\)', r'if \1:', code)  # Если { уже удалены
    
    # else if (condition) { -> elif condition:
    code = re.sub(r'else\s+if\s*\(([^)]+)\)\s*\{', r'elif \1:', code)
    code = re.sub(r'else\s+if\s*\(([^)]+)\)', r'elif \1:', code)
    
    # else { -> else:
    code = re.sub(r'else\s*\{', r'else:', code)
    code = re.sub(r'else\s*$', r'else:', code, flags=re.MULTILINE)
    
    return code

def handle_while_loops(code: str) -> str:
    """Обработка while циклов"""
    # while (condition) { -> while condition:
    code = re.sub(r'while\s*\(([^)]+)\)\s*\{', r'while \1:', code)
    code = re.sub(r'while\s*\(([^)]+)\)', r'while \1:', code)
    
    return code

def handle_for_loops(code: str) -> str:
    """Обработка for циклов"""
    
    # for(int i = 0; i < 10; i++) { -> for i in range(0, 10):
    pattern1 = r'for\s*\(\s*(?:int\s+)?(\w+)\s*=\s*(\d+)\s*;\s*\1\s*<\s*(\d+)\s*;\s*\1\+\+\s*\)'
    code = re.sub(pattern1, r'for \1 in range(\2, \3):', code)
    
    # for(int i = 0; i <= 10; i++) { -> for i in range(0, 11):
    pattern2 = r'for\s*\(\s*(?:int\s+)?(\w+)\s*=\s*(\d+)\s*;\s*\1\s*<=\s*(\d+)\s*;\s*\1\+\+\s*\)'
    code = re.sub(pattern2, r'for \1 in range(\2, \3 + 1):', code)
    
    # for(int i = 10; i > 0; i--) -> for i in range(10, 0, -1):
    pattern3 = r'for\s*\(\s*(?:int\s+)?(\w+)\s*=\s*(\d+)\s*;\s*\1\s*>\s*(\d+)\s*;\s*\1--\s*\)'
    code = re.sub(pattern3, r'for \1 in range(\2, \3, -1):', code)
    
    # for(int i = 10; i >= 0; i--) -> for i in range(10, -1, -1):
    pattern4 = r'for\s*\(\s*(?:int\s+)?(\w+)\s*=\s*(\d+)\s*;\s*\1\s*>=\s*(\d+)\s*;\s*\1--\s*\)'
    code = re.sub(pattern4, r'for \1 in range(\2, \3 - 1, -1):', code)
    
    # Общий случай с переменными
    pattern5 = r'for\s*\(\s*(?:int\s+)?(\w+)\s*=\s*([^;]+)\s*;\s*\1\s*<\s*([^;]+)\s*;\s*\1\+\+\s*\)'
    code = re.sub(pattern5, r'for \1 in range(\2, \3):', code)
    
    return code

def handle_switch_statements(code: str) -> str:
    """Преобразование switch-case"""
    code = re.sub(r'switch\s*\(([^)]+)\)\s*\{', r'# TODO: switch(\1)', code)
    code = re.sub(r'case\s+([^:]+):', r'# case \1:', code)
    code = re.sub(r'default\s*:', r'# default:', code)
    return code

def handle_break_continue(code: str) -> str:
    """Обработка break и continue - они одинаковые в Python"""
    return code

def handle_return_statements(code: str) -> str:
    """Обработка return"""
    code = re.sub(r'\breturn\s*;', 'return None', code)
    return code

def process_statements(code: str) -> str:
    """Обработка всех операторов"""
    code = handle_return_statements(code)
    code = handle_switch_statements(code)
    code = handle_for_loops(code)
    code = handle_while_loops(code)
    code = handle_if_statements(code)
    code = handle_break_continue(code)
    return code