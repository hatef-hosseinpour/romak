$(document).ready(function () {
    function listOfEnginroom(resp) {
        let selectElement = $('#select-enginroom');
        resp.forEach(function (obj) {
            let option = $('<option>');
            option.val(obj.id).text(obj.enginroom_name)

            selectElement.append(option)
        })
    }
    
});