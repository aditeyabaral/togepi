vc push
vc pull

show untracked changes
show git status


create db objects beforehand while making connection (dbUtils)


1. `vc add .`
    * walk through cwd recursively, adding every file if not present in db (check using relative path inside repo)
    
2. `vc add file1 file2`
    * Add arg files to db, if not present in db (check using relative path inside repo)

3. `vc commit -m "message"`
    * show untracked changes (?)
    * Add files to commit database and update fields in File

