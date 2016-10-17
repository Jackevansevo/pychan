// Show error message if both content and image fields are blank on form submit
$('#reply-form').submit(function() {
    if ($('#id_content').val() === '' && $('#id_image').val() === '') {
        $('#validation-error').show();
        $('#id_content').addClass('is-danger');
        // Prevent the form submission
        return false;
    }
});

// Closes alerts on button click
$('.notification > button').click(function() {
    $(this).parent().hide();
});

// Hide the scroll-to-reply button if current scroll position is at bottom of
// the viewport
$(window).scroll(function() {
    var distanceFromBottom = Math.floor(
        $(document).height() - $(document).scrollTop() - $(window).height()
    );
    if (distanceFromBottom < 300 ) {
        $('a.scroll-to-reply').fadeOut('slow');
    } else {
        $('a.scroll-to-reply').fadeIn('slow');
    }
});


// Scrolls to the reply form on button click
$('#scroll-to-reply').click(function() {
    $('html, body').animate({
        scrollTop: $('#reply-form').offset().top
    }, 800);
    $('#id_content').focus();
});
