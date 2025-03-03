"""
РАБОТУ ВЫПОЛНИЛ СТУДЕНТ БАТОВ ВЛАДИСЛАВ КЭ-402


Результат работы программы

User: Boris
User: Boris
Идентификация прошла успешно, добро пожаловать в систему
Перечень Ваших прав:
Файл_1: Чтение
Файл_2: Запись
CD-RW: Запись
Дисковод: Передача прав
Принтер: Чтение, Передача прав
Жду ваших указаний > read
Над каким объектом производится операция? 1
Операция прошла успешно
Жду ваших указаний > write
Над каким объектом производится операция? 2
Операция прошла успешно
Жду ваших указаний > grant
Право на какой объект передается? 4
Какое право передается? Чтение
Какому пользователю передается право? Ivan
Операция прошла успешно
Жду ваших указаний > quit
Работа пользователя Boris завершена. До свидания.

User:


"""
import random

# Возможные права доступа
rights_list = ["Чтение", "Запись", "Передача прав"]
all_rights = set(rights_list)

# Все возможные комбинации прав (8 вариантов: от отсутствия до полного набора)
possible_rights = [
    set(),
    {"Чтение"},
    {"Запись"},
    {"Передача прав"},
    {"Чтение", "Запись"},
    {"Чтение", "Передача прав"},
    {"Запись", "Передача прав"},
    {"Чтение", "Запись", "Передача прав"}
]

# Вариант 4: 6 пользователей и 5 объектов
users = ["Ivan", "Sergey", "Boris", "Olga", "Anna", "Dmitry"]
objects = ["Файл_1", "Файл_2", "CD-RW", "Дисковод", "Принтер"]

# Создание матрицы доступа: для каждого пользователя и объекта задаём набор прав
access_matrix = {}
for user in users:
    access_matrix[user] = {}
    for obj in objects:
        if user == "Ivan":  # Администратор – полные права для всех объектов
            access_matrix[user][obj] = all_rights.copy()
        else:
            # Для остальных пользователей права выбираются случайным образом
            access_matrix[user][obj] = random.choice(possible_rights)


def print_access_rights(user):
    """Вывод списка объектов и прав доступа для пользователя"""
    print(f"User: {user}")
    print("Идентификация прошла успешно, добро пожаловать в систему")
    print("Перечень Ваших прав:")
    for obj in objects:
        rights = access_matrix[user][obj]
        if rights == all_rights:
            rights_str = "Полные права"
        elif not rights:
            rights_str = "Запрет"
        else:
            rights_str = ", ".join(rights)
        print(f"{obj}: {rights_str}")


def check_operation(user, obj, operation):
    """
    Проверка возможности выполнения операции:
    для 'read' – наличие права 'Чтение',
    для 'write' – наличие права 'Запись'
    """
    if operation == "read":
        return "Чтение" in access_matrix[user][obj] or access_matrix[user][obj] == all_rights
    elif operation == "write":
        return "Запись" in access_matrix[user][obj] or access_matrix[user][obj] == all_rights
    return False


def grant_right(from_user, obj, right, to_user):
    """
    Осуществляет передачу права:
    если from_user обладает правом 'Передача прав' для данного объекта,
    добавляет указанное право to_user.
    """
    if "Передача прав" in access_matrix[from_user][obj] or access_matrix[from_user][obj] == all_rights:
        access_matrix[to_user][obj].add(right)
        return True
    else:
        return False


def main():
    while True:
        user = input("User: ").strip()
        if user not in users:
            print("Идентификация не пройдена. Неверный идентификатор.")
            continue

        # После успешной идентификации выводим перечень прав доступа
        print_access_rights(user)

        while True:
            command = input("Жду ваших указаний > ").strip().lower()
            if command == "quit":
                print(f"Работа пользователя {user} завершена. До свидания.\n")
                break
            elif command in ["read", "write"]:
                obj_input = input("Над каким объектом производится операция? ").strip()
                # Позволяем вводить как номер (индекс) объекта, так и его имя
                if obj_input.isdigit():
                    index = int(obj_input) - 1
                    if 0 <= index < len(objects):
                        obj_name = objects[index]
                    else:
                        print("Неверный номер объекта.")
                        continue
                else:
                    obj_name = obj_input
                    if obj_name not in objects:
                        print("Объект не найден.")
                        continue
                if check_operation(user, obj_name, command):
                    print("Операция прошла успешно")
                else:
                    print("Отказ в выполнении операции. У Вас нет прав для ее осуществления.")
            elif command == "grant":
                obj_input = input("Право на какой объект передается? ").strip()
                if obj_input.isdigit():
                    index = int(obj_input) - 1
                    if 0 <= index < len(objects):
                        obj_name = objects[index]
                    else:
                        print("Неверный номер объекта.")
                        continue
                else:
                    obj_name = obj_input
                    if obj_name not in objects:
                        print("Объект не найден.")
                        continue
                # Проверка права на передачу для текущего пользователя
                if not ("Передача прав" in access_matrix[user][obj_name] or access_matrix[user][
                    obj_name] == all_rights):
                    print("Отказ в выполнении операции. У Вас нет прав для ее осуществления.")
                    continue
                right_to_grant = input("Какое право передается? ").strip()
                if right_to_grant not in ["Чтение", "Запись", "Передача прав"]:
                    print("Неверное право.")
                    continue
                target_user = input("Какому пользователю передается право? ").strip()
                if target_user not in users:
                    print("Пользователь не найден.")
                    continue
                if grant_right(user, obj_name, right_to_grant, target_user):
                    print("Операция прошла успешно")
                else:
                    print("Отказ в выполнении операции. У Вас нет прав для ее осуществления.")
            else:
                print("Неверная команда.")


if __name__ == "__main__":
    main()
