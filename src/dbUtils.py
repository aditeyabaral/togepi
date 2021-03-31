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


def checkUserRepositoryExists(user_id, repo_name):
    table = Table("repository", metadata, autoload=True, autoload_with=engine)
    # change this to table.select
    query = table.select().where(
        and_(table.c.owner_id == user_id, table.c.name == repo_name))
    result = connection.execute(query).fetchall()
    return bool(result)


def getUsername(user_id):
    table = Table("developer", metadata, autoload=True, autoload_with=engine)
    # change this to table.select
    query = table.select().where(table.c._id == user_id)
    result = connection.execute(query).fetchall()[0][1]
    return result


def getAllUserID():
    table = Table("developer", metadata, autoload=True, autoload_with=engine)
    # change this to table.select
    all_users = session.query(table.columns._id).all()
    return all_users


def getAllRepositoryID():
    table = Table("repository", metadata, autoload=True, autoload_with=engine)
    # change this to table.select
    all_repos = session.query(table.columns._id).all()
    return all_repos


def createUser(_id, username, email, password):
    table = Table("developer", metadata, autoload=True, autoload_with=engine)
    query = table.insert().values(_id=_id, username=username,
                                  email=email, password=password)
    result = connection.execute(query)
    print("New user successfully created.")


def checkUserCredentials(username, password):
    table = Table("developer", metadata, autoload=True, autoload_with=engine)
    query = table.select().where(table.c.username == username)
    result = connection.execute(query).fetchall()

    if result:
        if password == result[0][-1]:
            print(f"Welcome back, {result[0][1]}")
            return result[0][0]
        else:
            print("Invalid password. Please try again.")
    else:
        print("Invalid username or password.")


def createRepository(user_id, repo_name, repo_id, description, url, create_time, visibility):
    table = Table("repository", metadata, autoload=True, autoload_with=engine)
    query = table.insert().values(_id=repo_id, owner_id=user_id, name=repo_name,
                                  description=description, url=url, create_time=create_time, visibility=visibility)
    result = connection.execute(query)
    print("New repository successfully created.")


def createUserRepositoryRelation(user_id, repo_id, relation="owner"):
    table = Table("repositoryuserelation", metadata,
                  autoload=True, autoload_with=engine)
    query = table.insert().values(developer_id=user_id,
                                  repository_id=repo_id, relation=relation)
    result = connection.execute(query)


def createFile(user_id, repo_name, repo_id, description, url, create_time, visibility):
    table = Table("repository", metadata, autoload=True, autoload_with=engine)
    query = table.insert().values(_id=repo_id, owner_id=user_id, name=repo_name,
                                  description=description, url=url, create_time=create_time, visibility=visibility)
    result = connection.execute(query)
    print("New repository successfully created.")