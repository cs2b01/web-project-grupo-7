from flask import Flask,render_template, request, session, Response, redirect
from database import connector
from model import entities
import json

db = connector.Manager()
engine = db.createEngine()
db_session = db.getSession(engine)


app = Flask(__name__)

@app.route("/index/")
def main():
    return render_template('index.html')

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/restaurantes/")
def restaurantes():
    restaurantes = db_session.query(entities.Restaurant.name).all()
    return render_template('restaurantes.html', restaurantes=restaurantes)

@app.route("/restaurantes/<id>/menu")
def menu(id):
    return render_template('menu.html')

@app.route("/restaurantes/<id>/personal")
def personal(id):
    return render_template('personal.html')


if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))
