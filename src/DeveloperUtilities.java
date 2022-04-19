import java.io.*;
import java.sql.*;
import java.util.*;
import com.fasterxml.uuid.*;

class DeveloperUtilities
{
    public void logoutUser(Coffee coffee)
    {
        if (coffee.userID == null) System.out.println("You are not logged in.");
        else
        {
            coffee.userID = null;
            // coffee.repositoryID = null;
            System.out.println("Logged out successfully");
        }
    }

    public HashMap<String, String> getUserCredentials()
    {
        HashMap<String, String> credentials = new HashMap<String, String>();
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter your username: ");
        credentials.put("username", sc.nextLine().strip());
        System.out.print("Enter your password: ");
        // Console console = System.console();
        credentials.put("password", new String(System.console().readPassword()).strip());
        return credentials;
    }

    public void loginUser(Coffee coffee) throws SQLException
    {
        HashMap<String, String> credentials = getUserCredentials();
        String username = credentials.get("username");
        String password = credentials.get("password");
        System.out.println("Logging in...");
        String userID = coffee.devDB.validateUserCredentials(username, password);
        if (userID != null)
        {
            coffee.userID = userID;
            System.out.println("Logged in successfully. Welcome, " + username + "!");
            // return userID;
        }
        else System.out.println("Invalid username or password. Please try again.");
    }

    public String generateUserID()
    {
        return Generators.timeBasedGenerator().generate().toString();
    }

    public void registerUser(Coffee coffee) throws Exception 
    {
        // replace all with throws Exception
        // look for errors, rollback commit if dropbox job fails
        Scanner sc = new Scanner(System.in);

        String emailAddress;
        while (true)
        {
            System.out.print("Enter your email address: ");
            emailAddress = sc.nextLine().strip();
            if (coffee.devDB.validateEmailAddress(emailAddress)) break;
        }

        String username;
        while (true)
        {
            System.out.print("Enter a username: ");
            username = sc.nextLine().strip();
            if (coffee.devDB.validateUsername(username)) break;
        }

        String password;
        while (true)
        {
            System.out.print("Enter a password: ");
            password = new String(System.console().readPassword()).strip();
            if (coffee.devDB.validatePassword(password))
            {
                System.out.print("Confirm your password: ");
                if (new String(System.console().readPassword()).strip().equals(password)) break;
                else System.out.println("Passwords do not match. Please try again.");
            }
            else System.out.println("Invalid password. Please try again."); // display conditions for password strength
        }

        String userID = generateUserID();
        coffee.devDB.createUser(userID, username, emailAddress, password);
        coffee.dropBox.createFolder("/" + username);
        coffee.userID = userID;
        System.out.println("Logged in successfully. Welcome, " + username + "!");
        // return username
    }
}