function getCookie(name) {
    cookies = document.cookie.split('; ');

    if (cookies.length == 1) {
        c = document.cookie.split('=');

        if ((c[0] == name)) {
            return c[1];
        }
    }
    else {
        for (i in cookies) {
            var x = cookies[i].split('=');
            
            if ((x[0] == name)) {
                return x[1];
            }
        }
    }

    return '';
}