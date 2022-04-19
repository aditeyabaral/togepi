import java.io.*;
import java.nio.*;
import java.sql.*;
import java.util.*;
import java.lang.*;
import java.util.regex.*;

class RelationDatabaseUtilities extends DatabaseUtilities
{
    private static String tableName = "repositoryuserelation";

    public void createUserRepositoryRelation(String userID, String repositoryID, String relation) throws SQLException
    {
        String query = "INSERT INTO " + tableName + " (developer_id, repository_id, relation) VALUES (?, ?, ?)";
        PreparedStatement pstmt = conn.prepareStatement(query);
        pstmt.setString(1, userID);
        pstmt.setString(2, repositoryID);
        pstmt.setString(3, relation);
        pstmt.executeUpdate();
    }

    public String getUserRepositoryRelation(String userID, String repositoryID) throws SQLException
    {
        String query = "SELECT relation FROM " + tableName + " WHERE developer_id = ? AND repository_id = ?";
        PreparedStatement pstmt = conn.prepareStatement(query);
        pstmt.setString(1, userID);
        pstmt.setString(2, repositoryID);
        ResultSet rs = pstmt.executeQuery();
        if (rs.next()) return rs.getString("relation");
        else return null;
    }

    public HashMap<String, String> getAllRelations(String repositoryID) throws SQLException
    {
        HashMap<String, String> relations = new HashMap<String, String>();
        String query = "SELECT * FROM " + tableName + " WHERE repository_id = ?";
        PreparedStatement pstmt = conn.prepareStatement(query);
        pstmt.setString(1, repositoryID);
        ResultSet rs = pstmt.executeQuery();
        while(rs.next())
        {
            relations.put(rs.getString("developer_id"), rs.getString("relation"));
        }
        return relations;
    }

    public String getRepositoryOwnerFromRepositoryId(String repositoryId) throws SQLException
    {
        String query = "SELECT developer_id FROM " + tableName + " WHERE repository_id = ? AND relation = 'owner'";
        PreparedStatement pstmt = conn.prepareStatement(query);
        pstmt.setString(1, repositoryId);
        ResultSet rs = pstmt.executeQuery();
        if (rs.next()) return rs.getString("developer_id");
        else return null;
    }
}

// class TestRelationDatabaseUtilities
// {
//     public static void main(String[] args) throws Exception
//     {
//         RelationDatabaseUtilities rdu = new RelationDatabaseUtilities();
//         rdu.connect();
//         rdu.createUserRepositoryRelation("181b0f1e-9d7a-11ec-8e79-b11667294a65", "1", "owner");
//         rdu.createUserRepositoryRelation("64bddb9f-a1d6-11ec-9def-f99dab75ea53", "1", "collaborator");
//         System.out.println(rdu.getUserRepositoryRelation("64bddb9f-a1d6-11ec-9def-f99dab75ea53", "1"));
//         System.out.println(rdu.getUserRepositoryRelation("181b0f1e-9d7a-11ec-8e79-b11667294a65", "1"));
//         System.out.println(rdu.getAllRelations("1"));
//         System.out.println(rdu.getRepositoryOwnerFromRepositoryId("1"));
//     }
// }