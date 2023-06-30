import brain
import connectToMongo
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
import bcrypt
import os
from flask import Flask, render_template, request, url_for, redirect, session


# ############   connectToMongo object    ############
test_client = MongoClient(os.getenv('ATLAS_URI'))
tutor_db = test_client['tutorDB']
data = connectToMongo.ConnectToMongo()

# users' login data collection
records = tutor_db["col_login"]

brain.executeEveryXminute()

# ##########    webpage part    #############
app = Flask(__name__)
app.secret_key = "testing"


@app.route("/", methods=['post', 'get'])
def index():
    message = ''
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        email = request.form.get("email")

        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_found = records.find_one({"email": email})

        if email_found:
            message = 'This email already exists in database'
            return render_template('index.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('index.html', message=message)
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'email': email, 'password': hashed}
            records.insert_one(user_input)
            return redirect(url_for("login"))

    return render_template('index.html')


@app.route('/logged_in', methods=["POST", "GET"])
def logged_in():
    if "email" in session:
        user_email = session["email"]

        tutors_col = data.tutor_db[user_email].find({})

        # add or delete a tutor ID in MongoDB
        if request.method == "POST":
            if request.form.getlist('add') == [""]:
                # adding a new tutor
                data.Add(int(request.form.get("tutorID")), user_email)
            if request.form.getlist("delete") == [""]:
                data.Remove(int(request.form.get("tutorID")), user_email)

        return render_template('logged_in.html', email=user_email, tutors=tutors_col)
    else:
        return redirect(url_for("login"))


@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            password_check = email_found['password']

            if bcrypt.checkpw(password.encode('utf-8'), password_check):
                session["email"] = email_val
                return redirect(url_for('logged_in'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("signout.html")
    else:
        return render_template('index.html')


if __name__ == "__main__":
    # app.run(debug=True, use_reloader=False)
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
