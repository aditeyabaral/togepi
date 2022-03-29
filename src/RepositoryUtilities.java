import java.io.*;
import java.sql.*;
import java.util.*;
// import java.lang.*;

class RepositoryUtilities
{
    public String getRepositoryIdFromLocalClone()
    {
        File file = new File(".coffee/bean");
        if (file.exists())
        {
            try
            {
                BufferedReader br = new BufferedReader(new FileReader(file));
                String line = br.readLine();
                line = line.trim();
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
            Process p = Runtime.getRuntime().exec("diff " + file1 + " " + file2);
            BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));
            String line = br.readLine();
            StringBuilder sb = new StringBuilder();
            while (line != null)
            {
                sb.append(line);
                sb.append("\n");
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
}

class TestRepositoryUtilities
{
    public static void main(String[] args) throws Exception
    {
        RepositoryUtilities ru = new RepositoryUtilities();
        System.out.println(ru.getRepositoryIdFromLocalClone());
    }
}