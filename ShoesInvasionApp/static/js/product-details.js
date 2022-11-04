// function getToken(name) {
//     var cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         var cookies = document.cookie.split(';');
//         for (var i = 0; i < cookies.length; i++) {
//             var cookie = cookies[i].trim();
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
//   }
// var csrftoken = getToken('csrftoken') 
// var csrftoken = document.getElementsByName('csrfmiddlewaretoken').value


var addToCart = document.getElementById('addToCart')
addToCart.addEventListener('click', function(){
    console.log("Add to cart clicked")
    var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value
    var color = document.getElementById('color').value
    console.log(color)
    var size = document.getElementById('size').value
    console.log(size)
    var quantity = document.getElementById("quantity_count").value
    console.log(quantity)
    var url ='add_to_cart/'
    var productID = document.getElementById('product_id').value
    console.log(productID)
    var status = document.getElementById('status').value
    console.log(status)
    console.log("Detail collection over")
    console.log(csrfToken)

    fetch(url,
        {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrfToken,  
        }, 
        mode:'same-origin',
        body:JSON.stringify({'color':color,'size':size,'quantity':quantity,'shoe_id':productID,'status':status})
        })
        .then((respose) => {
            return respose.json();
        })
        .then((data) => {
            if (data == "Shoe Failed")
            {
                window.location.href = "login";
            }else{
                // Either Reload or change the variable. Decide later. 
                location.reload()
            }
        });

});