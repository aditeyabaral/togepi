import os
import dotenv
from sqlalchemy import and_
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker


dotenv.load_dotenv()
engine = create_engine(os.environ["DB_URL"])
connection = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData()

repo_table = Table("repository", metadata, autoload=True, autoload_with=engine)
dev_table = Table("developer", metadata, autoload=True, autoload_with=engine)
file_table = Table("file", metadata, autoload=True, autoload_with=engine)
repo_user_table = Table("repositoryuserelation", metadata,
                        autoload=True, autoload_with=engine)


def checkUserRepositoryExists(user_id, repo_name):
    query = repo_table.select().where(
        and_(repo_table.c.owner_id == user_id, repo_table.c.name == repo_name))
    result = connection.execute(query).fetchall()
    return bool(result)


def getUsername(user_id):
    query = dev_table.select().where(dev_table.c._id == user_id)
    result = connection.execute(query).fetchall()[0][1]
    return result


def getAllUsername():
    all_users = session.query(dev_table.columns.username).all()
    return all_users


def getAllUserID():
    all_users = session.query(dev_table.columns._id).all()
    return all_users


def getAllRepositoryID():
    all_repos = session.query(repo_table.columns._id).all()
    return all_repos


def getAllFileID():
    all_files = session.query(file_table.columns._id).all()
    return all_files


def createUser(_id, username, email, password):
    query = dev_table.insert().values(_id=_id, username=username,
                                      email=email, password=password)
    result = connection.execute(query)
    print("New user successfully created.")


def checkUserCredentials(username, password):
    query = dev_table.select().where(dev_table.c.username == username)
    result = connection.execute(query).fetchall()

    if result:
        if password == result[0][-1]:
            print(f"Welcome back, {result[0][1]}")
            return result[0][0]
        else:
            print("Invalid password. Please try again.")
    else:
        print("Invalid username or password.")


def checkFileInDatabase(repo_id, filepath):
    query = file_table.select().where(
        and_(file_table.c.repository_id == repo_id, file_table.c.path == filepath))
    result = connection.execute(query).fetchall()
    return bool(result)


def createFile(_id, path, repository_id, status, last_modified=None, last_committed=None, last_pushed=None):
    query = file_table.insert().values(_id=_id, repository_id=repository_id, path=path,
                                       status=status, last_modified=last_modified, last_committed=last_committed, last_pushed=last_pushed)
    result = connection.execute(query)
    print(f"File {path} successfully tracked.")


def createRepository(user_id, repo_name, repo_id, description, url, create_time, visibility):
    query = repo_table.insert().values(_id=repo_id, owner_id=user_id, name=repo_name,
                                       description=description, url=url, create_time=create_time, visibility=visibility)
    result = connection.execute(query)
    print("New repository successfully created.")


def createUserRepositoryRelation(user_id, repo_id, relation="owner"):
    query = repo_user_table.insert().values(developer_id=user_id,
                                            repository_id=repo_id, relation=relation)
    result = connection.execute(query)
