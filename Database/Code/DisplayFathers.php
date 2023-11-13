<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" integrity="sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi" crossorigin="anonymous">

<style>
table, th, td {
    border: 1px solid black;
    margin-right: 2em;
}
</style>
</head>
<body>



<?php
// ------------------SHOW ERRORS--------------------------------
// ini_set('display_errors', '1');
// ini_set('display_startup_errors', '1');
// error_reporting(E_ALL);
// ----------------------------------------------------------------

$pdo = new PDO('mysql:host=localhost', 'root', 'root', );
$pdo->setAttribute( PDO::ATTR_ERRMODE, PDO::ERRMODE_WARNING );
        

$pdo ->query("USE emplDB");
    
$sql = "SELECT * FROM employees
WHERE department = 'Driver'
AND emergency_relationship = 'Father'";

$stmt = $pdo ->query($sql);

// $result = $stmt->fetchAll(PDO::FETCH_ASSOC);
// $stmt->execute();

echo "<table class = 'table'><tr>
<th>Name</th>
<th>Department</th>
<th>Emergency relationship</th>
<th>Name</th>
</tr>";
while($row = $stmt->fetch(PDO::FETCH_ASSOC)){
    echo"<tr>
        <td>".$row['name']."</td>
        <td>".$row['department']." </td> 
        <td>".$row['emergency_relationship']."</td>
        <td>".$row['name']."</td>
        </tr>";
        
    };
    // <td>".$row['emergency']."</td>
    
    echo "</table>";


?>

<a type="button" class="btn btn-light" href="index.php">
    <h6>Home Page:
        <small class="text-muted">
            index
        </small>
        </h6>
    </a>
</body>
</html>