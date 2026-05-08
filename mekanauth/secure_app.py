from flask import Flask, render_template, request
import bcrypt
import logging
import time

app = Flask(__name__)

# Failed attempt tracking
failed_attempts = {}

# Maksimum cəhd
MAX_ATTEMPTS = 3

# Logging sistemi
logging.basicConfig(
    filename="security.log",
    level=logging.INFO,
    format="%(asctime)s %(message)s"
)

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

        ip = request.remote_addr

        # Account lockout
        if username in failed_attempts:

            if failed_attempts[username] >= MAX_ATTEMPTS:

                logging.warning(
                    f"BLOCKED ACCOUNT: {username} IP:{ip}"
                )

                message = "Too many failed attempts"

                return render_template(
                    "secure_login.html",
                    message=message
                )

        # Generic error message
        generic_error = "Invalid username or password"

        # Username enumeration prevention
        if username not in users:

            message = generic_error

            logging.warning(
                f"FAILED LOGIN unknown user IP:{ip}"
            )

            time.sleep(1)

            return render_template(
                "secure_login.html",
                message=message
            )

        stored_hash = users[username].encode()

        # Password hash verification
        if bcrypt.checkpw(
            password.encode(),
            stored_hash
        ):

            message = "Secure login successful"

            failed_attempts[username] = 0

            logging.info(
                f"SUCCESSFUL LOGIN {username} IP:{ip}"
            )

        else:

            if username not in failed_attempts:

                failed_attempts[username] = 0

            failed_attempts[username] += 1

            message = generic_error

            logging.warning(
                f"FAILED LOGIN {username} IP:{ip}"
            )

            # Brute force yavaşlatma
            time.sleep(2)

    return render_template(
        "secure_login.html",
        message=message
    )


if __name__ == "__main__":

    app.run(debug=True, port=5001)