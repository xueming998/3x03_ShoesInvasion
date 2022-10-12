
// console.log(csrftoken)
console.log("Running")
var updateBtns = document.getElementsByClassName('quantityChange')

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
    console.log("Update Button Pressed")
    var shoppingCartID = this.dataset.product
    var action = this.dataset.action
    console.log('shoppingCartID:', shoppingCartID, 'Action:', action)
    shoppingCartOrder(shoppingCartID, action)
    })
}


// DeleteBtn 
var deletBtn = document.getElementById('deletBtn')
    deletBtn.addEventListener('click', function(){
    console.log("DeleteBtn Pressed")
    var url ='del_cartItem/'
    var shoppingCartID = this.dataset.product
    console.log(shoppingCartID)
    fetch(url,
    {
    method:'POST',
    headers:{
    'Content-Type':'application/json',
            'X-CSRFToken':csrftoken, 
    }, 
    body:JSON.stringify({'shoppingCartID':shoppingCartID})
    })
    .then((respose) => {
    return respose.json();
    })
    .then((data) => {
    // Either Reload or change the variable. Decide later. 
        location.reload()
    });
})

//checkoutBtn 
var checkoutBtn = document.getElementById('checkoutBtn')
checkoutBtn.addEventListener('click', function(){
    console.log("checkoutBtn Pressed")
    var url ='checkout_cartItem/'
    var user_id = this.dataset.product
    console.log(user_id)
    fetch(url,
    {
    method:'POST',
    headers:{
    'Content-Type':'application/json',
            'X-CSRFToken':csrftoken, 
    }, 
    body:JSON.stringify({'user_id':user_id})
    })
    .then((respose) => {
    console.log(respose)
    return respose.json();
    })
    .then((data) => {
    // Redirect to purchase complete page --> Prevents going back to shopping cart for any weird errors
    window.location.replace('paymentSuccess')
    });
})

function shoppingCartOrder(shoppingCartID,action)
{
console.log("Updating Data from Shopping Cart ")
var url ='update_cartItem/'
// 'X-CSRFToken':csrftoken, (Supposed to be inside headers)
fetch(url,
{
method:'POST',
headers:{
'Content-Type':'application/json',
        'X-CSRFToken':csrftoken, 
}, 
body:JSON.stringify({'shoppingCartID':shoppingCartID, 'action':action})
})
.then((respose) => {
return respose.json();
})
.then((data) => {
// Either Reload or change the variable. Decide later. 
    location.reload()
});

}