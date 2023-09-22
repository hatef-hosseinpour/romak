$(document).ready(function () {
    var map = L.map('map').setView([35.6892, 51.3890], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
    }).addTo(map);

    var marker;
    map.on('click', function (e) {
        $('#location-input').val(e.latlng.lat + ',' + e.latlng.lng);
       
        console.log($('#location-input').val());
        $.ajax({
            url: '//', // Add your URL here for the fetch
            type: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val(),
            },
            data: {
                location: e.latlng.lat + ',' + e.latlng.lng
            },
            success: function (response) {
                // Handle success response
                console.log($('#location-input').val());
                $("#map").removeClass("invalid");
            }
        });

        if (marker) {
            map.removeLayer(marker);
        }
        marker = L.marker(e.latlng).addTo(map);
    });

    map.doubleClickZoom.disable();

    // Locate button click event handler
    $('#locate-button').click(function () {
        if ("geolocation" in navigator) {
            navigator.geolocation.getCurrentPosition(function (position) {
                var lat = position.coords.latitude;
                var lng = position.coords.longitude;

                map.setView([lat, lng], 13);
                if (marker) {
                    map.removeLayer(marker);
                }
                marker = L.marker([lat, lng]).addTo(map);

                $('#location-input').val(lat + ',' + lng);
            }, function (error) {
                console.error("Error getting current position:", error.message);
            });
        } else {
            console.error("Geolocation is not available.");
        }
    });
});
