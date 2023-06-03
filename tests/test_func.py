import json
import pytest
from src.func import get_input_data, get_executed_operations, format_from_account, format_to_account, format_date, get_message

@pytest.fixture
def operation_list():
    return [
        {
            "id": 431131847,
            "state": "EXECUTED",
            "date": "2018-05-05T01:38:56.538074",
            "operationAmount": {
                "amount": "56071.02",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод с карты на счет",
            "from": "MasterCard 9454780748494532",
            "to": "Счет 51958934737718181351"
        },
        {
            "id": 176798279,
            "state": "CANCELED",
            "date": "2019-04-18T11:22:18.800453",
            "operationAmount": {
                "amount": "73778.48",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Открытие вклада",
            "to": "Счет 90417871337969064865"
        }
    ]


def test_get_executed_operations(operation_list):
    executed_operations = get_executed_operations(operation_list)
    assert executed_operations[0]['state'] == 'EXECUTED'


def test_format_from_account():
    assert format_from_account('Счет 1234567890123456') == 'Счет 1234 56** **** 3456'
    assert format_from_account('Счет 12345678901234567890') == 'Счет 1234 56** **** 7890'
    assert format_from_account('МИР 1234567890123456') == 'МИР 1234 56** **** 3456'
    assert format_from_account('МИР 12345678901234567890') == 'МИР 1234 56** **** 7890'
    assert format_from_account('Visa Platinum 1234567890123456') == 'Visa Platinum 1234 56** **** 3456'
    assert format_from_account('Visa Platinum 12345678901234567890') == 'Visa Platinum 1234 56** **** 7890'
    assert format_from_account('Visa Classic 1234567890123456') == 'Visa Classic 1234 56** **** 3456'
    assert format_from_account('Visa Classic 12345678901234567890') == 'Visa Classic 1234 56** **** 7890'
    assert format_from_account('Visa Gold 1234567890123456') == 'Visa Gold 1234 56** **** 3456'
    assert format_from_account('Visa Gold 12345678901234567890') == 'Visa Gold 1234 56** **** 7890'

def test_format_to_account():
    assert format_to_account('Счет 1234567890123456') == 'Счет **3456'
    assert format_to_account('Счет 12345678901234567890') == 'Счет **7890'
    assert format_to_account('МИР 1234567890123456') == 'МИР **3456'
    assert format_to_account('МИР 12345678901234567890') == 'МИР **7890'
    assert format_to_account('Visa Platinum 1234567890123456') == 'Visa Platinum **3456'
    assert format_to_account('Visa Platinum 12345678901234567890') == 'Visa Platinum **7890'
    assert format_to_account('Visa Classic 1234567890123456') == 'Visa Classic **3456'
    assert format_to_account('Visa Classic 12345678901234567890') == 'Visa Classic **7890'
    assert format_to_account('Visa Gold 1234567890123456') == 'Visa Gold **3456'
    assert format_to_account('Visa Gold 12345678901234567890') == 'Visa Gold **7890'

def test_format_date():
    formatted_date = format_date('2023-05-20T08:30:00')
    assert format_date('2019-02-14T17:38:09.910336') == '14.02.2019'
    assert format_date('2018-08-14T05:42:30.104666') == '14.08.2018'
    assert format_date('2019-03-29T10:57:20.635567') == '29.03.2019'
    assert format_date('2019-06-16T22:17:01.825020') == '16.06.2019'


def test_get_message():
    operation_1 = {
    "id": 801684332,
    "state": "EXECUTED",
    "date": "2019-11-05T12:04:13.781725",
    "operationAmount": {
      "amount": "21344.35",
      "currency": {
        "name": "руб.",
        "code": "RUB"
      }
    },
    "description": "Открытие вклада",
    "to": "Счет 77613226829885488381"
  }
    operation_2 = {
    "id": 154927927,
    "state": "EXECUTED",
    "date": "2019-11-19T09:22:25.899614",
    "operationAmount": {
      "amount": "30153.72",
      "currency": {
        "name": "руб.",
        "code": "RUB"
      }
    },
    "description": "Перевод организации",
    "from": "Maestro 7810846596785568",
    "to": "Счет 43241152692663622869"
  }

    assert get_message(operation_1) == "05.11.2019 Открытие вклада\nСчёт отправителя неизвестен -> Счет **8381\n21344.35 руб. \n"
    assert get_message(operation_2) == "19.11.2019 Перевод организации\nMaestro 7810 84** **** 5568 -> Счет **2869\n30153.72 руб. \n"


def test_main():
    with pytest.raises(FileNotFoundError):
        get_input_data('../error_operations.json')
