import sqlite3


N = 4  # Количество продуктов в магазине - импортируется в основной файл

def initiate_db():
    connection = sqlite3.connect('products_14_5.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT UNIQUE NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    );
    ''')

    cursor.execute('CREATE INDEX IF NOT EXISTS idx_title ON Products (title)')

    for i in range(1, N + 1):
        try:
            cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
                       (
                           f'Продукт {i}',
                           f'Описание {i}',
                           f'{100 * i} руб.'
                       )
                       )
        except sqlite3.IntegrityError as ex:
            if 'UNIQUE constraint failed' in str(ex):
                continue
            else:
                raise ex

    connection.commit()

    connection = sqlite3.connect('users_14_5.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
        );
        ''')

    cursor.execute('CREATE INDEX IF NOT EXISTS idx_username ON Users (username)')

    connection.commit()
    connection.close()

def get_all_products():
    connection = sqlite3.connect('products_14_5.db')
    cursor = connection.cursor()
    products_list = cursor.execute('SELECT * FROM Products')
    msg = []
    for product in products_list:
        msg.append(f'Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}')
    connection.commit()
    return msg

def add_user(username, email, age):
    connection = sqlite3.connect('users_14_5.db')
    cursor = connection.cursor()
    try:
        cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES(?, ?, ?, ?)',
                   (
                   f'{username}',
                   f'{email}',
                   f'{age}',
                   1000
                   )
                   )
    except sqlite3.IntegrityError as ex:
            if 'UNIQUE constraint failed' in str(ex):
                print(f'Обработка исключения: {ex}')
            else:
                raise ex
    connection.commit()
    connection.close()

def is_included(username):
    connection = sqlite3.connect('users_14_5.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Users WHERE username=?', (username,))
    check_username = cursor.fetchone()
    connection.commit()
    connection.close()
    if check_username is not None:
        return True
    else:
        return False
