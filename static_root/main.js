$(document).ready(function () {
    console.log('Working main js')
    $('#modal-btn').click(function() {
        $('.ui.modal')
        .modal('show')
        ;
    })
    $('.ui.dropdown').dropdown()
})
