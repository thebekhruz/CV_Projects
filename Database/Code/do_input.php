<?php
// ------------------SHOW ERRORS--------------------------------
// ini_set('display_errors', '1');
// ini_set('display_startup_errors', '1');
// error_reporting(E_ALL);
// ----------------------------------------------------------------

// showData();
insertData();
openPage();


function showData(){
    foreach($_POST as $name_of_the_input => $value_of_input){
        echo("$name_of_the_input ==> $value_of_input \n\n");
        // echo("\n");
    }
}

function insertData(){
    $emp_id = $_POST['emp_id'];
    $name = $_POST['name'];
    $address = $_POST['address'];
    $dob = $_POST['dob'];
    $nin = $_POST['nin'];
    $department = $_POST['department'];
    $emergency_name = $_POST['emergency_name'];
    $emergency_relationship = $_POST['emergency_relationship'];
    $emergency_phone = $_POST['emergency_phone'];

    
    $pdo = new PDO('mysql:host=localhost', 'root', 'root', );
    $pdo->setAttribute( PDO::ATTR_ERRMODE, PDO::ERRMODE_WARNING );



    $pdo ->query("USE emplDB");
    $sql = "INSERT INTO employees (emp_id, `name`, `address`, dob, nin, department, emergency_name, emergency_relationship, emergency_phone) VALUES ('$emp_id', '$name', '$address', '$dob', '$nin', '$department', '$emergency_name', '$emergency_relationship', '$emergency_phone')";

    $stmt = $pdo ->query($sql);
    
    $stmt->execute([
        'emp_id' => $emp_id,
        'name' => $name,
        'address' => $address,
        'dob' => $dob,
        'nin' => $nin,
        'department' => $department,
        'emergency_name' => $emergency_name,
        'emergency_relationship' => $emergency_relationship,
        'emergency_phone' => $emergency_phone
    ]);

    // echo("Data inserted successfully \n");

}
function openPage(){
    header("Location: index.php");

}


?>