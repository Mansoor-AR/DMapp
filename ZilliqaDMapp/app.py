from flask import Flask
from flask import request
from flask import jsonify
import json
from haversine import haversine
import subprocess

app = Flask(__name__)


@app.route("/getbalance")
def get_balance():
    command = "node GetBalances.js"
    try:
        res = subprocess.check_output(command, shell = True)
        result = res.decode("utf-8") 
        toWrite = open("result_temp.html", "w")
        toWrite.write("<!DOCTYPE html><html><head><title>Current Balances</title><body><h2>Current Balances. Demo Only!</h2>")
        toprint = result.split('%')
        toWrite.write(toprint[0]+"<br>") 
        toWrite.write(toprint[1]+"<br>")
        toWrite.write(toprint[2]+"<br>")
        toWrite.write(toprint[3]+"<br>")
        toWrite.write(toprint[4]+"<br>")
        toWrite.write(toprint[5]+"<br>")
        toWrite.write(toprint[6]+"<br>")
        toWrite.write(toprint[7]+"<br>")
        toWrite.write("</body></html>")   
        toWrite.close()
        print("This is what we got from Kaya:")
        print(result)
        with open("result_temp.html", "r") as f:
            return f.read()
    except subprocess.CalledProcessError as e:
        print("An error occured: "+e)
        with open("result_temp.html", "r") as f:
            return f.read()
    except subprocess.SubprocessError as e:
        print("An error occured:" + e)



@app.route('/makepayment', methods=['POST'])
def make_payment():
    if request.method == 'POST':
        command = "node makepayment.js"
        try:
            res = subprocess.check_output(command, shell = True)
            result = res.decode("utf-8")
            print("Payment transaction from Kaya:")
            print(result)
        except subprocess.CalledProcessError as e:
            print("An error occured: "+e)
    else:
        # POST Error 405 Method Not Allowed
        print("Method not POST!")
        print(request)
        pass
    return 'POST operation completed'



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


@app.route('/submitRoute', methods=['POST'])
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
        path_json[d['routeName']] = {"points": [{"name": '{:.0f}'.format(
            i), "coordinates": coordinates} for i, coordinates in enumerate(new_path_points)]}
        path_json_string = json.dumps(path_json)
        with open("path.json", "w") as f:
            f.write(path_json_string)
    else:
        # POST Error 405 Method Not Allowed
        pass
    return 'POST operation completed'


@app.route('/getFastestRoute', methods=['POST'])
def get_fastest_route():
    if request.method == 'POST':
        data = request.form
        keys = list(data.to_dict().keys())
        d = json.loads(keys[0])
        from_coordinates = d['from_coordinates'].split(',')
        from_coordinates = [float(coordinate)
                            for coordinate in from_coordinates]
        to_coordinates = d['to_coordinates'].split(',')
        to_coordinates = [float(coordinate) for coordinate in to_coordinates]
        closest_subpath = get_fastest_subpath(from_coordinates, to_coordinates)
    return json.dumps(closest_subpath), 200


def get_fastest_subpath(from_coordinates, to_coordinates):
    with open("path.json", "r") as f:
        path_json_string = f.read()
    path_json = json.loads(path_json_string)
    direct_distance = haversine(from_coordinates, to_coordinates)
    print("Direct distance between two points: {:.2f} km".format(
        direct_distance))
    closest_path_name, closest_subpath = get_closest_subpath(
        from_coordinates, to_coordinates, path_json)
    return {closest_path_name: closest_subpath}


def get_closest_subpath(from_coordinates, to_coordinates, path_json):
    closest_path_name, closest_path = get_closest_path(
        from_coordinates, to_coordinates, path_json)
    i = get_path_closest_distance_stop_index(from_coordinates, closest_path)
    j = get_path_closest_distance_stop_index(to_coordinates, closest_path)
    closest_subpath = closest_path
    i, j = min(i, j), max(i, j)
    closest_subpath['points'] = closest_subpath['points'][i: j+1]
    return closest_path_name, closest_subpath


def get_closest_path(from_coordinates, to_coordinates, path_json):
    path_from_distances = {path_name: get_path_closest_distance_stop(
        from_coordinates, path_json[path_name]) for path_name in path_json}
    path_to_distances = {path_name: get_path_closest_distance_stop(
        to_coordinates, path_json[path_name]) for path_name in path_json}
    path_sum_distances = {k: path_from_distances.get(k, 0) + path_to_distances.get(
        k, 0) for k in set(path_from_distances) | set(path_to_distances)}
    closest_path_name = min(path_sum_distances, key=path_sum_distances.get)
    return closest_path_name, path_json[closest_path_name]


def get_path_closest_distance_stop(coordinates, path):
    path_coordinate_sequence = [point['coordinates']
                                for point in path['points']]
    path_distance_sequence = [haversine(
        coordinates, point_coordinates) for point_coordinates in path_coordinate_sequence]
    return min(path_distance_sequence)


def get_path_closest_distance_stop_index(coordinates, path):
    path_coordinate_sequence = [point['coordinates']
                                for point in path['points']]
    path_distance_sequence = [haversine(
        coordinates, point_coordinates) for point_coordinates in path_coordinate_sequence]
    return path_distance_sequence.index(min(path_distance_sequence))


if __name__ == '__main__':
    app.run()
