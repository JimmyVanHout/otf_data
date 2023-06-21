from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route("/user_interface", methods=["GET", "POST"])
def user_interface():
    if request.method == "GET":
        return render_template("user_interface.html")
    else:
        with open("user_input.json", "w") as file:
            file.write(json.dumps(request.form))
        return render_template("submitted.html")
