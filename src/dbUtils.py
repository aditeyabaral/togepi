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

class DataBase:
    repo_table = Table("repository", metadata, autoload=True, autoload_with=engine)
    commit_table = Table("commit", metadata, autoload=True, autoload_with=engine)
    dev_table = Table("developer", metadata, autoload=True, autoload_with=engine)
    file_table = Table("file", metadata, autoload=True, autoload_with=engine)
    repo_user_table = Table("repositoryuserelation", metadata,
                                autoload=True, autoload_with=engine)
    def __init__(self):
        pass
    
class fileDBUtils(DataBase):
    def __init__(self):
        super().__init__()
    
    def createFile(self, _id, path, repository_id, status, last_modified=None, last_committed=None, last_pushed=None):
        query = self.file_table.insert().values(_id=_id, repository_id=repository_id, path=path,
                                        status=status, last_modified=last_modified, last_committed=last_committed, last_pushed=last_pushed)
        result = connection.execute(query)
        print(f"File {path} successfully tracked.")

    def getTrackedFiles(self, repo_id):
        query = self.file_table.select().where(self.file_table.c.repository_id == repo_id)
        result = connection.execute(query).fetchall()
        tracked_files = list()
        for f in result:
            tracked_files.append(f[1])
        return tracked_files
    
    def getAllFileID(self):
        all_files = session.query(self.file_table.columns._id).all()
        return all_files

    def getFileID(self, repo_id, fname):
        query = self.file_table.select().where(
            and_(self.file_table.c.repository_id == repo_id, self.file_table.c.path == fname))
        result = connection.execute(query).fetchall()
        return result[0][0]

    def checkFileInDatabase(self, repo_id, filepath):
        query = self.file_table.select().where(
            and_(self.file_table.c.repository_id == repo_id, self.file_table.c.path == filepath))
        result = connection.execute(query).fetchall()
        return bool(result)
    
    def updateFileModifiedTime(self, repo_id, fname, last_modified_time):
        query = self.file_table.update().where(and_(self.file_table.c.repository_id == repo_id,
                                            self.file_table.c.path == fname)).values(last_modified=last_modified_time)

        result = connection.execute(query)

        query = self.file_table.update().where(and_(self.file_table.c.repository_id == repo_id,
                                            self.file_table.c.path == fname)).values(status="modified")
        result = connection.execute(query)


    def updateFileCommitTime(self, repo_id, modified_file, last_committed_time):
        query = self.file_table.update().where(and_(self.file_table.c.repository_id == repo_id,
                                            self.file_table.c.path == modified_file)).values(last_committed=last_committed_time)
        result = connection.execute(query)


    def updateFilePushTime(self, repo_id, filename, last_pushed_time):
        query = self.file_table.update().where(and_(self.file_table.c.repository_id == repo_id,
                                            self.file_table.c.path == filename)).values(last_pushed=last_pushed_time)

        result = connection.execute(query)

        query = self.file_table.update().where(and_(self.file_table.c.repository_id == repo_id,
                                            self.file_table.c.path == filename)).values(status="unchanged")
        result = connection.execute(query)


    def getLastModifyTime(self, repo_id, fname):
        query = self.file_table.select().where(
            and_(self.file_table.c.repository_id == repo_id, self.file_table.c.path == fname))
        result = connection.execute(query).fetchall()
        print(result)
        return result[0][4]

