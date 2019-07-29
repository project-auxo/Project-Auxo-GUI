import actuate_bbb
from flask import Flask, request, abort

app = Flask(__name__)
bbb = actuate_bbb.BBB()


# Launch the mdagent
@app.route("/")
def index():
    return "Empty"

# Change LED via post request
@app.route("/change_led_status", methods=["POST"])
def change_led_status():
    status = int(request.form['status'])

    if status in [0, 1]:
        bbb.change_led(status)
    else:
        abort(500)

    return "OK"


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
