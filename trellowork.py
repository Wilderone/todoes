import requests

import json
import sys

api_key = "099b5e1035b15dbecf0728ccb828b536"
token = "6f5102bb0c65eb9a6ccbd6e15843e7492971f1a0f74dcb8d515cd9c1493feff7"


auth_params = {
    "key": api_key,
    "token": token
}
base_url = "https://api.trello.com/1/{}"
board_id = "BderuOiC"


def set_api(api_key, token, board_id_n=None):
    api_key = api_key
    token = token
    if board_id_n:
        board_id = board_id_n


def column_data(tab):
    """Базовая обработка url"""
    return requests.get(base_url.format(
        'boards') + '/' + board_id + f'/{tab}', params=auth_params).json()


def get_board_id(board_name):
    """Получение полного ID board"""
    response = requests.get(
        'https://api.trello.com/1/members/me/boards', params=auth_params).json()
    board_id = None

    for board in response:
        print(board['name'])
        if board['name'] == str(board_name):
            board_id = board['id']
    return board_id


def create_column(board_name, list_name):
    """Создание колонки в указанном боарде"""

    board_id = get_board_id(board_name)
    query = {
        'name': list_name + ' Задач: 0',
        'idBoard': board_id,
        "key": api_key,
        "token": token
    }

    response = requests.request('POST', base_url.format('lists'), params=query)

    print(f'Список {response["name"]} создан.')


def read():

    colums = column_data('lists')
    for column in colums:

        tasks = requests.get(base_url.format('lists')+'/' +
                             column['id']+'/cards', params=auth_params).json()

        if not tasks:
            print(f'В "{column["name"]}" задач нет!')
            continue
        for task in tasks:

            print(
                f'Колонка:  "{column["name"]}" ID задачи: "{task["idShort"]}"  Название задачи: "{task["name"]}"')


def update_counter(column_data):
    """Обновление имени листа, сплитит по ' Задач:'"""
    tasks_count = 0
    curr_name = column_data['name'].split(' Задач:')[0]
    # получение списка задач в листе для их пересчёта
    column_tasks = requests.get(base_url.format(
        'lists') + '/' + column_data['id'] + '/cards', params=auth_params).json()
    # пересчёт задач
    for task in column_tasks:
        tasks_count += 1
    # put для обновления имени задачи
    requests.put(base_url.format('lists/')+column_data['id']+"/name", params={
        "value": f'{curr_name} Задач: {tasks_count}',
        **auth_params
    })
    return tasks_count


def update_all_cols():
    colums = column_data('lists')
    for col in colums:
        update_counter(col)


def create(column_name, name):
    """Создаём новую запись в листе"""
    colums = column_data('lists')
    for column in colums:
        parsed_name = column_name.split(' Задач:')[0]
        print(parsed_name, name)
        if str(parsed_name).lower() == str(column['name'].split(' Задач:')[0]).lower():
            requests.post(base_url.format('cards'), data={
                          'name': name, 'idList': column['id'], **auth_params})

            print(name + ' создано')
            break


def move(name, column_name):
    # Получим данные всех колонок на доске
    parsed_name = column_name.split(' Задач:')[0]
    column_data = requests.get(base_url.format(
        'boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Среди всех колонок нужно найти задачу по имени и получить её id
    same_name_tasks = []
    task_id = None
    for column in column_data:

        column_tasks = requests.get(base_url.format(
            'lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                same_name_tasks.append(task)
    if len(same_name_tasks) == 0:
        # эту простыню можно разбить на пару функций. Или сделать через классы. Но было лень :)
        print(f"Задачи {name} не найдено!")
        return
    if len(same_name_tasks) > 1:
        print('По запросу найдены задачи: \n')
        for t in same_name_tasks:
            print(
                f'{t["name"]} - ID {t["idShort"]} в списке {t["idList"]}\n')
    choice = int(input('Введите ID требуемой задачи: '))
    for i in same_name_tasks:
        if i['idShort'] == int(choice):
            task_id = i
            break
        else:
            task_id = same_name_tasks[0]

    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу
    for column in column_data:

        if column['name'].split(' Задач:')[0].lower() == parsed_name.lower():
            # И выполним запрос к API для перемещения задачи в нужную колонку
            requests.put(base_url.format('cards') + '/' + task_id['id'] +
                         '/idList', data={'value': column['id'], **auth_params})

            print(f'Задача {name} перемещена в {column_name}')


if __name__ == "__main__":
    print('python trellwork.py help для справки')
    if sys.argv[1] == 'help':
        print(f'\nsetapi "api_key" "token" "board_id(optional) Для установки своих параметров подключения"\ncreate "col_name" "field_name" для создания записи \nmove "name" "col_name" для перемещения задач \nmk "board_name" "list_name" для создания списков\nБез аргументов для списка задач')
    if sys.argv[1] == 'setapi':
        set_api(sys.argv[2], sys.argv[3], sys.argv[4])
    if len(sys.argv) < 2:
        read()
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
        update_all_cols()
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])
        update_all_cols()
    elif sys.argv[1] == 'mk':
        create_column(sys.argv[2], sys.argv[3])
        update_all_cols()
