
function initialize_map_cb() {

    // get the map and make sure it is the same size as the window
    var background_map = $("#background_map");
    var full_window    = $(window)

    background_map.css({
        height: full_window.height() + 'px',
        width:  full_window.width()  + 'px',
        position: 'fixed'
    })

  var myLatlng = new google.maps.LatLng(-34.397, 150.644);

  var map = new google.maps.Map(
      document.getElementById("background_map"),
      {
          zoom: 8,
          center: myLatlng,
          mapTypeId: google.maps.MapTypeId.ROADMAP
      }
  );

  // var resize_background_map = function () {
  // 
  //     // FIXME - trigger map to resize
  // 
  // }
  
  // $(window)
  //   .resize( resize_background_map )
  //   .trigger("resize");
  
}


function load_background_map () {

    // load the map asynchronously
    $(window).load(function() {    
        var script = document.createElement("script");
        script.type = "text/javascript";
        script.src = "http://maps.google.com/maps/api/js?sensor=false&callback=initialize_map_cb";
        document.body.appendChild(script);
    });

}