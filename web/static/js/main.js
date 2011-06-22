
function PYC () {
    this.map            = false;
    this.council_ids    = [];
    
    this.init = function () {
        this.resize_background_map();
        this.initialize_map();

        // set the resize cb and trigger it
        var me = this;
        $(window)
          .resize( function () { me.resize_background_map() } );
    }

    // ----------------------
    
    this.resize_background_map = function () {

        var full_window = $(window);
        var background_map = $("#background_map");

        // change the background div to be the size of the window
        background_map.css({
            height: full_window.height() + 'px',
            width:  full_window.width()  + 'px',
        })

        // tell the map we've changed size (if it is set)
        if (this.map)
          google.maps.event.trigger( this.map, 'resize' );
          
    };
    
    
    this.initialize_map = function () {
        var myLatlng = new google.maps.LatLng( 54, -4 );
    
        var options = {
            zoom: 6,
            center: myLatlng,
    
            // use the roadmap as it is probably clearest
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            backgroundColor: '99b3cc',
    
            // try to make the map as static as possible - it is not meant to
            // become a distraction
            disableDefaultUI:       true,
            disableDoubleClickZoom: true,
            draggable:              false,
            keyboardShortcuts:      false,
            scrollwheel:            false
        };
    
        this.map = new google.maps.Map(
            document.getElementById("background_map"),
            options
        );
        
        // if there are councils then show them on the map
        if ( this.council_ids.length ) {
            var id = this.council_ids[0];
            var url = 'http://mapit.mysociety.org/area/' + id + '.kml';

            var kml = new google.maps.KmlLayer(
                url,
                {
                    map: this.map,
                    clickable: false,
                    suppressInfoWindows: true
                }
            );
        }
        
    };

    this.add_council_by_mapit_id = function ( id ) {
        this.council_ids.push( id );
    };


    
};

// set everything up
pyc = new PYC();
$( function() { pyc.init() } );
