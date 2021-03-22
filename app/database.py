import os
import dotenv
import datetime
from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from utils import *

dotenv.load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DB_KEY"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    _id = db.Column(db.String(26), primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __init__(self, name, email, password) -> None:
        self.username = name
        self.email = email
        self.user_id = getRandomID()  # Check database
        self.password = password


class Repository(db.Model):
    __tablename__ = "repository"
    _id = db.Column(db.String(26), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(1024), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    visibility = db.Column(db.String(10), nullable=False)
    owner_id = db.Column(db.String(1024), db.ForeignKey(
        'user._id', ondelete='CASCADE'), nullable=False)
    # user_relation = db.relationship("user", back_populates="repository")

    def __init__(self, repo_name, visibility) -> None:
        self.name = repo_name
        self.visibility = visibility
        self._id = getRandomID()  # check with database
        self.url = getRepoURL(self.name, self._id)
        self.create_time = datetime.utcnow()


class OwnerRepositoryRelation(db.Model):
    __tablename__ = "repositoryuserelation"
    _id = db.Column(db.String(26), primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(26), db.ForeignKey(
        'user._id'), nullable=False)  # Check cascade
    repository_id = db.Column(db.String(26), db.ForeignKey(
        'repository._id', ondelete='CASCADE'), nullable=False)
    relation = db.Column(db.String(20), nullable=False)
    # user_relation = db.relationship("user", back_populates="repositoryuserelation")
    # repository_relation = db.relationship("repository", back_populates="repositoryuserelation")

    def __init__(self, user_id, repository_id, relation) -> None:
        self.user_id = user_id
        self.repository_id = repository_id
        self.relation = relation


@app.route("/", methods=["GET", "POST"])
def home():
    return redirect("https://github.com/aditeyabaral/version-control", 302)


if __name__ == "__main__":
    app.run()
