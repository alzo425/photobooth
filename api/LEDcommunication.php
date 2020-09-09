<?php
header('Content-Type: application/json');

require_once('../lib/config.php');

function LEDcommunication($Mode)
{

    global $config;

    exec("killall -9 python3 > logKill.txt 2>&1 &");
    
    $dir="/var/www/html/api";
    chdir($dir);
    $cmd = "python3 PhotoBoothLEDsV2.py -$Mode > log.txt 2>&1 &";

    exec($cmd, $output, $returnValue);

    if ($returnValue) {
        die(json_encode([
                'error' => 'Execution not possible',
                'cmd' => $cmd,
                'returnValue' => $returnValue,
                'output' => $output,
            ]));
        }

}

//übergabe json an frontend error handling
// no mode provided from frontend, error return
if (!isset($_POST['mode'])) {
    die(json_encode([
        'error' => 'No mode provided'
    ]));
 } 
// choos which mode was provided and forward it to executeable function
if ($_POST['mode'] === 'home'){
     LEDcommunication('home');
    die(json_encode([
        'success' => 'home'
    ]));
} elseif ($_POST['mode'] === 'flashing'){
     LEDcommunication('flashing');
    die(json_encode([
        'success' => 'flashing'
    ]));
} elseif ($_POST['mode'] === 'gallery'){
     LEDcommunication('gallery');
    die(json_encode([
        'success' => 'gallery'
    ]));
} elseif ($_POST['mode'] === 'loading'){
     LEDcommunication('loading');
    die(json_encode([
        'success' => 'loading'
    ]));
} elseif ($_POST['mode'] === 'picture'){
     LEDcommunication('picture');
    die(json_encode([
        'success' => 'picture'
    ]));
}


// send imagename to frontend
echo json_encode([
    'success' => 'mode'
]);

