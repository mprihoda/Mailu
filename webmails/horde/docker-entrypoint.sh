#!/bin/bash

#set -e

# TODO: migrate database
# copy htdocs to volume
if [ ! -e /var/www/html/index.php -o "$HORDE_UPGRADE" = "true" ]; then
    tar cf - --one-file-system -C /usr/src/horde . | tar xf -
fi

# check and enable default config
if [ ! -e config/conf.php ]; then
    cp /usr/src/base-conf.php config/conf.php
    cp /usr/src/imp-backends.php imp/config/backends.php
    horde-db-migrate
fi

if [ ! -e config/registry.local.php ]; then
    cp /usr/src/registry.local.php config/registry.local.php
fi
chown -R www-data.www-data .

exec "$@"
