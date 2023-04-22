<?php

require_once "utils.php";

function get_integrity_logs()
{
    $json_data = @file_get_contents(get_log_file_path());
    if (!$json_data) {
        return "No logs";
    } else {
        return json_decode($json_data);
    };
}

add_action('rest_api_init', function () {
    register_rest_route('logging', 'check-logs', array(
        'methods' => WP_REST_Server::READABLE,
        'callback' => 'get_integrity_logs',
        'permission_callback' => '__return_true'
    ));
});
