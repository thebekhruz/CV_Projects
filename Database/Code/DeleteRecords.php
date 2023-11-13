
<?php

DeleteRecords();
InsertRecords();
openPage();

    function DeleteRecords(){
        $pdo = new PDO('mysql:host=localhost', 'root', 'root', );
        $pdo->setAttribute( PDO::ATTR_ERRMODE, PDO::ERRMODE_WARNING );


        $emp_idDelete = $_POST['emp_idDelete'];
        $emp_id = $_POST['emp_id'];

        $pdo ->query("USE emplDB");
        $sql = "DELETE FROM `employees`
        WHERE `emp_id` ='$emp_idDelete' ;";

        $stmt = $pdo ->query($sql);
        
        // echo "Thank you employee has been deleted. \n";
    }

function InsertRecords()
{
    $pdo = new PDO('mysql:host=localhost', 'root', 'root', );
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_WARNING);

    
    $emp_idDelete = $_POST['emp_idDelete'];
    $emp_id = $_POST['emp_id'];

    $emp_id = $_POST['emp_id'];
    $todaysDate = date('d/m/Y');
    $timeNow = date('h:i');

    $pdo ->query("USE emplDB");
    $sql = "INSERT INTO `deleted_employees`
    (deletedEmp_id, `date`, `time`, emp_id)
    VALUES( '$emp_idDelete', '$todaysDate', '$timeNow', '$emp_id')";

    $stmt = $pdo ->query($sql);

    $stmt->execute([
        'deletedEmp_id' => $emp_idDelete,
        'date' => $todaysDate,
        'time' => $timeNow,
        'emp_id' => $emp_id,
    ]);

    // echo "Thank you employee has been added to your Deleted Employees table.";



}
function openPage(){
    header("Location: index.php");

}






?>