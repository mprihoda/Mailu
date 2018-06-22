FROM php:5.6-apache

MAINTAINER agsola
ENV HORDE_VERSION 5.2.22

RUN apt-get update && apt-get install -y \
        libfreetype6-dev \
        libicu-dev \
        libjpeg62-turbo-dev \
        libldap2-dev \
        libmcrypt-dev \
        libmysqlclient-dev \
        libpng12-dev \
        libpq-dev \
        libxml2-dev \
        libmagickwand-dev libmagickcore-dev \
        libssh2-1-dev \
        libbz2-dev bzip2 \
        libc-client2007e-dev libkrb5-dev \
        locales \
    && rm -rf /var/lib/apt/lists/*

COPY locale.gen /etc
COPY locale /etc/default

RUN locale-gen

RUN docker-php-ext-configure gd --with-png-dir=/usr --with-freetype-dir=/usr --with-jpeg-dir=/usr \
    && docker-php-ext-configure ldap --with-libdir=lib/x86_64-linux-gnu/ \
    && docker-php-ext-configure imap --with-kerberos --with-imap-ssl \
    && docker-php-ext-configure mbstring \
    && docker-php-ext-configure gettext \
    && docker-php-ext-configure mysql \
    && docker-php-ext-configure mysqli \
    && docker-php-ext-install gd iconv mcrypt imap mysql mysqli bz2 pgsql xmlrpc gettext ldap mbstring intl \
    && pecl install imagick \
    && pecl install memcache \
    && a2enmod rewrite

VOLUME /var/www/html

RUN pear upgrade PEAR \
#    && pear config-set http_proxy http://x.x.x.x:8080 \ <-- If you need a proxy
 && pear upgrade channel://pear.php.net/XML_Serializer-0.20.2 \
 && pear upgrade channel://pear.php.net/Date_Holidays-0.21.8 \
 && pear upgrade channel://pear.php.net/Text_LanguageDetect-0.3.0 \
 && pear upgrade channel://pear.php.net/SOAP-0.13.0 \
 && pear upgrade channel://pear.php.net/Console_Color2-0.1.2 \
 && pear upgrade channel://pecl.php.net/msgpack-0.5.7 \
 && pear upgrade channel://pear.php.net/Numbers_Words-0.18.1 \
 && pear upgrade channel://pear.php.net/Image_Text-0.7.0 \
 && pear install Auth_SASL2-beta \
 && pear upgrade channel://pecl.php.net/ssh2-0.12 \
    && pear channel-discover pear.horde.org \
    && rm -rf /var/www/html/* \
    && pear install horde/horde_role \
    && pear config-set horde_dir /usr/src/horde \
#    && pear run-scripts horde/horde_role \
    && pear install -a -B horde/webmail-$HORDE_VERSION \
    && echo 'extension=memcache.so' > /usr/local/etc/php/conf.d/docker-php-ext-memcache.ini

RUN pear config-set horde_dir /var/www/html

COPY docker-entrypoint.sh /entrypoint.sh
COPY base-conf.php /usr/src
COPY registry.local.php /usr/src
COPY imp-backends.php /usr/src
COPY default-vhost.conf /etc/apache2/sites-available/000-default.conf

EXPOSE 80 443

VOLUME /tmp

ENTRYPOINT ["/entrypoint.sh"]
CMD ["apache2-foreground"]
