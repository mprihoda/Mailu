#!/bin/bash

#set -e

get_conf_string () {
    php -r "include ('config/conf.php'); echo \$conf['$1']['$2'];"
}

# TODO: migrate database
# copy htdocs to volume
if [ ! -e /var/www/html/index.php -o "$HORDE_UPGRADE" = "true" ]; then
    tar cf - --one-file-system -C /usr/src/horde . | tar xf -
fi

# check and enable default config
if [ ! -e config/conf.php ]; then
    cp /usr/src/base-conf.php config/conf.php
    cp /usr/src/imp-backends.php imp/config/backends.php
    cp /usr/src/nls-config.php config/nls.local.php
    sed -i "/auth.*admins/c \$conf['auth']['admins'] = array('root@${DOMAIN:-maildev-cmi.e-bs.cz}');" config/conf.php
    horde-db-migrate
    DB=$(get_conf_string "sql" "database")
    if [ -e "${DB}" ]; then
        chown www-data:www-data ${DB}
    fi
fi

sed -i "/testdisable/c \$conf['testdisable'] = ${HORDE_TEST_DISABLE:-true};" config/conf.php
sed -i "/log.*enabled/c \$conf['log']['enabled'] = ${HORDE_LOG:-false};" config/conf.php
sed -i "/log.*priority/c \$conf['log']['priority'] = ${HORDE_LOG_LEVEL:-WARN};" config/conf.php

if [ ! -e config/registry.local.php ]; then
    cp /usr/src/registry.local.php config/registry.local.php
fi
chown -R www-data.www-data .

exec "$@"
