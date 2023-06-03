import json
import pytest
from src.func import get_input_data, get_executed_operations, format_from_account, format_to_account, format_date, get_message

@pytest.fixture
def operation_list():
    return [
        {
            'state': 'EXECUTED',
            'date': '2023-05-20T08:30:00',
            'from': '1234567890123456',
            'to': '9876543210987654',
            'description': 'Payment',
            'operationAmount': {
                'amount': 100.0,
                'currency': {'name': 'USD'}
            }
        },
        {
            'state': 'PENDING',
            'date': '2023-05-21T10:00:00',
            'from': '9876543210987654',
            'to': '1234567890123456',
            'description': 'Transfer',
            'operationAmount': {
                'amount': 200.0,
                'currency': {'name': 'EUR'}
            }
        }
    ]





def test_get_executed_operations(operation_list):
    executed_operations = get_executed_operations(operation_list)
    assert len(executed_operations) == 1
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
    assert formatted_date == '20.05.2023'


def test_get_message():
    operation = {
        'date': '2023-05-20T08:30:00',
        'from': '1234567890123456',
        'to': '9876543210987654',
        'description': 'Payment',
        'operationAmount': {
            'amount': 100.0,
            'currency': {'name': 'USD'}
        }
    }
    message = get_message(operation)
    expected_message = "20.05.2023 Payment\n123456 **** **** 3456 -> 9876 ** **7654\n100.0 USD\n"
    assert message == expected_message