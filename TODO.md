1. Cache dictionary containing user_id, username, repo_id, repo_name

2. Clean up utils function calls

3. `tgp commit -m "message"`
    * if possible- counts of filenames changed, additions, deletions
    * Update fields in File DB - last_modified, last_committed
    * Update fields in Commit
    * if file is modified, set status = "modified"
    * show files in repo currently not being tracked [untracked changes] -- NOT PRIORITY

4. `tgp push`
    * Push only modified files -- NOT PRIORITY
    * Update fields in File DB - last_pushed
    * Update fields in DB - for all files in repo, set status = "unchanged"
    
5. `tgp status`
    * for all tracked_files:
        *   find diffs -- if diffs, print filename to screen 
        *   if local is newer than dropbox:
            * show changes to push
        *   else
            * show changes to pull
6. `tgp pull`
    *   download and overwrite all files 

7. `tgp clone`
    * TBD -- NOT PRIORITY

8. Code cleanup

9. DB Cleanup

10. README

11. help command

12. Rename info.txt --> tgpinfo.txt

13. Format of IDs --> Remove '#'

14. Testing

15. Track .togepi/info.txt by default

16. Deletion of files

17. Add, Commit, Push - only owner and collaborator have access

18. Add collaborators