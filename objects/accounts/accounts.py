from flask import Blueprint, request, render_template, Response
from database import get_db
import bcrypt

db = get_db()

accounts = Blueprint('accounts', __name__, template_folder='templates')


@accounts.route("/register", method=("GET", "POST"))
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        data = request.get_json(True)
        username = data["username"]
        password = data["password"]
        confirm = data["confirm"]
        if password != confirm:
            return render_template("register.html", msg="password_invalid")
        