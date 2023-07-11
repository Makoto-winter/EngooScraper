import brain
import connectToMongo
from pymongo import MongoClient
from dotenv import load_dotenv
import password_checker

load_dotenv()
import bcrypt
import os
from flask import Flask, render_template, request, url_for, redirect, session, flash

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
    return render_template('top.html')


@app.route("/register", methods=['post', 'get'])
def register():
    message = ''
    if "email" in session:
        return redirect(url_for('logged_in'))
    if request.method == "POST":
        email = request.form.get("email")

        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_found = records.find_one({"email": email})

        if str(email).split('@')[-1] != ("gmail.com" or "yahoo.com" or "yahoo.co.jp" or "outlook.com" or "hotmail.com"):
            print(str(email).split('@')[-1])
            message = "You can only use gmail.com, yahoo.com, yahoo.co.jp, outlook.com or hotmail.com!"
            return render_template('pages-register.html', message=message)
        elif email_found:
            message = 'This email already exists in our database.'
            return render_template('pages-register.html', message=message)
        elif password1 != password2:
            message = 'Passwords should match!'
            return render_template('pages-register.html', message=message)
        else:
            if password_checker.password_check(password1):
                hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
                user_input = {'email': email, 'password': hashed}
                records.insert_one(user_input)
                return render_template('pages-redirect-login.html')
            else:
                message = 'Your password does not satisfy the requirement!'
                return render_template('pages-register.html', message=message)

    return render_template('pages-register.html')


@app.route('/logged_in', methods=["POST", "GET"])
def logged_in():
    if "email" in session:
        user_email = session["email"]

        tutors_col = data.tutor_db[user_email].find({})

        # add or delete a tutor ID in MongoDB
        try:
            if request.method == "POST":

                # adding a tutor
                if request.form.getlist('add') == [""]:
                    # extracting ID from the input address sucha as
                    # https://engoo.com/tutors/37327
                    # https://eikaiwa.dmm.com/teacher/index/49833/
                    try:
                        tutorID = int(str(request.form.get("tutor_address")).split('/')[-2])
                    except:
                        tutorID = int(str(request.form.get("tutor_address")).split('/')[-1])
                    finally:
                        # adding a new tutor
                        data.Add(tutorID, user_email)
                # deleting a tutor
                elif request.form.getlist("delete") == [""]:
                    data.Remove(int(request.form.get("tutorID")), user_email)

        # if the tutor does not exist, return to logged_in page.
        except:
            return render_template('pages-redirect-non-existent-tutor.html')

        return render_template('tables-data.html', email=user_email, tutors=tutors_col)
    else:
        return redirect(url_for("login"))


@app.route("/login", methods=["POST", "GET"])
def login():
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
                message = 'Email found. Wrong password'
                return render_template('pages-login.html', message=message)
        else:
            message = 'The input credentials do not exist.'
            return render_template('pages-login.html', message=message)
    return render_template('pages-login.html')


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template('pages-redirect-signout-home.html')
    else:
        return render_template('index.html')


@app.route("/terms", methods=["POST", "GET"])
def terms():
    return render_template('terms.html')


if __name__ == "__main__":
    # app.run(debug=True, use_reloader=False)
    from waitress import serve

    serve(app, host="0.0.0.0", port=8080)
