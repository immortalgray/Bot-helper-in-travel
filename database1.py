import sqlite3

def prepare_database():
    connection = sqlite3.connect('users.db')
    cur = connection.cursor()

    query = (f'CREATE TABLE IF NOT EXISTS users3' \
                    f'(id INTEGER AUTO_INCREMENT PRIMARY KEY, ' \
                    f'user_id INTEGER, ' \
                    f'role TEXT, ' \
                    f'content TEXT, ' \
                    f'tokens INTEGER,' \
                    f'stt_blocks INTEGER)')

    cur.execute(query)
    connection.commit()
    cur.close()

def regestration_for_people(user_id, role, content, tokens, stt_blocks):
    connection = sqlite3.connect('users.db')
    cur = connection.cursor()
    first_info = (user_id, role, content, tokens, stt_blocks)
    cur.execute(
        f'INSERT INTO users3 (user_id, role, content, tokens, stt_blocks) VALUES (?, ?, ?, ?, ?);',
        first_info)
    connection.commit()
    cur.close()

def regestration_for_assistent(user_id, role, content, tokens, stt_blocks):
    connection = sqlite3.connect('users.db')
    cur = connection.cursor()
    first_info = (user_id, role, content, tokens, stt_blocks)
    cur.execute(
        f'INSERT INTO users3 (user_id, role, content, tokens, stt_blocks) VALUES (?, ?, ?, ?, ?);',
        first_info)
    connection.commit()
    cur.close()

def get_answer(user_id):
    connection = sqlite3.connect('users.db')
    cur = connection.cursor()
    results = cur.execute(f'SELECT content FROM users3 WHERE role = "assistent" and user_id = {user_id} ORDER BY id DESC;')
    for res in results:
        return str(res[0])

def get_prompt(user_id):
    connection = sqlite3.connect('users.db')
    cur = connection.cursor()
    results = cur.execute(f'SELECT content FROM users3 WHERE role = "user" and user_id = {user_id} ORDER BY id DESC;')
    for res in results:
        return str(res[0])