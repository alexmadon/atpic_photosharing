# http://openlayers.org/dev/examples/dynamic-text-layer.html
# GET /dev/examples/textfile.txt?bbox=-81.685549020767,-55.845699906349,98.314450979233,34.154300093651
# http://openlayers.org/dev/examples/textfile.txt
"""
        <script src="../OpenLayers.js"></script>
        <script type="text/javascript">
            var map;
        
            function init(){
                map = new OpenLayers.Map('map');
                var wms = new OpenLayers.Layer.WMS(
                    "OpenLayers WMS", "http://vmap0.tiles.osgeo.org/wms/vmap0",
                    {layers: 'basic'}
                );

                var layer = new OpenLayers.Layer.Vector("POIs", {
                    strategies: [new OpenLayers.Strategy.BBOX({resFactor: 1.1})],
                    protocol: new OpenLayers.Protocol.HTTP({
                        url: "textfile.txt",
                        format: new OpenLayers.Format.Text()
                    })
                });

                map.addLayers([wms, layer]);
                map.zoomToMaxExtent();

                // Interaction; not needed for initial display.
                selectControl = new OpenLayers.Control.SelectFeature(layer);
                map.addControl(selectControl);
                selectControl.activate();
                layer.events.on({
                    'featureselected': onFeatureSelect,
                    'featureunselected': onFeatureUnselect
                });
            }
             

            // Needed only for interaction, not for the display.
            function onPopupClose(evt) {
                // 'this' is the popup.
                var feature = this.feature;
                if (feature.layer) { // The feature is not destroyed
                    selectControl.unselect(feature);
                } else { // After "moveend" or "refresh" events on POIs layer all 
                         //     features have been destroyed by the Strategy.BBOX
                    this.destroy();
                }
            }
            function onFeatureSelect(evt) {
                feature = evt.feature;
                popup = new OpenLayers.Popup.FramedCloud("featurePopup",
                                         feature.geometry.getBounds().getCenterLonLat(),
                                         new OpenLayers.Size(100,100),
                                         "<h2>"+feature.attributes.title + "</h2>" +
                                         feature.attributes.description,
                                         null, true, onPopupClose);
                feature.popup = popup;
                popup.feature = feature;
                map.addPopup(popup, true);
            }
            function onFeatureUnselect(evt) {
                feature = evt.feature;
                if (feature.popup) {
                    popup.feature = null;
                    map.removePopup(feature.popup);
                    feature.popup.destroy();
                    feature.popup = null;
                }
            }
        </script>
    </head>
    <body onload="init()">
"""
