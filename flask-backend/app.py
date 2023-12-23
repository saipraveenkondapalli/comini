from flask import Flask, request, jsonify, render_template, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
import os


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app
db = SQLAlchemy(app)

CORS(app, resources={r"/*": {"origins": "*"}})


login_manger = LoginManager()
login_manger.init_app(app)


class NewsArticle(db.Model):
    __tablename__ = "NewsArticle"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    url = db.Column(db.String(500), unique=True, nullable=False)
    new_title = db.Column(db.String(500), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    new_summary = db.Column(db.Text, nullable=False)


@login_manger.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


class User(db.Model, UserMixin):
    __tablename__ = "NewsUser"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.Text, nullable=False)


@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    news_articles = NewsArticle.query.all()
    return render_template("dashboard.html", articles=news_articles)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            return render_template("login.html", error="Invalid username/password")

        login_user(user)
        return redirect("/dashboard")

    return render_template("login.html")


@app.route("/logout", methods=["GET"])
def logout():
    logout_user()


@app.route("/register", methods=["GET", "POST"])
def register():
    new_user = User(
        username="guest@saipraveen.software",
        password=generate_password_hash("guest@12345"),
    )
    db.session.add(new_user)
    db.session.commit()
    return redirect("/login")


@app.route("/new", methods=["POST"])
def news():
    payload = request.get_json()
    new_news = NewsArticle(**payload)
    db.session.add(new_news)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "already exists"}), 409
    return jsonify({"message": "created"}), 201


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()


