import java.io.*;
import java.nio.*;
import java.sql.*;
import java.util.*;
import java.lang.*;

class DatabaseUtilities
{
    private static String url;
    private static String user;
    private final String password;
    Connection conn;
    DatabaseUtilities()
    {
        url = "jdbc:postgresql://ec2-54-83-82-187.compute-1.amazonaws.com:5432/d3au8v0r6o7dut";
        user = "kphftpinxhfrbj";
        password = "c2d60d0b6766191a629bc71e6e60bb36090ca28361052e1902bc9e78c2b53c48";
    }

    public void connect() throws SQLException, ClassNotFoundException
    {
        // Class.forName("org.postgresql.Driver");
        conn = DriverManager.getConnection(url, user, password);
    }
}