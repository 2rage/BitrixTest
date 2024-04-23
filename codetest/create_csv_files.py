import sqlite3
import pandas as pd

conn = sqlite3.connect('superheroes.db')
c = conn.cursor()


top_strength = pd.read_sql_query('''
    SELECT * FROM superheroes 
    WHERE strength IS NOT NULL AND strength != 'null' AND strength != ''
    ORDER BY CAST(strength AS INTEGER) DESC 
    LIMIT 5
''', conn)
top_strength.to_csv('top_strength.csv', index=False)


tall_strong_heroes = pd.read_sql_query('SELECT s.name, a.height, s.strength FROM superheroes s JOIN appearance a ON s.id = a.hero_id WHERE a.height > 180 AND s.strength > 80', conn)
tall_strong_heroes.to_csv('tall_strong_heroes.csv', index=False)


avg_by_gender = pd.read_sql_query('SELECT a.gender, AVG(s.intelligence) AS avg_intelligence, AVG(s.strength) AS avg_strength, AVG(s.speed) AS avg_speed, AVG(s.power) AS avg_power FROM superheroes s JOIN appearance a ON s.id = a.hero_id GROUP BY a.gender', conn)
avg_by_gender.to_csv('avg_by_gender.csv', index=False)

conn.close()