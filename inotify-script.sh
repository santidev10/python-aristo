# this script monitors the directory where tech-admin uploads the xml file. Then it
# executes resume.py that resumes the manual step on Octopus workflow

inotifywait -r -m /home/azureuser/flask-app/static/files |
    while read a b file; do
     [[ $b == *CREATE* ]]  && python3 /home/azureuser/utils/resume.py
    done
