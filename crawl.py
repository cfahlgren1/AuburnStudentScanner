import os, grp, time, sys
from time import sleep

print (" " + """

############################################
  ___          _                             
 / _ \        | |                            
/ /_\ \ _   _ | |__   _   _  _ __  _ __      
|  _  || | | || '_ \ | | | || '__|| '_ \     
| | | || |_| || |_) || |_| || |   | | | |    
\_| |_/ \__,_||_.__/  \__,_||_|   |_| |_|    
 _____  _               _               _    
/  ___|| |             | |             | |   
\ `--. | |_  _   _   __| |  ___  _ __  | |_  
 `--. \| __|| | | | / _` | / _ \| '_ \ | __| 
/\__/ /| |_ | |_| || (_| ||  __/| | | || |_  
\____/  \__| \__,_| \__,_| \___||_| |_| \__| 
 _____                                       
/  ___|                                      
\ `--.   ___  __ _  _ __   _ __    ___  _ __ 
 `--. \ / __|/ _` || '_ \ | '_ \  / _ \| '__|
/\__/ /| (__| (_| || | | || | | ||  __/| |   
\____/  \___|\__,_||_| |_||_| |_| \___||_|  
 

############################################                             
                                             
""")

time.sleep(0.5)

# Change directory to root home
os.chdir("/home")

# Top Level User Directories
dirList = ['new-ece', 'u1', 'u2', 'u3', 'che_h2', 'cse_h1', 'cse_h2']

# Ignore these common system directories
ignoreDirList = ['.evolution', '.matlab', '.nautilus', '.mozilla', '.felix', 'Connections', 'UserData', '$RECYCLE.BIN',
                 '.config', '.local', '.ssh', '.wastebasket', '.fm',
                 '.netscape-cache', '.login', '.logout', '.Xdefaults', 'Desktop', 'Documents', 'Application Data',
                 'appdata', 'bash_history', '.cache', '.openwin-init', 'Startup', 'Accessories', 'Programs',
                 'Administrative Tools', 'Libraries', 'SendTo', 'Start Menu', 'Themes', 'AccountPictures', 'Recent',
                 'My Pictures', 'CachedFiles', 'Pinned', 'abrt', 'share', 'mail', 'Vault', 'Microsoft', 'ClassicShell',
                 'Internet Explorer', 'Network', 'Windows', 'Quick Launch', 'User Pinned', 'ImplicitAppShortcuts',
                 'Pbk', '_hiddenPbk', 'Recent', 'AutomaticDestinations', 'CustomDestinations', 'Oracle', 'Adobe',
                 '.appdata', '.Application Data', 'Application Data', 'Mozilla', 'Custom Office Templates']

# Ignore these common system files
ignoreFileList = ['.fm', 'wastebasket', '.login', '.Xdefaults', 'ntuser.cmd', 'Bluetooth File Transfer.LNK',
                  'Documents.library-ms', 'Pictures.library-ms', 'mail', '.logout', '.bash_history', 'Xdefaults',
                  '.openwin-init', '.cshrc', 'known_hosts', '$RECYCLE.BIN', 'desktop.ini', 'Google Chrome.lnk',
                  'lastnotification', 'Documents.mydocs', 'Bluetooth File Transer.LNK', 'TranscodedWallpaper',
                  'CachedImage_1920_1080_POS4.jpg', 'Videos.library-ms', 'Music.library-ms', 'startscreen.lnk',
                  'motd.legal-displayed', 'Internet Explorer.lnk', 'rasphone.pbk',
                  'f01b4d95cf55d32a.customDestinations-ms', '5d696d521de238c3.customDestinations-ms',
                  '7e4dca80246863e3.customDestinations-ms']

# Counts on different user and types
incrementer = 0

newece_count = 0  # Count of users in new-ece directory
u1_count_total = 0  # Count of users in u1 directory
u2_count_total = 0  # Count of users in u2 directory
u3_count_total = 0  # Count of users in u3 directory
cse_h2_count_total = 0  # Count of users in cse_h2
cse_h1_count_total = 0  # Count of users in cse_h1
che_h2_count_total = 0  # Count of users in che_h2

active_users = 0  # Count of users that have created files
total_file_count = 0  # Count files in total
acc_file_count = 0  # Count files that are readable

neng_count = 0  # Count users in neng group
ee_count = 0  # Count users in ee group
ugrad_count = 0  # Count users in ugrad group

for directory in dirList:
    t0 = time.time()
    temp_path = ("/home/" + directory + "/")
    try:
        os.chdir(temp_path)
        for user_dirs in os.listdir(temp_path):
            if (user_dirs not in ignoreDirList):
                # Count how many users are in each directory
                if (directory == "u1"): u1_count_total += 1
                if (directory == "u2"): u2_count_total += 1
                if (directory == "u3"): u3_count_total += 1
                if (directory == "new-ece"): newece_count += 1
                if (directory == "cse_h1"): cse_h1_count_total += 1
                if (directory == "cse_h2"): cse_h2_count_total += 1
                if (directory == "che_h2"): cse_h2_count_total += 1

                # Variable to count number of files
                numOfFiles = 0
                numOfAccFiles = 0
                numOfWritable = 0

                # Set the path to change the directory
                user_path = (temp_path + user_dirs + "/")

                # User Count Incrementer
                incrementer += 1

                # Change Directory to User Folder and catch errors
                try:
                    os.chdir(user_path)
                    
                    # Grab group id and user id to use on folders
                    stat_info = os.stat(user_path)
                    uid = stat_info.st_uid
                    gid = stat_info.st_gid
                  
                    # Check if folder is part of the ee group
                    if (str(grp.getgrgid(gid)[0]) == "ee"):
                        ee_count += 1
                    # Check if folder is part of neng group
                    if (str(grp.getgrgid(gid)[0]) == "neng"):
                        neng_count += 1
                    # Check if folder is part of the ugrad group
                    if (str(grp.getgrgid(gid)[0]) == "ugrad"):
                        ugrad_count += 1

                except Exception:
                    continue

                # Crawl through user directory and count files
                for roots, dirs, files in os.walk(user_path):
                    # Count all files
                    for file in files:
                        # Check file against common system file list
                        if file not in ignoreFileList:
                            try:

                                # Check Different Accesses
                                check_access_file = os.access(file, os.R_OK)
                                check_x_access = os.access(file, os.X_OK)
                                check_w_access = os.access(file, os.W_OK)

                                # Check Read and Execute Access Permissions
                                if (check_access_file == True or check_x_access == True):
                                    acc_file_count += 1
                                    numOfAccFiles += 1
                                # Check Write Access
                                if (check_w_access == True):
                                    numOfWritable += 1

                            except Exception:
                                pass
                            # Increment the file count variables
                            numOfFiles += 1
                            total_file_count += 1
                # Check if user has created files and is active
                if (numOfFiles >= 1):
                    active_users += 1

                print(str(incrementer) + "\t USER: " + user_dirs + "\tPATH: " + user_path + "\tNumOfFiles: " + str(
                    numOfFiles) + "\tGROUP: " + str(grp.getgrgid(gid)[0]) + "\tAccessible Files: " + str(
                    numOfAccFiles) + "\tWritable: " + str(numOfWritable))

    # Catch Permission Denied Errors when opening directories
    except Exception():
        pass

# Print report
print("\n\nTOTAL COUNT:  " + str(incrementer))
print("ACTIVE USERS   :  " + str(active_users))
print("TOTAL FILE COUNT: " + str(total_file_count))
print("ACCESSIBLE FILES: " + str(acc_file_count))
print("new-ece count:    " + str(newece_count))
print("u1 total count:   " + str(u1_count_total))
print("u2 total count:   " + str(u2_count_total))
print("u3 total count:   " + str(u3_count_total))
print("cse_h1 total count: " + str(cse_h1_count_total))
print("cse_h2 total count: " + str(cse_h2_count_total))
print("che_h2 total count: " + str(che_h2_count_total))
print("ugrad group count: " + str(ugrad_count))
print("neng group count : " + str(neng_count))
print("ee group count   : " + str(ee_count))

