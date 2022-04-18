import java.nio.*;
import java.nio.file.*;
import java.io.*;
import java.util.*;
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
        this.API_KEY = "sl.BDrNOM7-n0dNCnBTGe8F0bRP_r6CDkAvtTD7arCwC7UpwI1iFb5DoSSyG0xnGETlhQRGsobpKlFx-q9kYI8ga6SisxUohv9ew042iWjn701l1b_aj8vaX9cAWKRjZmJ5a8JRf-sluiFg";
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

            if (!fileName.startsWith(".togepi"))
            {
                outputString.add(fileName);
            }
        }

        return outputString;
    }

    // public LocalDateTime getLastCloudCommitTime(String dropboxPath) throws DbxException, ClassNotFoundException, IOException

    // public LocalDateTime getLastLocalCommitTime(String localPath) throws DbxException, ClassNotFoundException, IOException

    public void downloadFolder(String localPath, String dropboxPath) throws DbxException, ClassNotFoundException, IOException, InterruptedException
    {
        // handle pull condition in calling function
        if (dropboxPath.charAt(0) != '/') dropboxPath = "/" + dropboxPath;
        FileOutputStream downloadedFolder = new FileOutputStream(localPath);
        client.files().downloadZipBuilder(dropboxPath).start().download(downloadedFolder);
        Process p = Runtime.getRuntime().exec("unzip -o " + localPath);
        p.waitFor();
        downloadedFolder.close();
        File f = new File(localPath);
        f.delete();
    }
}