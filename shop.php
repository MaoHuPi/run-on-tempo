<?php
$type = @$_GET['type'] ? $_GET['type'] : '';
if($type != ''){
    $dir = [];
    if($type == 'character'){
        $dir = scandir(__DIR__.'/character/');
    }
    else if($type == 'song'){
        $dir = scandir(__DIR__.'/song/');
    }
    $dir = array_slice($dir, 2);
    $path = dirname('https://'.$_SERVER['HTTP_HOST'].$_SERVER['REQUEST_URI']);
    for($i = 0; $i < count($dir); $i++){
        $dir[$i] = $path.'/'.$type.'/'.$dir[$i];
    }
    echo(json_encode($dir));
}
?>