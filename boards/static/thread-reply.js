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
        $('#id_content').removeClass('is-danger');
    $(this).parent().hide();
});
