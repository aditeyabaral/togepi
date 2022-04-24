import java.nio.*;
import java.nio.file.*;
import java.io.*;
import java.util.*;
import java.time.format.*;
import java.time.*;
import java.util.stream.*;
import com.dropbox.core.*;
import com.dropbox.core.v2.*;
import com.dropbox.core.v2.files.*;
import com.dropbox.core.v2.users.*;
// import com.dropbox.core.v2.users.FullAccount;

class DropBoxUtilities
{
    String API_KEY;
    DbxClientV2 client;
    DbxRequestConfig config;

    public DropBoxUtilities()
    {
        this.API_KEY = "sl.BGNCAH9Y1hhVUYc-Sbhk8ie1NNR2H5cP7x2LMLikY2Ebp0LM6HebbH_uK_Ulc5LkBmSWJ56GhArTaZUUFqKXUCEiAHlZ6oa_eowpOYIPb_HPhfEunz2tsZdlVFXexoqIvGEB2zlCGMeH";
        this.config = DbxRequestConfig.newBuilder("dropbox/java-tutorial").build();
        this.client = new DbxClientV2(config, API_KEY);
    }

    public void downloadFile(String localPath, String dropboxPath) throws DbxException, ClassNotFoundException, IOException
    {
        if (dropboxPath.charAt(0) != '/') dropboxPath = "/" + dropboxPath;
        FileOutputStream downloadedFile = new FileOutputStream(localPath);
        try 
        {
            client.files().download(dropboxPath).download(downloadedFile);
        } 
        finally 
        {
            downloadedFile.close();
        }
    }

    public String getFileContent(String dropboxPath) throws DbxException, ClassNotFoundException, IOException
    {
        if (dropboxPath.charAt(0) != '/') dropboxPath = "/" + dropboxPath;
        StringBuilder sb = new StringBuilder();
        try (InputStream in = client.files().download(dropboxPath).getInputStream()) 
        {
            BufferedReader br = new BufferedReader(new InputStreamReader(in));
            String line;
            while ((line = br.readLine()) != null)
            {
                sb.append(line);
                sb.append("\n");
            }
        }
        return sb.toString();
    }

    public void uploadFile(String localPath, String dropboxPath) throws DbxException, ClassNotFoundException, IOException
    {
        if (dropboxPath.charAt(0) != '/') dropboxPath = "/" + dropboxPath;
        FileInputStream uploadedFile = new FileInputStream(localPath);
        try 
        {
            client.files().uploadBuilder(dropboxPath).withMode(WriteMode.OVERWRITE).uploadAndFinish(uploadedFile);
        } 
        finally 
        {
            uploadedFile.close();
        }
    }

    public ArrayList<String> listDropBoxFiles(String dropboxPath) throws DbxException, ClassNotFoundException, IOException
    {
        if (dropboxPath.equals("/")) dropboxPath = "";
        ArrayList<String> fileList = new ArrayList<String>();
        for (Metadata metadata : client.files().listFolder(dropboxPath).getEntries()) 
        {
            fileList.add(metadata.getPathLower());
        }
        return fileList;
    }

    public void createFolder(String dropboxPath) throws DbxException, ClassNotFoundException, IOException
    {
        if (dropboxPath.charAt(0) != '/') dropboxPath = "/" + dropboxPath;
        client.files().createFolder(dropboxPath);
    }

    public ArrayList<String> uploadFolder(String localPath, String dropboxPath) throws DbxException, ClassNotFoundException, IOException
    {
        if (dropboxPath.charAt(0) != '/') dropboxPath = "/" + dropboxPath;
        ArrayList<String> fileList = new ArrayList<String>();
        Files.find(Paths.get(localPath), 999, (p, bfa) -> true).forEach(path -> fileList.add(path.toString()));

        ArrayList<String> outputString = new ArrayList<String>();
        for (String file : fileList)
        {
            String fileName = "/" + file;
            fileName = Paths.get(fileName).normalize().toString();
            fileName = dropboxPath + fileName;
            System.out.println("Uploading " + fileName);
            if (Files.isDirectory(Paths.get(file)))
            {
                try
                {
                    createFolder(fileName);
                }
                catch (DbxException e)
                {
                    // System.out.println("Folder already exists");
                    ;
                }
            }
            else
            {
                uploadFile(file, fileName);
            }

            if (!fileName.startsWith(".coffee"))
            {
                outputString.add(fileName);
            }
        }

        return outputString;
    }

    public LocalDateTime getLastDropBoxCommitTime(String dropboxPath) throws DbxException, ClassNotFoundException, IOException
    {
        if (dropboxPath.charAt(0) != '/') dropboxPath = "/" + dropboxPath;
        dropboxPath = dropboxPath + "/.coffee";
        String fileName, timestamp;
        ArrayList<String> fileList = listDropBoxFiles(dropboxPath);
        ArrayList<LocalDateTime> commitTimes = new ArrayList<LocalDateTime>();
        for (String file : fileList)
        {
            fileName = file.substring(dropboxPath.length() + 1);
            if (fileName.equals(".bean")) continue;
            String[] fileNameSplit = fileName.split("$");
            timestamp = fileNameSplit[fileNameSplit.length - 1];
            LocalDateTime localDateTime = LocalDateTime.parse(timestamp, DateTimeFormatter.ofPattern("%Y-%m-%d---%H:%M:%S"));
            commitTimes.add(localDateTime);
        }
        commitTimes.sort(Comparator.naturalOrder());
        int num_commits = commitTimes.size();
        if (num_commits == 0) return null;
        return commitTimes.get(commitTimes.size() - 1);
    }

    public LocalDateTime getLastLocalCommitTime() throws DbxException, ClassNotFoundException, IOException
    {
        ArrayList<LocalDateTime> commitTimes = new ArrayList<LocalDateTime>();
        File commitDirectory = new File(".coffee");
        String fileName, timestamp;
        for (File file : commitDirectory.listFiles())
        {
            fileName = file.getName();
            if (fileName.equals(".bean")) continue;
            String[] fileNameSplit = fileName.split("$");
            timestamp = fileNameSplit[fileNameSplit.length - 1];
            LocalDateTime localDateTime = LocalDateTime.parse(timestamp, DateTimeFormatter.ofPattern("%Y-%m-%d---%H:%M:%S"));
            commitTimes.add(localDateTime);
        }
        commitTimes.sort(Comparator.naturalOrder());
        int num_commits = commitTimes.size();
        if (num_commits == 0) return null;
        return commitTimes.get(commitTimes.size() - 1);
    }

    
    public void downloadFolder(String localPath, String dropboxPath, boolean pull) throws DbxException, ClassNotFoundException, IOException, InterruptedException
    {

        String absolutePath = System.getProperty("user.dir") + localPath;
        if (pull == true) 
        {
            // Change to the parent directory
            absolutePath = absolutePath.substring(0, absolutePath.lastIndexOf("/"));
        }

        localPath = absolutePath + "CLONE.zip";
        localPath = Paths.get(localPath).normalize().toString();
        if (dropboxPath.charAt(0) != '/') dropboxPath = "/" + dropboxPath;
        FileOutputStream downloadedFolder = new FileOutputStream(localPath);
        client.files().downloadZipBuilder(dropboxPath).start().download(downloadedFolder);
        Process p = Runtime.getRuntime().exec("unzip -o " + localPath + " -d " + localPath.substring(0, localPath.length() - 9));
        p.waitFor();
        downloadedFolder.close();
        File f = new File(localPath);
        f.delete();
    }

    public void downloadFolder(String localPath, String dropboxPath) throws DbxException, ClassNotFoundException, IOException, InterruptedException
    {
        downloadFolder(localPath, dropboxPath, false);
    }

}