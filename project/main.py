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
def trips():
    return render_template('trips.html')

@main.route("/trips", methods=['POST'])
@login_required
def trips_post(): 

    if current_user.is_authenticated:
        item = request.form.get('Item') 
        price = request.form.get('PriceItem')
        date = request.form.get('DateItem')
        email  = current_user.email
       
        new_item = Items(email=email, item=item, price =price, date =date)
        db.session.add(new_item)
        db.session.commit()
        flash('Item added')
        
    return redirect(url_for("main.trips"))


@main.route('/myexpenses')
@login_required
def myexpenses():
    return render_template('myexpenses.html')

@main.route('/myexpenses')
@login_required
def myexpenses_post():
    return redirect(url_for("main.myexpenses"))


@main.route('/profile')
@login_required
def profile():
    item = Items.query.filter_by(email = current_user.email).all()
    total =0
    for i in item:
        total = total+i.price
    return render_template('profile.html',name=current_user.name, item = item, total = total)
@main.route('/delete', methods = ["POST"])
def delete():
    
    id = request.form["id"] 
    item = Items.query.get_or_404(id)
    
    db.session.delete(item)
    db.session.commit()
    return id        
