$(document).ready(function () {
    $(document).on('change', '.marital_status_inp' , function (e) {
        const childContainer = $(this).parents('.mb-3').next();
        if ($(this).val() === '2'){
            childContainer.removeClass('d-none');
        }else{
            childContainer.addClass('d-none');
        }
    });
    $('.tab_link .nav-item a').on('click', function(e) {
        e.preventDefault();
        const $id = $(this).attr('id').replace('-tab', '');
        $('.tab_link .nav-item a').removeClass('active');
        $(this).addClass('active');
        $('.profile-tab').addClass('d-none').removeClass('d-block');
        $('#' + $id).removeClass('d-none');
    });
});
