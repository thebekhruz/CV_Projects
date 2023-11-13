<?php
// ------------------SHOW ERRORS--------------------------------
// ini_set('display_errors', '1');
// ini_set('display_startup_errors', '1');
// error_reporting(E_ALL);
// ----------------------------------------------------------------
// showData();
UpdateData();
openPage();
function showData(){
    foreach($_POST as $name_of_the_input => $value_of_input){
        echo("$name_of_the_input ==> $value_of_input \n\n");
        // echo("Hello $name_of_the_input");
    }
}

function UpdateData(){
    $emp_id = $_POST["emp_id"];
    $salary = $_POST["salary"];

    $pdo = new PDO('mysql:host=localhost', 'root', 'root', );
    $pdo->setAttribute( PDO::ATTR_ERRMODE, PDO::ERRMODE_WARNING );
        

    $pdo ->query("USE emplDB");
    $sql = "UPDATE employees SET salary = '$salary' WHERE emp_id ='$emp_id'";

    $stmt = $pdo ->query($sql);
    $stmt->execute([
        'salary' => $salary
    ]);
}
function openPage(){
    header("Location: index.php");

}

?>