#!/bin/bash

LOCAL_REPO='/Users/chensle/emse/SE6356.MS1-SoftwareMaintenanceEvolutionAndRe-Engineering-F18/Projects/local_repo/peep-pdfbox'
LOG_DIR='/Users/chensle/PycharmProjects/gminer/files'
COMMIT_LOGFILE_NAME='pdf_gitall.log'
DIFF_LOGFILE_NAME='pdf_diffall.log'
COMMIT_LOGFILE_PATH=${LOG_DIR}/${COMMIT_LOGFILE_NAME}
DIFF_LOGFILE_PATH=${LOG_DIR}/${DIFF_LOGFILE_NAME}
BRANCH_ARRAY=(1.1.x 1.2 1.2.x 1.3 1.4 1.5 1.6 1.7 1.8 2.0 before-apache-packages before-maven-layout no-awt trunk xmpbox-refactoring)

 cd ${LOCAL_REPO}
 for branch in "${BRANCH_ARRAY[@]}"
    do
       echo $branch
       git checkout -f ${branch}
       git log  --since="03/01/2008" --until=”11/01/2017” >> ${COMMIT_LOGFILE_PATH} 
       git rev-list --all --until=”11/01/2017” |git diff-tree -r -name-only --stdin | grep : >> ${DIFF_LOGFILE_PATH}
    done
