from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.security import gen_salt
from . import db
import random, string
from .models import User, Items

main = Blueprint('main', __name__)

@main.route('/') 
def index():
    
    return render_template('index.html')

@main.route('/trips') 
@login_required
def trips():
    return render_template('trips.html')

@main.route("/trips", methods=['POST'])
@login_required
def trips_post(): 

    if current_user.is_authenticated:
        # add trip details
        item = request.form.get('Item') 
        price = request.form.get('PriceItem')
        date = request.form.get('DateItem')
        email  = current_user.email
       
        new_item = Items(email=email, item=item, price =price, date =date)
        db.session.add(new_item)
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
    item = Items.query.filter_by(email = current_user.email).all()
    total =0
    for i in item:
        total = total+i.price
    return render_template('myexpenses.html',name=current_user.name, item = item, total = total)


@main.route('/myexpenses', methods = ["POST"])
@login_required
def myexpenses_post():

    if current_user.is_authenticated:
        item = request.form.get('Item') 
        price = request.form.get('PriceItem')
        date = request.form.get('DateItem')
        email  = current_user.email
       
        new_item = Items(email=email, item=item, price =price, date =date)
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

      
