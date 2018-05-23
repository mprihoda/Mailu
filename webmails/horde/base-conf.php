<?php
if (!function_exists("safe_env")) {
    function safe_env($key, $fallback)
    {
        if (array_key_exists($key, $_ENV)) {
            return $_ENV[$key];
        }
        return $fallback;
    }
}

if (!function_exists("decodebool")) {
    function decodebool($value)
    {
        return filter_var($value, FILTER_VALIDATE_BOOLEAN);
    }
}

if (!function_exists("decodelist")) {
    function decodelist($value)
    {
        return explode(",", $value);
    }
}
/* CONFIG START. DO NOT CHANGE ANYTHING IN OR AFTER THIS LINE. */
// $Id: 08fc885cd91fbae2d752e274b554c5f1645129c8 $
$conf['vhosts'] = false;
$conf['debug_level'] = E_ALL & ~E_NOTICE;
$conf['max_exec_time'] = 0;
$conf['compress_pages'] = true;
$conf['secret_key'] = $_ENV['SECRET_KEY'];
$conf['umask'] = 077;
$conf['testdisable'] = decodebool(safe_env('HORDE_TEST_DISABLE', 'true'));
$conf['use_ssl'] = 1;
$conf['server']['port'] = 443;
$conf['server']['name'] = $_SERVER['SERVER_NAME'];
$conf['urls']['token_lifetime'] = 30;
$conf['urls']['hmac_lifetime'] = 30;
$conf['urls']['pretty'] = false;
$conf['safe_ips'] = array();
$conf['session']['name'] = 'Horde';
$conf['session']['use_only_cookies'] = true;
$conf['session']['timeout'] = 0;
$conf['session']['cache_limiter'] = 'nocache';
$conf['session']['max_time'] = 72000;
$conf['cookie']['domain'] = $_SERVER['SERVER_NAME'];
$conf['cookie']['path'] = '/';
$conf['sql']['database'] = '/data/prefs.sqlite';
$conf['sql']['charset'] = 'utf-8';
$conf['sql']['logqueries'] = false;
$conf['sql']['phptype'] = 'sqlite';
$conf['nosql']['phptype'] = false;
$conf['ldap']['useldap'] = false;
$conf['auth']['admins'] = decodelist(safe_env('HORDE_ADMINS', 'root@maildev-cmi.e-bs.cz'));
$conf['auth']['checkip'] = true;
$conf['auth']['checkbrowser'] = true;
$conf['auth']['resetpassword'] = false;
$conf['auth']['alternate_login'] = false;
$conf['auth']['redirect_on_logout'] = false;
$conf['auth']['list_users'] = 'list';
$conf['auth']['params']['hostspec'] = 'front';
$conf['auth']['params']['port'] = 993;
$conf['auth']['params']['secure'] = 'ssl';
$conf['auth']['driver'] = 'imap';
$conf['auth']['params']['count_bad_logins'] = false;
$conf['auth']['params']['login_block'] = false;
$conf['auth']['params']['login_block_count'] = 5;
$conf['auth']['params']['login_block_time'] = 5;
$conf['signup']['allow'] = false;
$conf['log']['priority'] = safe_env('HORDE_LOG_LEVEL', 'INFO');
$conf['log']['ident'] = 'HORDE';
$conf['log']['name'] = '/data/horde.log';
$conf['log']['type'] = 'file';
$conf['log']['enabled'] = decodebool(safe_env('HORDE_LOG', 'false'));
$conf['log_accesskeys'] = false;
$conf['prefs']['maxsize'] = 65535;
$conf['prefs']['params']['driverconfig'] = 'horde';
$conf['prefs']['driver'] = 'Sql';
$conf['alarms']['params']['driverconfig'] = 'horde';
$conf['alarms']['params']['ttl'] = 300;
$conf['alarms']['driver'] = 'Sql';
$conf['group']['params']['driverconfig'] = 'horde';
$conf['group']['driver'] = 'Sql';
$conf['perms']['driverconfig'] = 'horde';
$conf['perms']['driver'] = 'Sql';
$conf['share']['no_sharing'] = false;
$conf['share']['auto_create'] = true;
$conf['share']['world'] = true;
$conf['share']['any_group'] = false;
$conf['share']['hidden'] = false;
$conf['share']['cache'] = false;
$conf['share']['driver'] = 'Sqlng';
$conf['cache']['default_lifetime'] = 86400;
$conf['cache']['params']['sub'] = 0;
$conf['cache']['driver'] = 'File';
$conf['cache']['use_memorycache'] = '';
$conf['cachecssparams']['url_version_param'] = true;
$conf['cachecss'] = false;
$conf['cachejsparams']['url_version_param'] = true;
$conf['cachejs'] = false;
$conf['cachethemes'] = false;
$conf['lock']['params']['driverconfig'] = 'horde';
$conf['lock']['driver'] = 'Sql';
$conf['token']['params']['driverconfig'] = 'horde';
$conf['token']['driver'] = 'Sql';
$conf['history']['params']['driverconfig'] = 'horde';
$conf['history']['driver'] = 'Sql';
$conf['davstorage']['params']['driverconfig'] = 'horde';
$conf['davstorage']['driver'] = 'Sql';
$conf['mailer']['params']['host'] = 'smtp';
$conf['mailer']['params']['port'] = 25;
$conf['mailer']['params']['secure'] = 'none';
$conf['mailer']['params']['auth'] = false;
$conf['mailer']['params']['lmtp'] = false;
$conf['mailer']['type'] = 'smtp';
$conf['vfs']['params']['driverconfig'] = 'horde';
$conf['vfs']['type'] = 'Sql';
$conf['sessionhandler']['type'] = 'Builtin';
$conf['sessionhandler']['hashtable'] = false;
$conf['spell']['driver'] = '';
$conf['gnupg']['keyserver'] = array('pool.sks-keyservers.net');
$conf['gnupg']['timeout'] = 10;
$conf['nobase64_img'] = false;
$conf['image']['driver'] = false;
$conf['exif']['driver'] = 'Bundled';
$conf['timezone']['location'] = 'ftp://ftp.iana.org/tz/tzdata-latest.tar.gz';
$conf['problems']['email'] = 'mph@e-bs.cz';
$conf['problems']['maildomain'] = 'e-bs.cz';
$conf['problems']['tickets'] = false;
$conf['problems']['attachments'] = true;
$conf['menu']['links']['help'] = 'all';
$conf['menu']['links']['prefs'] = 'authenticated';
$conf['menu']['links']['problem'] = 'all';
$conf['menu']['links']['login'] = 'all';
$conf['menu']['links']['logout'] = 'authenticated';
$conf['portal']['fixed_blocks'] = array();
$conf['accounts']['driver'] = 'null';
$conf['user']['verify_from_addr'] = false;
$conf['user']['select_view'] = true;
$conf['facebook']['enabled'] = false;
$conf['twitter']['enabled'] = false;
$conf['urlshortener'] = false;
$conf['weather']['provider'] = false;
$conf['imap']['enabled'] = false;
$conf['imsp']['enabled'] = false;
$conf['kolab']['enabled'] = false;
$conf['hashtable']['driver'] = 'none';
$conf['activesync']['enabled'] = false;
/* CONFIG END. DO NOT CHANGE ANYTHING IN OR BEFORE THIS LINE. */
