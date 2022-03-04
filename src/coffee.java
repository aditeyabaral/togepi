import java.io.*;
import java.nio.*;
import java.sql.*;
import java.util.*;
import java.lang.*;
import java.util.regex.*;
import java.lang.reflect.*;

class Coffee
{
    String userID;
    String repositoryID;
    CommandLineUtilities cmd;
    Coffee()
    {
        userID = null;
        repositoryID = null;
        cmd = new CommandLineUtilities();
    }

    public static void main(String[] args) throws Exception
    {
        Class.forName("org.postgresql.Driver");
        
        CommandRunner runner = new CommandRunner();
        runner.initCommandMaps();

        Coffee coffee = new Coffee();
        Scanner sc = new Scanner(System.in);
        Boolean debug = args.length > 0 && args[0].equals("--debug");
        if (debug) System.out.println("Running in debug mode");
        System.out.println("Welcome to Coffee!");

        String command;
        while (true)
        {
            System.out.print(">>> ");
            command = sc.nextLine().strip();

            if (command.equals("exit") || command.equals("quit")) System.exit(0);
            else
            {
                try { runner.run(coffee, command); }
                catch (Exception e)
                {
                    if (debug) e.printStackTrace();
                    else System.out.println("Invalid command. Type help to learn more.\nYou can also visit https://github.com/Yashi-Chawla/coffee#how-to-use-coffee to read the entire documentation.");
                }

            }
        }
    }
}