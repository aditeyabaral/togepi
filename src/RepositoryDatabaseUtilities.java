import java.io.*;
import java.nio.*;
import java.sql.*;
import java.util.*;
import java.lang.*;
import java.time.*;
import java.util.regex.*;

class RepositoryDatabaseUtilities extends DatabaseUtilities
{

    RepositoryDatabaseUtilities() {
        super("repository");
    }

    public void createRepository(String repositoryId, String repositoryName, String description, String url, LocalDateTime createTime, String visibility, String userId)
    {
        String query = "INSERT INTO " + tableName + " (_id, name, description, url, create_time, visibility, owner_id) VALUES (?, ?, ?, ?, ?, ?, ?)";
        try
        {
            PreparedStatement pstmt = conn.prepareStatement(query);
            pstmt.setString(1, repositoryId);
            pstmt.setString(2, repositoryName);
            pstmt.setString(3, description);
            pstmt.setString(4, url);
            pstmt.setTimestamp(5, Timestamp.valueOf(createTime));
            pstmt.setString(6, visibility);
            pstmt.setString(7, userId);
            pstmt.executeUpdate();
        }
        catch (SQLException e)
        {
            e.printStackTrace();
        }
    }

    public ArrayList<String> getAllRepositoryId() throws SQLException
    {
        ArrayList<String> repositoryIds = new ArrayList<String>();
        String query = "SELECT _id FROM " + tableName;
        PreparedStatement pstmt = conn.prepareStatement(query);
        ResultSet rs = pstmt.executeQuery();
        while(rs.next()) repositoryIds.add(rs.getString("_id"));
        return repositoryIds;
    }

    public Boolean checkUserHasRepository(String userId, String repositoryName) throws SQLException
    {
        String query = "SELECT * FROM " + tableName + " WHERE owner_id = ? AND name = ?";
        PreparedStatement pstmt = conn.prepareStatement(query);
        pstmt.setString(1, userId);
        pstmt.setString(2, repositoryName);
        ResultSet rs = pstmt.executeQuery();
        if (rs.next()) return true;
        else return false;
    }

    public String getRepositoryVisbilityFromUsernameRepositoryName(String username, String repositoryName) throws SQLException
    {
        // use coffee instance passed here, using tableName for now
        String query = "SELECT _id from developer WHERE username = ?";
        PreparedStatement pstmt = conn.prepareStatement(query);
        pstmt.setString(1, username);
        ResultSet rs = pstmt.executeQuery();
        if (rs.next())
        {
            String developerId = rs.getString("_id");
            query = "SELECT visibility from " + tableName + " WHERE owner_id = ? AND name = ?";
            pstmt = conn.prepareStatement(query);
            pstmt.setString(1, developerId);
            pstmt.setString(2, repositoryName);
            rs = pstmt.executeQuery();
            if (rs.next()) return rs.getString("visibility");
            else return null;
        }
        else return null;
    }

    public String getRepositoryNameFromId(String repoId) throws SQLException
    {
        String query = "SELECT name FROM " + tableName + " WHERE _id = ?";
        PreparedStatement pstmt = conn.prepareStatement(query);
        pstmt.setString(1, repoId);
        ResultSet rs = pstmt.executeQuery();
        if (rs.next()) return rs.getString("name");
        else return null;
    }

    public String getRepositoryIdFromUserIdRepositoryName(String userId, String repositoryName) throws SQLException
    {
        String query = "SELECT _id FROM " + tableName + " WHERE owner_id = ? AND name = ?";
        PreparedStatement pstmt = conn.prepareStatement(query);
        pstmt.setString(1, userId);
        pstmt.setString(2, repositoryName);
        ResultSet rs = pstmt.executeQuery();
        if (rs.next()) return rs.getString("_id");
        else return null;
    }
}

// class TestRepositoryDatabaseUtilities
// {
//     public static void main(String[] args) throws Exception
//     {
//         RepositoryDatabaseUtilities rdu = new RepositoryDatabaseUtilities();
//         rdu.connect();
//         rdu.createRepository("2", "test", "test_desc", "test_url", LocalDateTime.now(), "public", "64bddb9f-a1d6-11ec-9def-f99dab75ea53");
//         System.out.println(rdu.getAllRepositoryId());
//         System.out.println(rdu.checkUserHasRepository("64bddb9f-a1d6-11ec-9def-f99dab75ea53", "test"));
//         System.out.println(rdu.getRepositoryVisbilityFromUsernameRepositoryName("adi", "test"));
//     }
// }