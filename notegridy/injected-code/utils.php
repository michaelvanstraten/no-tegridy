<?php

function get_root() {
    return pathinfo(str_replace("phar://", "", plugin_dir_path( __FILE__ )), PATHINFO_DIRNAME);
}

function get_log_file_path()
{
    return get_root() . "/log.json";
}

function get_key_file_path() {
    return get_root() . "/.key_file";
}
