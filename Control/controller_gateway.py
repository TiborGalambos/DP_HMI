import socket

from flask import Flask, jsonify, request

from Control.controller import Controller

app = Flask(__name__)
controller = Controller()
@app.route('/route_update', methods=['POST'])
def route_update():

    data = request.json
    print(data)

    controller.display_route(data)
    return jsonify({"status": "success", "message": "Route update received"}), 200

@app.route('/reset_message', methods=['POST'])
def reset_message():
    controller.reset()
    return jsonify({"status": "success", "message": "Route update received"}), 200


@app.route('/settings', methods=['POST'])
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
                            show_delay = show_delays)

    print("from gateway")
    print(use_display_1, use_display_2, speed, brightness, com_port, show_delays)
    return jsonify({"status": "success", "message": "Settings updated"}), 200


@app.route('/basic_message', methods=['POST'])
def basic_message():
    req = request.json
    message = req.get("message")
    print(message)

    controller.display_message(message=message)

    return jsonify({"status": "success", "message": "Basic message received"}), 200


@app.route('/controller_connectivity_test', methods=['GET'])
def self_test():
    return jsonify({"status": "success",}), 200

@app.route('/controller_internet_connectivity_test', methods=['GET'])
def test_internet():
    try:
        socket.setdefaulttimeout(5)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(('8.8.8.8', 53))
        return jsonify({"internet_status": "success", }), 200
    except socket.error as e:
        print(e)
        return jsonify({"internet_status": "fail", }), 503

@app.route('/controller_display_panel_1_test', methods=['GET'])
def test_ethernet_panel():
    try:
        if controller.test_ethernet_panel_connectivity():
            return jsonify({"ethernet_display_panel_connectivity": "success", }), 200
        else:
            return jsonify({"ethernet_display_panel_connectivity": "fail", }), 503
    except:
        return jsonify({"ethernet_display_panel_connectivity": "fail", }), 503

@app.route('/controller_display_panel_2_test', methods=['GET'])
def test_ibis_panel():
    try:
        if controller.test_ibis_panel_connectivity():
            return jsonify({"ibis_display_panel_connectivity": "success", }), 200
        else:
            return jsonify({"ibis_display_panel_connectivity": "fail", }), 503
    except:
        return jsonify({"ibis_display_panel_connectivity": "fail", }), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)