from app import create_app
from app.utils import update_heights, fetch_and_populate_heroes
from app.config import api_token

if __name__ == '__main__':
    app = create_app()
    update_heights(app)
    with app.app_context():
        fetch_and_populate_heroes(api_token)
    app.run(debug=True)
