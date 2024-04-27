from app import create_app
from app.utils import update_heights, fetch_and_populate_heroes

if __name__ == '__main__':
    app = create_app()
    update_heights(app)
    with app.app_context():
        api_token = 'PASTE_YOUR_SUPERHEROAPI_KEY'
        fetch_and_populate_heroes(api_token)
    app.run(debug=True)
