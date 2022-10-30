<?php
include ("../functions.php");
session_start();

$success = true;
$errorMsg = '';

// Checking for User ID
if(empty($_POST["product_id"])){
    //Missing User ID
	$errorMsg .= "Product ID is required.<br>";
	$success = false;
}else{
	$product_id = $_POST["product_id"];
}

if ($success == true)
{
	$status = deleteProduct($product_id);

	if ($status) {
		$response["success"] = "1";
//		$response["msg"] = "Delete Success";
                $response["msg"] = $status;
	} else {
		$response["success"] = "0";
		
	}
}
else
{
	$response["success"] = "0";
	$response["msg"] = $errorMsg;
}

echo json_encode($response);
?>