from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import userUtils
import repoUtils
import validationUtils
import cliUtils
import os
os.environ["APP_DIR"] = os.getcwd()

cache = {
    "current_user_id": None,
    "current_username": None,
    "current_repository_id": None,
    "current_repository_name": None
}


def getDirectoryDialog():
    global cache
    dir_path = filedialog.askdirectory()
    print(dir_path)
    try:
        info = open(f"{dir_path}/.togepi/tgpinfo.txt", 'r').read().split('\n')
        cache["current_repository_id"] = info[0].split(",")[1]
        cache["current_repository_name"] = info[1].split(",")[1]
    except:
        pass
    return dir_path


class HomeApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("Togepi")
        self.root.configure(background="#d2d2c9")
        # self.root.geometry("480x640")

        self.username = None
        self.user_id = None
        self.repository_id = None
        self.repository_name = None

        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()
        self.welcome = Label(self.root, text="Togepi", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 80))
        self.welcome.pack()
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()

        self.welcome = Label(
            self.root, text="Welcome to Togepi\nPlease login or sign up to proceed", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()

        self.signup_button_choice = Button(
            self.root,
            text="SIGN UP",
            command=self.signUp,
            bg="#4759b8",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.signup_button_choice.config(height=2, width=30, borderwidth=0)
        self.signup_button_choice.pack(side=TOP, expand=1)
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()

        self.login_button_choice = Button(
            self.root,
            text="LOGIN",
            command=self.logIn,
            bg="#4759b8",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.login_button_choice.config(height=2, width=30, borderwidth=0)
        self.login_button_choice.pack(side=TOP, expand=1)
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()

        self.exit_button_choice = Button(
            self.root,
            text="EXIT",
            command=self.onCloseRoot,
            bg="#4759b8",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.exit_button_choice.config(height=2, width=30, borderwidth=0)
        self.exit_button_choice.pack(side=TOP, expand=1)
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.onCloseRoot)
        self.root.mainloop()

    def onCloseWindow(self):
        self.window.destroy()

    def onCloseRoot(self):
        self.root.destroy()

    def loadHome(self):
        self.onCloseRoot()
        HomeApp()

    def verifyLoginCredentials(self):
        global cache
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        self.user_id, self.username = userUtils.loginUser(
            [self.username, self.password])
        print(self.username, self.password)
        if self.username is None:
            messagebox.showerror("Error", "Incorrect username or password")
        else:
            cache["current_user_id"] = self.user_id
            cache["current_username"] = self.username
            self.onCloseRoot()
            MainApp(self.user_id, self.username)

    def verifySignupCredentials(self):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        self.email = self.email_entry.get()
        print(self.username, self.password, self.email)
        unamevalidate = validationUtils.validateUsername(self.username)
        pwdvalidate = validationUtils.validatePassword(self.password)
        emailvalidate = validationUtils.validateEmail(self.email)
        print(unamevalidate, pwdvalidate, emailvalidate)
        if not (unamevalidate[0] or pwdvalidate or emailvalidate):
            if not unamevalidate[0]:
                if unamevalidate[1] == 0:
                    messagebox.showerror(
                        "Error", "Invalid username! Cannot be greater than 50 chars long")
                if unamevalidate[1] == 1:
                    messagebox.showerror(
                        "Error", "Invalid username! No special chars at start or end")
                elif unamevalidate[1] == 2:
                    messagebox.showerror("Error", "Username is not unique!")
            elif not pwdvalidate:
                messagebox.showerror("Error", "Invalid password!")
            elif not emailvalidate:
                messagebox.showerror("Error", "Invalid email address!")
        else:
            cache["current_username"] = self.username
            UserId = userUtils.generateUserID()
            cache["current_user_id"] = UserId
            print(cache)
            userUtils.createUserGUI(
                UserId, self.username, self.password, self.email)
            self.onCloseRoot()
            MainApp(self.user_id, self.username)

    def logIn(self):
        self.onCloseRoot()
        self.root = Tk()
        self.root.title("Togepi")
        self.root.configure(background="#d2d2c9")

        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()
        self.welcome = Label(self.root, text="Togepi", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 80))
        self.welcome.pack()
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()

        self.welcome = Label(
            self.root, text="Please enter your credentials", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()

        self.welcome = Label(self.root, text="Username",
                             background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()

        self.username = StringVar()
        self.username_entry = Entry(self.root, textvariable=self.username)
        self.username_entry.pack()

        self.welcome = Label(self.root, text="Password",
                             background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()

        self.password = StringVar()
        self.password_entry = Entry(
            self.root, textvariable=self.password, show="*")
        self.password_entry.pack()

        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()

        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()

        self.login_button = Button(
            self.root,
            text="LOGIN",
            command=self.verifyLoginCredentials,
            bg="#4759b8",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.login_button.config(height=2, width=30, borderwidth=0)
        self.login_button.pack(side=TOP, expand=1)
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()

        self.exit_button_choice = Button(
            self.root,
            text="BACK",
            command=self.loadHome,
            bg="#4759b8",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.exit_button_choice.config(height=2, width=30, borderwidth=0)
        self.exit_button_choice.pack(side=TOP, expand=1)
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()

        self.root.protocol("WM_DELETE_root", self.onCloseRoot)
        self.root.mainloop()

    def signUp(self):
        self.onCloseRoot()
        self.root = Tk()
        self.root.title("Togepi")
        self.root.configure(background="#d2d2c9")

        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()
        self.welcome = Label(self.root, text="Togepi", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 80))
        self.welcome.pack()
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()

        self.welcome = Label(
            self.root, text="Please enter your credentials", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()

        self.welcome = Label(self.root, text="Username",
                             background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()

        self.username = StringVar()
        self.username_entry = Entry(self.root, textvariable=self.username)
        self.username_entry.pack()

        self.welcome = Label(self.root, text="Password",
                             background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()

        self.password = StringVar()
        self.password_entry = Entry(
            self.root, textvariable=self.password, show='*')
        self.password_entry.pack()

        self.welcome = Label(self.root, text="E-Mail", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()

        self.email = StringVar()
        self.email_entry = Entry(self.root, textvariable=self.email)
        self.email_entry.pack()

        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()

        self.signup_button = Button(
            self.root,
            text="SIGN UP",
            command=self.verifySignupCredentials,
            bg="#4759b8",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.signup_button.config(height=2, width=30, borderwidth=0)
        self.signup_button.pack(side=TOP, expand=1)
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()

        self.exit_button_choice = Button(
            self.root,
            text="BACK",
            command=self.loadHome,
            bg="#4759b8",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.exit_button_choice.config(height=2, width=30, borderwidth=0)
        self.exit_button_choice.pack(side=TOP, expand=1)
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()

        self.root.protocol("WM_DELETE_root", self.onCloseRoot)
        self.root.mainloop()


class MainApp():
    def __init__(self, user_id, username):
        self.root = Tk()
        self.root.title(f"Togepi: {username}")
        self.root.configure(background="#d2d2c9")

        self.username = username
        self.user_id = user_id
        self.repository_id = None
        self.repository_name = None
        self.dir_path = None
        cache["current_user_id"] = self.user_id
        cache["current_username"] = self.username

        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()

        self.welcome = Label(self.root, text="Togepi", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 80))
        self.welcome.pack()

        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()

        text_welcome = f"Welcome, {self.username}"
        self.welcome = Label(self.root, text=text_welcome,
                             background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 20))
        self.welcome.pack()

        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()

        self.choose_dir_button = Button(
            self.root,
            text="CHOOSE REPOSITORY DIRECTORY",
            command=self.chooseRepositoryDirectory,
            bg="#4759b8",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.choose_dir_button.config(height=2, width=30, borderwidth=0)
        self.choose_dir_button.pack(side=TOP, expand=1)
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()

        self.create_repo_button = Button(
            self.root,
            text="CREATE REPOSITORY",
            command=self.createRepository,
            bg="#4759b8",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.create_repo_button.config(height=2, width=30, borderwidth=0)
        self.create_repo_button.pack(side=TOP, expand=1)
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()

        self.clone_repo_button = Button(
            self.root,
            text="CLONE REPOSITORY",
            command=self.cloneRepository,
            bg="#4759b8",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.clone_repo_button.config(height=2, width=30, borderwidth=0)
        self.clone_repo_button.pack(side=TOP, expand=1)
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()

        self.logout_button = Button(
            self.root,
            text="LOG OUT",
            command=self.logOut,
            bg="#4759b8",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.logout_button.config(height=2, width=30, borderwidth=0)
        self.logout_button.pack(side=TOP, expand=1)
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.onCloseRoot)
        self.root.mainloop()

    def chooseRepositoryDirectory(self):
        self.dir_path = getDirectoryDialog()
        print("self.dir_path", self.dir_path)
        cliUtils.cd(self.dir_path)
        self.onCloseRoot()
        RepositoryApp(self.dir_path)

    def cloneRepository(self):
        self.window = Tk()
        self.window.title("Togepi")
        self.window.configure(background="#d2d2c9")

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()
        self.welcome = Label(self.window, text="Togepi", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 80))
        self.welcome.pack()
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.welcome = Label(
            self.window, text="Please enter repository details", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.welcome = Label(self.window, text="Username",
                             background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.username_entry = Entry(self.window)
        self.username_entry.pack()

        self.welcome = Label(
            self.window, text="Repository Name", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.repo_name_entry = Entry(self.window)
        self.repo_name_entry.pack()

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.clone_button = Button(
            self.window,
            text="CLONE",
            command=self.clone,
            bg="#4759b8",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.clone_button.config(height=2, width=30, borderwidth=0)
        self.clone_button.pack(side=TOP, expand=1)
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.window.protocol("WM_DELETE_WINDOW", self.onCloseWindow)
        self.window.mainloop()

    def clone(self):
        global cache
        owner_name = self.username_entry.get()
        repo_name = self.repo_name_entry.get()
        clone_path = f"{owner_name}/{repo_name}"
        status = repoUtils.clone(cache, clone_path)
        if not status:
            messagebox.showerror(
                "Error", "You are not a collaborator on this repository, cannot clone")
        self.onCloseWindow()

    def createRepository(self):
        self.window = Tk()
        self.window.title("Togepi")
        self.window.configure(background="#d2d2c9")

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()
        self.welcome = Label(self.window, text="Togepi", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 80))
        self.welcome.pack()
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.welcome = Label(
            self.window, text="Please enter repository details", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.welcome = Label(
            self.window, text="Repository Name", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.repo_name_entry = Entry(self.window)
        self.repo_name_entry.pack()

        self.welcome = Label(
            self.window, text="Repository Description", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.repo_desc_entry = Entry(self.window)
        self.repo_desc_entry.pack()

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.welcome = Label(
            self.window, text="Repository Visibility", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.radio_var = StringVar(self.window, "public")
        public_choice_button = Radiobutton(
            self.window, text="Public", variable=self.radio_var, value="public")
        public_choice_button.pack()
        private_choice_button = Radiobutton(
            self.window, text="Private", variable=self.radio_var, value="private")
        private_choice_button.pack()

        self.create_button = Button(
            self.window,
            text="CREATE",
            command=self.create,
            bg="#4759b8",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.create_button.config(height=2, width=30, borderwidth=0)
        self.create_button.pack(side=TOP, expand=1)
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.window.protocol("WM_DELETE_WINDOW", self.onCloseWindow)
        self.window.mainloop()

    def create(self):
        repo_name = self.repo_name_entry.get()
        description = self.repo_desc_entry.get()
        visibility = self.radio_var.get()
        if repo_name == '' or repo_name is None:
            messagebox.showerror("Error", "Repository Name cannot be empty")
            self.onCloseWindow()
        print("CACHE IN CREATE", cache)
        status = repoUtils.initGUI(cache, repo_name, description, visibility)
        if status[0]:
            cache["current_repository_id"] = status[1][0]
            cache["current_repository_name"] = status[1][1]
            self.dir_path = status[2]
            self.onCloseWindow()
            self.onCloseRoot()
            print("Repo path (create):", self.dir_path)
            RepositoryApp(self.dir_path)
        else:
            if status[1] == 1:
                messagebox.showerror(
                    "Error", "Repository already exists with that name!")
                self.onCloseWindow()
            elif status[1] == 2:
                messagebox.showerror(
                    "Error", "Repository name must be under 50 chars")
                self.onCloseWindow()

    def logOut(self):
        global cache
        cache["current_user_id"] = None
        cache["current_username"] = None
        cache["current_repository_id"] = None
        cache["current_repository_name"] = None
        self.onCloseRoot()
        HomeApp()

    def onCloseWindow(self):
        self.window.destroy()

    def onCloseRoot(self):
        self.root.destroy()


class RepositoryApp:
    def __init__(self, dir_path):
        self.repo_name = cache["current_repository_name"]
        self.root = Tk()
        # self.root.geometry("800x600")

        win_title = f"Repository: {self.repo_name}"
        self.root.title(win_title)
        self.root.configure(background="#d2d2c9")

        self.dir_path = dir_path
        self.repo_id = cache["current_repository_id"]
        self.username = cache["current_username"]
        self.user_id = cache["current_user_id"]

        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()
        self.welcome = Label(self.root, text="Togepi", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 80))
        self.welcome.pack()
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()

        self.left_frame = Frame(self.root, bg="#d2d2c9")
        self.left_frame.pack(fill=Y, side=LEFT)

        self.right_frame = Frame(self.root, bg="#d2d2c9")
        self.right_frame.pack(padx=20, fill=Y, side=LEFT)

        self.add_button = Button(
            self.left_frame,
            text="ADD",
            command=self.add,
            bg="#4759b8",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.add_button.config(height=2, width=30, borderwidth=0)
        self.add_button.pack()

        self.blank = Label(self.left_frame, bg="#d2d2c9")
        self.blank.pack()
        self.blank = Label(self.left_frame, bg="#d2d2c9")
        self.blank.pack()

        self.commit_button = Button(
            self.left_frame,
            text="COMMIT",
            command=self.commitChanges,
            bg="#4759b8",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.commit_button.config(height=2, width=30, borderwidth=0)
        self.commit_button.pack()

        self.blank = Label(self.left_frame, bg="#d2d2c9")
        self.blank.pack()
        self.blank = Label(self.left_frame, bg="#d2d2c9")
        self.blank.pack()

        self.push_button = Button(
            self.left_frame,
            text="PUSH",
            command=self.pushChanges,
            bg="#4759b8",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.push_button.config(height=2, width=30, borderwidth=0)
        self.push_button.pack()

        self.blank = Label(self.left_frame, bg="#d2d2c9")
        self.blank.pack()
        self.blank = Label(self.left_frame, bg="#d2d2c9")
        self.blank.pack()

        self.pull_button = Button(
            self.left_frame,
            text="PULL",
            command=self.pullChanges,
            bg="#4759b8",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.pull_button.config(height=2, width=30, borderwidth=0)
        self.pull_button.pack()

        self.blank = Label(self.left_frame, bg="#d2d2c9")
        self.blank.pack(fill=Y)
        self.blank = Label(self.left_frame, bg="#d2d2c9")
        self.blank.pack()

        self.add_collab_button = Button(
            self.left_frame,
            text="ADD COLLABORATOR",
            command=self.addCollaborator,
            bg="#4759b8",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.add_collab_button.config(height=2, width=30, borderwidth=0)
        self.add_collab_button.pack()

        self.blank = Label(self.left_frame, bg="#d2d2c9")
        self.blank.pack(fill=Y)
        self.blank = Label(self.left_frame, bg="#d2d2c9")
        self.blank.pack()

        self.exit_button_choice = Button(
            self.left_frame,
            text="BACK",
            command=self.loadMain,
            bg="#4759b8",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.exit_button_choice.config(height=2, width=30, borderwidth=0)
        self.exit_button_choice.pack(side=TOP, expand=1)
        self.blank = Label(self.left_frame, bg="#d2d2c9")
        self.blank.pack()

        self.verboseLabel = Label(
            self.right_frame, text=f"{self.repo_name}", background="#d2d2c9", width=75)
        self.verboseLabel.config(fg="#6d031c", font=("Comfortaa", 13))
        self.verboseLabel.pack()

        self.blank = Label(self.right_frame, bg="#d2d2c9")
        self.blank.pack(fill=Y)

        self.root.protocol("WM_DELETE_WINDOW", self.onCloseRoot)
        self.root.mainloop()

    def loadMain(self):
        global cache
        self.onCloseRoot()
        os.chdir(os.environ["APP_DIR"])
        cache["current_repository_id"] = None
        cache["current_repository_name"] = None
        MainApp(cache["current_user_id"], cache["current_username"])

    def add(self):
        if self.dir_path != os.getcwd():
            os.chdir(self.dir_path)
        # filepaths = self.dir_path
        # user_id = cache["current_user_id"]
        # username = cache["current_username"]
        # repo_id = cache["current_repository_id"]
        # repo_name = cache["current_repository_name"]
        print("Adding", cache)
        add_status = repoUtils.add(cache, ".")
        if not add_status[0]:
            messagebox.showerror(
                "Error", "You do not have add access to this repository")
        else:
            textvar = "\n".join(add_status[1])
            self.verboseLabel.config(text=textvar)

    def commit(self):
        # user_id = cache["current_user_id"]
        # username = cache["current_username"]
        # repo_id = cache["current_repository_id"]
        # repo_name = cache["current_repository_name"]
        commit_msg = self.commit_msg_entry.get()
        commit_status = repoUtils.commit(cache, commit_msg)
        if not commit_status[0]:
            messagebox.showerror(
                "Error", "You do not have commit access to this repository")
        else:
            textvar = commit_status[1]
            self.verboseLabel.config(text=textvar)
            self.onCloseWindow()

    def push(self):
        # user_id = cache["current_user_id"]
        # username = cache["current_username"]
        # repo_id = cache["current_repository_id"]
        # repo_name = cache["current_repository_name"]
        print("PUSH", cache)
        push_status = repoUtils.push(cache)
        if not push_status[0]:
            messagebox.showerror(
                "Error", "You do not have push access to this repository")
        else:
            textvar = "\n".join(push_status[1])
            self.verboseLabel.config(text=textvar)
            self.onCloseWindow()

    def commitChanges(self):
        repo_name = cache["current_repository_name"]
        self.window = Tk()
        self.window.title(f"Commit Changes: {repo_name}")
        self.window.configure(background="#d2d2c9")

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.welcome = Label(self.window, text="Togepi", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 80))
        self.welcome.pack()

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.welcome = Label(
            self.window, text="Please enter commit message", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.commit_msg_entry = Entry(self.window)
        self.commit_msg_entry.pack()

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.commit_button2 = Button(
            self.window,
            text="COMMIT",
            command=self.commit,
            bg="#4759b8",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.commit_button2.config(height=2, width=30, borderwidth=0)
        self.commit_button2.pack()

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.window.protocol("WM_DELETE_WINDOW", self.onCloseWindow)
        self.window.mainloop()

    def pushChanges(self):
        repo_name = cache["current_repository_name"]
        self.window = Tk()
        self.window.title(f"Push Changes: {repo_name}")
        self.window.configure(background="#d2d2c9")
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()
        self.welcome = Label(self.window, text="Togepi", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 80))
        self.welcome.pack()
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.push_changes_button2 = Button(
            self.window,
            text="PUSH CHANGES",
            command=self.push,
            bg="#4759b8",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.push_changes_button2.config(height=2, width=30, borderwidth=0)
        self.push_changes_button2.pack(side=TOP, expand=1)
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()
        self.window.protocol("WM_DELETE_WINDOW", self.onCloseWindow)
        self.window.mainloop()

    def pullChanges(self):
        repo_name = cache["current_repository_name"]
        self.window = Tk()
        self.window.title(f"Pull Changes: {repo_name}")
        self.window.configure(background="#d2d2c9")
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()
        self.welcome = Label(self.window, text="Togepi", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 80))
        self.welcome.pack()
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()
        textmsg = f"Repository: {repo_name}"
        self.welcome = Label(self.window, text=textmsg, background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 25))
        self.welcome.pack()
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.pull_changes_button2 = Button(
            self.window,
            text="PULL CHANGES",
            command=self.pull,
            bg="#4759b8",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.pull_changes_button2.config(height=2, width=30, borderwidth=0)
        self.pull_changes_button2.pack(side=TOP, expand=1)

        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()
        self.window.protocol("WM_DELETE_WINDOW", self.onCloseWindow)
        self.window.mainloop()

    def pull(self):
        print("PULL", cache)
        pull_status = repoUtils.pull(cache)
        if not pull_status[0]:
            if pull_status[1] == 1:
                messagebox.showerror(
                    "Error", "You do not have pull access on this repository.")
            elif pull_status[1] == 2:
                messagebox.showwarning(
                    "Warning", "No commits have been pushed to repository.")
            elif pull_status[1] == 3:
                messagebox.showerror("Error", "No commits have been created.")
            elif pull_status[1] == 4:
                messagebox.showerror(
                    "Error", "No changes to pull, repository is upto date.")
        else:
            messagebox.showinfo("Info", "Pulled Successfully")
        self.onCloseWindow()

    def addCollaborator(self):
        self.window = Tk()
        self.window.title(f"Add Collaborator: {self.repo_name}")
        self.window.configure(background="#d2d2c9")

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.welcome = Label(self.window, text="Togepi", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 80))
        self.welcome.pack()

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.welcome = Label(
            self.window, text="Add collaborator", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()

        self.welcome = Label(
            self.window, text="Please enter collaborator username", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 20))
        self.welcome.pack()

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.add_collab_entry = Entry(self.window)
        self.add_collab_entry.pack()

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.add_collab_button2 = Button(
            self.window,
            text="ADD AS COLLABORATOR",
            command=self.addcollab,
            bg="#4759b8",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.add_collab_button2.config(height=2, width=30, borderwidth=0)
        self.add_collab_button2.pack()

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.window.protocol("WM_DELETE_WINDOW", self.onCloseWindow)
        self.window.mainloop()

    def addcollab(self):
        collab_username = self.add_collab_entry.get()
        if collab_username == '' or collab_username is None:
            messagebox.showerror("Error", "Collaborator name cannot be empty")
        else:
            add_collab_status = repoUtils.addCollaborator(cache, collab_username)
            if add_collab_status[0] == True:
                messagebox.showinfo("Info", "Added collaborator!")
            else:
                if add_collab_status[1] == 1:
                    messagebox.showerror("Error", "You are not owner of this repository, cannot add collaborator!")
                elif add_collab_status[1] == 2:
                    messagebox.showerror("Error", f"User {collab_username} is already a collaborator!")
                elif add_collab_status[1] == 3:
                    messagebox.showerror("Error", f"User {collab_username} does not exist! Please check username")
        self.onCloseWindow()

    def onCloseWindow(self):
        self.window.destroy()

    def onCloseRoot(self):
        self.root.destroy()


if __name__ == "__main__":
    HomeApp()
