#!/bin/bash

#set -e

get_conf_string () {
    php -r "include ('config/conf.php'); echo \$conf['$1']['$2'];"
}

DB=$(get_conf_string "sql" "database")

if [ ! -e "$DB" ]; then
    horde-db-migrate
    chown www-data:www-data ${DB}
fi

exec "$@"
