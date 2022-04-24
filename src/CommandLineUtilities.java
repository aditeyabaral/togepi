import java.io.*;
import java.nio.file.*;

class CommandLineUtilities
{
    public void clearScreen()
    {
        System.out.print("\033[H\033[2J");
        System.out.flush();
    }

    public void ls(String path)
    {
        // normalize paths
        String current_path = System.getProperty("user.dir");
        path = Paths.get(current_path, path).normalize().toString();
        try
        {
            Files.list(Paths.get(path)).forEach(System.out::println);
        }
        catch (IOException e)
        {
            System.out.println("Error: " + e.getMessage());
        }
    }

    public void ls()
    {
        ls(".");
    }

    public void cat(String filename)
    {
        try
        {
            String current_path = System.getProperty("user.dir");
            filename = Paths.get(current_path, filename).normalize().toString();
            File file = new File(filename);
            if (file.exists() && file.isFile())
            {
                BufferedReader br = new BufferedReader(new FileReader(file));
                String line;
                while ((line = br.readLine()) != null)
                {
                    System.out.println(line);
                }
                br.close();
            }
            else
            {
                System.out.println("Error: File does not exist");
            }
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
    }

    public void mkdir(String path)
    {
        try
        {
            String current_path = System.getProperty("user.dir");
            Path folder_path = Paths.get(current_path, path).normalize();
            File folder = new File(folder_path.toString());
            if (!folder.exists())
            {
                folder.mkdir();
            }
            else
            {
                System.out.println("Error: Folder already exists");
            }
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
    }

    public void rm(String path)
    {
        try
        {
            String current_path = System.getProperty("user.dir");
            Path file_path = Paths.get(current_path, path).normalize();
            File file = new File(file_path.toString());
            if (file.exists() && file.isFile())
            {
                file.delete();
            }
            else
            {
                System.out.println("Error: File does not exist");
            }
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
    }

    public void rmdir(String path)
    {
        try
        {
            String current_path = System.getProperty("user.dir");
            Path folder_path = Paths.get(current_path, path).normalize();
            File folder = new File(folder_path.toString());
            if (folder.exists())
            {
                folder.delete();
            }
            else
            {
                System.out.println("Error: Folder does not exist");
            }
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
    }

    public void cd(String path)
    {
        try
        {
            String current_path = System.getProperty("user.dir");
            Path folder_path = Paths.get(current_path, path).normalize();
            File folder = new File(folder_path.toString());
            if (folder.exists())
            {
                System.setProperty("user.dir", folder_path.toString());
            }
            else
            {
                System.out.println("Error: Folder does not exist");
            }
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
    }

    // public void nano(String filename);

    public void help() {
        // TODO: add cfe commands
        System.out.println("ls: list files and folders");
        System.out.println("cat: display file contents");
        System.out.println("mkdir: create a new folder");
        System.out.println("rm: delete a file");
        System.out.println("rmdir: delete a folder");
        System.out.println("cd: change current directory");
        System.out.println("clear: clear the screen");
        System.out.println("help: display this message");
    }

    public void coffee()
    {
        String s = "                                                      \n"  +                           
        "                                                                  \n" +      
        "                                                    %%% %%%%#     \n" +      
        "                                                 %%%%%%(%%%%%%%   \n" +      
        "                                              (%%%%%%% %%%%%%%%%  \n" +      
        "    %%%%%%%%%%%.                             %%%%%%%%% %%%%%%%%%# \n" +      
        "   %%%%%%%%%%%%%%%%%                        %%%%%%%%%  %%%%%%%%%% \n" +      
        " %% .%%%%%%%%%%%%%%%%%%                    %%%%%%%%%   %%%%%%%%%% \n" +      
        "%%%%%% %%%%%%%%%%%%%%%%%%                 %%%%%%%%%*   %%%%%%%%%% \n" +      
        "%%%%%%%%  %%%%%%%%%%%%%%%%%               %%%%%%%%%    %%%%%%%%%  \n" +      
        "%%%%%%%%%%    %%%%%%%%%%%%%%              %%%%%%%%%   %%%%%%%%%   \n" +      
        " %%%%%%%%%%.     %%%%%%%%%%%%             %%%%%%%%%  %%%%%%%%%    \n" +      
        " *%%%%%%%%%%%      %%%%%%%%%%%            #%%%%%%%% #%%%%%%%      \n" +      
        "  *%%%%%%%%%%%%#     %%%%%%%%%%            (%%%%%%% %%%%%%(       \n" +      
        "    %%%%%%%%%%%%%%%   *%%%%%%%%              %%%%%% %%%%          \n" +      
        "     %%%%%%%%%%%%%%%%%  %%%%%%%(                                  \n" +      
        "       %%%%%%%%%%%%%%%%%% *%%%%                                   \n" +      
        "          %%%%%%%%%%%%%%%%%%                                      \n" +      
        "             %%%%%%%%%%%%%%%#                                     \n" +      
        "                  .%%%%%%%                                        \n" +      
        "                                              %%%%%% %%%          \n" +      
        "                                           %%%%%%%% %%%%%         \n" +      
        "                                         %%%%%%%%  %%%%%%%        \n" +      
        "                                       %%%%%%%%   %%%%%%%         \n" +      
        "                                      %%%%%%%%   %%%%%%%%         \n" +      
        "                                     (%%%%%%%  %%%%%%%%#          \n" +      
        "                                     #%%%%%% *%%%%%%%%            \n" +      
        "                                      %%%%% %%%%%%%               \n" +      
        "                                       #%% %%%%%                  \n" +      
        "                                                                  \n";     
        System.out.println(s);
    }
}