import json


def get_input_data(file_name: str):
    """
    :param file_name: Название json-файла с исходными данными
    :return: данные json-файла в виде списка словарей
    """
    with open(file_name, 'r', encoding='utf-8') as f:
        input_data = json.load(f)
    return input_data


def get_executed_operations(operation_list: list):
    """
    Функция игнорирует операции статус перевода которых неизвестен
    :param operation_list: Список со словарями с данными по операциям
    :return: Список из 5 успешных операций
    """
    executed_operations = []
    for operation in operation_list:
        if 'state' in operation.keys():
            if operation['state'] == 'EXECUTED':
                executed_operations.append(operation)
        else:
            continue
    return executed_operations[0:5]


def format_from_account(input_from_account: str):
    """
    Форматирует номер счета отправителя, приводя его к виду, в котором часть номера срыта
    :param input_from_account: Строка с номером счета отправителя
    :return: Строка с отформатированным номером счета отправителя
    """
    from_account_split = input_from_account.split(" ")

    account_list = []
    for i in from_account_split[1]:
        account_list.append(i)

    for i in range(6, 12):
        account_list[i] = "*"

    counter = 0
    new_account = []

    for num in account_list:
        new_account.append(num)
        counter += 1
        if counter == 4:
            new_account.append(' ')
            counter = 0

    del new_account[len(new_account) - 1]
    from_account = ''.join(new_account)
    from_account_split[1] = from_account

    return " ".join(from_account_split)


def format_to_account(input_to_account: str):
    """
    Форматирует номер счета получателя, приводя его к виду, в котором часть номера срыта
    :param input_to_account: Строка с номером счета получателя
    :return: Строка с отформатированным номером счета получателя
    """
    to_account_split = input_to_account.split(" ")
    to_account_list = []
    for i in to_account_split[1]:
        to_account_list.append(i)

    for num in range(0, 16):
        to_account_list[num] = "*"
    to_account_split[1] = "".join(to_account_list)[-6:]

    return " ".join(to_account_split)


def format_date(input_date: str):
    """
    Форматирует дату и время операции оставляя только дату в нужном формате
    :param input_date: Строка с данными о дате и времени операции
    :return: Строка с данными о дате в заданном формате
    """
    date_list = input_date[0:10].split('-')
    return '.'.join(date_list[::-1])


def get_message(operation: dict):
    """
    По полученным данным из словаря генерирует сообщение пользователю
    :param operation: Словарь с данными по операции
    :return: Сообщение об операции
    """
    date = format_date(operation['date'])
    description = operation['description']
    if 'from' not in operation.keys():
        from_account = 'Счет отправителя неизвестен'
    else:
        from_account = format_from_account(operation['from'])
    to_account = format_to_account(operation['to'])
    amount = operation['operationAmount']['amount']
    currency = operation['operationAmount']['currency']['name']

    first_line_list = [date, description]
    second_line_list = [from_account, '->', to_account]
    third_line_list = [amount, currency, '\n']

    first_line = ' '.join(first_line_list)
    second_line = ' '.join(second_line_list)
    third_line = ' '.join(third_line_list)

    return '\n'.join([first_line, second_line, third_line])
