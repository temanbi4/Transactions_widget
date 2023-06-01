import json

def mask_account_number(account_number):
    """
    Функция для замаскирования номера карты или номера счета.
    Видны первые 6 цифр и последние 4, разбитые по блокам по 4 цифры, разделенные пробелом.

    Параметры:
    - account_number (str): Номер карты или номер счета.

    Возвращает:
    - str: Замаскированный номер карты или номер счета.
    """
    masked_number = "XXXX " + " ".join([account_number[i:i+4] for i in range(6, len(account_number)-4, 4)]) + " " + account_number[-4:]
    return masked_number

def print_recent_operations():
    """
    Функция для вывода на экран списка из 5 последних выполненных клиентом операций.

    Выводит операции в формате:
    <дата перевода> <описание перевода> <откуда> -> <куда> <сумма перевода> <валюта>
    """
    with open('operations.json') as file:
        data = json.load(file)

    executed_operations = [operation for operation in data if operation['state'] == 'EXECUTED']
    sorted_operations = sorted(executed_operations, key=lambda x: x['date'], reverse=True)
    recent_operations = sorted_operations[:5]

    for operation in recent_operations:
        date = operation['date'][:10]  # Берем только первые 10 символов, содержащих дату
        description = operation['description']
        from_account = mask_account_number(operation.get('from', ''))
        to_account = mask_account_number(operation.get('to', ''))
        amount = operation['operationAmount']['amount']
        currency = operation['operationAmount']['currency']['name']

        print(f"{date} {description}")
        print(f"{from_account} -> {to_account}")
        print(f"{amount} {currency}")
        print()