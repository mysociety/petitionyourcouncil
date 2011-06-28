
function PYC () {
    this.map               = false;
    this.council_ids       = [];
    this.map_bounds        = false;
    this.display_petitions = false;
    this.info_box       = false;

    this.set_map_bounds = function ( n, e, s, w ) {

        var ne = new google.maps.LatLng( n, e );
        var sw = new google.maps.LatLng( s, w );

        this.map_bounds = new google.maps.LatLngBounds( sw, ne );

        return true;
    };

    
    this.init = function () {
        this.resize_background_map();
        this.initialize_map();

        // set the resize cb and trigger it
        var me = this;
        $(window)
          .resize( function () { me.resize_background_map() } );

        if ( this.display_petitions ) {
            this.start_displaying_petitions();
        }
    };

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
        if (this.map) {
            var centre = this.map.getCenter();
            google.maps.event.trigger( this.map, 'resize' );
            this.map.panTo( centre );            
        }
          
    };
    
    
    this.initialize_map = function () {

        var options = {
            zoom: 6,
            center: this.map_bounds.getCenter(),
    
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
        
        this.map.fitBounds( this.map_bounds );
        
        // if there are councils then show them on the map
        for ( var i = 0; i < this.council_ids.length; i++ ) {
            
            var id = this.council_ids[i];

            var url = 'http://mapit.mysociety.org/area/' + id + '.kml';

            var kml = new google.maps.KmlLayer(
                url,
                {
                    map: this.map,
                    clickable: false,
                    suppressInfoWindows: true,
                    preserveViewport: true
                }
            );
        }
        
    };

    this.add_council_by_mapit_id = function ( id ) {
        this.council_ids.push( id );
    };

    this.start_displaying_petitions = function () {

        var self = this;

        var runner = function ( last_id ) {
            $.ajax({
                url: '/petition/next.json',
                data: { 'last_id': last_id },
                success: function ( data, textStatus, jqXHR ) {
                    self.draw_petition( data );
                    setTimeout( function () { runner(data.id); } , 8000 );
                },
                error: function () {
                    if ( this.info_box )
                        this.info_box.close();                    
                },
            });
        };
        
        runner( 0 );        
    };

    this.draw_petition = function (data) {

        if ( this.info_box )
            this.info_box.close();

        var position = new google.maps.LatLng( data.lat, data.lon );

        var heading = $('<strong />').text( data.council );
        var title   = $('<div />').text( data.title );
        var content = $('<div />').append(heading).append(title);

        this.info_box = new InfoBox(
            {
                content: content.html(),
                position: position,
                closeBoxURL: '',         // have no close box
                maxWidth: 300
            }
        );
        
        this.info_box.open( this.map );
    };

};

// set everything up
pyc = new PYC();
$( function() { pyc.init() } );
