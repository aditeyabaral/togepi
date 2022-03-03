import java.io.*;
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

    public void logoutUser(Coffee coffee)
    {
        coffee.userID = null;
        coffee.repositoryID = null;
    }

    public void generateCLICommandMap() throws Exception
    {
        Pattern cdPattern = Pattern.compile("cd ([\\.A-Za-z0-9\\/_]+)");
        Pattern lsPattern = Pattern.compile("ls ([\\.A-Za-z0-9\\/_]*)");
        Pattern catPattern = Pattern.compile("cat ([\\.A-Za-z0-9\\/_]+)");
        // Pattern nanoPattern = Pattern.compile("cd ([\.A-Za-z0-9\\/_]+)");
        Pattern mkdirPattern = Pattern.compile("mkdir ([\\.A-Za-z0-9\\/_]+)");
        Pattern rmdirPattern = Pattern.compile("rmdir ([\\.A-Za-z0-9\\/_]+)");
        // Pattern rmPattern = Pattern.compile("rm ([\.A-Za-z0-9\\/_]+)");

        commandsCLI = new HashMap<Pattern, Method>();
        commandsCLI.put(cdPattern, CommandLineUtilities.class.getMethod("cd", String.class));
        commandsCLI.put(lsPattern, CommandLineUtilities.class.getMethod("ls", String.class));
        commandsCLI.put(catPattern, CommandLineUtilities.class.getMethod("cat", String.class));
        // commandsCLI.put(nanoPattern, CommandLineUtilities.class.getMethod("nano", String.class));
        commandsCLI.put(mkdirPattern, CommandLineUtilities.class.getMethod("mkdir", String.class));
        commandsCLI.put(rmdirPattern, CommandLineUtilities.class.getMethod("rmdir", String.class));
        // commandsCLI.put(rmPattern, CommandLineUtilities.class.getMethod("rm", String.class));
    }

    public Method getCLIMethod(String command) throws Exception
    {

        if (command.equals("ls")) return CommandLineUtilities.class.getDeclaredMethod("ls");
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

    public void run(Coffee coffee, CommandLineUtilities cmd, String command) throws Exception
    {
        Method method = getCLIMethod(command);
        System.out.println(method);
        if (method != null)
        {
            String[] tempArgs = command.split(" ");
            if (tempArgs.length > 1)
            {
                String arg = tempArgs[1];
                method.invoke(cmd, arg);
            }
            else
                method.invoke(cmd);
        }
    }

    // public void setRepositoryDetails(Coffee coffee);

}