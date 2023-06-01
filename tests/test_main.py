import pytest
from src import func


@pytest.fixture
def input_list():
    return [
        {'state': 'EXECUTED', 'id': 441945886},
        {'no_key': 'EXECUTED', 'id': 230157932},
        {'state': 'CANCELED', 'id': 638231325},
        {'state': 'CANCELED', 'id': 153863158},
        {'state': 'EXECUTED', 'id': 231354132},
        {'state': 'EXECUTED', 'id': 228764651},
        {'state': 'EXECUTED', 'id': 233543532},
        {'state': 'EXECUTED', 'id': 453540452},
        {'state': 'EXECUTED', 'id': 229786462},
        {'state': 'EXECUTED', 'id': 230157932}
    ]


def test_get_executed_operations(input_list):
    assert func.get_executed_operations(input_list) == [
        {'state': 'EXECUTED', 'id': 441945886},
        {'state': 'EXECUTED', 'id': 231354132},
        {'state': 'EXECUTED', 'id': 228764651},
        {'state': 'EXECUTED', 'id': 233543532},
        {'state': 'EXECUTED', 'id': 453540452}
    ]


def test_format_from_account():
    assert func.format_from_account('Maestro 1596837868705199') == 'Maestro 1596 83** **** 5199'


def test_format_to_account():
    assert func.format_to_account('Счет 64686473678894779589') == 'Счет **9589'


def test_format_date():
    assert func.format_date('2019-08-26T10:50:58.294041') == '26.08.2019'


@pytest.fixture
def operation():
    return {
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {
            "amount": "31957.58",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        },
        "description": "Перевод организации",
        "from": "Maestro 1596837868705199",
        "to": "Счет 64686473678894779589"
    }


@pytest.fixture
def operation_without_from():
    return {
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {
            "amount": "31957.58",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        },
        "description": "Перевод организации",
        "to": "Счет 64686473678894779589"
    }


def test_message(operation):
    assert func.get_message(operation) == """26.08.2019 Перевод организации
Maestro 1596 83** **** 5199 -> Счет **9589
31957.58 руб. 
"""


def test_message_withot_from(operation_without_from):
    assert func.get_message(operation_without_from) == """26.08.2019 Перевод организации
Счет отправителя неизвестен -> Счет **9589
31957.58 руб. 
"""
