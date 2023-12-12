import math
import mysql.connector
from geopy.distance import geodesic
from flask import Blueprint, request

connection = mysql.connector.connect(
    host='127.0.0.1',
    port='3306',
    database='flight_game',
    user='dbuser',
    password='1234',
    autocommit=True
)

airport_type = username = str()

routes = Blueprint('game', __name__)


def check_username(user):
    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT screen_name FROM game WHERE screen_name = '" + user + "'")

    if cursor.rowcount == 0:
        cursor.execute("SELECT COUNT(id) from game")
        last_id = cursor.fetchone()
        new_id = last_id[0] + 1

        cursor.execute(
            "INSERT INTO game (id ,co2_limit, co2_budget, location, screen_name, target, attempts, difficulty) "
            f"VALUES ({new_id},'999', '10000', NULL, '{user}', NULL, NULL, NULL)")
    else:
        cursor.execute(
            f"UPDATE game SET location = NULL, target = NULL WHERE screen_name = '{user}'")


@routes.route('/settings-data', methods=['POST'])
def init_game():
    global airport_type, username
    game_dif = int()
    location, coords = list(range(2)), list(range(2))

    username = request.form['username']
    difficulty = request.form['difficulty']
    distance = request.form['distance']

    check_username(username)

    match difficulty:
        case 'easy':
            airport_type = "'large_airport'"
            game_dif = 0
        case 'normal':
            airport_type = "'large_airport' OR TYPE = 'medium_airport'"
            game_dif = 1
        case 'hard':
            airport_type = "'large_airport' OR TYPE = 'medium_airport' OR TYPE = 'small_airport'"
            game_dif = 2

    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT ident, name, latitude_deg, longitude_deg FROM airport "
                   f"WHERE type = {airport_type} ORDER BY RAND() LIMIT 1")
    location[0] = cursor.fetchall()

    for row in location[0]:
        coords[0] = [row[2], row[3]]
        cursor.execute(f"UPDATE game SET location = '{row[0]}' WHERE screen_name = '{username}'")

    while True:
        cursor = connection.cursor(buffered=True)
        cursor.execute("SELECT ident, name, latitude_deg, longitude_deg FROM airport "
                       f"WHERE type = {airport_type} ORDER BY RAND() LIMIT 1")
        location[1] = cursor.fetchall()

        for row in location[1]:
            coords[1] = [row[2], row[3]]

        match distance:
            case 'close':
                if 1000 <= geodesic(coords[0], coords[1]).km < 5000:
                    break
            case 'medium':
                if 5000 <= geodesic(coords[0], coords[1]).km < 11000:
                    break
            case 'far':
                if 11000 <= geodesic(coords[0], coords[1]).km:
                    break

    for row in location[1]:
        cursor.execute(f"UPDATE game SET target = '{row[0]}', attempts = 0, difficulty = {game_dif},"
                       f" distance = 0 WHERE screen_name = '{username}'")

    return location[0] + location[1]


@routes.route('/navigation-data', methods=['POST'])
def game_navigation():
    arrive = False
    temp_coords = list(range(2))
    reach = 0
    # Index 0: Closer / Index 1: Farther / Index 2: Same distance
    attempts = travel_distance = int()
    coords, location = list(range(3)), list(range(3))
    # Index 0 = Current airport / Index 1 = Target airport / Index 2 = Next airport

    data = request.get_json()
    temp_coords[0] = [data['lat'], data['lng']]

    cursor = connection.cursor(buffered=True)

    cursor.execute(f"SELECT attempts FROM game WHERE screen_name = '{username}'")
    for data in cursor.fetchall():
        attempts = data[0]

    cursor.execute(f"SELECT distance FROM game WHERE screen_name = '{username}'")
    for data in cursor.fetchall():
        travel_distance = data[0]

    for i in range(2):
        if i == 0:
            value = 'location'
        else:
            value = 'target'
        cursor.execute(f"SELECT ident, name, latitude_deg, longitude_deg FROM airport "
                       f"LEFT JOIN game ON game.{value} = ident WHERE game.screen_name = '{username}'")
        result = cursor.fetchall()
        for row in result:
            location[i] = [row[0], row[1], row[2], row[3]]
            coords[i] = [row[2], row[3]]

    cursor.execute("SELECT ident, name, latitude_deg, longitude_deg FROM airport "
                   f"WHERE type = {airport_type}")
    airports = cursor.fetchall()

    length = 1000
    # Placeholder value for now
    for row in airports:
        temp_coords[1] = [row[2], row[3]]

        if math.dist(temp_coords[0], temp_coords[1]) < length and math.dist(temp_coords[0], temp_coords[1]) != 0:
            length = math.dist(temp_coords[0], temp_coords[1])
            coords[2] = [row[2], row[3]]
            location[2] = [row[0], row[1], row[2], row[3]]

    attempts += 1
    travel_distance += int(geodesic(coords[0], coords[2]).km)

    if location[2] == location[1]:
        cursor.execute("UPDATE game SET co2_limit = NULL, location = NULL, target = NULL, attempts = NULL, "
                       f"difficulty = NULL, distance = NULL WHERE screen_name = '{username}'")
        arrive = True
    elif location[2] == location[0]:
        reach = 2
    else:
        cursor.execute(f"UPDATE game SET location = '{location[2][0]}', attempts = {attempts}, "
                       f"distance = {travel_distance} WHERE screen_name = '{username}'")

        if geodesic(coords[2], coords[1]).km < geodesic(coords[0], coords[1]):
            reach = 0
        else:
            reach = 1

    return [location[2], attempts, travel_distance, arrive, reach]
