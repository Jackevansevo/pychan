modals = [];

$(".image-preview").each(function() {
    modals.push(($(this).attr('data-target')))
})

max_index = modals.length-1;

$(".image-preview").click(function() {

    modal = $(this).attr('data-target');
    index = modals.indexOf(modal)

    $(modal).addClass('is-active');

    $(".modal-close").click(function() {
        $('.modal').removeClass('is-active');
    })

    $(document).keydown(function(key) {

        // Remove all the classes
        $('.modal').removeClass('is-active');

        switch(key.which) {
            case 37:
                if(index ==  0) {
                    index = max_index
                } else {
                    index -= 1
                }
                break;
            case 39:
                if(index ==  max_index) {
                    index = 0
                } else {
                    index += 1
                }
                break;
            default: return; // exit this handler for other keys
        }
        $(modals[index]).addClass('is-active')
        key.preventDefault(); // prevent the default action (scroll / move caret)
    });

})


