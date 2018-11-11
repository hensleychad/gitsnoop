#!/bin/bash

LOCAL_REPO='/Users/chensle/emse/SE6356.MS1-SoftwareMaintenanceEvolutionAndRe-Engineering-F18/Projects/local_repo/peep-commons-math/'
LOG_DIR='/Users/chensle/PycharmProjects/gminer/files'
COMMIT_LOGFILE_NAME='math_gitall.log'
DIFF_LOGFILE_NAME='math_diffall.log'
COMMIT_LOGFILE_PATH=${LOG_DIR}/${COMMIT_LOGFILE_NAME}
DIFF_LOGFILE_PATH=${LOG_DIR}/${DIFF_LOGFILE_NAME}
BRANCH_ARRAY=(3.6-release 3.6.1-release EXPERIMENTAL MANTISSA MATH-1153 MATH_1_1 MATH_1_1_RC1_tmp MATH_1_3 MATH_2_0_tmp MATH_2_X MATH_3_X complex-and-primitive-arrays develop feature-MATH-1290 feature-MATH-1333 feature-MATH-1370 feature-MATH-1372 feature-MATH-1416field-ode fix-math-1342 h10-builds master master-old task-MATH-1366)

 cd ${LOCAL_REPO}
 for branch in "${BRANCH_ARRAY[@]}"
    do
       echo $branch
       git checkout -f ${branch}
       git log  --since="03/01/2001" --until=”11/01/2017” >> ${COMMIT_LOGFILE_PATH} 
       git rev-list --all --until=”11/01/2017” |git diff-tree -r -name-only --stdin | grep : >> ${DIFF_LOGFILE_PATH}
    done
