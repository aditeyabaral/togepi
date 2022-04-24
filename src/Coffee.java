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
    DropBoxUtilities dropBox;
    RepositoryUtilities repo;

    CommitDatabaseUtilities commitDB;
    DeveloperDatabaseUtilities devDB;
    RelationDatabaseUtilities relDB;
    FileDatabaseUtilities fileDB;
    RepositoryDatabaseUtilities repoDB;

    private Coffee()
    {
        userID = null;
        repositoryID = null;
        runner = new CommandRunner();
        cmd = new CommandLineUtilities();
        dev = new DeveloperUtilities();
        dropBox = new DropBoxUtilities();
        repo = new RepositoryUtilities();

        commitDB = new CommitDatabaseUtilities();
        devDB = new DeveloperDatabaseUtilities();
        relDB = new RelationDatabaseUtilities();
        fileDB = new FileDatabaseUtilities();
        repoDB = new RepositoryDatabaseUtilities();
    }

    private static Coffee coffeeInstance = new Coffee();

    public static void main(String[] args) throws Exception
    {
        Class.forName("org.postgresql.Driver");
        Scanner sc = new Scanner(System.in);
        
        Boolean debug = args.length > 0 && args[0].equals("--debug");
        if (debug) System.out.println("Running in debug mode");
        System.out.println("Welcome to Coffee!");
        System.out.println("Type 'help' for a list of commands");
        System.out.println("Type 'quit' to quit Coffee");

        coffeeInstance.runner.initCommandMaps();
        coffeeInstance.commitDB.connect();
        coffeeInstance.devDB.connect();
        coffeeInstance.relDB.connect();
        coffeeInstance.fileDB.connect();
        coffeeInstance.repoDB.connect();
        
        String command;
        while (true)
        {
            System.out.print(">>> ");
            command = sc.nextLine().strip();

            if (command.equals("exit") || command.equals("quit"))
            {
                coffeeInstance.commitDB.conn.close();
                coffeeInstance.devDB.conn.close();
                coffeeInstance.relDB.conn.close();
                coffeeInstance.fileDB.conn.close();
                coffeeInstance.repoDB.conn.close();
                System.exit(0);
            }
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