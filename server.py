from __main__ import app
from flask import json, render_template, request, Response
from objects.accounts.helper import user_exist

print("/"*10)

@app.route("/")
def inpt():
    user_exist()

    return render_template("index.html")

@app.route("/home")
def home():
    return "hello"