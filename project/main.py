from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.security import gen_salt
from . import db
import random, string
from .models import User, Items, Trip

main = Blueprint('main', __name__)

currentTripId = None

@main.route('/') 
def index():
    # currentTripId = None
    return render_template('index.html')

@main.route('/trips') 
@login_required 
def trips():
    # currentTripId = None
    trip = Trip.query.filter_by(email = current_user.email).all()
    return render_template('trips.html', trip =trip)

@main.route("/trips", methods=['POST'])
@login_required
def trips_post(): 
    # currentTripId = None
    if current_user.is_authenticated:
        # add trip details
        TripName = request.form.get('TripName') 
        StartDate = request.form.get('StartDate')
        EndDate = request.form.get('EndDate')
        email  = current_user.email
       
        new_trip = Trip(email=email, trip = TripName, startdate = StartDate, enddate = EndDate)
        db.session.add(new_trip)
        db.session.commit()
        flash('Trip added') 
        
        return redirect(url_for("main.trips"))
    
    if current_user.is_authenticated:
        item = Items.query.filter_by(email = current_user.email).all()
        total =0
        for i in item:
            total = total+i.price
            return render_template('profile.html',name=current_user.name, item = item, total = total)


@main.route('/myexpenses')
@login_required 
def myexpenses():


    if currentTripId == None:
        return redirect(url_for("main.trips_post"))
    
    currentTripIdCopy = currentTripId
    currentTripId = None
    
    item = Items.query.filter_by(email = current_user.email, tripId = currentTripIdCopy).all()
    total =0 

    for i in item:
        try:
            total = total+i.price
        except:
            continue

    return render_template('myexpenses.html',name=current_user.name, item = item, total = total, tripId = currentTripIdCopy, tripName = Trip.startdate)


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
            new_item = Items(email=current_user.email, item=item, price =price, date =date, tripId = tripId)
            db.session.add(new_item)
            db.session.commit()
            flash('Expense added')

    return redirect(url_for("main.myexpenses")) 



@main.route('/delete', methods = ["POST"])
def delete():
    
    id = request.form["id"] 
    item = Items.query.get_or_404(id)
    
    db.session.delete(item)
    db.session.commit()
    return id  

@main.route('/profile')
@login_required
def profile():
    pass
    # item = Items.query.filter_by(email = current_user.email).all()
    # total =0
    # for i in item:
    #     total = total+i.price
    return render_template('profile.html')

      
