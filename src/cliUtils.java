import java.io.*;
import java.nio.file.*;

class CliUtils
{
    public void clearScreen()
    {
        System.out.print("\033[H\033[2J");
        System.out.flush();
    }

    // public void nano(String filename);

    public void ls(String path)
    {
        // Check for . as well as path
        String current_path = System.getProperty("user.dir");
        path = Paths.get(current_path, path).toString();
        try
        {
            Files.list(Paths.get(path)).forEach(System.out::println);
        }
        catch (IOException e)
        {
            System.out.println("Error: " + e.getMessage());
        }
    }

    public void cat(String filename)
    {
        try
        {
            String current_path = System.getProperty("user.dir");
            filename = Paths.get(current_path, filename).toString();
            File file = new File(filename);
            if (file.exists())
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
            Path folder_path = Paths.get(current_path, path);
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

    public void rmdir(String path)
    {
        try
        {
            String current_path = System.getProperty("user.dir");
            Path folder_path = Paths.get(current_path, path);
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

    // public void help();

    public void togepi()
    {
        String s = "                            ...:`                 \n"
        + "           `....         ...    /                 \n"
        + "           /   `....` ...    `  `/                \n"
        + "          --        `-`     ``````:  .-.--......  \n"
        + "          /`               ```````:-.```````  `/  \n"
        + "          /`     ``.-.    ``..```````         .:  \n"
        + " `..     `/`    --:d/    ```oo`:``````````````/   \n"
        + "-```--. .-`     -.:- +o+/```h+`/`````````````-`   \n"
        + ":`   `.:-: `.`   `` `sss-`````.`````````````-.    \n"
        + "`-`    `::..`:   .` .so/```````````````````.-     \n"
        + " :```  `-    `:`-.-../-.-.``````````````````-     \n"
        + "  :````:`.`   -.     ``  :-```..-.   `.--...:....`\n"
        + "  `:----+o:               .-..`` :.`.---.`      --\n"
        + "   :..`:os`    :-..`       `` `.:/+-``-       `.: \n"
        + "   /````..     :`...--`      -+o-/s- :```````.--  \n"
        + "   /```        +-+`-::/:-`   .so`/o+ -/.```./-`   \n"
        + "   +`::`   ````+/o`  -+:+-    +o+o/.``.---../     \n"
        + "   /soso-``  ``-++/./+++-``````-.``````````:`     \n"
        + "    oooos+.   ``/+++++:``````````..````````:      \n"
        + "    `/`/sos:`  ``//:-`````````.:+++/```` `:       \n"
        + "     `:`-oos+```````````````./++/o+:`  ``:        \n"
        + "       --.sos/`````````````:+o/.:+o`  `-.         \n"
        + "        `/os+`````````````+++o//+o-`.-.           \n"
        + "     `-..``.:---```````````-::///+:-/--`          \n"
        + "    :--`    `..:+-.----..----:/::.`   `.-.        \n"
        + "    -+....----.               `--.     .-:.       \n"
        + "                                 `....----";
    System.out.println(s);
    }
}