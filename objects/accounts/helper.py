from database import get_db
from app import app

with app.app_context():
    db = get_db()

def user_exist():
    print('-'*10)
    users = db.get_collection("users").find_one("guest", "global", owner=False)
    print(users)