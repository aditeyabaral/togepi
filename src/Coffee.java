import java.io.*;
import java.nio.*;
import java.sql.*;
import java.util.*;
import java.lang.*;
import java.nio.file.*;
import java.util.regex.*;
import java.lang.reflect.*;


class Coffee
{
    // singleton class

    String userID;
    String repositoryID;

    CommandRunner runner;
    CommandLineUtilities cmd;
    DeveloperUtilities dev;
    DeveloperDatabaseUtilities devDB;
    DropBoxUtilities dropBox;
    RepositoryUtilities repo;

    private Coffee()
    {
        userID = null;
        repositoryID = null;
        runner = new CommandRunner();
        cmd = new CommandLineUtilities();
        dev = new DeveloperUtilities();
        devDB = new DeveloperDatabaseUtilities();
        dropBox = new DropBoxUtilities();
        repo = new RepositoryUtilities();
    }

    private static Coffee coffeeInstance = new Coffee();

    public static void main(String[] args) throws Exception
    {
        Class.forName("org.postgresql.Driver");
        Scanner sc = new Scanner(System.in);
        
        Boolean debug = args.length > 0 && args[0].equals("--debug");
        if (debug) System.out.println("Running in debug mode");
        System.out.println("Welcome to Coffee!");

        coffeeInstance.runner.initCommandMaps();
        coffeeInstance.devDB.connect();
        
        String command;
        while (true)
        {
            System.out.print(">>> ");
            command = sc.nextLine().strip();

            if (command.equals("exit") || command.equals("quit")) System.exit(0);
            else
            {
                try { coffeeInstance.runner.run(coffeeInstance, command); }
                catch (Exception e)
                {
                    if (debug) e.printStackTrace();
                    else System.out.println("Invalid command. Type help to learn more.\nYou can also visit https://github.com/Yashi-Chawla/coffee#how-to-use-coffee to read the entire documentation.");
                }
            }
            // System.out.println(coffee.repositoryID + " " + coffee.userID);
        }
    }
}