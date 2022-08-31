#!/bin/bash
# chmod ugo+x sh
# https://habr.com/ru/company/ruvds/blog/325522/

set -e   # выход при ошибке
set -u   # переменные нужно инициализировать


##############################
# ПЕРЕМЕННЫЕ
##############################
PATH_SH="${PWD}"
PATH_SH_ML="${PATH_SH}/sh_ml.sh"
PATH_SH_LOADER="${PATH_SH}/sh_loader.sh"
DIVIDER='************************************************************************'



##############################
# COLOR
##############################
ESC=$(printf '\033') RESET="${ESC}[0m"   BLACK="${ESC}[30m" RED="${ESC}[31m"
GREEN="${ESC}[32m"   YELLOW="${ESC}[33m" BLUE="${ESC}[34m"  MAGENTA="${ESC}[35m"
CYAN="${ESC}[36m"    WHITE="${ESC}[37m"  GRAY="${ESC}[90m"  DEFAULT="${ESC}[39m"
print_green()   { printf "${GREEN}%s${RESET}\n" "$1"; }
print_blue()    { printf "${BLUE}%s${RESET}\n" "$1"; }
print_red()     { printf "${RED}%s${RESET}\n" "$1"; }
print_yellow()  { printf "${YELLOW}%s${RESET}\n" "$1"; }
print_magenta() { printf "${MAGENTA}%s${RESET}\n" "$1"; }
print_cyan()    { printf "${CYAN}%s${RESET}\n" "$1"; }
print_gray()    { printf "${GRAY}%s${RESET}\n" "$1"; }



##############################
# FUN: FRONTEND
##############################
function front_dev {
    #rm -r -f backend/static/src
    #cp backend/templates/index_dev.html backend/templates/index.html
    cd frontend
    npm run serve
}

function front_prod {
    #rm -r -f backend/static/src
    cd frontend
    npm run build
    #cp ../backend/static/src/vue/dist/index.html ../backend/templates/index.html
}



##############################
# FUN: BACKEND
##############################
function back_main_dev {
    cd backend
    source env/bin/activate
    python3 manage.py runserver 0.0.0.0:8000
}



##############################
# RUN FUN FROM OTHER SH
##############################
function run_external {
    # @param1 - name module
    # @param2 - name function
    # @param3 ... - param
    NAME_SH="$1" ; shift
    NAME_FUN="$1" ; shift
    . ${NAME_SH} "${NAME_FUN} $@"
}




##############################
# FUN: CONSOLE
##############################
function console {
    echo "From quit console type [exit]"
    ssh dev@200.200.200.$1
}





##############################
# FUN: ITEM
##############################
function item_show {
    local val1="["`print_green "$1"`"]"
    val1=`printf "%-21s" "$val1"`
    local val2=`printf "%-29s" "$2"`
    printf "${val1}${val2}$3"
}

function item_exec {
	cd ${PATH_SH}
    local b=0
    for i in "${!KEYS[@]}"; do
        if [[ "${KEYS[$i]}" = "$1" ]]; then
            print_green "${DIVIDER}"
            echo       "${MENU[$i]}"
            print_green "${DIVIDER}"
            ${EXEC[$i]}
            b=1
            break
        fi
    done
    if [[ "${b}" = 0 ]]; then
        print_red "${DIVIDER}"
        print_red "[$1] is not an option"
        print_red "${DIVIDER}"
    fi
}



##############################
# MENU
##############################
KEYS_001="f"
EXEC_001="front_dev"
MENU_001=`item_show "${KEYS_001}" "frontend main" "run development"`

KEYS_002="fp"
EXEC_002="front_prod"
MENU_002=`item_show "${KEYS_002}" "frontend main" "run production"`

##############################

KEYS_100="b"
EXEC_100="back_main_dev"
MENU_100=`item_show "${KEYS_100}" "backend main" "run development"`

##############################
KEYS_110="ml.dev"
EXEC_110="run_external ${PATH_SH_ML} ml_run mlServerText"
MENU_110=`item_show "${KEYS_110}" "ml serverText" "run development"`

KEYS_111="ml.dm.+"
EXEC_111="run_external ${PATH_SH_ML} ml_run mlServerText start"
MENU_111=`item_show "${KEYS_111}" "ml serverText" "daemon start"`

KEYS_112="ml.dm.-"
EXEC_112="run_external ${PATH_SH_ML} ml_run mlServerText stop"
MENU_112=`item_show "${KEYS_112}" "ml serverText" "daemon stop"`

KEYS_113="ml.dm.?"
EXEC_113="run_external ${PATH_SH_ML} ml_run mlServerText status"
MENU_113=`item_show "${KEYS_113}" "ml serverText" "daemon status"`

KEYS_115="ml.dc.i"
EXEC_115="run_external ${PATH_SH_ML} ml_docker mlServerText ml-server-text i"
MENU_115=`item_show "${KEYS_115}" "ml serverText" "docker refresh image"`

KEYS_116="ml.dc.c"
EXEC_116="run_external ${PATH_SH_ML} ml_docker mlServerText ml-server-text c"
MENU_116=`item_show "${KEYS_116}" "ml serverText" "docker refresh container"`

KEYS_117="ml.dc.p"
EXEC_117="run_external ${PATH_SH_ML} ml_docker mlServerText ml-server-text p"
MENU_117=`item_show "${KEYS_117}" "ml serverText" "docker push image"`

KEYS_118="ml.dc.-"
EXEC_118="run_external ${PATH_SH_ML} ml_docker mlServerText ml-server-text -"
MENU_118=`item_show "${KEYS_118}" "ml serverText" "docker remove image & container"`

##############################

KEYS_120="tg.dev"
EXEC_120="run_external ${PATH_SH_LOADER} loader_run loaderTG"
MENU_120=`item_show "${KEYS_120}" "loader telegram" "run development"`

KEYS_121="tg.dm.+"
EXEC_121="run_external ${PATH_SH_LOADER} loader_run loaderTG start"
MENU_121=`item_show "${KEYS_121}" "loader telegram" "daemon start"`

KEYS_122="tg.dm.-"
EXEC_122="run_external ${PATH_SH_LOADER} loader_run loaderTG stop"
MENU_122=`item_show "${KEYS_122}" "loader telegram" "daemon stop"`

KEYS_123="tg.dm.?"
EXEC_123="run_external ${PATH_SH_LOADER} loader_run loaderTG status"
MENU_123=`item_show "${KEYS_123}" "loader telegram" "daemon status"`

KEYS_125="tg.dc.i"
EXEC_125="run_external ${PATH_SH_LOADER} loader_docker loaderTG loader-tg i"
MENU_125=`item_show "${KEYS_125}" "loader telegram" "docker refresh image"`

KEYS_126="tg.dc.c"
EXEC_126="run_external ${PATH_SH_LOADER} loader_docker loaderTG loader-tg c"
MENU_126=`item_show "${KEYS_126}" "loader telegram" "docker refresh container"`

KEYS_127="tg.dc.p"
EXEC_127="run_external ${PATH_SH_LOADER} loader_docker loaderTG loader-tg p"
MENU_127=`item_show "${KEYS_127}" "loader telegram" "docker push image"`

KEYS_128="tg.dc.-"
EXEC_128="run_external ${PATH_SH_LOADER} loader_docker loaderTG loader-tg -"
MENU_128=`item_show "${KEYS_128}" "loader telegram" "docker remove image & container"`

##############################

KEYS_130="sr.dev"
EXEC_130="run_external ${PATH_SH_LOADER} loader_run loaderSiteRSS"
MENU_130=`item_show "${KEYS_130}" "loader siteRSS" "run development"`

KEYS_131="sr.dm.+"
EXEC_131="run_external ${PATH_SH_LOADER} loader_run loaderSiteRSS start"
MENU_131=`item_show "${KEYS_131}" "loader siteRSS" "daemon start"`

KEYS_132="sr.dm.-"
EXEC_132="run_external ${PATH_SH_LOADER} loader_run loaderSiteRSS stop"
MENU_132=`item_show "${KEYS_132}" "loader siteRSS" "daemon stop"`

KEYS_133="sr.dm.?"
EXEC_133="run_external ${PATH_SH_LOADER} loader_run loaderSiteRSS status"
MENU_133=`item_show "${KEYS_133}" "loader siteRSS" "daemon status"`

KEYS_135="sr.dc.i"
EXEC_135="run_external ${PATH_SH_LOADER} loader_docker loaderSiteRSS loader-siterss i"
MENU_135=`item_show "${KEYS_135}" "loader siteRSS" "docker refresh image"`

KEYS_136="sr.dc.c"
EXEC_136="run_external ${PATH_SH_LOADER} loader_docker loaderSiteRSS loader-siterss c"
MENU_136=`item_show "${KEYS_136}" "loader siteRSS" "docker refresh container"`

KEYS_137="sr.dc.p"
EXEC_137="run_external ${PATH_SH_LOADER} loader_docker loaderSiteRSS loader-siterss p"
MENU_137=`item_show "${KEYS_137}" "loader siteRSS" "docker push image"`

KEYS_138="sr.dc.-"
EXEC_138="run_external ${PATH_SH_LOADER} loader_docker loaderSiteRSS loader-siterss -"
MENU_138=`item_show "${KEYS_138}" "loader siteRSS" "docker remove image & container"`

##############################

KEYS_231="231"
EXEC_231="console 231"
MENU_231=`item_show "${KEYS_231}" "console" "231 (map osm)"`

KEYS_232="232"
EXEC_232="console 232"
MENU_232=`item_show "${KEYS_232}" "console" "232 (map yandex)"`

KEYS_233="233"
EXEC_233="console 233"
MENU_233=`item_show "${KEYS_233}" "console" "233 (mySQL)"`

KEYS_234="234"
EXEC_234="console 234"
MENU_234=`item_show "${KEYS_234}" "console" "234 (ftp)"`

KEYS_235="235"
EXEC_235="console 235"
MENU_235=`item_show "${KEYS_235}" "console" "235 (manticore)"`

KEYS_236="236"
EXEC_236="console 236"
MENU_236=`item_show "${KEYS_236}" "console" "236 (site osm)"`

##############################

KEYS=( \
    "${KEYS_001}" "${KEYS_002}" \
    "${KEYS_100}" \
    "" \
    "${KEYS_110}" "${KEYS_111}" "${KEYS_112}" "${KEYS_113}" "${KEYS_115}" "${KEYS_116}" "${KEYS_117}" "${KEYS_118}" \
    "" \
    "${KEYS_120}" "${KEYS_121}" "${KEYS_122}" "${KEYS_123}" "${KEYS_125}" "${KEYS_126}" "${KEYS_127}" "${KEYS_128}" \
    "${KEYS_130}" "${KEYS_131}" "${KEYS_132}" "${KEYS_133}" "${KEYS_135}" "${KEYS_136}" "${KEYS_137}" "${KEYS_138}" \
    "" \
    "${KEYS_231}" "${KEYS_232}" "${KEYS_233}" "${KEYS_234}" "${KEYS_235}" "${KEYS_236}" \
    )
EXEC=( \
    "${EXEC_001}" "${EXEC_002}" \
    "${EXEC_100}" \
    "" \
    "${EXEC_110}" "${EXEC_111}" "${EXEC_112}" "${EXEC_113}" "${EXEC_115}" "${EXEC_116}" "${EXEC_117}" "${EXEC_118}" \
    "" \
    "${EXEC_120}" "${EXEC_121}" "${EXEC_122}" "${EXEC_123}" "${EXEC_125}" "${EXEC_126}" "${EXEC_127}" "${EXEC_128}" \
    "${EXEC_130}" "${EXEC_131}" "${EXEC_132}" "${EXEC_133}" "${EXEC_135}" "${EXEC_136}" "${EXEC_137}" "${EXEC_138}" \
    "" \
    "${EXEC_231}" "${EXEC_232}" "${EXEC_233}" "${EXEC_234}" "${EXEC_235}" "${EXEC_236}" \
    )
MENU=( \
    "${MENU_001}" "${MENU_002}" \
    "${MENU_100}" \
    "${DIVIDER}" \
    "${MENU_110}" "${MENU_111}" "${MENU_112}" "${MENU_113}" "${MENU_115}" "${MENU_116}" "${MENU_117}" "${MENU_118}" \
    "${DIVIDER}" \
    "${MENU_120}" "${MENU_121}" "${MENU_122}" "${MENU_123}" "${MENU_125}" "${MENU_126}" "${MENU_127}" "${MENU_128}" \
    "${MENU_130}" "${MENU_131}" "${MENU_132}" "${MENU_133}" "${MENU_135}" "${MENU_136}" "${MENU_137}" "${MENU_138}" \
    "${DIVIDER}" \
    "${MENU_231}" "${MENU_232}" "${MENU_233}" "${MENU_234}" "${MENU_235}" "${MENU_236}" \
    )





##############################
# ключи/параметры НЕ заданы
##############################
if [ $# -eq 0 ]
then
    print_blue "${DIVIDER}"
    print_blue 'ОСНОВНЫЕ КОМАНДЫ'
    print_blue "${DIVIDER}"
    print_blue 'KEY         SERVICE                      OPERATION'
    print_blue "${DIVIDER}"
    for i in "${!MENU[@]}"; do
        if [ "${MENU[$i]}" != "${DIVIDER}" ]
        then
            echo "${MENU[$i]}"
        else
            print_gray "${DIVIDER}"
        fi
    done
    echo -ne "Choose an option:  "
    read -r KEYS_SEL
    KEYS_SEL="${KEYS_SEL}" | xargs  # обрезать пробелы
else
    KEYS_SEL="$@"
fi

##############################
# анализ выбора
##############################
for KEY in $KEYS_SEL; do
    item_exec "$KEY"
done
