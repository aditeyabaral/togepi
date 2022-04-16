import java.io.*;
import java.sql.*;
import java.util.*;
import java.lang.*;
import java.time.*;
import com.fasterxml.uuid.*;

class RepositoryUtilities
{
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
            File file = new File(".coffee/.bean");
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

    public String getRepositoryOwner(Coffee coffee, String repositoryId)
    {
        return null; // implement RelationDatabaseUtilities first
    }
}

// class TestRepositoryUtilities
// {
//     public static void main(String[] args) throws Exception
//     {
//         RepositoryUtilities ru = new RepositoryUtilities();
//         System.out.println(ru.getRepositoryIdFromLocalClone());
//         String diff = ru.getDiffBetweenFiles("repoUtils.py", "repoUtils2.py");
//         HashMap<String, Integer> diffMap = ru.checkFileIsModified(diff);
//         System.out.println(diffMap);
//         String repoId = ru.generateRepositoryID();
//         System.out.println(repoId);
//     }
// }