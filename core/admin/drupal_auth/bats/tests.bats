#!/usr/bin/env bats

CHECKPASS=../checkpassword.py

@test "returns 2 for invalid arguments" {
    # Supply no command to run
    run $CHECKPASS
    [ "$status" -eq 2 ]
    [ "${lines[1]}" = "Command missing" ]

    # Supply command, but
    run $CHECKPASS yes
    [ "$status" -eq 2 ]
    [ "${lines[1]}" = "Unable to read input from file descriptor 3." ]

}

@test "returns 111 for internal failure" {
    run $CHECKPASS -f configs/invalid_config.json true 3< requests/valid_request
    [ "$status" -eq 111 ]

    run $CHECKPASS -f configs/test_config.json true 3< requests/invalid_request
    [ "$status" -eq 111 ]
}

@test "returns 1 for authentication failure" {
    run $CHECKPASS -f configs/test_config.json true 3< requests/invalid_password_request
    [ "$status" -eq 1 ]
}

@test "returns 0 for successful authenticaton" {
    run $CHECKPASS -f configs/test_config.json echo yes 3< requests/valid_request
    [ "$status" -eq 0 ]
    [ "$output" = "yes" ]
}

@test "sets \$HOME on successful authentication" {
    run $CHECKPASS -f configs/test_config.json env 3< requests/valid_request
    line=`echo "$output" | grep HOME`
    [ "$line" = "HOME=/mail/testuser@mailtest-cmi.e-bs.cz" ]
}

@test "sets \$USER on successful authentication" {
    run $CHECKPASS -f configs/test_config.json env 3< requests/valid_request
    line=`echo "$output" | grep USER=`
    [ "$line" = "USER=testuser@mailtest-cmi.e-bs.cz" ]
}

@test "sets \$userdb_uid, \$userdb_gid and \$EXTRA with names of the vars" {
    run $CHECKPASS -f configs/test_config.json env 3< requests/valid_request
    userdb_uid=`echo "$output" | grep userdb_uid=`
    userdb_gid=`echo "$output" | grep userdb_gid=`
    extra=`echo "$output" | grep EXTRA`
    [ "$userdb_uid" = "userdb_uid=8" ]
    [ "$userdb_gid" = "userdb_gid=12" ]
    [ "$extra" = "EXTRA=userdb_home userdb_uid userdb_gid" ]
}