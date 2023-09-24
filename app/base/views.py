from flask import render_template, redirect, url_for, Blueprint, request, current_app
from flask_login import current_user, login_required
from app.__init__ import bcrypt

from flask import jsonify
from sqlalchemy import desc
from app.user.models import User
from app import db # Leaderboard stuff

from datetime import date # point check

from . import base_blueprint # blueprint

@base_blueprint.route('/aboutUs')
def aboutUs():
    return render_template('base/aboutUs.html')

@base_blueprint.route('/leaderboard') 
@login_required
def leaderboard():
    top_points_users = User.query.order_by(desc(User.points)).limit(10).all() # top 10
    top_multiplier_users = User.query.order_by(desc(User.point_multiplier)).limit(10).all()
    
    if current_user.is_authenticated: # check current user rank
        current_user_points = current_user.points
        current_user_multiplier = current_user.point_multiplier

        user_points_rank = User.query.filter(User.points > current_user.points).count() + 1
        user_multiplier_rank = User.query.filter(User.point_multiplier > current_user.point_multiplier).count() + 1
    else:
        current_user_points = None # justin case
        current_user_multiplier = None
        user_points_rank = None
        user_multiplier_rank = None

    return render_template( # lots of vars lol
        'base/leaderboard.html',
        top_points_users=top_points_users,
        top_multiplier_users=top_multiplier_users,
        current_user_points=current_user_points,
        current_user_multiplier=current_user_multiplier,
        user_points_rank=user_points_rank,
        user_multiplier_rank=user_multiplier_rank
        )

def check_daily():
    if current_user.is_authenticated:
        today = date.today()
        if current_user.last_visited is None or current_user.last_visited < today:
            current_user.last_visited = today
            current_user.points += (1 * current_user.point_multiplier)
            db.session.commit()

def get_top_users(): # for leaderboard
    all_users = db.session.query(User).all()
    sorted_by_points = sorted(all_users, key=lambda user: user.points, reverse=True)[:10]
    sorted_by_multiplier = sorted(all_users, key=lambda user: user.point_multiplier, reverse=True)[:10]

    top_points_list = []
    top_multiplier_list = []

    # Populate top_points_list
    for user in sorted_by_points:
        top_points_list.append({"username": user.username, "points": user.points})

    # Populate top_multiplier_list
    for user in sorted_by_multiplier:
        top_multiplier_list.append({"username": user.username, "multiplier": user.point_multiplier})

    return top_points_list, top_multiplier_list


def update_forced(): # only use if needed. alters database
    users = User.query.all()
    for user in users:
        user.points = user.points or 0
        user.point_multiplier = user.point_multiplier or 1
        user.streek = user.streek or 1
    db.session.commit()



