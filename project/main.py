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

@main.route("/home", methods=['POST'])
@login_required
def home(): 

    if current_user.is_authenticated:
        item = request.form.get('Item') 
        price = request.form.get('PriceItem')
        email  = current_user.email
         
        new_item = Items(email=email, item=item, price =price)
        db.session.add(new_item)
        db.session.commit()
 
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    item = Items.query.filter_by(email = current_user.email).all()
    total =0
    for i in item:
        total = total+i.price
    return render_template('profile.html',name=current_user.name, item = item, total = total)

def delete():
    ID = Items.query.filter_by(id = id).all()
    db.session.delete(ID)
    db.session.commit()
    return redirect(url_for('profile'))