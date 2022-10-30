<?php 
include ("../functions.php");
function startSQLs(){
    // Start SQL connection
        $config = parse_ini_file('../../../../private/db-config.ini');
        $conn = new mysqli($config['servername'], $config['username'],
            $config['password'], $config['dbname']);
  // Check connection
	if (!$conn->connect_error)
	{
		return $conn;   
	}
	else
	{
		return NULL;
	}
}
session_start();

$success = true;
$errorMsg = '';

// Checking for Product Price
if(empty($_POST["product_price"])){
    //Missing Product Price
	$errorMsg .= "User ID is required.<br>";
	$success = false;
}else{
	$product_price = sanitize_input($_POST["product_price"]);
        $product_price = floatval($product_price);
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
    $status = insertProducts($product_name,$product_price,$product_info,$product_brand);
    if ($status) {
	$response["success"] = "1";
	$response["msg"] = "Insert Success";
    } else {
	$response["success"] = "0";
	$response["msg"] = "Insert Failed";
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