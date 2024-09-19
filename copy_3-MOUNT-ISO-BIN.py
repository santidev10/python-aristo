from subprocess import PIPE, Popen
import os, re, subprocess

os.chdir("/mnt/efs")
os.mkdir("Aristocrat-VLT/")
os.mkdir("Aristocrat-VLT/platform")
os.mkdir("Aristocrat-VLT/platform/packages")
os.mkdir("Aristocrat-VLT/platform/bin")
os.mkdir("disk")
retail_dirs = []
with Popen(["ls"], stdout=PIPE, bufsize=1, universal_newlines=True) as p:
    for dir in p.stdout:
        if re.search("^Monaco.*DEV.zip$", dir):
            dir_name = os.path.splitext(dir)[0]    # remove .zip
            os.mkdir(dir_name)
            zip_file = dir.strip()   # remove \n
# unzip DEV release
process = subprocess.Popen(['sudo', 'unzip', zip_file, '-d', dir_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = process.communicate()
if err:
     print('unzip raised an error:', err.decode())
     exit(1)

# Copy packages
# dir_name = "Monaco_WinnersWorldR25_270_FullBuild_Gdk35_2.7.0.8_DEV"   # this line only for testing this part
packages_dir = dir_name + "/Platform/packages/"
file_list = []
with Popen(["ls", packages_dir], text=True, stdout=PIPE) as p:
     for file in p.stdout:
          file_list.append(file.strip())
for file in file_list:
    file_str = packages_dir + "/" + file.strip()
    process = subprocess.Popen(['sudo', 'cp', file_str, "Aristocrat-VLT/platform/packages"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if err:
         print('Copy Packages raised an error:', err.decode())
         exit(1)
     
# Mount ISO and Copy BIN 
dir_name = "Monaco_WinnersWorldR25_270_FullBuild_Gdk35_2.7.0.8_DEV"  # this line only for testing this part
retail_dir = dir_name + "/RETAIL_Platform_Files/"
file_list = []
with Popen(["ls", retail_dir], text=True, stdout=PIPE) as p:
     for file in p.stdout:
          file_list.append(file.strip())
print(file_list)
for file in file_list:
     if "iso" in file:
          iso_file = file.strip()
          iso_path = retail_dir + iso_file
          subprocess.run(["sudo", "mount", "-o", "loop", iso_path, "/mnt/efs/disk"])
          print(iso_path)
disk_path = "/mnt/efs/disk/"
with Popen(["ls", disk_path], text=True, stdout=PIPE) as p:
     for file in p.stdout:
          file_str = disk_path + file.strip()
          #print(file_str)
          process = subprocess.Popen(['sudo', 'cp', '-dr', file_str, "Aristocrat-VLT/platform/bin"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
          out, err = process.communicate()
          if err:
               print('Copy Packages raised an error:', err.decode())
               exit(1)







