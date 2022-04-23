"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, jsonify, redirect, url_for, send_file, flash
from flask_login import login_user, logout_user, login_required
from app.forms import CarForm, LoginForm, RegisterForm, SearchForm
from app.models import Users, Cars, Favourites
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
import os


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")
    # return send_file(os.path.join('../dist/', 'index.html'))


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/api/register', methods=['POST']) ## Accepts user information and saves it to the database 
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        name = form.name.data
        email = form.email.data
        location = form.location.data
        biography = form.biography.data
        photo = form.photo.data
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        date_joined = form.date_joined.data 

        user = Users(username=username,password=password,name=name,email=email,location=location,biography=biography,photo=photo,date_joined=date_joined)
        db.session.add(user)
        db.session.commit()

        flash('User successfully registered')
        return redirect(url_for("home"))

    return jsonify({"errors": form_errors(form)}), 401



@app.route('/api/auth/login', methods=['POST']) ## Accepts login credentials as username and password
def login():
    form = LoginForm()
    #if request.method == "POST":

    if form.validate_on_submit():
        uname = form.username.data
        pword = form.password.data
        user = Users.query.filter_by(user.username==uname).first()
        if user is not None and check_password_hash(user.password,pword):
            login_user(user)
            flash('User successfully logged in', 'success')
            return redirect(url_for("explore"))  
    return jsonify({"message": "Invalid username or password"}), 401


@app.route('/api/auth/logout', methods=['POST']) ## Logout a user
@login_required
def logout():
    logout_user()
    flash("Logged out.", "danger")
    return redirect(url_for("home"))


@app.route('/api/cars', methods=['GET']) ## Return all cars
@login_required
def getCars():
   if request.method == "GET":
       cars = Cars.query.all()
       if cars != 0:
           for c in cars:
                return jsonify(cars)
       elif cars == 0:
           return jsonify({"message": "could not get car"}), 401

@app.route('/api/cars', methods=['POST']) ## Used for adding new cars
@login_required
def addCars():
    form = CarForm()
    if request.method == "POST" and form.validate_on_submit():
        description = form.description.data
        make  = form.make.data
        model = form.model.data
        colour = form.colour.data
        year = form.year.data
        transmission = form.transmission.data
        car_type = form.car_type.data
        price = form.price.data
        photo = form.photo.data
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['Cars_FOLDER'], filename))
        
        newcar = Cars(description = description, make = make ,model = model, colour = colour, year = year, transmission = transmission, car_type = car_type, price = price, photo = photo  )
        db.session.add(newcar)
        db.session.commit()
        flash('New car added!')
        return redirect(url_for("home"))
    
    return jsonify({"errors": form_errors(form)}), 401


@app.route('/api/cars/{car_id}', methods=['GET']) ## Get Details of a specific car
@login_required
def getCarbyId(car_id):
    if request.method == "GET":
        car = Cars.query.filter_by(Cars.id==car_id).first()
        if car != 0:
            for i in car:
                return jsonify(car)
    return jsonify({"message": "no car with id found"}), 401


@app.route('/api/cars/{car_id}/favourite', methods=['POST']) ## Add car to Favourites for logged in user
@login_required
def addfaveCar(car_id):
    #if request.method == "POST":
    car = Cars.query.filter_by(Cars.id==car_id).first()
    if car not in Favourites:
        favecar = Favourites(car)
        db.session.add(favecar)
        db.session.commit()
        return jsonify({"message": "Car Successfully Favourited"}), 200
    else:
        return jsonify({"message": "Car was already favourited"}), 401



@app.route('/api/search', methods=['GET']) ## Search for cars by make or model
@login_required
def searchCar():
    form = SearchForm()
    #if request.method == "GET":
    if form.validate_on_submit():
        make = form.make.data
        model = form.model.data
        if make in Cars.make or model in Cars.model:   
            result = Cars.query.filter_by(Cars.make==make, Cars.model==model).first()
            return result
        return jsonify({"message": "Car Not found"}), 404


@app.route('/api/users/{user_id}', methods=['GET']) ## Get Details of a user
@login_required
def getUserbyId(user_id):
    if request.method == "GET":
        user = Users.query.filter_by(Users.user_id==user_id).first()
        if user != 0:
            for u in user:
               return jsonify(user)
        elif user == 0:
            return jsonify({"message": "User was not found"}), 401


@app.route('/api/users/{user_id}/favourites', methods=['GET']) ## Get cars that a user has favourited
@login_required
def getfaveCar(user_id):
    if request.method == "GET":
        fave = Favourites.query.filter_by(Favourites.user_id==user_id).first()
        if fave != 0 :
            for f in fave:
               return jsonify(fave)
        elif fave == 0:
            return jsonify({"message": "Favourite not found"}), 401
        
    


# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return jsonify(error="Page Not Found"), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
