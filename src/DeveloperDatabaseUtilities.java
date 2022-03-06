import java.io.*;
import java.nio.*;
import java.sql.*;
import java.util.*;
import java.lang.*;
import java.util.regex.*;

class DeveloperDatabaseUtilities extends DatabaseUtilities
{
    private static String tableName = "developer";

    public ArrayList<String> getAllUsernames() throws SQLException
    {
        ArrayList<String> usernames = new ArrayList<String>();
        String query = "SELECT username FROM " + tableName;
        PreparedStatement pstmt = conn.prepareStatement(query);
        ResultSet rs = pstmt.executeQuery();
        while(rs.next()) usernames.add(rs.getString("username"));
        return usernames;
    }

    public ArrayList<String> getAllUserIDs() throws SQLException
    {
        ArrayList<String> userIDs = new ArrayList<String>();
        String query = "SELECT _id FROM " + tableName;
        PreparedStatement pstmt = conn.prepareStatement(query);
        ResultSet rs = pstmt.executeQuery();
        while(rs.next()) userIDs.add(rs.getString("userID"));
        return userIDs;
    }

    public ArrayList<String> getAllEmailAddresses() throws SQLException
    {
        ArrayList<String> emailAddresses = new ArrayList<String>();
        String query = "SELECT email FROM " + tableName;
        PreparedStatement pstmt = conn.prepareStatement(query);
        ResultSet rs = pstmt.executeQuery();
        while(rs.next()) emailAddresses.add(rs.getString("email"));
        return emailAddresses;
    }

    public void createUser(String userID, String username, String emailAddress, String password) throws SQLException
    {
        String query = "INSERT INTO " + tableName + " (_id, username, email, password) VALUES (?, ?, ?, ?)";
        PreparedStatement pstmt = conn.prepareStatement(query);
        pstmt.setString(1, userID);
        pstmt.setString(2, username);
        pstmt.setString(3, emailAddress);
        pstmt.setString(4, password);
        pstmt.executeUpdate();
    }

    public Boolean validateUsername(String username) throws SQLException
    {

        if (username.length() < 3 || username.length() > 50)
        {
            System.out.println("Username must be between 3 and 50 characters");
            return false;
        }
        Pattern pattern = Pattern.compile("^[A-Za-z0-9]+(?:[ _-][A-Za-z0-9]+)*$");
        Matcher matcher = pattern.matcher(username);
        boolean validUsernameCheck = matcher.matches();
        if (!validUsernameCheck)
        {
            System.out.println("Invalid username! Username cannot contain special characters at the beginning or end, or consecutively!");
            return false;
        }
        ArrayList<String> usernames = getAllUsernames();
        if (usernames.contains(username))
        {
            System.out.println("Sorry, that username already exists! Please try another one.");
            return false;
        }
        return true;
    }

    public Boolean validateEmailAddress(String emailAddress) throws SQLException
    {
        Pattern pattern = Pattern.compile("^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,6}$");
        Matcher matcher = pattern.matcher(emailAddress);
        boolean validEmailAddressCheck = matcher.matches();
        if (!validEmailAddressCheck)
        {
            System.out.println("Invalid email address format! Please try again.");
            return false;
        }
        ArrayList<String> emailAddresses = getAllEmailAddresses();
        if (emailAddresses.contains(emailAddress))
        {
            System.out.println("The entered address already has a coffee account! Use another email address or login to your existing account.");
            return false;
        }
        return true;
    }

    public Boolean validatePassword(String password) throws SQLException
    {
        Pattern pattern = Pattern.compile("^(?=.*[A-Za-z])(?=.*\\d)[A-Za-z\\d]{8,}$");
        Matcher matcher = pattern.matcher(password);
        boolean validPasswordCheck = matcher.matches();
        if (!validPasswordCheck)
        {
            System.out.println("Invalid password! Password must contain at least one letter and one number, and must be at least 8 characters long.");
            return false;
        }
        return true;
    }

    public String validateUserCredentials(String username, String password) throws SQLException
    {
        String query = "SELECT _id FROM " + tableName + " WHERE username = ? AND password = ?";
        PreparedStatement pstmt = conn.prepareStatement(query);
        pstmt.setString(1, username);
        pstmt.setString(2, password);
        ResultSet rs = pstmt.executeQuery();
        if (rs.next()) return rs.getString("_id");
        return null;
    }
}

