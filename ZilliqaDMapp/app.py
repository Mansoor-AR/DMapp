from flask import Flask
from flask import request
from flask import jsonify
import json
from haversine import haversine
import subprocess

app = Flask(__name__)

@app.route("/testNode")
def test_node():
    command = "node Quickstart.js"
    try:
        result = subprocess.check_output(command, shell =True)
        print(result)
    except subprocess.CalledProcessError as e:
        print("An error occured: "+e)

@app.route("/")
def main_page():
    with open("main.html", "r") as f:
        return f.read()

@app.route("/contribute")
def contribute_route_page():
    with open("contribute.html", "r") as f:
        return f.read()

@app.route("/user")
def user_page():
    with open("user.html", "r") as f:
        return f.read()

@app.route("/path.json")
def request_path_file():
    with open("path.json", "r") as f:
        return f.read()

@app.route("/web3.min.js")
def request_web3min_file():
    with open("web3.min.js", "r") as f:
        return f.read()

@app.route('/submitRoute', methods = ['POST'])
def submit_route():
    if request.method == 'POST':
        data = request.form
        keys = list(data.to_dict().keys())
        d = json.loads(keys[0])
        route_name = d['routeName']
        new_path_points = d['newPathPoints']
        new_path_points = [list(point.values()) for point in new_path_points]
        print(route_name)
        print(new_path_points)
        with open("path.json", "r") as f:
            path_json_string = f.read()
        path_json = json.loads(path_json_string)
        path_json[d['routeName']] = {"points": [{"name": '{:.0f}'.format(i), "coordinates": coordinates} for i, coordinates in enumerate(new_path_points)]}
        path_json_string = json.dumps(path_json)
        with open("path.json", "w") as f:
            f.write(path_json_string)
    else:
        # POST Error 405 Method Not Allowed
        pass
    return 'POST operation completed'

@app.route('/getFastestRoute', methods = ['POST'])
def get_fastest_route():
    if request.method == 'POST':
        data = request.form
        keys = list(data.to_dict().keys())
        d = json.loads(keys[0])
        from_coordinates = d['from_coordinates'].split(',')
        from_coordinates = [float(coordinate) for coordinate in from_coordinates]
        to_coordinates = d['to_coordinates'].split(',')
        to_coordinates = [float(coordinate) for coordinate in to_coordinates]
        closest_subpath = get_fastest_subpath(from_coordinates, to_coordinates)
    return json.dumps(closest_subpath), 200

def get_fastest_subpath(from_coordinates, to_coordinates):
    with open("path.json", "r") as f:
        path_json_string = f.read()
    path_json = json.loads(path_json_string)
    direct_distance = haversine(from_coordinates, to_coordinates)
    print("Direct distance between two points: {:.2f} km".format(direct_distance))
    closest_path_name, closest_subpath = get_closest_subpath(from_coordinates, to_coordinates, path_json)
    return {closest_path_name: closest_subpath}

def get_closest_subpath(from_coordinates, to_coordinates, path_json):
    closest_path_name, closest_path = get_closest_path(from_coordinates, to_coordinates, path_json)
    i = get_path_closest_distance_stop_index(from_coordinates, closest_path)
    j = get_path_closest_distance_stop_index(to_coordinates, closest_path)
    closest_subpath = closest_path
    i, j = min(i, j), max(i, j)
    closest_subpath['points'] = closest_subpath['points'][i: j+1]
    return closest_path_name, closest_subpath

def get_closest_path(from_coordinates, to_coordinates, path_json):
    path_from_distances = {path_name: get_path_closest_distance_stop(from_coordinates, path_json[path_name]) for path_name in path_json}
    path_to_distances = {path_name: get_path_closest_distance_stop(to_coordinates, path_json[path_name]) for path_name in path_json}
    path_sum_distances = {k: path_from_distances.get(k, 0) + path_to_distances.get(k, 0) for k in set(path_from_distances) | set(path_to_distances)}
    closest_path_name = min(path_sum_distances, key=path_sum_distances.get)
    return closest_path_name, path_json[closest_path_name]

def get_path_closest_distance_stop(coordinates, path):
    path_coordinate_sequence = [point['coordinates'] for point in path['points']]
    path_distance_sequence = [haversine(coordinates, point_coordinates) for point_coordinates in path_coordinate_sequence]
    return min(path_distance_sequence)

def get_path_closest_distance_stop_index(coordinates, path):
    path_coordinate_sequence = [point['coordinates'] for point in path['points']]
    path_distance_sequence = [haversine(coordinates, point_coordinates) for point_coordinates in path_coordinate_sequence]
    return path_distance_sequence.index(min(path_distance_sequence))

if __name__ == '__main__':
    app.run()
