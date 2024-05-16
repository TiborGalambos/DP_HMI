import socket
from threading import Thread
from flask import Flask, jsonify, request
from jsonschema import validate, ValidationError
from Controller.controller import Controller

app = Flask(__name__)
controller = Controller()

# schemas for validation
route_update_schema = {
    "type": "object",
    "properties": {
        "routeID": {"type": "string"},
        "remaining_route_stations": {
            "type": "array",
            "items": {"type": "string"}
        },
        "destination_station": {"type": "string"},
        "state": {"type": "string"},
        "delay": {"type": "number"},
        "display_1": {"type": "boolean"},
        "display_2": {"type": "boolean"}
    },
    "required": ["routeID", "remaining_route_stations", "destination_station", "state"]
}

settings_schema = {
    "type": "object",
    "properties": {
        "display_1": {"type": "boolean"},
        "display_2": {"type": "boolean"},
        "show_delay": {"type": "boolean"},
        "brightness": {"type": "number"},
        "speed": {"type": "number"},
        "com_port": {"type": "number"}
    },
    "required": ["display_1", "display_2", "show_delay", "brightness", "speed", "com_port"]
}

message_schema = {
    "type": "object",
    "properties": {
        "message": {"type": "string"}
    },
    "required": ["message"]
}

# creating the decorator for the validation
def validate_json(schema):
    def decorator(f):
        def decorated_function(*args, **kwargs):
            try:
                validate(instance=request.json, schema=schema)
            except ValidationError as e:
                error_message = e.message
                return jsonify({"status": "error", "message": f"Validation error: {error_message}"}), 400
            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorated_function
    return decorator

@app.route('/route_update', methods=['POST'])
@validate_json(route_update_schema)
def route_update():
    data = request.json
    print(data)

    thread = Thread(target=controller.display_route, args=(data,))
    thread.start()
    return jsonify({"status": "success", "message": "Route update received"}), 200

@app.route('/reset_message', methods=['POST'])
def reset_message():
    thread = Thread(target=controller.reset)
    thread.start()
    return jsonify({"status": "success", "message": "Route update received"}), 200

@app.route('/settings', methods=['POST'])
@validate_json(settings_schema)
def update_settings():
    settings = request.json
    print(settings)

    use_display_1 = bool(settings.get("display_1"))
    use_display_2 = bool(settings.get("display_2"))
    speed = settings.get("speed")
    brightness = settings.get("brightness")
    com_port = settings.get("com_port")
    show_delays = settings.get("show_delay")

    controller.set_settings(display_1=use_display_1,
                            display2=use_display_2,
                            speed=speed,
                            brightness=brightness,
                            com_port=com_port,
                            show_delay=show_delays)

    print("from gateway")
    print(use_display_1, use_display_2, speed, brightness, com_port, show_delays)
    return jsonify({"status": "success", "message": "Settings updated"}), 200

@app.route('/basic_message', methods=['POST'])
@validate_json(message_schema)
def basic_message():
    req = request.json
    message = req.get("message")
    print(message)

    controller.display_message(message=message)
    return jsonify({"status": "success", "message": "Basic message received"}), 200

@app.route('/emergency_message', methods=['POST'])
@validate_json(message_schema)
def emergency_message():
    req = request.json
    message = req.get("message")
    print(message)

    controller.display_emergency(message=message)
    return jsonify({"status": "success", "message": "Emergency message received"}), 200

@app.route('/controller_connectivity_test', methods=['GET'])
def self_test():
    return jsonify({"status": "success"}), 200

@app.route('/controller_internet_connectivity_test', methods=['GET'])
def test_internet():
    try:
        socket.setdefaulttimeout(5)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(('8.8.8.8', 53))
        return jsonify({"internet_status": "success"}), 200
    except socket.error as e:
        print(e)
        return jsonify({"internet_status": "fail"}), 503

@app.route('/controller_display_panel_1_test', methods=['GET'])
def test_ethernet_panel():
    try:
        if controller.test_ethernet_panel_connectivity():
            return jsonify({"ethernet_display_panel_connectivity": "success"}), 200
        else:
            return jsonify({"ethernet_display_panel_connectivity": "fail"}), 503
    except:
        return jsonify({"ethernet_display_panel_connectivity": "fail"}), 503

@app.route('/controller_display_panel_2_test', methods=['GET'])
def test_ibis_panel():
    try:
        if controller.test_ibis_panel_connectivity():
            return jsonify({"ibis_display_panel_connectivity": "success"}), 200
        else:
            return jsonify({"ibis_display_panel_connectivity": "fail"}), 503
    except:
        return jsonify({"ibis_display_panel_connectivity": "fail"}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
