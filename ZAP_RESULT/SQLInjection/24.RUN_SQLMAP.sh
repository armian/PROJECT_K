# 아래 2 라인은 수정되어야 함
CACHE_FILE="~/.sqlmap/output/YOUR_DOMAIN"
INPUT_SQL_FILE="./22.sqlmap_url.txt"

# 처음만 체크하고, 이후 exit 부분을 주석 처리
if [ ! -f ${CACHE_FILE} ]
then
    echo "CACHE_FILE (${CACHE_FILE}) does not exist"
    echo "modify 'CACHE_FILE' environment variable !!"
    echo "delete './start_num.txt' if your first time !!"
    exit
fi

if [ ! -f ${INPUT_SQL_FILE} ]
then
    echo "INPUT_SQL_FILE (${INPUT_SQL_FILE}) does not exist"
    exit
fi

NUM_FILE="./start_num.txt"
TMP_FILE="${NUM_FILE}.tmp"

# ${NUM_FILE}이 없으면 생성 (최초 값은 2)
if [ ! -f ${NUM_FILE} ]
then
    echo "2" > ${NUM_FILE}
fi

# 전체 레코드 수
total_num=`wc -l ${INPUT_SQL_FILE} | awk '{print $1}'`
echo "total_num = ${total_num}"

# 현재 처리할 순서
cur_num=`cat ${NUM_FILE}`
echo "cur_num = ${cur_num}"

# 전체 레코드 수와 현재 처리할 순서를 비교
if [ ${cur_num} -gt ${total_num} ]
then
    echo "No more recored... (${total_num})"
    exit
fi

# 명령어 실행
command_1="rm -rf ${CACHE_FILE}"
command_2=`head -${cur_num} ${INPUT_SQL_FILE} | tail -1`

echo "command_1=${command_1}"
eval "${command_1}"
echo
echo "command_2=${command_2}"
eval "${command_2}"

echo
echo
echo "processsed (${cur_num}) ${command_2}"
echo
echo


# 다음 처리할 값을 구하여 저장
awk '{printf("%d",$0+1)}' ${NUM_FILE} > ${TMP_FILE}
mv ${TMP_FILE} ${NUM_FILE}
