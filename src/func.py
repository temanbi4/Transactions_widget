import json


def get_input_data(file_name):
    """
    :param file_name: Название json-файла с исходными данными
    :return: данные json-файла в виде списка словарей
    """
    with open(file_name, 'r', encoding='utf-8') as f:
        input_data = json.load(f)
    return input_data

def get_executed_operations(operation_list):
    """
    Функция определяет статуст перевода
    :param operation_list: Список со словарями с данными по операциям
    :return: Список из 5 успешных операций
    """
    executed_operations = []
    for operation in operation_list:
        if 'state' in operation.keys():
            if operation['state'] == 'EXECUTED':
                date = operation.get('date')
                formatted_date = date[:10]
                executed_operations.append((formatted_date, operation))
            else:
                continue

    sorted_operations = sorted(executed_operations, key=lambda x: x[0], reverse=True)
    last_five_operations = [operation[1] for operation in sorted_operations[:5]]
    return last_five_operations

def format_from_account(input_from_account):
    '''
    Функция скрывает номер карты отправителя
    :param input_from_account: Номер счёта отправителя
    :return: Скрытый счёт отправителя
    '''
    from_account_split = input_from_account.split(" ")
    if len(from_account_split) == 2:
        if len(from_account_split[1]) == 16:
           new_str = ' ' + from_account_split[-1][0:4] + ' ' + from_account_split[-1][4:6] + '** ' + '**** ' + from_account_split[-1][12:16]
        elif len(from_account_split[1]) == 20:
           new_str = ' ' + from_account_split[-1][0:4] + ' ' + from_account_split[-1][4:6] + '** ' + '**** ' + from_account_split[-1][16:20]
        else:
           return "Invalid bank account from"
        return from_account_split[0] + new_str
    if len(from_account_split) == 3:
        if len(from_account_split[2]) == 16:
           new_str = ' ' + from_account_split[-1][0:4] + ' ' + from_account_split[-1][4:6] + '** ' + '**** ' + from_account_split[-1][12:16]
        elif len(from_account_split[2]) == 20:
           new_str = ' ' + from_account_split[-1][0:4] + ' ' + from_account_split[-1][4:6] + '** ' + '**** ' + from_account_split[-1][16:20]
        else:
           return "Invalid bank account to"
        return from_account_split[0] + " " +  from_account_split[1] + new_str
def format_to_account(input_to_account):
    """
    Функция скрывает номер карты получателя
    :param input_to_account: Номер счёта получателя
    :return: Скрытый счёт получателя
    """

    to_account_split = input_to_account.split(" ")
    if len(to_account_split) == 2:
        if len(to_account_split[-1]) == 16:
            new_str = ' **' + to_account_split[-1][12:16]
        elif len(to_account_split[-1]) == 20:
            new_str = ' **' + to_account_split[-1][16:20]
        else:
            return "Invalid bank account to"
        return to_account_split[0] + new_str
    if len(to_account_split) == 3:
        if len(to_account_split[-1]) == 16:
            new_str = ' **' + to_account_split[-1][12:16]
        elif len(to_account_split[-1]) == 20:
            new_str = ' **' + to_account_split[-1][16:20]
        else:
            return "Invalid bank account to"
        return to_account_split[0] + " "+ to_account_split[1] + new_str
def format_date(input_date):
    """
    Форматирует дату и время операции оставляя только дату в нужном формате
    :param input_date: Строка с данными о дате и времени операции
    :return: Строка с данными о дате в заданном формате
    """
    date_list = input_date[0:10].split('-')
    return '.'.join(date_list[::-1])

def get_message(operation):
    '''
    Функция создаст структуру выводящего сообщения
    :param operation: Работаем со словарём файла operations.json
    :return: Готовое сообщение с данными
    '''
    date = format_date(operation['date'])
    description = operation['description']
    if 'from' not in operation.keys():
        from_account = 'Счёт отправителя неизвестен'
    else:
        from_account = format_from_account(operation['from'])
    to_account = format_to_account(operation['to'])
    amount = operation['operationAmount']['amount']
    currency = operation['operationAmount']['currency']['name']

    first_line_list = [date, description]
    second_line_list = [from_account, '->', to_account]
    third_line_list = [amount, currency,'\n']

    first_line = ' '.join(first_line_list)
    second_line = ' '.join(second_line_list)
    third_line = ' '.join(third_line_list)

    return '\n'.join([first_line, second_line, third_line])