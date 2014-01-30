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
    console.log('Submitting login popup...');
    var data = $('#login-form').serializeArray();
    console.log(data);

    $.ajax({
        url: '/login/',
        type: 'POST',
        data: data,

        success: function (response) {
            if (response.login == true) {
                document.location.href = '/user/' + response.username
            } else {
                $('#login-error').html(response.errors).show()
            }
        },
        error: function () {
            console.log("Login error")
        }
    });
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
                document.location.href = '/thanks';
            } else {
                console.log(response)
                $('#signup-error').html(response)
                errors = response;
                for (error in errors) {
                    console.log(error);
                    console.log(errors[error]);
                    var id = '#error-' + error;
                    $(id).html($(errors[error]+"ul li").text());
                }
            }
        },
        error: function () {
            console.log("Signup error")
        }
    });
};