<?php
    if (!isset($_SERVER['PHP_AUTH_USER'])) {
        header("WWW-Authenticate: Basic realm=\"Private Area\"");
        header("HTTP/1.0 401 Unauthorized");
        print "Sorry - you need valid credentials to be granted access!\n";
        exit;
    } else {
        if (($_SERVER['PHP_AUTH_USER'] == 'test') && ($_SERVER['PHP_AUTH_PW'] == 'test')) {
            print "Welcome to the compute engine";
        } else {
            header("WWW-Authenticate: Basic realm=\"Private Area\"");
            header("HTTP/1.0 401 Unauthorized");
            print "Sorry - you need valid credentials to be granted access!\n";
            exit;
        }
    }
?>
<!DOCTYPE html>
<html>
<head>
        <title>Compute Engine</title>
</head>
<body>
<h2>Compute Engine</h2>
<p style="color:red">Note: Please check server status before submitting any task.
<p>Check server status:</p>
<button><a href="./cgi-bin/update_stats.py">Check</a></button>
<p>Upload a File, .py or .c </p>
<form enctype="multipart/form-data" action="./cgi-bin/save_file.py" method="post">
        <p>File: <input type="file" name="file"></p>
        <p>Select priority<p>
        <input type="radio" name="priority" value="3">Low<br>
        <input type="radio" name="priority" value="2" checked="checked">Medium<br>
        <input type="radio" name="priority" value="1">High<br>
        <p><input type="submit" value="Upload"></p>
</form>
</body>
</html>
