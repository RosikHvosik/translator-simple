# statements.py
import re

def handle_if_statements(code: str) -> str:
    # Заменяем if (condition) { на if condition:
    code = re.sub(r'if\s*\((.*?)\)\s*\{', r'if \1:', code)
    
    # Заменяем else { на else:
    code = re.sub(r'else\s*\{', r'else:', code)
    
    # Заменяем else if { на elif:
    code = re.sub(r'else\s+if\s*\((.*?)\)\s*\{', r'elif \1:', code)
    
    return code

def handle_while_loops(code: str) -> str:
    # Заменяем while (condition) { на while condition:
    code = re.sub(r'while\s*\((.*?)\)\s*\{', r'while \1:', code)
    
    return code

def handle_for_loops(code: str) -> str:
    # Обработка классических for циклов: for(int i = 0; i < 10; i++)
    for_pattern = r'for\s*\(\s*(?:\w+\s+)?(\w+)\s*=\s*([^;]+);\s*(\w+)\s*<\s*([^;]+);\s*(\w+)\+\+\s*\)\s*\{'
    def replace_classic_for(match):
        var = match.group(1)
        start = match.group(2)
        cond_var = match.group(3)
        end = match.group(4)
        
        if var == cond_var and match.group(5) == var:
            return f'for {var} in range({start}, {end}):'
    
    code = re.sub(for_pattern, replace_classic_for, code)
    
    # Обработка for с декрементом
    for_dec_pattern = r'for\s*\(\s*(?:\w+\s+)?(\w+)\s*=\s*([^;]+);\s*(\w+)\s*>\s*([^;]+);\s*(\w+)--\s*\)\s*\{'
    def replace_dec_for(match):
        var = match.group(1)
        start = match.group(2)
        cond_var = match.group(3)
        end = match.group(4)
        
        if var == cond_var and match.group(5) == var:
            return f'for {var} in range({start}, {end}, -1):'
    
    code = re.sub(for_dec_pattern, replace_dec_for, code)
    
    # Обработка других for вариантов
    general_for_pattern = r'for\s*\(\s*(?:\w+\s+)?(\w+)\s*=\s*([^;]+);\s*(\w+)\s*([<>=!]+)\s*([^;]+);\s*(\w+)([-+]+)([+-]?)\s*\)\s*\{'
    def replace_general_for(match):
        var = match.group(1)
        start = match.group(2)
        cond_var = match.group(3)
        op = match.group(4)
        end = match.group(5)
        inc_var = match.group(6)
        inc_op = match.group(7)
        inc_val = match.group(8) if match.group(8) else '1'
        
        if var == cond_var == inc_var:
            if op == '<' and inc_op == '++':
                return f'for {var} in range({start}, {end}):'
            elif op == '<=' and inc_op == '++':
                return f'for {var} in range({start}, {end} + 1):'
            elif op == '>' and inc_op == '--':
                return f'for {var} in range({start}, {end}, -1):'
            elif op == '>=' and inc_op == '--':
                return f'for {var} in range({start}, {end} - 1, -1):'
        
        # Если не можем конвертировать в range, оставляем как комментарий
        return f'# for loop: {var}={start}; {cond_var}{op}{end}; {inc_var}{inc_op}{inc_val}'
    
    code = re.sub(general_for_pattern, replace_general_for, code)
    
    return code

def handle_switch_statements(code: str) -> str:
    # В Python нет switch-case, преобразуем в if-elif
    switch_pattern = r'switch\s*\((.*?)\)\s*\{([^}]*)\}'
    
    def replace_switch(match):
        switch_var = match.group(1).strip()
        cases_content = match.group(2)
        
        # Разбиваем на case и default
        cases = re.split(r'(case\s+.*?:|default\s*:)', cases_content)
        
        python_code = []
        python_code.append(f'# switch({switch_var}) - converted to if-elif')
        
        current_condition = None
        for part in cases:
            part = part.strip()
            if part.startswith('case '):
                case_value = part[5:].rstrip(':').strip()
                current_condition = f'{switch_var} == {case_value}'
            elif part.startswith('default:'):
                current_condition = 'True'
            elif part and current_condition:
                # Добавляем if/elif с содержимым case
                if current_condition == 'True':  # default
                    python_code.append(f'else:')
                else:
                    python_code.append(f'if {current_condition}:')
                
                # Добавляем содержимое case с отступом
                for line in part.split('\n'):
                    if line.strip():
                        python_code.append(f'    {line.strip()}')
                
                current_condition = None
        
        return '\n'.join(python_code)
    
    code = re.sub(switch_pattern, replace_switch, code)
    return code

def handle_break_continue(code: str) -> str:
    # break и continue в Python такие же, просто оставляем как есть
    # Но убираем точки с запятой
    code = re.sub(r'break\s*;', 'break', code)
    code = re.sub(r'continue\s*;', 'continue', code)
    
    return code

def process_statements(code: str) -> str:
    code = handle_switch_statements(code)
    code = handle_for_loops(code)
    code = handle_while_loops(code)
    code = handle_if_statements(code)
    code = handle_break_continue(code)
    return code