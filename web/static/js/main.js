// Adapted from the jQuery entry on http://css-tricks.com/perfect-full-page-background-image/
$(window).load(function() {    

    var background_map = $("#background_map");
    
    var resize_background_map = function () {
    
        // FIXME - trigger map to resize

    }
    
    theWindow
      .resize( resize_background_map )
      .trigger("resize");
    
});