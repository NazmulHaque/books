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

    $.ajax({
        url: '/signup/',
        type: 'POST',
        data: data,
        success: function (response) {
            if (response == 'true') {
                window.location = '/thanks';
            } else {
                $(".signup-error").html('');
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

$(function () {
    $('#profile-menu li').click(function (e) {
        e.preventDefault();
        var profileMenuType = e.target.id;
        console.log(profileMenuType);
        showInfoForm(profileMenuType);
    });
});

showInfoForm = function ($profileMenuType) {
    console.log("Showing Basic Info Form ...");
    console.log($profileMenuType);
    var url = '';
    if ($profileMenuType == 'update-basic-info') {
        url = '/user/update-basic-info/';
    } else if ($profileMenuType == 'update-profile-photo') {
        url = '/user/update-profile-photo/';
    } else if ($profileMenuType == 'change-password') {
        url = '/user/change-password/'
    }
    console.log(url);
    $.ajax({
        url: url,
        success: function (response) {
            $('#profile-update-default-view').hide();
            $('#profile-update-form').html(response);
        },
        error: function () {
            console.log('error')
        }
    });
};

$(function () {
    $(document).on('click', "#submit-basic-info-button", function (e) {
        console.log("Submitting Basic Info Form...");
        e.preventDefault();
        submitBasicInfoForm();
    });
});

submitBasicInfoForm = function () {
    console.log('Submitting Basic Info Form...');
    var data = $('#update-basic-info-form').serializeArray();
    console.log(data);

    $.ajax({
        url: "/user/update-basic-info/",
        type: 'POST',
        data: data,
        success: function (response) {
            console.log('Submitted');
            if (response == 'true') {
                $('#profile-update-message').html("Your Basic Profile Info is Successfully Updated.");
                setTimeout( "$('#profile-update-message').hide();",3000 );
                $('#profile-update-form').hide();
                $('#profile-update-default-view').html('');
            } else {
                for (error in response) {
                    var id = '#error-' + error;
                    $(id).html($(response[error] + "ul li").text());
                }
            }
        },
        error: function () {
            console.log('error');
        }
    });
};
$(function () {
    $(document).on('change', "#update-basic-info-form input, #update-basic-info-form textarea", function () {
        $("#submit-basic-info-button").removeAttr("disabled", "disabled");
    });
});