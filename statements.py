# statements.py - ИСПРАВЛЕННАЯ ВЕРСИЯ
import re

def handle_if_statements(code: str) -> str:
    """Обработка if/else/elif конструкций"""
    # if (condition) { на if condition:
    code = re.sub(r'if\s*\(([^)]+)\)\s*\{', r'if \1:', code)
    
    # else if (condition) { на elif condition:
    code = re.sub(r'else\s+if\s*\(([^)]+)\)\s*\{', r'elif \1:', code)
    
    # else { на else:
    code = re.sub(r'else\s*\{', r'else:', code)
    
    return code

def handle_while_loops(code: str) -> str:
    """Обработка while циклов"""
    # while (condition) { на while condition:
    code = re.sub(r'while\s*\(([^)]+)\)\s*\{', r'while \1:', code)
    
    return code

def handle_for_loops(code: str) -> str:
    """Обработка for циклов"""
    
    # Классический for: for(int i = 0; i < 10; i++) или for(i = 0; i < 10; i++)
    pattern1 = r'for\s*\(\s*(?:int\s+)?(\w+)\s*=\s*(\d+)\s*;\s*\1\s*<\s*(\d+)\s*;\s*\1\+\+\s*\)\s*\{'
    code = re.sub(pattern1, r'for \1 in range(\2, \3):', code)
    
    # for с <=
    pattern2 = r'for\s*\(\s*(?:int\s+)?(\w+)\s*=\s*(\d+)\s*;\s*\1\s*<=\s*(\d+)\s*;\s*\1\+\+\s*\)\s*\{'
    code = re.sub(pattern2, r'for \1 in range(\2, \3 + 1):', code)
    
    # for с декрементом: for(int i = 10; i > 0; i--)
    pattern3 = r'for\s*\(\s*(?:int\s+)?(\w+)\s*=\s*(\d+)\s*;\s*\1\s*>\s*(\d+)\s*;\s*\1--\s*\)\s*\{'
    code = re.sub(pattern3, r'for \1 in range(\2, \3, -1):', code)
    
    # for с >=
    pattern4 = r'for\s*\(\s*(?:int\s+)?(\w+)\s*=\s*(\d+)\s*;\s*\1\s*>=\s*(\d+)\s*;\s*\1--\s*\)\s*\{'
    code = re.sub(pattern4, r'for \1 in range(\2, \3 - 1, -1):', code)
    
    # Более общий случай с переменными вместо чисел
    pattern5 = r'for\s*\(\s*(?:int\s+)?(\w+)\s*=\s*([^;]+)\s*;\s*\1\s*<\s*([^;]+)\s*;\s*\1\+\+\s*\)\s*\{'
    code = re.sub(pattern5, r'for \1 in range(\2, \3):', code)
    
    return code

def handle_switch_statements(code: str) -> str:
    """
    Преобразование switch-case в if-elif
    В Python нет switch, используем if-elif
    """
    # Упрощенная версия - для полной поддержки нужен парсер
    # Пока просто помечаем как TODO
    code = re.sub(r'switch\s*\(([^)]+)\)\s*\{', r'# TODO: switch(\1) - convert to if-elif', code)
    code = re.sub(r'case\s+([^:]+):', r'# case \1:', code)
    code = re.sub(r'default\s*:', r'# default:', code)
    
    return code

def handle_break_continue(code: str) -> str:
    """Обработка break и continue"""
    # В Python они такие же, просто убираем точки с запятой
    # Но точки с запятой убираются позже в _handle_syntax
    return code

def handle_return_statements(code: str) -> str:
    """Обработка return"""
    # return value; -> return value (точка с запятой уберется позже)
    # return; -> return None
    code = re.sub(r'\breturn\s*;', 'return None;', code)
    return code

def process_statements(code: str) -> str:
    """Обработка всех операторов в правильном порядке"""
    code = handle_return_statements(code)
    code = handle_switch_statements(code)
    code = handle_for_loops(code)
    code = handle_while_loops(code)
    code = handle_if_statements(code)
    code = handle_break_continue(code)
    return code