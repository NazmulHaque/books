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

$(document).ready(function () {
    $('#login-button').click(function (e) {
        e.preventDefault();
        submitLoginPopup();
    });
});

submitLoginPopup = function () {
    console.log('Submitting login popup...');
    var data = $nc('#login-form').serializeArray();
//    data.push({name: 'request_from', value: 'popup'});
    console.log(data);
    $nc.ajax({
        url: '/login',
        type: 'POST',
        data: data,
//        timeout: app.settings.ajax.timeout,
        success: function (response) {
            console.log(response);

            if ($nc.trim(response) == "true") {
                if (app.globals.login_success_redirect_url == '')
                    window.location = '/';
                else
                    window.location = app.globals.login_success_redirect_url;
            } else {
                $nc('#nc-login-popup div.nc-popup-scroll-area').html(response);
                app.hidePopupOverlay();
                app.bindLoginPopup();
            }
        },
        error: function (xhr, status, error) {
            console.error('Ajax status: ' + status);
            console.error('Ajax error: ' + error);
            console.error('Ajax error: ' + xhr.responseText);
            console.log('Something went wrong. Please try again.');
            $nc('#nc-login-popup div.nc-popup-scroll-area').next('p').addClass('nc-left nc-popup-error').html('Something went wrong. Please try again.');
            app.hidePopupOverlay();
        }
    });
}