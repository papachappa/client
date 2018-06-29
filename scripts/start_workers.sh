#!/usr/bin/env bash

# exit codes:
# 1 -- conflict between remote and local setting(obsolete)
# 2 -- wrong arguments passed
# 3 -- getopt programming error


VAR_CELERY_DIR=""
CLIENT_SETTINGS_DIR=""

# if settings file setted other options not required
SETTINGS_FILE=''
ALIAS=''
HOSTNAME='' # DEFAULT: `hostname`
HOSTADDR=''
USER=''
PASSWORD=''
VHOST=''
NOTSET='t' # NOTSET: t|f

########################## <PARSING PASSED ARGUMENTS> ###################
LONG=hostname:,user:,password:,hostip:,alias:,vhost:,help,"show-available,show-alias:,show-current,remove-alias:,remove-all-aliases,settings-file:"
PARSED=$(getopt --options -- --longoptions $LONG --name "$0" -- "$@")
if [[ $? -ne 0 ]]; then
    #  then getopt has complained about wrong arguments to stdout
    exit 2
fi
eval set -- "$PARSED"

while true; do
    case "$1" in
        --help)
            echo "start_workers [ALIAS] [OPTION]"
            echo "starting celery workers based on passed/saved configs"
            echo
            echo "OPTIONS:"
            echo -e "--show-available\t\t"          "show available aliases"
            echo -e "--show-alias[=]<alias>\t\t"    "show settings presented in <alias>"
            echo -e "--show-current\t\t\t"          "show current alias in use"
            echo -e "--remove-alias[=]<alias>\t"    "remove alias with <alias> name"
            echo -e "--remove-all-aliases\t\t"      "will remove all aliases"
            echo -e "--alias[=]<alias>\t\t"         "same as ALIAS"
            echo -e "--user[=]<user>\t\t\t"         "rabbitmq host user"
            echo -e "--password[=]<password>\t\t"   "rabbitmq host password"
            echo -e "--vhost[=]<vhost>\t\t"         "rabbitmq host vhost"
            echo -e "--hostip[=]<hostip>\t\t"       "rabbitmq host address"
            echo -e "--hostname[=]<hostname>\t\t"   "alias for connection name"
            echo -e "--help\t\t\t\t"                "shows current help"
            echo
            echo "USAGE:"
            echo "ALIAS is name for file with saved settings, stored in settings dir. "
            echo -nE "executing \`start_workers ALIAS\` without any options will follow to "
            echo "trying to load saved settings w/ ALIAS name."
            echo "If file exists, to user will be sugested rewrite or create new file."
            echo "\`configure.ini\` restricted to use as ALIAS."
            exit 0
            ;;
        --settings-file)
            SETTINGS_FILE="$2"
            if [[ -z "$SETTINGS_FILE" ]]
            then
                echo 'settings-file cannot be empty'
                exit 3
            fi
            shift 2
            break
            ;;
        --show-current)
            _c=$(cat "$CLIENT_SETTINGS_DIR/configure.ini" 2>/dev/null) || echo "no aliases created yet"
            if [[ "$_c" ]]
            then
                echo -e "$_c\n"
                cat "$CLIENT_SETTINGS_DIR/$_c"
            fi
            exit 0
            ;;
        --show-available)
            find "$CLIENT_SETTINGS_DIR" -maxdepth 1 -type f -not -name "*.py" -not -name 'configure.ini' -exec basename {} \;
            exit 0
            ;;
        --show-alias)
            cat "$CLIENT_SETTINGS_DIR/$2" 2>/dev/null || echo "'$2' does not exist"
            exit 0
            ;;
        --remove-alias)
            rm --force "$CLIENT_SETTINGS_DIR/$2"
            exit 0
            ;;
        --remove-all-aliases)
            find "$CLIENT_SETTINGS_DIR" -maxdepth 1 -type f -not -name "*.py" -not -name 'configure.ini' -delete
            exit 0
            ;;            
        --hostname)
            HOSTNAME="$2"
            NOTSET='f'
            shift 2
            ;;
        --user)
            USER="$2"
            NOTSET='f'
            shift 2
            ;;
        --password)
            PASSWORD="$2"
            NOTSET='f'
            shift 2
            ;;
        --hostip)
            HOSTADDR="$2"
            NOTSET='f'
            shift 2
            ;;
        --vhost)
            VHOST="$2"
            NOTSET='f'
            shift 2
            ;;
        --alias)
            ALIAS="$2"
            shift 2
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "Programming error"
            exit 3
            ;;
    esac
done
######################### </PARSING PASSED ARGUMENTS> ###################


######################### <SETTINGS FILE STUFF> #########################
function create_new {
    fname="$1"
    cat /dev/null > $fname
    [[ $USER ]]             && echo "user=$USER"         >> $fname
    [[ $PASSWORD ]]         && echo "password=$PASSWORD" >> $fname
    [[ $VHOST ]]            && echo "vhost=$VHOST"       >> $fname
    [[ $HOSTADDR ]]         && echo "host=$HOSTADDR"     >> $fname
    [[ $HOSTNAME ]]         && echo "hostname=$HOSTNAME" >> $fname
}

function rewrite_alias {
    while true; do
        read -p "'$ALIAS' founded, rewrite it? If 'n' then existing file will be used. (y/n): " yn
        case $yn in
            [Yy]* ) rewrite='y'; break;;
            [Nn]* ) rewrite='n'; break;;
            * ) echo "Please answer yes or no.";;
        esac
    done

    if [[ "$rewrite" == 'y' ]]
    then
        create_new "$CLIENT_SETTINGS_DIR/$ALIAS"
    fi
}

function process_settings {
    [[ -z "$ALIAS" ]] && ALIAS="$1"

    if [[ "$ALIAS" == 'configure.ini' ]]
    then
        another_name=$(date +%y%m%d%H%M)
        echo "'$ALIAS' reserved. '$another_name' will be used"
        ALIAS=$another_name
    fi

    # if alias is empty and settings presented
    if [[ -z "$ALIAS" && "$NOTSET" == 'f' ]]
    then
        another_name=$(date +%y%m%d%H%M)
        echo "Alias is empty, '$another_name' will be used"
        ALIAS=$another_name
    fi

    # if file with settings exists and settings presented
    if [[ -f "$CLIENT_SETTINGS_DIR/$ALIAS" && "$NOTSET" == 'f' ]]
    then
        rewrite_alias
    fi

    if [[ "$ALIAS" && ! -f "$CLIENT_SETTINGS_DIR/$ALIAS" ]]
    then
        create_new "$CLIENT_SETTINGS_DIR/$ALIAS"
    fi

    if [[ "$ALIAS" ]]
    then
        echo "$ALIAS" > "$CLIENT_SETTINGS_DIR/configure.ini"
    # if alias not presented and nothing is setted up
    elif [[ "$NOTSET" == 't' ]]
    then
        echo -e "alias is not presented and nothing is setted up\n"
        fname=$([[ -f "$CLIENT_SETTINGS_DIR/configure.ini" ]] && cat "$CLIENT_SETTINGS_DIR/configure.ini")
        if [[ "$fname" && -f "$CLIENT_SETTINGS_DIR/$fname" ]]
        then
            echo "'$fname' file will be used"
            echo "with next settings:"
            cat "$CLIENT_SETTINGS_DIR/$fname"
            HOSTNAME=$(cat "$CLIENT_SETTINGS_DIR/$fname" | grep 'hostname' | cut -d= -f2)
        else
            echo "development local settings will be used"
        fi
    fi

    echo

    if [[ -f "$CLIENT_SETTINGS_DIR/$ALIAS" && -z "$HOSTNAME" ]]
    then
        HOSTNAME=$(cat "$CLIENT_SETTINGS_DIR/$ALIAS" | grep 'hostname' | cut -d= -f2)
    fi
    if [[ -z "$HOSTNAME" ]]; then HOSTNAME="$(hostname)"; fi
}

if [[ -z "$SETTINGS_FILE" ]]
then
    process_settings
else
    cp "$SETTINGS_FILE" "$CLIENT_SETTINGS_DIR/"
    echo $(basename "$SETTINGS_FILE") > "$CLIENT_SETTINGS_DIR/configure.ini"
    HOSTNAME=$(cat "$SETTINGS_FILE" | grep 'hostname' | cut -d= -f2)
    if [[ -z "$HOSTNAME" ]]; then HOSTNAME="$(hostname)"; fi
fi
######################### </SETTINGS FILE STUFF> ########################


######################### <START WORKERS> ###############################
# just to be sure
if [ "$( ls -A $VAR_CELERY_DIR/pid/ | grep pid)" ]
then
    stop_workers
fi

# w8 until everything stops
sleep .5

celery -A client multi start tests \
        --hostname="$HOSTNAME" \
        --pidfile="$VAR_CELERY_DIR/pid/%n.pid" \
        --logfile="$VAR_CELERY_DIR/logs/%n_worker.log" \
        -l info \
        -Q:tests "tests@$HOSTNAME"
######################### </START WORKERS> ##############################
