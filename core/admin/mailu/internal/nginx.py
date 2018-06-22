import os

from mailu import app, db, models

import re
import socket
import urllib

from drupal_auth import checkpassword

SUPPORTED_AUTH_METHODS = ["none", "plain"]

STATUSES = {
    "authentication": ("Authentication credentials invalid", {
        "imap": "AUTHENTICATIONFAILED",
        "smtp": "535 5.7.8",
        "pop3": "-ERR Authentication failed"
    }),
}

drupal_conf = checkpassword.load_config(os.environ['DRUPAL_CONF'])

cf = checkpassword.ConfiguredConnectionFactory(drupal_conf)


def check_drupal_password(user, password):
    hashed_password = checkpassword.query_password(user, cf)
    # If there is no such user, fall back to local db...
    # TODO: ensure that users removed from DO will loose access
    if hashed_password is None:
        return None
    return checkpassword.check_user_password(password, hashed_password)


def sync_drupal_user(user_name, domain_name, password):
    user = models.User.query.get(user_name + '@' + domain_name)
    if user is None:
        domain = models.Domain.query.get(domain_name)
        if domain is None:
            domain = models.Domain(name=domain_name)
            db.session.add(domain)
        user = models.User(localpart=user_name, domain=domain, global_admin=False)
        db.session.add(user)
    user.set_password(password, app.config['PASSWORD_SCHEME'])
    db.session.commit()


def try_drupal_auth(user_email, password):
    '''
    Try auth using drupal, for configured domain.
    :param user_email: User's email
    :param password: User's password
    :return: True on auth success, False on auth failure, None if not processed by Drupal
    '''
    if '@' in user_email:
        (just_user, domain) = user_email.split('@')
        if domain == drupal_conf['domain']:
            try:
                drupal_auth = check_drupal_password(just_user, password)
            except:
                # Failed with exception, that means there is a problem with something else, not the password.
                # Try to proceed with local login
                return None
            if drupal_auth:
                sync_drupal_user(just_user, domain, password)
                return True
            elif drupal_auth is None:
                return None
            else:
                return False
    return None


def get_user_with_external_auth(user_email, password):
    drupal_auth = try_drupal_auth(user_email, password)
    if drupal_auth is False:
        # Disrupt the normal processing, we have failed auth in Drupal
        return None
    return models.User.query.get(user_email)


def handle_authentication(headers):
    """ Handle an HTTP nginx authentication request
    See: http://nginx.org/en/docs/mail/ngx_mail_auth_http_module.html#protocol
    """
    method = headers["Auth-Method"]
    protocol = headers["Auth-Protocol"]
    # Incoming mail, no authentication
    if method == "none" and protocol == "smtp":
        server, port = get_server(headers["Auth-Protocol"], False)
        return {
            "Auth-Status": "OK",
            "Auth-Server": server,
            "Auth-Port": port
        }
    # Authenticated user
    elif method == "plain":
        server, port = get_server(headers["Auth-Protocol"], True)
        user_email = urllib.parse.unquote(headers["Auth-User"])
        password = urllib.parse.unquote(headers["Auth-Pass"])
        ip = urllib.parse.unquote(headers["Client-Ip"])
        user = get_user_with_external_auth(user_email, password)
        status = False
        if user:
            for token in user.tokens:
                if (token.check_password(password) and
                        (not token.ip or token.ip == ip)):
                    status = True
            if user.check_password(password):
                status = True
            if status:
                if protocol == "imap" and not user.enable_imap:
                    status = False
                elif protocol == "pop3" and not user.enable_pop:
                    status = False
        if status and user.enabled:
            return {
                "Auth-Status": "OK",
                "Auth-Server": server,
                "Auth-Port": port
            }
        else:
            status, code = get_status(protocol, "authentication")
            return {
                "Auth-Status": status,
                "Auth-Error-Code": code,
                "Auth-Wait": 0
            }
    # Unexpected
    return {}


def get_status(protocol, status):
    """ Return the proper error code depending on the protocol
    """
    status, codes = STATUSES[status]
    return status, codes[protocol]

def extract_host_port(host_and_port, default_port):
    host, _, port = re.match('^(.*)(:([0-9]*))?$', host_and_port).groups()
    return host, int(port) if port else default_port

def get_server(protocol, authenticated=False):
    if protocol == "imap":
        hostname, port = extract_host_port(app.config['HOST_IMAP'], 143)
    elif protocol == "pop3":
        hostname, port = extract_host_port(app.config['HOST_POP3'], 110)
    elif protocol == "smtp":
        if authenticated:
            hostname, port = extract_host_port(app.config['HOST_AUTHSMTP'], 10025)
        else:
            hostname, port = extract_host_port(app.config['HOST_SMTP'], 25)
    address = socket.gethostbyname(hostname)
    return address, port
