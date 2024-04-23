import sqlite3
import requests


api_token = 'REMOVED'
base_url = 'https://superheroapi.com/api/' + api_token + '/'

def fetch_superhero_data(hero_id):
    response = requests.get(base_url + str(hero_id))
    return response.json()

def safe_int_conversion(value):
    try:
        return int(''.join(filter(str.isdigit, value)))
    except ValueError:
        return 0  
    
conn = sqlite3.connect('superheroes.db')
c = conn.cursor()

for i in range(1, 101):
    hero_data = fetch_superhero_data(i)
    if 'appearance' in hero_data and 'powerstats' in hero_data:
        try:
            
            height = safe_int_conversion(hero_data['appearance'].get('height', '0'))
            weight = safe_int_conversion(hero_data['appearance'].get('weight', '0'))
            intelligence = hero_data['powerstats'].get('intelligence', '0')
            strength = hero_data['powerstats'].get('strength', '0')
            speed = hero_data['powerstats'].get('speed', '0')
            power = hero_data['powerstats'].get('power', '0')
            
            print(f"Добавление супергероя {hero_data['name']} с характеристиками: Intelligence={intelligence}, Strength={strength}, Speed={speed}, Power={power}")

            c.execute('INSERT INTO superheroes (id, name, intelligence, strength, speed, power) VALUES (?, ?, ?, ?, ?, ?)',
                      (i, hero_data['name'], intelligence, strength, speed, power))

            c.execute('INSERT INTO appearance (gender, race, height, weight, hero_id) VALUES (?, ?, ?, ?, ?)',
                      (hero_data['appearance']['gender'], hero_data['appearance']['race'], height, weight, i))
        except Exception as e:
            print(f"Ошибка при добавлении супергероя с id {i}: {e}")
    else:
        print(f"Нет полных данных для супергероя с id {i}: {hero_data}")

conn.commit()
conn.close()
