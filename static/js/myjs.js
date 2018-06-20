function bind_fold() {
    $('.center-block').click(function () {
        if($(this).siblings('.hidden').hasClass('hidden')){
            $(this).siblings('.hidden').removeClass('hidden');
        }
        else{
            $(this).siblings().addClass('hidden');
        }

    });
};
$(document).ready(function () {
   bind_fold();
});