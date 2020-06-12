import requests
import trello
from trello import TrelloApi
import json
import sys
api_key = "099b5e1035b15dbecf0728ccb828b536"
token = "6f5102bb0c65eb9a6ccbd6e15843e7492971f1a0f74dcb8d515cd9c1493feff7"
# trello_u = trello.TrelloApi(api_key, token)
# response = trello_u.boards.new('from api')
# board_id = response['id']
# for col in trello_u.boards.get_list(board_id):
#     print(col['name'])
# for col in trello_u.boards.get_list(board_id):
#     if "Нужно" in col['name']:
#         list_id = col['id']
#         print(trello_u.lists.get_card(list_id))
# card = trello_u.cards.new('Trello api creating card', list_id)
# print(card)

auth_params = {
    "key": api_key,
    "token": token
}
base_url = "https://api.trello.com/1/{}"
board_id = "BderuOiC"


def column_data(tab):
    return requests.get(base_url.format(
        'boards') + '/' + board_id + f'/{tab}', params=auth_params).json()


def read():
    colums = column_data('lists')

    for column in colums:
        print('Колонка', column['name'])
        tasks = requests.get(base_url.format('lists')+'/' +
                             column['id']+'/cards', params=auth_params).json()
        if not tasks:
            print('\t' + 'Нет задач!')
            continue
        for task in tasks:
            print('\t'+task['name'])


def create(column_name, name):
    colums = column_data('lists')
    for column in colums:
        print(column['name'])
        if column['name'] == column_name:
            requests.post(base_url.format('cards'), data={
                          'name': name, 'idList': column['id'], **auth_params})
            print(name + ' создано')
            break


def move(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format(
        'boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Среди всех колонок нужно найти задачу по имени и получить её id
    task_id = None
    for column in column_data:
        column_tasks = requests.get(base_url.format(
            'lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                task_id = task['id']
                break
        if task_id:
            break

    # Теперь, когда у нас есть id задачи, которую мы хотим переместить
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу
    for column in column_data:
        if column['name'] == column_name:
            # И выполним запрос к API для перемещения задачи в нужную колонку
            requests.put(base_url.format('cards') + '/' + task_id +
                         '/idList', data={'value': column['id'], **auth_params})
            print(f'Задача {name} перемещена в {column_name}')
            break


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])
