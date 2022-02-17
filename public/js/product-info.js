window.onload = function() {
    cookies = document.cookie.split('; ');

    if (cookies.length == 1) {
        c = document.cookie.split('=');

        if ((c[0] == 'addToCart') && (c[1] == 'successful')) {
            document.getElementById('alert').style.display = 'block';

            setTimeout(function() {
                document.getElementById('alert').style.display = 'none';
            }, 2500)
        }
    }
    else {
        for (i in cookies) {
            var x = cookies[i].split('=');
            
            if ((x[0] == 'addToCart') && (x[1] == 'successful')) {
                document.getElementById('alert').style.display = 'block';

                setTimeout(function() {
                    document.getElementById('alert').style.display = 'none';
                }, 2000)
            }
        }
    }
}

window.onscroll = function() {
    if (document.getElementById('alert').style.display == 'block') {
        document.getElementById('alert').style.display = 'none';
    }
}


function redirectToLogin() {
    document.getElementById('addToCart').innerHTML = '<i class="fa fa-spinner fa-spin fa-fw fa-2x"></i>';

    location.replace('/login' + '?redirect=/cart/add/' + document.getElementById('productID').value + '?source=' + window.location.pathname);
}


function addToCart() {
    document.getElementById('addToCart').innerHTML = '<i class="fa fa-spinner fa-spin fa-fw fa-2x"></i>';

    location.replace('/cart/add/' + document.getElementById('productID').value + '?source=' + window.location.pathname);
}


function buyNow() {
    location.replace('/cart/add/' + document.getElementById('productID').value + '?source=/cart&next=/cart/checkout')
}