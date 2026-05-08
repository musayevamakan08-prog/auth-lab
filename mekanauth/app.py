from flask import Flask, render_template, request
import time

app = Flask(__name__)

# İstifadəçiləri yüklə
def load_users():

    users = {}

    with open("users.txt", "r") as file:

        for line in file:

            username, password = line.strip().split(":")

            users[username] = password

    return users


@app.route("/", methods=["GET", "POST"])
def login():

    message = ""

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        users = load_users()

        # USERNAME ENUMERATION
        if username not in users:

            message = "User does not exist"

        else:

            # PASSWORD CHECK
            if users[username] == password:

                message = "Login successful"

            else:

                # AUTHENTICATION FAILURE
                message = "Incorrect password"

                # BRUTE FORCE mümkün olur
                time.sleep(1)

    return render_template("login.html", message=message)


if __name__ == "__main__":

    app.run(debug=True)