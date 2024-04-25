from app import create_app, db
from app.models import Superhero, Appearance
import requests

def fetch_and_populate_heroes(api_token, start_id=1, end_id=100):
    base_url = 'https://superheroapi.com/api/{}/'.format(api_token)

    # Определяем, с какого ID начать заполнение
    hero_count = Superhero.query.order_by(Superhero.id.desc()).first()
    start_id = 1 if not hero_count else hero_count.id + 1

    if hero_count and hero_count.id >= end_id:
        print(f"База данных уже заполнена {hero_count.id} супергероями.")
        return
    else:
        if hero_count:
            print(f"В базе данных {hero_count.id} супергероев. Заполняем оставшиеся.")
        else:
            print("База данных пуста. Начинаем заполнение базы данных.")


    for hero_id in range(start_id, end_id + 1):
        response = requests.get(base_url + str(hero_id))
        if response.status_code == 200:
            data = response.json()
            new_hero = Superhero(
                id=data['id'],
                name=data.get('name'),
                intelligence=data['powerstats'].get('intelligence', 0),
                strength=data['powerstats'].get('strength', 0),
                speed=data['powerstats'].get('speed', 0),
                power=data['powerstats'].get('power', 0)
            )
            db.session.add(new_hero)
            try:
                db.session.commit()
                print(f"Супергерой '{new_hero.name}' успешно добавлен.")
            except Exception as e:
                db.session.rollback()
                print(f"Failed to add superhero '{new_hero.name}': {e}")

            appearance_data = data['appearance']
            new_appearance = Appearance(
                gender=appearance_data.get('gender'),
                race=appearance_data.get('race'),
                height=str(appearance_data.get('height', [''])[0]),
                weight=str(appearance_data.get('weight', [''])[0]),
                hero_id=new_hero.id
            )
            db.session.add(new_appearance)
            try:
                db.session.commit()
                print(f"Внешний вид '{new_hero.name}' успещно добавлен.")
            except Exception as e:
                db.session.rollback()
                print(f"Ошибка добавления внешнего вида '{new_hero.name}': {e}")
        else:
            print(f"Ошибка при обновлении данных героя: {hero_id}")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        api_token = 'REMOVED'  # Замените на ваш API ключ
        fetch_and_populate_heroes(api_token)
        app.run(debug=True)  # Запускаем Flask-приложение после заполнения базы данных
