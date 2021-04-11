import os
from tkinter import *
import cliUtils
import repoUtils
from tkinter import filedialog
from tkinter import messagebox


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

        self.push_changes_button = Button(
            self.root,
            text="PUSH CHANGES",
            command=self.pushChanges,
            bg="#4759b8",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.push_changes_button.config(height=2, width=30, borderwidth=0)
        self.push_changes_button.pack(side=TOP, expand=1)
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()

        self.pull_changes_button = Button(
            self.root,
            text="PULL CHANGES",
            command=self.pullChanges,
            bg="#4759b8",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.pull_changes_button.config(height=2, width=30, borderwidth=0)
        self.pull_changes_button.pack(side=TOP, expand=1)
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
        self.onCloseWindow()
        self.onCloseRoot()
        RepositoryApp(self.dir_path)

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
        global cache
        owner_name = self.username_entry.get()
        repo_name = self.repo_name_entry.get()
        clone_path = f"{owner_name}/{repo_name}"
        status = repoUtils.clone(cache, clone_path)
        if not status:
            messagebox.showerror("Error", "You are not a collaborator on this repository, cannot clone")
        else:
            self.dir_path = os.getcwd()
            info = open(f"{self.dir_path}/.togepi/tgpinfo.txt", 'r').read().split('\n')
            cache["current_repository_id"] = info[0].split(",")[1]
            cache["current_repository_name"] = info[1].split(",")[1]
            self.onCloseWindow()
            self.onCloseRoot()
            RepositoryApp(self.dir_path)

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

        self.radio_var = StringVar(self.window, "public")
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
        if repo_name == '' or repo_name is None:
            messagebox.showerror("Error","Repository Name cannot be empty")
            return
        status = repoUtils.initGUI(cache, repo_name, description, visibility)
        if status[0]:
            cache["current_repository_id"] = status[1][0]
            cache["current_repository_name"] = status[1][1]
        else:
            if status[1]==1:
                messagebox.showerror("Error","Repository already exists with that name!")
            elif status[1]==2:
                messagebox.showerror("Error","Repository name must be under 50 chars")

    def logOut(self):
        self.onCloseRoot()
        HomeApp()

    def onCloseWindow(self):
        self.window.destroy()

    def onCloseRoot(self):
        self.root.destroy()
