import random
import string
import sqlite3

def generate_promo_code(length=11):
    characters = string.ascii_uppercase + string.digits
    promo_code = ''.join(random.choices(characters, k=length))
    return promo_code

connection = sqlite3.connect("../promo.db")
sql = connection.cursor()
sql.execute("CREATE TABLE IF NOT EXISTS promocodes (id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT UNIQUE NOT NULL);")
connection.commit()
for i in range(0, 30000):
    a = generate_promo_code()
    try:
        sql.execute('INSERT INTO promocodes (code) VALUES (?)', (a, ))
        connection.commit()
        print(f"{a} промокодов успешно сохранены в базу данных.")
    except sqlite3.IntegrityError:
        print("Ошибка: Некоторые промокоды уже существуют в базе данных.")