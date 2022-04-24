import os
import dotenv
from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from eralchemy import render_er

dotenv.load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ""
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Developer(db.Model):
    __tablename__ = "developer"
    _id = db.Column(db.String(26), primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __init__(self, name, email, password, developer_id) -> None:
        self.username = name
        self.email = email
        self._id = developer_id
        self.password = password


class Repository(db.Model):
    __tablename__ = "repository"
    _id = db.Column(db.String(26), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(150))
    url = db.Column(db.String(1024), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    visibility = db.Column(db.String(10), nullable=False)
    owner_id = db.Column(db.String(1024), db.ForeignKey(
        'developer._id', ondelete='CASCADE'), nullable=False)
    # user_relation = db.relationship("user", back_populates="repository")

    def __init__(self, repo_name, visibility, repo_id, url, owner_id, create_time, description=None) -> None:
        self._id = repo_id
        self.name = repo_name
        self.description = description
        self.url = url
        self.create_time = create_time
        self.visibility = visibility
        self.owner_id = owner_id


class OwnerRepositoryRelation(db.Model):
    __tablename__ = "repositoryuserelation"
    developer_id = db.Column(db.String(26), db.ForeignKey(
        'developer._id'), primary_key=True)  # Check cascade
    repository_id = db.Column(db.String(26), db.ForeignKey(
        'repository._id', ondelete='CASCADE'), primary_key=True)
    relation = db.Column(db.String(20), nullable=False)
    # user_relation = db.relationship("user", back_populates="repositoryuserelation")
    # repository_relation = db.relationship("repository", back_populates="repositoryuserelation")

    def __init__(self, developer_id, repository_id, relation) -> None:
        self.developer_id = developer_id
        self.repository_id = repository_id
        self.relation = relation


class File(db.Model):
    __tablename__ = "file"
    _id = db.Column(db.String(26), primary_key=True)
    path = db.Column(db.String(100), nullable=False)
    repository_id = db.Column(db.String(26), db.ForeignKey(
        'repository._id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.String(15), nullable=False)
    last_modified = db.Column(db.DateTime)
    last_committed = db.Column(db.DateTime)
    last_pushed = db.Column(db.DateTime)

    def __init__(self, _id, path, repository_id, status, last_modified=None, last_committed=None, last_pushed=None) -> None:
        self._id = _id
        self.path = path
        self.repository_id = repository_id
        self.status = status
        self.last_modified = last_modified
        self.last_committed = last_committed
        self.last_pushed = last_pushed


class Commit(db.Model):
    __tablename__ = "commit"
    _id = db.Column(db.String(26), primary_key=True)
    developer_id = db.Column(db.String(26), db.ForeignKey(
        'developer._id', ondelete='CASCADE'))
    repository_id = db.Column(db.String(26), db.ForeignKey(
        'repository._id', ondelete='CASCADE'), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.String(100))
    file_id = db.Column(db.String(26), db.ForeignKey(
        'file._id', ondelete='CASCADE'), primary_key=True)

    def __init__(self, _id, developer_id, repository_id, time, file_id, message=None) -> None:
        self._id = _id
        self.developer_id = developer_id
        self.repository_id = repository_id
        self.time = time
        self.file_id = file_id
        self.message = message


@app.route("/", methods=["GET", "POST"])
def home():
    return redirect("https://github.com/aditeyabaral/version-control", 302)


if __name__ == "__main__":
    render_er(db.Model, 'model_erd.png')

    app.run()
