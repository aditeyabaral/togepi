import os
import dotenv
from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy

dotenv.load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DB_URL"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    _id = db.Column(db.String(26), primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __init__(self, name, email, password, user_id) -> None:
        self.username = name
        self.email = email
        self._id = user_id  # Check database
        self.password = password


class Repository(db.Model):
    __tablename__ = "repository"
    _id = db.Column(db.String(26), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100))
    url = db.Column(db.String(1024), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    visibility = db.Column(db.String(10), nullable=False)
    owner_id = db.Column(db.String(1024), db.ForeignKey(
        'user._id', ondelete='CASCADE'), nullable=False)
    # user_relation = db.relationship("user", back_populates="repository")

    def __init__(self, repo_name, visibility, repo_id, url, owner_id, create_time, description=None) -> None:
        self.name = repo_name
        self.visibility = visibility
        self._id = repo_id  # check with database
        self.url = url
        self.create_time = create_time
        self.description = description
        self.owner_id = owner_id


class OwnerRepositoryRelation(db.Model):
    __tablename__ = "repositoryuserelation"
    user_id = db.Column(db.String(26), db.ForeignKey(
        'user._id'), primary_key=True)  # Check cascade
    repository_id = db.Column(db.String(26), db.ForeignKey(
        'repository._id', ondelete='CASCADE'), primary_key=True)
    relation = db.Column(db.String(20), nullable=False)
    # user_relation = db.relationship("user", back_populates="repositoryuserelation")
    # repository_relation = db.relationship("repository", back_populates="repositoryuserelation")

    def __init__(self, user_id, repository_id, relation) -> None:
        self.user_id = user_id
        self.repository_id = repository_id
        self.relation = relation


class File(db.Model):
    __tablename__ = "file"
    path = db.Column(db.String(26), nullible=False, primary_key=True)
    repository_id = db.Column(db.String(26), nullable=False, primary_key=True)
    status = db.Column(db.String(15), nullable=False)
    last_modified = db.Column(db.DateTime, nullable=False)
    last_committed = db.Column(db.DateTime)
    last_pushed = db.Column(db.DateTime)
    

    def __init__(self, path, repository_id, status="unchanged", last_modified=None, last_committed=None, last_pushed=None) -> None:
        self.path = path
        self.repository_id = repository_id
        self.status = status
        self.last_modified = last_modified
        self.last_committed = last_committed
        self.last_pushed = last_pushed


@app.route("/", methods=["GET", "POST"])
def home():
    return redirect("https://github.com/aditeyabaral/version-control", 302)


if __name__ == "__main__":
    app.run()
