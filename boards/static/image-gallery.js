$(document).ready(function() {

    // Get a list of images and their image-preview
    const modals = Array.from(document.getElementsByClassName("image-preview")).map(el => el.getAttribute('data-target'));

    // Set the Max index
    max_index = modals.length -1;

    var index;

    $(this).keydown(function(key) {

        // A key press should remove the previously active Modal
        $(modals[index]).removeClass('is-active');

        if (typeof index == 'undefined')  index = 0; 

        // Handle the key press
        switch(key.which) {
            case 37:
                if(index == 0) index = max_index + 1; index -= 1;
                break;
            case 39:
                if(index == max_index) index = -1; index += 1;
                break;
            default:
                return;
        }

        $(modals[index]).addClass('is-active');
        key.preventDefault();

    });

    // Remove the Model is-active class if the close button is clicked
    $(".modal-close").click(function() {
        $(modals[index]).removeClass('is-active');
    })

    // Clicking the image will display the Modal
    $(".image-preview").click(function() {
        modal = $(this).attr('data-target');
        index = modals.indexOf(modal)
        $(modal).addClass('is-active');
    });

});
