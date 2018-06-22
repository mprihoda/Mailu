<?php
    // IMAP server
    $servers['imap'] = array(
        // ENABLED by default; will connect to IMAP port on local server
        'disabled' => false,
        'name' => 'IMAP Server',
        'hostspec' => 'imap',
        'hordeauth' => false,
        'protocol' => 'imap',
        'port' => 143,
        // Plaintext logins are disabled by default on IMAP servers (see RFC 3501
        // [6.2.3]), so TLS is the only guaranteed authentication available by
        // default.
        // 'secure' => 'tls',
        'secure' => false,
    );
?>
