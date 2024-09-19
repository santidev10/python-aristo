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

process = subprocess.Popen(['sudo', 'unzip', zip_file, '-d', dir_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = process.communicate()
if err:
     print('unzip raised an error:', err.decode())
     exit(1)


# azureuser@octopus-worker-ubuntu:/mnt/efs$ sudo unzip Monaco_WinnersWorldR25_270_FullBuild_Gdk35_2.7.0.8_DEV.zip -d Monaco_WinnersWorldR25_270_FullBuild_Gdk35_2.7.0.8_DEV

