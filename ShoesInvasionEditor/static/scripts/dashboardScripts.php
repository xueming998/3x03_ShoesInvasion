<?php

// only usable for statements with no variable 
function executeStmt($string,$conn){
  $stmt = $conn->prepare($string);
  if($stmt->execute()){
    return $stmt->get_result();
  }
  return 0;
}

// only usable for this php sql functions
function stmt_iterate($result){
  if ($result->num_rows == 1){
    $row = $result->fetch_assoc();
    return $row['result'];
  }
  return '0';
}

// function to get the number of shoes sold for each type
function getCountShoeType($value,$conn){

  $stmt = $conn->prepare("SELECT SUM(quantity) as result FROM Transaction_Items WHERE product_id IN (SELECT product_id FROM Products where product_category=?)");
  $stmt->bind_param("s",$value);
  $stmt->execute();
  $result = $stmt->get_result();
  $stmt->close();
  if ($result->num_rows == 1){
    $row = $result->fetch_assoc();
    return $row['result'];
  }
  return '0';
}
?>