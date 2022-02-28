import java.sql.*;
import java.util.*;
import java.time.*;

class RepositoryDataBaseUtils
{
    Connection conn;
    public RepositoryDataBaseUtils(Connection conn)
    {
        this.conn = conn;
    }

    public void createRepository(String ownerID, String repoName, String repoID, String description, String url, LocalDateTime createTime, String visibility) throws SQLException
    {
        String sql = "INSERT INTO repository(owner_id, name, _id, description, url, create_time, visibility) VALUES(?,?,?,?,?,?,?)";
        PreparedStatement pstmt = conn.prepareStatement(sql);
        pstmt.setString(1, ownerID);
        pstmt.setString(2, repoName);
        pstmt.setString(3, repoID);
        pstmt.setString(4, description);
        pstmt.setString(5, url);
        pstmt.setTimestamp(6, Timestamp.valueOf(createTime));
        pstmt.setString(7, visibility);
        pstmt.executeUpdate();
    }

    public List<String> getAllRepositoryID() throws SQLException
    {
        List<String> repoIDList = new ArrayList<String>();
        String sql = "SELECT _id FROM repository";
        PreparedStatement pstmt = conn.prepareStatement(sql);
        ResultSet rs = pstmt.executeQuery();
        while(rs.next())
        {
            repoIDList.add(rs.getString("_id"));
        }
        return repoIDList;
    }
}

class TestDataBaseUtils
{
    public static void main(String[] args) throws SQLException, ClassNotFoundException
    {
        Class.forName("org.postgresql.Driver");
        String url = "jdbc:postgresql://ec2-54-83-82-187.compute-1.amazonaws.com:5432/d3au8v0r6o7dut";
        String user = "kphftpinxhfrbj";
        String password = "c2d60d0b6766191a629bc71e6e60bb36090ca28361052e1902bc9e78c2b53c48";
        Connection conn = DriverManager.getConnection(url, user, password);
        System.out.println("Connected to the database");

        RepositoryDataBaseUtils rdbu = new RepositoryDataBaseUtils(conn);

        rdbu.createRepository("USER#001", "test", "REPO#002", "my first repo", "test", LocalDateTime.now(), "public");


        List<String> repoIDList = rdbu.getAllRepositoryID();
        System.out.println(repoIDList);
        for(String repoID : repoIDList)
        {
            System.out.println(repoID);
        }
    }
}