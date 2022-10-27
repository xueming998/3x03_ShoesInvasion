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
//   var csrftoken = getToken('csrftoken')
var addToCart = document.getElementById('addToCart')
addToCart.addEventListener('click', function(){
    console.log("Add to cart clicked")

    var color = document.getElementById('color').value;
    var size = document.getElementById('size').value;
    var quantity = document.getElementById("quantity_count").value;
    var url ='add_to_cart/'
    var productID = document.getElementById('product_id').value;

    fetch(url,
        {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken, 
        }, 
        body:JSON.stringify({'color':color,'size':size,'quantity':quantity,'shoe_id':productID,'user_id':1})
        })
        .then((respose) => {
            return respose.json();
        })
        .then((data) => {
        // Either Reload or change the variable. Decide later. 
            location.reload()
        });
});