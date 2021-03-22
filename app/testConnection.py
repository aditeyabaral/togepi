import os
import time
import dotenv
from sqlalchemy import create_engine, MetaData, Table, insert

dotenv.load_dotenv()
engine = create_engine("postgresql://kepemjzojleuqu:d332cdc4377408f8a7546ba4d5105800a306ae81f1152111a5ce34c754ce8ccb@ec2-107-22-245-82.compute-1.amazonaws.com:5432/ddq1diapa4e65i")
connection = engine.connect()

print(connection)