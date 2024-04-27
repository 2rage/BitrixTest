import sqlite3

# Для теста заполненности БД

conn = sqlite3.connect('superheroes.db')

cursor = conn.cursor()

query = "SELECT name FROM sqlite_master WHERE type='table';"

cursor.execute(query)


tables = cursor.fetchall()
if tables:
    print("Список таблиц в базе данных:")
    for table in tables:
        print(table[0])
else:
    print("В базе данных нет таблиц.")


cursor.close()
conn.close()