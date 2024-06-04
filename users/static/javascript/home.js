$(document).ready(function () {
    $(document).on('change', '.marital_status_inp' , function (e) {
        const childContainer = $(this).parents('.mb-3').next();
        if ($(this).val() === '2'){
            childContainer.removeClass('d-none');
        }else{
            childContainer.addClass('d-none');
        }
    });
});
