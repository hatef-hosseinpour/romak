$(document).ready(function () {
    function listOfEnginroom(resp) {
        let selectElement = $('#select-enginroom');
        resp.forEach(function (obj) {
            let option = $('<option>');
            option.val(obj.id).text(obj.enginroom_name)

            selectElement.append(option)
        })
    }
    $.ajax({
        type: "GET",
        url: "/api/enginroom/",
        success: function (response) {
            listOfEnginroom(response)
        },
        error: function (error) {
            console.error('Error fetcing Enginroom details:', error.reponseJSON);

        }
    });
});