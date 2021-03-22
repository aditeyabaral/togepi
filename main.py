import utils
import datetime


class Repository:
    def __init__(self, repo_name, visibility) -> None:
        self.repo_name = repo_name
        self.visibility = visibility
        self.repo_id = utils.getRandomID()  # check with database
        self.repo_url = utils.getRepoURL(self.repo_name, self.repo_id)
        self.date_created = datetime.datetime.now()

    def setRepositoryName(self, new_name):
        if self.repo_name != new_name:
            prompt = f"Do you want to change the name of the repository from {self.repo_name} to {new_name}? [y/n]"
            choice = input(prompt)
            if choice.lower() == 'y':
                self.repo_name = new_name
            else:
                print("Changed discarded.")
        else:
            print("New name is the same as the old name.")

    def setVisibility(self, new_visibility):
        if self.visibility == new_visibility:
            prompt = f"Do you want to change the visibility of the repository from {self.visibility} to {new_visibility}? [y/n]"
            choice = input(prompt)
            if choice.lower() == 'y':
                self.visibility = new_visibility
            else:
                print("Changed discarded.")
        else:
            print("New visibility permission is the same as the old permission.")

    def deleteRepository(self):
        # delete from database
        pass


class User:
    def __init__(self, name, email, password) -> None:
        self.username = name
        self.email = email
        self.owner_repositories = list()
        self.collaborator_repositories = list()
        self.user_id = utils.getRandomID()  # Create new database for user Ids?
        self.password = password

    def createRepository(self, repo_name, visibility):
        repository = Repository(repo_name, visibility)
        self.owner_repositories.append(repository)

