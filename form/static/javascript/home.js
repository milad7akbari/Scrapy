$(document).ready(function () {
    const $section = $('.mySection');
    const $length = $section.length;
    let $currentIndex = 0;

    $section.eq($currentIndex).removeClass('d-none').addClass('active');
    $('.header .allPage').text($length);
    $('.header .curPage').text($currentIndex + 1);
    updateProgress($currentIndex);

    $(document).on('click', '.btnToggleDropdownMenu', function () {
        $(this).next().toggleClass('d-none');
    });
    $(document).on('click', '.englishLanguageMenu b', function () {
        $('.btnToggleDropdownMenu').text($(this).text());
        $(this).parent().prev().prev().val($(this).data('lang-eng'));
        $('.englishLanguageMenu').toggleClass('d-none');
    });

    $(document).on('click', '.btnNextPrev', function () {
        if ($(this).hasClass('next')) {
            $currentIndex++;
        } else {
            $currentIndex--;
        }
        // let validateFlag = true;
        // validateFlag = validationForm($currentIndex);
        // if (!validateFlag){
        //     $currentIndex -= 1;
        // }
        updateSection($currentIndex);
        updateButtons($currentIndex);
        updateProgress($currentIndex);

    });

    function validationInvestmentForm(){
        var living_budget = $(".living_budget_inp").val();
        if (living_budget.trim() === "") {
            $(".living_budget_inp").addClass("error");
            return message_func("Please enter your budget live.");
        }
        var tuition_fees = $(".tuition_fees_inp").val();
        if (tuition_fees.trim() === "") {
            $(".tuition_fees_inp").addClass("error");
            return message_func("Please enter your tuition fee.");
        }
        var study_setting = $(".study_setting_inp").val();
        if (study_setting.trim() === "") {
            $(".study_setting_inp").addClass("error");
            return message_func("Please enter your rural urban.");
        }
        var current_assets = $(".current_assets_inp").val();
        if (current_assets.trim() === "") {
            $(".current_assets_inp").addClass("error");
            return message_func("Please enter your budget assets.");
        }
        var expected_move_date = $(".expected_move_date_inp").val();
        if (expected_move_date.trim() === "") {
            $(".expected_move_date_inp").addClass("error");
            return message_func("Please enter your start study.");
        }
    }
    function validationEducationForm(){

        var highest_level = $(".highest_level_inp").val();
        if (highest_level.trim() === "") {
            $(".highest_level_inp").addClass("error");
            return message_func("Please enter your highest level.");
        }
        var interested_field = $(".interested_field_inp").val();
        if (interested_field.trim() === "") {
            $(".interested_field_inp").addClass("error");
            return message_func("Please enter your interested field.");
        }
        var english_score = $(".english_score").val();
        if (english_score.trim() === "") {
            $(".english_score").addClass("error");
            return message_func("Please enter your language skill.");
        }
        var year_highest_level = $(".year_highest_level_inp").val();
        if (year_highest_level.trim() === "") {
            $(".year_highest_level_inp").addClass("error");
            return message_func("Please enter your year highest level.");
        }
        return true;

    }
    function validationJobForm(){

        var current_job_inp = $(".current_job_inp").val();
        if (current_job_inp.trim() === "") {
            $(".current_job_inp").addClass("error");
            return message_func("Please enter your current_job.");
        }
        var skill_aspiring_inp = $(".skill_aspiring_inp").val();
        if (skill_aspiring_inp.trim() === "") {
            $(".skill_aspiring_inp").addClass("error");
            return message_func("Please enter your skill_aspiring.");
        }
        var goal_inp = $(".goal_inp").val();
        if (goal_inp.trim() === "") {
            $(".goal_inp").addClass("error");
            return message_func("Please enter your goal.");
        }
        var relevant_experience_inp = $(".relevant_experience_inp").val();
        if (relevant_experience_inp.trim() === "") {
            $(".relevant_experience_inp").addClass("error");
            return message_func("Please enter your year relevant_experience.");
        }

        return true;

    }
    function validationForm(index) {
        $("input").removeClass("error");
        let errFlag = true;
        if (index === 1){
            errFlag = validationPersonalForm();
            if (!errFlag){
                return false;
            }
        }
        if (index === 2){
            errFlag = validationEducationForm();
            if (!errFlag){
                return false;
            }
        }
        if (index === 3){
            errFlag = validationJobForm();
            if (!errFlag){
                return false;
            }
        }
        if (index === 4){
            errFlag = validationInvestmentForm();
            if (!errFlag){
                return false;
            }
        }

        return true;


    }



    function updateSection(index) {
        $section.addClass('d-none').removeClass('active');
        $section.eq(index).removeClass('d-none').addClass('active');
    }

    function updateButtons(index) {
        $('.btnNextPrev.prev').toggleClass('d-none', index === 0);
        $('.btnNextPrev.next').toggleClass('d-none', index === $length - 1);
        $('.btnFinish').toggleClass('d-none', index !== $length - 1);
    }

    function updateProgress(index) {
        const $stepName = $section.eq(index).data('filter-title');
        const width = ((index + 1) / $length) * 100;
        $('#progressBar').animate({
            width: width + '%'
        }, (index === 0) ? 0 : 500); // Animating the width change over 500 milliseconds
        $('.header .curPage').text(index + 1);
        $('#stepName').text($stepName + ' Information');
    }

    function message_func(msg) {
        $('#regForm').append('<div id="tempMessage" class="d-flex position-fixed align-items-center justify-content-center" style="left: 0;width: 350px;bottom: 0;padding: 20px;"><p class="alert alert-danger w-100 p-3 m-0" style="font-size: 15px">' + msg + '</p></div>');
        setTimeout(function () {
            $('#tempMessage').remove();
        }, 250222);
        return false;
    }
});
