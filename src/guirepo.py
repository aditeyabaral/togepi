from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
import repoUtils

class RepositoryApp:
    def __init__(self, dir_path):
        self.repo_name = cache["current_repository_name"]
        self.root = Tk()
        self.root.geometry("800x600")

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
        self.right_frame.pack(fill=Y, side=RIGHT)

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

        self.blank = Label(self.left_frame, bg="#d2d2c9")
        self.blank.pack(fill=Y)

        self.verboseLabel = Label(self.right_frame, text="Label here", background="#d2d2c9")
        self.verboseLabel.config(fg="#6d031c", font=("Comfortaa", 15))
        self.verboseLabel.pack()

        self.blank = Label(self.right_frame, bg="#d2d2c9")
        self.blank.pack(fill=Y)

        self.root.protocol("WM_DELETE_WINDOW", self.onCloseRoot)
        self.root.mainloop()
    
    def add(self):
        filepaths = self.dir_path
        user_id = cache["current_user_id"]
        username = cache["current_username"]
        repo_id = cache["current_repository_id"]
        repo_name = cache["current_repository_name"]
        print("Adding", cache)
        add_status = repoUtils.add(cache, ".")
        if not add_status:
            messagebox.showerror("Error", "You do not have add access to this repository")

    def commit(self):
        user_id = cache["current_user_id"]
        username = cache["current_username"]
        repo_id = cache["current_repository_id"]
        repo_name = cache["current_repository_name"]
        commit_msg = self.commit_msg_entry.get()
        commit_status = repoUtils.commit(cache, commit_msg)
        if not commit_status[0]:
            messagebox.showerror("Error", "You do not have commit access to this repository")
    
    def push(self):
        user_id = cache["current_user_id"]
        username = cache["current_username"]
        repo_id = cache["current_repository_id"]
        repo_name = cache["current_repository_name"]
        print("PUSH", cache)
        push_status = repoUtils.push(cache)
        if not push_status:
            messagebox.showerror("Error", "You do not have push access to this repository")
        '''
        add_status = repoUtils.add(cache, ".")
        if not add_status:
            messagebox.showerror("Error", "You do not have add access to this repository")
        else:
            commit_msg = self.commit_msg_entry.get()
            commit_status = repoUtils.commit(cache, commit_msg)
            if not commit_status[0]:
                messagebox.showerror("Error", "You do not have commit access to this repository")
            push_status = repoUtils.push(cache)
            if not push_status:
                messagebox.showerror("Error", "You do not have push access to this repository")
        '''
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

        self.welcome = Label(self.window, text="Please enter commit message", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.commit_msg_entry = Entry(self.window)
        self.commit_msg_entry.pack()

        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()
        self.blank = Label(self.window, bg="#d2d2c9")
        self.blank.pack()

        self.commit_button2 = Button(
            self.window,
            text="COMMIT CHANGES",
            command=self.commit,
            bg="#4759b8",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.commit_button2.config(height=2, width=30, borderwidth=0)
        self.commit_button2.pack(side=TOP, expand=1)

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
                messagebox.showerror("Error", "You do not have pull access on this repository.")
            elif pull_status[1] == 2:
                messagebox.showwarning("Warning", "No commits have been pushed to repository.")
            elif pull_status[1] == 3:
                messagebox.showerror("Error", "No commits have been created.")
            elif pull_status[1] == 4:
                messagebox.showerror("Error", "No changes to pull, repository is upto date.")
        else:
            messagebox.showinfo("Info", "Pulled Successfully")

    def onCloseWindow(self):
        self.window.destroy()

    def onCloseRoot(self):
        self.root.destroy()


#HomeApp()
#MainApp("USER000001", "aditeyabaral")
#RepositoryApp("/aditeyabaral/testrepo")from tkinter import *

