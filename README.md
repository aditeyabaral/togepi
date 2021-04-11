# Togepi

A version control system built using Python and DropBox API

<p align="center">
  <img src="img/togepi.jpg">
</p>

Togepi can be used both on command line as well as through a GUI window, however we do suggest using the CLI to access all of Togepi's features, due to certain implementation based restrictions in the GUI.

Togepi supports most major version control features such as `add`, `commit`, `pull`, `push`, `status`, `clone` to name a few. The CLI also features prominent CLI utility tools to help out such as `cd`, `mkdir`, `rmdir`, `nano`, `ls` and `cat`.

The GUI interface is basic and supports only the core features. There are no plans to extend work on the GUI since the interface was included as a course deliverable.

# Setting up Togepi
1. Create a virtual environment using virtualenv
```bash
virtualenv togepi
source togepi/bin/activate
```
2. Install the dependencies using `pip3 install -r requirements.txt`
3. Create a `.env` file and add the following keys
```env
DATABASE_URL=
DB_URL=(same as above)
DROPBOX_API_KEY=
DROPBOX_API_SECRET=
DROPBOX_ACC_TOK=
```
4. Create the database schema for Togepi

You can create the schema for the database using `database.py` inside the `app` directory. Navigate into the folder, run `python3` and execute the following commands
```Python
>>> from database import db
>>> db.create_all()
```
Note that if you are running it via an online database such as Heroku-PostgreSQL, you will need to run the above commands on the hosted Python environment.

# How to use Togepi

## Command Line Interface

To run Togepi on command-line, run `python3 src/main.py`

### Create User

You can create users using `togepi user create`.




# Contributing to Togepi

# Acknowledgements

This project was made as a part of the Object Oriented Analysis and Design & Software Engineering Laboratory Course (UE18CS355) at PES University. 

[Aditeya Baral](https://github.com/aditeyabaral)<br>
[Aronya Baksy](https://github.com/abaksy)<br>
[Ansh Sarkar](https://github.com/anshsarkar)