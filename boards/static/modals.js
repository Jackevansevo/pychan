// Closes the Modal Form when the close button is clicked
$('.delete, .cancel').click(function() {
    $('.modal').removeClass('is-active');
});

// Shows the modal form on button click
$('.show-modal').click(function() {
    var modal = $(this).attr('data-target');
    $(modal).addClass('is-active');
    $(modal).find('input:text').first().focus();
});


// Reshows modal form if any errors are present after submission
$(document).ready(function() {
    if($('.modal-error').length) {
        $('.modal-error').first().closest('.modal').addClass('is-active');
    }
});
