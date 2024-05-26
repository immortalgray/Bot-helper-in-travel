import sqlite3
import config
def count_tokens_in_project(message):
    count = 0
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    results = cursor.execute(f'SELECT SUM(tokens) FROM users3;')
    for result in results:
        if result[0] == None:
            count = 0
        else:
            count += result[0]
    if count >= config.MAX_TOKENS_FOR_PEOPLE:
        return False,
    else:
        return True
