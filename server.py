from flask import Flask, json, render_template, request, Response
from users import db, DB

app = Flask(__name__)


@app.route('/')
def home():
    x  = db.users.find()
    res = ""
    for i in x:
        res += json.dumps(i) + '<br>'
    return res

@app.route('/inp')
def inpt():
    return render_template("index.html")

@app.route('/add', methods=["POST"])
def add():
    if request.method == "POST":
        name = request.form.get("name")
        reg = request.form.get("reg")
        contact = request.form.get("contact")
        email = request.form.get("email")
        DB().add_member(name, reg, contact, email)
    return Response(status=200)

@app.route("/dev/exec")
def dev_exec():
    print(DB().add_group("member", [0,1,0,0]))
    print(DB().add_group("admin", [1,1,1,1]))
    print(DB().add_scope("member", "form", [1,1,1,0]))
    return "done"