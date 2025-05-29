import sqlite3

connection_promo = sqlite3.connect("../promo.db")
connection_db = sqlite3.connect("../data.db")
sql_promo = connection_promo.cursor()
sql_db = connection_db.cursor()

all_promos = sql_promo.execute("SELECT code FROM promocodes;").fetchall()

for promo in all_promos:
    sql_db.execute("INSERT INTO promos (promocode) VALUES (?);", (promo[0], ))
connection_db.commit()