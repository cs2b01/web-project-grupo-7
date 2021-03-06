from flask import Flask,render_template, request, session, Response, redirect, url_for
from database import connector
from model import entities
import json
from flask_cors import CORS

db = connector.Manager()
engine = db.createEngine()
cache=[[],[],[],[],[],[]]

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/static/<content>', methods=['GET','POST','PUT','DELETE'])
def static_content(content):
    return render_template(content)

@app.route("/index")
def main():
    return render_template('index.html')

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/restaurantes/")
def restaurantes():
    if (len(cache[1])==0):
        db_session = db.getSession(engine)
        restaurantes = db_session.query(entities.Restaurant).all()
        cache[1]=restaurantes
        return render_template('restaurantes.html', restaurantes=restaurantes)
    else:
        return render_template('restaurantes.html', restaurantes=cache[1])

@app.route("/personal/")
def personal():
    if(len(cache[2])==0):
        db_session = db.getSession(engine)
        employees = db_session.query(entities.Employee).order_by(entities.Employee.restaurant_id.asc()).all()
        cache[2]=employees
        return render_template('personal.html', employees=employees)
    else:
        return render_template('personal.html', employees=cache[2])

@app.route("/restaurantes/<id>")
def menu(id):
    db_session = db.getSession(engine)
    plates = db_session.query(entities.Plate).filter_by(restaurant_id=id).all()
    return render_template('menu.html',plates=plates)




#CRUD--------------------------------------------------------------------------

@app.route('/plates', methods = ['GET'])
def get_plate():
        session = db.getSession(engine)
        dbResponse = session.query(entities.Plate)
        data = dbResponse[:]
        return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/plates', methods = ['POST'])
def create_plate():
    c =  json.loads(request.form['values'])
    plate = entities.Plate(
        name=c['name'],
        ingredients=c['ingredients'],
        price=c['price'],
        restaurant_id=c['restaurant']['name']['id']
    )
    session = db.getSession(engine)

    session.add(plate)
    session.commit()
    return 'Created Plate'

@app.route('/plates', methods = ['PUT'])
def update_plate():
    session = db.getSession(engine)
    id = request.form['key']
    plate = session.query(entities.Plate).filter(entities.Plate.id == id).first()
    c =  json.loads(request.form['values'])
    for key in c.keys():
        try:
            setattr(plate, key, c[key])
        except AttributeError:
            setattr(plate,'restaurant_id', c['restaurant']['name']['id'])
    session.add(plate)
    session.commit()
    return 'Plate updated'

@app.route('/plates', methods = ['DELETE'])
def delete_plates():
    id = request.form['key']
    session = db.getSession(engine)
    plate = session.query(entities.Plate).filter(entities.Plate.id == id).one()
    session.delete(plate)
    session.commit()
    return "Deleted Plate"



@app.route('/restaurants', methods = ['GET'])
def get_restaurant():
        session = db.getSession(engine)
        dbResponse = session.query(entities.Restaurant)
        data = []
        for data in dbResponse:
            data.append(user)
        message = {'data':data}
        return Response(json.dumps(message, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/restaurants', methods = ['POST'])
def create_restaurant():
    c =  json.loads(request.form['values'])
    restaurant = entities.Restaurant(
        name=c['name'],
        owner=c['owner'],
        address=c['address'],
        phone_number=c['phone_number']
    )
    session = db.getSession(engine)

    session.add(restaurant)
    session.commit()
    return 'Created Restaurant'

@app.route('/restaurants', methods = ['PUT'])
def update_restaurant():
    session = db.getSession(engine)
    id = request.form['key']
    restaurant = session.query(entities.Restaurant).filter(entities.Restaurant.id == id).first()
    c =  json.loads(request.form['values'])
    for key in c.keys():
        setattr(restaurant, key, c[key])
    session.add(restaurant)
    session.commit()
    return 'Restaurant updated'

@app.route('/restaurants', methods = ['DELETE'])
def delete_restaurant():
    id = request.form['key']
    session = db.getSession(engine)
    restaurant = session.query(entities.Restaurant).filter(entities.Restaurant.id == id).one()
    session.delete(restaurant)
    session.commit()
    return "Deleted Plate"



@app.route('/employees', methods = ['GET'])
def get_employee():
        session = db.getSession(engine)
        dbResponse = session.query(entities.Employee)
        data = dbResponse[:]
        return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/employees', methods = ['POST'])
def create_employee():
    c =  json.loads(request.form['values'])
    employee = entities.Employee(
        name=c['name'],
        lastname=c['lastname'],
        position=c['position'],
        restaurant_id=c['restaurant']['name']['id']
    )
    session = db.getSession(engine)

    session.add(employee)
    session.commit()
    return 'Created Plate'

@app.route('/employees', methods = ['PUT'])
def update_employee():
    session = db.getSession(engine)
    id = request.form['key']
    employee = session.query(entities.Employee).filter(entities.Employee.id == id).first()
    c =  json.loads(request.form['values'])
    for key in c.keys():
        try:
            setattr(employee, key, c[key])
        except AttributeError:
            setattr(employee,'restaurant_id',c['restaurant']['name']['id'])
    session.add(employee)
    session.commit()
    return 'Plate updated'

@app.route('/employees', methods = ['DELETE'])
def delete_employee():
    id = request.form['key']
    session = db.getSession(engine)
    employee = session.query(entities.Employee).filter(entities.Employee.id == id).one()
    session.delete(employee)
    session.commit()
    return "Deleted Plate"


@app.route('/personal', methods = ['GET'])
def get_personal():
    session = db.getSession(engine)
    dbResponse = session.query(entities.Plate)
    data = dbResponse[:]
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/authenticate', methods = ["POST"])
def authenticate():
    message = json.loads(request.data)
    username = message['username']
    password = message['password']
    db_session = db.getSession(engine)
    try:
        user = db_session.query(entities.User
            ).filter(entities.User.username == username
            ).filter(entities.User.password == password
            ).one()
        session['logged_user'] = user.id
        message = {'message': 'Authorized', 'user_id': user.id, 'username': user.username}
        return Response(json.dumps(message,cls=connector.AlchemyEncoder), status=200, mimetype='application/json')
    except Exception:
        message = {'message': 'Unauthorized'}
        return Response(message, status=401, mimetype='application/json')


if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))
