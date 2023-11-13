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


    $pdo = new PDO('mysql:host=localhost', 'root', 'root', );
    $pdo->setAttribute( PDO::ATTR_ERRMODE, PDO::ERRMODE_WARNING );
            

    $pdo ->query("USE emplDB");

    $todaysDate =  date('F, Y');

    echo "This month: $todaysDate. These people have birthday!";
    echo "
    <br>
    <br>
    <a type='button' class='btn btn-light' href='index.php'>
        <h6>Home Page:
            <small class='text-muted'>
              index
            </small>
        </h6>
    </a>";

    $sql = "SELECT * FROM `employees` WHERE dob LIKE '___12%';";

    $stmt = $pdo ->query($sql);

    echo "<table class = 'table table table-striped'><tr>
    <th>Employee ID</th>
    <th>Name</th>
    <th>address</th>
    <th>Department</th>
    <th>Date of Birth</th>
    </tr>";

    while($row = $stmt->fetch(PDO::FETCH_ASSOC)){
        echo"<tr>
            <td>".$row['emp_id']."</td>
            <td>".$row['name']." </td> 
            <td>".$row['address']."</td>
            <td>".$row['department']."</td>
            <td>".$row['dob']."</td>

            </tr>";
            
        };
    echo "</table>";        

?>