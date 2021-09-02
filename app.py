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
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db = SQLAlchemy(app)

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    first_second_name = db.Column(db.String(200), nullable=False)
    age = db.Column(db.String(3), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<User %r>" % self.id

if user.query.filter_by(username="admin").first():
    pass
else:
    admin = user(username="admin", password="123", first_second_name="Administrator", age="Unknown") #username: admin | password: 123
    db.session.add(admin)
    db.session.commit()

@app.route("/", methods=["POST", "GET"])


def loginPage():
    if request.method == "POST":
        usernameLogin = request.form["loginUsername"]
        passwordLogin = request.form["loginPassword"]
        existingUser = user.query.filter_by(username=usernameLogin).first()
        if existingUser:
            if user.query.filter_by(username=usernameLogin, password=passwordLogin).first():
                if usernameLogin == "admin":
                    return redirect(url_for(".adminPanel", username=usernameLogin))
                else:
                    return redirect("/user/panel")
            else:
                return "Wrong username or password!"
        else:
            return "No register user with that username!"

    else:
        return render_template("index.html")

@app.route("/user/panel")

def userControl():
    return render_template("userlogin.html")

@app.route("/admin/panel", methods=["POST", "GET"])

def adminPanel():
    if request.method == "POST":
        pass
    else:
        doctors = user.query.order_by(user.date_created).all()
        try:
            usernameReq = request.args["username"]
            return render_template("adminview.html", doctors=doctors, username=usernameReq)
        except:
            return render_template("adminview.html", doctors=doctors)

@app.route("/admin/userAdd/", methods=["POST", "GET"])

def userAdd():
    if request.method == "POST":
        newUsername = request.form["newUsername"] # Name and id in userAdd form should be "newUsername".
        newPassword = request.form["newPassword"] # Name and id in userAdd form should be "newPassword".
        first_second_name = request.form["firstAndSecondName"] # Name and id in userAdd form should be "firstAndSecondName".
        age = request.form["age"] # Name and id in userAdd form should be "age".
        print(f"{newUsername} {newPassword}")

        if user.query.filter_by(username=newUsername).first():
            return "User already has that username!"
        else:
            newUser = user(username=newUsername, password=newPassword, first_second_name=first_second_name, age=age)
            db.session.add(newUser)
            db.session.commit()
            return redirect("/admin/panel")
    else:
        return render_template("userAdd.html")

@app.route("/admin/<int:id>") # Doesn't work. Needs to be fixed!

def userRemove(id):
    findUser = user.query.get_or_404(id)
    if findUser:
        db.session.delete(findUser)
        db.session.commit()
        return redirect("/admin/panel")
    else:
        print("User does not exist!")
        


if __name__ == "__main__":
    app.run(debug=True)