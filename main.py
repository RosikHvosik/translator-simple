import re
from typing import Tuple
from .preprocessor import preprocess, normalize_code_structure
from .utils import preserve_strings, restore_strings, preserve_char_literals, restore_char_literals, normalize_whitespace
from .declarations import process_declarations
from .functions import process_functions
from .structures import process_structures
from .statements import process_statements
from .expressions import process_expressions

class CToPythonTranslator:
    def __init__(self):
        self.processing_order = [
            self._preprocess,
            self._handle_structures,
            self._handle_declarations,
            self._handle_functions,
            self._handle_statements,
            self._handle_expressions,
            self._handle_syntax,
            self._format_code
        ]
    
    def _preprocess(self, code: str) -> str:
        # Сохраняем строковые и символьные литералы
        code, self._strings = preserve_strings(code)
        code, self._chars = preserve_char_literals(code)
        
        # Убираем препроцессорные директивы
        code = preprocess(code)
        
        return code
    
    def _handle_structures(self, code: str) -> str:
        return process_structures(code)
    
    def _handle_declarations(self, code: str) -> str:
        return process_declarations(code)
    
    def _handle_functions(self, code: str) -> str:
        return process_functions(code)
    
    def _handle_statements(self, code: str) -> str:
        return process_statements(code)
    
    def _handle_expressions(self, code: str) -> str:
        return process_expressions(code)
    
    def _handle_syntax(self, code: str) -> str:
        # Убираем точки с запятой
        code = re.sub(r';', '', code)
        
        # Убираем фигурные скобки
        code = re.sub(r'\{', '', code)
        code = re.sub(r'\}', '', code)
        
        return code
    
    def _format_code(self, code: str) -> str:
        lines = code.split('\n')
        result_lines = []
        indent_level = 0
        
        for line in lines:
            stripped = line.strip()
            if stripped:
                # Уменьшаем отступ для else
                if stripped.startswith('else:'):
                    indent_level = max(0, indent_level - 1)
                    result_lines.append('    ' * indent_level + stripped)
                    indent_level += 1  # else также увеличивает отступ
                elif stripped.startswith('elif '):
                    indent_level = max(0, indent_level - 1)
                    result_lines.append('    ' * indent_level + stripped)
                    indent_level += 1
                elif stripped.endswith(':'):
                    # Строка заканчивается на :, увеличиваем отступ
                    result_lines.append('    ' * indent_level + stripped)
                    indent_level += 1
                else:
                    result_lines.append('    ' * indent_level + stripped)
            else:
                # Пустая строка - уменьшаем отступ если следующая строка вне блока
                result_lines.append('')
        
        # Восстанавливаем строковые и символьные литералы
        final_code = '\n'.join(result_lines)
        final_code = restore_char_literals(final_code, self._chars)
        final_code = restore_strings(final_code, self._strings)
        
        # Нормализуем пробелы
        final_code = normalize_whitespace(final_code)
        final_code = normalize_code_structure(final_code)
        
        return final_code
    
    def translate(self, c_code: str) -> str:
        code = c_code
        for processor in self.processing_order:
            code = processor(code)
        return code

def translate_c_to_python(c_code: str) -> str:
    translator = CToPythonTranslator()
    return translator.translate(c_code)

if __name__ == "__main__":
    sample_c_code = """
    #include <stdio.h>
    
    struct Person {
        int age;
        char* name;
    };
    
    void print_person(struct Person* p) {
        printf("Name: %s, Age: %d\\n", p->name, p->age);
    }
    
    int main() {
        struct Person p;
        p.age = 25;
        p.name = "Ivan";
        
        int arr[3];
        arr[0] = 10;
        arr[1] = 20;
        arr[2] = 30;
        
        int i = 0;
        while (i < 3) {
            printf("%d ", arr[i]);
            i++;
        }
        
        if (p.age > 20) {
            printf("\\nOlder than 20\\n");
        } else {
            printf("\\n20 or younger\\n");
        }
        
        print_person(&p);
        
        for(int j = 0; j < 5; j++) {
            printf("%d ", j);
        }
        
        return 0;
    }
    """
    
    python_code = translate_c_to_python(sample_c_code)
    print("Результат трансляции:")
    print(python_code)