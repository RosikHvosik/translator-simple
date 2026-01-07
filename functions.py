# functions.py - ИСПРАВЛЕННАЯ ВЕРСИЯ
import re
from typing import List, Tuple

def handle_function_declarations(code: str) -> str:
    """Обработка объявлений функций"""
    pattern = r'(\w+(?:\s+\w+)*)\s+(\w+)\s*\(([^)]*)\)\s*\{'
    
    def replace_function(match):
        return_type_with_qualifiers = match.group(1).strip()
        func_name = match.group(2)
        params = match.group(3).strip()
        
        # Обрабатываем параметры
        python_params = []
        if params and params != 'void':
            param_list = [p.strip() for p in params.split(',')]
            for param in param_list:
                if param:
                    param_parts = param.split()
                    if len(param_parts) >= 2:
                        param_name = param_parts[-1].replace('*', '').replace('[', '').replace(']', '')
                        python_params.append(param_name)
                    else:
                        python_params.append(param_parts[-1].replace('*', ''))
        
        params_str = ', '.join(python_params)
        return f'def {func_name}({params_str}):'
    
    code = re.sub(pattern, replace_function, code)
    return code

def parse_printf_format(format_str: str, args: List[str]) -> str:
    """
    Конвертирует printf("format", args) в f-строку Python
    НОВАЯ ФУНКЦИЯ для улучшенной обработки
    """
    # Убираем кавычки
    fmt = format_str.strip('"')
    
    # Находим все спецификаторы формата
    specifiers = re.findall(r'%[-#+ 0]?[*]?(?:\d+|\*)?(?:\.(?:\d+|\*))?[hlL]?[diouxXeEfFgGaAcspn%]', fmt)
    
    if not specifiers or not args:
        # Нет спецификаторов - простая строка
        return format_str
    
    # Заменяем спецификаторы на {arg}
    result = fmt
    arg_idx = 0
    
    replacements = {
        r'%d': '{}',
        r'%i': '{}',
        r'%u': '{}',
        r'%f': '{:.2f}',
        r'%lf': '{:.2f}',
        r'%s': '{}',
        r'%c': '{}',
        r'%x': '{:x}',
        r'%X': '{:X}',
        r'%o': '{:o}',
        r'%%': '%',
    }
    
    # Простая замена (можно улучшить)
    for spec in specifiers:
        if spec == '%%':
            result = result.replace('%%', '%', 1)
        elif arg_idx < len(args):
            # Находим подходящую замену
            for pattern, repl in replacements.items():
                if re.match(pattern, spec):
                    result = result.replace(spec, f'{{{args[arg_idx]}}}', 1)
                    arg_idx += 1
                    break
    
    return f'f"{result}"'

def handle_function_calls(code: str) -> str:
    """Обработка вызовов функций с улучшенной поддержкой printf"""
    
    # УЛУЧШЕННАЯ обработка printf
    printf_pattern = r'printf\s*\(\s*("(?:[^"\\]|\\.)*")(?:\s*,\s*([^)]+))?\s*\)'
    
    def replace_printf(match):
        format_str = match.group(1)
        args_str = match.group(2)
        
        if not args_str:
            # printf("text") → print("text")
            # Заменяем \n на реальный перенос или оставляем
            return f'print({format_str})'
        else:
            # printf("format", args) → print(f"format".format(args))
            args = [arg.strip() for arg in args_str.split(',')]
            f_string = parse_printf_format(format_str, args)
            return f'print({f_string})'
    
    code = re.sub(printf_pattern, replace_printf, code)
    
    # Другие стандартные функции C
    replacements = {
        r'scanf\s*\(': '# scanf - use input(): ',
        r'gets\s*\(': 'input(',
        r'puts\s*\(': 'print(',
        r'strlen\s*\(': 'len(',
        r'malloc\s*\(': '# malloc - use list or dict: ',
        r'free\s*\(': '# free - automatic in Python: ',
        r'sizeof\s*\(': '# sizeof - use sys.getsizeof(): ',
    }
    
    for old, new in replacements.items():
        code = re.sub(old, new, code)
    
    return code

def handle_return_statements(code: str) -> str:
    """Обработка return с типами"""
    # return уже корректен в Python, но убираем ;
    code = re.sub(r'return\s+([^;]+);', r'return \1', code)
    code = re.sub(r'return\s*;', r'return None', code)
    return code

def process_functions(code: str) -> str:
    """Обработка всех функций"""
    code = handle_function_calls(code)
    code = handle_return_statements(code)
    code = handle_function_declarations(code)
    return code