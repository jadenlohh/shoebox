if (document.getElementById('changePwdForm') != null) {
    document.getElementById('changePwdForm').addEventListener('submit', function(event) {
        if (!validpwd()) {
            event.preventDefault();
    
            document.getElementById('msg').classList.add('animation');
            document.getElementById('msg').style.color = 'red';
            document.getElementById('msg').innerHTML = 'Your password must be at least 8 characters long with \
            a mix of numbers, uppercase and lowercase letters';
        }
        else if (document.getElementById('newPwd').value != document.getElementById('confirmPwd').value) {
            event.preventDefault();
    
            document.getElementById('msg').classList.add('animation');
            document.getElementById('msg').style.color = 'red';
            document.getElementById('msg').innerHTML = 'Passwords does not match!';
        }
    
        setTimeout(function() {
            document.getElementById('msg').classList.remove('animation');
        }, 500)
    })
}

if (document.getElementById('manageAccountForm') != null) {
    var email = document.getElementById('email');
    var firstName = document.getElementById('firstName');
    var lastName = document.getElementById('lastName');

    var email_value = email.value;
    var firstName_value = firstName.value;
    var lastName_value = lastName.value;

    firstName.onkeyup = function() {
        if (document.getElementById('firstName').value != firstName_value) {
            document.getElementById('submitBtn').disabled = false;
        } 
        else {
            document.getElementById('submitBtn').disabled = true;
        }
    }

    lastName.onkeyup = function() {
        if (document.getElementById('lastName').value != lastName_value) {
            document.getElementById('submitBtn').disabled = false;
        } 
        else {
            document.getElementById('submitBtn').disabled = true;
        }
    }

    email.onkeyup = function() {
        if (document.getElementById('email').value != email_value) {
            document.getElementById('submitBtn').disabled = false;
        } 
        else {
            document.getElementById('submitBtn').disabled = true;
        }
    }
}

function validpwd() {
    const password = document.getElementById('newPwd').value;

    const lowerCaseLetters = /[a-z]/g;
    const upperCaseLetters = /[A-Z]/g;
    const numbers = /[0-9]/g;

    return password.match(lowerCaseLetters) && password.match(upperCaseLetters) &&
        password.match(numbers) && password.length >= 8;
}
