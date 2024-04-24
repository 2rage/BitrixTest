from flask import Flask, render_template
import sqlite3
import pandas as pd

app = Flask(__name__)

def query_database(query):
    conn = sqlite3.connect('superheroes.db')
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/top-strength')
def top_strength():
    data = query_database('''
        SELECT * FROM superheroes 
        WHERE strength IS NOT NULL AND strength != 'null' AND strength != ''
        ORDER BY CAST(strength AS INTEGER) DESC 
        LIMIT 5
    ''')
    return render_template('table.html', data=data.to_html(classes='table table-hover', header="true"), title='Top 5 Superheroes by Strength')

@app.route('/tall-strong')
def tall_strong():
    data = query_database('''
        SELECT s.name, a.height, s.strength FROM superheroes s 
        JOIN appearance a ON s.id = a.hero_id 
        WHERE a.height > 180 AND s.strength > 80
    ''')
    return render_template('table.html', data=data.to_html(classes='table table-hover', header="true"), title='Superheroes Taller Than 180 and Stronger Than 80')

@app.route('/avg-by-gender')
def avg_by_gender():
    data = query_database('''
        SELECT a.gender, AVG(s.intelligence) AS avg_intelligence, AVG(s.strength) AS avg_strength, 
        AVG(s.speed) AS avg_speed, AVG(s.power) AS avg_power 
        FROM superheroes s JOIN appearance a ON s.id = a.hero_id 
        GROUP BY a.gender
    ''')
    return render_template('table.html', data=data.to_html(classes='table table-hover', header="true"), title='Average Stats by Gender')

if __name__ == '__main__':
    app.run(debug=True)
