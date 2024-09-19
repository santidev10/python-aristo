from subprocess import PIPE, Popen
import os, re, subprocess

os.chdir("/mnt/efs")
with Popen(["ls"], stdout=PIPE, bufsize=1, universal_newlines=True) as p:
    for line in p.stdout:
        if re.search("zip", line):
            directory = os.path.splitext(line)[0]
print(directory)
os.chdir(directory)
path = os.getcwd()
retail_dirs = []
file_email = []
with Popen(["ls"], stdout=PIPE, bufsize=1, universal_newlines=True) as p:
    for dir in p.stdout:
        if re.search("^RETAIL*", dir):
            retail_dirs.append(dir.rstrip())
    if retail_dirs:
        for dir in retail_dirs:
            os.chdir(path+"/"+dir)
            lis = os.listdir()
            for file in lis:
                if "manifest" in file:
                    file_email.append(os.path.abspath(file))
        os.chdir("../Platform/packages")
        files_lis = os.listdir()
        for file in files_lis:
            if "manifest" in file and "Runtime" not in file and "Platform" not in file:
                file_email.append(os.path.abspath(file))
            if "info" in file:
                file_email.append(os.path.abspath(file))
    else:
        os.chdir(path+"/Platform/packages")
        files_lis = os.listdir()
        for file in files_lis:
            if re.search("manifest$", file):
                file_email.append(os.path.abspath(file))
            elif re.search("info$", file):
                file_email.append(os.path.abspath(file))
os.mkdir("/mnt/efs/files-email")
os.chdir("/mnt/efs/files-email")

outf = open('list.txt','w')
for fileToZip in file_email:
    outf.write(fileToZip+'\n')
outf.close()

cmd = '7z a -tzip package.zip -i@list.txt'
out = subprocess.check_output(cmd , shell = True)
