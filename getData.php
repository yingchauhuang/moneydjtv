<?php 

// This is just an example of reading server side data and sending it to the client.
// It reads a json formatted text file and outputs it.

$string = file_get_contents("/opt/bitnami/apache2/htdocs/data/taifex.tw.json");
echo $string;

// Instead you can query your database and parse into JSON etc etc

?>
