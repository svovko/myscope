$(function() {

    // locate stars
    $( "#locateStar" ).click(function() {

         $.ajax({
            url: '/locate/' + $( "#ids1" ).val(),
            success: function(data) {
                $('#message').html(data['message']);
            }
        });

    });

    // take single image
    $( "#takepicture" ).click(function() {

         $.ajax({
            url: '/take_picture',
            success: function(data) {
                $('#message').html(data['message']);
            }
        });

    });

    // locate DSO
    $( "#locateMO" ).click(function() {

         $.ajax({
            url: '/locate/' + $( "#ids2" ).val(),
            success: function(data) {
                $('#message').html(data['message']);
            }
        });

    });

    // set initial position
    $( "#lookingAtStar" ).click(function() {

         $.ajax({
            url: '/lookingAt/' + $( "#ids1" ).val(),
            success: function(data) {
                $('#message').html(data['message']);
            }
        });

    });

    // manual turn scope
    $( ".direction" ).click(function() {

         $.ajax({
            url: '/dir/' + $( this ).data('dir'),
            success: function(data) {
                $('#message').html(data['message']);
            }
        });

    });

    // set manual steps
    $( ".step" ).click(function() {

         $.ajax({
            url: '/steps/' + $( this ).data('step'),
            success: function(data) {
                $('#message').html(data['message']);
            }
        });

    });

    // set location data
    $( "#btn_location" ).click(function() {
      if (navigator.geolocation) navigator.geolocation.getCurrentPosition(function(position){
        var d = new Date();
        dt = d.getFullYear() + '-' + (d.getMonth()+1) + '-' + d.getDate() + ' ' + // 2004-02-29
             d.getHours() + ':' + d.getMinutes() + ':' + d.getSeconds(); // 16:21:42

        var lat = position.coords.latitude;
        var lon = position.coords.longitude;

        $.ajax({
            url: '/initialize/' +lat+" "+lon+";"+dt,
            success: function(data) {
                $('#message').html(data['message']);
                $( "#btn_location" ).addClass( "d-none" );
                $( ".form-row" ).removeClass("d-none").addClass( "d-block" );
            }
        });
      });
      else alert("Geolocation is not supported by this browser.");
    });
});

function setDisplay()
{
    document.documentElement.requestFullscreen();
    screen.orientation.lock('landscape');
}