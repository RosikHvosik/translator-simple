# structures.py
import re
from .types_mapper import map_type

def handle_structs(code: str) -> str:
    # Регулярное выражение для struct
    struct_pattern = r'struct\s+(\w+)\s*\{([^}]*)\};'
    
    def replace_struct(match):
        struct_name = match.group(1)
        fields_content = match.group(2)
        
        # Разбиваем поля на строки и обрабатываем каждое
        fields = [field.strip() for field in fields_content.split(';') if field.strip()]
        
        class_def_lines = [f'class {struct_name}:']
        
        # Добавляем конструктор
        class_def_lines.append('    def __init__(self):')
        
        if fields:
            for field in fields:
                field = field.strip()
                if field:
                    # Извлекаем тип и имя поля
                    field_parts = field.split()
                    if len(field_parts) >= 2:
                        field_type = ' '.join(field_parts[:-1])
                        field_name = field_parts[-1].replace('*', '')
                        
                        # Маппим тип и добавляем инициализацию
                        python_type = map_type(field_type)
                        if python_type == 'int':
                            class_def_lines.append(f'        self.{field_name} = 0')
                        elif python_type == 'float':
                            class_def_lines.append(f'        self.{field_name} = 0.0')
                        elif python_type == 'str':
                            class_def_lines.append(f'        self.{field_name} = ""')
                        elif python_type == 'bool':
                            class_def_lines.append(f'        self.{field_name} = False')
                        else:
                            class_def_lines.append(f'        self.{field_name} = None')
        else:
            # Если нет полей, просто добавляем pass
            class_def_lines.append('        pass')
        
        return '\n'.join(class_def_lines)
    
    code = re.sub(struct_pattern, replace_struct, code)
    
    # Обработка использования struct: struct Person p;
    struct_usage_pattern = r'struct\s+(\w+)\s+(\w+)\s*;'
    code = re.sub(struct_usage_pattern, r'\2 = \1()', code)
    
    # Обработка указателей на struct: struct Person* p;
    struct_ptr_pattern = r'struct\s+(\w+)\s*\*\s*(\w+)\s*;'
    code = re.sub(struct_ptr_pattern, r'\2 = \1()', code)
    
    return code

def handle_unions(code: str) -> str:
    # В Python нет аналога union, преобразуем в класс
    union_pattern = r'union\s+(\w+)\s*\{([^}]*)\};'
    
    def replace_union(match):
        union_name = match.group(1)
        fields_content = match.group(2)
        
        fields = [field.strip() for field in fields_content.split(';') if field.strip()]
        
        class_def_lines = [f'class {union_name}:']
        class_def_lines.append('    def __init__(self):')
        
        if fields:
            for field in fields:
                field = field.strip()
                if field:
                    field_parts = field.split()
                    if len(field_parts) >= 2:
                        field_name = field_parts[-1].replace('*', '')
                        class_def_lines.append(f'        self.{field_name} = None')
        else:
            class_def_lines.append('        pass')
        
        return '\n'.join(class_def_lines)
    
    code = re.sub(union_pattern, replace_union, code)
    return code

def handle_enums(code: str) -> str:
    # Регулярное выражение для enum
    enum_pattern = r'enum\s+(\w+)\s*\{([^}]*)\};'
    
    def replace_enum(match):
        enum_name = match.group(1)
        values_content = match.group(2)
        
        # Разбиваем значения
        values = [val.strip() for val in values_content.split(',') if val.strip()]
        
        # Создаем класс с константами
        class_def_lines = [f'class {enum_name}:']
        
        counter = 0
        for value in values:
            value = value.strip()
            if '=' in value:
                # Обработка присвоений: VALUE = 5
                name, val = value.split('=')
                name = name.strip()
                val = val.strip()
                class_def_lines.append(f'    {name} = {val}')
                try:
                    counter = int(val) + 1
                except ValueError:
                    counter += 1
            else:
                # Автоматическая нумерация
                class_def_lines.append(f'    {value} = {counter}')
                counter += 1
        
        return '\n'.join(class_def_lines)
    
    code = re.sub(enum_pattern, replace_enum, code)
    
    # Обработка использования enum: enum Color c;
    enum_usage_pattern = r'enum\s+(\w+)\s+(\w+)\s*;'
    code = re.sub(enum_usage_pattern, r'\2 = \1()', code)
    
    return code

def process_structures(code: str) -> str:
    code = handle_enums(code)
    code = handle_unions(code)
    code = handle_structs(code)
    return code