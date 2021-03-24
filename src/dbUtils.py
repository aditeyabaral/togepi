import os
import dotenv
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker


dotenv.load_dotenv()
engine = create_engine(os.environ["DB_URL"])
connection = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

metadata = MetaData()


def getAllUserID():
    table = Table("developer", metadata, autoload=True, autoload_with=engine)
    # change this to table.select
    all_users = session.query(table.columns._id).all()
    return all_users


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
