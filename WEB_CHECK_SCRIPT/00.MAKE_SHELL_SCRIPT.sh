#!/bin/bash

ROOT_DIR="/home/armian/webhack_storage"
HTTP_COMMAND="01.RUN_HTTP.sh"
TRACE_COMMAND="02.RUN_TRACE.sh"
NMAP_COMMAND="03.RUN_NMAP.sh"
NMAP_DETAIL_COMMAND="03.RUN_NMAP_DETAIL.sh"
NIKTO_COMMAND="04.RUN_NIKTO_PORT.sh"
VULPATH_COMMAND="05.RUN_VULPATH.sh"

NMAP_TEMPLATE="${ROOT_DIR}/COMMAND_TEMPLATE/${NMAP_COMMAND}-template"
NMAP_DETAIL_TEMPLATE="${ROOT_DIR}/COMMAND_TEMPLATE/${NMAP_DETAIL_COMMAND}-template"
NIKTO_TEMPLATE="${ROOT_DIR}/COMMAND_TEMPLATE/${NIKTO_COMMAND}-template"
VULPATH_TEMPLATE="${ROOT_DIR}/COMMAND_TEMPLATE/${VULPATH_COMMAND}-template"
HTTP_TEMPLATE="${ROOT_DIR}/COMMAND_TEMPLATE/${HTTP_COMMAND}-template"
TRACE_TEMPLATE="${ROOT_DIR}/COMMAND_TEMPLATE/${TRACE_COMMAND}-template"

VULPATH_FILE="${ROOT_DIR}/COMMAND/vulpath.txt"

site_template="SITE_NAME"
site_name_full=`pwd`
site_name=`echo ${site_name_full} | awk -F"/" '{print $NF}'`
echo ${site_name}

REPORT_FILE=00-$site_name-$(date +"%Y").txt
REPORT_FILE_BAK=00-$site_name-$(date +"%Y%m%d_%H%M%S").txt.bak
echo ${REPORT_FILE}
echo ${REPORT_FILE_BAK}

if [ -f ${REPORT_FILE} ]
then
    echo "backup ${REPORT_FILE} -> ${REPORT_FILE_BAK}"
    mv ${REPORT_FILE} ${REPORT_FILE_BAK}
fi

nslookup ${site_name} > ${REPORT_FILE}
#nslookup ${site_name} | grep Name | tail -1 > ${REPORT_FILE}
#nslookup ${site_name} | grep Address | tail -1 >> ${REPORT_FILE}

# NMAP
echo ${NMAP_COMMAND}
sed "s;${site_template};${site_name};g" ${NMAP_TEMPLATE} > ${NMAP_COMMAND}
chmod 755 ${NMAP_COMMAND}

# NMAP_DETAIL
echo ${NMAP_DETAIL_COMMAND}
sed "s;${site_template};${site_name};g" ${NMAP_DETAIL_TEMPLATE} > ${NMAP_DETAIL_COMMAND}
chmod 755 ${NMAP_DETAIL_COMMAND}

# PORT ARRAY for NIKTO
declare -a port
port=('80' '443')

for ((i=0; i<${#port[@]}; i++)) do
    nikto_command=`echo ${NIKTO_COMMAND} | sed "s;PORT;${port[i]};g"`
    echo ${nikto_command}
    cat ${NIKTO_TEMPLATE} | sed "s;${site_template};${site_name};g" | sed "s;PORT;${port[i]};g" > ${nikto_command}
chmod 755 ${nikto_command}
done

# VULPATH
echo ${VULPATH_COMMAND}
cat ${VULPATH_TEMPLATE} | sed "s;${site_template};${site_name};g" | sed "s;VULPATH;${VULPATH_FILE};g"  > ${VULPATH_COMMAND}
chmod 755 ${VULPATH_COMMAND}

# HTTP
echo ${HTTP_COMMAND}
cat ${HTTP_TEMPLATE} | sed "s;${site_template};${site_name};g" > ${HTTP_COMMAND}
chmod 755 ${HTTP_COMMAND}


# TRACE
echo ${TRACE_COMMAND}
cat ${TRACE_TEMPLATE} | sed "s;${site_template};${site_name};g" > ${TRACE_COMMAND}
chmod 755 ${TRACE_COMMAND}
