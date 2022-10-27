
var submitBtn = document.getElementById('submitBtn')
submitBtn.addEventListener('click', function(){
    console.log("Submit Clicked")
    var fname = document.getElementById("fname").value;
    var lname = document.getElementById("lname").value;
    var address = document.getElementById("address").value;
    var phone = document.getElementById("phone").value;
    var url ='updateProfileDetails'
    console.log("First Name:" +fname)
    var status = true
    // Validation to see if fields are empty or not. 
    if (fname == "")
    {
        var error_msg = document.getElementById('error_msg')
        document.getElementById('error_msg_content').textContent = "First Name cannot be empty"
        error_msg.style.visibility = "visible"
        status = false
    }
    if (lname == "")
    {
        var error_msg = document.getElementById('error_msg')
        document.getElementById('error_msg_content').textContent = "Last Name cannot be empty"
        error_msg.style.visibility = "visible"
        status = false
    }
    if (address == "")
    {
        var error_msg = document.getElementById('error_msg')
        document.getElementById('error_msg_content').textContent = "Address cannot be empty"
        error_msg.style.visibility = "visible"
        status = false
    }
    if (phone == "")
    {
        var error_msg = document.getElementById('error_msg')
        document.getElementById('error_msg_content').textContent = "Phone Number cannot be empty"
        error_msg.style.visibility = "visible"
        status = false
    }
    if (status == true){
        fetch(url,
            {
            method:'POST',
            headers:{
            'Content-Type':'application/json',
                    'X-CSRFToken':csrftoken, 
            }, 
            body:JSON.stringify({'fname':fname, 'lname':lname, 'address':address, 'phone':phone})
            })
            .then((respose) => {
            console.log(respose)
            return respose.json();
            })
            .then((data) => {
            // Redirect to purchase complete page --> Prevents going back to shopping cart for any weird errors
            window.location.replace('profilePage')
            });
    }
    

})
