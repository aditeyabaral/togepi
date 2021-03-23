import os
import dotenv
from sqlalchemy import create_engine, MetaData, Table, insert

dotenv.load_dotenv()
engine = create_engine(os.environ["DB_URL"])
connection = engine.connect()

print(connection)