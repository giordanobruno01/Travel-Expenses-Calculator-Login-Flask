
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.security import gen_salt
from . import db
import random, string
from .models import User, Items

main = Blueprint('main', __name__)
# def generateID():
#     alpha = string.ascii_letters
#     for i in range(4):

@main.route('/')
def index():
    # if current_user.is_authenticated:
    #     item = request.form.get('item')
    #     price = request.form.get('PriceItem')
    #     name  = current_user.name
        
    #     new_item = Items(name=name, item=item, price =price)
    #     db.session.add(new_item)
    #     db.session.commit()

    return render_template('index.html')

# @main.route("/home")
# @login_required
# def home():
#     return render_template('index.html')

@main.route("/home", methods=['get'])
@login_required
def home():

    if current_user.is_authenticated:
        item = request.form.get('Item')
        price = request.form.get('PriceItem')
        name  = current_user.name
        
        new_item = Items(name=name, item=item, price =price)
        db.session.add(new_item)
        db.session.commit()

    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():

    return render_template('profile.html',name=current_user.name)

# @main.route("/")