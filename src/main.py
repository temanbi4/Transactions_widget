import func


data_list = func.get_input_data('../operations.json')

operations = func.get_executed_operations(data_list)

for operation in operations:
    print(func.get_message(operation))