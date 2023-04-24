<?php

try
{
    $pharDir = $argv[1];
    $pharFile = $argv[2];

    // clean up
    if (file_exists($pharFile)) 
    {
        unlink($pharFile);
    }

    // create phar
    $phar = new Phar($pharFile);

    // start buffering. Mandatory to modify stub to add shebang
    $phar->startBuffering();

    // Add the rest of the apps files
    $phar->buildFromDirectory($pharDir);

    $phar->stopBuffering();

    // plus - compressing it into gzip  
    $phar->compressFiles(Phar::GZ);
}
catch (Exception $e)
{
    echo $e->getMessage();
}
