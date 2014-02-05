$(function () {
    $('#user-name').click(function (e) {
        e.stopPropagation();
        $('#user-menu').show();
        $(document).click(function (e) {
            if (e.target.id != "user-menu" && !$(e.target).is('li')) {
                $('#user-menu').hide();
                $(document).unbind('click');
            }
        });
    });

    $('#signup-switch-button').click(function (e) {
        console.log('clicking...')
        e.preventDefault();
        $('.login-form-view').hide();
        $('.signup-form-view').show();
    });

    $('#login-switch-button').click(function (e) {
        e.preventDefault();
        $('.signup-form-view').hide();
        $('#signup-form .form-error').html('');
        $('.login-form-view').show();
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

    $("#submit-ad-button").click(function (e) {
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
        beforeSend: function(){
            if ($("#login-form input[name='username']").val() == '' || $("#login-form input[name='password']").val() == ''){
                return false
            }
        },
        success: loginAuthentication,

        error: commonErrorMessage
    });
};

commonErrorMessage = function () {
    console.log("Something went Wrong...")
};

loginAuthentication = function (response) {
    if (response.login == true) {
        window.location = '/user/' + response.username;
    } else {
        $('#login-error').html(response.errors);
        $('#login-error').show();
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
        $('#signup-success-message').html("Thanks for registration. Log in to explore your book.")
        $('.signup-form-view').hide();
        $('.login-form-view').show();
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

submitSearch = function () {
    console.log("Searching your query...");
    var data = $('#search-form').serializeArray();
    console.log(data);

    $.ajax({
        url: "/search-result/",
        type: 'POST',
        data: data,
        success: searchResult,
        error: commonErrorMessage
    });
};

searchResult = function (response) {
    $('#search-result-view').show();
    $('#recent-posts-view').hide();
    $("#search-result").html(response);
    var totalPage = $("#search-result input[name='total']").val();
    console.log(totalPage);

    if (totalPage > 2) {
        var paginator = $('#search-result-view #paginator').pagination({
            items: totalPage,
            itemsOnPage: 2,
            hrefTextPrefix: '#',
            cssStyle: 'light-theme',
            onPageClick: customSearchPagination
        });
    } else {
        $('#search-result-view #paginator').pagination('destroy');
    }

};

customSearchPagination = function () {
    var page = $('#search-result-view #paginator').pagination('getCurrentPage');
    var data = {
        query: $("#search-form input[name='query']").val(),
        page: page,
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
    };
    console.log(data);

    $.ajax({
        url: '/search-result/',
        type: 'POST',
        data: data,

        success: customSearchPaginationResult
    });
};

customSearchPaginationResult = function (response) {
    $("#search-result").html(response);

};

$(function () {
    var totalPage = $("#recent-posts input[name='total']").val();
    console.log(totalPage);
    if (totalPage > 2) {
        $('#recent-posts-view #paginator').pagination({
            items: totalPage,
            itemsOnPage: 2,
            hrefTextPrefix: '#',
            cssStyle: 'light-theme',
            onPageClick: recentSearchPagination
        });
    }
});

recentSearchPagination = function () {
    var page = $('#recent-posts-view #paginator').pagination('getCurrentPage');
    var data = {
        page: page,
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
    };
    console.log(data);

    $.ajax({
        url: '/recent-search/',
        type: 'POST',
        data: data,

        success: recentSearchPaginationResult
    });

};

recentSearchPaginationResult = function (response) {
    $('#recent-posts').html(response);
};
