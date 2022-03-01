$(function() {


    /*************************** + modal windows + *********************/
    // open stars modal
    $( "#btnSearch" ).click(function() {
        //alert($("#q").val());
        //alert($('input[name="type"]:checked').val());

        //alert('/search?q=' + $("#q").val() + '&t=' +$('input[name="type"]:checked').val());
        $('#searchResult').empty();

        // load search results
         $.ajax({
                url: '/search?q=' + $("#q").val() + '&t=' +$('input[name="type"]:checked').val(),
                success: function(data) {
                      Object.keys(data).forEach(function(key) {
                          var listItem = document.createElement('option');
                          listItem.value=key;
                          listItem.innerHTML = key + ' - ' + data[key][6];
                          $('#searchResult').append(listItem);
                       });
                }
         });
    });


    $( "#openStarsModal" ).click(function() {
         $("#starsModal").modal("show");
         $('#starselection').empty();

         // load visible stars
         $.ajax({
                url: '/filter_data?t=*',
                success: function(data) {
                      Object.keys(data).forEach(function(key) {
                          var listItem = document.createElement('option');
                          listItem.value=key;
                          listItem.innerHTML = key + ' - ' + data[key][6];
                          $('#starsselection').append(listItem);
                       });
                }
         });

    });

    // change altitude
    $("#altitudeRangeDeg").change(function(){
        $('#lblAltitudeDeg').text('Altitude (deg): ' + $(this).val());
    });

    // change azimuth
    $("#azimuthRangeDeg").change(function(){
        $('#lblAzimuthDeg').text('Azimuth (deg): ' + $(this).val());
    });

    // change altitude
    $("#altitudeRangeMin").change(function(){
        $('#lblAltitudeMin').text('Altitude (min): ' + $(this).val());
    });

    // change azimuth
    $("#azimuthRangeMin").change(function(){
        $('#lblAzimuthMin').text('Azimuth (min): ' + $(this).val());
    });

    // turn altitude
    $("#changeAltitude").click(function(){
        var alt = parseInt($("#altitudeRangeDeg").val()) * 60 + parseInt($("#altitudeRangeMin").val());
        $.ajax({
            url: '/set_altitude/' + (alt*60),
            success: function(data) { $('#messageBox').html(data['message']); }
        });
    });

    // turn azimuth
    $("#changeAzimuth").click(function(){
        var az = parseInt($("#azimuthRangeDeg").val()) * 60 + parseInt($("#azimuthRangeMin").val());
        $.ajax({
            url: '/set_azimuth/' + (az*60),
            success: function(data) { $('#messageBox').html(data['message']); }
        });
    });

    // set top speed
    $("#changeTopSpeed").click(function(){
        $.ajax({
            url: '/set_top_speed/' + $("#topSpeed").val(),
            success: function(data) { $('#messageBox').html(data['message']); }
        });
    });

    // set bottom speed
    $("#changeBottomSpeed").click(function(){
        $.ajax({
            url: '/set_bottom_speed/' + $("#bottomSpeed").val(),
            success: function(data) { $('#messageBox').html(data['message']); }
        });
    });

    // close stars modal
    $( "#closeStarsModal" ).click(function() {
        $("#starsModal").modal("hide");
    });

    // open MO modal
    $( "#openNGCModal" ).click(function() {
         $("#NGCModal").modal("show");
    });

    // close stars modal
    $( "#closeNGCModal" ).click(function() {
        $("#NGCModal").modal("hide");
    });

    // close preview modal
    $( "#img_preview" ).click(function() {
        $("#previewModal").modal('hide');
    });

    // open search modal
    $( "#openSearchModal" ).click(function() {
        $("#searchModal").modal('show');
    });

    // open degrees modal
    $( "#openDegreesModal" ).click(function() {
        $("#moveDegreesModal").modal('show');
    });

    // open speed modal
    $( "#openSpeedModal" ).click(function() {
        $("#setSpeedModal").modal('show');
    });
    /*************************** - modal windows - *********************/





    /*************************** + locating objects + *********************/
    // locate stars
    $( "#locateStar" ).click(function() {

         $.ajax({
            url: '/locate/' + $( "#starsselection" ).val(),
            success: function(data) { $('#messageBox').html(data['message']); }
        });

    });

    // locate NGCIC
    $( "#locateNGCIC" ).click(function() {

         $.ajax({
            url: '/locate/' + $( "#objectselection" ).val(),
            success: function(data) { $('#messageBox').html(data['message']); }
        });

    });

    // locate obj (from search result)
    $( "#locateObj" ).click(function() {

         $.ajax({
            url: '/locate/' + $( "#searchResult" ).val(),
            success: function(data) { $('#messageBox').html(data['message']); }
        });

    });


    // set initial position
    $( "#lookingAtStar" ).click(function() {

         $.ajax({
            url: '/lookingAt/' + $( "#starsselection" ).val(),
            success: function(data) { $('#messageBox').html(data['message']); }
         });

    });

    $("#startTracking").click(function(){
        $("#stopTracking").toggle();
        $(this).toggle();

        $.ajax({
            url: '/startTracking',
            success: function(data) { $('#messageBox').html(data['message']); }
        });

    });

    $("#stopTracking").click(function(){
        $("#startTracking").toggle();
        $(this).toggle();

        $.ajax({
            url: '/stopTracking',
            success: function(data) { $('#messageBox').html(data['message']); }
        });
    });
    /*************************** - locating objects - *********************/






    /*************************** + camera control + *********************/
    // take single image
    $( "#takePicture" ).click(function() {

         $.ajax({
            url: '/take_picture',
            success: function(data) {
                $('#messageBox').html(data['message']);
                $("#img_preview").attr("src", data['src']);
                $("#previewModal").modal('show');
            }
        });

    });

    // set ISO
    $( ".iso" ).click(function() {

         $.ajax({
            url: '/set_iso/' + $( this ).data('iso'),
            success: function(data) { $('#messageBox').html(data['message']); }
        });

    });


    // set exposure
    $( ".expButton" ).click(function() {

         $.ajax({
            url: '/set_exp/' + $( this ).data('exp'),
            success: function(data) { $('#messageBox').html(data['message']); }
        });

    });
    /*************************** - camera control - *********************/





    /*************************** + telescope control + *********************/
    // manual turn scope (up, down, left, right)
    // $( ".direction" ).click(function() {

    //      $.ajax({
    //         url: '/dir/' + $( this ).data('dir'),
    //         success: function(data) {
    //             $('#messageBox').html(data['message']);
    //         }
    //     });

    // });

    $(document).keydown(function (e) {
        //alert(e.keyCode);
        switch (e.keyCode)
        {
            // left
            case 37:
                $.ajax({
                    url: '/dir/left',
                    success: function(data) { $('#messageBox').html(data['message']); }
                }); break;
            // up
            case 38: 
                $.ajax({
                    url: '/dir/up',
                    success: function(data) { $('#messageBox').html(data['message']); }
                }); break;
            // right
            case 39:
                $.ajax({
                    url: '/dir/right',
                    success: function(data) { $('#messageBox').html(data['message']); }
                }); break;
            // down
            case 40: 
                $.ajax({
                    url: '/dir/down',
                    success: function(data) { $('#messageBox').html(data['message']); }
                }); break;
        }
    });

    $( ".direction" ).mousedown(function() {

        $.ajax({
           url: '/start_turning/' + $( this ).data('dir'),
           success: function(data) { $('#messageBox').html(data['message']); }
       });

   });

    function stop_turning(dir)
    {
        //alert('stop_turning: ' + dir);
        $.ajax({
            url: '/stop_turning/' + dir,
            success: function(data) { $('#messageBox').html(data['message']); }
        });
    }

    $( ".direction" ).mouseup( function() {
        //alert('mouseup');
        setTimeout( stop_turning, 1000, $( this ).data('dir') );
    });

    // set manual steps
    $( ".step" ).click(function() {

         $.ajax({
            url: '/steps/' + $( this ).data('step'),
            success: function(data) { $('#messageBox').html(data['message']); }
        });

    });

    // set initial position
    $( "#resetPosition" ).click(function() {

         $.ajax({
            url: '/resetPosition',
            success: function(data) { $('#messageBox').html(data['message']); }
        });

    });
    /*************************** - telescope control - *********************/





    /*************************** + initialization + *********************/
    // set location data
    $( "#btn_location" ).click(function() {

      // hide button: stop tracking
      $("#stopTracking").toggle();

      if (navigator.geolocation) navigator.geolocation.getCurrentPosition(function(position){
        var d = new Date();
        dt = d.getFullYear() + '-' + (d.getMonth()+1) + '-' + d.getDate() + ' ' + // 2004-02-29
             d.getHours() + ':' + d.getMinutes() + ':' + d.getSeconds(); // 16:21:42

        var lat = position.coords.latitude;
        var lon = position.coords.longitude;

        $.ajax({
            url: '/initialize/' +lat+" "+lon+";"+dt,
            success: function(data) {
                $( '#messageBox' ).html(data['message']);
                $( '#btn_location' ).addClass( 'd-none' );
            }
        });
      });
      else alert("Geolocation is not supported by this browser.");
    });
    /*************************** - initialization - *********************/





    /*************************** + data filtering + *********************/
    $("#typeselection, #constellationselection, #messier").each(function(){
        $( this ).change(function() {
            var t = $('#typeselection').val();
            var c = $('#constellationselection').val();
            var m = $("#messier").is(':checked');

            $('#objectselection').empty();
            /*var x = {'NGC7838':['G', '00:06:53.95', '+08:21:03.1', 'Psc', '', '', ''], 'NGC7839':['**', '00:07:00.63', '+27:38:06.8', 'Peg', '', '', ''], 'NGC7840':['G', '00:07:08.80', '+08:23:00.6', 'Psc', '', '', ''] }
            Object.keys(x).forEach(function(key) {
              var listItem = document.createElement('option');
              listItem.value=key;
              listItem.innerHTML = x[key];
              $('#objectselection').append(listItem);
            });*/

            $.ajax({
                url: '/filter_data?t=' + t + "&c=" + c + "&m=" + m,
                success: function(data) {
                      Object.keys(data).forEach(function(key) {
                          var listItem = document.createElement('option');
                          listItem.value=key;
                          listItem.innerHTML = key + ' - ' + data[key][6];
                          $('#objectselection').append(listItem);
                       });
                }
            });

        });
    });
    /*************************** - data filtering - *********************/





    /*************************** + GUI settings + *********************/
    // toggle gui buttons
    // $('.video_bg').click(function(){
    //     $('#resetPosition').toggle();
    //     $('#setDisplay').toggle();
    //     $('#openStarsModal').toggle();
    //     $('#openNGCModal').toggle();
    //     $('#messageBox').toggle();

    //     $('.top-right').toggle();
    // });

    // display settings - set full screen & landscape mode
    $('#setDisplay').click(function(){
        document.documentElement.requestFullscreen();
        screen.orientation.lock('landscape');
    });

    $('#toggleMenu').click(function(){
        $(".menu").toggle();
    });
    /*************************** - GUI settings - *********************/


});