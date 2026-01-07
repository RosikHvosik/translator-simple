"""
main.py - ПОЛНОСТЬЮ ПЕРЕРАБОТАННАЯ ВЕРСИЯ
Исправлены все критические баги
"""
import re
from typing import Tuple, List

from preprocessor import preprocess, normalize_code_structure
from utils import (preserve_strings, restore_strings, 
                   preserve_char_literals, restore_char_literals, 
                   normalize_whitespace)
from declarations import process_declarations
from functions import process_functions
from structures import process_structures
from statements import process_statements
from expressions import process_expressions

class CToPythonTranslator:
    def __init__(self):
        self.processing_order = [
            self._preprocess,
            self._handle_structures,
            self._handle_functions,      # ФУНКЦИИ ДО ОБЪЯВЛЕНИЙ!
            self._handle_statements,      # ОПЕРАТОРЫ ДО ВЫРАЖЕНИЙ!
            self._handle_declarations,
            self._handle_expressions,
            self._handle_syntax,
            self._fix_indentation,        # НОВЫЙ ЭТАП
            self._format_code
        ]
    
    def _preprocess(self, code: str) -> str:
        # Сохраняем строковые и символьные литералы
        code, self._strings = preserve_strings(code)
        code, self._chars = preserve_char_literals(code)
        
        # Убираем препроцессорные директивы и комментарии
        code = preprocess(code)
        
        return code
    
    def _handle_structures(self, code: str) -> str:
        return process_structures(code)
    
    def _handle_functions(self, code: str) -> str:
        return process_functions(code)
    
    def _handle_statements(self, code: str) -> str:
        return process_statements(code)
    
    def _handle_declarations(self, code: str) -> str:
        return process_declarations(code)
    
    def _handle_expressions(self, code: str) -> str:
        return process_expressions(code)
    
    def _handle_syntax(self, code: str) -> str:
        """Удаление C-синтаксиса после всех преобразований"""
        # Сначала убираем точки с запятой
        code = re.sub(r';', '', code)
        
        # Потом убираем фигурные скобки - они уже стали двоеточиями
        code = re.sub(r'\{', '', code)
        code = re.sub(r'\}', '', code)
        
        return code
    
    def _fix_indentation(self, code: str) -> str:
        """
        НОВАЯ ФУНКЦИЯ: Исправление отступов на основе структуры кода
        """
        lines = code.split('\n')
        result = []
        indent = 0
        
        for line in lines:
            stripped = line.strip()
            
            if not stripped:
                result.append('')
                continue
            
            # Уменьшаем отступ для elif, else
            if stripped.startswith(('elif ', 'else:')):
                indent = max(0, indent - 1)
            
            # Добавляем строку с текущим отступом
            result.append('    ' * indent + stripped)
            
            # Увеличиваем отступ после строк с двоеточием
            if stripped.endswith(':'):
                indent += 1
            
            # Специальная обработка return, break, continue, pass
            # После них отступ не меняется, но следующая строка может быть на уровень ниже
            
        return '\n'.join(result)
    
    def _format_code(self, code: str) -> str:
        """Финальное форматирование"""
        
        # Восстанавливаем строковые и символьные литералы
        code = restore_char_literals(code, self._chars)
        code = restore_strings(code, self._strings)
        
        # Нормализуем пробелы
        code = normalize_whitespace(code)
        code = normalize_code_structure(code)
        
        # Убираем лишние пустые строки между строками кода
        lines = code.split('\n')
        result = []
        prev_empty = False
        
        for line in lines:
            if not line.strip():
                if not prev_empty:
                    result.append('')
                prev_empty = True
            else:
                result.append(line)
                prev_empty = False
        
        # Добавляем пустые строки между определениями классов/функций
        final_lines = []
        for i, line in enumerate(result):
            final_lines.append(line)
            if line.startswith(('class ', 'def ')) and i < len(result) - 1:
                if result[i + 1].strip() and not result[i + 1].startswith('    '):
                    final_lines.append('')
        
        return '\n'.join(final_lines)
    
    def translate(self, c_code: str) -> str:
        """Главная функция трансляции"""
        code = c_code
        for processor in self.processing_order:
            code = processor(code)
            # DEBUG: раскомментируйте для отладки
            # print(f"\n=== После {processor.__name__} ===")
            # print(code[:500])
        return code

def translate_c_to_python(c_code: str) -> str:
    """
    Главная функция для трансляции C кода в Python
    
    Args:
        c_code: Строка с кодом на языке C
    
    Returns:
        Строка с кодом на языке Python
    """
    translator = CToPythonTranslator()
    return translator.translate(c_code)

if __name__ == "__main__":
    print("=" * 60)
    print("C to Python Translator")
    print("=" * 60)
    
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
    
    print("\n--- C КОД ---")
    print(sample_c_code)
    
    print("\n" + "=" * 60)
    print("--- PYTHON КОД ---")
    print("=" * 60)
    
    python_code = translate_c_to_python(sample_c_code)
    print(python_code)
    
    print("\n" + "=" * 60)
    print("Трансляция завершена!")
    print("=" * 60)