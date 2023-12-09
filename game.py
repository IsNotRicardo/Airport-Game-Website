import mysql.connector
from flask import Blueprint

connection = mysql.connector.connect(
    host='127.0.0.1',
    port='3306',
    database='flight_game',
    user='dbuser',
    password='1234',
    autocommit=True
)

routes = Blueprint('game', __name__)


@routes.route('/')
def check_username():
    print()


@routes.route('/')
def init_game():
    print()