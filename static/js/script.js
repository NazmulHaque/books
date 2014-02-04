var count = 0
$(function () {
    $('#user-name').click(function () {
        if (count == 0) {
            $('.user-settings').show();
            count = 1;
        } else {
            $('.user-settings').hide();
            count = 0;
        }
    });

    $('#login-button').click(function (e) {
        e.preventDefault();
        submitLoginForm();
    });

    $('#signup-button').click(function (e) {
        e.preventDefault();
        submitSignupForm();
    });

    $('#profile-menu li').click(function (e) {
        e.preventDefault();
        var profileMenuType = e.target.id;
        showUserInfoForm(profileMenuType);
    });

    $("#submit-basic-info-first-time-button").click(function (e) {
        e.preventDefault();
        submitBasicInfoFirstTimeForm();
    });

    $("#post-ad-form input, #post-ad-form textarea").change(function () {
        $("#post-ad-button").removeAttr("disabled", "disabled");
    });

    $("#post-ad-button").click(function (e) {
        e.preventDefault();
        submitPostAdForm();
    });

    $("#search-button").click(function (e) {
        e.preventDefault();
        submitSearch();
    });

});


//selector after ajax load
$(function () {
//    $(document).on('click', "#submit-profile-photo-form", function (e) {
//        e.preventDefault();
//        submitProfilePhotoForm();
//    });
    $(document).on('click', "#submit-basic-info-button", function (e) {
        e.preventDefault();
        submitBasicInfoForm();
    });

    $(document).on('click', "#change-password-button", function (e) {
        e.preventDefault();
        submitChangePasswordForm();
    });

    $(document).on('change', "#update-basic-info-form input, #update-basic-info-form textarea", function () {
        $("#submit-basic-info-button").removeAttr("disabled", "disabled");
    });
    $(document).on('change', "#update-basic-info-first-time-form input, #update-basic-info-first-time-form textarea", function () {
        $("#submit-basic-info-first-time-button").removeAttr("disabled", "disabled");
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

        error: commonErrorMessage
    });
};

commonErrorMessage = function () {
    console.log("Something went Wrong...")
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
        window.location = '/user/' + response.username;
    } else {
        $('#login-error').html(response.errors);
    }
};

submitSignupForm = function () {
    console.log('Submitting login popup...');
    var data = $('#signup-form').serializeArray();

    $.ajax({
        url: '/signup/',
        type: 'POST',
        data: data,
        success: signupSuccess,
        error: commonErrorMessage
    });
};

signupSuccess = function (response) {
    if (response == 'true') {
        window.location = '/thanks';
    } else {
        $("#signup-form .form-error").html('');
        for (error in response) {
            var id = '#error-' + error;
            $(id).html($(response[error] + "ul li").text());
        }
    }
};

showUserInfoForm = function ($profileMenuType) {
    console.log("Showing Basic Info Form ...");
    console.log($profileMenuType);
    var url = '';
    if ($profileMenuType == 'update-basic-info') {
        url = '/user/update-basic-info/';
    } else if ($profileMenuType == 'update-profile-photo') {
        url = '/user/upload-profile-photo/';
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
        error: commonErrorMessage
    });
};

submitBasicInfoForm = function () {
    console.log('Submitting Basic Info Form...');
    var data = $('#update-basic-info-form').serializeArray();
    console.log(data);

    $.ajax({
        url: "/user/update-basic-info/",
        type: 'POST',
        data: data,
        success: basicInfoSubmissionSuccess,
        error: commonErrorMessage
    });
};

basicInfoSubmissionSuccess = function (response) {
    if (response == 'true') {
        $('#profile-update-message').html("Your Basic Profile Info is Successfully Updated.");
        setTimeout("$('#profile-update-message').hide();", 3000);
        $('#profile-update-default-view').show();
        $('#profile-update-form').html('');
    } else {
        $("#update-basic-info-form .form-error").html('');
        for (error in response) {
            var id = '#error-' + error;
            $(id).html($(response[error] + "ul li").text());
        }
    }
};

submitBasicInfoFirstTimeForm = function () {
    console.log('Submitting Basic Info Form...');
    var data = $('#update-basic-info-first-time-form').serializeArray();
    console.log(data);

    $.ajax({
        url: "/user/update-profile-first-time/",
        type: 'POST',
        data: data,
        success: function (response) {
            console.log(response)
            if (response.submit == true) {
                window.location = '/user/' + response.username;
            } else {
                for (error in response) {
                    var id = '#error-' + error;
                    $(id).html($(response[error] + "ul li").text());
                }
            }
        },
        error: commonErrorMessage
    });
};

basicInfoFirstUpdateSuccess = function (response) {
    if (response.submit == true) {
        window.location = '/user/' + response.username;
    } else {
        $("#update-basic-info-first-time-form .form-error").html('');
        for (error in response) {
            var id = '#error-' + error;
            $(id).html($(response[error] + "ul li").text());
        }
    }
};

//submitProfilePhotoForm = function () {
//    console.log("Uploading profile photo ...")
//    var data = $('#update-profile-photo-form').serializeArray();
//    console.log(data);
//    $.ajax({
//            url: "/user/upload-profile-photo/",
//            type: 'POST',
//            data: data,
//
//            success: function (response) {
//                if (response == 'true') {
//                    $('#profile-update-message').html("Your Profile Photo Uploaded Successfully.");
//                    setTimeout("$('#profile-update-message').hide();", 3000);
//                    $('#profile-update-default-view').show();
//                    $('#profile-update-form').html('');
//                } else {
//                    $("#photo-upload-error").html(response);
//                }
//            },
//            error: function () {
//                console.log("error");
//            }
//
//        }
//    );
//};

submitChangePasswordForm = function () {
    console.log('Submitting Change Password Form...');
    var data = $('#change-password-form').serializeArray();
    console.log(data);

    $.ajax({
        url: "/user/change-password/",
        type: 'POST',
        data: data,
        success: passwordChangeSuccess,
        error: commonErrorMessage
    });
};

passwordChangeSuccess = function (response) {
    if (response == 'true') {
        $('#profile-update-message').html("Your Password Changed Successfully.");
        setTimeout("$('#profile-update-message').hide();", 3000);
        $('#profile-update-default-view').show();
        $('#profile-update-form').html('');
    } else {
        $("#change-password-form .form-error").html('');
        for (error in response) {
            var id = '#error-' + error;
            $(id).html($(response[error] + "ul li").text());
        }
    }
};

submitPostAdForm = function () {
    console.log("Posting your ad...");
    var data = $('#post-ad-form').serializeArray();

    $.ajax({
        url: "/product/add/",
        type: 'POST',
        data: data,
        success: postAdSuccess,
        error: commonErrorMessage
    });
};

postAdSuccess = function (response) {
    if (response.add == true) {
        window.location = ('/user/' + response.username);
    } else {
        $("#post-ad-form .form-error").html('');
        for (error in response) {
            var id = '#error-' + error;
            $(id).html($(response[error] + "ul li").text());
        }
    }
};

submitSearch = function (){
    console.log("Searching your query...");
    var data = $('#search-box').serializeArray();
    console.log(data);

    $.ajax({
        url: "/search/",
        type: 'POST',
        data: data,
        success: searchResult,
        error: commonErrorMessage
    });
};

searchResult = function(response){
    $("#search-result").html(response);
};

