from logging import debug
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(
__name__,
static_url_path='', 
static_folder='public/static',
template_folder="public/views"
)
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
        username = request.form["loginUsername"]
        password = request.form["loginPassword"]
        existingUser = user.query.filter_by(username=username).first()
        if existingUser:
            if user.query.filter_by(username=username, password=password).first():
                return redirect("/user/<username>")
            else:
                return "Wrong username or password!"
        else:
            return "No register user with that username!"

    else:
        return render_template("index.html")

@app.route("/user/<username>/")

def userControl():
    return render_template("userlogin.html")

@app.route("/Admin/UserAdd/", methods=["POST", "GET"])

def userAdd():
    if request.method == "POST":
        newUsername = request.form["newUsername"] # Name and id in userAdd form should be "newUsername".
        newPassword = request.form["newPassword"] # Name and id in userAdd form should be "newPassword".

        if user.query.filter_by(username=newUsername).first():
            return "User already has that username!"
        else:
            newUser = user(username=newUsername, password=newPassword)
            db.session.add(newUser)
            db.session.commit()
            return redirect("/Admin/UserAdd/")

@app.route("/Admin/UserRemove/<int:id>/")

def userRemove(userId):
    findUser = user.query.filter_by(id=userId).first()
    if findUser:
        db.session.delete(findUser)
        db.session.commit()
        return redirect("/Admin/UserRemove/")
    else:
        print("User does not exist!")
        


if __name__ == "__main__":
    app.run(debug=True)