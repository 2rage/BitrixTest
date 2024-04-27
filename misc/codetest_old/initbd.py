import sqlite3


conn = sqlite3.connect('superheroes.db')
c = conn.cursor()


c.execute('''
CREATE TABLE IF NOT EXISTS superheroes (
    id INTEGER PRIMARY KEY,
    name TEXT,
    intelligence INTEGER,
    strength INTEGER,
    speed INTEGER,
    power INTEGER
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS appearance (
    gender TEXT,
    race TEXT,
    height INTEGER,
    weight INTEGER,
    hero_id INTEGER,
    FOREIGN KEY (hero_id) REFERENCES superheroes(id)
)
''')


conn.commit()
conn.close()