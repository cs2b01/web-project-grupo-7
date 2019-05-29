from flask import Flask,render_template, request, session, Response, redirect, url_for
from database import connector
from model import entities
import json

db = connector.Manager()
engine = db.createEngine()





app = Flask(__name__)

@app.route("/index/")
def main():
    return render_template('index.html')

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/restaurantes/")
def restaurantes():
    db_session = db.getSession(engine)
    restaurantes = db_session.query(entities.Restaurant.name).all()
    return render_template('restaurantes.html', restaurantes=restaurantes)

@app.route("/restaurantes/new", methods=['POST','GET'])
def nuevo_restaurante():
    if request.method == "GET":
        return render_template('nuevo_restaurante.html')

    else:
        db_session = db.getSession(engine)
        nombre = request.form.get('nombre')
        _owner = request.form.get('owner')
        direccion = request.form.get('direccion')
        telefono = request.form.get('telefono')

        restaurante = entities.Restaurant(name=nombre, owner=_owner, address=direccion, phone_number=telefono)
        db_session.add(restaurante)
        db_session.commit()
        return redirect(url_for('restaurantes'))

@app.route("/restaurantes/<id>/menu")
def menu(id):
    return render_template('menu.html')

@app.route("/restaurantes/<id>/menu/new")
def nuevo_menu(id):
    return render_template('nuevo_plato.html')

@app.route("/restaurantes/<id>/personal")
def personal(id):
    return render_template('personal.html')

@app.route("/restaurantes/<id>/personal/new")
def nuevo_personal(id):
    return render_template('nuevo_personal.html')


if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))
