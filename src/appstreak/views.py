from flask import Blueprint

from src.libstreak.use_cases import *

views = Blueprint(__name__, "views")


def view_misc():
    """
    Views:
    main page /taknikiyaat/
    rating /taknikiyaat/rating/ (individual/team)
    groups /taknikiyaat/groups/
    profile /taknikiyaat/profile/{username}
    """
    pass


@views.route("/")
def view_homepage():
    response = homepage()  # TDOO render here, then to FE
    return response


@views.route("/you")
def view_user_profile():
    response = user_profile()
    return response


@views.route("/ranking")
def view_rating():
    response = rating()
    return response


@views.route("/scrap")
def view_scrap_user_profile():
    response = scrap_user_profile()
    return response
