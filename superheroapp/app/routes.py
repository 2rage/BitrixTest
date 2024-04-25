from flask import render_template, request, session, Response, redirect, url_for
from .models import Superhero, Appearance
from .database import db
from .models import Superhero

def create_routes(app):

    @app.route('/top5_by_strength')
    def top5_by_strength():
        # Фильтрация записей, где 'strength' не является ни NULL, ни пустой строкой
        heroes = Superhero.query.filter(Superhero.strength != 'null', Superhero.strength.isnot(None)).order_by(Superhero.strength.desc()).limit(5).all()

        headers = ["Name", "Strength"]
        data = [
            [hero.name, hero.strength] for hero in heroes if hero.strength
        ]
        # Сохранение заголовков и данных в сессии
        session['headers'] = headers
        session['data'] = data

        return render_template('table.html', title="Топ 5 супергероев по силе", headers=headers, data=data)


    @app.route('/heroes_tall_strong')
    def heroes_tall_strong():
        heroes = db.session.query(Superhero).join(Appearance).filter(
            Appearance.height > '180', Superhero.strength > 80
        ).all()
        
        headers = ["Имя", "Интеллект", "Сила", "Скорость", "Мощность", "Пол", "Раса", "Рост", "Вес"]

        data = [
            [
                hero.name, hero.intelligence, hero.strength, hero.speed, hero.power,
                hero.appearances[0].gender, hero.appearances[0].race,
                hero.appearances[0].height, hero.appearances[0].weight
            ] for hero in heroes
        ]

        # Сохранение заголовков и данных в сессии
        session['headers'] = headers
        session['data'] = data

        return render_template('table.html', title="Герои выше 180 см и с силой более 80", headers=headers, data=data)

    @app.route('/average_by_gender')
    def average_by_gender():
        data = db.session.query(
            Appearance.gender,
            db.func.avg(Superhero.intelligence).label('average_intelligence'),
            db.func.avg(Superhero.strength).label('average_strength'),
            db.func.avg(Superhero.speed).label('average_speed'),
            db.func.avg(Superhero.power).label('average_power')
        ).join(Superhero).group_by(Appearance.gender).all()

        headers = ["Пол", "Средний интеллект", "Средняя сила", "Средняя скорость", "Средняя мощность"]

        rows = [[d.gender, round(d.average_intelligence, 2), round(d.average_strength, 2),
                round(d.average_speed, 2), round(d.average_power, 2)] for d in data]

        # Сохранение заголовков и данных в сессии
        session['headers'] = headers
        session['data'] = rows

        return render_template('table.html', title="Средние значения по полу", headers=headers, data=rows)

    def generate_csv(headers, data): # Функция для генерации CSV
        def generate():
            yield ','.join(headers) + '\n'  # Заголовки столбцов
            for row in data:
                yield ','.join('"' + str(cell).replace('"', '""') + '"' for cell in row) + '\n'  # Данные

        return Response(generate(), mimetype='text/csv', headers={"Content-disposition": "attachment; filename=data.csv"})

    @app.route('/export_csv', methods=["POST"])
    def export_csv():
        # Предполагается, что заголовки и данные хранятся в сессии
        headers = session.get('headers')
        data = session.get('data')

        if not headers or not data:
            return "Нет данных для экспорта", 400

        return generate_csv(headers, data)


    @app.route('/')
    def index():
        heroes = Superhero.query.all()  # Загрузка всех супергероев из базы данных
        return render_template('index.html', heroes=heroes)

    return app