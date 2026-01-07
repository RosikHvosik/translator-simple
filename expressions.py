# expressions.py
import re

def handle_operators(code: str) -> str:
    # Убираем ++ и -- (преобразуем в += 1 и -= 1)
    # Пре-инкремент: ++x -> x += 1
    code = re.sub(r'\+\+(\w+)', r'\1 += 1', code)
    # Пост-инкремент: x++ -> x += 1 (в Python порядок не важен в простых случаях)
    code = re.sub(r'(\w+)\+\+', r'\1 += 1', code)
    # Пре-декремент: --x -> x -= 1
    code = re.sub(r'--(\w+)', r'\1 -= 1', code)
    # Пост-декремент: x-- -> x -= 1
    code = re.sub(r'(\w+)--', r'\1 -= 1', code)
    
    # Логические операторы
    code = re.sub(r'\|\|', 'or', code)
    code = re.sub(r'&&', 'and', code)
    code = re.sub(r'!', 'not ', code)
    
    return code

def handle_pointers(code: str) -> str:
    # Убираем * из объявлений (уже обработано в declarations)
    # Обработка разыменования указателя: *ptr -> ptr (в Python нет указателей как в C)
    code = re.sub(r'\*\s*(\w+)', r'\1', code)
    
    # Обработка оператора адреса: &var -> var (в Python нет необходимости в адресах)
    code = re.sub(r'&(\w+)', r'\1', code)
    
    return code

def handle_arrays_and_pointers(code: str) -> str:
    # arr[i] уже в правильном формате для Python
    # Убираем лишние операции с указателями
    return code

def handle_assignment_operators(code: str) -> str:
    # +=, -=, *=, /=, %= уже в правильном формате
    # &=, |=, ^=, <<=, >>= также уже в правильном формате
    
    # Обработка простого присваивания (убираем ;)
    code = re.sub(r'([^=])=([^=])', r'\1 = \2', code)
    
    return code

def process_expressions(code: str) -> str:
    """Обработка всех выражений"""
    code = handle_assignment_operators(code)
    code = handle_pointers(code)
    code = handle_operators(code)
    code = handle_arrays_and_pointers(code)
    return code