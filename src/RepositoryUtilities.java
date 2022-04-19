import java.io.*;
import java.nio.*;
import java.sql.*;
import java.util.*;
import java.lang.*;
import java.time.*;
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
}

// class TestRepositoryUtilities
// {
//     public static void main(String[] args) throws Exception
//     {
//         Class.forName("org.postgresql.Driver");
//         RepositoryUtilities ru = new RepositoryUtilities();
//         Coffee coffee = new Coffee();
//         coffee.userID = "181b0f1e-9d7a-11ec-8e79-b11667294a65";
//         coffee.repositoryID = "1";
//         coffee.devDB.connect();
//         ru.init(coffee, "test");
//     }
// }