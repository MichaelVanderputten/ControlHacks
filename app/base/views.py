from flask import render_template, redirect, url_for, Blueprint, request, current_app
from flask_login import current_user, login_required
from app.__init__ import bcrypt

from flask import jsonify
from sqlalchemy import desc
from app.user.models import User
from app import db # Leaderboard stuff

from datetime import date, timedelta# point check

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
        current_user_points = None # just in case
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
        yesterday = today - timedelta(days=1)

        if current_user.last_visited is None: # first time visiting
            current_user.last_visited = today
            current_user.streak = 1
            db.session.commit()
        
        elif current_user.last_visited < today:
            days_since_last_visit = (today - current_user.last_visited).days

            if current_user.last_visited == yesterday:
                current_user.streak += 1 # add to streak
                current_user.point_multiplier += 1
            else:
                current_user.streak = 1 # reset streak
                #current_user.point_multiplier = 1 # If we want multiplier to be reset too
                if days_since_last_visit > 7:
                    current_user.point_multiplier = 1
                else:
                    current_user.point_multiplier = max(1, current_user.point_multiplier - 1)
                    # reduce multiplier by 1 with max of 1

            current_user.points += (1 * current_user.point_multiplier)
            current_user.last_visited = today
            db.session.commit() # add points, update database

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



