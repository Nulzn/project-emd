from logging import debug
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from cryptography.fernet import Fernet

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///SERVER.db"
db = SQLAlchemy(app)

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<User %r>" % self.id

@app.route("/", methods=["POST", "GET"])

def loginPage():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        key = Fernet.generate_key()
        f = Fernet(key)
        storedPassword = f.encrypt(password)
        existingUser = user.query.filter_by(username=username).first()
        if existingUser is None:
            return "No register user with that username!"
        else:
            if user.query.filter_by(username=username, password=storedPassword).first():
                return redirect("/user/<username>/")
            else:
                return "Wrong username or password!"

    else:
        return render_template("/public/views/userlogin.html")

@app.route("/user/<username>/", methods=["POST", "GET"])

def userControl():
    return render_template("/public/views/userview.html")

@app.route("/Admin/UserAdd/", methods=["POST", "GET"])

def userAdd():
    newUsername = request.form["newUsername"]
    newPassword = request.form["newPassword"]

    if user.query.filter_by(username=newUsername).first():
        return "User already has that username!"
    else:
        key = Fernet.generate_key()
        f = Fernet(key)
        newHashedPassword = f.encrypt(newPassword)
        newUser = user(username=newUsername, password=newHashedPassword)
        db.session.add(newUser)
        db.session.commit()
        return redirect("/Admin/UserAdd/")

@app.route("/Admin/UserRemove/<int:id>/")

def userRemove(userId):
    findUser = user.query.filter_by(id=userId).first()
    if findUser is None:
        print("User does not exist!")
    else:
        db.session.delete(findUser)
        db.session.commit()
        return redirect("/Admin/UserRemove/")


if __name__ == "__main__":
    app.run(debug=True)