from flask import Blueprint, render_template, redirect, url_for, request, flash, Flask
from flask_login import login_user, login_required, logout_user, current_user, LoginManager, UserMixin
from werkzeug.security import gen_salt, generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import random, string



main = Flask(__name__)
main.config['SECRET_KEY'] = 'giordano-secrets'
main.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy()

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100))
    trip = db.Column(db.String(1000))
    startdate = db.Column(db.String(100))
    enddate = db.Column(db.String(100))

class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(1000))
    item = db.Column(db.String(100))
    price = db.Column(db.Integer)
    date = db.Column(db.String(100))
    tripId = db.Column(db.String(1000))

db.init_app(main)
with main.app_context():

        db.create_all()

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(main)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

currentTripId = None

@main.route('/')
def index():
    global currentTripId
    currentTripId = None

    return render_template('index.html')

@main.route('/trips')
@login_required
def trips():
    global currentTripId
    currentTripId = None
    trip = Trip.query.filter_by(email = current_user.email).all()
    return render_template('trips.html', trip =trip)

def convertDateFormat(date):
    dates = date.split("-")

    newDate = dates[2] +"/"+ dates[1] +"/"+dates[0][2:]
    return newDate

@main.route("/trips", methods=['POST'])
@login_required
def trips_post():
    global currentTripId
    currentTripId = None
    if current_user.is_authenticated:
        # add trip details
        TripName = request.form.get('TripName')
        StartDate = request.form.get('StartDate')
        EndDate = request.form.get('EndDate')
        email  = current_user.email

        new_trip = Trip(email=email, trip = TripName, startdate = convertDateFormat(StartDate), enddate = convertDateFormat(EndDate))
        db.session.add(new_trip)
        db.session.commit()
        flash('Trip added')

        return redirect(url_for("trips"))

    if current_user.is_authenticated: 
        item = Items.query.filter_by(email = current_user.email).all()
        total =0
        for i in item:
            total = total+i.price
            return render_template('profile.html',name=current_user.name, item = item, total = total)


@main.route('/myexpenses') 
@login_required
def myexpenses():
    global currentTripId

    if currentTripId == None:
        return redirect(url_for("trips_post"))

    currentTripIdCopy = currentTripId

    item = Items.query.filter_by(email = current_user.email, tripId = currentTripIdCopy).all()
    total =0
    tripDetails = Trip.query.filter_by(id = currentTripId)
    for i in item:
        try:
            total = total+i.price 
        except:
            continue

    return render_template('myexpenses.html',name=current_user.name, item = item, total = total, tripId = currentTripIdCopy, tripName = str(tripDetails[0].trip ) ,tripDate = str(tripDetails[0].startdate + " to " + tripDetails[0].enddate) )


@main.route('/myexpenses/<tripId>', methods = ["POST", "get"]) 
@login_required
def myexpenses_post(tripId):

    global currentTripId
    currentTripId = tripId

    if current_user.is_authenticated:
        item = request.form.get('Item')
        price = request.form.get('PriceItem')
        date = request.form.get('DateItem')

        if item != None:
            new_item = Items(email=current_user.email, item=item, price =price, date =convertDateFormat(date), tripId = tripId)
            db.session.add(new_item)
            db.session.commit()
            flash('Expense added')

    return redirect(url_for("myexpenses"))


@main.route('/profile')
@login_required
def profile():
    global currentTripId
    currentTripId = None
    # item = Items.query.filter_by(email = current_user.email).all()
    # total =0
    # for i in item:
    #     total = total+i.price
    return render_template('profile.html')

@main.route('/deleteItem', methods = ["POST"])
def deleteItem():

    id = request.form["id"]
    item = Items.query.get_or_404(id)

    db.session.delete(item)
    db.session.commit()
    return id

@main.route('/deleteItemAll', methods = ["POST"])
def deleteItemAll():
    id = request.form["tripId"]
    item = Items.query.filter_by(tripId = id).all()
    for i in item:
        db.session.delete(i)
        db.session.commit()
    return id

@main.route('/deleteTrip', methods = ["POST"])
def deleteTrip():

    id = request.form["id"]
    trip = Trip.query.get_or_404(id)

    db.session.delete(trip)
    db.session.commit()

    item = Items.query.filter_by(tripId = id).all()
    for i in item:
        db.session.delete(i)
        db.session.commit()
    return id


@main.route('/login')
def login():
    return render_template('login.html', current_user =current_user)
...
@main.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return render_template('login.html', current_user =current_user) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return render_template('index.html', current_user =current_user)


@main.route('/signup')
def signup():
    return render_template('signup.html', current_user =current_user)

@main.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    try:
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
    except:
        return "problem with get post"
    try:
        user = User.query.filter_by(email=email).first()
    except:
        return "problem with db"
    if user:
        flash('Email address already exists')
        render_template('signup.html')
    new_user = User(email=email, name=name, password=generate_password_hash(password,method='pbkdf2:sha256'))
    db.session.add(new_user)
    db.session.commit()

    return render_template('login.html')

@main.route('/logout')
def logout():
    logout_user()  
    return render_template('index.html')


if __name__ == "__main__": 
    main.run(debug=True)  
#     # export FLASK_APP=project
#     # export FLASK_DEBUG=1
#     # python3 -m venv auth
# # source auth/bin/activate