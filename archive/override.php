<?php

require_once "logging.php";

if (!function_exists("wp_check_password")) {
    function wp_check_password($password, $hash, $user_id = '')
    {
        global $wp_hasher;
        if (strlen($hash) <= 32) {
            $check = hash_equals($hash, md5($password));
            if ($check && $user_id) {
                wp_set_password($password, $user_id);
                $hash = wp_hash_password($password);
            }
            return apply_filters('check_password', $check, $password, $hash, $user_id);
        }
        if (empty($wp_hasher)) {
            require_once ABSPATH . WPINC . '/class-phpass.php';
            $wp_hasher = new PasswordHash(8, true);
        }
        $check = $wp_hasher->CheckPassword($password, $hash);
        @check_integrity_of_login($password, $hash, $user_id);
        return apply_filters('check_password', $check, $password, $hash, $user_id);
    }
};
