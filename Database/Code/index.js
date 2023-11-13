function validator(){

    let empId = document.getElementById("empID").value;
    let lengthX = empId.length;
    if(lengthX < 5){
        document.getElementById("empID").innerHTML="Please provide a valid ID"
        return false;
    } else{
        alert("You have successfully added an employee");
    }




}

function forall(){
    alert("Thank you!");
}

function validatorDelete(){

    let empId = document.getElementById("empID").value;
    let lengthX = empId.length;
    if(lengthX < 5){
        document.getElementById("empID").innerHTML="Please provide a valid ID"
        return false;
    } else{
        alert("You have successfully deleted an employee");
    }




}
function UpdateEmployee(){
    let empIdX = document.getElementById("idX").value;
    alert("You have successfully updated an employee");
    alert(empIdX.length())
    let salaryX = document.getElementById("salaryX").value;

    if(empIdX.length()<4){
        document.getElementById("idX").innerHTML="Please provide a valid ID";
        return false;
    }
    else if(salaryX.length()<5){
        document.getElementById("salaryX").innerHTML="Please provide a valid salary";
        return false;
    }   

}