var count = 0
$(document).ready(function () {
    $('#user-name').click(function () {
        console.log('click');
        if (count == 0) {
            $('.user-settings').show();
            count = 1;
        } else {
            $('.user-settings').hide();
            count = 0;
        }
        ;
    });
});

$(function () {
    $('#login-button').click(function (e) {
        e.preventDefault();
        submitLoginForm();
    });
});

submitLoginForm = function () {
    console.log("Login processing ...");
    var data = $('#login-form').serializeArray();
    console.log(data);

    $.ajax({
        url: '/login/',
        type: 'POST',
        data: data,

        beforeSend: function () {
            if (checkLoginEmptyFields(data) == false) {
                return false;
            }
        },

        success: loginAuthentication,

        error: function () {
            console.log("Login error")
        }
    });
};

checkLoginEmptyFields = function (data) {
    var loginFormInputs = $("#login-form input");
    loginFormInputs.removeClass('empty-input');

    if (data[1].value == '' || data[2].value == '') {
        $('#login-error').html('');

        if (data[1].value == '' && data[2].value == '') {
            loginFormInputs.addClass('empty-input');
        } else if (data[1].value == '') {
            $("#login-form input[name='username']").addClass('empty-input');
        } else if (data[2].value == "") {
            $("#login-form input[name='password']").addClass('empty-input');
        }
        return false;
    } else {
        return true;
    }
};

loginAuthentication = function (response) {
    if (response.login == true) {
        window.location = '/user/' + response.username
    } else {
        $('#login-error').html(response.errors);
    }
};


$(function () {
    $('#signup-button').click(function (e) {
        e.preventDefault();
        submitSignupForm();
    });
});

submitSignupForm = function () {
    console.log('Submitting login popup...');
    var data = $('#signup-form').serializeArray();
    console.log(data);

    $.ajax({
        url: '/signup/',
        type: 'POST',
        data: data,
        success: function (response) {
            if (response == 'true') {
                window.location = '/thanks';
            } else {
                $("#login-error").html('');
                for (error in response) {
                    var id = '#error-' + error;
                    $(id).html($(response[error] + "ul li").text());
                }
            }
        },
        error: function () {
            console.log("Signup error")
        }
    });
};