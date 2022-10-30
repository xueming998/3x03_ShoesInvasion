<?php 
include ("../functions.php");
session_start();

$success = true;
$errorMsg = ''; 

// Checking for Product ID
if(empty($_POST["product_id"])){
    //Missing Product ID
	$errorMsg .= "Product ID is required.<br>";
	$success = false;
}else{
	$product_id = sanitize_input($_POST["product_id"]);
}

// Checking for Product Price
if(empty($_POST["product_price"])){
    //Missing Product Price
	$errorMsg .= "User ID is required.<br>";
	$success = false;
}else{
	$product_price = sanitize_input($_POST["product_price"]);
}

// Checking for Product ID
if(empty($_POST["product_name"])){
    //Missing Product ID
	$errorMsg .= "Product Name is required.<br>";
	$success = false;
}else{
	$product_name = sanitize_input($_POST["product_name"]);
}

// Checking for Product Info
if(empty($_POST["product_info"])){
    //Missing Product Info
	$errorMsg .= "Product Info is required.<br>";
	$success = false;
}else{
	$product_info = sanitize_input($_POST['product_info']);
}

// Checking for Product Brand
if(empty($_POST["product_brand"])){
    //Missing Product Brand
	$errorMsg .= "Product Brand is required.<br>";
	$success = false;
}else{
	$product_brand = sanitize_input($_POST['product_brand']);
}

if ($success == true)
{
		$status = updateProducts($product_id,$product_name,$product_price,$product_info,$product_brand);
		if ($status) {
			$response["sta"] = "1";
			$response["msg"] = "Update Success";
		} else {
			$response["success"] = "0";
			$response["msg"] = "Update Failed";
		}
}
else
{
	$response["success"] = "0";
	$response["msg"] = $errorMsg;
}


echo json_encode($response);

?>


?>