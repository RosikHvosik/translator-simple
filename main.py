"""
main.py - ПОЛНОСТЬЮ ИСПРАВЛЕННАЯ ВЕРСИЯ
Исправлены все критические баги:
1. Порядок обработки (syntax до functions)
2. Улучшенная обработка отступов
3. Printf корректно заменяется на print
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
        # ИСПРАВЛЕНО: Правильный порядок обработки
        self.processing_order = [
            self._preprocess,
            self._handle_structures,      # 1. Структуры первыми
            self._handle_declarations,    # 2. Объявления переменных
            self._handle_syntax,          # 3. Убираем { } ; РАНО!
            self._handle_statements,      # 4. Циклы, условия
            self._handle_expressions,     # 5. Операторы, указатели
            self._handle_functions,       # 6. Функции ПОСЛЕ удаления скобок
            self._fix_indentation,        # 7. Исправляем отступы
            self._format_code             # 8. Финальное форматирование
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
        
        # Потом убираем фигурные скобки
        code = re.sub(r'\{', '', code)
        code = re.sub(r'\}', '', code)
        
        return code
    
    def _fix_indentation(self, code: str) -> str:
        """
        ИСПРАВЛЕНО: Улучшенная обработка отступов
        - elif/else на том же уровне что и if
        - После return/break/continue правильное уменьшение отступа
        - Учитываются пустые строки
        """
        lines = code.split('\n')
        result = []
        indent = 0
        prev_was_block_end = False
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Пустые строки
            if not stripped:
                result.append('')
                continue
            
            # ИСПРАВЛЕНО: elif/else уменьшают отступ ПЕРЕД добавлением
            if stripped.startswith(('elif ', 'else:')):
                indent = max(0, indent - 1)
            
            # ИСПРАВЛЕНО: После return/break/continue/pass следующая строка
            # возвращается на уровень выше (если это не elif/else)
            if prev_was_block_end:
                if not stripped.startswith(('elif ', 'else:', 'except:', 'finally:')):
                    indent = max(0, indent - 1)
                prev_was_block_end = False
            
            # Добавляем строку с текущим отступом
            result.append('    ' * indent + stripped)
            
            # Увеличиваем отступ после строк с двоеточием
            if stripped.endswith(':'):
                indent += 1
            
            # Помечаем завершающие операторы блока
            if stripped.startswith(('return', 'break', 'continue', 'pass')):
                prev_was_block_end = True
        
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
    print("C to Python Translator - ИСПРАВЛЕННАЯ ВЕРСИЯ")
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
    print("ПРОВЕРКА ИСПРАВЛЕНИЙ:")
    print("=" * 60)
    
    # Проверка 1: printf заменен
    if "print(" in python_code and "printf" not in python_code:
        print("✓ Printf корректно заменен на print")
    else:
        print("✗ Ошибка: printf не заменен")
    
    # Проверка 2: p->name заменен
    if "p.name" in python_code and "p->name" not in python_code:
        print("✓ p->name корректно заменен на p.name")
    else:
        print("✗ Ошибка: p->name не заменен")
    
    # Проверка 3: Отступы
    lines = python_code.split('\n')
    if_lines = [l for l in lines if 'if ' in l and l.strip().startswith('if')]
    else_lines = [l for l in lines if l.strip().startswith('else:')]
    
    if if_lines and else_lines:
        if_indent = len(if_lines[0]) - len(if_lines[0].lstrip())
        else_indent = len(else_lines[0]) - len(else_lines[0].lstrip())
        
        if if_indent == else_indent:
            print(f"✓ Отступы корректны: if и else на уровне {if_indent}")
        else:
            print(f"✗ Ошибка отступов: if={if_indent}, else={else_indent}")
    
    print("\n" + "=" * 60)
    print("Трансляция завершена!")
    print("=" * 60)