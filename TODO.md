vc push
vc pull

show untracked changes
show git status

1. `vc init reponame`
    * Call mkdir with reponame
    * Get repo details, push to database
    * Inside repo, make folder named .togepi
        * This folder will store each version of each file (in folders maybe)
        * Also store repo_id and other details in info.txt

2. `checkCwdIsRepository()`
    * Check and set `current_repository` global variable

3. `vc add .`
    * walk through cwd recursively, adding every file if not present in db (check using relative path inside repo)
    
4. `vc add file1 file2`
    * Add arg files to db, if not present in db (check using relative path inside repo)

5. `vc commit -m "message"`
    * show untracked changes (?)
    * Add files to commit database and update fields in File

