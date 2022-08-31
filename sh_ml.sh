#!/bin/bash
# chmod ugo+x sh_ml.sh

set -e   # выход при ошибке
set -u   # переменные нужно инициализировать


##############################
# ПЕРЕМЕННЫЕ
##############################
DOCKER_HUB="saphir001"



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
# FUN: ml_run
##############################
function ml_run {
    # run
    # @param1 folder               mlServerText
    # @param2 command              "" "start" "stop" "status"

    cd backend_ml/daemons/$1
    source env/bin/activate
    if [ $# = 1 ]; then
        python3 $1.py
    else
        python3 daemon.py "$2"
    fi
}



##############################
# FUN: ml_docker
##############################
function ml_docker {
    # refresh image/container/hub.docker.com
    # @param1 folder               loaderSiteRSS
    # @param2 image/container name loader-siterss
    # @param3 command              icp-         refresh [i]mage, [c]ontainer, [p]ush to hub.docker.com, [-] del image and container

    local NAME_IMAGE=$DOCKER_HUB/$2
    local NAME_CONTAINER=$2

    set +e
        if [[ $3 =~ "-" ]] || [[ $3 =~ "i" ]] || [[ $3 =~ "c" ]]; then
            print_blue "Remove container ""$NAME_IMAGE"
            docker stop $NAME_CONTAINER
            docker rm $NAME_CONTAINER
        fi;
        if [[ $3 =~ "-" ]] || [[ $3 =~ "i" ]]; then
            print_blue "Remove image ""$NAME_CONTAINER"
            docker rmi $NAME_IMAGE
        fi
    set -e

    cd backend_ml

    if [[ $3 =~ "i" ]]; then
        print_blue "Create image ""$NAME_IMAGE"
        cd daemons/$1
        source env/bin/activate
        pip uninstall pkg-resources==0.0.0
        pip freeze > requirements.txt
        deactivate
        cd ../..
        docker build --no-cache=true --build-arg LNAME=$1 -t $NAME_IMAGE -f daemons/$1/Dockerfile .

    fi; if [[ $3 =~ "p" ]]; then        # slowly operation, need docker login
        print_blue "Push image ""$NAME_IMAGE"
        docker push $NAME_IMAGE

    fi; if [[ $3 =~ "c" ]]; then
        print_blue "Create container ""$NAME_IMAGE"
        # run as daemon
        # docker run -d -v "${PWD}""/log:/app/backend_ml/log" -e LNAME=$1 -p 5002:5000 --name $NAME_CONTAINER $NAME_IMAGE

        # run and wait in console
        # run as user: http://wiki.ros.org/docker/Tutorials/GUI#login_as_yourself
        docker run \
            -it \
            -v "${PWD}""/log:/app/backend_ml/log" \
            -v "/devstorage/lib_ml:/devstorage/lib_ml" \
            -e LNAME=$1 \
            -p 5000:5000 \
            --rm \
            --name $NAME_CONTAINER \
            $NAME_IMAGE
            # -v "/tmp/.X11-unix:/tmp/.X11-unix:rw" \
        # docker exec -it $NAME_CONTAINER /bin/bash
    fi

    print_blue "Info"
    docker images
    docker ps -a
}



##############################
# ВЫПОЛНИТЬ ФУНКЦИЮ $1
##############################
FUN="$1"
shift
$FUN "$@"


