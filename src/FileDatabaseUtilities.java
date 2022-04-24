import java.time.*;
import java.util.*;
import java.sql.*;

public class FileDatabaseUtilities extends DatabaseUtilities {
    private String fileTableName = "file";

    public void createFile(String fileID, String path, String repositoryId, String status, LocalDateTime lastModified, LocalDateTime lastCommitted, LocalDateTime lastPushed) {
        String query = "INSERT INTO " + fileTableName + " (_id, path, repository_id, status, last_modified, last_committed, last_pushed) VALUES (?, ?, ?, ?, ?, ?, ?)";
        PreparedStatement pstmt;
        try {
            pstmt = conn.prepareStatement(query);
            pstmt.setString(1, fileID);
            pstmt.setString(2, path);
            pstmt.setString(3, repositoryId);
            pstmt.setString(4, status);
            pstmt.setObject(5, lastModified);
            pstmt.setObject(6, lastCommitted);
            pstmt.setObject(7, lastPushed);
            
            pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public ArrayList<String> getTrackedFiles(String repositoryId) {
        ArrayList<String> trackedFiles = new ArrayList<String>();
        String query = "SELECT path FROM " + fileTableName + " WHERE repository_id = ?";
        PreparedStatement pstmt;
        try {
            pstmt = conn.prepareStatement(query);
            pstmt.setString(1, repositoryId);
            ResultSet rs = pstmt.executeQuery();
            while (rs.next()) {
                trackedFiles.add(rs.getString("path"));
            }
            return trackedFiles;
        } catch (SQLException e) {
            e.printStackTrace();
            return null;
        }
    }

    public ArrayList<String> getAllFileID() {
        ArrayList<String> fileIDs = new ArrayList<String>();
        String query = "SELECT _id FROM " + fileTableName;
        PreparedStatement pstmt;
        try {
            pstmt = conn.prepareStatement(query);
            ResultSet rs = pstmt.executeQuery();
            while (rs.next()) {
                fileIDs.add(rs.getString("_id"));
            }
            return fileIDs;
        } catch (SQLException e) {
            e.printStackTrace();
            return null;
        }
    }

    public String getFileID(String repoID, String fileName) {
        String query = "SELECT _id FROM " + fileTableName + " WHERE repository_id = ? AND path = ?";
        PreparedStatement pstmt;
        try {
            pstmt = conn.prepareStatement(query);
            pstmt.setString(1, repoID);
            pstmt.setString(2, fileName);
            ResultSet rs = pstmt.executeQuery();
            if(rs.next()) {
                return rs.getString("_id");
            }
            else {
                return null;
            }
        } catch (SQLException e) {
            e.printStackTrace();
            return null;
        }
    }

    public Boolean checkFileInDatabase(String repoID, String path) {
        String query = "SELECT _id FROM " + fileTableName + " WHERE repository_id = ? AND path = ?";
        PreparedStatement pstmt;
        try {
            pstmt = conn.prepareStatement(query);
            pstmt.setString(1, repoID);
            pstmt.setString(2, path);
            ResultSet rs = pstmt.executeQuery();
            if(rs.next()) {
                return true;
            }
            else return false;

        } catch (SQLException e) {
            e.printStackTrace();
            return false;
        }       
    }

    public void updateFileModifiedTime(String repoID, String path, LocalDateTime lastModifiedTime) {
        String query = "UPDATE " + fileTableName + " SET last_modified = ? WHERE repository_id = ? AND path = ?";
        PreparedStatement pstmt;
        try {
            pstmt = conn.prepareStatement(query);
            pstmt.setObject(1, lastModifiedTime);
            pstmt.setString(2, repoID);
            pstmt.setString(3, path);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return;
    }

    public void updateFileCommitTime(String repoID, String path, LocalDateTime lastCommitTime) {
        String query = "UPDATE " + fileTableName + " SET last_committed = ? WHERE repository_id = ? AND path = ?";
        PreparedStatement pstmt;
        try {
            pstmt = conn.prepareStatement(query);
            pstmt.setObject(1, lastCommitTime);
            pstmt.setString(2, repoID);
            pstmt.setString(3, path);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return;
    }
    
    public void updateFilePushTime(String repoID, String path, LocalDateTime lastPushTime) {
        String query = "UPDATE " + fileTableName + " SET last_pushed = ? WHERE repository_id = ? AND path = ?";
        PreparedStatement pstmt;
        try {
            pstmt = conn.prepareStatement(query);
            pstmt.setObject(1, lastPushTime);
            pstmt.setString(2, repoID);
            pstmt.setString(3, path);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }

        String query2 = "UPDATE " + fileTableName + " SET status = 'unchanged' WHERE repository_id = ? AND path = ?";
        PreparedStatement pstmt2;
        try {
            pstmt2 = conn.prepareStatement(query2);
            pstmt2.setString(1, repoID);
            pstmt2.setString(2, path);
            pstmt2.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }

        return;
    }

    public Timestamp getLastModifiedTime(String repoID, String path) {
        String query = "SELECT last_modified FROM " + fileTableName + " WHERE repository_id = ? AND path = ?";
        PreparedStatement pstmt;
        try {
            pstmt = conn.prepareStatement(query);
            pstmt.setString(1, repoID);
            pstmt.setString(2, path);
            ResultSet rs = pstmt.executeQuery();
            return rs.getTimestamp("last_modified");
        } catch (SQLException e) {
            e.printStackTrace();
            return null;
        }
    }   
}