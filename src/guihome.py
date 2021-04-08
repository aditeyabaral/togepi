from tkinter import *
from tkinter import filedialog
import userUtils
import repoUtils
import validationUtils

cache = {
    "current_user_id": None,
    "current_username": None,
    "current_repository_id": None,
    "current_repository_name": None
}


def getDirectoryDialog():
    dir_path = filedialog.askdirectory()
    print(dir_path)
    return dir_path


class HomeApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("Togepi")
        self.root.configure(background="#d2d2c9")
        #self.root.geometry("480x640")

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

        self.welcome = Label(self.root, text="Welcome to Togepi\nPlease login or sign up to proceed", background="#d2d2c9")
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

        self.root.protocol("WM_DELETE_WINDOW", self.onCloseRoot)
        self.root.mainloop()

    def onCloseWindow(self):
        self.window.destroy()

    def onCloseRoot(self):
        self.root.destroy()

    def verifyLoginCredentials(self):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        self.user_id, self.username = userUtils.loginUser(self.username, self.password)
        print(self.username, self.password)
        if self.username is None:
            self.validation_str.set("Incorrect username or password")
        else:
            cache["current_user_id"] = self.user_id
            cache["current_username"] = self.username
            self.onCloseWindow()
            self.onCloseRoot()
            MainApp(self.user_id, self.username)
            
    def verifySignupCredentials(self):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        self.email = self.email_entry.get()
        unamevalidate = validationUtils.validateUsername(self.username)
        pwdvalidate = validationUtils.validatePassword(self.password)
        emailvalidate = validationUtils.validateEmail(self.email)
        if not (unamevalidate and pwdvalidate and emailvalidate):
            self.validation_str.set("Sign-In Failed!")
        else:
            cache["current_user_id"] = self.user_id
            cache["current_username"] = self.username
            UserId = userUtils.generateUserID()
            userUtils.createUserGUI(UserId, self.username, self.password, self.email)
            self.onCloseWindow()
            self.onCloseRoot()
            MainApp(self.user_id, self.username)

    def logIn(self):
        self.window = Tk()
        self.window.title("Togepi")
        self.window.configure(background="#d2d2c9")
        #self.window.geometry("480x640")

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()
        self.welcome = Label(self.window, text="Togepi", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 80))
        self.welcome.pack()
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.welcome = Label(self.window, text="Please enter your credentials", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.welcome = Label(self.window, text="Username", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.username = StringVar()
        self.username_entry = Entry(self.window, textvariable=self.username)
        self.username_entry.pack()

        self.welcome = Label(self.window, text="Password", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.password = StringVar()
        self.password_entry = Entry(self.window, textvariable=self.password, show="*")
        self.password_entry.pack()

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.validation_str = StringVar()
        self.validation_str.set("hello")
        self.validation_login = Message(self.window, textvariable=self.validation_str, background="#d2d2c9")
        self.validation_login.config(fg="#6d031c", font=("Comfortaa", 30))
        self.validation_login.pack()

        self.login_button = Button(
            self.window,
            text="LOGIN",
            command=self.verifyLoginCredentials,
            bg="#4759b8",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.login_button.config(height=2, width=30, borderwidth=0)
        self.login_button.pack(side=TOP, expand=1)
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.window.protocol("WM_DELETE_WINDOW", self.onCloseWindow)
        self.window.mainloop()
    
    def signUp(self):
        self.window = Tk()
        self.window.title = "Togepi"
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

        self.welcome = Label(self.window, text="Please enter your credentials", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.welcome = Label(self.window, text="Username", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.username = StringVar()
        self.username_entry = Entry(self.window, textvariable=self.username)
        self.username_entry.pack()

        self.welcome = Label(self.window, text="Password", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.password = StringVar()
        self.password_entry = Entry(self.window, textvariable=self.password)
        self.password_entry.pack()

        self.welcome = Label(self.window, text="E-Mail", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.email = StringVar()
        self.email_entry = Entry(self.window, textvariable=self.email)
        self.email_entry.pack()

        self.validation_str = StringVar()
        self.validation_str.set("hello")
        self.validation_login = Message(self.window, textvariable=self.validation_str, background="#d2d2c9")
        self.validation_login.config(fg="#6d031c", font=("Comfortaa", 30))
        self.validation_login.pack()

        self.signup_button = Button(
            self.window,
            text="LOGIN",
            command=self.verifySignupCredentials,
            bg="#4759b8",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.signup_button.config(height=2, width=30, borderwidth=0)
        self.signup_button.pack(side=TOP, expand=1)
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.window.protocol("WM_DELETE_WINDOW", self.onCloseWindow)
        self.window.mainloop()




        


class MainApp():
    def __init__(self, user_id, username):
        self.root = Tk()
        self.root.title("Togepi")
        self.root.configure(background="#d2d2c9")
        #self.root.geometry("480x640")

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
        # spawn new window with dir

    def cloneRepository(self):
        self.window = Tk()
        self.window.title("Togepi")
        self.window.configure(background="#d2d2c9")
        #self.window.geometry("480x640")

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()
        self.welcome = Label(self.window, text="Togepi", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 80))
        self.welcome.pack()
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.welcome = Label(self.window, text="Please enter repository details", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.welcome = Label(self.window, text="Username", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.username_entry = Entry(self.window)
        self.username_entry.pack()

        self.welcome = Label(self.window, text="Repository Name", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.repo_name_entry = Entry(self.window)
        self.repo_name_entry.pack()

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        # create Message box, update with unable to clone or some status if status variable in clone is False,
        # set to successfully cloned if status = True

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
        print(cache)
        owner_name = self.username_entry.get()
        repo_name = self.repo_name_entry.get()
        clone_path = f"{owner_name}/{repo_name}"
        status = repoUtils.clone(cache, clone_path)
        if not status:
            pass
            #wut2do

    def createRepository(self):
        self.window = Tk()
        self.window.title("Togepi")
        self.window.configure(background="#d2d2c9")
        #self.window.geometry("480x640")

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()
        self.welcome = Label(self.window, text="Togepi", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 80))
        self.welcome.pack()
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.welcome = Label(self.window, text="Please enter repository details", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.welcome = Label(self.window, text="Repository Name", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.repo_name_entry = Entry(self.window)
        self.repo_name_entry.pack()

        self.welcome = Label(self.window, text="Repository Description", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.repo_desc_entry = Entry(self.window)
        self.repo_desc_entry.pack()

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.welcome = Label(self.window, text="Repository Visibility", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.radio_var = StringVar()
        public_choice_button = Radiobutton(self.window, text="Public", variable=self.radio_var, value="public")  
        public_choice_button.pack() 
        private_choice_button = Radiobutton(self.window, text="Private", variable=self.radio_var, value="private")  
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
        status = repoUtils.initGUI(cache, repo_name, description, visibility)
        if status[0]:
            pass
        else:
            #Error in creating repo
            pass
            # do something


    def logOut(self):
        self.onCloseRoot()
        HomeApp()

    def onCloseWindow(self):
        self.window.destroy()

    def onCloseRoot(self):
        self.root.destroy()

#HomeApp()
MainApp("USER000001", "aditeyabaral")