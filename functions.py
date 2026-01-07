import re
from .types_mapper import map_type

def handle_function_declarations(code: str) -> str:
    """Обработка объявлений функций"""
    # Регулярное выражение для поиска функций
    # int func(int x, float y) {
    pattern = r'(\w+(?:\s+\w+)*)\s+(\w+)\s*\(([^)]*)\)\s*\{'
    
    def replace_function(match):
        return_type_with_qualifiers = match.group(1).strip()
        func_name = match.group(2)
        params = match.group(3).strip()
        
        # Очищаем возвращаемый тип от служебных слов
        clean_return_type = return_type_with_qualifiers.replace('void', '').replace('static', '').replace('inline', '').strip()
        if not clean_return_type:
            clean_return_type = 'void'
        
        # Обрабатываем параметры
        python_params = []
        if params and params != 'void':
            param_list = [p.strip() for p in params.split(',')]
            for param in param_list:
                if param:
                    param_parts = param.split()
                    if len(param_parts) >= 2:
                        param_type = ' '.join(param_parts[:-1])
                        param_name = param_parts[-1].replace('*', '')
                        python_params.append(param_name)
                    else:
                        # Если формат странный, просто берем последнюю часть
                        python_params.append(param_parts[-1].replace('*', ''))
        
        params_str = ', '.join(python_params)
        if func_name == 'main':
            # Для main функции добавляем if __name__ == "__main__":
            return f'def {func_name}({params_str}):'
        else:
            return f'def {func_name}({params_str}):'
    
    code = re.sub(pattern, replace_function, code)
    
    return code

def handle_function_calls(code: str) -> str:
    # Простая замена - в большинстве случаев вызовы функций одинаковы
    # Но нужно учитывать специфичные C функции
    replacements = {
        r'printf\s*\(': 'print(',
        r'scanf\s*\(': '# scanf equivalent not directly available in Python',
        r'gets\s*\(': '# gets is unsafe, use input()',
        r'puts\s*\(': 'print(',
        r'getchar\s*\(\)': 'input()[0] if input() else None',
        r'putchar\s*\(': 'print(',
    }
    
    for old, new in replacements.items():
        code = re.sub(old, new, code)
    
    return code

def process_functions(code: str) -> str:
    """Обработка всех функций"""
    code = handle_function_calls(code)
    code = handle_function_declarations(code)
    return code