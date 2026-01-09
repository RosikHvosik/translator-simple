"""
test_all_fixes.py
Комплексный тест всех исправлений транслятора
"""

from main import translate_c_to_python

def print_separator(title=""):
    print("\n" + "=" * 70)
    if title:
        print(f" {title}")
        print("=" * 70)

def test_printf_fix():
    """Тест 1: Printf должен заменяться на print"""
    print_separator("ТЕСТ 1: Printf внутри блока")
    
    c_code = """
    int main() {
        if (x > 5) {
            printf("Hello World");
        }
        printf("Outside");
        return 0;
    }
    """
    
    print("C код:")
    print(c_code)
    
    result = translate_c_to_python(c_code)
    
    print("\nPython код:")
    print(result)
    
    # Проверка
    success = True
    if "print(" in result:
        print("\n✓ УСПЕХ: print() найден")
    else:
        print("\n✗ ОШИБКА: print() не найден")
        success = False
    
    if "printf" not in result:
        print("✓ УСПЕХ: printf полностью заменен")
    else:
        print("✗ ОШИБКА: printf остался в коде")
        print(f"  Найдено: {[line for line in result.split('\\n') if 'printf' in line]}")
        success = False
    
    return success

def test_indentation_fix():
    """Тест 2: Отступы в if-else"""
    print_separator("ТЕСТ 2: Отступы if-else")
    
    c_code = """
    int main() {
        if (x > 5) {
            printf("big");
        } else {
            printf("small");
        }
        return 0;
    }
    """
    
    print("C код:")
    print(c_code)
    
    result = translate_c_to_python(c_code)
    
    print("\nPython код:")
    print(result)
    
    # Проверка отступов
    lines = result.split('\n')
    
    # Находим строки if и else
    if_line = None
    else_line = None
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('if ') and 'def' not in line:
            if_line = line
        if stripped.startswith('else:'):
            else_line = line
    
    success = True
    
    if if_line and else_line:
        if_indent = len(if_line) - len(if_line.lstrip())
        else_indent = len(else_line) - len(else_line.lstrip())
        
        print(f"\nОтступ if:   {if_indent} пробелов")
        print(f"Отступ else: {else_indent} пробелов")
        
        if if_indent == else_indent:
            print("✓ УСПЕХ: if и else на одном уровне")
        else:
            print("✗ ОШИБКА: if и else на разных уровнях")
            success = False
    else:
        print("✗ ОШИБКА: Не найдены строки if или else")
        success = False
    
    return success

def test_pointer_access_fix():
    """Тест 3: p->field должен стать p.field"""
    print_separator("ТЕСТ 3: Доступ через указатель p->field")
    
    c_code = """
    struct Node {
        int data;
    };
    
    void func(struct Node* ptr) {
        ptr->data = 42;
        printf("Value: %d", ptr->data);
    }
    """
    
    print("C код:")
    print(c_code)
    
    result = translate_c_to_python(c_code)
    
    print("\nPython код:")
    print(result)
    
    # Проверка
    success = True
    
    if "ptr.data" in result:
        print("\n✓ УСПЕХ: ptr->data заменен на ptr.data")
    else:
        print("\n✗ ОШИБКА: ptr.data не найден")
        success = False
    
    if "ptr->data" not in result:
        print("✓ УСПЕХ: ptr->data не осталось в коде")
    else:
        print("✗ ОШИБКА: ptr->data все еще в коде")
        success = False
    
    return success

def test_full_program():
    """Тест 4: Полная программа из задания"""
    print_separator("ТЕСТ 4: Полная программа")
    
    c_code = """
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
        
        int i = 0;
        while (i < 3) {
            printf("%d ", arr[i]);
            i++;
        }
        
        if (p.age > 20) {
            printf("Older than 20");
        } else {
            printf("20 or younger");
        }
        
        print_person(&p);
        
        for(int j = 0; j < 5; j++) {
            printf("%d ", j);
        }
        
        return 0;
    }
    """
    
    print("C код:")
    print(c_code)
    
    result = translate_c_to_python(c_code)
    
    print("\nPython код:")
    print(result)
    
    # Комплексная проверка
    checks = {
        "Класс Person": "class Person:" in result,
        "Функция print_person": "def print_person" in result,
        "Функция main": "def main():" in result,
        "print вместо printf": "print(" in result and "printf" not in result,
        "p.name вместо p->name": "p.name" in result and "p->name" not in result,
        "p.age вместо p->age": "p.age" in result and "p->age" not in result,
        "Цикл for": "for j in range" in result,
        "Цикл while": "while i < 3:" in result,
        "Условие if": "if p.age > 20:" in result,
        "Условие else": "else:" in result,
        "Нет фигурных скобок": "{" not in result and "}" not in result,
        "Нет точек с запятой": ";" not in result,
    }
    
    print("\n" + "-" * 70)
    print("ПРОВЕРКА ЭЛЕМЕНТОВ:")
    print("-" * 70)
    
    success_count = 0
    total = len(checks)
    
    for name, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"{status} {name}")
        if passed:
            success_count += 1
    
    print("-" * 70)
    print(f"Успешно: {success_count}/{total} ({success_count*100//total}%)")
    
    return success_count == total

def test_nested_blocks():
    """Тест 5: Вложенные блоки и отступы"""
    print_separator("ТЕСТ 5: Вложенные блоки")
    
    c_code = """
    int main() {
        if (x > 0) {
            if (y > 0) {
                printf("Both positive");
            } else {
                printf("X positive, Y not");
            }
        } else {
            printf("X not positive");
        }
        return 0;
    }
    """
    
    print("C код:")
    print(c_code)
    
    result = translate_c_to_python(c_code)
    
    print("\nPython код:")
    print(result)
    
    # Проверка вложенности
    lines = result.split('\n')
    
    print("\nАнализ отступов:")
    for i, line in enumerate(lines):
        if line.strip():
            indent = len(line) - len(line.lstrip())
            print(f"Строка {i+1}: отступ={indent:2d} | {line.strip()[:50]}")
    
    # Простая проверка: должны быть разные уровни отступов
    indents = set()
    for line in lines:
        if line.strip():
            indent = len(line) - len(line.lstrip())
            indents.add(indent)
    
    if len(indents) >= 3:
        print(f"\n✓ УСПЕХ: Найдено {len(indents)} уровней отступов: {sorted(indents)}")
        return True
    else:
        print(f"\n✗ ОШИБКА: Только {len(indents)} уровней отступов")
        return False

def main():
    print("=" * 70)
    print(" КОМПЛЕКСНОЕ ТЕСТИРОВАНИЕ ИСПРАВЛЕНИЙ")
    print("=" * 70)
    
    tests = [
        ("Printf замена", test_printf_fix),
        ("Отступы if-else", test_indentation_fix),
        ("Указатели p->field", test_pointer_access_fix),
        ("Полная программа", test_full_program),
        ("Вложенные блоки", test_nested_blocks),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ ОШИБКА в тесте '{name}': {e}")
            results.append((name, False))
    
    # Итоговый отчет
    print_separator("ИТОГОВЫЙ ОТЧЕТ")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ ПРОЙДЕН" if result else "✗ ПРОВАЛЕН"
        print(f"{status}: {name}")
    
    print("-" * 70)
    print(f"Всего тестов: {total}")
    print(f"Пройдено: {passed}")
    print(f"Провалено: {total - passed}")
    print(f"Процент успеха: {passed*100//total}%")
    
    if passed == total:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! Транслятор работает корректно!")
    else:
        print("\n⚠️  Есть проблемы. Проверьте провалившиеся тесты.")
    
    print("=" * 70)

if __name__ == "__main__":
    main()