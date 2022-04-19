import java.sql.*;
import java.util.*;
import java.time.*;

class CommitDatabaseUtilities extends DatabaseUtilities
{
    private static String tableName = "commit";

    public ArrayList<String> getAllCommitID() throws SQLException
    {
        ArrayList<String> commitIDs = new ArrayList<String>();
        String query = "SELECT _id FROM " + tableName;
        PreparedStatement pstmt = conn.prepareStatement(query);
        ResultSet rs = pstmt.executeQuery();
        while(rs.next()) commitIDs.add(rs.getString("_id"));
        return commitIDs;
    }

    public void createCommit(String commitID, String userID, String repositoryID, LocalDateTime commitTime, String fileID, String commitMessage) throws SQLException
    {
        String query = "INSERT INTO " + tableName + " (_id, developer_id, repository_id, time, message, file_id) VALUES (?, ?, ?, ?, ?, ?)";
        PreparedStatement pstmt = conn.prepareStatement(query);
        pstmt.setString(1, commitID);
        pstmt.setString(2, userID);
        pstmt.setString(3, repositoryID);
        pstmt.setTimestamp(4, Timestamp.valueOf(commitTime));
        pstmt.setString(5, commitMessage);
        pstmt.setString(6, fileID);
        pstmt.executeUpdate();
    }
}
