import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.lang.*;
import java.util.regex.*;
import java.lang.reflect.*;

class CommandRunner
{
    HashMap<Pattern, Method> commandsCLI;

    public void initCommandMaps() throws Exception
    {
        generateCLICommandMap();
    }

    public void setRepositoryDetails(Coffee coffee) throws Exception
    {
        String currentPath = System.getProperty("user.dir");
        currentPath = Paths.get(currentPath).normalize().toString();
        File currentDirectory = new File(currentPath);
        File[] files = currentDirectory.listFiles();
        Boolean found = false;
        for (File file : files)
        {
            if (file.isDirectory() && file.getName().equals(".coffee"))
            {
                found = true;
                File infoFile = new File(Paths.get(file.getPath(), "cfeinfo.txt").normalize().toString());
                String content = new String(Files.readAllBytes(infoFile.toPath()));
                String[] lines = content.split("\n");
                String repositoryID = lines[0].split(",")[1];
                coffee.repositoryID = repositoryID;
                break;
            }
        }
        if (!found) coffee.repositoryID = null; // is this needed?
    }

    public void generateCLICommandMap() throws Exception
    {
        Pattern cdPattern = Pattern.compile("cd ([\\.A-Za-z0-9\\/_]+)");
        Pattern lsPattern = Pattern.compile("ls ([\\.A-Za-z0-9\\/_]*)");
        Pattern catPattern = Pattern.compile("cat ([\\.A-Za-z0-9\\/_]+)");
        // Pattern nanoPattern = Pattern.compile("cd ([\.A-Za-z0-9\\/_]+)");
        Pattern mkdirPattern = Pattern.compile("mkdir ([\\.A-Za-z0-9\\/_]+)");
        Pattern rmdirPattern = Pattern.compile("rmdir ([\\.A-Za-z0-9\\/_]+)");
        Pattern rmPattern = Pattern.compile("rm ([\\.A-Za-z0-9\\/_]+)");

        commandsCLI = new HashMap<Pattern, Method>();
        commandsCLI.put(cdPattern, CommandLineUtilities.class.getMethod("cd", String.class));
        commandsCLI.put(lsPattern, CommandLineUtilities.class.getMethod("ls", String.class));
        commandsCLI.put(catPattern, CommandLineUtilities.class.getMethod("cat", String.class));
        // commandsCLI.put(nanoPattern, CommandLineUtilities.class.getMethod("nano", String.class));
        commandsCLI.put(mkdirPattern, CommandLineUtilities.class.getMethod("mkdir", String.class));
        commandsCLI.put(rmdirPattern, CommandLineUtilities.class.getMethod("rmdir", String.class));
        commandsCLI.put(rmPattern, CommandLineUtilities.class.getMethod("rm", String.class));
    }

    public Method getCLIMethod(String command) throws Exception
    {

        if (command.equals("ls")) return CommandLineUtilities.class.getMethod("ls");
        else if (command.equals("cls")) return CommandLineUtilities.class.getMethod("clearScreen");
        else if (command.equals("clear")) return CommandLineUtilities.class.getMethod("clearScreen");
        // else if (command.equals("help")) return CommandLineUtilities.class.getMethod("help");
        // else if (command.equals("coffee")) return CommandLineUtilities.class.getMethod("coffee");

        for (Map.Entry<Pattern, Method> entry : commandsCLI.entrySet())
        {
            Matcher matcher = entry.getKey().matcher(command);
            if (matcher.matches())
            {
                Method method = entry.getValue();
                return method;
            }
        }
        return null;
    }

    public Method getDeveloperMethod(String command) throws Exception
    {
        if (command.equals("cfe user logout")) return DeveloperUtilities.class.getMethod("logoutUser", Coffee.class);
        else if (command.equals("cfe user login")) return DeveloperUtilities.class.getMethod("loginUser", Coffee.class);
        else if (command.equals("cfe user register")) return DeveloperUtilities.class.getMethod("registerUser", Coffee.class);
        else return null;
    }

    public void run(Coffee coffee, String command) throws Exception
    {
        Method method;
        
        method = getCLIMethod(command);
        if (method != null)
        {
            // System.out.println(method);
            String[] tempArgs = command.split(" ");
            if (tempArgs.length > 1)
            {
                String arg = tempArgs[1];
                method.invoke(coffee.cmd, arg);
            }
            else
                method.invoke(coffee.cmd);
            setRepositoryDetails(coffee);
            return;
        }

        method = getDeveloperMethod(command);
        if (method != null)
        {
            // System.out.println(method);
            method.invoke(coffee.dev, coffee);
            return;
        }

        method = getRepositoryMethod(command);
        if (method != null)
        {
            // System.out.println(method);
            if (coffee.repositoryID == null)
                System.out.println("You are not logged in to a repository. Please login to a repository first.");
            else
            {
                String[] tempArgs = command.split(" ");
                if (tempArgs.length > 1)
                {
                    String arg = tempArgs[1];
                    method.invoke(coffee.repo, coffee, arg);
                }
                else
                    method.invoke(coffee.repo, coffee);
            return;
            }
        }

        throw new Exception();
    }

}