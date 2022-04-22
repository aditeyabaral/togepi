import java.io.*;
import java.nio.*;
import java.sql.*;
import java.util.*;
import java.lang.*;
import java.time.*;
import com.dropbox.core.*;
import com.fasterxml.uuid.*;

class RepositoryUtilities
{
    // public String getRepoIDFromDir(String dir) throws IOException
    // {
    //     // Get the current working directory
    //     String currentPath = System.getProperty("user.dir");
    //     currentPath = Paths.get(currentPath).normalize().toString();
    //     File currentDirectory = new File(currentPath);

    //     // Get the files in the current directory
    //     File[] files = currentDirectory.listFiles();

    //     // Search for the .coffee directory
    //     for (File file : files)
    //     {
    //         if (file.isDirectory() && file.getName().equals(".coffee"))
    //         {

    //             // Read the cfeinfo.txt file
    //             File infoFile = new File(Paths.get(file.getPath(), "cfeinfo.txt").normalize().toString());
    //             String content = new String(Files.readAllBytes(infoFile.toPath()));

    //             // Split the content into lines
    //             String[] lines = content.split("\n");

    //             // Extract the repository ID from first line
    //             String repositoryID = lines[0].split(",")[1];
    //             return repositoryID;
    //         }
    //     }
    //     return null;
    // }

    // public String getFileDiff(String cloudFileContent, String localFileContent) throws Exception
    // {
    //     List<String> cloudLines = Arrays.asList(cloudFileContent.split("\n"));
    //     List<String> localLines = Arrays.asList(localFileContent.split("\n"));

    //     Patch<String> patch = DiffUtils.diff(cloudLines, localLines);
    //     List<String> patchedDiff = DiffUtils.patch(cloudLines, patch);

    //     // List<Delta<String>> deltas = patch.getDeltas();
    //     System.out.print(String.join("\n", patchedDiff));
    //     return String.join("\n", patchedDiff);
    // }

    public String getRepositoryIdFromLocalClone()
    {
        File file = new File(".coffee/.bean");
        if (file.exists())
        {
            try
            {
                BufferedReader br = new BufferedReader(new FileReader(file));
                String line = br.readLine();
                line = line.trim();
                line = line.split(",")[1];
                br.close();
                return line;
            }
            catch (Exception e)
            {
                System.out.println("Error: " + e.getMessage());
                return null;
            }
        }
        else return null;
    }

    public String getDiffBetweenFiles(String file1, String file2)
    {
        try
        {
            Process p = Runtime.getRuntime().exec("diff -u " + file1 + " " + file2);
            BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));
            String line = br.readLine();
            StringBuilder sb = new StringBuilder();
            while (line != null)
            {
                if ((line.startsWith("+") || line.startsWith("-")) && !(line.startsWith("+++") || line.startsWith("---")))
                {
                    sb.append(line);
                    sb.append("\n");
                }
                line = br.readLine();
            }
            return sb.toString();
        }
        catch (Exception e)
        {
            System.out.println("Error: " + e.getMessage());
            return null;
        }
    }

    public String getDiffBetweenFileContents(String content1, String content2)
    {
        String id1 = Generators.timeBasedGenerator().generate().toString();
        String id2 = Generators.timeBasedGenerator().generate().toString();
        String file1 = id1+".txt";
        String file2 = id2+".txt";

        try
        {
            BufferedWriter bw = new BufferedWriter(new FileWriter(file1));
            bw.write(content1);
            bw.close();
            bw = new BufferedWriter(new FileWriter(file2));
            bw.write(content2);
            bw.close();

            String diff = getDiffBetweenFiles(file1, file2);
            File f1 = new File(file1);
            f1.delete();
            File f2 = new File(file2);
            f2.delete();
            return diff;
        }
        catch (Exception e)
        {
            System.out.println("Error: " + e.getMessage());
            return null;
        }
    }

    public HashMap checkFileIsModified(String diff)
    {
        HashMap<String, Integer> diffMap = new HashMap<String, Integer>();
        if (diff.length() < 0)
        {
            diffMap.put("modified", 0);
            return diffMap;
        }
        else
        {
            String[] lines = diff.split("\n");
            int additions = 0;
            int deletions = 0;
            for (String line : lines)
            {
                if (line.startsWith("+") || line.startsWith("-") || line.startsWith("?"))
                {
                    if (line.startsWith("+")) additions++;
                    else if (line.startsWith("-")) deletions++;
                }
            }
            if (additions > 0 || deletions > 0)
            {
                diffMap.put("modified", 1);
                diffMap.put("additions", additions);
                diffMap.put("deletions", deletions);
            }
            else diffMap.put("modified", 0);
            return diffMap;
        }
    }

    public String generateRepositoryID()
    {
        return Generators.timeBasedGenerator().generate().toString();
    }

    public String generateFileID()
    {
        return Generators.timeBasedGenerator().generate().toString();
    }

    public String generateCommitID()
    {
        return Generators.timeBasedGenerator().generate().toString();
    }

    public void createBeanFile(String userId, String repoName, String repoId, String description, String url, LocalDateTime createTime, String visibility)
    {
        try
        {
            File file = new File(repoName + "/.coffee/.bean");
            if (!file.exists()) file.createNewFile();
            BufferedWriter bw = new BufferedWriter(new FileWriter(file));
            bw.write("repositoryId," + repoId); bw.newLine();
            bw.write("repositoryName," + repoName); bw.newLine();
            bw.write("userId," + userId); bw.newLine();
            bw.write("url," + url); bw.newLine();
            bw.write("description," + description); bw.newLine();
            bw.write("createTime," + createTime.toString()); bw.newLine();
            bw.write("visibility," + visibility); bw.newLine();
            bw.write("collaborators,"); bw.newLine();
            bw.close();
        }
        catch (Exception e)
        {
            System.out.println("Error: " + e.getMessage());
        }
    }

    public void init(Coffee coffee, String repoName) throws Exception
    {
        System.out.println("Initializing repository " + repoName);
        String userID = coffee.userID;
        String username = coffee.devDB.getUsernameFromUserId(userID);
        
        if (coffee.repoDB.checkUserHasRepository(userID, repoName))
        {
            System.out.println("Error: Repository already exists! Repository names have to be unique.");
            return;
        }

        if (repoName.length() > 50)
        {
            System.out.println("Error: Repository name cannot be more than 50 characters long.");
            return;
        }

        coffee.cmd.mkdir(repoName);
        coffee.cmd.mkdir(repoName + "/.coffee");
        String repoId = generateRepositoryID();
        
        Scanner sc = new Scanner(System.in);
        
        String description = "";
        String descriptionChoice;
        System.out.print("Enter repository description [y/n]: ");
        descriptionChoice = sc.nextLine().toLowerCase();
        if (descriptionChoice.equals("y"))
        {
            System.out.print("Enter repository description [150 characters]: ");
            description = sc.nextLine();
            if (description.length() > 150)
            {
                System.out.println("Error: Repository description cannot be more than 150 characters long. Truncating description.");
                description = description.substring(0, 150);
            }
        }

        String url = "/" + username + "/" + repoName;
        LocalDateTime createTime = LocalDateTime.now();
        
        String visibility = "public";
        String visibilityChoice;
        System.out.print("Enter repository visibility [public/private]: ");
        visibilityChoice = sc.nextLine().toLowerCase();
        if (visibilityChoice.equals("private")) visibility = "private";
        else if (visibilityChoice.equals("public")) visibility = "public";
        else
        {
            System.out.println("Error: Invalid visibility. Defaulting to public.");
            visibility = "public";
        }
    
        createBeanFile(userID, repoName, repoId, description, url, createTime, visibility);
        coffee.repoDB.createRepository(repoId, repoName, description, url, createTime, visibility, userID);
        coffee.relDB.createUserRepositoryRelation(userID, repoId, "owner");
        coffee.dropBox.uploadFolder(repoName, username);
        System.out.println("Repository created successfully!");
    }

    public void commit(Coffee coffee) throws SQLException, DbxException, IOException, FileNotFoundException, ClassNotFoundException
    {
        String userID = coffee.userID;
        String repositoryID = coffee.repositoryID;
        String repositoryName = coffee.repoDB.getRepositoryNameFromId(repositoryID);

        String message = "";
        String messageChoice;
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter commit message [y/n]: ");
        messageChoice = sc.nextLine().toLowerCase();
        if (messageChoice.equals("y"))
        {
            System.out.print("Enter commit message [150 characters]: ");
            message = sc.nextLine();
            if (message.length() > 150)
            {
                System.out.println("Error: Commit message cannot be more than 150 characters long. Truncating message.");
                message = message.substring(0, 150);
            }
        }

        String relation = coffee.relDB.getUserRepositoryRelation(userID, repositoryID);
        if (!(relation.equals("owner") || relation.equals("collaborator")))
        {
            System.out.println("Error: You do not have commit acccess to this repository.");
            return;
        }
        
        String ownerId = coffee.relDB.getRepositoryOwnerFromRepositoryId(repositoryID);
        String ownerName = coffee.devDB.getUsernameFromUserId(ownerId);

        ArrayList<String> trackedFiles = coffee.fileDB.getTrackedFiles(repositoryID);
        HashMap<String, String> fileDiffs = new HashMap<String, String>();
        int numFilesModified = 0;
        HashMap<String, Integer> numDiffs = new HashMap<String, Integer>();
        numDiffs.put("additions", 0);
        numDiffs.put("deletions", 0);

        BufferedReader br;
        File fileObject;
        String cloudFilePath;
        String cloudFileContent;
        String diff;
        for(String file : trackedFiles)
        {
            fileObject = new File(file);
            br = new BufferedReader(new FileReader(fileObject));
            String fileContent = "";
            String line;
            while((line = br.readLine()) != null) fileContent += line + "\n";
            br.close();

            cloudFilePath = "/" + ownerName + "/" + repositoryName + "/" + file;
            cloudFileContent = coffee.dropBox.getFileContent(cloudFilePath);
            diff = getDiffBetweenFileContents(fileContent, cloudFileContent);
            HashMap<String, Integer> diffMap = checkFileIsModified(diff);

            if (diffMap.get("modified") > 0)
            {
                fileDiffs.put(file, diff);
                long lastModifiedLong = fileObject.lastModified();
                LocalDateTime lastModified = LocalDateTime.ofInstant(Instant.ofEpochMilli(lastModifiedLong), ZoneId.systemDefault());
                coffee.fileDB.updateFileModifiedTime(repositoryID, file, lastModified);
                numFilesModified++;
                numDiffs.put("additions", numDiffs.get("additions") + diffMap.get("additions"));
                numDiffs.put("deletions", numDiffs.get("deletions") + diffMap.get("deletions"));
            }
        }

        String commitId = generateCommitID();
        LocalDateTime commitTime = LocalDateTime.now();
        String commitTimeString = commitTime.toString().substring(0, 19);
        String[] commitTimeArray = commitTimeString.split(" ");
        commitTimeString = commitTimeArray[0] + "$" + commitTimeArray[1] ;
        String commitFolderName = "./.coffee/" + commitId + "--" + commitTimeString;

        String file;
        String fileId;
        for(Map.Entry <String, String> entry : fileDiffs.entrySet())
        {
            file = (String) entry.getKey();
            diff = (String) entry.getValue();
            fileId = coffee.fileDB.getFileID(repositoryID, file);

            File commitFolder = new File(commitFolderName);
            if (!commitFolder.exists()) commitFolder.mkdir();

            File commitFile = new File(commitFolderName + "/" + fileId + ".diff");
            FileWriter fw = new FileWriter(commitFile);
            fw.write(file + "\n\n");
            fw.write(diff);

            coffee.commitDB.createCommit(commitId, userID, repositoryID, commitTime, fileId, message);
            coffee.fileDB.updateFileCommitTime(repositoryID, file, commitTime);
            System.out.println("added changes: " + file);
        }
        System.out.println(numFilesModified + " file(s) modified: " + numDiffs.get("additions") + " additions(+) " + numDiffs.get("deletions") + " deletions(-)");
    }

    public void pull(Coffee coffee) throws SQLException, DbxException, ClassNotFoundException, IOException, InterruptedException
    {
        String userID = coffee.userID;
        String repositoryID = coffee.repositoryID;
        String repositoryName = coffee.repoDB.getRepositoryNameFromId(repositoryID);

        // A user can always pull changes, even if they are not a collaborator
        // String relation = coffee.relDB.getUserRepositoryRelation(userID, repositoryID);
        // if (!(relation.equals("owner") || relation.equals("collaborator")))
        // {
        //     System.out.println("Error: You do not have pull acccess to this repository.");
        //     return;
        // }
        
        String ownerId = coffee.relDB.getRepositoryOwnerFromRepositoryId(repositoryID);
        String ownerName = coffee.devDB.getUsernameFromUserId(ownerId);

        String dropBoxPath = "/" + ownerName + "/" + repositoryName;
        LocalDateTime dropBoxCommitTime = coffee.dropBox.getLastDropBoxCommitTime(dropBoxPath);
        LocalDateTime localCommitTime = coffee.dropBox.getLastLocalCommitTime();

        if (dropBoxCommitTime == null)
        {
            System.out.println("No commits have been pushed to repository.");
            return;
        }
        else
        {
            if (localCommitTime != null)
            {
                if (localCommitTime.equals(dropBoxCommitTime))
                {
                    System.out.println("No changes to pull, repository is upto date.");
                    return;
                }
                else if (localCommitTime.isAfter(dropBoxCommitTime))
                {
                    System.out.println("Error: You have local commits that are newer than the repository.");
                    return;
                }
                else
                {
                    System.out.println("Pulling changes from repository...");
                    coffee.dropBox.downloadFolder("/", dropBoxPath);
                }
            }
            else
            {
                System.out.println("Pulling changes from repository...");
                coffee.dropBox.downloadFolder("/", dropBoxPath);
            }
        }
    }

    public void push(Coffee coffee) throws SQLException, DbxException, ClassNotFoundException, IOException, InterruptedException
    {
        String repositoryID = coffee.repositoryID;
        String repositoryName = coffee.repoDB.getRepositoryNameFromId(repositoryID);
        String userID = coffee.userID;

        // A user must be a collaborator to push
        String relation = coffee.relDB.getUserRepositoryRelation(userID, repositoryID);
        if (!(relation.equals("owner") || relation.equals("collaborator")))
        {
            System.out.println("Error: You do not have push acccess to this repository.");
            return;
        }
        
        String ownerId = coffee.relDB.getRepositoryOwnerFromRepositoryId(repositoryID);
        String ownerName = coffee.devDB.getUsernameFromUserId(ownerId);

        String dropBoxPath = "/" + ownerName + "/" + repositoryName;
        LocalDateTime now = LocalDateTime.now(); 

        ArrayList<String> trackedFiles = coffee.fileDB.getTrackedFiles(repositoryID);

        for (String filePath : trackedFiles)
        {
            coffee.fileDB.updateFilePushTime(repositoryID, filePath, now);
        }

        ArrayList<String> outputString = coffee.dropBox.uploadFolder("../" + repositoryName, dropBoxPath);
    }


    public void status(Coffee coffee) throws SQLException, FileNotFoundException {
        String repositoryID = coffee.repositoryID;
        String repositoryName = coffee.repoDB.getRepositoryNameFromId(repositoryID);
        String userID = coffee.userID;

        String ownerId = coffee.relDB.getRepositoryOwnerFromRepositoryId(repositoryID);
        String ownerName = coffee.devDB.getUsernameFromUserId(ownerId);

        ArrayList<String> trackedFiles = coffee.fileDB.getTrackedFiles(repositoryID);

        // A user must be a collaborator to view
        String relation = coffee.relDB.getUserRepositoryRelation(userID, repositoryID);
        if (!(relation.equals("owner") || relation.equals("collaborator")))
        {
            System.out.println("Error: You do not have acccess to this repository.");
            return;
        }

        for (String filePath: trackedFiles)
        {
            try {
                String cloudFilePath = "/" + ownerName + "/" + repositoryName + "/" + filePath.subSequence(2, filePath.length());
                String cloudContent = coffee.dropBox.getFileContent(cloudFilePath);

                // Find diff
                String id = Generators.timeBasedGenerator().generate().toString();
                String tempFileString = id+".txt";
                BufferedWriter bw = new BufferedWriter(new FileWriter(tempFileString));
                bw.write(cloudContent);
                bw.close();

                String diff = getDiffBetweenFiles(tempFileString, filePath);
                File tempFile = new File(tempFileString);
                tempFile.delete();
                
                if (checkFileIsModified(diff).get("modified") == (Integer) 1) {
                    File file = new File(filePath);
                    long lastModified = file.lastModified();
                    LocalDateTime lastModifiedTime = LocalDateTime.ofInstant(Instant.ofEpochMilli(lastModified), ZoneId.systemDefault());
                    coffee.fileDB.updateFileModifiedTime(repositoryID, filePath, lastModifiedTime);
                    System.out.println("modified: " + filePath);
                }
            }
            catch (Exception e) {
                continue;
            }
            
        }
    }

    public void clone(Coffee coffee, String clonePath) throws SQLException, DbxException, ClassNotFoundException, IOException, InterruptedException
    {
        String[] clonePathComponents = clonePath.split("/");
        String ownerName = clonePathComponents[0];
        String repositoryName = clonePathComponents[1];
        String visibility = coffee.repoDB.getRepositoryVisbilityFromUsernameRepositoryName(ownerName, repositoryName);

        if(!(visibility.equals("public")))
        {
            String userID = coffee.userID;
            String relation = coffee.relDB.getUserRepositoryRelation(userID, coffee.repositoryID);
            if (!(relation.equals("owner") || relation.equals("collaborator")))
            {
                System.out.println("Error: You do not have acccess to this repository.");
                return;
            }
            System.out.println("Cloning repository " + repositoryName + "...");
            coffee.dropBox.downloadFolder("/", clonePath);
        }
        else
        {
            System.out.println("Cloning repository " + repositoryName + "...");
            coffee.dropBox.downloadFolder("/", clonePath);
        }
    }

    public void addCollaborator(Coffee coffee, String collaboratorName) throws SQLException
    {
        String userID = coffee.userID;
        String repositoryID = coffee.repositoryID;
        String collaboratorID = coffee.devDB.getUserIdFromUsername(collaboratorName);

        String relation = coffee.relDB.getUserRepositoryRelation(userID, repositoryID);
        if (!relation.equals("owner"))
        {
            System.out.println("Error: You need to be the owner of the repository to add collaborators.");
            return;
        }

        if (collaboratorID == null)
        {
            System.out.println("Error: User " + collaboratorName + " does not exist.");
            return;
        }

        relation = coffee.relDB.getUserRepositoryRelation(collaboratorID, repositoryID);
        if (relation != null)
        {
            System.out.println("Error: User " + collaboratorName + " is already a collaborator.");
            return;
        }

        if (userID.equals(collaboratorID))
        {
            System.out.println("Error: You cannot add yourself as a collaborator.");
            return;
        }

        coffee.relDB.createUserRepositoryRelation(collaboratorID, repositoryID, "collaborator");
        System.out.println("User " + collaboratorName + " added as a collaborator.");
    }
}