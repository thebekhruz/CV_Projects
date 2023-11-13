<!DOCTYPE html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Employees Data</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" integrity="sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi" crossorigin="anonymous">
    <link rel="stylesheet" href="index.css">
    <script src="index.js"></script>

</head>
<body>
    <!-- Keeps everything in one box -->
    <div class="container">
        <!-- Header -->
        <div class="row text-center">
            <div class ="col myHeader"  >
                <h2>Employee Database</h2>
            </div>        
        </div>
        
        <!-- Keeps main Content -->
        <div class="row">
            <!-- Defines Link column -->
            <div class="col links text-left LinkX" >
                <div class="row" >
                    <div class="row"> 
                    <!--Button 1  -->
                    <a type="button" class="btn btn-light" href="index.php">
                        <h6>Home Page:
                            <small class="text-muted">
                                index
                            </small>
                        </h6>
                        </a>
                    </div>
                    <div class="row">
                         <!--Button 2  -->
                    <a type="button" class="btn btn-light" href="AddingEmployee.php">
                        <h6>Task 1:
                            <small class="text-muted">
                                Adding employees
                            </small>
                        </h6>
                    </a>
                    </div>
                     <!-- Button 3 -->
                    <div class="row"> 
                        <a type="button" class="btn btn-light" href="UpdateEmployee.php">
                            <h6>Task 2:
                                <small class="text-muted">
                                    Update the details 
                                </small>
                            </h6>
                        </a>
                    </div>
                    <div class="row"> 
                        <a type="button" class="btn btn-light" href="DeleteRecordMain.php">
                            <h6>Task 3 and Task 6:
                                <small class="text-muted">
                                    Deleting Employee Info 
                                </small>
                            </h6>
                        </a>
                    </div>
                    <!-- Button 4 -->
                    <div class="row"> 
                    <a type="button" class="btn btn-light" href="DisplayFathers.php">
                            <h6>Task 4:
                                <small class="text-muted">
                                Drivers who have emergency contact their Father
                                </small>
                            </h6>
                    </a>
                    </div>
                    <div class="row"> 
                    <a type="button" class="btn btn-light" href="BirthdayCards.php">
                            <h6>Task 5:
                                <small class="text-muted">
                                Birthday Cards
                                </small>
                            </h6>
                        </a> 

                    </div>
                    
                </div>
            </div>            
            <!-- Defines Content column -->
            <div class="col-6 content text-right" id="ContentColumn">
                <h2>Content</h2>
                <p>Hello please select what you want to do on the left side of the screen! 
                    
                
                Thank you!
                </p>
            </div>
                
        </div>
    </div>


</body>